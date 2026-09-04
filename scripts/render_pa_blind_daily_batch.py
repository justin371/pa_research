#!/usr/bin/env python3
"""Render outcome-hidden Daily charts for PA Research visual calibration.

This utility only renders manifest-selected historical windows. It does not rank
symbols, detect patterns, create candidates, or read replay/result artifacts.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import errno
import hashlib
from io import BytesIO, TextIOWrapper
import json
import math
import os
import re
import stat
import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from pa_source_binding import require_source_snapshot, verify_source_snapshot


REQUIRED_COLUMNS = {"Symbol", "Date", "Open", "High", "Low", "Close", "Volume"}
_NEUTRAL_PNG_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.png", re.IGNORECASE | re.ASCII)
_LABEL_HIDDEN_NUMERIC_ID = re.compile(r"(?:EH1|MC2|BH1)-[0-9]{3}", re.ASCII)
_BQ1_VISIBLE_ID = re.compile(r"BQ1-([A-Z]{1,5}(?:\.[A-Z])?)", re.ASCII)
_IDENTITY_HIDDEN_SAMPLE_ID = re.compile(r"(?:EH1|MC2|BH1)-[0-9]{3}", re.ASCII)
_SHA256 = re.compile(r"[0-9a-f]{64}", re.ASCII)
_WINDOWS_DEVICE_NAMES = {"CON", "PRN", "AUX", "NUL"} | {
    f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10)
}


def _positive_integer(value: object, field: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{field} must be a positive integer")
    return value


def _neutral_png_filename(value: object, sample_id: str) -> str:
    # Use one portable namespace, even when rendering on another OS. In Windows
    # a colon can name an NTFS data stream, and devices stay reserved with suffixes.
    if (
        not isinstance(value, str)
        or _NEUTRAL_PNG_NAME.fullmatch(value) is None
        or value.split(".", 1)[0].upper() in _WINDOWS_DEVICE_NAMES
    ):
        raise ValueError(f"{sample_id}: chart_file must be a single neutral PNG filename")
    return value


def _repository_relative_file(repo_root: Path, value: object, field: str) -> Path:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError(f"{field} must be a non-empty repository-relative path")
    # Manifest paths use one portable POSIX-style namespace. This rejects NTFS
    # alternate streams, UNC/device spellings and names that Windows normalizes.
    if "\\" in value or ":" in value:
        raise ValueError(f"{field} must use a portable repository-relative CSV path")
    components = value.split("/")
    if any(
        not component
        or component in {".", ".."}
        or component.endswith((" ", "."))
        or component.split(".", 1)[0].upper() in _WINDOWS_DEVICE_NAMES
        for component in components
    ):
        raise ValueError(f"{field} contains a non-portable path component")
    if not components[-1].lower().endswith(".csv"):
        raise ValueError(f"{field} must identify a CSV file")
    raw_path = Path(*components)
    if raw_path.is_absolute() or raw_path.drive:
        raise ValueError(f"{field} must be repository-relative")
    resolved_root = repo_root.resolve()
    resolved_path = (resolved_root / raw_path).resolve()
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"{field} escapes repo_root") from exc
    if not resolved_path.is_file():
        raise ValueError(f"{field} must identify an existing regular CSV file")
    return resolved_path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class SourceSnapshot:
    path: Path
    data: bytes
    sha256: str


def _opened_handle_path(file_descriptor: int) -> Path | None:
    if os.name == "nt":
        import msvcrt

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        get_final_path = kernel32.GetFinalPathNameByHandleW
        get_final_path.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32]
        get_final_path.restype = ctypes.c_uint32
        handle = msvcrt.get_osfhandle(file_descriptor)
        buffer = ctypes.create_unicode_buffer(32768)
        length = get_final_path(handle, buffer, len(buffer), 0)
        if length == 0 or length >= len(buffer):
            error = ctypes.get_last_error()
            raise OSError(error, ctypes.FormatError(error))
        value = buffer.value
        if value.startswith("\\\\?\\UNC\\"):
            value = "\\\\" + value[8:]
        elif value.startswith("\\\\?\\"):
            value = value[4:]
        return Path(value)
    if sys.platform.startswith("linux"):
        return Path(os.readlink(f"/proc/self/fd/{file_descriptor}"))
    return None


def _read_source_snapshot(repo_root: Path, price_file: Path, field: str) -> SourceSnapshot:
    resolved_root = repo_root.resolve()
    before = price_file.stat(follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f"{field} must identify an existing regular CSV file")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(price_file, flags)
    except OSError as exc:
        raise ValueError(f"{field} could not be opened as a regular file") from exc
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise ValueError(f"{field} changed while it was being opened")
        opened_path = _opened_handle_path(descriptor)
        if opened_path is not None:
            try:
                opened_path.resolve().relative_to(resolved_root)
            except ValueError as exc:
                raise ValueError(f"{field} opened outside repo_root") from exc
        with os.fdopen(descriptor, "rb", closefd=True) as handle:
            descriptor = -1
            data = handle.read()
            after_read = os.fstat(handle.fileno())
        after = price_file.stat(follow_symlinks=False)
        identity = (opened.st_dev, opened.st_ino)
        if (
            (after_read.st_dev, after_read.st_ino) != identity
            or (after.st_dev, after.st_ino) != identity
            or after_read.st_size != len(data)
        ):
            raise ValueError(f"{field} changed while it was being read")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return SourceSnapshot(price_file, data, hashlib.sha256(data).hexdigest())


def _text_reader(source: Path | SourceSnapshot):
    if isinstance(source, SourceSnapshot):
        return TextIOWrapper(BytesIO(source.data), encoding="utf-8-sig", newline="")
    return source.open("r", encoding="utf-8-sig", newline="")


def _source_label(source: Path | SourceSnapshot) -> Path:
    return source.path if isinstance(source, SourceSnapshot) else source


def _canonical_decimal(value: str, field: str) -> str:
    try:
        number = Decimal(value.strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError(f"{field} must be a decimal number") from exc
    if not number.is_finite():
        raise ValueError(f"{field} must be finite")
    return format(number.normalize(), "f")


def source_window_fingerprint(price_file: Path | SourceSnapshot, symbol: str, cutoff: date, window_size: int) -> tuple[int, str]:
    rows: list[tuple[date, str]] = []
    label = _source_label(price_file)
    with _text_reader(price_file) as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError(f"{label}: missing required OHLCV columns")
        for row_number, row in enumerate(reader, start=2):
            if row["Symbol"].strip().upper() != symbol:
                continue
            session_date = date.fromisoformat(row["Date"])
            if session_date > cutoff:
                continue
            normalized = "|".join(
                [
                    session_date.isoformat(),
                    *(
                        _canonical_decimal(row[field], f"{label}:{row_number}:{field}")
                        for field in ("Open", "High", "Low", "Close", "Volume")
                    ),
                ]
            )
            rows.append((session_date, normalized))
    rows.sort(key=lambda item: item[0])
    visible = rows[-window_size:]
    payload = "\n".join(normalized for _, normalized in visible).encode("utf-8")
    return len(visible), hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class DailyBar:
    symbol: str
    session_date: date
    open: float
    high: float
    low: float
    close: float
    volume: float


def _finite_float(value: str, field: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} must be finite")
    return number


def load_symbol_bars(price_file: Path | SourceSnapshot, symbol: str) -> list[DailyBar]:
    label = _source_label(price_file)
    with _text_reader(price_file) as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{label}: missing columns {sorted(missing)}")
        bars = []
        for row in reader:
            if row["Symbol"].strip().upper() != symbol.upper():
                continue
            bar = DailyBar(
                symbol=symbol.upper(),
                session_date=date.fromisoformat(row["Date"]),
                open=_finite_float(row["Open"], "Open"),
                high=_finite_float(row["High"], "High"),
                low=_finite_float(row["Low"], "Low"),
                close=_finite_float(row["Close"], "Close"),
                volume=_finite_float(row["Volume"], "Volume"),
            )
            if (
                min(bar.open, bar.high, bar.low, bar.close) <= 0
                or bar.volume < 0
                or bar.high < max(bar.open, bar.close)
                or bar.low > min(bar.open, bar.close)
            ):
                raise ValueError(f"{symbol} {bar.session_date}: invalid OHLCV row")
            bars.append(bar)
    bars.sort(key=lambda bar: bar.session_date)
    if not bars:
        raise ValueError(f"{label}: symbol {symbol} has no rows")
    if len({bar.session_date for bar in bars}) != len(bars):
        raise ValueError(f"{label}: symbol {symbol} has duplicate dates")
    return bars


def _approved_label_hidden_id(sample_id: object, symbol: str, identity_hidden: bool) -> bool:
    if not isinstance(sample_id, str):
        return False
    if _LABEL_HIDDEN_NUMERIC_ID.fullmatch(sample_id) is not None:
        return True
    match = _BQ1_VISIBLE_ID.fullmatch(sample_id)
    return not identity_hidden and match is not None and match.group(1) == symbol


def _publish_directory_no_replace(staging_root: Path, output_dir: Path) -> None:
    source = str(staging_root)
    destination = str(output_dir)
    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        move_file = kernel32.MoveFileW
        move_file.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
        move_file.restype = ctypes.c_int
        if not move_file(source, destination):
            error = ctypes.get_last_error()
            if error in {80, 183}:
                raise FileExistsError(error, ctypes.FormatError(error), destination)
            raise OSError(error, ctypes.FormatError(error), destination)
        return
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform.startswith("linux"):
        rename_no_replace = getattr(libc, "renameat2", None)
        if rename_no_replace is None:
            raise OSError(errno.ENOTSUP, "atomic no-replace directory publication is unavailable")
        rename_no_replace.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        rename_no_replace.restype = ctypes.c_int
        result = rename_no_replace(-100, os.fsencode(source), -100, os.fsencode(destination), 1)
    elif sys.platform == "darwin":
        rename_no_replace = getattr(libc, "renamex_np", None)
        if rename_no_replace is None:
            raise OSError(errno.ENOTSUP, "atomic no-replace directory publication is unavailable")
        rename_no_replace.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        rename_no_replace.restype = ctypes.c_int
        result = rename_no_replace(os.fsencode(source), os.fsencode(destination), 0x00000004)
    else:
        raise OSError(errno.ENOTSUP, "atomic no-replace directory publication is unavailable")
    if result != 0:
        error = ctypes.get_errno()
        if error in {errno.EEXIST, errno.ENOTEMPTY}:
            raise FileExistsError(error, os.strerror(error), destination)
        raise OSError(error, os.strerror(error), destination)


def ema(values: Sequence[float], period: int) -> list[float]:
    if period <= 0:
        raise ValueError("EMA period must be positive")
    if not values:
        return []
    alpha = 2.0 / (period + 1.0)
    result = [float(values[0])]
    for value in values[1:]:
        result.append(alpha * float(value) + (1.0 - alpha) * result[-1])
    return result


def deterministic_index(symbol: str, row_count: int, seed: str, minimum_context: int, minimum_future: int) -> int:
    _positive_integer(row_count, "row_count")
    _positive_integer(minimum_context, "minimum_context_bars")
    _positive_integer(minimum_future, "minimum_hidden_future_bars")
    span = row_count - minimum_context - minimum_future + 1
    if span <= 0:
        raise ValueError(f"{symbol}: insufficient rows for deterministic blind selection")
    digest = hashlib.sha256(f"{seed}|{symbol}".encode("utf-8")).digest()
    value = int.from_bytes(digest[:4], byteorder="little", signed=False)
    return minimum_context - 1 + value % span


def explicit_cutoff_index(bars: Sequence[DailyBar], cutoff_date: str) -> int:
    matches = [index for index, bar in enumerate(bars) if bar.session_date.isoformat() == cutoff_date]
    if len(matches) != 1:
        raise ValueError(f"explicit cutoff {cutoff_date} must match exactly one completed Daily bar")
    return matches[0]


def _set_date_ticks(axis: plt.Axes, bars: Sequence[DailyBar], maximum: int = 9) -> None:
    if not bars:
        return
    count = min(maximum, len(bars))
    positions = sorted({round(index * (len(bars) - 1) / max(1, count - 1)) for index in range(count)})
    axis.set_xticks(positions)
    axis.set_xticklabels([bars[index].session_date.isoformat() for index in positions], rotation=30, ha="right")


def _relative_tick_spec(bars: Sequence[DailyBar], maximum: int = 9) -> tuple[list[int], list[str]]:
    """Return identity-neutral bar offsets ending at T0."""
    if not bars:
        return [], []
    count = min(maximum, len(bars))
    positions = sorted({round(index * (len(bars) - 1) / max(1, count - 1)) for index in range(count)})
    labels = ["T0" if index == len(bars) - 1 else f"T-{len(bars) - 1 - index}" for index in positions]
    return positions, labels


def _set_relative_ticks(axis: plt.Axes, bars: Sequence[DailyBar], maximum: int = 9) -> None:
    positions, labels = _relative_tick_spec(bars, maximum)
    axis.set_xticks(positions)
    axis.set_xticklabels(labels, rotation=0, ha="center")


def _chart_title(
    sample_id: str,
    last_bar: DailyBar,
    daily_count: int,
    local_count: int,
    identity_hidden: bool,
) -> str:
    if identity_hidden:
        heading = f"{sample_id} | historical Daily | identity and calendar date hidden | outcome hidden"
    else:
        heading = (
            f"{sample_id} | {last_bar.symbol} | historical Daily cutoff "
            f"{last_bar.session_date.isoformat()} | outcome hidden"
        )
    return f"{heading}\nTop: last {daily_count} completed Daily bars; Bottom: last {local_count} completed Daily bars"


def _plot_price(axis: plt.Axes, bars: Sequence[DailyBar], ema_series: dict[int, Sequence[float]]) -> None:
    body_width = 0.66
    for index, bar in enumerate(bars):
        rising = bar.close >= bar.open
        color = "#17823b" if rising else "#c23b3b"
        axis.vlines(index, bar.low, bar.high, color=color, linewidth=0.65, alpha=0.9)
        bottom = min(bar.open, bar.close)
        height = max(abs(bar.close - bar.open), max(abs(bar.close), 1.0) * 0.00025)
        axis.add_patch(
            Rectangle(
                (index - body_width / 2.0, bottom),
                body_width,
                height,
                facecolor=color,
                edgecolor=color,
                linewidth=0.45,
                alpha=0.9,
            )
        )
    colors = {20: "#1f77b4", 50: "#ff8c00", 200: "#6a3d9a"}
    for period, values in ema_series.items():
        axis.plot(range(len(bars)), values, color=colors[period], linewidth=1.0, label=f"EMA{period}")
    axis.grid(True, alpha=0.16)
    axis.legend(loc="upper left", ncol=3, fontsize=8, frameon=False)
    axis.set_ylabel("Price")


def _plot_volume(axis: plt.Axes, bars: Sequence[DailyBar]) -> None:
    colors = ["#17823b" if bar.close >= bar.open else "#c23b3b" for bar in bars]
    axis.bar(range(len(bars)), [bar.volume for bar in bars], color=colors, width=0.68, alpha=0.55)
    axis.grid(True, alpha=0.12)
    axis.set_ylabel("Volume")
    axis.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))


def render_sample(
    bars: Sequence[DailyBar],
    cutoff_index: int,
    sample_id: str,
    output_file: Path,
    daily_window: int,
    local_window: int,
    identity_hidden: bool = False,
) -> None:
    _neutral_png_filename(output_file.name, sample_id)
    if type(cutoff_index) is not int or not 0 <= cutoff_index < len(bars):
        raise ValueError("cutoff_index must select an existing completed bar")
    _positive_integer(daily_window, "daily_chart_bars")
    _positive_integer(local_window, "local_chart_bars")
    if local_window > daily_window:
        raise ValueError("local_chart_bars must not exceed daily_chart_bars")
    if output_file.exists() or output_file.is_symlink():
        raise FileExistsError(f"refusing to overwrite chart: {output_file}; use a new output directory")
    context = list(bars[: cutoff_index + 1])
    closes = [bar.close for bar in context]
    full_emas = {period: ema(closes, period) for period in (20, 50, 200)}

    daily_start = max(0, len(context) - daily_window)
    local_start = max(0, len(context) - local_window)
    daily_bars = context[daily_start:]
    local_bars = context[local_start:]
    daily_emas = {period: values[daily_start:] for period, values in full_emas.items()}
    local_emas = {period: values[local_start:] for period, values in full_emas.items()}

    # Reserve space for both date/relative ticks and the context xlabel before
    # the local panel. Applies only to new renders; frozen PNGs are unchanged.
    figure = plt.figure(figsize=(18, 11), dpi=140, layout="constrained")
    grid = figure.add_gridspec(4, 1, height_ratios=(3.8, 0.9, 3.8, 0.9), hspace=0.08)
    daily_price = figure.add_subplot(grid[0, 0])
    daily_volume = figure.add_subplot(grid[1, 0], sharex=daily_price)
    local_price = figure.add_subplot(grid[2, 0])
    local_volume = figure.add_subplot(grid[3, 0], sharex=local_price)

    _plot_price(daily_price, daily_bars, daily_emas)
    _plot_volume(daily_volume, daily_bars)
    _plot_price(local_price, local_bars, local_emas)
    _plot_volume(local_volume, local_bars)

    daily_price.set_title(
        _chart_title(sample_id, context[-1], len(daily_bars), len(local_bars), identity_hidden),
        fontsize=12,
    )
    plt.setp(daily_price.get_xticklabels(), visible=False)
    plt.setp(local_price.get_xticklabels(), visible=False)
    if identity_hidden:
        _set_relative_ticks(daily_volume, daily_bars)
        _set_relative_ticks(local_volume, local_bars)
        daily_volume.set_xlabel("Completed Daily bars relative to cutoff (T0); calendar dates hidden")
        local_volume.set_xlabel("Local detail relative to T0; identity, dates, pattern and outcome hidden")
    else:
        _set_date_ticks(daily_volume, daily_bars)
        _set_date_ticks(local_volume, local_bars)
        daily_volume.set_xlabel("Historical completed Daily bars only")
        local_volume.set_xlabel("Local detail; no pattern, entry, stop, target, or result annotation")

    # Finish encoding before touching the destination. Exclusive creation also
    # protects a file that appeared after preflight; frozen charts are immutable.
    try:
        with BytesIO() as buffer:
            figure.savefig(buffer, format="png", bbox_inches="tight")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with output_file.open("xb") as handle:
                handle.write(buffer.getvalue())
    finally:
        plt.close(figure)


def render_manifest(manifest_path: Path, repo_root: Path, output_dir: Path) -> list[Path]:
    repo_root = repo_root.resolve()
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError(f"refusing to reuse output directory: {output_dir}; use a new output directory")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("label_hidden") is not True or manifest.get("outcome_hidden") is not True:
        raise ValueError("blind manifest must set label_hidden and outcome_hidden to true")
    selection_mode = manifest.get("selection_mode", "deterministic_cutoff")
    if selection_mode not in {"deterministic_cutoff", "explicit_cutoff"}:
        raise ValueError(f"unsupported selection_mode: {selection_mode}")
    seed = manifest.get("selection_seed")
    if selection_mode == "deterministic_cutoff" and (not isinstance(seed, str) or not seed.strip()):
        raise ValueError("selection_seed must be a non-empty string for deterministic_cutoff")
    minimum_context = _positive_integer(manifest["minimum_context_bars"], "minimum_context_bars")
    minimum_future = _positive_integer(manifest["minimum_hidden_future_bars"], "minimum_hidden_future_bars")
    daily_window = _positive_integer(manifest.get("daily_chart_bars", 504), "daily_chart_bars")
    local_window = _positive_integer(manifest.get("local_chart_bars", 120), "local_chart_bars")
    if local_window > daily_window:
        raise ValueError("local_chart_bars must not exceed daily_chart_bars")
    identity_hidden = manifest.get("identity_hidden", False)
    if not isinstance(identity_hidden, bool):
        raise ValueError("identity_hidden must be boolean")
    source_binding_required = manifest.get("source_binding_required", False)
    if not isinstance(source_binding_required, bool):
        raise ValueError("source_binding_required must be boolean")
    renderer_source_snapshot = None
    if source_binding_required:
        renderer_source_path = Path(__file__).resolve(strict=True)
        renderer_source_snapshot = require_source_snapshot(
            sys.modules.get(__name__),
            globals(),
            renderer_source_path,
            "renderer source",
        )
        expected_renderer_sha256 = manifest.get("renderer_source_sha256")
        if not isinstance(expected_renderer_sha256, str) or _SHA256.fullmatch(expected_renderer_sha256) is None:
            raise ValueError("renderer_source_sha256 must be a lowercase SHA-256 digest")
        if renderer_source_snapshot.sha256 != expected_renderer_sha256:
            raise ValueError("renderer_source_sha256 does not match the current renderer")
    seen_ids = set()
    seen_chart_files = set()
    seen_evidence = set()
    source_snapshots: dict[Path, SourceSnapshot] = {}
    plans = []
    samples = manifest.get("samples")
    if not isinstance(samples, list) or not samples:
        raise ValueError("samples must be a non-empty list")

    # Preflight all evidence identities before creating any image. Renaming a
    # sample or copying the CSV cannot make the same symbol/cutoff independent.
    for sample in samples:
        evidence_key = (sample["symbol"].strip().upper(), date.fromisoformat(sample["cutoff_date"]))
        if evidence_key in seen_evidence:
            raise ValueError(f"duplicate symbol/cutoff evidence: {evidence_key}")
        seen_evidence.add(evidence_key)

    # Validate every sample, source boundary and destination before the first
    # render. A malformed late row must not produce an apparently usable prefix.
    for sample in samples:
        sample_id = sample["sample_id"]
        if sample_id in seen_ids:
            raise ValueError(f"duplicate sample_id: {sample_id}")
        seen_ids.add(sample_id)
        chart_file = Path(_neutral_png_filename(sample["chart_file"], sample_id))
        symbol = sample["symbol"].strip().upper()
        if (
            not _approved_label_hidden_id(sample_id, symbol, identity_hidden)
            or chart_file.name != f"{sample_id}.png"
        ):
            raise ValueError(
                "label_hidden samples must use an approved neutral ID namespace "
                "and an exactly matching PNG filename"
            )
        if identity_hidden and _IDENTITY_HIDDEN_SAMPLE_ID.fullmatch(sample_id) is None:
            raise ValueError("identity_hidden samples must use an approved numeric identity-hidden ID namespace")
        if chart_file.name.casefold() in seen_chart_files:
            raise ValueError(f"duplicate chart_file: {chart_file.name}")
        seen_chart_files.add(chart_file.name.casefold())
        price_file = _repository_relative_file(repo_root, sample.get("price_file"), f"{sample_id}: price_file")
        snapshot = source_snapshots.get(price_file)
        if snapshot is None:
            snapshot = _read_source_snapshot(repo_root, price_file, f"{sample_id}: price_file")
            source_snapshots[price_file] = snapshot
        if source_binding_required:
            expected_source_sha256 = sample.get("source_file_sha256")
            expected_window_sha256 = sample.get("source_window_sha256")
            expected_window_rows = sample.get("source_window_rows")
            if not isinstance(expected_source_sha256, str) or _SHA256.fullmatch(expected_source_sha256) is None:
                raise ValueError(f"{sample_id}: source_file_sha256 must be a lowercase SHA-256 digest")
            if not isinstance(expected_window_sha256, str) or _SHA256.fullmatch(expected_window_sha256) is None:
                raise ValueError(f"{sample_id}: source_window_sha256 must be a lowercase SHA-256 digest")
            expected_window_rows = _positive_integer(expected_window_rows, f"{sample_id}: source_window_rows")
            if snapshot.sha256 != expected_source_sha256:
                raise ValueError(f"{sample_id}: source_file_sha256 does not match price_file")
            actual_rows, actual_window_sha256 = source_window_fingerprint(
                snapshot, symbol, date.fromisoformat(sample["cutoff_date"]), daily_window
            )
            if actual_rows != expected_window_rows or actual_window_sha256 != expected_window_sha256:
                raise ValueError(f"{sample_id}: frozen source window binding does not match price_file")
        bars = load_symbol_bars(snapshot, symbol)
        if selection_mode == "deterministic_cutoff":
            cutoff_index = deterministic_index(symbol, len(bars), seed, minimum_context, minimum_future)
            expected_cutoff = bars[cutoff_index].session_date.isoformat()
            if sample["cutoff_date"] != expected_cutoff:
                raise ValueError(
                    f"{sample_id}: cutoff {sample['cutoff_date']} does not match deterministic selection {expected_cutoff}"
                )
        else:
            cutoff_index = explicit_cutoff_index(bars, sample["cutoff_date"])
        if cutoff_index + 1 < minimum_context or len(bars) - cutoff_index - 1 < minimum_future:
            raise ValueError(f"{sample_id}: context/future boundary failed")
        plans.append((bars, cutoff_index, sample_id, chart_file.name))

    # Encode the entire batch in a sibling directory on the destination volume.
    # One platform-native atomic no-replace operation publishes it; no partial
    # final prefix is exposed and no per-file rollback can delete foreign data.
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".pa-blind-render-", dir=output_dir.parent) as staging_directory:
        staging_root = Path(staging_directory)
        for bars, cutoff_index, display_id, chart_name in plans:
            staged_file = staging_root / chart_name
            render_sample(
                bars,
                cutoff_index,
                display_id,
                staged_file,
                daily_window,
                local_window,
                identity_hidden=identity_hidden,
            )
        if renderer_source_snapshot is not None:
            verify_source_snapshot(renderer_source_snapshot, "renderer source")
        _publish_directory_no_replace(staging_root, output_dir)
    return [output_dir / chart_name for _, _, _, chart_name in plans]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    outputs = render_manifest(args.manifest.resolve(), args.repo_root.resolve(), args.output_dir.resolve())
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

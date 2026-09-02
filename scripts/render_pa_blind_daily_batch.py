#!/usr/bin/env python3
"""Render outcome-hidden Daily charts for PA Research visual calibration.

This utility only renders manifest-selected historical windows. It does not rank
symbols, detect patterns, create candidates, or read replay/result artifacts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


REQUIRED_COLUMNS = {"Symbol", "Date", "Open", "High", "Low", "Close", "Volume"}


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


def load_symbol_bars(price_file: Path, symbol: str) -> list[DailyBar]:
    with price_file.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{price_file}: missing columns {sorted(missing)}")
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
        raise ValueError(f"{price_file}: symbol {symbol} has no rows")
    if len({bar.session_date for bar in bars}) != len(bars):
        raise ValueError(f"{price_file}: symbol {symbol} has duplicate dates")
    return bars


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

    output_file.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_file, bbox_inches="tight")
    plt.close(figure)


def render_manifest(manifest_path: Path, repo_root: Path, output_dir: Path) -> list[Path]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("label_hidden") is not True or manifest.get("outcome_hidden") is not True:
        raise ValueError("blind manifest must set label_hidden and outcome_hidden to true")
    selection_mode = manifest.get("selection_mode", "deterministic_cutoff")
    if selection_mode not in {"deterministic_cutoff", "explicit_cutoff"}:
        raise ValueError(f"unsupported selection_mode: {selection_mode}")
    seed = manifest.get("selection_seed")
    if selection_mode == "deterministic_cutoff" and not seed:
        raise ValueError("deterministic_cutoff requires selection_seed")
    minimum_context = int(manifest["minimum_context_bars"])
    minimum_future = int(manifest["minimum_hidden_future_bars"])
    daily_window = int(manifest.get("daily_chart_bars", 504))
    local_window = int(manifest.get("local_chart_bars", 120))
    identity_hidden = manifest.get("identity_hidden", False)
    if not isinstance(identity_hidden, bool):
        raise ValueError("identity_hidden must be boolean")
    outputs = []
    seen_ids = set()
    seen_chart_files = set()

    for sample in manifest["samples"]:
        sample_id = sample["sample_id"]
        if sample_id in seen_ids:
            raise ValueError(f"duplicate sample_id: {sample_id}")
        seen_ids.add(sample_id)
        chart_file = Path(sample["chart_file"])
        if chart_file.name != sample["chart_file"] or chart_file.suffix.lower() != ".png":
            raise ValueError(f"{sample_id}: chart_file must be a single neutral PNG filename")
        if chart_file.name in seen_chart_files:
            raise ValueError(f"duplicate chart_file: {chart_file.name}")
        seen_chart_files.add(chart_file.name)
        symbol = sample["symbol"].upper()
        price_file = (repo_root / sample["price_file"]).resolve()
        bars = load_symbol_bars(price_file, symbol)
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
        output_file = output_dir / chart_file.name
        render_sample(
            bars,
            cutoff_index,
            sample_id,
            output_file,
            daily_window,
            local_window,
            identity_hidden=identity_hidden,
        )
        outputs.append(output_file)
    return outputs


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

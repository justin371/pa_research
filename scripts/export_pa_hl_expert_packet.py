#!/usr/bin/env python3
"""Export the frozen H/L allowlist for integrity checks, not human-handoff approval."""

from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
from typing import Any


PACKET_RELATIVE = Path("research/calibration/external_human_hl_v1")
EXPECTED_MANIFEST_SHA256 = "d1616e568bceebbe605d498548ffc5c346cec1365831ba9035ab131ad9765b23"
DOCUMENT_ALLOWLIST = (
    "README.md",
    "expert_criteria_CN.md",
    "annotation_form.md",
    "annotation_schema_v1.json",
    "manifest.json",
)
INTERNAL_HASH_FILE = "neutral_chart_sha256.json"
FROZEN_DOCUMENT_HASHES = {
    "README.md": "599285a806674e0984bdb43a5a9d041f4e4b7d097af3b0235a2f12813f719995",
    "expert_criteria_CN.md": "d5626e0b97ecfc0bb1fb97541f178f9b0d129ea6fb9231817ae4db7ea22039d4",
    "annotation_form.md": "333aced39b8dc0547118d983d6dae48cbb3aac97a63eb7ae69dca07c37582ccd",
    "annotation_schema_v1.json": "7cd0d7f07308af4bde06f9e0139edb30663f8c26e790fb12d2096cf6a87dbdbd",
    "manifest.json": EXPECTED_MANIFEST_SHA256,
}
FROZEN_CHART_INVENTORY_SHA256 = "f41c29f3c6f88e2d2b6c5beda468b5b0f913ac2fa11e087d7b30bbe024cf3d8a"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _publish_directory_no_replace(staging_root: Path, output_dir: Path) -> None:
    """Atomically publish the complete allowlist without replacing anything."""

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


def frozen_file_hashes(packet_root: Path) -> dict[str, str]:
    inventory_bytes = (packet_root / INTERNAL_HASH_FILE).read_bytes()
    if hashlib.sha256(inventory_bytes).hexdigest() != FROZEN_CHART_INVENTORY_SHA256:
        raise ValueError("chart inventory does not match its independently frozen hash")
    inventory = json.loads(inventory_bytes.decode("utf-8"))
    return {
        **FROZEN_DOCUMENT_HASHES,
        **{f"charts/{row['expert_sample_id']}.png": row["chart_sha256"] for row in inventory["charts"]},
    }


def build_allowlist(repo_root: Path) -> tuple[Path, list[tuple[Path, Path]]]:
    packet_root = (repo_root / PACKET_RELATIVE).resolve()
    manifest_path = packet_root / "manifest.json"
    if sha256_file(manifest_path) != EXPECTED_MANIFEST_SHA256:
        raise ValueError("manifest hash does not match the frozen identity-neutral packet")
    manifest = load_json(manifest_path)
    if manifest.get("identity_hidden") is not True or manifest.get("calendar_dates_hidden") is not True:
        raise ValueError("manifest must freeze identity_hidden and calendar_dates_hidden")
    samples = manifest.get("samples")
    if not isinstance(samples, list) or len(samples) != 16 or manifest.get("sample_count") != 16:
        raise ValueError("manifest must contain exactly 16 samples")

    frozen_hashes = frozen_file_hashes(packet_root)
    hash_manifest = load_json(packet_root / INTERNAL_HASH_FILE)
    expected_hashes = {
        row["expert_sample_id"]: row["chart_sha256"] for row in hash_manifest.get("charts", [])
    }
    if hash_manifest.get("chart_count") != 16 or len(expected_hashes) != 16:
        raise ValueError("neutral chart hash inventory must contain exactly 16 rows")

    copies = [(packet_root / name, Path(name)) for name in DOCUMENT_ALLOWLIST]
    seen_ids: set[str] = set()
    for index, sample in enumerate(samples, start=1):
        sample_id = f"EH1-{index:03d}"
        if sample.get("expert_sample_id") != sample_id or sample_id in seen_ids:
            raise ValueError("manifest sample IDs must be unique and ordered EH1-001 through EH1-016")
        seen_ids.add(sample_id)
        relative_chart = Path(sample.get("chart_path", ""))
        if relative_chart != Path("charts") / f"{sample_id}.png":
            raise ValueError(f"{sample_id}: chart path is not packet-relative and identity-neutral")
        chart = packet_root / relative_chart
        if not chart.is_file() or sha256_file(chart) != expected_hashes.get(sample_id):
            raise ValueError(f"{sample_id}: chart is missing or its frozen hash does not match")
        copies.append((chart, relative_chart))

    if len(copies) != 21 or len({destination.as_posix() for _, destination in copies}) != 21:
        raise ValueError("expert allowlist must contain exactly 21 unique files")
    for source, destination in copies:
        if not source.is_file():
            raise ValueError(f"allowlisted source file is missing: {source}")
        if sha256_file(source) != frozen_hashes[destination.as_posix()]:
            raise ValueError(f"{destination}: content does not match its frozen hash")
    return packet_root, copies


def export_packet(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    packet_root, copies = build_allowlist(repo_root.resolve())
    frozen_hashes = frozen_file_hashes(packet_root)
    destination_root = output_dir.resolve()
    if destination_root == packet_root or packet_root in destination_root.parents:
        raise ValueError("output directory must not be inside the frozen source packet")
    if destination_root.exists() or destination_root.is_symlink():
        raise FileExistsError(f"output directory must not exist: {destination_root}")
    destination_root.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".pa-expert-packet-", dir=destination_root.parent) as staging_directory:
        staging_root = Path(staging_directory)
        for source, relative_destination in copies:
            destination = staging_root / relative_destination
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        exported = sorted(path.relative_to(staging_root).as_posix() for path in staging_root.rglob("*") if path.is_file())
        expected = sorted(relative.as_posix() for _, relative in copies)
        if exported != expected:
            raise RuntimeError("exported files do not exactly match the closed allowlist")
        for relative in exported:
            if sha256_file(staging_root / relative) != frozen_hashes[relative]:
                raise RuntimeError(f"{relative}: exported bytes do not match the frozen hash")
        _publish_directory_no_replace(staging_root, destination_root)
    return {
        # Byte integrity cannot establish blindness or pre-reveal commitment.
        # This frozen v1 packet includes overlapping same-instrument cutoffs.
        "status": "integrity_verified_handoff_blocked",
        "integrity_verified": True,
        "human_handoff_ready": False,
        "accuracy_study_ready": False,
        "handoff_blockers": [
            "independent_pre_reveal_commitment",
            "cross_sample_future_exposure",
        ],
        "source_packet": str(packet_root),
        "output_dir": str(destination_root),
        "file_count": len(exported),
        "document_count": len(DOCUMENT_ALLOWLIST),
        "chart_count": 16,
        "manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "chart_inventory_sha256": FROZEN_CHART_INVENTORY_SHA256,
        "exported_file_sha256": frozen_hashes,
        "real_annotations_included": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = export_packet(args.repo_root, args.output_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0  # Successful integrity export, never authorization to contact experts.


if __name__ == "__main__":
    sys.exit(main())

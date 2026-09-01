#!/usr/bin/env python3
"""Export only the identity-neutral external-human H/L packet allowlist."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
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


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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
    for source, _ in copies:
        if not source.is_file():
            raise ValueError(f"allowlisted source file is missing: {source}")
    return packet_root, copies


def export_packet(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    packet_root, copies = build_allowlist(repo_root.resolve())
    destination_root = output_dir.resolve()
    if destination_root.exists() and any(destination_root.iterdir()):
        raise FileExistsError(f"output directory must be absent or empty: {destination_root}")
    destination_root.mkdir(parents=True, exist_ok=True)
    for source, relative_destination in copies:
        destination = destination_root / relative_destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    exported = sorted(path.relative_to(destination_root).as_posix() for path in destination_root.rglob("*") if path.is_file())
    expected = sorted(relative.as_posix() for _, relative in copies)
    if exported != expected:
        raise RuntimeError("exported files do not exactly match the closed allowlist")
    return {
        "status": "ready_for_isolated_human_handoff",
        "source_packet": str(packet_root),
        "output_dir": str(destination_root),
        "file_count": len(exported),
        "document_count": len(DOCUMENT_ALLOWLIST),
        "chart_count": 16,
        "manifest_sha256": EXPECTED_MANIFEST_SHA256,
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
    return 0


if __name__ == "__main__":
    sys.exit(main())

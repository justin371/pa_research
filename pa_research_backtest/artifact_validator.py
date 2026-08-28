"""Read-only validation for PA Research replay artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

from .engine import ENGINE_VERSION, build_summary


CURRENT_METADATA_FIELDS = {
    "engine_version",
    "backtesting_version",
    "python_version",
    "pandas_version",
    "numpy_version",
    "engine_source_sha256",
    "data_source",
    "data_status",
    "as_of_time",
    "price_file",
    "price_file_sha256",
    "contract_file",
    "contract_file_sha256",
    "result_set_sha256",
    "results_file",
    "results_file_sha256",
    "result_row_count",
    "commission",
    "spread",
    "cash",
    "scope",
    "summary_provenance",
}

CURRENT_SUMMARY_FIELDS = {
    "engine_version",
    "backtesting_version",
    "contract_count",
    "completed_trade_count",
    "win_rate_eligible_count",
    "win_rate_eligibility_mismatch_count",
    "win_rate_guard_exclusion_count",
    "pre_entry_provenance_complete_count",
    "pre_entry_provenance_incomplete_count",
    "pre_entry_provenance_status_counts",
    "contract_eligibility_mismatch_count",
    "event_bucket_mismatch_count",
    "contract_space_bucket_mismatch_count",
    "event_bucket_contract_counts",
    "contract_space_bucket_counts",
    "outcome_bucket_counts",
    "result_set_sha256",
    "results_file_sha256",
    "engine_source_sha256",
    "run_metadata",
}

SUMMARY_PROVENANCE_FIELDS = {
    "result_columns",
    "pre_entry_provenance_complete_count",
    "pre_entry_provenance_incomplete_count",
    "pre_entry_provenance_status_counts",
    "contract_eligibility_mismatch_count",
    "event_bucket_mismatch_count",
    "contract_space_bucket_mismatch_count",
    "win_rate_eligibility_mismatch_count",
    "win_rate_guard_exclusion_count",
    "completed_trade_count",
    "outcome_bucket_counts",
}

REQUIRED_RESULT_COLUMNS = {
    "sample_id",
    "symbol",
    "decision_date",
    "direction",
    "primary_pattern",
    "internal_label",
    "order_branch",
    "event_context",
    "contract_frozen",
    "lineage_id",
    "fill_status",
    "trade_result",
    "evidence_status",
    "win_rate_eligible",
    "realized_R",
    "pre_entry_provenance_status",
    "pre_entry_provenance_missing_fields",
    "planned_entry_trigger",
}

ROUNDTRIP_SUMMARY_FIELDS = (
    "contract_count",
    "filled_count",
    "completed_trade_count",
    "win_rate_eligible_count",
    "win_rate_eligibility_mismatch_count",
    "win_rate_guard_exclusion_count",
    "pre_entry_provenance_complete_count",
    "pre_entry_provenance_incomplete_count",
    "pre_entry_provenance_status_counts",
    "contract_eligibility_mismatch_count",
    "event_bucket_mismatch_count",
    "contract_space_bucket_mismatch_count",
    "event_bucket_contract_counts",
    "contract_space_bucket_counts",
    "outcome_bucket_counts",
    "win_rate_pct",
    "realized_R_mean",
    "realized_R_median",
    "realized_R_min",
    "realized_R_max",
)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_result_set_sha256(path: Path) -> str:
    """Hash the exact emitted CSV after normalizing platform line endings."""

    payload = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(payload).hexdigest()


def _values_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if isinstance(left, float) and math.isnan(left):
            return isinstance(right, float) and math.isnan(right)
        if isinstance(right, float) and math.isnan(right):
            return False
        return math.isclose(float(left), float(right), rel_tol=1e-12, abs_tol=1e-12)
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            _values_equal(left[key], right[key]) for key in left
        )
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            _values_equal(item_left, item_right)
            for item_left, item_right in zip(left, right)
        )
    return left == right


def _missing_fields(mapping: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(field for field in required if field not in mapping)


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON root must be an object")
    return value


def _historical_result(
    artifact_dir: Path,
    *,
    engine_version: Any,
    historical_reasons: list[str],
    missing_metadata_fields: list[str],
    missing_summary_fields: list[str],
    missing_result_columns: list[str],
    row_count: int | None,
) -> dict[str, Any]:
    return {
        "status": "historical_incomplete",
        "artifact_dir": str(artifact_dir),
        "engine_version": engine_version,
        "row_count": row_count,
        "historical_reasons": historical_reasons,
        "missing_metadata_fields": missing_metadata_fields,
        "missing_summary_fields": missing_summary_fields,
        "missing_result_columns": missing_result_columns,
        "issues": [],
    }


def validate_artifact(artifact_dir: str | Path) -> dict[str, Any]:
    """Validate one replay output directory without changing any file."""

    directory = Path(artifact_dir).expanduser().resolve()
    result: dict[str, Any] = {
        "status": "invalid",
        "artifact_dir": str(directory),
        "engine_version": None,
        "row_count": None,
        "historical_reasons": [],
        "missing_metadata_fields": [],
        "missing_summary_fields": [],
        "missing_result_columns": [],
        "issues": [],
    }
    if not directory.is_dir():
        result["issues"].append("artifact directory does not exist")
        return result

    results_path = directory / "results.csv"
    summary_path = directory / "summary.json"
    metadata_path = directory / "run_metadata.json"
    missing_files = [
        str(path.name)
        for path in (results_path, summary_path, metadata_path)
        if not path.is_file()
    ]
    if missing_files:
        result["issues"].append(f"missing artifact file(s): {', '.join(missing_files)}")
        return result

    try:
        summary = _load_json(summary_path)
        metadata = _load_json(metadata_path)
        results = pd.read_csv(results_path)
    except (
        OSError,
        ValueError,
        UnicodeError,
        json.JSONDecodeError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
    ) as exc:
        result["issues"].append(f"cannot parse artifact: {exc}")
        return result

    result["row_count"] = int(len(results))
    result["engine_version"] = metadata.get("engine_version", summary.get("engine_version"))
    missing_metadata = _missing_fields(metadata, CURRENT_METADATA_FIELDS)
    missing_summary = _missing_fields(summary, CURRENT_SUMMARY_FIELDS)
    missing_result_columns = sorted(REQUIRED_RESULT_COLUMNS - set(results.columns))
    historical_reasons: list[str] = []
    if missing_metadata:
        historical_reasons.append("metadata predates the current artifact schema")
    if missing_summary:
        historical_reasons.append("summary predates the current artifact schema")
    if missing_result_columns:
        historical_reasons.append("results.csv predates the current result schema")
    metadata_engine = metadata.get("engine_version")
    summary_engine = summary.get("engine_version")
    if metadata_engine != ENGINE_VERSION:
        historical_reasons.append(
            f"metadata engine_version={metadata_engine!r} is not current {ENGINE_VERSION!r}"
        )
    if summary_engine != ENGINE_VERSION:
        historical_reasons.append(
            f"summary engine_version={summary_engine!r} is not current {ENGINE_VERSION!r}"
        )
    if historical_reasons:
        return _historical_result(
            directory,
            engine_version=result["engine_version"],
            historical_reasons=historical_reasons,
            missing_metadata_fields=missing_metadata,
            missing_summary_fields=missing_summary,
            missing_result_columns=missing_result_columns,
            row_count=len(results),
        )

    issues: list[str] = []
    result["issues"] = issues
    summary_provenance = metadata["summary_provenance"]
    if not isinstance(summary_provenance, dict):
        issues.append("metadata summary_provenance must be an object")
        return result
    missing_summary_provenance = _missing_fields(summary_provenance, SUMMARY_PROVENANCE_FIELDS)
    if missing_summary_provenance:
        issues.append(
            "summary_provenance missing field(s): " + ", ".join(missing_summary_provenance)
        )

    if summary.get("run_metadata") != metadata:
        issues.append("summary.json run_metadata does not equal run_metadata.json")
    if metadata.get("result_row_count") != len(results):
        issues.append("metadata result_row_count does not equal results.csv row count")
    if summary.get("contract_count") != len(results):
        issues.append("summary contract_count does not equal results.csv row count")

    result_columns = list(results.columns)
    if summary_provenance.get("result_columns") != result_columns:
        issues.append("summary_provenance result_columns do not equal results.csv columns")

    results_hash = _sha256_file(results_path)
    if metadata.get("results_file_sha256") != results_hash:
        issues.append("metadata results_file_sha256 does not match results.csv")
    if summary.get("results_file_sha256") != results_hash:
        issues.append("summary results_file_sha256 does not match results.csv")

    roundtrip_records = results.to_dict(orient="records")
    try:
        roundtrip_summary = build_summary(roundtrip_records)
    except (TypeError, ValueError, KeyError) as exc:
        issues.append(f"cannot rebuild summary from results.csv: {exc}")
        roundtrip_summary = None
    roundtrip_result_set_hash = _canonical_result_set_sha256(results_path)
    if metadata.get("result_set_sha256") != roundtrip_result_set_hash:
        issues.append("metadata result_set_sha256 does not match CSV round-trip")
    if summary.get("result_set_sha256") != roundtrip_result_set_hash:
        issues.append("summary result_set_sha256 does not match CSV round-trip")

    for field in ("engine_version", "backtesting_version", "engine_source_sha256"):
        if metadata.get(field) != summary.get(field):
            issues.append(f"metadata and summary disagree on {field}")

    for field in SUMMARY_PROVENANCE_FIELDS - {"result_columns"}:
        if field in summary_provenance and not _values_equal(
            summary_provenance[field], summary.get(field)
        ):
            issues.append(f"summary_provenance does not match summary field {field}")

    if roundtrip_summary is not None:
        for field in ROUNDTRIP_SUMMARY_FIELDS:
            if not _values_equal(roundtrip_summary.get(field), summary.get(field)):
                issues.append(f"CSV round-trip does not match summary field {field}")

    result["status"] = "current_valid" if not issues else "invalid"
    result["checks"] = {
        "results_file_sha256": results_hash,
        "result_set_sha256": roundtrip_result_set_hash,
        "summary_metadata_equal": summary.get("run_metadata") == metadata,
        "summary_provenance_columns_equal": summary_provenance.get("result_columns")
        == result_columns,
        "csv_summary_roundtrip": roundtrip_summary is not None and not any(
            issue.startswith("CSV round-trip") for issue in issues
        ),
    }
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only validation for PA Research replay artifacts."
    )
    parser.add_argument(
        "artifact_dir",
        help="Directory containing results.csv, summary.json and run_metadata.json",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = validate_artifact(args.artifact_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if report["status"] == "current_valid":
        return 0
    if report["status"] == "historical_incomplete":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Read-only comparison of two frozen external-human PA H/L records."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


COMPARATOR_VERSION = "pa_hl_expert_pair_comparison_v1"
LABEL_FIELD = "expert_ordinary_hl_label"
EXCLUSION_FIELD = "primary_exclusion"
COMPARISON_FIELDS = (
    "evidence_usable",
    "parent_state",
    "direction",
    "ema20_slope",
    "ema50_slope",
    "ema200_context",
    "A_leg_quality",
    "B_leg_class",
    "lineage_status",
    LABEL_FIELD,
    EXCLUSION_FIELD,
    "confidence_1_to_5",
    "major_high_low_reading",
    "A_leg_evidence",
    "B_leg_evidence",
    "lineage_and_attempt_evidence",
    "first_obstacle_and_space",
    "why_not_BOP_or_third_push_or_range_repeat",
    "main_uncertainty",
)


def _load_single_record_validator():
    validator_path = Path(__file__).with_name("validate_pa_hl_expert_annotations.py")
    spec = importlib.util.spec_from_file_location("pa_hl_single_record_validator", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load single-record validator: {validator_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SINGLE_VALIDATOR = _load_single_record_validator()


def _input_identity(path: Path, document: Any | None, validation: dict[str, Any]) -> dict[str, Any]:
    identifier = None
    if isinstance(document, dict) and isinstance(document.get("annotator"), dict):
        identifier = document["annotator"].get("identifier")
    try:
        record_sha256 = SINGLE_VALIDATOR.sha256_file(path)
    except OSError:
        record_sha256 = None
    return {
        "path": str(path),
        "record_sha256": record_sha256,
        "annotator_identifier": identifier,
        "single_record_validation": validation,
    }


def _load_if_valid_json(path: Path) -> Any | None:
    try:
        return SINGLE_VALIDATOR.load_json(path)
    except ValueError:
        return None


def _base_report(
    manifest_path: Path,
    expert_a_path: Path,
    expert_b_path: Path,
) -> tuple[dict[str, Any], Any | None, Any | None]:
    validation_a = SINGLE_VALIDATOR.validate(manifest_path, expert_a_path)
    validation_b = SINGLE_VALIDATOR.validate(manifest_path, expert_b_path)
    document_a = _load_if_valid_json(expert_a_path)
    document_b = _load_if_valid_json(expert_b_path)
    report = {
        "comparator_version": COMPARATOR_VERSION,
        "status": "invalid",
        "packet_id": validation_a.get("packet_id") or validation_b.get("packet_id"),
        "manifest_sha256": validation_a.get("manifest_sha256") or validation_b.get("manifest_sha256"),
        "expert_a": _input_identity(expert_a_path, document_a, validation_a),
        "expert_b": _input_identity(expert_b_path, document_b, validation_b),
        "pair_ineligible_reasons": [],
        "sample_comparisons": [],
        "summary": {
            "packet_total": validation_a.get("expected_sample_count") or validation_b.get("expected_sample_count"),
            "clean_pair_comparison_count": 0,
            "exact_all_field_agreement_count": 0,
            "label_and_exclusion_agreement_count": 0,
            "label_or_exclusion_disagreement_count": 0,
            "human_adjudication_records_created": 0,
            "model_prediction_coverage": 0,
            "accuracy_denominator": 0,
            "accuracy_excluded_reasons": {"adjudication_not_frozen": 0, "model_prediction_not_supplied": 0},
        },
        "trade_statistics": {
            "completed_trade_denominator": 0,
            "validated_win_rate": "not-computable",
            "conclusion": "no-new-positive",
        },
    }
    return report, document_a, document_b


def compare(manifest_path: Path, expert_a_path: Path, expert_b_path: Path) -> dict[str, Any]:
    """Validate both records, then compare exact frozen fields without adjudicating."""

    report, document_a, document_b = _base_report(manifest_path, expert_a_path, expert_b_path)
    validation_a = report["expert_a"]["single_record_validation"]
    validation_b = report["expert_b"]["single_record_validation"]
    statuses = (validation_a["status"], validation_b["status"])
    if "invalid" in statuses:
        report["status"] = "invalid"
        return report

    ineligible_reasons: list[str] = []
    if statuses[0] != "clean_eligible":
        ineligible_reasons.append("expert_a is not clean_eligible")
    if statuses[1] != "clean_eligible":
        ineligible_reasons.append("expert_b is not clean_eligible")

    identifier_a = report["expert_a"]["annotator_identifier"]
    identifier_b = report["expert_b"]["annotator_identifier"]
    if isinstance(identifier_a, str) and isinstance(identifier_b, str):
        if identifier_a.strip().casefold() == identifier_b.strip().casefold():
            ineligible_reasons.append("expert identifiers are not distinct")

    if ineligible_reasons:
        report["status"] = "valid_ineligible"
        report["pair_ineligible_reasons"] = sorted(set(ineligible_reasons))
        return report

    assert isinstance(document_a, dict) and isinstance(document_b, dict)
    rows_a = {row["expert_sample_id"]: row for row in document_a["annotations"]}
    rows_b = {row["expert_sample_id"]: row for row in document_b["annotations"]}
    comparisons: list[dict[str, Any]] = []
    for sample_id in sorted(rows_a):
        row_a = rows_a[sample_id]
        row_b = rows_b[sample_id]
        disagreement_fields = [field for field in COMPARISON_FIELDS if row_a[field] != row_b[field]]
        label_and_exclusion_agree = (
            row_a[LABEL_FIELD] == row_b[LABEL_FIELD]
            and row_a[EXCLUSION_FIELD] == row_b[EXCLUSION_FIELD]
        )
        comparisons.append(
            {
                "expert_sample_id": sample_id,
                "expert_a": {
                    LABEL_FIELD: row_a[LABEL_FIELD],
                    EXCLUSION_FIELD: row_a[EXCLUSION_FIELD],
                    "evidence_usable": row_a["evidence_usable"],
                },
                "expert_b": {
                    LABEL_FIELD: row_b[LABEL_FIELD],
                    EXCLUSION_FIELD: row_b[EXCLUSION_FIELD],
                    "evidence_usable": row_b["evidence_usable"],
                },
                "label_and_exclusion_agree": label_and_exclusion_agree,
                "exact_all_field_agreement": not disagreement_fields,
                "disagreement_fields": disagreement_fields,
                "adjudication_state": "not_recorded",
                "final_label": None,
                "accuracy_denominator_eligible": False,
                "accuracy_excluded_reasons": [
                    "adjudication_not_frozen",
                    "model_prediction_not_supplied",
                ],
            }
        )

    exact_count = sum(row["exact_all_field_agreement"] for row in comparisons)
    label_agreement_count = sum(row["label_and_exclusion_agree"] for row in comparisons)
    report["status"] = "comparison_ready"
    report["sample_comparisons"] = comparisons
    report["summary"] = {
        "packet_total": len(comparisons),
        "clean_pair_comparison_count": len(comparisons),
        "exact_all_field_agreement_count": exact_count,
        "label_and_exclusion_agreement_count": label_agreement_count,
        "label_or_exclusion_disagreement_count": len(comparisons) - label_agreement_count,
        "human_adjudication_records_created": 0,
        "model_prediction_coverage": 0,
        "accuracy_denominator": 0,
        "accuracy_excluded_reasons": {
            "adjudication_not_frozen": len(comparisons),
            "model_prediction_not_supplied": len(comparisons),
        },
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--expert-a", required=True, type=Path)
    parser.add_argument("--expert-b", required=True, type=Path)
    args = parser.parse_args(argv)
    report = compare(args.manifest, args.expert_a, args.expert_b)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"comparison_ready": 0, "invalid": 1, "valid_ineligible": 2}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())

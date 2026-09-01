#!/usr/bin/env python3
"""Read-only validation of a frozen external-human PA H/L pair adjudication."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


SCHEMA_VERSION = "pa_hl_expert_pair_adjudication_v1"
FINAL_LABELS = {"H1", "H2", "L1", "L2", "not_ordinary_HL"}
ADJUDICATION_STATES = {
    "experts_agree",
    "both_reasonable_boundary",
    "adjudicator_choice",
    "insufficient_evidence",
    "contaminated",
}
EXCLUDED_REASONS = {
    "pair_not_clean",
    "evidence_not_usable",
    "no_final_single_label",
    "boundary_or_unclear",
    "insufficient_evidence",
    "contaminated",
    "model_prediction_missing",
    "model_prediction_not_frozen_before_reveal",
}
ROOT_FIELDS = {
    "schema_version",
    "packet_id",
    "manifest_sha256",
    "expert_pair",
    "adjudication_freeze",
    "samples",
    "summary",
}
EXPERT_PAIR_FIELDS = {"expert_a", "expert_b", "distinct_identifiers"}
EXPERT_IDENTITY_FIELDS = {"record_sha256", "annotator_identifier", "single_record_validator_status"}
FREEZE_FIELDS = {
    "comparison_frozen_at",
    "adjudication_started_at",
    "adjudication_frozen_at",
    "source_or_model_hypotheses_seen_before_freeze",
    "future_or_outcome_evidence_seen_before_freeze",
    "knowledge_status",
}
SAMPLE_FIELDS = {
    "expert_sample_id",
    "expert_a",
    "expert_b",
    "comparison",
    "adjudication_state",
    "adjudicator",
    "final_label",
    "rationale",
    "accuracy_eligibility",
}
SNAPSHOT_FIELDS = {"expert_ordinary_hl_label", "primary_exclusion", "evidence_usable"}
COMPARISON_RECORD_FIELDS = {"label_and_exclusion_agree", "disagreement_fields"}
ADJUDICATOR_FIELDS = {
    "role",
    "identifier",
    "independent_of_expert_a_and_b",
    "source_or_model_hypotheses_seen_before_freeze",
    "future_or_outcome_evidence_seen_before_freeze",
    "knowledge_status",
}
ACCURACY_FIELDS = {
    "model_prediction_frozen_before_expert_reveal",
    "model_prediction_label",
    "eligible",
    "excluded_reason",
}
SUMMARY_FIELDS = {
    "packet_total",
    "clean_expert_pair_count",
    "adjudicated_single_label_count",
    "boundary_or_unclear_count",
    "contaminated_count",
    "model_prediction_coverage",
    "accuracy_denominator",
    "excluded_reasons",
    "completed_trade_denominator",
    "validated_win_rate",
    "conclusion",
}


def _load_pair_comparator():
    path = Path(__file__).with_name("compare_pa_hl_expert_annotations.py")
    spec = importlib.util.spec_from_file_location("pa_hl_pair_comparator_for_adjudication", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pair comparator: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


COMPARATOR = _load_pair_comparator()
SINGLE_VALIDATOR = COMPARATOR.SINGLE_VALIDATOR


@dataclass
class Validation:
    errors: list[str] = field(default_factory=list)
    ineligible_reasons: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def ineligible(self, message: str) -> None:
        self.ineligible_reasons.append(message)


def exact_fields(value: Any, expected: set[str], location: str, result: Validation) -> bool:
    if not isinstance(value, dict):
        result.error(f"{location} must be an object")
        return False
    missing = sorted(expected - set(value))
    extra = sorted(set(value) - expected)
    if missing:
        result.error(f"{location} missing fields: {', '.join(missing)}")
    if extra:
        result.error(f"{location} unknown fields: {', '.join(extra)}")
    return not missing and not extra


def parse_time(value: Any, location: str, result: Validation) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        result.error(f"{location} must be a non-empty ISO-8601 timestamp")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        result.error(f"{location} is not a valid ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None:
        result.error(f"{location} must include a timezone offset")
        return None
    return parsed


def _validate_expert_identity(
    identity: Any,
    source_path: Path,
    source_document: dict[str, Any],
    location: str,
    result: Validation,
) -> None:
    if not exact_fields(identity, EXPERT_IDENTITY_FIELDS, location, result):
        return
    if identity["record_sha256"] != SINGLE_VALIDATOR.sha256_file(source_path):
        result.error(f"{location}.record_sha256 does not match source expert record bytes")
    if identity["annotator_identifier"] != source_document["annotator"]["identifier"]:
        result.error(f"{location}.annotator_identifier does not match source expert record")
    if identity["single_record_validator_status"] != "clean_eligible":
        result.error(f"{location}.single_record_validator_status must be clean_eligible")


def _validate_adjudicator(
    adjudicator: Any,
    source_identifiers: set[str],
    location: str,
    result: Validation,
) -> bool:
    if not exact_fields(adjudicator, ADJUDICATOR_FIELDS, location, result):
        return False
    expected = {
        "role": "external_human_adjudicator",
        "independent_of_expert_a_and_b": True,
        "source_or_model_hypotheses_seen_before_freeze": False,
        "future_or_outcome_evidence_seen_before_freeze": False,
        "knowledge_status": "clean",
    }
    for field_name, expected_value in expected.items():
        if adjudicator[field_name] != expected_value:
            result.error(f"{location}.{field_name} must equal {expected_value!r}")
    identifier = adjudicator["identifier"]
    if not isinstance(identifier, str) or not identifier.strip():
        result.error(f"{location}.identifier must be non-empty")
    elif identifier.strip().casefold() in source_identifiers:
        result.error(f"{location}.identifier must be distinct from both source experts")
    return True


def _expected_exclusion_reason(
    *,
    global_clean: bool,
    state: str,
    evidence_a: Any,
    evidence_b: Any,
    final_label: Any,
    model_label: Any,
    model_frozen: Any,
) -> str | None:
    if state == "contaminated":
        return "contaminated"
    if not global_clean:
        return "pair_not_clean"
    if evidence_a != "yes" or evidence_b != "yes":
        return "evidence_not_usable"
    if state == "both_reasonable_boundary":
        return "boundary_or_unclear"
    if state == "insufficient_evidence":
        return "insufficient_evidence"
    if final_label not in FINAL_LABELS:
        return "no_final_single_label"
    if model_label is None:
        return "model_prediction_missing"
    if model_frozen is not True:
        return "model_prediction_not_frozen_before_reveal"
    return None


def validate(
    manifest_path: Path,
    expert_a_path: Path,
    expert_b_path: Path,
    adjudication_path: Path,
) -> dict[str, Any]:
    result = Validation()
    pair_report = COMPARATOR.compare(manifest_path, expert_a_path, expert_b_path)
    if pair_report["status"] != "comparison_ready":
        return {
            "status": "invalid",
            "errors": [f"source expert pair is not comparison_ready: {pair_report['status']}"],
            "ineligible_reasons": pair_report.get("pair_ineligible_reasons", []),
            "source_pair_validation": pair_report,
        }
    try:
        manifest = SINGLE_VALIDATOR.load_json(manifest_path)
        expert_a_document = SINGLE_VALIDATOR.load_json(expert_a_path)
        expert_b_document = SINGLE_VALIDATOR.load_json(expert_b_path)
        document = SINGLE_VALIDATOR.load_json(adjudication_path)
    except ValueError as exc:
        return {
            "status": "invalid",
            "errors": [str(exc)],
            "ineligible_reasons": [],
            "source_pair_validation": pair_report,
        }

    if not exact_fields(document, ROOT_FIELDS, "root", result):
        return {
            "status": "invalid",
            "errors": result.errors,
            "ineligible_reasons": [],
            "source_pair_validation": pair_report,
        }
    if document["schema_version"] != SCHEMA_VERSION:
        result.error(f"unsupported schema_version: {document['schema_version']!r}")
    if document["packet_id"] != manifest.get("packet_id"):
        result.error("packet_id does not match manifest")
    manifest_hash = SINGLE_VALIDATOR.sha256_file(manifest_path)
    if document["manifest_sha256"] != manifest_hash:
        result.error("manifest_sha256 does not match manifest bytes")

    expert_pair = document["expert_pair"]
    if exact_fields(expert_pair, EXPERT_PAIR_FIELDS, "expert_pair", result):
        _validate_expert_identity(expert_pair["expert_a"], expert_a_path, expert_a_document, "expert_pair.expert_a", result)
        _validate_expert_identity(expert_pair["expert_b"], expert_b_path, expert_b_document, "expert_pair.expert_b", result)
        if expert_pair["distinct_identifiers"] is not True:
            result.error("expert_pair.distinct_identifiers must be true")

    freeze = document["adjudication_freeze"]
    global_clean = False
    if exact_fields(freeze, FREEZE_FIELDS, "adjudication_freeze", result):
        comparison_frozen = parse_time(freeze["comparison_frozen_at"], "adjudication_freeze.comparison_frozen_at", result)
        adjudication_started = parse_time(freeze["adjudication_started_at"], "adjudication_freeze.adjudication_started_at", result)
        adjudication_frozen = parse_time(freeze["adjudication_frozen_at"], "adjudication_freeze.adjudication_frozen_at", result)
        expert_frozen_times = [
            parse_time(expert_a_document["freeze"]["annotation_frozen_at"], "expert_a.freeze.annotation_frozen_at", result),
            parse_time(expert_b_document["freeze"]["annotation_frozen_at"], "expert_b.freeze.annotation_frozen_at", result),
        ]
        if comparison_frozen is not None and all(value is not None for value in expert_frozen_times):
            if comparison_frozen < max(expert_frozen_times):
                result.error("comparison_frozen_at must not precede either expert annotation freeze")
        if comparison_frozen is not None and adjudication_started is not None and adjudication_started < comparison_frozen:
            result.error("adjudication_started_at must not precede comparison_frozen_at")
        if adjudication_started is not None and adjudication_frozen is not None and adjudication_frozen <= adjudication_started:
            result.error("adjudication_frozen_at must be after adjudication_started_at")
        for flag in (
            "source_or_model_hypotheses_seen_before_freeze",
            "future_or_outcome_evidence_seen_before_freeze",
        ):
            if not isinstance(freeze[flag], bool):
                result.error(f"adjudication_freeze.{flag} must be boolean")
            elif freeze[flag]:
                result.ineligible(f"adjudication_freeze.{flag}=true")
        if freeze["knowledge_status"] not in {"clean", "contaminated", "uncertain"}:
            result.error("adjudication_freeze.knowledge_status has invalid value")
        elif freeze["knowledge_status"] != "clean":
            result.ineligible(f"adjudication knowledge_status={freeze['knowledge_status']}")
        global_clean = not result.ineligible_reasons

    source_rows_a = {row["expert_sample_id"]: row for row in expert_a_document["annotations"]}
    source_rows_b = {row["expert_sample_id"]: row for row in expert_b_document["annotations"]}
    comparator_rows = {row["expert_sample_id"]: row for row in pair_report["sample_comparisons"]}
    expected_ids = [row["expert_sample_id"] for row in manifest["samples"]]
    samples = document["samples"]
    computed_rows: list[dict[str, Any]] = []
    if not isinstance(samples, list):
        result.error("samples must be an array")
        samples = []
    elif len(samples) != len(expected_ids):
        result.error(f"samples must contain exactly {len(expected_ids)} rows")

    source_identifiers = {
        expert_a_document["annotator"]["identifier"].strip().casefold(),
        expert_b_document["annotator"]["identifier"].strip().casefold(),
    }
    for index, row in enumerate(samples):
        location = f"samples[{index}]"
        if not exact_fields(row, SAMPLE_FIELDS, location, result):
            continue
        sample_id = row["expert_sample_id"]
        expected_id = expected_ids[index] if index < len(expected_ids) else None
        if sample_id != expected_id:
            result.error(f"{location}.expert_sample_id must equal {expected_id!r}")
            continue
        source_a = source_rows_a[sample_id]
        source_b = source_rows_b[sample_id]
        comparator_row = comparator_rows[sample_id]
        snapshots_valid = True
        for side_name, snapshot, source in (
            ("expert_a", row["expert_a"], source_a),
            ("expert_b", row["expert_b"], source_b),
        ):
            if not exact_fields(snapshot, SNAPSHOT_FIELDS, f"{location}.{side_name}", result):
                snapshots_valid = False
                continue
            for field_name in SNAPSHOT_FIELDS:
                if snapshot[field_name] != source[field_name]:
                    result.error(f"{location}.{side_name}.{field_name} does not match source expert record")
                    snapshots_valid = False

        comparison = row["comparison"]
        if exact_fields(comparison, COMPARISON_RECORD_FIELDS, f"{location}.comparison", result):
            if comparison["label_and_exclusion_agree"] != comparator_row["label_and_exclusion_agree"]:
                result.error(f"{location}.comparison.label_and_exclusion_agree does not match comparator")
            if comparison["disagreement_fields"] != comparator_row["disagreement_fields"]:
                result.error(f"{location}.comparison.disagreement_fields does not exactly match comparator")

        state = row["adjudication_state"]
        if state not in ADJUDICATION_STATES:
            result.error(f"{location}.adjudication_state has invalid value: {state!r}")
        final_label = row["final_label"]
        if final_label is not None and final_label not in FINAL_LABELS:
            result.error(f"{location}.final_label has invalid value: {final_label!r}")
        rationale = row["rationale"]
        if not isinstance(rationale, str) or not rationale.strip():
            result.error(f"{location}.rationale must be non-empty")

        adjudicator = row["adjudicator"]
        adjudicator_valid = adjudicator is None
        if adjudicator is not None:
            adjudicator_valid = _validate_adjudicator(adjudicator, source_identifiers, f"{location}.adjudicator", result)
        if state == "adjudicator_choice" and adjudicator is None:
            result.error(f"{location}: adjudicator_choice requires a clean third adjudicator")
        if state == "experts_agree" and adjudicator is not None:
            result.error(f"{location}: experts_agree must not name an adjudicator")

        if snapshots_valid and state == "experts_agree":
            if not comparator_row["label_and_exclusion_agree"]:
                result.error(f"{location}: experts_agree requires matching source label and exclusion")
            if source_a["evidence_usable"] != "yes" or source_b["evidence_usable"] != "yes":
                result.error(f"{location}: experts_agree requires both source records evidence_usable=yes")
            if source_a["expert_ordinary_hl_label"] not in FINAL_LABELS:
                result.error(f"{location}: experts_agree cannot turn unclear into a final label")
            if final_label != source_a["expert_ordinary_hl_label"]:
                result.error(f"{location}: experts_agree final_label must equal both frozen expert labels")
        elif state == "adjudicator_choice":
            if final_label not in FINAL_LABELS:
                result.error(f"{location}: adjudicator_choice requires a final single label")
            if not adjudicator_valid:
                result.error(f"{location}: adjudicator_choice adjudicator is not clean and independent")
        elif state in {"both_reasonable_boundary", "insufficient_evidence", "contaminated"}:
            if final_label is not None:
                result.error(f"{location}: {state} must not have a final_label")

        accuracy = row["accuracy_eligibility"]
        expected_reason: str | None = "no_final_single_label"
        if exact_fields(accuracy, ACCURACY_FIELDS, f"{location}.accuracy_eligibility", result):
            model_frozen = accuracy["model_prediction_frozen_before_expert_reveal"]
            model_label = accuracy["model_prediction_label"]
            if not isinstance(model_frozen, bool):
                result.error(f"{location}.accuracy_eligibility.model_prediction_frozen_before_expert_reveal must be boolean")
            if model_label is not None and model_label not in FINAL_LABELS:
                result.error(f"{location}.accuracy_eligibility.model_prediction_label has invalid value")
            if not isinstance(accuracy["eligible"], bool):
                result.error(f"{location}.accuracy_eligibility.eligible must be boolean")
            expected_reason = _expected_exclusion_reason(
                global_clean=global_clean,
                state=state,
                evidence_a=source_a["evidence_usable"],
                evidence_b=source_b["evidence_usable"],
                final_label=final_label,
                model_label=model_label,
                model_frozen=model_frozen,
            )
            expected_eligible = expected_reason is None
            if accuracy["eligible"] is not expected_eligible:
                result.error(f"{location}.accuracy_eligibility.eligible does not match recomputed eligibility")
            if accuracy["excluded_reason"] != expected_reason:
                result.error(f"{location}.accuracy_eligibility.excluded_reason must equal {expected_reason!r}")
            if accuracy["excluded_reason"] is not None and accuracy["excluded_reason"] not in EXCLUDED_REASONS:
                result.error(f"{location}.accuracy_eligibility.excluded_reason has invalid value")
        computed_rows.append(
            {
                "state": state,
                "final_label": final_label,
                "model_label": accuracy.get("model_prediction_label") if isinstance(accuracy, dict) else None,
                "eligible": accuracy.get("eligible") is True if isinstance(accuracy, dict) else False,
                "excluded_reason": expected_reason,
                "clean_pair": global_clean and state != "contaminated",
            }
        )

    expected_excluded_reasons: dict[str, int] = {}
    for row in computed_rows:
        reason = row["excluded_reason"]
        if reason is not None:
            expected_excluded_reasons[reason] = expected_excluded_reasons.get(reason, 0) + 1
    expected_summary = {
        "packet_total": len(expected_ids),
        "clean_expert_pair_count": sum(row["clean_pair"] for row in computed_rows),
        "adjudicated_single_label_count": sum(row["final_label"] in FINAL_LABELS for row in computed_rows),
        "boundary_or_unclear_count": sum(row["state"] in {"both_reasonable_boundary", "insufficient_evidence"} for row in computed_rows),
        "contaminated_count": sum(row["state"] == "contaminated" for row in computed_rows),
        "model_prediction_coverage": sum(row["model_label"] in FINAL_LABELS for row in computed_rows),
        "accuracy_denominator": sum(row["eligible"] for row in computed_rows),
        "excluded_reasons": expected_excluded_reasons,
        "completed_trade_denominator": 0,
        "validated_win_rate": "not-computable",
        "conclusion": "no-new-positive",
    }
    summary = document["summary"]
    if exact_fields(summary, SUMMARY_FIELDS, "summary", result):
        for field_name, expected_value in expected_summary.items():
            if summary[field_name] != expected_value:
                result.error(f"summary.{field_name} does not match independently recomputed value {expected_value!r}")

    status = "invalid" if result.errors else "valid_ineligible" if result.ineligible_reasons else "valid"
    return {
        "status": status,
        "packet_id": manifest.get("packet_id"),
        "manifest_sha256": manifest_hash,
        "source_pair_status": pair_report["status"],
        "expected_sample_count": len(expected_ids),
        "received_sample_count": len(samples),
        "recomputed_summary": expected_summary,
        "errors": result.errors,
        "ineligible_reasons": sorted(set(result.ineligible_reasons)),
        "records_created_or_modified": 0,
        "trade_statistics": {
            "completed_trade_denominator": 0,
            "validated_win_rate": "not-computable",
            "conclusion": "no-new-positive",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--expert-a", required=True, type=Path)
    parser.add_argument("--expert-b", required=True, type=Path)
    parser.add_argument("--adjudication", required=True, type=Path)
    args = parser.parse_args(argv)
    report = validate(args.manifest, args.expert_a, args.expert_b, args.adjudication)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"valid": 0, "invalid": 1, "valid_ineligible": 2}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())

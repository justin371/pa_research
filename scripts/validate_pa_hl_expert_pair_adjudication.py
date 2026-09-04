#!/usr/bin/env python3
"""Read-only validation of a frozen external-human PA H/L pair adjudication."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import importlib.util
import hashlib
import json
import math
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
SUMMARY_INTEGER_FIELDS = {
    "packet_total",
    "clean_expert_pair_count",
    "adjudicated_single_label_count",
    "boundary_or_unclear_count",
    "contaminated_count",
    "model_prediction_coverage",
    "accuracy_denominator",
    "completed_trade_denominator",
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


def _is_allowed_string(value: Any, allowed: set[str]) -> bool:
    """Return whether a JSON value is a string in the supplied enum."""

    # JSON arrays/objects become unhashable Python values.  Type-check first so
    # malformed input is reported as invalid instead of escaping as TypeError.
    return isinstance(value, str) and value in allowed


def _is_json_integer(value: Any) -> bool:
    """Return whether a finite JSON number has an integral mathematical value."""

    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    return isinstance(value, float) and math.isfinite(value) and value.is_integer()


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
    source_bytes: bytes,
    source_document: dict[str, Any],
    location: str,
    result: Validation,
) -> None:
    if not exact_fields(identity, EXPERT_IDENTITY_FIELDS, location, result):
        return
    if identity["record_sha256"] != hashlib.sha256(source_bytes).hexdigest():
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
        actual_value = adjudicator[field_name]
        if isinstance(expected_value, bool):
            matches = isinstance(actual_value, bool) and actual_value is expected_value
        else:
            matches = actual_value == expected_value
        if not matches:
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
    if not _is_allowed_string(final_label, FINAL_LABELS):
        return "no_final_single_label"
    if model_label is None:
        return "model_prediction_missing"
    if not _is_allowed_string(model_label, FINAL_LABELS):
        return "model_prediction_missing"
    # V1 carries only self-attested fields in the adjudication record. Even a
    # true claim cannot prove when the prediction existed. Fail closed until
    # an independently anchored pre-reveal receipt has an adopted verifier.
    return "model_prediction_not_frozen_before_reveal"


def validate(
    manifest_path: Path,
    expert_a_path: Path,
    expert_b_path: Path,
    adjudication_path: Path,
) -> dict[str, Any]:
    result = Validation()
    try:
        manifest_bytes = manifest_path.read_bytes()
        expert_a_bytes = expert_a_path.read_bytes()
        expert_b_bytes = expert_b_path.read_bytes()
        adjudication_bytes = adjudication_path.read_bytes()
    except OSError as exc:
        return {
            "status": "invalid",
            "errors": [f"cannot read adjudication input: {exc}"],
            "ineligible_reasons": [],
        }
    pair_report = COMPARATOR.compare(
        manifest_path,
        expert_a_path,
        expert_b_path,
        _manifest_bytes=manifest_bytes,
        _expert_a_bytes=expert_a_bytes,
        _expert_b_bytes=expert_b_bytes,
    )
    if pair_report["status"] != "comparison_ready":
        return {
            "status": "invalid",
            "errors": [f"source expert pair is not comparison_ready: {pair_report['status']}"],
            "ineligible_reasons": pair_report.get("pair_ineligible_reasons", []),
            "source_pair_validation": pair_report,
        }
    try:
        manifest = SINGLE_VALIDATOR.load_json_bytes(manifest_bytes, manifest_path)
        expert_a_document = SINGLE_VALIDATOR.load_json_bytes(expert_a_bytes, expert_a_path)
        expert_b_document = SINGLE_VALIDATOR.load_json_bytes(expert_b_bytes, expert_b_path)
        document = SINGLE_VALIDATOR.load_json_bytes(adjudication_bytes, adjudication_path)
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
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    if document["manifest_sha256"] != manifest_hash:
        result.error("manifest_sha256 does not match manifest bytes")

    expert_pair = document["expert_pair"]
    if exact_fields(expert_pair, EXPERT_PAIR_FIELDS, "expert_pair", result):
        _validate_expert_identity(expert_pair["expert_a"], expert_a_bytes, expert_a_document, "expert_pair.expert_a", result)
        _validate_expert_identity(expert_pair["expert_b"], expert_b_bytes, expert_b_document, "expert_pair.expert_b", result)
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
        knowledge_status = freeze["knowledge_status"]
        if not _is_allowed_string(knowledge_status, {"clean", "contaminated", "uncertain"}):
            result.error("adjudication_freeze.knowledge_status has invalid value")
        elif knowledge_status != "clean":
            result.ineligible(f"adjudication knowledge_status={knowledge_status}")
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
            agreement = comparison["label_and_exclusion_agree"]
            if not isinstance(agreement, bool):
                result.error(f"{location}.comparison.label_and_exclusion_agree must be boolean")
            elif agreement != comparator_row["label_and_exclusion_agree"]:
                result.error(f"{location}.comparison.label_and_exclusion_agree does not match comparator")
            disagreement_fields = comparison["disagreement_fields"]
            if not isinstance(disagreement_fields, list):
                result.error(f"{location}.comparison.disagreement_fields must be an array")
            elif disagreement_fields != comparator_row["disagreement_fields"]:
                result.error(f"{location}.comparison.disagreement_fields does not exactly match comparator")

        state = row["adjudication_state"]
        state_valid = _is_allowed_string(state, ADJUDICATION_STATES)
        if not state_valid:
            result.error(f"{location}.adjudication_state has invalid value: {state!r}")
        state_for_logic = state if state_valid else ""
        final_label = row["final_label"]
        final_label_valid = final_label is None or _is_allowed_string(final_label, FINAL_LABELS)
        if not final_label_valid:
            result.error(f"{location}.final_label has invalid value: {final_label!r}")
        final_label_for_logic = final_label if final_label_valid else None
        rationale = row["rationale"]
        if not isinstance(rationale, str) or not rationale.strip():
            result.error(f"{location}.rationale must be non-empty")

        adjudicator = row["adjudicator"]
        adjudicator_valid = adjudicator is None
        if adjudicator is not None:
            adjudicator_valid = _validate_adjudicator(adjudicator, source_identifiers, f"{location}.adjudicator", result)
        if state_for_logic == "adjudicator_choice" and adjudicator is None:
            result.error(f"{location}: adjudicator_choice requires a clean third adjudicator")
        if state_for_logic == "experts_agree" and adjudicator is not None:
            result.error(f"{location}: experts_agree must not name an adjudicator")

        if snapshots_valid and state_for_logic == "experts_agree":
            if not comparator_row["label_and_exclusion_agree"]:
                result.error(f"{location}: experts_agree requires matching source label and exclusion")
            if source_a["evidence_usable"] != "yes" or source_b["evidence_usable"] != "yes":
                result.error(f"{location}: experts_agree requires both source records evidence_usable=yes")
            if source_a["expert_ordinary_hl_label"] not in FINAL_LABELS:
                result.error(f"{location}: experts_agree cannot turn unclear into a final label")
            if final_label != source_a["expert_ordinary_hl_label"]:
                result.error(f"{location}: experts_agree final_label must equal both frozen expert labels")
        elif state_for_logic == "adjudicator_choice":
            if not _is_allowed_string(final_label_for_logic, FINAL_LABELS):
                result.error(f"{location}: adjudicator_choice requires a final single label")
            if not adjudicator_valid:
                result.error(f"{location}: adjudicator_choice adjudicator is not clean and independent")
        elif state_for_logic == "both_reasonable_boundary":
            if final_label is not None:
                result.error(f"{location}: {state} must not have a final_label")
            if comparator_row["label_and_exclusion_agree"] is not False:
                result.error(
                    f"{location}: both_reasonable_boundary requires label/exclusion disagreement"
                )
        elif state_for_logic in {"insufficient_evidence", "contaminated"}:
            if final_label is not None:
                result.error(f"{location}: {state} must not have a final_label")

        accuracy = row["accuracy_eligibility"]
        expected_reason: str | None = "no_final_single_label"
        if exact_fields(accuracy, ACCURACY_FIELDS, f"{location}.accuracy_eligibility", result):
            model_frozen = accuracy["model_prediction_frozen_before_expert_reveal"]
            model_label = accuracy["model_prediction_label"]
            if not isinstance(model_frozen, bool):
                result.error(f"{location}.accuracy_eligibility.model_prediction_frozen_before_expert_reveal must be boolean")
            if model_label is not None and not _is_allowed_string(model_label, FINAL_LABELS):
                result.error(f"{location}.accuracy_eligibility.model_prediction_label has invalid value")
            if not isinstance(accuracy["eligible"], bool):
                result.error(f"{location}.accuracy_eligibility.eligible must be boolean")
            expected_reason = _expected_exclusion_reason(
                global_clean=global_clean,
                state=state_for_logic,
                evidence_a=source_a["evidence_usable"],
                evidence_b=source_b["evidence_usable"],
                final_label=final_label_for_logic,
                model_label=model_label if model_label is None or _is_allowed_string(model_label, FINAL_LABELS) else None,
                model_frozen=model_frozen,
            )
            expected_eligible = expected_reason is None
            if accuracy["eligible"] is not expected_eligible:
                result.error(f"{location}.accuracy_eligibility.eligible does not match recomputed eligibility")
            if accuracy["excluded_reason"] != expected_reason:
                result.error(f"{location}.accuracy_eligibility.excluded_reason must equal {expected_reason!r}")
            if accuracy["excluded_reason"] is not None and not _is_allowed_string(
                accuracy["excluded_reason"], EXCLUDED_REASONS
            ):
                result.error(f"{location}.accuracy_eligibility.excluded_reason has invalid value")
        computed_rows.append(
            {
                "state": state_for_logic,
                "final_label": final_label_for_logic,
                "model_label": (
                    accuracy.get("model_prediction_label")
                    if isinstance(accuracy, dict)
                    and (
                        accuracy.get("model_prediction_label") is None
                        or _is_allowed_string(accuracy.get("model_prediction_label"), FINAL_LABELS)
                    )
                    else None
                ),
                "eligible": expected_reason is None,
                "excluded_reason": expected_reason,
                "clean_pair": global_clean and state_for_logic != "contaminated",
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
        for field_name in SUMMARY_INTEGER_FIELDS:
            if not _is_json_integer(summary[field_name]):
                result.error(f"summary.{field_name} must be a JSON integer")
        excluded_reasons = summary["excluded_reasons"]
        if not isinstance(excluded_reasons, dict):
            result.error("summary.excluded_reasons must be an object")
        else:
            for reason, count in excluded_reasons.items():
                if not isinstance(reason, str):
                    result.error("summary.excluded_reasons keys must be strings")
                if not _is_json_integer(count) or count < 0:
                    result.error(
                        f"summary.excluded_reasons[{reason!r}] must be a non-negative JSON integer"
                    )
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
        "model_prediction_freeze_verification": "unavailable_v1_self_attestation_only",
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

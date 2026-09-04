#!/usr/bin/env python3
"""Read-only validation for future external-human PA H/L annotations."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


SCHEMA_VERSION = "pa_hl_expert_annotations_v1"
EXPECTED_SAMPLE_COUNT = 16
CANONICAL_MANIFEST_SHA256 = "d1616e568bceebbe605d498548ffc5c346cec1365831ba9035ab131ad9765b23"
SAMPLE_ID_RE = re.compile(r"^EH1-[0-9]{3}$")
ROOT_FIELDS = {"schema_version", "packet_id", "manifest_sha256", "annotator", "freeze", "annotations"}
ANNOTATOR_FIELDS = {"role", "identifier", "independent"}
FREEZE_FIELDS = {
    "annotation_started_at",
    "annotation_frozen_at",
    "source_or_model_hypotheses_seen_before_freeze",
    "future_or_outcome_evidence_seen_before_freeze",
    "knowledge_status",
}
TEXT_FIELDS = {
    "major_high_low_reading",
    "A_leg_evidence",
    "B_leg_evidence",
    "lineage_and_attempt_evidence",
    "first_obstacle_and_space",
    "why_not_BOP_or_third_push_or_range_repeat",
    "main_uncertainty",
}
ANNOTATION_FIELDS = {
    "expert_sample_id",
    "evidence_usable",
    "parent_state",
    "direction",
    "ema20_slope",
    "ema50_slope",
    "ema200_context",
    "A_leg_quality",
    "B_leg_class",
    "lineage_status",
    "expert_ordinary_hl_label",
    "primary_exclusion",
    "confidence_1_to_5",
    *TEXT_FIELDS,
}
ENUMS = {
    "evidence_usable": {"yes", "no", "uncertain"},
    "parent_state": {"open_trend", "trading_range", "range_edge", "transition", "climax", "unclear"},
    "direction": {"long", "short", "no_valid_direction"},
    "ema20_slope": {"rising", "falling", "flat", "unclear"},
    "ema50_slope": {"rising", "falling", "flat", "unclear"},
    "ema200_context": {"supportive", "conflicting", "neutral", "unclear"},
    "A_leg_quality": {"strong", "ordinary", "event_driven", "unclear"},
    "B_leg_class": {"controlled", "controlled_late", "deep_but_late_controlled", "uncontrolled", "range_like", "not_formed", "unclear"},
    "lineage_status": {"same_lineage", "reset", "unclear"},
    "expert_ordinary_hl_label": {"H1", "H2", "L1", "L2", "not_ordinary_HL", "unclear"},
    "primary_exclusion": {"not_applicable", "accepted_BOP", "third_push_H3_L3", "range_repeat", "event_or_gap", "EMA_gate_fail", "insufficient_space", "A_not_directional", "B_not_controlled", "lineage_reset", "no_valid_direction", "insufficient_evidence", "other"},
}
ORDINARY_LABELS = {"H1", "H2", "L1", "L2"}
CONTROLLED_B = {"controlled", "controlled_late", "deep_but_late_controlled"}


@dataclass
class Validation:
    errors: list[str] = field(default_factory=list)
    ineligible_reasons: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def ineligible(self, message: str) -> None:
        self.ineligible_reasons.append(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json_bytes(payload: bytes, source: object) -> Any:
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid UTF-8 JSON: {source}: {exc}") from exc


def load_json(path: Path) -> Any:
    try:
        return load_json_bytes(path.read_bytes(), path)
    except OSError as exc:
        raise ValueError(f"cannot read valid UTF-8 JSON: {path}: {exc}") from exc


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

    # JSON arrays/objects become unhashable Python values.  Type-check before
    # membership so malformed input is reported as invalid instead of escaping
    # as a TypeError from a branch-specific policy check.
    return isinstance(value, str) and value in allowed


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


def validate_annotation(row: Any, index: int, result: Validation) -> str | None:
    location = f"annotations[{index}]"
    if not exact_fields(row, ANNOTATION_FIELDS, location, result):
        sample_id = row.get("expert_sample_id") if isinstance(row, dict) else None
        return sample_id if isinstance(sample_id, str) else None
    sample_id = row["expert_sample_id"]
    if not isinstance(sample_id, str) or SAMPLE_ID_RE.fullmatch(sample_id) is None:
        result.error(f"{location}.expert_sample_id is invalid")
    for field_name, allowed in ENUMS.items():
        value = row[field_name]
        # Check the JSON type before set membership.  Lists and objects are
        # valid JSON values but unhashable Python values; testing either
        # directly with ``value not in allowed`` would crash the validator
        # instead of returning its promised structured invalid result.
        if not _is_allowed_string(value, allowed):
            result.error(f"{location}.{field_name} has invalid value: {value!r}")
    confidence = row["confidence_1_to_5"]
    if isinstance(confidence, bool) or not isinstance(confidence, int) or not 1 <= confidence <= 5:
        result.error(f"{location}.confidence_1_to_5 must be an integer from 1 to 5")
    for field_name in TEXT_FIELDS:
        value = row[field_name]
        if not isinstance(value, str) or not value.strip():
            result.error(f"{location}.{field_name} must contain reasoned evidence")

    label = row["expert_ordinary_hl_label"]
    exclusion = row["primary_exclusion"]
    if isinstance(label, str) and label in ORDINARY_LABELS:
        if row["evidence_usable"] != "yes":
            result.error(f"{location}: ordinary H/L requires evidence_usable=yes")
        if row["parent_state"] != "open_trend":
            result.error(f"{location}: ordinary H/L requires parent_state=open_trend")
        if row["lineage_status"] != "same_lineage":
            result.error(f"{location}: ordinary H/L requires lineage_status=same_lineage")
        if not _is_allowed_string(row["A_leg_quality"], {"strong", "ordinary"}):
            result.error(f"{location}: ordinary H/L requires directional non-event A leg")
        if not _is_allowed_string(row["B_leg_class"], CONTROLLED_B):
            result.error(f"{location}: ordinary H/L requires a controlled B leg")
        if exclusion != "not_applicable":
            result.error(f"{location}: ordinary H/L requires primary_exclusion=not_applicable")
        if isinstance(label, str) and label.startswith("H"):
            if row["direction"] != "long" or row["ema20_slope"] != "rising" or row["ema50_slope"] != "rising":
                result.error(f"{location}: H1/H2 requires long direction and rising EMA20/50")
        if isinstance(label, str) and label.startswith("L"):
            if row["direction"] != "short" or row["ema20_slope"] != "falling" or row["ema50_slope"] != "falling":
                result.error(f"{location}: L1/L2 requires short direction and falling EMA20/50")
    elif label == "not_ordinary_HL" and exclusion == "not_applicable":
        result.error(f"{location}: not_ordinary_HL requires a primary exclusion")
    elif label == "unclear" and not _is_allowed_string(exclusion, {"insufficient_evidence", "other"}):
        result.error(f"{location}: unclear label requires insufficient_evidence or other exclusion")

    if row["evidence_usable"] == "no":
        if isinstance(label, str) and label in ORDINARY_LABELS:
            result.error(f"{location}: unusable evidence cannot receive an ordinary H/L label")
        if exclusion != "insufficient_evidence":
            result.error(f"{location}: evidence_usable=no requires insufficient_evidence exclusion")
    return sample_id if isinstance(sample_id, str) else None


def validate(
    manifest_path: Path,
    annotations_path: Path,
    *,
    _manifest_bytes: bytes | None = None,
    _annotations_bytes: bytes | None = None,
) -> dict[str, Any]:
    result = Validation()
    try:
        manifest_bytes = manifest_path.read_bytes() if _manifest_bytes is None else _manifest_bytes
        annotations_bytes = (
            annotations_path.read_bytes() if _annotations_bytes is None else _annotations_bytes
        )
        actual_manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
        manifest = load_json_bytes(manifest_bytes, manifest_path)
        document = load_json_bytes(annotations_bytes, annotations_path)
    except (OSError, ValueError) as exc:
        return {"status": "invalid", "errors": [str(exc)], "ineligible_reasons": []}

    if actual_manifest_hash != CANONICAL_MANIFEST_SHA256:
        result.error("manifest bytes do not match the frozen canonical expert packet")
    if not isinstance(manifest, dict):
        return {"status": "invalid", "errors": ["manifest must be an object"], "ineligible_reasons": []}
    if not isinstance(manifest.get("packet_id"), str) or not manifest["packet_id"].strip():
        result.error("manifest packet_id must be a non-empty string")
    manifest_samples = manifest.get("samples")
    expected_ids: list[str] = []
    if not isinstance(manifest_samples, list):
        result.error("manifest samples must be an array")
        manifest_samples = []
    for index, row in enumerate(manifest_samples):
        if not isinstance(row, dict):
            result.error(f"manifest.samples[{index}] must be an object")
            continue
        sample_id = row.get("expert_sample_id")
        if not isinstance(sample_id, str) or SAMPLE_ID_RE.fullmatch(sample_id) is None:
            result.error(f"manifest.samples[{index}].expert_sample_id is invalid")
            continue
        expected_ids.append(sample_id)
    if len(manifest_samples) != EXPECTED_SAMPLE_COUNT:
        result.error(f"manifest must contain exactly {EXPECTED_SAMPLE_COUNT} samples")
    if len(expected_ids) != len(set(expected_ids)):
        result.error("manifest sample IDs are duplicated")
    if manifest.get("sample_count") != len(manifest_samples):
        result.error("manifest sample_count does not match samples")
    if manifest.get("sample_count") != EXPECTED_SAMPLE_COUNT:
        result.error(f"manifest sample_count must equal {EXPECTED_SAMPLE_COUNT}")

    if not exact_fields(document, ROOT_FIELDS, "root", result):
        return {"status": "invalid", "errors": result.errors, "ineligible_reasons": []}
    if document["schema_version"] != SCHEMA_VERSION:
        result.error(f"unsupported schema_version: {document['schema_version']!r}")
    if document["packet_id"] != manifest.get("packet_id"):
        result.error("packet_id does not match manifest")
    if document["manifest_sha256"] != actual_manifest_hash:
        result.error("manifest_sha256 does not match manifest bytes")

    annotator = document["annotator"]
    if exact_fields(annotator, ANNOTATOR_FIELDS, "annotator", result):
        if annotator["role"] != "external_human_expert":
            result.error("annotator.role must be external_human_expert")
        if not isinstance(annotator["identifier"], str) or not annotator["identifier"].strip():
            result.error("annotator.identifier must be non-empty")
        if not isinstance(annotator["independent"], bool):
            result.error("annotator.independent must be boolean")
        elif not annotator["independent"]:
            result.ineligible("annotator is not independent")

    freeze = document["freeze"]
    if exact_fields(freeze, FREEZE_FIELDS, "freeze", result):
        started = parse_time(freeze["annotation_started_at"], "freeze.annotation_started_at", result)
        frozen = parse_time(freeze["annotation_frozen_at"], "freeze.annotation_frozen_at", result)
        if started is not None and frozen is not None and frozen <= started:
            result.error("annotation_frozen_at must be after annotation_started_at")
        for flag in ("source_or_model_hypotheses_seen_before_freeze", "future_or_outcome_evidence_seen_before_freeze"):
            if not isinstance(freeze[flag], bool):
                result.error(f"freeze.{flag} must be boolean")
            elif freeze[flag]:
                result.ineligible(f"freeze.{flag}=true")
        knowledge_status = freeze["knowledge_status"]
        if not isinstance(knowledge_status, str) or knowledge_status not in {"clean", "contaminated", "uncertain"}:
            result.error("freeze.knowledge_status has invalid value")
        elif knowledge_status != "clean":
            result.ineligible(f"knowledge_status={knowledge_status}")

    annotations = document["annotations"]
    actual_ids: list[str] = []
    if not isinstance(annotations, list):
        result.error("annotations must be an array")
    else:
        for index, row in enumerate(annotations):
            sample_id = validate_annotation(row, index, result)
            if sample_id:
                actual_ids.append(sample_id)
        duplicates = sorted({sample_id for sample_id in actual_ids if actual_ids.count(sample_id) > 1})
        missing = sorted(set(expected_ids) - set(actual_ids))
        extra = sorted(set(actual_ids) - set(expected_ids))
        if duplicates:
            result.error(f"duplicate expert_sample_id values: {', '.join(duplicates)}")
        if missing:
            result.error(f"missing expert_sample_id values: {', '.join(missing)}")
        if extra:
            result.error(f"unexpected expert_sample_id values: {', '.join(extra)}")
        if len(annotations) != len(expected_ids):
            result.error(f"annotation cardinality must equal manifest: {len(expected_ids)}")

    status = "invalid" if result.errors else "valid_ineligible" if result.ineligible_reasons else "clean_eligible"
    return {
        "status": status,
        "packet_id": manifest.get("packet_id"),
        "manifest_sha256": actual_manifest_hash,
        "expected_sample_count": len(expected_ids),
        "received_annotation_count": len(annotations) if isinstance(annotations, list) else None,
        "errors": result.errors,
        "ineligible_reasons": sorted(set(result.ineligible_reasons)),
        "trade_statistics": {
            "completed_trade_denominator": 0,
            "validated_win_rate": "not-computable",
            "conclusion": "no-new-positive",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--annotations", required=True, type=Path)
    args = parser.parse_args(argv)
    report = validate(args.manifest, args.annotations)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"clean_eligible": 0, "invalid": 1, "valid_ineligible": 2}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())

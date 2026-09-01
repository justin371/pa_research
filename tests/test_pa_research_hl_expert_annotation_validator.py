import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = REPO_ROOT / "research" / "calibration" / "external_human_hl_v1"
MANIFEST_PATH = PACKET_ROOT / "manifest.json"
SCHEMA_PATH = PACKET_ROOT / "annotation_schema_v1.json"
POLICY_PATH = PACKET_ROOT / "adjudication_and_denominator_policy_CN.md"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_hl_expert_annotations.py"

SPEC = importlib.util.spec_from_file_location("hl_expert_validator", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def synthetic_annotation(sample_id: str):
    return {
        "expert_sample_id": sample_id,
        "evidence_usable": "yes",
        "parent_state": "trading_range",
        "direction": "no_valid_direction",
        "ema20_slope": "flat",
        "ema50_slope": "flat",
        "ema200_context": "neutral",
        "A_leg_quality": "ordinary",
        "B_leg_class": "range_like",
        "lineage_status": "same_lineage",
        "expert_ordinary_hl_label": "not_ordinary_HL",
        "primary_exclusion": "range_repeat",
        "confidence_1_to_5": 3,
        "major_high_low_reading": "synthetic major-high/low evidence",
        "A_leg_evidence": "synthetic A-leg evidence",
        "B_leg_evidence": "synthetic B-leg evidence",
        "lineage_and_attempt_evidence": "synthetic lineage evidence",
        "first_obstacle_and_space": "synthetic obstacle evidence",
        "why_not_BOP_or_third_push_or_range_repeat": "synthetic route evidence",
        "main_uncertainty": "synthetic uncertainty",
    }


def clean_document():
    manifest = read_json(MANIFEST_PATH)
    return {
        "schema_version": "pa_hl_expert_annotations_v1",
        "packet_id": manifest["packet_id"],
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "annotator": {
            "role": "external_human_expert",
            "identifier": "synthetic-test-expert",
            "independent": True,
        },
        "freeze": {
            "annotation_started_at": "2026-09-01T10:00:00+08:00",
            "annotation_frozen_at": "2026-09-01T11:00:00+08:00",
            "source_or_model_hypotheses_seen_before_freeze": False,
            "future_or_outcome_evidence_seen_before_freeze": False,
            "knowledge_status": "clean",
        },
        "annotations": [synthetic_annotation(row["expert_sample_id"]) for row in manifest["samples"]],
    }


class HlExpertAnnotationValidatorTests(unittest.TestCase):
    def validate_document(self, document):
        with tempfile.TemporaryDirectory() as temp_dir:
            annotations_path = Path(temp_dir) / "synthetic_annotations.json"
            annotations_path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
            return VALIDATOR.validate(MANIFEST_PATH, annotations_path)

    def test_clean_complete_synthetic_record_is_eligible(self):
        report = self.validate_document(clean_document())
        self.assertEqual(report["status"], "clean_eligible")
        self.assertEqual(report["expected_sample_count"], 16)
        self.assertEqual(report["received_annotation_count"], 16)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["ineligible_reasons"], [])
        self.assertEqual(report["trade_statistics"]["completed_trade_denominator"], 0)
        self.assertEqual(report["trade_statistics"]["validated_win_rate"], "not-computable")
        self.assertEqual(report["trade_statistics"]["conclusion"], "no-new-positive")

    def test_contamination_and_nonindependence_are_valid_but_ineligible(self):
        document = clean_document()
        document["annotator"]["independent"] = False
        document["freeze"]["source_or_model_hypotheses_seen_before_freeze"] = True
        document["freeze"]["knowledge_status"] = "contaminated"
        report = self.validate_document(document)
        self.assertEqual(report["status"], "valid_ineligible")
        self.assertEqual(report["errors"], [])
        self.assertEqual(
            set(report["ineligible_reasons"]),
            {
                "annotator is not independent",
                "freeze.source_or_model_hypotheses_seen_before_freeze=true",
                "knowledge_status=contaminated",
            },
        )

    def test_freeze_order_timezone_and_manifest_hash_are_hard_errors(self):
        document = clean_document()
        document["manifest_sha256"] = "0" * 64
        document["freeze"]["annotation_started_at"] = "2026-09-01T12:00:00"
        document["freeze"]["annotation_frozen_at"] = "2026-09-01T11:00:00+08:00"
        report = self.validate_document(document)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("manifest_sha256" in error for error in report["errors"]))
        self.assertTrue(any("timezone" in error for error in report["errors"]))

    def test_missing_duplicate_and_extra_sample_ids_are_rejected(self):
        document = clean_document()
        document["annotations"][0]["expert_sample_id"] = "EH1-002"
        document["annotations"][-1]["expert_sample_id"] = "EH1-999"
        report = self.validate_document(document)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("duplicate expert_sample_id", joined)
        self.assertIn("missing expert_sample_id", joined)
        self.assertIn("unexpected expert_sample_id", joined)

    def test_manifest_requires_exact_sixteen_well_formed_ids(self):
        manifest = read_json(MANIFEST_PATH)
        document = clean_document()
        manifest["samples"] = manifest["samples"][:-1]
        manifest["sample_count"] = 15
        document["annotations"] = document["annotations"][:-1]
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "synthetic_manifest.json"
            annotations_path = Path(temp_dir) / "synthetic_annotations.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            document["manifest_sha256"] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            annotations_path.write_text(json.dumps(document), encoding="utf-8")
            report = VALIDATOR.validate(manifest_path, annotations_path)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("exactly 16" in error for error in report["errors"]))

        manifest = read_json(MANIFEST_PATH)
        document = clean_document()
        manifest["samples"][0]["expert_sample_id"] = "EH1-bad"
        document["annotations"][0]["expert_sample_id"] = "EH1-bad"
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_path = Path(temp_dir) / "synthetic_manifest.json"
            annotations_path = Path(temp_dir) / "synthetic_annotations.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            document["manifest_sha256"] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            annotations_path.write_text(json.dumps(document), encoding="utf-8")
            report = VALIDATOR.validate(manifest_path, annotations_path)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("manifest.samples[0].expert_sample_id is invalid" in error for error in report["errors"]))

    def test_enum_confidence_and_reasoned_evidence_are_enforced(self):
        document = clean_document()
        row = document["annotations"][0]
        row["parent_state"] = "looks_bullish"
        row["confidence_1_to_5"] = 6
        row["B_leg_evidence"] = " "
        report = self.validate_document(document)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("parent_state", joined)
        self.assertIn("confidence_1_to_5", joined)
        self.assertIn("B_leg_evidence", joined)

    def test_ordinary_h_and_l_labels_require_direction_ema_lineage_and_control(self):
        document = clean_document()
        row = document["annotations"][0]
        row.update(
            {
                "parent_state": "open_trend",
                "direction": "long",
                "ema20_slope": "rising",
                "ema50_slope": "rising",
                "A_leg_quality": "strong",
                "B_leg_class": "controlled",
                "lineage_status": "same_lineage",
                "expert_ordinary_hl_label": "H1",
                "primary_exclusion": "not_applicable",
            }
        )
        self.assertEqual(self.validate_document(document)["status"], "clean_eligible")

        bad = copy.deepcopy(document)
        bad_row = bad["annotations"][0]
        bad_row["direction"] = "short"
        bad_row["ema50_slope"] = "falling"
        bad_row["lineage_status"] = "reset"
        bad_row["B_leg_class"] = "uncontrolled"
        report = self.validate_document(bad)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("H1/H2 requires long", joined)
        self.assertIn("same_lineage", joined)
        self.assertIn("controlled B leg", joined)

    def test_not_ordinary_and_unclear_labels_require_explicit_exclusion(self):
        document = clean_document()
        document["annotations"][0]["primary_exclusion"] = "not_applicable"
        document["annotations"][1]["expert_ordinary_hl_label"] = "unclear"
        document["annotations"][1]["primary_exclusion"] = "range_repeat"
        report = self.validate_document(document)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("not_ordinary_HL requires", joined)
        self.assertIn("unclear label requires", joined)

    def test_unusable_evidence_requires_insufficient_evidence_exclusion(self):
        document = clean_document()
        row = document["annotations"][0]
        row["evidence_usable"] = "no"
        row["expert_ordinary_hl_label"] = "unclear"
        row["primary_exclusion"] = "insufficient_evidence"
        self.assertEqual(self.validate_document(document)["status"], "clean_eligible")
        row["primary_exclusion"] = "range_repeat"
        self.assertEqual(self.validate_document(document)["status"], "invalid")

    def test_cli_exit_codes_and_read_only_behavior(self):
        manifest_hash_before = hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as temp_dir:
            annotations_path = Path(temp_dir) / "synthetic_annotations.json"
            annotations_path.write_text(json.dumps(clean_document()), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(VALIDATOR.main(["--manifest", str(MANIFEST_PATH), "--annotations", str(annotations_path)]), 0)
            contaminated = clean_document()
            contaminated["freeze"]["future_or_outcome_evidence_seen_before_freeze"] = True
            annotations_path.write_text(json.dumps(contaminated), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(VALIDATOR.main(["--manifest", str(MANIFEST_PATH), "--annotations", str(annotations_path)]), 2)
            invalid = clean_document()
            invalid["annotations"] = []
            annotations_path.write_text(json.dumps(invalid), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(VALIDATOR.main(["--manifest", str(MANIFEST_PATH), "--annotations", str(annotations_path)]), 1)
        self.assertEqual(hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(), manifest_hash_before)

    def test_schema_validator_and_policy_share_core_contract(self):
        schema = read_json(SCHEMA_PATH)
        annotation_properties = schema["properties"]["annotations"]["items"]["properties"]
        self.assertEqual(set(annotation_properties), VALIDATOR.ANNOTATION_FIELDS)
        self.assertEqual(schema["properties"]["annotations"]["minItems"], VALIDATOR.EXPECTED_SAMPLE_COUNT)
        self.assertEqual(schema["properties"]["annotations"]["maxItems"], VALIDATOR.EXPECTED_SAMPLE_COUNT)
        self.assertEqual(annotation_properties["expert_sample_id"]["pattern"], VALIDATOR.SAMPLE_ID_RE.pattern)
        for field_name, allowed in VALIDATOR.ENUMS.items():
            self.assertEqual(set(annotation_properties[field_name]["enum"]), allowed)
        policy = POLICY_PATH.read_text(encoding="utf-8")
        for token in (
            "clean_eligible",
            "valid_ineligible",
            "invalid",
            "experts_agree",
            "both_reasonable_boundary",
            "adjudicator_choice",
            "accuracy_denominator",
            "不得静默删除困难样本",
            "completed_trade_denominator: 0",
            "validated win-rate: not-computable",
            "conclusion: no-new-positive",
        ):
            self.assertIn(token, policy)

    def test_real_packet_remains_without_annotation_artifacts(self):
        self.assertFalse((PACKET_ROOT / "expert_annotations.json").exists())
        self.assertFalse((PACKET_ROOT / "expert_annotations.csv").exists())
        self.assertFalse(any("annotation" in path.name and path.suffix in {".json", ".csv"} for path in PACKET_ROOT.iterdir() if path.name != "annotation_schema_v1.json"))


if __name__ == "__main__":
    unittest.main()

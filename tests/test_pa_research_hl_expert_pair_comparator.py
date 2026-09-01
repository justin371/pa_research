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
ANNOTATION_SCHEMA_PATH = PACKET_ROOT / "annotation_schema_v1.json"
PAIR_SCHEMA_PATH = PACKET_ROOT / "pair_adjudication_schema_v1.json"
MAPPING_PATH = PACKET_ROOT / "transcription_mapping_v1.json"
MAPPING_DOC_PATH = PACKET_ROOT / "transcription_mapping_CN.md"
FORM_PATH = PACKET_ROOT / "annotation_form.md"
COMPARATOR_PATH = REPO_ROOT / "scripts" / "compare_pa_hl_expert_annotations.py"

SPEC = importlib.util.spec_from_file_location("hl_expert_pair_comparator", COMPARATOR_PATH)
COMPARATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = COMPARATOR
SPEC.loader.exec_module(COMPARATOR)


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


def clean_document(identifier: str):
    manifest = read_json(MANIFEST_PATH)
    return {
        "schema_version": "pa_hl_expert_annotations_v1",
        "packet_id": manifest["packet_id"],
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "annotator": {
            "role": "external_human_expert",
            "identifier": identifier,
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


class HlExpertPairComparatorTests(unittest.TestCase):
    def compare_documents(self, expert_a, expert_b):
        with tempfile.TemporaryDirectory() as temp_dir:
            expert_a_path = Path(temp_dir) / "synthetic_a.json"
            expert_b_path = Path(temp_dir) / "synthetic_b.json"
            expert_a_path.write_text(json.dumps(expert_a, ensure_ascii=False), encoding="utf-8")
            expert_b_path.write_text(json.dumps(expert_b, ensure_ascii=False), encoding="utf-8")
            return COMPARATOR.compare(MANIFEST_PATH, expert_a_path, expert_b_path)

    def test_two_clean_distinct_records_are_compared_without_adjudication(self):
        report = self.compare_documents(clean_document("synthetic-a"), clean_document("synthetic-b"))
        self.assertEqual(report["status"], "comparison_ready")
        self.assertEqual(len(report["sample_comparisons"]), 16)
        self.assertEqual(report["summary"]["clean_pair_comparison_count"], 16)
        self.assertEqual(report["summary"]["exact_all_field_agreement_count"], 16)
        self.assertEqual(report["summary"]["human_adjudication_records_created"], 0)
        self.assertEqual(report["summary"]["accuracy_denominator"], 0)
        self.assertEqual(report["trade_statistics"]["completed_trade_denominator"], 0)
        self.assertEqual(report["trade_statistics"]["validated_win_rate"], "not-computable")
        self.assertEqual(report["trade_statistics"]["conclusion"], "no-new-positive")
        for row in report["sample_comparisons"]:
            self.assertEqual(row["adjudication_state"], "not_recorded")
            self.assertIsNone(row["final_label"])
            self.assertFalse(row["accuracy_denominator_eligible"])

    def test_field_level_disagreements_are_exact_and_do_not_choose_a_label(self):
        expert_a = clean_document("synthetic-a")
        expert_b = clean_document("synthetic-b")
        row = expert_b["annotations"][0]
        row["confidence_1_to_5"] = 4
        row["main_uncertainty"] = "different synthetic uncertainty"
        row["primary_exclusion"] = "insufficient_space"
        report = self.compare_documents(expert_a, expert_b)
        first = report["sample_comparisons"][0]
        self.assertEqual(
            first["disagreement_fields"],
            ["primary_exclusion", "confidence_1_to_5", "main_uncertainty"],
        )
        self.assertFalse(first["label_and_exclusion_agree"])
        self.assertFalse(first["exact_all_field_agreement"])
        self.assertEqual(first["expert_a"]["primary_exclusion"], "range_repeat")
        self.assertEqual(first["expert_b"]["primary_exclusion"], "insufficient_space")
        self.assertIsNone(first["final_label"])
        self.assertEqual(report["summary"]["label_or_exclusion_disagreement_count"], 1)

    def test_single_record_validator_runs_before_pair_comparison(self):
        expert_a = clean_document("synthetic-a")
        expert_b = clean_document("synthetic-b")
        expert_b["annotations"] = []
        report = self.compare_documents(expert_a, expert_b)
        self.assertEqual(report["status"], "invalid")
        self.assertEqual(report["expert_a"]["single_record_validation"]["status"], "clean_eligible")
        self.assertEqual(report["expert_b"]["single_record_validation"]["status"], "invalid")
        self.assertEqual(report["sample_comparisons"], [])

    def test_contaminated_or_same_identifier_pair_is_ineligible_and_not_compared(self):
        expert_a = clean_document("same-person")
        expert_b = clean_document("same-person")
        expert_b["freeze"]["future_or_outcome_evidence_seen_before_freeze"] = True
        report = self.compare_documents(expert_a, expert_b)
        self.assertEqual(report["status"], "valid_ineligible")
        self.assertEqual(report["sample_comparisons"], [])
        self.assertIn("expert_b is not clean_eligible", report["pair_ineligible_reasons"])
        self.assertIn("expert identifiers are not distinct", report["pair_ineligible_reasons"])

    def test_cli_exit_codes_and_inputs_are_read_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            expert_a_path = Path(temp_dir) / "synthetic_a.json"
            expert_b_path = Path(temp_dir) / "synthetic_b.json"
            expert_a_path.write_text(json.dumps(clean_document("synthetic-a")), encoding="utf-8")
            expert_b_path.write_text(json.dumps(clean_document("synthetic-b")), encoding="utf-8")
            before = (hashlib.sha256(expert_a_path.read_bytes()).hexdigest(), hashlib.sha256(expert_b_path.read_bytes()).hexdigest())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    COMPARATOR.main(
                        [
                            "--manifest",
                            str(MANIFEST_PATH),
                            "--expert-a",
                            str(expert_a_path),
                            "--expert-b",
                            str(expert_b_path),
                        ]
                    ),
                    0,
                )
            expert_b = clean_document("synthetic-b")
            expert_b["annotator"]["independent"] = False
            expert_b_path.write_text(json.dumps(expert_b), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(COMPARATOR.main(["--manifest", str(MANIFEST_PATH), "--expert-a", str(expert_a_path), "--expert-b", str(expert_b_path)]), 2)
            expert_b["annotations"] = []
            expert_b_path.write_text(json.dumps(expert_b), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(COMPARATOR.main(["--manifest", str(MANIFEST_PATH), "--expert-a", str(expert_a_path), "--expert-b", str(expert_b_path)]), 1)
            self.assertEqual(hashlib.sha256(expert_a_path.read_bytes()).hexdigest(), before[0])

    def test_pair_schema_records_all_outcomes_and_denominator_boundary(self):
        schema = read_json(PAIR_SCHEMA_PATH)
        sample = schema["$defs"]["sampleAdjudication"]
        states = set(sample["properties"]["adjudication_state"]["enum"])
        self.assertEqual(
            states,
            {
                "experts_agree",
                "both_reasonable_boundary",
                "adjudicator_choice",
                "insufficient_evidence",
                "contaminated",
            },
        )
        disagreement_enum = set(sample["properties"]["comparison"]["properties"]["disagreement_fields"]["items"]["enum"])
        self.assertEqual(disagreement_enum, set(COMPARATOR.COMPARISON_FIELDS))
        self.assertEqual(schema["properties"]["samples"]["minItems"], 16)
        self.assertEqual(schema["properties"]["samples"]["maxItems"], 16)
        self.assertEqual(
            [
                item["allOf"][1]["properties"]["expert_sample_id"]["const"]
                for item in schema["properties"]["samples"]["prefixItems"]
            ],
            [f"EH1-{index:03d}" for index in range(1, 17)],
        )
        self.assertIs(schema["properties"]["samples"]["items"], False)
        summary = schema["properties"]["summary"]["properties"]
        self.assertEqual(summary["completed_trade_denominator"]["const"], 0)
        self.assertEqual(summary["validated_win_rate"]["const"], "not-computable")
        self.assertEqual(summary["conclusion"]["const"], "no-new-positive")

    def test_transcription_mapping_exactly_covers_form_and_annotation_schema(self):
        mapping = read_json(MAPPING_PATH)
        annotation_schema = read_json(ANNOTATION_SCHEMA_PATH)
        row_required = set(annotation_schema["properties"]["annotations"]["items"]["required"])
        mapped_rows = {entry["target"].removeprefix("annotations[].") for entry in mapping["annotation_fields"]}
        self.assertEqual(mapped_rows, row_required)
        self.assertEqual(len(mapping["annotation_fields"]), len(row_required))

        declaration_targets = {entry["target"] for entry in mapping["declaration_fields"]}
        expected_declarations = {
            "annotator.role",
            "annotator.identifier",
            "annotator.independent",
            "freeze.annotation_started_at",
            "freeze.annotation_frozen_at",
            "freeze.source_or_model_hypotheses_seen_before_freeze",
            "freeze.future_or_outcome_evidence_seen_before_freeze",
            "freeze.knowledge_status",
        }
        self.assertEqual(declaration_targets, expected_declarations)
        form = FORM_PATH.read_text(encoding="utf-8")
        for entry in mapping["declaration_fields"] + mapping["annotation_fields"]:
            self.assertIn(entry["source"], form)
        self.assertEqual(mapping["policy"], "exact_fields_only_no_inference")
        self.assertIn("fill_blank", mapping["forbidden_operations"])
        self.assertIn("infer_from_chart", mapping["forbidden_operations"])

    def test_synthetic_yes_no_and_verbatim_mapping_has_no_inference_branch(self):
        conversion = {"no": False, "yes": True}
        self.assertIs(conversion["no"], False)
        self.assertIs(conversion["yes"], True)
        for ambiguous in ("", "y", "probably", "是", "yes/no"):
            self.assertNotIn(ambiguous, conversion)
        synthetic_text = "synthetic: uncertain because left resistance is close"
        self.assertEqual(str(synthetic_text), synthetic_text)
        mapping_doc = MAPPING_DOC_PATH.read_text(encoding="utf-8")
        for token in (
            "annotation_form.md",
            "transcription_mapping_v1.json",
            "incomplete",
            "validator",
            "real annotations: 0",
            "no-new-positive",
        ):
            self.assertIn(token, mapping_doc)

    def test_real_packet_still_has_no_expert_records(self):
        prohibited = {
            "expert_annotations.json",
            "expert_annotations.csv",
            "expert_a.json",
            "expert_b.json",
            "pair_adjudication.json",
        }
        self.assertFalse(any((PACKET_ROOT / name).exists() for name in prohibited))


if __name__ == "__main__":
    unittest.main()

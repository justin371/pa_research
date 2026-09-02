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
PAIR_SCHEMA_PATH = PACKET_ROOT / "pair_adjudication_schema_v1.json"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_hl_expert_pair_adjudication.py"
POLICY_PATH = PACKET_ROOT / "adjudication_and_denominator_policy_CN.md"
AUDIT_PATH = REPO_ROOT / "research" / "hl_pair_adjudication_validator_audit_2026-09-01_CN.md"
RESEARCH_INDEX = REPO_ROOT / "research" / "README.md"
DOCS_VALIDATOR = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"

SPEC = importlib.util.spec_from_file_location("hl_pair_adjudication_validator", VALIDATOR_PATH)
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


def clean_expert_document(identifier: str):
    manifest = read_json(MANIFEST_PATH)
    return {
        "schema_version": "pa_hl_expert_annotations_v1",
        "packet_id": manifest["packet_id"],
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "annotator": {"role": "external_human_expert", "identifier": identifier, "independent": True},
        "freeze": {
            "annotation_started_at": "2026-09-01T10:00:00+08:00",
            "annotation_frozen_at": "2026-09-01T11:00:00+08:00",
            "source_or_model_hypotheses_seen_before_freeze": False,
            "future_or_outcome_evidence_seen_before_freeze": False,
            "knowledge_status": "clean",
        },
        "annotations": [synthetic_annotation(row["expert_sample_id"]) for row in manifest["samples"]],
    }


def build_adjudication(expert_a_path: Path, expert_b_path: Path):
    expert_a = read_json(expert_a_path)
    expert_b = read_json(expert_b_path)
    pair_report = VALIDATOR.COMPARATOR.compare(MANIFEST_PATH, expert_a_path, expert_b_path)
    assert pair_report["status"] == "comparison_ready"
    samples = []
    for comparison in pair_report["sample_comparisons"]:
        sample_id = comparison["expert_sample_id"]
        source_a = next(row for row in expert_a["annotations"] if row["expert_sample_id"] == sample_id)
        source_b = next(row for row in expert_b["annotations"] if row["expert_sample_id"] == sample_id)
        samples.append(
            {
                "expert_sample_id": sample_id,
                "expert_a": {field: source_a[field] for field in VALIDATOR.SNAPSHOT_FIELDS},
                "expert_b": {field: source_b[field] for field in VALIDATOR.SNAPSHOT_FIELDS},
                "comparison": {
                    "label_and_exclusion_agree": comparison["label_and_exclusion_agree"],
                    "disagreement_fields": comparison["disagreement_fields"],
                },
                "adjudication_state": "experts_agree",
                "adjudicator": None,
                "final_label": source_a["expert_ordinary_hl_label"],
                "rationale": "synthetic exact agreement",
                "accuracy_eligibility": {
                    "model_prediction_frozen_before_expert_reveal": False,
                    "model_prediction_label": None,
                    "eligible": False,
                    "excluded_reason": "model_prediction_missing",
                },
            }
        )
    return {
        "schema_version": "pa_hl_expert_pair_adjudication_v1",
        "packet_id": expert_a["packet_id"],
        "manifest_sha256": expert_a["manifest_sha256"],
        "expert_pair": {
            "expert_a": {
                "record_sha256": hashlib.sha256(expert_a_path.read_bytes()).hexdigest(),
                "annotator_identifier": expert_a["annotator"]["identifier"],
                "single_record_validator_status": "clean_eligible",
            },
            "expert_b": {
                "record_sha256": hashlib.sha256(expert_b_path.read_bytes()).hexdigest(),
                "annotator_identifier": expert_b["annotator"]["identifier"],
                "single_record_validator_status": "clean_eligible",
            },
            "distinct_identifiers": True,
        },
        "adjudication_freeze": {
            "comparison_frozen_at": "2026-09-01T11:10:00+08:00",
            "adjudication_started_at": "2026-09-01T11:15:00+08:00",
            "adjudication_frozen_at": "2026-09-01T12:00:00+08:00",
            "source_or_model_hypotheses_seen_before_freeze": False,
            "future_or_outcome_evidence_seen_before_freeze": False,
            "knowledge_status": "clean",
        },
        "samples": samples,
        "summary": {
            "packet_total": 16,
            "clean_expert_pair_count": 16,
            "adjudicated_single_label_count": 16,
            "boundary_or_unclear_count": 0,
            "contaminated_count": 0,
            "model_prediction_coverage": 0,
            "accuracy_denominator": 0,
            "excluded_reasons": {"model_prediction_missing": 16},
            "completed_trade_denominator": 0,
            "validated_win_rate": "not-computable",
            "conclusion": "no-new-positive",
        },
    }


class HlPairAdjudicationValidatorTests(unittest.TestCase):
    def fixture(self, mutate_experts=None):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        expert_a = clean_expert_document("synthetic-a")
        expert_b = clean_expert_document("synthetic-b")
        if mutate_experts is not None:
            mutate_experts(expert_a, expert_b)
        expert_a_path = root / "synthetic_a.json"
        expert_b_path = root / "synthetic_b.json"
        adjudication_path = root / "synthetic_pair_adjudication.json"
        expert_a_path.write_text(json.dumps(expert_a, ensure_ascii=False), encoding="utf-8")
        expert_b_path.write_text(json.dumps(expert_b, ensure_ascii=False), encoding="utf-8")
        adjudication = build_adjudication(expert_a_path, expert_b_path)
        return temp_dir, expert_a_path, expert_b_path, adjudication_path, adjudication

    def validate_document(self, mutate_record=None, mutate_experts=None):
        temp_dir, expert_a_path, expert_b_path, adjudication_path, adjudication = self.fixture(mutate_experts)
        try:
            if mutate_record is not None:
                mutate_record(adjudication)
            adjudication_path.write_text(json.dumps(adjudication, ensure_ascii=False), encoding="utf-8")
            return VALIDATOR.validate(MANIFEST_PATH, expert_a_path, expert_b_path, adjudication_path)
        finally:
            temp_dir.cleanup()

    def test_clean_synthetic_pair_adjudication_is_valid_and_recomputed(self):
        report = self.validate_document()
        self.assertEqual(report["status"], "valid")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["ineligible_reasons"], [])
        self.assertEqual(report["recomputed_summary"]["packet_total"], 16)
        self.assertEqual(report["recomputed_summary"]["accuracy_denominator"], 0)
        self.assertEqual(report["recomputed_summary"]["excluded_reasons"], {"model_prediction_missing": 16})
        self.assertEqual(report["records_created_or_modified"], 0)
        self.assertEqual(report["trade_statistics"]["validated_win_rate"], "not-computable")

    def test_source_record_hash_identifier_and_snapshot_are_immutable(self):
        def mutate(record):
            record["expert_pair"]["expert_a"]["record_sha256"] = "0" * 64
            record["expert_pair"]["expert_b"]["annotator_identifier"] = "invented"
            record["samples"][0]["expert_a"]["primary_exclusion"] = "insufficient_space"

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("record_sha256", joined)
        self.assertIn("annotator_identifier", joined)
        self.assertIn("does not match source expert record", joined)

    def test_comparison_and_ordered_ids_must_match_the_read_only_comparator(self):
        def mutate(record):
            record["samples"][0]["comparison"]["disagreement_fields"] = ["main_uncertainty"]
            record["samples"][1]["expert_sample_id"] = "EH1-001"

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("does not exactly match comparator", joined)
        self.assertIn("must equal 'EH1-002'", joined)

    def test_freeze_order_and_timezone_are_hard_errors(self):
        def mutate(record):
            freeze = record["adjudication_freeze"]
            freeze["comparison_frozen_at"] = "2026-09-01T10:30:00+08:00"
            freeze["adjudication_started_at"] = "2026-09-01T10:15:00"
            freeze["adjudication_frozen_at"] = "2026-09-01T10:00:00+08:00"

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("must not precede either expert", joined)
        self.assertIn("timezone", joined)

    def test_global_contamination_is_valid_ineligible_when_all_denominators_recompute(self):
        def mutate(record):
            record["adjudication_freeze"]["knowledge_status"] = "contaminated"
            for row in record["samples"]:
                row["accuracy_eligibility"]["excluded_reason"] = "pair_not_clean"
            record["summary"]["clean_expert_pair_count"] = 0
            record["summary"]["excluded_reasons"] = {"pair_not_clean": 16}

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "valid_ineligible")
        self.assertEqual(report["errors"], [])
        self.assertIn("adjudication knowledge_status=contaminated", report["ineligible_reasons"])

    def test_agreement_cannot_invent_or_repair_a_final_label(self):
        def mutate(record):
            record["samples"][0]["final_label"] = "H1"

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("final_label must equal both frozen expert labels" in error for error in report["errors"]))

    def test_boundary_insufficient_and_contaminated_states_forbid_final_labels(self):
        states = ("insufficient_evidence", "contaminated")
        for state in states:
            with self.subTest(state=state):
                def mutate(record, state=state):
                    record["samples"][0]["adjudication_state"] = state
                    record["samples"][0]["final_label"] = None
                    reason = {
                        "both_reasonable_boundary": "boundary_or_unclear",
                        "insufficient_evidence": "insufficient_evidence",
                        "contaminated": "contaminated",
                    }[state]
                    record["samples"][0]["accuracy_eligibility"]["excluded_reason"] = reason
                    record["summary"]["adjudicated_single_label_count"] = 15
                    record["summary"]["boundary_or_unclear_count"] = int(state != "contaminated")
                    record["summary"]["contaminated_count"] = int(state == "contaminated")
                    record["summary"]["clean_expert_pair_count"] = 15 if state == "contaminated" else 16
                    record["summary"]["excluded_reasons"] = {"model_prediction_missing": 15, reason: 1}

                report = self.validate_document(mutate)
                self.assertEqual(report["status"], "valid", report["errors"])

    def test_boundary_rejects_same_labels_and_accepts_real_disagreement(self):
        def make_boundary(record):
            record["samples"][0]["adjudication_state"] = "both_reasonable_boundary"
            record["samples"][0]["final_label"] = None
            record["samples"][0]["accuracy_eligibility"]["excluded_reason"] = "boundary_or_unclear"
            record["summary"]["adjudicated_single_label_count"] = 15
            record["summary"]["boundary_or_unclear_count"] = 1
            record["summary"]["clean_expert_pair_count"] = 16
            record["summary"]["excluded_reasons"] = {
                "model_prediction_missing": 15,
                "boundary_or_unclear": 1,
            }

        same_label_report = self.validate_document(make_boundary)
        self.assertEqual(same_label_report["status"], "invalid")
        self.assertTrue(
            any("requires label/exclusion disagreement" in error for error in same_label_report["errors"])
        )

        def make_real_disagreement(expert_a, expert_b):
            del expert_a
            expert_b["annotations"][0].update(
                {
                    "parent_state": "open_trend",
                    "direction": "long",
                    "ema20_slope": "rising",
                    "ema50_slope": "rising",
                    "ema200_context": "supportive",
                    "A_leg_quality": "strong",
                    "B_leg_class": "controlled",
                    "lineage_status": "same_lineage",
                    "expert_ordinary_hl_label": "H1",
                    "primary_exclusion": "not_applicable",
                }
            )

        real_disagreement_report = self.validate_document(make_boundary, make_real_disagreement)
        self.assertEqual(real_disagreement_report["status"], "valid", real_disagreement_report["errors"])

    def test_summary_accepts_finite_integral_float_counts(self):
        def mutate(record):
            record["summary"]["clean_expert_pair_count"] = 16.0
            record["summary"]["excluded_reasons"]["model_prediction_missing"] = 16.0

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "valid", report["errors"])

    def test_adjudicator_choice_requires_clean_distinct_third_human(self):
        def mutate(record):
            row = record["samples"][0]
            row["adjudication_state"] = "adjudicator_choice"
            row["adjudicator"] = {
                "role": "external_human_adjudicator",
                "identifier": "synthetic-a",
                "independent_of_expert_a_and_b": True,
                "source_or_model_hypotheses_seen_before_freeze": False,
                "future_or_outcome_evidence_seen_before_freeze": False,
                "knowledge_status": "clean",
            }

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "invalid")
        self.assertTrue(any("distinct from both source experts" in error for error in report["errors"]))

    def test_frozen_model_prediction_can_enter_recomputed_accuracy_denominator(self):
        def mutate(record):
            eligibility = record["samples"][0]["accuracy_eligibility"]
            eligibility["model_prediction_frozen_before_expert_reveal"] = True
            eligibility["model_prediction_label"] = "not_ordinary_HL"
            eligibility["eligible"] = True
            eligibility["excluded_reason"] = None
            record["summary"]["model_prediction_coverage"] = 1
            record["summary"]["accuracy_denominator"] = 1
            record["summary"]["excluded_reasons"] = {"model_prediction_missing": 15}

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "valid", report["errors"])
        self.assertEqual(report["recomputed_summary"]["accuracy_denominator"], 1)

    def test_summary_tampering_is_rejected(self):
        def mutate(record):
            record["summary"]["accuracy_denominator"] = 16
            record["summary"]["validated_win_rate"] = "60%"

        report = self.validate_document(mutate)
        self.assertEqual(report["status"], "invalid")
        joined = "\n".join(report["errors"])
        self.assertIn("summary.accuracy_denominator", joined)
        self.assertIn("summary.validated_win_rate", joined)

    def test_ineligible_source_expert_pair_is_rejected_before_adjudication(self):
        def mutate_experts(_expert_a, expert_b):
            expert_b["annotator"]["independent"] = False

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            expert_a = clean_expert_document("synthetic-a")
            expert_b = clean_expert_document("synthetic-b")
            mutate_experts(expert_a, expert_b)
            a_path = root / "a.json"
            b_path = root / "b.json"
            pair_path = root / "pair.json"
            a_path.write_text(json.dumps(expert_a), encoding="utf-8")
            b_path.write_text(json.dumps(expert_b), encoding="utf-8")
            pair_path.write_text("{}", encoding="utf-8")
            report = VALIDATOR.validate(MANIFEST_PATH, a_path, b_path, pair_path)
        self.assertEqual(report["status"], "invalid")
        self.assertIn("source expert pair is not comparison_ready", report["errors"][0])

    def test_cli_exit_codes_and_read_only_inputs(self):
        temp_dir, a_path, b_path, pair_path, record = self.fixture()
        try:
            pair_path.write_text(json.dumps(record), encoding="utf-8")
            before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in (a_path, b_path, pair_path)}
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(VALIDATOR.main(["--manifest", str(MANIFEST_PATH), "--expert-a", str(a_path), "--expert-b", str(b_path), "--adjudication", str(pair_path)]), 0)
            contaminated = copy.deepcopy(record)
            contaminated["adjudication_freeze"]["knowledge_status"] = "uncertain"
            for row in contaminated["samples"]:
                row["accuracy_eligibility"]["excluded_reason"] = "pair_not_clean"
            contaminated["summary"]["clean_expert_pair_count"] = 0
            contaminated["summary"]["excluded_reasons"] = {"pair_not_clean": 16}
            pair_path.write_text(json.dumps(contaminated), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(VALIDATOR.main(["--manifest", str(MANIFEST_PATH), "--expert-a", str(a_path), "--expert-b", str(b_path), "--adjudication", str(pair_path)]), 2)
            invalid = copy.deepcopy(record)
            invalid["samples"] = []
            pair_path.write_text(json.dumps(invalid), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(VALIDATOR.main(["--manifest", str(MANIFEST_PATH), "--expert-a", str(a_path), "--expert-b", str(b_path), "--adjudication", str(pair_path)]), 1)
            self.assertEqual(hashlib.sha256(a_path.read_bytes()).hexdigest(), before[a_path.name])
            self.assertEqual(hashlib.sha256(b_path.read_bytes()).hexdigest(), before[b_path.name])
        finally:
            temp_dir.cleanup()

    def test_schema_and_validator_share_state_and_summary_contracts(self):
        schema = read_json(PAIR_SCHEMA_PATH)
        sample = schema["$defs"]["sampleAdjudication"]
        self.assertEqual(set(sample["properties"]["adjudication_state"]["enum"]), VALIDATOR.ADJUDICATION_STATES)
        self.assertEqual(set(schema["properties"]["summary"]["required"]), VALIDATOR.SUMMARY_FIELDS)
        excluded = schema["$defs"]["accuracyEligibility"]["properties"]["excluded_reason"]["oneOf"][0]["enum"]
        self.assertEqual(set(excluded), VALIDATOR.EXCLUDED_REASONS)

    def test_repository_contains_no_real_pair_adjudication_record(self):
        self.assertFalse((PACKET_ROOT / "pair_adjudication.json").exists())
        self.assertFalse((PACKET_ROOT / "expert_a.json").exists())
        self.assertFalse((PACKET_ROOT / "expert_b.json").exists())

    def test_policy_audit_and_index_register_read_only_validator_boundary(self):
        policy = POLICY_PATH.read_text(encoding="utf-8")
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("validate_pa_hl_expert_pair_adjudication.py", policy)
        self.assertIn("sample contaminated", policy)
        self.assertIn("summary 必须从 16 行重新计数", policy)
        self.assertIn(AUDIT_PATH.name, RESEARCH_INDEX.read_text(encoding="utf-8"))
        self.assertIn("research/hl_pair_adjudication_validator_audit_2026-09-01_CN.md", DOCS_VALIDATOR.read_text(encoding="utf-8"))
        for token in (
            "real pair adjudication artifacts: 0",
            "records_created_or_modified=0",
            "no-new-positive",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit)


if __name__ == "__main__":
    unittest.main()

from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = REPO_ROOT / "research"
REVIEWS_PATH = RESEARCH_ROOT / "morphology_calibration_blind_reviews_2026-09-01.json"
ADJUDICATION_PATH = RESEARCH_ROOT / "morphology_calibration_blind_adjudication_2026-09-01.json"
METRICS_PATH = RESEARCH_ROOT / "morphology_calibration_metrics_2026-09-01.json"
AUDIT_PATH = RESEARCH_ROOT / "morphology_calibration_adjudication_audit_2026-09-01_CN.md"
COHORT_ROOT = (
    RESEARCH_ROOT
    / "assets"
    / "visual_recognition"
    / "2026-09-01"
    / "morphology_calibration_candidate_v1"
)

PAIR_FIELDS = (
    "parent_state",
    "direction",
    "a_leg_quality",
    "b_leg_class",
    "visual_family",
    "attempt_label",
    "three_push_variant",
    "ema_gate",
    "stage_1_status",
    "selection_disposition",
)
EXPECTED_REVIEWS_SHA256 = "0f290849431ed2f246be08de9526b4fa58e7453b98af21b9f6a7a5299200d160"
EXPECTED_ADJUDICATION_SHA256 = "101b7e6da4d0d11f04ffc5bf1e52f3bdf1efb1857d1d727a5aec8b7b1ceefa40"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_metric(exact: int, denominator: int) -> dict:
    return {
        "denominator": denominator,
        "exact_agreements": exact,
        "rate": float(
            (Decimal(exact) / Decimal(denominator)).quantize(
                Decimal("0.0001"),
                rounding=ROUND_HALF_UP,
            )
        ),
    }


class MorphologyCalibrationAdjudicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reviews_doc = load_json(REVIEWS_PATH)
        cls.adjudication_doc = load_json(ADJUDICATION_PATH)
        cls.metrics = load_json(METRICS_PATH)
        cls.reviews = cls.reviews_doc["reviews"]
        cls.adjudications = cls.adjudication_doc["adjudications"]

    def test_frozen_records_have_declared_hashes_and_pre_answer_order(self):
        self.assertEqual(sha256(REVIEWS_PATH), EXPECTED_REVIEWS_SHA256)
        self.assertEqual(sha256(ADJUDICATION_PATH), EXPECTED_ADJUDICATION_SHA256)
        self.assertEqual(self.metrics["blind_reviews_sha256"], EXPECTED_REVIEWS_SHA256)
        self.assertEqual(
            self.metrics["blind_adjudication_sha256"],
            EXPECTED_ADJUDICATION_SHA256,
        )
        self.assertFalse(self.reviews_doc["answer_key_opened_before_freeze"])
        self.assertFalse(self.adjudication_doc["answer_key_opened_before_freeze"])
        self.assertFalse(self.reviews_doc["future_or_outcome_evidence_used"])
        self.assertEqual(
            self.adjudication_doc["blind_reviews_sha256"],
            EXPECTED_REVIEWS_SHA256,
        )

    def test_review_and_adjudication_cardinality_and_eligibility(self):
        grouped = defaultdict(list)
        for review in self.reviews:
            grouped[review["sample_id"]].append(review)
            self.assertEqual(review["knowledge_status"], "clean")
        self.assertEqual(len(self.reviews), 32)
        self.assertEqual(len(grouped), 16)
        self.assertEqual({len(rows) for rows in grouped.values()}, {2})
        self.assertEqual(len(self.adjudications), 16)
        self.assertEqual(
            {row["sample_id"] for row in self.adjudications},
            set(grouped),
        )
        for row in self.adjudications:
            self.assertEqual(row["adjudicator_knowledge_status"], "clean")
            self.assertEqual(row["eligibility"], "strict_eligible")
        self.assertEqual(
            Counter(row["decision"] for row in self.adjudications),
            Counter(
                {
                    "both_reasonable_boundary": 12,
                    "reviewers_agree": 1,
                    "adjudicator_choice": 3,
                }
            ),
        )

    def test_pair_and_reviewer_to_adjudication_metrics_recompute_exactly(self):
        grouped = defaultdict(list)
        for review in self.reviews:
            grouped[review["sample_id"]].append(review)
        adjudication_by_id = {
            row["sample_id"]: row for row in self.adjudications
        }

        pair_metrics = {}
        reviewer_to_adjudication_metrics = {}
        for field in PAIR_FIELDS:
            pair_exact = sum(
                rows[0][field] == rows[1][field]
                for rows in grouped.values()
            )
            pair_metrics[field] = field_metric(pair_exact, 16)
            adjudication_exact = sum(
                review[field]
                == adjudication_by_id[review["sample_id"]][field]
                for review in self.reviews
            )
            reviewer_to_adjudication_metrics[field] = field_metric(
                adjudication_exact,
                32,
            )

        self.assertEqual(
            pair_metrics,
            self.metrics["reviewer_pair_field_agreement"],
        )
        self.assertEqual(
            reviewer_to_adjudication_metrics,
            self.metrics["reviewer_to_adjudication_field_agreement"],
        )
        self.assertEqual(
            dict(Counter(row["decision"] for row in self.adjudications)),
            self.metrics["adjudication_decisions"],
        )

    def test_candidate_hypothesis_confusion_and_boundaries_recompute(self):
        comparison = self.metrics["candidate_source_comparison"]
        samples = comparison["samples"]
        family_confusion = defaultdict(Counter)
        hl_confusion = defaultdict(Counter)
        hl_exact = 0
        hl_total = 0
        three_push_exact = 0
        three_push_total = 0
        negative_not_deep = 0
        negative_total = 0

        for sample in samples:
            family_confusion[sample["candidate_family"]][
                sample["adjudicated_visual_family"]
            ] += 1
            if sample["candidate_family"] == "H_L_like":
                hl_total += 1
                hl_exact += bool(sample["hl_attempt_exact"])
                source_attempt = sample["candidate_label"].split("_event", 1)[0]
                source_attempt = source_attempt.split("_expansion", 1)[0]
                source_attempt = source_attempt.split("_transition", 1)[0]
                hl_confusion[source_attempt][
                    sample["adjudicated_attempt_label"]
                ] += 1
            elif sample["candidate_family"] == "THREE_PUSH_like":
                three_push_total += 1
                three_push_exact += bool(sample["family_exact"])
            elif sample["candidate_family"] == "NEGATIVE_CONTROL":
                negative_total += 1
                negative_not_deep += bool(
                    sample["negative_control_not_deep_reviewed"]
                )

        self.assertEqual(
            {key: dict(value) for key, value in family_confusion.items()},
            comparison["family_confusion_matrix"],
        )
        self.assertEqual(
            {key: dict(value) for key, value in hl_confusion.items()},
            comparison["hl_attempt_confusion_matrix"],
        )
        self.assertEqual(
            {"numerator": hl_exact, "denominator": hl_total},
            comparison["hl_attempt_exact"],
        )
        self.assertEqual(
            {"numerator": three_push_exact, "denominator": three_push_total},
            comparison["three_push_family_exact"],
        )
        self.assertEqual(
            {"numerator": negative_not_deep, "denominator": negative_total},
            comparison["negative_control_not_deep_reviewed"],
        )
        self.assertIn("not ground truth", comparison["warning"])

    def test_audit_and_reviewer_package_preserve_interpretation_boundary(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for token in (
            "模型视觉裁决",
            "不是外部人工专家复核",
            "16/16",
            "12 个裁决为 `both_reasonable_boundary`",
            "1/8",
            "3/4",
            "4/4",
            "completed_trade_denominator: 0",
            "validated win-rate: not-computable",
            "conclusion: no-new-positive",
            "PA Research only",
            "不修改 Codex Trading",
            "不创建量化扫描器",
            "不连接 Execution Agent",
        ):
            self.assertIn(token, audit)

        reviewer_facing_text = (
            (COHORT_ROOT / "README.md").read_text(encoding="utf-8")
            + (COHORT_ROOT / "review_form.md").read_text(encoding="utf-8")
        ).lower()
        for forbidden in (
            "morphology_calibration_adjudication",
            "morphology_calibration_metrics",
            "answer_key",
        ):
            self.assertNotIn(forbidden, reviewer_facing_text)

    def test_trade_statistics_remain_not_computable(self):
        self.assertEqual(
            self.metrics["trade_statistics"],
            {
                "completed_trade_denominator": 0,
                "validated_win_rate": "not-computable",
                "conclusion": "no-new-positive",
            },
        )


if __name__ == "__main__":
    unittest.main()

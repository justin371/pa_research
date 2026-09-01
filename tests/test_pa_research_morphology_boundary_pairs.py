import hashlib
import json
from collections import Counter
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = REPO_ROOT / "research" / "calibration" / "morphology_boundary_pairs_v1"
MANIFEST_PATH = PACKET_ROOT / "manifest.json"
README_PATH = PACKET_ROOT / "README.md"
REVIEW_FORM_PATH = PACKET_ROOT / "review_form.md"
REVIEWS_PATH = REPO_ROOT / "research" / "morphology_boundary_pairs_normalized_blind_reviews_2026-09-01.json"
METRICS_PATH = REPO_ROOT / "research" / "morphology_boundary_pairs_metrics_2026-09-01.json"
EXPECTED_MANIFEST_SHA256 = "8cfa9ce927718bd60daa6aee640f86ebab92d33c323879859b7f6c6ebc3deaed"
EXPECTED_REVIEWS_SHA256 = "fa8e7251479159879fcd5320ece8cbe8f6d80dd13af6dde000e3ee9401bcd54e"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class MorphologyBoundaryPairsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read_json(MANIFEST_PATH)

    def test_manifest_is_a_frozen_reused_calibration_packet_not_holdout(self):
        self.assertEqual(
            hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
            EXPECTED_MANIFEST_SHA256,
        )
        manifest = self.manifest
        self.assertEqual(manifest["selection_mode"], "curated_from_prior_blind_boundary_evidence")
        self.assertEqual(manifest["evidence_role"], "calibration_not_holdout_not_accuracy_test")
        self.assertTrue(manifest["selection_frozen_before_current_review"])
        self.assertTrue(manifest["reuses_prior_blind_images"])
        self.assertTrue(manifest["label_hidden"])
        self.assertTrue(manifest["outcome_hidden"])
        self.assertTrue(manifest["future_bars_hidden"])
        self.assertEqual(manifest["pair_count"], 6)
        self.assertEqual(manifest["sample_count"], 12)

    def test_every_pair_has_two_unique_existing_neutral_charts(self):
        samples = self.manifest["samples"]
        self.assertEqual(len(samples), 12)
        self.assertEqual(len({sample["packet_sample_id"] for sample in samples}), 12)
        self.assertEqual(len({sample["chart_path"] for sample in samples}), 12)
        self.assertEqual(Counter(sample["pair_id"] for sample in samples), Counter({f"PB1-{n:03d}": 2 for n in range(1, 7)}))
        for sample in samples:
            with self.subTest(sample=sample["packet_sample_id"]):
                path = REPO_ROOT / sample["chart_path"]
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 100_000)
                self.assertRegex(sample["source_sample_id"], r"^(?:BH1|MC2)-\d{3}$")

    def test_manifest_contains_no_answer_or_outcome_fields(self):
        forbidden = {
            "symbol",
            "cutoff_date",
            "candidate_family",
            "candidate_label",
            "direction",
            "a_leg_quality",
            "b_leg_class",
            "visual_family",
            "attempt_label",
            "outcome",
            "result",
            "win_rate",
        }
        for sample in self.manifest["samples"]:
            self.assertFalse(forbidden.intersection(sample), sample["packet_sample_id"])

    def test_reviewer_docs_preserve_freeze_order_and_boundaries(self):
        readme = README_PATH.read_text(encoding="utf-8")
        form = REVIEW_FORM_PATH.read_text(encoding="utf-8")
        for token in (
            "不是新 holdout",
            "逐图标签冻结后",
            "不把 pair 中任一张预设为“正确例”",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no automatic pattern detector",
            "no Futu/OpenD",
            "no Execution Agent",
            "conclusion: no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, readme)
        self.assertIn("labels_frozen_first", form)
        self.assertIn("why_not_same_route", form)

    def test_normalized_reviews_are_complete_clean_and_pair_ordered(self):
        self.assertEqual(hashlib.sha256(REVIEWS_PATH.read_bytes()).hexdigest(), EXPECTED_REVIEWS_SHA256)
        document = read_json(REVIEWS_PATH)
        self.assertTrue(document["selection_frozen_before_current_review"])
        self.assertTrue(document["individual_labels_frozen_before_pair_contrast"])
        self.assertFalse(document["old_answers_or_outcomes_opened_before_freeze"])
        self.assertFalse(document["future_or_outcome_evidence_used"])
        self.assertEqual(document["human_expert_status"], "not_performed")
        self.assertEqual(len(document["reviews"]), 24)
        self.assertEqual(len(document["pair_contrasts"]), 12)
        for sample in self.manifest["samples"]:
            pair = [r for r in document["reviews"] if r["packet_sample_id"] == sample["packet_sample_id"]]
            self.assertEqual(len(pair), 2, sample["packet_sample_id"])
            self.assertEqual(len({r["reviewer_id"] for r in pair}), 2)
            self.assertTrue(all(r["knowledge_status"] == "clean" for r in pair))
        self.assertTrue(all(row["labels_frozen_first"] for row in document["pair_contrasts"]))

    def test_metrics_recompute_and_do_not_claim_accuracy_or_trades(self):
        document = read_json(REVIEWS_PATH)
        metrics = read_json(METRICS_PATH)
        grouped = {
            sample_id: [r for r in document["reviews"] if r["packet_sample_id"] == sample_id]
            for sample_id in {r["packet_sample_id"] for r in document["reviews"]}
        }
        for field, recorded in metrics["reviewer_pair_field_agreement"].items():
            exact = sum(pair[0][field] == pair[1][field] for pair in grouped.values())
            self.assertEqual(recorded["denominator"], 12)
            self.assertEqual(recorded["exact_agreements"], exact)
            self.assertAlmostEqual(recorded["rate"], exact / 12, places=4)
        mutual_h_l = sum(pair[0]["visual_family"] == pair[1]["visual_family"] == "H_L_like" for pair in grouped.values())
        self.assertEqual(mutual_h_l, 0)
        self.assertEqual(metrics["routing_observations"]["mutual_h_l_like_samples"], 0)
        self.assertEqual(metrics["pair_route_contrast"]["exact_agreements"], 5)
        self.assertEqual(metrics["pair_route_contrast"]["denominator"], 6)
        self.assertEqual(metrics["ground_truth"]["overall_accuracy"], "not-computable")
        self.assertEqual(metrics["trade_statistics"]["completed_trade_denominator"], 0)
        self.assertEqual(metrics["trade_statistics"]["validated_win_rate"], "not-computable")
        self.assertEqual(metrics["trade_statistics"]["conclusion"], "no-new-positive")


if __name__ == "__main__":
    unittest.main()

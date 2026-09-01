import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
COHORT_ROOT = (
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-09-01"
    / "morphology_boundary_holdout_v1"
)
MANIFEST_PATH = COHORT_ROOT / "manifest.json"
README_PATH = COHORT_ROOT / "README.md"
REVIEW_FORM_PATH = COHORT_ROOT / "review_form.md"
REVIEWS_PATH = REPO_ROOT / "research" / "morphology_boundary_holdout_blind_reviews_2026-09-01.json"
METRICS_PATH = REPO_ROOT / "research" / "morphology_boundary_holdout_metrics_2026-09-01.json"
PRIOR_MANIFEST_PATHS = (
    COHORT_ROOT.parent / "selection_quality_blind_batch1" / "manifest.json",
    COHORT_ROOT.parent / "morphology_calibration_candidate_v1" / "manifest.json",
)
RENDERER_PATH = REPO_ROOT / "scripts" / "render_pa_blind_daily_batch.py"
EXPECTED_MANIFEST_SHA256 = "13d82d0065f4c1acc73f3e065e1412651cda63c252a66a82e0d7e0a0421c38dd"
EXPECTED_REVIEWS_SHA256 = "c818f536ce6b38f04e57579bc15902773dd6434d8ca6ded72fd5a9dc531bdbfc"
PNG_TOKEN_RE = re.compile(r"(?<![\w.-])([A-Za-z0-9][\w.-]*\.png)(?![\w.-])", re.I)

SPEC = importlib.util.spec_from_file_location("holdout_renderer", RENDERER_PATH)
RENDERER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = RENDERER
SPEC.loader.exec_module(RENDERER)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class MorphologyBoundaryHoldoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read_json(MANIFEST_PATH)

    def test_manifest_was_frozen_with_strict_blind_boundaries(self):
        self.assertEqual(
            hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
            EXPECTED_MANIFEST_SHA256,
        )
        manifest = self.manifest
        self.assertEqual(manifest["cohort_id"], "deterministic_boundary_holdout")
        self.assertEqual(manifest["selection_mode"], "deterministic_cutoff")
        self.assertEqual(manifest["selection_seed"], "pa-morph-boundary-holdout-v1")
        self.assertTrue(manifest["selection_frozen_before_view"])
        self.assertTrue(manifest["label_hidden"])
        self.assertTrue(manifest["outcome_hidden"])
        self.assertTrue(manifest["future_bars_hidden"])
        self.assertGreaterEqual(manifest["minimum_context_bars"], 500)
        self.assertGreaterEqual(manifest["minimum_hidden_future_bars"], 40)
        self.assertEqual(len(manifest["samples"]), 12)

    def test_every_cutoff_recomputes_and_has_required_context_and_future(self):
        manifest = self.manifest
        for sample in manifest["samples"]:
            with self.subTest(sample=sample["sample_id"]):
                bars = RENDERER.load_symbol_bars(
                    REPO_ROOT / sample["price_file"],
                    sample["symbol"],
                )
                cutoff_index = RENDERER.deterministic_index(
                    sample["symbol"],
                    len(bars),
                    manifest["selection_seed"],
                    manifest["minimum_context_bars"],
                    manifest["minimum_hidden_future_bars"],
                )
                self.assertEqual(
                    bars[cutoff_index].session_date.isoformat(),
                    sample["cutoff_date"],
                )
                self.assertGreaterEqual(
                    cutoff_index + 1,
                    manifest["minimum_context_bars"],
                )
                self.assertGreaterEqual(
                    len(bars) - cutoff_index - 1,
                    manifest["minimum_hidden_future_bars"],
                )

    def test_exact_symbol_date_samples_do_not_overlap_prior_blind_cohorts(self):
        current = {
            (sample["symbol"], sample["cutoff_date"])
            for sample in self.manifest["samples"]
        }
        prior = {
            (sample["symbol"], sample["cutoff_date"])
            for path in PRIOR_MANIFEST_PATHS
            for sample in read_json(path)["samples"]
        }
        self.assertEqual(len(current), 12)
        self.assertTrue(current.isdisjoint(prior))

    def test_reviewer_inventory_matches_manifest_and_disk(self):
        expected = {
            sample["chart_file"] for sample in self.manifest["samples"]
        }
        self.assertEqual(
            set(PNG_TOKEN_RE.findall(README_PATH.read_text(encoding="utf-8"))),
            expected,
        )
        self.assertEqual({path.name for path in COHORT_ROOT.glob("*.png")}, expected)
        self.assertTrue(
            all((COHORT_ROOT / name).stat().st_size > 100_000 for name in expected)
        )

    def test_review_form_leaves_reviewer_knowledge_status_blank(self):
        review_form = REVIEW_FORM_PATH.read_text(encoding="utf-8")
        for sample in self.manifest["samples"]:
            row = next(
                line
                for line in review_form.splitlines()
                if line.startswith(f"| {sample['sample_id']} |")
            )
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            self.assertEqual(cells[1], "")

    def test_reviewer_package_preserves_research_boundaries(self):
        text = README_PATH.read_text(encoding="utf-8")
        for token in (
            "不建立人工专家真值",
            "不查看结果",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
            "conclusion: no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, text)

    def test_blind_reviews_are_complete_clean_and_frozen_before_answers(self):
        self.assertEqual(
            hashlib.sha256(REVIEWS_PATH.read_bytes()).hexdigest(),
            EXPECTED_REVIEWS_SHA256,
        )
        document = read_json(REVIEWS_PATH)
        self.assertFalse(document["answer_or_outcome_opened_before_freeze"])
        self.assertFalse(document["future_or_outcome_evidence_used"])
        self.assertEqual(document["human_expert_status"], "not_performed")
        self.assertEqual(document["review_count"], 24)
        self.assertEqual(document["sample_count"], 12)
        reviews = document["reviews"]
        expected_samples = {
            sample["sample_id"] for sample in self.manifest["samples"]
        }
        self.assertEqual({review["sample_id"] for review in reviews}, expected_samples)
        for sample_id in expected_samples:
            pair = [review for review in reviews if review["sample_id"] == sample_id]
            self.assertEqual(len(pair), 2, sample_id)
            self.assertEqual(len({review["reviewer_id"] for review in pair}), 2)
            self.assertTrue(all(review["knowledge_status"] == "clean" for review in pair))

    def test_metrics_recompute_pair_agreement_and_keep_ground_truth_absent(self):
        reviews = read_json(REVIEWS_PATH)["reviews"]
        metrics = read_json(METRICS_PATH)
        fields = tuple(metrics["reviewer_pair_field_agreement"])
        grouped = {
            sample_id: [r for r in reviews if r["sample_id"] == sample_id]
            for sample_id in {r["sample_id"] for r in reviews}
        }
        for field in fields:
            exact = sum(
                pair[0][field] == pair[1][field] for pair in grouped.values()
            )
            recorded = metrics["reviewer_pair_field_agreement"][field]
            self.assertEqual(recorded["denominator"], 12)
            self.assertEqual(recorded["exact_agreements"], exact)
            self.assertAlmostEqual(recorded["rate"], exact / 12, places=4)

        mutual_h_l = sum(
            pair[0]["visual_family"] == pair[1]["visual_family"] == "H_L_like"
            for pair in grouped.values()
        )
        mutual_deep = sum(
            pair[0]["selection_disposition"]
            == pair[1]["selection_disposition"]
            == "deep_reviewed"
            for pair in grouped.values()
        )
        self.assertEqual(metrics["routing_observations"]["mutual_h_l_like_samples"], mutual_h_l)
        self.assertEqual(metrics["routing_observations"]["mutual_deep_review_samples"], mutual_deep)
        self.assertEqual(mutual_h_l, 0)
        self.assertEqual(mutual_deep, 1)
        self.assertEqual(metrics["ground_truth"]["human_expert_status"], "not_performed")
        self.assertEqual(metrics["ground_truth"]["overall_accuracy"], "not-computable")
        self.assertEqual(metrics["trade_statistics"]["completed_trade_denominator"], 0)
        self.assertEqual(metrics["trade_statistics"]["validated_win_rate"], "not-computable")
        self.assertEqual(metrics["trade_statistics"]["conclusion"], "no-new-positive")


if __name__ == "__main__":
    unittest.main()

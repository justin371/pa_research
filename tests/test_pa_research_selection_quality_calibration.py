"""Regression checks for the selection-quality and blind-visual baseline contracts."""

import json
from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
DAILY_CARD = REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md"
CALIBRATION = REPO_ROOT / "docs" / "visual_calibration_protocol_v0_1_CN.md"
TRIAGE = REPO_ROOT / "research" / "visual_pattern_triage_protocol_CN.md"
AUDIT = REPO_ROOT / "research" / "selection_quality_process_audit_2026-09-01_CN.md"
PREDICTIONS = (
    REPO_ROOT
    / "research"
    / "selection_quality_blind_batch1_predictions_2026-09-01_CN.md"
)
ASSET_DIR = (
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-09-01"
    / "selection_quality_blind_batch1"
)


def read(path):
    return path.read_text(encoding="utf-8")


class PaResearchSelectionQualityCalibrationTests(unittest.TestCase):
    def test_discovery_and_deep_review_contracts_share_reconciliation_fields(self):
        required = (
            "coverage_bucket:",
            "shortlist_rank:",
            "rank_basis:",
            "selection_disposition:",
            "wait_for_structure",
            "duplicate_lineage",
            "event_boundary",
            "insufficient_evidence",
        )
        for path in (DAILY_CARD, TRIAGE):
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in required:
                    self.assertIn(token, content)
        self.assertIn("discovery_pool_total:", read(DAILY_CARD))
        self.assertIn("selection_disposition_counts:", read(DAILY_CARD))

    def test_calibration_separates_discovery_labels_and_outcomes(self):
        content = read(CALIBRATION)
        for token in (
            "cohort_id: deterministic_discovery_cohort",
            "cohort_id: curated_morphology_cohort",
            "label_hidden: yes",
            "outcome_hidden: yes",
            "future_bars_hidden: yes",
            "knowledge_contaminated",
            "standard_converging",
            "parabolic_climactic",
            "expanding",
            "truncated_third_push",
            "overshoot_failed_breakout",
            "nested_or_complex",
            "trend_pullback",
            "range_edge",
            "候选 precision / recall",
            "视觉一致不等于交易盈利",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, content)

    def test_manifest_and_png_inventory_are_complete_and_neutral(self):
        manifest = json.loads(read(ASSET_DIR / "manifest.json"))
        samples = manifest["samples"]
        self.assertEqual(len(samples), 12)
        self.assertTrue(manifest["label_hidden"])
        self.assertTrue(manifest["outcome_hidden"])
        self.assertEqual(manifest["minimum_context_bars"], 600)
        self.assertEqual(manifest["minimum_hidden_future_bars"], 40)
        self.assertIn("not market-random", manifest["symbol_selection_scope"])
        self.assertEqual(len({row["sample_id"] for row in samples}), 12)
        self.assertEqual(len({row["symbol"] for row in samples}), 12)
        self.assertEqual(len({row["chart_file"] for row in samples}), 12)

        pngs = {path.name for path in ASSET_DIR.glob("*.png")}
        self.assertEqual(pngs, {row["chart_file"] for row in samples})
        for row in samples:
            self.assertRegex(row["sample_id"], r"^BQ1-[A-Z]+$")
            self.assertNotRegex(row["chart_file"].lower(), r"h1|h2|l1|l2|winner|loser|target")
            data = (ASSET_DIR / row["chart_file"]).read_bytes()
            self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_predictions_are_frozen_without_accuracy_or_trade_claim(self):
        content = read(PREDICTIONS)
        sample_ids = set(re.findall(r"`(BQ1-[A-Z]+)`", content))
        self.assertEqual(len(sample_ids), 12)
        for token in (
            "frozen_visual_answer",
            "outcome-hidden",
            "expert_adjudication: pending",
            "trade_state: not_authorized",
            "conclusion: no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, content)
        self.assertNotIn("expert_adjudication: completed", content)
        self.assertNotRegex(content, r"(?m)^accuracy:\s*[0-9]")
        self.assertNotRegex(content, r"(?m)^win_rate:\s*[0-9]")

    def test_current_audit_updates_inventory_without_rewriting_history(self):
        content = read(AUDIT)
        for token in (
            "current_visual_asset_readmes: 12",
            "current_visual_png_assets: 117",
            "strict_class_balanced_calibration: not_started",
            "2026-08-29/30 的旧审计中“11 个 README / 105 张 PNG”是当时的历史快照",
            "conclusion: no-new-positive",
            "validated win-rate: not-computable",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, content)


if __name__ == "__main__":
    unittest.main()

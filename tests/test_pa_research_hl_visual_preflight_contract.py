"""Regression checks for H/L visual preflight fields and asset provenance."""

import csv
from collections import Counter
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
ASSET_ROOT = REPO_ROOT / "research" / "assets" / "visual_recognition"
AUDIT_PATH = BACKTEST_ROOT / "hl_visual_preflight_contract_audit_2026-08-29_CN.md"

CONTRACT_SPECS = (
    ("hl_contracts_2026-08-26.csv", 5),
    ("hl_contracts_batch2_2026-08-26.csv", 3),
    ("hl_large_contracts_2026-08-27.csv", 37),
    ("hl_next_contracts_2026-08-27.csv", 5),
    ("hl_next2_contracts_2026-08-27.csv", 2),
    ("hl_next4_contracts_2026-08-27.csv", 2),
    ("hl_next5_contracts_2026-08-27.csv", 6),
)

REQUIRED_FIELDS = (
    "label_source",
    "daily_context_window",
    "major_high_low_review",
    "ema20_50_200_review",
    "contract_frozen",
)


def read_contracts(filename):
    with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class PaResearchHlVisualPreflightContractTests(unittest.TestCase):
    def test_all_frozen_hl_contracts_have_complete_visual_preflight_fields(self):
        rows = []
        for filename, expected_count in CONTRACT_SPECS:
            current = read_contracts(filename)
            self.assertEqual(len(current), expected_count, filename)
            rows.extend(current)
            for row in current:
                with self.subTest(contract=row["sample_id"], file=filename):
                    self.assertEqual(row["label_source"], "human_chart_review")
                    self.assertEqual(row["daily_context_window"], ">=2y")
                    self.assertEqual(row["major_high_low_review"], "complete")
                    self.assertEqual(row["ema20_50_200_review"], "complete")
                    self.assertEqual(row["contract_frozen"], "yes")
                    self.assertTrue(all(row[field].strip() for field in REQUIRED_FIELDS))

        self.assertEqual(len(rows), 60)
        expected_counters = {
            "label_source": Counter({"human_chart_review": 60}),
            "daily_context_window": Counter({">=2y": 60}),
            "major_high_low_review": Counter({"complete": 60}),
            "ema20_50_200_review": Counter({"complete": 60}),
            "contract_frozen": Counter({"yes": 60}),
        }
        for field in REQUIRED_FIELDS:
            self.assertEqual(Counter(row[field] for row in rows), expected_counters[field])

    def test_local_asset_cardinality_and_external_boundaries_are_explicit(self):
        self.assertEqual(len(list(ASSET_ROOT.rglob("README.md"))), 11)
        self.assertEqual(len(list(ASSET_ROOT.rglob("*.png"))), 105)
        expected_local_counts = {
            "2026-08-26/hl_contract_batch": 5,
            "2026-08-26/hl_contract_batch2": 3,
            "2026-08-27/hl_large_backtest": 23,
            "2026-08-27/hl_next_backtest": 5,
            "2026-08-27/hl_next2_backtest": 3,
        }
        for relative_dir, expected_count in expected_local_counts.items():
            with self.subTest(asset_dir=relative_dir):
                self.assertEqual(
                    len(list((ASSET_ROOT / relative_dir).glob("*.png"))),
                    expected_count,
                )

        next4_selection = (BACKTEST_ROOT / "hl_next4_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        next4_replay = (BACKTEST_ROOT / "hl_next4_replay_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        next5_selection = (BACKTEST_ROOT / "hl_next5_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        next5_replay = (BACKTEST_ROOT / "hl_next5_replay_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(".codex\\artifacts\\pa-research-hl-next4-20260827", next4_selection)
        self.assertIn(".codex\\artifacts\\pa-research-hl-next5-20260827", next5_selection)
        self.assertIn("ROST 缺少决策日视觉 artifact", next4_selection)
        self.assertIn("descriptive research record", next4_selection)
        self.assertIn("不能作为新的可交易候选或已验证视觉样本", next4_selection)
        self.assertIn("后续图", next4_replay)
        self.assertIn("不能替代", next4_replay)
        self.assertIn(".codex\\artifacts\\pa-research-hl-next5-20260827", next5_replay)
        self.assertIn("每个窗口均有至少两年左侧 Daily 背景", next5_selection)

    def test_authority_docs_validator_and_audit_keep_provenance_separate(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for token in (
            "7 份 CSV 共 60 行",
            "`label_source`",
            "`daily_context_window`",
            "`major_high_low_review`",
            "`ema20_50_200_review`",
            "`contract_frozen`",
            "105 张 PNG",
            "114 张和 78 张",
            "ROST",
            "post-decision",
            "provenance gap",
            "descriptive research record",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

        visual_card = (REPO_ROOT / "docs" / "visual_pa_review_card_CN.md").read_text(
            encoding="utf-8"
        )
        output_schema = (REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md").read_text(
            encoding="utf-8"
        )
        backtesting = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`contract_frozen: yes` 只表示字段合同已经冻结", visual_card)
        self.assertIn("不是视觉 artifact provenance 或交易授权", output_schema)
        self.assertIn("不能把它升级为新的可交易候选或 validated sample", backtesting)

        indexed = (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        )
        for path in indexed:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT_PATH.name, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

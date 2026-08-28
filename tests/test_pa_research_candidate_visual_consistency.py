"""Regression checks for PA Research candidate/visual-record boundaries."""

import csv
import unittest
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"

SELECTION_SPECS = (
    (
        "hl_large_selection_2026-08-27_CN.md",
        "hl_large_contracts_2026-08-27.csv",
        37,
        {"long": 20, "short": 17},
        {"H1": 15, "H2": 5, "L1": 12, "L2": 5},
    ),
    (
        "hl_next_selection_2026-08-27_CN.md",
        "hl_next_contracts_2026-08-27.csv",
        5,
        {"long": 4, "short": 1},
        {"H1": 4, "L1": 1},
    ),
    (
        "hl_next2_selection_2026-08-27_CN.md",
        "hl_next2_contracts_2026-08-27.csv",
        2,
        {"long": 2, "short": 0},
        {"H1": 2},
    ),
    (
        "hl_next4_selection_2026-08-27_CN.md",
        "hl_next4_contracts_2026-08-27.csv",
        2,
        {"long": 2, "short": 0},
        {"H1": 2},
    ),
    (
        "hl_next5_selection_2026-08-27_CN.md",
        "hl_next5_contracts_2026-08-27.csv",
        6,
        {"long": 0, "short": 6},
        {"L1": 6},
    ),
)

DETAILED_CONTRACT_FILES = {
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
}


def read_contracts(filename):
    with (BACKTEST_ROOT / filename).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class CandidateVisualConsistencyTests(unittest.TestCase):
    def test_selection_contract_counts_and_direction_summaries(self):
        for selection_file, contract_file, expected_count, expected_directions, expected_labels in SELECTION_SPECS:
            with self.subTest(selection=selection_file):
                selection_text = (BACKTEST_ROOT / selection_file).read_text(encoding="utf-8")
                rows = read_contracts(contract_file)

                self.assertEqual(len(rows), expected_count)
                self.assertIn("方向分布", selection_text)
                for direction, count in expected_directions.items():
                    self.assertIn(f"{direction}={count}", selection_text)
                actual_directions = Counter(row["direction"] for row in rows)
                self.assertEqual(
                    {direction: actual_directions.get(direction, 0) for direction in expected_directions},
                    expected_directions,
                )
                self.assertEqual(
                    Counter(row["internal_label"] for row in rows), expected_labels
                )
                self.assertTrue(all(row["contract_frozen"] == "yes" for row in rows))

    def test_frozen_contracts_keep_required_pre_entry_axes(self):
        base_required_fields = (
            "direction",
            "lineage_id",
            "decision_date",
            "primary_pattern",
            "internal_label",
            "order_branch",
            "entry_trigger",
            "structural_stop",
            "first_obstacle",
            "daily_context_window",
            "major_high_low_review",
            "ema20_50_200_review",
            "event_context",
            "daily_ema20_slope",
            "daily_ema50_slope",
            "h_l_ema_slope_gate",
        )
        detailed_required_fields = (
            "a_leg_quality",
            "b_leg_class",
            "pre_entry_space_R",
            "space_status",
            "contract_state",
        )
        for _, contract_file, _, _, _ in SELECTION_SPECS:
            for row in read_contracts(contract_file):
                with self.subTest(contract=row.get("sample_id")):
                    required_fields = base_required_fields
                    if contract_file in DETAILED_CONTRACT_FILES:
                        required_fields += detailed_required_fields
                    for field in required_fields:
                        self.assertTrue(row[field], field)
                    self.assertEqual(row["daily_context_window"], ">=2y")
                    self.assertEqual(row["major_high_low_review"], "complete")
                    self.assertEqual(row["ema20_50_200_review"], "complete")
                    self.assertTrue(row["lineage_id"])

    def test_next3_stays_candidate_only(self):
        text = (BACKTEST_ROOT / "hl_next3_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("新冻结合同方向分布", text)
        self.assertIn("long=0", text)
        self.assertIn("short=0", text)
        self.assertIn("没有可进入回放的交易合同", text)

    def test_next5_summary_does_not_leak_post_outcome_results(self):
        text = (BACKTEST_ROOT / "hl_next5_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        pre_data = text.split("## 股票池与数据边界", 1)[0]
        for phrase in (
            "5 条成交并完成",
            "3 条完成交易",
            "2 胜 1 负",
            "3/5=",
            "earnings_adjacent` 组 1 负",
        ):
            self.assertNotIn(phrase, pre_data)
        self.assertIn("hl_next5_replay_2026-08-27_CN.md", text)
        self.assertIn("不属于本文件的冻结前证据", text)

    def test_special_records_keep_provenance_and_state_separate(self):
        next4 = (BACKTEST_ROOT / "hl_next4_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("ROST 缺少决策日视觉 artifact", next4)
        self.assertIn("不能把该缺口与合同已冻结混为一谈", next4)

        inventory = (REPO_ROOT / "strategy" / "pattern_inventory_candidates.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("目录标签，不是统一输出合同中的单一 `research_state`", inventory)
        self.assertIn("process-target-reached", inventory)

    def test_tsla_meta_note_is_observation_only(self):
        text = (
            REPO_ROOT / "strategy" / "reviews" / "2026-06-25-tsla-meta-example.md"
        ).read_text(encoding="utf-8")
        for field in (
            "direction: no_valid_direction",
            "gate_result: observation_only",
            "order_branch: observation_only",
            "research_state: pattern_like",
            "trade_state: not_authorized",
            "handoff_status: research_only",
        ):
            self.assertIn(field, text)
        self.assertIn("不是实际成交日志、冻结合同或胜率样本", text)

    def test_audit_is_indexed_and_preserves_no_new_positive_boundary(self):
        report = (
            REPO_ROOT / "research" / "candidate_visual_record_consistency_audit_2026-08-29_CN.md"
        ).read_text(encoding="utf-8")
        self.assertIn("no-new-positive", report)
        self.assertIn("validated win-rate: not-computable", report)
        self.assertIn("不修改 Codex Trading", report)
        self.assertIn("pattern_like", report)
        self.assertIn("candidate_pending", report)
        self.assertIn("valid_no_trade", report)

        research_readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
        strategy_readme = (REPO_ROOT / "strategy" / "README.md").read_text(encoding="utf-8")
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(
            encoding="utf-8"
        )
        self.assertIn("candidate_visual_record_consistency_audit_2026-08-29_CN.md", research_readme)
        self.assertIn("candidate_visual_record_consistency_audit_2026-08-29_CN.md", strategy_readme)
        self.assertIn("candidate_visual_record_consistency_audit_2026-08-29_CN.md", validator)


if __name__ == "__main__":
    unittest.main()

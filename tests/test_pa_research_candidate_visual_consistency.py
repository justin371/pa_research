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

    def test_all_selection_records_declare_historical_daily_scope(self):
        for filename in (
            "hl_large_selection_2026-08-27_CN.md",
            "hl_next_selection_2026-08-27_CN.md",
            "hl_next2_selection_2026-08-27_CN.md",
            "hl_next3_selection_2026-08-27_CN.md",
            "hl_next4_selection_2026-08-27_CN.md",
            "hl_next5_selection_2026-08-27_CN.md",
        ):
            content = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
            with self.subTest(selection=filename):
                self.assertIn("contract_scope: historical_context_only", content)
                self.assertIn("timeframes_seen: Daily", content)
                self.assertIn("frozen_pre_outcome", content)

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

    def test_visual_inventory_has_explicit_canonical_direction_for_every_row(self):
        inventory = (REPO_ROOT / "strategy" / "pattern_inventory_candidates.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "| 视觉候选 ID | direction | 先看什么 | 代表性入口 | 当前状态 |",
            inventory,
        )
        rows = [
            line
            for line in inventory.splitlines()
            if line.startswith("| `VIS-")
        ]
        self.assertGreaterEqual(len(rows), 80)
        allowed_directions = {"long", "short", "no_valid_direction"}
        for row in rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            with self.subTest(candidate=row.split("|")[1].strip()):
                self.assertEqual(len(cells), 5)
                self.assertIn(cells[1], allowed_directions)
        self.assertIn(
            "完整候选卡和冻结合同仍必须逐行写 canonical `direction`",
            inventory,
        )
        self.assertNotIn("research_positive conditional", inventory)
        self.assertNotIn("valid no-trade", inventory)
        self.assertNotIn("research_positive_candidate", inventory)
        expected_direction = {
            "VIS-ABC-BULL-H2-REPEATED-SUPPORT": "long",
            "VIS-ABC-BEAR-L2-EARLY-TRIGGER": "short",
            "VIS-H3-L3-SECOND-PUSH-EXPANSION": "no_valid_direction",
            "VIS-ABC-BULL-GROWTH-UNIVERSE-2024Q3": "no_valid_direction",
            "VIS-MTR-TSLA-RANGE-TOP-L2": "short",
        }
        by_id = {
            row.split("|")[1].strip().strip("`"): row.split("|")[2].strip()
            for row in rows
        }
        self.assertEqual(
            {candidate: by_id[candidate] for candidate in expected_direction},
            expected_direction,
        )

    def test_legacy_selection_batches_disclose_structured_field_boundary(self):
        for filename, count in (
            ("hl_large_selection_2026-08-27_CN.md", "37 条旧 CSV"),
            ("hl_next_selection_2026-08-27_CN.md", "5 条旧 CSV"),
        ):
            content = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
            with self.subTest(selection=filename):
                self.assertIn("结构化字段覆盖边界", content)
                self.assertIn(count, content)
                for field in (
                    "a_leg_quality",
                    "b_leg_class",
                    "pre_entry_space_R",
                    "space_status",
                    "contract_state",
                ):
                    self.assertIn(field, content)
                self.assertTrue(
                    "不能由历史几何或回放结果补齐" in content
                    or "不能从文字、回放结果或后验走势补写" in content
                )

    def test_legacy_visual_candidate_entries_declare_scope_and_unknown_gates(self):
        specifications = (
            (
                "crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md",
                "contract_scope: historical_context_only",
                "directional_bias: bear",
                "direction: short",
                "timeframes_seen: Daily / 60m / 15m",
                "daily_context_window: <2y",
                "a_leg_quality: unclear",
                "b_leg_class: unclear",
                "event_context: unknown",
                "event_bucket: event_unverified_or_pending",
                "sector_state: aligned",
                "market_state: aligned",
                "permission: short_allowed",
                "first_independent_obstacle: pending",
                "pre_entry_space_R: unknown",
                "space_status: unknown",
            ),
            (
                "meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md",
                "contract_scope: stage_1_fast_screen",
                "directional_bias: bull",
                "direction: long",
                "timeframes_seen: Daily",
                "daily_context_window: unavailable",
                "a_leg_quality: unclear",
                "b_leg_class: unclear",
                "event_context: unknown",
                "event_bucket: event_unverified_or_pending",
                "sector_state: unknown",
                "market_state: unknown",
                "permission: unknown",
                "first_independent_obstacle: pending",
                "pre_entry_space_R: unknown",
                "space_status: unknown",
            ),
            (
                "msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md",
                "contract_scope: stage_1_fast_screen",
                "directional_bias: bear",
                "direction: short",
                "timeframes_seen: Daily",
                "daily_context_window: <2y",
                "a_leg_quality: unclear",
                "b_leg_class: unclear",
                "event_context: unknown",
                "event_bucket: event_unverified_or_pending",
                "sector_state: unknown",
                "market_state: unknown",
                "permission: unknown",
                "first_independent_obstacle: pending",
                "pre_entry_space_R: unknown",
                "space_status: unknown",
            ),
            (
                "nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md",
                "contract_scope: stage_1_fast_screen",
                "directional_bias: bull",
                "direction: long",
                "timeframes_seen: Daily",
                "daily_context_window: <2y",
                "a_leg_quality: unclear",
                "b_leg_class: unclear",
                "event_context: unknown",
                "event_bucket: event_unverified_or_pending",
                "sector_state: unknown",
                "market_state: unknown",
                "permission: unknown",
                "first_independent_obstacle: pending",
                "pre_entry_space_R: unknown",
                "space_status: unknown",
            ),
            (
                "visual_screen_candidate_grid_2024_2025_CN.md",
                "contract_scope: stage_1_fast_screen",
                "directional_bias: changing",
                "direction: no_valid_direction",
                "timeframes_seen: Daily",
                "daily_context_window: unavailable",
                "a_leg_quality: unclear",
                "b_leg_class: unclear",
                "event_context: unknown",
                "event_bucket: event_unverified_or_pending",
                "sector_state: unknown",
                "market_state: unknown",
                "permission: unknown",
                "first_independent_obstacle: pending",
                "pre_entry_space_R: unknown",
                "space_status: unknown",
            ),
        )
        for filename, *tokens in specifications:
            content = (REPO_ROOT / "research" / filename).read_text(encoding="utf-8")
            with self.subTest(candidate=filename):
                for token in tokens + [
                    "research_state: pattern_like",
                    "trade_state: not_authorized",
                    "gate_result: pending",
                ]:
                    self.assertIn(token, content)

    def test_klac_case_exposes_direction_and_canonical_status(self):
        content = (
            REPO_ROOT
            / "research"
            / "klac_h3_bear_flag_case_2025-03-12_2025-03-28.md"
        ).read_text(encoding="utf-8")
        self.assertIn("方向：`short`（研究方向；不是交易授权）", content)
        self.assertIn("research_positive_conditional", content)
        self.assertNotIn("research_positive_candidate", content)

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
        self.assertIn("视觉候选目录缺少独立方向列", report)
        self.assertIn("50 条旧合同没有", report)
        self.assertIn("日线候选输出链的周期和合同边界", report)
        self.assertIn("Daily-first", report)

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

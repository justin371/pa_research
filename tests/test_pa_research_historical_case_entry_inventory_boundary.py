from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "research" / "backtesting" / "historical_case_entry_inventory_contract_audit_2026-08-29_CN.md"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"

INDEX_PATHS = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "research" / "README.md",
    REPO_ROOT / "research" / "backtesting" / "README.md",
    REPO_ROOT / "patterns" / "README.md",
    REPO_ROOT / "foundations" / "README.md",
    REPO_ROOT / "strategy" / "README.md",
)

DIRECT_ONLY_ENTRY_PATHS = tuple(
    REPO_ROOT / relative_path
    for relative_path in (
        "research/adbe_bearish_abc_l1_visual_screen_2026-01-12_2026-01-27.md",
        "research/amzn_bearish_abc_l1_no_gap_first_support_boundary_2024-09-23_2024-10-15.md",
        "research/amzn_bullish_h2_shallow_b_boundary_2024-12-09_2024-12-11.md",
        "research/anet_bearish_l2_event_boundary_2024-02-12_2024-02-21.md",
        "research/anet_bullish_h2_visual_boundary_2023-11-15_2023-11-22.md",
        "research/anet_h3_l3_case_study_2024-05-16_2024-06-10.md",
        "research/bkng_bullish_h2_gap_trigger_boundary_2024-06-12_2024-06-18.md",
        "research/cme_bearish_abc_l1_visual_screen_2026-05-20_2026-06-17.md",
        "research/coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md",
        "research/cost_bullish_abc_h2_visual_boundary_2025-04-21_2025-05-16.md",
        "research/crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md",
        "research/dis_bearish_abc_l1_opening_skip_first_support_2024-07-16_2024-08-02.md",
        "research/jnj_bullish_h1_opening_skip_first_obstacle_boundary_2025-08-01_2025-09-02.md",
        "research/lly_bullish_abc_h1_h2_first_obstacle_boundary_2024-06-06_2024-06-13.md",
        "research/lrcx_bearish_abc_l1_gap_first_support_2024-07-10_2024-07-25.md",
        "research/mar_4h_l1_case_study_2026-06-18_2026-06-25.md",
        "research/mcd_bearish_abc_l1_counter_market_first_support_2025-05-19_2025-06-27.md",
        "research/mdt_bullish_abc_h2_visual_screen_2025-05-23_2025-07-02.md",
        "research/meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md",
        "research/msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md",
        "research/nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md",
        "research/nvda_bullish_h1_trigger_branch_first_obstacle_2025-04-21_2025-05-08.md",
        "research/nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md",
        "research/pm_bullish_abc_h1_visual_screen_2026-01-05_2026-01-23.md",
        "research/spy_bullish_h1_h2_index_control_first_resistance_2025-07-07_2025-07-18.md",
        "research/tsla_bearish_abc_candidate_screen_2026-08-22.md",
        "research/tsla_bearish_abc_case_2024-07-11_2024-08-05.md",
        "research/tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md",
        "research/tsla_h1_h2_case_study_2025-08-28_2025-09-05.md",
        "research/tsla_h1_h2_case_study_2025-12-08_2025-12-12.md",
        "research/tsla_h1_h2_case_study_2026-05-15_2026-05-22.md",
        "research/tsla_l3_case_study_2026-03-25_2026-03-30.md",
        "research/v_bullish_abc_h2_no_gap_first_obstacle_boundary_2024-05-06_2024-05-17.md",
        "research/vrt_bullish_abc_h1_deep_b_first_obstacle_boundary_2026-04-14_2026-04-20.md",
        "research/xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md",
    )
)

HISTORICAL_SCREEN_PATHS = tuple(
    REPO_ROOT / relative_path
    for relative_path in (
        "research/adbe_bearish_abc_l1_visual_screen_2026-01-12_2026-01-27.md",
        "research/cme_bearish_abc_l1_visual_screen_2026-05-20_2026-06-17.md",
        "research/mdt_bullish_abc_h2_visual_screen_2025-05-23_2025-07-02.md",
        "research/pm_bullish_abc_h1_visual_screen_2026-01-05_2026-01-23.md",
    )
)

ACTIVE_POST_OUTCOME_FIELD = re.compile(
    r"(?im)^\s*(?:outcome|entry_price|entry_date|exit_price|exit_date|exit_reason|bars_held|fill_status|trade_result|realized_R|win_rate_eligible|path_result|first_obstacle_hit|ambiguous_intrabar|gap_adjustment|evidence_status)\s*:"
)

HISTORICAL_SCREEN_BOUNDARY_TOKENS = (
    "contract_scope: historical_context_only",
    "data_status: historical",
    "as_of_time:",
    "timezone:",
    "session_state: historical_close",
    "timeframes_seen:",
    "chart_scope: partial",
    "daily_context_window: <2y",
    "major_high_low_review:",
    "ema20_50_200_review:",
    "parent_state:",
    "direction:",
    "lineage_status: pending",
    "order_branch: observation_only",
    "structural_stop:",
    "structural_invalidation:",
    "first_independent_obstacle:",
    "pre_entry_space_R:",
    "space_status:",
    "rough_R_R:",
    "research_state:",
    "trade_state:",
    "gate_result:",
    "handoff_status: research_only",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class HistoricalCaseEntryInventoryBoundaryTests(unittest.TestCase):
    def test_inventory_declares_scope_counts_and_boundaries(self):
        content = read(AUDIT_PATH)
        for token in (
            "inventory_scope: historical_case_entry_inventory_only",
            "matrix_coverage_basis: five aggregate matrices only",
            "row_contract_source: linked_entry_file",
            "row_contract_scope: per_entry",
            "row_result_boundary: independent_replay_or_result_only",
            "historical_alias_policy: display_only_until_mapped",
            "66 个",
            "31 个",
            "35 个",
            "证据头",
            "左侧前置",
            "结构解释",
            "订单",
            "风险/空间",
            "事前证据",
            "事后结果",
            "历史别名",
        ):
            self.assertIn(token, content, token)

    def test_all_direct_only_entries_are_linked_and_exist(self):
        content = read(AUDIT_PATH)
        self.assertEqual(len(DIRECT_ONLY_ENTRY_PATHS), 35)
        for path in DIRECT_ONLY_ENTRY_PATHS:
            with self.subTest(path=path.as_posix()):
                self.assertTrue(path.is_file())
                self.assertIn(path.name, content)

    def test_direct_only_entries_have_no_active_structured_results(self):
        for path in DIRECT_ONLY_ENTRY_PATHS:
            with self.subTest(path=path.as_posix()):
                self.assertIsNone(
                    ACTIVE_POST_OUTCOME_FIELD.search(read(path)),
                    "historical entry must not become a structured result row",
                )

    def test_four_recent_screens_have_minimal_historical_boundary(self):
        for path in HISTORICAL_SCREEN_PATHS:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in HISTORICAL_SCREEN_BOUNDARY_TOKENS:
                    self.assertIn(token, content, token)

    def test_all_canonical_indexes_link_inventory(self):
        audit_name = AUDIT_PATH.name
        for path in INDEX_PATHS:
            with self.subTest(path=path.as_posix()):
                self.assertIn(audit_name, read(path))

    def test_validator_has_inventory_and_screen_guards(self):
        content = read(VALIDATOR_PATH)
        for token in (
            "$historicalCaseEntryInventoryAuditPath",
            "$historicalCaseEntryPaths",
            "$historicalCaseEntryPostOutcomeFieldPattern",
            "historical case inventory audit is missing",
            "historical case inventory audit is missing entry link",
            "post-outcome field leaked into historical case inventory entry",
            "$historicalScreenBoundaryPaths",
            "$historicalScreenBoundaryTokens",
        ):
            self.assertIn(token, content, token)

    def test_scope_and_statistical_boundaries_are_preserved(self):
        content = read(AUDIT_PATH)
        for token in (
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "修改 Codex Trading",
            "创建量化扫描器",
            "连接 Execution Agent",
            "增加样本",
            "运行回放",
        ):
            self.assertIn(token, content, token)


if __name__ == "__main__":
    unittest.main()

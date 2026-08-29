from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "research" / "backtesting" / "top_level_research_entry_boundary_audit_2026-08-30_CN.md"
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

ENTRY_PATHS = tuple(
    REPO_ROOT / relative_path
    for relative_path in (
        "research/aapl_bullish_h1_event_driven_a_2024-05-03_2024-05-09.md",
        "research/amzn_bullish_h2_shallow_b_boundary_2024-12-09_2024-12-11.md",
        "research/crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md",
        "research/klac_h1_case_study_2025-10-14_2025-10-24.md",
        "research/klac_h3_bear_flag_case_2025-03-12_2025-03-28.md",
        "research/nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md",
        "research/nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md",
        "research/tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md",
        "research/tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md",
    )
)

POST_OUTCOME_FIELD = re.compile(
    r"(?im)^\s*(?:outcome|entry_price|entry_date|exit_price|exit_date|exit_reason|bars_held|"
    r"fill_status|trade_result|realized_R|win_rate_eligible|path_result|first_obstacle_hit|"
    r"ambiguous_intrabar|gap_adjustment|evidence_status)\s*:"
)
PROMOTED_STATUS = re.compile(
    r"(?im)^\s*(?:trade_state|handoff_status|research_state)\s*:\s*"
    r"(?:authorized|ready_for_system|validated)\s*$"
)
ACTIVE_PRIMARY_OR_INTERNAL = re.compile(
    r"(?im)^\s*(?:primary_pattern|internal_label)\s*:\s*"
    r"(?:ABC_CONT|BOP|H1_L1|H2_L2|H3_L3|H1|H2|L1|L2|H3|L3)\s*$"
)

BOUNDARY_TOKENS = (
    "contract_scope: historical_context_only",
    "data_status: historical",
    "as_of_time:",
    "timezone:",
    "session_state: historical_close",
    "timeframes_seen: Daily / 60m / 15m",
    "chart_scope: partial",
    "daily_context_window: <2y",
    "major_high_low_review: partial",
    "ema20_50_200_review:",
    "parent_state:",
    "direction:",
    "lineage_status: pending",
    "state_transition:",
    "order_branch: observation_only",
    "actual_fill_or_open_skip: not_applicable",
    "structural_stop: pending",
    "structural_invalidation: pending",
    "first_independent_obstacle:",
    "pre_entry_space_R: unknown",
    "space_status:",
    "rough_R_R: unknown",
    "research_state: research_positive_conditional",
    "trade_state:",
    "gate_result:",
    "handoff_status: research_only",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TopLevelResearchEntryBoundaryTests(unittest.TestCase):
    def test_audit_declares_scan_scope_counts_and_statistical_boundary(self):
        content = read(AUDIT_PATH)
        for token in (
            "inventory_scope: top_level_research_entry_boundary_audit_only",
            "scan_scope: research_root_markdown_non_readme",
            "case_like_selection: filename_and_header_heuristic",
            "row_contract_source: linked_entry_file",
            "row_contract_scope: per_entry",
            "row_result_boundary: independent_replay_or_result_only",
            "historical_alias_policy: display_only_until_mapped",
            "171 个历史研究报告",
            "58 个文件",
            "113 个主要是",
            "9 份 ticker-like 历史案例",
            "no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, content, token)

    def test_all_residual_entries_are_linked_and_exist(self):
        content = read(AUDIT_PATH)
        self.assertEqual(len(ENTRY_PATHS), 9)
        for path in ENTRY_PATHS:
            with self.subTest(path=path.as_posix()):
                self.assertTrue(path.is_file())
                self.assertIn(path.name, content)

    def test_each_residual_entry_has_the_minimum_historical_boundary(self):
        for path in ENTRY_PATHS:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in BOUNDARY_TOKENS:
                    self.assertIn(token, content, token)
                self.assertIsNone(ACTIVE_PRIMARY_OR_INTERNAL.search(content))

    def test_residual_entries_do_not_contain_results_or_authorization(self):
        for path in ENTRY_PATHS:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                self.assertIsNone(POST_OUTCOME_FIELD.search(content))
                self.assertIsNone(PROMOTED_STATUS.search(content))

    def test_all_canonical_indexes_and_validator_cover_the_audit(self):
        audit_name = AUDIT_PATH.name
        for path in INDEX_PATHS:
            with self.subTest(index=path.as_posix()):
                self.assertIn(audit_name, read(path))
        validator = read(VALIDATOR_PATH)
        for token in (
            "$topLevelConditionalEntryBoundaryAuditPath",
            "$topLevelConditionalEntryPaths",
            "$topLevelConditionalEntryBoundaryTokens",
            "top-level conditional entry boundary audit is missing",
            "top-level conditional entry is missing from boundary audit",
            "post-outcome field leaked into top-level conditional entry",
            "active promoted status leaked into top-level conditional entry",
        ):
            self.assertIn(token, validator, token)

    def test_scope_and_non_promotion_boundaries_are_explicit(self):
        content = read(AUDIT_PATH)
        for token in (
            "回放结果及真实交易日志始终分开",
            "没有新增图表样本",
            "不把历史研究升级为授权",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, content, token)


if __name__ == "__main__":
    unittest.main()

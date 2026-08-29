from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "research" / "backtesting" / "pattern_case_matrix_strategy_entry_contract_audit_2026-08-29_CN.md"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"
INVENTORY_PATH = REPO_ROOT / "strategy" / "pattern_inventory_candidates.md"
META_REVIEW_PATH = REPO_ROOT / "strategy" / "reviews" / "2026-06-25-tsla-meta-example.md"

AGGREGATE_MATRIX_PATHS = (
    REPO_ROOT / "research" / "abc_decision_matrix_CN.md",
    REPO_ROOT / "research" / "core_pattern_case_matrix_CN.md",
    REPO_ROOT / "research" / "tsla_abc_h1_h2_comparison_matrix.md",
    REPO_ROOT / "research" / "tsla_bearish_abc_comparison_matrix.md",
)

INDEX_PATHS = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "research" / "README.md",
    REPO_ROOT / "research" / "backtesting" / "README.md",
    REPO_ROOT / "patterns" / "README.md",
    REPO_ROOT / "foundations" / "README.md",
    REPO_ROOT / "strategy" / "README.md",
)

ROW_CONTRACT_FIELDS = (
    "contract_scope",
    "evidence_header",
    "parent_state",
    "direction",
    "primary_pattern",
    "internal_label",
    "state_transition",
    "order_branch",
    "actual_fill_or_open_skip",
    "structural_stop",
    "structural_invalidation",
    "first_independent_obstacle",
    "pre_entry_space_R",
    "space_status",
    "rough_R_R",
    "research_state",
    "trade_state",
    "gate_result",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PatternCaseMatrixContractBoundaryTests(unittest.TestCase):
    def test_aggregate_matrices_declare_display_scope_and_row_contract_source(self):
        required_tokens = (
            "matrix_scope: aggregate_display_only",
            "row_contract_source: linked_case_file",
            "row_contract_scope: per_row",
            "row_result_boundary: independent_replay_or_result_only",
            "historical_alias_policy: display_only_until_mapped",
        )
        for path in AGGREGATE_MATRIX_PATHS:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in required_tokens:
                    self.assertIn(token, content)
                for field in ROW_CONTRACT_FIELDS:
                    self.assertIn(field, content)
                self.assertIsNone(
                    re.search(r"(?m)^\s*primary_pattern\s*:", content),
                    "aggregate matrices must not assign one global primary_pattern",
                )

    def test_inventory_declares_navigation_scope_without_promoting_index_columns(self):
        content = read(INVENTORY_PATH)
        for token in (
            "inventory_scope: visual_navigation_only",
            "row_contract_source: linked_case_file",
            "row_contract_scope: per_row",
            "row_result_boundary: independent_replay_or_result_only",
            "historical_alias_policy: display_only_until_mapped",
            "当前状态",
            "不能替代的 canonical 字段",
        ):
            self.assertIn(token, content, token)
        for field in ROW_CONTRACT_FIELDS:
            self.assertIn(field, content, field)
        self.assertIn("完整候选卡和冻结合同仍必须逐行写 canonical `direction`", content)
        self.assertIn("不能被复制成入场前的 `research_positive_conditional`", content)

    def test_history_review_has_complete_incomplete_evidence_and_geometry_axes(self):
        content = read(META_REVIEW_PATH)
        for token in (
            "contract_scope: historical_context_only",
            "data_status: incomplete",
            "as_of_time: unknown",
            "timeframes_seen: Daily / unknown lower timeframe",
            "chart_scope: partial",
            "daily_context_window: unavailable",
            "major_high_low_review: unavailable",
            "ema20_50_200_review: unavailable",
            "parent_state: unclear",
            "direction: no_valid_direction",
            "primary_pattern: other",
            "internal_label: pending",
            "state_transition: none",
            "order_branch: observation_only",
            "actual_fill_or_open_skip: not_applicable",
            "structural_stop: pending",
            "structural_invalidation: pending",
            "first_independent_obstacle: unknown",
            "pre_entry_space_R: unknown",
            "space_status: unknown",
            "rough_R_R: unknown",
            "research_state: pattern_like",
            "trade_state: not_authorized",
            "thesis_state: pending",
            "gate_result: observation_only",
            "handoff_status: research_only",
        ):
            self.assertIn(token, content, token)
        self.assertIsNone(re.search(r"(?m)^\s*outcome\s*:", content))

    def test_index_and_strategy_entry_point_to_the_audit_and_matrices(self):
        audit_name = AUDIT_PATH.name
        for path in INDEX_PATHS:
            with self.subTest(path=path.as_posix()):
                self.assertIn(audit_name, read(path))
        research_index = read(REPO_ROOT / "research" / "README.md")
        strategy_index = read(REPO_ROOT / "strategy" / "README.md")
        self.assertIn("abc_decision_matrix_CN.md", research_index)
        self.assertIn("core_pattern_case_matrix_CN.md", strategy_index)
        self.assertIn("abc_decision_matrix_CN.md", strategy_index)

    def test_validator_checks_aggregate_history_and_audit_contracts(self):
        content = read(VALIDATOR_PATH)
        for token in (
            "$aggregateMatrixContractPaths",
            "matrix_scope: aggregate_display_only",
            "inventory_scope: visual_navigation_only",
            "row_contract_source: linked_case_file",
            "row_result_boundary: independent_replay_or_result_only",
            "$historicalMetaReviewRelativePath",
            "historical META review must not add an outcome field",
            "$patternCaseMatrixAuditPath",
        ):
            self.assertIn(token, content, token)

    def test_audit_preserves_scope_and_statistical_boundaries(self):
        content = read(AUDIT_PATH)
        for token in (
            "matrix_scope: aggregate_display_only",
            "inventory_scope: visual_navigation_only",
            "independent_replay_or_result_only",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "不修改 Codex Trading",
            "不创建量化扫描器",
            "不连接 Execution Agent",
        ):
            self.assertIn(token, content, token)


if __name__ == "__main__":
    unittest.main()

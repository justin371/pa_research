import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = (
    REPO_ROOT
    / "research"
    / "backtesting"
    / "visual_authority_schema_alignment_audit_2026-08-29_CN.md"
)
VISUAL_CARD = REPO_ROOT / "docs" / "visual_pa_review_card_CN.md"

ACTIVE_FRAMEWORKS = (
    REPO_ROOT / "research" / "market_state_context_visual_evidence_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "inside_bar_two_bar_reversal_visual_framework_CN.md",
    REPO_ROOT / "research" / "triangle_expanding_range_visual_framework_CN.md",
    REPO_ROOT / "research" / "late_trend_entry_visual_framework_CN.md",
    REPO_ROOT / "research" / "multitimeframe_visual_review_framework_CN.md",
)

MIGRATED_DOCUMENTS = (
    REPO_ROOT / "research" / "abc_continuation_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "abc_hl_stratified_outcome_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "bop_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "channel_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "channel_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "core_pattern_cross_audit_CN.md",
    REPO_ROOT / "research" / "cross_pattern_visual_priority_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "failed_breakout_climax_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "h1_l1_first_entry_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "h2_l2_second_entry_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "late_trend_entry_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "mtr_three_push_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "multitimeframe_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "triangle_expanding_range_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "triangle_expanding_range_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "visual_review_workflow_boundary_audit_2026-08-24_CN.md",
)

INDEXES = (
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "research" / "README.md",
    REPO_ROOT / "strategy" / "README.md",
    REPO_ROOT / "patterns" / "README.md",
    REPO_ROOT / "research" / "backtesting" / "README.md",
)


def read(path):
    return path.read_text(encoding="utf-8")


def has_active_field(content, field):
    return re.search(rf"(?m)^{re.escape(field)}:", content) is not None


class VisualAuthoritySchemaAlignmentTests(unittest.TestCase):
    def test_visual_card_separates_display_aliases_from_canonical_axes(self):
        content = read(VISUAL_CARD)
        for token in (
            "primary_pattern: ABC_CONT | BOP | RFB | H3_L3 | MTR | other",
            "pattern_family: ABC_CONT | BOP | RFB_SECOND | H3_L3 | MTR | other",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            "lineage_status: same_lineage / reset / unclear / pending",
            "lineage_id:",
            "历史显示值 `RFB_SECOND` 只映射到兼容主标签 `RFB`",
        ):
            self.assertIn(token, content, token)

        for field in ("attempt", "same_lineage"):
            self.assertFalse(has_active_field(content, field), field)

    def test_visual_frameworks_have_evidence_and_separate_state_axes(self):
        common_tokens = (
            "contract_scope:",
            "data_status:",
            "as_of_time:",
            "timeframes_seen:",
            "daily_context_window:",
            "major_high_low_review:",
            "ema20_50_200_review:",
            "direction: long / short / no_valid_direction",
            "order_branch:",
            "research_state:",
            "trade_state:",
            "gate_result:",
            "handoff_status: research_only / not_ready / ready_for_system",
        )
        stale_fields = (
            "final_state",
            "order_contract",
            "first_obstacle",
            "rough_rr",
            "three_push_state",
            "trigger_order",
            "actual_or_assumed_fill",
            "review_timeframe",
        )
        for path in ACTIVE_FRAMEWORKS:
            content = read(path)
            with self.subTest(path=path.relative_to(REPO_ROOT).as_posix()):
                for token in common_tokens:
                    self.assertIn(token, content, token)
                first_obstacle_field = (
                    "parent_first_independent_obstacle:"
                    if path.name == "multitimeframe_visual_review_framework_CN.md"
                    else "first_independent_obstacle:"
                )
                self.assertIn(first_obstacle_field, content)
                for field in stale_fields:
                    self.assertFalse(has_active_field(content, field), field)

    def test_migrated_audits_keep_canonical_geometry_and_state_axes(self):
        for path in MIGRATED_DOCUMENTS:
            content = read(path)
            with self.subTest(path=path.relative_to(REPO_ROOT).as_posix()):
                self.assertIn("first_independent_obstacle", content)
                self.assertIn("research_state", content)
                self.assertIn("trade_state", content)
                self.assertIn("gate_result", content)
                self.assertFalse(has_active_field(content, "final_state"))
                self.assertFalse(has_active_field(content, "order_contract"))

    def test_audit_is_indexed_and_preserves_research_boundary(self):
        audit = read(AUDIT)
        for token in (
            "23 个活动文档",
            "no-new-positive",
            "validated win-rate: not-computable",
            "不修改 Codex Trading",
            "不创建量化扫描器",
            "不连接 Futu/OpenD",
            "不连接 Execution Agent",
            "不修改 CSV/历史结果/engine 有效语义",
        ):
            self.assertIn(token, audit, token)

        for path in INDEXES:
            self.assertIn(AUDIT.name, read(path), path.as_posix())


if __name__ == "__main__":
    unittest.main()

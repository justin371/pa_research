import re
from pathlib import Path
import unittest

from pa_test_support import isolated_repo, run_docs_validator


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = (
    REPO_ROOT
    / "research"
    / "backtesting"
    / "visual_authority_schema_alignment_audit_2026-08-29_CN.md"
)
REMAINING_FRAMEWORK_AUDIT = (
    REPO_ROOT
    / "research"
    / "backtesting"
    / "remaining_visual_framework_contract_audit_2026-08-29_CN.md"
)
VISUAL_CARD = REPO_ROOT / "docs" / "visual_pa_review_card_CN.md"
DAILY_RULES = REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"

CANONICAL_PARENT_STATE = (
    "parent_state: open_trend / trading_range / range_edge / transition / climax / unclear"
)
LEGACY_PARENT_STATE_LINE = re.compile(
    r"(?m)^\s*(?:parent_state|market_state):\s+"
    r"(?:trend|range|channel|mature_range|climax_or_exhaustion|accepted_breakout|event-or-gap)"
    r"\s*(?:/.*)?$"
)

ACTIVE_FRAMEWORKS = (
    REPO_ROOT / "research" / "market_state_context_visual_evidence_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "inside_bar_two_bar_reversal_visual_framework_CN.md",
    REPO_ROOT / "research" / "triangle_expanding_range_visual_framework_CN.md",
    REPO_ROOT / "research" / "late_trend_entry_visual_framework_CN.md",
    REPO_ROOT / "research" / "multitimeframe_visual_review_framework_CN.md",
    REPO_ROOT / "research" / "channel_visual_framework_CN.md",
    REPO_ROOT / "research" / "bop_gap_acceptance_framework_CN.md",
    REPO_ROOT / "research" / "order_branch_visual_protocol_CN.md",
    REPO_ROOT / "research" / "failed_breakout_climax_visual_framework_CN.md",
    REPO_ROOT / "research" / "final_flag_visual_framework_CN.md",
    REPO_ROOT / "research" / "mtr_visual_framework_CN.md",
    REPO_ROOT / "research" / "head_shoulders_rounded_top_bottom_visual_framework_CN.md",
    REPO_ROOT / "research" / "opening_reversal_visual_framework_CN.md",
    REPO_ROOT / "research" / "three_push_pressure_state_framework_CN.md",
)

CANONICAL_MAPPING_TEMPLATES = (
    REPO_ROOT / "research" / "cross_pattern_visual_priority_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "priority_pattern_visual_candidate_matrix_2026-08-24_CN.md",
    REPO_ROOT / "strategy" / "pattern_inventory_candidates.md",
    REPO_ROOT / "research" / "channel_visual_framework_CN.md",
    REPO_ROOT / "research" / "channel_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "channel_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "h1_l1_first_entry_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "h2_l2_second_entry_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "multitimeframe_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "late_trend_entry_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "event_sector_market_gate_visual_evidence_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "order_risk_contract_visual_evidence_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "opening_reversal_visual_framework_CN.md",
)

CURRENT_PARENT_STATE_TEMPLATES = CANONICAL_MAPPING_TEMPLATES + (
    REPO_ROOT / "research" / "double_top_bottom_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "double_top_bottom_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "failed_breakout_climax_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "head_shoulders_rounded_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "head_shoulders_rounded_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "inside_bar_two_bar_reversal_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "inside_bar_two_bar_reversal_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "support_resistance_visual_evidence_gap_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "triangle_expanding_range_visual_boundary_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "triangle_expanding_range_visual_evidence_gap_audit_2026-08-24_CN.md",
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
            "primary_pattern: ABC_CONT | BOP | H1_L1 | H2_L2 | H3_L3 | RFB | MTR | other",
            "pattern_family: ABC_CONT | BOP | H1_L1 | H2_L2 | RFB_SECOND | H3_L3 | MTR | other",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            "lineage_status: same_lineage / reset / unclear / pending",
            "lineage_id:",
            "历史显示值 `RFB_SECOND` 只映射到兼容主标签 `RFB`",
        ):
            self.assertIn(token, content, token)

        for field in ("attempt", "same_lineage"):
            self.assertFalse(has_active_field(content, field), field)
        self.assertIn(CANONICAL_PARENT_STATE, content)
        self.assertNotRegex(content, LEGACY_PARENT_STATE_LINE)

    def test_fast_screen_uses_visual_candidate_not_primary_pattern(self):
        content = read(VISUAL_CARD)
        fast_screen = re.search(
            r"(?s)## 快速视觉初筛：先判断像不像(?P<section>.*?)## 快筛停止条件",
            content,
        )
        self.assertIsNotNone(fast_screen)
        section = fast_screen.group("section")
        self.assertIn(
            "pattern_candidate: ABC-CONT / H1-H2-H3 / L1-L2-L3 / range-edge / MTR / other",
            section,
        )
        self.assertIsNone(re.search(r"(?m)^\s*primary_pattern\s*:", section))

    def test_current_mapping_templates_keep_primary_internal_and_direction_separate(self):
        primary_pattern = re.compile(
            r"(?m)^\s*primary_pattern:\s*"
            r"(?:ABC_CONT|BOP|H1_L1|H2_L2|H3_L3|RFB|MTR|other)\b"
        )
        for path in CANONICAL_MAPPING_TEMPLATES:
            content = read(path)
            with self.subTest(path=path.relative_to(REPO_ROOT).as_posix()):
                self.assertRegex(content, primary_pattern)
                self.assertIn("direction: long / short / no_valid_direction", content)
                self.assertIn(
                    "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
                    content,
                )
                for legacy_field in (
                    r"(?m)^\s*primary_pattern:\s*$",
                    r"(?m)^\s*internal_label:\s*$",
                    r"(?m)^\s*H_or_L_attempt(?:_and_signal_K)?\s*:",
                    r"(?m)^\s*parent_state_and_location\s*:",
                    r"(?m)^\s*parent_actual_or_assumed_fill\s*:",
                    r"(?m)^\s*actual_or_assumed_fill\s*:",
                    r"(?m)^\s*pattern_and_attempt\s*:",
                    r"(?m)^\s*decision_timestamp\s*:",
                    r"(?m)^\s*decision_time\s*:",
                ):
                    self.assertIsNone(re.search(legacy_field, content), legacy_field)

    def test_current_review_cards_use_canonical_parent_state(self):
        for path in CURRENT_PARENT_STATE_TEMPLATES:
            content = read(path)
            with self.subTest(path=path.relative_to(REPO_ROOT).as_posix()):
                self.assertIn(CANONICAL_PARENT_STATE, content)
                self.assertNotRegex(content, LEGACY_PARENT_STATE_LINE)

    def test_visual_frameworks_have_evidence_and_separate_state_axes(self):
        common_tokens = (
            "contract_scope:",
            "data_status:",
            "as_of_time:",
            "timeframes_seen:",
            "daily_context_window:",
            "major_high_low_review:",
            "ema20_50_200_review:",
            CANONICAL_PARENT_STATE,
            "direction: long / short / no_valid_direction",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            "state_transition:",
            "order_branch:",
            "branch_role:",
            "gap_policy:",
            "actual_fill_or_open_skip:",
            "structural_stop:",
            "structural_invalidation:",
            "first_independent_obstacle:",
            "rough_space_to_first_obstacle_R:",
            "pre_entry_space_R:",
            "space_status:",
            "rough_R_R:",
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

    def test_remaining_frameworks_keep_pattern_specific_fields_separate(self):
        checks = {
            "bop_gap_acceptance_framework_CN.md": (
                "breakout_boundary:",
                "acceptance_close:",
                "follow_through:",
                "retest_zone:",
                "role_reversal_held:",
            ),
            "failed_breakout_climax_visual_framework_CN.md": (
                "breakout_boundary:",
                "breakout_state:",
                "first_reverse:",
                "second_confirmation:",
                "third_push_state:",
            ),
            "final_flag_visual_framework_CN.md": (
                "final_flag_state:",
                "last_attempt_state:",
                "breakout_state:",
            ),
            "mtr_visual_framework_CN.md": (
                "mtr_state: reversal_attempt / mtr_candidate / mtr_confirmed_for_research / failed_mtr_thesis",
                "first_reverse:",
                "second_confirmation:",
            ),
            "head_shoulders_rounded_top_bottom_visual_framework_CN.md": (
                "shape_type:",
                "neckline:",
                "shoulder_separation:",
                "rounded_phase:",
                "breakout_state:",
            ),
            "opening_reversal_visual_framework_CN.md": (
                "pre_open_context:",
                "gap_or_open_position:",
                "first_opening_pressure:",
                "failure_or_acceptance:",
            ),
            "three_push_pressure_state_framework_CN.md": (
                "data_status:",
                "as_of_time:",
                "timeframes_seen:",
                "actual_fill_or_open_skip:",
                "handoff_status:",
            ),
            "visual_pattern_triage_protocol_CN.md": (
                "contract_scope: deep_review / historical_context_only",
                "signal_bar:",
                "confirmation_bar:",
                "new_trigger:",
                "order_branch:",
                "structural_stop:",
                "first_independent_obstacle:",
                "rough_space_to_first_obstacle_R:",
                "space_status:",
                "handoff_status:",
            ),
        }
        for name, tokens in checks.items():
            path = REPO_ROOT / "research" / name
            content = read(path)
            with self.subTest(path=path.relative_to(REPO_ROOT).as_posix()):
                for token in tokens:
                    self.assertIn(token, content, token)

    def test_order_protocol_has_no_merged_active_geometry_aliases(self):
        paths = (
            REPO_ROOT / "research" / "order_branch_visual_protocol_CN.md",
            REPO_ROOT / "research" / "order_contract_cross_pattern_audit_CN.md",
        )
        for path in paths:
            content = read(path)
            for field in (
                "decision_time",
                "trigger_price_or_zone",
                "actual_or_assumed_fill",
                "structural_stop_zone",
                "rough_space_to_obstacle",
                "gap_or_event_state",
                "timeframe_and_parent_contract",
                "trigger_or_zone",
                "space_to_first_obstacle",
                "final_status",
            ):
                self.assertFalse(has_active_field(content, field), f"{field}: {path}")
            self.assertIn("as_of_time:", content)
            self.assertIn("actual_fill_or_open_skip:", content)
            self.assertIn("rough_space_to_first_obstacle_R:", content)

    def test_opening_and_matrix_examples_do_not_merge_contract_fields(self):
        opening = read(REPO_ROOT / "research" / "opening_reversal_visual_framework_CN.md")
        for field in (
            r"(?m)^\s*pre_open_context\s*/\s*market_state\s*$",
            r"(?m)^\s*first_independent_obstacle\s*/\s*measured_move\s*$",
            r"(?m)^\s*event_and_sector_filter\s*$",
            r"(?m)^\s*outcome_at_decision_time\s*$",
        ):
            self.assertIsNone(re.search(field, opening), field)

        matrix = read(
            REPO_ROOT
            / "research"
            / "priority_pattern_visual_candidate_matrix_2026-08-24_CN.md"
        )
        self.assertIn("rough_R_R", matrix)
        self.assertNotRegex(matrix, r"(?m)^rough_RR:")
        self.assertNotRegex(matrix, r"(?m)^order:")
        self.assertNotRegex(matrix, r"(?m)^gate:")

    def test_abc_gap_reprice_uses_canonical_branch_role(self):
        content = read(REPO_ROOT / "patterns" / "03_abc_continuation" / "README.md")
        self.assertIn("branch_role: gap_reprice", content)
        self.assertNotRegex(content, r"(?m)^reprice_after_gap:")

    def test_daily_rules_and_migrated_templates_use_canonical_parent_state(self):
        self.assertIn(CANONICAL_PARENT_STATE, read(DAILY_RULES))
        for path in (
            REPO_ROOT
            / "research"
            / "cross_pattern_visual_priority_audit_2026-08-24_CN.md",
            REPO_ROOT / "research" / "abc_hl_stratified_outcome_audit_2026-08-24_CN.md",
        ):
            content = read(path)
            with self.subTest(path=path.relative_to(REPO_ROOT).as_posix()):
                self.assertIn(CANONICAL_PARENT_STATE, content)
                self.assertNotRegex(content, LEGACY_PARENT_STATE_LINE)

    def test_validator_rejects_legacy_parent_state_enum_in_active_template(self):
        with isolated_repo() as fixture_root:
            target = (
                fixture_root
                / "research"
                / "inside_bar_two_bar_reversal_visual_framework_CN.md"
            )
            target.write_text(
                read(target) + "\nparent_state: trend / range / channel / transition\n",
                encoding="utf-8",
            )

            result = run_docs_validator(fixture_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-canonical parent_state enum remains", result.stdout)

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

    def test_remaining_framework_audit_is_indexed_and_preserves_boundary(self):
        audit = read(REMAINING_FRAMEWORK_AUDIT)
        for token in (
            "remaining visual frameworks",
            "order_branch_visual_protocol_CN.md",
            "opening_reversal_visual_framework_CN.md",
            "state_transition",
            "actual_fill_or_open_skip",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

        for path in INDEXES:
            self.assertIn(REMAINING_FRAMEWORK_AUDIT.name, read(path), path.as_posix())


if __name__ == "__main__":
    unittest.main()

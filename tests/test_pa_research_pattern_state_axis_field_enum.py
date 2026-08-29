import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
PATTERNS_INDEX = PATTERNS_ROOT / "README.md"
RESEARCH_INDEX = REPO_ROOT / "research" / "README.md"
STRATEGY_INDEX = REPO_ROOT / "strategy" / "README.md"
SCHEMA = REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md"
VISUAL_CARD = REPO_ROOT / "docs" / "visual_pa_review_card_CN.md"
DAILY_RULES = REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md"
AUDIT_PATH = REPO_ROOT / "research" / "pattern_state_axis_field_enum_audit_2026-08-29_CN.md"


PATTERN_DIRS = (
    "01_h1_l1_first_entry",
    "02_h2_l2_second_entry",
    "03_abc_continuation",
    "04_range_edge_second_entry",
    "05_failed_breakout_climax",
    "06_breakout_pullback_bop",
    "07_mtr_reversal",
    "08_three_push_h3_l3",
    "09_vcp_minervini",
    "10_final_flag",
    "11_opening_reversal",
    "12_channel",
    "13_inside_bar_two_bar_reversal",
    "14_triangle_expanding_range",
    "15_double_top_bottom",
    "16_head_shoulders_rounded",
)
CORE_ORDER_BRANCH_DIRS = PATTERN_DIRS[3:8]


def read(path):
    return path.read_text(encoding="utf-8")


class PatternStateAxisFieldEnumTests(unittest.TestCase):
    def test_state_transition_enum_is_canonical_across_authority_docs(self):
        canonical = "state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate"
        for path in (SCHEMA, VISUAL_CARD, DAILY_RULES):
            self.assertIn(canonical, read(path), path.as_posix())
        self.assertNotIn("state_transition: none / pending / BOP /", read(VISUAL_CARD))

    def test_pattern_index_uses_expanded_canonical_field_names(self):
        index = read(PATTERNS_INDEX)
        for token in (
            "lineage_status / lineage_id / internal_label / attempt_direction / third_push_state / first_reverse / second_confirmation / range_edge_three_push / range_edge_side",
            "daily_context_window / major_high_low_review / ema20_50_200_review",
            "signal_bar / confirmation_bar / new_trigger / follow_through",
            "structural_stop / structural_invalidation",
            "first_independent_obstacle / rough_space_to_first_obstacle_R / space_status / rough_R_R",
            "event_context / event_bucket / sector_state / market_state / permission / gate_result",
        ):
            self.assertIn(token, index, token)
        self.assertNotIn("lineage_and_attempt_count", index)
        self.assertNotIn("signal_bar_and_trigger", index)
        self.assertNotIn("structural_stop / invalidation", index)

    def test_active_pattern_readmes_do_not_use_legacy_status_aliases(self):
        observation_alias = re.compile(r"(?<![\w-])observation-only(?![\w-])", re.IGNORECASE)
        no_trade_alias = re.compile(r"(?<![A-Za-z_])no_trade(?![A-Za-z_])", re.IGNORECASE)
        for directory in PATTERN_DIRS:
            content = read(PATTERNS_ROOT / directory / "README.md")
            self.assertIsNone(observation_alias.search(content), directory)
            self.assertIsNone(no_trade_alias.search(content), directory)

    def test_mtr_state_is_separate_from_canonical_thesis_state(self):
        content = read(PATTERNS_ROOT / "07_mtr_reversal" / "README.md")
        self.assertIn(
            "mtr_state: reversal_attempt / mtr_candidate / mtr_confirmed_for_research / failed_mtr_thesis",
            content,
        )
        self.assertIn("thesis_state: working / failed / invalidated / replaced / pending", content)
        self.assertIsNone(re.search(r"(?m)^thesis_state:.*(?:reversal|MTR|failed-MTR)", content))

    def test_core_pattern_order_branch_templates_keep_research_stop_limit(self):
        for directory in CORE_ORDER_BRANCH_DIRS:
            content = read(PATTERNS_ROOT / directory / "README.md")
            order_line = next(
                line for line in content.splitlines() if line.startswith("order_branch:")
            )
            self.assertIn("stop_limit", order_line, directory)
            self.assertIn("observation_only", order_line, directory)

    def test_audit_covers_scope_and_all_sixteen_directories(self):
        audit = read(AUDIT_PATH)
        for directory in PATTERN_DIRS:
            self.assertIn(f"../patterns/{directory}/README.md", audit, directory)
        for index_path in (PATTERNS_INDEX, RESEARCH_INDEX, STRATEGY_INDEX):
            self.assertIn(AUDIT_PATH.name, read(index_path), index_path.as_posix())
        for token in (
            "state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)


if __name__ == "__main__":
    unittest.main()

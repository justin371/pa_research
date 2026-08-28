from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
AUDIT_PATH = (
    REPO_ROOT
    / "research"
    / "common_visual_preflight_field_consistency_audit_2026-08-29_CN.md"
)


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


def read(path):
    return path.read_text(encoding="utf-8")


class CommonVisualPreflightFieldTests(unittest.TestCase):
    def test_core_documents_use_canonical_visual_preflight_fields(self):
        schema = read(REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md")
        visual = read(REPO_ROOT / "docs" / "visual_pa_review_card_CN.md")
        daily = read(REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md")
        common = read(REPO_ROOT / "docs" / "common_context.md")
        rules = read(
            REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md"
        )

        canonical_schema_tokens = (
            "chart_scope: full / partial / unavailable",
            "daily_context_window: >=2y / <2y / unavailable",
            "major_high_low_review: complete / partial / unavailable",
            "ema20_50_200_review: complete / partial / unavailable",
            "a_leg_quality: strong / ordinary / unclear / event_driven",
            "b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear",
            "b_leg_location:",
        )
        for token in canonical_schema_tokens:
            with self.subTest(document="schema", token=token):
                self.assertIn(token, schema)

        self.assertNotIn("chart_scope: full / partial\n", schema)

        for token in (
            "chart_scope:             # full / partial / unavailable",
            "event_context:           # none / earnings / macro / gap / other / unknown",
            "a_leg_quality: strong / ordinary / unclear / event_driven",
            "b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear",
            "b_leg_location:",
        ):
            with self.subTest(document="visual", token=token):
                self.assertIn(token, visual)
        for stale in ("none known", "A_quality:", "B_quality:", "location_of_B_end:"):
            self.assertNotIn(stale, visual)

        for token in (
            "chart_scope: full / partial / unavailable",
            "timeframes_seen:",
            "ema20_50_200_review: complete / partial / unavailable",
            "daily_ema20_50_200:",
            "two_year_chart_coverage",
            "canonical `major_highs_lows`",
        ):
            with self.subTest(document="daily", token=token):
                self.assertIn(token, daily)
        self.assertNotIn("chart_scope: full_2y_plus_local_zoom", daily)
        self.assertNotIn("final_state:\n", daily)

        for token in (
            "### Common visual preflight",
            "data_status: historical / delayed / live_confirmed / incomplete",
            "chart_scope: full / partial / unavailable",
            "daily_context_window: >=2y / <2y / unavailable",
            "major_high_low_review: complete / partial / unavailable",
            "ema20_50_200_review: complete / partial / unavailable",
            "a_leg_quality: strong / ordinary / unclear / event_driven",
            "b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear",
            "first_independent_obstacle:",
        ):
            with self.subTest(document="common_context", token=token):
                self.assertIn(token, common)

        for token in (
            "completed_bar_as_of:",
            "avg_20d_dollar_volume_usd:",
            "daily_context_window: >=2y / <2y / unavailable",
            "chart_scope: full / partial / unavailable",
            "major_high_low_review: complete / partial / unavailable",
            "ema20_50_200_review: complete / partial / unavailable",
            "a_leg_quality: strong / ordinary / unclear / event_driven",
            "b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear",
            "why_it_meets_or_fails_the_rule:",
            "possible_entry_trigger:",
        ):
            with self.subTest(document="daily_rules", token=token):
                self.assertIn(token, rules)
        for stale in (
            "completed_daily_bar_as_of:",
            "average_dollar_volume_20d:",
            "two_year_daily_context:",
            "why_it_meets_the_rule:",
            "possible_daily_entry_trigger:",
        ):
            self.assertNotIn(stale, rules)

    def test_all_pattern_readmes_carry_the_same_evidence_header_boundary(self):
        for directory in PATTERN_DIRS:
            content = read(PATTERNS_ROOT / directory / "README.md")
            with self.subTest(directory=directory):
                self.assertIn(
                    "../../docs/pa_research_output_schema_v0_1_CN.md", content
                )
                self.assertIn(
                    "../../docs/visual_pa_review_card_CN.md", content
                )
                self.assertIn(
                    "data_status: historical / delayed / live_confirmed / incomplete",
                    content,
                )
                for token in ("as_of_time", "chart_scope", "timeframes_seen"):
                    self.assertIn(token, content)
                self.assertIn("至少两年的 Daily 左侧背景", content)
                self.assertTrue("重要高点" in content or "主要高点" in content)
                self.assertTrue("重要低点" in content or "主要低点" in content)
                self.assertIn("EMA20/50/200", content)
                self.assertIn("pending", content)
                self.assertTrue(
                    "第一独立障碍" in content
                    or "first_independent_obstacle" in content
                    or "首障碍" in content
                )

    def test_pattern_index_and_pattern_specific_state_keep_canonical_boundary(self):
        index = read(PATTERNS_ROOT / "README.md")
        for token in (
            "timeframes_seen / data_status / as_of_time / timezone / session_state / chart_scope",
            "left_structure_and_location / major_highs_lows / support_resistance_and_role_zones",
            "daily_ema20_50_200 / a_leg_quality / b_leg_class / b_leg_location",
            "main_uncertainty_or_exclusion / failure_or_no_trade_reason",
        ):
            self.assertIn(token, index)
        self.assertNotIn("timeframe / data_status / as_of_time", index)
        self.assertNotIn("parent_state / market_context\n", index)

        failed_breakout = read(
            PATTERNS_ROOT / "05_failed_breakout_climax" / "README.md"
        )
        self.assertIn("breakout_climax_state:", failed_breakout)
        self.assertNotIn("final_state:", failed_breakout)
        self.assertIn("canonical `research_state`", failed_breakout)

    def test_audit_is_indexed_and_preserves_research_boundary(self):
        report = read(AUDIT_PATH)
        for path in (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            PATTERNS_ROOT / "README.md",
        ):
            self.assertIn(AUDIT_PATH.name, read(path), path.as_posix())
        for directory in PATTERN_DIRS:
            self.assertIn(f"../patterns/{directory}/README.md", report, directory)
        for token in (
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
            "no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, report, token)


if __name__ == "__main__":
    unittest.main()

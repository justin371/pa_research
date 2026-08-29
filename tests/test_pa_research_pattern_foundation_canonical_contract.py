from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
FOUNDATIONS_ROOT = REPO_ROOT / "foundations"
AUDIT_PATH = (
    REPO_ROOT
    / "research"
    / "backtesting"
    / "pattern_foundation_canonical_contract_audit_2026-08-29_CN.md"
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

FOUNDATION_DIRS = (
    "01_support_resistance",
    "02_measured_move_targets",
    "03_late_trend_entry_filter",
    "04_multitimeframe_review",
    "05_event_sector_market_gate",
    "06_order_risk_contracts",
    "07_market_state_context",
    "08_leg_pressure_signal_quality",
)

FOUNDATION_CANONICAL_TOKENS = {
    "03_late_trend_entry_filter": (
        "contract_scope: deep_review / daily_candidate / historical_context_only",
        "timeframes_seen:",
        "daily_context_window: >=2y / <2y / unavailable",
        "major_high_low_review: complete / partial / unavailable",
        "ema20_50_200_review: complete / partial / unavailable",
        "direction: long / short / no_valid_direction",
        "order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only",
        "actual_fill_or_open_skip:",
        "structural_stop:",
        "first_independent_obstacle:",
        "pre_entry_space_R:",
        "space_status:",
        "research_state:",
        "trade_state:",
        "gate_result:",
        "handoff_status:",
    ),
    "04_multitimeframe_review": (
        "chart_scope: full / partial / unavailable",
        "daily_context_window: >=2y / <2y / unavailable",
        "major_high_low_review: complete / partial / unavailable",
        "ema20_50_200_review: complete / partial / unavailable",
        "primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other",
        "signal_bar:",
        "new_trigger:",
        "actual_fill_or_open_skip:",
        "gap_policy:",
        "structural_stop:",
        "first_independent_obstacle:",
        "pre_entry_space_R:",
        "space_status:",
        "research_state:",
        "trade_state:",
        "gate_result:",
        "handoff_status:",
    ),
    "05_event_sector_market_gate": (
        "contract_scope: deep_review",
        "data_status: historical / delayed / live_confirmed / incomplete",
        "as_of_time:",
        "timeframes_seen:",
        "direction: long / short / no_valid_direction",
        "permission: long_allowed / short_allowed / both_allowed / no_direction / unknown",
        "gate_result: pass / conditional / observation_only / valid_no_trade / pending",
    ),
    "06_order_risk_contracts": (
        "contract_scope: deep_review / daily_candidate / historical_context_only",
        "as_of_time:",
        "timeframes_seen:",
        "new_trigger:",
        "order_price_or_zone:",
        "order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only",
        "actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable",
        "structural_invalidation:",
        "structural_stop:",
        "first_independent_obstacle:",
        "rough_space_to_first_obstacle_R:",
        "pre_entry_space_R:",
        "space_status:",
        "research_state:",
        "trade_state:",
        "gate_result:",
        "handoff_status:",
    ),
    "07_market_state_context": (
        "contract_scope: deep_review / daily_candidate / historical_context_only",
        "data_status: historical / delayed / live_confirmed / incomplete",
        "timeframes_seen:",
        "daily_context_window: >=2y / <2y / unavailable",
        "parent_state: open_trend / trading_range / range_edge / transition / climax / unclear",
        "range_state: mature / developing / transition / not_range",
        "lineage_status: same_lineage / reset / unclear / pending",
        "state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate",
        "research_state:",
        "trade_state:",
        "gate_result:",
        "handoff_status:",
    ),
    "08_leg_pressure_signal_quality": (
        "a_leg_quality: strong / ordinary / unclear / event_driven",
        "b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear",
        "b_leg_location:",
        "signal_bar:",
        "confirmation_bar:",
        "new_trigger:",
        "follow_through:",
        "daily_ema20_slope: up / flat / down / unknown",
        "daily_ema50_slope: up / flat / down / unknown",
        "h_l_pullback_location:",
        "direction: long / short / no_valid_direction",
        "primary_pattern:",
        "internal_label:",
        "lineage_status:",
        "research_state:",
        "trade_state:",
        "gate_result:",
        "handoff_status:",
    ),
}

FOUNDATION_LEGACY_PATTERNS = {
    "03_late_trend_entry_filter": (
        r"(?m)^timeframe:",
        r"(?m)^actual_fill_assumption:",
        r"(?m)^rough_R_R_to_first_obstacle:",
        r"(?m)^final_state:",
    ),
    "04_multitimeframe_review": (
        r"(?m)^parent_pattern:",
        r"(?m)^actual_or_assumed_fill:",
        r"(?m)^gap_state:",
        r"(?m)^decision:",
    ),
    "06_order_risk_contracts": (
        r"(?m)^decision_time:",
        r"(?m)^timeframe_and_parent_contract:",
        r"(?m)^trigger_or_zone:",
        r"(?m)^actual_or_assumed_fill:",
        r"(?m)^space_to_first_obstacle:",
        r"(?m)^final_status:",
    ),
    "07_market_state_context": (
        r"(?m)^timeframe:",
        r"(?m)^attempt_lineage:",
        r"(?m)^breakout_acceptance:",
        r"(?m)^decision:",
        r"(?m)^parent_state:.*mature_range",
    ),
    "08_leg_pressure_signal_quality": (
        r"(?m)^A_quality:",
        r"(?m)^EMA20_slope:",
        r"(?m)^EMA50_slope:",
        r"(?m)^pullback_location:",
        r"(?m)^decision:",
    ),
}


def read(path):
    return path.read_text(encoding="utf-8")


class PatternFoundationCanonicalContractTests(unittest.TestCase):
    def test_all_pattern_readmes_inherit_common_contract(self):
        for directory in PATTERN_DIRS:
            content = read(PATTERNS_ROOT / directory / "README.md")
            with self.subTest(directory=directory):
                for token in (
                    "../../docs/pa_research_output_schema_v0_1_CN.md",
                    "../../docs/visual_pa_review_card_CN.md",
                    "data_status: historical / delayed / live_confirmed / incomplete",
                    "as_of_time",
                    "timeframes_seen",
                    "chart_scope",
                    "daily_context_window",
                    "primary_pattern",
                    "EMA20/50/200",
                    "pending",
                ):
                    self.assertIn(token, content, token)
                self.assertTrue("重要高点" in content or "主要高点" in content)
                self.assertTrue("重要低点" in content or "主要低点" in content)
                self.assertIn("支撑阻力", content)
                self.assertTrue(
                    "第一独立障碍" in content
                    or "first_independent_obstacle" in content
                    or "首障碍" in content
                )

    def test_three_push_local_card_uses_canonical_scope(self):
        content = read(PATTERNS_ROOT / "08_three_push_h3_l3" / "README.md")
        for token in (
            "contract_scope: deep_review / daily_candidate / historical_context_only",
            "timeframes_seen: Daily / 4H / 1H / 15m / other",
            "daily_context_window: >=2y / <2y / unavailable",
            "major_high_low_review: complete / partial / unavailable",
            "ema20_50_200_review: complete / partial / unavailable",
            "direction: long / short / no_valid_direction",
            "primary_pattern: ABC_CONT / BOP / H3_L3 / other",
            "lineage_status: same_lineage / reset / unclear / pending",
            "third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear",
            "state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate",
            "actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable",
            "structural_invalidation:",
            "structural_stop:",
            "first_independent_obstacle:",
            "rough_space_to_first_obstacle_R:",
            "pre_entry_space_R:",
            "count_timeframe",
        ):
            self.assertIn(token, content, token)
        self.assertIsNone(re.search(r"(?m)^timeframe:", content))
        self.assertIsNone(re.search(r"(?m)^context_timeframes_seen:", content))

    def test_three_push_local_card_uses_the_complete_thesis_state_enum(self):
        content = read(PATTERNS_ROOT / "08_three_push_h3_l3" / "README.md")
        self.assertIn(
            "thesis_state: working / failed / invalidated / replaced / pending",
            content,
        )

    def test_event_gate_matches_the_daily_earnings_hard_exclusion(self):
        event_gate = read(FOUNDATIONS_ROOT / "05_event_sector_market_gate" / "README.md")
        daily_rules = read(
            REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md"
        )
        expected = (
            "已知财报在未来三个交易 session 内：不新开仓，不赌财报；候选写 "
            "`gate_result: valid_no_trade` 和 `trade_state: valid_no_trade`"
        )
        self.assertIn(expected, event_gate)
        for token in (
            "earnings_next_three_sessions: yes",
            "gate_result: valid_no_trade",
            "trade_state: valid_no_trade",
        ):
            self.assertIn(token, daily_rules)
        self.assertNotIn(
            "候选写 `gate_result: valid_no_trade` 或 `gate_result: pending`",
            event_gate,
        )

    def test_late_trend_pattern_whitelist_is_scoped_to_the_contract(self):
        content = read(
            FOUNDATIONS_ROOT / "03_late_trend_entry_filter" / "README.md"
        )
        self.assertIn(
            "当 `contract_scope: daily_candidate` 时，下面的 `primary_pattern` 只能写 `ABC_CONT` 或 `BOP`",
            content,
        )

    def test_foundation_index_and_readmes_keep_authority_links(self):
        index = read(FOUNDATIONS_ROOT / "README.md")
        self.assertIn("pa_research_output_schema_v0_1_CN.md", index)
        self.assertIn("visual_pa_review_card_CN.md", index)
        self.assertIn(AUDIT_PATH.name, index)
        for directory in FOUNDATION_DIRS:
            with self.subTest(directory=directory):
                self.assertIn(f"{directory}/README.md", index)
                content = read(FOUNDATIONS_ROOT / directory / "README.md")
                self.assertIn(
                    "../../docs/pa_research_output_schema_v0_1_CN.md", content
                )

    def test_active_foundation_templates_use_canonical_fields(self):
        for directory, tokens in FOUNDATION_CANONICAL_TOKENS.items():
            content = read(FOUNDATIONS_ROOT / directory / "README.md")
            with self.subTest(directory=directory):
                for token in tokens:
                    self.assertIn(token, content, token)

    def test_active_foundation_legacy_keys_are_absent(self):
        for directory, patterns in FOUNDATION_LEGACY_PATTERNS.items():
            content = read(FOUNDATIONS_ROOT / directory / "README.md")
            with self.subTest(directory=directory):
                for pattern in patterns:
                    self.assertIsNone(re.search(pattern, content), pattern)

    def test_audit_and_indexes_preserve_research_boundary(self):
        report = read(AUDIT_PATH)
        for directory in PATTERN_DIRS:
            self.assertIn(f"../../patterns/{directory}/README.md", report, directory)
        for directory in FOUNDATION_DIRS:
            self.assertIn(
                f"../../foundations/{directory}/README.md", report, directory
            )
        for path in (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            PATTERNS_ROOT / "README.md",
            FOUNDATIONS_ROOT / "README.md",
        ):
            self.assertIn(AUDIT_PATH.name, read(path), path.as_posix())
        for token in (
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, report, token)


if __name__ == "__main__":
    unittest.main()

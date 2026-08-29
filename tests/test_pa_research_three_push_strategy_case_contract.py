from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
STRATEGY = REPO_ROOT / "strategy" / "01_three_push_wedge_candidate.md"
GATE = REPO_ROOT / "research" / "h3_l3_research_gate_CN.md"
VISUAL = REPO_ROOT / "research" / "h3_l3_visual_comparison_CN.md"
PRESSURE = REPO_ROOT / "research" / "three_push_pressure_state_framework_CN.md"
MTR = REPO_ROOT / "research" / "mtr_visual_framework_CN.md"
MTR_THREE_PUSH = REPO_ROOT / "research" / "mtr_three_push_visual_boundary_audit_2026-08-24_CN.md"
AUDIT = REPO_ROOT / "research" / "backtesting" / "three_push_strategy_case_contract_audit_2026-08-29_CN.md"


THIRD_PUSH_ENUM = (
    "third_push_state: exhaustion_candidate / continuation_or_climax / "
    "range_repeat_test / channel_continuation / unclear"
)
LINEAGE_ENUM = "lineage_status: same_lineage / reset / unclear / pending"
SPACE_ENUM = (
    "space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / "
    "borderline / blocked / unknown"
)
PRIMARY_ENUM = (
    "primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other"
)
INTERNAL_ENUM = "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending"
MTR_STATE_ENUM = (
    "mtr_state: reversal_attempt / mtr_candidate / "
    "mtr_confirmed_for_research / failed_mtr_thesis"
)


def read(path):
    return path.read_text(encoding="utf-8")


class ThreePushStrategyCaseContractTests(unittest.TestCase):
    def test_strategy_maps_explanatory_buckets_to_canonical_contract(self):
        content = read(STRATEGY)
        for token in (
            "no-new-positive",
            "validated win-rate: not-computable",
            "A/B/C 是解释性分流，不是新的状态枚举",
            "contract_scope: deep_review / daily_candidate / historical_context_only",
            PRIMARY_ENUM,
            INTERNAL_ENUM,
            LINEAGE_ENUM,
            "attempt_direction: bullish_attempts / bearish_attempts / unknown",
            THIRD_PUSH_ENUM,
            "first_reverse: none / touch / structural_break",
            "second_confirmation: yes / no / pending",
            "range_edge_side: upper / lower / none / pending",
            "direction: long / short / no_valid_direction",
            "first_independent_obstacle:",
            SPACE_ENUM,
            "research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending",
            "trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending",
            "gate_result: pass / conditional / observation_only / valid_no_trade / pending",
        ):
            self.assertIn(token, content, token)
        self.assertNotIn("research_positive_candidate", content)
        self.assertNotIn("valid no-trade", content)

    def test_active_three_push_documents_use_canonical_axes(self):
        for path in (GATE, VISUAL, PRESSURE):
            content = read(path)
            self.assertIn(PRIMARY_ENUM, content, path.as_posix())
            self.assertIn(INTERNAL_ENUM, content, path.as_posix())
            self.assertIn(THIRD_PUSH_ENUM, content, path.as_posix())
            self.assertIn(LINEAGE_ENUM, content, path.as_posix())
            self.assertIn("first_reverse: none / touch / structural_break", content, path.as_posix())
            self.assertIn("second_confirmation: yes / no / pending", content, path.as_posix())
            self.assertIn("direction: long / short / no_valid_direction", content, path.as_posix())

        visual = read(VISUAL)
        self.assertIn("| 案例 | `lineage_status` | 第三推效率 / `third_push_state` |", visual)
        self.assertIn("research_positive_conditional", visual)
        for legacy in ("h3_l3_state:", "reverse_trigger_present", "short_reaction_candidate"):
            self.assertNotIn(legacy, visual, legacy)

        pressure = read(PRESSURE)
        for legacy in (
            "same_lineage:",
            "first_obstacle:",
            "rough_rr:",
            "status: research_candidate / short_reaction / continuation / valid_no_trade",
        ):
            self.assertNotIn(legacy, pressure, legacy)

    def test_mtr_state_uses_the_mtr_pattern_enum(self):
        for path in (REPO_ROOT / "patterns" / "07_mtr_reversal" / "README.md", MTR_THREE_PUSH):
            content = read(path)
            self.assertIn(MTR_STATE_ENUM, content, path.as_posix())
            self.assertIsNone(
                re.search(
                    r"(?m)^mtr_state: not_started / reversal_attempt / candidate / "
                    r"confirmed_for_research / failed$",
                    content,
                ),
            )
        self.assertRegex(
            read(MTR_THREE_PUSH),
            r"(?m)^primary_pattern: H3_L3 / MTR / other$",
        )
        self.assertIn(INTERNAL_ENUM, read(MTR_THREE_PUSH))

    def test_mtr_framework_does_not_use_short_reaction_as_pressure_state(self):
        content = read(MTR)
        self.assertIn(
            "`exhaustion_candidate`、`continuation_or_climax`、`range_repeat_test` 或 `channel_continuation`",
            content,
        )
        self.assertIn("research_positive_conditional", content)
        self.assertNotIn("short_reaction_candidate", content)

    def test_audit_preserves_case_boundaries_and_no_new_denominator(self):
        content = read(AUDIT)
        for path in (
            "../../strategy/01_three_push_wedge_candidate.md",
            "../h3_l3_research_gate_CN.md",
            "../h3_l3_visual_comparison_CN.md",
            "../three_push_pressure_state_framework_CN.md",
            "../mtr_visual_framework_CN.md",
            "../klac_h3_bear_flag_case_2025-03-12_2025-03-28.md",
            "../asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md",
        ):
            self.assertIn(path, content, path)
        for token in (
            "third_push_state=exhaustion_candidate",
            "first_independent_obstacle",
            "research_state=research_positive_conditional",
            "H3/L3 冻结行数为 0",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, content, token)
        self.assertIsNone(re.search(r"(?m)^research_positive_candidate", content))


if __name__ == "__main__":
    unittest.main()

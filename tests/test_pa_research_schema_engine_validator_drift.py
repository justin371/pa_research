from dataclasses import fields
from pathlib import Path
import re
import unittest

from pa_research_backtest import engine


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md"
VISUAL_CARD = REPO_ROOT / "docs" / "visual_pa_review_card_CN.md"
DAILY_CARD = REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md"
DAILY_RULES = REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md"
BACKTEST_README = REPO_ROOT / "research" / "backtesting" / "README.md"
ORDER_PROTOCOL = REPO_ROOT / "research" / "order_contract_cross_pattern_audit_CN.md"
VALIDATOR = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"

RAW_EVENT_CONTEXT_TOKEN = (
    "event_context: raw pre-entry event note (examples: none / earnings / macro / gap / other / unknown; "
    "dated/compound qualifiers allowed)"
)
VISUAL_RAW_EVENT_CONTEXT_TOKEN = (
    "event_context:           # raw pre-entry event note; examples: none / earnings / macro / gap / other / unknown; "
    "dated/compound qualifiers allowed"
)
ACTIVE_RAW_EVENT_TEMPLATES = (
    REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md",
    REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md",
    REPO_ROOT / "foundations" / "05_event_sector_market_gate" / "README.md",
    REPO_ROOT / "research" / "bop_gap_acceptance_framework_CN.md",
    REPO_ROOT / "research" / "bop_multiday_pullback_candidate_audit_2026-08-24_CN.md",
    REPO_ROOT / "research" / "common_visual_preflight_field_consistency_audit_2026-08-29_CN.md",
    REPO_ROOT / "research" / "event_sector_multitimeframe_cross_pattern_audit_CN.md",
    REPO_ROOT / "research" / "failed_breakout_climax_visual_framework_CN.md",
    REPO_ROOT / "research" / "final_flag_visual_framework_CN.md",
    REPO_ROOT / "research" / "head_shoulders_rounded_top_bottom_visual_framework_CN.md",
    REPO_ROOT / "research" / "mtr_visual_framework_CN.md",
    REPO_ROOT / "research" / "order_branch_visual_protocol_CN.md",
    REPO_ROOT / "research" / "opening_reversal_visual_framework_CN.md",
    REPO_ROOT / "research" / "visual_pattern_triage_protocol_CN.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_active_field(content: str, field: str) -> bool:
    return re.search(rf"(?m)^\s*{re.escape(field)}\s*:", content) is not None


class SchemaEngineValidatorDriftTests(unittest.TestCase):
    def test_engine_enum_sets_are_declared_in_validator_and_schema(self):
        self.assertEqual(engine.SUPPORTED_DIRECTIONS, {"long", "short"})
        self.assertEqual(
            engine.SUPPORTED_PATTERNS,
            {"ABC_CONT", "BOP", "H1_L1", "H2_L2", "H3_L3", "RFB", "MTR", "other"},
        )
        self.assertEqual(
            engine.SUPPORTED_LABELS,
            {"H1", "H2", "L1", "L2", "H3", "L3", "none", "pending"},
        )
        self.assertEqual(engine.SUPPORTED_EMA_SLOPES, {"up", "flat", "down", "unknown"})
        self.assertEqual(
            engine.SUPPORTED_H_L_EMA_GATES,
            {"long_pass", "short_pass", "fail_flat_or_opposite", "pending", "not_applicable"},
        )
        self.assertEqual(
            engine.SUPPORTED_SPACE_STATUSES,
            {"strict_ge_1R", "borderline_ge_1R", "clearly_positive", "borderline", "blocked", "unknown"},
        )
        self.assertEqual(engine.SUPPORTED_META_CONFLUENCE, {"present", "absent", "unknown"})
        self.assertEqual(
            engine.SUPPORTED_ORDER_BRANCHES,
            {"stop_confirmation", "limit_retest", "market_close"},
        )
        self.assertEqual(
            engine.SUPPORTED_GAP_POLICIES,
            {"accept_open", "skip", "flag_only", "not_applicable"},
        )

        validator = read(VALIDATOR)
        schema = read(SCHEMA)
        for token in (
            "'long'",
            "'short'",
            "'ABC_CONT'",
            "'BOP'",
            "'H1_L1'",
            "'H2_L2'",
            "'H3_L3'",
            "'RFB'",
            "'MTR'",
            "'other'",
            "'strict_ge_1R'",
            "'borderline_ge_1R'",
            "'clearly_positive'",
            "'fail_flat_or_opposite'",
            "'not_applicable'",
            "'stop_confirmation'",
            "'limit_retest'",
            "'market_close'",
            "'accept_open'",
            "'flag_only'",
        ):
            self.assertIn(token, validator, token)
        for token in (
            "direction: long / short / no_valid_direction",
            "primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            "daily_ema20_slope: up / flat / down / unknown",
            "h_l_ema_slope_gate: long_pass / short_pass / fail_flat_or_opposite / pending / not_applicable",
            "space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown",
            "meta_confluence: present / absent / unknown",
            "order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only",
            "gap_policy: accept_open / skip / flag_only / not_applicable",
        ):
            self.assertIn(token, schema, token)

    def test_active_event_context_is_raw_and_event_bucket_is_the_closed_axis(self):
        schema = read(SCHEMA)
        self.assertIn(RAW_EVENT_CONTEXT_TOKEN, schema)
        self.assertIn("`event_context` 不是封闭枚举", schema)
        self.assertIn("event_bucket: ordinary_non_event", schema)
        for path in ACTIVE_RAW_EVENT_TEMPLATES:
            with self.subTest(path=path.relative_to(REPO_ROOT).as_posix()):
                content = read(path)
                self.assertIn(RAW_EVENT_CONTEXT_TOKEN, content)
                self.assertNotIn(
                    "event_context: none / earnings / macro / gap / other / unknown",
                    content,
                )

        visual = read(VISUAL_CARD)
        self.assertIn(VISUAL_RAW_EVENT_CONTEXT_TOKEN, visual)
        self.assertIn("`event_context` 是可带日期、来源和复合限定的原始事前事件记录", visual)

    def test_result_evidence_status_includes_engine_non_trade_state(self):
        schema = read(SCHEMA)
        engine_source = read(REPO_ROOT / "pa_research_backtest" / "engine.py")
        self.assertIn(
            "evidence_status: comparable / excluded / excluded_incomplete_horizon / excluded_ambiguous / observation_only / not-a-trade",
            schema,
        )
        self.assertIn('evidence_status = "not-a-trade"', engine_source)
        self.assertIn("`evidence_status: not-a-trade` 是 engine 对 no-fill、opening-skip 或 not-traded", schema)
        self.assertEqual(engine.TRADE_RESULTS, {"win", "loss", "scratch"})

    def test_visual_compatibility_pattern_list_keeps_daily_candidate_boundary(self):
        visual = read(VISUAL_CARD)
        self.assertIn(
            "primary_pattern: ABC_CONT | BOP | H1_L1 | H2_L2 | H3_L3 | RFB | MTR | other",
            visual,
        )
        self.assertIn(
            "pattern_family: ABC_CONT | BOP | H1_L1 | H2_L2 | RFB_SECOND | H3_L3 | MTR | other",
            visual,
        )
        for path in (DAILY_CARD, DAILY_RULES):
            self.assertIn("primary_pattern: ABC_CONT / BOP", read(path), path.as_posix())
        self.assertIn("`daily_candidate` 只允许 `ABC_CONT` 或 `BOP`", read(SCHEMA))

    def test_research_fields_have_explicit_projection_and_are_not_engine_contract_fields(self):
        schema = read(SCHEMA)
        readme = read(BACKTEST_README)
        dataclass_fields = {field.name for field in fields(engine.BacktestContract)}
        required_fields = set(engine.REQUIRED_CONTRACT_COLUMNS)

        for token in (
            "`new_trigger`",
            "`entry_trigger`",
            "`first_independent_obstacle`",
            "`first_obstacle`",
            "`actual_fill_or_open_skip`",
            "`fill_status`",
            "研究记录到当前回放器的字段映射只在冻结阶段显式发生",
        ):
            self.assertIn(token, schema, token)
        for token in (
            "`new_trigger` 先冻结为数值 `entry_trigger`",
            "`first_independent_obstacle` 先冻结为数值 `first_obstacle`",
            "`actual_fill_or_open_skip` 没有直接输入映射",
            "`event_context` 是可带日期/复合限定的原始事前事件说明",
        ):
            self.assertIn(token, readme, token)

        for research_only_field in (
            "new_trigger",
            "first_independent_obstacle",
            "actual_fill_or_open_skip",
            "state_transition",
            "bop_state",
            "branch_role",
            "a_leg_quality",
            "b_leg_class",
            "b_leg_location",
        ):
            self.assertNotIn(research_only_field, required_fields, research_only_field)
            self.assertNotIn(research_only_field, dataclass_fields, research_only_field)
        self.assertIn("entry_trigger", required_fields)
        self.assertIn("first_obstacle", required_fields)
        self.assertIn("entry_trigger", dataclass_fields)
        self.assertIn("first_obstacle", dataclass_fields)

    def test_cross_pattern_order_protocol_has_canonical_active_fields_only(self):
        content = read(ORDER_PROTOCOL)
        for token in (
            "contract_scope: deep_review / historical_context_only",
            "as_of_time:",
            "primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other",
            "new_trigger:",
            "actual_fill_or_open_skip:",
            "structural_invalidation:",
            "structural_stop:",
            "first_independent_obstacle:",
            "rough_space_to_first_obstacle_R:",
            "research_state:",
            "trade_state:",
            "这些旧名称不再作为统一订单卡的活动字段",
        ):
            self.assertIn(token, content, token)
        for field in (
            "decision_time",
            "timeframe_and_parent_contract",
            "trigger_or_zone",
            "actual_or_assumed_fill",
            "structural_stop_zone",
            "space_to_first_obstacle",
            "final_status",
        ):
            self.assertFalse(has_active_field(content, field), field)


if __name__ == "__main__":
    unittest.main()

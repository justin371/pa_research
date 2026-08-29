import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
AUDIT = REPO_ROOT / "research" / "evidence_scope_status_boundary_audit_2026-08-29_CN.md"
TRIAGE = REPO_ROOT / "research" / "visual_pattern_triage_protocol_CN.md"
BACKTEST_README = REPO_ROOT / "research" / "backtesting" / "README.md"
PATTERN_INVENTORY = REPO_ROOT / "strategy" / "pattern_inventory_candidates.md"
SMOKE = REPO_ROOT / "research" / "visual_recognition_smoke_test_2026-08-24_CN.md"


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


class EvidenceScopeStatusTests(unittest.TestCase):
    def test_all_pattern_readmes_require_per_symbol_daily_window(self):
        for directory in PATTERN_DIRS:
            content = read(PATTERNS_ROOT / directory / "README.md")
            with self.subTest(directory=directory):
                self.assertIn("data_status: historical / delayed / live_confirmed / incomplete", content)
                self.assertIn("timeframes_seen", content)
                self.assertIn("chart_scope", content)
                self.assertIn("daily_context_window", content)
                self.assertIn("至少两年的 Daily 左侧背景", content)

    def test_daily_candidate_scope_is_daily_only(self):
        schema = read(REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md")
        visual = read(REPO_ROOT / "docs" / "visual_pa_review_card_CN.md")
        daily_card = read(REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md")
        daily_rules = read(REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md")
        common = read(REPO_ROOT / "docs" / "common_context.md")

        self.assertIn(
            "当 `contract_scope: daily_candidate` 时，`timeframes_seen` 必须只写 `Daily`",
            schema,
        )
        self.assertIn(
            "当 `contract_scope: daily_candidate` 时，`timeframes_seen` 只能填写 `Daily`",
            visual,
        )
        self.assertIn("timeframes_seen: Daily", daily_rules)
        self.assertIn("4H/60m/15m 只在候选入选后的独立深审或订单合同中使用", common)
        for token in (
            "contract_scope: daily_candidate",
            "directional_bias: bull / bear / balanced / changing",
            "permission: long_allowed / short_allowed / both_allowed / no_direction / unknown",
            "lineage_id:",
            "market_context_id:",
            "bop_state: acceptance_watch / ordinary_pullback / failed_breakout / gap_event / bull_flag_continuation / not_applicable",
            "role_reversal_held: yes / no / unclear / not_occurred",
            "本卡逐标的记录的 `contract_scope` 固定为 `daily_candidate`：`timeframes_seen` 只能填写 `Daily`",
        ):
            self.assertIn(token, daily_card, token)

    def test_triage_protocol_uses_canonical_scope_fields(self):
        content = read(TRIAGE)
        self.assertIn("contract_scope: stage_1_fast_screen", content)
        self.assertIn("timeframes_seen:", content)
        self.assertNotRegex(content, r"(?m)^timeframe_seen:")
        self.assertIn("data_status: historical / delayed / live_confirmed / incomplete", content)
        self.assertIn("chart_scope: full / partial / unavailable", content)
        self.assertIn("daily_context_window: >=2y / <2y / unavailable", content)

    def test_legacy_records_do_not_mix_status_and_session_or_use_singular_timeframe(self):
        paths = (
            REPO_ROOT / "research" / "cost_bullish_abc_h2_visual_boundary_2025-04-21_2025-05-16.md",
            REPO_ROOT / "research" / "jnj_bullish_h1_first_obstacle_2025-09-18_2025-10-08.md",
            REPO_ROOT / "research" / "jpm_bullish_h1_first_obstacle_failure_2025-08-22_2025-09-05.md",
            REPO_ROOT / "research" / "nvda_bullish_h1_trigger_branch_first_obstacle_2025-04-21_2025-05-08.md",
            REPO_ROOT / "research" / "tsla_bearish_abc_candidate_screen_2026-08-22.md",
            REPO_ROOT / "research" / "tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md",
            SMOKE,
        )
        for path in paths:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                self.assertNotRegex(content, r"(?m)^timeframe_seen:")
                self.assertNotRegex(
                    content,
                    r"(?m)^data_status:\s*(?:historical_close|historical / after-close|historical public)",
                )
                for field in ("data_status:", "timeframes_seen:", "chart_scope:", "daily_context_window:"):
                    self.assertIn(field, content)

        for path in (
            REPO_ROOT / "research" / "tsla_bearish_abc_candidate_screen_2026-08-22.md",
            REPO_ROOT / "research" / "tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md",
        ):
            self.assertIn("data_status: historical", read(path))
            self.assertIn("session_state: historical_close", read(path))

        smoke = read(SMOKE)
        self.assertEqual(len(re.findall(r"^data_status: historical$", smoke, re.MULTILINE)), 5)
        self.assertEqual(len(re.findall(r"^daily_context_window: >=2y$", smoke, re.MULTILINE)), 4)
        self.assertIn("data_status_note: public data; not Futu; not live authorization", smoke)

    def test_replay_and_candidate_inventory_disclose_upstream_boundary(self):
        backtest = read(BACKTEST_README)
        inventory = read(PATTERN_INVENTORY)
        self.assertIn(
            "`contract_scope`、`data_status`、`chart_scope` 和 `timeframes_seen` 属于上游视觉/研究记录的证据 provenance",
            backtest,
        )
        self.assertIn("`daily_context_window` 不是“CSV 有两年价格”这一事实的别名", backtest)
        for token in (
            "timeframes_seen",
            "data_status: historical / delayed / live_confirmed / incomplete",
            "chart_scope: full / partial / unavailable",
            "daily_context_window: >=2y / <2y / unavailable",
            "如果目标是 `daily_candidate`，第一步只能看完成的 Daily",
            "只要“看起来像”只能先进入研究 inventory 的 `stage_1_fast_screen`/观察行",
            "contract_scope: stage_1_fast_screen / deep_review / daily_candidate / historical_context_only",
            "outcome                     # 仅独立 replay/result 的事后字段；候选记录保持 pending，不用于授权",
        ):
            self.assertIn(token, inventory)
        self.assertNotRegex(inventory, r"(?m)^timeframe$")

    def test_audit_and_indexes_cover_scope_status_boundary(self):
        audit = read(AUDIT)
        for token in (
            "contract_scope: daily_candidate",
            "timeframes_seen: Daily",
            "daily_context_window",
            "chart_scope",
            "data_status",
            "historical_close` 是 `session_state` 的值",
            "回放 CSV",
            "16 个 `patterns/*/README.md`",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

        for path in (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            PATTERNS_ROOT / "README.md",
        ):
            self.assertIn(AUDIT.name, read(path), path.as_posix())


if __name__ == "__main__":
    unittest.main()

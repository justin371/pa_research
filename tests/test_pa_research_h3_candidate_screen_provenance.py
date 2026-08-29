from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCREEN_2025 = REPO_ROOT / "research" / "h3_l3_candidate_screen_2025-08_2025-11_CN.md"
SCREEN_TARGETED = REPO_ROOT / "research" / "h3_l3_candidate_screen_futu_targeted_2024_2026_CN.md"
AUDIT = REPO_ROOT / "research" / "backtesting" / "h3_l3_candidate_screen_provenance_audit_2026-08-29_CN.md"


COMMON_FIELDS = (
    "lineage_status: same_lineage / reset / unclear / pending",
    "attempt_direction: bullish_attempts / bearish_attempts / unknown",
    "third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear",
    "first_reverse: none / touch / structural_break",
    "second_confirmation: yes / no / pending",
    "range_edge_three_push: yes / no / pending",
    "range_edge_side: upper / lower / none / pending",
    "direction: long / short / no_valid_direction",
    "state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate",
    "order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only",
    "gap_policy: accept_open / skip / flag_only / not_applicable",
    "first_independent_obstacle:",
    "space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown",
    "research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending",
    "trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending",
    "gate_result: pass / conditional / observation_only / valid_no_trade / pending",
)


def read(path):
    return path.read_text(encoding="utf-8")


class H3CandidateScreenProvenanceTests(unittest.TestCase):
    def test_both_logs_declare_historical_partial_evidence(self):
        for path in (SCREEN_2025, SCREEN_TARGETED):
            content = read(path)
            for token in (
                "contract_scope: historical_context_only",
                "data_status: historical",
                "as_of_time: unavailable_in_original_log",
                "timezone: unavailable_in_original_log",
                "session_state: historical_close_review",
                "chart_scope: partial",
                "timeframes_seen: Daily",
                *COMMON_FIELDS,
            ):
                self.assertIn(token, content, f"{token}: {path.as_posix()}")
            self.assertIn("no-new-positive", content, path.as_posix())
            self.assertIn("validated win-rate: not-computable", content, path.as_posix())
            self.assertIn("不是 `live_confirmed`", content)

    def test_existing_screen_conclusions_remain_boundary_conclusions(self):
        first = read(SCREEN_2025)
        for token in (
            "AVGO",
            "MSFT",
            "PANW",
            "MRVL",
            "DELL",
            "LULU",
            "TXN",
            "TGT 与 DIS",
            "NOW",
            "本轮暂未找到足以升级为 H3/L3 正向候选的图",
            "本日志不产生胜率分母",
        ):
            self.assertIn(token, first, token)

        targeted = read(SCREEN_TARGETED)
        for token in (
            "BKNG",
            "PM",
            "AMD",
            "GOOGL",
            "NKE",
            "valid_no_trade",
            "event-gap-boundary",
            "continuation-not-reversal",
            "当前没有达到该条件的独立 L3 正向样本",
            "不建立统计分母",
        ):
            self.assertIn(token, targeted, token)

    def test_audit_covers_source_scope_and_preserves_statistics(self):
        content = read(AUDIT)
        for token in (
            "../h3_l3_candidate_screen_2025-08_2025-11_CN.md",
            "../h3_l3_candidate_screen_futu_targeted_2024_2026_CN.md",
            "data_status: historical",
            "as_of_time: unavailable_in_original_log",
            "事件链接只覆盖明确列出的部分核对",
            "third_push_state",
            "opening-skip/gap-reprice",
            "7 份 CSV、60 行",
            "H3/L3 冻结行数为 0",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, content, token)


if __name__ == "__main__":
    unittest.main()

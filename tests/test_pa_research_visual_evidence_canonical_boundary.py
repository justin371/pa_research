"""Regression checks for historical visual evidence and canonical field boundaries."""

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
THREE_PUSH = REPO_ROOT / "research" / "three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md"
LINEAGE = REPO_ROOT / "research" / "h_l_lineage_visual_boundary_audit_2026-08-24_CN.md"
ROUND5 = REPO_ROOT / "research" / "visual_recognition_round5_two_year_daily_2026-08-24_CN.md"
AUDIT = REPO_ROOT / "research" / "backtesting" / "visual_evidence_canonical_boundary_audit_2026-08-29_CN.md"

CANONICAL_THIRD_PUSH = (
    "third_push_state: exhaustion_candidate / continuation_or_climax / "
    "range_repeat_test / channel_continuation / unclear"
)
CANONICAL_LINEAGE = "lineage_status: same_lineage / reset / unclear / pending"
CANONICAL_PATTERN = "primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other"
CANONICAL_SPACE = (
    "space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / "
    "borderline / blocked / unknown"
)


def read(path):
    return path.read_text(encoding="utf-8")


class VisualEvidenceCanonicalBoundaryTests(unittest.TestCase):
    def test_lineage_protocol_uses_canonical_axes_and_conservative_alias_mapping(self):
        content = read(LINEAGE)
        for token in (
            "contract_scope: historical_context_only",
            "data_status: historical / delayed / live_confirmed / incomplete",
            "major_high_low_review: complete / partial / unavailable",
            "ema20_50_200_review: complete / partial / unavailable",
            CANONICAL_LINEAGE,
            CANONICAL_PATTERN,
            "secondary_context:",
            "lineage_id:",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            "attempt_direction: bullish_attempts / bearish_attempts / unknown",
            CANONICAL_THIRD_PUSH,
            "first_reverse: none / touch / structural_break",
            "second_confirmation: yes / no / pending",
            "range_edge_three_push: yes / no / pending",
            "range_edge_side: upper / lower / none / pending",
            "order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only",
            "gap_policy: accept_open / skip / flag_only / not_applicable",
            CANONICAL_SPACE,
            "research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending",
            "历史自然语言标签",
            "lineage_status: pending",
            "third_push_state: range_repeat_test",
        ):
            self.assertIn(token, content, token)

        self.assertIsNone(re.search(r"(?m)^\s*lineage_status:\s*same-lineage", content))
        self.assertIsNone(re.search(r"(?m)^\s*third_push_state:\s*exhaustion-candidate", content))
        self.assertNotIn("state_result:", content)

    def test_round5_has_historical_evidence_header_and_case_summary(self):
        content = read(ROUND5)
        for token in (
            "contract_scope: historical_context_only",
            "data_status: historical",
            "as_of_time: per-case cutoff; query timestamp unavailable in original log",
            "timezone: unavailable_in_original_log",
            "session_state: historical_close",
            "timeframes_seen: Daily / 4H / 15m (case-specific)",
            "chart_scope: partial",
            "daily_context_window: >=2y (8/8 cases)",
            "major_high_low_review: complete (8/8 cases)",
            "ema20_50_200_review: complete (8/8 cases)",
            CANONICAL_LINEAGE,
            "聚合 provenance，故意不填写 active `primary_pattern`",
            "lineage_id",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            CANONICAL_THIRD_PUSH,
            CANONICAL_SPACE,
            "first_independent_obstacle: visual candidate only; not a frozen order field",
            "pre_entry_space_R: unknown unless trigger and structural stop are independently frozen",
            "order_branch: observation_only",
            "space_status: unknown",
            "no-new-positive: maintained",
        ):
            self.assertIn(token, content, token)

        self.assertEqual(len(re.findall(r"(?m)^### [1-8]\. ", content)), 8)
        for token in (
            "COHR 2026-05-13",
            "COHR 2026-06-22",
            "SPY 2026-06-15",
            "SPY 2026-07-15",
            "QQQ 2026-06-22",
            "QQQ 2026-07-17",
            "IWM 2026-05-28",
            "IWM 2026-06-25",
            "direction: long",
            "direction: short",
            "direction: no_valid_direction",
            "third_push_state: range_repeat_test",
            "lineage_status: pending",
            "lineage_status: unclear",
        ):
            self.assertIn(token, content, token)

        self.assertIsNone(re.search(r"(?m)^\s*lineage_status:\s*(?:same-lineage-provisional|same-pressure-zone-provisional|provisional)", content))
        self.assertIsNone(re.search(r"(?m)^\s*first_obstacle_candidate:", content))
        self.assertIsNone(re.search(r"(?m)^\s*primary_pattern:", content))
        self.assertIsNone(re.search(r"(?m)^\s*lineage_id:", content))

    def test_three_push_audit_preserves_conditional_not_production_boundary(self):
        content = read(THREE_PUSH)
        for token in (
            "validated win-rate: not-computable",
            "contract_scope: historical_context_only",
            CANONICAL_LINEAGE,
            CANONICAL_THIRD_PUSH,
            "first_reverse: none / touch / structural_break",
            "second_confirmation: yes / no / pending",
            "range_edge_side: upper / lower / none / pending",
            "direction: long / short / no_valid_direction",
            "first_independent_obstacle:",
            CANONICAL_SPACE,
            "research_state: research_positive_conditional",
            "trade_state: not_authorized",
            "research_positive_candidate",
            "历史说明别名",
            "no-new-positive",
        ):
            self.assertIn(token, content, token)

        self.assertNotIn("research_state: research_positive_candidate", content)
        self.assertIn("third_push_state: exhaustion_candidate", content)
        self.assertIn("third_push_state: range_repeat_test", content)

    def test_audit_and_indexes_record_scope_and_frozen_statistics_boundary(self):
        audit = read(AUDIT)
        for token in (
            "three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md",
            "h_l_lineage_visual_boundary_audit_2026-08-24_CN.md",
            "visual_recognition_round5_two_year_daily_2026-08-24_CN.md",
            "lineage_status: pending",
            "third_push_state: range_repeat_test",
            "space_status: unknown",
            "完整闭合逐案记录",
            "样本独立性",
            "7 份 CSV、60 行",
            "H3/L3 冻结合同仍为 0",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

        indexed_paths = (
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            REPO_ROOT / "research" / "backtesting" / "README.md",
        )
        for path in indexed_paths:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT.name, read(path))


if __name__ == "__main__":
    unittest.main()

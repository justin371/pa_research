"""Regression checks for the remaining visual-asset provenance boundaries."""

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
ROUND4_REPORT = REPO_ROOT / "research" / "visual_recognition_round4_historical_practice_2026-08-24_CN.md"
ROUND4_ASSET = (
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-08-24"
    / "round4_historical_practice"
    / "README.md"
)
ROUND5_REPORT = REPO_ROOT / "research" / "visual_recognition_round5_two_year_daily_2026-08-24_CN.md"
ROUND5_ASSET = (
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-08-24"
    / "round5_two_year_daily"
    / "README.md"
)
TSLA_ASSET = (
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-08-24"
    / "tsla_public_mtf"
    / "README.md"
)
AUDIT = (
    REPO_ROOT
    / "research"
    / "backtesting"
    / "visual_asset_canonical_boundary_audit_2026-08-29_CN.md"
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


class VisualAssetCanonicalBoundaryTests(unittest.TestCase):
    def test_round4_report_keeps_short_window_and_observation_only_boundary(self):
        content = read(ROUND4_REPORT)
        for token in (
            "contract_scope: historical_context_only",
            "data_status: historical",
            "as_of_time: per-case cutoff; dataset end 2026-08-10",
            "timezone: unavailable_in_original_snapshot",
            "session_state: historical_close",
            "timeframes_seen: Daily / 4H / 15m (case-specific)",
            "chart_scope: partial",
            "daily_context_window: <2y",
            "major_high_low_review: partial",
            "ema20_50_200_review: partial",
            "daily_ema20_slope: unknown",
            "daily_ema50_slope: unknown",
            "h_l_ema_slope_gate: pending",
            "parent_state: open_trend / trading_range / range_edge / transition / climax / unclear",
            "direction: long / short / no_valid_direction",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            "lineage_status: same_lineage / reset / unclear / pending",
            "attempt_direction: bullish_attempts / bearish_attempts / unknown",
            "third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear",
            "range_edge_three_push: yes / no / pending",
            "range_edge_side: upper / lower / none / pending",
            "first_independent_obstacle: visual candidate only; not a frozen order field",
            "pre_entry_space_R: unknown unless trigger and structural stop are independently frozen",
            "space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown",
            "research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending",
            "trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending",
            "gate_result: pass / conditional / observation_only / valid_no_trade / pending",
            "handoff_status: not_ready",
            "no-new-positive: maintained",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, content, token)

        self.assertIsNone(re.search(r"(?m)^two_year_daily:", content))
        self.assertIsNone(re.search(r"(?m)^primary_pattern:", content))

    def test_all_remaining_asset_readmes_are_unlabelled_and_canonical(self):
        cases = (
            (
                ROUND4_ASSET,
                (
                    "as_of_time: 2026-08-10 dataset end; 2026-07-29 targeted cutoff case-specific",
                    "daily_context_window: <2y",
                    "major_high_low_review: partial",
                    "ema20_50_200_review: partial",
                    "round4_historical_practice",
                ),
            ),
            (
                ROUND5_ASSET,
                (
                    "as_of_time: per-case cutoff; query timestamp unavailable in original log",
                    "daily_context_window: >=2y",
                    "major_high_low_review: complete in paired historical review; per-case text below",
                    "ema20_50_200_review: complete in paired historical review; Daily EMA only",
                    "visual_recognition_round5_two_year_daily_2026-08-24_CN.md",
                ),
            ),
            (
                TSLA_ASSET,
                (
                    "as_of_time: 2026-08-21 16:00 America/New_York",
                    "timeframes_seen: Daily / 4H-like / 1H / 15m",
                    "daily_context_window: >=2y",
                    "major_high_low_review: complete in paired smoke review; not drawn on the asset",
                    "ema20_50_200_review: complete in paired smoke review; Daily EMA only",
                    "visual_recognition_smoke_test_2026-08-24_CN.md",
                ),
            ),
        )
        common = (
            "contract_scope: historical_context_only",
            "data_status: historical",
            "timezone:",
            "session_state: historical_close",
            "timeframes_seen:",
            "chart_scope:",
            "daily_ema20_slope: unknown",
            "daily_ema50_slope: unknown",
            "h_l_ema_slope_gate: pending",
            "direction: no_valid_direction",
            "lineage_status: pending",
            "internal_label: pending",
            "third_push_state: unclear",
            "research_state: observation_only",
            "trade_state: observation_only",
            "gate_result: observation_only",
            "handoff_status: not_ready",
        )
        for path, tokens in cases:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in common + tokens:
                    self.assertIn(token, content, token)
                self.assertIsNone(re.search(r"(?m)^primary_pattern:", content))

    def test_paired_reports_and_audit_keep_no_new_positive_boundary(self):
        for path, tokens in (
            (
                ROUND5_REPORT,
                (
                    "daily_context_window: >=2y (8/8 cases)",
                    "major_high_low_review: complete (8/8 cases)",
                    "no-new-positive: maintained",
                ),
            ),
            (
                AUDIT,
                (
                    "Round4、Round5 与 TSLA",
                    "round4_historical_practice/README.md",
                    "round5_two_year_daily/README.md",
                    "tsla_public_mtf/README.md",
                    "daily_context_window: <2y",
                    "daily_context_window: >=2y",
                    "major_high_low_review",
                    "ema20_50_200_review",
                    "no-new-positive",
                    "validated win-rate: not-computable",
                    "PA Research only",
                    "no Codex Trading",
                    "no quantitative scanner",
                    "no Execution Agent",
                ),
            ),
        ):
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in tokens:
                    self.assertIn(token, content, token)

    def test_new_audit_is_indexed_everywhere(self):
        for path in INDEXES:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT.name, read(path))


if __name__ == "__main__":
    unittest.main()

"""Regression checks for visual smoke/triage and Round2/Round3 asset boundaries."""

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE = REPO_ROOT / "research" / "visual_recognition_smoke_test_2026-08-24_CN.md"
TRIAGE = REPO_ROOT / "research" / "visual_pattern_triage_protocol_CN.md"
AUDIT = (
    REPO_ROOT
    / "research"
    / "backtesting"
    / "visual_recognition_canonical_boundary_audit_2026-08-29_CN.md"
)
ASSET_READMES = (
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-08-24"
    / "round2_multisymbol"
    / "README.md",
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-08-24"
    / "round3_hl_drills"
    / "README.md",
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-08-24"
    / "round3_l1_l2_mar"
    / "README.md",
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


class VisualRecognitionCanonicalBoundaryTests(unittest.TestCase):
    def test_smoke_document_preserves_stage_one_boundary_and_maps_legacy_labels(self):
        content = read(SMOKE)
        for token in (
            "contract_scope: stage_1_fast_screen",
            "contract_scope: historical_context_only",
            "visual_pattern_label",
            "attempt_or_count",
            "lineage_status: same_lineage / reset / unclear / pending",
            "third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear",
            "primary_pattern",
            "research_state",
            "trade_state",
            "gate_result",
            "as_of_time: unavailable_in_original_images",
            "daily_context_window: unavailable",
            "major_high_low_review: unavailable",
            "ema20_50_200_review: unavailable",
            "no-new-positive-for-clean-multiday-BOP",
        ):
            self.assertIn(token, content, token)

        self.assertIsNone(re.search(r"(?m)^primary_pattern:", content))
        self.assertNotIn("| `primary_pattern:", content)

    def test_smoke_historical_sections_declare_complete_scope_or_conservative_gap(self):
        content = read(SMOKE)
        for token in (
            "as_of_time: 2026-08-21 16:00 America/New_York",
            "timezone: America/New_York",
            "session_state: historical_close",
            "major_high_low_review: complete",
            "ema20_50_200_review: complete",
            "daily_ema20_slope: unknown",
            "daily_ema50_slope: unknown",
            "h_l_ema_slope_gate: pending",
            "lineage_status: pending",
            "third_push_state: range_repeat_test",
            "direction: no_valid_direction (aggregate; per-case visual direction remains descriptive)",
            "as_of_time: 2026-06-26; latest complete Daily bar in asset request",
            "timeframes_seen: Daily (~2Y left context) / 4H-like / 60m proxy",
            "15m-evidence-missing",
            "a_leg_quality: ordinary",
        ):
            self.assertIn(token, content, token)

    def test_triage_protocol_exposes_canonical_stage_and_order_axes(self):
        content = read(TRIAGE)
        for token in (
            "contract_scope: stage_1_fast_screen / historical_context_only",
            "data_status: historical / delayed / live_confirmed / incomplete",
            "session_state: premarket / RTH / after_hours / historical_close / unknown",
            "major_high_low_review: complete / partial / unavailable",
            "ema20_50_200_review: complete / partial / unavailable",
            "parent_state: open_trend / trading_range / range_edge / transition / climax / unclear",
            "primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other",
            "internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending",
            "lineage_status: same_lineage / reset / unclear / pending",
            "third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear",
            "range_edge_side: upper / lower / none / pending",
            "research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending",
            "trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending",
            "gap_policy: accept_open / skip / flag_only / not_applicable",
            "rough_space` 和",
            "stage_2_status` 是历史工作别名",
            "strong-looking-A",
            "a_leg_quality: strong / ordinary / unclear / event_driven",
            "它不是扫描器，也不是胜率模型",
        ):
            self.assertIn(token, content, token)

    def test_asset_readmes_declare_pairing_and_unlabeled_state(self):
        for path in ASSET_READMES:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in (
                    "contract_scope: historical_context_only",
                    "data_status: historical",
                    "as_of_time:",
                    "timezone:",
                    "session_state: historical_close",
                    "timeframes_seen:",
                    "chart_scope:",
                    "daily_context_window:",
                    "major_high_low_review:",
                    "ema20_50_200_review:",
                    "daily_ema20_slope: unknown",
                    "daily_ema50_slope: unknown",
                    "h_l_ema_slope_gate: pending",
                    "direction: no_valid_direction",
                    "lineage_status: pending",
                    "internal_label: pending",
                    "research_state: observation_only",
                    "trade_state: observation_only",
                    "gate_result: observation_only",
                    "handoff_status: not_ready",
                    "primary_pattern",
                    "secondary_context",
                ):
                    self.assertIn(token, content, token)
                self.assertNotRegex(content, r"(?m)^primary_pattern:")

    def test_audit_and_indexes_preserve_no_new_positive_boundary(self):
        audit = read(AUDIT)
        for token in (
            "visual_recognition_smoke_test_2026-08-24_CN.md",
            "visual_pattern_triage_protocol_CN.md",
            "round2_multisymbol/README.md",
            "round3_hl_drills/README.md",
            "round3_l1_l2_mar/README.md",
            "major_high_low_review",
            "ema20_50_200_review",
            "primary_pattern",
            "internal_label",
            "third_push_state",
            "BOP",
            "MTR",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

        for path in INDEXES:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT.name, read(path))


if __name__ == "__main__":
    unittest.main()

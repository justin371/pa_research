"""Regression checks for canonical provenance across every visual-asset README."""

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = REPO_ROOT / "research" / "assets" / "visual_recognition"
ASSET_READMES = tuple(sorted(ASSET_ROOT.glob("**/README.md")))
CONTRACT_ASSET_READMES = tuple(
    ASSET_ROOT / relative
    for relative in (
        Path("2026-08-26/hl_contract_batch/README.md"),
        Path("2026-08-26/hl_contract_batch2/README.md"),
        Path("2026-08-27/hl_large_backtest/README.md"),
        Path("2026-08-27/hl_next_backtest/README.md"),
        Path("2026-08-27/hl_next2_backtest/README.md"),
    )
)
SMOKE = REPO_ROOT / "research" / "visual_recognition_smoke_test_2026-08-24_CN.md"
PRE_ENTRY = REPO_ROOT / "research" / "backtesting" / "visual_asset_pre_entry_evidence_audit_2026-08-29_CN.md"
HANDOFF = REPO_ROOT / "docs" / "research_to_system_handoff_CN.md"
AUDIT = REPO_ROOT / "research" / "backtesting" / "visual_asset_provenance_coverage_audit_2026-08-29_CN.md"
INDEXES = (
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "research" / "README.md",
    REPO_ROOT / "strategy" / "README.md",
    REPO_ROOT / "patterns" / "README.md",
    REPO_ROOT / "research" / "backtesting" / "README.md",
)


def read(path):
    return path.read_text(encoding="utf-8")


class VisualAssetProvenanceCoverageTests(unittest.TestCase):
    def test_all_eleven_asset_readmes_expose_canonical_provenance(self):
        self.assertEqual(len(ASSET_READMES), 11)
        common = (
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
        )
        for path in ASSET_READMES:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in common:
                    self.assertIn(token, content, token)
                self.assertIsNone(re.search(r"(?m)^primary_pattern:", content))
                self.assertIsNone(re.search(r"(?m)^timeframe_seen:", content))

    def test_contract_asset_readmes_keep_per_case_fields_out_of_aggregate_header(self):
        for path in CONTRACT_ASSET_READMES:
            content = read(path)
            with self.subTest(path=path.as_posix()):
                for token in (
                    "daily_context_window: >=2y",
                    "major_high_low_review: complete in paired",
                    "ema20_50_200_review: complete in paired",
                    "third_push_state: unclear",
                    "range_edge_three_push: pending",
                    "range_edge_side: pending",
                    "first_independent_obstacle:",
                    "pre_entry_space_R:",
                    "space_status: unknown",
                    "order_branch: observation_only",
                    "label_source: human_chart_review",
                ):
                    self.assertIn(token, content, token)
                self.assertIsNone(re.search(r"(?m)^primary_pattern:", content))

    def test_known_aliases_are_mapped_or_removed_from_active_fields(self):
        pre_entry = read(PRE_ENTRY)
        self.assertIn("Round4 的 canonical `daily_context_window: <2y`", pre_entry)
        self.assertIn("`two_year_daily: pending`", pre_entry)
        self.assertIsNone(re.search(r"(?m)^two_year_daily:", pre_entry))

        smoke = read(SMOKE)
        self.assertIn("daily_context_window_review: saved assets >=2y; public five unavailable", smoke)
        self.assertIsNone(re.search(r"(?m)^two_year_daily_context:", smoke))

        handoff = read(HANDOFF)
        self.assertIn("no-new-positive", handoff)
        self.assertNotIn("no_new_positive", handoff)

    def test_audit_and_indexes_preserve_scope_counts_and_conclusion(self):
        audit = read(AUDIT)
        for token in (
            "11 个视觉资产目录",
            "105 张 PNG",
            "contract_scope: historical_context_only",
            "daily_context_window: <2y",
            "daily_context_window: >=2y",
            "major_high_low_review",
            "ema20_50_200_review",
            "two_year_daily: pending",
            "two_year_daily_context: pass",
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

"""Regression checks for H/L leg-quality, location, and EMA field boundaries."""

import csv
from collections import Counter
from dataclasses import fields
from pathlib import Path
import unittest

from pa_research_backtest.engine import BacktestContract, REQUIRED_CONTRACT_COLUMNS


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "hl_leg_quality_location_axis_consistency_audit_2026-08-29_CN.md"

CONTRACT_FILES = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
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

CORE_CANONICAL_FIELDS = (
    "a_leg_quality",
    "b_leg_class",
    "b_leg_location",
)
HL_CANONICAL_FIELDS = (
    "h_l_pullback_location",
    "h_l_ema_slope_gate",
)


def _rows_and_headers():
    rows = []
    headers = {}
    for filename in CONTRACT_FILES:
        path = BACKTEST_ROOT / filename
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers[filename] = set(reader.fieldnames or ())
            rows.extend((filename, row) for row in reader)
    return headers, rows


class PaResearchHlLegQualityLocationAxisConsistencyTests(unittest.TestCase):
    def test_current_contract_coverage_and_alias_values_are_explicit(self):
        headers, rows = _rows_and_headers()
        self.assertEqual(len(rows), 60)
        self.assertEqual(sum("a_leg_quality" in header for header in headers.values()), 3)
        self.assertEqual(sum("b_leg_class" in header for header in headers.values()), 3)
        self.assertEqual(sum("b_leg_location" in header for header in headers.values()), 0)
        self.assertTrue(all("h_l_pullback_location" in header for header in headers.values()))
        self.assertTrue(all("h_l_ema_slope_gate" in header for header in headers.values()))

        a_values = Counter(row.get("a_leg_quality", "").strip() for _, row in rows if row.get("a_leg_quality", "").strip())
        b_values = Counter(row.get("b_leg_class", "").strip() for _, row in rows if row.get("b_leg_class", "").strip())
        gate_values = Counter(row["h_l_ema_slope_gate"].strip() for _, row in rows)
        self.assertEqual(a_values, Counter({"strong_A": 9, "ordinary_A": 1}))
        self.assertEqual(b_values, Counter({"controlled_B": 9, "deep_late_controlled_B": 1}))
        self.assertEqual(gate_values, Counter({"long_pass": 27, "short_pass": 28, "fail_flat_or_opposite": 5}))
        self.assertTrue(all(row["h_l_pullback_location"].strip() for _, row in rows))

    def test_engine_minimum_contract_does_not_consume_upstream_ab_fields(self):
        self.assertNotIn("a_leg_quality", REQUIRED_CONTRACT_COLUMNS)
        self.assertNotIn("b_leg_class", REQUIRED_CONTRACT_COLUMNS)
        self.assertNotIn("b_leg_location", REQUIRED_CONTRACT_COLUMNS)
        contract_fields = {field.name for field in fields(BacktestContract)}
        self.assertNotIn("a_leg_quality", contract_fields)
        self.assertNotIn("b_leg_class", contract_fields)
        self.assertNotIn("b_leg_location", contract_fields)
        self.assertIn("h_l_pullback_location", contract_fields)
        self.assertIn("h_l_ema_slope_gate", contract_fields)

    def test_authority_docs_register_canonical_fields_and_historical_aliases(self):
        core_paths = (
            REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md",
            REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md",
            REPO_ROOT / "docs" / "common_context.md",
            REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md",
            REPO_ROOT / "docs" / "visual_pa_review_card_CN.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
        )
        for path in core_paths:
            with self.subTest(path=path.as_posix()):
                content = path.read_text(encoding="utf-8")
                for field in CORE_CANONICAL_FIELDS:
                    self.assertIn(field, content)
                self.assertIn("strong_A", content)
                self.assertIn("ordinary_A", content)
                self.assertIn("controlled_B", content)
                self.assertIn("deep_late_controlled_B", content)
        hl_paths = (
            REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md",
            REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md",
            REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md",
            REPO_ROOT / "docs" / "visual_pa_review_card_CN.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
        )
        for path in hl_paths:
            with self.subTest(path=path.as_posix(), fields="H/L"):
                content = path.read_text(encoding="utf-8")
                for field in HL_CANONICAL_FIELDS:
                    self.assertIn(field, content)
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(encoding="utf-8")
        for alias in ("strong_A", "ordinary_A", "controlled_B", "deep_late_controlled_B"):
            self.assertIn(alias, validator)
        self.assertIn("canonical or registered historical alias required", validator)

    def test_all_pattern_readmes_and_reports_preserve_scope(self):
        for directory in PATTERN_DIRS:
            path = REPO_ROOT / "patterns" / directory / "README.md"
            content = path.read_text(encoding="utf-8")
            with self.subTest(directory=directory):
                self.assertIn("../../docs/pa_research_output_schema_v0_1_CN.md", content)
                self.assertNotIn("strong_A", content)
                self.assertNotIn("controlled_B", content)

        selection = (BACKTEST_ROOT / "hl_next2_selection_2026-08-27_CN.md").read_text(encoding="utf-8")
        self.assertIn("ordinary_A", selection)
        self.assertIn("deep_late_controlled_B", selection)
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for token in (
            "7 个 H/L 冻结合同",
            "10/60",
            "0/60",
            "strong_A=9",
            "controlled_B=9",
            "不能从结果、位置文本或缺失列倒推",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

    def test_audit_is_indexed_and_validator_required(self):
        indexed_paths = (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        )
        for path in indexed_paths:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT_PATH.name, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

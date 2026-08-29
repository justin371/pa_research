"""Regression checks for special_subtype scope and event-axis separation."""

import csv
from collections import Counter
from dataclasses import fields
from pathlib import Path
import unittest

from pa_research_backtest.engine import BacktestContract, REQUIRED_CONTRACT_COLUMNS, _event_bucket


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "special_subtype_event_axis_consistency_audit_2026-08-29_CN.md"

CONTRACT_FILES = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
)

SPECIAL_SUBTYPE_ENUM = (
    "special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none"
)


def _contract_headers() -> list[set[str]]:
    headers: list[set[str]] = []
    for filename in CONTRACT_FILES:
        with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
            headers.append(set(next(csv.reader(handle))))
    return headers


class PaResearchSpecialSubtypeEventAxisConsistencyTests(unittest.TestCase):
    def test_special_subtype_is_upstream_annotation_not_hl_replay_input(self):
        headers = _contract_headers()
        self.assertEqual(len(headers), 7)
        self.assertTrue(all("special_subtype" not in header for header in headers))
        self.assertNotIn("special_subtype", REQUIRED_CONTRACT_COLUMNS)
        self.assertNotIn("special_subtype", {field.name for field in fields(BacktestContract)})

        rules = (REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md").read_text(encoding="utf-8")
        schema = (REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md").read_text(encoding="utf-8")
        visual_card = (REPO_ROOT / "docs" / "visual_pa_review_card_CN.md").read_text(encoding="utf-8")
        daily_card = (REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md").read_text(encoding="utf-8")
        backtesting_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(SPECIAL_SUBTYPE_ENUM, rules)
        self.assertIn(SPECIAL_SUBTYPE_ENUM, schema)
        self.assertIn(SPECIAL_SUBTYPE_ENUM, visual_card)
        self.assertIn(SPECIAL_SUBTYPE_ENUM, daily_card)
        self.assertIn("不属于当前 H/L 最小回放合同", backtesting_readme)

    def test_event_bucket_is_independent_of_missing_special_subtype(self):
        self.assertEqual(
            Counter(
                _event_bucket(value)
                for value in (
                    "ordinary_non_event",
                    "earnings-driven",
                    "earnings_adjacent",
                    "historical_event_filter_not_verified;exploratory_only",
                    "none",
                )
            ),
            Counter(
                {
                    "ordinary_non_event": 1,
                    "event_driven": 1,
                    "earnings_adjacent": 1,
                    "event_unverified_or_pending": 1,
                    "unknown": 1,
                }
            ),
        )

    def test_audit_records_scope_and_does_not_invent_subtype_results(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "0/7",
            "0/60",
            "`ordinary_non_event` | 11",
            "`event_unverified_or_pending` | 40",
            "不能产生 subtype 胜率",
            "不能替代 raw `event_context` 或 canonical `event_bucket`",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(phrase, audit, phrase)

    def test_audit_is_indexed_and_validator_required(self):
        indexed_files = (
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        )
        for path in indexed_files:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT_PATH.name, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

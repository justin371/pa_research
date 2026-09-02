"""Regression checks for H/L report space, version, and conclusion wording."""

import csv
from collections import Counter
from pathlib import Path
import unittest

from pa_research_backtest.engine import ENGINE_VERSION


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_NAME = "hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md"

LEGACY_CONTRACTS = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
)
EXPLICIT_CONTRACTS = (
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
)
HL_REPLAY_REPORTS = (
    "hl_contract_batch_replay_2026-08-26_CN.md",
    "hl_contract_batch2_replay_2026-08-26_CN.md",
    "hl_large_replay_2026-08-27_CN.md",
    "hl_next_replay_2026-08-27_CN.md",
    "hl_next2_replay_2026-08-27_CN.md",
    "hl_next3_replay_2026-08-27_CN.md",
    "hl_next4_replay_2026-08-27_CN.md",
    "hl_next5_replay_2026-08-27_CN.md",
)
HL_SELECTION_REPORTS = (
    "hl_large_selection_2026-08-27_CN.md",
    "hl_next_selection_2026-08-27_CN.md",
    "hl_next2_selection_2026-08-27_CN.md",
    "hl_next3_selection_2026-08-27_CN.md",
    "hl_next4_selection_2026-08-27_CN.md",
    "hl_next5_selection_2026-08-27_CN.md",
)

# These dated replay reports are historical audit artifacts generated under
# engine 0.3.9.  Keep their provenance pinned to the recorded version; current
# runtime/readme version checks belong to current-state tests.
HISTORICAL_REPLAY_ENGINE_VERSION = "0.3.9"


class PaResearchHlReportSpaceVersionConsistencyTests(unittest.TestCase):
    def _rows(self, filename: str) -> list[dict[str, str]]:
        with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_legacy_contract_reports_keep_historical_geometry_separate(self):
        report_names = (
            "hl_contract_batch_replay_2026-08-26_CN.md",
            "hl_contract_batch2_replay_2026-08-26_CN.md",
            "hl_large_selection_2026-08-27_CN.md",
            "hl_large_replay_2026-08-27_CN.md",
            "hl_next_selection_2026-08-27_CN.md",
            "hl_next_replay_2026-08-27_CN.md",
        )
        for filename in LEGACY_CONTRACTS:
            with self.subTest(contract=filename):
                headers = set(self._rows(filename)[0])
                self.assertNotIn("pre_entry_space_R", headers)
                self.assertNotIn("space_status", headers)

        for filename in report_names:
            with self.subTest(report=filename):
                text = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("历史几何", text)
                self.assertIn("unknown_contract_space", text)

        large_selection = (BACKTEST_ROOT / "hl_large_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("属于 `borderline`", large_selection)
        self.assertIn("不是当前 CSV `space_status`", large_selection)

    def test_custom_space_thresholds_are_sensitivity_slices(self):
        expected = {
            "hl_next2_replay_2026-08-27_CN.md": "历史几何空间 `>=1.40R` 敏感性子集",
            "hl_next4_replay_2026-08-27_CN.md": "事前空间 `>=1.50R` 敏感性子集",
            "hl_next5_replay_2026-08-27_CN.md": "事前空间 `>=1.50R` 敏感性子集",
        }
        for filename, phrase in expected.items():
            with self.subTest(report=filename):
                text = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
                self.assertIn(phrase, text)
                self.assertIn("附加敏感性切片", text)
                self.assertNotIn("strict `space_R >= 1.40`", text)
                self.assertNotIn("strict `space_R >= 1.50`", text)

        large_replay = (BACKTEST_ROOT / "hl_large_replay_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("历史几何空间 `>=1R` 且 EMA 通过的敏感性子集", large_replay)
        self.assertNotIn("## 严格空间子集", large_replay)

    def test_hl_replay_reports_preserve_current_version_and_conclusion_boundary(self):
        self.assertEqual(len(HL_REPLAY_REPORTS), 8)
        for filename in HL_REPLAY_REPORTS:
            with self.subTest(report=filename):
                text = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
                self.assertIn(f"当前 PA Research engine 为 `{HISTORICAL_REPLAY_ENGINE_VERSION}`", text)
                self.assertIn("no-new-positive", text)
                self.assertIn("validated win-rate: not-computable", text)

        # The two 2026-08-26 legacy reports predate the user's explicit 60%
        # target.  Later H/L reports must carry the target in their own
        # historical conclusion, while the audit above records the corpus-wide
        # interpretation.
        for filename in HL_REPLAY_REPORTS[2:]:
            with self.subTest(target_report=filename):
                text = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("60%", text)

        for filename in HL_SELECTION_REPORTS:
            with self.subTest(selection=filename):
                text = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("frozen_pre_outcome", text)

    def test_contract_space_partition_and_audit_indexes_are_stable(self):
        legacy_rows = [row for filename in LEGACY_CONTRACTS for row in self._rows(filename)]
        explicit_rows = [row for filename in EXPLICIT_CONTRACTS for row in self._rows(filename)]
        self.assertEqual(len(legacy_rows), 50)
        self.assertEqual(len(explicit_rows), 10)
        self.assertEqual(
            Counter(row.get("space_status", "") for row in legacy_rows),
            Counter({"": 50}),
        )
        self.assertEqual(
            Counter(row.get("space_status", "") for row in explicit_rows),
            Counter({"strict_ge_1R": 9, "borderline_ge_1R": 1}),
        )

        audit = (BACKTEST_ROOT / AUDIT_NAME).read_text(encoding="utf-8")
        for phrase in (
            "ENGINE_VERSION = 0.3.9",
            "9 条 `strict_ge_1R`、1 条 `borderline_ge_1R`",
            "50 unknown",
            "1.40R",
            "1.50R",
            "no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(phrase, audit, phrase)

        indexed_paths = (
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        )
        for path in indexed_paths:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT_NAME, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

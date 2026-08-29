"""Regression checks for event, space, and independence-field boundaries."""

import csv
from collections import Counter
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "event_space_lineage_consistency_audit_2026-08-29_CN.md"


class PaResearchEventSpaceLineageConsistencyTests(unittest.TestCase):
    def _contract_rows(self) -> list[dict[str, str]]:
        rows = []
        for path in sorted(BACKTEST_ROOT.glob("*contracts*.csv")):
            if path.name == "contracts.example.csv":
                continue
            with path.open(encoding="utf-8-sig", newline="") as handle:
                rows.extend(csv.DictReader(handle))
        return rows

    def test_hl_next_legacy_geometry_is_not_explicit_space_evidence(self):
        contract_path = BACKTEST_ROOT / "hl_next_contracts_2026-08-27.csv"
        with contract_path.open(encoding="utf-8-sig", newline="") as handle:
            headers = set(next(csv.reader(handle)))
        self.assertNotIn("pre_entry_space_R", headers)
        self.assertNotIn("space_status", headers)

        readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        selection = (BACKTEST_ROOT / "hl_next_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        replay = (BACKTEST_ROOT / "hl_next_replay_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("全部通过事前 `>=1R` 空间字段", readme)
        self.assertIn("unknown_contract_space", readme)
        self.assertIn("未写入显式 CSV 字段", selection)
        self.assertIn("unknown_contract_space", selection)
        self.assertIn("非当前显式 strict-space", replay)
        self.assertIn("unknown_contract_space", replay)

    def test_current_contract_partition_matches_audit(self):
        rows = self._contract_rows()
        self.assertEqual(len(rows), 60)
        self.assertEqual(
            Counter(bool(row.get("pre_entry_space_R", "").strip()) for row in rows),
            Counter({False: 50, True: 10}),
        )
        self.assertEqual(
            Counter(row.get("space_status", "") for row in rows),
            Counter({"": 50, "strict_ge_1R": 9, "borderline_ge_1R": 1}),
        )
        self.assertEqual(sum(bool(row.get("market_context_id", "").strip()) for row in rows), 0)
        lineage_counts = Counter(row["lineage_id"].strip().casefold() for row in rows)
        self.assertEqual(len(lineage_counts), 53)
        self.assertEqual(sum(count > 1 for count in lineage_counts.values()), 7)
        self.assertEqual(sum(count for count in lineage_counts.values() if count > 1), 14)

        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "7 个 CSV / 60 条",
            "4 个 CSV / 50 条",
            "3 个 CSV / 10 条",
            "9 条 `strict_ge_1R`、1 条 `borderline_ge_1R`",
            "`market_context_id` | 0/60",
            "53 个唯一 lineage、7 个共享组、共享组共 14 条",
            "`event_unverified_or_pending` | 40",
            "`unknown` | 1",
            "validated win-rate",
            "no-new-positive",
        ):
            self.assertIn(phrase, audit, phrase)

    def test_event_bucket_is_derived_and_not_written_into_contracts(self):
        rows = self._contract_rows()
        self.assertTrue(rows)
        self.assertNotIn("event_bucket", rows[0])
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("`event_bucket` 由 engine 根据该字段派生", audit)
        self.assertIn("unknown/pending", audit)
        self.assertIn("不能覆盖合同中的 `event_context`", audit)

    def test_audit_is_indexed_and_scope_is_preserved(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "event_context",
            "event_bucket",
            "space_status",
            "pre_entry_space_R",
            "lineage_id",
            "market_context_id",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(phrase, audit, phrase)

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

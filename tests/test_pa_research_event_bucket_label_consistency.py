"""Regression checks for raw event_context and canonical report labels."""

import csv
from collections import Counter
from pathlib import Path
import unittest

from pa_research_backtest.engine import _event_bucket


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "event_bucket_label_consistency_audit_2026-08-29_CN.md"

CONTRACT_FILES = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
)

EXPECTED_BUCKETS = Counter(
    {
        "ordinary_non_event": 11,
        "event_reviewed_non_event": 3,
        "event_driven": 4,
        "earnings_adjacent": 1,
        "event_unverified_or_pending": 40,
        "unknown": 1,
    }
)


def _read_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for filename in CONTRACT_FILES:
        with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
            rows.extend(csv.DictReader(handle))
    return rows


class PaResearchEventBucketLabelConsistencyTests(unittest.TestCase):
    def test_current_frozen_contracts_match_canonical_event_buckets(self):
        rows = _read_rows()
        self.assertEqual(len(rows), 60)
        self.assertEqual(Counter(_event_bucket(row["event_context"]) for row in rows), EXPECTED_BUCKETS)

        self.assertEqual(_event_bucket("earnings-driven"), "event_driven")
        self.assertEqual(_event_bucket("earnings_adjacent"), "earnings_adjacent")
        self.assertEqual(_event_bucket("ordinary_non_event"), "ordinary_non_event")
        self.assertEqual(
            _event_bucket("earnings_window_clear_by_company_IR;sector_context_pending;public_price_reaudit"),
            "event_unverified_or_pending",
        )
        self.assertEqual(_event_bucket("none"), "unknown")

    def test_next5_preserves_raw_labels_but_uses_canonical_replay_groups(self):
        selection = (BACKTEST_ROOT / "hl_next5_selection_2026-08-27_CN.md").read_text(encoding="utf-8")
        replay = (BACKTEST_ROOT / "hl_next5_replay_2026-08-27_CN.md").read_text(encoding="utf-8")

        self.assertIn("canonical `event_bucket`", selection)
        self.assertIn("`earnings-driven` -> `event_driven`", selection)
        self.assertIn("`earnings_adjacent` -> `earnings_adjacent`", selection)
        self.assertIn("`ordinary_non_event` -> `ordinary_non_event`", selection)
        self.assertIn("| event_driven", replay)
        self.assertIn("| earnings_adjacent", replay)
        self.assertIn("| ordinary_non_event", replay)
        self.assertNotIn("| earnings-driven |", replay)
        self.assertNotIn("| earnings-adjacent |", replay)
        self.assertNotIn("| ordinary |", replay)

    def test_pending_and_unknown_rows_are_not_reported_as_ordinary(self):
        rows = _read_rows()
        pending_rows = [
            row
            for row in rows
            if any(token in row["event_context"].lower() for token in ("pending", "not_verified", "public_price_reaudit"))
        ]
        self.assertEqual(len(pending_rows), 40)
        self.assertTrue(all(_event_bucket(row["event_context"]) == "event_unverified_or_pending" for row in pending_rows))
        self.assertEqual(sum(_event_bucket(row["event_context"]) == "ordinary_non_event" for row in rows), 11)

        audit = AUDIT_PATH.read_text(encoding="utf-8")
        self.assertIn("不能升级为 `ordinary_non_event`", audit)
        self.assertIn("`event_unverified_or_pending=40`", audit)
        self.assertIn("`unknown=1`", audit)

    def test_audit_is_indexed_and_required(self):
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

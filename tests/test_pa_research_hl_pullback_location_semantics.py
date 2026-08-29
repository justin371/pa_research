"""Regression checks for H/L pullback-location text and direction boundaries."""

import csv
from collections import Counter
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "hl_pullback_location_semantics_audit_2026-08-29_CN.md"

CONTRACT_FILES = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
)


def _rows_and_headers():
    rows = []
    headers = {}
    for filename in CONTRACT_FILES:
        with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers[filename] = set(reader.fieldnames or ())
            rows.extend((filename, row) for row in reader)
    return rows, headers


class PaResearchHlPullbackLocationSemanticsTests(unittest.TestCase):
    def test_location_direction_and_ema_tokens_are_consistent(self):
        rows, _ = _rows_and_headers()
        self.assertEqual(len(rows), 60)
        locations = [row["h_l_pullback_location"].strip() for _, row in rows]
        self.assertTrue(all(locations))
        self.assertFalse(any(location.lower() in {"unknown", "pending"} for location in locations))

        upward_or_retest = [
            row
            for _, row in rows
            if any(token in row["h_l_pullback_location"] for token in ("rising_EMA20", "above_rising_EMA20", "EMA20_retest"))
        ]
        downward = [
            row
            for _, row in rows
            if any(token in row["h_l_pullback_location"] for token in ("falling_EMA20", "falling_EMA50", "downward_EMA20"))
        ]
        self.assertEqual(len(upward_or_retest), 31)
        self.assertEqual(Counter(row["direction"] for row in upward_or_retest), Counter({"long": 31}))
        self.assertEqual(len(downward), 22)
        self.assertEqual(Counter(row["direction"] for row in downward), Counter({"short": 22}))

        anomalies = [
            row["sample_id"]
            for _, row in rows
            if (row["direction"] == "long" and any(token in row["h_l_pullback_location"] for token in ("falling", "downward")))
            or (row["direction"] == "short" and any(token in row["h_l_pullback_location"] for token in ("rising", "upward")))
        ]
        self.assertEqual(anomalies, [])

        short_support = [
            row
            for _, row in rows
            if row["direction"] == "short" and "support" in row["h_l_pullback_location"]
        ]
        self.assertEqual(len(short_support), 7)
        self.assertEqual(
            sum(
                any(token in row["h_l_pullback_location"] for token in ("role_reversal", "turned_resistance", "broken_support"))
                for row in short_support
            ),
            6,
        )
        self.assertEqual(
            sum("post_event" in row["h_l_pullback_location"] for row in short_support),
            1,
        )

    def test_historical_b_words_in_location_do_not_fill_separate_b_fields(self):
        rows, headers = _rows_and_headers()
        self.assertTrue(all("b_leg_location" not in header for header in headers.values()))
        historical_b_rows = [
            row
            for _, row in rows
            if any(token in row["h_l_pullback_location"] for token in ("controlled_B", "deep_late_controlled_B", "small_controlled_B"))
        ]
        self.assertEqual(len(historical_b_rows), 5)
        self.assertEqual(
            Counter(row.get("b_leg_class", "").strip() for row in historical_b_rows),
            Counter({"": 1, "controlled_B": 3, "deep_late_controlled_B": 1}),
        )

    def test_authority_docs_and_audit_preserve_location_scope(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for token in (
            "7 份 CSV 共 60 行",
            "位置字段 60/60 非空",
            "rising_EMA20",
            "falling_EMA20",
            "role_reversal",
            "controlled_B",
            "不能替代 A/B 字段",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

        docs = (
            REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md",
            REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md",
            REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md",
            REPO_ROOT / "docs" / "visual_pa_review_card_CN.md",
            REPO_ROOT / "docs" / "common_context.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "patterns" / "README.md",
        )
        for path in docs:
            with self.subTest(path=path.as_posix()):
                content = path.read_text(encoding="utf-8")
                self.assertIn("h_l_pullback_location", content)
                self.assertIn("support", content)
        output_schema = (REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md").read_text(encoding="utf-8")
        self.assertIn("不是方向、EMA gate 或空间枚举", output_schema)
        backtesting = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("不能把当前未破支撑当成空头资格", backtesting)

        indexed_paths = (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        )
        for path in indexed_paths:
            with self.subTest(path=path.as_posix(), index=True):
                self.assertIn(AUDIT_PATH.name, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

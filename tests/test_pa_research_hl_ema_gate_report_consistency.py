"""Regression checks for H/L EMA-gate direction, report counts, and denominators."""

import csv
from collections import Counter
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "hl_ema_gate_report_consistency_audit_2026-08-29_CN.md"

CONTRACT_FILES = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
)

EXPECTED_GATE_COUNTS = {
    "hl_contracts_2026-08-26.csv": Counter(
        {"long_pass": 2, "short_pass": 2, "fail_flat_or_opposite": 1}
    ),
    "hl_contracts_batch2_2026-08-26.csv": Counter(
        {"long_pass": 1, "short_pass": 2}
    ),
    "hl_large_contracts_2026-08-27.csv": Counter(
        {"long_pass": 16, "short_pass": 17, "fail_flat_or_opposite": 4}
    ),
    "hl_next_contracts_2026-08-27.csv": Counter(
        {"long_pass": 4, "short_pass": 1}
    ),
    "hl_next2_contracts_2026-08-27.csv": Counter({"long_pass": 2}),
    "hl_next4_contracts_2026-08-27.csv": Counter({"long_pass": 2}),
    "hl_next5_contracts_2026-08-27.csv": Counter({"short_pass": 6}),
}

REPLAY_REPORTS = (
    "hl_contract_batch_replay_2026-08-26_CN.md",
    "hl_contract_batch2_replay_2026-08-26_CN.md",
    "hl_large_replay_2026-08-27_CN.md",
    "hl_next_replay_2026-08-27_CN.md",
    "hl_next2_replay_2026-08-27_CN.md",
    "hl_next3_replay_2026-08-27_CN.md",
    "hl_next4_replay_2026-08-27_CN.md",
    "hl_next5_replay_2026-08-27_CN.md",
)


def _all_rows():
    for filename in CONTRACT_FILES:
        with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
            yield filename, list(csv.DictReader(handle))


class PaResearchHlEmaGateReportConsistencyTests(unittest.TestCase):
    def test_frozen_contract_gate_counts_and_direction_mapping(self):
        rows = list(_all_rows())
        self.assertEqual(sum(len(file_rows) for _, file_rows in rows), 60)

        aggregate = Counter()
        for filename, file_rows in rows:
            gates = Counter(row["h_l_ema_slope_gate"].strip() for row in file_rows)
            self.assertEqual(gates, EXPECTED_GATE_COUNTS[filename])
            aggregate.update(gates)
            for row in file_rows:
                label = row["internal_label"].strip().upper()
                direction = row["direction"].strip().lower()
                gate = row["h_l_ema_slope_gate"].strip().lower()
                ema20 = row["daily_ema20_slope"].strip().lower()
                ema50 = row["daily_ema50_slope"].strip().lower()
                self.assertTrue(row["h_l_pullback_location"].strip())
                if label in {"H1", "H2"}:
                    self.assertEqual(direction, "long")
                    self.assertIn(gate, {"long_pass", "fail_flat_or_opposite"})
                    if gate == "long_pass":
                        self.assertEqual((ema20, ema50), ("up", "up"))
                elif label in {"L1", "L2"}:
                    self.assertEqual(direction, "short")
                    self.assertEqual(gate, "short_pass")
                    self.assertEqual((ema20, ema50), ("down", "down"))
                else:
                    self.fail(f"unexpected H/L label in frozen contract: {filename} / {label}")

        self.assertEqual(
            aggregate,
            Counter({"long_pass": 27, "short_pass": 28, "fail_flat_or_opposite": 5}),
        )
        self.assertFalse(
            any(
                row["h_l_ema_slope_gate"].strip().lower() == "pending"
                or row["daily_ema20_slope"].strip().lower() == "unknown"
                or row["daily_ema50_slope"].strip().lower() == "unknown"
                for _, file_rows in rows
                for row in file_rows
            )
        )

    def test_replay_reports_keep_eligibility_and_denominator_boundaries(self):
        reports = {
            name: (BACKTEST_ROOT / name).read_text(encoding="utf-8")
            for name in REPLAY_REPORTS
        }
        self.assertIn("contract_count=5", reports["hl_contract_batch_replay_2026-08-26_CN.md"])
        self.assertIn("eligible_contract_count=4", reports["hl_contract_batch_replay_2026-08-26_CN.md"])
        self.assertIn("observation_only_count=1", reports["hl_contract_batch_replay_2026-08-26_CN.md"])
        self.assertIn("引擎层（只按 EMA 闸门判断合同是否可回放）", reports["hl_contract_batch2_replay_2026-08-26_CN.md"])
        self.assertIn("16 / 17 / 4", (BACKTEST_ROOT / "hl_large_selection_2026-08-27_CN.md").read_text(encoding="utf-8"))
        self.assertIn("普通组没有成交分母", reports["hl_next_replay_2026-08-27_CN.md"])
        self.assertIn("没有冻结 H2/L2", reports["hl_next2_replay_2026-08-27_CN.md"])
        self.assertIn("no-eligible-contracts", reports["hl_next3_replay_2026-08-27_CN.md"])
        self.assertIn("0 胜 2 负", reports["hl_next4_replay_2026-08-27_CN.md"])
        self.assertIn("3 胜 2 负", reports["hl_next5_replay_2026-08-27_CN.md"])
        for name, content in reports.items():
            with self.subTest(report=name):
                self.assertIn("no-new-positive", content)
                self.assertIn("胜率", content)
        self.assertIn("回放成交分母", reports["hl_next3_replay_2026-08-27_CN.md"])
        for name in (
            "hl_contract_batch2_replay_2026-08-26_CN.md",
            "hl_large_replay_2026-08-27_CN.md",
            "hl_next2_replay_2026-08-27_CN.md",
            "hl_next4_replay_2026-08-27_CN.md",
            "hl_next5_replay_2026-08-27_CN.md",
        ):
            with self.subTest(report=name, token="pending"):
                self.assertIn("pending", reports[name])

    def test_audit_and_indexes_record_the_validator_fix_without_new_evidence(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for token in (
            "7 份 CSV 共 60 行",
            "long_pass",
            "short_pass",
            "fail_flat_or_opposite",
            "h_l_pullback_location",
            "相反的 pass gate",
            "未知 EMA 斜率",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

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

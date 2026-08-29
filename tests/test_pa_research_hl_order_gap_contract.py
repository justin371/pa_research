"""Regression checks for H/L order, gap-policy, and outcome-state boundaries."""

import csv
from collections import Counter
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "hl_order_gap_contract_audit_2026-08-29_CN.md"
CONTRACT_SPECS = (
    ("hl_contracts_2026-08-26.csv", 5),
    ("hl_contracts_batch2_2026-08-26.csv", 3),
    ("hl_large_contracts_2026-08-27.csv", 37),
    ("hl_next_contracts_2026-08-27.csv", 5),
    ("hl_next2_contracts_2026-08-27.csv", 2),
    ("hl_next4_contracts_2026-08-27.csv", 2),
    ("hl_next5_contracts_2026-08-27.csv", 6),
)


def read_contracts(filename):
    with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class PaResearchHlOrderGapContractTests(unittest.TestCase):
    def test_frozen_hl_contracts_have_stable_order_and_gap_partition(self):
        rows = []
        for filename, expected_count in CONTRACT_SPECS:
            current = read_contracts(filename)
            self.assertEqual(len(current), expected_count, filename)
            rows.extend(current)
            self.assertEqual(
                Counter(row["order_branch"] for row in current),
                Counter({"stop_confirmation": expected_count}),
                filename,
            )

        self.assertEqual(len(rows), 60)
        self.assertEqual(
            Counter(row["gap_policy"] for row in rows),
            Counter({"skip": 59, "accept_open": 1}),
        )

        numeric_fields = ("entry_trigger", "structural_stop", "first_obstacle", "target_price")
        for row in rows:
            with self.subTest(sample_id=row["sample_id"]):
                values = {field: float(row[field]) for field in numeric_fields}
                self.assertEqual(float(row["max_hold_bars"]), 10.0)
                self.assertEqual(values["first_obstacle"], values["target_price"])
                if row["direction"] == "long":
                    self.assertLess(values["structural_stop"], values["entry_trigger"])
                    self.assertGreater(values["first_obstacle"], values["entry_trigger"])
                elif row["direction"] == "short":
                    self.assertGreater(values["structural_stop"], values["entry_trigger"])
                    self.assertLess(values["first_obstacle"], values["entry_trigger"])
                else:
                    self.fail(f"unexpected direction: {row['direction']}")

    def test_only_tsm_uses_pre_frozen_accept_open(self):
        rows = [row for filename, _ in CONTRACT_SPECS for row in read_contracts(filename)]
        accepted = [row for row in rows if row["gap_policy"] == "accept_open"]
        self.assertEqual(len(accepted), 1)
        tsm = accepted[0]
        self.assertEqual(tsm["sample_id"], "PA-HL2-TSM-L1-20250325")
        self.assertEqual(tsm["direction"], "short")
        self.assertEqual(tsm["order_branch"], "stop_confirmation")
        self.assertEqual(tsm["entry_trigger"], "179.80")
        self.assertEqual(tsm["structural_stop"], "184.00")
        self.assertEqual(tsm["first_obstacle"], "170.43")

        report = (BACKTEST_ROOT / "hl_contract_batch2_replay_2026-08-26_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("gap_policy=accept_open", report)
        self.assertIn("accepted_open", report)
        self.assertIn("不把旧价 `179.80` 当实际成交价", report)

    def test_authority_templates_and_order_protocol_expose_gap_policy(self):
        template_paths = (
            REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md",
            REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md",
            REPO_ROOT / "docs" / "visual_pa_review_card_CN.md",
            REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md",
            REPO_ROOT / "foundations" / "06_order_risk_contracts" / "README.md",
            REPO_ROOT / "research" / "order_branch_visual_protocol_CN.md",
        )
        for path in template_paths:
            with self.subTest(path=path.as_posix()):
                content = path.read_text(encoding="utf-8")
                self.assertIn("gap_policy:", content)
                self.assertIn("accept_open / skip / flag_only / not_applicable", content)

        selection_rules = (REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md").read_text(
            encoding="utf-8"
        )
        order_protocol = (REPO_ROOT / "research" / "order_branch_visual_protocol_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`gap_policy=skip`", selection_rules)
        self.assertIn("`gap_policy=skip`", order_protocol)
        self.assertIn("`no-fill`", order_protocol)
        self.assertIn("`opening-skip`", order_protocol)
        self.assertIn("`unproven`", order_protocol)

    def test_audit_indexes_and_preserves_non_statistical_scope(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for token in (
            "60/60",
            "59 行",
            "gap_policy=skip",
            "gap_policy=accept_open",
            "no-fill",
            "opening-skip",
            "accepted-open",
            "first_obstacle=target_price",
            "max_hold_bars=10",
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

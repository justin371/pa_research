"""Regression checks for H/L lineage and market-context independence boundaries."""

import csv
from collections import Counter, defaultdict
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "hl_lineage_market_context_independence_audit_2026-08-29_CN.md"
HL_CONTRACT_NAMES = (
    "hl_contracts_2026-08-26.csv",
    "hl_contracts_batch2_2026-08-26.csv",
    "hl_large_contracts_2026-08-27.csv",
    "hl_next_contracts_2026-08-27.csv",
    "hl_next2_contracts_2026-08-27.csv",
    "hl_next4_contracts_2026-08-27.csv",
    "hl_next5_contracts_2026-08-27.csv",
)


class PaResearchHlLineageMarketContextIndependenceTests(unittest.TestCase):
    def _rows_by_file(self) -> dict[str, list[dict[str, str]]]:
        rows_by_file = {}
        for name in HL_CONTRACT_NAMES:
            path = BACKTEST_ROOT / name
            with path.open(encoding="utf-8-sig", newline="") as handle:
                rows_by_file[name] = list(csv.DictReader(handle))
        return rows_by_file

    def test_current_hl_lineage_and_market_context_partition(self):
        rows_by_file = self._rows_by_file()
        expected = {
            "hl_contracts_2026-08-26.csv": (5, 4, 1, 2),
            "hl_contracts_batch2_2026-08-26.csv": (3, 3, 0, 0),
            "hl_large_contracts_2026-08-27.csv": (37, 31, 6, 12),
            "hl_next_contracts_2026-08-27.csv": (5, 5, 0, 0),
            "hl_next2_contracts_2026-08-27.csv": (2, 2, 0, 0),
            "hl_next4_contracts_2026-08-27.csv": (2, 2, 0, 0),
            "hl_next5_contracts_2026-08-27.csv": (6, 6, 0, 0),
        }
        all_rows = []
        for name, rows in rows_by_file.items():
            lineage_counts = Counter(row["lineage_id"].strip().casefold() for row in rows)
            shared = [count for count in lineage_counts.values() if count > 1]
            self.assertEqual(
                (len(rows), len(lineage_counts), len(shared), sum(shared)),
                expected[name],
                name,
            )
            self.assertTrue(all("market_context_id" not in row for row in rows), name)
            all_rows.extend(rows)

        self.assertEqual(len(all_rows), 60)
        all_lineages = Counter(row["lineage_id"].strip().casefold() for row in all_rows)
        self.assertEqual(len(all_lineages), 53)
        self.assertEqual(sum(count > 1 for count in all_lineages.values()), 7)
        self.assertEqual(sum(count for count in all_lineages.values() if count > 1), 14)

        identity_keys = [
            (
                row["symbol"].strip().upper(),
                row["decision_date"].strip(),
                row["direction"].strip(),
                row["primary_pattern"].strip(),
                row["internal_label"].strip(),
            )
            for row in all_rows
        ]
        self.assertEqual(len(identity_keys), len(set(identity_keys)))

    def test_shared_lineage_groups_are_the_expected_dependency_paths(self):
        rows_by_file = self._rows_by_file()
        groups = defaultdict(list)
        for rows in rows_by_file.values():
            for row in rows:
                groups[row["lineage_id"].strip().casefold()].append(
                    (row["symbol"], row["decision_date"], row["internal_label"])
                )
        shared = {
            lineage: sorted(members)
            for lineage, members in groups.items()
            if len(members) > 1
        }
        self.assertEqual(
            shared,
            {
                "cohr-2022-04-bear-leg": [("COHR", "2022-04-08", "L1"), ("COHR", "2022-04-14", "L2")],
                "cohr-2022-06-bear-leg": [("COHR", "2022-06-14", "L1"), ("COHR", "2022-06-22", "L2")],
                "cohr-2024-06-bull-leg": [("COHR", "2024-06-10", "H1"), ("COHR", "2024-06-21", "H2")],
                "mar-2023-01-recovery": [("MAR", "2023-01-11", "H1"), ("MAR", "2023-01-18", "H2")],
                "rblx-2023-08-bear-leg": [("RBLX", "2023-08-11", "L1"), ("RBLX", "2023-08-17", "L2")],
                "rblx-2025-11-bear-leg": [("RBLX", "2025-11-13", "L1"), ("RBLX", "2025-11-20", "L2")],
                "tsla-2025-08-local": [("TSLA", "2025-08-18", "H1"), ("TSLA", "2025-08-21", "H2")],
            },
        )

    def test_reports_do_not_equate_distinct_lineage_with_independence(self):
        batch = (BACKTEST_ROOT / "hl_contract_batch_replay_2026-08-26_CN.md").read_text(encoding="utf-8")
        batch2 = (BACKTEST_ROOT / "hl_contract_batch2_replay_2026-08-26_CN.md").read_text(encoding="utf-8")
        large_selection = (BACKTEST_ROOT / "hl_large_selection_2026-08-27_CN.md").read_text(encoding="utf-8")
        large_replay = (BACKTEST_ROOT / "hl_large_replay_2026-08-27_CN.md").read_text(encoding="utf-8")
        next_replay = (BACKTEST_ROOT / "hl_next_replay_2026-08-27_CN.md").read_text(encoding="utf-8")
        next5_replay = (BACKTEST_ROOT / "hl_next5_replay_2026-08-27_CN.md").read_text(encoding="utf-8")

        self.assertNotIn("使用独立 lineage 标识", batch)
        self.assertIn("使用不同的 lineage 标识", batch)
        self.assertNotIn("## 三个独立 lineage 的冻结合同", batch2)
        self.assertIn("三个记录了不同 lineage 的冻结合同", batch2)
        self.assertIn("| `market_context_id` | 0/37 条 |", large_selection)
        self.assertIn("31 / 6 组（12 条依赖行）", large_selection)
        self.assertIn("`market_context_id=0/37`", large_replay)
        self.assertIn("依赖记录：5 条各有不同的 `lineage_id`", next_replay)
        self.assertIn("6 个 `lineage_id` 在本批内均唯一", next5_replay)
        self.assertIn("没有 `market_context_id`", next5_replay)

    def test_audit_is_indexed_and_preserves_scope(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "53 个规范化 `lineage_id`",
            "7 个共享 lineage 组、共 14 条依赖行",
            "`market_context_id` 列",
            "不能输出经市场状态控制的独立性调整胜率",
            "selection",
            "replay",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(phrase, audit, phrase)

        indexed_files = (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
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

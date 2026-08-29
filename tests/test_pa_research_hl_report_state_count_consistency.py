"""Regression checks for H/L selection/replay report state counts."""

import csv
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "hl_report_state_count_consistency_audit_2026-08-29_CN.md"

CONTRACT_SPECS = (
    ("hl_contracts_2026-08-26.csv", 5),
    ("hl_contracts_batch2_2026-08-26.csv", 3),
    ("hl_large_contracts_2026-08-27.csv", 37),
    ("hl_next_contracts_2026-08-27.csv", 5),
    ("hl_next2_contracts_2026-08-27.csv", 2),
    ("hl_next4_contracts_2026-08-27.csv", 2),
    ("hl_next5_contracts_2026-08-27.csv", 6),
)


def read_csv_rows(filename):
    with (BACKTEST_ROOT / filename).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class PaResearchHlReportStateCountConsistencyTests(unittest.TestCase):
    def test_seven_frozen_csv_counts_match_the_audit_scope(self):
        rows = []
        for filename, expected_count in CONTRACT_SPECS:
            current = read_csv_rows(filename)
            self.assertEqual(len(current), expected_count, filename)
            rows.extend(current)
        self.assertEqual(len(rows), 60)

    def test_replay_reports_preserve_each_batch_state_count(self):
        expected_fragments = {
            "hl_contract_batch_replay_2026-08-26_CN.md": (
                "contract_count=5",
                "eligible_contract_count=4",
                "observation_only_count=1",
                "filled_count=3",
                "completed_trade_count=3",
                "opening-skip / no trade",
                "win_rate_pct=33.33%",
            ),
            "hl_contract_batch2_replay_2026-08-26_CN.md": (
                "contract_count=3",
                "eligible=3",
                "filled=3",
                "completed=3",
                "3/3 wins = 100.00%",
                "KLAC",
                "valid_no_trade",
            ),
            "hl_large_replay_2026-08-27_CN.md": (
                "37 条冻结合同中，33 条",
                "17 条实际成交",
                "15 条因预先指定的 `gap_policy=skip` 开盘跳过",
                "1 条未触发",
                "4 条为 `observation_only`",
                "13 胜 4 负",
            ),
            "hl_next_replay_2026-08-27_CN.md": (
                "本批 5 条人工看图冻结合同",
                "只有 2 条实际成交并完成",
                "3 条普通非事件合同都因 `gap_policy=skip`",
                "完成成交为 1 胜 1 负",
            ),
            "hl_next2_replay_2026-08-27_CN.md": (
                "本批 2 条人工冻结合同",
                "2 胜 0 负",
                "本批分母为 2",
            ),
            "hl_next4_replay_2026-08-27_CN.md": (
                "本批只有 2 条人工冻结合同",
                "0 胜 2 负",
                "replay2",
                "两条都成交",
                "同一 artifact 根目录下另有旧 `replay` 输出；它使用相同输入文件但记录为两条 `unproven`",
            ),
            "hl_next5_replay_2026-08-27_CN.md": (
                "本批回放 6 条人工冻结合同",
                "5 条成交并完成",
                "1 条因开盘跳过旧触发位而未成交",
                "3 胜 2 负",
            ),
        }
        for filename, fragments in expected_fragments.items():
            content = (BACKTEST_ROOT / filename).read_text(encoding="utf-8")
            for fragment in fragments:
                with self.subTest(report=filename, fragment=fragment):
                    self.assertIn(fragment, content)

    def test_next3_is_a_zero_contract_control_batch(self):
        selection = (BACKTEST_ROOT / "hl_next3_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        replay = (BACKTEST_ROOT / "hl_next3_replay_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("人工审阅 18 个候选", replay)
        self.assertIn("没有冻结交易合同", replay)
        self.assertIn("回放成交分母 | 0", replay)
        self.assertIn("no-eligible-contracts", replay)
        self.assertIn("frozen_pre_outcome", selection)
        self.assertNotIn("contract_count=0", replay)

    def test_audit_and_indexes_lock_the_count_and_denominator_boundary(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for fragment in (
            "7 份有冻结合同",
            "**合计（7 个冻结批次）**",
            "**34**",
            "**20**",
            "**1**",
            "**5**",
            "**34**",
            "**23 / 11**",
            "34 filled + 20 opening-skip + 1 no-fill + 5 observation_only = 60",
            "eligible`/EMA gate 是“允许进入该历史回放层”",
            "`filled` 只表示历史路径有成交",
            "next3",
            "18 个候选、0 条冻结合同",
            "next4",
            "旧 `replay` 记录为两条 `unproven`",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(fragment, audit, fragment)

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

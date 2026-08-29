"""Regression checks for historical replay and transaction-log boundaries."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "historical_replay_result_log_provenance_audit_2026-08-29_CN.md"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"


class HistoricalReplayResultLogProvenanceTests(unittest.TestCase):
    def test_audit_records_external_inventory_and_historical_validator_boundary(self):
        text = AUDIT_PATH.read_text(encoding="utf-8")

        for phrase in (
            "13 份 `results.csv`",
            "88 行、63 个不同 `sample_id`",
            "13 个 `sample_id` 组重复",
            "38 行",
            "25 行",
            "historical_incomplete",
            "退出码 `2`",
            "current_valid",
            "no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(phrase, text)

    def test_replay_results_are_distinguished_from_actual_transaction_logs(self):
        text = AUDIT_PATH.read_text(encoding="utf-8")

        self.assertIn("`results.csv` 是模拟结果记录，不是券商订单、成交、持仓或账户交易日志", text)
        self.assertIn("当前 PA Research 没有实际订单、实际成交、持仓、账户 P&L 或 Execution Agent 交易日志", text)
        for directory in ("journal", "trade_log", "transaction", "ledger"):
            self.assertIn(f"`{directory}/`", text)
            self.assertFalse((REPO_ROOT / directory).exists(), directory)

    def test_recursive_transaction_log_inventory_is_empty_and_review_note_is_not_a_log(self):
        excluded_parts = {".git", ".codex", ".venv", "node_modules", "__pycache__"}
        reserved_names = {"journal", "trade_log", "transaction", "ledger"}
        current_log_dirs = [
            path
            for path in REPO_ROOT.rglob("*")
            if path.is_dir()
            and path.name in reserved_names
            and not any(part.lower() in excluded_parts for part in path.relative_to(REPO_ROOT).parts)
        ]
        self.assertEqual(current_log_dirs, [])

        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "当前 checkout 的交易日志 inventory",
            "| `journal/` | 0 |",
            "| `journal/plans/` | 0 |",
            "| `journal/reviews/` | 0 |",
            "| `trade_log/` | 0 |",
            "| `transaction/` | 0 |",
            "| `ledger/` | 0 |",
            "| `strategy/reviews/` | 1 个研究文件 |",
            "目录名 `reviews` 不能把其中的研究观察笔记升级成成交",
        ):
            self.assertIn(phrase, audit)

        review = (
            REPO_ROOT / "strategy" / "reviews" / "2026-06-25-tsla-meta-example.md"
        ).read_text(encoding="utf-8")
        self.assertIn("不是实际成交日志、冻结合同或胜率样本", review)

    def test_current_checkout_does_not_contain_persisted_replay_triples(self):
        artifact_names = {"results.csv", "summary.json", "run_metadata.json"}
        current_artifacts = [
            path
            for path in REPO_ROOT.rglob("*")
            if path.is_file() and path.name in artifact_names and ".git" not in path.parts
        ]
        self.assertEqual(current_artifacts, [])

    def test_validator_rejects_nested_transaction_log_dirs_and_replay_artifacts(self):
        with tempfile.TemporaryDirectory(prefix="pa-log-boundary-validator-") as temp_dir:
            fixture_root = Path(temp_dir) / "repo"
            shutil.copytree(
                REPO_ROOT,
                fixture_root,
                ignore=shutil.ignore_patterns(
                    ".git", ".codex", ".venv", "node_modules", "__pycache__"
                ),
            )
            (fixture_root / "research" / "nested" / "journal").mkdir(parents=True)
            (fixture_root / "research" / "nested" / "results.csv").write_text(
                "sample_id\n", encoding="utf-8"
            )

            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(fixture_root / "scripts" / VALIDATOR_PATH.name),
                    "-RepoRoot",
                    str(fixture_root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reserved actual transaction-log directory is present", result.stdout)
            self.assertIn("persisted replay artifact is not allowed", result.stdout)

    def test_axes_cannot_be_reconstructed_from_outcomes(self):
        text = AUDIT_PATH.read_text(encoding="utf-8")

        for phrase in (
            "不能由盈利方向、结果标签或后验走势改写",
            "不能由回放收益或事后均线位置补齐",
            "不能由 `space_to_first_obstacle_R`、`first_obstacle_hit` 或 `realized_R` 倒推严格空间",
            "不能因为日期不同或结果不同就宣称独立",
            "不能反向修改上述事前标签或创造新合同",
        ):
            self.assertIn(phrase, text)

    def test_audit_is_indexed_and_validator_guarded(self):
        docs_readme = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        research_readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
        backtesting_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        strategy_readme = (REPO_ROOT / "strategy" / "README.md").read_text(encoding="utf-8")
        handoff = (REPO_ROOT / "docs" / "research_to_system_handoff_CN.md").read_text(
            encoding="utf-8"
        )
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(
            encoding="utf-8"
        )
        filename = AUDIT_PATH.name

        for index_text in (docs_readme, research_readme, backtesting_readme, strategy_readme, handoff):
            self.assertIn(filename, index_text)
        self.assertIn(filename, validator)
        self.assertIn("historical replay/result-log provenance audit", validator)
        self.assertIn("reserved actual transaction-log directory is present", validator)
        self.assertIn("persisted replay artifact is not allowed", validator)
        self.assertIn("当前 PA Research checkout 没有 `journal/`、`trade_log/`、`transaction/` 或 `ledger/` 目录", handoff)
        self.assertIn("no-new-positive", handoff)
        self.assertIn("validated win-rate: not-computable", handoff)


if __name__ == "__main__":
    unittest.main()

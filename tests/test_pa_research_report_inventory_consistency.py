import csv
from collections import Counter
import hashlib
from pathlib import Path
import unittest

from pa_research_backtest.engine import ENGINE_VERSION


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"


class PaResearchReportInventoryConsistencyTests(unittest.TestCase):
    def test_current_inventory_and_report_boundaries_are_consistent(self):
        csv_files = sorted(BACKTEST_ROOT.glob("*.csv"))
        contract_files = sorted(
            path
            for path in csv_files
            if "contracts" in path.name and path.name != "contracts.example.csv"
        )
        example_files = [path for path in csv_files if path.name == "contracts.example.csv"]
        intake_files = sorted(path for path in csv_files if "intake" in path.name)
        price_files = sorted(path for path in csv_files if "prices" in path.name)

        frozen_rows = []
        rows_by_file = {}
        for path in contract_files:
            with path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows_by_file[path.name] = rows
            frozen_rows.extend(rows)

        intake_rows = []
        for path in intake_files:
            with path.open(encoding="utf-8", newline="") as handle:
                intake_rows.extend(list(csv.DictReader(handle)))

        self.assertEqual(len(csv_files), 18)
        self.assertEqual(len(contract_files), 7)
        self.assertEqual(len(example_files), 1)
        self.assertEqual(len(intake_files), 2)
        self.assertEqual(len(price_files), 8)
        self.assertEqual(len(frozen_rows), 60)
        self.assertEqual(len(intake_rows), 25)

        directions = Counter(row["direction"] for row in frozen_rows)
        patterns = Counter(row["primary_pattern"] for row in frozen_rows)
        labels = Counter(row["internal_label"] for row in frozen_rows)
        branches = Counter(row["order_branch"] for row in frozen_rows)
        states = Counter(row.get("contract_state", "") for row in frozen_rows)
        spaces = Counter(row.get("space_status", "") for row in frozen_rows)
        ema_gates = Counter(row.get("h_l_ema_slope_gate", "") for row in frozen_rows)
        symbols = {row["symbol"] for row in frozen_rows}
        lineages = Counter(row["lineage_id"] for row in frozen_rows)
        event_contexts = [row["event_context"] for row in frozen_rows]

        self.assertEqual(directions, Counter({"long": 32, "short": 28}))
        self.assertEqual(patterns, Counter({"H1_L1": 46, "H2_L2": 14}))
        self.assertEqual(labels, Counter({"H1": 24, "H2": 8, "L1": 22, "L2": 6}))
        self.assertEqual(branches, Counter({"stop_confirmation": 60}))
        self.assertEqual(states, Counter({"": 50, "frozen_pre_outcome": 10}))
        self.assertEqual(spaces, Counter({"": 50, "strict_ge_1R": 9, "borderline_ge_1R": 1}))
        self.assertEqual(ema_gates, Counter({"long_pass": 27, "short_pass": 28, "fail_flat_or_opposite": 5}))
        self.assertEqual(len(symbols), 16)
        self.assertEqual(len(lineages), 53)
        self.assertEqual(sum(count > 1 for count in lineages.values()), 7)
        self.assertEqual(sum(count for count in lineages.values() if count > 1), 14)
        self.assertEqual(sum("ordinary_non_event" in value for value in event_contexts), 11)
        self.assertEqual(sum(value == "none" for value in event_contexts), 1)
        self.assertEqual(sum("historical_event_filter_not_verified" in value for value in event_contexts), 37)

        abc_rows = next(path for path in intake_files if path.name.startswith("abc_bop_"))
        with abc_rows.open(encoding="utf-8", newline="") as handle:
            abc_intake = list(csv.DictReader(handle))
        self.assertEqual(Counter(row["primary_pattern"] for row in abc_intake), Counter({"ABC_CONT": 6, "BOP": 4}))
        self.assertEqual(Counter(row["contract_frozen"] for row in intake_rows), Counter({"no": 25}))
        self.assertTrue(all("sample_id" not in row for row in intake_rows))

        inventory = (BACKTEST_ROOT / "contract_csv_inventory_audit_2026-08-29_CN.md").read_text(encoding="utf-8")
        coverage = (BACKTEST_ROOT / "contract_coverage_audit_2026-08-28_CN.md").read_text(encoding="utf-8")
        partition = (BACKTEST_ROOT / "frozen_contract_field_partition_audit_2026-08-29_CN.md").read_text(encoding="utf-8")
        event_space = (BACKTEST_ROOT / "event_space_eligibility_audit_2026-08-29_CN.md").read_text(encoding="utf-8")
        lineage = (BACKTEST_ROOT / "replay_lineage_independence_audit_2026-08-29_CN.md").read_text(encoding="utf-8")

        self.assertIn(f"下现有 {len(csv_files)} 个 CSV", inventory)
        self.assertIn(f"| 非示例冻结合同 | {len(contract_files)} | {len(frozen_rows)} |", inventory)
        self.assertIn(f"| 回放示例合同 | {len(example_files)} | 1 |", inventory)
        self.assertIn(f"| ABC/BOP intake | {len(intake_files)} | {len(intake_rows)} |", inventory)
        self.assertIn(f"| 价格快照 | {len(price_files)} | — |", inventory)
        self.assertIn("`long=32`、`short=28`", inventory)
        self.assertIn("`H1_L1=46`、`H2_L2=14`", inventory)
        self.assertIn("`stop_confirmation=60`", inventory)
        self.assertIn("空 50、`frozen_pre_outcome` 10", inventory)
        self.assertIn("`strict_ge_1R=9`、`borderline_ge_1R=1", inventory)

        self.assertIn("| 非示例人工合同 CSV | 7 个 |", coverage)
        self.assertIn("| 合同记录 | 60 条 |", coverage)
        self.assertIn("| 不同股票代码 | 16 个 |", coverage)
        self.assertIn("| 不同 lineage | 53 个 |", coverage)
        self.assertIn("| 共享 lineage 组 | 7 组（每组 2 条，共 14 条） |", coverage)
        self.assertIn("H1+L1 为 46/60", coverage)
        self.assertIn("H2+L2 为 14/60", coverage)
        self.assertIn("| **合计** | **60** | **32/28** | **24/8/22/6** | **46/14** | **55/5** | **9 strict / 1 borderline / 50 unknown** |", partition)
        self.assertIn("| `ordinary_non_event` | 11 |", event_space)
        self.assertIn("| `event_reviewed_non_event` | 3 |", event_space)
        self.assertIn("| `event_driven` | 4 |", event_space)
        self.assertIn("| `earnings_adjacent` | 1 |", event_space)
        self.assertIn("| `event_unverified_or_pending` | 40 |", event_space)
        self.assertIn("| `unknown` | 1 |", event_space)
        self.assertIn("| 冻结 H/L 合同 | 7 个 CSV、60 条 |", lineage)
        self.assertIn("| 共享 lineage | 7 组、14 条 |", lineage)
        self.assertIn("| ABC/BOP intake | 6 条 ABC、4 条 BOP |", lineage)
        self.assertIn("| `market_context_id` | 0/60 条已记录 |", lineage)

        replay_files = sorted(BACKTEST_ROOT.glob("*replay*.md"))
        version_report = (BACKTEST_ROOT / "version_conclusion_consistency_audit_2026-08-29_CN.md").read_text(encoding="utf-8")
        self.assertEqual(len(replay_files), 11)
        self.assertIn("| 回放报告数 | 11 |", version_report)
        self.assertIn("| 明确包含 `no-new-positive` | 11 / 11 |", version_report)
        self.assertIn("| 明确包含 `validated win-rate: not-computable` | 11 / 11 |", version_report)
        self.assertIn(f"| 当前维护版本 `{ENGINE_VERSION}` 有明确语境 | 11 / 11 |", version_report)
        for path in replay_files:
            content = path.read_text(encoding="utf-8")
            self.assertIn("no-new-positive", content, path.name)
            self.assertIn("validated win-rate: not-computable", content, path.name)
            self.assertIn(ENGINE_VERSION, content, path.name)

        artifact_names = {"results.csv", "summary.json", "run_metadata.json"}
        current_artifacts = [
            path
            for path in REPO_ROOT.rglob("*")
            if path.is_file() and path.name in artifact_names and ".git" not in path.parts
        ]
        artifact_report = (BACKTEST_ROOT / "artifact_inventory_audit_2026-08-29_CN.md").read_text(encoding="utf-8")
        self.assertEqual(current_artifacts, [])
        self.assertIn("| 当前 checkout 中的 `results.csv` | 0 |", artifact_report)
        self.assertIn("| 当前 checkout 中的 `summary.json` | 0 |", artifact_report)
        self.assertIn("| 当前 checkout 中的 `run_metadata.json` | 0 |", artifact_report)
        self.assertIn("| 可配对的回放合同/价格输入组 | 7 |", artifact_report)

        readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        scope_report = (BACKTEST_ROOT / "scope_boundary_dependency_audit_2026-08-29_CN.md").read_text(encoding="utf-8")
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(encoding="utf-8")
        consistency_report = (BACKTEST_ROOT / "report_index_inventory_consistency_audit_2026-08-29_CN.md").read_text(encoding="utf-8")
        engine_sha256 = hashlib.sha256((REPO_ROOT / "pa_research_backtest" / "engine.py").read_bytes()).hexdigest()
        self.assertIn(f"当前引擎版本 `{ENGINE_VERSION}`", readme)
        self.assertIn("backtesting==0.6.6", scope_report)
        self.assertIn("matplotlib==3.10.9", scope_report)
        self.assertIn("validator_engine_contract_parity_audit_2026-08-29_CN.md", validator)
        self.assertIn(f"engine.py` SHA-256 为 `{engine_sha256}`", consistency_report)

        for relative_path in (
            "contract_csv_inventory_audit_2026-08-29_CN.md",
            "validator_engine_contract_parity_audit_2026-08-29_CN.md",
            "report_index_inventory_consistency_audit_2026-08-29_CN.md",
        ):
            self.assertIn(relative_path, readme)
            research_readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
            self.assertIn(relative_path, research_readme)


if __name__ == "__main__":
    unittest.main()

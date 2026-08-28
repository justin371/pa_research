import csv
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from pa_research_backtest.engine import (
    ContractValidationError,
    SUPPORTED_DIRECTIONS,
    SUPPORTED_ORDER_BRANCHES,
    SUPPORTED_PATTERNS,
    load_contracts,
    validate_contract,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"


class PaResearchContractConsistencyTests(unittest.TestCase):
    def test_engine_enum_boundary_matches_current_contract(self):
        self.assertEqual(SUPPORTED_DIRECTIONS, {"long", "short"})
        self.assertEqual(
            SUPPORTED_ORDER_BRANCHES,
            {"stop_confirmation", "limit_retest", "market_close"},
        )
        self.assertEqual(
            SUPPORTED_PATTERNS,
            {"ABC_CONT", "BOP", "H1_L1", "H2_L2", "H3_L3", "RFB", "MTR", "other"},
        )

    def test_example_contract_is_a_supported_frozen_replay_contract(self):
        contract = load_contracts(BACKTEST_ROOT / "contracts.example.csv")[0]

        self.assertEqual(contract.direction, "long")
        self.assertEqual(contract.primary_pattern, "ABC_CONT")
        self.assertEqual(contract.internal_label, "H1")
        self.assertEqual(contract.order_branch, "stop_confirmation")
        self.assertEqual(contract.contract_frozen, "yes")

    def test_all_frozen_contract_csvs_pass_loader_and_entry_geometry(self):
        contract_paths = sorted(
            path
            for path in BACKTEST_ROOT.glob("*contracts*.csv")
            if path.name != "contracts.example.csv"
        )
        self.assertTrue(contract_paths)

        for path in contract_paths:
            with self.subTest(path=path.name):
                contracts = load_contracts(path)
                self.assertTrue(contracts)
                for contract in contracts:
                    self.assertEqual(contract.contract_frozen, "yes")
                    self.assertIn(contract.direction, SUPPORTED_DIRECTIONS)
                    self.assertIn(contract.primary_pattern, SUPPORTED_PATTERNS)
                    self.assertIn(contract.order_branch, SUPPORTED_ORDER_BRANCHES)
                    entry_reference = (
                        None
                        if contract.order_branch == "market_close"
                        else contract.entry_trigger
                    )
                    validate_contract(contract, entry_reference=entry_reference)

    def test_intake_csvs_are_not_replay_contract_inputs(self):
        intake_paths = sorted(BACKTEST_ROOT.glob("*intake*.csv"))
        self.assertTrue(intake_paths)

        for path in intake_paths:
            with self.subTest(path=path.name):
                with path.open(encoding="utf-8", newline="") as handle:
                    rows = list(csv.DictReader(handle))
                self.assertTrue(rows)
                self.assertIn("intake_id", rows[0])
                self.assertNotIn("sample_id", rows[0])
                self.assertTrue(all(row["contract_frozen"].strip().lower() == "no" for row in rows))
                with self.assertRaises(ContractValidationError):
                    load_contracts(path)

    def test_docs_validator_rejects_unsupported_order_branch_in_isolated_copy(self):
        target_name = "hl_next4_contracts_2026-08-27.csv"
        validator = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"

        with tempfile.TemporaryDirectory(prefix="pa-validator-fixture-") as temp_dir:
            fixture_root = Path(temp_dir)
            shutil.copytree(
                REPO_ROOT,
                fixture_root,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc"),
            )
            target = fixture_root / "research" / "backtesting" / target_name
            with target.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertTrue(rows)
            rows[0]["order_branch"] = "stop_limit"
            with target.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(ContractValidationError):
                load_contracts(target)

            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(validator),
                    "-RepoRoot",
                    str(fixture_root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid order_branch", result.stdout)

    def test_docs_validator_rejects_engine_invalid_contract_boundaries(self):
        target_name = "hl_next4_contracts_2026-08-27.csv"
        validator = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"

        with tempfile.TemporaryDirectory(prefix="pa-validator-boundaries-") as temp_dir:
            fixture_root = Path(temp_dir)
            shutil.copytree(
                REPO_ROOT,
                fixture_root,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", "*.pyc"),
            )
            source = fixture_root / "research" / "backtesting" / target_name
            contract_dir = source.parent
            with source.open(encoding="utf-8", newline="") as handle:
                base_rows = list(csv.DictReader(handle))
            self.assertTrue(base_rows)

            def write_rows(filename, rows, fieldnames=None):
                names = fieldnames or list(rows[0].keys())
                path = contract_dir / filename
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=names)
                    writer.writeheader()
                    writer.writerows(
                        {name: row.get(name, "") for name in names}
                        for row in rows
                    )
                return path

            def run_validator():
                return subprocess.run(
                    [
                        "powershell.exe",
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-File",
                        str(validator),
                        "-RepoRoot",
                        str(fixture_root),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

            invalid_cases = (
                ("missing required column", lambda row: row.pop("lineage_id"), "missing frozen contract column 'lineage_id'", [field for field in base_rows[0].keys() if field != "lineage_id"]),
                ("non-finite number", lambda row: row.__setitem__("structural_stop", "NaN"), "non-finite structural_stop", None),
                ("direction/label mismatch", lambda row: row.__setitem__("direction", "short"), "H1/H2 direction mismatch", None),
                ("pattern/label mismatch", lambda row: row.__setitem__("primary_pattern", "H2_L2"), "H2_L2 mapping mismatch", None),
                ("invalid internal label", lambda row: row.__setitem__("internal_label", "H9"), "invalid internal_label", None),
                ("invalid gap policy", lambda row: row.__setitem__("gap_policy", "not_applicable"), "non-market-close branch cannot use gap_policy=not_applicable", None),
                ("missing H/L location", lambda row: row.__setitem__("h_l_pullback_location", "NA"), "missing h_l_pullback_location", None),
                ("invalid non-H/L EMA slope", lambda row: (row.__setitem__("internal_label", "none"), row.__setitem__("primary_pattern", "ABC_CONT"), row.__setitem__("daily_ema20_slope", "sideways")), "invalid daily_ema20_slope", None),
                ("incomplete META", lambda row: (row.__setitem__("meta_confluence", "present"), row.__setitem__("meta_zone", ""), row.__setitem__("meta_components", "EMA20")), "meta_confluence=present requires meta_zone", None),
            )
            expected_messages = []
            for name, mutate, expected_message, fieldnames in invalid_cases:
                with self.subTest(name=name):
                    rows = [dict(base_rows[0])]
                    rows[0]["sample_id"] = f"parity-{name}"
                    rows[0]["lineage_id"] = f"parity-{name}"
                    mutate(rows[0])
                    safe_name = name.replace(" ", "_").replace("/", "_")
                    path = write_rows(f"parity_{safe_name}_contracts.csv", rows, fieldnames=fieldnames)
                    with self.assertRaises(ContractValidationError):
                        load_contracts(path)
                    expected_messages.append(expected_message)

            duplicate_rows = [dict(base_rows[0]), dict(base_rows[0])]
            duplicate_rows[0]["sample_id"] = "parity-duplicate"
            duplicate_rows[0]["lineage_id"] = "parity-duplicate"
            duplicate_rows[1]["sample_id"] = "parity-duplicate"
            duplicate_rows[1]["lineage_id"] = "parity-duplicate"
            with self.subTest(name="duplicate contract"):
                duplicate_path = write_rows("parity_duplicate_contracts.csv", duplicate_rows)
                with self.assertRaises(ContractValidationError):
                    load_contracts(duplicate_path)
                expected_messages.append("duplicate frozen sample_id")

            family_rows = [dict(base_rows[0]), dict(base_rows[0])]
            family_rows[0]["sample_id"] = "parity-family-a"
            family_rows[1]["sample_id"] = "parity-family-b"
            family_rows[0]["lineage_id"] = "parity-family"
            family_rows[1]["lineage_id"] = "parity-family"
            family_rows[1]["decision_date"] = f"{family_rows[0]['decision_date']}T00:00:00"
            with self.subTest(name="duplicate contract family with normalized date"):
                family_path = write_rows("parity_family_contracts.csv", family_rows)
                with self.assertRaises(ContractValidationError):
                    load_contracts(family_path)
                expected_messages.append("duplicate frozen contract family")

            geometry_rows = [dict(base_rows[0])]
            geometry_rows[0]["sample_id"] = "parity-geometry"
            geometry_rows[0]["lineage_id"] = "parity-geometry"
            entry_reference = float(geometry_rows[0]["entry_trigger"])
            geometry_rows[0]["target_price"] = str(entry_reference)
            geometry_path = write_rows("parity_geometry_contracts.csv", geometry_rows)
            contract = load_contracts(geometry_path)[0]
            with self.assertRaisesRegex(ContractValidationError, "long target_price"):
                validate_contract(contract, entry_reference=contract.entry_trigger)
            expected_messages.append("long target_price must be above entry reference")

            result = run_validator()
            self.assertNotEqual(result.returncode, 0)
            for expected_message in expected_messages:
                self.assertIn(expected_message, result.stdout)

    def test_daily_candidate_templates_keep_top_level_pattern_boundary(self):
        rules = (REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md").read_text(
            encoding="utf-8"
        )
        review_card = (REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("primary_pattern: ABC_CONT / BOP", rules)
        self.assertIn("primary_pattern: ABC_CONT / BOP", review_card)
        self.assertNotIn("primary_pattern: ABC_CONT / BOP / H1_L1", review_card)

    def test_record_only_states_are_documented_as_not_direct_replay_input(self):
        unified = (REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md").read_text(
            encoding="utf-8"
        )
        replay_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("研究记录超集", unified)
        self.assertIn("no_valid_direction", unified)
        self.assertIn("stop_limit", unified)
        self.assertIn("actual_fill_or_open_skip", unified)
        self.assertIn("不能直接传给当前回放器", unified)
        self.assertIn("当前 engine `0.3.9` 的回放输入边界", replay_readme)
        self.assertIn("`direction` 只接受 `long` 或 `short`", replay_readme)
        self.assertIn("`order_branch` 只接受", replay_readme)
        self.assertIn("不能直接传给当前回放器", replay_readme)
        self.assertIn("fill_status", replay_readme)


if __name__ == "__main__":
    unittest.main()

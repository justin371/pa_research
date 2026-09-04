"""Synthetic public-boundary regressions; not trading-performance evidence."""

from contextlib import redirect_stdout
from io import StringIO
import json
import hashlib
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import pandas as pd

from pa_source_binding import load_source_module
from pa_research_backtest.engine import (
    ContractValidationError,
    build_summary,
    run_contract,
    validate_contract,
)
from pa_research_backtest.artifact_validator import validate_artifact
from test_pa_research_backtest import make_contract, make_prices
from test_pa_research_artifact_validator import create_current_artifact

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "research/backtesting"
ENGINE_PATH = ROOT / "pa_research_backtest" / "engine.py"
engine_module = load_source_module(ENGINE_PATH, "test_source_bound_replay_engine", "engine source")
main = engine_module.main


class ReviewFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prices = make_prices([
            ("2026-01-01", 9, 9.2, 8.8, 9), ("2026-01-02", 9, 9.2, 8.8, 9),
            ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
            ("2026-01-04", 10.2, 12.5, 10.1, 12.2),
            ("2026-01-05", 12.2, 12.4, 12, 12.1),
        ])
        cls.valid_result = run_contract(make_contract(), cls.prices)

    def test_summary_requires_explicit_resolved_states(self):
        self.assertEqual(build_summary([self.valid_result])["completed_trade_count"], 1)
        for mutation in (
            {"path_result": "pending"}, {"path_result": "unresolved-entry-bar-protective-fill"},
            {"path_result": "reprice-required"}, {"ambiguous_intrabar": "unknown"},
            {"ambiguous_intrabar": None}, {"fill_status": None}, {"evidence_status": None},
        ):
            with self.subTest(mutation=mutation):
                row = dict(self.valid_result, **mutation)
                summary = build_summary([row])
                self.assertEqual(summary["completed_trade_count"], 0)
                self.assertTrue(all(g["completed_trade_count"] == 0 for g in summary["groups"]))
        for field in ("ambiguous_intrabar", "fill_status", "evidence_status", "win_rate_eligible"):
            with self.subTest(missing=field):
                row = dict(self.valid_result)
                row.pop(field)
                self.assertEqual(build_summary([row])["completed_trade_count"], 0)

    def test_pending_and_untyped_third_push_contracts_cannot_enter_denominator(self):
        for overrides in (
            {"internal_label": "pending"},
            {
                "primary_pattern": "H3_L3",
                "internal_label": "none",
                "h_l_ema_slope_gate": "not_applicable",
                "daily_ema20_slope": "",
                "daily_ema50_slope": "",
                "h_l_pullback_location": "",
            },
        ):
            with self.subTest(overrides=overrides), self.assertRaises(ContractValidationError):
                validate_contract(make_contract(**overrides))

        imported = dict(
            self.valid_result,
            internal_label="pending",
            contract_eligibility="eligible",
        )
        self.assertEqual(build_summary([imported])["completed_trade_count"], 0)

    def test_cli_rejects_input_output_alias_before_any_write(self):
        for input_name in ("prices", "contracts"):
            for output_name in ("results.csv", "summary.json", "run_metadata.json"):
                with self.subTest(input=input_name, output=output_name), TemporaryDirectory() as temp:
                    directory = Path(temp)
                    paths = {}
                    for name in ("prices", "contracts"):
                        path = directory / (output_name if name == input_name else name + ".csv")
                        shutil.copyfile(EXAMPLES / (name + ".example.csv"), path)
                        paths[name] = path
                    before = {p.name: p.read_bytes() for p in directory.iterdir()}
                    with redirect_stdout(StringIO()), self.assertRaisesRegex(ValueError, "overlap"):
                        main(["--prices", str(paths["prices"]), "--contracts", str(paths["contracts"]),
                              "--output-dir", str(directory)])
                    self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})

    def test_cli_rejects_engine_source_change_during_run(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            prices = root / "prices.csv"
            contracts = root / "contracts.csv"
            fake_engine = root / "engine.py"
            output_dir = root / "artifact"
            shutil.copyfile(EXAMPLES / "prices.example.csv", prices)
            shutil.copyfile(EXAMPLES / "contracts.example.csv", contracts)
            original_source = ENGINE_PATH.read_bytes()
            fake_engine.write_bytes(original_source)
            bound_engine = load_source_module(fake_engine, "test_mutating_replay_engine", "engine source")
            original_run = bound_engine.run_contracts

            def replace_source_after_execution(*args, **kwargs):
                results = original_run(*args, **kwargs)
                fake_engine.write_bytes(original_source + b"\n# replaced during run\n")
                return results

            with patch.object(bound_engine, "run_contracts", side_effect=replace_source_after_execution):
                with redirect_stdout(StringIO()), self.assertRaisesRegex(
                    RuntimeError, "engine source changed during run"
                ):
                    bound_engine.main(
                        [
                            "--prices",
                            str(prices),
                            "--contracts",
                            str(contracts),
                            "--output-dir",
                            str(output_dir),
                        ]
                    )
            self.assertFalse(output_dir.exists())

    def test_cli_rejects_loaded_source_a_after_path_becomes_b(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            fake_engine = root / "engine.py"
            output_dir = root / "artifact"
            source_a = ENGINE_PATH.read_bytes()
            fake_engine.write_bytes(source_a)
            bound_engine = load_source_module(fake_engine, "test_pre_main_replaced_engine", "engine source")
            fake_engine.write_bytes(source_a + b"\n# source B restored before main\n")
            with redirect_stdout(StringIO()), self.assertRaisesRegex(
                RuntimeError, "engine source changed during run"
            ):
                bound_engine.main(
                    [
                        "--prices",
                        str(EXAMPLES / "prices.example.csv"),
                        "--contracts",
                        str(EXAMPLES / "contracts.example.csv"),
                        "--output-dir",
                        str(output_dir),
                    ]
                )
            self.assertFalse(output_dir.exists())

    def test_summary_rejects_invalid_entry_geometry(self):
        for mutation in (
            {"structural_stop": 11}, {"target_price": 9}, {"first_obstacle": 9},
            {"entry_price": None}, {"entry_price": "bad"}, {"entry_price": float("inf")},
            {"planned_entry_trigger": 8},
        ):
            with self.subTest(mutation=mutation):
                summary = build_summary([dict(self.valid_result, **mutation)])
                self.assertEqual(summary["completed_trade_count"], 0)
                self.assertEqual(summary["pre_entry_provenance_incomplete_count"], 1)

    def test_summary_rejects_inconsistent_or_missing_economics(self):
        for mutation in (
            {"realized_R": 5}, {"net_pnl": -2}, {"gross_pnl": 100},
            {"commission_paid": -1}, {"commission_paid": True}, {"exit_price": 11},
            {"risk_per_unit": 2}, {"risk_per_unit": 0}, {"net_pnl": float("inf")},
        ):
            with self.subTest(mutation=mutation):
                summary = build_summary([dict(self.valid_result, **mutation)])
                self.assertEqual(summary["completed_trade_count"], 0)
                self.assertEqual(summary["win_rate_guard_exclusion_count"], 1)
        for field in ("exit_price", "risk_per_unit", "net_pnl", "gross_pnl", "commission_paid"):
            with self.subTest(missing=field):
                row = dict(self.valid_result)
                row.pop(field)
                self.assertEqual(build_summary([row])["completed_trade_count"], 0)

    def test_artifact_rejects_conflicting_results_even_with_rebuilt_hashes(self):
        with TemporaryDirectory() as temp:
            directory = Path(temp) / "artifact"
            create_current_artifact(directory)
            self.assertEqual(validate_artifact(directory)["status"], "current_valid")
            results_path = directory / "results.csv"
            frame = pd.read_csv(results_path)
            frame.loc[0, "realized_R"] = 5.0
            frame.to_csv(results_path, index=False)
            summary = build_summary(pd.read_csv(results_path).to_dict(orient="records"))
            metadata = json.loads((directory / "run_metadata.json").read_text())
            content = results_path.read_bytes()
            metadata["results_file_sha256"] = hashlib.sha256(content).hexdigest()
            metadata["result_set_sha256"] = hashlib.sha256(content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()
            for key in metadata["summary_provenance"]:
                metadata["summary_provenance"][key] = list(frame.columns) if key == "result_columns" else summary[key]
            for key in ("results_file_sha256", "result_set_sha256", "engine_source_sha256"):
                summary[key] = metadata[key]
            summary["run_metadata"] = metadata
            (directory / "run_metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
            (directory / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
            report = validate_artifact(directory)
            self.assertEqual(report["status"], "invalid")
            self.assertTrue(any("eligibility" in issue for issue in report["issues"]))

    def test_forced_limit_entry_stop_is_counted_on_entry_day(self):
        for direction in ("long", "short"):
            with self.subTest(direction=direction):
                rows = [
                    ("2026-01-01", 10.5, 10.8, 10.2, 10.5),
                    ("2026-01-02", 10.5, 10.8, 10.2, 10.5),
                    ("2026-01-03", 10.2, 10.3, 8.8, 9.2),
                    ("2026-01-04", 9.2, 9.3, 8.7, 8.9),
                ]
                overrides = {"order_branch": "limit_retest"}
                if direction == "short":
                    rows = [(d, 20-o, 20-low, 20-h, 20-c) for d,o,h,low,c in rows]
                    overrides.update(direction="short", internal_label="L1", structural_stop=11,
                        first_obstacle=8, target_price=8, daily_ema20_slope="down",
                        daily_ema50_slope="down", h_l_ema_slope_gate="short_pass",
                        h_l_pullback_location="falling_ema20")
                result = run_contract(make_contract(**overrides), make_prices(rows), commission=0.001)
                self.assertEqual(result["trade_result"], "loss")
                self.assertEqual(result["exit_date"], "2026-01-03")
                self.assertEqual(result["bars_held"], 0)
                self.assertEqual(result["first_obstacle_hit"], "no")
                self.assertAlmostEqual(result["realized_R"], -1.021 if direction == "short" else -1.019)
                self.assertEqual(build_summary([result])["completed_trade_count"], 1)

    def test_entry_bar_resolution_matrix_keeps_real_ambiguity(self):
        # Long cases, mirrored around 10 for short. OHLC literals specify
        # independently whether protection MUST follow entry or may predate it.
        cases = [
            ("stop_confirmation", (9.8, 10.5, 8.5, 10.2), "pending", None),
            ("stop_confirmation", (9.8, 10.5, 8.5, 8.8), "loss", -1),
            ("stop_confirmation", (10.2, 10.5, 8.5, 10.1), "loss", -1),
            ("stop_confirmation", (9.8, 12.5, 9.5, 10.2), "win", 2),
            ("limit_retest", (10.2, 12.5, 9.5, 10.5), "pending", None),
            ("limit_retest", (10.2, 12.5, 9.5, 12.1), "win", 2),
            ("limit_retest", (9.8, 12.5, 9.5, 10.5), "win", 2),
            ("limit_retest", (10.2, 12.5, 8.5, 10.5), "pending", None),
        ]
        for direction in ("long", "short"):
            for branch, bar, label, _ in cases:
                with self.subTest(direction=direction, branch=branch, bar=bar):
                    rows = [("2026-01-01", 10, 10.2, 9.8, 10),
                            ("2026-01-02", 10, 10.2, 9.8, 10),
                            ("2026-01-03", *bar), ("2026-01-04", 10, 12.5, 8.5, 10)]
                    overrides = {"order_branch": branch}
                    if direction == "short":
                        rows = [(d, 20-o, 20-low, 20-h, 20-c) for d,o,h,low,c in rows]
                        overrides.update(direction="short", internal_label="L1", structural_stop=11,
                            first_obstacle=8, target_price=8, daily_ema20_slope="down",
                            daily_ema50_slope="down", h_l_ema_slope_gate="short_pass",
                            h_l_pullback_location="falling_ema20")
                    result = run_contract(make_contract(**overrides), make_prices(rows))
                    self.assertEqual(result["trade_result"], label)
                    if label != "pending":
                        self.assertEqual(result["exit_date"], "2026-01-03")
                        self.assertEqual(result["bars_held"], 0)
                        self.assertEqual(build_summary([result])["completed_trade_count"], 1)
                    else:
                        self.assertIsNone(result["realized_R"])
                        self.assertEqual(build_summary([result])["completed_trade_count"], 0)

    def test_cli_rejects_hardlink_alias_and_preserves_source_bytes(self):
        with TemporaryDirectory() as temp:
            directory = Path(temp)
            contracts = directory / "contracts.csv"
            shutil.copyfile(EXAMPLES / "contracts.example.csv", contracts)
            alias = directory / "results.csv"
            os.link(contracts, alias)
            before = contracts.read_bytes()
            with self.assertRaisesRegex(ValueError, "overlap"):
                main(["--prices", str(EXAMPLES / "prices.example.csv"),
                      "--contracts", str(contracts), "--output-dir", str(directory)])
            self.assertEqual(contracts.read_bytes(), before)
            self.assertEqual(alias.read_bytes(), before)

    def test_cli_publish_rejects_destination_created_after_preflight(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            prices = root / "prices.csv"
            contracts = root / "contracts.csv"
            output_dir = root / "artifact"
            shutil.copyfile(EXAMPLES / "prices.example.csv", prices)
            shutil.copyfile(EXAMPLES / "contracts.example.csv", contracts)
            before = {path: path.read_bytes() for path in (prices, contracts)}
            original_check = engine_module._check_output_paths
            calls = 0

            def create_destination_after_check(inputs, outputs):
                nonlocal calls
                original_check(inputs, outputs)
                calls += 1
                if calls == 2:
                    output_dir.mkdir()
                    (output_dir / "foreign.txt").write_text("foreign\n", encoding="utf-8")

            with patch.object(engine_module, "_check_output_paths", create_destination_after_check):
                with redirect_stdout(StringIO()), self.assertRaises(FileExistsError):
                    main(["--prices", str(prices), "--contracts", str(contracts),
                          "--output-dir", str(output_dir)])
            self.assertEqual({path: path.read_bytes() for path in (prices, contracts)}, before)
            self.assertEqual((output_dir / "foreign.txt").read_text(encoding="utf-8"), "foreign\n")
            self.assertEqual([path.name for path in output_dir.iterdir()], ["foreign.txt"])

    def test_cli_serialization_failure_does_not_publish_partial_artifact(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            output_dir = root / "artifact"
            original_dumps = engine_module.json.dumps
            calls = 0

            def fail_second_serialization(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise RuntimeError("synthetic serialization failure")
                return original_dumps(*args, **kwargs)

            with patch.object(engine_module.json, "dumps", fail_second_serialization):
                with redirect_stdout(StringIO()), self.assertRaisesRegex(RuntimeError, "synthetic"):
                    main(["--prices", str(EXAMPLES / "prices.example.csv"),
                          "--contracts", str(EXAMPLES / "contracts.example.csv"),
                          "--output-dir", str(output_dir)])
            self.assertFalse(output_dir.exists())

    def test_entry_day_stop_does_not_claim_uncertain_obstacle_reached(self):
        for direction in ("long", "short"):
            with self.subTest(direction=direction):
                rows = [("2026-01-01", 10.5, 10.8, 10.2, 10.5),
                        ("2026-01-02", 10.5, 10.8, 10.2, 10.5),
                        ("2026-01-03", 10.2, 11.7, 8.5, 11.5),
                        ("2026-01-04", 11.5, 11.8, 8.7, 8.9)]
                overrides = dict(order_branch="limit_retest", first_obstacle=11)
                if direction == "short":
                    rows = [(d, 20-o, 20-low, 20-h, 20-c) for d,o,h,low,c in rows]
                    overrides.update(direction="short", internal_label="L1", structural_stop=11,
                        first_obstacle=9, target_price=8, daily_ema20_slope="down",
                        daily_ema50_slope="down", h_l_ema_slope_gate="short_pass",
                        h_l_pullback_location="falling_ema20")
                result = run_contract(make_contract(**overrides), make_prices(rows))
                self.assertEqual(result["trade_result"], "loss")
                self.assertEqual(result["first_obstacle_hit"], "unknown")
                self.assertEqual(result["path_result"], "invalidated")
                self.assertEqual(result["exit_date"], "2026-01-03")
                self.assertAlmostEqual(result["realized_R"], -1)
                self.assertEqual(build_summary([result])["completed_trade_count"], 1)

    def test_insufficient_cash_is_not_a_market_no_fill(self):
        result = run_contract(make_contract(), self.prices, cash=5)
        self.assertEqual(result["fill_status"], "unproven")
        self.assertEqual(result["path_result"], "configuration-error-insufficient-cash")
        self.assertEqual(result["win_rate_eligible"], "no")
        summary = build_summary([result])
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertEqual(summary["outcome_bucket_counts"].get("configuration_error"), 1)

    def test_cash_admission_at_cost_adjusted_boundary(self):
        for direction in ("long", "short"):
            for branch in ("stop_confirmation", "limit_retest", "market_close"):
                with self.subTest(direction=direction, branch=branch):
                    opening = 100.5 if branch == "limit_retest" else 99.5
                    rows = [("2026-01-01", 100, 101, 99, 100),
                            ("2026-01-02", 100, 101, 99, 100),
                            ("2026-01-03", opening, 105, 95, 102),
                            ("2026-01-04", 102, 125, 101, 122),
                            ("2026-01-05", 122, 124, 120, 122)]
                    overrides = dict(entry_trigger=100, structural_stop=90, first_obstacle=120,
                                     target_price=120, order_branch=branch,
                                     gap_policy="not_applicable" if branch == "market_close" else "accept_open")
                    if direction == "short":
                        rows = [(d, 200-o, 200-low, 200-h, 200-c) for d,o,h,low,c in rows]
                        overrides.update(direction="short", internal_label="L1", structural_stop=110,
                            first_obstacle=80, target_price=80, daily_ema20_slope="down",
                            daily_ema50_slope="down", h_l_ema_slope_gate="short_pass",
                            h_l_pullback_location="falling_ema20")
                    threshold = 103 if direction == "long" else 101
                    contract, prices = make_contract(**overrides), make_prices(rows)
                    rejected = run_contract(contract, prices, cash=threshold - 0.01, spread=.01, commission=.02)
                    self.assertEqual(rejected["path_result"], "configuration-error-insufficient-cash")
                    admitted = run_contract(contract, prices, cash=threshold, spread=.01, commission=.02)
                    self.assertEqual(admitted["fill_status"], "filled")
                    self.assertAlmostEqual(admitted["entry_price"], 101 if direction == "long" else 99)

    def test_no_market_trigger_is_still_no_fill_with_small_cash(self):
        result = run_contract(make_contract(entry_trigger=15, first_obstacle=20, target_price=20),
                              self.prices, cash=5)
        self.assertEqual(result["fill_status"], "no-fill")
        self.assertEqual(result["path_result"], "no-entry-trigger")

    def test_summary_preserves_valid_normalization_and_close_entry(self):
        normalized = dict(self.valid_result, direction=" LONG ")
        self.assertEqual(build_summary([normalized])["completed_trade_count"], 1)
        prices = make_prices([
            ("2026-01-01", 10, 10.2, 9.8, 10), ("2026-01-02", 10, 10.2, 9.8, 10),
            ("2026-01-03", 10, 12.5, 9.5, 12), ("2026-01-04", 12, 12.5, 11, 12),
        ])
        close = run_contract(make_contract(order_branch="market_close", gap_policy="not_applicable",
                                           entry_trigger=100), prices)
        self.assertEqual(close["trade_result"], "win")
        self.assertEqual(build_summary([close])["completed_trade_count"], 1)


if __name__ == "__main__":
    unittest.main()

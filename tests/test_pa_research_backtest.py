import hashlib
import json
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from pa_research_backtest.engine import (
    BacktestContract,
    ContractValidationError,
    build_summary as _build_summary,
    load_contracts,
    load_prices,
    main,
    run_contract,
)


def make_prices(rows):
    frame = pd.DataFrame(rows, columns=["Date", "Open", "High", "Low", "Close"])
    frame["Symbol"] = "PA-EX"
    frame["Volume"] = 1_000_000
    frame["Date"] = pd.to_datetime(frame["Date"])
    return frame.set_index("Date")


def make_contract(**overrides):
    values = {
        "sample_id": "TEST-001",
        "symbol": "PA-EX",
        "decision_date": pd.Timestamp("2026-01-02"),
        "direction": "long",
        "primary_pattern": "ABC_CONT",
        "internal_label": "H1",
        "order_branch": "stop_confirmation",
        "entry_trigger": 10.0,
        "structural_stop": 9.0,
        "first_obstacle": 12.0,
        "target_price": 12.0,
        "max_hold_bars": 5,
        "gap_policy": "accept_open",
        "label_source": "human_chart_review",
        "daily_context_window": ">=2y",
        "major_high_low_review": "complete",
        "ema20_50_200_review": "complete",
        "event_context": "none",
        "contract_frozen": "yes",
        "lineage_id": "TEST-LINEAGE-001",
        "daily_ema20_slope": "up",
        "daily_ema50_slope": "up",
        "h_l_ema_slope_gate": "long_pass",
        "h_l_pullback_location": "rising_ema20;prior_support",
        "meta_confluence": "absent",
        "meta_zone": "",
        "meta_components": "",
    }
    values.update(overrides)
    return BacktestContract(**values)


def _complete_synthetic_result_rows(results):
    """Give summary-only fixtures explicit pre-entry evidence without changing production code."""

    completed = []
    for index, result in enumerate(results, start=1):
        row = dict(result)
        row.setdefault("sample_id", f"SYNTH-{index}")
        row.setdefault("symbol", "PA-EX")
        row.setdefault("decision_date", "2026-01-02")
        row.setdefault("direction", "long")
        row.setdefault("primary_pattern", "ABC_CONT")
        row.setdefault("internal_label", "H1")
        row.setdefault("order_branch", "stop_confirmation")
        if str(row["order_branch"]).lower() == "market_close":
            row.setdefault("planned_entry_trigger", "")
        else:
            row.setdefault("planned_entry_trigger", 10.0)
        row.setdefault("structural_stop", 9.0)
        row.setdefault("first_obstacle", 12.0)
        row.setdefault("target_price", 12.0)
        row.setdefault("max_hold_bars", 5)
        row.setdefault("gap_policy", "accept_open")
        row.setdefault("label_source", "human_chart_review")
        row.setdefault("daily_context_window", ">=2y")
        row.setdefault("major_high_low_review", "complete")
        row.setdefault("ema20_50_200_review", "complete")
        row.setdefault("event_context", "none")
        row.setdefault("contract_frozen", "yes")
        row.setdefault("lineage_id", f"SYNTH-LINEAGE-{index}")
        row.setdefault("path_result", "target-reached")
        label = str(row["internal_label"]).upper()
        if label in {"H1", "H2"}:
            row.setdefault("daily_ema20_slope", "up")
            row.setdefault("daily_ema50_slope", "up")
            row.setdefault("h_l_ema_slope_gate", "long_pass")
            row.setdefault("h_l_pullback_location", "rising_ema20")
            row.setdefault("meta_confluence", "absent")
        elif label in {"L1", "L2"}:
            row.setdefault("direction", "short")
            row.setdefault("daily_ema20_slope", "down")
            row.setdefault("daily_ema50_slope", "down")
            row.setdefault("h_l_ema_slope_gate", "short_pass")
            row.setdefault("h_l_pullback_location", "falling_ema20")
            row.setdefault("meta_confluence", "absent")
        completed.append(row)
    return completed


def build_summary(results):
    """Keep existing summary fixtures explicit; raw provenance tests call _build_summary."""

    return _build_summary(_complete_synthetic_result_rows(results))


class PaResearchBacktestTests(unittest.TestCase):
    def test_long_stop_target_and_realized_r(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.2, 12.5, 10.1, 12.2),
                ("2026-01-05", 12.2, 12.4, 12.0, 12.1),
            ]
        )
        result = run_contract(make_contract(), prices)
        self.assertEqual(result["fill_status"], "filled")
        self.assertEqual(result["entry_price"], 10.0)
        self.assertEqual(result["exit_reason"], "target")
        self.assertEqual(result["trade_result"], "win")
        self.assertAlmostEqual(result["realized_R"], 2.0)

    def test_gap_skip_is_not_a_trade(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 11.0, 12.0, 10.8, 11.5),
                ("2026-01-04", 11.5, 11.8, 8.5, 9.0),
            ]
        )
        result = run_contract(make_contract(gap_policy="skip"), prices)
        self.assertEqual(result["fill_status"], "opening-skip")
        self.assertEqual(result["win_rate_eligible"], "no")

    def test_gap_accept_open_records_actual_fill(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 11.0, 11.5, 10.8, 11.2),
                ("2026-01-04", 11.2, 12.5, 11.0, 12.2),
            ]
        )
        result = run_contract(make_contract(), prices)
        self.assertEqual(result["fill_status"], "filled")
        self.assertEqual(result["gap_adjustment"], "accepted_open")
        self.assertEqual(result["entry_price"], 11.0)

    def test_gap_reprice_is_required_when_old_target_is_invalid(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 11.0, 11.5, 10.8, 11.2),
                ("2026-01-04", 11.2, 11.5, 10.8, 11.0),
            ]
        )
        result = run_contract(
            make_contract(target_price=10.5, first_obstacle=10.5),
            prices,
        )
        self.assertEqual(result["fill_status"], "unproven")
        self.assertEqual(result["exit_reason"], "gap-reprice-required")
        self.assertEqual(result["win_rate_eligible"], "no")

    def test_short_limit_target(self):
        prices = make_prices(
            [
                ("2026-01-01", 11.0, 11.5, 10.5, 11.0),
                ("2026-01-02", 11.0, 11.5, 10.5, 11.0),
                ("2026-01-03", 9.8, 11.0, 9.5, 10.0),
                ("2026-01-04", 10.0, 10.2, 7.5, 8.0),
            ]
        )
        contract = make_contract(
            direction="short",
            primary_pattern="H2_L2",
            internal_label="L2",
            order_branch="limit_retest",
            entry_trigger=10.0,
            structural_stop=11.0,
            first_obstacle=8.0,
            target_price=8.0,
            gap_policy="flag_only",
            daily_ema20_slope="down",
            daily_ema50_slope="down",
            h_l_ema_slope_gate="short_pass",
            h_l_pullback_location="falling_ema20;prior_resistance",
        )
        result = run_contract(contract, prices)
        self.assertEqual(result["fill_status"], "filled")
        self.assertEqual(result["trade_result"], "win")
        self.assertAlmostEqual(result["realized_R"], 2.0)

    def test_target_gap_after_entry_is_a_completed_target(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 13.0, 13.5, 12.5, 13.2),
            ]
        )
        result = run_contract(make_contract(), prices)
        self.assertEqual(result["fill_status"], "filled")
        self.assertEqual(result["exit_reason"], "target")
        self.assertEqual(result["trade_result"], "win")
        self.assertAlmostEqual(result["realized_R"], 3.0)

    def test_stop_gap_after_entry_is_a_completed_stop(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 8.0, 8.5, 7.5, 8.2),
            ]
        )
        result = run_contract(make_contract(), prices)
        self.assertEqual(result["fill_status"], "filled")
        self.assertEqual(result["exit_reason"], "stop")
        self.assertEqual(result["trade_result"], "loss")
        self.assertAlmostEqual(result["realized_R"], -2.0)

    def test_same_bar_stop_target_is_excluded(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.2, 12.5, 8.5, 11.0),
                ("2026-01-05", 11.0, 11.5, 10.5, 11.0),
            ]
        )
        result = run_contract(make_contract(), prices)
        self.assertEqual(result["ambiguous_intrabar"], "yes")
        self.assertEqual(result["trade_result"], "pending")
        self.assertEqual(result["win_rate_eligible"], "no")
        self.assertEqual(result["first_obstacle_hit"], "unknown")

    def test_data_end_before_horizon_is_not_a_completed_trade(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.2, 10.5, 9.8, 10.0),
            ]
        )
        result = run_contract(make_contract(max_hold_bars=10), prices)
        self.assertEqual(result["fill_status"], "filled")
        self.assertEqual(result["path_result"], "incomplete-horizon")
        self.assertEqual(result["trade_result"], "pending")
        self.assertEqual(result["win_rate_eligible"], "no")

    def test_time_exit_respects_max_hold_bars(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.1, 10.3, 10.1, 10.2),
                ("2026-01-05", 10.1, 10.3, 10.1, 10.2),
                ("2026-01-06", 10.1, 10.3, 10.1, 10.2),
                ("2026-01-07", 10.1, 10.3, 10.1, 10.2),
            ]
        )
        result = run_contract(make_contract(max_hold_bars=3), prices)
        self.assertEqual(result["entry_date"], "2026-01-03")
        self.assertEqual(result["exit_date"], "2026-01-07")
        self.assertEqual(result["exit_reason"], "time_exit")
        # The contract holds three completed post-entry bars, then the
        # non-market-close close order fills on the following bar's open.
        self.assertEqual(result["bars_held"], 4)

    def test_market_close_time_exit_uses_actual_trade_entry_bar(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 10.1, 10.3, 10.1, 10.2),
                ("2026-01-04", 10.1, 10.3, 10.1, 10.2),
                ("2026-01-05", 10.1, 10.3, 10.1, 10.2),
            ]
        )
        contract = make_contract(
            primary_pattern="other",
            internal_label="none",
            order_branch="market_close",
            entry_trigger=None,
            structural_stop=8.0,
            first_obstacle=20.0,
            target_price=20.0,
            max_hold_bars=2,
            gap_policy="not_applicable",
            daily_ema20_slope="",
            daily_ema50_slope="",
            h_l_ema_slope_gate="not_applicable",
            h_l_pullback_location="",
        )
        result = run_contract(contract, prices)
        self.assertEqual(result["entry_date"], "2026-01-02")
        self.assertEqual(result["exit_date"], "2026-01-04")
        self.assertEqual(result["exit_reason"], "time_exit")
        self.assertEqual(result["bars_held"], 2)
        self.assertLessEqual(result["bars_held"], result["max_hold_bars"])

    def test_time_exit_ignores_post_exit_bar_obstacle_and_ambiguity(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.0, 10.2, 9.8, 10.0),
                ("2026-01-05", 10.0, 12.5, 8.5, 10.0),
                ("2026-01-06", 10.0, 10.2, 9.8, 10.0),
            ]
        )
        result = run_contract(make_contract(max_hold_bars=1), prices)
        self.assertEqual(result["exit_reason"], "time_exit")
        self.assertEqual(result["ambiguous_intrabar"], "no")
        self.assertEqual(result["first_obstacle_hit"], "no")
        self.assertEqual(result["trade_result"], "scratch")

    def test_time_exit_requested_at_data_end_is_incomplete(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.1, 10.3, 10.1, 10.2),
                ("2026-01-05", 10.1, 10.3, 10.1, 10.2),
                ("2026-01-06", 10.1, 10.3, 10.1, 10.2),
            ]
        )
        result = run_contract(make_contract(max_hold_bars=3), prices)
        self.assertEqual(result["fill_status"], "filled")
        self.assertEqual(result["path_result"], "incomplete-horizon")
        self.assertEqual(result["exit_reason"], "data_end")
        self.assertEqual(result["trade_result"], "pending")
        self.assertEqual(result["win_rate_eligible"], "no")

    def test_missing_visual_context_is_rejected(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
            ]
        )
        with self.assertRaises(ContractValidationError):
            run_contract(make_contract(daily_context_window="<2y"), prices)

    def test_h_l_ema_gate_failure_is_observation_only(self):
        contract = make_contract(
            daily_ema20_slope="flat",
            h_l_ema_slope_gate="fail_flat_or_opposite",
        )
        result = run_contract(contract, make_prices([]))
        self.assertEqual(result["fill_status"], "not-traded")
        self.assertEqual(result["contract_eligibility"], "observation_only")
        self.assertEqual(result["evidence_status"], "observation_only")
        self.assertEqual(result["win_rate_eligible"], "no")

    def test_h_l_ema_pass_must_match_direction_and_slopes(self):
        contract = make_contract(
            daily_ema50_slope="flat",
            h_l_ema_slope_gate="long_pass",
        )
        with self.assertRaises(ContractValidationError):
            run_contract(contract, make_prices([]))

    def test_h3_and_l3_are_separate_directional_labels(self):
        h3 = make_contract(
            primary_pattern="H3_L3",
            internal_label="H3",
            h_l_ema_slope_gate="not_applicable",
        )
        l3 = make_contract(
            sample_id="TEST-L3",
            direction="short",
            primary_pattern="H3_L3",
            internal_label="L3",
            structural_stop=11.0,
            first_obstacle=8.0,
            target_price=8.0,
            gap_policy="flag_only",
            daily_ema20_slope="down",
            daily_ema50_slope="down",
            h_l_ema_slope_gate="not_applicable",
        )
        self.assertEqual(run_contract(h3, make_prices([]))["fill_status"], "unproven")
        self.assertEqual(run_contract(l3, make_prices([]))["fill_status"], "unproven")

    def test_combined_h3_l3_label_is_rejected(self):
        with self.assertRaises(ContractValidationError):
            run_contract(
                make_contract(
                    primary_pattern="H3_L3",
                    internal_label="H3_L3",
                    h_l_ema_slope_gate="not_applicable",
                ),
                make_prices([]),
            )

    def test_cross_pattern_internal_label_mixing_is_rejected(self):
        with self.assertRaises(ContractValidationError):
            run_contract(
                make_contract(primary_pattern="H1_L1", internal_label="H2"),
                make_prices([]),
            )
        with self.assertRaises(ContractValidationError):
            run_contract(
                make_contract(primary_pattern="BOP", internal_label="H1"),
                make_prices([]),
            )

    def test_frozen_contract_requires_lineage_id(self):
        with self.assertRaises(ContractValidationError):
            run_contract(make_contract(lineage_id=""), make_prices([]))

    def test_meta_present_requires_zone_and_two_sources(self):
        contract = make_contract(
            meta_confluence="present",
            meta_zone="10.0",
            meta_components="EMA20",
        )
        with self.assertRaises(ContractValidationError):
            run_contract(contract, make_prices([]))

    def test_result_and_summary_preserve_h_l_context(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.2, 12.5, 10.1, 12.2),
            ]
        )
        result = run_contract(
            make_contract(
                meta_confluence="present",
                meta_zone="9.8-10.0",
                meta_components="EMA20;prior_support",
            ),
            prices,
        )
        self.assertEqual(result["h_l_ema_slope_gate"], "long_pass")
        self.assertEqual(result["meta_confluence"], "present")
        summary = build_summary([result])
        self.assertEqual(summary["groups"][0]["h_l_ema_slope_gate"], "long_pass")
        self.assertEqual(summary["groups"][0]["meta_confluence"], "present")

    def test_result_and_summary_preserve_lineage(self):
        prices = make_prices(
            [
                ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                ("2026-01-04", 10.2, 12.5, 10.1, 12.2),
            ]
        )
        result = run_contract(make_contract(lineage_id="LINEAGE-1"), prices)
        self.assertEqual(result["lineage_id"], "LINEAGE-1")
        summary = build_summary([result])
        self.assertEqual(summary["groups"][0]["lineage_id"], "LINEAGE-1")

    def test_summary_surfaces_shared_lineage_dependence(self):
        results = [
            {
                "primary_pattern": "H1_L1",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "SHARED-1",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "trade_result": "win",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "primary_pattern": "H2_L2",
                "internal_label": "H2",
                "direction": "long",
                "lineage_id": "SHARED-1",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "trade_result": "loss",
                "realized_R": -1.0,
                "ambiguous_intrabar": "no",
            },
        ]
        summary = build_summary(results)
        self.assertEqual(summary["unique_lineage_count"], 1)
        self.assertEqual(summary["shared_lineage_group_count"], 1)
        self.assertEqual(summary["shared_lineage_row_count"], 2)
        self.assertEqual(summary["cross_pattern_lineage_group_count"], 1)
        self.assertEqual(summary["independence_status"], "dependent_lineage_rows_present")
        self.assertIsNone(summary["independence_adjusted_win_rate_pct"])

    def test_summary_excludes_duplicate_sample_rows_from_denominator(self):
        results = [
            {
                "sample_id": "DUPLICATE-1",
                "symbol": "PA-EX",
                "decision_date": "2026-01-02",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "LINEAGE-A",
                "market_context_id": "MARKET-A",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "target-reached",
                "trade_result": "win",
                "win_rate_eligible": "yes",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "sample_id": "DUPLICATE-1",
                "symbol": "PA-EX",
                "decision_date": "2026-01-02",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "LINEAGE-B",
                "market_context_id": "MARKET-B",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "target-reached",
                "trade_result": "win",
                "win_rate_eligible": "yes",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
        ]
        summary = build_summary(results)
        self.assertEqual(summary["duplicate_sample_id_group_count"], 1)
        self.assertEqual(summary["duplicate_sample_id_row_count"], 2)
        self.assertEqual(summary["duplicate_sample_id_extra_row_count"], 1)
        self.assertEqual(summary["duplicate_result_row_count"], 2)
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertEqual(summary["outcome_bucket_counts"]["duplicate_result"], 2)
        self.assertEqual(summary["independence_status"], "duplicate_result_rows_present")
        self.assertIsNone(summary["independence_adjusted_win_rate_pct"])

    def test_summary_excludes_duplicate_contract_families(self):
        results = [
            {
                "sample_id": "FAMILY-A",
                "symbol": "PA-EX",
                "decision_date": "2026-01-02",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "SAME-FAMILY",
                "market_context_id": "MARKET-A",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "target-reached",
                "trade_result": "win",
                "win_rate_eligible": "yes",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "sample_id": "FAMILY-B",
                "symbol": "PA-EX",
                "decision_date": "2026-01-02",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "SAME-FAMILY",
                "market_context_id": "MARKET-B",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "target-reached",
                "trade_result": "win",
                "win_rate_eligible": "yes",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
        ]
        summary = build_summary(results)
        self.assertEqual(summary["duplicate_sample_id_group_count"], 0)
        self.assertEqual(summary["duplicate_contract_family_group_count"], 1)
        self.assertEqual(summary["duplicate_contract_family_row_count"], 2)
        self.assertEqual(summary["duplicate_result_row_count"], 2)
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertEqual(summary["independence_status"], "duplicate_result_rows_present")

    def test_summary_withholds_independence_rate_when_market_context_is_missing(self):
        results = [
            {
                "sample_id": "MARKET-MISSING-A",
                "symbol": "PA-EX",
                "decision_date": "2026-01-02",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "LINEAGE-A",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "target-reached",
                "trade_result": "win",
                "win_rate_eligible": "yes",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "sample_id": "MARKET-MISSING-B",
                "symbol": "PA-EX",
                "decision_date": "2026-01-03",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "LINEAGE-B",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "invalidated",
                "trade_result": "loss",
                "win_rate_eligible": "yes",
                "realized_R": -1.0,
                "ambiguous_intrabar": "no",
            },
        ]
        summary = build_summary(results)
        self.assertEqual(summary["missing_market_context_count"], 2)
        self.assertEqual(summary["independence_status"], "missing_market_context")
        self.assertIsNone(summary["independence_adjusted_win_rate_pct"])
        self.assertEqual(summary["completed_trade_count"], 2)

    def test_summary_surfaces_shared_market_context_and_overlapping_exposure(self):
        results = [
            {
                "sample_id": "OVERLAP-A",
                "symbol": "PA-EX",
                "decision_date": "2026-01-02",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "LINEAGE-A",
                "market_context_id": "MARKET-SHARED",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "target-reached",
                "trade_result": "win",
                "win_rate_eligible": "yes",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
                "entry_date": "2026-01-05",
                "exit_date": "2026-01-08",
            },
            {
                "sample_id": "OVERLAP-B",
                "symbol": "PA-EX",
                "decision_date": "2026-01-03",
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "LINEAGE-B",
                "market_context_id": "MARKET-SHARED",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "invalidated",
                "trade_result": "loss",
                "win_rate_eligible": "yes",
                "realized_R": -1.0,
                "ambiguous_intrabar": "no",
                "entry_date": "2026-01-07",
                "exit_date": "2026-01-10",
            },
        ]
        summary = build_summary(results)
        self.assertEqual(summary["shared_market_context_group_count"], 1)
        self.assertEqual(summary["shared_market_context_row_count"], 2)
        self.assertEqual(summary["exposure_overlap_group_count"], 1)
        self.assertEqual(summary["exposure_overlap_row_count"], 2)
        self.assertEqual(summary["independence_status"], "shared_market_context_rows_present")
        self.assertIsNone(summary["independence_adjusted_win_rate_pct"])

    def test_summary_separates_event_and_explicit_space_evidence(self):
        results = [
            {
                "primary_pattern": "H1_L1",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "ORDINARY-1",
                "order_branch": "stop_confirmation",
                "event_context": "ordinary_non_event",
                "space_status": "strict_ge_1R",
                "pre_entry_space_R": 1.5,
                "fill_status": "filled",
                "trade_result": "win",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "primary_pattern": "H1_L1",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "ORDINARY-2",
                "order_branch": "stop_confirmation",
                "event_context": "ordinary_non_event",
                "fill_status": "filled",
                "trade_result": "loss",
                "realized_R": -1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "primary_pattern": "H1_L1",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "UNVERIFIED-1",
                "order_branch": "stop_confirmation",
                "event_context": "historical_event_filter_not_verified;exploratory_only",
                "fill_status": "filled",
                "trade_result": "win",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
        ]
        summary = build_summary(results)
        self.assertEqual(summary["event_bucket_contract_counts"]["ordinary_non_event"], 2)
        self.assertEqual(summary["event_bucket_contract_counts"]["event_unverified_or_pending"], 1)
        self.assertEqual(summary["contract_space_bucket_counts"]["strict_ge_1R"], 1)
        self.assertEqual(summary["contract_space_bucket_counts"]["unknown_contract_space"], 2)
        self.assertEqual(summary["ordinary_non_event_completed_trade_count"], 2)
        self.assertEqual(summary["ordinary_non_event_win_rate_pct"], 50.0)
        self.assertEqual(summary["ordinary_non_event_strict_space_completed_trade_count"], 1)
        self.assertEqual(summary["ordinary_non_event_strict_space_win_rate_pct"], 100.0)

    def test_summary_recomputes_pre_entry_buckets(self):
        summary = build_summary(
            [
                {
                    "primary_pattern": "H1_L1",
                    "internal_label": "H1",
                    "direction": "long",
                    "lineage_id": "BUCKET-1",
                    "order_branch": "stop_confirmation",
                    "event_context": "ordinary_non_event",
                    "event_bucket": "event_driven",
                    "contract_space_bucket": "strict_ge_1R",
                    "fill_status": "filled",
                    "trade_result": "win",
                    "realized_R": 1.0,
                    "ambiguous_intrabar": "no",
                }
            ]
        )
        self.assertEqual(summary["event_bucket_contract_counts"], {"ordinary_non_event": 1})
        self.assertEqual(summary["contract_space_bucket_counts"], {"unknown_contract_space": 1})
        self.assertEqual(summary["event_bucket_mismatch_count"], 1)
        self.assertEqual(summary["contract_space_bucket_mismatch_count"], 1)

    def test_summary_uses_ema_gate_for_completed_trade_eligibility(self):
        summary = build_summary(
            [
                {
                    "primary_pattern": "H1_L1",
                    "internal_label": "H1",
                    "direction": "long",
                    "lineage_id": "GATE-1",
                    "order_branch": "stop_confirmation",
                    "event_context": "ordinary_non_event",
                    "daily_ema20_slope": "flat",
                    "daily_ema50_slope": "up",
                    "h_l_ema_slope_gate": "fail_flat_or_opposite",
                    "contract_eligibility": "eligible",
                    "fill_status": "filled",
                    "evidence_status": "comparable",
                    "win_rate_eligible": "yes",
                    "trade_result": "win",
                    "path_result": "target-reached",
                    "realized_R": 2.0,
                    "ambiguous_intrabar": "no",
                }
            ]
        )
        self.assertEqual(summary["contract_eligibility_mismatch_count"], 1)
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertIsNone(summary["win_rate_pct"])

    def test_summary_excludes_missing_h_l_ema_gate_from_denominator(self):
        row = _complete_synthetic_result_rows(
            [
                {
                    "primary_pattern": "H1_L1",
                    "internal_label": "H1",
                    "direction": "long",
                    "fill_status": "filled",
                    "evidence_status": "comparable",
                    "win_rate_eligible": "yes",
                    "trade_result": "win",
                    "path_result": "target-reached",
                    "realized_R": 2.0,
                    "ambiguous_intrabar": "no",
                }
            ]
        )[0]
        row.pop("h_l_ema_slope_gate")
        summary = _build_summary([row])
        self.assertEqual(summary["pre_entry_provenance_status_counts"], {"incomplete": 1})
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertEqual(summary["outcome_bucket_counts"]["pre_entry_provenance_incomplete"], 1)

    def test_summary_excludes_missing_event_context_from_denominator(self):
        row = _complete_synthetic_result_rows(
            [
                {
                    "primary_pattern": "H1_L1",
                    "internal_label": "H1",
                    "direction": "long",
                    "fill_status": "filled",
                    "evidence_status": "comparable",
                    "win_rate_eligible": "yes",
                    "trade_result": "win",
                    "path_result": "target-reached",
                    "realized_R": 2.0,
                    "ambiguous_intrabar": "no",
                }
            ]
        )[0]
        row["event_context"] = ""
        summary = _build_summary([row])
        self.assertEqual(summary["pre_entry_provenance_status_counts"], {"incomplete": 1})
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertEqual(summary["outcome_bucket_counts"]["pre_entry_provenance_incomplete"], 1)

    def test_summary_excludes_missing_planned_entry_trigger_from_denominator(self):
        row = _complete_synthetic_result_rows(
            [
                {
                    "primary_pattern": "H1_L1",
                    "internal_label": "H1",
                    "direction": "long",
                    "fill_status": "filled",
                    "evidence_status": "comparable",
                    "win_rate_eligible": "yes",
                    "trade_result": "win",
                    "path_result": "target-reached",
                    "realized_R": 2.0,
                    "ambiguous_intrabar": "no",
                }
            ]
        )[0]
        row.pop("planned_entry_trigger")
        summary = _build_summary([row])
        self.assertEqual(summary["pre_entry_provenance_status_counts"], {"incomplete": 1})
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertEqual(summary["outcome_bucket_counts"]["pre_entry_provenance_incomplete"], 1)

    def test_summary_excludes_missing_path_result_from_denominator(self):
        row = _complete_synthetic_result_rows(
            [
                {
                    "primary_pattern": "ABC_CONT",
                    "internal_label": "H1",
                    "direction": "long",
                    "fill_status": "filled",
                    "evidence_status": "comparable",
                    "win_rate_eligible": "yes",
                    "trade_result": "win",
                    "realized_R": 2.0,
                    "ambiguous_intrabar": "no",
                }
            ]
        )[0]
        row.pop("path_result")

        summary = _build_summary([row])

        self.assertEqual(summary["pre_entry_provenance_status_counts"], {"complete": 1})
        self.assertEqual(summary["completed_trade_count"], 0)
        self.assertIsNone(summary["win_rate_pct"])
        self.assertEqual(summary["outcome_bucket_counts"]["missing_path_result"], 1)

    def test_summary_is_descriptive_only(self):
        results = [
            {"primary_pattern": "ABC_CONT", "internal_label": "H1", "direction": "long", "order_branch": "stop_confirmation", "event_context": "none", "fill_status": "filled", "trade_result": "win", "realized_R": 2.0, "ambiguous_intrabar": "no"},
            {"primary_pattern": "ABC_CONT", "internal_label": "H1", "direction": "long", "order_branch": "stop_confirmation", "event_context": "none", "fill_status": "filled", "trade_result": "loss", "realized_R": -1.0, "ambiguous_intrabar": "no"},
        ]
        summary = build_summary(results)
        self.assertEqual(summary["study_status"], "research_only / descriptive_only / not-validated")
        self.assertEqual(summary["win_rate_pct"], 50.0)

    def test_summary_requires_explicit_eligibility_and_completed_evidence(self):
        results = [
            {
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "BAD-FLAG",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "target-reached",
                "trade_result": "win",
                "win_rate_eligible": "no",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "BAD-PATH",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "incomplete-horizon",
                "trade_result": "pending",
                "win_rate_eligible": "yes",
                "realized_R": 1.0,
                "ambiguous_intrabar": "no",
            },
            {
                "primary_pattern": "ABC_CONT",
                "internal_label": "H1",
                "direction": "long",
                "lineage_id": "VALID-LOSS",
                "order_branch": "stop_confirmation",
                "event_context": "none",
                "fill_status": "filled",
                "evidence_status": "comparable",
                "path_result": "invalidated",
                "trade_result": "loss",
                "win_rate_eligible": "yes",
                "realized_R": -1.0,
                "ambiguous_intrabar": "no",
            },
        ]
        summary = build_summary(results)
        self.assertEqual(summary["win_rate_eligible_count"], 2)
        self.assertEqual(summary["win_rate_eligibility_mismatch_count"], 2)
        self.assertEqual(summary["win_rate_guard_exclusion_count"], 1)
        self.assertEqual(summary["completed_trade_count"], 1)
        self.assertEqual(summary["win_rate_pct"], 0.0)
        self.assertEqual(summary["outcome_bucket_counts"]["completed_win_loss_scratch"], 1)
        self.assertEqual(summary["outcome_bucket_counts"]["incomplete_horizon"], 1)
        self.assertEqual(summary["outcome_bucket_counts"]["eligibility_flag_mismatch"], 1)

    def test_load_prices_normalizes_and_validates(self):
        frame = load_prices(
            pd.io.common.BytesIO(
                b"ticker,date,open,high,low,close\nPA-EX,2026-01-01,9,10,8,9\n"
            )
        )
        self.assertEqual(frame.iloc[0]["Open"], 9)
        self.assertEqual(frame.iloc[0]["Symbol"], "PA-EX")

    def test_cli_metadata_records_engine_and_result_file_provenance(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            prices_path = temp_path / "prices.csv"
            contracts_path = temp_path / "contracts.csv"
            output_path = temp_path / "output"
            make_prices(
                [
                    ("2026-01-01", 9.0, 9.2, 8.8, 9.0),
                    ("2026-01-02", 9.0, 9.2, 8.8, 9.0),
                    ("2026-01-03", 9.5, 10.5, 9.5, 10.2),
                    ("2026-01-04", 10.2, 12.5, 10.1, 12.2),
                ]
            ).reset_index().to_csv(prices_path, index=False)
            pd.DataFrame([make_contract().as_record()]).to_csv(contracts_path, index=False)

            with redirect_stdout(StringIO()):
                self.assertEqual(
                    main(
                        [
                            "--prices",
                            str(prices_path),
                            "--contracts",
                            str(contracts_path),
                            "--output-dir",
                            str(output_path),
                        ]
                    ),
                    0,
                )

            summary = json.loads((output_path / "summary.json").read_text(encoding="utf-8"))
            metadata = json.loads((output_path / "run_metadata.json").read_text(encoding="utf-8"))
            results_path = output_path / "results.csv"
            results = pd.read_csv(results_path)
            expected_results_hash = hashlib.sha256(results_path.read_bytes()).hexdigest()
            self.assertEqual(metadata["engine_version"], summary["engine_version"])
            self.assertEqual(metadata["backtesting_version"], summary["backtesting_version"])
            self.assertEqual(summary["run_metadata"], metadata)
            self.assertEqual(metadata["result_row_count"], 1)
            self.assertEqual(metadata["results_file"], str(results_path.resolve()))
            self.assertEqual(metadata["results_file_sha256"], expected_results_hash)
            self.assertEqual(summary["results_file_sha256"], expected_results_hash)
            self.assertTrue(metadata["result_set_sha256"])
            self.assertIn("pre_entry_provenance_status", results.columns)
            self.assertIn("pre_entry_provenance_missing_fields", results.columns)
            summary_provenance = metadata["summary_provenance"]
            self.assertEqual(summary_provenance["result_columns"], list(results.columns))
            for field in (
                "pre_entry_provenance_complete_count",
                "pre_entry_provenance_incomplete_count",
                "pre_entry_provenance_status_counts",
                "contract_eligibility_mismatch_count",
                "event_bucket_mismatch_count",
                "contract_space_bucket_mismatch_count",
                "win_rate_eligibility_mismatch_count",
                "win_rate_guard_exclusion_count",
                "completed_trade_count",
                "outcome_bucket_counts",
            ):
                self.assertEqual(summary_provenance[field], summary[field])
            roundtrip = _build_summary(results.to_dict(orient="records"))
            for field in (
                "pre_entry_provenance_complete_count",
                "pre_entry_provenance_incomplete_count",
                "pre_entry_provenance_status_counts",
                "contract_eligibility_mismatch_count",
                "event_bucket_mismatch_count",
                "contract_space_bucket_mismatch_count",
                "completed_trade_count",
                "win_rate_pct",
            ):
                self.assertEqual(roundtrip[field], summary[field])

    def test_contract_loader_rejects_case_insensitive_duplicate_sample_id(self):
        csv = StringIO(
            "sample_id,symbol,decision_date,direction,primary_pattern,internal_label,order_branch,"
            "entry_trigger,structural_stop,first_obstacle,target_price,max_hold_bars,gap_policy,"
            "label_source,daily_context_window,major_high_low_review,ema20_50_200_review,event_context,contract_frozen,lineage_id\n"
            "TEST-A,PA-EX,2026-01-02,long,other,none,market_close,,8,12,12,5,"
            "not_applicable,human_chart_review,>=2y,complete,complete,none,yes,FAMILY-1\n"
            "test-a,PA-EX,2026-01-03,long,other,none,market_close,,8,12,12,5,"
            "not_applicable,human_chart_review,>=2y,complete,complete,none,yes,FAMILY-2\n"
        )
        with self.assertRaisesRegex(ContractValidationError, "duplicate sample_id"):
            load_contracts(csv)

    def test_contract_loader_rejects_case_insensitive_duplicate_lineage_family(self):
        csv = StringIO(
            "sample_id,symbol,decision_date,direction,primary_pattern,internal_label,order_branch,"
            "entry_trigger,structural_stop,first_obstacle,target_price,max_hold_bars,gap_policy,"
            "label_source,daily_context_window,major_high_low_review,ema20_50_200_review,event_context,contract_frozen,lineage_id\n"
            "TEST-A,PA-EX,2026-01-02,long,other,none,market_close,,8,12,12,5,"
            "not_applicable,human_chart_review,>=2y,complete,complete,none,yes,FAMILY-1\n"
            "TEST-B,PA-EX,2026-01-02,long,other,none,stop_confirmation,10,8,12,12,5,"
            "accept_open,human_chart_review,>=2y,complete,complete,none,yes,family-1\n"
        )
        with self.assertRaisesRegex(ContractValidationError, "duplicate contract family"):
            load_contracts(csv)

    def test_contract_loader_keeps_canonical_none_label(self):
        csv = StringIO(
            "sample_id,symbol,decision_date,direction,primary_pattern,internal_label,order_branch,"
            "entry_trigger,structural_stop,first_obstacle,target_price,max_hold_bars,gap_policy,"
            "label_source,daily_context_window,major_high_low_review,ema20_50_200_review,event_context,contract_frozen,lineage_id\n"
            "TEST-OTHER,PA-EX,2026-01-02,long,other,none,market_close,,8,12,12,5,"
            "not_applicable,human_chart_review,>=2y,complete,complete,none,yes,OTHER-LINEAGE\n"
        )
        contract = load_contracts(csv)[0]
        self.assertEqual(contract.primary_pattern, "other")
        self.assertEqual(contract.internal_label, "none")

    def test_strict_space_status_requires_numeric_evidence(self):
        with self.assertRaisesRegex(ContractValidationError, "requires pre_entry_space_R"):
            run_contract(
                make_contract(space_status="strict_ge_1R", pre_entry_space_R=None),
                make_prices([]),
            )

    def test_blocked_space_status_requires_numeric_evidence(self):
        with self.assertRaisesRegex(ContractValidationError, "requires pre_entry_space_R"):
            run_contract(
                make_contract(space_status="blocked", pre_entry_space_R=None),
                make_prices([]),
            )

    def test_contract_loader_rejects_duplicate_contract_family(self):
        csv = StringIO(
            "sample_id,symbol,decision_date,direction,primary_pattern,internal_label,order_branch,"
            "entry_trigger,structural_stop,first_obstacle,target_price,max_hold_bars,gap_policy,"
            "label_source,daily_context_window,major_high_low_review,ema20_50_200_review,event_context,contract_frozen,lineage_id\n"
            "TEST-A,PA-EX,2026-01-02,long,other,none,market_close,,8,12,12,5,"
            "not_applicable,human_chart_review,>=2y,complete,complete,none,yes,FAMILY-1\n"
            "TEST-B,PA-EX,2026-01-02,long,other,none,stop_confirmation,10,8,12,12,5,"
            "accept_open,human_chart_review,>=2y,complete,complete,none,yes,FAMILY-1\n"
        )
        with self.assertRaises(ContractValidationError):
            load_contracts(csv)


if __name__ == "__main__":
    unittest.main()

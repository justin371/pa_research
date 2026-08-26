import unittest
from io import StringIO

import pandas as pd

from pa_research_backtest.engine import (
    BacktestContract,
    ContractValidationError,
    build_summary,
    load_prices,
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

    def test_summary_is_descriptive_only(self):
        results = [
            {"primary_pattern": "ABC_CONT", "internal_label": "H1", "direction": "long", "order_branch": "stop_confirmation", "event_context": "none", "fill_status": "filled", "trade_result": "win", "realized_R": 2.0, "ambiguous_intrabar": "no"},
            {"primary_pattern": "ABC_CONT", "internal_label": "H1", "direction": "long", "order_branch": "stop_confirmation", "event_context": "none", "fill_status": "filled", "trade_result": "loss", "realized_R": -1.0, "ambiguous_intrabar": "no"},
        ]
        summary = build_summary(results)
        self.assertEqual(summary["study_status"], "research_only / descriptive_only / not-validated")
        self.assertEqual(summary["win_rate_pct"], 50.0)

    def test_load_prices_normalizes_and_validates(self):
        frame = load_prices(
            pd.io.common.BytesIO(
                b"ticker,date,open,high,low,close\nPA-EX,2026-01-01,9,10,8,9\n"
            )
        )
        self.assertEqual(frame.iloc[0]["Open"], 9)
        self.assertEqual(frame.iloc[0]["Symbol"], "PA-EX")

    def test_contract_loader_keeps_canonical_none_label(self):
        from pa_research_backtest.engine import load_contracts

        csv = StringIO(
            "sample_id,symbol,decision_date,direction,primary_pattern,internal_label,order_branch,"
            "entry_trigger,structural_stop,first_obstacle,target_price,max_hold_bars,gap_policy,"
            "label_source,daily_context_window,major_high_low_review,ema20_50_200_review,event_context,contract_frozen\n"
            "TEST-OTHER,PA-EX,2026-01-02,long,other,none,market_close,,8,12,12,5,"
            "not_applicable,human_chart_review,>=2y,complete,complete,none,yes\n"
        )
        contract = load_contracts(csv)[0]
        self.assertEqual(contract.primary_pattern, "other")
        self.assertEqual(contract.internal_label, "none")


if __name__ == "__main__":
    unittest.main()

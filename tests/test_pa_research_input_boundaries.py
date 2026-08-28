from dataclasses import replace
from io import StringIO
import math
from pathlib import Path
import unittest

from pa_research_backtest.engine import (
    ContractValidationError,
    load_contracts,
    load_prices,
    main,
    run_contract,
    validate_contract,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class PaResearchInputBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.contract = load_contracts(
            REPO_ROOT / "research" / "backtesting" / "contracts.example.csv"
        )[0]

    def test_direct_contract_rejects_nonfinite_required_numbers(self):
        for field in ("structural_stop", "first_obstacle", "target_price", "entry_trigger"):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ContractValidationError, field + " must be finite"):
                    validate_contract(replace(self.contract, **{field: math.nan}))

    def test_direct_contract_rejects_noninteger_max_hold_bars(self):
        with self.assertRaisesRegex(ContractValidationError, "max_hold_bars must be an integer"):
            validate_contract(replace(self.contract, max_hold_bars=5.0))

    def test_direct_contract_rejects_nonfinite_space_evidence(self):
        with self.assertRaisesRegex(ContractValidationError, "pre_entry_space_R must be finite"):
            validate_contract(replace(self.contract, pre_entry_space_R=math.inf))

    def test_run_contract_rejects_nonfinite_or_invalid_cost_parameters(self):
        for kwargs in (
            {"commission": math.nan},
            {"spread": math.inf},
            {"cash": math.nan},
            {"cash": 0.0},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaisesRegex(ValueError, "finite"):
                    run_contract(self.contract, None, **kwargs)

    def test_cli_rejects_nonfinite_cost_parameters_before_loading_files(self):
        with self.assertRaisesRegex(SystemExit, "finite"):
            main(
                [
                    "--prices",
                    "missing-prices.csv",
                    "--contracts",
                    "missing-contracts.csv",
                    "--output-dir",
                    "missing-output",
                    "--commission",
                    "nan",
                ]
            )

    def test_price_loader_rejects_nonfinite_ohlcv(self):
        csv = StringIO(
            "Date,Open,High,Low,Close,Volume,Symbol\n"
            "2026-01-01,inf,inf,1,inf,1,PA-EX\n"
        )
        with self.assertRaisesRegex(ValueError, "non-finite OHLCV"):
            load_prices(csv)

    def test_empty_inputs_raise_project_specific_errors(self):
        with self.assertRaisesRegex(ValueError, "price CSV contains no rows or columns"):
            load_prices(StringIO(""))
        with self.assertRaisesRegex(ContractValidationError, "contract CSV contains no rows or columns"):
            load_contracts(StringIO(""))

    def test_mixed_timezone_price_dates_are_rejected_as_input_error(self):
        csv = StringIO(
            "Date,Open,High,Low,Close,Volume,Symbol\n"
            "2026-01-01T00:00:00Z,1,2,0,1,1,PA-EX\n"
            "2026-01-02T00:00:00+08:00,1,2,0,1,1,PA-EX\n"
        )
        with self.assertRaisesRegex(ValueError, "invalid or mixed-timezone Date"):
            load_prices(csv)


if __name__ == "__main__":
    unittest.main()

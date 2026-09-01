import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_pa_blind_daily_batch.py"
SPEC = importlib.util.spec_from_file_location("render_pa_blind_daily_batch", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class BlindDailyBatchTests(unittest.TestCase):
    def test_deterministic_index_preserves_context_and_hidden_future(self):
        index = MODULE.deterministic_index("TEST", 700, "seed", 600, 40)
        self.assertGreaterEqual(index + 1, 600)
        self.assertGreaterEqual(700 - index - 1, 40)
        self.assertEqual(index, MODULE.deterministic_index("TEST", 700, "seed", 600, 40))

    def test_renderer_creates_outcome_hidden_png_from_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            price_file = root / "prices.csv"
            rows = []
            first = date(2020, 1, 1)
            for index in range(700):
                close = 100.0 + index * 0.05 + (index % 9 - 4) * 0.2
                rows.append(
                    {
                        "Symbol": "TEST",
                        "Date": (first + timedelta(days=index)).isoformat(),
                        "Open": close - 0.15,
                        "High": close + 0.45,
                        "Low": close - 0.5,
                        "Close": close,
                        "Volume": 1_000_000 + index * 100,
                    }
                )
            with price_file.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)

            cutoff_index = MODULE.deterministic_index("TEST", len(rows), "seed", 600, 40)
            manifest = {
                "label_hidden": True,
                "outcome_hidden": True,
                "selection_mode": "deterministic_cutoff",
                "selection_seed": "seed",
                "minimum_context_bars": 600,
                "minimum_hidden_future_bars": 40,
                "daily_chart_bars": 504,
                "local_chart_bars": 120,
                "samples": [
                    {
                        "sample_id": "BQ-TEST",
                        "symbol": "TEST",
                        "price_file": "prices.csv",
                        "cutoff_date": rows[cutoff_index]["Date"],
                        "chart_file": "BQ-TEST.png",
                    }
                ],
            }
            manifest_file = root / "manifest.json"
            manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
            output_dir = root / "charts"

            outputs = MODULE.render_manifest(manifest_file, root, output_dir)

            self.assertEqual(outputs, [output_dir / "BQ-TEST.png"])
            self.assertTrue(outputs[0].is_file())
            self.assertGreater(outputs[0].stat().st_size, 10_000)

    def test_manifest_cutoff_must_match_deterministic_selection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            price_file = root / "prices.csv"
            with price_file.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["Symbol", "Date", "Open", "High", "Low", "Close", "Volume"],
                )
                writer.writeheader()
                first = date(2020, 1, 1)
                for index in range(700):
                    writer.writerow(
                        {
                            "Symbol": "TEST",
                            "Date": (first + timedelta(days=index)).isoformat(),
                            "Open": 100,
                            "High": 101,
                            "Low": 99,
                            "Close": 100.5,
                            "Volume": 1_000_000,
                        }
                    )
            manifest_file = root / "manifest.json"
            manifest_file.write_text(
                json.dumps(
                    {
                        "label_hidden": True,
                        "outcome_hidden": True,
                        "selection_mode": "deterministic_cutoff",
                        "selection_seed": "seed",
                        "minimum_context_bars": 600,
                        "minimum_hidden_future_bars": 40,
                        "samples": [
                            {
                                "sample_id": "BQ-TEST",
                                "symbol": "TEST",
                                "price_file": "prices.csv",
                                "cutoff_date": "2020-01-01",
                                "chart_file": "BQ-TEST.png",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "does not match deterministic selection"):
                MODULE.render_manifest(manifest_file, root, root / "charts")

    def test_explicit_cutoff_mode_preserves_context_and_hidden_future(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            price_file = root / "prices.csv"
            first = date(2020, 1, 1)
            rows = []
            for index in range(700):
                rows.append(
                    {
                        "Symbol": "TEST",
                        "Date": (first + timedelta(days=index)).isoformat(),
                        "Open": 100,
                        "High": 101,
                        "Low": 99,
                        "Close": 100.5,
                        "Volume": 1_000_000,
                    }
                )
            with price_file.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)

            manifest_file = root / "manifest.json"
            manifest_file.write_text(
                json.dumps(
                    {
                        "label_hidden": True,
                        "outcome_hidden": True,
                        "selection_mode": "explicit_cutoff",
                        "minimum_context_bars": 500,
                        "minimum_hidden_future_bars": 40,
                        "daily_chart_bars": 504,
                        "local_chart_bars": 120,
                        "samples": [
                            {
                                "sample_id": "MC-001",
                                "symbol": "TEST",
                                "price_file": "prices.csv",
                                "cutoff_date": rows[549]["Date"],
                                "chart_file": "MC-001.png",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            outputs = MODULE.render_manifest(manifest_file, root, root / "charts")
            self.assertEqual(outputs, [root / "charts" / "MC-001.png"])
            self.assertTrue(outputs[0].is_file())

    def test_manifest_requires_blind_flags(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_file = root / "manifest.json"
            manifest_file.write_text(
                json.dumps(
                    {
                        "selection_seed": "seed",
                        "minimum_context_bars": 600,
                        "minimum_hidden_future_bars": 40,
                        "samples": [],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "label_hidden and outcome_hidden"):
                MODULE.render_manifest(manifest_file, root, root / "charts")


if __name__ == "__main__":
    unittest.main()

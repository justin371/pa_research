import contextlib
import io
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from pa_research_backtest.artifact_validator import main as validate_main
from pa_research_backtest.artifact_validator import validate_artifact
from pa_research_backtest.engine import main as replay_main


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"


def create_current_artifact(output_dir: Path) -> None:
    with contextlib.redirect_stdout(io.StringIO()):
        result = replay_main(
            [
                "--prices",
                str(BACKTEST_ROOT / "prices.example.csv"),
                "--contracts",
                str(BACKTEST_ROOT / "contracts.example.csv"),
                "--output-dir",
                str(output_dir),
            ]
        )
    if result != 0:
        raise AssertionError(f"replay main returned {result}")


class PaResearchArtifactValidatorTests(unittest.TestCase):
    def test_current_artifact_is_valid_and_unchanged(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            before = {
                name: (output_dir / name).read_bytes()
                for name in ("results.csv", "summary.json", "run_metadata.json")
            }

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "current_valid")
            self.assertEqual(report["issues"], [])
            self.assertTrue(report["checks"]["summary_metadata_equal"])
            self.assertTrue(report["checks"]["summary_provenance_columns_equal"])
            self.assertTrue(report["checks"]["csv_summary_roundtrip"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = validate_main([str(output_dir)])
            self.assertEqual(exit_code, 0)
            self.assertIn('"status": "current_valid"', output.getvalue())
            for name, content in before.items():
                self.assertEqual((output_dir / name).read_bytes(), content)

    def test_cli_returns_one_for_missing_or_malformed_artifact_files(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            base = root / "base"
            create_current_artifact(base)
            variants = {}

            missing = root / "missing"
            shutil.copytree(base, missing)
            (missing / "summary.json").unlink()
            variants["missing summary"] = missing

            malformed_json = root / "malformed-json"
            shutil.copytree(base, malformed_json)
            (malformed_json / "summary.json").write_text("{", encoding="utf-8")
            variants["malformed JSON"] = malformed_json

            empty_csv = root / "empty-csv"
            shutil.copytree(base, empty_csv)
            (empty_csv / "results.csv").write_text("", encoding="utf-8")
            variants["empty CSV"] = empty_csv

            malformed_csv = root / "malformed-csv"
            shutil.copytree(base, malformed_csv)
            (malformed_csv / "results.csv").write_text('"unterminated\n', encoding="utf-8")
            variants["malformed CSV"] = malformed_csv

            for label, artifact_dir in variants.items():
                with self.subTest(label=label):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        exit_code = validate_main([str(artifact_dir)])
                    self.assertEqual(exit_code, 1)
                    self.assertIn('"status": "invalid"', output.getvalue())

    def test_missing_current_provenance_is_historical_with_exit_two(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            metadata_path = output_dir / "run_metadata.json"
            summary_path = output_dir / "summary.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            metadata.pop("summary_provenance")
            summary["run_metadata"] = metadata
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            summary_path.write_text(json.dumps(summary), encoding="utf-8")

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "historical_incomplete")
            self.assertIn("metadata predates the current artifact schema", report["historical_reasons"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = validate_main([str(output_dir)])
            self.assertEqual(exit_code, 2)
            self.assertIn('"status": "historical_incomplete"', output.getvalue())

    def test_missing_required_result_column_is_historical_with_exit_two(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            results_path = output_dir / "results.csv"
            results = pd.read_csv(results_path)
            results.drop(columns=["direction"]).to_csv(results_path, index=False)

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "historical_incomplete")
            self.assertIn("results.csv predates the current result schema", report["historical_reasons"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = validate_main([str(output_dir)])
            self.assertEqual(exit_code, 2)
            self.assertIn('"status": "historical_incomplete"', output.getvalue())

    def test_legacy_artifact_is_explicitly_historical_incomplete(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            metadata_path = output_dir / "run_metadata.json"
            summary_path = output_dir / "summary.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            metadata.pop("summary_provenance")
            metadata["engine_version"] = "0.3.1"
            summary["engine_version"] = "0.3.1"
            summary["run_metadata"] = metadata
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            summary_path.write_text(json.dumps(summary), encoding="utf-8")

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "historical_incomplete")
            self.assertIn("metadata predates the current artifact schema", report["historical_reasons"])
            self.assertIn("metadata engine_version='0.3.1' is not current '0.3.9'", report["historical_reasons"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = validate_main([str(output_dir)])
            self.assertEqual(exit_code, 2)
            self.assertIn('"status": "historical_incomplete"', output.getvalue())

    def test_current_artifact_hash_tampering_is_invalid(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            results_path = output_dir / "results.csv"
            results_path.write_bytes(results_path.read_bytes() + b"\n")

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "invalid")
            self.assertIn("metadata results_file_sha256 does not match results.csv", report["issues"])

    def test_current_artifact_summary_provenance_tampering_is_invalid(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            metadata_path = output_dir / "run_metadata.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["summary_provenance"]["completed_trade_count"] = 999
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "invalid")
            self.assertIn("summary.json run_metadata does not equal run_metadata.json", report["issues"])

    def test_current_artifact_source_hash_tampering_is_invalid(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            metadata_path = output_dir / "run_metadata.json"
            summary_path = output_dir / "summary.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            metadata["engine_source_sha256"] = "0" * 64
            summary["engine_source_sha256"] = "0" * 64
            summary["run_metadata"] = metadata
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            summary_path.write_text(json.dumps(summary), encoding="utf-8")

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "invalid")
            self.assertIn(
                "metadata engine_source_sha256 does not match engine_source",
                report["issues"],
            )

    def test_current_artifact_source_file_unavailable_is_invalid_with_exit_one(self):
        with TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            create_current_artifact(output_dir)
            metadata_path = output_dir / "run_metadata.json"
            summary_path = output_dir / "summary.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            metadata["engine_source"] = str(Path(temp_dir) / "missing-engine.py")
            summary["run_metadata"] = metadata
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            summary_path.write_text(json.dumps(summary), encoding="utf-8")

            report = validate_artifact(output_dir)

            self.assertEqual(report["status"], "invalid")
            self.assertIn("metadata engine_source file is unavailable", report["issues"])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = validate_main([str(output_dir)])
            self.assertEqual(exit_code, 1)
            self.assertIn('"status": "invalid"', output.getvalue())


if __name__ == "__main__":
    unittest.main()

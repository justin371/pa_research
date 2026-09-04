"""Regressions for descriptor-bound publication source provenance."""

from contextlib import redirect_stdout
from io import StringIO
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import call, patch

import pa_source_binding
from pa_source_binding import read_source_snapshot
import pa_research_backtest.engine as conventional_engine


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "research" / "backtesting"
ENGINE_SOURCE = ROOT / "pa_research_backtest" / "engine.py"
RENDERER_SOURCE = ROOT / "scripts" / "render_pa_blind_daily_batch.py"


class SourceBindingTests(unittest.TestCase):
    def _ordinary_import(self, source: Path, module_name: str):
        spec = importlib.util.spec_from_file_location(module_name, source)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        self.addCleanup(sys.modules.pop, module_name, None)
        spec.loader.exec_module(module)
        return module

    def test_snapshot_bytes_and_identity_come_from_one_descriptor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.py"
            source_a = b"VALUE = 'A'\n"
            source.write_bytes(source_a)
            file_stat = source.stat()
            with patch.object(pa_source_binding.os, "open", return_value=71) as opened, patch.object(
                pa_source_binding.os, "fstat", side_effect=[file_stat, file_stat]
            ) as fstat, patch.object(
                pa_source_binding.os, "read", side_effect=[source_a, b""]
            ) as read, patch.object(pa_source_binding.os, "close") as close:
                snapshot = read_source_snapshot(source, "test source")

            self.assertEqual(snapshot.content, source_a)
            self.assertEqual(snapshot.identity, (file_stat.st_dev, file_stat.st_ino))
            opened.assert_called_once()
            self.assertEqual(fstat.call_args_list, [call(71), call(71)])
            self.assertEqual(read.call_args_list[0], call(71, 1024 * 1024))
            self.assertEqual(read.call_args_list[1], call(71, 1024 * 1024))
            close.assert_called_once_with(71)

    def test_conventional_engine_import_cannot_publish_bound_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "artifact"
            with redirect_stdout(StringIO()), self.assertRaisesRegex(
                RuntimeError, "source-bound launcher"
            ):
                conventional_engine.main(
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

    def test_conventional_engine_cannot_transplant_public_snapshot_after_a_to_b_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_b = root / "engine.py"
            source_b.write_bytes(ENGINE_SOURCE.read_bytes() + b"\n# source B\n")
            transplanted = read_source_snapshot(source_b, "engine source")
            output_dir = root / "artifact"
            with patch.object(conventional_engine, "__file__", str(source_b)), patch.object(
                conventional_engine,
                "__PA_TRUSTED_SOURCE_SNAPSHOT__",
                transplanted,
                create=True,
            ), redirect_stdout(StringIO()), self.assertRaisesRegex(
                RuntimeError, "source-bound launcher"
            ):
                conventional_engine.main(
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

    def test_conventional_renderer_cannot_transplant_public_snapshot_after_a_to_b_change(self):
        renderer = self._ordinary_import(RENDERER_SOURCE, "test_conventional_blind_renderer")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_b = root / "renderer.py"
            source_b.write_bytes(RENDERER_SOURCE.read_bytes() + b"\n# source B\n")
            transplanted = read_source_snapshot(source_b, "renderer source")
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "label_hidden": True,
                        "outcome_hidden": True,
                        "selection_mode": "explicit_cutoff",
                        "minimum_context_bars": 1,
                        "minimum_hidden_future_bars": 1,
                        "source_binding_required": True,
                        "renderer_source_sha256": transplanted.sha256,
                    }
                ),
                encoding="utf-8",
            )
            output_dir = root / "charts"
            with patch.object(renderer, "__file__", str(source_b)), patch.object(
                renderer,
                "__PA_TRUSTED_SOURCE_SNAPSHOT__",
                transplanted,
                create=True,
            ), self.assertRaisesRegex(RuntimeError, "source-bound launcher"):
                renderer.render_manifest(manifest, root, output_dir)
            self.assertFalse(output_dir.exists())

    def test_batch_one_reproduction_uses_new_non_frozen_output_directory(self):
        readme = (
            ROOT
            / "research"
            / "assets"
            / "visual_recognition"
            / "2026-09-01"
            / "selection_quality_blind_batch1"
            / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("render_pa_blind_daily_batch_bound.py", readme)
        self.assertIn(
            "--output-dir .\\.codex\\artifacts\\selection-quality-blind-batch1-repro-20260904",
            readme,
        )
        self.assertNotIn(
            "--output-dir .\\research\\assets\\visual_recognition\\2026-09-01\\selection_quality_blind_batch1",
            readme,
        )
        self.assertIn("输出目录必须尚不存在", readme)
        self.assertIn("不覆盖冻结图", readme)
        self.assertIn("不承诺新旧 PNG 字节相同", readme)


if __name__ == "__main__":
    unittest.main()

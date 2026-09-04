import csv
import json
import tempfile
import unittest
from unittest.mock import patch
from datetime import date, timedelta
from pathlib import Path

from pa_source_binding import load_source_module


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_pa_blind_daily_batch.py"
MODULE = load_source_module(SCRIPT, "test_source_bound_blind_daily_renderer", "renderer source")


class BlindDailyBatchTests(unittest.TestCase):
    @staticmethod
    def _write_synthetic_png(*args, **kwargs):
        output_file = args[3]
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_bytes(b"synthetic-png")

    def _synthetic_manifest(self, root=None):
        bars = [MODULE.DailyBar("TEST", date(2020, 1, 1) + timedelta(days=i), 100, 101, 99, 100.5, 1000) for i in range(700)]
        if root is not None:
            (root / "prices.csv").write_text(
                "Symbol,Date,Open,High,Low,Close,Volume\nTEST,2020-01-01,100,101,99,100.5,1000\n",
                encoding="utf-8",
            )
        manifest = {
            "label_hidden": True, "outcome_hidden": True,
            "selection_mode": "explicit_cutoff", "minimum_context_bars": 500,
            "minimum_hidden_future_bars": 40, "daily_chart_bars": 504,
            "local_chart_bars": 120,
            "samples": [{"sample_id": f"MC2-{index:03d}", "symbol": "TEST", "price_file": "prices.csv",
                         "cutoff_date": bars[cutoff].session_date.isoformat(), "chart_file": f"MC2-{index:03d}.png"}
                        for index, cutoff in enumerate((620, 621), start=1)],
        }
        return bars, manifest

    def test_manifest_rejects_invalid_integer_parameters_before_render(self):
        for field in ("minimum_context_bars", "minimum_hidden_future_bars", "daily_chart_bars", "local_chart_bars"):
            for value in (True, 500.5, "500", 0, -1):
                with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    bars, manifest = self._synthetic_manifest(root)
                    manifest[field] = value
                    source = root / "manifest.json"
                    source.write_text(json.dumps(manifest), encoding="utf-8")
                    with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(MODULE, "render_sample") as render:
                        with self.assertRaisesRegex(ValueError, field):
                            MODULE.render_manifest(source, root, root / "charts")
                        render.assert_not_called()

    def test_all_sample_validation_precedes_any_render(self):
        for defect in ("duplicate_id", "bad_filename", "bad_cutoff", "case_collision"):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bars, manifest = self._synthetic_manifest(root)
                second = manifest["samples"][1]
                if defect == "duplicate_id":
                    second["sample_id"] = "S620"
                elif defect == "bad_filename":
                    second["chart_file"] = "../outside.png"
                elif defect == "case_collision":
                    second["chart_file"] = "s620.PNG"
                else:
                    second["cutoff_date"] = "2025-01-01"
                source = root / "manifest.json"
                source.write_text(json.dumps(manifest), encoding="utf-8")
                with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(MODULE, "render_sample") as render:
                    with self.assertRaises(ValueError):
                        MODULE.render_manifest(source, root, root / "charts")
                    render.assert_not_called()
                self.assertFalse((root / "charts").exists())

    def test_existing_late_output_prevents_entire_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bars, manifest = self._synthetic_manifest(root)
            output = root / "charts"
            output.mkdir()
            frozen = output / "MC2-002.png"
            frozen.write_bytes(b"frozen-sentinel")
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(MODULE, "render_sample") as render:
                with self.assertRaises(FileExistsError):
                    MODULE.render_manifest(source, root, output)
                render.assert_not_called()
            self.assertEqual(frozen.read_bytes(), b"frozen-sentinel")
            self.assertFalse((output / "MC2-001.png").exists())

    def test_direct_render_never_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "frozen.png"
            target.write_bytes(b"frozen-sentinel")
            bars, _ = self._synthetic_manifest()
            with self.assertRaises(FileExistsError):
                MODULE.render_sample(bars, 620, "S620", target, 504, 120)
            self.assertEqual(target.read_bytes(), b"frozen-sentinel")

    def test_direct_render_rejects_invalid_cutoff_and_windows(self):
        bars, _ = self._synthetic_manifest()
        for cutoff, daily, local in ((-2, 504, 120), (700, 504, 120), (True, 504, 120), (620, 0, 120), (620, 504, -1), (620, 120, 504)):
            with self.subTest(cutoff=cutoff, daily=daily, local=local), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "chart.png"
                with self.assertRaises(ValueError):
                    MODULE.render_sample(bars, cutoff, "TEST", target, daily, local)
                self.assertFalse(target.exists())

    def test_output_created_after_preflight_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "chart.png"
            bars, _ = self._synthetic_manifest()

            def concurrent_writer(buffer, **kwargs):
                target.write_bytes(b"concurrent-sentinel")
                buffer.write(b"synthetic-png")

            with patch("matplotlib.figure.Figure.savefig", side_effect=concurrent_writer), patch.object(MODULE.plt, "close", wraps=MODULE.plt.close) as close:
                with self.assertRaises(FileExistsError):
                    MODULE.render_sample(bars, 620, "TEST", target, 504, 120)
                self.assertTrue(close.called)
            self.assertEqual(target.read_bytes(), b"concurrent-sentinel")

    def test_encoding_failure_leaves_no_output_and_closes_figure(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "charts" / "chart.png"
            bars, _ = self._synthetic_manifest()
            with patch("matplotlib.figure.Figure.savefig", side_effect=OSError("synthetic encoding failure")), patch.object(MODULE.plt, "close", wraps=MODULE.plt.close) as close:
                with self.assertRaisesRegex(OSError, "synthetic encoding failure"):
                    MODULE.render_sample(bars, 620, "TEST", target, 504, 120)
                self.assertTrue(close.called)
            self.assertFalse(target.exists())
            self.assertFalse(target.parent.exists())

    def test_duplicate_symbol_cutoff_is_rejected_before_any_render(self):
        for mode in ("explicit_cutoff", "deterministic_cutoff"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                manifest = {
                    "label_hidden": True, "outcome_hidden": True,
                    "selection_mode": mode, "selection_seed": "seed",
                    "minimum_context_bars": 600, "minimum_hidden_future_bars": 40,
                    "samples": [
                        {"sample_id": "DUP-A", "symbol": "TEST", "price_file": "a.csv", "cutoff_date": "2021-09-01", "chart_file": "A.png"},
                        {"sample_id": "DUP-B", "symbol": "test", "price_file": "copied.csv", "cutoff_date": "2021-09-01", "chart_file": "B.png"},
                    ],
                }
                source = root / "manifest.json"
                source.write_text(json.dumps(manifest), encoding="utf-8")
                with patch.object(MODULE, "render_sample") as render:
                    with self.assertRaisesRegex(ValueError, "duplicate symbol/cutoff"):
                        MODULE.render_manifest(source, root, root / "charts")
                    render.assert_not_called()
                self.assertFalse((root / "charts").exists())

    def test_same_symbol_different_cutoffs_are_not_treated_as_duplicate(self):
        bars = [MODULE.DailyBar("TEST", date(2020, 1, 1) + timedelta(days=i), 100, 101, 99, 100.5, 1000) for i in range(700)]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {
                "label_hidden": True, "outcome_hidden": True,
                "selection_mode": "explicit_cutoff", "minimum_context_bars": 600,
                "minimum_hidden_future_bars": 40,
                "samples": [
                    {"sample_id": f"MC2-{index:03d}", "symbol": "TEST", "price_file": "prices.csv", "cutoff_date": bars[cutoff].session_date.isoformat(), "chart_file": f"MC2-{index:03d}.png"}
                    for index, cutoff in enumerate((620, 621), start=1)
                ],
            }
            (root / "prices.csv").write_text("synthetic", encoding="utf-8")
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(
                MODULE, "render_sample", side_effect=self._write_synthetic_png
            ) as render:
                outputs = MODULE.render_manifest(source, root, root / "charts")
            self.assertEqual(len(outputs), 2)
            self.assertEqual(render.call_count, 2)

    def test_manifest_rejects_price_file_outside_repo_before_render(self):
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            root = temp_root / "repo"
            root.mkdir()
            outside = temp_root / "outside.csv"
            outside.write_text("private-synthetic-data", encoding="utf-8")
            bars, manifest = self._synthetic_manifest(root)
            source = root / "manifest.json"
            for value in ("../outside.csv", str(outside.resolve()), "C:outside.csv"):
                with self.subTest(price_file=value):
                    manifest["samples"][0]["price_file"] = value
                    source.write_text(json.dumps(manifest), encoding="utf-8")
                    with patch.object(MODULE, "load_symbol_bars") as load, patch.object(
                        MODULE, "render_sample"
                    ) as render:
                        with self.assertRaisesRegex(ValueError, "price_file"):
                            MODULE.render_manifest(source, root, root / "charts")
                        load.assert_not_called()
                        render.assert_not_called()
                    self.assertFalse((root / "charts").exists())

    def test_manifest_rejects_price_file_symlink_outside_repo(self):
        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            root = temp_root / "repo"
            root.mkdir()
            outside = temp_root / "outside.csv"
            outside.write_text("private-synthetic-data", encoding="utf-8")
            link = root / "linked.csv"
            try:
                link.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            bars, manifest = self._synthetic_manifest(root)
            manifest["samples"][0]["price_file"] = "linked.csv"
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            with patch.object(MODULE, "load_symbol_bars") as load, patch.object(
                MODULE, "render_sample"
            ) as render:
                with self.assertRaisesRegex(ValueError, "price_file"):
                    MODULE.render_manifest(source, root, root / "charts")
                load.assert_not_called()
                render.assert_not_called()

    def test_batch_encoding_failure_leaves_no_final_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bars, manifest = self._synthetic_manifest(root)
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            calls = 0

            def fail_second(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("synthetic second-image failure")
                self._write_synthetic_png(*args, **kwargs)

            with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(
                MODULE, "render_sample", side_effect=fail_second
            ):
                with self.assertRaisesRegex(OSError, "second-image failure"):
                    MODULE.render_manifest(source, root, root / "charts")
            self.assertFalse((root / "charts" / "MC2-001.png").exists())
            self.assertFalse((root / "charts" / "MC2-002.png").exists())

    def test_hidden_manifest_rejects_answer_bearing_ids_and_filenames(self):
        for sample_id in ("H1-001", "L2-WINNER", "BOP-positive", "short-target-hit", "BQ1-H1-WINNER"):
            with self.subTest(sample_id=sample_id), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bars, manifest = self._synthetic_manifest(root)
                manifest["samples"][0]["sample_id"] = sample_id
                manifest["samples"][0]["chart_file"] = f"{sample_id}.png"
                source = root / "manifest.json"
                source.write_text(json.dumps(manifest), encoding="utf-8")
                with patch.object(MODULE, "load_symbol_bars") as load, patch.object(
                    MODULE, "render_sample"
                ) as render:
                    with self.assertRaisesRegex(ValueError, "approved neutral"):
                        MODULE.render_manifest(source, root, root / "charts")
                    load.assert_not_called()
                    render.assert_not_called()

    def test_hidden_manifest_preserves_approved_neutral_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for identity_hidden in (False, True):
                bars, manifest = self._synthetic_manifest(root)
                manifest["identity_hidden"] = identity_hidden
                source = root / f"manifest-{identity_hidden}.json"
                source.write_text(json.dumps(manifest), encoding="utf-8")
                with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(
                    MODULE, "render_sample", side_effect=self._write_synthetic_png
                ) as render:
                    MODULE.render_manifest(source, root, root / f"charts-{identity_hidden}")
                self.assertEqual([call.args[2] for call in render.call_args_list], ["MC2-001", "MC2-002"])

    def test_atomic_promotion_preserves_destination_created_during_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bars, manifest = self._synthetic_manifest(root)
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            output = root / "charts"
            concurrent = output / "MC2-002.png"
            calls = 0

            def create_staged_then_race(*args, **kwargs):
                nonlocal calls
                calls += 1
                self._write_synthetic_png(*args, **kwargs)
                if calls == 2:
                    output.mkdir(parents=True, exist_ok=True)
                    concurrent.write_bytes(b"concurrent-sentinel")

            with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(
                MODULE, "render_sample", side_effect=create_staged_then_race
            ):
                with self.assertRaises(FileExistsError):
                    MODULE.render_manifest(source, root, output)
            self.assertFalse((output / "MC2-001.png").exists())
            self.assertEqual(concurrent.read_bytes(), b"concurrent-sentinel")

    def test_atomic_promotion_rejects_empty_destination_created_at_publish(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bars, manifest = self._synthetic_manifest(root)
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            output = root / "charts"
            real_publish = MODULE._publish_directory_no_replace

            def create_empty_destination_then_publish(staging_root, destination):
                destination.mkdir()
                return real_publish(staging_root, destination)

            with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(
                MODULE, "render_sample", side_effect=self._write_synthetic_png
            ), patch.object(
                MODULE, "_publish_directory_no_replace", side_effect=create_empty_destination_then_publish
            ):
                with self.assertRaises(FileExistsError):
                    MODULE.render_manifest(source, root, output)
            self.assertTrue(output.is_dir())
            self.assertEqual(list(output.iterdir()), [])

    def test_manifest_rejects_ntfs_stream_device_unc_and_non_csv_source_paths(self):
        invalid = (
            "prices.csv:hidden",
            "NUL.csv",
            "folder/COM1.csv",
            "C:\\outside.csv",
            "\\\\server\\share\\outside.csv",
            "folder/trailing. /prices.csv",
            "prices.txt",
        )
        for value in invalid:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bars, manifest = self._synthetic_manifest(root)
                manifest["samples"][0]["price_file"] = value
                source = root / "manifest.json"
                source.write_text(json.dumps(manifest), encoding="utf-8")
                with patch.object(MODULE, "load_symbol_bars") as load, patch.object(
                    MODULE, "render_sample"
                ) as render:
                    with self.assertRaisesRegex(ValueError, "price_file"):
                        MODULE.render_manifest(source, root, root / "charts")
                    load.assert_not_called()
                    render.assert_not_called()

    def test_manifest_rejects_directory_named_csv_before_parse(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "directory.csv").mkdir()
            bars, manifest = self._synthetic_manifest(root)
            manifest["samples"][0]["price_file"] = "directory.csv"
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            with patch.object(MODULE, "load_symbol_bars") as load, patch.object(
                MODULE, "render_sample"
            ) as render:
                with self.assertRaisesRegex(ValueError, "regular CSV file"):
                    MODULE.render_manifest(source, root, root / "charts")
                load.assert_not_called()
                render.assert_not_called()

    def test_source_binding_rejects_changed_file_and_visible_window_before_render(self):
        for changed_binding in ("file", "window"):
            with self.subTest(changed_binding=changed_binding), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                price_file = root / "prices.csv"
                rows = []
                first = date(2020, 1, 1)
                for index in range(700):
                    rows.append(
                        {
                            "Symbol": "TEST",
                            "Date": (first + timedelta(days=index)).isoformat(),
                            "Open": 100,
                            "High": 101,
                            "Low": 99,
                            "Close": 100.5,
                            "Volume": 1000,
                        }
                    )
                with price_file.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(rows)
                cutoff = date.fromisoformat(rows[620]["Date"])
                window_rows, window_sha256 = MODULE.source_window_fingerprint(price_file, "TEST", cutoff, 504)
                sample = {
                    "sample_id": "MC2-001",
                    "symbol": "TEST",
                    "price_file": "prices.csv",
                    "cutoff_date": cutoff.isoformat(),
                    "chart_file": "MC2-001.png",
                    "source_file_sha256": MODULE._sha256_file(price_file),
                    "source_window_rows": window_rows,
                    "source_window_sha256": window_sha256,
                }
                if changed_binding == "file":
                    sample["source_file_sha256"] = "0" * 64
                else:
                    sample["source_window_sha256"] = "0" * 64
                manifest = {
                    "label_hidden": True,
                    "outcome_hidden": True,
                    "selection_mode": "explicit_cutoff",
                    "minimum_context_bars": 500,
                    "minimum_hidden_future_bars": 40,
                    "daily_chart_bars": 504,
                    "local_chart_bars": 120,
                    "source_binding_required": True,
                    "renderer_source_sha256": MODULE._sha256_file(SCRIPT),
                    "samples": [sample],
                }
                source = root / "manifest.json"
                source.write_text(json.dumps(manifest), encoding="utf-8")
                with patch.object(MODULE, "render_sample") as render:
                    with self.assertRaisesRegex(ValueError, "source_file_sha256|source window binding"):
                        MODULE.render_manifest(source, root, root / "charts")
                    render.assert_not_called()

    def test_source_binding_and_render_use_one_immutable_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            price_file = root / "prices.csv"
            first = date(2020, 1, 1)
            rows = [
                {
                    "Symbol": "TEST",
                    "Date": (first + timedelta(days=index)).isoformat(),
                    "Open": 100,
                    "High": 101,
                    "Low": 99,
                    "Close": 100.5,
                    "Volume": 1000,
                }
                for index in range(700)
            ]
            with price_file.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            original_text = price_file.read_text(encoding="utf-8")
            cutoff = date.fromisoformat(rows[620]["Date"])
            window_rows, window_sha256 = MODULE.source_window_fingerprint(price_file, "TEST", cutoff, 504)
            manifest = {
                "label_hidden": True,
                "outcome_hidden": True,
                "selection_mode": "explicit_cutoff",
                "minimum_context_bars": 500,
                "minimum_hidden_future_bars": 40,
                "daily_chart_bars": 504,
                "local_chart_bars": 120,
                "source_binding_required": True,
                "renderer_source_sha256": MODULE._sha256_file(SCRIPT),
                "samples": [
                    {
                        "sample_id": "MC2-001",
                        "symbol": "TEST",
                        "price_file": "prices.csv",
                        "cutoff_date": cutoff.isoformat(),
                        "chart_file": "MC2-001.png",
                        "source_file_sha256": MODULE._sha256_file(price_file),
                        "source_window_rows": window_rows,
                        "source_window_sha256": window_sha256,
                    }
                ],
            }
            source = root / "manifest.json"
            source.write_text(json.dumps(manifest), encoding="utf-8")
            real_fingerprint = MODULE.source_window_fingerprint
            rendered_closes = []

            def fingerprint_then_replace(snapshot, *args, **kwargs):
                result = real_fingerprint(snapshot, *args, **kwargs)
                price_file.write_text(
                    original_text.replace(",100,101,99,100.5,1000", ",200,201,199,200.5,1000"),
                    encoding="utf-8",
                )
                return result

            def capture_snapshot_bars(*args, **kwargs):
                rendered_closes.append(args[0][0].close)
                self._write_synthetic_png(*args, **kwargs)

            with patch.object(MODULE, "source_window_fingerprint", side_effect=fingerprint_then_replace), patch.object(
                MODULE, "render_sample", side_effect=capture_snapshot_bars
            ):
                outputs = MODULE.render_manifest(source, root, root / "charts")
            self.assertEqual(rendered_closes, [100.5])
            self.assertEqual(outputs, [root / "charts" / "MC2-001.png"])

    def test_bound_renderer_rejects_its_source_changing_during_render(self):
        manifest_path = (
            ROOT
            / "research/assets/visual_recognition/2026-09-01"
            / "morphology_calibration_candidate_v1/manifest.json"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_renderer = root / "render_pa_blind_daily_batch.py"
            original_source = SCRIPT.read_bytes()
            fake_renderer.write_bytes(original_source)
            bound_renderer = load_source_module(
                fake_renderer,
                "test_mutating_blind_daily_renderer",
                "renderer source",
            )
            changed = False

            def replace_renderer_source(*args, **kwargs):
                nonlocal changed
                self._write_synthetic_png(*args, **kwargs)
                if not changed:
                    fake_renderer.write_bytes(original_source + b"\n# replaced during render\n")
                    changed = True

            with patch.object(bound_renderer, "render_sample", side_effect=replace_renderer_source):
                with self.assertRaisesRegex(RuntimeError, "renderer source changed during run"):
                    bound_renderer.render_manifest(manifest_path, ROOT, root / "charts")
            self.assertFalse((root / "charts").exists())

    def test_bound_renderer_rejects_loaded_source_a_after_path_becomes_b(self):
        manifest_path = (
            ROOT
            / "research/assets/visual_recognition/2026-09-01"
            / "morphology_calibration_candidate_v1/manifest.json"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_renderer = root / "render_pa_blind_daily_batch.py"
            source_a = SCRIPT.read_bytes()
            fake_renderer.write_bytes(source_a)
            bound_renderer = load_source_module(
                fake_renderer,
                "test_pre_render_replaced_renderer",
                "renderer source",
            )
            fake_renderer.write_bytes(source_a + b"\n# source B restored before render\n")
            with patch.object(bound_renderer, "render_sample", side_effect=self._write_synthetic_png):
                with self.assertRaisesRegex(RuntimeError, "renderer source changed during run"):
                    bound_renderer.render_manifest(manifest_path, ROOT, root / "charts")
            self.assertFalse((root / "charts").exists())

    def test_render_ema_uses_all_pre_cutoff_history_as_warmup(self):
        bars = [
            MODULE.DailyBar(
                "TEST",
                date(2020, 1, 1) + timedelta(days=index),
                100 + index,
                102 + index,
                99 + index,
                101 + index,
                1000,
            )
            for index in range(600)
        ]
        captured = []

        def capture_price(_axis, visible_bars, ema_series):
            captured.append((list(visible_bars), {period: list(values) for period, values in ema_series.items()}))

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "MC2-001.png"
            with patch.object(MODULE, "_plot_price", side_effect=capture_price):
                MODULE.render_sample(bars, 599, "MC2-001", output, 504, 120)
        full_ema = MODULE.ema([bar.close for bar in bars], 200)
        self.assertEqual(len(captured), 2)
        self.assertEqual(captured[0][1][200], full_ema[-504:])
        self.assertEqual(captured[1][1][200], full_ema[-120:])
        self.assertNotEqual(captured[0][1][200], MODULE.ema([bar.close for bar in bars[-504:]], 200))

    def test_deterministic_seed_must_be_non_empty_string(self):
        for value in (True, 123, [], {}, "", "   "):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                bars, manifest = self._synthetic_manifest(root)
                manifest["selection_mode"] = "deterministic_cutoff"
                manifest["selection_seed"] = value
                source = root / "manifest.json"
                source.write_text(json.dumps(manifest), encoding="utf-8")
                with patch.object(MODULE, "load_symbol_bars", return_value=bars), patch.object(
                    MODULE, "render_sample"
                ) as render:
                    with self.assertRaisesRegex(ValueError, "selection_seed"):
                        MODULE.render_manifest(source, root, root / "charts")
                    render.assert_not_called()

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
                        "sample_id": "BQ1-TEST",
                        "symbol": "TEST",
                        "price_file": "prices.csv",
                        "cutoff_date": rows[cutoff_index]["Date"],
                        "chart_file": "BQ1-TEST.png",
                    }
                ],
            }
            manifest_file = root / "manifest.json"
            manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
            output_dir = root / "charts"

            outputs = MODULE.render_manifest(manifest_file, root, output_dir)

            self.assertEqual(outputs, [output_dir / "BQ1-TEST.png"])
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
                                "sample_id": "BQ1-TEST",
                                "symbol": "TEST",
                                "price_file": "prices.csv",
                                "cutoff_date": "2020-01-01",
                                "chart_file": "BQ1-TEST.png",
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
                                "sample_id": "MC2-001",
                                "symbol": "TEST",
                                "price_file": "prices.csv",
                                "cutoff_date": rows[549]["Date"],
                                "chart_file": "MC2-001.png",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            outputs = MODULE.render_manifest(manifest_file, root, root / "charts")
            self.assertEqual(outputs, [root / "charts" / "MC2-001.png"])
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

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "pa_visual_examples", ROOT / "scripts" / "pa_visual_examples.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def entry(identifier="bop-1", **overrides):
    value = {
        "id": identifier,
        "title": "Breakout Pullback",
        "concepts": ["breakout", "pullback"],
        "source_url": "https://example.test/brooks",
        "page": 42,
        "visual_status": "available",
        "contrast_note": "A failed breakout returns into the range.",
        "usage": "teaching_with_outcome",
    }
    value.update(overrides)
    return value


class PaVisualExamplesTests(unittest.TestCase):
    def write_registry(self, document):
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / "registry.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        self.addCleanup(directory.cleanup)
        return path

    def test_query_is_case_insensitive_and_searches_concepts_and_contrast(self):
        rows = [
            entry("bop-1"),
            entry("range-1", title="Range example", concepts=["balance"], contrast_note="A failed breakout at the range edge."),
            entry("other", title="Trend example", concepts=["trend"], contrast_note="Clean continuation."),
        ]
        self.assertEqual(
            [row["id"] for row in MODULE.search_registry(rows, "FAILED BREAKOUT")],
            ["bop-1", "range-1"],
        )
        self.assertEqual(len(MODULE.search_registry(rows)), 3)

    def test_malformed_page_and_http_url_are_rejected(self):
        for changes in (
            {"page": 0},
            {"source_url": "http://example.test/ref"},
            {"source_url": "https://"},
            {"concepts": "breakout"},
            {"concepts": ["breakout", 3]},
        ):
            path = self.write_registry([entry(**changes)])
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                MODULE.load_registry(path)

    def test_duplicate_ids_are_rejected(self):
        path = self.write_registry([entry("same"), entry("same", title="another")])
        with self.assertRaisesRegex(ValueError, "duplicate entry id"):
            MODULE.load_registry(path)

    def test_cli_reports_only_available_local_images_and_returns_json(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / "found.png").write_bytes(b"image")
        registry = root / "registry.json"
        registry.write_text(
            json.dumps([entry("visual", image_paths=["found.png", "missing.png"])]),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "pa_visual_examples.py"), "--query", "VISUAL", "--registry", str(registry)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result[0]["source_url"], "https://example.test/brooks")
        self.assertEqual(result[0]["page"], 42)
        self.assertEqual(result[0]["local_image_paths"], [str((root / "found.png").resolve())])


if __name__ == "__main__":
    unittest.main()

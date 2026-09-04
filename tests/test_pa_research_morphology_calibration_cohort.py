import csv
from datetime import date
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from pa_source_binding import load_source_module


REPO_ROOT = Path(__file__).resolve().parents[1]
COHORT_ROOT = (
    REPO_ROOT
    / "research"
    / "assets"
    / "visual_recognition"
    / "2026-09-01"
    / "morphology_calibration_candidate_v1"
)
MANIFEST_PATH = COHORT_ROOT / "manifest.json"
README_PATH = COHORT_ROOT / "README.md"
REVIEW_FORM_PATH = COHORT_ROOT / "review_form.md"
AUDIT_PATH = REPO_ROOT / "research" / "morphology_calibration_candidate_cohort_audit_2026-09-01_CN.md"
RENDERER_PATH = REPO_ROOT / "scripts" / "render_pa_blind_daily_batch.py"
RENDERER = load_source_module(RENDERER_PATH, "cohort_source_bound_blind_daily_renderer", "renderer source")
PNG_TOKEN_RE = re.compile(r"(?<![\w.-])([A-Za-z0-9][\w.-]*\.png)(?![\w.-])", re.IGNORECASE)
FORBIDDEN_REVIEW_FIELDS = {
    "candidate_family",
    "candidate_label",
    "answer",
    "expert_label",
    "result",
    "trade_result",
    "realized_R",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def subtract_calendar_years(value: date, years: int) -> date:
    try:
        return value.replace(year=value.year - years)
    except ValueError:
        if value.month == 2 and value.day == 29:
            return value.replace(year=value.year - years, day=28)
        raise


def source_window_key(sample: dict, window_size: int, repo_root: Path = REPO_ROOT) -> tuple[str, date, str]:
    symbol = sample["symbol"].strip().upper()
    cutoff = date.fromisoformat(sample["cutoff_date"])
    with (repo_root / sample["price_file"]).open(encoding="utf-8-sig", newline="") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["Symbol"].strip().upper() == symbol and date.fromisoformat(row["Date"]) <= cutoff
        ]
    rows.sort(key=lambda row: date.fromisoformat(row["Date"]))
    visible = rows[-window_size:]
    normalized_rows = []
    for row in visible:
        normalized_rows.append(
            "|".join(
                [
                    date.fromisoformat(row["Date"]).isoformat(),
                    *(format(Decimal(row[field].strip()).normalize(), "f") for field in ("Open", "High", "Low", "Close", "Volume")),
                ]
            )
        )
    normalized = "\n".join(normalized_rows)
    return symbol, cutoff, hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def sorted_symbol_dates(rows: list[dict], symbol: str) -> list[date]:
    normalized_symbol = symbol.strip().upper()
    return sorted(
        date.fromisoformat(row["Date"])
        for row in rows
        if row["Symbol"].strip().upper() == normalized_symbol
    )


class MorphologyCalibrationCohortTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(read(MANIFEST_PATH))

    def test_manifest_is_strict_label_and_outcome_hidden_candidate_cohort(self):
        manifest = self.manifest
        self.assertEqual(manifest["cohort_id"], "curated_morphology_cohort")
        self.assertEqual(manifest["selection_mode"], "explicit_cutoff")
        self.assertTrue(manifest["label_hidden"])
        self.assertTrue(manifest["outcome_hidden"])
        self.assertTrue(manifest["future_bars_hidden"])
        self.assertTrue(manifest["selection_frozen_before_view"])
        self.assertGreaterEqual(manifest["minimum_context_bars"], 500)
        self.assertGreaterEqual(manifest["minimum_hidden_future_bars"], 40)
        self.assertGreaterEqual(manifest["daily_chart_bars"], 500)
        self.assertEqual(len(manifest["samples"]), 16)

    def test_reviewer_manifest_has_neutral_unique_ids_and_no_answer_fields(self):
        samples = self.manifest["samples"]
        ids = [sample["sample_id"] for sample in samples]
        files = [sample["chart_file"] for sample in samples]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(files), len(set(files)))
        for sample in samples:
            self.assertRegex(sample["sample_id"], r"^MC2-\d{3}$")
            self.assertEqual(sample["chart_file"], f"{sample['sample_id']}.png")
            self.assertTrue(FORBIDDEN_REVIEW_FIELDS.isdisjoint(sample))
        reviewer_text = read(README_PATH).lower()
        self.assertNotIn("candidate_label", reviewer_text)
        self.assertNotIn("candidate_family", reviewer_text)
        self.assertNotIn("answer_key", reviewer_text)

    def test_review_form_does_not_predeclare_reviewer_knowledge_status(self):
        review_form = read(REVIEW_FORM_PATH)
        for sample in self.manifest["samples"]:
            with self.subTest(sample=sample["sample_id"]):
                row = next(
                    line for line in review_form.splitlines() if line.startswith(f"| {sample['sample_id']} |")
                )
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                self.assertEqual(cells[1], "")

    def test_every_cutoff_has_declared_bar_count_and_hidden_future(self):
        minimum_context = self.manifest["minimum_context_bars"]
        minimum_future = self.manifest["minimum_hidden_future_bars"]
        for sample in self.manifest["samples"]:
            with self.subTest(sample=sample["sample_id"]):
                price_path = REPO_ROOT / sample["price_file"]
                with price_path.open("r", encoding="utf-8-sig", newline="") as handle:
                    rows = [
                        row
                        for row in csv.DictReader(handle)
                        if row["Symbol"].strip().upper() == sample["symbol"]
                    ]
                dates = sorted_symbol_dates(rows, sample["symbol"])
                cutoff = date.fromisoformat(sample["cutoff_date"])
                self.assertEqual(dates.count(cutoff), 1)
                cutoff_index = dates.index(cutoff)
                self.assertGreaterEqual(cutoff_index + 1, minimum_context)
                self.assertGreaterEqual(len(rows) - cutoff_index - 1, minimum_future)

    def test_hidden_future_count_is_independent_of_csv_row_order(self):
        rows = [
            {"Symbol": "TEST", "Date": "2024-01-03"},
            {"Symbol": "OTHER", "Date": "2024-01-01"},
            {"Symbol": "TEST", "Date": "2024-01-01"},
            {"Symbol": "TEST", "Date": "2024-01-04"},
            {"Symbol": "TEST", "Date": "2024-01-02"},
        ]
        ordered = sorted_symbol_dates(rows, "test")
        cutoff_index = ordered.index(date(2024, 1, 2))
        self.assertEqual(cutoff_index + 1, 2)
        self.assertEqual(len(ordered) - cutoff_index - 1, 2)

    def test_manifest_binds_renderer_source_files_and_visible_windows(self):
        self.assertTrue(self.manifest["source_binding_required"])
        self.assertEqual(
            self.manifest["renderer_source_sha256"],
            hashlib.sha256(RENDERER_PATH.read_bytes()).hexdigest(),
        )
        window_size = self.manifest["daily_chart_bars"]
        for sample in self.manifest["samples"]:
            with self.subTest(sample=sample["sample_id"]):
                price_path = REPO_ROOT / sample["price_file"]
                self.assertEqual(sample["source_file_sha256"], hashlib.sha256(price_path.read_bytes()).hexdigest())
                _, _, window_sha256 = source_window_key(sample, window_size)
                self.assertEqual(sample["source_window_rows"], window_size)
                self.assertEqual(sample["source_window_sha256"], window_sha256)

    def test_audit_and_renderer_window_canonicalization_remain_identical(self):
        window_size = self.manifest["daily_chart_bars"]
        for sample in self.manifest["samples"]:
            with self.subTest(sample=sample["sample_id"]):
                symbol, cutoff, audit_sha256 = source_window_key(sample, window_size)
                renderer_rows, renderer_sha256 = RENDERER.source_window_fingerprint(
                    REPO_ROOT / sample["price_file"], symbol, cutoff, window_size
                )
                self.assertEqual(renderer_rows, sample["source_window_rows"])
                self.assertEqual(renderer_sha256, audit_sha256)

    def test_source_window_identity_survives_copy_or_rename_but_not_data_change(self):
        rows = ["Symbol,Date,Open,High,Low,Close,Volume"]
        for day in range(1, 11):
            rows.append(f"TEST,2024-01-{day:02d},100.0,102.00,99.000,101.0,{1000 + day}.0")
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            original = root / "original.csv"
            copied = root / "renamed.csv"
            changed = root / "changed.csv"
            original.write_text("\n".join(rows) + "\n", encoding="utf-8")
            shutil.copyfile(original, copied)
            changed_rows = list(rows)
            changed_rows[-1] = changed_rows[-1].replace("101.0", "101.1")
            changed.write_text("\n".join(changed_rows) + "\n", encoding="utf-8")
            common = {"symbol": "test", "cutoff_date": "2024-01-10"}
            original_key = source_window_key({**common, "price_file": "original.csv"}, 10, root)
            copied_key = source_window_key({**common, "price_file": "renamed.csv"}, 10, root)
            changed_key = source_window_key({**common, "price_file": "changed.csv"}, 10, root)
            self.assertEqual(original_key, copied_key)
            self.assertNotEqual(original_key, changed_key)

    def test_readme_calendar_spans_match_source_windows_without_overclaim(self):
        content = read(README_PATH)
        self.assertIn("daily_context_window: <2y", content)
        self.assertIn("--output-dir .\\.codex\\artifacts\\morphology-candidate-review-20260903", content)
        self.assertNotIn("--output-dir .\\research\\assets", content)
        short_count = 0
        for sample in self.manifest["samples"]:
            with (REPO_ROOT / sample["price_file"]).open(encoding="utf-8-sig", newline="") as handle:
                dates = sorted(row["Date"] for row in csv.DictReader(handle)
                               if row["Symbol"].strip().upper() == sample["symbol"]
                               and row["Date"] <= sample["cutoff_date"])
            visible = dates[-self.manifest["daily_chart_bars"]:]
            cutoff = date.fromisoformat(sample["cutoff_date"])
            anniversary = subtract_calendar_years(cutoff, 2)
            span = ">=2y" if date.fromisoformat(visible[0]) <= anniversary else "<2y"
            short_count += span == "<2y"
            self.assertIn(f"| {sample['sample_id']} | {visible[0]} | {sample['cutoff_date']} | {len(visible)} | {span} |", content)
        self.assertEqual(short_count, 7)

    def test_calendar_anniversary_handles_leap_day(self):
        self.assertEqual(subtract_calendar_years(date(2024, 2, 29), 2), date(2022, 2, 28))
        self.assertEqual(subtract_calendar_years(date(2025, 2, 28), 2), date(2023, 2, 28))
        self.assertEqual(subtract_calendar_years(date(2024, 3, 1), 2), date(2022, 3, 1))

    def test_readme_inventory_exactly_matches_manifest_and_disk(self):
        manifest_pngs = {sample["chart_file"] for sample in self.manifest["samples"]}
        readme_pngs = set(PNG_TOKEN_RE.findall(read(README_PATH)))
        disk_pngs = {path.name for path in COHORT_ROOT.glob("*.png")}
        self.assertEqual(readme_pngs, manifest_pngs)
        self.assertEqual(disk_pngs, manifest_pngs)

    def test_audit_preserves_research_and_statistics_boundaries(self):
        content = read(AUDIT_PATH)
        for token in (
            "candidate_answer_status: isolated_not_ground_truth",
            "main_agent_review_status: knowledge_contaminated_descriptive_only",
            "expert_adjudication: pending",
            "conclusion: no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, content)

    def test_audit_discloses_calendar_limit_and_prior_cohort_reuse(self):
        content = read(AUDIT_PATH)
        self.assertIn("daily_context_window: <2y", content)
        self.assertNotIn("daily_context_window: >=2y", content)
        selection_path = COHORT_ROOT.parent / "selection_quality_blind_batch1" / "manifest.json"
        selection_manifest = json.loads(read(selection_path))
        selection = selection_manifest["samples"]
        candidate_window = self.manifest["daily_chart_bars"]
        selection_window = selection_manifest["daily_chart_bars"]
        overlap = [
            (candidate["sample_id"], prior["sample_id"])
            for candidate in self.manifest["samples"]
            for prior in selection
            if source_window_key(candidate, candidate_window) == source_window_key(prior, selection_window)
        ]
        self.assertEqual(len(overlap), 7)
        for candidate_id, prior_id in overlap:
            self.assertIn(f"| {candidate_id} | {prior_id} |", content)
        self.assertIn("不能算作新增独立样本", content)


if __name__ == "__main__":
    unittest.main()

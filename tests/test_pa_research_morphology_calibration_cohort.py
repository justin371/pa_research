import csv
import json
from pathlib import Path
import re
import unittest


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

    def test_every_cutoff_has_two_year_context_and_hidden_future(self):
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
                dates = [row["Date"] for row in rows]
                self.assertEqual(dates.count(sample["cutoff_date"]), 1)
                cutoff_index = dates.index(sample["cutoff_date"])
                self.assertGreaterEqual(cutoff_index + 1, minimum_context)
                self.assertGreaterEqual(len(rows) - cutoff_index - 1, minimum_future)

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


if __name__ == "__main__":
    unittest.main()

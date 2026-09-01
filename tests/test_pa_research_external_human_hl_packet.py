import hashlib
import json
from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = REPO_ROOT / "research" / "calibration" / "external_human_hl_v1"
MANIFEST_PATH = PACKET_ROOT / "manifest.json"
README_PATH = PACKET_ROOT / "README.md"
CRITERIA_PATH = PACKET_ROOT / "expert_criteria_CN.md"
FORM_PATH = PACKET_ROOT / "annotation_form.md"
EXPECTED_MANIFEST_SHA256 = "5b4d75981253cc8cc47fa6a40242fad1ef889bbd9db7f4912696d64d3b54675a"
SOURCE_MANIFESTS = (
    REPO_ROOT / "research/assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/manifest.json",
    REPO_ROOT / "research/assets/visual_recognition/2026-09-01/morphology_boundary_holdout_v1/manifest.json",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ExternalHumanHlPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read_json(MANIFEST_PATH)

    def test_manifest_is_frozen_label_outcome_and_future_hidden(self):
        self.assertEqual(hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(), EXPECTED_MANIFEST_SHA256)
        manifest = self.manifest
        self.assertEqual(manifest["evidence_role"], "external_human_annotation_packet_not_ground_truth_until_frozen")
        self.assertTrue(manifest["selection_frozen_before_external_review"])
        self.assertTrue(manifest["candidate_balance_hidden_from_expert"])
        self.assertTrue(manifest["source_hypotheses_isolated"])
        self.assertTrue(manifest["label_hidden"])
        self.assertTrue(manifest["outcome_hidden"])
        self.assertTrue(manifest["future_bars_hidden"])
        self.assertGreaterEqual(manifest["minimum_context_bars"], 500)
        self.assertGreaterEqual(manifest["minimum_hidden_future_bars"], 40)
        self.assertEqual(manifest["sample_count"], 16)

    def test_sixteen_neutral_samples_resolve_to_qualified_source_charts(self):
        samples = self.manifest["samples"]
        self.assertEqual([s["expert_sample_id"] for s in samples], [f"EH1-{n:03d}" for n in range(1, 17)])
        self.assertEqual(len({s["chart_path"] for s in samples}), 16)
        source_by_directory = {path.parent.resolve(): read_json(path) for path in SOURCE_MANIFESTS}
        for sample in samples:
            with self.subTest(sample=sample["expert_sample_id"]):
                self.assertEqual(set(sample), {"expert_sample_id", "chart_path"})
                chart = (REPO_ROOT / sample["chart_path"]).resolve()
                self.assertTrue(chart.is_file())
                self.assertGreater(chart.stat().st_size, 100_000)
                source = source_by_directory[chart.parent]
                self.assertGreaterEqual(source["minimum_context_bars"], 500)
                self.assertGreaterEqual(source["minimum_hidden_future_bars"], 40)
                self.assertTrue(source["label_hidden"])
                self.assertTrue(source["outcome_hidden"])
                self.assertTrue(source["future_bars_hidden"])
                self.assertIn(chart.name, {row["chart_file"] for row in source["samples"]})

    def test_expert_packet_does_not_expose_source_identity_or_hypothesis_mapping(self):
        combined = "\n".join(path.read_text(encoding="utf-8") for path in (README_PATH, CRITERIA_PATH, FORM_PATH))
        self.assertNotIn("curation_key", combined)
        for symbol in ("ROST", "MAR", "TSLA", "TOL", "RBLX", "CBOE", "MCHP", "VEEV", "COHR", "DDOG", "NDAQ"):
            self.assertIsNone(re.search(rf"(?<![A-Z0-9]){symbol}(?![A-Z0-9])", combined), symbol)
        for sample in self.manifest["samples"]:
            self.assertNotIn("symbol", sample)
            self.assertNotIn("cutoff_date", sample)
            self.assertNotIn("candidate_family", sample)
            self.assertNotIn("candidate_label", sample)
            self.assertNotIn("hypothesis", sample)
            self.assertNotIn("outcome", sample)

    def test_annotation_rows_are_blank_and_require_reasoned_evidence(self):
        form = FORM_PATH.read_text(encoding="utf-8")
        for sample_id in (f"EH1-{n:03d}" for n in range(1, 17)):
            row = next(line for line in form.splitlines() if line.startswith(f"| {sample_id} |"))
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            self.assertEqual(cells[0], sample_id)
            self.assertTrue(all(cell == "" for cell in cells[1:]), row)
        for token in (
            "major_high_low_reading",
            "A_leg_evidence",
            "B_leg_evidence",
            "lineage_and_attempt_evidence",
            "first_obstacle_and_space",
            "why_not_BOP_or_third_push_or_range_repeat",
            "source_or_model_hypotheses_seen_before_freeze",
            "future_or_outcome_evidence_seen_before_freeze",
        ):
            self.assertIn(token, form)

    def test_criteria_enforce_hl_precedence_and_hard_negative_reasons(self):
        criteria = CRITERIA_PATH.read_text(encoding="utf-8")
        for token in (
            "parent_state=open_trend",
            "EMA20/50",
            "连续 3–4 根饱满同向实体",
            "B leg 必须从属于 A",
            "lineage_status=same_lineage",
            "第三次必须转 H3/L3/三推",
            "accepted_BOP",
            "third_push_H3_L3",
            "range_repeat",
            "event_or_gap",
            "EMA_gate_fail",
            "insufficient_space",
            "confidence_1_to_5",
            "不是胜率",
        ):
            self.assertIn(token, criteria)

    def test_no_human_labels_or_accuracy_claim_exist_yet(self):
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("human_expert_status: not_performed", readme)
        self.assertIn("ground_truth_status: not_established", readme)
        self.assertIn("overall_accuracy: not-computable", readme)
        self.assertIn("validated win-rate: not-computable", readme)
        self.assertIn("conclusion: no-new-positive", readme)
        self.assertFalse((PACKET_ROOT / "expert_annotations.json").exists())
        self.assertFalse((PACKET_ROOT / "expert_annotations.csv").exists())
        self.assertIn(".codex/goals/", (REPO_ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_packet_preserves_repository_and_execution_boundaries(self):
        combined = README_PATH.read_text(encoding="utf-8") + CRITERIA_PATH.read_text(encoding="utf-8")
        for token in (
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no automatic pattern detector",
            "no Futu/OpenD",
            "no Execution Agent",
        ):
            self.assertIn(token, combined)


if __name__ == "__main__":
    unittest.main()

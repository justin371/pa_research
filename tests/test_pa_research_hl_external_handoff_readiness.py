import hashlib
import importlib.util
import json
from datetime import date
from pathlib import Path
import sys
import struct
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_ROOT = REPO_ROOT / "research" / "calibration" / "external_human_hl_v1"
MANIFEST_PATH = PACKET_ROOT / "manifest.json"
CHECKLIST_PATH = PACKET_ROOT / "coordinator_handoff_checklist_CN.md"
AUDIT_PATH = REPO_ROOT / "research" / "hl_external_human_handoff_readiness_audit_2026-09-01_CN.md"
RESEARCH_INDEX = REPO_ROOT / "research" / "README.md"
DOCS_VALIDATOR = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"
EXPECTED_MANIFEST_SHA256 = "d1616e568bceebbe605d498548ffc5c346cec1365831ba9035ab131ad9765b23"
CHART_HASH_PATH = PACKET_ROOT / "neutral_chart_sha256.json"
RENDERER_PATH = REPO_ROOT / "scripts" / "render_pa_blind_daily_batch.py"
EXPORTER_PATH = REPO_ROOT / "scripts" / "export_pa_hl_expert_packet.py"

SPEC = importlib.util.spec_from_file_location("hl_handoff_renderer", RENDERER_PATH)
RENDERER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = RENDERER
SPEC.loader.exec_module(RENDERER)

EXPORT_SPEC = importlib.util.spec_from_file_location("hl_handoff_exporter", EXPORTER_PATH)
EXPORTER = importlib.util.module_from_spec(EXPORT_SPEC)
assert EXPORT_SPEC.loader is not None
sys.modules[EXPORT_SPEC.name] = EXPORTER
EXPORT_SPEC.loader.exec_module(EXPORTER)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class HlExternalHandoffReadinessTests(unittest.TestCase):
    def test_identity_hidden_renderer_omits_symbol_and_calendar_date(self):
        last_bar = RENDERER.DailyBar("SECRET", date(2026, 9, 1), 1, 2, 0.5, 1.5, 100)
        title = RENDERER._chart_title("EH1-001", last_bar, 504, 120, identity_hidden=True)
        self.assertNotIn("SECRET", title)
        self.assertNotIn("2026-09-01", title)
        self.assertIn("identity and calendar date hidden", title)
        positions, labels = RENDERER._relative_tick_spec([last_bar] * 120)
        self.assertEqual(positions[-1], 119)
        self.assertEqual(labels[-1], "T0")
        self.assertTrue(all(label == "T0" or label.startswith("T-") for label in labels))

    def test_frozen_packet_is_exactly_sixteen_unique_existing_charts(self):
        manifest = json.loads(read(MANIFEST_PATH))
        self.assertEqual(hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(), EXPECTED_MANIFEST_SHA256)
        self.assertEqual(manifest["sample_count"], 16)
        self.assertTrue(manifest["identity_hidden"])
        self.assertTrue(manifest["calendar_dates_hidden"])
        self.assertEqual(
            [row["expert_sample_id"] for row in manifest["samples"]],
            [f"EH1-{index:03d}" for index in range(1, 17)],
        )
        chart_paths = [PACKET_ROOT / row["chart_path"] for row in manifest["samples"]]
        self.assertEqual(len({path.resolve() for path in chart_paths}), 16)
        self.assertTrue(all(path.is_file() for path in chart_paths))
        self.assertTrue(all(path.parent.resolve() == (PACKET_ROOT / "charts").resolve() for path in chart_paths))
        self.assertTrue(all(path.name == f"EH1-{index:03d}.png" for index, path in enumerate(chart_paths, 1)))
        chart_hashes = json.loads(read(CHART_HASH_PATH))
        expected = {row["expert_sample_id"]: row["chart_sha256"] for row in chart_hashes["charts"]}
        self.assertEqual(
            {path.stem: hashlib.sha256(path.read_bytes()).hexdigest() for path in chart_paths},
            expected,
        )
        for path in chart_paths:
            header = path.read_bytes()[:24]
            self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", header[16:24])
            self.assertGreaterEqual(width, 2000)
            self.assertGreaterEqual(height, 1200)

    def test_coordinator_checklist_has_a_closed_twenty_one_file_allowlist(self):
        checklist = read(CHECKLIST_PATH)
        for token in (
            "expert-facing allowlist: 21 files",
            "README.md",
            "expert_criteria_CN.md",
            "annotation_form.md",
            "annotation_schema_v1.json",
            "manifest.json",
            "16 张唯一截止图",
            "不要把整个 repo",
            "curation_key.json",
            "来源 cohort 的 manifest",
            "不能由模型推断或补齐空白",
            "export_pa_hl_expert_packet.py",
        ):
            self.assertIn(token, checklist, token)

    def test_safe_exporter_copies_exact_allowlist_and_refuses_nonempty_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "isolated_packet"
            report = EXPORTER.export_packet(REPO_ROOT, output)
            exported = sorted(path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file())
            expected = sorted(
                [*EXPORTER.DOCUMENT_ALLOWLIST]
                + [f"charts/EH1-{index:03d}.png" for index in range(1, 17)]
            )
            self.assertEqual(exported, expected)
            self.assertEqual(report["file_count"], 21)
            self.assertEqual(report["real_annotations_included"], 0)
            self.assertEqual(hashlib.sha256((output / "manifest.json").read_bytes()).hexdigest(), EXPECTED_MANIFEST_SHA256)
            self.assertFalse((output / "neutral_chart_sha256.json").exists())
            self.assertFalse((output / "coordinator_handoff_checklist_CN.md").exists())
            with self.assertRaises(FileExistsError):
                EXPORTER.export_packet(REPO_ROOT, output)

    def test_collection_ready_remaining_tooling_and_human_gate_are_not_conflated(self):
        combined = read(CHECKLIST_PATH) + read(AUDIT_PATH)
        for token in (
            "internal_packet_and_contract_work: complete",
            "collection_handoff_readiness: ready",
            "independent_agent_work_remaining_before_requesting_humans: none",
            "external_human_expert_A: not_started",
            "external_human_expert_B: not_started",
            "external_human_execution=not_started",
            "ground_truth_status: not_established",
            "overall accuracy: not-computable",
            "validated win-rate: not-computable",
            "conclusion: no-new-positive",
        ):
            self.assertIn(token, combined, token)

    def test_real_annotations_and_tracked_curation_keys_remain_absent(self):
        allowed_machine_contracts = {
            "annotation_schema_v1.json",
            "manifest.json",
            "neutral_chart_sha256.json",
            "pair_adjudication_schema_v1.json",
            "transcription_mapping_v1.json",
        }
        annotation_artifacts = [
            path
            for path in PACKET_ROOT.iterdir()
            if path.is_file()
            and path.suffix.lower() in {".json", ".csv"}
            and path.name not in allowed_machine_contracts
        ]
        self.assertEqual(annotation_artifacts, [])
        self.assertTrue((PACKET_ROOT / "pair_adjudication_schema_v1.json").is_file())
        self.assertTrue((PACKET_ROOT / "transcription_mapping_v1.json").is_file())
        tracked_scope_keys = [
            path
            for path in REPO_ROOT.rglob("curation_key.json")
            if ".codex" not in path.relative_to(REPO_ROOT).parts
        ]
        self.assertEqual(tracked_scope_keys, [])
        self.assertIn(".codex/goals/", read(REPO_ROOT / ".gitignore"))

    def test_audit_and_checklist_are_canonical_and_required(self):
        research_index = read(RESEARCH_INDEX)
        validator = read(DOCS_VALIDATOR)
        self.assertIn(AUDIT_PATH.name, research_index)
        self.assertIn("calibration/external_human_hl_v1/coordinator_handoff_checklist_CN.md", read(AUDIT_PATH))
        for relative_path in (
            "research/calibration/external_human_hl_v1/coordinator_handoff_checklist_CN.md",
            "research/calibration/external_human_hl_v1/neutral_chart_sha256.json",
            "research/hl_external_human_handoff_readiness_audit_2026-09-01_CN.md",
            "scripts/export_pa_hl_expert_packet.py",
        ):
            self.assertIn(relative_path, validator)

    def test_scope_and_statistics_boundaries_are_explicit(self):
        combined = read(CHECKLIST_PATH) + read(AUDIT_PATH)
        for token in (
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no automatic pattern detector",
            "no Futu/OpenD",
            "no Execution Agent",
            "completed_trade_denominator: 0",
        ):
            self.assertIn(token, combined, token)


if __name__ == "__main__":
    unittest.main()

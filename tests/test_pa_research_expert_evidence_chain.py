"""Synthetic regressions for frozen packet identity and export integrity."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = runpy.run_path(str(ROOT / "tests/test_pa_research_hl_pair_adjudication_validator.py"))
PAIR = FIXTURES["VALIDATOR"]
SINGLE = PAIR.SINGLE_VALIDATOR
COMPARATOR = PAIR.COMPARATOR
EXPORTER = runpy.run_path(str(ROOT / "scripts/export_pa_hl_expert_packet.py"))
PACKET = EXPORTER["PACKET_RELATIVE"]


class ExpertEvidenceChainTests(unittest.TestCase):
    class SequencedSource:
        """Path-like test double that can change between filesystem reads."""

        def __init__(self, label, *, byte_versions, text_versions=None):
            self.label = label
            self.byte_versions = list(byte_versions)
            self.text_versions = list(text_versions or [])
            self.read_count = 0

        @staticmethod
        def _next(versions):
            if len(versions) > 1:
                return versions.pop(0)
            return versions[0]

        def read_bytes(self):
            self.read_count += 1
            return self._next(self.byte_versions)

        def read_text(self, encoding="utf-8"):
            self.read_count += 1
            if self.text_versions:
                return self._next(self.text_versions)
            return self._next(self.byte_versions).decode(encoding)

        def __str__(self):
            return self.label

    def test_integrity_export_does_not_authorize_expert_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            report = EXPORTER["export_packet"](ROOT, Path(directory) / "out")
        self.assertEqual(report["status"], "integrity_verified_handoff_blocked")
        self.assertTrue(report["integrity_verified"])
        self.assertFalse(report["human_handoff_ready"])
        self.assertFalse(report["accuracy_study_ready"])
        self.assertEqual(
            set(report["handoff_blockers"]),
            {"independent_pre_reveal_commitment", "cross_sample_future_exposure"},
        )

    def test_export_cli_success_only_means_integrity_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            with contextlib.redirect_stdout(io.StringIO()) as stream:
                code = EXPORTER["main"](["--repo-root", str(ROOT), "--output-dir", str(Path(directory) / "out")])
        self.assertEqual(code, 0)
        report = json.loads(stream.getvalue())
        self.assertFalse(report["human_handoff_ready"])
        self.assertEqual(report["file_count"], 21)

    def test_replaced_manifest_cannot_pass_any_public_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.json"
            original = json.loads(FIXTURES["MANIFEST_PATH"].read_text(encoding="utf-8"))
            original["packet_id"] = "synthetic-noncanonical-packet"
            manifest.write_text(json.dumps(original), encoding="utf-8")
            digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
            experts = []
            for identifier in ("synthetic-a", "synthetic-b"):
                document = FIXTURES["clean_expert_document"](identifier)
                target = root / (identifier + ".json")
                target.write_text(json.dumps(document), encoding="utf-8")
                experts.append(target)
            adjudication = root / "adjudication.json"
            record = FIXTURES["build_adjudication"](*experts)
            record.update(packet_id=original["packet_id"], manifest_sha256=digest)
            for role, target in zip(("expert_a", "expert_b"), experts):
                document = json.loads(target.read_text(encoding="utf-8"))
                document.update(packet_id=original["packet_id"], manifest_sha256=digest)
                target.write_text(json.dumps(document), encoding="utf-8")
                record["expert_pair"][role]["record_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            adjudication.write_text(json.dumps(record), encoding="utf-8")
            invocations = (
                (SINGLE.main, ["--manifest", str(manifest), "--annotations", str(experts[0])]),
                (COMPARATOR.main, ["--manifest", str(manifest), "--expert-a", str(experts[0]), "--expert-b", str(experts[1])]),
                (PAIR.main, ["--manifest", str(manifest), "--expert-a", str(experts[0]), "--expert-b", str(experts[1]), "--adjudication", str(adjudication)]),
            )
            for entry, arguments in invocations:
                with self.subTest(entry=entry.__module__):
                    with contextlib.redirect_stdout(io.StringIO()) as stream:
                        code = entry(arguments)
                    self.assertEqual(code, 1)
                    result = json.loads(stream.getvalue())
                    self.assertEqual(result["status"], "invalid")
                    self.assertIn("frozen", json.dumps(result))

    def packet_copy(self, root):
        target = root / PACKET
        shutil.copytree(ROOT / PACKET, target)
        return target

    def test_prefilled_form_and_altered_criteria_are_not_exportable(self):
        for name in ("annotation_form.md", "expert_criteria_CN.md", "README.md", "annotation_schema_v1.json"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                packet = self.packet_copy(root)
                source = packet / name
                source.write_bytes(source.read_bytes() + b"\nMODEL_ANSWER EH1-001=H1\n")
                with self.assertRaisesRegex(ValueError, "frozen"):
                    EXPORTER["export_packet"](root, root / "out")
                self.assertFalse((root / "out").exists())

    def test_chart_and_matching_hash_inventory_replacement_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = self.packet_copy(root)
            replacement = (packet / "charts/EH1-002.png").read_bytes()
            (packet / "charts/EH1-001.png").write_bytes(replacement)
            inventory_path = packet / "neutral_chart_sha256.json"
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
            for row in inventory["charts"]:
                if row["expert_sample_id"] == "EH1-001":
                    row["chart_sha256"] = hashlib.sha256(replacement).hexdigest()
            inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frozen"):
                EXPORTER["export_packet"](root, root / "out")
            self.assertFalse((root / "out").exists())

    def test_copy_time_content_change_never_returns_ready(self):
        copy2 = shutil.copy2

        def altered_copy(source, destination):
            copied = copy2(source, destination)
            if Path(destination).name == "annotation_form.md":
                Path(destination).write_bytes(b"MODEL_ANSWER EH1-001=H1")
            return copied

        with tempfile.TemporaryDirectory() as directory, patch.object(shutil, "copy2", altered_copy):
            with self.assertRaisesRegex((ValueError, RuntimeError), "frozen|hash"):
                EXPORTER["export_packet"](ROOT, Path(directory) / "out")

    def test_export_rejects_destination_inside_frozen_source_packet(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet = self.packet_copy(root)
            destination = packet / "nested-export"
            with self.assertRaisesRegex(ValueError, "inside the frozen source packet"):
                EXPORTER["export_packet"](root, destination)
            self.assertFalse(destination.exists())

    def test_copy_failure_does_not_publish_partial_packet(self):
        copy2 = shutil.copy2
        calls = 0

        def fail_after_first_copy(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic copy failure")
            return copy2(source, destination)

        with tempfile.TemporaryDirectory() as directory, patch.object(shutil, "copy2", fail_after_first_copy):
            destination = Path(directory) / "out"
            with self.assertRaisesRegex(OSError, "synthetic"):
                EXPORTER["export_packet"](ROOT, destination)
            self.assertFalse(destination.exists())

    def test_single_record_manifest_parse_and_hash_share_one_snapshot(self):
        canonical = FIXTURES["MANIFEST_PATH"].read_bytes()
        tampered_document = json.loads(canonical.decode("utf-8"))
        tampered_document["packet_id"] = "switched-after-parse"
        tampered = json.dumps(tampered_document).encode("utf-8")
        manifest = self.SequencedSource(
            "synthetic-changing-manifest.json",
            byte_versions=[canonical, tampered],
        )
        with tempfile.TemporaryDirectory() as directory:
            annotations = Path(directory) / "annotations.json"
            annotations.write_text(
                json.dumps(FIXTURES["clean_expert_document"]("synthetic-a")),
                encoding="utf-8",
            )
            report = SINGLE.validate(manifest, annotations)
        self.assertEqual(report["status"], "clean_eligible")
        self.assertEqual(report["manifest_sha256"], hashlib.sha256(canonical).hexdigest())
        self.assertEqual(manifest.read_count, 1)

    def test_pair_comparison_uses_the_validated_expert_snapshot(self):
        canonical_document = FIXTURES["clean_expert_document"]("synthetic-a")
        tampered_document = json.loads(json.dumps(canonical_document))
        tampered_document["annotations"][0]["main_uncertainty"] = "switched after validation"
        canonical_text = json.dumps(canonical_document)
        tampered_text = json.dumps(tampered_document)
        expert_a = self.SequencedSource(
            "synthetic-changing-expert-a.json",
            byte_versions=[canonical_text.encode("utf-8")],
            text_versions=[canonical_text, tampered_text],
        )
        with tempfile.TemporaryDirectory() as directory:
            expert_b = Path(directory) / "expert-b.json"
            expert_b.write_text(
                json.dumps(FIXTURES["clean_expert_document"]("synthetic-b")),
                encoding="utf-8",
            )
            report = COMPARATOR.compare(FIXTURES["MANIFEST_PATH"], expert_a, expert_b)
        self.assertEqual(report["status"], "comparison_ready")
        self.assertEqual(report["summary"]["exact_all_field_agreement_count"], 16)
        self.assertEqual(expert_a.read_count, 1)

    def test_pair_adjudication_reads_each_input_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expert_a_path = root / "expert-a.json"
            expert_b_path = root / "expert-b.json"
            adjudication_path = root / "adjudication.json"
            expert_a_path.write_text(
                json.dumps(FIXTURES["clean_expert_document"]("synthetic-a")),
                encoding="utf-8",
            )
            expert_b_path.write_text(
                json.dumps(FIXTURES["clean_expert_document"]("synthetic-b")),
                encoding="utf-8",
            )
            adjudication_path.write_text(
                json.dumps(FIXTURES["build_adjudication"](expert_a_path, expert_b_path)),
                encoding="utf-8",
            )
            sources = [
                self.SequencedSource(
                    str(path),
                    byte_versions=[path.read_bytes()],
                )
                for path in (
                    FIXTURES["MANIFEST_PATH"],
                    expert_a_path,
                    expert_b_path,
                    adjudication_path,
                )
            ]
            report = PAIR.validate(*sources)
        self.assertEqual(report["status"], "valid")
        self.assertEqual([source.read_count for source in sources], [1, 1, 1, 1])


if __name__ == "__main__":
    unittest.main()

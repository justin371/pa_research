import csv
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
CALIBRATION_ROOT = ROOT / "research" / "calibration" / "external_human_hl_v1"


def _load_script_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ANNOTATION_VALIDATOR = _load_script_module(
    "full_review_annotation_validator",
    ROOT / "scripts" / "validate_pa_hl_expert_annotations.py",
)
PAIR_VALIDATOR = _load_script_module(
    "full_review_pair_validator",
    ROOT / "scripts" / "validate_pa_hl_expert_pair_adjudication.py",
)
RENDERER = _load_script_module(
    "full_review_daily_renderer",
    ROOT / "scripts" / "render_pa_blind_daily_batch.py",
)
EXPORTER = _load_script_module(
    "full_review_packet_exporter",
    ROOT / "scripts" / "export_pa_hl_expert_packet.py",
)


def _manifest_ids(manifest_path: Path) -> list[str]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [
        row["expert_sample_id"]
        for row in manifest["samples"]
        if isinstance(row, dict) and isinstance(row.get("expert_sample_id"), str)
    ]


def _annotation_row(sample_id: str, *, label: str = "H1", direction: str = "long") -> dict:
    rising = direction == "long"
    return {
        "expert_sample_id": sample_id,
        "evidence_usable": "yes",
        "parent_state": "open_trend",
        "direction": direction,
        "ema20_slope": "rising" if rising else "falling",
        "ema50_slope": "rising" if rising else "falling",
        "ema200_context": "supportive",
        "A_leg_quality": "strong",
        "B_leg_class": "controlled",
        "lineage_status": "same_lineage",
        "expert_ordinary_hl_label": label,
        "primary_exclusion": "not_applicable",
        "confidence_1_to_5": 4,
        "major_high_low_reading": "major structure is readable",
        "A_leg_evidence": "directional A leg is visible",
        "B_leg_evidence": "controlled B leg is visible",
        "lineage_and_attempt_evidence": "same-lineage attempt is visible",
        "first_obstacle_and_space": "first obstacle and space are recorded",
        "why_not_BOP_or_third_push_or_range_repeat": "not a breakout or third-push repeat",
        "main_uncertainty": "minor bar-level uncertainty only",
    }


def _annotation_document(manifest_path: Path, identifier: str, *, first_row: dict | None = None) -> dict:
    rows = [_annotation_row(sample_id) for sample_id in _manifest_ids(manifest_path)]
    if first_row is not None:
        rows[0] = first_row
    return {
        "schema_version": "pa_hl_expert_annotations_v1",
        "packet_id": json.loads(manifest_path.read_text(encoding="utf-8"))["packet_id"],
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "annotator": {
            "role": "external_human_expert",
            "identifier": identifier,
            "independent": True,
        },
        "freeze": {
            "annotation_started_at": "2026-09-01T00:00:00+00:00",
            "annotation_frozen_at": "2026-09-01T01:00:00+00:00",
            "source_or_model_hypotheses_seen_before_freeze": False,
            "future_or_outcome_evidence_seen_before_freeze": False,
            "knowledge_status": "clean",
        },
        "annotations": rows,
    }


def _write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def _source_identity(path: Path, identifier: str) -> dict:
    return {
        "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "annotator_identifier": identifier,
        "single_record_validator_status": "clean_eligible",
    }


def _pair_document(
    manifest_path: Path,
    expert_a_path: Path,
    expert_b_path: Path,
    *,
    boundary_first: bool,
) -> dict:
    comparison_report = PAIR_VALIDATOR.COMPARATOR.compare(
        manifest_path, expert_a_path, expert_b_path
    )
    expert_a = json.loads(expert_a_path.read_text(encoding="utf-8"))
    expert_b = json.loads(expert_b_path.read_text(encoding="utf-8"))
    rows_a = {row["expert_sample_id"]: row for row in expert_a["annotations"]}
    rows_b = {row["expert_sample_id"]: row for row in expert_b["annotations"]}
    comparisons = {
        row["expert_sample_id"]: row for row in comparison_report["sample_comparisons"]
    }
    samples = []
    excluded_reasons: dict[str, int] = {}
    for index, sample_id in enumerate(_manifest_ids(manifest_path)):
        comparison = comparisons[sample_id]
        is_boundary = boundary_first and index == 0
        state = "both_reasonable_boundary" if is_boundary else "experts_agree"
        final_label = None if is_boundary else rows_a[sample_id]["expert_ordinary_hl_label"]
        excluded_reason = "boundary_or_unclear" if is_boundary else "model_prediction_missing"
        excluded_reasons[excluded_reason] = excluded_reasons.get(excluded_reason, 0) + 1
        samples.append(
            {
                "expert_sample_id": sample_id,
                "expert_a": {
                    key: rows_a[sample_id][key]
                    for key in ("expert_ordinary_hl_label", "primary_exclusion", "evidence_usable")
                },
                "expert_b": {
                    key: rows_b[sample_id][key]
                    for key in ("expert_ordinary_hl_label", "primary_exclusion", "evidence_usable")
                },
                "comparison": {
                    "label_and_exclusion_agree": comparison["label_and_exclusion_agree"],
                    "disagreement_fields": comparison["disagreement_fields"],
                },
                "adjudication_state": state,
                "adjudicator": None,
                "final_label": final_label,
                "rationale": "Frozen rationale for this synthetic regression record.",
                "accuracy_eligibility": {
                    "model_prediction_frozen_before_expert_reveal": False,
                    "model_prediction_label": None,
                    "eligible": False,
                    "excluded_reason": excluded_reason,
                },
            }
        )
    summary = {
        "packet_total": 16,
        "clean_expert_pair_count": 16,
        "adjudicated_single_label_count": 15 if boundary_first else 16,
        "boundary_or_unclear_count": 1 if boundary_first else 0,
        "contaminated_count": 0,
        "model_prediction_coverage": 0,
        "accuracy_denominator": 0,
        "excluded_reasons": excluded_reasons,
        "completed_trade_denominator": 0,
        "validated_win_rate": "not-computable",
        "conclusion": "no-new-positive",
    }
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return {
        "schema_version": "pa_hl_expert_pair_adjudication_v1",
        "packet_id": manifest["packet_id"],
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "expert_pair": {
            "expert_a": _source_identity(expert_a_path, "expert-a"),
            "expert_b": _source_identity(expert_b_path, "expert-b"),
            "distinct_identifiers": True,
        },
        "adjudication_freeze": {
            "comparison_frozen_at": "2026-09-01T02:00:00+00:00",
            "adjudication_started_at": "2026-09-01T03:00:00+00:00",
            "adjudication_frozen_at": "2026-09-01T04:00:00+00:00",
            "source_or_model_hypotheses_seen_before_freeze": False,
            "future_or_outcome_evidence_seen_before_freeze": False,
            "knowledge_status": "clean",
        },
        "samples": samples,
        "summary": summary,
    }


class FullReviewInputRegressionTests(unittest.TestCase):
    def test_valid_annotation_and_wrong_enum_types_are_structured_invalid(self):
        manifest_path = CALIBRATION_ROOT / "manifest.json"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_copy = root / "manifest.json"
            manifest_copy.write_bytes(manifest_path.read_bytes())
            unclear_row = _annotation_row("EH1-001", label="unclear", direction="no_valid_direction")
            unclear_row.update(
                {
                    "evidence_usable": "uncertain",
                    "parent_state": "unclear",
                    "ema20_slope": "unclear",
                    "ema50_slope": "unclear",
                    "ema200_context": "unclear",
                    "A_leg_quality": "unclear",
                    "B_leg_class": "unclear",
                    "lineage_status": "unclear",
                    "primary_exclusion": "insufficient_evidence",
                }
            )
            unusable_row = _annotation_row("EH1-001", label="not_ordinary_HL", direction="no_valid_direction")
            unusable_row.update(
                {
                    "evidence_usable": "no",
                    "parent_state": "unclear",
                    "ema20_slope": "unclear",
                    "ema50_slope": "unclear",
                    "ema200_context": "unclear",
                    "A_leg_quality": "unclear",
                    "B_leg_class": "unclear",
                    "lineage_status": "unclear",
                    "primary_exclusion": "insufficient_evidence",
                }
            )
            documents = {
                "valid-h1": _annotation_document(manifest_copy, "expert-a"),
                "unclear": _annotation_document(manifest_copy, "expert-a", first_row=unclear_row),
                "evidence-no": _annotation_document(manifest_copy, "expert-a", first_row=unusable_row),
            }
            bad_json_types = ([], {}, True, 1, None)
            for variant, document in documents.items():
                valid_path = root / f"valid-{variant}.json"
                _write_json(valid_path, document)
                with self.subTest(variant=variant, positive=True):
                    self.assertEqual(
                        ANNOTATION_VALIDATOR.validate(manifest_copy, valid_path)["status"],
                        "clean_eligible",
                    )
                for field in ANNOTATION_VALIDATOR.ENUMS:
                    for bad_index, bad_value in enumerate(bad_json_types):
                        with self.subTest(variant=variant, field=field, bad_index=bad_index):
                            mutated = deepcopy(document)
                            mutated["annotations"][0][field] = bad_value
                            bad_path = root / f"bad-{variant}-{field}-{bad_index}.json"
                            _write_json(bad_path, mutated)
                            report = ANNOTATION_VALIDATOR.validate(manifest_copy, bad_path)
                            self.assertEqual(report["status"], "invalid")
                            self.assertTrue(report["errors"])

    def test_annotation_unknown_fields_and_missing_manifest_identity_are_rejected(self):
        manifest_path = CALIBRATION_ROOT / "manifest.json"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_copy = root / "manifest.json"
            manifest_copy.write_bytes(manifest_path.read_bytes())
            document = _annotation_document(manifest_copy, "expert-a")

            root_extra = json.loads(json.dumps(document))
            root_extra["unexpected"] = True
            root_extra_path = root / "root-extra.json"
            _write_json(root_extra_path, root_extra)
            root_report = ANNOTATION_VALIDATOR.validate(manifest_copy, root_extra_path)
            self.assertEqual(root_report["status"], "invalid")
            self.assertTrue(any("unknown fields" in error for error in root_report["errors"]))

            row_extra = json.loads(json.dumps(document))
            row_extra["annotations"][0]["unexpected"] = True
            row_extra_path = root / "row-extra.json"
            _write_json(row_extra_path, row_extra)
            row_report = ANNOTATION_VALIDATOR.validate(manifest_copy, row_extra_path)
            self.assertEqual(row_report["status"], "invalid")
            self.assertTrue(any("unknown fields" in error for error in row_report["errors"]))

            for name, mutation in (
                ("missing-field-id-list", "missing"),
                ("extra-field-id-list", "extra"),
            ):
                malformed = deepcopy(document)
                malformed["annotations"][0]["expert_sample_id"] = []
                if mutation == "missing":
                    del malformed["annotations"][0]["main_uncertainty"]
                else:
                    malformed["annotations"][0]["unexpected"] = True
                malformed_path = root / f"{name}.json"
                _write_json(malformed_path, malformed)
                malformed_report = ANNOTATION_VALIDATOR.validate(manifest_copy, malformed_path)
                self.assertEqual(malformed_report["status"], "invalid")
                self.assertTrue(malformed_report["errors"])

            non_object = deepcopy(document)
            non_object["annotations"][0] = ["EH1-001"]
            non_object_path = root / "non-object-row.json"
            _write_json(non_object_path, non_object)
            non_object_report = ANNOTATION_VALIDATOR.validate(manifest_copy, non_object_path)
            self.assertEqual(non_object_report["status"], "invalid")
            self.assertTrue(non_object_report["errors"])

            broken_manifest = json.loads(manifest_copy.read_text(encoding="utf-8"))
            del broken_manifest["samples"][0]["expert_sample_id"]
            broken_manifest_path = root / "broken-manifest.json"
            _write_json(broken_manifest_path, broken_manifest)
            broken_document = _annotation_document(broken_manifest_path, "expert-a")
            broken_document_path = root / "broken-manifest-document.json"
            _write_json(broken_document_path, broken_document)
            broken_report = ANNOTATION_VALIDATOR.validate(
                broken_manifest_path, broken_document_path
            )
            self.assertEqual(broken_report["status"], "invalid")
            self.assertTrue(
                any("manifest.samples[0].expert_sample_id" in error for error in broken_report["errors"])
            )

    def test_boundary_requires_actual_label_or_exclusion_disagreement(self):
        manifest_path = CALIBRATION_ROOT / "manifest.json"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_copy = root / "manifest.json"
            manifest_copy.write_bytes(manifest_path.read_bytes())
            expert_a_path = root / "expert-a.json"
            expert_b_path = root / "expert-b.json"
            _write_json(expert_a_path, _annotation_document(manifest_copy, "expert-a"))
            _write_json(expert_b_path, _annotation_document(manifest_copy, "expert-b"))

            invalid_adjudication_path = root / "invalid-boundary.json"
            _write_json(
                invalid_adjudication_path,
                _pair_document(
                    manifest_copy,
                    expert_a_path,
                    expert_b_path,
                    boundary_first=True,
                ),
            )
            invalid_report = PAIR_VALIDATOR.validate(
                manifest_copy,
                expert_a_path,
                expert_b_path,
                invalid_adjudication_path,
            )
            self.assertEqual(invalid_report["status"], "invalid")
            self.assertTrue(
                any("requires label/exclusion disagreement" in error for error in invalid_report["errors"])
            )

            expert_b_document = _annotation_document(
                manifest_copy,
                "expert-b",
                first_row=_annotation_row("EH1-001", label="L1", direction="short"),
            )
            _write_json(expert_b_path, expert_b_document)
            valid_adjudication_path = root / "valid-boundary.json"
            _write_json(
                valid_adjudication_path,
                _pair_document(
                    manifest_copy,
                    expert_a_path,
                    expert_b_path,
                    boundary_first=True,
                ),
            )
            valid_report = PAIR_VALIDATOR.validate(
                manifest_copy,
                expert_a_path,
                expert_b_path,
                valid_adjudication_path,
            )
            self.assertEqual(valid_report["status"], "valid")

    def test_pair_wrong_enum_type_and_boolean_count_are_invalid_without_crashing(self):
        manifest_path = CALIBRATION_ROOT / "manifest.json"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_copy = root / "manifest.json"
            manifest_copy.write_bytes(manifest_path.read_bytes())
            expert_a_path = root / "expert-a.json"
            expert_b_path = root / "expert-b.json"
            _write_json(expert_a_path, _annotation_document(manifest_copy, "expert-a"))
            _write_json(expert_b_path, _annotation_document(manifest_copy, "expert-b"))
            base = _pair_document(
                manifest_copy,
                expert_a_path,
                expert_b_path,
                boundary_first=False,
            )

            bad_state = json.loads(json.dumps(base))
            bad_state["samples"][0]["adjudication_state"] = []
            bad_state_path = root / "bad-state.json"
            _write_json(bad_state_path, bad_state)
            state_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, bad_state_path
            )
            self.assertEqual(state_report["status"], "invalid")
            self.assertTrue(state_report["errors"])

            bad_count = json.loads(json.dumps(base))
            bad_count["summary"]["clean_expert_pair_count"] = True
            bad_count_path = root / "bad-count.json"
            _write_json(bad_count_path, bad_count)
            count_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, bad_count_path
            )
            self.assertEqual(count_report["status"], "invalid")
            self.assertTrue(
                any("clean_expert_pair_count must be a JSON integer" in error for error in count_report["errors"])
            )

            zero_count = deepcopy(base)
            zero_count["summary"]["accuracy_denominator"] = False
            zero_count_path = root / "bad-zero-count.json"
            _write_json(zero_count_path, zero_count)
            zero_count_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, zero_count_path
            )
            self.assertEqual(zero_count_report["status"], "invalid")
            self.assertTrue(
                any("accuracy_denominator must be a JSON integer" in error for error in zero_count_report["errors"])
            )

            integral_float = deepcopy(base)
            integral_float["summary"]["clean_expert_pair_count"] = 16.0
            integral_float["summary"]["excluded_reasons"]["model_prediction_missing"] = 16.0
            integral_float_path = root / "valid-integral-float-counts.json"
            _write_json(integral_float_path, integral_float)
            integral_float_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, integral_float_path
            )
            self.assertEqual(integral_float_report["status"], "valid", integral_float_report["errors"])

            expert_b_document = _annotation_document(
                manifest_copy,
                "expert-b",
                first_row=_annotation_row("EH1-001", label="L1", direction="short"),
            )
            _write_json(expert_b_path, expert_b_document)
            boundary = _pair_document(
                manifest_copy,
                expert_a_path,
                expert_b_path,
                boundary_first=True,
            )
            boundary_path = root / "valid-boundary-counts.json"
            _write_json(boundary_path, boundary)
            boundary_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, boundary_path
            )
            self.assertEqual(boundary_report["status"], "valid")

            bad_boundary_count = deepcopy(boundary)
            bad_boundary_count["summary"]["boundary_or_unclear_count"] = True
            bad_boundary_count_path = root / "bad-boundary-count.json"
            _write_json(bad_boundary_count_path, bad_boundary_count)
            bad_boundary_count_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, bad_boundary_count_path
            )
            self.assertEqual(bad_boundary_count_report["status"], "invalid")
            self.assertTrue(
                any(
                    "boundary_or_unclear_count must be a JSON integer" in error
                    for error in bad_boundary_count_report["errors"]
                )
            )

            frozen_predictions = deepcopy(boundary)
            for sample in frozen_predictions["samples"][1:]:
                model_label = sample["final_label"]
                sample["accuracy_eligibility"].update(
                    {
                        "model_prediction_frozen_before_expert_reveal": True,
                        "model_prediction_label": model_label,
                        "eligible": True,
                        "excluded_reason": None,
                    }
                )
            frozen_predictions["summary"].update(
                {
                    "model_prediction_coverage": 15,
                    "accuracy_denominator": 15,
                    "excluded_reasons": {"boundary_or_unclear": 1},
                }
            )
            frozen_predictions_path = root / "valid-zero-model-missing-reason.json"
            _write_json(frozen_predictions_path, frozen_predictions)
            frozen_predictions_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, frozen_predictions_path
            )
            self.assertEqual(frozen_predictions_report["status"], "valid")

            bad_zero_reason = deepcopy(frozen_predictions)
            bad_zero_reason["summary"]["excluded_reasons"]["model_prediction_missing"] = False
            bad_zero_reason_path = root / "bad-zero-model-missing-reason.json"
            _write_json(bad_zero_reason_path, bad_zero_reason)
            bad_zero_reason_report = PAIR_VALIDATOR.validate(
                manifest_copy, expert_a_path, expert_b_path, bad_zero_reason_path
            )
            self.assertEqual(bad_zero_reason_report["status"], "invalid")
            self.assertTrue(
                any(
                    "summary.excluded_reasons['model_prediction_missing'] must be a non-negative JSON integer" in error
                    for error in bad_zero_reason_report["errors"]
                )
            )

    def test_renderer_accepts_positive_ohlcv_and_rejects_nonpositive_price_or_negative_volume(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            price_path = root / "prices.csv"
            fieldnames = ["Symbol", "Date", "Open", "High", "Low", "Close", "Volume"]

            def write_row(values: dict) -> None:
                with price_path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(values)

            positive = {
                "Symbol": "TEST",
                "Date": "2026-01-02",
                "Open": 10,
                "High": 11,
                "Low": 9,
                "Close": 10.5,
                "Volume": 0,
            }
            write_row(positive)
            bars = RENDERER.load_symbol_bars(price_path, "TEST")
            self.assertEqual(len(bars), 1)
            self.assertEqual(bars[0].volume, 0.0)

            for field, value in (("Open", -10), ("Low", 0), ("Volume", -1)):
                with self.subTest(field=field):
                    invalid = dict(positive)
                    invalid[field] = value
                    write_row(invalid)
                    with self.assertRaisesRegex(ValueError, "invalid OHLCV row"):
                        RENDERER.load_symbol_bars(price_path, "TEST")

    def test_exported_isolated_packet_has_only_resolving_local_markdown_links(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "expert-packet"
            report = EXPORTER.export_packet(ROOT, output_dir)
            self.assertEqual(report["status"], "ready_for_isolated_human_handoff")
            exported_files = sorted(
                path.relative_to(output_dir).as_posix()
                for path in output_dir.rglob("*")
                if path.is_file()
            )
            self.assertEqual(len(exported_files), 21)
            self.assertNotIn("adjudication_and_denominator_policy_CN.md", exported_files)
            self.assertNotIn("transcription_mapping_CN.md", exported_files)

            link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
            output_root = output_dir.resolve()
            for markdown_path in output_dir.rglob("*.md"):
                for raw_target in link_pattern.findall(markdown_path.read_text(encoding="utf-8")):
                    target = raw_target.strip().strip("<>")
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc or target.startswith("#"):
                        continue
                    relative_target = parsed.path
                    if not relative_target:
                        continue
                    resolved = (markdown_path.parent / Path(relative_target)).resolve()
                    self.assertTrue(
                        resolved.is_relative_to(output_root),
                        f"local link escapes export: {markdown_path} -> {target}",
                    )
                    self.assertTrue(
                        resolved.exists(),
                        f"broken local link in export: {markdown_path} -> {target}",
                    )


if __name__ == "__main__":
    unittest.main()

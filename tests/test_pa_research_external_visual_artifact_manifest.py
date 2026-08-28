import csv
import hashlib
import json
import re
import struct
from collections import Counter
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
MANIFEST_PATH = BACKTEST_ROOT / "external_visual_artifact_manifest_2026-08-29.json"
AUDIT_PATH = BACKTEST_ROOT / "external_visual_artifact_provenance_audit_2026-08-29_CN.md"
EXTERNAL_ROOT = Path.home() / ".codex" / "artifacts"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
DATE_RE = re.compile(r"_(\d{4}-\d{2}-\d{2})_")


def category_for(name):
    if "unannotated" in name:
        return "unannotated"
    if "candidate_review" in name:
        return "candidate_review"
    if "target_review" in name:
        return "target_review"
    if "local_review" in name:
        return "local_review"
    return "other"


def inventory_external_pngs(root):
    entries = []
    categories = Counter()
    dimensions = Counter()
    invalid = []
    for path in sorted(root.glob("*.png")):
        data = path.read_bytes()
        categories[category_for(path.name)] += 1
        if not data.startswith(PNG_SIGNATURE) or len(data) < 24:
            invalid.append(path.name)
            dimensions["invalid"] += 1
        else:
            width, height = struct.unpack(">II", data[16:24])
            dimensions[f"{width}x{height}"] += 1
        entries.append((path.name, hashlib.sha256(data).hexdigest(), path.stat().st_size))
    return {
        "entries": entries,
        "category_counts": dict(sorted(categories.items())),
        "dimension_counts": dict(sorted(dimensions.items())),
        "invalid_pngs": invalid,
        "total_bytes": sum(size for _, _, size in entries),
        "manifest_sha256": hashlib.sha256(
            "".join(f"{name}\t{digest}\t{size}\n" for name, digest, size in entries).encode()
        ).hexdigest(),
    }


def load_manifest():
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


class PaResearchExternalVisualArtifactManifestTests(unittest.TestCase):
    def test_manifest_is_logical_and_has_explicit_contract_mapping(self):
        raw = MANIFEST_PATH.read_text(encoding="utf-8")
        manifest = json.loads(raw)

        self.assertEqual(manifest["manifest_version"], 1)
        self.assertEqual(manifest["generated_on"], "2026-08-29")
        self.assertEqual(manifest["source_state"], "read_only_inventory_of_existing_local_artifacts")
        self.assertNotIn("C:\\Users\\", raw)
        self.assertNotIn("/Users/", raw)
        self.assertNotIn("/home/", raw)

        roots = {artifact["artifact_id"]: artifact for artifact in manifest["artifact_roots"]}
        self.assertEqual(set(roots), {"hl_next4", "hl_next5"})
        for artifact in roots.values():
            self.assertEqual(artifact["storage"], "external_local_artifact_not_in_checkout")
            self.assertEqual(artifact["scope"], "top_level_png_files_only")
            self.assertEqual(artifact["invalid_pngs"], [])
            names = artifact["png_files"]
            self.assertEqual(names, sorted(set(names)))
            self.assertTrue(all(name.lower().endswith(".png") for name in names))
            self.assertEqual(len(names), artifact["png_count"])
            self.assertEqual(sum(artifact["category_counts"].values()), artifact["png_count"])

        next4 = roots["hl_next4"]
        next5 = roots["hl_next5"]
        self.assertEqual(next4["png_count"], 114)
        self.assertEqual(next4["total_bytes"], 19313991)
        self.assertEqual(next4["manifest_sha256"], "cb562710981aad627efa90f91ad325a87ca94f230aa47ca975b772db7b3ee4c2")
        self.assertEqual(next5["png_count"], 78)
        self.assertEqual(next5["total_bytes"], 19025901)
        self.assertEqual(next5["manifest_sha256"], "ed9fc8f7a817e3749122745f2eec2f9d736b879b21f277faae65da7adfdf617a")

        next4_mapping = {row["sample_id"]: row for row in next4["contract_mappings"]}
        rost = next4_mapping["PA-HL-NEXT4-ROST-H1-20260107"]
        self.assertEqual(rost["status"], "missing_decision_date_asset")
        self.assertEqual(rost["decision_date_assets"], [])
        self.assertEqual(
            rost["nearest_post_decision_assets"],
            ["ROST_2026-01-08_candidate_review.png", "ROST_2026-01-13_candidate_review.png"],
        )
        self.assertEqual(
            next4_mapping["PA-HL-NEXT4-CBOE-H1-20250522"]["status"],
            "decision_date_match",
        )
        self.assertTrue(
            all(row["status"] == "decision_date_match" for row in next5["contract_mappings"])
        )

    def test_manifest_contract_mappings_match_current_contract_csvs(self):
        manifest = load_manifest()
        csv_by_artifact = {
            "hl_next4": "hl_next4_contracts_2026-08-27.csv",
            "hl_next5": "hl_next5_contracts_2026-08-27.csv",
        }
        for artifact in manifest["artifact_roots"]:
            with self.subTest(artifact=artifact["artifact_id"]):
                rows = []
                with (BACKTEST_ROOT / csv_by_artifact[artifact["artifact_id"]]).open(
                    encoding="utf-8", newline=""
                ) as handle:
                    rows = list(csv.DictReader(handle))
                mappings = {row["sample_id"]: row for row in artifact["contract_mappings"]}
                self.assertEqual(set(mappings), {row["sample_id"] for row in rows})
                for row in rows:
                    mapping = mappings[row["sample_id"]]
                    self.assertEqual(mapping["symbol"], row["symbol"])
                    self.assertEqual(mapping["decision_date"], row["decision_date"])
                    self.assertTrue(all("/" not in name and "\\" not in name for name in mapping["decision_date_assets"]))

    def test_external_inventory_reproduces_manifest_when_artifacts_are_available(self):
        manifest = load_manifest()
        unavailable = []
        for artifact in manifest["artifact_roots"]:
            root = EXTERNAL_ROOT / artifact["root_name"]
            if not root.is_dir():
                unavailable.append(artifact["root_name"])
                continue
            inventory = inventory_external_pngs(root)
            self.assertEqual([name for name, _, _ in inventory["entries"]], artifact["png_files"])
            self.assertEqual(inventory["total_bytes"], artifact["total_bytes"])
            self.assertEqual(inventory["category_counts"], artifact["category_counts"])
            self.assertEqual(inventory["dimension_counts"], artifact["dimension_counts"])
            self.assertEqual(inventory["invalid_pngs"], artifact["invalid_pngs"])
            self.assertEqual(inventory["manifest_sha256"], artifact["manifest_sha256"])
        if unavailable:
            self.skipTest("external artifact roots unavailable: " + ", ".join(unavailable))

    def test_audit_and_selection_records_disclose_the_rost_evidence_gap(self):
        report = AUDIT_PATH.read_text(encoding="utf-8")
        selection = (BACKTEST_ROOT / "hl_next4_selection_2026-08-27_CN.md").read_text(encoding="utf-8")
        replay = (BACKTEST_ROOT / "hl_next4_replay_2026-08-27_CN.md").read_text(encoding="utf-8")
        research_readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
        backtesting_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(encoding="utf-8")

        self.assertIn("missing_decision_date_asset", report)
        self.assertIn("PA-HL-NEXT4-ROST-H1-20260107", report)
        self.assertIn("ROST_2026-01-08_candidate_review.png", report)
        self.assertIn("post-decision", report)
        self.assertIn("external_visual_artifact_manifest_2026-08-29.json", report)
        self.assertIn("visual evidence", selection.lower())
        self.assertIn("external_visual_artifact_manifest_2026-08-29.json", selection)
        self.assertIn("ROST_2026-01-08_candidate_review.png", replay)
        self.assertIn("no-new-positive", report)
        self.assertIn("validated win-rate: not-computable", report)
        for content in (research_readme, backtesting_readme, validator):
            self.assertIn("external_visual_artifact_provenance_audit_2026-08-29_CN.md", content)


if __name__ == "__main__":
    unittest.main()

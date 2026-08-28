import csv
import re
import struct
from pathlib import Path
from urllib.parse import unquote
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = REPO_ROOT / "research" / "assets" / "visual_recognition"
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
VISUAL_AUDIT = BACKTEST_ROOT / "visual_asset_pre_entry_evidence_audit_2026-08-29_CN.md"

PNG_TOKEN_RE = re.compile(
    r"(?<![\w.-])([A-Za-z0-9][\w.-]*\.png)(?![\w.-])", re.IGNORECASE
)
MARKDOWN_LINK_RE = re.compile(r"\]\(([^)]+)\)")
OUTCOME_FIELD_RE = re.compile(
    r"(^|_)(?:result|outcome|realized|fill_status|win_rate|exit)(_|$)",
    re.IGNORECASE,
)

LOCAL_CONTRACT_COLLECTIONS = (
    (
        "2026-08-26/hl_contract_batch",
        "hl_contracts_2026-08-26.csv",
        "Daily_2y_cutoff",
        frozenset(),
    ),
    (
        "2026-08-26/hl_contract_batch2",
        "hl_contracts_batch2_2026-08-26.csv",
        "Daily_2y_cutoff",
        frozenset(),
    ),
    (
        "2026-08-27/hl_next_backtest",
        "hl_next_contracts_2026-08-27.csv",
        "decision_date",
        frozenset(),
    ),
    (
        "2026-08-27/hl_next2_backtest",
        "hl_next2_contracts_2026-08-27.csv",
        "decision_date",
        frozenset({"PHM_2023-05-31_boundary.png"}),
    ),
)

EXTERNAL_ONLY_BATCHES = (
    (
        "hl_next4_selection_2026-08-27_CN.md",
        "hl_next4_replay_2026-08-27_CN.md",
        "pa-research-hl-next4-20260827",
    ),
    (
        "hl_next5_selection_2026-08-27_CN.md",
        "hl_next5_replay_2026-08-27_CN.md",
        "pa-research-hl-next5-20260827",
    ),
)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def png_tokens(text):
    return set(PNG_TOKEN_RE.findall(text))


def local_png_links(readme):
    for match in MARKDOWN_LINK_RE.finditer(readme.read_text(encoding="utf-8")):
        target = match.group(1).strip().split()[0]
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")]
        target = unquote(target.split("#", 1)[0])
        if target.lower().endswith(".png") and "://" not in target:
            yield target


def assert_pre_entry_contract_fields(test_case, rows, source_name):
    test_case.assertTrue(rows, source_name)
    fields = set(rows[0])
    test_case.assertFalse(
        sorted(field for field in fields if OUTCOME_FIELD_RE.search(field)),
        f"outcome-like field leaked into frozen contract: {source_name}",
    )
    required_values = (
        "symbol",
        "decision_date",
        "direction",
        "primary_pattern",
        "internal_label",
        "label_source",
        "daily_context_window",
        "major_high_low_review",
        "ema20_50_200_review",
        "event_context",
        "contract_frozen",
        "lineage_id",
        "h_l_pullback_location",
        "meta_confluence",
    )
    for row in rows:
        for field in required_values:
            test_case.assertTrue(
                row.get(field, "").strip(),
                f"missing pre-entry field {field}: {source_name}/{row.get('sample_id', '')}",
            )
        test_case.assertEqual(row["contract_frozen"].strip().lower(), "yes")
        test_case.assertEqual(row["label_source"].strip(), "human_chart_review")
        test_case.assertEqual(row["daily_context_window"].strip(), ">=2y")
        test_case.assertEqual(row["major_high_low_review"].strip(), "complete")
        test_case.assertEqual(row["ema20_50_200_review"].strip(), "complete")
        if row.get("space_status", "").strip():
            test_case.assertTrue(row.get("pre_entry_space_R", "").strip())


class PaResearchVisualAssetConsistencyTests(unittest.TestCase):
    def test_every_local_visual_readme_covers_exact_png_inventory(self):
        readmes = sorted(ASSET_ROOT.rglob("README.md"))
        self.assertEqual(len(readmes), 11)

        for readme in readmes:
            with self.subTest(readme=readme.relative_to(ASSET_ROOT)):
                actual_paths = sorted(readme.parent.rglob("*.png"))
                actual_names = {path.name for path in actual_paths}
                content = readme.read_text(encoding="utf-8")
                listed_names = png_tokens(content)
                self.assertEqual(
                    actual_names - listed_names,
                    set(),
                    f"PNG asset is not in README manifest: {readme}",
                )
                self.assertEqual(
                    listed_names - actual_names,
                    set(),
                    f"README has stale PNG manifest entry: {readme}",
                )

                for target in local_png_links(readme):
                    target_path = (readme.parent / target).resolve()
                    self.assertTrue(
                        target_path.is_file() and target_path.suffix.lower() == ".png",
                        f"broken local PNG link: {readme} -> {target}",
                    )

        self.assertEqual(
            sum(1 for _ in ASSET_ROOT.rglob("*.png")),
            105,
        )

    def test_local_png_assets_have_valid_headers_and_dimensions(self):
        for path in sorted(ASSET_ROOT.rglob("*.png")):
            with self.subTest(path=path.relative_to(ASSET_ROOT)):
                data = path.read_bytes()
                self.assertGreater(len(data), 24)
                self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
                width, height = struct.unpack(">II", data[16:24])
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)

    def test_freeze_contracts_match_local_visual_cutoffs(self):
        for relative_dir, csv_name, naming, boundary_names in LOCAL_CONTRACT_COLLECTIONS:
            asset_dir = ASSET_ROOT / relative_dir
            rows = read_csv(BACKTEST_ROOT / csv_name)
            with self.subTest(collection=relative_dir):
                assert_pre_entry_contract_fields(self, rows, csv_name)
                actual_names = {path.name for path in asset_dir.glob("*.png")}
                expected_names = set(boundary_names)
                for row in rows:
                    if naming == "Daily_2y_cutoff":
                        expected_names.add(
                            f"{row['symbol']}_Daily_2y_cutoff_{row['decision_date']}.png"
                        )
                    else:
                        expected_names.add(f"{row['symbol']}_{row['decision_date']}.png")
                self.assertEqual(actual_names, expected_names)

                readme_text = (asset_dir / "README.md").read_text(encoding="utf-8")
                self.assertTrue(expected_names <= png_tokens(readme_text))

    def test_large_collection_preserves_window_to_contract_cardinality_boundary(self):
        asset_dir = ASSET_ROOT / "2026-08-27/hl_large_backtest"
        rows = read_csv(BACKTEST_ROOT / "hl_large_contracts_2026-08-27.csv")
        assert_pre_entry_contract_fields(self, rows, "hl_large_contracts_2026-08-27.csv")

        actual_names = {path.name for path in asset_dir.glob("*.png")}
        symbols = {row["symbol"] for row in rows}
        self.assertEqual(len(rows), 37)
        self.assertEqual(len(actual_names), 23)
        self.assertEqual(
            {name.split("_", 1)[0] for name in actual_names},
            symbols,
        )
        readme_text = (asset_dir / "README.md").read_text(encoding="utf-8")
        self.assertIn("23", readme_text)
        self.assertIn("局部序列", readme_text)

    def test_external_only_batches_are_explicitly_outside_checkout(self):
        for selection_name, replay_name, artifact_name in EXTERNAL_ONLY_BATCHES:
            with self.subTest(selection=selection_name):
                selection = (BACKTEST_ROOT / selection_name).read_text(encoding="utf-8")
                replay = (BACKTEST_ROOT / replay_name).read_text(encoding="utf-8")
                self.assertIn(f".codex\\artifacts\\{artifact_name}", selection)
                self.assertIn("外部审计目录", selection)
                self.assertIn("Matplotlib", selection)
                self.assertIn("图像", replay)

        self.assertFalse((ASSET_ROOT / "2026-08-27/hl_next4_backtest").exists())
        self.assertFalse((ASSET_ROOT / "2026-08-27/hl_next5_backtest").exists())

    def test_visual_audit_is_indexed_and_preserves_conclusion_boundary(self):
        report = VISUAL_AUDIT.read_text(encoding="utf-8")
        research_readme = (REPO_ROOT / "research" / "README.md").read_text(encoding="utf-8")
        backtesting_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")
        validator = (REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1").read_text(
            encoding="utf-8"
        )

        self.assertIn("视觉资产与事前证据边界审计", report)
        self.assertIn("105", report)
        self.assertIn("no-new-positive", report)
        self.assertIn("validated win-rate: not-computable", report)
        self.assertIn("外部审计目录", report)
        for content in (research_readme, backtesting_readme, validator):
            self.assertIn("visual_asset_pre_entry_evidence_audit_2026-08-29_CN.md", content)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
ASSET_ROOT = REPO_ROOT / "research" / "assets" / "visual_recognition"
AUDIT_PATH = BACKTEST_ROOT / "canonical_entry_cross_coverage_audit_2026-08-30_CN.md"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"

INDEX_PATHS = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "research" / "README.md",
    BACKTEST_ROOT / "README.md",
    REPO_ROOT / "patterns" / "README.md",
    REPO_ROOT / "foundations" / "README.md",
    REPO_ROOT / "strategy" / "README.md",
)

MARKDOWN_LINK_RE = re.compile(
    r"(?<!\!)\[[^\]]*\]\(([^)\r\n]+)\)|!\[[^\]]*\]\(([^)\r\n]+)\)"
)
PNG_TOKEN_RE = re.compile(
    r"(?<![\w.-])([A-Za-z0-9][\w.-]*\.png)(?![\w.-])", re.IGNORECASE
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def linked_paths(index_path: Path) -> set[str]:
    paths: set[str] = set()
    for match in MARKDOWN_LINK_RE.finditer(read(index_path)):
        target = (match.group(1) or match.group(2)).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = target.split("#", 1)[0].split("?", 1)[0].strip()
        if not target or re.match(r"(?i)^(?:[a-z][a-z0-9+.-]*:|//)", target):
            continue
        resolved = (index_path.parent / target).resolve()
        try:
            paths.add(resolved.relative_to(REPO_ROOT).as_posix())
        except ValueError:
            continue
    return paths


def canonical_index_linked_paths() -> set[str]:
    return set().union(*(linked_paths(path) for path in INDEX_PATHS))


def section_entry_paths() -> list[str]:
    paths = set()
    paths.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "docs").rglob("*.md")
    )
    paths.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "foundations").rglob("README.md")
    )
    paths.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "patterns").rglob("README.md")
    )
    paths.update(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "strategy").rglob("*.md")
    )
    return sorted(paths)


def backtesting_report_paths() -> list[str]:
    return sorted(
        f"research/backtesting/{path.name}"
        for path in BACKTEST_ROOT.glob("*.md")
        if path.name != "README.md"
    )


def asset_readme_paths() -> list[str]:
    return sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in ASSET_ROOT.rglob("README.md")
    )


class CanonicalEntryCrossCoverageTests(unittest.TestCase):
    def test_audit_declares_current_counts_and_policies(self):
        content = read(AUDIT_PATH)
        for token in (
            "inventory_scope: canonical_entry_cross_coverage_audit_only",
            "canonical_index_count: 7",
            "report_link_resolution: real_local_markdown_and_machine_target",
            "section_entry_policy: direct_canonical_for_active_sections",
            "research_root_policy: non_self_markdown_reachable",
            "asset_png_policy: README_manifest_exact_inventory",
            "template_inventory: Markdown_authority_cards_and_section_readmes",
            "docs_markdown_entries: 7",
            "foundations_readme_entries: 9",
            "patterns_readme_entries: 17",
            "strategy_markdown_entries: 7",
            "backtesting_reports: 76",
            "required_research_reports: 62",
            "visual_asset_readmes: 11",
            "png_assets: 105",
            "backtesting_csv: 18",
            "backtesting_json: 1",
            "backtesting_executable_entries: 3",
            "top_level_research_reports: 171",
            "canonical_direct_top_level: 55",
            "topical_only_top_level: 116",
            "all_top_level_research_reachable: yes",
            "current_docs_markdown_entries: 9",
            "current_section_entry_total: 42",
            "current_required_research_reports: 69",
            "current_visual_asset_readmes: 14",
            "current_png_assets: 145",
            "current_top_level_research_reports: 178",
            "current_missing_section_entries: 0",
        ):
            self.assertIn(token, content, token)

    def test_audit_is_required_and_indexed_everywhere(self):
        audit_name = AUDIT_PATH.name
        validator = read(VALIDATOR_PATH)
        for path in INDEX_PATHS:
            with self.subTest(index=path.relative_to(REPO_ROOT).as_posix()):
                self.assertTrue(path.is_file())
                self.assertIn(audit_name, read(path))
        self.assertIn(f"'research/backtesting/{audit_name}'", validator)

    def test_dynamic_report_section_and_asset_coverage_has_no_gap(self):
        indexed = canonical_index_linked_paths()
        self.assertEqual(
            [path for path in section_entry_paths() if path not in indexed], []
        )
        self.assertEqual(
            [path for path in backtesting_report_paths() if path not in indexed], []
        )
        self.assertEqual(
            [path for path in asset_readme_paths() if path not in indexed], []
        )
        self.assertEqual(len(section_entry_paths()), 42)
        self.assertEqual(len(backtesting_report_paths()), 76)
        self.assertEqual(len(asset_readme_paths()), 14)

    def test_visual_png_manifests_have_no_unlisted_assets(self):
        readmes = sorted(ASSET_ROOT.rglob("README.md"))
        self.assertEqual(len(readmes), 14)
        for readme in readmes:
            with self.subTest(asset=readme.relative_to(ASSET_ROOT).as_posix()):
                actual = {path.name for path in readme.parent.rglob("*.png")}
                listed = set(PNG_TOKEN_RE.findall(read(readme)))
                self.assertEqual(actual, listed)
        self.assertEqual(sum(len(list(readme.parent.rglob("*.png"))) for readme in readmes), 145)

    def test_audit_preserves_missing_zero_and_research_boundaries(self):
        content = read(AUDIT_PATH)
        for token in (
            "missing_backtesting_reports: 0",
            "missing_section_entries: 0",
            "missing_required_reports: 0",
            "missing_asset_readmes: 0",
            "missing_machine_artifacts: 0",
            "missing_executable_entries: 0",
            "png_manifest_gap: 0",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, content, token)


if __name__ == "__main__":
    unittest.main()

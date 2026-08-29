from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"
AUDIT_PATH = BACKTEST_ROOT / "required_report_index_coverage_audit_2026-08-29_CN.md"

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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def required_files_from_validator() -> list[str]:
    text = read(VALIDATOR_PATH)
    match = re.search(r"\$requiredFiles = @\((.*?)\)\r?\nforeach", text, re.S)
    if match is None:
        raise AssertionError("validator requiredFiles block is missing")
    return re.findall(r"'([^']+)'", match.group(1))


def required_research_reports() -> list[str]:
    return [
        path
        for path in required_files_from_validator()
        if (
            re.fullmatch(r"research/[^/]+\.md", path)
            or re.fullmatch(r"research/backtesting/[^/]+\.md", path)
        )
        and not path.endswith("/README.md")
    ]


def linked_paths(index_path: Path) -> set[str]:
    """Return repository-relative paths targeted by local Markdown links."""
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


def backtesting_report_paths() -> list[str]:
    return sorted(
        f"research/backtesting/{path.name}"
        for path in BACKTEST_ROOT.glob("*.md")
        if path.name != "README.md"
    )


class RequiredReportIndexCoverageTests(unittest.TestCase):
    def test_validator_declares_required_report_index_guard(self):
        text = read(VALIDATOR_PATH)
        self.assertIn("$canonicalResearchIndexRelativePaths", text)
        self.assertIn("$requiredResearchReportPaths", text)
        self.assertIn(
            "required research report is not referenced by a canonical index",
            text,
        )

    def test_all_required_research_reports_are_in_a_canonical_index(self):
        indexed_paths = canonical_index_linked_paths()
        missing = [
            path
            for path in required_research_reports()
            if path not in indexed_paths
        ]
        self.assertEqual(missing, [])

    def test_all_backtesting_reports_are_in_a_canonical_index(self):
        indexed_paths = canonical_index_linked_paths()
        report_paths = backtesting_report_paths()
        missing = [
            path
            for path in report_paths
            if path not in indexed_paths
        ]
        self.assertEqual(missing, [])

    def test_audit_is_indexed_and_preserves_scope(self):
        report = read(AUDIT_PATH)
        self.assertIn(AUDIT_PATH.name, read(REPO_ROOT / "docs" / "README.md"))
        self.assertIn(AUDIT_PATH.name, read(REPO_ROOT / "research" / "README.md"))
        self.assertIn(AUDIT_PATH.name, read(BACKTEST_ROOT / "README.md"))
        self.assertIn(AUDIT_PATH.name, read(REPO_ROOT / "strategy" / "README.md"))
        for token in (
            "85 个必需文件",
            "58 个是",
            "70 个是报告文件",
            "没有孤立报告",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, report, token)

    def test_audit_counts_match_the_current_validator_and_backtesting_inventory(self):
        report = read(AUDIT_PATH)
        required_files = required_files_from_validator()
        required_reports = required_research_reports()
        backtesting_reports = backtesting_report_paths()
        self.assertIn(
            f"`$requiredFiles` 当前包含 {len(required_files)} 个必需文件",
            report,
        )
        self.assertIn(
            f"其中 {len(required_reports)} 个是 `research/`",
            report,
        )
        self.assertIn(
            f"当前 `research/backtesting/` 有 {len(backtesting_reports) + 1} 个 Markdown 文件，其中 {len(backtesting_reports)} 个是报告文件",
            report,
        )


if __name__ == "__main__":
    unittest.main()

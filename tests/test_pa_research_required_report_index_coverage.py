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
        index_texts = [read(path) for path in INDEX_PATHS]
        missing = [
            path
            for path in required_research_reports()
            if not any(Path(path).name in content for content in index_texts)
        ]
        self.assertEqual(missing, [])

    def test_all_backtesting_reports_are_in_a_canonical_index(self):
        index_texts = [read(path) for path in INDEX_PATHS]
        report_paths = sorted(
            path
            for path in BACKTEST_ROOT.glob("*.md")
            if path.name != "README.md"
        )
        missing = [
            path.name
            for path in report_paths
            if not any(path.name in content for content in index_texts)
        ]
        self.assertEqual(missing, [])

    def test_audit_is_indexed_and_preserves_scope(self):
        report = read(AUDIT_PATH)
        self.assertIn(AUDIT_PATH.name, read(REPO_ROOT / "docs" / "README.md"))
        self.assertIn(AUDIT_PATH.name, read(REPO_ROOT / "research" / "README.md"))
        self.assertIn(AUDIT_PATH.name, read(BACKTEST_ROOT / "README.md"))
        self.assertIn(AUDIT_PATH.name, read(REPO_ROOT / "strategy" / "README.md"))
        for token in (
            "83 个必需文件",
            "56 个是",
            "68 个是报告文件",
            "没有孤立报告",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, report, token)


if __name__ == "__main__":
    unittest.main()

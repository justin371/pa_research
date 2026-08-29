"""Regression checks for PA Research conclusion and authorization wording."""

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"
AUDIT_NAME = "conclusion_boundary_consistency_audit_2026-08-29_CN.md"
CONTRACT_COVERAGE_NAME = "contract_coverage_audit_2026-08-28_CN.md"
CORE_BOUNDARY_INDEX_PATHS = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "patterns" / "README.md",
    REPO_ROOT / "research" / "README.md",
    REPO_ROOT / "strategy" / "README.md",
    REPO_ROOT / "research" / "backtesting" / "README.md",
)
CORE_BOUNDARY_TOKENS = (
    "PA Research only",
    "no-new-positive",
    "validated win-rate: not-computable",
    "60%",
    "不是 Codex Trading 生产规则",
    "量化扫描器",
    "Execution Agent",
)

LEGACY_STATUS_PATTERNS = (
    re.compile(r"(?m)^\s*validated_win_rate\s*:"),
    re.compile(r"(?m)^\s*win_rate\s*:\s*not-computable\s*$"),
)


def markdown_paths() -> list[Path]:
    paths = [REPO_ROOT / "README.md"]
    for root_name in ("docs", "research", "strategy"):
        paths.extend((REPO_ROOT / root_name).rglob("*.md"))
    return sorted(set(paths))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PaResearchConclusionBoundaryConsistencyTests(unittest.TestCase):
    def test_active_markdown_has_no_legacy_conclusion_status_lines(self):
        offenders = []
        for path in markdown_paths():
            text = read(path)
            if any(pattern.search(text) for pattern in LEGACY_STATUS_PATTERNS):
                offenders.append(path.relative_to(REPO_ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_contract_coverage_uses_canonical_boundary(self):
        text = read(BACKTEST_ROOT / CONTRACT_COVERAGE_NAME)
        self.assertIn("validated win-rate: not-computable", text)
        self.assertIn("conclusion: no-new-positive", text)
        self.assertNotRegex(text, LEGACY_STATUS_PATTERNS[0])
        self.assertNotRegex(text, LEGACY_STATUS_PATTERNS[1])
        for token in (
            "本文件只属于 PA Research",
            "不创建量化扫描器",
            "不连接 Execution Agent",
        ):
            self.assertIn(token, text)

    def test_validator_guards_legacy_status_and_canonical_reports(self):
        text = read(VALIDATOR_PATH)
        self.assertIn("$legacyConclusionStatusPatterns", text)
        self.assertIn("legacy non-canonical conclusion status", text)
        self.assertIn(CONTRACT_COVERAGE_NAME, text)
        self.assertIn(AUDIT_NAME, text)

    def test_audit_records_target_and_authorization_boundaries(self):
        text = read(BACKTEST_ROOT / AUDIT_NAME)
        for token in (
            "60% 的 23 个 Markdown 文件",
            "validated win-rate: not-computable",
            "conclusion: no-new-positive",
            "win_rate_eligible",
            "research_positive_conditional",
            "ready_for_system",
            "不修改 Codex Trading",
            "不创建量化扫描器",
            "不连接 Execution Agent",
        ):
            self.assertIn(token, text, token)

        for index_path in (
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "research" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "strategy" / "README.md",
        ):
            with self.subTest(index=index_path):
                self.assertIn(AUDIT_NAME, read(index_path))

    def test_core_boundary_indexes_share_version_and_conclusion_summary(self):
        for index_path in CORE_BOUNDARY_INDEX_PATHS:
            text = read(index_path)
            with self.subTest(index=index_path):
                for token in CORE_BOUNDARY_TOKENS:
                    self.assertIn(token, text)

        audit = read(BACKTEST_ROOT / AUDIT_NAME)
        for token in CORE_BOUNDARY_TOKENS:
            self.assertIn(token, audit)
        backtesting_readme = read(BACKTEST_ROOT / "README.md")
        self.assertIn("study_status", backtesting_readme)
        self.assertIn("统一统计结论", backtesting_readme)


if __name__ == "__main__":
    unittest.main()

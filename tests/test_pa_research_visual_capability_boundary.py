"""Regression checks for visual-recognition capability and provenance wording."""

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"
AUDIT_NAME = "visual_capability_boundary_audit_2026-08-29_CN.md"

HIGH_RISK_CAPABILITY_PHRASES = (
    "视觉工作版已经可以使用",
    "视觉识别已达到工作版",
    "可以稳定分辨",
    "能够稳定回答",
    "可以稳定找出",
    "目前可以稳定使用",
    "稳定判断顺序",
    "稳定阻止",
    "足以支持视觉助手当前工作版",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def visual_markdown_paths() -> list[Path]:
    paths = [REPO_ROOT / "README.md"]
    for root_name in ("docs", "research", "strategy"):
        paths.extend((REPO_ROOT / root_name).rglob("*.md"))
    return sorted(set(paths))


class PaResearchVisualCapabilityBoundaryTests(unittest.TestCase):
    def test_high_risk_capability_phrases_are_not_left_unqualified(self):
        offenders = []
        for path in visual_markdown_paths():
            text = read(path)
            for phrase in HIGH_RISK_CAPABILITY_PHRASES:
                if phrase in text:
                    offenders.append(f"{path.relative_to(REPO_ROOT).as_posix()}: {phrase}")
        self.assertEqual(offenders, [])

    def test_abc_capability_docs_state_the_research_only_qualification(self):
        expected = {
            "research/abc_visual_evidence_gap_audit_2026-08-24_CN.md": (
                "人工完整图表",
                "不是准确率测试",
                "自动识别器",
                "交易授权",
            ),
            "research/abc_research_status_v0_3_CN.md": (
                "按同一流程",
                "不是每张图都准确识别的保证",
                "自动扫描能力",
            ),
            "research/abc_pattern_coverage_audit_CN.md": (
                "现有案例中的视觉原则可复用",
                "研究范围内使用工作版字段",
            ),
        }
        for relative_path, tokens in expected.items():
            text = read(REPO_ROOT / relative_path)
            with self.subTest(path=relative_path):
                for token in tokens:
                    self.assertIn(token, text, token)

    def test_audit_records_capability_provenance_and_scope_boundaries(self):
        text = read(BACKTEST_ROOT / AUDIT_NAME)
        for token in (
            "human_chart_review / approximate_pattern_like_only",
            "validated win-rate: not-computable",
            "conclusion: no-new-positive",
            "daily_context_window: <2y / unavailable",
            "major_high_low_review",
            "ema20_50_200_review",
            "pattern_like",
            "research_positive_conditional",
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

    def test_validator_requires_the_visual_capability_audit(self):
        text = read(VALIDATOR_PATH)
        self.assertIn(AUDIT_NAME, text)
        self.assertIn("visual_capability: human_chart_review / approximate_pattern_like_only", read(BACKTEST_ROOT / AUDIT_NAME))


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
AUDIT_PATH = REPO_ROOT / "research" / "pattern_visual_preflight_audit_2026-08-29_CN.md"


PATTERN_DIRS = (
    "01_h1_l1_first_entry",
    "02_h2_l2_second_entry",
    "03_abc_continuation",
    "04_range_edge_second_entry",
    "05_failed_breakout_climax",
    "06_breakout_pullback_bop",
    "07_mtr_reversal",
    "08_three_push_h3_l3",
    "09_vcp_minervini",
    "10_final_flag",
    "11_opening_reversal",
    "12_channel",
    "13_inside_bar_two_bar_reversal",
    "14_triangle_expanding_range",
    "15_double_top_bottom",
    "16_head_shoulders_rounded",
)
CORE_DIRS = set(PATTERN_DIRS[:8])


def read(path):
    return path.read_text(encoding="utf-8")


class PatternVisualPreflightTests(unittest.TestCase):
    def test_every_pattern_readme_has_the_common_visual_preflight(self):
        for directory in PATTERN_DIRS:
            path = PATTERNS_ROOT / directory / "README.md"
            content = read(path)
            self.assertIn("../../docs/visual_pa_review_card_CN.md", content, directory)
            self.assertIn("至少两年的 Daily 左侧背景", content, directory)
            self.assertTrue("重要高点" in content or "主要高点" in content, directory)
            self.assertTrue("重要低点" in content or "主要低点" in content, directory)
            for token in ("支撑阻力", "EMA20/50/200", "pending"):
                self.assertIn(token, content, f"{directory}: {token}")
            self.assertTrue(
                "第一独立障碍" in content or "first_independent_obstacle" in content or "首障碍" in content,
                directory,
            )

            header = "\n".join(content.splitlines()[:6])
            self.assertIn("document_maturity=provisional", header, directory)
            if directory in CORE_DIRS:
                self.assertIn("document_status=adopted", header, directory)
            else:
                self.assertIn("document_status=research_only", header, directory)

    def test_shared_index_preserves_strong_a_and_controlled_b_without_forcing_independent_counts(self):
        index = read(PATTERNS_ROOT / "README.md")
        self.assertIn("至少两年的 Daily 左侧", index)
        self.assertIn("强 A→H1/L1 优先", index)
        self.assertIn("区间边缘三推不要求强 A", index)
        self.assertIn("独立主题只把 A/B 作为背景对照，不强行添加 ABC/H-L 计数", index)
        self.assertIn("EMA20/50/200", index)
        self.assertIn("第一独立障碍", index)

    def test_preflight_audit_preserves_route_specific_a_leg_exception(self):
        report = read(AUDIT_PATH)
        for token in (
            "强 A→H1/L1 优先",
            "H2/L2 可以承接普通 A",
            "成熟区间边缘三推是明确例外",
            "允许普通/偏弱 A",
            "区间中部三推仍为观察",
        ):
            self.assertIn(token, report, token)
        self.assertNotIn(
            "对 ABC、H1/L1、H2/L2、BOP、MTR 和三推等含有 A/B 语义的入口，强 A 仍是优先筛选条件",
            report,
        )

    def test_audit_is_indexed_and_validator_guarded(self):
        report = read(AUDIT_PATH)
        for path in (
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            PATTERNS_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        ):
            self.assertIn(AUDIT_PATH.name, read(path), path.as_posix())
        for directory in PATTERN_DIRS:
            self.assertIn(f"../patterns/{directory}/README.md", report, directory)
        for token in (
            "daily_context_window: >=2y / <2y / unavailable",
            "major_highs",
            "major_lows",
            "daily_ema20_50_200",
            "A_quality: strong",
            "B_quality: controlled",
            "first_independent_obstacle",
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

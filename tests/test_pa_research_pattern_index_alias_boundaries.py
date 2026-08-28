import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
PATTERNS_INDEX = PATTERNS_ROOT / "README.md"
STRATEGY_INVENTORY = REPO_ROOT / "strategy" / "pattern_inventory_candidates.md"
COVERAGE_AUDIT = REPO_ROOT / "research" / "abc_pattern_coverage_audit_CN.md"
AUDIT_PATH = REPO_ROOT / "research" / "pattern_index_alias_boundary_audit_2026-08-29_CN.md"


CORE_DIRS = (
    "01_h1_l1_first_entry",
    "02_h2_l2_second_entry",
    "03_abc_continuation",
    "04_range_edge_second_entry",
    "05_failed_breakout_climax",
    "06_breakout_pullback_bop",
    "07_mtr_reversal",
    "08_three_push_h3_l3",
)
INDEPENDENT_DIRS = (
    "09_vcp_minervini",
    "10_final_flag",
    "11_opening_reversal",
    "12_channel",
    "13_inside_bar_two_bar_reversal",
    "14_triangle_expanding_range",
    "15_double_top_bottom",
    "16_head_shoulders_rounded",
)
ALL_DIRS = CORE_DIRS + INDEPENDENT_DIRS


def text(path):
    return path.read_text(encoding="utf-8")


class PatternIndexAliasBoundaryTests(unittest.TestCase):
    def test_patterns_index_has_exact_sixteen_entries_and_tiers(self):
        index = text(PATTERNS_INDEX)
        actual_dirs = sorted(
            path.name
            for path in PATTERNS_ROOT.iterdir()
            if path.is_dir() and re.match(r"^\d{2}_", path.name)
        )
        self.assertEqual(actual_dirs, sorted(ALL_DIRS))

        linked_dirs = set(re.findall(r"\]\((\d{2}_[a-z0-9_]+)/README\.md\)", index))
        self.assertEqual(linked_dirs, set(ALL_DIRS))
        self.assertIn("当前核心范围", index)
        self.assertIn("独立体系主题", index)

        for directory in CORE_DIRS:
            header = text(PATTERNS_ROOT / directory / "README.md").splitlines()[:6]
            self.assertIn("document_status=adopted", "\n".join(header), directory)
            self.assertIn("document_maturity=provisional", "\n".join(header), directory)
        for directory in INDEPENDENT_DIRS:
            header = text(PATTERNS_ROOT / directory / "README.md").splitlines()[:6]
            self.assertIn("document_status=research_only", "\n".join(header), directory)
            self.assertIn("document_maturity=provisional", "\n".join(header), directory)

    def test_secondary_indexes_and_audit_cover_all_directory_names(self):
        inventory = text(STRATEGY_INVENTORY)
        report = text(AUDIT_PATH)
        for directory in ALL_DIRS:
            self.assertIn(f"../patterns/{directory}/README.md", inventory, directory)
            self.assertIn(f"../patterns/{directory}/README.md", report, directory)

        coverage = text(COVERAGE_AUDIT)
        self.assertIn("../patterns/09_vcp_minervini/README.md", coverage)
        self.assertIn("VCP / Minervini 独立主题", coverage)

    def test_representative_examples_use_canonical_primary_and_secondary_axes(self):
        matrix = text(
            REPO_ROOT / "research" / "priority_pattern_visual_candidate_matrix_2026-08-24_CN.md"
        )
        self.assertIn("primary_pattern: ABC_CONT", matrix)
        self.assertIn("internal_label: H2", matrix)
        self.assertEqual(matrix.count("| 案例 | 主标签 |"), 1)
        self.assertNotIn("primary_pattern: H2", matrix)
        self.assertIsNone(
            re.search(
                r"(?m)^\| \[`[^]]+`\]\([^)]*\) \| "
                r"`(?:H1|H2|H3|L1|L2|L3|range-edge second-entry|range-bottom reaction|BOP /[^`]+)` \|",
                matrix,
            )
        )
        self.assertIn("| `RFB` | `L2` |", matrix)

        bop_audit = text(REPO_ROOT / "research" / "cross_pattern_visual_priority_audit_2026-08-24_CN.md")
        self.assertIn(
            "primary_pattern: BOP\n"
            "secondary_context: former_range / former_double_top / former_triangle\n"
            "state_transition: breakout_acceptance",
            bop_audit,
        )
        self.assertNotIn("primary_pattern: BOP / accepted_breakout", bop_audit)
        self.assertNotIn("BOP_acceptance`", bop_audit)

        meta = text(REPO_ROOT / "strategy" / "reviews" / "2026-06-25-tsla-meta-example.md")
        self.assertIn("primary_pattern: other", meta)
        self.assertIn("pattern_like_reason:", meta)
        self.assertNotIn("primary_pattern: H3_L3", meta)
        self.assertIn("internal_label: pending", meta)

    def test_audit_and_indexes_preserve_scope_and_research_status(self):
        report = text(AUDIT_PATH)
        for path in (
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            PATTERNS_INDEX,
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        ):
            self.assertIn(AUDIT_PATH.name, text(path), path.as_posix())
        for token in (
            "16 个 pattern",
            "primary_pattern: ABC_CONT",
            "internal_label=H1 / L1",
            "internal_label=H2 / L2",
            "internal_label=H3 或 L3",
            "state_transition",
            "no-new-positive",
            "validated win-rate: not-computable",
            "不修改 Codex Trading",
            "不创建量化扫描器",
            "不连接 Execution Agent",
        ):
            self.assertIn(token, report, token)


if __name__ == "__main__":
    unittest.main()

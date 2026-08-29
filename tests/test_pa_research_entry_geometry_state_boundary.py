import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
PATTERN_DIRS = tuple(
    path.name
    for path in sorted(PATTERNS_ROOT.iterdir())
    if path.is_dir() and (path / "README.md").is_file()
)


def read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class EntryGeometryStateBoundaryTests(unittest.TestCase):
    def test_daily_candidate_card_uses_canonical_geometry_fields(self):
        content = read("docs/daily_candidate_review_card_CN.md")
        for token in (
            "new_trigger:",
            "order_price_or_zone:",
            "structural_stop:",
            "structural_invalidation:",
            "first_independent_obstacle:",
            "pre_entry_space_R:",
            "space_status:",
            "rough_R_R:",
            "target_layers:",
            "main_uncertainty_or_exclusion:",
        ):
            self.assertIn(token, content, token)
        self.assertNotIn("trigger_price_or_zone:", content)
        self.assertNotIn("structural_stop_or_zone:", content)
        self.assertLess(
            content.index("first_independent_obstacle:"),
            content.index("rough_R_R:"),
        )

    def test_visual_review_card_uses_pre_entry_geometry_and_state_boundary(self):
        content = read("docs/visual_pa_review_card_CN.md")
        for token in (
            "structural_stop:",
            "structural_stop_zone:",
            "first_independent_obstacle:",
            "rough_space_to_first_obstacle_R:",
            "pre_entry_space_R:",
            "space_status:",
            "rough_R_R:",
            "`observation_only` 或 `pending`",
            "`valid_no_trade`",
        ):
            self.assertIn(token, content, token)
        for stale in (
            r"(?m)^\s*stop_zone:",
            r"(?m)^\s*stop_price_or_area:",
            r"(?m)^\s*space_to_first_obstacle:",
        ):
            self.assertIsNone(re.search(stale, content), stale)

    def test_pattern_index_maps_shorthand_without_creating_new_contract_fields(self):
        content = read("patterns/README.md")
        for token in (
            "### Pattern-specific shorthand",
            "`location` / `location_and_left_structure` / `major_location`",
            "`space` / `target_path`",
            "`trigger` / `trigger_price_or_zone`",
            "`structural_stop_or_zone` / `stop_zone`",
            "`first_magnet`",
            "structural_stop / structural_invalidation",
            "first_independent_obstacle / rough_space_to_first_obstacle_R / space_status / rough_R_R",
            "几何顺序固定为：结构失效/止损 → 首障碍 → 入场前空间 → 粗略 R/R → 目标层",
        ):
            self.assertIn(token, content, token)

    def test_all_pattern_readmes_share_status_boundary_and_schema_pointer(self):
        self.assertEqual(len(PATTERN_DIRS), 16)
        status_boundary = (
            "状态边界：关键图表、事件、触发或空间证据尚不完整时使用"
        )
        for directory in PATTERN_DIRS:
            content = (PATTERNS_ROOT / directory / "README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("PA Research 统一输出合同 v0.1", content, directory)
            self.assertIn(status_boundary, content, directory)
            self.assertIn(
                "形态、方向和入场几何已可复核但已知硬闸门否决交易时使用",
                content,
                directory,
            )
            self.assertIn("两者都不建立订单，不能互换", content, directory)

    def test_authority_docs_and_audit_preserve_scope_and_conclusion(self):
        schema = read("docs/pa_research_output_schema_v0_1_CN.md")
        common = read("docs/common_context.md")
        audit = read(
            "research/entry_geometry_state_boundary_audit_2026-08-29_CN.md"
        )
        self.assertIn("structural_invalidation` 与 `structural_stop`", schema)
        self.assertIn("`observation_only` 与 `valid_no_trade` 的边界", schema)
        self.assertIn("### Entry geometry and state boundary", common)
        self.assertIn("observation_only", common)
        self.assertIn("valid_no_trade", common)
        for token in (
            "统一几何顺序",
            "no-new-positive",
            "validated win-rate: not-computable",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)


if __name__ == "__main__":
    unittest.main()

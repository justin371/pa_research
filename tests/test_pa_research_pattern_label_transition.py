import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
PATTERNS_INDEX = PATTERNS_ROOT / "README.md"
SCHEMA = REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md"
DAILY_RULES = REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md"
DAILY_CARD = REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md"
VISUAL_CARD = REPO_ROOT / "docs" / "visual_pa_review_card_CN.md"
COMMON_CONTEXT = REPO_ROOT / "docs" / "common_context.md"
SMOKE_TEST = REPO_ROOT / "research" / "visual_recognition_smoke_test_2026-08-24_CN.md"
AUDIT = REPO_ROOT / "research" / "pattern_label_transition_audit_2026-08-29_CN.md"
RESEARCH_INDEX = REPO_ROOT / "research" / "README.md"
DOCS_INDEX = REPO_ROOT / "docs" / "README.md"
STRATEGY_INDEX = REPO_ROOT / "strategy" / "README.md"


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


def read(path):
    return path.read_text(encoding="utf-8")


class PatternLabelTransitionTests(unittest.TestCase):
    def test_daily_candidate_primary_pattern_whitelist_is_explicit(self):
        expected = "primary_pattern: ABC_CONT / BOP"
        for path in (DAILY_RULES, DAILY_CARD):
            self.assertIn(expected, read(path), path.as_posix())

        for path in (SCHEMA, PATTERNS_INDEX, VISUAL_CARD, COMMON_CONTEXT, AUDIT):
            content = read(path)
            self.assertIn("daily_candidate", content, path.as_posix())
            self.assertIn("ABC_CONT", content, path.as_posix())
            self.assertIn("BOP", content, path.as_posix())

        index = read(PATTERNS_INDEX)
        self.assertIn("`primary_pattern` 只允许 `ABC_CONT` 或 `BOP`", index)
        self.assertIn("H1/H2/L1/L2 只能写入 `internal_label`", index)

    def test_hl_labels_are_internal_and_range_edge_is_not_h3_l3(self):
        schema = read(SCHEMA)
        visual = read(VISUAL_CARD)
        index = read(PATTERNS_INDEX)
        audit = read(AUDIT)

        for content in (schema, visual, index, audit):
            self.assertIn("internal_label", content)
            self.assertIn("range_edge_three_push", content)
        self.assertIn("range_edge_three_push` 只是区间边缘位置/分支旗标，不是 `primary_pattern`", schema)
        self.assertIn("range_edge_three_push` 是成熟区间上沿/下沿的独立位置分支旗标", audit)
        self.assertIn("H3/L3 与 `range_edge_three_push` 的关系边界", audit)
        self.assertNotIn(
            "pattern_family: TPB_H1_H2_H3 | L1_L2_L3",
            visual,
        )
        self.assertIn(
            "pattern_family: ABC_CONT | BOP | RFB_SECOND | H3_L3 | MTR | other",
            visual,
        )
        self.assertIsNone(
            re.search(r"(?m)^primary_pattern:\s*(?:H1|H2|L1|L2)(?:\s|$)", visual)
        )

    def test_all_pattern_readmes_declare_mapping_and_bop_invalidation(self):
        for directory in PATTERN_DIRS:
            content = read(PATTERNS_ROOT / directory / "README.md")
            self.assertIn("统一合同映射：", content, directory)
            self.assertIn(
                "direction: long / short / no_valid_direction", content, directory
            )
            self.assertIn("BOP 状态迁移：若事前可见边界被日线强收盘越过", content, directory)
            self.assertIn("state_transition: breakout_acceptance", content, directory)
            self.assertIn("旧订单合同失效", content, directory)

    def test_bop_transition_rebuilds_contract_in_authority_docs(self):
        transition_tokens = (
            "primary_pattern: BOP",
            "state_transition: breakout_acceptance",
            "new_trigger",
            "structural_stop",
            "first_independent_obstacle",
        )
        for path in (SCHEMA, VISUAL_CARD, PATTERNS_INDEX, AUDIT):
            content = read(path)
            for token in transition_tokens:
                self.assertIn(token, content, f"{token}: {path.as_posix()}")

        self.assertIn("不能沿用旧 entry/stop/target", read(SCHEMA))
        self.assertIn("不能沿用旧 entry/stop/target", read(VISUAL_CARD))
        self.assertIn("不能沿用旧 entry/stop/target", read(PATTERNS_INDEX))

    def test_visual_smoke_test_uses_non_contract_label(self):
        content = read(SMOKE_TEST)
        self.assertIn("visual_pattern_label:", content)
        self.assertIn("不是统一合同的 `primary_pattern` 字段", content)
        self.assertIsNone(re.search(r"(?m)^primary_pattern:", content))

    def test_audit_and_indexes_cover_all_entries_and_scope(self):
        audit = read(AUDIT)
        for directory in PATTERN_DIRS:
            self.assertIn(f"../patterns/{directory}/README.md", audit, directory)
        for path in (RESEARCH_INDEX, DOCS_INDEX, STRATEGY_INDEX, PATTERNS_INDEX):
            self.assertIn(AUDIT.name, read(path), path.as_posix())
        for token in (
            "日线候选的主标签白名单",
            "H1/H2/L1/L2 只能写入 `internal_label`",
            "primary_pattern: BOP",
            "state_transition: breakout_acceptance",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)


if __name__ == "__main__":
    unittest.main()

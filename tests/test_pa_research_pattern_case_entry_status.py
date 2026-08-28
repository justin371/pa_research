import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_ROOT = REPO_ROOT / "patterns"
PATTERNS_INDEX = PATTERNS_ROOT / "README.md"
RESEARCH_INDEX = REPO_ROOT / "research" / "README.md"
STRATEGY_INDEX = REPO_ROOT / "strategy" / "README.md"
AUDIT_PATH = REPO_ROOT / "research" / "pattern_case_entry_status_audit_2026-08-29_CN.md"


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


class PatternCaseEntryStatusTests(unittest.TestCase):
    def test_dated_case_table_rows_have_local_markdown_entries(self):
        for directory in PATTERN_DIRS:
            path = PATTERNS_ROOT / directory / "README.md"
            for line in read(path).splitlines():
                if (
                    line.startswith("|")
                    and re.search(r"\b20\d{2}-\d{2}", line)
                    and line.count("|") >= 3
                ):
                    self.assertIn("](", line, f"unlinked dated case row: {path}: {line}")

    def test_active_pattern_docs_use_canonical_no_trade_status(self):
        legacy_status = re.compile(r"(?<![\w-])valid(?:-| )no-trade(?![\w-])")
        for directory in PATTERN_DIRS:
            content = read(PATTERNS_ROOT / directory / "README.md")
            self.assertIsNone(
                legacy_status.search(content),
                f"legacy no-trade alias in {directory}",
            )
        research_index = read(RESEARCH_INDEX)
        self.assertNotIn("no_new_positive", research_index)
        self.assertIn("no-new-positive", research_index)

    def test_repaired_iwm_entry_and_indexes_are_covered(self):
        range_edge = read(PATTERNS_ROOT / "04_range_edge_second_entry" / "README.md")
        self.assertIn("IWM 2024-04-17–04-30", range_edge)
        self.assertIn("range_edge_second_entry_framework_CN.md", range_edge)

        for index_path in (PATTERNS_INDEX, RESEARCH_INDEX, STRATEGY_INDEX):
            self.assertIn(AUDIT_PATH.name, read(index_path), index_path.as_posix())
        audit = read(AUDIT_PATH)
        for directory in PATTERN_DIRS:
            self.assertIn(f"../patterns/{directory}/README.md", audit, directory)
        for token in (
            "valid_no_trade",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(token, audit, token)

    def test_audit_does_not_claim_a_validated_positive(self):
        active_docs = [read(PATTERNS_ROOT / directory / "README.md") for directory in PATTERN_DIRS]
        corpus = "\n".join(active_docs + [read(AUDIT_PATH)])
        self.assertIsNone(re.search(r"(?i)validated\s+positive", corpus))


if __name__ == "__main__":
    unittest.main()

"""Regression checks for selection/replay evidence boundaries."""

import csv
import re
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"
AUDIT_PATH = BACKTEST_ROOT / "pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md"

EXPECTED_SELECTIONS = {
    "hl_large_selection_2026-08-27_CN.md",
    "hl_next_selection_2026-08-27_CN.md",
    "hl_next2_selection_2026-08-27_CN.md",
    "hl_next3_selection_2026-08-27_CN.md",
    "hl_next4_selection_2026-08-27_CN.md",
    "hl_next5_selection_2026-08-27_CN.md",
}

POST_OUTCOME_COLUMNS = {
    "entry_price",
    "entry_date",
    "exit_price",
    "exit_date",
    "exit_reason",
    "bars_held",
    "fill_status",
    "trade_result",
    "realized_R",
    "win_rate_eligible",
    "path_result",
    "first_obstacle_hit",
    "ambiguous_intrabar",
    "gap_adjustment",
    "evidence_status",
}

POST_OUTCOME_FIELD_RE = re.compile(
    r"(?im)^\s*(?:entry_price|entry_date|exit_price|exit_date|exit_reason|bars_held|"
    r"fill_status|trade_result|realized_R|win_rate_eligible|path_result|"
    r"first_obstacle_hit|ambiguous_intrabar|gap_adjustment|evidence_status)\s*:"
)
OUTCOME_TABLE_RE = re.compile(
    r"(?im)^\s*\|[^\r\n]*(?:完成成交|是否成交|胜负|胜率)[^\r\n]*"
    r"实现\s*R[^\r\n]*\|"
)


class PaResearchPreEntryPostOutcomeBoundaryTests(unittest.TestCase):
    def test_selection_records_are_pre_outcome_only(self):
        paths = sorted(BACKTEST_ROOT.glob("*_selection_*.md"))
        self.assertEqual({path.name for path in paths}, EXPECTED_SELECTIONS)

        for path in paths:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("frozen_pre_outcome", content)
                self.assertIsNone(
                    POST_OUTCOME_FIELD_RE.search(content),
                    f"post-outcome field leaked into selection record: {path.name}",
                )
                self.assertNotRegex(
                    content,
                    r"(?im)^##\s+回放与统计状态\s*$",
                )
                self.assertIsNone(
                    OUTCOME_TABLE_RE.search(content),
                    f"post-outcome table leaked into selection record: {path.name}",
                )

    def test_frozen_contract_headers_do_not_contain_result_columns(self):
        paths = sorted(
            path
            for path in BACKTEST_ROOT.glob("*contracts*.csv")
            if path.name != "contracts.example.csv"
        )
        self.assertEqual(len(paths), 7)

        for path in paths:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                headers = set(next(csv.reader(handle), []))
            with self.subTest(path=path.name):
                self.assertFalse(
                    headers & POST_OUTCOME_COLUMNS,
                    f"post-outcome column leaked into frozen contract: {path.name}",
                )

    def test_candidate_cards_have_no_post_outcome_field_definitions(self):
        paths = (
            REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md",
            REPO_ROOT / "docs" / "visual_pa_review_card_CN.md",
        )
        for path in paths:
            with self.subTest(path=path.name):
                self.assertIsNone(
                    POST_OUTCOME_FIELD_RE.search(path.read_text(encoding="utf-8")),
                    f"post-outcome field leaked into candidate card: {path.name}",
                )

    def test_next3_replay_keeps_the_no_contract_boundary(self):
        selection = (BACKTEST_ROOT / "hl_next3_selection_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )
        replay = (BACKTEST_ROOT / "hl_next3_replay_2026-08-27_CN.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("本批没有可冻结的交易合同", selection)
        self.assertIn("事前记录边界", selection)
        self.assertIn("没有任何一条同时通过", replay)
        self.assertIn("实现 R", replay)
        self.assertIn("contract CSV contains no rows", replay)

    def test_audit_and_indexes_preserve_the_boundary(self):
        audit = AUDIT_PATH.read_text(encoding="utf-8")
        for phrase in (
            "6 份 `research/backtesting/*_selection_*.md`",
            "11 个仓库内视觉资产 README",
            "direction",
            "signal_bar / new_trigger",
            "structural_invalidation / structural_stop",
            "first_independent_obstacle / space_status",
            "event_context / lineage_id",
            "hl_next3_selection_2026-08-27_CN.md",
            "frozen_pre_outcome",
            "no-new-positive",
            "validated win-rate: not-computable",
            "PA Research only",
            "no Codex Trading",
            "no quantitative scanner",
            "no Execution Agent",
        ):
            self.assertIn(phrase, audit, phrase)

        indexed_files = (
            REPO_ROOT / "research" / "README.md",
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "strategy" / "README.md",
            REPO_ROOT / "patterns" / "README.md",
            BACKTEST_ROOT / "README.md",
            REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1",
        )
        for path in indexed_files:
            with self.subTest(path=path.as_posix()):
                self.assertIn(AUDIT_PATH.name, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import unittest

from pa_research_backtest.engine import (
    SUPPORTED_DIRECTIONS,
    SUPPORTED_ORDER_BRANCHES,
    SUPPORTED_PATTERNS,
    load_contracts,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"


class PaResearchContractConsistencyTests(unittest.TestCase):
    def test_engine_enum_boundary_matches_current_contract(self):
        self.assertEqual(SUPPORTED_DIRECTIONS, {"long", "short"})
        self.assertEqual(
            SUPPORTED_ORDER_BRANCHES,
            {"stop_confirmation", "limit_retest", "market_close"},
        )
        self.assertEqual(
            SUPPORTED_PATTERNS,
            {"ABC_CONT", "BOP", "H1_L1", "H2_L2", "H3_L3", "RFB", "MTR", "other"},
        )

    def test_example_contract_is_a_supported_frozen_replay_contract(self):
        contract = load_contracts(BACKTEST_ROOT / "contracts.example.csv")[0]

        self.assertEqual(contract.direction, "long")
        self.assertEqual(contract.primary_pattern, "ABC_CONT")
        self.assertEqual(contract.internal_label, "H1")
        self.assertEqual(contract.order_branch, "stop_confirmation")
        self.assertEqual(contract.contract_frozen, "yes")

    def test_daily_candidate_templates_keep_top_level_pattern_boundary(self):
        rules = (REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md").read_text(
            encoding="utf-8"
        )
        review_card = (REPO_ROOT / "docs" / "daily_candidate_review_card_CN.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("primary_pattern: ABC_CONT / BOP", rules)
        self.assertIn("primary_pattern: ABC_CONT / BOP", review_card)
        self.assertNotIn("primary_pattern: ABC_CONT / BOP / H1_L1", review_card)

    def test_record_only_states_are_documented_as_not_direct_replay_input(self):
        unified = (REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md").read_text(
            encoding="utf-8"
        )
        replay_readme = (BACKTEST_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("研究记录超集", unified)
        self.assertIn("no_valid_direction", unified)
        self.assertIn("stop_limit", unified)
        self.assertIn("actual_fill_or_open_skip", unified)
        self.assertIn("不能直接传给当前回放器", unified)
        self.assertIn("当前 engine `0.3.9` 的回放输入边界", replay_readme)
        self.assertIn("`direction` 只接受 `long` 或 `short`", replay_readme)
        self.assertIn("`order_branch` 只接受", replay_readme)
        self.assertIn("不能直接传给当前回放器", replay_readme)
        self.assertIn("fill_status", replay_readme)


if __name__ == "__main__":
    unittest.main()

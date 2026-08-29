import csv
from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = REPO_ROOT / "docs" / "pa_research_output_schema_v0_1_CN.md"
DAILY_RULES = REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md"
VISUAL_CARD = REPO_ROOT / "docs" / "visual_pa_review_card_CN.md"
PATTERN = REPO_ROOT / "patterns" / "08_three_push_h3_l3" / "README.md"
FRAMEWORK = REPO_ROOT / "research" / "three_push_pressure_state_framework_CN.md"
AUDIT = REPO_ROOT / "research" / "backtesting" / "three_push_h3_l3_contract_boundary_audit_2026-08-29_CN.md"
BACKTEST_ROOT = REPO_ROOT / "research" / "backtesting"


THIRD_PUSH_ENUM = (
    "third_push_state: exhaustion_candidate / continuation_or_climax / "
    "range_repeat_test / channel_continuation / unclear"
)
RANGE_SIDE_ENUM = "range_edge_side: upper / lower / none / pending"


def read(path):
    return path.read_text(encoding="utf-8")


class ThreePushContractBoundaryTests(unittest.TestCase):
    def test_canonical_three_push_fields_are_present_across_authority_docs(self):
        for path in (SCHEMA, DAILY_RULES, VISUAL_CARD, PATTERN, FRAMEWORK):
            content = read(path)
            self.assertIn(THIRD_PUSH_ENUM, content, path.as_posix())
            self.assertIn(RANGE_SIDE_ENUM, content, path.as_posix())
            self.assertIn("first_reverse: none / touch / structural_break", content, path.as_posix())
            self.assertIn("second_confirmation: yes / no / pending", content, path.as_posix())

        self.assertIsNone(re.search(r"(?m)^h3_l3_state:", read(VISUAL_CARD)))
        self.assertIsNone(re.search(r"(?m)^push_state:", read(FRAMEWORK)))
        self.assertNotIn(
            "third_push_state: exhaustion / expansion-or-climax / range-repeat / channel-continuation",
            read(PATTERN),
        )

    def test_range_edge_side_direction_and_status_boundaries_are_explicit(self):
        schema = read(SCHEMA)
        rules = read(DAILY_RULES)
        pattern = read(PATTERN)
        audit = read(AUDIT)

        for content in (schema, rules, pattern, audit):
            self.assertIn("range_edge_three_push", content)
            self.assertIn("range_edge_side", content)
            self.assertIn("upper", content)
            self.assertIn("lower", content)
            self.assertIn("no_valid_direction", content)

        self.assertIn("当它为 `no` 时 side 写 `none`", schema)
        self.assertIn("当它为 `pending` 时 side 写 `pending`", schema)
        self.assertIn("range_edge_three_push: yes`，必须同时记录 `range_edge_side: upper / lower", rules)
        self.assertIn("range_edge_side=upper` 只建立空头研究方向", pattern)
        self.assertIn("canonical `direction` 仍可以是 `no_valid_direction`", audit)

    def test_pressure_state_is_separate_from_order_and_trade_state(self):
        for path in (SCHEMA, PATTERN, AUDIT):
            content = read(path)
            for token in (
                "third_push_state",
                "first_reverse",
                "second_confirmation",
                "order_branch",
                "trade_state",
                "gate_result",
            ):
                self.assertIn(token, content, f"{token}: {path.as_posix()}")
        self.assertIn("不能互相替代", read(SCHEMA))
        self.assertIn("第三推极值不构成入场", read(AUDIT))

    def test_current_frozen_inventory_has_no_h3_or_range_edge_denominator(self):
        paths = sorted(
            path
            for path in BACKTEST_ROOT.glob("*contracts*.csv")
            if path.name != "contracts.example.csv"
        )
        self.assertEqual(len(paths), 7)
        rows = []
        for path in paths:
            with path.open(encoding="utf-8", newline="") as handle:
                file_rows = list(csv.DictReader(handle))
            self.assertTrue(file_rows, path.name)
            rows.extend(file_rows)

        self.assertEqual(len(rows), 60)
        self.assertFalse(
            any(
                row.get("primary_pattern") == "H3_L3"
                or row.get("internal_label") in {"H3", "L3"}
                for row in rows
            )
        )
        self.assertNotIn("range_edge_three_push", rows[0])
        self.assertNotIn("third_push_state", rows[0])

        audit = read(AUDIT)
        for token in (
            "冻结合同 CSV | 7 份",
            "冻结合同总行数 | 60",
            "H3/L3 冻结行 | 0",
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

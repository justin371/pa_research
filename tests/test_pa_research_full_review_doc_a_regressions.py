"""Regression checks for the doc-a research-review boundary repairs."""

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class FullReviewDocARegressionTests(unittest.TestCase):
    def test_double_top_separates_incomplete_evidence_from_known_no_trade_gate(self):
        content = read(
            "research/double_top_bottom_visual_boundary_audit_2026-08-24_CN.md"
        )

        self.assertIn(
            "只有形状，或父级、方向、触发/空间等证据仍不完整时，输出 "
            "`observation_only`；资料仍可能补齐时同时保留 `pending`。",
            content,
        )
        self.assertIn(
            "当父级已确认处于区间中部、首障碍不足约 `1R`、原方向已经重新接受，"
            "或已知事件/跳空已经改变几何，且形态、方向和入场几何足够复核时，输出 "
            "`valid_no_trade`。",
            content,
        )
        self.assertNotRegex(
            content,
            r"只有形状、父级是区间中部、首障碍不足约 `1R`、原方向已经重新接受、"
            r"或事件/跳空改变几何时，输出 `valid_no_trade`",
        )

    def test_cost_keeps_daily_signal_high_and_intraday_observation_distinct(self):
        content = read(
            "research/cost_bullish_h1_first_obstacle_boundary_2024-05-13_2024-05-16.md"
        )
        order_section = re.search(
            r"(?s)^## 3\. 订单与低周期顺序\n(?P<section>.*?)^## 4\. ",
            content,
            re.MULTILINE,
        )
        self.assertIsNotNone(order_section)
        section = order_section.group("section")
        for token in (
            "Daily signal-high contract",
            "`05-15` 收盘后的 Daily 高点约 `779.96`",
            "15m",
            "intraday observation",
            "gap_policy: skip",
            "opening-skip",
            "unproven",
            "reprice",
        ):
            self.assertIn(token, section, token)
        self.assertIn("不能声称已有订单", section)
        self.assertNotIn("14:15–14:30 为 Daily signal-high contract 的激活时间", section)
        quality_line = next(
            line for line in content.splitlines() if line.startswith("| signal quality |")
        )
        self.assertIn("15m 价格观察顺序可核对", quality_line)
        self.assertIn("不是冻结订单触发证明", quality_line)
        self.assertNotIn("15m 触发顺序可重建", quality_line)

    def test_final_flag_separates_single_reverse_bar_from_near_magnet_gate(self):
        content = read("research/final_flag_visual_boundary_audit_2026-08-24_CN.md")

        self.assertIn(
            "| 只有一根反向 K，尚无确认/跟随 | `observation_only` / `pending` |",
            content,
        )
        self.assertIn(
            "| 方向和几何已可复核但首磁铁近 | `valid_no_trade` |",
            content,
        )

    def test_h3_l3_does_not_treat_unproved_first_obstacle_as_valid_no_trade(self):
        content = read("research/h3_l3_research_gate_CN.md")

        self.assertIn(
            "若第一障碍或触发前几何尚未证明，标签只能是“形态观察”、"
            "`observation_only`，必要时 `pending`",
            content,
        )
        self.assertIn(
            "形态、方向和入场几何已足够复核且已知首障碍硬闸门明确不足，才用 "
            "`valid_no_trade`",
            content,
        )

    def test_late_trend_separates_missing_acceptance_from_known_geometry_gate(self):
        content = read("research/late_trend_entry_visual_framework_CN.md")

        self.assertIn(
            "只有一根大 K、没有后续接受/跟随，或高周期/低周期关系仍只是局部扩张且未完成复核，"
            "输出 `observation_only`；资料可能补齐时保留 `pending`",
            content,
        )
        self.assertIn(
            "形态、方向和入场几何均已复核，但最后一根趋势 K 已贴近主要磁铁/左侧高低点、"
            "首障碍不足约 1R、结构止损过窄，或已知财报/重大事件明确使几何失真，"
            "输出 `valid_no_trade`",
            content,
        )


if __name__ == "__main__":
    unittest.main()

"""Regression checks for the doc-b research-review boundary repairs."""

from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class FullReviewDocBRegressionTests(unittest.TestCase):
    def test_sector_endpoints_are_not_entry_time_evidence(self):
        crwd = read(
            "research/crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md"
        )
        self.assertIn("2024-10-04", crwd)
        self.assertIn("post-cutoff audit", crwd)
        self.assertIn("不能计入 `10-03` 的市场、板块或 META 确认", crwd)
        self.assertIn("10-03` 事前同步方向未核验", crwd)
        self.assertNotIn("SOXX 同期方向大体配合", crwd)

        jpm = read(
            "research/jpm_bullish_h1_first_obstacle_failure_2025-08-22_2025-09-05.md"
        )
        self.assertIn("板块事前未核验", jpm)
        self.assertIn("sector-unverified", jpm)
        self.assertIn("post-entry/day-close audit", jpm)
        self.assertIn("同期、带时间戳的盘中板块证据仍未核验", jpm)
        self.assertNotIn("入场时板块方向是支持的", jpm)
        self.assertNotIn("板块顺势", jpm)

        nke = read(
            "research/nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md"
        )
        self.assertIn("post-entry/day-close audit", nke)
        self.assertIn("不能计入 `09:45` 的市场/板块或 META 确认", nke)
        self.assertIn("sector-unverified/mixed", nke)
        self.assertNotIn("当日并未同步走弱", nke)

    def test_nvda_separates_first_possible_touch_from_fill_and_recovery(self):
        content = read(
            "research/nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md"
        )

        self.assertIn("现有记录中最早已见越过的 K 线窗口", content)
        self.assertIn("价格越过不能证明订单激活", content)
        self.assertIn("实际成交或准确 fill clock", content)
        self.assertIn("recovery confirmation", content)
        self.assertIn("fill-unproven", content)
        self.assertNotIn("首次可能触及/越过", content)
        self.assertNotIn("11:30` 这一小时完成触发", content)
        self.assertIn("不能计入 `09-24` 的市场、板块或 META 确认", content)
        self.assertIn("触发后的路径审计", content)
        self.assertNotIn("随后是 `09-24` 当日约 `121.6` 的阻力簇", content)
        self.assertIn("不能倒灌为原分支的事前止损依据", content)
        self.assertIn("后验混时的 `1.9R`", content)
        self.assertIn("约 `1.35R`", content)

    def test_msft_title_window_does_not_freeze_hindsight_bars(self):
        content = read(
            "research/msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md"
        )

        self.assertIn("pre-entry freeze", content)
        self.assertIn("title-window", content)
        self.assertIn("2025-11-21", content)
        self.assertIn("不计入 `11-20` 的事前证据", content)
        self.assertIn("pattern_like", content)
        self.assertIn("pending", content)

    def test_tsla_later_paths_do_not_support_selection_or_exclusion(self):
        content = read(
            "research/tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md"
        )

        self.assertIn("post-outcome/path audit", content)
        self.assertIn("不能用于强化该日的候选排序", content)
        self.assertIn("不是 10-04 当时筛除证据", content)
        self.assertIn("不是 12-12 当时筛除证据", content)
        self.assertIn("post-outcome/path-audit 的后验边界样本分类", content)
        self.assertIn("post-outcome/path-audit 的后验边界审计", content)
        self.assertNotIn("且后续继续走高。", content)


if __name__ == "__main__":
    unittest.main()

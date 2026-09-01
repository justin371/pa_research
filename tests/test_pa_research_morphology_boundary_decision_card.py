import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
CARD_PATH = REPO_ROOT / "docs" / "morphology_boundary_decision_card_CN.md"
PROTOCOL_PATH = REPO_ROOT / "docs" / "visual_calibration_protocol_v0_1_CN.md"
METRICS_PATH = REPO_ROOT / "research" / "morphology_calibration_metrics_2026-09-01.json"
ADJUDICATION_PATH = REPO_ROOT / "research" / "morphology_calibration_blind_adjudication_2026-09-01.json"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_pa_research_docs.ps1"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class MorphologyBoundaryDecisionCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.card = read(CARD_PATH)
        cls.protocol = read(PROTOCOL_PATH)
        cls.metrics = json.loads(read(METRICS_PATH))
        adjudication = json.loads(read(ADJUDICATION_PATH))
        cls.adjudication_by_id = {
            row["sample_id"]: row for row in adjudication["adjudications"]
        }

    def test_card_is_canonical_indexed_and_validator_required(self):
        relative_name = "morphology_boundary_decision_card_CN.md"
        self.assertIn(relative_name, read(REPO_ROOT / "docs" / "README.md"))
        self.assertIn(relative_name, read(REPO_ROOT / "research" / "README.md"))
        self.assertIn(
            f"'docs/{relative_name}'",
            read(VALIDATOR_PATH),
        )
        for path in (
            REPO_ROOT / "docs" / "visual_pa_review_card_CN.md",
            REPO_ROOT / "research" / "visual_pattern_triage_protocol_CN.md",
            REPO_ROOT / "docs" / "pa_research_daily_selection_rules_v0_1_CN.md",
            REPO_ROOT / "patterns" / "01_h1_l1_first_entry" / "README.md",
            REPO_ROOT / "patterns" / "02_h2_l2_second_entry" / "README.md",
            REPO_ROOT / "patterns" / "03_abc_continuation" / "README.md",
            REPO_ROOT / "patterns" / "06_breakout_pullback_bop" / "README.md",
            REPO_ROOT / "patterns" / "08_three_push_h3_l3" / "README.md",
        ):
            with self.subTest(path=path):
                self.assertIn(relative_name, read(path))

    def test_card_freezes_state_precedence_before_hl_counting(self):
        for token in (
            "BOP 状态迁移 > 区间/第三推分流 > 普通 ABC/H-L 计数 > 交易几何",
            "事前可见边界是否已被收盘突破、获得跟随，并在回踩时守住",
            "当前是否为成熟区间边缘，或同一 lineage 的第三次有意义尝试",
            "才允许研究 `ABC_CONT + internal_label H1/H2/L1/L2`",
            "旧 ABC/H-L/三推合同失效",
            "计数重置",
        ):
            self.assertIn(token, self.card)

    def test_b_leg_classes_separate_pressure_structure_and_range(self):
        for value in (
            "`not_formed`",
            "`controlled`",
            "`controlled_late`",
            "`deep_but_late_controlled`",
            "`uncontrolled`",
            "`range_like`",
            "`unclear`",
        ):
            self.assertIn(value, self.card)
        for token in (
            "反向压力是在缩小、持平，还是扩大",
            "母腿的关键极值或起点是否仍然有效",
            "宽范围两边来回获得跟随",
            "不设固定回撤百分比、K 线数量、EMA 距离或实体阈值",
        ):
            self.assertIn(token, self.card)

    def test_frozen_pair_examples_match_tracked_adjudication(self):
        expected = {
            "MC2-004": ("BOP_like", "H2_like", "wait_for_structure"),
            "MC2-010": ("BOP_like", "H1_like", "deep_reviewed"),
            "MC2-002": ("H_L_like", "H2_like", "wait_for_structure"),
            "MC2-008": ("ABC_CONT_like", "H2_like", "wait_for_structure"),
            "MC2-007": ("THREE_PUSH_like", "L3_like", "rejected_gate"),
            "MC2-014": ("THREE_PUSH_like", "L3_like", "rejected_gate"),
            "MC2-012": ("THREE_PUSH_like", "H3_like", "rejected_gate"),
            "MC2-015": ("THREE_PUSH_like", "H3_like", "wait_for_structure"),
            "MC2-005": ("BOP_like", "pending", "event_boundary"),
        }
        metric_ids = {
            row["sample_id"]
            for row in self.metrics["candidate_source_comparison"]["samples"]
        }
        for sample_id, values in expected.items():
            with self.subTest(sample=sample_id):
                self.assertIn(sample_id, self.card)
                self.assertIn(sample_id, metric_ids)
                row = self.adjudication_by_id[sample_id]
                self.assertEqual(
                    (
                        row["visual_family"],
                        row["attempt_label"],
                        row["selection_disposition"],
                    ),
                    values,
                )

    def test_protocol_separates_model_adjudication_from_human_ground_truth(self):
        for token in (
            "独立模型裁决与人工专家真值分层",
            "reviewers_agree",
            "both_reasonable_boundary",
            "adjudicator_choice",
            "模型裁决用于定位字段分歧和边界，不是人工专家 ground truth",
            "human_expert_status: not_performed",
            "ground_truth_status: not_established",
            "overall_accuracy: not-computable",
        ):
            self.assertIn(token, self.protocol)

    def test_card_preserves_research_and_statistics_boundaries(self):
        for token in (
            "PA Research only",
            "不是人工专家真值",
            "不创建量化扫描器",
            "不修改 Codex Trading",
            "不连接 Execution Agent",
            "conclusion: no-new-positive",
            "validated win-rate: not-computable",
        ):
            self.assertIn(token, self.card)


if __name__ == "__main__":
    unittest.main()

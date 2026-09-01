# 普通 H1/H2/L1/L2 外部人工专家盲标包 v1

日期：2026-09-01
状态：`packet_ready / annotation_not_performed / label-hidden / outcome-hidden / future-hidden`

本包包含 16 张既有历史 Daily 截止图。候选集在外部专家标注前冻结，并经过平衡策划；具体平衡类别、来源假设、股票和截止日期对专家隐藏。所有来源假设只是 model/source hypotheses，不是答案或 ground truth。

使用顺序：

1. 先阅读[专家标注标准](expert_criteria_CN.md)；
2. 按 `EH1-001` 至 `EH1-016` 顺序打开下列图，独立完成[空白标注表](annotation_form.md)；
3. 完成并冻结全部记录后，才可把结果交回 PA Research；
4. 在外部专家记录被冻结并通过 contamination 检查之前，不打开任何来源 hypothesis key。

| expert_sample_id | 截止图 |
|---|---|
| EH1-001 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-004.png) |
| EH1-002 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-009.png) |
| EH1-003 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-002.png) |
| EH1-004 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-010.png) |
| EH1-005 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-007.png) |
| EH1-006 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-013.png) |
| EH1-007 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-005.png) |
| EH1-008 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-014.png) |
| EH1-009 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_boundary_holdout_v1/BH1-001.png) |
| EH1-010 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_boundary_holdout_v1/BH1-009.png) |
| EH1-011 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-003.png) |
| EH1-012 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-012.png) |
| EH1-013 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-008.png) |
| EH1-014 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_boundary_holdout_v1/BH1-002.png) |
| EH1-015 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-001.png) |
| EH1-016 | [打开图](../../assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/MC2-006.png) |

[机器 manifest](manifest.json)只保存中性编号和图路径，不包含标签、股票、日期、候选 family、结果或未来路径。

```text
human_expert_status: not_performed
ground_truth_status: not_established
overall_accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
PA Research only
no Codex Trading
no quantitative scanner
no automatic pattern detector
no Futu/OpenD
no Execution Agent
```

# 普通 H/L 外部专家盲标表 v1

标注人只打开 [专家标准](expert_criteria_CN.md)、本表和 README 中对应的截止图。所有字段必须在查看任何答案、未来或结果前冻结。

允许值：

```text
evidence_usable: yes / no / uncertain
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
direction: long / short / no_valid_direction
ema20_slope, ema50_slope: rising / falling / flat / unclear
ema200_context: supportive / conflicting / neutral / unclear
A_leg_quality: strong / ordinary / event_driven / unclear
B_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / not_formed / unclear
lineage_status: same_lineage / reset / unclear
expert_ordinary_hl_label: H1 / H2 / L1 / L2 / not_ordinary_HL / unclear
primary_exclusion: not_applicable / accepted_BOP / third_push_H3_L3 / range_repeat / event_or_gap / EMA_gate_fail / insufficient_space / A_not_directional / B_not_controlled / lineage_reset / no_valid_direction / insufficient_evidence / other
confidence_1_to_5: 1 / 2 / 3 / 4 / 5
```

| expert_sample_id | evidence_usable | parent_state | direction | ema20_slope | ema50_slope | ema200_context | A_leg_quality | B_leg_class | lineage_status | expert_ordinary_hl_label | primary_exclusion | confidence_1_to_5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EH1-001 | | | | | | | | | | | | |
| EH1-002 | | | | | | | | | | | | |
| EH1-003 | | | | | | | | | | | | |
| EH1-004 | | | | | | | | | | | | |
| EH1-005 | | | | | | | | | | | | |
| EH1-006 | | | | | | | | | | | | |
| EH1-007 | | | | | | | | | | | | |
| EH1-008 | | | | | | | | | | | | |
| EH1-009 | | | | | | | | | | | | |
| EH1-010 | | | | | | | | | | | | |
| EH1-011 | | | | | | | | | | | | |
| EH1-012 | | | | | | | | | | | | |
| EH1-013 | | | | | | | | | | | | |
| EH1-014 | | | | | | | | | | | | |
| EH1-015 | | | | | | | | | | | | |
| EH1-016 | | | | | | | | | | | | |

每张图还必须填写以下自由文本，不能只投票：

```text
expert_sample_id:
major_high_low_reading:
A_leg_evidence:
B_leg_evidence:
lineage_and_attempt_evidence:
first_obstacle_and_space:
why_not_BOP_or_third_push_or_range_repeat:
main_uncertainty:
```

冻结声明：

```text
annotator_role: external_human_expert
annotator_independent: no / yes
annotation_started_at:
annotation_frozen_at:
source_or_model_hypotheses_seen_before_freeze: no / yes
future_or_outcome_evidence_seen_before_freeze: no / yes
knowledge_status: clean / contaminated / uncertain
signature_or_identifier:
```

所有字段都必须由专家明确填写。表到 JSON 只能由协调人按内部无推断转录合同逐字段复制；空白、含糊或冲突值必须退回人工确认，不能推断或代填。

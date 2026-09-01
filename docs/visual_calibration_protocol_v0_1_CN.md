# PA Research 图表视觉校准协议 v0.1

日期：2026-09-01  
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

## 一、目的

本协议把两件容易混淆的事情分开测量：

1. **图形识别一致性**：从未标注、结果隐藏的图表中，是否能正确记录父级、方向、A/B质量、H1/H2/L1/L2-like、三推-like、位置和否决原因；
2. **交易结果统计**：在独立冻结触发、结构止损、第一障碍和持有合同后，历史路径如何结束。

图形识别一致不等于盈利；盈利也不能把错误的形态命名、错误位置或事后解释改成正确识别。本协议不创建自动识别器、量化扫描器、生产规则或 Execution Agent 接口。

简写为：视觉一致不等于交易盈利。

## 二、两种校准批次

### 2.1 确定性发现批次

`cohort_id: deterministic_discovery_cohort`

从满足图表 provenance 的历史价格池中，用预先冻结的随机/哈希规则选 symbol 和 cutoff；不根据形态或结果挑图。用途是测量：

- 候选发现是否漏掉专家认为值得深审的图；
- 是否把区间中部、EMA冲突、首障碍拥挤或事件重订误选成高质量候选；
- `deep_reviewed / deferred_capacity / wait_for_structure / rejected_gate / event_boundary` 的处置是否与专家一致。

确定性发现批次可以自然出现零个某类 pattern；不能为了凑 H2/L2 或三推正例替换抽样图。

### 2.2 形态覆盖批次

`cohort_id: curated_morphology_cohort`

由独立专家在只看截止日前证据的前提下建立平衡形态集，专门覆盖 H1/H2/L1/L2、三推变形和相似负例。它用于测量标签边界，不代表市场自然发生率，也不能与确定性发现批次混算召回率。

三推形态覆盖批次可以使用下列**校准显示变形**：

```text
standard_converging
parabolic_climactic
expanding
truncated_third_push
overshoot_failed_breakout
nested_or_complex
trend_pullback
range_edge
unclear
```

这些词只帮助比较视觉读法，不是新的 canonical setup 或 `third_push_state` 枚举。完整记录仍映射到 `exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear`，并结合父级、位置和反向确认判断。

## 三、严格盲测资格

每张图至少满足：

```text
sample_id:
source_price_artifact:
cutoff_date:
daily_context_window: >=2y
major_high_low_review: visually_available
ema20_50_200_review: visually_available
label_hidden: yes
outcome_hidden: yes
future_bars_hidden: yes
selection_frozen_before_view: yes
reviewer_knowledge_status: clean / possibly_contaminated / contaminated
```

- 图上不能出现 pattern、方向、入场、止损、目标、结果或作者裁决标记。
- 截止日之后的 K 线、回放报告和旧案例文字在首次答案冻结前不得打开。
- 若 reviewer 已经看过同一 symbol/date 的合同、标签或结果，该行保留描述性记录，但从严格盲测分母排除。
- 文件名含 symbol/date 不构成泄漏；含 H1、L2、winner、target 等标签则不合格。
- 图像必须显示至少两年 Daily、重要高低点和 EMA20/50/200；局部图只能作为补充，不能替代完整背景。

## 四、首次答案冻结字段

首次答案只记录事前视觉判断：

```text
sample_id:
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
direction: long / short / no_valid_direction
a_leg_quality: strong / ordinary / unclear / event_driven
b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear / not_formed
calibration_visual_family: ABC_CONT_like / BOP_like / H_L_like / THREE_PUSH_like / NONE / UNCLEAR
calibration_attempt_label: H1_like / H2_like / L1_like / L2_like / H3_like / L3_like / pending / not_applicable
calibration_three_push_variant:
ema_gate_reading: long_pass / short_pass / fail_flat_or_opposite / pending
location_reading:
first_obstacle_reading:
stage_1_status:
shortlist_rank:
selection_disposition:
main_uncertainty:
prediction_frozen_at:
```

`calibration_*` 是盲测显示字段，不得直接写入正式 `primary_pattern`、`internal_label` 或冻结交易合同。精确 H/L 计数仍需同一主周期、同一 lineage、第一次失败/不足和第二次尝试证据。

## 五、独立模型裁决与人工专家真值分层

### 5.1 独立模型裁决

可以在两份首次答案冻结后，让一个未接触候选答案、未来 K 线或结果的独立模型 adjudicator 查看同图和两份 reviewer 记录，并对每个样本选择：

```text
reviewers_agree
both_reasonable_boundary
adjudicator_choice
insufficient_chart_evidence
knowledge_contaminated
```

模型裁决用于定位字段分歧和边界，不是人工专家 ground truth。`both_reasonable_boundary` 不得为了提高一致率改成一致；`adjudicator_choice` 也不能称为模型正确或识别准确率。若需要事件资料、低周期或未来 K 线才能裁决，必须标记证据不足或进入另一层合同，不能倒灌到 Daily 首次答案。

### 5.2 外部人工专家复核

外部人工专家若在不知道首次答案和候选来源的条件下先冻结独立答案，才可形成单独的 human-expert comparison。人工专家仍需声明知识污染状态、图表充分性和使用的证据层；其意见不能由模型裁决代替，也不能因为和候选来源一致就自动成为交易真值。

在人工专家复核未完成前，统一写：

```text
human_expert_status: not_performed
ground_truth_status: not_established
overall_accuracy: not-computable
```

## 六、识别指标

图形识别至少分开报告：

- 每个字段的 exact agreement；
- parent/direction/A/B/EMA/location/处置的 critical disagreement 数；
- `deep_reviewed` 的候选 precision：专家同意值得深审的数量 ÷ 模型深审数量；
- 候选 recall：模型深审或合理延后的专家正向数量 ÷ 专家正向数量；
- false-positive 原因：区间中部、EMA冲突、事件污染、首障碍、A弱、B失控、lineage错误；
- false-negative 原因：未发现强 A、把等待 B 当否决、容量延后丢失、三推变形漏认；
- H1/H2/L1/L2 和各三推变形的混淆矩阵。

总 accuracy 在类别不平衡时容易误导，不能单独使用。`possibly_contaminated/contaminated`、图表不足两年、标签可见和结果可见的样本从严格指标分母排除，只保留描述性附录。

候选 precision / recall 必须成对报告，并同时列出专家正向分母、深审容量延后数和证据不足数。

## 七、与交易结果的隔离

只有在视觉答案和专家裁决冻结后，另立数值合同并通过事件、流动性、市场/板块、触发、结构止损和首障碍空间闸门，才可进入回放。回放胜率必须按方向、pattern、事件、lineage和市场背景分层。

- 识别校准的样本数不能充当完成交易数；
- `pattern_like`、专家同意或首障碍看起来有空间，不自动获得 `win_rate_eligible=yes`；
- 60% 胜率与至少 1R 仍是待检验目标；当前 validated win rate 不可计算；
- 初期约30个独立图可以暴露识别错误，但不能验证交易优势；观察到约60%胜率时，通常仍需接近100个可比、独立完成交易，才有机会把95% Wilson下界推到约50%以上。

## 八、范围边界

- 本协议只属于 PA Research；
- 不修改 Codex Trading，不从 Codex Trading 导入规则；
- 不创建量化扫描器或自动 pattern detector；
- 不连接 Execution Agent；
- 当前结论保持 `no-new-positive / validated win-rate: not-computable`，直到独立证据支持改变。

```text
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

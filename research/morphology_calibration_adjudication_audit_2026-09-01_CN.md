# 形态覆盖候选集 v1 独立盲审与裁决审计（2026-09-01）

状态：`document_status=completed / evidence_scope=visual_calibration_only / adjudication_source=independent_model_review / human_expert_status=not_performed`

## 一、结论先行

本轮完成了 16 张两年 Daily 截止图的 reviewer-first 盲审：每张图先由两名互相独立的视觉 reviewer 判断，再由未接触候选答案的第三名 adjudicator 处理分歧。32 份初审和 16 份裁决在候选答案揭示前冻结；所有记录的 `knowledge_status` 均为 `clean`，16/16 样本均为 `strict_eligible`。

这是一轮独立的**模型视觉裁决**，不是外部人工专家复核，也不是交易结果回放。它能衡量本轮读图的一致性和边界混淆，不能把模型共识升级为人类专家真值。

主要发现：

- 趋势背景、方向和 EMA gate 相对稳定；两 reviewer 的精确一致率分别为 `75.00% / 81.25% / 75.00%`；
- B leg 分类只有 `25.00%` 一致，visual family 为 `56.25%`，说明当前主要误差不在“看不见趋势”，而在回调性质和形态家族边界；
- 16 个样本中有 12 个裁决为 `both_reasonable_boundary`，只有 1 个为 `reviewers_agree`，另有 3 个需要 adjudicator 选择；因此不能报告整体识别准确率；
- 候选来源中的 H1/H2/L1/L2 标签仅 `1/8` 与盲裁决精确一致；三推候选的 family 为 `3/4` 一致；4/4 相似负控均未被升级为 `deep_reviewed`；
- 没有任何完成交易结果进入分母。`conclusion: no-new-positive`，`validated win-rate: not-computable`。

## 二、盲法与冻结顺序

1. reviewer 只看到中性编号图 `MC2-001` 至 `MC2-016`，不知道股票代码、候选 family、候选 label、未来 K 线或结果；
2. 每张图由两个独立 reviewer 完成统一字段记录，共 32 份；
3. 初审记录先冻结，再把同一张图和两份初审交给独立 adjudicator；
4. adjudicator 仍看不到候选答案，只处理 reviewer 分歧并记录 `reviewers_agree`、`both_reasonable_boundary` 或 `adjudicator_choice`；
5. 16 份裁决冻结后，才揭示隔离的候选来源标签，且明确把它当作 candidate hypothesis，不当作 ground truth；
6. 最后计算一致率、边界混淆和负控状态，不查看未来结果，不计算交易胜率。

冻结证据：

- [32 份盲审原始记录](morphology_calibration_blind_reviews_2026-09-01.json)：SHA-256 `0f290849431ed2f246be08de9526b4fa58e7453b98af21b9f6a7a5299200d160`；
- [16 份盲裁决原始记录](morphology_calibration_blind_adjudication_2026-09-01.json)：SHA-256 `101b7e6da4d0d11f04ffc5bf1e52f3bdf1efb1857d1d727a5aec8b7b1ceefa40`；
- 候选来源标签在上述两次冻结之后才揭示；隔离答案键 SHA-256 为 `bbd2a31bab4034727ebcab3061f6c7f0a5c556e1237edc9fb35b90a34a98e145`；
- [机器可读统计与混淆矩阵](morphology_calibration_metrics_2026-09-01.json)记录全部分母和逐样本比较。

候选图和 reviewer-facing README 保持答案隐藏，不反向加入裁决链接；详细候选集边界见[形态覆盖候选集 v1 审计](morphology_calibration_candidate_cohort_audit_2026-09-01_CN.md)。

## 三、两名 reviewer 的字段一致率

| 字段 | 精确一致 | 分母 | 一致率 |
|---|---:|---:|---:|
| parent_state | 12 | 16 | 75.00% |
| direction | 13 | 16 | 81.25% |
| a_leg_quality | 12 | 16 | 75.00% |
| b_leg_class | 4 | 16 | 25.00% |
| visual_family | 9 | 16 | 56.25% |
| attempt_label | 10 | 16 | 62.50% |
| three_push_variant | 10 | 16 | 62.50% |
| ema_gate | 12 | 16 | 75.00% |
| stage_1_status | 12 | 16 | 75.00% |
| selection_disposition | 11 | 16 | 68.75% |

这里的“一致”只表示两个 reviewer 写出同一枚举，不代表两者一定正确。尤其 `b_leg_class=25.00%`，说明“B 是否受控、是否过深/过晚、是否已区间化”仍需更明确的视觉锚点。

## 四、reviewer 与盲裁决的一致率

以 32 份 reviewer 记录分别对照同图 adjudication：

| 字段 | 精确一致 | 分母 | 一致率 |
|---|---:|---:|---:|
| parent_state | 28 | 32 | 87.50% |
| direction | 29 | 32 | 90.63% |
| a_leg_quality | 28 | 32 | 87.50% |
| b_leg_class | 20 | 32 | 62.50% |
| visual_family | 25 | 32 | 78.13% |
| attempt_label | 26 | 32 | 81.25% |
| three_push_variant | 26 | 32 | 81.25% |
| ema_gate | 28 | 32 | 87.50% |
| stage_1_status | 28 | 32 | 87.50% |
| selection_disposition | 27 | 32 | 84.38% |

这些数值会受到 adjudicator 从两份初审中择一或保留边界的影响，只适合作为“分歧收敛程度”，不能解释为独立准确率。

## 五、H/L 与三推边界

候选来源标签只是构造 cohort 时的假设，揭示后出现的比较如下：

| 候选来源 | 盲裁决结果 | 解释 |
|---|---|---|
| H/L family，8 张 | family 仅 1 张仍为 H/L；其余为 BOP 3、三推 3、ABC continuation 1 | 当前 H/L 候选定义过宽，突破状态、第三次尝试和普通延续容易混入 |
| H1/H2/L1/L2，8 张 | attempt 精确一致 1/8 | 不能把旧候选标签当真值或识别成功率 |
| 三推 family，4 张 | 三推 3、ABC continuation 1 | family 较稳定，但 continuation/climax、range-edge、terminal/breakout 等 variant 仍需分层 |
| 相似负控，4 张 | 0 张进入 deep_reviewed | gate 有效，但其中 3 张仍被读成 H/L/BOP-like，说明“不交易”与“不是该 family”必须分开 |

H/L attempt 的具体混淆为：`H1→H2/H3`、`H2→H2/H1`、`L1→L3/pending`、`L2→pending/L3`，每条各 1 张。最需要修订的不是强行提高 H1/H2 命中率，而是先把以下限制条件固定：

- 只有趋势与 EMA20/50 方向门槛通过后，才允许计数 H1/H2 或 L1/L2；
- 先判定是否已经突破并接受，避免把 BOP 重新贴成普通 H/L；
- 第三次有意义尝试优先进入 H3/L3/三推边界，不降格为普通 H1/H2/L1/L2；
- `selection_disposition` 独立于 `visual_family`：形态相似但位置、空间、事件或 EMA gate 不合格，仍可正确拒绝。

## 六、可用结论与禁止解释

本轮可以支持：

- 模型能够直接从两年 Daily 图中较稳定地读取大趋势、方向和 EMA 背景；
- B leg 性质、H/L 尝试计数与 H/L/BOP/三推/普通延续之间的边界仍不稳定；
- 下一轮规则优化应优先做边界卡和反例对，而不是扩大候选数量。

本轮不能支持：

- 不能声称已经获得人工专家 ground truth；
- 不能把 reviewer-to-adjudication 一致率叫作“识别准确率”；
- 不能由 16 张图推导胜率、盈亏比、入场授权或选股器性能；
- 不能因为三推 family 为 3/4 就证明三推交易有正期望。

## 七、统计与仓库边界

```text
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

本审计只属于 `PA Research only`。它不修改 Codex Trading，不创建量化扫描器，不连接 Futu/OpenD，不连接 Execution Agent，也不构成自动交易或交易建议。

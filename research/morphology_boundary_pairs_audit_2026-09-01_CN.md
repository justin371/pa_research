# 形态边界正反例对校准审计（2026-09-01）

状态：`document_status=completed / evidence_scope=curated_reused_visual_calibration / not_holdout / human_expert_status=not_performed`

## 一、结论

本轮用此前已隐藏未来的 12 张中性 Daily 图组成 6 对边界校准样本。每张图仍保留至少两年左侧背景、EMA20/50/200、原始成交量和重要高低点；6 名 Luna Max reviewer 各自只看分配到的 4 张图。每张图的逐图标签先冻结，再填写 pair contrast。24/24 份记录均为 `knowledge_status=clean`。

主要结果：

- `visual_family` 两 reviewer 精确一致 `10/12 = 83.33%`，高于前一新 holdout 的 `8/12 = 66.67%`；
- `breakout_acceptance_status` 为 `9/12 = 75.00%`；6 对中有 5 对对决定性路由差异形成语义一致；
- `b_leg_class` 仍只有 `5/12 = 41.67%`，没有改善；`attempt_label` 也只有 `5/12 = 41.67%`；
- 普通 `H_L_like` 的双 reviewer 共同正例仍为 `0/12`。只有一名 reviewer 在 `PB1-001B` 写出 `H_L_like / H2_like`，另一名把同图保留为未接受的 BOP watch；
- `PB1-004` 仍是主要失败对：reviewer C 将 A 图读成空头 ABC continuation、B 图读成区间边缘三推；reviewer D 将两图都读成不同状态的三推。

因此，成对比较对 BOP 接受、事件边界和三推分流有帮助，但没有解决 B 腿层级和普通 H1/H2/L1/L2 的可复现识别。由于本批故意复用旧图、并依据旧分歧策划，不能把 83.33% 当作独立 holdout 表现或准确率。

```text
overall accuracy: not-computable
validated win-rate: not-computable
conclusion: no-new-positive
```

## 二、冻结与证据边界

1. [校准包 manifest](calibration/morphology_boundary_pairs_v1/manifest.json)在当前 reviewer 看图前冻结，SHA-256 为 `8cfa9ce927718bd60daa6aee640f86ebab92d33c323879859b7f6c6ebc3deaed`；
2. 12 张图全部来自此前的 label-hidden、outcome-hidden、future-hidden cohort，不新增市场扫描或行情连接；
3. reviewer 不打开旧盲审、裁决、来源 manifest、未来价格、结果或 curation key；
4. [标准化盲审记录](morphology_boundary_pairs_normalized_blind_reviews_2026-09-01.json) SHA-256 为 `fa8e7251479159879fcd5320ece8cbe8f6d80dd13af6dde000e3ee9401bcd54e`；
5. [机器可读统计](morphology_boundary_pairs_metrics_2026-09-01.json)只计算 reviewer 一致性和 pair 路由差异，不计算准确率、胜率或盈亏比。

标准化记录保留全部分类枚举与每对的决定性路由摘要；它没有把旧模型 adjudication 当作答案。隔离 curation key 只说明为什么选择这些图，并明确是 hypothesis，不是 ground truth。

## 三、逐字段一致率

| 字段 | 精确一致 | 分母 | 一致率 |
|---|---:|---:|---:|
| parent_state | 8 | 12 | 66.67% |
| direction | 10 | 12 | 83.33% |
| a_leg_quality | 11 | 12 | 91.67% |
| b_leg_class | 5 | 12 | 41.67% |
| breakout_acceptance_status | 9 | 12 | 75.00% |
| lineage_status | 9 | 12 | 75.00% |
| visual_family | 10 | 12 | 83.33% |
| attempt_label | 5 | 12 | 41.67% |
| three_push_variant | 8 | 12 | 66.67% |
| ema_gate | 8 | 12 | 66.67% |
| stage_1_status | 9 | 12 | 75.00% |
| selection_disposition | 9 | 12 | 75.00% |

本表的一致只表示同一图的两名 reviewer 写出相同枚举，不表示两者正确。pair route 的 `5/6` 是对决定性差异的人工标准化语义一致，也不是精确文本一致或外部验证。

## 四、六对图真正教会了什么

| Pair | 两 reviewer 可共同保留的差异 | 仍未解决的边界 |
|---|---|---|
| PB1-001 | A 图有边界外收盘、跟随并守位；B 图仍在前高边缘等待接受 | B 图是 BOP watch 还是 H2-like |
| PB1-002 | A 图是已接受 BOP；B 图仍是长期下降背景中的 transition/三推 | B 图 B 腿是 range-like 还是 deep-late-controlled |
| PB1-003 | A 图有接受突破；B 图无突破跟随、保持第三推路径 | B 图 parent state 是 range edge 还是 open trend |
| PB1-004 | 两图都不适合直接套普通 H/L | A 图 ABC continuation versus L3；B 图 H3/L3 与方向均分歧 |
| PB1-005 | 普通边界突破必须和跳空放量事件边界分开 | 事件图 B 腿是 range-like 还是 controlled-late |
| PB1-006 | transition 中的衰竭三推与 range-edge 三推不是同一管理路径 | 区间边缘方向、attempt 与 EMA gate 仍需冻结锚点 |

最可靠的成对提示不是“两个轮廓看起来不同”，而是按顺序问：

1. 有无事前边界；
2. 是否日线收在边界外；
3. 是否有跟随或守住回踩；
4. 是否由事件跳空/异常扩张主导；
5. 未接受突破时，是否已到同一 lineage 的第三次有意义尝试；
6. 只有以上均未改写 family，才允许讨论普通 H1/H2/L1/L2。

## 五、下一步

下一轮不应继续扩大配对数量，而应专门补普通 H/L 的外部人工专家正例与 hard negative：同一开放趋势、EMA20/50 同向、强 A、小而犹豫 B、前方有空间，并由专家明确说明为什么它不是 BOP、不是第三推、不是区间重复测试。没有这种 ground truth 前，不应声称 H/L 识别成功率。

## 六、范围

本审计只属于 `PA Research only`。它不修改 Codex Trading，不创建量化扫描器或自动 pattern detector，不连接 Futu/OpenD，不连接 Execution Agent，不构成交易建议、候选授权或生产系统规则。

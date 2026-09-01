# 普通 H1/H2/L1/L2 外部专家标注标准 v1

状态：`expert-facing / label-hidden / outcome-hidden / annotation-only`

## 标注目标

本包只回答一个问题：在截止图当时，是否存在可以合理识别的普通 H1/H2/L1/L2 尝试？它不要求判断未来输赢，也不要求把每张图强行分到四个标签之一。

普通 H/L 在 PA Research 中只是 ABC continuation 内部的尝试标签，不是独立交易授权。专家必须先完成以下分流，最后才能计数：

```text
证据可用
  -> parent state 与方向
  -> 是否已经接受 BOP
  -> 是否是第三次有意义尝试 / H3-L3
  -> 是否只是区间重复测试或事件异常
  -> A、B、lineage、EMA 与空间门槛
  -> ordinary H1/H2/L1/L2 或 not_ordinary_HL
```

## 必须同时满足的普通 H/L 条件

1. `parent_state=open_trend`，不是大区间中部、混乱 transition 或高潮事件状态；
2. long 时 EMA20/50 明确上行，short 时 EMA20/50 明确下行；EMA200 只作背景，但明显冲突必须说明；
3. A leg 有方向推动，最好连续 3–4 根饱满同向实体；重叠、缓慢磨行或异常事件跳空不能直接当普通强 A；
4. B leg 必须从属于 A：K 线较小、犹豫、回撤受控，在 EMA20/50、前高/前低或既有支撑阻力附近稳定；大方向 K 线、双向宽幅轮动或反向趋势均不合格；
5. `lineage_status=same_lineage`；事件重定价、被接受的突破或结构重建会 reset 旧计数；
6. H1/L1 是回调后的第一次有意义尝试，H2/L2 是同一谱系的第二次；第三次必须转 H3/L3/三推，不得继续写普通 H2/L2；
7. 入场位置到左侧第一重要高低点或支撑阻力必须有可见空间。空间不清楚或明显不足时，即使形状相似也写 `not_ordinary_HL`；
8. 截止图当时必须能识别，不能依赖隐藏未来 K 线或事后走势解释。

## 优先排除项

如不属于普通 H/L，只选择一个最先改变路由的 `primary_exclusion`：

- `accepted_BOP`：已有事前边界、日线收盘越界，并有跟随或守住回踩；
- `third_push_H3_L3`：同一 lineage 的第三次有意义尝试；
- `range_repeat`：大区间内反复穿越、没有清楚回调终点；
- `event_or_gap`：财报/新闻式跳空、异常放量或重定价破坏普通结构；
- `EMA_gate_fail`：EMA20/50 走平、反向或方向证据冲突；
- `insufficient_space`：左侧第一障碍太近，无法覆盖结构风险；
- `A_not_directional`：A 缺少推动；
- `B_not_controlled`：B 过深、过大、失控或区间化；
- `lineage_reset`：旧计数已因状态迁移失效；
- `no_valid_direction`：没有可接受的 long/short 方向；
- `insufficient_evidence`：图本身不足以判断；
- `other`：必须写明。

排除顺序不是“哪个理由最显眼”，而是哪个理由最早阻止普通 H/L 计数。例如 accepted BOP 已成立时，优先写 `accepted_BOP`，不要继续争论它长得像 H1 还是 H2。

## 专家必须记录的证据

- `major_high_low_reading`：两年左侧最相关高点、低点或区间边界；
- `ema20_slope / ema50_slope / ema200_context`；
- `A_leg_evidence`：推动或不推动的可见理由；
- `B_leg_evidence`：受控、失控或区间化的可见理由；
- `lineage_and_attempt_evidence`：为什么是第一/第二次，或为什么计数已 reset；
- `first_obstacle_and_space`：第一障碍和空间是否足够；
- `confidence_1_to_5`：只表示本图标注信心，不是胜率。

## 禁止事项

- 不查看股票代码、截止日期、旧模型答案、旧裁决、未来 K 线、回放结果或交易盈亏；
- 不因为图在“正例包”中就假定它是正例；本包正负顺序已隐藏；
- 不把形态标签升级为交易建议、准确率或胜率；
- 不填写无法从图上直接支持的新闻原因或参与者意图。

```text
PA Research only
no Codex Trading
no quantitative scanner
no automatic pattern detector
no Futu/OpenD
no Execution Agent
conclusion: no-new-positive
validated win-rate: not-computable
```

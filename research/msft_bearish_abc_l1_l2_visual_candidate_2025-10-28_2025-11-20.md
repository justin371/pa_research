# MSFT 空头 ABC / L1-L2-like 视觉候选：2025-10-28 至 2025-11-20

状态：`pattern_like / bearish-ABC-candidate / L1-L2-like / gap-trigger-boundary / pending`

```text
contract_scope: stage_1_fast_screen
directional_bias: bear
direction: short
data_status: historical
timeframes_seen: Daily
chart_scope: partial
daily_context_window: <2y
major_high_low_review: partial
ema20_50_200_review: unavailable
a_leg_quality: unclear
b_leg_class: unclear
event_context: unknown
event_bucket: event_unverified_or_pending
sector_state: unknown
market_state: unknown
permission: unknown
first_independent_obstacle: pending
pre_entry_space_R: unknown
space_status: unknown
research_state: pattern_like
trade_state: not_authorized
gate_result: pending
```

这是第一阶段历史视觉记录，不是 `daily_candidate`：Daily 左侧窗口不足两年，事件、市场/板块、首障碍和订单几何仍待核验；`direction` 只表示观察方向，不能把后见之明或低周期补查变成授权。

## 1. 图表证据

- 标的：`US.MSFT`
- 周期：Daily；先看 `2025-09-01`–`2025-11-28` 完整窗口，再放大 `2025-10-20`–`2025-11-28`。
- 数据：Futu OpenD 历史 QFQ，收盘后读取；不是实时行情，没有下单。
- `2025-11-20` 只是标题/候选观察截止点，本文没有建立新的 pre-entry freeze；完整图表可见至 `2025-11-28` 不等于已冻结的事前证据。`2025-11-21` 及以后只能作为 title-window 后的 hindsight/path audit，不计入 `11-20` 的事前证据。
- 这是第一阶段视觉候选。它的价值是补空头方向的对照，不代表已经通过事件、订单或 R/R 审计。

## 2. 为什么看起来像空头 ABC / L1-L2

### 父级背景

`2025-10-28` 之前价格仍在高位，父级更接近上涨后的转折/过渡，而不是已经很干净的开放空头趋势。因此，后续空头结构可以先记录，但不能把它当作最纯净的趋势延续样本。

### A 腿

局部空头 A 可先看 `2025-10-28` 之后至 `2025-11-07`：

- `2025-10-28` 之后出现方向性转弱；
- `2025-10-30`、`2025-10-31` 和 `2025-11-05`–`11-07` 继续压低价格；
- 空头推进的持续性比普通的小幅回落更清楚，但 `2025-10-28` 的跳空/事件背景使 A 的纯净度下降。

### B 腿

`2025-11-10`–`2025-11-14` 出现反向反弹，最高回到约 `509.31`，但没有回到 A 起点附近。它可以先标为“反弹后段受控、但并不弱”的 B；也可能是父级过渡中的新交易区间，不能只凭形状冻结成教科书 B。

### C / L1-L2-like 尝试

`2025-11-18`–`2025-11-20` 再次向下，视觉上像 B 后的空头恢复，能够提名为 L1/L2-like 研究分支；`2025-11-21` 仅作 title-window 后的 hindsight/path audit，不计入 `11-20` 的事前证据。这里暂不决定是 L1 还是 L2：要先确认 `11-10`–`11-14` 是否属于同一回调、第一次空头尝试是否真正失败，以及是否发生了计数重置。

## 3. 第一阶段结论

| 项目 | 当前判断 |
| --- | --- |
| pattern family | `ABC-CONT? / TPB-L1-L2-like` |
| market state | 高位转弱后的过渡，随后出现空头恢复 |
| A quality | `directional-looking but event/gap-contaminated` |
| B quality | `countertrend rebound / late-controlled-pending` |
| H/L count | `L1/L2-like`，计数未冻结 |
| signal quality | `2025-11-18` 方向性较强，但需低周期核对 |
| visual reason | 空头推进、反弹未回到 A 起点、随后再次走低 |
| main uncertainty | 父级是否已转空、事件影响、B 是否是新区间、L1/L2 计数和订单成交 |
| stage-1 status | `pattern_like / gap-trigger-boundary / pending` |

## 4. 订单与后见之明边界

如果把 `2025-11-17` 的低点约 `500.79` 作为 sell-stop，`2025-11-18` 开盘约 `491.32`，已经跳过原触发价。因而不能说“在 `500.79` 正常成交后一路下跌”。原始 stop 分支必须重订，或者等待新的反弹/新的 L 级别设置。

这不会抹掉日线上的空头形态候选；它只说明 `morphology-positive` 与 `order-valid` 是两个不同字段。事件、跳空、父级过渡也必须单独保留，不能把它当成普通空头 ABC 正例。

## 5. 下一轮若值得深入

1. 核对财报/事件日期，判断 A 是否属于事件驱动；
2. 用 60m/15m 重建 `2025-11-18` 后是否出现新的、没有跳过的 L 触发；
3. 先冻结入场前左侧主要支撑，再讨论结构止损和首障碍；
4. 判断它是趋势恢复、区间顶部失败，还是高位反转候选；
5. 只有这些问题清楚后，才讨论 MM 或粗略 R/R。

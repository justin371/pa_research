# JNJ 多头 H1-like：视觉上清楚、第一阻力过近（2025-09-18–2025-10-08）

状态：`pattern_like / bullish-H1-like / first-obstacle-crowded / valid_no_trade / event-context-pending`

## 1. 研究目的

这是一个第一阶段视觉候选，不是已经验证的交易规则。它用来训练助手识别：

> 方向性上涨 → 单日深回调并快速收回 → 第一次多头尝试（H1-like）

它的形态比“碰到 EMA 就买”清楚，但触发上方有几乎立即可见的前高，因此把“形态像”和“值得交易”分开。

## 2. 数据与可见范围

```text
symbol: US.JNJ
timeframe_seen: Daily / 60m / 15m
data_source: Futu OpenD historical QFQ
data_status: historical / after-close; not live
review_window: 2025-09-18–2025-10-08
sector_context: XLV
event_context: pending; must be checked before any real use
```

## 3. 视觉结构

### 背景与 A 腿

- `2025-09-18` 日内低点约 `170.88`，随后价格逐步恢复；`2025-09-30`–`2025-10-03` 的推进较有方向性，`2025-10-03` 高点约 `186.52`。
- 这条上涨可以作为 `ordinary-to-directional A` 或过渡背景中的局部 A；它不是完全无争议的教科书强 A，因为前段包含过渡与多次小回调。
- 因此第一轮可以标为 `pattern_like`，但不能只凭后面的上涨结果把 A 追认成强趋势 A。

### B 回调与信号 K

- `2025-10-06` 先出现小幅回落；`2025-10-07` 开盘约 `180.61`，日内最低约 `179.79`，随后强力收回，收盘约 `185.64`，高点约 `185.97`。
- 这根 K 线有明显下影和接近高位的收盘，属于视觉上质量较好的多头恢复 K；但它的日内下探很深，B 更准确地写成 `deep-but-position-controlled-B`，不能直接称为浅 B。
- 这段可以先记为 `H1-like`：没有把 10-07 之后的上涨倒灌成已经知道会成功，只描述当时第一次恢复尝试的外形。

## 4. 低周期触发顺序

- `2025-10-07` 60m 在开盘阶段先探到约 `179.79`，随后在中午前后恢复到 `185.97` 附近；收盘仍约 `185.64`。
- 若在 `2025-10-07` 高点约 `185.97` 上方挂 buy-stop，`2025-10-08` 开盘约 `185.62`，没有跳过原触发；`10-08 09:45` 的 15m 高点约 `186.25`，价格顺序上可以重建原 stop 触发。
- 这里的触发是“存在的”，但触发存在不等于交易值得做；必须继续看第一道独立阻力。

## 5. 止损、第一阻力与粗略空间

- 结构止损研究区应放在 `2025-10-07` 深探低点约 `179.79` 下方，而不是为了改善 R/R 放在信号 K 内部。
- 触发约 `185.97` 上方，入场前已经可见的 `2025-10-03` 高点约 `186.52` 只有约 `0.55` 的上行空间；相对于结构风险，这远低于基本的 `1R` 空间要求。
- 所以即使信号 K 很漂亮、10-08 后来继续上行，也不能把这笔日线新仓写成合格交易。第一阻力优先于任何远端 MM；MM 只能作为后续目标研究，不能取消近端高点。
- `XLV` 在 `2025-10-07`–`10-08` 只表现为横向/轻微支持，不能提供特别强的板块许可。

## 6. 结论

```text
visual_pattern: bullish H1-like / ABC candidate
A_quality: ordinary-to-directional; not fully clean
B_quality: deep but recovered at a meaningful location
signal_quality: visually good long-tail recovery bar
order_branch: buy-stop above 2025-10-07 high; no opening skip
structural_stop: below 2025-10-07 low zone
first_obstacle: 2025-10-03 high around 186.52
space: blocked / far below 1R
current_status: pattern_like / valid_no_trade
```

这个案例的学习价值是：**优质信号 K 可以确认局部买压回来了，但不能抹掉触发上方几乎贴着的主要高点。** 它应保留在视觉边界库，不作为条件正向样本；若以后只做短线、采用更窄且不同的止损，必须另建一个低周期交易合同，不能与日线结构分支混算。

## 7. 尚未冻结

- 财报与其他事件背景尚未核对；
- EMA20/EMA50 的精确位置没有作为入场充分条件；
- MM/AB=CD 未作为决定因素；
- 这只是一个独立视觉案例，不能推出胜率。

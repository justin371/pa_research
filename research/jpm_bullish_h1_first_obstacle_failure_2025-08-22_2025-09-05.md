# JPM 多头 H1-like：板块顺势但首阻力拥挤、跟随失败（2025-08-22–2025-09-05）

状态：`pattern_like / bullish-H1-like / sector-aligned-at-entry / first-obstacle-blocked / follow-through-failure / valid_no_trade / event-context-pending`

## 1. 研究目的

这个案例用来训练助手识别另一种常见情况：

> 上涨背景 → 两日回调 → 第一次多头恢复看起来很强 → 触发后没有持续跟随

它不是把“2025-09-05 大跌”倒灌成预测，而是先按 2025-09-04 当时能看到的结构判断入场是否值得；后面的强反转只用来审计跟随是否兑现。

## 2. 数据与可见范围

```text
symbol: US.JPM
timeframe_seen: Daily / 60m / 15m
data_source: Futu OpenD historical QFQ
data_status: historical / after-close; not live
review_window: 2025-08-22–2025-09-05
sector_context: XLF
event_context: pending; must be checked before any real use
```

## 3. 当时可见的视觉结构

### A 腿与 B 回调

- `2025-08-22`–`2025-08-29` 延续上涨，`08-29` 高点约 `297.26`，收盘约 `295.76`；父级上涨背景比 JNJ 案例更清楚。
- `2025-09-02` 低点约 `288.97`，收盘恢复到约 `294.07`；`09-03` 再次下探至约 `290.82`，高点约 `294.93`，收盘约 `293.89`。
- B 没有跌破 `08-22` 的局部低点，仍可视为母腿内的深回调；但它不是浅 B，而是 `deep-but-controlled-B` 的候选。买压在 09-04 之前重新出现，但回调并非完全没有反向力度。

### H1-like 信号

- `2025-09-04` 日线高点约 `298.72`、收盘约 `298.12`，实体和收盘位置都偏强。
- 若按第一次恢复的定义，在 `09-03` 高点约 `294.93` 上方挂 buy-stop，`09-04 09:45` 的 15m 高点约 `295.13` 已经触发，之后价格逐步推进到 `298` 附近。
- 因此它在视觉和订单顺序上可以先记为 `H1-like`；不能因为次日失败，就否定 09-04 当时的局部买压恢复。

## 4. 订单分支必须分开

### H1 stop 分支

- 研究触发：`294.93` 上方 buy-stop；
- `09-04` 盘中触发，没有开盘跳过；
- 结构止损研究区：`288.97` 下方，不能放在信号 K 内部；
- 入场前第一阻力：`08-29` 高点约 `297.26`；
- 触发到第一阻力约 `2.33`，相对结构风险约 `5.96`，只有约 `0.39R`，因此日线新仓应跳过。

### 等待突破前高的分支

- 如果把 `297.26` 上方作为新的触发，这已经更接近突破交易，而不是前一个 H1 stop 合同；不能把它和 `294.93` 的 H1 分支混算。
- `09-05` 开盘约 `297.95` 已经越过 `297.26`，所以原价 stop、开盘接受和回测 limit 必须分开。当天最高约 `299.42` 后快速转弱，说明“突破触发”也没有自动获得跟随。

## 5. 失败与板块背景

- `09-04` 当天 XLF 从约 `52.87` 推进至约 `53.23`，入场时板块方向是支持的；不能把失败简单归因于明显的板块逆势。
- `09-05` JPM 先冲到约 `299.42`，随后逐步跌至约 `288.79`；这使 09-04 的局部恢复失去跟随，并跌回 B 低点附近。
- 这不是“形态从未存在”，而是一个 `follow-through-failure`；同时，第一阻力在入场前已经足够近，所以即使没有后续大跌，日线 H1 也不应按正常新仓执行。

## 6. 结论

```text
visual_pattern: bullish H1-like / ABC candidate
A_quality: directional and parent trend clearer than JNJ
B_quality: deep but remained inside parent structure
signal_quality: strong daily recovery and 15m trigger sequence
order_branch: H1 buy-stop above 2025-09-03 high; separate breakout branch above 2025-08-29 high
structural_stop: below 2025-09-02 low zone
first_obstacle: 2025-08-29 high around 297.26
space: blocked (~0.39R on the H1 branch)
follow_through: failed on 2025-09-05
current_status: pattern_like / valid_no_trade
```

学习重点是：**板块顺势、信号 K 漂亮、低周期确实触发，仍然不能取消入场前已经可见的第一阻力；如果改成等待前高突破，那就是另一种订单和另一种 pattern。** 这个案例不作为正向样本，但比单纯的“没有触发”更能训练助手理解订单分支和跟随失败。

## 7. 尚未冻结

- 财报和其他事件背景尚未核对；
- 不能由单次失败推出 H1 的胜率；
- 远端 MM/AB=CD 没有资格覆盖首阻力；
- 若研究短线分支，必须另定低周期止损，不能套用日线结构结论。



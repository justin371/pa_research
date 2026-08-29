# COST 多头 ABC / H2-like：普通 A、深 B、低周期触发与首阻力边界（2025-04-21–2025-05-16）

状态：`pattern_like / ordinary-directional-A / deep-B / bullish-H1-H2-like / low-cycle-triggered / first-obstacle-borderline / sector-aligned / valid_no_trade / event-context-pending`

## 1. 研究目的

这个案例用来补充 NVDA、JNJ、JPM 之外的普通多头样本：图形可以先看起来像上涨 A → 回调 B → H2-like 恢复，但不因为低周期确实触发就自动升级为可交易正例。

## 2. 数据与范围

```text
symbol: US.COST
timeframes_seen: Daily / 60m / 15m
data_source: Futu OpenD historical QFQ; after-close; not live
data_status: historical
chart_scope: unavailable
daily_context_window: unavailable
review_window: 2025-04-21–2025-05-16
sector_context: XLP; market reference SPY
event_context: pending; not used as positive evidence
```

本轮仍以完整日线外形为第一层，低周期只用于验证是否值得保留，不是量化扫描或真实交易。

## 3. 第一轮视觉结构

### A 腿：普通、方向性可见，但父级带过渡色彩

从 `2025-04-21` 的低点约 `934.98` 开始，价格在 `04-22`–`05-02` 逐步恢复到约 `1010.69` 的高点。推进不是每一天都强，但高低点整体抬高，收盘也逐渐站回上涨均线附近。

它可以先标成 `ordinary-directional-A`，而不是 `strong-looking-A`。更大的左侧背景仍受到 4 月市场冲击影响，因此父级更接近“过渡后恢复”，不是最干净的开放趋势。

### B 腿：深、时间较长，后段才出现稳定

`2025-05-05`–`2025-05-14` 反复回落，`05-14` 低点约 `983.41`；`05-13` 的范围也较大，卖压不能简单描述成持续萎缩。

因此 B 先记为 `deep-B / late-stabilizing`。它没有跌回 `04-21` 的母腿低点，但相比浅而受控的 B，应该降低优先级，更偏向等待第二次尝试。

### H2-like 恢复

`2025-05-15` 先下探到约 `975.95`，随后逐步收回并收在约 `1003.22`；这个“先测试、更深下探、再强力收回”的顺序，视觉上更像 B 后的 H2-like 恢复，而不是简单的一根阳线。

XLP 在 `05-15` 同步走强，SPY 也偏强，所以板块和大盘没有直接给出逆向否决；这只是 META 的许可项，不替代位置与空间。

## 4. 低周期订单分支

### 分支 A：以 `05-14` 高点作为 setup bar

- 研究触发：`05-14` 高点约 `992.68` 上方 buy-stop；
- `05-15` 开盘约 `985.53`，没有跳过原触发；
- `05-15 10:15` 的 15m 高点约 `994.95`，可以重建越过触发位；
- 触发前后的结构低点应看 `05-15` 的约 `975.95`，不能用更小的 15m 低点把风险压窄。

这是一个真实可重建的低周期触发，但触发真实不等于空间足够。

### 分支 B：以 `05-15` 日线高点作为新的 setup bar

如果等到 `05-15` 高点约 `1006.72` 上方再挂日线 buy-stop，`05-16` 盘中才越过该区域；此时 `05-02` 高点约 `1010.69` 已几乎贴着触发，订单更接近突破分支，不能与前一个 H2-like 合同合并。

## 5. 第一阻力与粗略空间

触发前最重要的左侧高点是 `2025-05-02` 的约 `1010.69`，它比远端 MM 更优先。

| 分支 | 研究触发 | 结构风险参考 | 第一阻力 | 粗略判断 |
| --- | ---: | ---: | ---: | --- |
| `05-14` 高点上方的 15m H2-like | `992.68` 附近 | `975.95` 下方 | `1010.69` | 约 `0.8R` 左右，属于边界，偏向跳过 |
| `05-15` 高点上方的日线分支 | `1006.72` 附近 | `975.95` 下方 | `1010.69` | 首阻力几乎覆盖触发，空间明显不足 |

所以 COST 的结论不是“形态不成立”，而是：**形态可以保留为 pattern_like，低周期也可以触发，但第一阻力把它降为 valid no-trade。**

## 6. 当前结论

```text
visual_pattern: bullish ABC continuation / H1-H2-like
parent_state: transition-to-uptrend rather than clean open trend
A_quality: ordinary-directional
B_quality: deep and late-stabilizing
count: H1/H2-like; exact count not frozen
signal_quality: 05-15 recovery is visually useful, with a deep test first
order: 05-14 high stop and 05-15 high stop are separate contracts
low_cycle: 05-15 10:15 15m can reconstruct the earlier trigger
first_obstacle: 05-02 high around 1010.69
space: borderline for the earlier branch, blocked for the later branch
current_status: pattern_like / valid_no_trade
```

## 7. 可迁移结论

- 普通 A 不是自动排除，但应优先等待 H2，而不是把 H1 当成高质量信号；
- 深 B 后出现“先下探、再收回”的 K 线，可以进入 H2-like 候选，但必须说明 B 前段卖压并不弱；
- 低周期触发、板块顺势和信号 K 质量都不能取消入场前可见的主要高点；
- `05-14` setup bar 与 `05-15` setup bar 是两份不同的订单合同，不能用后续上涨合并统计；
- 这正是视觉助手应该快速筛出的边界：图形值得看，但不值得为了追求一个交易而压窄止损。

## 8. 尚未冻结

- 财报和其他事件背景尚未独立核对；
- A 的起点可能采用更大或更晚尺度，当前不冻结唯一 ABC 锚点；
- 不把 `0.8R` 边界升级为固定阈值，也不把本案例移交 Codex Trading。

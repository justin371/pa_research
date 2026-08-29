# NVDA 多头 ABC / H1-like：触发分支含糊与首阻力拥挤（2025-04-21–2025-05-08）

状态：`pattern_like / strong-looking-A / deep-but-late-controlled-B / bullish-H1-like / sector-aligned / trigger-branch-ambiguous / first-obstacle-blocked / valid_no_trade / event-context-pending`

## 1. 研究目的

这个案例不是为了证明 NVDA 可以交易，而是训练助手在完整图表上先识别一个清楚的多头外形，再检查：

1. H1 的 setup bar 到底是哪一根；
2. 低周期是否真的越过了触发位；
3. 触发后的第一道左侧阻力是否已经把空间堵住。

它说明“视觉上很强”与“订单合同清楚、空间足够”必须分开。

## 2. 数据与可见范围

```text
symbol: US.NVDA
timeframes_seen: Daily / 60m / 15m
data_source: Futu OpenD historical QFQ; after-close; not live
data_status: historical
chart_scope: unavailable
daily_context_window: unavailable
review_window: 2025-04-21–2025-05-08
sector_context: SMH; market reference SPY
event_context: pending; not used as positive evidence
```

本轮仍是视觉优先研究，不是量化扫描，也没有真实下单。

## 3. 第一轮视觉结构

### 父级与 A 腿

`2025-04-21`–`2025-05-02` 可以先看作上涨背景中的方向性 A：

- `04-21` 低点约 `94.91` 后，价格连续抬高；
- `04-23`–`04-25` 买压明显增强，收盘多靠近高位；
- `05-01`–`05-02` 再次推向约 `115.24` 的高点。

这不是把每一天都定义成独立腿，而是把它作为一个强-looking、方向性清楚的母腿候选。A 的起点仍可按更大尺度调整，不需要在第一轮冻结。

### B 回调

`2025-05-05`–`2025-05-06` 形成短时间、但幅度不算浅的回调：

- `05-05` 仍在高位附近震荡；
- `05-06` 低点约 `110.67`，盘中卖压明显，但收盘重新回到约 `113.38`；
- B 没有破坏 `04-21` 以来的上涨父级，后段出现稳定和收回。

因此 B 可先标成 `deep-but-late-controlled-B`，不能偷换成“全天都很弱”的浅回调。它值得继续看，但优先级低于浅而干净的 B。

### H1-like 恢复

`2025-05-07` 高点约 `117.52`、收盘约 `116.90`，恢复力度明显，视觉上像 B 后第一次有效的多头尝试，即 `H1-like`。

SMH 在 `05-07`、`05-08` 同步走强，SPY 也没有给出明显逆向背景，所以板块/市场过滤没有直接否决这个视觉候选。

## 4. 订单合同不能混在一起

### 分支 A：把 `05-06` 当 setup bar

- 研究触发：`05-06` 高点约 `114.58` 上方 buy-stop；
- `05-07` 盘中 15m 价格后来越过该位置，顺序上可以重建触发；
- 但触发发生在一个很大的晚盘 15m 推进中，精确成交、滑点和“先触发后接受”的过程不能从这份粗周期数据中假装确定；
- 结构止损参考 `05-06` 低点 `110.67` 下方，不能为了改善 R/R 任意压到晚盘小 K 线内部。

触发前已经可见的最近独立阻力是 `05-02` 高点约 `115.24`。从 `114.58` 到 `115.24` 只有约 `0.66`，相对约 `3.9` 的结构风险仅约 `0.17R`。所以这个 H1 分支即使真实触发，也应因首阻力过近而跳过。

### 分支 B：把 `05-07` 当新的日线 setup bar

- 研究触发：`05-07` 高点约 `117.52` 上方 buy-stop；
- `05-08` 开盘约 `118.09`，已经跳过原触发价；
- 这不能记录成在 `117.52` 正常成交，而应另列为开盘接受、重订或等待回测的分支；
- 这个分支已经不是分支 A 的 H1 合同，不能把两者的 R/R、成交和结果合并。

分支 B 可能在强趋势里继续走，但它必须重新回答成交价、结构止损和首障碍，不能因为后面继续上涨就把原 H1 订单事后改写成成功交易。

## 5. 当前结论

```text
visual_pattern: bullish ABC continuation / H1-like
parent_state: upward trend candidate, not obvious range-middle
A_quality: strong-looking and directional
B_quality: deep but late-controlled
signal_quality: 05-07 daily recovery is visually strong
sector_context: SMH aligned at the visual recovery
order_branch: 05-06 high trigger and 05-07 high trigger are separate contracts
first_obstacle: 05-02 high around 115.24 for the earlier H1 branch
space: blocked for the earlier branch; later gap-reprice branch pending
current_status: pattern_like / valid_no_trade
```

## 6. 学习重点

- 第一轮可以很快把这个图形标为 `pattern_like`，不需要先把 A、B 和价格量到小数点；
- `05-07` 的强恢复不能自动解决 `05-06` setup bar 上方很近的前高；
- 低周期“后来越过了触发位”和“有足够空间交易”是两个问题；
- 以 `05-07` 为新 setup bar 后，开盘跳过会产生新的订单分支，不能与原 H1 混算；
- 这类案例最适合训练 PA 助手的筛选顺序：先识别像不像，再决定是否值得做订单审计，最后才看目标和管理。

## 7. 尚未冻结

- `05-07` 晚盘大幅 15m 推进的精确触发路径和滑点需要更细数据才能复核；
- 财报及其他事件背景尚未独立核对，因此不把它升级为条件正向样本；
- 不能由 `05-08` 之后的走势反推 `05-07` 的原始 H1 合同应当执行；
- 不把这个案例转成固定数值阈值或 Codex Trading 规则。

# COST 多头 H1-like：优质信号 K，但第一阻力贴近与开盘跳过边界（2024-05-13 至 2024-05-16）

状态（历史观察；非已成交订单）：`pattern_like / strong-looking-A / controlled-after-first-pressure-B / bullish-H1-like / low-cycle-price-observation / first-obstacle-crowded / opening-path-unproven / sector-mixed / event-context-pending / valid_no_trade`

## 1. 研究目的与数据

- 标的：`US.COST`；
- 周期：完整 Daily 背景，再用 `2024-05-15`–`05-16` 的 15m 核对触发顺序；
- 数据：Futu OpenD 历史 QFQ，收盘后读取；不是实时行情，没有下单；
- 目的：记录一个“形态和信号 K 都像，但第一阻力几乎贴着触发位”的视觉边界，不把后续上涨倒灌成入场依据。

## 2. 完整图表上的 A、B、H1-like

### A 腿

从 `2024-05-02` 附近约 `711.78–725.38` 的区域开始，价格连续推进到 `2024-05-10` 高点约 `777.52`。中间 `05-03`、`05-06`、`05-07`、`05-09` 多次收在高位，视觉上可以先记为 `strong-looking-A`。这仍是人工判断，不冻结为固定涨幅或 K 线数量。

### B 腿

`2024-05-13` 从高点约 `779.78` 回落到低点约 `764.08`，`05-14` 再下探至约 `761.95`，但没有破坏整个上涨背景。第一天反向压力很强，第二天波动收窄，因此更准确的标签是 `controlled-after-first-pressure-B`，不是“浅 B”。

### C / H1-like

`2024-05-15` 开盘约 `768.96`，最低也约 `768.96`，最高约 `779.96`，收盘约 `777.37`。它是一个实体较强、收盘靠近高位的多头信号 K，视觉上可作为 B 后第一次恢复的 `H1-like`。但信号 K 的质量只说明方向反应，不能替代空间审计。

## 3. 订单与低周期顺序

- `05-15` 收盘后的 Daily 高点约 `779.96`，才可以作为假设的 **Daily signal-high contract** 的 signal-high；Daily K 未收盘前不能据此冻结合同，也不能从 15m 观察推导激活时间；
- `05-15` 的 15m 在约 `14:15–14:30` 重新越过 `779.78–779.96`，这里只是 `intraday observation`，可核对价格先后，但不证明 Daily signal-high contract 已激活或已有订单；
- `05-16` 开盘约 `782.08`，已经高于原 `779.96` 触发参考。只有在入场前已冻结 `gap_policy: skip` 时，才可把这个次日开盘分支标为 `opening-skip`；本记录没有冻结该 policy，因此原始成交仍是 `unproven`，开盘重订是另一份 `reprice` 合同，不能声称已有订单；
- 不能因为 `05-16` 后继续上涨，就把原 buy-stop 写成已经按理想价成交。

## 4. 第一阻力、结构止损与 R/R

### 第一独立障碍

触发前可见的最近阻力就是 `05-13` 高点约 `779.78`，而 `05-10` 高点约 `777.52` 也在同一高点簇内。研究触发约 `779.96` 已经位于这个阻力簇边缘，第一段可见空间几乎为零。这里应直接判为 `first-obstacle-crowded`，而不是等 MM 或后续新高来挽救交易几何。

### 结构止损

如果研究 H1-like 的日线结构，止损应观察 `05-14` 低点约 `761.95` 下方并留缓冲；用 15m 信号 K 的小低点会制造不真实的窄风险。无论采用哪种合理结构止损，触发价上方的第一阻力都已经先否定了直接入场的空间。

### R/R 判断

本案例不冻结精确 R/R，因为第一独立阻力几乎就在触发位，首段空间不足 `1R`，实际应标为 `valid_no_trade`。`05-16` 的高点约 `794.68` 只能作为后续路径审计，不能回写为 `05-15` 当时已知的目标。

## 5. 板块与事件

- `XLP` 在 `05-15` 收盘约 `72.81`，相对 `05-14` 约 `72.76` 基本横向，没有给出清楚的消费必需品板块顺势确认；因此标记 `sector-mixed`；
- 财报/重大事件日期在本案例中没有独立核验，保留 `event-context-pending`；
- 板块和事件即使全部通过，也不能改变第一阻力贴近这一核心结论。

## 6. 当前判断

| 项目 | 当前判断 |
| --- | --- |
| market state | 强上涨背景中的短 B 后第一次恢复 |
| A quality | `strong-looking-A` |
| B quality | 第一天下压较强、第二天收窄；`controlled-after-first-pressure` |
| H/L count | `05-15` bullish H1-like；不把后续上涨倒灌为 H2 |
| signal quality | Daily 实体和收盘较好；15m 价格观察顺序可核对，不是冻结订单触发证明 |
| order | 未冻结 `gap_policy`；`05-16` 开盘越过 `779.96`；只有 `gap_policy: skip` 才是 `opening-skip`，否则保留 `unproven`/`reprice` 分支，不声称已有订单 |
| structural stop | `05-14` 低点 `761.95` 下方的结构观察区 |
| first obstacle | `05-13`/`05-10` 高点簇 `777.52–779.78`，贴近触发 |
| tradeability | 第一段空间不足，直接日线入场 `valid_no_trade` |
| status | `pattern_like / first-obstacle-crowded / opening-path-unproven / sector-mixed / valid_no_trade` |

## 7. 可复用结论

1. 优质信号 K 只能提高形态层的可信度，不能取消第一阻力；
2. 形态上的 H1-like 与交易上的“值得买”必须分栏记录；
3. 触发位被次日开盘越过时，只有预先冻结 `gap_policy: skip` 才能标记 `opening-skip`；否则精确 stop 的成交保持 `unproven`，开盘重订和放弃交易是独立分支；
4. 后续价格走得很远，不会把入场前已经拥挤的第一障碍变成事前可知的宽阔空间；
5. 这是视觉助手应快速筛出的 `pattern_like but no-trade` 样本，不是已验证规则或交易建议；保留原始价格观察，`no-new-positive`。

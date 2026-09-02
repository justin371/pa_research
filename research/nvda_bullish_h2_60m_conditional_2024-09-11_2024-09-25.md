# NVDA 多头 H2 视觉与低周期条件候选：2024-09-11 至 2024-09-25

## Canonical historical-entry boundary（2026-08-30）

```text
contract_scope: historical_context_only
data_source: Futu OpenD historical QFQ Daily plus historical 60m/15m review
data_status: historical
as_of_time: 2024-09-24 historical decision cutoff; original query timestamp unavailable
timezone: unavailable_in_original_log
session_state: historical_close
timeframes_seen: Daily / 60m / 15m
chart_scope: partial
daily_context_window: <2y
major_high_low_review: partial
ema20_50_200_review: unavailable
parent_state: open_trend
direction: long
lineage_status: pending
state_transition: none
order_branch: observation_only
actual_fill_or_open_skip: not_applicable
structural_stop: pending
structural_invalidation: pending
first_independent_obstacle: pre-entry visual resistance near 120.6; 121.6 is post-trigger path audit; not frozen
pre_entry_space_R: unknown
space_status: unknown
rough_R_R: unknown
research_state: research_positive_conditional
trade_state: not_authorized
gate_result: conditional
handoff_status: research_only
```

本块只固定 H2、深但后段受控 B 和低周期条件候选的历史范围；不激活
`primary_pattern`/`internal_label`，不把低周期假设或后续走势变成日线成交/统计结果。

## 研究状态

这是一个比单纯“看起来像”更进一步的条件候选，但仍不是已验证规则或真实交易记录。重点是把日线结构、60m/15m 触发、宽结构止损和窄低周期止损分开。

- 标的：NVDA；
- 窗口：`2024-09-11`–`2024-09-25`；
- 数据：Futu OpenD 历史 QFQ 的 Daily、60m、15m；收盘后读取，不是实时行情；
- 板块参考：SOXX 截止点同步方向 pending；原始记录含截止点后的路径观察；
- 当前标签：`research_positive_conditional / bullish-H2 / deep-but-late-controlled-B / low-cycle-trigger-window-observed / daily-space-borderline / event-check-pending / fill-unproven`。

## 1. 完整背景与 A/B

在 `2024-09-11`–`2024-09-12`，价格从约 `107`–`109` 区域快速推进到约 `120.6`，实体、收盘位置和连续跟随都较清楚，可以先标为 `strong-looking-A`。这不是把后面的上涨结果倒灌成 A，而是截至 `09-12` 收盘时已经能看到方向性推进。

随后 `2024-09-13`–`09-18` 出现明显反向卖压，最低约 `113.0`。B 并不浅，不能写成“弱回调”；但它在前一段上涨的结构支撑附近止跌，且 `09-19` 出现第一次向上尝试：

- `09-19` 反弹到约 `119.5`，没有突破 `09-12` 的约 `120.6` 高点；
- `09-20`–`09-23` 再次回到约 `114.7`，形成第二次更有意义的尝试条件；
- 因此 `09-24` 的上破可以先标为 H2，而不是把 `09-19` 之后的每一根阳线都当成新的计数。

更准确的 B 标签是 `deep-but-late-controlled-B`：前段卖压不弱，但后段在 `113–115` 支撑簇附近止住，并出现第二次尝试。

## 2. 触发前可知的订单分支

`2024-09-23` 的高点约 `116.81` 在 `09-24` 开盘前已经可见。`09-24` 没有直接跳空越过该触发位：

- `09-24 10:30` 约 O`116.33` / H`117.43` / L`115.66` / C`115.80`，在现有记录中是最早已见越过 `116.81` 的 K 线窗口；价格越过不能证明订单激活、实际成交或准确 fill clock；
- `09-24 11:30` 约 H`117.27` / L`115.20` / C`117.20`，重新收回并越过 `116.81`，属于 recovery confirmation/new branch，不应写成原始 buy-stop 的首次触发时刻；
- `09-24 12:30` 出现更强的方向性扩张，最高约 `121.43`。

因此可以记录两个不同合同：

1. **原方向确认分支**：在 `116.81` 上方挂 buy-stop；`10:30` 是现有记录中最早已见越过的 K 线窗口，但价格越过不能证明订单激活，actual fill 未知；`11:30` 只能记为 recovery confirmation，不能把它当原始 stop 的 first fill；
2. **更保守的低周期分支**：等 `11:30` 信号 K 高点约 `117.27` 上方再用 buy-stop，成交更晚但确认更清楚。

这两种入场不能混算，也不能用 `09-25` 的高点倒推原订单本来就必然成交。

## 3. 止损与第一阻力

### 宽结构（日线/大级别）假设

- 支撑簇：约 `113.0–115.2`；`09-18` 低点和 `09-23` 的测试可作为原 `116.81`/`10:30` 分支此前已知的背景。`09-24 11:30` 信号 K 的低点约 `115.2` 只有在该信号完成后才能作为新低周期分支的参考，或作为后验观察，不能倒灌为原分支的事前止损依据；
- 原 `116.81`/`10:30` 分支的结构止损：若交易理由是日线 ABC/H2，只使用此前已知支持和原研究假设，止损应放在约 `112.5` 附近的失效区域；不能用信号完成后才出现的 `115.2` 或 `114.8` 改写原分支；
- 从约 `116.8` 到约 `112.5` 的风险约 `4.3`；
- 触发前第一主要阻力是 `09-12` 高点约 `120.6`；到 `120.6` 的空间约 `3.8`，所以日线宽止损只有约 `0.9R`，属于边界而不是理想波段。`09-24` 当日约 `121.6` 的阻力簇属于触发后的路径审计，不纳入 canonical first obstacle 或入场时空间。

### 低周期假设

如果明确把交易定义为 `11:30` 信号完成后的 `60m/15m` 支撑反应延续，而不是日线结构反转，才可以把该新分支的信号 K 低点约 `115.2` 外侧作为窄止损参考，例如约 `114.8` 附近；这不是原 `116.81`/`10:30` 分支的事前合同。

- 原 `116.8` 入场、约 `114.8` 研究止损、到 `120.6` 约 `1.9R` 的组合，是把早入场与 `11:30` 之后低点混在一起的后验混时几何，不是可冻结合同，不能继续作为低周期分支的论据；
- 若单独重冻结 `11:30` 新分支，可研究 `117.27` 上方 buy-stop、约 `114.8` 止损和 `120.6` 第一阻力，粗略约 `1.35R`；这只是条件假设，实际成交仍未证实，且需重新完成事前证据、事件和订单审计；
- 但这不是日线止损的替代品，而是另一笔低周期交易假设；若价格重新接受到支撑簇下方，窄止损路径失效。

因此本例的结论是：**日线直接交易空间边界；只有在 `11:30` 后的 `117.27` 新合同能够重新冻结且通过各项核验时，低周期确认分支才值得继续研究，不能用后验混时的 `1.9R` 窄止损支持它。**

## 4. 信号质量与板块

- `09-24 11:30` 先下探 `115.2` 再收回并越过前一日高点，符合“测试后收回”的优质候选外观；
- `12:30` 的强扩张提供了跟随，但它属于触发后的证据，不能提前写成入场理由；
- SOXX 从 `09-11` 到 `09-13` 明显上行，`09-18` 回调后 `09-19`–`09-25` 的走势保留为历史路径观察；其中 `09-25` 的重新走强发生在 `09-24` 截止点之后，不能计入 `09-24` 的市场、板块或 META 确认。带时间戳的同期盘中板块证据仍待核验，板块支持保持 pending；
- 财报/事件日期尚未在本文件中独立核验，所以事件过滤仍标为 `event-check-pending`，不把该样本写成无事件基准。

## 5. 事后过程审计（不倒灌）

触发后 `09-25` 最高约 `124.75`，超过了前面的 `120.6–121.6` 阻力簇。这个结果说明候选的低周期路径值得研究，但不能把后续延伸改写成入场前必然知道的目标，也不能用它证明该类 H2 已经有稳定胜率。

## 6. 当前可复用结论

1. 深 B 不自动否决 H2，但必须把它标为“前段强、后段受控”，不能与浅 B 混为一类；
2. H1 失败和 H2 成立，需要有真正的第二次位置测试，而不是连续两根阳线；
3. 日线结构止损与 15m/60m 窄止损代表不同交易 thesis，不能用窄止损把日线首障碍人为做得漂亮；
4. 原触发没有被开盘跳过时，stop 分支可以独立审计；后续强跟随只作为过程结果；
5. 在进入真实规则前，仍需核对事件日期、更多同类样本和失败分支。

# NFLX 空头 ABC / L1-like：强方向 A、深但受控 B、无缺口触发与首支撑空间（2025-02-14 至 2025-03-28）

状态：`pattern_like / research_positive_conditional / strong-looking-A / deep-but-controlled-B / L1-like / no-gap-trigger / first-obstacle-space-positive / sector-aligned / earnings-filter-passed / pending`

## Canonical historical-entry boundary（2026-08-30）

```text
contract_scope: historical_context_only
data_source: Futu OpenD historical QFQ Daily plus historical 60m/15m review
data_status: historical
as_of_time: 2025-03-28 historical decision cutoff; original query timestamp unavailable
timezone: unavailable_in_original_log
session_state: historical_close
timeframes_seen: Daily / 60m / 15m
chart_scope: partial
daily_context_window: <2y
major_high_low_review: partial
ema20_50_200_review: unavailable
parent_state: open_trend
direction: short
lineage_status: pending
state_transition: none
order_branch: observation_only
actual_fill_or_open_skip: not_applicable
structural_stop: pending
structural_invalidation: pending
first_independent_obstacle: visual support zone near 88.75–90.10; not frozen
pre_entry_space_R: unknown
space_status: unknown
rough_R_R: unknown
research_state: research_positive_conditional
trade_state: not_authorized
gate_result: conditional
handoff_status: research_only
```

本块只固定强方向 A、深但受控 B 和首支撑空间的历史研究语义；不激活
`primary_pattern`/`internal_label`，也不把首障碍到达或后续路径写成胜率结果。

## 1. 证据头

- 标的：`US.NFLX`
- 周期：先看 Daily 完整窗口 `2025-01-15`–`2025-04-30`，再用 60m/15m 核对 `2025-03-27`–`2025-03-31`。
- 数据：Futu OpenD 历史 QFQ，收盘后读取；不是实时行情，没有下单。
- 目的：这是目前比 AMZN 更接近“方向性强 A → 受控回调 B → 第一次空头恢复”的独立视觉候选。它用于研究筛选和订单审计，不是已经验证的交易规则。

## 2. 视觉结构

### A 腿：方向性明显，先标为 strong-looking

从 `2025-02-14` 高点约 `106.45` 开始，价格在后续数周向下推进，并在 `2025-03-10` 触及约 `85.45`。中间仍有反弹和重叠，但高点逐步降低、低点持续下移，整体没有演化成一个宽幅横向交易区间。

这里可以先把它看成一条 `strong-looking A`，比普通方向性 A 更值得优先深入；但“强”仍是视觉判断，不是由固定跌幅或固定大阴线数量定义。A 的起点、终点和中间反弹必须在实时决策时已经可见，不能用后面的成功结果倒推。

### B 腿：回撤较深，但仍没有收回 A 起点

`2025-03-11`–`2025-03-25` 从 `85.45` 附近反弹到约 `99.87`，明显低于 A 起点 `106.45`。B 内部有较深的回撤，例如 `2025-03-12` 低点约 `90.10`、`2025-03-13` 低点约 `88.75`，所以不能把它描述成浅 B。

但截至 `2025-03-25`，B 仍然没有突破 A 的起点，也没有明显变成一个覆盖整段母腿的宽幅交易区间。当前更准确的标签是 `deep-but-controlled-B`：深，但结构仍可作为原空头 A 后的反向回调来观察。深 B 会降低优先级，不能自动等同于受控浅回调。

### C / L1-like：第一次空头恢复

`2025-03-27` 低点约 `96.63664` 可作为 B 后的研究触发参考。`2025-03-28` 没有从开盘直接跳过该价位：日线开盘约 `97.20`，仍在触发位上方。

低周期顺序需要分成两层：

- `09:45` 的 15m K 线最低约 `96.20277`，盘中首次刺破 `96.63664`，但收盘约 `97.115`，仍收回触发位上方；若原计划是 sell-stop，这一根已经可能触发成交，但不能把它误写成“收盘确认”。
- `10:15` 的 15m K 线收盘约 `96.24172`，确认收在触发位下方；`10:30` 进一步下行，提供了更清楚的跟随证据。

因此，这里可标为 `L1-like`，但要保留“盘中先刺破、收盘后确认”的订单分支。`2025-03-31` 的反弹是新的后续信息，不能回写成 `2025-03-28` 当时已经知道的内容。

后续继续下跌不自动增加 L2。没有新的反向 B、独立第二次空头尝试和同一回调 lineage 之前，先记录为 L1 后跟随。

## 3. 订单分支：无缺口，但盘中刺破与收盘确认要分开

### 分支 A：sell-stop，接受盘中触发

- 在 `2025-03-27` 低点约 `96.63664` 下方挂 sell-stop；
- `2025-03-28 09:45` 盘中最低已经低于触发位，因此原始 stop 可能在这一段成交；
- 之后价格先收回触发位上方，再在 `10:15` 收盘确认下破，说明成交后仍要面对第一次下破失败/回收风险。

### 分支 B：收盘确认或低周期跟随

- 如果不接受第一根 15m 的刺破，而要求收盘在触发位下方，则 `10:15` 是较保守的确认点；
- 这个分支成交更晚、风险几何会改变，不能和 `09:45` stop 成交合并统计；
- `10:30` 的继续下行可以作为跟随，不是第二次独立 L2。

### 分支 C：limit-retest

本案例没有开盘缺口，因此不需要 gap-reprice 分支。但如果研究者选择等待跌破后的回测再卖出，必须单独记录是否真的回到 `96.64` 附近、是否成交；不能用后续下跌证明 limit 本来会成交。

## 4. 结构止损、第一支撑与粗略 R/R

### 结构止损

若研究 `2025-03-28` 的空头恢复，保守结构止损应放在 B 高点 `99.87` 上方并留缓冲，暂以约 `100.8–101.2` 作为视觉研究区间。不能用 `09:45` 之后的小级别局部高点把止损压得过窄，因为那会隐藏 B 的结构失效条件。

### 第一独立支撑

在 `2025-03-28` 决策时，左侧可见的第一支撑先看：

- `2025-03-12` 低点约 `90.10`；
- `2025-03-13` 低点约 `88.75`。

因此第一目标区可先记为 `88.75–90.10`。`2025-03-28` 日内更低点、`2025-03-31` 低点和 4 月后续走势不能倒灌成入场前目标。

### 粗略几何

| 假设 | 研究成交 | 结构止损代理 | 第一支撑区 | 粗略观察 |
| --- | ---: | ---: | ---: | --- |
| `09:45` 盘中 stop 触发 | `96.64` 附近 | `100.8–101.2` 上方 | `90.10` | 约 `1.4R–1.6R` |
| `09:45` 盘中 stop 触发 | `96.64` 附近 | `100.8–101.2` 上方 | `88.75` | 约 `1.7R–1.9R` |
| `10:15` 收盘确认 | 更低、约 `96.2` 或之后 | 同上 | 同上 | 成交更晚，空间仍可研究，但不能假定与前一分支相同 |

这只是视觉筛选阶段的粗略 R/R，没有计入手续费、滑点、波动扩张和实际成交队列。它的价值在于：与 AMZN 的 `1.1R–1.4R` 边界相比，本案例在首支撑处留下了更明显的研究空间，但还没有足够证据把它冻结为“应该交易”。

## 5. 市场、板块与事件过滤

- `2025-03-28` 的 `SPY`、`QQQ` 和通信服务相关的 `XLC` 同期偏弱，NFLX 的空头方向获得一定市场/板块许可；这只是 META 中的一个加分项，不能替代 A、B、止损和首障碍判断。
- Netflix 官方投资者关系公告显示，2025 年第一季度业绩发布安排在 `2025-04-17`。`2025-03-28` 距离财报尚远，通过用户设定的“财报前三个交易日不交易”过滤；但事件背景仍应记录，不能把它称为完全无事件样本。

来源：Netflix 官方 [`Netflix to Announce First Quarter 2025 Financial Results`](https://ir.netflix.net/investor-news-and-events/financial-releases/press-release-details/2025/Netflix-to-Announce-First-Quarter-2025-Financial-Results/default.aspx)。

## 6. 当前判断

| 项目 | 当前判断 |
| --- | --- |
| market state | 空头方向腿后的反向回调与第一次恢复 |
| A quality | `strong-looking / directional` |
| B quality | `deep / still below A origin / late controlled` |
| H/L count | `03-28` L1-like；后续先记为 L1 后跟随，不自动增加 L2 |
| signal quality | 09:45 盘中刺破、10:15 收盘确认；需要区分两种成交合同 |
| order | 无开盘缺口；sell-stop、收盘确认、limit-retest 分开记录 |
| structural stop | B 高点 `99.87` 上方，研究约 `100.8–101.2` |
| first obstacle | `88.75–90.10` 左侧支撑区 |
| tradeability | 首障碍粗略约 `1.4R–1.9R`，比 AMZN 宽裕，属于条件正向候选 |
| status | `pattern_like / research_positive_conditional / no-gap-trigger / sector-aligned / pending` |

## 7. 事后过程审计：不回写前置判断

以下内容只在完成 `2025-03-28` 的决策审计后记录，不能拿来证明当时“必然应该入场”：

- `09:45` 盘中触发后，价格先在低周期回收到约 `97.50`，相对 `96.64` 约有 `0.86` 的不利波动；这说明第一根刺破并不是无风险的直线下跌。
- `2025-03-28` 日线最低约 `92.92`，`2025-03-31` 最低约 `90.06`，已经触及入场前预先标出的第一支撑区 `88.75–90.10` 的上沿。
- 以第一支撑 `90.10` 作为第一目标，两个订单分支都至少完成了“首障碍到达”的过程目标；这只能把样本保留为 `research_positive_conditional / process-target-reached`，不能单独证明胜率或冻结规则。
- 后续 `2025-04-04` 的更深下跌不用于提高原始 R/R，也不用于把 `2025-03-28` 事后升级成 L2；它只是后续路径信息。

## 8. 可复用结论

1. 视觉阶段可以先接受“strong-looking A + deep-but-controlled B + L1-like”作为值得深入的候选，不需要先把强 A 写成固定百分比条件。
2. 深 B 仍然要降低优先级；它只有在没有破坏 A 起点、没有明显区间化且后段压力收敛时，才保留为条件正向候选。
3. 无开盘缺口不等于没有订单歧义：盘中刺破、收盘确认和回测 limit 仍然是三种不同的成交假设。
4. 首支撑有空间时，才值得继续审计低周期触发；MM 仍然放在第一支撑之后，不能用远端目标替代近端障碍。
5. 连续下跌不自动变成 L2。L2 必须有新的反向 B 和独立第二次空头尝试，不能只看后面又跌了几根 K 线。
6. 这是比 AMZN 更值得深入、且事后首障碍确实到达的视觉候选，但仍是 `research_positive_conditional`，不是已验证胜率或生产规则。

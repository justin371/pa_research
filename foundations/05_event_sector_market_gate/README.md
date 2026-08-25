# 财报 / 事件 / 板块 / 大盘前置闸门

文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一输出字段见[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)。本层的 `permission` 和 `gate_result` 是闸门字段，不是方向或交易授权的替代品。

这是所有 PA pattern 进入深审前的共同背景层。它不是 pattern，也不是评分器；它决定候选是否可以进入形态审计、需要拆成事件样本，还是应该直接观望。

## 1. 固定顺序

```text
数据来源与状态 → 财报/重大事件窗口 → 板块与大盘方向许可
→ Daily/4H 父级背景与主要位置 → 低周期确认与实际订单 → pattern 审计
```

前置闸门不能替代 H1/H2、ABC、BOP、MTR 或三推判断；也不能因为“顺势”就取消首障碍、结构止损或 R/R。

## 2. 数据状态

每次复核先记录 `data_source`、`data_status`、`as_of_time` 和 `timeframes_seen`。来源可以是 Futu OpenD、收盘后公开数据、图表截图或其他来源；状态必须写成 `historical`、`delayed`、`live_confirmed` 或 `incomplete`。

收盘后历史数据可以做视觉复核，但不能说成实时；Futu OpenD 只有在连接、权限和具体周期返回都确认后，才能标记 `live_confirmed`。数据不完整可以给 `pattern_like` 初筛，不能声称实际触发或成交已确认。

## 3. 财报与重大事件

- 已知财报在未来三个交易 session 内：不新开仓，不赌财报；候选写 `gate_result: valid_no_trade` 或 `gate_result: pending`，并保留 `earnings_next_three_sessions: yes`。
- 已有仓位的管理与新入场分开，不能把减仓/止损悄悄算成新交易。
- 财报后的跳空、宏观冲击、监管消息、并购和产品发布记录为 `event_context: earnings / macro / gap / other`，不能与普通 PA K 线混作无事件基准。
- 事件时间或影响不清楚时保留 `pending`，不凭结果删除事件字段。
- 事件后强 A 可以说明重新定价，但不自动证明普通趋势延续或高胜率。

事件可能同时改变开盘、波动、成交、缺口、支撑阻力和第一障碍。因此事件过滤先于 pattern 标签。

## 4. 板块与大盘许可

记录相关 ETF/指数和状态：半导体优先 SOXX 或 SMH，其他行业使用最相关 ETF；市场通常参考 SPY、QQQ 或相关指数。状态使用 `aligned`、`mixed`、`counter` 或 `unknown`。

- 板块与大盘顺势是许可/加分项，不是入场信号；
- 两者不同步时写 `mixed`，不凭感觉合并；
- 个股逆板块不是绝对禁止，但需要主要位置、更清楚的结构、二次确认和足够空间，否则降级为 `observation_only`；
- 板块走弱会降低 H1/L1 优先级，更倾向等 H2、支撑反应或更强确认；
- 板块顺势也不能取消财报禁做、跳空重订或首阻力拥挤。

## 5. 事件、缺口与订单合同

事件或开盘跳空穿过原 stop 时：

1. 原合同记为 `opening-skip / original-not-filled-or-fill-unknown`；
2. 按实际可能成交价重算止损、首障碍和风险；
3. 回到旧结构区才另立 `limit-retest`；
4. 缺口被接受并有跟随时，另立 `BOP / gap-and-go`；
5. 不把重订价、回测和原 stop 混成一个结果。

事件 gap-and-go 不是普通 ABC 的延续样本；若继续研究，必须单独记录事件类型、开盘接受、实际成交和路径。

## 6. 降级规则

以下任一项出现时，不能直接升级为新仓：

- 财报前三个交易 session；
- 事件跳空与普通 K 线证据未分开；
- 板块/大盘明显逆向，而 pattern 只有一次尝试；
- 高周期在主要阻力/支撑下，15m 才出现相反方向信号；
- 低周期数据不完整，无法确认触发；
- 用低周期窄止损掩盖高周期结构风险；
- 开盘跳过原 stop 后，成交、首障碍和 R/R 未重算；
- 事件或板块通过，但第一独立障碍仍不足约 1R。

输出可为 `research_state: pattern_like / observation_only`、`gate_result: valid_no_trade / pending` 或 `trade_state: conditional`，而不是强行给出入场。

## 7. 统一闸门卡

```text
contract_scope: deep_review
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
query_period_end:
completed_bar_as_of:
timeframes_seen:
earnings_next_three_sessions: yes / no / unknown
event_context: none / earnings / macro / gap / other / unknown
event_source_as_of:
direction: long / short / no_valid_direction
sector_reference / sector_state:
market_reference / market_state:
parent_timeframe:
lower_timeframe / lower_role:
permission: long_allowed / short_allowed / both_allowed / no_direction / unknown
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

## 8. 证据入口与边界

既有完整闸门见 [`财报、板块与多周期前置过滤`](../../research/event_sector_multitimeframe_cross_pattern_audit_CN.md)，专项证据审计见 [`事件/板块/大盘视觉证据审计`](../../research/event_sector_market_gate_visual_evidence_audit_2026-08-24_CN.md)。本层只服务 PA Research 的视觉筛选和人工交易计划，不预测财报、不创建量化分数、不修改 Codex Trading，也不连接 Execution Agent。

# H3/L3 历史候选筛选日志证据与统计边界审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / historical / not-quantitative / no-new-positive`

## 1. 范围

本轮只审计[`2025-08 至 2025-11 H3/L3 候选日志`](../h3_l3_candidate_screen_2025-08_2025-11_CN.md)和[`2024–2026 L3 定向候选筛选`](../h3_l3_candidate_screen_futu_targeted_2024_2026_CN.md)的证据头、事件来源、canonical 字段、订单/首障碍空间和结论边界。没有重新下载行情、访问 Futu OpenD、查看新图、运行回放或改变任何历史结果。

## 2. 发现的问题与修复

### 2.1 历史数据状态没有结构化写清楚

两份日志都说明数据来自 Futu OpenD 的历史 QFQ 日线，但原始日志没有保留查询时间和时区。若只写“收盘后读取”，容易被误读成当前或实时证据。

已在两份日志的证据头明确写入：

```text
contract_scope: historical_context_only
data_status: historical
as_of_time: unavailable_in_original_log
timezone: unavailable_in_original_log
session_state: historical_close_review
chart_scope: partial
timeframes_seen: Daily
```

因此这些文件只能支持历史视觉筛选和事后过程审计，不能写成 `live_confirmed`，也不能用于当前交易授权。

### 2.2 事件来源覆盖范围有限

定向日志保留了 BKNG、AMD、GOOGL、NKE 的既有财报链接，但没有链接的 PM 及其他排除标的不能因此自动变成普通非事件样本。2025-08 至 2025-11 日志中多个案例也明确写着 `event-context-pending`，不能被摘要成事件过滤已通过。

已在日志中注明：事件链接只覆盖明确列出的部分核对；未独立核实的记录使用 `event_bucket: event_unverified_or_pending` 或继续补核。财报/缺口仍是 lineage 和订单合同的独立边界，不能由三次高低点计数覆盖。

### 2.3 历史状态标签与 canonical 字段分开

两份日志中的 `strong-trend`、`H1-H2-like`、`provisional-H3-like`、`count-ambiguous`、`range-transition`、`event-gap-boundary` 和 `first-obstacle-crowded` 是历史说明标签，不是新的字段枚举。两份日志现都附上相同的 canonical 阅读轴：

```text
lineage_status: same_lineage / reset / unclear / pending
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
direction: long / short / no_valid_direction
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
gap_policy: accept_open / skip / flag_only / not_applicable
structural_stop:
first_independent_obstacle:
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

这只是记录合同，不会把每一行的历史显示标签自动填成已冻结字段。尤其是 `attempt_direction` 不替代 `direction`，`range_edge_side` 不替代触发，`space_status` 不替代实际订单成交。

## 3. 对现有筛选结论的保留

| 日志 | 既有结论 | 处理 |
| --- | --- | --- |
| 2025-08 至 2025-11 | AVGO/MSFT/PANW/MRVL/DELL/LULU/TXN/TGT/DIS/NOW 等是强趋势、宽 B、事件/缺口、区间过渡或首障碍边界；没有新的 H3/L3 正向样本 | 保留所有边界，不把 `H1-H2-like` 或 `provisional-H3-like` 升级为正向合同 |
| 2024–2026 L3 定向筛选 | BKNG、PM 形态接近但首障碍不足；AMD、GOOGL、NKE 被趋势/区间/事件边界否决；WMT 是强多头延续而非空头 H3 | 保留 `valid_no_trade`、事件边界和 continuation-not-reversal 结论，不将后续路径倒灌为入场证据 |

两份日志都没有冻结三推/H3/L3 的数值回放合同。KLAC 仍只是条件性研究基准；L3 仍为 `no-new-positive`，`validated win-rate: not-computable`。

## 4. 统计边界

本轮没有修改 CSV、结果文件或 engine。既有合同审计的冻结集合仍为 7 份 CSV、60 行，H3/L3 冻结行数为 0；本轮两份筛选日志没有进入 H/L 统计分母，也没有新增胜率或盈亏比。

历史候选日志里的“形态像”“首障碍不足”“开盘跳过”“事件待核实”和“观察”必须分别保留，不能合并成一个成功/失败标签。只有人工重新冻结 lineage、方向、触发、结构止损、首障碍、空间和订单分支后，才可另建独立回放合同。

## 5. 结论与范围

- 两份日志现在明确是历史、部分证据覆盖的视觉筛选记录，不是实时行情或量化扫描结果；
- 事件链接的覆盖范围和缺失时间戳已显式标注，不能把未核实标的升级为普通非事件；
- canonical `third_push_state`、`lineage_status`、`direction`、订单/空间和状态轴已写入日志的统一阅读合同；
- 所有既有边界、`valid_no_trade`、opening-skip/gap-reprice 和后续失效结论均保留；
- `no-new-positive` 与 `validated win-rate: not-computable` 保持不变。

本审计只属于 PA Research：`PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。

# H3/L3 定向候选筛选：Futu OpenD 2024–2026

> 状态：第一阶段视觉快筛记录；`historical / no-new-positive / validated win-rate: not-computable / not-quantitative`，不是统计回测，也不是交易建议。
>
> 数据：本机 Futu OpenD 收盘后 QFQ 日线；原始日志没有保留查询时间和时区，因此 `data_status=historical`，不是 `live_confirmed`。先用结构化数据定位窗口，再用完整日线图检查。精确的低周期成交与财报前信息不在本轮结论内。

## 证据头

```text
contract_scope: historical_context_only
review_date: 2026-08-29
data_source: Futu OpenD historical QFQ Daily
data_status: historical
as_of_time: unavailable_in_original_log
timezone: unavailable_in_original_log
session_state: historical_close_review
chart_scope: partial
timeframes_seen: Daily
```

## 统一字段阅读

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
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
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

`pattern_like`、`count-ambiguous`、`range-transition`、`event-gap-boundary` 和 `first-obstacle-crowded` 是历史显示标签，不是新的字段枚举。它们必须分别通过 `lineage_status`、`third_push_state`、`event_bucket`、`first_independent_obstacle`、`space_status` 和 `trade_state/gate_result` 表达；触发、空间或合同未冻结时，`direction` 保持 `no_valid_direction`。

## 目的

补充一个真正独立的 L3 衰竭样本；如果候选只是区间重复低点、事件重定价、趋势延续，或第一道独立阻力没有空间，就直接归档为边界，不把后续上涨倒灌成入场证据。当前没有达到该条件的独立 L3 正向样本，因此本日志保持 `no-new-positive`，不建立统计分母。

## 快筛结果

| 标的与窗口 | 视觉判断 | 订单/首障碍 | 当前标签 |
|---|---|---|---|
| `BKNG`：`2026-07-06`、`07-14`、`07-23`；`07-24` 触发 | 上涨背景清楚，三次回压逐步落到约 `180.57/171.16/171.02`，第三次后有多头信号；形态比多数候选干净 | 若在 `07-24` 高点上方追踪，结构止损需放在约 `170` 下方；前方 `07-17` 高点约 `184.36`，首障碍空间不足约 `1R` | `pattern_like / valid_no_trade / first-obstacle-crowded` |
| `PM`：`2025-02-28`、`03-10`、`03-14`；`03-14` 触发 | 上涨背景和三次回压外形存在，第三次较弱；但位置贴近前高簇 | 粗略入场约 `145.78`、结构止损约 `140.81`、首障碍约 `150.38`，只有约 `0.93R`；应先判为不值得做 | `pattern_like / first-obstacle-borderline / valid_no_trade` |
| `AMD`：`2024-10-23`、`11-04`、`11-15`；`11-19` 触发 | 第三次下探幅度收缩，但母级仍是空头趋势，信号后没有持续接受，随后继续走低 | 形态不能因一个强多头日线升级；而且 `2024-10-29` 财报位于该 lineage 内，事件污染需单独处理 | `continuation_or_failure / event-boundary / not-positive-L3` |
| `GOOGL`：`2026-02-05`、`02-17`、`03-03`；`03-03` 触发 | 第二、第三低点约 `295.86/296.32`，第三点没有清楚创新低；更像区间/过渡中的重复测试 | 首障碍约 `319.10`，粗略空间仍不足以抵消结构风险；`2026-02-04` 财报刚发生，母腿需要重置 | `range-transition / count-ambiguous / valid_no_trade` |
| `NKE`：`2024-06-17`、`07-01`、`07-10`；`07-10` 触发 | 数据筛选出的第三次回压外形被 `2024-06-27` 财报跳空切断，不能把前后波动拼成一个普通 L3 | 事件重定价优先于形态计数；不进入订单或 R/R 审计 | `event-gap-boundary / not-admissible` |

## 直接淘汰的其他窗口

- `AMZN 2025-09`–`10`：低点逐步下移，但父级更像宽幅下行/过渡；`2025-10-30` 后的事件缺口使后续不能倒灌。
- `SNOW 2024-10`–`11`：三个低点主要是区间底部的重复测试，不是开放趋势中的三次衰竭推进。
- `NFLX 2024-03`–`05`：`2024-04-19` 的事件缺口切断了原有 lineage。
- `UBER 2025-07`–`08`：第三次低点接近财报窗口，且整体更像空头延续后的反应。
- `NVDA 2026-02`–`04`：`2026-02-25/26` 的事件波动改变了计数，不能作为干净 L3。

## 本轮结论

1. `BKNG` 是本轮最接近 L3 衰竭的视觉候选，但首障碍否决了交易质量；它不能作为 L3 正向交易样本。
2. `PM` 说明“形态像”仍可能被首障碍压缩；不足 `1R` 时，后续是否上涨不改变当时的 no-trade 判断。
3. `AMD` 和 `NKE` 说明事件/趋势延续会让三次低点失去同一 lineage；不能只按低点数量命名 L3。
4. 本轮仍没有找到同时满足“同一 lineage、第三次衰竭、反向触发、结构止损可放置、首障碍有空间”的独立 L3 正向样本。L3 保持条件性规则，不镜像 KLAC 的 H3 结论。

## 互补 H3 快筛：WMT 2024-08–09

同一批历史数据用相反方向做了轻量 H3 筛选，`WMT` 的 `2024-08-15`、`08-22`、`09-03` 三个高点外形看似逐步上移，第三次后也出现了短线阴线。但完整图表显示：

- EMA20/50 和左侧结构都在明显上行，三个高点发生在多头趋势中；
- 这更像强趋势中的浅回调与重新推进，而不是空头背景中的 H3 反转尝试；
- 因此即使粗略首障碍空间看起来尚可，也不能把它作为空头 H3 正向样本。

当前标签：`strong-bull-trend / continuation-not-reversal / not-H3-short`。这条边界再次确认：H3/L3 的方向背景和父级市场状态先于局部三次计数。

## 研究边界

本轮筛选使用了候选触发后的历史走势来做事后审计，但候选是否可交易的判断只使用触发前可见的背景、位置、订单、结构止损和首障碍。下一轮只有在出现新的事件干净窗口或新的订单合同证据时才继续；不重复扫描本表样本。

## 事件来源

事件链接只覆盖本日志中明确列出的部分财报核对；没有链接的标的不能因此自动标记为普通非事件，仍应保持 `event_unverified_or_pending` 或单独补核。所有链接都是历史事件来源，不改变本文件的历史数据状态。

- [Booking Holdings 2026 Q2 earnings（2026-08-04）](https://ir.bookingholdings.com/news/news-details/2026/Booking-Holdings-to-Make-Second-Quarter-2026-Earnings-Press-Release-Available-on-Companys-Investor-Relations-Website-on-August-4/default.aspx)
- [AMD 2024 Q3 earnings（2024-10-29）](https://ir.amd.com/financial-information/sec-filings/content/0000002488-24-000161/q32024991.htm)
- [Alphabet 2025 Q4 earnings（2026-02-04）](https://abc.xyz/investor/news/news-details/2026/Alphabet-Announces-Fourth-Quarter-2025-and-Fiscal-Year-Results-2026-KEvZIMKBLS/default.aspx)
- [Nike FY2024 Q4 earnings（2024-06-27）](https://investors.nike.com/investors/news-events-and-reports/investor-news/investor-news-details/2024/NIKE-Inc.-Reports-Fiscal-2024-Fourth-Quarter-and-Full-Year-Results/default.aspx)

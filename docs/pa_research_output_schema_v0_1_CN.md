# PA Research 统一输出合同 v0.1

日期：2026-08-25
文档状态：`adopted / research-only / not-quantitative`

## 目的与适用范围

本文件统一 PA Research 的视觉复核、日线候选和历史案例输出字段。它只定义研究记录的结构，不定义量化扫描条件、生产交易规则、订单接口或 Execution Agent 行为。

使用顺序仍由各自上游规则决定：

1. 日线候选先遵循[`PA Research 日线选股规则 v0.1`](pa_research_daily_selection_rules_v0_1_CN.md)；
2. 完整图表复核使用[`PA 图表视觉复核卡`](visual_pa_review_card_CN.md)；
3. 核心 pattern 的切换和历史别名映射见[`核心八个 Pattern 交叉一致性审计`](../research/core_pattern_cross_audit_CN.md)；
4. 是否可以交接给 Codex Trading 另遵循[`研究交接规范`](research_to_system_handoff_CN.md)。

`contract_scope` 必须先写清楚：

```text
stage_1_fast_screen / deep_review / daily_candidate / historical_context_only
```

`stage_1_fast_screen` 和 `historical_context_only` 可以暂缺成交、止损、首障碍和 R/R，但必须写 `pending` 或 `unknown`，不能被当作完整候选。

## 一、证据头与市场闸门

```text
symbol:
review_date:
contract_scope:
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:
timeframes_seen:
chart_scope: full / partial
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable

event_context: none / earnings / macro / gap / other / unknown
event_source_as_of:
earnings_next_three_sessions: yes / no / unknown
sector_reference:
sector_state: aligned / mixed / counter / unknown
market_reference:
market_state: aligned / mixed / counter / unknown
permission: long_allowed / short_allowed / both_allowed / no_direction / unknown
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

`as_of_time`、时区、session 和 `completed_bar_as_of` 必须能区分报告生成时间、查询窗口结束时间和实际可用的最新完整 K 线。历史数据不能写成实时数据。

## 二、结构、方向与 pattern

```text
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
direction: long / short / no_valid_direction
left_structure_and_location:
major_highs_lows:
support_resistance_and_role_zones:
daily_ema20_50_200:

primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
secondary_context:
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
internal_label: H1 / H2 / L1 / L2 / H3_L3 / none / pending
pattern_like_reason:
```

`direction` 是当前研究合同的方向，不是 `directional_bias` 的同义词：

- 多头 H1/H2、Bullish ABC 或多头 BOP 写 `long`；
- 空头 L1/L2、Bearish ABC 或空头 BOP 写 `short`；
- 区间中部、父级冲突、方向未冻结或没有有效交易方向写 `no_valid_direction`。

同一案例可以有 `directional_bias: bull`，但因首障碍或事件闸门不合格而写 `direction: no_valid_direction`。不能用后续涨跌倒推方向。

## 三、BOP 专用字段

当 `primary_pattern: BOP` 时必须填写：

```text
bop_state: acceptance_watch / ordinary_pullback / failed_breakout / gap_event / bull_flag_continuation
breakout_boundary:
acceptance_close:
follow_through:
retest_zone:
role_reversal_held: yes / no / unclear / not_occurred
```

`BOP` 是独立主合同。ABC、H1/H2 或三推只能放入 `secondary_context`，不能使用 `BOP_ABC` 作为主 pattern，也不能把 BOP 与 ABC/H-L 结果混算。没有回踩时只能写 `acceptance_watch` 或相应的 gap/event 分支，不能补写不存在的回踩。

## 四、订单与风险字段

```text
signal_bar:
confirmation_bar:
new_trigger:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
order_price_or_zone:
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
structural_stop:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
rough_R_R:
target_layers:
main_uncertainty_or_exclusion:
```

`order_branch` 只表达基础订单合同；`branch_role` 记录反向 stop、角色转换回测、跳空重订等研究分支。历史文件中的 `stop`、`limit-retest`、`market-close`、`reverse-stop` 和 `limit-edge` 是别名，更新新记录时必须映射到上述字段，不能继续作为同一字段的混合枚举。

## 五、状态轴与交接轴

不同状态不能塞进一个 `status`：

```text
document_status: draft / adopted / historical / research_only
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
thesis_state: working / failed / invalidated / replaced / pending
handoff_status: research_only / not_ready / ready_for_system
```

这些字段不代表胜率或实盘授权。`research_positive_conditional` 仍是人工研究状态；`valid_no_trade` 不是亏损；`handoff_status: ready_for_system` 只有在研究交接规范的全部晋级闸门通过后才可使用。`adopted` 只表示文档被采纳，不表示规则已经验证或可执行。

## 六、最小输出模板

```text
### [symbol] [review_date] — [primary_pattern]

contract_scope:
direction:
data_status:
as_of_time:
parent_state:
primary_pattern:
secondary_context:
internal_label:
key_breakout_or_structure_location:
why_it_meets_or_fails_the_rule:
possible_entry_trigger:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R:
research_state:
trade_state:
gate_result:
handoff_status:
main_uncertainty_or_exclusion:
```

任何缺失字段都必须明确写 `unknown`、`pending` 或 `not_applicable`。本合同只服务 PA Research；不创建行情扫描器、不修改 Codex Trading、不连接 Execution Agent。

# TSLA META Example — 2026-06-25

## 统一输出边界

```text
contract_scope: historical_context_only
symbol: TSLA
review_date: 2026-06-25
data_source: historical chart note
data_status: incomplete
as_of_time: unknown
timezone: unknown
session_state: historical_close
timeframes_seen: Daily / unknown lower timeframe
chart_scope: partial
daily_context_window: unavailable
major_high_low_review: unavailable
ema20_50_200_review: unavailable
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
event_context: unknown
event_bucket: unknown
directional_bias: changing
direction: no_valid_direction
primary_pattern: other
secondary_context: potential_three_push_wedge;support_reaction;META_candidate
pattern_like_reason: potential_three_push_visual_shape;incomplete_left_context;count_pending
range_edge_three_push: pending
state_transition: none
lineage_status: pending
lineage_id: pending
internal_label: pending
permission: no_direction
gate_result: observation_only
order_branch: observation_only
actual_fill_or_open_skip: not_applicable
structural_invalidation: pending
first_independent_obstacle: unknown
rough_space_to_first_obstacle_R: unknown
research_state: pattern_like
trade_state: not_authorized
handoff_status: research_only
```

这是一条历史形态观察笔记，不是实际成交日志、冻结合同或胜率样本。由于两年 Daily、EMA、事件、精确触发、结构失效和第一障碍没有在本笔记中闭合，方向明确保留为 `no_valid_direction`，不把“Potential Trigger”升级成交易授权。

## Status

Draft retrospective review. This example is for validating the META framework, not yet a production backtest rule.

## Market

- Symbol: TSLA
- Timeframe: Daily
- Third-push area: 2026-06-25 to 2026-06-26

## Observed Structure

Three downside pushes were identified near:

1. 2026-05-19: low near 393.6
2. 2026-06-10: low near 380.2
3. 2026-06-25 to 2026-06-26: low near 371

The lows continued downward, but the distance of each push appeared to contract.

## Converging Edges

- Potential three-push wedge
- Prior support from the April trading area
- Price near the 370 area
- Selling momentum appeared to weaken
- The location was reached after an extended decline

## Expected Behavior

The first expectation was a bounce or pause.

A full trend reversal was not assumed.

## Potential Trigger

A long setup would require evidence of buying pressure, such as:

- A strong bullish reversal bar
- A break above the signal bar
- A successful test of the third-push low
- Follow-through after the initial reaction

## Invalidation

The idea would be invalid if price:

- Broke strongly below the third-push low
- Accepted below the prior support area
- Continued down without any meaningful buying response

## Potential Targets

- First target: the nearest lower high
- Short-term reference: approximately 402–403
- Larger confirmation area: approximately 412–418

## Evaluation

The META location suggested that a reaction was more likely.

It did not, by itself, prove that the trend had reversed.

The key research question is:

> Does a three-push pattern at prior support produce a tradable bounce often enough to justify a defined trigger and structural stop?

## Evidence Needed

To validate this setup, review more historical examples and record:

- Location
- Number of independent edges
- Trigger type
- Stop distance
- First target
- Maximum favorable excursion
- Maximum adverse excursion
- Result in R

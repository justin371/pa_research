# H/L 下一批人工看图回放资产（2026-08-27）

状态：`visual_review_asset / no_pattern_labels / frozen_pre_outcome`

## Canonical provenance boundary

```text
contract_scope: historical_context_only
data_source: public Yahoo Chart API historical Daily OHLCV via Jina Reader
data_status: historical
as_of_time: 2026-08-26 latest complete RTH bar
review_time: 2026-08-27 Asia/Shanghai
timezone: America/New_York
session_state: historical_close
timeframes_seen: Daily
chart_scope: full
daily_context_window: >=2y
major_high_low_review: complete in paired frozen-contract review
ema20_50_200_review: complete in paired frozen-contract review
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
direction: no_valid_direction
lineage_status: pending
internal_label: pending
third_push_state: unclear
range_edge_three_push: pending
range_edge_side: pending
research_state: observation_only
trade_state: observation_only
gate_result: observation_only
first_independent_obstacle: paired contract only; not frozen in this asset
pre_entry_space_R: unknown unless trigger and structural stop are independently frozen
space_status: unknown
order_branch: observation_only
label_source: human_chart_review
handoff_status: not_ready
```

这是五条人工冻结合同的无标签图像资产；`direction`、`internal_label`、EMA gate、事件和
空间必须按配对合同逐行读取。资产本身不冻结 `primary_pattern`、订单或回放结果。

本目录保存 PA Research 下一批 H1/L1 人工冻结合同的证据图。每张 PNG 都包含：

- 截至决策日的两年 Daily 左侧背景；
- 局部 Daily 序列；
- 原始 OHLC K 线、EMA20/50/200 和原始成交量；
- 源时区 `America/New_York`。

图上不显示 H1/L1 标签、入场位、止损、第一障碍或回放结果。标签和合同参数在回放前写入 [`hl_next_contracts_2026-08-27.csv`](../../../../backtesting/hl_next_contracts_2026-08-27.csv)，不从结果反推。

## 图像清单

| 标的 / 决策日 | 方向 / 标签 | 事件分组 | 文件 |
| --- | --- | --- | --- |
| ZS 2021-07-19 | long / H1 | ordinary non-event | `ZS_2021-07-19.png` |
| DDOG 2021-07-19 | long / H1 | ordinary non-event | `DDOG_2021-07-19.png` |
| DDOG 2023-07-24 | long / H1 | ordinary non-event | `DDOG_2023-07-24.png` |
| ZS 2023-09-19 | long / H1 | event-driven | `ZS_2023-09-19.png` |
| DDOG 2023-03-07 | short / L1 | event-driven aftershock | `DDOG_2023-03-07.png` |

## 人工审阅边界

每个决策日先查看至少两年 Daily 左侧，再检查重要高点/低点、支撑阻力、EMA20/50/200、父级趋势、A/B 质量、回调位置、META 和第一障碍空间。多头 H1 只有 EMA20/50 同时向上时冻结；空头 L1 只有两者同时向下时冻结。未通过强 A、受控 B、事件分层或约 `>=1R` 首障碍空间的候选不在本目录中；H2/L2 没有为了凑数加入。

价格快照为公开 Yahoo Chart API 历史 Daily OHLCV，经 agent-reach 的 Jina 公开路由获取；复核时间为 `2026-08-27 Asia/Shanghai`，最新完整日线为 `2026-08-26 America/New_York`。本 session 没有成功调用 Futu MCP，因此资产不是 Futu 或实时数据。

本目录只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。Matplotlib 用于绘图，不承担 pattern 识别。

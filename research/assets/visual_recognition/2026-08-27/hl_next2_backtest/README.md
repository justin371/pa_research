# H/L 下一批（二）人工看图回放资产（2026-08-27）

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
first_independent_obstacle: paired contract or boundary review only; not frozen in this asset
pre_entry_space_R: unknown unless trigger and structural stop are independently frozen
space_status: unknown
order_branch: observation_only
label_source: human_chart_review
handoff_status: not_ready
```

这是两条冻结 H1 合同和一张 H2-like 闸门拒绝边界图的混合资产；`direction`、
`internal_label`、EMA gate、空间和 `PHM` 的观察状态必须按配对记录逐行读取。资产本身不冻结
`primary_pattern`、订单或回放结果，边界图也不增加 H2/L2 分母。

本目录保存下一批 H/L 人工合同的证据图。每张图都在决策日截断，并包含：

- 至少两年 Daily 左侧背景；
- 局部 Daily OHLC K 线；
- EMA20、EMA50、EMA200；
- 原始成交量；
- 源时区 `America/New_York`。

图上不显示 H1/H2/L1/L2 标签、入场位、止损、第一障碍或回放结果。标签与合同参数见 [`hl_next2_contracts_2026-08-27.csv`](../../../../backtesting/hl_next2_contracts_2026-08-27.csv)，不是从结果反推。

## 图像清单

| 标的 / 决策日 | 人工处理 | 文件 |
| --- | --- | --- |
| TOL 2023-04-26 | 冻结 `long / H1`，普通 A、受控 B、META present、空间 1.5840R | [`TOL_2023-04-26.png`](TOL_2023-04-26.png) |
| VEEV 2024-01-18 | 冻结 `long / H1`，强 A、deep-late-controlled B、边界空间 1.0085R、META absent | [`VEEV_2024-01-18.png`](VEEV_2024-01-18.png) |
| PHM 2023-05-31 | H2-like 观察/拒绝样本；EMA20 方向闸门未通过 | [`PHM_2023-05-31_boundary.png`](PHM_2023-05-31_boundary.png) |

## 视觉审阅边界

人工审阅顺序是先看两年左侧背景，再看重要高点/低点、支撑阻力、EMA20/50/200、A/B 质量、回调位置、META、失败路径和首障碍空间。H1/H2 多头要求 EMA20/50 同时向上；L1/L2 对称要求两条均线同时向下。H2/L2 不能因为局部形状相似就机械计数，必须有同一 lineage 的第一次尝试和第二次有意义尝试。

这些 PNG 是无标签审计资产，不是量化扫描器的输出。Matplotlib 负责渲染，不负责识别形态；原始下载文本、脚本缓存和外部运行输出不提交到仓库。

价格数据为公开 Yahoo Chart API 历史 Daily OHLCV，经 agent-reach 的 Jina 公开路由读取；复核时间为 `2026-08-27 Asia/Shanghai`，最新完整 RTH 日线为 `2026-08-26 America/New_York`。本 session 没有成功调用 Futu MCP，因此资产不是 Futu 或实时数据。

本目录只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

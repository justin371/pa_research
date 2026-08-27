# H/L 下一批人工看图回放资产（2026-08-27）

状态：`visual_review_asset / no_pattern_labels / frozen_pre_outcome`

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

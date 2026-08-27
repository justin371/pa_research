# H/L 下一批（二）人工看图回放资产（2026-08-27）

状态：`visual_review_asset / no_pattern_labels / frozen_pre_outcome`

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

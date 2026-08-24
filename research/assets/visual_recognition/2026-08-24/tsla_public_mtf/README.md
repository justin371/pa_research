# TSLA 多周期视觉识别资产（2026-08-24）

这些 PNG 是用于 PA Research 视觉识别验收的静态派生图，不是实时行情、交易授权或量化扫描输入。

- 标的：`TSLA`
- 数据状态：公开历史 OHLC；通过 Jina Reader 读取 Yahoo Finance Chart API；不是 Futu 数据，也不是实时授权
- 来源查询窗口：`2024-08-24T00:00:00Z` 至 `2026-08-25T00:00:00Z`
- 来源时区：`America/New_York`；本次返回的最新完整 RTH bar 为 `2026-08-21 16:00 EDT`
- Daily：约两年左侧背景，显示 EMA20/50/200；不绘制 pattern 标签
- 4H-like：由同一来源的 60m RTH bar 按每个交易日连续四根聚合；因此保留 `4H-like` 名称，不冒充原生 4H 数据
- 1H：`2026-08-03` 至 `2026-08-21`
- 15m：`2026-08-17` 至 `2026-08-21`，RTH

原始查询入口：

- Daily：`https://r.jina.ai/http://query1.finance.yahoo.com/v8/finance/chart/TSLA?period1=1724457600%26period2=1787616000%26interval=1d%26events=history%26includeAdjustedClose=true`
- 60m（用于 4H-like 与 1H）：`https://r.jina.ai/http://query1.finance.yahoo.com/v8/finance/chart/TSLA?period1=1783641600%26period2=1787616000%26interval=60m%26events=history%26includeAdjustedClose=true`
- 15m：`https://r.jina.ai/http://query1.finance.yahoo.com/v8/finance/chart/TSLA?period1=1783641600%26period2=1787616000%26interval=15m%26events=history%26includeAdjustedClose=true`

图像只用于先识别背景、位置、推动腿/计数、pattern 和失效条件；订单、结构止损、第一障碍、R/R、评分和自动化均不在本资产内。

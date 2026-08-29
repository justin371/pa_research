# 多标的多周期视觉识别资产（2026-08-24）

这些 PNG 是 PA Research 的第二轮未标注视觉验收资产：先看图，再记录背景、位置、关键高低点、EMA 和 pattern 候选。它们不是实时行情、交易授权或量化扫描输入。

- 标的：`AAPL`、`NVDA`、`SPY`、`RBLX`
- 资产生成日期：`2026-08-24`
- 数据状态：公开历史 OHLC；通过 Jina Reader 读取 Yahoo Finance Chart API；不是 Futu 数据，也不是实时授权
- Daily 查询窗口：`2024-08-24T00:00:00Z` 至 `2026-08-25T00:00:00Z`
- 60m/15m 查询窗口：`2026-07-10T00:00:00Z` 至 `2026-08-25T00:00:00Z`
- 来源时区：`America/New_York`
- 返回的最新完整 RTH bar：`2026-08-21 16:00 America/New_York`；请求结束日不等于数据实际最新日
- Daily：约两年左侧背景，显示 EMA20/50/200；不绘制 pattern 标签
- 4H-like：同一来源的 60m RTH bar 按每个交易日连续四根聚合；保留 `4H-like` 名称，不冒充原生 4H
- 1H：`2026-08-01` 至 `2026-08-24`
- 15m：`2026-08-17` 至 `2026-08-24`，RTH

## Canonical provenance boundary

```text
contract_scope: historical_context_only
data_source: public Yahoo Finance Chart API via Jina Reader
data_status: historical
as_of_time: 2026-08-21 16:00 America/New_York
timezone: America/New_York
session_state: historical_close
timeframes_seen: Daily / 4H-like / 1H / 15m
chart_scope: full
daily_context_window: >=2y
major_high_low_review: complete in paired smoke review; not drawn on the asset
ema20_50_200_review: complete in paired smoke review; Daily EMA only
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
direction: no_valid_direction (unlabeled asset; per-case reading is in the paired review)
lineage_status: pending
internal_label: pending
research_state: observation_only
trade_state: observation_only
gate_result: observation_only
handoff_status: not_ready
```

`primary_pattern`、`secondary_context`、H1/H2/L1/L2、三推、BOP 和 MTR 在这组
无标签资产中不冻结；对应显示标签和保守映射见配对的[`PA 图表视觉识别冒烟验收`](../../../../visual_recognition_smoke_test_2026-08-24_CN.md)。
资产 README 的 `major_high_low_review` 与 `ema20_50_200_review` 只表示配对
历史复核已记录这些字段，不表示图片上的线条本身产生交易信号。

## 图像入口

| 标的 | 四周期合图 | Daily | 4H-like | 1H | 15m |
| --- | --- | --- | --- | --- | --- |
| AAPL | [montage](AAPL/AAPL_MTF_montage.png) | [Daily](AAPL/AAPL_Daily_2y.png) | [4H-like](AAPL/AAPL_4H_like.png) | [1H](AAPL/AAPL_1H.png) | [15m](AAPL/AAPL_15m.png) |
| NVDA | [montage](NVDA/NVDA_MTF_montage.png) | [Daily](NVDA/NVDA_Daily_2y.png) | [4H-like](NVDA/NVDA_4H_like.png) | [1H](NVDA/NVDA_1H.png) | [15m](NVDA/NVDA_15m.png) |
| SPY | [montage](SPY/SPY_MTF_montage.png) | [Daily](SPY/SPY_Daily_2y.png) | [4H-like](SPY/SPY_4H_like.png) | [1H](SPY/SPY_1H.png) | [15m](SPY/SPY_15m.png) |
| RBLX | [montage](RBLX/RBLX_MTF_montage.png) | [Daily](RBLX/RBLX_Daily_2y.png) | [4H-like](RBLX/RBLX_4H_like.png) | [1H](RBLX/RBLX_1H.png) | [15m](RBLX/RBLX_15m.png) |

## 原始查询入口

查询模板为：

`https://r.jina.ai/http://query1.finance.yahoo.com/v8/finance/chart/<SYMBOL>?period1=1724457600%26period2=1787616000%26interval=<INTERVAL>%26events=history%26includeAdjustedClose=true`

其中 `<SYMBOL>` 为上述四个标的，`<INTERVAL>` 分别为 `1d`、`60m` 和 `15m`。本地验收只保留派生图，不把原始 JSON 当作研究规则输入。

图像只用于先识别背景、位置、推动腿/计数、pattern 和视觉失效边界；订单、结构止损、第一障碍、R/R、评分和自动化均不在本资产内。

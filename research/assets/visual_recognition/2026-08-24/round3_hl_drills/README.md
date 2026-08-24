# H1/H2 与 L1/L2 局部盲测资产（2026-08-24）

这是第二轮多周期资产的局部放大盲测，不含 pattern 标签、计数标记或画线。它只用于复核同一周期内的 A 腿、B 回调、第一次/第二次方向尝试和视觉失效边界；Daily 两年背景仍使用[`第二轮多标的多周期资产`](../round2_multisymbol/README.md)中的同标的图。

- 标的：`SPY`、`NVDA`
- 数据状态：公开历史 OHLC；通过 Jina Reader 读取 Yahoo Finance Chart API；不是 Futu 数据，也不是实时授权
- 来源最新完整 RTH bar：`2026-08-21 16:00 America/New_York`
- SPY drill：`2026-08-03`–`2026-08-08`，1H/15m
- NVDA drill：`2026-08-03`–`2026-08-12`，1H/15m
- 所有图像只保留价格、成交量、时间轴和价格轴；不含 H/L、ABC 或三推标签

## 图像入口

| 标的 | 合图 | 1H | 15m |
| --- | --- | --- | --- |
| SPY | [drill montage](SPY/SPY_drill_montage.png) | [1H drill](SPY/SPY_1H_drill.png) | [15m drill](SPY/SPY_15m_drill.png) |
| NVDA | [drill montage](NVDA/NVDA_drill_montage.png) | [1H drill](NVDA/NVDA_1H_drill.png) | [15m drill](NVDA/NVDA_15m_drill.png) |

这组资产不改变交易系统，也不把视觉计数变成固定阈值或量化扫描器。

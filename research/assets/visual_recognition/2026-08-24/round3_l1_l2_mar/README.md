# MAR 空头 L1/L2-like 视觉资产（2026-08-24）

这组图用于补充一个未标注的空头 ABC/L1-L2-like 对照：先看两年 Daily 背景，再看 4H-like 与 60m 低周期。图上没有 L1/L2、ABC 或交易标签。

- 标的：`MAR`
- 数据状态：公开历史 OHLC；通过 Jina Reader 读取 Yahoo Finance Chart API；不是 Futu 数据，也不是实时授权
- Daily 窗口：`2024-06-18`–`2026-06-26`，显示 EMA20/50/200
- 4H-like：`2026-06-15`–`2026-06-26`，由 60m RTH bar 每交易日连续四根聚合
- 低周期：`2026-06-18`–`2026-06-25` 的 60m proxy
- Yahoo 的 15m 历史窗口要求在最近 60 日内，本案例日期超出该限制，因此没有伪造 15m 图；这也是验收限制的一部分
- 最新完整 Daily bar（本资产请求范围）：`2026-06-26`

## 图像入口

- [Daily ~2Y](MAR_Daily_2y.png)
- [4H-like](MAR_4H_like.png)
- [60m / 1H proxy](MAR_1H.png)
- [三周期合图](MAR_MTF_montage.png)

图像只用于识别背景、A/B 推动、第一次/第二次空头恢复和失效边界；订单、止损、R/R、评分和自动化不在本资产内。

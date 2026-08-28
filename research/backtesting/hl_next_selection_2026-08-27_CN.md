# H/L 下一批人工合同冻结记录（2026-08-27）

状态：`research_only / frozen_pre_outcome / descriptive_only / not-validated`

## 结论边界

本批不是自动筛选结果。标签、A/B 结构、H1/L1 计数、EMA 斜率、重要高低点、支撑阻力、META、事件分组、触发、结构止损和第一障碍均在回放前由人工看图冻结。目标胜率是用户修正后的 `60%` 待检验目标，不是生产规则、胜率承诺或收益保证。

本批只保留两个中等至大型市值的美国普通股：ZS 和 DDOG。两者均通过约 `$3B–$100B` 研究池、20 日平均日成交额 `$50M` 的准入检查；没有合格的 H2/L2 或第三标的被强行加入。

## 数据和准入快照

| 项目 | ZS | DDOG |
| --- | ---: | ---: |
| 研究市值快照 | 约 `$27.28B`（2026-08-07） | 约 `$84.00B`（2026-08-07） |
| 20 日平均日成交额 | 约 `$381.5M`（2026-07-30 至 2026-08-26） | 约 `$1.292B`（同区间） |
| 市值来源 | [StockAnalysis market cap](https://stockanalysis.com/stocks/zs/market-cap/) | [StockAnalysis market cap](https://stockanalysis.com/stocks/ddog/market-cap/) |
| 成交额计算 | Yahoo Daily `Close × Volume` | Yahoo Daily `Close × Volume` |

市值是可访问公开页面的近似快照，不是历史决策日的回填市值；成交额使用当前研究快照仅作股票池准入。价格文件为公开 Yahoo Chart API 历史 Daily OHLCV，经 agent-reach 的 Jina 公开路由读取；复核时间为 `2026-08-27 Asia/Shanghai`，源时区为 `America/New_York`，最新完整 RTH 日线为 `2026-08-26`。本 session 没有成功调用 Futu MCP，因此数据不是 Futu 或实时数据。

机器可读合同和价格快照分别是 [`hl_next_contracts_2026-08-27.csv`](hl_next_contracts_2026-08-27.csv) 和 [`hl_next_prices_2026-08-27.csv`](hl_next_prices_2026-08-27.csv)。人工图像见 [`H/L 下一批人工看图回放资产`](../assets/visual_recognition/2026-08-27/hl_next_backtest/README.md)。

## 冻结合同

空间按多头 `(first_obstacle - entry_trigger) / (entry_trigger - structural_stop)`、空头 `(entry_trigger - first_obstacle) / (structural_stop - entry_trigger)` 计算；`>=1R` 是进入本批严格空间门槛的最低线。

| 合同 | 方向 / 标签 | 决策日 | 触发 | 止损 | 第一障碍 | 冻结前空间 | A/B 与位置判断 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| ZS 2021-07-19 | long / H1 | 2021-07-19 | 223.56 | 217.30 | 236.46 | 2.06R | 强上涨腿；回调回到向上的 EMA20/前期支撑；B 后段有较大阴线，记为可交易但非完美小 B |
| DDOG 2021-07-19 | long / H1 | 2021-07-19 | 105.29 | 101.00 | 109.90 | 1.07R | 上涨背景；回调靠近向上的 EMA20 和前期支撑；首障碍仅略超过 1R |
| DDOG 2023-07-24 | long / H1 | 2023-07-24 | 111.63 | 108.50 | 117.45 | 1.86R | 强上涨腿；小实体/重叠回调回到向上的 EMA20 附近；首 B 日较大，后段收缩，保留并降级说明 |
| ZS 2023-09-19 | long / H1 | 2023-09-19 | 156.05 | 152.50 | 167.50 | 3.23R | 上涨腿和 EMA 闸门通过；回调回到 EMA20/前期支撑；9 月 5 日财报落在 A 腿内，单列 event-driven |
| DDOG 2023-03-07 | short / L1 | 2023-03-07 | 74.36 | 78.50 | 63.50 | 2.62R | 下跌背景；回调受控并回到向下的 EMA20/EMA50/前期阻力；2 月 16 日财报后的 aftershock，单列 event-driven |

方向分布：`long=4`、`short=1`；标签分布为 `H1=4`、`L1=1`。

所有合同统一使用 `stop_confirmation`、`max_hold_bars=10`、`gap_policy=skip`。开盘跳过旧触发位时不追价补成交；这是本批历史研究合同，不是生产持仓规则。

## 分组和独立性

普通非事件组：ZS 2021-07-19、DDOG 2021-07-19、DDOG 2023-07-24。事件驱动组：ZS 2023-09-19、DDOG 2023-03-07。每条合同有独立的 `lineage_id`；同一行情段没有用 H1/H2 或 L1/L2 重复计数。事件组不与普通组混合解释。

## 事件证据

- ZS 2021：公司 IR 确认 Q3 FY2021 财报日为 2021-05-25，Q4 FY2021 财报日为 2021-09-09；后者在决策日之后但超出十根 K 线回放窗口。来源：[Q3 FY2021](https://ir.zscaler.com/news-releases/news-release-details/zscaler-reports-third-quarter-fiscal-2021-financial-results)、[Q4 FY2021](https://ir.zscaler.com/news-releases/news-release-details/zscaler-reports-fourth-quarter-and-fiscal-2021-financial-results)。
- DDOG 2021：公司 IR 确认 Q2 FY2021 财报日为 2021-08-05，超出 2021-07-19 决策后的十根 K 线窗口。来源：[Q2 FY2021](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-second-quarter-2021-financial-results)。
- DDOG 2023-07：公司 IR 确认 Q2 FY2023 财报日为 2023-08-08，超出 2023-07-24 决策后的十根 K 线窗口。来源：[Q2 FY2023](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-second-quarter-2023-financial-results)。
- ZS 2023-09：公司 IR 确认 FY2023 Q4 财报日为 2023-09-05，落在候选 A 腿内；因此本合同不是普通非事件样本。下一季度财报日为 2023-11-27。来源：[FY2023 Q4](https://ir.zscaler.com/news-releases/news-release-details/zscaler-reports-fourth-quarter-and-fiscal-2023-financial-results)、[Q1 FY2024](https://ir.zscaler.com/news-releases/news-release-details/zscaler-reports-first-quarter-fiscal-2024-financial-results)。
- DDOG 2023-03：公司 IR 确认 FY2022 Q4 财报日为 2023-02-16，紧邻并影响后续 A 腿；公司在 2023-04-13 公告 Q1 FY2023 财报将在 2023-05-04 发布，后者超出回放窗口。来源：[FY2022 Q4](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-fourth-quarter-and-fiscal-year-2022-financial/)、[Q1 FY2023 日期公告](https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-date-first-quarter-fiscal-year-2023-earnings)。

## 排除记录

- FICO：虽通过市值/流动性范围，但 2024–2026 局部多为事件跳空、宽幅重定价或持续单边，无法在不放宽 B 质量和第一障碍规则的前提下冻结高质量 H/L。
- CDNS、SNPS：可见上涨/下跌腿，但候选多数首障碍不足约 1R，或 A/B 被事件与宽幅 K 线污染。
- VEEV：部分上涨腿由财报跳空启动，普通 H1 与 event-driven A 难以分离；其他局部空间不足。
- DDOG 2025-03-06：视觉上可记为事件后 L1-like，但首障碍与结构止损在严格口径下不足约 1R，排除，不为增加样本而压窄止损。
- ZS 2025-05-12 及多条 2024–2026 候选：前方左侧阻力贴近或 B 腿过宽，记为 observation/borderline，不进入本批。

## 研究边界

本批图像只用于人工识别和冻结，不是量化扫描器输出；Matplotlib 只负责渲染 OHLC、EMA 和成交量。回放器只回答冻结合同在历史价格路径下的成交、跳过、止损、目标或时间退出，不自动识别 H1/L1，也不下载行情。

本批只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。回放报告必须将普通组、事件组、成交/开盘跳过、胜率、实现 R、Wilson 区间、空间合格子集和失败路径分开，若证据不足则保持 `no-new-positive`。

# H/L 第二批人工看图合同资产（2026-08-26）

状态：`research_only / historical_visual_evidence / contract-frozen / not-validated`

本目录保存第二批相互独立 lineage 的人工看图证据。每张图都先看至少两年 Daily 左侧，再复核重要高点、低点、支撑阻力、EMA20/50/200、A/B、回调位置和 META；图上的 H2/L1 只是人工复核后的合同标签，不是程序自动识别结果。合同字段、空间边界和回放结果见[`H/L 第二批合同回放审计`](../../../../backtesting/hl_contract_batch2_replay_2026-08-26_CN.md)。

## 来源与时间边界

- 数据：Yahoo Chart API 历史 Daily OHLCV，通过 agent-reach 的 Jina 公开路由读取；不是实时行情，不连接 Futu OpenD。
- 源数据时区：`America/New_York`；数据和图像生成/复核日期：`2026-08-26`。
- 每张图右端是合同决策日；回放价格快照另存为[`hl_contract_batch2_prices_2026-08-26.csv`](../../../../backtesting/hl_contract_batch2_prices_2026-08-26.csv)。
- 两年窗口按决策日前可见的最近约 2 年 Daily bars 截取；图中不使用决策日之后的价格来冻结合同。
- 图像只服务 PA Research 的人工历史复核，不是量化扫描器输入，不是 Codex Trading 规则，也不连接 Execution Agent。

## 案例图

- [`KLAC H2 2025-06-02`](KLAC_Daily_2y_cutoff_2025-06-02.png)：多头形态清楚，但第一阻力约 `0.70R`，作为空间边界，不进入正向统计。
- [`TSM L1 2025-03-25`](TSM_Daily_2y_cutoff_2025-03-25.png)：空头 L1 公共价格重审；次日小缺口接受开盘重订。
- [`ADBE L1 2026-01-26`](ADBE_Daily_2y_cutoff_2026-01-26.png)：空头 L1 公共价格重审；父级处于转开放空头，市场背景逆势，单独降级解释。

## 依赖关系

三行分别使用 `KLAC-2025-05-local-public`、`TSM-2025-03-public-l1` 和 `ADBE-2026-01-public-l1`，不与第一批 TSLA/CRWD 合同共享局部 A/B lineage。独立 symbol/episode 只解决依赖控制，不能解决样本量、数据源差异或事件/市场背景问题；第二批仍不能验证胜率或盈亏比优势。

# H/L 首批人工看图合同资产（2026-08-26）

状态：`research_only / historical_visual_evidence / not-validated`

本目录保存第一批进入严格回放前的人工看图证据。每张图都先截取至少两年 Daily 左侧，再看局部 H1/H2/L1/L2 读法；图像本身不自动标注 pattern，具体计数、lineage、回调位置、重要高低点、EMA 方向和 META 记录在 [`H/L 首批合同回放审计`](../../../../backtesting/hl_contract_batch_replay_2026-08-26_CN.md) 中。

## 来源与时间边界

- 数据：Yahoo Chart API 历史 Daily OHLCV，通过 agent-reach 的 Jina 公开路由读取；不是实时行情，不连接 Futu OpenD。
- 源数据时区：`America/New_York`；资产生成/复核日期：`2026-08-26`。
- 每张图的右端是该案例的决策日；回放价格快照另存为 [`hl_contract_batch_prices_2026-08-26.csv`](../../../../backtesting/hl_contract_batch_prices_2026-08-26.csv)。
- 图像只服务 PA Research 的人工历史复核，不是量化扫描器输入，不是 Codex Trading 规则，也不连接 Execution Agent。

## 案例图

- [`TSLA H1 2025-08-18`](TSLA_Daily_2y_cutoff_2025-08-18.png)
- [`TSLA H2 2025-08-21`](TSLA_Daily_2y_cutoff_2025-08-21.png)
- [`TSLA L1 2025-03-03`](TSLA_Daily_2y_cutoff_2025-03-03.png)
- [`TSLA L2 2024-03-12`](TSLA_Daily_2y_cutoff_2024-03-12.png)
- [`CRWD H2 2024-10-02`](CRWD_Daily_2y_cutoff_2024-10-02.png)

## 依赖关系

TSLA `2025-08-18` H1 与 `2025-08-21` H2 共享 `TSLA-2025-08-local`，因此只能作为同一局部行情 lineage 的多个尝试保存，不能在统计上当作两个独立样本。TSLA `2025-03-03` L1、TSLA `2024-03-12` L2 和 CRWD `2024-10-02` H2 使用独立的研究 lineage 标识；样本量仍不足以验证胜率或盈亏比优势。

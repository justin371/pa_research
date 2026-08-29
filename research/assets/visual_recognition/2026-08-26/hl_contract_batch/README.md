# H/L 首批人工看图合同资产（2026-08-26）

状态：`research_only / historical_visual_evidence / not-validated`

## Canonical provenance boundary

```text
contract_scope: historical_context_only
data_source: public Yahoo Chart API historical Daily OHLCV via Jina Reader
data_status: historical
as_of_time: per-case decision cutoff
review_time: 2026-08-26; timezone recorded in source notes
timezone: America/New_York
session_state: historical_close
timeframes_seen: Daily
chart_scope: full
daily_context_window: >=2y
major_high_low_review: complete in paired contract review
ema20_50_200_review: complete in paired contract review
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
first_independent_obstacle: paired contract only; not frozen in this asset
pre_entry_space_R: unknown unless trigger and structural stop are independently frozen
space_status: unknown
order_branch: observation_only
label_source: human_chart_review
handoff_status: not_ready
```

这里的 `direction`、`lineage_status` 和 `internal_label` 是五个案例的聚合占位；每个
案例的 long/short、H1/H2/L1/L2、EMA gate、首障碍和订单字段只以配对的合同 CSV/回放审计为准。
资产本身不冻结 `primary_pattern`、订单、空间或统计结果。

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

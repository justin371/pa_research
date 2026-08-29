# Round5 两年 Daily 左侧背景视觉练习资产

状态：`document_status=historical / contract_scope=historical_context_only / research_state=observation_only`

## Canonical provenance boundary

```text
contract_scope: historical_context_only
data_source: read-only historical OHLC snapshot; source material only, not PA Research authority
data_status: historical
as_of_time: per-case cutoff; query timestamp unavailable in original log
timezone: unavailable_in_original_log
session_state: historical_close
timeframes_seen: Daily / 4H / 15m (case-specific)
chart_scope: partial
daily_context_window: >=2y
major_high_low_review: complete in paired historical review; per-case text below
ema20_50_200_review: complete in paired historical review; Daily EMA only
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
direction: no_valid_direction (aggregate; per-case visual direction is descriptive)
lineage_status: pending
internal_label: pending
third_push_state: unclear
range_edge_three_push: pending
range_edge_side: pending
research_state: observation_only
trade_state: observation_only
gate_result: observation_only
handoff_status: not_ready
```

这组无标签资产只负责提供两年 Daily 背景和局部练习图；`primary_pattern`、
`secondary_context`、H1/H2/L1/L2、三推、BOP、MTR、订单和空间不在资产本身冻结。
对应的 canonical 案例摘要、历史别名映射和 `no-new-positive` 结论见配对的
[`Round5 两年 Daily 左侧背景与 ABC/H-L/三推视觉练习`](../../../../visual_recognition_round5_two_year_daily_2026-08-24_CN.md)。
Codex Trading 只提供只读历史素材，不提供本轮规则、代码或执行能力。

## 用途与来源

本轮只保存没有 pattern 标注的历史 OHLC 图，用于 PA Research 的人工视觉复核。pattern、lineage、计数和边界结论写在研究记录中，不写入图像。

- 来源：只读使用 Codex Trading 历史 OHLC 快照 `cohr-revised-20260814/bars.json`，只取 OHLC、成交量和时间周期；本 README 不依赖本机 checkout 路径，Codex Trading 不提供本轮规则。
- 资产生成日期：`2026-08-24`；来源窗口结束：`2026-08-13`。
- 标的：`COHR`、`SPY`、`QQQ`、`IWM`。
- Daily：`2021-01-04`–`2026-08-13`；每个截断案例的左侧 Daily 至少两年，EMA20/50/200 从截断日前可用 Daily 收盘递推计算。
- 4H：约 `2026-01-02`–`2026-08-13`；COHR 另有 15m，三个指数标的的 15m 在该来源中不可用。
- 所有 targeted 图都在决策截断日停止，不使用截断日之后的走势解释形态。

## 背景筛选图

- [`4 标的 Daily 筛选板`](cohr_revised_daily_2021_2026_screen.png)
- [`COHR Daily 全窗口`](US_COHR_daily_full_2021_2026.png)
- [`SPY Daily 全窗口`](US_SPY_daily_full_2021_2026.png)
- [`QQQ Daily 全窗口`](US_QQQ_daily_full_2021_2026.png)
- [`IWM Daily 全窗口`](US_IWM_daily_full_2021_2026.png)

## 8 个截断多周期图

- [`COHR 2026-05-13`](US_COHR_MTF_cutoff_2026-05-13_unlabeled.png)
- [`COHR 2026-06-22`](US_COHR_MTF_cutoff_2026-06-22_unlabeled.png)
- [`SPY 2026-06-15`](US_SPY_MTF_cutoff_2026-06-15_unlabeled.png)
- [`SPY 2026-07-15`](US_SPY_MTF_cutoff_2026-07-15_unlabeled.png)
- [`QQQ 2026-06-22`](US_QQQ_MTF_cutoff_2026-06-22_unlabeled.png)
- [`QQQ 2026-07-17`](US_QQQ_MTF_cutoff_2026-07-17_unlabeled.png)
- [`IWM 2026-05-28`](US_IWM_MTF_cutoff_2026-05-28_unlabeled.png)
- [`IWM 2026-06-25`](US_IWM_MTF_cutoff_2026-06-25_unlabeled.png)

## 证据边界

PA Research 当前视觉协议要求先看两年 Daily 左侧，再看局部周期；本轮 8 个案例的 `daily_context_window` 均为 `>=2y`。这只证明背景字段可完成，不证明 H/L、ABC 或三推计数已经严格成立。SPY、QQQ、IWM 缺少 15m，只能保留 4H 局部证据；COHR 的 15m 也不能替代 Daily/4H 的母腿与 lineage。事件、板块和交易合同没有在本轮 OHLC-only 练习中补齐，相关结论继续保持 `pending`。

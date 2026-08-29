# Round4 历史图表视觉练习资产

状态：`document_status=historical / contract_scope=historical_context_only / research_state=observation_only`

## Canonical provenance boundary

```text
contract_scope: historical_context_only
data_source: read-only historical OHLC snapshot; source material only, not PA Research authority
data_status: historical
as_of_time: 2026-08-10 dataset end; 2026-07-29 targeted cutoff case-specific
timezone: unavailable_in_original_snapshot
session_state: historical_close
timeframes_seen: Daily / 4H / 15m (case-specific)
chart_scope: partial
daily_context_window: <2y
major_high_low_review: partial
ema20_50_200_review: partial
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
direction: no_valid_direction (aggregate; per-case visual direction remains descriptive)
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

Round4 的 `daily_context_window: <2y` 是 canonical 读取；原有的
`two_year_daily: pending` 只能作为历史显示别名。`major_high_low_review` 和
`ema20_50_200_review` 只覆盖现有短窗口，不能冒充用户要求的两年 Daily 左侧完整
复核。资产未标注 `primary_pattern`、`secondary_context`、H1/H2/L1/L2、三推、
BOP 或 MTR；这些只能在配对的历史研究记录中按证据记录。

## 用途

这一轮只保存历史 OHLC 图表，用于 PA Research 的人工视觉练习。图中没有 ABC、H/L 或其它 pattern 标签；标签和结论写在研究记录中，不写回图像。

## 来源与窗口

- 来源：只读使用 Codex Trading 的历史 OHLC 快照 `multisymbol-cohort3-20260812/bars.json`；本 README 不依赖某个本机 checkout 路径，也不把 Codex Trading 规则作为 PA Research authority。
- 该数据集覆盖 42 个标的；Daily 可用窗口约为 `2025-08-11`–`2026-08-10`，同时含 4H 与 15m bars。
- targeted 图在各自的历史决策日期截断；round4 选图板截断到 `2026-07-29`。不得用截断点之后的走势解释截断点的 pattern。
- 资产生成日期：`2026-08-24`；数据窗口结束：`2026-08-10`；targeted 截止点：`2026-07-29`。
- 原始 `h-tpb-gen-20260813` bars 不在 PA Research 资产中，因此本轮图不是对旧登记源文件的复原，而是独立的无标签历史图复核。

对应的历史复核记录见[`Round4 历史图表视觉练习与 H/L/ABC 复核`](../../../../visual_recognition_round4_historical_practice_2026-08-24_CN.md)；资产本身不冻结 pattern、订单、空间或统计结论。

## 资产

- [`42 标的 Daily 筛选板`](cohort3_daily_screen_20260729.png)
- [`7 个旧日期 targeted 多周期图总览`](legacy_targeted_mtf_montage.png)
- [`round4 选中多周期图总览`](round4_selected_mtf_montage.png)
- MRVL 的直接 Daily 复核图：[`MRVL`](MRVL_trading_repo_daily_review.png)
- 直接多周期图：[`AMZN`](US_AMZN_MTF_unlabeled.png)、[`DE`](US_DE_MTF_unlabeled.png)、[`JNJ`](US_JNJ_MTF_unlabeled.png)、[`NFLX`](US_NFLX_MTF_unlabeled.png)、[`NKE`](US_NKE_MTF_unlabeled.png)、[`MSFT`](US_MSFT_MTF_unlabeled.png)、[`XOM`](US_XOM_MTF_unlabeled.png)、[`GOOGL`](US_GOOGL_MTF_unlabeled.png)
- 其余 targeted 图：[`AMZN`](US_AMZN_targeted_unlabeled.png)、[`COP`](US_COP_targeted_unlabeled.png)、[`DE`](US_DE_targeted_unlabeled.png)、[`JNJ`](US_JNJ_targeted_unlabeled.png)、[`META`](US_META_targeted_unlabeled.png)、[`NFLX`](US_NFLX_targeted_unlabeled.png)、[`NKE`](US_NKE_targeted_unlabeled.png)

单标的图文件名中的 `targeted` 或 `MTF_unlabeled` 只表示截断方式和周期，不表示该图已经通过 lineage、两年背景或 pattern 验收。

## 缺失字段

PA Research 当前视觉口径要求先看至少两年 Daily 左侧，再记录 EMA20/50/200、重要高低点、支撑阻力、母腿/尝试/lineage 和失效边界。Round4 数据集只有约一年 Daily，因此新增图统一保留 `daily_context_window: <2y`；短窗口不能制造完整 lineage、H/L 计数或三推结论。

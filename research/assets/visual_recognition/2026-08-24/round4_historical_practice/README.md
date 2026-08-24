# Round4 历史图表视觉练习资产

状态：`visual-research / unlabeled / practice-and-boundary-only`

## 用途

这一轮只保存历史 OHLC 图表，用于 PA Research 的人工视觉练习。图中没有 ABC、H/L 或其它 pattern 标签；标签和结论写在研究记录中，不写回图像。

## 来源与窗口

- 来源：只读使用 Codex Trading 当前 checkout 中的 `.local/research/replay/multisymbol-cohort3-20260812/bars.json`，仅取历史 OHLC。
- 该数据集覆盖 42 个标的；Daily 可用窗口约为 `2025-08-11`–`2026-08-10`，同时含 4H 与 15m bars。
- targeted 图在各自的历史决策日期截断；round4 选图板截断到 `2026-07-29`。不得用截断点之后的走势解释截断点的 pattern。
- 原始 `h-tpb-gen-20260813` bars 不在当前 checkout，因此本轮图不是对旧登记源文件的复原，而是独立的无标签历史图复核。

## 资产

- [`42 标的 Daily 筛选板`](cohort3_daily_screen_20260729.png)
- [`7 个旧日期 targeted 多周期图总览`](legacy_targeted_mtf_montage.png)
- [`round4 选中多周期图总览`](round4_selected_mtf_montage.png)
- MRVL 的直接 Daily 复核图：[`MRVL`](MRVL_trading_repo_daily_review.png)

单标的图文件名中的 `targeted` 或 `MTF_unlabeled` 只表示截断方式和周期，不表示该图已经通过 lineage、两年背景或 pattern 验收。

## 缺失字段

PA Research 当前视觉口径要求先看至少两年 Daily 左侧，再记录 EMA20/50/200、重要高低点、支撑阻力、母腿/尝试/lineage 和失效边界。Round4 数据集只有约一年 Daily，因此新增图统一保留 `two_year_daily: pending`；短窗口不能制造完整 lineage、H/L 计数或三推结论。

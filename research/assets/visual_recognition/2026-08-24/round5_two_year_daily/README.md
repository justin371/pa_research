# Round5 两年 Daily 左侧背景视觉练习资产

状态：`visual-research / unlabeled / two-year-background / practice-and-boundary-only`

## 用途与来源

本轮只保存没有 pattern 标注的历史 OHLC 图，用于 PA Research 的人工视觉复核。pattern、lineage、计数和边界结论写在研究记录中，不写入图像。

- 来源：只读使用 Codex Trading 当前 checkout 的 `.local/research/replay/cohr-revised-20260814/bars.json`，只取 OHLC、成交量和时间周期；Codex Trading 不提供本轮规则。
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

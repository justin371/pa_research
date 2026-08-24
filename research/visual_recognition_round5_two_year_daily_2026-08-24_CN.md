# Round5 两年 Daily 左侧背景与 ABC/H-L/三推视觉练习（2026-08-24）

状态：`visual-research / two-year-background / practice-and-boundary-only / not-statistical / no-new-positive`

## 一、口径与数据

本轮只按 PA Research 当前的[`H/L lineage 与三推状态视觉边界复核`](h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)、[`完整图表视觉复核工作流边界审计`](visual_review_workflow_boundary_audit_2026-08-24_CN.md)和[`视觉 pattern 快筛协议`](visual_pattern_triage_protocol_CN.md)执行。Codex Trading 只提供只读历史 OHLC 素材，不提供规则；本轮没有修改 Codex Trading。

来源是 `cohr-revised-20260814/bars.json`，包含 `COHR`、`SPY`、`QQQ`、`IWM` 的 Daily（`2021-01-04`–`2026-08-13`）和 4H（约 `2026-01-02`–`2026-08-13`）；COHR 另有 15m。先查看完整 Daily 背景，再查看局部 Daily/4H/15m；每个 targeted 图都在截断日停止，避免把后续走势倒灌到识别时点。

EMA20/50/200 是按截断日前全部可见 Daily 收盘递推的背景线；重要高低点和支撑阻力是图上可见区域，不是自动线，也不替代结构失效。所有案例都明确写出主计数周期、母腿、尝试、lineage、首障碍候选和限制；`H1/H2/L1/L2-like` 与 `three-push` 只表示可练习的外形或边界，不是严格生产标签。

资产入口：[`Round5 两年 Daily 视觉练习资产`](assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md)。

## 二、8 个两年背景案例

### 1. COHR · 2026-05-13：ABC + H1-like 候选

图：[`COHR 2026-05-13`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_COHR_MTF_cutoff_2026-05-13_unlabeled.png)

- `review_timeframe: Daily`；4H/15m 只作局部补充；`daily_context_window: >=2y`；`left_context_review: complete`；图无 pattern 标注。
- `daily_ema20_50_200: 337.11 / 301.49 / 210.64`；截断日收盘约 `403.71`，在三条 EMA 上方。
- 两年窗口可见最高约 `413.00`（2026-05-13），最低约 `45.58`（2025-04-04）。局部重要点是 `2026-03-30` 低约 `215.55`、`2026-04-22` 高约 `364.80`、`2026-04-28` 低约 `291.00`；支撑候选 `291–308`，旧阻力 `354–365`，当前压力约 `413`。
- `parent_state: open_trend`；母腿可写为 `3-30 215.55 -> 4-22 364.80`，B 回撤到 `4-28 291.00`。第一次方向恢复在 Daily `5-13` 前逐步形成，4H 的 `5-06` 高约 `354.20`、`5-07` 低约 `308.17` 是其内部波动，不足以单独制造 Daily H2。
- `lineage_status: same-lineage-provisional`；`count_result: ABC-like + H1-like / pending`；尚未看见清楚的“第一次失败后第二次有意义尝试”，因此不冻结 H2。
- `first_obstacle_candidate: 413` 当前高点；此前阻力已被快速穿越，后续上方没有在截断前可见的独立障碍，空间状态为 `price-discovery / boundary`。
- 限制：COHR 的 15m 只覆盖局部后段，不能替代母级 Daily 计数；事件/板块没有在本轮 OHLC-only 复核中核对；快速扩张和信号过晚使其只能是 `pattern_candidate / first-obstacle-boundary`。

### 2. COHR · 2026-06-22：三推 / 区间重复测试边界

图：[`COHR 2026-06-22`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_COHR_MTF_cutoff_2026-06-22_unlabeled.png)

- `review_timeframe: 4H`，Daily 负责母级背景；`daily_context_window: >=2y`；`daily_ema20_50_200: 384.45 / 355.83 / 250.36`；截断日收盘约 `425.48`，仍在三条 EMA 上方。
- 两年窗口最高约 `440.00`（2026-06-03），最低约 `45.58`（2025-04-04）。局部支撑候选 `335–344`（5-29/6-09 附近）和 `376–393`；上方压力 `439–440`。
- Daily 母级来自 `3-30 215.55 -> 4-22 364.80`，随后形成 `5-13 413.00`、`6-03 440.00` 和 4H `6-16 424.00` / `6-22` 再测上沿的一组高位尝试。
- `parent_state: open_trend -> mature upper boundary`；`lineage_status: unclear-to-range`；可视为 `three-push / range-repeat candidate`，但 `6-03` 新高和上沿接受改变了原始回调故事，不能直接叫 H3/L3 衰竭。
- `attempt_1: 5-13 upper test`；`attempt_2: 6-03 new extreme`；`attempt_3: 6-16/6-22 upper retest`。第三推的压力状态尚未完成分流，`count_result: three-push boundary / not_h3_l3 / pending`。
- `first_obstacle_candidate: 439–440`；多头空间在上沿明显拥挤，空头若没有反向接受也不能仅凭三次测试建立反转合同。
- 限制：4H 有重复上沿但缺少完整反向确认；15m 只能补局部时序；事件/板块未核对。状态为 `boundary_candidate / range-repeat`。

### 3. SPY · 2026-06-15：H2-like 第二次尝试边界

图：[`SPY 2026-06-15`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_SPY_MTF_cutoff_2026-06-15_unlabeled.png)

- `review_timeframe: 4H`；Daily 背景完整，`daily_ema20_50_200: 740.24 / 724.69 / 680.97`；截断日收盘约 `752.89`，位于三条 EMA 上方。
- 两年窗口最高约 `758.45`（2026-06-02），最低约 `475.12`（2025-04-07）。局部支撑候选 `720–730`（5-19/6-09），更低支撑约 `716`；阻力 `754–758`。
- `parent_state: open_bull`；母级方向可从 `3-30 627.66` 延伸到 `5-14 747.60`，之后 B/回撤扩展到 `6-09 720.73`。第一次恢复/尝试是 `6-02 758.45`，随后回撤并失败/不足；第二次尝试是 `6-15 754.74`。
- `lineage_status: same-lineage-provisional`；`count_result: ABC-like + H2-like / count-pending`。第一次失败证据比单根 EMA 触碰更完整，但第二次仍在原高点压力下，不能当严格 H2 正例。
- `first_obstacle_candidate: 758.45`；触发附近首障碍很近，空间为 `first-obstacle-boundary`。
- 限制：来源没有 SPY 15m，4H 不能补写 15m 确认；父级虽然多头，局部已接近高位重复测试；事件/板块未核对。状态为 `pattern_candidate / boundary_candidate`。

### 4. SPY · 2026-07-15：三推 / 上沿重复测试

图：[`SPY 2026-07-15`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_SPY_MTF_cutoff_2026-07-15_unlabeled.png)

- `review_timeframe: 4H`；`daily_context_window: >=2y`；`daily_ema20_50_200: 746.47 / 736.31 / 692.57`；截断日收盘约 `754.81`，三线多头排列。
- 两年最高仍约 `758.45`（6-02），最低约 `475.12`（2025-04-07）；局部支撑 `716–740`，上沿压力 `754–758`。
- 可见高位尝试包括 `6-02 758.45`、`6-15 754.74`、4H `7-06 752.41`、`7-10 755.42` 和截断附近再测。它们围绕同一上沿反复，而不是清楚的开放趋势新 A。
- `parent_state: mature_range / upper_edge`；`lineage_status: unclear-to-range`；`count_result: three-push-like / range-repeat / not_h3_l3`。没有把三次测试自动改写成楔形或反转。
- `first_obstacle_candidate: 758.45`；多头首障碍拥挤；若反向观察，第一支撑在 `740` 附近，仍需独立反向接受。
- 限制：没有 15m；多次高点间有局部重建，计数尺度不唯一；事件/板块未核对。状态为 `boundary_candidate / observation_only`。

### 5. QQQ · 2026-06-22：三推 / 区间重复测试边界

图：[`QQQ 2026-06-22`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_QQQ_MTF_cutoff_2026-06-22_unlabeled.png)

- `review_timeframe: 4H`；`daily_context_window: >=2y`；`daily_ema20_50_200: 722.31 / 695.88 / 630.27`；截断日收盘约 `737.95`，在三线之上。
- 两年最高约 `747.83`（6-03），最低约 `400.01`（2025-04-07）。局部支撑候选 `685–720`，阻力 `744–748`。
- 4H 上沿尝试依次可见 `6-03 747.83`、`6-15 743.94`、`6-22 745.45`；中间有回撤和停顿，但价格在同一高位带被接受。
- `parent_state: open_bull -> mature upper range`；`lineage_status: same-pressure-zone-provisional`；`count_result: three-push / range-repeat / not_h3_l3`。它是很好的“次数够了但不能自动做反向”的练习。
- `first_obstacle_candidate: 747.83`；多头空间贴近前高，空头第一支撑在 `720`/`685` 分层，需等控制权变化。
- 限制：没有 15m；4H 三次测试不等于 Daily 三推；事件/板块未核对。状态为 `boundary_candidate / observation_only`。

### 6. QQQ · 2026-07-17：bearish L1/L2-like 过渡边界

图：[`QQQ 2026-07-17`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_QQQ_MTF_cutoff_2026-07-17_unlabeled.png)

- `review_timeframe: 4H`；`daily_context_window: >=2y`；`daily_ema20_50_200: 715.63 / 705.92 / 644.38`；截断日收盘约 `695.33`，跌到 EMA20/50 下方但仍高于 EMA200。
- 两年最高约 `747.83`（6-03），最低约 `400.01`（2025-04-07）。局部支撑 `686–701`，反向压力 `724–748`。
- 4H 可读为下降 A `6-22 745.45 -> 6-26 702.81`；第一次反弹到 `6-30 737.62` 后失败，第一次空头推进到 `7-08 700.91`；第二次反弹到 `7-10 726.39` 后再向下到 `7-17 686.76`。
- `parent_state: Daily long trend -> 4H transition/bearish`；`lineage_status: provisional`；`count_result: bearish L1/L2-like / count-pending`。顺序像 L1/L2，但高周期仍处于状态切换，不能把它当普通开放空头趋势正例。
- `first_obstacle_candidate: 686.76`；若观察空头路径，首支撑已经很近，空间边界明显；向上重新接受 `724–748` 会削弱当前空头 lineage。
- 限制：没有 15m；父级过渡、局部区间化和重复反弹使 lineage 不够干净；事件/板块未核对。状态为 `pattern_candidate / boundary_candidate / pending`。

### 7. IWM · 2026-05-28：ABC + H2-like 候选

图：[`IWM 2026-05-28`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_IWM_MTF_cutoff_2026-05-28_unlabeled.png)

- `review_timeframe: Daily`；4H 作局部复核；`daily_context_window: >=2y`；`daily_ema20_50_200: 281.24 / 272.93 / 252.94`；截断日收盘约 `291.34`，在三线之上。
- 两年最高约 `292.05`（5-28），最低约 `169.50`（2025-04-07）。局部支撑 `269–278`，阻力 `286.90–292.05`。
- 母腿可写为 `3-30 238.12 -> 4-21 279.13`，B 回撤到 `4-29 269.72`；第一次恢复到 `5-07 286.90`，随后再次回撤到 `5-19 269.99`；截断日再出现第二次有意义恢复到 `5-28 292.05`。
- `parent_state: open_bull`；`lineage_status: same-lineage-provisional`；`count_result: ABC-like + H2-like / count-pending`。它最适合练习“第一次恢复不充分后再看第二次”，但 `5-07` 新高和后续 B 扩展也可能构成 reset，不能冻结严格 H2。
- `first_obstacle_candidate: 292.05`；多头在前高附近空间拥挤；若把 `5-19` 支撑作为结构边界，需另立合同，不能用局部窄止损替代母级风险。
- 限制：没有 15m；4H 支持几何但不能改变 Daily 计数；事件/板块未核对。状态为 `pattern_candidate / first-obstacle-boundary / count-pending`。

### 8. IWM · 2026-06-25：三推扩张 / 延续分流

图：[`IWM 2026-06-25`](assets/visual_recognition/2026-08-24/round5_two_year_daily/US_IWM_MTF_cutoff_2026-06-25_unlabeled.png)

- `review_timeframe: 4H`；`daily_context_window: >=2y`；`daily_ema20_50_200: 290.92 / 282.74 / 259.48`；截断日收盘约 `298.91`，在三线之上。
- 两年最高约 `301.50`（截断前局部高位），最低约 `169.50`（2025-04-07）。局部支撑 `277–289`，阻力 `292–301.50`。
- 上沿尝试依次可见 `5-28 292.05`、`6-04 292.18`、`6-15 297.91` 和 `6-25` 附近 `301.50`；第三次及后续尝试更高，既可能是扩张/高潮，也可能是趋势延续。
- `parent_state: open_bull -> mature upper boundary`；`lineage_status: unclear-to-range`；`count_result: three-push-like / expansion-or-climax-vs-continuation / pending`。不把第三推的更高价格直接解释成衰竭。
- `first_obstacle_candidate: 301.50`；多头首障碍位于当前上沿，空间拥挤；下方 `289` 是最近的结构边界候选。
- 限制：没有 15m；没有第三推后的反向接受，不能升级 MTR；事件/板块未核对。状态为 `boundary_candidate / observation_only`。

## 三、Round5 结论

1. **两年背景字段补齐**：4 个标的、8 个 targeted 案例均可完成 `daily_context_window: >=2y`，并记录 EMA20/50/200、主要高低点和支撑阻力。这个进展只解决左侧背景缺口，不等于 pattern 计数通过。
2. **最有帮助的 ABC/H-L 练习**：COHR `2026-05-13` 是 `ABC + H1-like`；SPY `2026-06-15`、IWM `2026-05-28` 可练习第一次不足后的 H2-like，但都受首障碍和 lineage/reset 限制；QQQ `2026-07-17` 提供 bearish L1/L2-like 的状态切换反例。
3. **最有帮助的三推边界**：COHR、SPY、QQQ 和 IWM 都出现高位重复测试；其中 COHR/QQQ 更像 `range-repeat`，IWM 需要保留 `expansion-or-climax` 与 `continuation` 对称分支，SPY 则显示成熟上沿如何阻止强行做 H3/L3。
4. **严格限制仍然有效**：8 个案例没有一个冻结为 strict same-lineage H1/H2/L1/L2 或 H3/L3；没有新增可比正向结果。SPY/QQQ/IWM 缺 15m，COHR 的 15m 只补局部；事件、板块和订单层均不在本轮 OHLC-only 证据中。

```text
round5_two_year_daily_symbols: 4
round5_targeted_multitimeframe_cases: 8
round5_two_year_daily_complete_cases: 8
round5_strict_same_lineage_freezes: 0
round5_new_comparable_positive_samples: 0
round5_pattern_candidates: 4
round5_three_push_or_range_boundaries: 4
no-new-positive: maintained
scope: PA Research only; no scanner; no Execution Agent; no Codex Trading changes
```

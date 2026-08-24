# ABC + H/L 分层历史结果审计（2026-08-24）

状态：`research-only / stratified-outcome-audit-v0.1 / pilot / not-statistical`

## 目的与范围

把 ABC、H1/L1 和 H2/L2 放进同一个研究族，但保留它们的层级关系：

- `ABC` 是母结构：方向性 A 腿、回调 B 腿、原方向 C 恢复；
- `H1/L1` 是 C 恢复中的第一次有意义尝试；
- `H2/L2` 是第一次尝试失败或不足后，同一回调 lineage 中的第二次尝试；
- `H3/L3`/三推先单独记录状态，不在本轮与 H1/H2 混算。

本文件的目标是找到“值得继续补样本”的分层，而不是从少数案例直接宣布高胜率。它只使用 PA Research 已有的案例和可追溯历史记录，不创建量化扫描器，不连接 Execution Agent，也不修改 Codex Trading。

视觉定义见[`ABC 趋势延续目录`](../patterns/03_abc_continuation/README.md)；同一 lineage、两年左侧背景和 reset 规则见[`H/L lineage 与三推状态视觉边界复核`](h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)。

## 一、分层合同

每个样本先记录母结构，再记录局部尝试：

```text
parent_pattern: ABC_CONTINUATION / not_abc / pending
parent_state: open_trend / range_edge / transition / event-or-gap / unclear
side: bull / bear
attempt: H1 / H2 / L1 / L2 / H3 / L3 / unclear
lineage_group:
review_timeframe:
A_quality: strong-looking / directional / ordinary / unclear
B_state: controlled / deep-late-controlled / uncontrolled / range-like / unclear
trigger_contract: same-contract-stop / close-confirmation / low-cycle-confirmation / gap-reprice / limit-retest / observation-only
```

不能把下列分支混成一个统计样本：

1. `ABC + H1/L1` 与 `ABC + H2/L2`；
2. Daily 结构止损与 15m/60m 独立短线止损；
3. 原始 stop、开盘后 gap-reprice、limit-retest 和收盘确认；
4. 开放趋势、区间边缘和过渡背景；
5. 同一母级行情中的多个触发点。

## 二、胜率与盈亏比口径

现有案例大量记录了“首障碍到达”和“形态成立、但不交易”。这些是过程证据，不能直接改写成胜负。统一审计字段如下：

| 字段 | 允许的记录 | 统计含义 |
| --- | --- | --- |
| `fill_status` | `filled / no-fill / opening-skip / unproven` | 是否有可证明的合同成交；未成交不进入交易胜率分母 |
| `entry_stop_target_frozen` | `yes / no` | 入场、结构失效、目标和时间边界是否在结果发生前写清 |
| `path_result` | `first-obstacle-reached / invalidated / no-fill / pending` | 只描述价格路径，不等于胜负 |
| `realized_R` | 数值 / `not-frozen` | 必须基于实际或明确定义的成交与结构止损，不能用窄止损事后美化 |
| `trade_result` | `win / loss / scratch / pending / not-applicable` | 只有目标、止损、成交和结束条件齐全才可计算 |
| `space_to_first_obstacle_R` | 事前粗略区间 | 触发到第一独立障碍的几何空间，不是实际盈亏比 |

因此：

- `process-target-reached` 只能写入 `path_result`，不能直接算 `win`；
- `valid_no_trade` 不是 `loss`，而是交易合同没有被授权；
- 原 stop 未成交但 gap-reprice 后到达首支撑，只进入 `gap-reprice` 子层；
- 没有统一的预设目标和结束条件时，`win_rate` 与 `realized_R` 保持 `not-computable`；
- 同一 lineage 的多个尝试按一个母级样本处理，不能按文件数量堆高胜率。

## 三、首批可追溯案例账本

以下记录只汇总已有文件中的前置结构、合同和过程结果；没有把后续走势倒灌为当时已知证据。`space_R` 是现有研究文件的粗略首障碍空间，不是统一回测结果。

| 案例 | ABC/H-L 分层 | 主要背景与合同 | 首障碍空间 | 已知过程结果 | 当前统计用途 |
| --- | --- | --- | --- | --- | --- |
| [`NFLX 2025-02-14–03-28`](nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md) | `ABC + L1-like` | 强-looking A、深但后段受控 B；无开盘缺口；盘中 stop 与收盘确认分开 | 约 `1.4R–1.9R` | 首支撑后来到达；成交/目标口径仍未统一 | **开放趋势空头几何候选**；不能算胜率 |
| [`TSM 2025-02-14–03-28`](tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) | `ABC + L1-like` | 强 A、受控 B；原 stop 被小缺口越过；只审计 gap-reprice | 约 `1.6R+`（重订分支） | 重订路径到达首支撑；原 stop 与旧价 limit 未成交 | **独立 gap-reprice 子层**；不得混入无缺口基准 |
| [`AMZN 2024-09-23–10-15`](amzn_bearish_abc_l1_no_gap_first_support_boundary_2024-09-23_2024-10-15.md) | `ABC + L1-like` | 普通/方向性 A、深 B；无 gap 但板块混合 | 约 `1.1R–1.4R` | 订单可重建，但研究结果未冻结 | **边界对照**；不能因无 gap 升级 |
| [`MCD 2025-05-20–06-25`](mcd_bearish_abc_l1_counter_market_first_support_2025-05-19_2025-06-27.md) | `ABC + L1-like` | strong-looking A、短而受控 B；触发时板块只部分转弱 | 约 `0.66R–0.78R` | 首支撑先到，但结构上事前已被否决 | **no-trade 控制组**；不是亏损样本 |
| [`CRWD 2024-09-11–10-11`](crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md) | `ABC + H2-like` | 强 A、深 B 后段稳定；低周期 buy-stop 可重建；事件背景另列 | 约 `1.5R–1.9R` | 首阻力后来被穿越；事件/成交口径仍未完全冻结 | **多头 H2 几何候选**；样本不足 |
| [`NVDA 2024-09-11–09-25`](nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md) | `ABC + H2` | 深但后段受控 B；Daily 与低周期是两个不同 thesis | Daily 约 `0.9R`；低周期约 `1.9R` | 低周期路径后来穿过首阻力簇 | **低周期独立合同候选**；不得与 Daily 合并 |
| [`TSLA 2025-08-06–08-22`](tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) | `ABC + H2` | 深 B 后段收缩；H1 失败后 H2；日线追入与 15m thesis 分开 | 低周期约 `1.27R–1.32R`；Daily 不足 `1R` | 低周期分支到达第一阻力；日线方案保持 no-trade | **多周期合同分层样本**；不是无条件正例 |
| [`TSLA 三案例矩阵`](tsla_abc_h1_h2_comparison_matrix.md) 中的 `2025-09-04` | `ABC + H2-like` | 与 `2025-08-22` 属同一更大行情 lineage；深 B 后 H2-like；次日 gap | 约 `0.59R`（Daily） | gap 后原理想合同失效 | **依赖样本/边界组**；不能与 `2025-08-22` 独立计数 |
| [`ADBE 2026-01-12–01-27`](adbe_bearish_abc_l1_visual_screen_2026-01-12_2026-01-27.md) | `ABC + L1-like` | 过渡转空、强-looking A、受控 B；市场逆势 | 空间初步优于拥挤边界，精确 R 未冻结 | 尚无统一结果记录 | **transition 子层**；不与开放趋势合并 |
| [`COST 2024-05-13–05-16`](cost_bullish_h1_first_obstacle_boundary_2024-05-13_2024-05-16.md) | `ABC + H1-like` | 信号 K 和低周期触发清楚，但高点簇贴近触发 | 约 `0.8R` 或更差 | 第一阻力事前否决，且原价被开盘跳过 | **H1 首障碍控制组** |

## 四、初步分层结果

| 分层 | 当前独立证据 | 可以说什么 | 不能说什么 |
| --- | --- | --- | --- |
| `ABC + L1`、强 A、受控/深后段受控 B、无 gap、首障碍约 `1.4R+` | NFLX：`n=1` 独立 lineage | 值得优先补充同口径样本 | 不能称高胜率，也不能把一次首支撑到达算成胜率 |
| `ABC + L1`、gap-reprice 后仍有空间 | TSM：`n=1` | 可以作为独立重订合同研究 | 不能与原 stop 或无 gap 样本混算 |
| `ABC + H2`、深 B 后段稳定、低周期确认、首障碍约 `1.5R+` | CRWD、NVDA、TSLA：有条件候选，但周期/事件/止损不同 | 是下一轮最值得标准化的 H2 分层 | 不能把 Daily `0.9R` 和低周期 `1.9R` 合并，也不能称已有稳定胜率 |
| `ABC + H1/L1`、首障碍低于约 `1R` | MCD、COST、SPY、JNJ 等多个边界 | 首障碍是有效的提前否决条件 | 不能把这些 valid-no-trade 当作策略亏损率 |
| `ABC + transition` 或 counter-market | ADBE、MCD 等 | 需要单独分层、降低可比性 | 不能与普通开放趋势样本合并 |

当前最值得继续寻找的不是“所有 H1/H2 的平均胜率”，而是两组可比样本：

1. `ABC + L1/L1-like + strong A + controlled/deep-late-controlled B + no-gap + first obstacle >= 1.4R`；
2. `ABC + H2/H2-like + first attempt failed + same lineage + low-cycle trigger confirmed + first obstacle >= 1.4R`。

两组仍须把多头/空头、开放趋势/过渡、Daily/低周期合同和事件状态分开。`gap-reprice`、区间边缘、MTR 和三推不进入这两个基准池。

## 五、进入胜率审计前的最小门槛

每个新样本必须在结果发生前冻结：

1. 主周期、两年左侧背景、A/B、H/L 计数和 `lineage_group`；
2. signal bar、触发价、成交/未成交规则和订单合同；
3. 结构失效位、第一独立障碍和预设目标/时间边界；
4. 事件、板块/市场状态和是否为 gap-reprice；
5. `MAE/MFE`、首障碍是否到达、是否先失效、实际 `realized_R`；
6. 该样本是否与已有样本共享母级行情。

统计时使用三层结果：

```text
process_result: filled / no-fill / opening-skip / path-target-reached / invalidated
trade_result: win / loss / scratch / pending / not-applicable
evidence_status: comparable / conditional / excluded / dependent-lineage
```

只有 `filled + entry_stop_target_frozen=yes + trade_result` 完整的样本才进入胜率分母。样本太少、合同不一致或共享 lineage 时只做描述，不做排名。未来若要把研究结论移交交易系统，还需要独立的样本外复核，不能由本文件直接升级。

## 当前结论

```text
abc_hl_stratification: established-for-research
fully_comparable_trade_samples: 0 under the unified outcome schema
win_rate: not-computable
realized_R_distribution: not-computable
priority_geometry_strata: ABC+L1 no-gap space-positive; ABC+H2 late-stabilized low-cycle
no_new_positive: maintained
scope: PA Research only; no scanner; no Execution Agent; no Codex Trading changes
```

这一步已经把“找机会”从单纯看形状推进到“先分层、再补同口径结果”。目前可以说哪些分层值得继续找样本，但还不能诚实地说哪一层已经证明了高胜率和良好盈亏比。

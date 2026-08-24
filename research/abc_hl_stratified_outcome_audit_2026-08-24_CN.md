# ABC + H/L 分层历史结果审计（2026-08-24）

状态：`research-only / stratified-outcome-audit-v0.4 / pilot / not-statistical`

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

## 六、补充 H2/L1 对照审计

本轮继续检查现有仓库中最接近两条候选分层、但尚未进入首批账本的案例。它们的共同作用是验证筛选条件是否会把“看起来像”误报成机会。

| 案例 | 目标分层 | 前置事实与空间 | 排除/保留原因 |
| --- | --- | --- | --- |
| [`AMZN 2024-12-09–12-11`](amzn_bullish_h2_shallow_b_boundary_2024-12-09_2024-12-11.md) | `ABC + H2-like`、强 A、controlled-B、低周期确认 | 无开盘跳过；XLY 同向；触发后独立左侧阻力未冻结，`223.5–224.2` 结构风险较宽；后续 `233` 只作过程审计 | `follow-through-mixed / event-context-pending`；不能加入无事件、空间已证实的 H2 正向池 |
| [`V 2024-05-06–05-17`](v_bullish_abc_h2_no_gap_first_obstacle_boundary_2024-05-06_2024-05-17.md) | `ABC + H2-like`、深但后段稳定、无 gap 低周期确认 | 低周期触发可重建；第一阻力簇 `276.89–277.72`，约 `0.85R–1.05R`，止损缓冲后更差 | `valid_no_trade / first-obstacle-boundary`；是空间控制组，不是正向样本 |
| [`KLAC 2025-05-07–06-03`](klac_h2_case_study_2025-05-07_2025-06-03.md) | `ABC + H2`、重复支撑、深 B 后段稳定 | H2 触发和 15m 确认清楚；首阻力 `79.03–79.79`，约 `0.8R–1.0R`；远端 MM 不能越过首障碍 | `research_positive_conditional` 仅指形态/合同可研究；几何仍为边界，不能加入空间正向基准 |
| [`TSLA 2025-12-08–12-12`](tsla_h1_h2_case_study_2025-12-08_2025-12-12.md) | `ABC + H2-like`、强 A、EMA20 附近二次测试 | H2 形态可读；触发上方 `467–474` 左侧阻力，日线约 `0.2R–0.4R`；信号 K 过宽 | `first-resistance-no-trade`；形态样本保留，交易结果不进入胜率池 |
| [`TSLA 2026-05-15–05-22`](tsla_h1_h2_case_study_2026-05-15_2026-05-22.md) | `ABC + H1/H2-like`、深回撤至 EMA50/200 与主要支撑 | Daily 直接触发到 `434.66` 约 `0.72R`；低周期可另立合同，但不能用窄止损替换母级结构风险 | `daily-valid-no-trade / low-cycle-contract-separate`；不能与标准 Daily H2 合并 |

补充审计后的变化是：H2-like 案例数量增加了，但**符合“同一合同、同一背景、首障碍有空间、事件已核对、结果可回放”全部条件的样本数量没有增加**。因此本轮不把任何新案例加入 `ABC+H2` 的空间正向基准，也不改变 `no-new-positive`。

## 七、借鉴 Codex Trading 的近似 pattern 审计

范围说明：本节只回看历史图表；所有 pattern、lineage、reset 和缺失字段口径以 PA Research 当前的[`H/L lineage 与三推状态视觉边界复核`](h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)、[`视觉复核工作流边界审计`](visual_review_workflow_boundary_audit_2026-08-24_CN.md)和[`视觉 pattern 快筛协议`](visual_pattern_triage_protocol_CN.md)为准。Codex Trading 只提供历史图表或 OHLC 资产，不提供规则。

本轮只读检查了 Codex Trading 的两类历史材料，并按“只有有帮助的图才保留为参考”筛选：

- `C:\Users\lwang\Documents\Codex\worktrees\trading\research\2026-08-13-legacy-process-register.json`：15 条历史 Daily 过程登记，标签包括 H1/H2/L1/L2/H3/L3。它引用的 `h-tpb-gen-20260813/bars.json` 和 `validation-fixed.json` 在当前 checkout 不存在，Git 对象历史中也没有可重放副本；这些登记行不计为图表案例，也不据此做视觉判断。
- `C:\Users\lwang\Documents\Codex\worktrees\trading\research\2026-08-13-mrvl-tpb-case-review_CN.md` 与其 `bars.json`：可重建 MRVL 的无标签 Daily 图，用于直接视觉复核。该 Trading 数据集只有约一年 Daily 左侧，不足以替代 PA Research 要求的两年背景，因此两年高低点和 EMA 背景仍以 PA Research 的独立视觉资产复核。

这里采用“近似对应即可进入研究候选层”的宽松视觉标准，但不放宽限制条件。`H1/H2/L1/L2` 仍只是当前回调中的腿数描述；没有同一 lineage、结构位置、守住、确认和首障碍，就只能记作 `pattern_candidate` 或 `boundary_candidate`。

### 7.1 登记表的处理

登记表中的 H/L 标签只用于确认“曾经存在待复核的历史日期”，不作为图表案例。由于缺少源图，无法逐项记录两年 Daily、EMA20/50/200、重要高低点/支撑阻力、母腿/尝试/lineage 或首障碍；本节不把它们混入视觉练习数量。

### 7.2 唯一保留的直接图形参考：MRVL

对 Codex Trading 的 MRVL bars 重新绘制无 pattern 标签的 Daily 图后，可以直接看到：3 月初强方向性 A 腿，随后两段逆势回撤，3 月 19 日回到约 `85` 的结构/EMA20 区域，3 月 20 日越过前一根信号高点。这是一个可借鉴的 `ABC-like + H2-like + TPB` 视觉候选，而不是因为文件已经写了 H2 才接受该标签。

| 视觉复核字段 | MRVL 观察与证据状态 |
| --- | --- |
| 两年 Daily 左侧 | **未满足**：当前 bars 只有约一年（`2025-08-11`–`2026-08-10`，251 根 Daily）；不能声称两年背景已完成。 |
| EMA20/50/200 | 决策日 `2026-03-19` 本地重算约 `85.90 / 83.91 / 81.85`；只作背景汇合，不作 setup、止损或首障碍。 |
| 重要高低点、支撑阻力 | A 腿附近 `2026-03-06` 高约 `93.33`、`2026-03-10` 高约 `94.98`；回撤低点约为 `2026-03-13` 的 `86.76`、`2026-03-18` 的 `87.10`、`2026-03-19` 的 `85.07`。可见支撑/回测区约 `85–86.5`；`93.37` 与 `94.98` 是决策前可见的近端/远端阻力候选。 |
| 母腿、尝试与 lineage | 母腿是 `3-06`–`3-10` 的方向性上冲；同一 Daily 回撤内先有一次恢复不足，再有 `3-19` 信号、`3-20` 越过 `3-19` 高点的 H2-like 第二次尝试。计数仍是 provisional，不能把 `5-12` 接成同一 episode。 |
| 首障碍与空间 | entry `89.6730`、结构 stop `84.50`；到 `93.37` 约 `0.71R`，到 `94.98` 约 `1.03R`。按 PA Research 当前案例合同，近端首障碍不足 `1R` 时保留为边界；远端口径仍是低 R/R 条件带。 |
| 关键限制 | 无 15m 触发/确认；`3-30` 异常波幅是事前警告；不能用后续上涨或 `5-12` 走势倒灌验证。分类为 `visual_candidate / space-boundary / 15m-evidence-missing`。 |

但首障碍审计同时成立：

- 入场约 `89.6730`、结构止损约 `84.50` 时，到 `93.37` 只有约 `0.71R`；
- 只有把更远的 `94.98` 当作第一障碍时才约 `1.03R`，仍进入低 R/R 条件带；
- 3 月 30 日的异常波幅和后续恢复不能倒灌到 3 月 20 日的决策；5 月 12 日也没有独立的 episode、信号、成交、止损和首障碍记录。

因此 MRVL 可以借鉴“怎样从图上读出 H2-like”，但不能借鉴为“高胜率 H2”或空间正向样本。它应进入 `visual_candidate / space-boundary / 15m-evidence-missing` 控制组。

### 7.3 跨仓库借鉴后保留的硬限制

1. 先看两年 Daily 左侧背景、EMA20/50/200、重要高低点和支撑阻力，再看 4H/1H/15m；Trading 回放中只有约一年 Daily 数据的案例，左侧背景标为 `insufficient_for_two_year_review`。
2. H2/L2 必须有同一回调中的第一次失败/不足与第二次有意义的尝试；两次相似价格、两个低点或识别器标签本身不够。
3. ABC 只能作为母结构的近似视觉描述；若父级已转为区间、成熟趋势或状态切换，不能把区间内三次摆动继续数成开放趋势 ABC/H3。
4. EMA20/50/200 只记录背景和汇合，不能替代结构磁铁、首障碍或结构性失效；局部停顿也不能充当首障碍。
5. Codex Trading 的旧 Daily 结果只能做路径/几何对照，不能直接并入本审计的成交分母；因为它们缺少可分离的 15m 信号、确认、MAE/MFE 和完整生命周期事件。

跨仓库借鉴目前只有 MRVL 提供了可直接复核的历史图；其余登记行因没有源图而被排除。本节不讨论当前规则或生产结论，只保留视觉研究中的 `pattern_candidate`、边界和缺失证据。

### 7.4 Round4 独立历史图练习

随后用 Codex Trading 当前保留的 `multisymbol-cohort3-20260812/bars.json` 做了独立的无标签图表练习：先筛选 42 个 Daily 标的，再放大 NKE、COP、AMZN、DE、JNJ、NFLX、META 七个历史日期，并额外练习 GOOGL、MSFT、XOM。详细字段、图像链接和逐例读法见[`Round4 历史图表视觉练习与 H/L/ABC 复核`](visual_recognition_round4_historical_practice_2026-08-24_CN.md)。

这一步的作用是检验“登记标签是否真的能从图上读出来”。结果并不一致：COP 最接近 `ABC-like + H1-like`；NFLX 可练习 bearish `ABC/L1-L2-like`；JNJ 只能保留 `H2-like hypothesis`；DE 是 `H2-like boundary`；AMZN、META、NKE 以及 GOOGL、MSFT、XOM 更多用于识别父级转区间、晚趋势和 lineage 不清楚的反例。Round4 的 Daily 左侧只有约一年，因此所有新增案例的两年背景仍是 `pending`，没有一个 strict same-lineage 计数被冻结。

### 7.5 Round5：两年 Daily 背景补齐后的独立练习

Round5 使用 `cohr-revised-20260814/bars.json` 的 `COHR`、`SPY`、`QQQ`、`IWM`，先看至少两年 Daily 左侧，再看各自截断到历史日期的 Daily/4H/15m 无标签图。详细逐例字段和资产见[`Round5 两年 Daily 左侧背景与 ABC/H-L/三推视觉练习`](visual_recognition_round5_two_year_daily_2026-08-24_CN.md)。

这轮 4 个标的、8 个 targeted 案例都完成了两年 Daily、EMA20/50/200、主要高低点和支撑阻力字段。COHR `2026-05-13` 是 `ABC + H1-like` 候选；SPY `2026-06-15` 和 IWM `2026-05-28` 是 H2-like 边界；QQQ `2026-07-17` 是 bearish L1/L2-like 的过渡边界。COHR、SPY、QQQ、IWM 的其余 targeted 图用于三推/区间重复或扩张/延续分流。由于首障碍拥挤、lineage/reset 仍有疑问、三个标的缺少 15m，Round5 没有冻结 strict same-lineage 计数，也没有新增可比正向样本；`no-new-positive` 保持不变。

## 当前结论

```text
abc_hl_stratification: established-for-research
fully_comparable_trade_samples: 0 under the unified outcome schema
win_rate: not-computable
realized_R_distribution: not-computable
priority_geometry_strata: ABC+L1 no-gap space-positive; ABC+H2 late-stabilized low-cycle
supplemental_cases_reviewed: 5
codex_trading_register_rows_screened: 15
legacy_register_rows_excluded_from_visual_count: 7
round4_daily_screen_symbols: 42
round4_targeted_multitimeframe_cases: 7
round4_additional_multitimeframe_practice_cases: 3
directly_reconstructed_codex_trading_visual_cases: 11
useful_codex_trading_chart_references: 11
approximate_h_l_visual_candidates_reviewed: 4
round4_strict_same_lineage_freezes: 0
round4_two_year_daily_complete_cases: 0
round5_two_year_daily_symbols: 4
round5_targeted_multitimeframe_cases: 8
round5_two_year_daily_complete_cases: 8
round5_strict_same_lineage_freezes: 0
round5_new_comparable_positive_samples: 0
new_comparable_positive_samples: 0
no_new_positive: maintained
scope: PA Research only; no scanner; no Execution Agent; no Codex Trading changes
```

这一步已经把“找机会”从单纯看形状推进到“先分层、再补同口径结果”。目前可以说哪些分层值得继续找样本，但还不能诚实地说哪一层已经证明了高胜率和良好盈亏比。

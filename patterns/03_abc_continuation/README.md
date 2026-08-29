# ABC：趋势延续

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录的 A/B/C 字段是差异字段。ABC 是母结构，方向必须单独写 `long`、`short` 或 `no_valid_direction`；H/L 只能作为 `internal_label`。

## 研究目的

把 A 腿、B 回调、C 恢复作为 Price Action 的操作性结构，而不是把它等同于外部波浪理论或几何 AB=CD。

## 共同图表范围前置

该入口的证据头还必须记录 `data_status: historical / delayed / live_confirmed / incomplete`、`as_of_time`、`chart_scope`、`daily_context_window` 和 `timeframes_seen`；历史、延迟、实时已确认与不完整不能互换。

状态边界：关键图表、事件、触发或空间证据尚不完整时使用 `pending`/`observation_only`；形态、方向和入场几何已可复核但已知硬闸门否决交易时使用 `valid_no_trade`。两者都不建立订单，不能互换。

统一合同映射：本目录的 ABC 是日线母级结构；`contract_scope: daily_candidate` 时 `primary_pattern` 写 `ABC_CONT` 或 `BOP`，H1/L1/H2/L2/H3/L3 只写入 `internal_label`，其他关系写入 `secondary_context`，`range_edge_three_push` 仅作位置分支。深审/历史记录可使用兼容主标签，但不能把内部尝试扩展成日线主标签。

BOP 状态迁移：若事前可见边界被日线强收盘越过、获得跟随并在回踩中守住，统一合同改写为 `primary_pattern: BOP`、`state_transition: breakout_acceptance`；本目录的原 pattern/反向 thesis 与旧订单合同失效，必须重建 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间，不能沿用旧 entry/stop/target 或把旧结果并入 BOP。

进入 ABC 判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。再核对强 A 与受控 B；涉及 H1/H2/L1/L2 时，Daily EMA20/50 还必须与方向一致，走平、反向或不可见时不得冻结普通 H/L。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能凭局部形状升级为可交易候选。

## 视觉定义

- A 是可在当时看见的方向性腿；
- B 是回调，不是已经形成的成熟交易区间；
- B 后段出现压力收缩、支撑/阻力反应或新的方向尝试；
- C 恢复原方向，并可表现为 H1/H2 或 L1/L2；
- 日线 H1/H2 方向要求 EMA20、EMA50 均向上，L1/L2 方向要求两者均向下；均线走平或反向时只保留为边界/观察；
- 如果 B 穿越关键结构并被接受，旧 ABC 合同结束，必须重建父级状态。

## 核心边界

- 交易区间内部不能把每一段摆动强行叫作第一腿、第二腿；
- 局部腿可以嵌套在更大腿中，不能事后用未来走势移动锚点；
- MM/AB=CD 用于空间和目标，不是 ABC 入场充分条件；
- 先看左侧主要高低点和第一障碍，再看投影目标。

## 最小视觉协议

| 阶段 | 多头观察 | 空头观察 |
| --- | --- | --- |
| `parent_state` | 开放上涨趋势，且 Daily EMA20/50 均向上；支撑反应或被接受的上涨突破 | 开放下跌趋势，且 Daily EMA20/50 均向下；阻力反应或被接受的下跌突破 |
| `A_leg` | 买压方向性、收盘、重叠、跟随 | 卖压方向性、收盘、重叠、跟随 |
| `B_pullback` | 卖压是否从前强后弱；是否守住结构 | 买压是否从前强后弱；是否守住结构 |
| `C_resumption` | H1/H2 信号与 buy-stop 确认 | L1/L2 信号与 sell-stop 确认 |
| `space` | 第一独立阻力与结构止损 | 第一独立支撑与结构止损 |
| `failure` | B 接受跌破支撑、回到区间或 C 无跟随 | B 接受突破阻力、回到区间或 C 无跟随 |

ABC 的判断顺序是：

```text
背景/左侧 → A 腿买压或卖压 → B 是否仍是回调
→ B 后段压力变化 → 位置与 H/L 尝试
→ C 信号与触发 → 首障碍/结构止损/R/R
```

## 三类 B 腿

1. `controlled-B`：浅回调或时间整理，反向压力逐步收缩；可以优先研究 H1/L1。
2. `deep-but-late-controlled-B`：前段反向压力较强，后段在结构位稳定；H1/L1 降级，H2/L2 保留。
3. `uncontrolled-B`：持续扩张、收盘靠极端、关键结构被接受或已经形成新趋势/区间；旧 ABC 合同结束。

“深”不是单独否决条件；是否仍是同一父级回调、后段是否稳定以及首障碍是否有空间更重要。

## 计数与时间尺度

- 同一周期、同一回调 lineage 内才继续计数；Daily、4H、1H、15m 分开记录。
- 交易区间中部的摆动不自动构成 A/B/C；区间边缘切换到区间目录。
- 局部腿可以嵌套在更大腿中；保留 local anchor 和 parent anchor，不用未来走势事后移动锚点。
- C 腿展开、新趋势极值出现、B 被结构性接受或回调变成区间时，旧 H/L 计数可能重置。
- Measured Move 和 AB=CD 只记录为目标/空间字段，不把它们变成入场授权。

## 订单分支

- `branch_role: same_contract` + `order_branch: stop_confirmation`：C 的信号 K 外 stop，结构止损按父级失效位；
- `low_cycle_confirmation`：低周期只确认高周期 ABC，不改变父级止损；
- `limit_retest`：回测支撑/阻力的独立合同；
- `reprice_after_gap`：开盘跳过旧触发后重新计算成交、止损、首障碍；
- `observation_only`：形态像但首障碍尚未确认、事件/板块证据不完整或市场状态不清。
- `valid_no_trade`：首障碍和结构几何已经可复核，但空间不足或已知事件/合同闸门否决交易。

不得把 C 腿后来的盈利、MM 到位或最终突破倒灌成 A/B/C 入场时已知的证据。

## 当前案例分组

| 分组 | 代表案例 | 研究用途 |
| --- | --- | --- |
| 多头强/条件 A-B-H | [`KLAC H2`](../../research/klac_h2_case_study_2025-05-07_2025-06-03.md)、[`TSLA H2`](../../research/tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) | 强 A、深/浅 B、H2 与首障碍分层 |
| 多头 H1 边界 | [`AAPL H1`](../../research/aapl_bullish_h1_event_driven_a_2024-05-03_2024-05-09.md)、[`COST H1`](../../research/cost_bullish_h1_first_obstacle_boundary_2024-05-13_2024-05-16.md) | 事件驱动 A、浅 B、信号质量和首阻力 |
| 空头开放/条件 ABC | [`NFLX L1`](../../research/nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md)、[`TSM L1`](../../research/tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) | 强 A、受控 B、缺口重订和首支撑 |
| 多头深 B 条件 ABC | [`CRWD H2`](../../research/crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md) | 深 B 后段稳定、H2-like、低周期确认、首阻力和事件边界 |
| 区间/过渡边界 | [`RBLX 区间边界`](../../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)、[`QCOM 宽 B`](../../research/qcom_bearish_abc_range_b_boundary_2025-02-21_2025-03-28.md) | 防止把区间内部或过渡状态硬叫趋势 ABC |

## 当前收口审计

[`ABC 趋势延续专项视觉证据审计`](../../research/abc_visual_evidence_gap_audit_2026-08-24_CN.md) 已把 NFLX/TSM 的空头 L1 条件候选、KLAC/CRWD 的多头深 B/H2 条件覆盖，以及 TSLA/QCOM/RBLX 的区间、过渡、跳空和计数重置边界放到同一套协议里。当前结论是：ABC 视觉识别可用，但普通无事件、双向、首障碍宽裕且过程完整的通用正例尚未冻结；`MM/AB=CD` 只负责目标层，不替代位置和订单审计。

## 当前目标验收

- A 腿质量决定优先看 H1/L1 还是等待 H2/L2；
- B 腿至少能区分受控、深但后段受控、未受控；
- C 腿与入场触发、结果审计分栏；
- 明确局部/父级腿、区间重置、缺口重订和首障碍 no-trade；
- 不引入 Elliott Wave，不把 ABC 做成量化阈值。

## 现有入口

- [`ABC 视觉综合`](../../research/abc_visual_synthesis_v0_2_CN.md)
- [`ABC 决策矩阵`](../../research/abc_decision_matrix_CN.md)
- [`ABC 覆盖审计`](../../research/abc_pattern_coverage_audit_CN.md)
- [`TSLA 2024 空头 ABC`](../../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md)
- [`NFLX 空头 ABC/L1`](../../research/nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md)
- [`H1/L1、H2/L2 与 ABC 证据缺口审计`](../../research/h1_h2_abc_evidence_gap_audit_2026-08-23_CN.md)
- [`ABC 趋势延续专项视觉证据审计`](../../research/abc_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`ABC + H/L 分层历史结果审计`](../../research/abc_hl_stratified_outcome_audit_2026-08-24_CN.md)：把 ABC 作为母结构、H1/L1 与 H2/L2 作为 C 腿尝试分层；当前只形成候选分层，胜率与 realized R 仍不可计算。

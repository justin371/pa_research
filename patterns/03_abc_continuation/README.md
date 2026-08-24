# ABC：趋势延续

状态：`visual-research / provisional / primary`

## 研究目的

把 A 腿、B 回调、C 恢复作为 Price Action 的操作性结构，而不是把它等同于外部波浪理论或几何 AB=CD。

## 视觉定义

- A 是可在当时看见的方向性腿；
- B 是回调，不是已经形成的成熟交易区间；
- B 后段出现压力收缩、支撑/阻力反应或新的方向尝试；
- C 恢复原方向，并可表现为 H1/H2 或 L1/L2；
- 如果 B 穿越关键结构并被接受，旧 ABC 合同结束，必须重建父级状态。

## 核心边界

- 交易区间内部不能把每一段摆动强行叫作第一腿、第二腿；
- 局部腿可以嵌套在更大腿中，不能事后用未来走势移动锚点；
- MM/AB=CD 用于空间和目标，不是 ABC 入场充分条件；
- 先看左侧主要高低点和第一障碍，再看投影目标。

## 最小视觉协议

| 阶段 | 多头观察 | 空头观察 |
| --- | --- | --- |
| `parent_state` | 开放上涨趋势、支撑反应或被接受的上涨突破 | 开放下跌趋势、阻力反应或被接受的下跌突破 |
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

- `same_contract_stop`：C 的信号 K 外 stop，结构止损按父级失效位；
- `low_cycle_confirmation`：低周期只确认高周期 ABC，不改变父级止损；
- `limit_retest`：回测支撑/阻力的独立合同；
- `reprice_after_gap`：开盘跳过旧触发后重新计算成交、止损、首障碍；
- `observation_only`：形态像但首障碍拥挤、事件/板块冲突或市场状态不清。

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

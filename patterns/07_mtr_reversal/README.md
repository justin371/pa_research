# MTR：主要趋势反转

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补成熟趋势、结构破坏和第二次反向确认。MTR 不能单独冻结方向或交易授权。

## 研究目的

研究成熟趋势或通道在主要位置上真正改变控制权的过程。MTR 不是一个双顶、三推或大反向 K 线的同义词，而是需要结构破坏、接受和第二次确认的高级合同。

## 共同图表范围前置

该入口的证据头还必须记录 `data_status: historical / delayed / live_confirmed / incomplete`、`as_of_time`、`chart_scope`、`daily_context_window` 和 `timeframes_seen`；历史、延迟、实时已确认与不完整不能互换。

状态边界：关键图表、事件、触发或空间证据尚不完整时使用 `pending`/`observation_only`；形态、方向和入场几何已可复核但已知硬闸门否决交易时使用 `valid_no_trade`。两者都不建立订单，不能互换。

方向字段边界：完整研究记录统一写 `direction: long / short / no_valid_direction`；方向字段是当前研究合同的方向，不是交易授权。

统一合同映射：本目录的 MTR 是高级反转研究语义；若 `contract_scope: daily_candidate`，`primary_pattern` 仍只写 `ABC_CONT` 或 `BOP`，H1/L1/H2/L2/H3/L3 写入 `internal_label`，其他关系写入 `secondary_context`，`range_edge_three_push` 仅作位置分支。已闭合的深审/历史 MTR 合同才可使用兼容 `MTR`，不能扩展日线选股主标签。

BOP 状态迁移：若事前可见边界被日线强收盘越过、获得跟随并在回踩中守住，统一合同改写为 `primary_pattern: BOP`、`state_transition: breakout_acceptance`；本目录的原 pattern/反向 thesis 与旧订单合同失效，必须重建 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间，不能沿用旧 entry/stop/target 或把旧结果并入 BOP。

原趋势 A 的质量和反向 B 的类别分别记录为 `a_leg_quality` 与 `b_leg_class`；它们只描述背景压力，不替代 MTR 的结构破坏、接受、第二次确认或 canonical 状态轴。

进入 MTR 判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。再核对原趋势 A 的推动力、反向 B 的受控程度和控制权变化；涉及 H/L 时，Daily EMA20/50 必须与方向一致。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能凭局部双顶、三推或一根大反向 K 升级为 MTR。

## 视觉定义

- 父级趋势已经成熟，且价格位于主要阻力/支撑或通道边界；
- 出现双顶/双底、三推、失败突破、Final Flag 或趋势线/通道破坏中的一个或多个证据；
- 第一次反向只是 reversal attempt；
- 反向方向再次出现确认并接受关键结构；
- 首障碍、结构止损和事件过滤证据尚未齐全时保留为 `observation_only`；若三者已可复核但硬闸门否决交易，使用 `valid_no_trade`。

## 主要边界

- 普通趋势回调不是 MTR；
- 区间边缘反应不等于主要趋势反转；
- 三推扩张可能是延续或高潮，不自动是楔形衰竭；
- 强突破接受可以否定原 MTR thesis，切换到 BOP；
- 首障碍太近时，形态可以像，但交易仍是 `valid_no_trade`。

## 最小视觉协议

```text
parent_trend_and_age:
major_location:
reversal_evidence: double-top/bottom / failed-breakout / channel-break / final-flag / other
first_reverse_attempt:
first_attempt_follow_through:
second_reverse_attempt:
structure_acceptance:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: reverse_stop / role_reversal_retest / gap_reprice / management
gap_policy: accept_open / skip / flag_only / not_applicable
structural_stop:
first_independent_obstacle:
rough_R_R:
mtr_state: reversal_attempt / mtr_candidate / mtr_confirmed_for_research / failed_mtr_thesis
thesis_state: working / failed / invalidated / replaced / pending
```

## MTR 的五个必要问题

1. 原趋势是否已经成熟，且当前位于主要高点/低点、通道边界或长期支撑阻力？
2. 反转证据是结构性失败，还是只有减速、影线和一根反向 K？
3. 第一次反向运动是否破坏了局部结构并得到跟随？
4. 是否出现第二次反向确认或回测守住？
5. 结构止损外到第一独立障碍是否仍有空间？

若第 3、4 或 5 项答不清楚，保留 `reversal_attempt`、`observation_only` 或 `pending`，不要升级为 MTR；若问题已明确且空间/事件/止损硬闸门失败，再记 `valid_no_trade`。

## 与三推和区间边缘的关系

- 双顶/双底和三推首先是位置/压力描述；它们可以提供 MTR 证据，但不自动授权反转；
- 成熟区间上沿/下沿的二次测试优先归入区间边缘目录；只有失败突破后产生新的反向接受，才另开 MTR 分支；
- 三推第三次推进扩张时，优先考虑延续/高潮，不要强行叫衰竭；
- 原方向强收盘突破并接受时，MTR thesis 失效，切换到 BOP。

## 订单与风险

- 默认研究反向 stop-confirmation；
- 已知颈线、失败边界、角色转换区才可单列 limit-retest；未回测不算成交；
- 极强反向收盘才考虑 market/close，且仍要过首障碍和事件过滤；
- 结构止损放在反转极端/失败边界外，不用低周期窄止损包装成大级别 MTR；
- 第一障碍不足约 1R、财报窗口或原趋势极端重新被接受时，记录 `valid_no_trade` 或 `failed-MTR-thesis`。

## 现有入口

- [`MTR 视觉框架`](../../research/mtr_visual_framework_CN.md)
- [`双顶/双底、MTR 与 Final Flag 对照`](../../research/double_top_bottom_mtr_final_flag_comparison_CN.md)
- [`头肩与圆顶/圆底边界`](../../research/head_shoulders_rounded_top_bottom_visual_framework_CN.md)
- [`TSLA 区间顶部 MTR 候选`](../../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md)
- [`NFLX 三推顶部边界`](../../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)
- [`MTR 与三推证据缺口审计`](../../research/mtr_three_push_evidence_gap_audit_2026-08-23_CN.md)：本轮没有新增无事件、二次确认清楚且首障碍宽裕的 MTR 正例。
- [`MTR 主要趋势反转专项视觉证据审计`](../../research/mtr_visual_evidence_gap_audit_2026-08-24_CN.md)：进一步把 MTR、区间边缘、普通回调和 BOP 失效分层。

## 当前案例对照

| 案例 | MTR 状态 | 研究结论 |
| --- | --- | --- |
| [`TSLA 2024-03-04–03-14`](../../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | 区间上沿重叠的 MTR candidate | L1 失败后 L2 清楚，但过程先破坏结构止损；静态空间不能代替路径审计 |
| [`NFLX 2024-08-05–09-26`](../../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | 高位多次测试 / MTR-like | 首支撑拥挤，且原方向后来重新接受，记 `valid_no_trade` |
| [`TSLA 2025-09-08–09-12`](../../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | failed-MTR-thesis → BOP | 阻力下反转尝试被强收盘突破否定，必须切换新合同 |
| [`ASML 2025-05-19–06-13`](../../research/asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md) | double-bottom-like / not-MTR | 低位两次测试后进入区间过渡，缺少结构接受和二次确认 |
| [`PLTR 2024-12-24–2025-01-08`](../../research/pltr_bearish_abc_l1_ordinary_a_boundary_2024-12-24_2025-01-08.md) | ordinary-pullback / early-reversal-candidate | A 腿普通、首支撑不足约 `1R`，不能因为双顶样外观升级为 MTR |
| [`LOW 2024-06-11–06-24`](../../research/low_bullish_h1_h2_first_obstacle_boundary_2024-06-11_2024-06-24.md) | parent-transition / reversal-attempt | 急跌后的多头恢复与前高阻力拥挤，保留为边界 |

## 当前目标验收

- 能从普通回调、区间边缘和 MTR candidate 三者中做出区分；
- 能把双顶/双底、三推、失败突破和通道破坏作为证据而非自动信号；
- 能记录第一反向、第二次确认、结构止损、首障碍和路径失效；
- 能在原方向 BOP 接受后废弃 MTR thesis；
- 保留至少一个形态像但首障碍/路径否决的边界案例。

本轮专项审计结论：TSLA 2024-03 是区间边缘重叠且过程先止损的 MTR candidate；NFLX、PLTR、LOW 说明首障碍或父级状态会否决形态；TSLA 2025-09 说明 BOP 接受会终止 MTR thesis。当前仍没有事件闭环、双向、二次确认清楚、首障碍宽裕且路径完整的普通 MTR 正例，因此保持 `provisional / no-new-positive`。

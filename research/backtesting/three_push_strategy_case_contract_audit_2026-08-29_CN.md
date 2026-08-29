# 三推策略与历史案例合同一致性审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative / no-new-positive`

## 1. 范围与目的

本轮审计[`三推楔形候选规则`](../../strategy/01_three_push_wedge_candidate.md)、[`H3/L3 研究闸门`](../h3_l3_research_gate_CN.md)、[`H3/L3 视觉比较`](../h3_l3_visual_comparison_CN.md)、[`三推压力状态框架`](../three_push_pressure_state_framework_CN.md)、[`MTR 视觉工作框架`](../mtr_visual_framework_CN.md)及其引用的历史案例。目标是确认三推策略的 A/B/C 解释层、第三推状态、方向、lineage、订单、首障碍、空间和统计结论不会互相替代。

本轮不下载行情、不看新图、不运行回放、不增加样本、不修改 CSV、历史结果或 engine 有效语义；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent 或 Futu/OpenD。

## 2. 发现与修复

### 2.1 策略页的 A/B/C 没有映射到统一合同

`strategy/01_three_push_wedge_candidate.md` 原来只定义 A 类高质量反转候选、B 类短线反应候选和 C 类延续/高潮边界，未明确它们对应的 canonical 字段。这样容易把“形态分类”误读成“交易状态”或胜率分组。

已补充统一字段和边界。A/B/C 是解释性分流，不是新的状态枚举：

- A/B/C 是解释性分流，不是新枚举；
- `third_push_state` 只描述压力状态，`research_state`、`trade_state`、`gate_result` 分别描述研究、交易和闸门结论；
- `attempt_direction` 不替代当前合同的 `direction`；触发、空间或合同未冻结时，`direction` 仍可为 `no_valid_direction`；
- `first_independent_obstacle` 必须是入场前可见的独立结构，EMA 不能单独制造空间；
- 当前无冻结的三推/H3/L3 回放合同，保持 `no-new-positive`，`validated win-rate: not-computable`。

### 2.2 视觉比较表仍使用旧字段

视觉比较表的回填表原来使用 `h3_l3_state`、`reverse_trigger_present` 和 `first_obstacle`，并把 `short_reaction_candidate` 混入第三推状态。它们分别混淆了三推压力、反向证据和订单几何。

已改为 `lineage_status`、`third_push_state`、`first_reverse`、`second_confirmation` 和 `first_independent_obstacle`。TSLA 的短线支撑反应现在记录为 `third_push_state: exhaustion_candidate`、`first_reverse: touch`、`second_confirmation: no`，而不是把短线反应当成新的压力状态；ASML 记录为 `range_repeat_test`，同时保留 `not_h3_l3` 作为案例结论。

### 2.3 压力框架输出块的状态轴已收敛

压力框架原输出块使用 `same_lineage`、`first_obstacle`、`rough_rr` 和 `status`，与统一合同的 `lineage_status`、`first_independent_obstacle`、`space_status`、`research_state`、`trade_state` 和 `gate_result` 不同。

已改为 canonical 字段，并补上 `direction`、`state_transition`、`gap_policy`。这只是记录合同修复，不改变三推压力的有效语义，也不让框架直接生成订单。

### 2.4 MTR 相邻结构的旧短线枚举已移除

MTR 框架曾把 `short_reaction_candidate` 与第三推状态并列。已改为 `exhaustion_candidate`、`continuation_or_climax`、`range_repeat_test` 和 `channel_continuation`；短线反应由 `first_reverse`、`second_confirmation`、`research_state`、`trade_state` 和空间字段表达。

## 3. 历史案例的 canonical 阅读

下表只把已存在的案例结论映射到当前字段，不是重新审查行情，也不是新增结果：

| 案例 | canonical 结构阅读 | 订单/空间边界 | 当前结论 |
| --- | --- | --- | --- |
| [`KLAC 2025-03-17–03-26`](../klac_h3_bear_flag_case_2025-03-12_2025-03-28.md) | `lineage_status=same_lineage`；`third_push_state=exhaustion_candidate`；`first_reverse=structural_break`；`second_confirmation=yes` | `order_branch=stop_confirmation`；首障碍约 `1.4–1.9R`，属于研究上的宽裕空间，但精确成交、止损 buffer 和其他新闻风险仍未冻结 | `research_state=research_positive_conditional`，不是生产规则或已验证正例 |
| [`TSLA 2026-05-19–06-26`](../h3_l3_research_gate_CN.md) | `lineage_status=unclear`；`third_push_state=exhaustion_candidate`；`first_reverse=touch`；`second_confirmation=no` | 反向触发后首阻力约 `0.63–0.83R`，`space_status=blocked`；不能用后续反弹扩大空间 | `trade_state=valid_no_trade`，只是短线反应边界 |
| [`XOM 2024-07-18–08-02`](../xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md) | `lineage_status=pending`；`third_push_state=continuation_or_climax`；`first_reverse=touch`；`second_confirmation=no` | 原 sell-stop 被开盘跳过；`branch_role=gap_reprice`，重订后首支撑约 `0.7R`，必须重算而不能沿用原 R/R | `trade_state=valid_no_trade`，不是衰竭三推正例 |
| [`ASML 2025-05-23–06-11`](../asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md) | `lineage_status=reset`；`third_push_state=range_repeat_test`；`first_reverse=none`；`second_confirmation=no` | `order_branch=observation_only`；第三次同级别推进、反向触发和空间均未冻结 | `trade_state=observation_only`，`not_h3_l3 / range-transition` 只是历史说明标签 |
| [`NFLX 2024-08-05–09-26`](../nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | `lineage_status=pending`；`third_push_state=range_repeat_test`；计数超过三次且重叠多 | 首支撑约 `0.1–0.25R`；即使低周期触发存在，也不能绕过首障碍 | `trade_state=valid_no_trade`，后续结构失效不能倒灌为入场证据 |

案例中的 `provisional`、`H3-like`、`range-transition`、`support-reaction-boundary` 等保留为历史叙述是允许的；它们不是新记录的字段枚举。新记录必须把它们映射为 canonical 字段，不能把 `research_positive_conditional`、`valid_no_trade` 或 `observation_only` 混成胜率标签。

## 4. 统计和样本边界

本轮不改变既有数据。前一轮合同审计已确认当前冻结集合为 7 份 CSV、60 行，H3/L3 冻结行数为 0；三推历史案例没有因此进入 H/L 回放分母。KLAC 仍是条件性研究候选，L3 仍是 `no-new-positive`，`validated win-rate: not-computable`。

因此本轮的交付物是字段和解释边界修复，不是胜率、盈亏比或样本量结论。只有在人工确认同一 lineage、第三推状态、方向、反向证据、数值订单、首障碍和空间后，才可另立回放合同；回放器不会从 OHLC 自动识别三推。

## 5. 结论

- 三推策略的 A/B/C 已明确为解释层，不再与交易状态或统计分组混淆；
- 当前相关框架和视觉比较表统一使用 `third_push_state`、`first_reverse`、`second_confirmation`、`lineage_status`、`first_independent_obstacle` 和 canonical 状态轴；
- 历史案例的 no-trade、开盘跳过、区间过渡和后续失效结论全部保留，不用后见之明升级为正向样本；
- `no-new-positive` 与 `validated win-rate: not-computable` 保持不变。

本审计只属于 PA Research：`PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。

## 6. 追加 canonical 主标签、内部标签与 MTR 状态复核（2026-08-29）

后续对三推策略页、压力状态框架、H3/L3 研究闸门、视觉比较/证据审计和区间边界审计的输出块逐项复核，发现这些“统一合同”示例仍漏写 `primary_pattern`/`internal_label`，容易让记录只保存压力状态而丢失主次标签映射。现已补齐 canonical `primary_pattern`、`internal_label` 与 `contract_scope`；`direction` 继续单独保留，`attempt_direction` 不得替代它，`daily_candidate` 主标签仍只允许 `ABC_CONT`/`BOP`。

同时复核 MTR 专用轴：`mtr_state` 只属于 MTR pattern-specific 观察，不替代 `thesis_state`、`research_state`、`trade_state` 或 `gate_result`。MTR/三推边界审计原先使用 `not_started / candidate / confirmed_for_research / failed` 的未登记简写，现收敛到 `reversal_attempt / mtr_candidate / mtr_confirmed_for_research / failed_mtr_thesis`；未开启 MTR 分支的记录使用三推自身的 `third_push_state` 与 `research_state` 表达，不把 MTR 字段强行写入普通三推。

本 follow-up 只修正 PA Research 文档、validator、索引说明和回归测试，不新增图表、合同、成交、回放或统计分母；`no-new-positive` 与 `validated win-rate: not-computable` 保持不变。

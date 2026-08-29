# 视觉历史报告与 canonical authority schema 对齐审计（2026-08-29）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 1. 审计结论

本轮只做 PA Research 文档字段对齐，不下载或查询行情、不看新图、不运行回放、不增加样本、不修改 CSV/历史结果/engine 有效语义。审计发现的真实问题是：若干视觉框架和跨案例复核模板仍把旧显示字段放在新记录的活动填写位置，可能让后续记录把结构状态、订单状态、研究状态和交易状态混成一个字段。

已将活动模板收敛到[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)、[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)和[`PA Pattern 视觉筛选协议`](../visual_pattern_triage_protocol_CN.md)的 canonical 字段。旧历史案例中的事实字段没有被改写；它们只作为历史显示语义读取，并与新记录模板分开。

当前统计边界保持：`no-new-positive`；`validated win-rate: not-computable`。本审计不产生新的胜率、样本、订单或交易授权。

## 2. authority 与范围

### 2.1 读取顺序

1. `contract_scope` 先区分 `stage_1_fast_screen`、`deep_review`、`daily_candidate` 和 `historical_context_only`；
2. `data_status`、`as_of_time`、`session_state`、`timeframes_seen`、`chart_scope` 和 `daily_context_window` 记录证据范围；
3. `major_high_low_review` 与 `ema20_50_200_review` 记录两年左侧、重要高低点和 EMA20/50/200 是否真正复核；
4. `direction`、`primary_pattern`、`internal_label`、`lineage_status`、`lineage_id` 和 `state_transition` 记录结构解释；
5. `order_branch`、`actual_fill_or_open_skip`、`structural_stop`、`first_independent_obstacle`、`pre_entry_space_R` 和 `space_status` 记录订单几何；
6. `research_state`、`trade_state`、`gate_result` 和 `handoff_status` 分开记录研究、交易、闸门和交接状态；交接枚举仍为 `research_only / not_ready / ready_for_system`。

这些轴彼此不能覆盖。`H1/H2/L1/L2/H3/L3` 是 `internal_label`，不是新的主标签；`BOP` 接受、MTR 候选和三推状态也不能把订单或结果写回结构字段。

### 2.2 本轮实际核对对象

本轮共修正 23 个活动文档，覆盖视觉复核卡、H/L lineage、市场状态、Inside Bar、Triangle、Late Trend、Multi-timeframe 及此前已经发现的跨案例审计模板：

- `docs/visual_pa_review_card_CN.md`；
- `research/h_l_lineage_visual_boundary_audit_2026-08-24_CN.md`；
- `research/market_state_context_visual_evidence_audit_2026-08-24_CN.md`；
- `research/inside_bar_two_bar_reversal_visual_framework_CN.md`；
- `research/triangle_expanding_range_visual_framework_CN.md`；
- `research/late_trend_entry_visual_framework_CN.md`；
- `research/multitimeframe_visual_review_framework_CN.md`；
- `research/abc_continuation_visual_boundary_audit_2026-08-24_CN.md`；
- `research/abc_hl_stratified_outcome_audit_2026-08-24_CN.md`；
- `research/bop_visual_boundary_audit_2026-08-24_CN.md`；
- `research/channel_visual_boundary_audit_2026-08-24_CN.md`；
- `research/channel_visual_evidence_gap_audit_2026-08-24_CN.md`；
- `research/core_pattern_cross_audit_CN.md`；
- `research/cross_pattern_visual_priority_audit_2026-08-24_CN.md`；
- `research/failed_breakout_climax_visual_evidence_gap_audit_2026-08-24_CN.md`；
- `research/h1_l1_first_entry_visual_boundary_audit_2026-08-24_CN.md`；
- `research/h2_l2_second_entry_visual_boundary_audit_2026-08-24_CN.md`；
- `research/late_trend_entry_visual_evidence_gap_audit_2026-08-24_CN.md`；
- `research/mtr_three_push_visual_boundary_audit_2026-08-24_CN.md`；
- `research/multitimeframe_visual_evidence_gap_audit_2026-08-24_CN.md`；
- `research/triangle_expanding_range_visual_boundary_audit_2026-08-24_CN.md`；
- `research/triangle_expanding_range_visual_evidence_gap_audit_2026-08-24_CN.md`；
- `research/visual_review_workflow_boundary_audit_2026-08-24_CN.md`。

五个入口已加入本审计：`docs/README.md`、`research/README.md`、`strategy/README.md`、`patterns/README.md` 和 `research/backtesting/README.md`。

## 3. 已修复的活动字段漂移

| 旧活动字段或混合写法 | 当前 canonical 写法 | 处理边界 |
| --- | --- | --- |
| `decision_time`、单数 `timeframe` | `as_of_time`、`timeframes_seen` | 报告时间与可见周期分开；所有周期仍可在 `timeframes_seen` 记录 |
| `review_timeframe` | `count_timeframe`，同时保留 `timeframes_seen` | 计数周期是 H/L 协议的补充字段，不再冒充全部证据周期 |
| `attempt` | `historical_count_label` / `internal_label` | 计数显示与 canonical 内部标签分开 |
| `parent_pattern` | `primary_pattern` + `secondary_context` | 父级图形显示不能覆盖当前主标签 |
| `order_contract`、`trigger_order`、`decision` | `order_branch` + `branch_role` + `actual_fill_or_open_skip` | 基础订单、分支角色和实际成交路径分开 |
| `first_obstacle`、`parent_first_obstacle` | `first_independent_obstacle`、`parent_first_independent_obstacle` | 最近独立障碍不能与结构止损混写 |
| `rough_rr`、混合 `status` | `rough_R_R`、`space_status`、`research_state`、`trade_state`、`gate_result` | 粗略几何不能代替状态轴或授权结论 |
| `final_status` | `research_state` + `trade_state` + `gate_result` + `handoff_status` | 不再用一个字段压缩四种不同状态 |
| `h3_l3_state`、`push_state` | `third_push_state` | 三推压力状态与 `first_reverse`、`second_confirmation` 分轴 |

### 3.1 五个原有视觉框架的具体处理

- 市场状态审计卡补齐 `contract_scope`、证据头、方向、lineage、订单、空间和四条状态轴；`range_upper/lower/midpoint` 等仍作为该审计的状态专用补充。
- Inside Bar/两根反转框架保留 `mother_bar`、`pattern_type`、`location` 和 `directional_bias`，但统一使用 `primary_pattern`、`internal_label`、`order_branch` 和三条状态轴。
- Triangle 框架保留 `triangle_status`、边界、测试次数和 `breakout_state`，并将首障碍、空间和结果状态改成 canonical 字段。
- Late Trend 框架把后段过滤字段作为补充，将信号、触发、订单、首障碍、空间和状态轴统一到当前合同；后段过滤不是第四个 pattern。
- Multi-timeframe 框架把父级 pattern、父级首障碍和实际成交的旧写法映射到 `primary_pattern`、`parent_first_independent_obstacle` 和 `actual_fill_or_open_skip`；低周期仍不能创造高周期空间。
- 后续复核将 `research/channel_visual_framework_CN.md` 作为第六个活动视觉框架纳入同一集合；`channel_type`/`channel_status` 仍是通道专用补充轴，不能替代 `parent_state`、`primary_pattern`、`internal_label` 或 `direction`。

## 4. 明确保留而不误判为当前漂移的字段

### 4.1 历史案例事实字段

以下文件中的 `A_quality`、`B_quality`、`attempt` 或 `first_obstacle` 是日期明确的历史案例叙述，不是新记录模板，也没有被本轮静默改写：

- `research/anet_bullish_h2_visual_boundary_2023-11-15_2023-11-22.md`；
- `research/coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md`；
- `research/cost_bullish_abc_h2_visual_boundary_2025-04-21_2025-05-16.md`；
- `research/jnj_bullish_h1_first_obstacle_2025-09-18_2025-10-08.md`；
- `research/jpm_bullish_h1_first_obstacle_failure_2025-08-22_2025-09-05.md`；
- `research/nvda_bullish_h1_trigger_branch_first_obstacle_2025-04-21_2025-05-08.md`。

它们应按原案例语境阅读；不能把这些旧字段复制到新模板，也不能因为字段名旧就改写历史结论、CSV 或结果 artifact。

### 4.2 模式专用观察字段

`pattern_family`、`mother_bar`、`triangle_status`、`upper_boundary/lower_boundary`、`tests`、`gap_state`、`parent_timeframe` 和后段过滤字段仍然有用，但它们必须标明是显示/补充字段。它们不能替代 `primary_pattern`、`direction`、`lineage_status`、`first_independent_obstacle` 或状态轴。

`first_obstacle_zone` 是视觉卡中对障碍区域的补充说明；真正的统一合同字段仍是 `first_independent_obstacle`。`pattern_family: RFB_SECOND` 是历史显示别名，只映射到 `primary_pattern: RFB`，不是新主标签。

## 5. validator 与回归边界

本审计对应的回归测试检查：

- 视觉卡有 canonical `primary_pattern`、`lineage_status`、`lineage_id`，不再有活动的 `same_lineage:` 或 `attempt:` 模板字段；
- 活动视觉框架都有 `contract_scope`、`data_status`、`as_of_time`、`timeframes_seen`、两年背景、重要高低点、EMA 复核、方向和 canonical 状态轴；
- 活动模板不再以 `final_state:`、`order_contract:`、`first_obstacle:`、`rough_rr:`、`parent_pattern:` 或 `three_push_state:` 作为统一输出字段；
- 历史案例旧字段只按登记的历史路径保留，且不被当作新的 canonical 合同或新的统计样本；
- 五个索引均能找到本审计，内部链接仍通过仓库 validator；
- `no-new-positive`、`validated win-rate: not-computable`、PA Research 隔离和禁止连接边界不回归。

validator 仍是只读文档/链接/合同边界校验器，不是行情工具、量化扫描器或执行层。

## 5.1 继续复核 parent_state 与 market_state 语义（2026-08-29）

后续逐项检查活动模板和迁移审计合同，发现并修复了同一字段名的两类漂移：

- `docs/visual_pa_review_card_CN.md` 和 `research/visual_pattern_triage_protocol_CN.md` 原先在父级状态位置使用 `market_state`，现改为 `parent_state`；`market_state` 只保留给板块/大盘方向一致性 `aligned / mixed / counter / unknown`。
- 日线选股模板、`patterns/05_failed_breakout_climax/README.md`、三个基础层模板、市场状态审计卡以及六个活动视觉框架全部使用 `parent_state: open_trend / trading_range / range_edge / transition / climax / unclear`。
- `research/cross_pattern_visual_priority_audit_2026-08-24_CN.md` 与 `research/abc_hl_stratified_outcome_audit_2026-08-24_CN.md` 的统一模板已去除 `mature_range`、`accepted_breakout` 和 `event-or-gap` 混合枚举；边界接受改由 `parent_state: open_trend` + `state_transition: breakout_acceptance` 表示，事件/缺口另写 `event_context`/`event_bucket`。

真正历史性的视觉证据/边界报告仍可保留原始显示词，但不能被活动模板或 canonical 字段复用。validator 现在要求上述活动路径出现 canonical `parent_state`，并拒绝旧的 `market_state`/`parent_state` 混合枚举；本轮没有新增样本或结果，`no-new-positive` 与 `validated win-rate: not-computable` 保持。

## 6. 最终边界

本轮修复只影响 PA Research 的文档、索引、validator/回归覆盖和新记录填写语义：

- 不修改 Codex Trading；
- 不创建量化扫描器；
- 不连接 Futu/OpenD；
- 不连接 Execution Agent；
- 不改写 CSV、历史结果、engine 有效语义或既有统计分母；
- 不把人工视觉审计升级为自动图形识别、已验证胜率或交易授权。

因此本轮的可接受结果仍是：字段和入口一致性得到修复，但没有新的可比正样本，`no-new-positive` 保持，`validated win-rate: not-computable` 保持。

## 7. 追加活动 label 映射与快筛入口复核（2026-08-29）

原报告保留“23 个活动文档”的首轮修复计数；本节记录其后的 PA Research-only follow-up，不把两轮计数混为新的样本或结果。复核发现并修复了活动入口的以下问题：

- 快速视觉初筛现在使用 `pattern_candidate`，不再把未闭合的候选观察写入 canonical `primary_pattern`；完整记录仍必须在 `primary_pattern`、`internal_label`、`direction` 三轴上分别落值。
- 跨 Pattern 矩阵、策略 inventory、H1/H2、Multi-timeframe、Late Trend、事件/市场闸门、订单/风险和 Opening Reversal 模板已统一 canonical 主标签、内部 H/L 标签和方向枚举；`daily_candidate` 的主标签白名单仍严格为 `ABC_CONT`/`BOP`。
- `H_or_L_attempt`、合并式 `pattern_and_attempt`、`decision_timestamp`、`decision_time`、`parent_state_and_location` 和 `actual_or_assumed_fill` 不再作为新记录入口；分别使用 `internal_label`、`as_of_time`、`parent_state` + `parent_location` 和 `actual_fill_or_open_skip`。
- Channel 框架已作为第六个活动视觉框架纳入 validator 与回归测试；通道字段只补充通道形态和状态，不改变统一 pattern、方向、订单、空间和状态轴。
- 当前复核卡中的 `parent_state` 已统一为 `open_trend / trading_range / range_edge / transition / climax / unclear`。日期明确的历史案例自由文本和历史显示别名保持原样，避免把历史事实重写成当前模板。

本 follow-up 只更新 PA Research 文档、索引说明、validator 和回归守卫，不查行情、不看新图、不运行回放、不新增样本，不修改 Codex Trading、CSV、结果 artifact 或 engine；`no-new-positive` 与 `validated win-rate: not-computable` 保持。

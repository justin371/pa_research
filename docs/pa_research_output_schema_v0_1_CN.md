# PA Research 统一输出合同 v0.1

日期：2026-08-25；合同修订：2026-08-26；批次证据字段修订：2026-08-28；回放结果口径修订：2026-08-29；样本独立性字段修订：2026-08-29；回放输入边界修订：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 目的与适用范围

本文件统一 PA Research 的视觉复核、日线候选和历史案例输出字段。它只定义研究记录的结构，不定义量化扫描条件、生产交易规则、订单接口或 Execution Agent 行为。

使用顺序仍由各自上游规则决定：

1. 日线候选先遵循[`PA Research 日线选股规则 v0.1`](pa_research_daily_selection_rules_v0_1_CN.md)；
2. 完整图表复核使用[`PA 图表视觉复核卡`](visual_pa_review_card_CN.md)；
3. 核心 pattern 的切换和历史别名映射见[`核心八个 Pattern 交叉一致性审计`](../research/core_pattern_cross_audit_CN.md)；
4. 是否可以交接给 Codex Trading 另遵循[`研究交接规范`](research_to_system_handoff_CN.md)。

`contract_scope` 必须先写清楚：

```text
stage_1_fast_screen / deep_review / daily_candidate / historical_context_only
```

`stage_1_fast_screen` 和 `historical_context_only` 可以暂缺成交、止损、首障碍和 R/R，但必须写 `pending` 或 `unknown`，不能被当作完整候选。

文档头的 `document_status`、`document_maturity` 和 `handoff_status` 是文档生命周期元数据，不是某一条案例的交易状态。当前仓库文档头使用 `document_maturity=provisional` 表示研究材料仍在迭代；它不能写入案例的 `research_state`。案例状态只使用下方状态轴定义的枚举。

## 0. 研究记录与当前回放输入的边界

本文件是 PA Research 的研究记录超集，统一视觉复核、日线候选和历史案例的字段；它不是当前 `backtesting.py` 输入 CSV 的逐项枚举。提交回放前，必须再按[`冻结合同回放器`](../research/backtesting/README.md)把研究记录收敛成可执行的冻结合同，不能把研究状态或区域文字直接当成订单合同。

- 当前日线候选的顶层 `primary_pattern` 仍只有 `ABC_CONT` 和 `BOP`；H1/H2/L1/L2/H3/L3 通过 `internal_label` 及 `secondary_context` 记录。`H1_L1`、`H2_L2`、`H3_L3`、`RFB`、`MTR` 和 `other` 在统一记录及当前回放器中保留，是历史/兼容冻结合同的 pattern 值，不会扩展日线选股规则。
- `primary_pattern` 的允许值必须结合 `contract_scope` 解读：`daily_candidate` 只允许 `ABC_CONT` 或 `BOP`；`deep_review`/`historical_context_only` 才能在对应合同已闭合时使用历史/兼容值。H1/H2/L1/L2 在日线候选中只能写入 `internal_label`，不能借由 `pattern_family`、`secondary_context` 或自由文本重新变成主标签。
- 研究记录的 `direction` 可以是 `no_valid_direction`，但当前回放输入只接受 `long` 或 `short`。没有有效方向的记录只能保留为研究记录，不能送入回放。
- 研究记录的 `order_branch` 可以记录 `stop_limit` 或 `observation_only`；当前 engine `0.3.9` 的回放输入只接受 `stop_confirmation`、`limit_retest` 和 `market_close`。`observation_only` 不建立交易合同，`stop_limit` 不能静默映射为普通 stop；两者目前不能直接传给当前回放器。
- 回放输入中的 `entry_trigger`、`structural_stop`、`first_obstacle` 和 `target_price` 必须是有限数值价格；研究卡中的价格区域、`pending` 或 `unknown` 不能直接替代这些冻结数值。`market_close` 可以没有 `entry_trigger`，但仍必须满足该分支的其他合同要求。
- 记录字段 `actual_fill_or_open_skip` 使用下划线状态，和回放结果字段 `fill_status` 的 `no-fill`、`opening-skip`、`unproven`、`not-traded` 不是同一字段，不能混写或互相推断。

`actual_fill_or_open_skip` 只表示研究合同/历史回放的订单路径注释，不是券商或账户的实际成交日志。仅有入场前证据的候选/视觉记录不得写 `filled`；若统一模板保留此字段，应写 `not_applicable`。真实交易日志必须来自另立的独立来源，不能由该字段或回放结果冒充。

## 一、证据头与市场闸门

```text
symbol:
review_date:
contract_scope:
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:
market_cap_usd:
market_cap_as_of:
market_cap_source:
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
daily_ema20_slope: up / flat / down / unknown
daily_ema50_slope: up / flat / down / unknown
h_l_ema_slope_gate: long_pass / short_pass / fail_flat_or_opposite / pending / not_applicable

event_context: none / earnings / macro / gap / other / unknown
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
event_source_as_of:
earnings_next_three_sessions: yes / no / unknown
sector_reference:
sector_state: aligned / mixed / counter / unknown
market_reference:
market_state: aligned / mixed / counter / unknown
permission: long_allowed / short_allowed / both_allowed / no_direction / unknown
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

`as_of_time`、时区、session 和 `completed_bar_as_of` 必须能区分报告生成时间、查询窗口结束时间和实际可用的最新完整 K 线。历史数据不能写成实时数据。

`chart_scope` 描述整张图表的可见完整度；`daily_context_window` 单独描述 Daily 左侧是否覆盖至少两年。批次卡中的 `two_year_chart_coverage` 只表示该批次的汇总覆盖率，不能替代逐标的 `daily_context_window`。`a_leg_quality` 和 `b_leg_class` 是共同的 A/B 视觉质量字段；独立主题可以记录它们作为背景对照，但不能因此继承 ABC/H-L 计数。

`a_leg_quality`、`b_leg_class` 和 `b_leg_location` 是分开的 canonical 字段：质量/类别不能塞进位置字段。历史 H/L 合同可能缺少这些可选上游字段，或保留旧写法 `strong_A`/`ordinary_A`（分别对应 `strong`/`ordinary`）和 `controlled_B`/`deep_late_controlled_B`（分别对应 `controlled`/`deep_but_late_controlled`）；这些只可作为明确登记的历史别名读取，不能静默当作当前 canonical 值，也不能由 `h_l_pullback_location` 或结果回填。`h_l_pullback_location` 只保留 H/L 回调位置及其历史说明，不能替代 A/B 字段。

`h_l_pullback_location` 是自由文本位置证据，不是方向、EMA gate 或空间枚举。`rising_EMA20`、`falling_EMA20`、`prior_support`、`prior_resistance`、`role_reversal` 和事件位置等词只描述观察到的地点；若空头文本提到 `support`，应明确它是前期/破位后的角色转换还是事件位置，不能把未破的当前支撑误读为空头优势。位置文字不能覆盖 `direction`、`daily_ema20_slope`、`daily_ema50_slope` 或 `h_l_ema_slope_gate`，也不能替代 `pre_entry_space_R`/`space_status`。

当 `contract_scope: daily_candidate` 时，`timeframes_seen` 必须只写 `Daily`；4H/1H/15m 只能放在候选入选后的 `deep_review` 或另立的订单合同中，不能倒灌成日线选股证据。若低周期已经改变研究问题，必须新建独立合同并重新记录范围、状态和入场几何。

`contract_frozen: yes` 是字段和订单几何的冻结状态，不是视觉 artifact provenance 或交易授权。决策日图、两年左侧、重要高低点或 EMA20/50/200 证据缺失时，必须在视觉/报告边界保留 `pending`、`observation_only` 或 provenance gap；后续日期图不能补写成入场前证据，也不能把历史回放记录升级为可交易或已验证样本。

每日批次记录还应使用[`每日候选批次与图表审查卡`](daily_candidate_review_card_CN.md)补充以下证据。它们是候选池和视觉审查字段，不会把回放合同变成扫描器输入：

```text
candidate_batch_id:
discovery_source:
universe_scope:
universe_coverage: complete / partial / discovery_only / unknown
directional_coverage: long / short / both / unknown
avg_20d_dollar_volume_usd:
liquidity_as_of:
liquidity_source:
event_source_as_of:
event_gate: pass / exclude / pending
```

`universe_coverage=discovery_only` 或 `unknown` 时，输出必须标为发现池/已审查子集；不能把发现页数量解释为完整市场合格数量。`avg_20d_dollar_volume_usd` 必须对应最近 20 个完整交易日，不能用单日事件成交额替代。

## 二、结构、方向与 pattern

```text
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
direction: long / short / no_valid_direction
left_structure_and_location:
major_highs_lows:
support_resistance_and_role_zones:
daily_ema20_50_200:
daily_ema20_slope: up / flat / down / unknown
daily_ema50_slope: up / flat / down / unknown
h_l_ema_slope_gate: long_pass / short_pass / fail_flat_or_opposite / pending / not_applicable
h_l_pullback_location:
a_leg_quality: strong / ordinary / unclear / event_driven
b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear
special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none
b_leg_location:
meta_confluence: present / absent / unknown
meta_zone:
meta_components:

primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
secondary_context:
range_edge_three_push: yes / no / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
market_context_id:
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_side: upper / lower / none / pending
pattern_like_reason:
```

`direction` 是当前研究合同的方向，不是 `directional_bias` 的同义词：

- 多头 H1/H2、Bullish ABC 或多头 BOP 写 `long`；
- 空头 L1/L2、Bearish ABC 或空头 BOP 写 `short`；
- 区间中部、父级冲突、方向未冻结或没有有效交易方向写 `no_valid_direction`。

同一案例可以有 `directional_bias: bull`，但因首障碍或事件闸门不合格而写 `direction: no_valid_direction`。不能用后续涨跌倒推方向。

对于 `internal_label: H1 / H2` 的多头候选，`h_l_ema_slope_gate` 必须为 `long_pass`（Daily EMA20、EMA50 均向上）；对于 `internal_label: L1 / L2` 的空头候选，必须为 `short_pass`（两条均向下）。走平、反向或资料不足时分别记录为 `fail_flat_or_opposite` 或 `pending`，不能写成普通高质量 H/L。`meta_confluence: present` 只表示多个独立来源在同一回调区域汇聚，不是自动触发器。

`meta_confluence` 的 canonical 枚举只有 `present / absent / unknown`；冻结的 H/L 合同必须填写其中之一，不能写 `pending`。当 META 证据尚不足以判断时，用 `unknown` 保留该字段，同时可在整体 `gate_result`、`trade_state`、`trigger_status` 或其他审查状态中保留 `pending`。`meta_zone`、`meta_components`、触发、止损、首障碍和空间仍各自独立，不能因为 META 为 `present` 而自动补齐或授权。

`special_subtype` 是结构或订单路径的补充研究注释，不能替代 `event_context` 或由 raw `event_context` 派生的 `event_bucket`。例如 `special_subtype: ordinary` 不等于 `event_bucket: ordinary_non_event`；`earnings_driven` 是 subtype 写法，而事件统计仍使用 canonical `event_driven`。`gap_reprice` 只描述重订价/订单路径，不自动决定事件 bucket。缺失 subtype 时保留未记录，不能从结果或其他字段回填。

`lineage_id` 是样本依赖控制的规范标识：同一父级结构、同一 A/B 回调或同一局部尝试的替代标签必须使用同一个 ID；不能因为决策日或 H1/H2、L1/L2 标签不同就另造独立样本。大小写和首尾空格不构成不同 lineage。`lineage_id` 不会替研究者自动识别结构，缺失或共享时只能保留描述性结果。

`market_context_id` 是可选的人工市场状态依赖标识，用于记录多只股票共享的同一市场/板块状态；它不是行情扫描器，也不由回放器推断。缺失、共享或与其他记录的持仓区间重叠时，回放器可以保留逐行描述值，但不得输出 independence-adjusted 胜率。没有该字段不等于市场状态已经独立。

`primary_pattern: H3_L3` 时，`internal_label` 必须明确写成 `H3`（多头第三次尝试）或 `L3`（空头第三次尝试），不得使用含混的 `H3_L3`；还必须额外区分 `range_edge_three_push: yes`、`no` 或 `pending`，并记录 `range_edge_side: upper / lower / none / pending`。区间边缘三推允许 A 腿普通或偏弱，但必须记录上沿/下沿位置、反向确认和区间外接受分流；区间中部重复测试不能凭次数升级。

`range_edge_three_push` 只是区间边缘位置/分支旗标，不是 `primary_pattern`，也不等同于 `H3_L3`。当它为 `yes` 时，`range_edge_side` 必须是 `upper` 或 `lower`：上沿只建立空头研究方向假设，下沿只建立多头研究方向假设；这不是自动授权，若触发、空间或合同尚未冻结，canonical `direction` 仍可写 `no_valid_direction`。当它为 `no` 时 side 写 `none`；当它为 `pending` 时 side 写 `pending`。在 `daily_candidate` 中，三推只可作为 `internal_label: H3 / L3` 与 `secondary_context` 的研究关系，且仍受日线主标签白名单约束；只有深审或历史记录已闭合同一 lineage、第三推状态和反向/延续分流时，才可使用兼容 `primary_pattern: H3_L3`。

三推状态统一使用 `third_push_state` 的 canonical 枚举：`exhaustion_candidate`、`continuation_or_climax`、`range_repeat_test` 和 `channel_continuation`；`unclear` 表示第三推状态不能从当时证据中分开。`attempt_direction` 只描述三次尝试的朝向，`direction` 仍是当前研究合同方向；`first_reverse`、`second_confirmation`、`order_branch`、`trade_state` 和 `gate_result` 分别记录反向证据、订单状态和闸门结果，不能互相替代。历史文档中的连字符或 `h3_l3_state`/`push_state` 仅按已登记别名阅读，新记录必须使用 canonical 字段。

## 三、BOP 专用字段

当 `primary_pattern: BOP` 时必须填写：

```text
bop_state: acceptance_watch / ordinary_pullback / failed_breakout / gap_event / bull_flag_continuation
breakout_boundary:
acceptance_close:
follow_through:
retest_zone:
role_reversal_held: yes / no / unclear / not_occurred
```

`BOP` 是独立主合同。ABC、H1/H2 或三推只能放入 `secondary_context`，不能使用 `BOP_ABC` 作为主 pattern，也不能把 BOP 与 ABC/H-L 结果混算。没有回踩时只能写 `acceptance_watch` 或相应的 gap/event 分支，不能补写不存在的回踩。

当事前可见边界被日线强收盘越过、获得跟随并在回踩中守住而形成 `state_transition: breakout_acceptance` 时，原 pattern/反向 thesis 与其旧订单合同立即失效；必须以 `primary_pattern: BOP` 重建 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间，不能沿用旧 entry/stop/target，也不能把旧合同结果并入 BOP。

## 四、订单与风险字段

```text
signal_bar:
confirmation_bar:
new_trigger:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
gap_policy: accept_open / skip / flag_only / not_applicable
order_price_or_zone:
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
structural_stop:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
rough_R_R:
target_layers:
main_uncertainty_or_exclusion:
```

`order_branch` 只表达基础订单合同；`branch_role` 记录反向 stop、角色转换回测、跳空重订等研究分支。历史文件中的 `stop`、`limit-retest`、`market-close`、`reverse-stop` 和 `limit-edge` 是别名，更新新记录时必须映射到上述字段，不能继续作为同一字段的混合枚举。

`gap_policy` 是入场前冻结的缺口处理政策，不得根据事后结果倒填：`skip` 表示开盘越过原触发时记为 `opening-skip`；`accept_open` 表示只有实际开盘价重新通过方向、止损和空间检查后才可记录实际开盘成交；`flag_only` 允许保留实际开盘路径但必须保留缺口旗标，几何失效时不能假定成交；`not_applicable` 只用于 `market_close`。因此 `no-fill`、`opening-skip` 和 `unproven` 都不是 win/loss，也不能进入严格胜率分母。

入场几何必须按固定顺序记录：先确定 `structural_invalidation` 与 `structural_stop`，再找入场方向上最近的 `first_independent_obstacle`，然后填写 `pre_entry_space_R`/`space_status`，最后才写 `rough_R_R`、`target_layers` 或 measured move。`rough_R_R` 不能跳过最近独立障碍；如果结构止损、首障碍或空间只能写区域、`pending` 或 `unknown`，就不能把它们伪装成冻结的数值合同。

### 回放结果和胜率分母

冻结合同回放的结果字段至少应保留：

```text
fill_status: filled / no-fill / opening-skip / unproven / not-traded
evidence_status: comparable / excluded / excluded_incomplete_horizon / excluded_ambiguous / observation_only
pre_entry_provenance_status: complete / incomplete
pre_entry_provenance_missing_fields:
planned_entry_trigger:
sample_id:
market_context_id:
win_rate_eligible: yes / no
trade_result: win / loss / scratch / pending / not-applicable
path_result: target-reached / invalidated / first-obstacle-reached / time_exit / incomplete-horizon / ambiguous / ...
ambiguous_intrabar: yes / no
first_obstacle_hit: yes / no / unknown
realized_R:
bars_held:
entry_date:
exit_date:
```

`first_obstacle_hit` 是路径过程字段，不是胜负标签；触及首障碍不能自动写成 `win`。若首障碍只出现在未解决的 stop/target 歧义路径上，应写 `unknown`。`realized_R` 只有在成交、路径完成、无未解决歧义且 `win_rate_eligible=yes` 时才可进入可比结果。`opening-skip`、`no-fill`、`observation_only`、`incomplete-horizon`、`ambiguous_intrabar` 和 `pending` 不进入胜率分母。`max_hold_bars` 表示实际交易 `entry_bar` 之后允许观察的完整 K 线数；非 `market_close` 的时间退出在观察窗口结束后的下一根 K 线开盘成交，因此 `bars_held` 这个 backtesting.py 的 entry/exit bar 索引距离可能比 `max_hold_bars` 多 1，不能把该执行索引差异误读成额外的自由持仓。`market_close` 按收盘时间索引计数；如果数据末尾没有可执行的时间退出价格，则必须标为 `incomplete-horizon`。

`summary.json` 的 `completed_trade_count` 只统计同时满足 `pre_entry_provenance_status=complete`、`win_rate_eligible=yes`、`trade_result=win/loss/scratch`、`evidence_status=comparable`、`fill_status=filled`、非空 `path_result`、无歧义/未完成 horizon、非重复结果且有有限 `realized_R` 的行；如果结果行带有 H/L EMA gate，还必须由该事前 gate 推导出 `contract_eligibility=eligible`。缺失 `path_result` 的结果没有足够的路径审计证据，只能留在排除 bucket，不能进入胜率分母。`pre_entry_provenance_status=incomplete` 的行只能作为描述性结果，`pre_entry_provenance_missing_fields` 必须保留缺失项。`win_rate_eligible_count` 是结果旗标数量，不应在旗标与结果不一致时直接当作分母；`win_rate_eligibility_mismatch_count`、`contract_eligibility_mismatch_count`、`event_bucket_mismatch_count`、`contract_space_bucket_mismatch_count`、`win_rate_guard_exclusion_count` 和互斥的 `outcome_bucket_counts` 必须保留用于审计。`event_bucket` 与 `contract_space_bucket` 必须从原始事前字段重算，结果文件中的同名派生字段不能反向覆盖合同证据。`first_obstacle_hit`、`space_to_first_obstacle_R` 和 `realized_R` 是结果阶段字段，不得回填入 `space_status`、`pre_entry_space_R` 或任何 EMA gate。

摘要还必须报告 `unique_sample_id_count`、`missing_sample_id_count`、重复 sample/合同族的 group/row/extra 计数、`unique_lineage_count`、共享 lineage 计数、`unique_market_context_count`、缺失/共享市场状态计数，以及同一标的持仓区间重叠计数。相同 `sample_id` 或同一合同族的重复行全部标记为 `duplicate_result`，不任意保留其中一份；不同 `lineage_id` 也不自动证明样本独立。`independence_status` 和 `independence_statistics_status` 必须明确说明缺失或依赖来源。

运行元数据应保留 `engine_version`、`backtesting_version`、`python_version`、`pandas_version`、`numpy_version`、`engine_source_sha256`、`price_file_sha256`、`contract_file_sha256`、`result_set_sha256`、`results_file` 和 `results_file_sha256`，并保留 `summary_provenance`。其中 `summary_provenance` 至少复制实际 `result_columns`、`pre_entry_provenance_status_counts`、`pre_entry_provenance_complete_count`、`pre_entry_provenance_incomplete_count`、`completed_trade_count`、`outcome_bucket_counts` 和各类 provenance/eligibility mismatch 计数；`summary.json` 中嵌套的 `run_metadata` 应与独立 `run_metadata.json` 一致。引擎源码指纹与运行时版本一起锁定执行语义，结果文件指纹锁定实际写出的 artifact；输入/结果指纹用于识别同一输入的重复 artifact 或同一 `sample_id` 的不同版本。它们是审计 provenance，不是交易信号。旧的、缺少这些字段的 `summary.json` 或 `run_metadata.json` 只能作为历史描述，不能与新摘要拼接成验证结果。

`scripts/validate_pa_research_artifact.py` 是只读校验入口：它从 `results.csv` 重建摘要关键计数，核对 `summary_provenance`、CSV/summary/metadata 的 hash、当前 `engine_source` hash 和嵌套 metadata 一致性。`result_set_sha256` 按 engine 约定统一 CSV 换行符后核对，`results_file_sha256` 仍核对实际文件字节。当前 engine/schema 完整且通过检查返回 `current_valid`；旧 engine、缺少当前字段或缺少 provenance 的输出返回 `historical_incomplete`，不能作为当前验证样本；结构损坏、文件解析失败、源码文件不可用或当前字段互相矛盾返回 `invalid`。CLI 返回码固定为 `0=current_valid`、`2=historical_incomplete`、`1=invalid`；`current_valid` 只表示 artifact 链路完整，不等于胜率已经验证。校验过程不下载行情、不重跑回放、不写回文件。

## 五、状态轴与交接轴

不同状态不能塞进一个 `status`：

```text
document_status: draft / adopted / historical / research_only
document_maturity: provisional
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
thesis_state: working / failed / invalidated / replaced / pending
handoff_status: research_only / not_ready / ready_for_system
```

这些字段不代表胜率或实盘授权。`research_positive_conditional` 仍是人工研究状态；`valid_no_trade` 不是亏损；`handoff_status: ready_for_system` 只有在研究交接规范的全部晋级闸门通过后才可使用。`adopted` 只表示文档被采纳，不表示规则已经验证或可执行。

### `observation_only` 与 `valid_no_trade` 的边界

- `observation_only`：图表、事件、方向、触发或空间证据仍不完整，或者只保留形态学习价值，尚未形成可复核的交易合同；不建立订单。若资料还可能补齐，可同时使用 `pending`。
- `valid_no_trade`：形态、方向和入场几何已经足够复核，但已知硬闸门（例如首障碍过近、结构止损过宽、事件排除或成交合同不合格）明确否决新交易；它是有效的不交易决定，不是亏损结果。
- 已知硬闸门失败不能用 `observation_only` 隐去；反过来，证据缺失也不能用 `valid_no_trade` 冒充已经完成的否决。`research_state`、`trade_state` 和 `gate_result` 仍须分轴填写，不能合并为一个最终状态。

## 六、最小输出模板

```text
### [symbol] [review_date] — [primary_pattern]

contract_scope:
symbol:
review_date:
data_source:
direction:
data_status:
as_of_time:
timezone:
session_state:
timeframes_seen:
chart_scope:
daily_context_window:
major_high_low_review:
ema20_50_200_review:
market_cap_usd:
market_cap_as_of:
market_cap_source:
parent_state:
directional_bias:
primary_pattern:
secondary_context:
range_edge_three_push:
internal_label:
state_transition:
lineage_status:
lineage_id:
market_context_id:
major_highs_lows:
support_resistance_and_role_zones:
daily_ema20_50_200:
daily_ema20_slope:
daily_ema50_slope:
h_l_ema_slope_gate:
h_l_pullback_location:
a_leg_quality:
b_leg_class:
special_subtype:
b_leg_location:
meta_confluence:
meta_zone:
meta_components:
event_context:
event_bucket:
event_source_as_of:
earnings_next_three_sessions:
sector_reference:
sector_state:
market_reference:
market_state:
permission:
key_breakout_or_structure_location:
why_it_meets_or_fails_the_rule:
possible_entry_trigger:
signal_bar:
confirmation_bar:
new_trigger:
order_branch:
branch_role:
gap_policy:
actual_fill_or_open_skip:
structural_stop:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R:
pre_entry_space_R:
space_status:
rough_R_R:
target_layers:
research_state:
trade_state:
thesis_state:
gate_result:
handoff_status:
main_uncertainty_or_exclusion:
```

任何缺失字段都必须明确写 `unknown`、`pending` 或 `not_applicable`。本合同只服务 PA Research；不创建行情扫描器、不修改 Codex Trading、不连接 Execution Agent。

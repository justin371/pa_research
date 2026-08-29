# Pattern README 与基础视觉框架 canonical 输出覆盖审计（2026-08-29）

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 审计目的与范围

本轮只审计 PA Research 的 16 个 pattern README、8 个基础视觉层、`patterns/README.md`、`foundations/README.md`、统一输出合同和视觉复核卡。重点核对 canonical 字段是否有明确继承入口、局部工作卡是否误用旧字段或自定义枚举、以及索引是否能把入口追溯到统一合同。

本轮只使用仓库现有文档、validator 和回归测试：不下载或查询行情、不连接 Futu/OpenD、不看新图、不运行回放、不增加样本，不修改 CSV、历史结果或 engine 有效语义。`scope_boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。

## Canonical authority

完整案例以[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)和[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)为 authority。各层只允许补充本层语义，不能把局部字段变成新的主标签、订单分支或统一状态。

本轮核对的共同字段边界为：

```text
contract_scope
data_status / as_of_time / timezone / session_state / timeframes_seen / chart_scope
daily_context_window / major_high_low_review / ema20_50_200_review
direction / primary_pattern / internal_label / lineage_status / lineage_id
third_push_state / state_transition
order_branch / actual_fill_or_open_skip
structural_invalidation / structural_stop
first_independent_obstacle / rough_space_to_first_obstacle_R / pre_entry_space_R / space_status / rough_R_R
research_state / trade_state / gate_result / handoff_status
```

状态轴仍然分开：

```text
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
```

`daily_candidate` 的 `primary_pattern` 仍只允许 `ABC_CONT` 或 `BOP`；H1/H2/L1/L2/H3/L3 放入 `internal_label`，其他关系放入 `secondary_context`。`4H-like`、`60m proxy` 等只在来源确实使用聚合周期时作为 `timeframes_seen` 的可读 provenance，并必须说明聚合口径，不能冒充原生 4H，也不能代替 `daily_context_window` 或复核完整度。

## 16 个 pattern README 覆盖

以下 16 个目录全部实际存在，并均有统一合同、视觉复核卡、两年 Daily 左侧、重要高低点、支撑阻力、EMA20/50/200、`pending`/`observation_only` 状态边界和 daily-candidate 主标签映射入口：

| 层级 | pattern README | canonical 处理 |
| --- | --- | --- |
| core | [`01_h1_l1_first_entry`](../../patterns/01_h1_l1_first_entry/README.md) | 继承统一合同；H1/L1 只作 `internal_label` |
| core | [`02_h2_l2_second_entry`](../../patterns/02_h2_l2_second_entry/README.md) | 继承统一合同；H2/L2 只作 `internal_label` |
| core | [`03_abc_continuation`](../../patterns/03_abc_continuation/README.md) | `ABC_CONT` 母结构，H/L 作为内部尝试 |
| core | [`04_range_edge_second_entry`](../../patterns/04_range_edge_second_entry/README.md) | 区间边缘补充字段；兼容 `RFB` 只在闭合历史/深审合同使用 |
| core | [`05_failed_breakout_climax`](../../patterns/05_failed_breakout_climax/README.md) | 失败突破/高潮补充字段；状态轴独立 |
| core | [`06_breakout_pullback_bop`](../../patterns/06_breakout_pullback_bop/README.md) | `BOP` 主合同；接受状态写入 `state_transition` |
| core | [`07_mtr_reversal`](../../patterns/07_mtr_reversal/README.md) | `mtr_state` 是专用观察轴，不替代 `thesis_state` |
| core | [`08_three_push_h3_l3`](../../patterns/08_three_push_h3_l3/README.md) | 详细局部卡已补齐 canonical 证据、结构、订单、空间和状态轴 |
| independent | [`09_vcp_minervini`](../../patterns/09_vcp_minervini/README.md) | 独立主题；未扩展 schema 时使用 `other`/补充语义 |
| independent | [`10_final_flag`](../../patterns/10_final_flag/README.md) | 独立主题；不自动变成 MTR、ABC 或 BOP |
| independent | [`11_opening_reversal`](../../patterns/11_opening_reversal/README.md) | 独立开盘事件主题；事件和订单另记 |
| independent | [`12_channel`](../../patterns/12_channel/README.md) | 独立通道状态主题；画线不自动产生交易信号 |
| independent | [`13_inside_bar_two_bar_reversal`](../../patterns/13_inside_bar_two_bar_reversal/README.md) | 独立 K 线结构；OHLC/接受未冻结时保留观察 |
| independent | [`14_triangle_expanding_range`](../../patterns/14_triangle_expanding_range/README.md) | 独立双向结构；突破/失败另写状态转换 |
| independent | [`15_double_top_bottom`](../../patterns/15_double_top_bottom/README.md) | 两次分离测试的独立主题；不自动升级 MTR |
| independent | [`16_head_shoulders_rounded`](../../patterns/16_head_shoulders_rounded/README.md) | 复杂结构主题；颈线、确认和空间不足时不授权 |

结论：16 个 README 采用“统一合同 + pattern-specific 差异字段”的继承模式，没有证据要求重复复制整套 22 个字段；`08_three_push_h3_l3` 原先有自己的局部合同，已改成 canonical 证据头和状态轴，并保留三推特有字段。没有把独立主题强行纳入 ABC/H-L/三推统计。

## 8 个基础视觉层覆盖

| 基础层 | 局部职责 | canonical 边界 |
| --- | --- | --- |
| [`01_support_resistance`](../../foundations/01_support_resistance/README.md) | 区域、角色、位置、止损和首障碍 | 只提供几何补充；不单独冻结 pattern 或订单 |
| [`02_measured_move_targets`](../../foundations/02_measured_move_targets/README.md) | MM、AB=CD、磁铁和目标层 | 先审首障碍与空间，不能用远端测量补救坏 R/R |
| [`03_late_trend_entry_filter`](../../foundations/03_late_trend_entry_filter/README.md) | 后段、追价、回调与后段状态 | 工作卡已改用 canonical 证据、触发、订单、止损、空间和三条状态轴；后段不是第四个 pattern |
| [`04_multitimeframe_review`](../../foundations/04_multitimeframe_review/README.md) | 父级、低周期确认和独立低周期合同 | `parent_*`/`lower_*` 只标周期层级；顶层主标签、订单、空间和状态轴仍使用 canonical 字段 |
| [`05_event_sector_market_gate`](../../foundations/05_event_sector_market_gate/README.md) | 财报、事件、板块、大盘和 permission | `permission`/`gate_result` 只是前置闸门，不代替方向、几何或交易状态 |
| [`06_order_risk_contracts`](../../foundations/06_order_risk_contracts/README.md) | 订单分支、成交/跳过、止损和 R/R | 工作卡已改用 `new_trigger`、`actual_fill_or_open_skip`、`structural_stop`、空间字段和分轴状态 |
| [`07_market_state_context`](../../foundations/07_market_state_context/README.md) | 趋势、交易区间、边缘、过渡和高潮 | `parent_state` 已统一为 `open_trend / trading_range / range_edge / transition / climax / unclear`；成熟度用本层 `range_state` 补充 |
| [`08_leg_pressure_signal_quality`](../../foundations/08_leg_pressure_signal_quality/README.md) | 强 A、B 压力、信号 K、EMA 和量价背景 | `a_leg_quality`、`b_leg_class`、`b_leg_location`、`daily_ema20_slope`/`daily_ema50_slope` 等使用 canonical 名称；其余压力描述仍是补充 |

## 已修复的明确问题

1. `patterns/08_three_push_h3_l3/README.md` 的局部卡曾使用单数 `timeframe` 和 `context_timeframes_seen`，容易把计数周期与完整证据范围混淆。现在使用 `timeframes_seen`；若只在一个周期计数，另用 pattern-specific `count_timeframe`，并补齐 `contract_scope`、数据状态、图表完整度、方向、主标签、lineage、触发、成交/跳过、结构止损、空间和状态轴。
2. `foundations/03_late_trend_entry_filter/README.md` 的局部卡曾缺少 `stop_limit`、`pre_entry_space_R`、`space_status` 和分轴状态，并使用 `final_state`。现在补齐 canonical 字段；`last_push` 的值也不再用活动连字符别名。
3. `foundations/04_multitimeframe_review/README.md` 的局部卡曾使用 `parent_pattern`、`actual_or_assumed_fill`、`gap_state` 和合并式 `decision`。现在保留父级/低周期层级补充，但同时填写 `primary_pattern`、`signal_bar`、`new_trigger`、`actual_fill_or_open_skip`、`gap_policy`、结构/空间字段和三条状态轴。
4. `foundations/06_order_risk_contracts/README.md` 的“统一订单卡”曾使用 `decision_time`、`trigger_or_zone`、`actual_or_assumed_fill`、`space_to_first_obstacle` 和 `final_status`。现在改为 canonical 订单、几何、成交/跳过和分轴状态字段；订单层的区域和管理描述仍作为补充保留。
5. `foundations/07_market_state_context/README.md` 的 `parent_state` 曾使用非 canonical `mature_range`，并用 `climax_or_exhaustion` 表示统一高潮状态。现在统一为 `trading_range` 和 `climax`，区间成熟度另写 `range_state`，避免局部状态冒充顶层枚举。
6. `foundations/08_leg_pressure_signal_quality/README.md` 的工作卡曾使用未登记的 `A_quality`、`EMA20_slope`、`EMA50_slope`、`pullback_location` 和合并式 `decision`。现在改为 `a_leg_quality`、`daily_ema20_slope`、`daily_ema50_slope`、`h_l_pullback_location`，并补充 `b_leg_class`、`b_leg_location`、触发和 canonical 状态轴；`B_shape` 等只保留为解释性压力字段。

`01`/`02` 的位置和测量层没有独立序列化合同；`05` 的卡只覆盖事件/板块/大盘闸门。这是职责边界，不是缺失：需要形成完整案例时，必须回到统一合同，不能把基础层局部卡当成完整交易记录。

## 追加交易日志边界复核（2026-08-29）

后续逐项复核发现，`foundations/03`、`foundations/04`、`patterns/06` 和 `patterns/08` 的局部卡虽然使用了 canonical `actual_fill_or_open_skip`，但原文没有在卡旁明确说明它是研究/回放订单路径，容易被误读成券商或账户成交日志；MM、事件闸门和少数独立 pattern 的“实际成交”措辞也存在同样的阅读风险。现已在 `foundations/README.md`、`patterns/README.md` 及相关局部卡补充统一限定，并将 `foundations/02` 的“实际成交假设”改成研究/回放路径表述。

边界固定为：订单卡中的 `actual_fill_or_open_skip` 只描述研究合同/历史回放订单路径；回放结果的 `fill_status`、`trade_result`、`realized_R` 等仍只能出现在独立 replay/result 记录；真实券商/账户交易日志必须来自独立来源。当前 PA Research checkout 不包含真实交易日志，不能用订单卡或回放结果代替它。此次只修改文档、索引校验和回归测试，不新增样本、成交、回放结果或胜率分母。

## 验收结论

- 16 个 pattern README 的目录和索引入口完整；核心八个与独立八个保持分层；
- 16 个 pattern README 都继承统一合同和视觉复核卡，`08` 的详细模板已去除周期字段混淆；
- 8 个基础层均指向统一合同，活动局部模板的旧字段和非 canonical 枚举已登记或修复；
- `timeframes_seen`、两年 Daily 左侧、重要高低点、EMA20/50/200、方向、结构止损、首障碍、入场前空间和状态轴没有被局部字段替代；
- 本轮没有新增样本、成交、回放结果或胜率分母；结论仍为 `no-new-positive`，`validated win-rate: not-computable`；
- 本轮只属于 `PA Research only`，不修改 Codex Trading，不创建量化扫描器，不连接 Futu/OpenD，不连接 Execution Agent。

该审计只验证文档契约和索引边界；它不表示 pattern 已自动识别、规则已验证或可以直接下单。

## 追加 canonical 枚举与事件闸门复核（2026-08-29）

继续逐项对照 16 个 pattern README、8 个基础层、日线选股规则和统一输出合同后，发现三处可复现的文档偏差：

1. `patterns/08_three_push_h3_l3/README.md` 的局部协议把 `thesis_state` 写成 `working / failed / replaced / pending`，遗漏统一合同的 `invalidated`；现已补齐。
2. `foundations/05_event_sector_market_gate/README.md` 原先对“已知财报未来三个交易 session”同时允许 `gate_result: pending`，与日线规则“已知即 `valid_no_trade`，仅日期/影响不清楚才 `pending`”冲突；现已统一为 `gate_result: valid_no_trade` + `trade_state: valid_no_trade`。
3. `foundations/03_late_trend_entry_filter/README.md` 的兼容 `primary_pattern` 列表覆盖 `daily_candidate`，但原文没有提示按 `contract_scope` 收窄；现已明确日线候选只能使用 `ABC_CONT`/`BOP`，兼容值仅用于闭合深审/历史记录。

validator 和回归测试已覆盖上述三条边界及旧事件文案回归。修复只涉及 PA Research 文档和守卫，不修改 16 个 pattern 的案例、CSV、样本、结果或 engine 有效语义；`no-new-positive` 与 `validated win-rate: not-computable` 保持不变，不创建量化扫描器、不连接 Execution Agent。

## 追加 parent_state 枚举与活动模板复核（2026-08-29）

继续对照统一输出合同、日线选股规则、视觉卡和活动基础层模板后，发现并修复以下可复现偏差：

1. `patterns/05_failed_breakout_climax/README.md` 的局部卡使用 `trend / range / channel / transition`，已改为 canonical `open_trend / trading_range / range_edge / transition / climax / unclear`。
2. `foundations/03_late_trend_entry_filter/README.md`、`foundations/04_multitimeframe_review/README.md` 和 `foundations/08_leg_pressure_signal_quality/README.md` 虽已声明 `parent_state`，但模板值为空；现补齐统一枚举，避免基础层重新发明父级状态。
3. 日线选股模板、市场状态审计卡和 Late Trend/Inside Bar/Triangle/Multi-timeframe 活动视觉模板均补齐同一 `parent_state` 枚举。

本轮同时修正了本报告此前的 `15 个 README` 计数笔误。validator 与回归测试现在会对这些活动路径要求 canonical `parent_state`，并拒绝旧的趋势/区间/通道混合枚举。历史证据报告中的旧词仍仅按日期明确的描述性别名读取，不作为新模板字段。

## 追加活动视觉复核卡 canonical label 与 parent_state 复核（2026-08-29）

在上一轮活动模板修复后，本轮继续只对 PA Research 的新记录入口做字段审计；不下载或查询行情、不看新图、不运行回放、不新增样本、不修改 CSV/历史结果/engine 有效语义。复核确认并修复了以下可复现的入口偏差：

1. `docs/visual_pa_review_card_CN.md` 的快速视觉初筛原先把待确认的 pattern 空栏写成 `primary_pattern`；现在使用非 canonical 的 `pattern_candidate`，只有完成闭合记录后才映射到 `primary_pattern`。
2. 跨 Pattern 优先矩阵、策略 inventory 及相关 H1/H2、Multi-timeframe、Late Trend、事件闸门、订单风险和 Opening Reversal 活动卡现在明确分开 `primary_pattern`、`internal_label` 和 `direction`；`daily_candidate` 仍只允许 `ABC_CONT`/`BOP`，H1/H2/L1/L2/H3/L3 只作为内部标签。
3. 策略 inventory 和 Channel 局部卡不再用 `H_or_L_attempt` 这类合并字段；旧的 H/L attempt 与 signal K 语义映射为 `internal_label` + `signal_bar`。Channel 的 `channel_type`/`channel_status` 仍是补充观察轴，不冒充 `parent_state` 或 pattern 主标签。
4. Channel 视觉框架已纳入活动视觉框架集合；其统一卡补齐证据头、两年 Daily/重要高低点/EMA 复核、canonical 结构/订单/空间/状态轴和 `handoff_status`。其余当前视觉复核卡的 `parent_state` 统一为 `open_trend / trading_range / range_edge / transition / climax / unclear`。
5. `decision_timestamp`/`decision_time`、`parent_state_and_location`、`actual_or_assumed_fill` 等旧合并入口已分别收敛到 `as_of_time`、`parent_state` + `parent_location`、`actual_fill_or_open_skip`；历史案例中的自由文本和日期明确的旧字段不改写，只作为历史事实/显示语义读取。

validator 与回归测试现对上述活动 mapping 模板、快筛字段、canonical `parent_state` 和索引边界提供守卫。修复只涉及 PA Research 的文档、索引、validator 和回归测试；`no-new-positive` 与 `validated win-rate: not-computable` 保持不变，不创建量化扫描器、不连接 Execution Agent。

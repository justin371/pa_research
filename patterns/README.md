# PA Research 核心 PA Pattern 与独立体系目录

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

每日候选筛选统一遵循 [`PA Research 日线选股规则 v0.1`](../docs/pa_research_daily_selection_rules_v0_1_CN.md)：只用完成的 Daily K 线选股，重点为 `ABC_CONT` 与 `BOP`；4H/1H/15m 不能改变日线候选主标签。

所有目录的新案例统一使用[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。本索引中的 pattern-specific “最小视觉协议”是差异字段，不是完整候选合同；每条记录仍必须有 `contract_scope`、`direction`、证据时间、事件/板块/大盘闸门、订单合同、结构止损、第一独立障碍和分轴状态。

统一边界：`v0.x` 规则/合同与回放引擎 `0.3.15` 均只属于 PA Research 研究层（`PA Research only`），不是 Codex Trading 生产规则；`no-new-positive` 和 `validated win-rate: not-computable` 保持不变，`60%` 仅是待检验目标；不创建量化扫描器，不连接 Execution Agent。

日线筛选优先级与全局研究优先级分开：日线只优先筛选 `ABC_CONT` 和 `BOP`；H2/L2 仍是全局 pattern 研究主线，但不覆盖日线主标签，也不代表已进入系统实现队列。

这里是 PA Research 当前阶段的核心研究入口。目标是让视觉助手能够在完整图表上：

1. 先识别背景、位置和左侧结构；
2. 再识别 pattern 是否真的成立；
3. 最后给出入场、结构止损、第一独立障碍、R/R 和 no-trade 分支。

“高胜率”在本项目中不是固定百分比，也不是看到标签就下单。每个 pattern 都必须经过背景、位置、信号 K、触发、空间、事件和失效条件的共同审计。

## 当前核心范围

| 顺序 | Pattern 目录 | 当前定位 |
| --- | --- | --- |
| 1 | [`H1/L1 第一次入场`](01_h1_l1_first_entry/README.md) | 强 A 腿后的第一次方向尝试；优先级低于 H2/L2，但必须实现 |
| 2 | [`H2/L2 第二次入场`](02_h2_l2_second_entry/README.md) | 当前最优先的趋势延续研究主线 |
| 3 | [`ABC 趋势延续`](03_abc_continuation/README.md) | A 腿、B 回调、C 恢复；区间中部不强行使用 |
| 4 | [`区间边缘二次入场`](04_range_edge_second_entry/README.md) | 区间顶部卖出、底部买入，以及失败突破后的二次机会 |
| 5 | [`失败突破与高潮`](05_failed_breakout_climax/README.md) | 失败接受、高潮后小反转/区间和 no-trade 分流 |
| 6 | [`突破回踩 / BOP`](06_breakout_pullback_bop/README.md) | 突破被接受后的回踩与新交易合同 |
| 7 | [`MTR 趋势反转`](07_mtr_reversal/README.md) | 高级形态；需要位置、结构破坏和第二次确认 |
| 8 | [`三推 / H3-L3 压力状态`](08_three_push_h3_l3/README.md) | 第三次测试的衰竭、扩张、区间边缘候选、区间中部观察和延续分流 |

## 独立体系主题

| 主题 | 目录 | 当前定位 |
| --- | --- | --- |
| VCP / Volatility Contraction Pattern（Minervini） | [`VCP / Minervini`](09_vcp_minervini/README.md) | 独立的强势股整理、连续收缩与 pivot 突破研究；不计入 Brooks 核心八个，不与 ABC/H-L/三推合并 |
| Final Flag / 最终旗形 | [`Final Flag`](10_final_flag/README.md) | 独立的趋势末端压缩与最后尝试分流；与普通旗形、MTR、BOP 和 VCP 分开 |
| Opening Reversal / 开盘反转 | [`Opening Reversal`](11_opening_reversal/README.md) | 独立的开盘第一波失败/接受与反向确认研究；与 BOP、区间边缘和普通 H/L 分开 |
| Channel / 紧通道、宽通道与状态切换 | [`Channel / 通道`](12_channel/README.md) | 独立的通道边界、紧/宽通道、扩张、突破接受与区间过渡研究；不把画线当成自动交易信号 |
| Inside Bar / 两根 K 线反转 | [`Inside Bar / 两根 K 线反转`](13_inside_bar_two_bar_reversal/README.md) | 独立区分严格内包、二内包/IOI、两根反转与 H/L 信号序列；不把小实体当成自动信号 |
| Triangle / 三角形与区间内区间 | [`Triangle / 三角形`](14_triangle_expanding_range/README.md) | 独立区分收缩三角形、扩张三角形、区间内区间、突破接受与失败；不把两点连线当成三角形 |
| Double Top / Double Bottom / 双顶双底 | [`Double Top / Double Bottom`](15_double_top_bottom/README.md) | 独立区分两次有分离测试、区间边缘、MTR、Final Flag 与普通延续；不把相近高低点自动当反转 |
| Head-and-Shoulders / Rounded / 头肩与圆顶圆底 | [`Head-and-Shoulders / Rounded`](16_head_shoulders_rounded/README.md) | 独立区分头肩、圆顶/圆底、复杂双顶双底、颈线接受与普通旗形；不把三个点自动当反转 |

## 基础视觉层

| 基础层 | 目录 | 当前定位 |
| --- | --- | --- |
| Support / Resistance / 支撑阻力 | [`Support / Resistance`](../foundations/01_support_resistance/README.md) | 所有 pattern 共用的位置、结构止损、首障碍与角色转换过滤；不是独立交易形态 |
| Measured Move / AB=CD / 磁铁目标 | [`Measured Move / targets`](../foundations/02_measured_move_targets/README.md) | 所有 pattern 共用的空间、第一独立障碍、目标层级和持仓管理；不是独立交易形态 |
| Late Trend Entry / 趋势后段过滤 | [`Late Trend Entry / 追价过滤`](../foundations/03_late_trend_entry_filter/README.md) | 所有 pattern 共用的时机、空间、高潮、突破接受和新增仓位过滤；不是独立交易形态 |
| Multi-timeframe Review / 多周期复核 | [`Multi-timeframe Review`](../foundations/04_multitimeframe_review/README.md) | 所有 pattern 共用的 Daily/4H/1H/15m 职责、确认、独立低周期合同和跳空重订；不是独立交易形态 |
| Event / Sector / Market Gate / 事件板块闸门 | [`Event / Sector / Market Gate`](../foundations/05_event_sector_market_gate/README.md) | 所有 pattern 共用的财报、重大事件、板块/大盘许可和订单重订前置过滤；不是独立交易形态 |
| Order / Risk Contracts / 订单风险合同 | [`Order / Risk Contracts`](../foundations/06_order_risk_contracts/README.md) | 所有 pattern 共用的 stop、limit、market-close、stop-limit、实际成交、结构止损和 R/R 语义；不是独立交易形态 |
| Market State / Context / 市场状态与父级背景 | [`Market State / Context`](../foundations/07_market_state_context/README.md) | 所有 pattern 共用的趋势/区间/边缘/过渡/高潮分类、second-leg trap 与突破接受后的状态重建；不是独立交易形态 |
| Leg Pressure / Signal Quality / 腿与信号 K 质量 | [`Leg Pressure / Signal Quality`](../foundations/08_leg_pressure_signal_quality/README.md) | 所有 pattern 共用的强 A、B 压力变化、setup/signal/trigger/follow-through 与 EMA/量价汇合；不是独立交易形态 |

## 统一研究字段

每个目录都按同一套视觉顺序研究：

```text
contract_scope
timeframes_seen / data_status / as_of_time / timezone / session_state / chart_scope
parent_state / market_context_id
direction: long / short / no_valid_direction
left_structure_and_location / major_highs_lows / support_resistance_and_role_zones
daily_ema20_50_200 / a_leg_quality / b_leg_class / b_leg_location / special_subtype
lineage_status / lineage_id / internal_label / attempt_direction / third_push_state / first_reverse / second_confirmation / range_edge_three_push / range_edge_side
daily_context_window / major_high_low_review / ema20_50_200_review
daily_ema20_slope / daily_ema50_slope / h_l_ema_slope_gate / h_l_pullback_location
primary_pattern / secondary_context / pattern_like_reason
state_transition / bop_state
signal_bar / confirmation_bar / new_trigger / follow_through
order_branch / branch_role / actual_fill_or_open_skip
structural_stop / structural_invalidation
first_independent_obstacle / rough_space_to_first_obstacle_R / space_status / rough_R_R
event_context / event_bucket / sector_state / market_state / permission / gate_result
research_state / trade_state / thesis_state / handoff_status
main_uncertainty_or_exclusion / failure_or_no_trade_reason
```

`a_leg_quality`、`b_leg_class`、`b_leg_location` 的 canonical 字段分别代表 A 质量、B 类别和 B 位置。历史 H/L 合同可能缺少这些字段，或使用已登记的旧别名：`strong_A`→`strong`、`ordinary_A`→`ordinary`、`controlled_B`→`controlled`、`deep_late_controlled_B`→`deep_but_late_controlled`。别名只用于历史解释，不改变 CSV、不进入新的胜率分母，也不能把 `h_l_pullback_location` 当作独立 B 位置或类别字段。

本次 H/L A/B 质量、位置和 EMA 字段覆盖核对见[`H/L A/B 质量、位置与 EMA 字段一致性审计`](../research/backtesting/hl_leg_quality_location_axis_consistency_audit_2026-08-29_CN.md)。

H/L 回调位置自由文本与方向、EMA gate、support/role-reversal 和历史 B 词的语义边界见[`H/L 回调位置文本语义与方向边界审计`](../research/backtesting/hl_pullback_location_semantics_audit_2026-08-29_CN.md)。

H/L META 状态、组件与空间/授权边界见[`H/L META 字段与授权边界审计`](../research/backtesting/hl_meta_boundary_audit_2026-08-29_CN.md)。

H/L 两年背景、重要高低点、EMA20/50/200 和图像 provenance 边界见[`H/L 视觉前置证据与冻结资格审计`](../research/backtesting/hl_visual_preflight_contract_audit_2026-08-29_CN.md)。

H/L lineage、共享父级、缺失 `market_context_id` 与独立性分母边界见[`H/L lineage、市场状态与独立性分母审计`](../research/backtesting/hl_lineage_market_context_independence_audit_2026-08-29_CN.md)。

H/L 订单分支、预冻结缺口政策和成交/结果状态边界见[`H/L 订单分支、缺口政策与结果状态边界审计`](../research/backtesting/hl_order_gap_contract_audit_2026-08-29_CN.md)。

H/L selection/replay 的合同数、成交状态和严格分母计数见[`H/L selection/replay 状态计数一致性审计`](../research/backtesting/hl_report_state_count_consistency_audit_2026-08-29_CN.md)。

选择报告、候选卡和视觉记录只保存入场前证据；成交、退出、胜负、胜率和 `realized_R` 只能出现在独立 replay/result 记录中。结果不能反向改写 pattern、方向、lineage、触发、结构止损、首障碍或空间字段。逐文件复核见[`选择记录与回放结果证据边界审计`](../research/backtesting/pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md)；事件/空间/独立性字段的派生与引用复核见[`事件、空间与独立性字段引用一致性审计`](../research/backtesting/event_space_lineage_consistency_audit_2026-08-29_CN.md)；H/L raw `event_context` 与 canonical `event_bucket` 的显示分层见[`H/L event bucket 标签一致性审计`](../research/backtesting/event_bucket_label_consistency_audit_2026-08-29_CN.md)；`special_subtype` 与事件轴的范围边界见[`H/L special subtype 与事件轴一致性审计`](../research/backtesting/special_subtype_event_axis_consistency_audit_2026-08-29_CN.md)；H/L EMA 闸门、回调位置和报告分母复核见[`H/L EMA 闸门、回调位置与报告分母一致性审计`](../research/backtesting/hl_ema_gate_report_consistency_audit_2026-08-29_CN.md)；H/L 报告的历史几何、显式空间状态和敏感性阈值复核见[`H/L 报告空间、版本与结论表述一致性审计`](../research/backtesting/hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md)。

各 pattern README 中的“成交/实际成交/成交路径”以及 `actual_fill_or_open_skip` 均只描述研究合同或历史回放订单路径，不是券商或账户的真实交易日志。真实交易日志若存在，必须来自独立来源；pattern 文档或回放结果不能代替它。

### Pattern-specific shorthand 与 canonical 几何

各目录的最小视觉协议只补 pattern-specific 信息；其中的 `location`、`location_and_left_structure`、`major_location`、`prior_boundary`、`space`、`trigger`、`target_path` 和 `first_magnet` 等短字段是人读的差异字段，不是统一合同的新枚举。完整记录必须回填统一字段：

| 差异字段或旧别名 | 统一合同字段 | 说明 |
| --- | --- | --- |
| `location` / `location_and_left_structure` / `major_location` | `left_structure_and_location`、`major_highs_lows`、`support_resistance_and_role_zones` | 记录左侧位置和角色区；BOP 的 `prior_boundary` 还要写 `key_breakout_or_structure_location` |
| `space` / `target_path` | `first_independent_obstacle`、`rough_space_to_first_obstacle_R`、`pre_entry_space_R`、`space_status`、`rough_R_R` | 先审计最近独立障碍，再写粗略 R/R 和远端目标 |
| `trigger` / `trigger_price_or_zone` | `new_trigger`、`order_price_or_zone` | 触发与订单价格/区域分开记录 |
| `structural_stop_or_zone` / `stop_zone` | `structural_stop`、`structural_invalidation` | 研究阶段可写区域；冻结回放前才收敛为数值止损 |
| `first_magnet` | `first_independent_obstacle` | 仅保留为历史别名，不能跳过最近独立障碍 |

几何顺序固定为：结构失效/止损 → 首障碍 → 入场前空间 → 粗略 R/R → 目标层。`observation_only` 用于关键证据仍不完整或只保留形态观察；`valid_no_trade` 用于形态、方向和几何已可复核但已知硬闸门否决交易。两者都不建立订单，不能互换。

### 日线主标签白名单与状态迁移

`contract_scope: daily_candidate` 时，`primary_pattern` 只允许 `ABC_CONT` 或 `BOP`。H1/H2/L1/L2 只能写入 `internal_label`，H3/L3 在日线候选中也只能写入 `internal_label`，其他关系写入 `secondary_context`；`range_edge_three_push` 只是区间边缘位置分支，不是主标签，也不等同于 `H3_L3`。`H1_L1`、`H2_L2`、`H3_L3`、`RFB`、`MTR`、`other` 以及独立主题名称只用于深审/历史兼容记录，不能扩展日线选股主标签。

若事前可见边界被日线强收盘越过、获得跟随并在回踩中守住，统一合同改写为 `primary_pattern: BOP`、`state_transition: breakout_acceptance`；原 pattern/反向 thesis 与旧订单合同失效，必须重建 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间，不能沿用旧 entry/stop/target 或把旧结果并入 BOP。

## 范围边界

- 这些目录是视觉研究和历史复核入口，不是量化扫描器，也不直接连接 Execution Agent。
- `research/` 根目录中的案例正文暂不搬迁；由[`research/研究索引`](../research/README.md)负责导航，目录只负责 pattern 导航和研究合同。
- Measured Move、AB=CD、EMA 和缺口回补是位置/空间因素；META 是位置汇合框架；它们都不单独构成 pattern，META 也不替代独立空间闸门。
- VCP、Final Flag、Opening Reversal、Channel、Inside Bar 与 Triangle 已建立独立研究目录，但都处于 `visual-research / provisional`，不计入核心八个。三推虽然可以成为 MTR 的证据，但在这里作为独立 pattern 单独实现。

## 共同规则

先看背景和左侧，再看形态；先看第一独立障碍，再看 MM；强趋势不等于可以在趋势末端追价。统一背景见 [`docs/common_context.md`](../docs/common_context.md)，覆盖状态见 [`research/abc_pattern_coverage_audit_CN.md`](../research/abc_pattern_coverage_audit_CN.md)。

16 个目录进入 pattern-specific 判断前，都先按[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点/低点、支撑阻力、前高/前低、EMA20/50/200、父级状态和第一独立障碍。对开放趋势 ABC/H-L、需要原趋势压力背景的 MTR 等适用路径核对 A/B 质量；强 A 优先服务 H1/L1，H2/L2 可以承接普通 A 后的第二次有意义尝试。成熟区间边缘三推是例外：A 腿可以普通或偏弱，但必须核对已确认的上沿/下沿、第三推位置、反向证据和空间；独立主题只把 A/B 作为背景对照，不强行添加 ABC/H-L 计数。涉及 H1/H2/L1/L2 时还要确认 Daily EMA20/50 与方向一致；缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`。

## 核心 pattern 交叉审计

八个目录的共存关系、切换条件、状态词汇和共同否决层见[`核心八个 Pattern 交叉一致性审计`](../research/core_pattern_cross_audit_CN.md)。使用时先判父级市场状态，再判结构/计数，最后判状态转换和交易合同；不要因为多个标签同时出现就重复计算优势。

16 个目录的完整入口、独立主题边界和 canonical `primary_pattern`/`internal_label`/`state_transition` 映射见[`Pattern 索引、别名与主次标签边界审计`](../research/pattern_index_alias_boundary_audit_2026-08-29_CN.md)。

16 个目录的两年 Daily 左侧、重要高低点、EMA20/50/200、适用路径的 A/B 质量（强 A→H1/L1 优先；区间边缘三推不要求强 A）、位置和首障碍共同前置证据见[`Pattern 视觉复核前置证据审计`](../research/pattern_visual_preflight_audit_2026-08-29_CN.md)。

共同视觉前置字段的 canonical 名称、批次级与逐标的覆盖边界见[`共同视觉前置字段一致性审计`](../research/common_visual_preflight_field_consistency_audit_2026-08-29_CN.md)。

16 个目录的案例入口、条件/边界/no-trade 文案和 canonical `valid_no_trade` 状态见[`Pattern 案例入口与状态一致性审计`](../research/pattern_case_entry_status_audit_2026-08-29_CN.md)。

16 个目录的 canonical 状态轴、字段命名和 pattern-specific 模板边界见[`Pattern 状态轴、字段与枚举一致性审计`](../research/pattern_state_axis_field_enum_audit_2026-08-29_CN.md)。

16 个 pattern README、8 个基础视觉层与活动视觉复核卡的 canonical 输出继承、局部模板字段和枚举边界见[`Pattern README 与基础视觉框架 canonical 输出覆盖审计`](../research/backtesting/pattern_foundation_canonical_contract_audit_2026-08-29_CN.md)。

订单语义和 R/R 的跨 pattern 规则见[`八个 Pattern 的订单合同与 R/R 审计`](../research/order_contract_cross_pattern_audit_CN.md)。

16 个目录的日线主标签白名单、H/L 内部标签、三推/区间边缘分隔和 BOP 旧合同失效边界见[`Pattern 主标签映射与 BOP 状态迁移审计`](../research/pattern_label_transition_audit_2026-08-29_CN.md)。

16 个入口的逐标的图表范围、两年 Daily 覆盖、周期集合和数据状态边界见[`证据范围与数据状态一致性审计`](../research/evidence_scope_status_boundary_audit_2026-08-29_CN.md)。

MTR 与三推/H3-L3 的边界复核见[`MTR 与三推/H3-L3 视觉边界复核`](../research/mtr_three_push_visual_boundary_audit_2026-08-24_CN.md)：三推是压力观察入口；成熟区间边缘的第三推可以先成为独立反转候选，MTR 仍需要控制权改变和反向二次确认；`mtr_state` 使用 MTR 专用枚举，不替代 `thesis_state`。

三推字段、区间边缘方向和统计隔离的专项复核见[`三推/H3-L3 与区间边缘合同边界审计`](../research/backtesting/three_push_h3_l3_contract_boundary_audit_2026-08-29_CN.md)：新记录统一使用 `primary_pattern`、`internal_label`、`third_push_state`、`range_edge_side` 和 canonical 方向，当前没有冻结 H3/L3 合同，不新增统计分母。

H1/L1 第一次入场的边界复核见[`H1/L1 第一次入场视觉边界复核`](../research/h1_l1_first_entry_visual_boundary_audit_2026-08-24_CN.md)：强 A 和受控 B 只是筛选入口，第一次失败要保留 H2/L2 或 no-trade 分支。

H2/L2 第二次入场的边界复核见[`H2/L2 第二次入场视觉边界复核`](../research/h2_l2_second_entry_visual_boundary_audit_2026-08-24_CN.md)：第二次必须属于同一回调且发生在有意义位置；区间、重建和低周期合同另行处理。

ABC 趋势延续的边界复核见[`ABC 趋势延续视觉边界复核`](../research/abc_continuation_visual_boundary_audit_2026-08-24_CN.md)：A/B/C、嵌套腿、区间摆动、B 失控和 MM/首障碍必须分栏审计。

ABC、H1/L1 与 H2/L2 的分层历史结果审计见[`ABC + H/L 分层历史结果审计`](../research/abc_hl_stratified_outcome_audit_2026-08-24_CN.md)：先按母结构、lineage、合同和首障碍分层，再讨论胜率与 realized R；当前仍为 pilot、`not-statistical`。

BOP / 突破接受与突破回踩的边界复核见[`BOP 视觉边界复核`](../research/bop_visual_boundary_audit_2026-08-24_CN.md)：突破前合同在接受后必须废弃或重建，影线、gap-and-go、真实回踩与失败突破分开。

失败突破与高潮反转的边界复核见[`失败突破与高潮反转视觉边界复核`](../research/failed_breakout_climax_visual_boundary_audit_2026-08-24_CN.md)：测试、失败候选、小反转/区间、MTR 和 BOP 接受必须按状态切换分开。

交易区间边缘二次入场边界复核见[`交易区间边缘二次入场视觉边界复核`](../research/range_edge_second_entry_visual_boundary_audit_2026-08-24_CN.md)：边缘计数、中部观望、second-leg trap 与 limit/stop 合同分开。

Final Flag 最终旗形边界复核见[`Final Flag 最终旗形视觉边界复核`](../research/final_flag_visual_boundary_audit_2026-08-24_CN.md)：趋势末端压缩、普通旗形、区间过渡、BOP 接受和反向二次确认分开。

Opening Reversal 开盘反转边界复核见[`Opening Reversal 开盘反转视觉边界复核`](../research/opening_reversal_visual_boundary_audit_2026-08-24_CN.md)：开盘第一波失败、开盘接受、普通 H/L、事件缺口与实际订单重订分开。

Channel 通道边界复核见[`Channel 通道视觉边界复核`](../research/channel_visual_boundary_audit_2026-08-24_CN.md)：两点连线、紧/宽通道、边界扩张、区间过渡、BOP 接受和订单合同分开。

Inside Bar / 两根 K 线边界复核见[`Inside Bar / 两根 K 线反转视觉边界复核`](../research/inside_bar_two_bar_reversal_visual_boundary_audit_2026-08-24_CN.md)：严格整根范围、二内包/IOI、两根反转、H/L 序列、区间噪音和跳空重订分开。

Triangle / 三角形边界复核见[`Triangle / 三角形视觉边界复核`](../research/triangle_expanding_range_visual_boundary_audit_2026-08-24_CN.md)：收缩、扩张、区间内区间、BOP 接受、失败突破和两点连线误判分开。

Double Top / Double Bottom 双顶双底边界复核见[`双顶双底视觉边界复核`](../research/double_top_bottom_visual_boundary_audit_2026-08-24_CN.md)：两次有分离测试、区间边缘、普通延续、Final Flag、MTR、BOP 否定和首障碍分开。

Head-and-Shoulders / Rounded 头肩与圆顶圆底边界复核见[`头肩与圆顶圆底视觉边界复核`](../research/head_shoulders_rounded_visual_boundary_audit_2026-08-24_CN.md)：复杂双顶/底、真实颈线、圆形状态转移、普通旗形和 BOP 否定分开。

跨 Pattern 视觉优先级与冲突复核见[`Cross-Pattern 视觉优先级与冲突消解审计`](../research/cross_pattern_visual_priority_audit_2026-08-24_CN.md)：先判父级和位置，再选主标签、次标签、状态切换和 `valid_no_trade`。

完整图表统一复核卡见[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)，工作流边界演练见[`完整图表视觉复核工作流边界审计`](../research/visual_review_workflow_boundary_audit_2026-08-24_CN.md)：快筛先判断像不像，深审再处理订单、止损、首障碍和粗略 R/R。

实际图像识别冒烟结果见[`PA 图表视觉识别冒烟验收`](../research/visual_recognition_smoke_test_2026-08-24_CN.md)：公开图像只用于验证能否先识别 pattern 和边界，最终盲测验收仍待未标注、周期清晰的图表集。

第二轮未标注多标的、两年 Daily 背景、EMA20/50/200 与多周期图像资产已并入同一份[`PA 图表视觉识别验收记录`](../research/visual_recognition_smoke_test_2026-08-24_CN.md)，资产入口见[`第二轮多标的多周期视觉资产`](../research/assets/visual_recognition/2026-08-24/round2_multisymbol/README.md)；状态仍为 `acceptance-pending`，干净 BOP/MTR 正例保持 `no-new-positive`。

H1/H2、L1/L2 的局部未标注计数复核见[`H1/H2 与 L1/L2 局部盲测资产`](../research/assets/visual_recognition/2026-08-24/round3_hl_drills/README.md)及同一份[`PA 图表视觉识别验收记录`](../research/visual_recognition_smoke_test_2026-08-24_CN.md)的第三轮记录；计数仍须满足同一主周期和同一回调 lineage，未升级为固定规则。

H/L 与三推共用的第二阶段 lineage、两年左侧背景、重要高低点、支撑阻力和 EMA20/50/200 前置复核见[`H/L lineage 与三推状态视觉边界复核`](../research/h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)；先登记母腿和失败/不足，再决定计数或状态，当前仍为研究层 `count-pending`。

空头 L1/L2-like 的 Daily/4H-like/60m 对照见[`MAR 空头 L1/L2-like 视觉资产`](../research/assets/visual_recognition/2026-08-24/round3_l1_l2_mar/README.md)；该历史窗口的 15m 数据不可得，报告保留 `15m-evidence-missing`，不把缺失证据补写成确认。

Round4 历史图表视觉练习见[`Round4 历史图表视觉练习与 H/L/ABC 复核`](../research/visual_recognition_round4_historical_practice_2026-08-24_CN.md)及其[`无标签图表资产`](../research/assets/visual_recognition/2026-08-24/round4_historical_practice/README.md)；本轮增加 42 标的筛选和 7 个 targeted 多周期复核，但 cohort3 Daily 左侧不足两年，所有新增计数保持 `pending`。

Round5 两年 Daily 左侧背景练习见[`Round5 两年 Daily 左侧背景与 ABC/H-L/三推视觉练习`](../research/visual_recognition_round5_two_year_daily_2026-08-24_CN.md)及其[`无标签图表资产`](../research/assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md)；本轮 4 个标的、8 个 targeted 案例完成两年背景字段，但严格计数和可比正样本仍为 `0`。

历史视觉证据与 canonical 字段边界的统一审计见[`历史视觉证据与 canonical 边界审计`](../research/backtesting/visual_evidence_canonical_boundary_audit_2026-08-29_CN.md)：provisional lineage 映射为 `pending`，区间重复使用 `range_repeat_test`，视觉首障碍不自动成为冻结空间；逐案闭合才填写主标签与 lineage ID。

视觉识别冒烟、快筛协议与 Round2/Round3 资产的字段映射和配对 provenance 见[`视觉识别冒烟、快筛协议与 Round2/Round3 资产 canonical 边界审计`](../research/backtesting/visual_recognition_canonical_boundary_audit_2026-08-29_CN.md)：历史展示标签不冒充 `primary_pattern`/`internal_label`，快筛不冻结 `lineage_id`，局部图不替代两年 Daily，`no-new-positive` 保持不变。

Round4、Round5 与 TSLA 视觉资产的 provenance、两年 Daily、重要高低点、EMA 和多周期职责见[`Round4、Round5 与 TSLA 视觉资产 canonical 边界审计`](../research/backtesting/visual_asset_canonical_boundary_audit_2026-08-29_CN.md)：短窗口、未标注资产和配对复核均不自动冻结 pattern、`lineage_id`、订单或统计结果。

全部 11 个视觉资产目录的 README provenance 和 105 张 PNG 的配对/统计边界见[`全部视觉资产 README canonical provenance 覆盖审计`](../research/backtesting/visual_asset_provenance_coverage_audit_2026-08-29_CN.md)：README 聚合头不冻结 `primary_pattern`/`lineage_id`，合同资产仍按逐行合同读取，窗口数量不等于样本数量。

六个活动视觉框架、视觉历史报告、配对复核记录与 canonical authority schema 的字段对齐见[`视觉历史报告与 canonical authority schema 对齐审计`](../research/backtesting/visual_authority_schema_alignment_audit_2026-08-29_CN.md)：当前模板使用统一状态轴，历史案例别名只保留为事实/显示语义，不新增样本或结果。

其余视觉框架、订单分支协议和 pattern-specific 案例入口的合同边界见[`remaining visual frameworks 合同边界审计`](../research/backtesting/remaining_visual_framework_contract_audit_2026-08-29_CN.md)：补齐证据头、`parent_state`、方向/主次标签、状态转换、订单/空间字段和历史别名边界，不新增样本或结果。

聚合 Pattern 案例矩阵、Strategy inventory 与历史案例入口的逐案合同边界见[`Pattern 案例矩阵、策略入口与历史别名合同审计`](../research/backtesting/pattern_case_matrix_strategy_entry_contract_audit_2026-08-29_CN.md)：矩阵字段只作导航，历史显示别名不覆盖 canonical 主次标签、状态、订单或空间。
矩阵之外的历史案例入口合同见[`历史案例入口合同盘点审计`](../research/backtesting/historical_case_entry_inventory_contract_audit_2026-08-29_CN.md)：历史显示别名只作导航，不能替代逐案 evidence、状态、订单、空间或结果边界。
顶层 research 条件性历史入口的状态和结果边界见[`顶层 research 历史正向条件入口边界审计`](../research/backtesting/top_level_research_entry_boundary_audit_2026-08-30_CN.md)：`research_positive_conditional` 不会自动变成 canonical 主标签或授权。
报告、活动模板、视觉资产和历史 inventory 的 canonical 入口交叉覆盖见[`PA Research canonical 入口交叉覆盖审计`](../research/backtesting/canonical_entry_cross_coverage_audit_2026-08-30_CN.md)：资产 manifest 不等于逐图候选入口。
- canonical schema、活动模板、validator 与 engine 的字段/枚举/版本边界见[`schema / engine / validator 漂移审计`](../research/backtesting/schema_engine_validator_drift_audit_2026-08-30_CN.md)：研究字段不能直接替代冻结回放输入。

优先 Pattern 的代表性视觉候选与正/反例矩阵见[`优先 Pattern 代表性视觉候选矩阵`](../research/priority_pattern_visual_candidate_matrix_2026-08-24_CN.md)：每个案例只保留一个主标签，次标签、状态切换、订单合同和首障碍单独记录。

BOP 真实多日回踩的专项审计见[`BOP 真实多日回踩候选审计`](../research/bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)：当前区分了状态切换、同日回测、缺口重订和真正缺失的多日回踩正例。

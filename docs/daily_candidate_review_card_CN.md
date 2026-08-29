# PA Research 每日候选批次与图表审查卡 v0.1

日期：2026-08-28<br>
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

本卡是 PA Research 的**批次记录和人工审查模板**。它把候选池覆盖、数据来源、两年 Daily 左侧、强阻力、A/B/H-L、事件、流动性和空间证据放在同一张卡上，避免把“发现页上的股票”误称为“已经通过规则的候选”。

本卡不新增选股阈值，不自动识别 pattern，不创建量化扫描器，不连接 Execution Agent，也不改变[`PA Research 日线选股规则 v0.1`](pa_research_daily_selection_rules_v0_1_CN.md)的硬闸门。它只要求把已有规则执行时的证据记录完整。

## 一、批次级证据：先说明看了多大的池子

每一批候选先填写下面的字段。`discovery_only` 只能说明发现来源，不能被写成完整市场筛选结果。

```text
candidate_batch_id:
review_date:
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:

universe_scope: US_common_stock_only / mixed / unknown
asset_type_filter: common_stock / includes_etf / unknown
market_cap_rule: $3B-$100B
liquidity_rule: 20d_avg_dollar_volume >= $50M
discovery_source:
discovery_filters_applied:
universe_coverage: complete / partial / discovery_only / unknown
coverage_limitation:

long_pool_seen:
short_pool_seen:
directional_coverage: long / short / both / unknown
long_pool_reviewed:
short_pool_reviewed:
event_status_coverage: complete / partial / unknown
two_year_chart_coverage: complete / partial / unknown
deep_review_limit:
```

### 批次级硬要求

1. 市值、20日平均成交额和事件状态必须记录各自的来源及截至时间；不能用搜索页面的默认筛选名称代替实际数值。
2. `universe_coverage: discovery_only` 或 `unknown` 时，输出只能称为“发现池/已审查子集”，不能称为“市场上全部合格标的”。
3. 多头和空头要分别记录。某一方向没有合格案例是有效结果，不能为了凑数把另一方向的标的补进去。
4. 发现池可以高召回；最终候选仍必须逐标的通过 PA Research 日线规则和人工图表审查。
5. 同一批次内必须统一数据截止日、时区和已完成 K 线口径。不同日期的数据不能混成“今天的机会”。

## 二、逐标的证据头

```text
symbol:
direction: long / short / no_valid_direction
asset_type: common_stock / ETF / index / unknown
review_date:
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state:
completed_bar_as_of:

market_cap_usd:
market_cap_as_of:
market_cap_source:
avg_20d_dollar_volume_usd:
liquidity_as_of:
liquidity_source:
market_cap_gate: pass / fail / pending
liquidity_gate: pass / fail / pending

event_context: none / earnings / macro / gap / other / unknown
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
event_source_as_of:
earnings_next_three_sessions: yes / no / unknown
event_gate: pass / exclude / pending
sector_reference:
sector_state: aligned / mixed / counter / unknown
market_reference:
market_state: aligned / mixed / counter / unknown
```

缺失数据必须写 `unknown` 或 `pending`。不能把没有查到财报、成交额或板块证据写成 `none` 或 `pass`。

## 三、两年 Daily 左侧审查

每个候选必须先看至少两年 Daily 左侧，再看近六个月局部图。若图表不足两年，保留为 `partial-context / pending`，不能用局部走势补写左侧结构。

```text
daily_context_window: >=2y / <2y / unavailable
chart_scope: full / partial / unavailable
timeframes_seen:
major_high_low_review: complete / partial / unavailable
major_highs:
major_lows:
support_zones:
resistance_zones:
role_reversal_zones:
leftmost_relevant_obstacle:

daily_ema20_slope: up / flat / down / unknown
daily_ema50_slope: up / flat / down / unknown
ema20_50_200_review: complete / partial / unavailable
daily_ema20_50_200:
daily_ema200_context:
price_vs_ema20_50_200:
h_l_ema_slope_gate: long_pass / short_pass / fail_flat_or_opposite / pending / not_applicable
h_l_pullback_location:

parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
left_context_summary:
```

`two_year_chart_coverage` 是批次级覆盖摘要；逐标的必须以 `daily_context_window`、`chart_scope`、`major_high_low_review` 和 `ema20_50_200_review` 记录实际证据。`major_highs`/`major_lows` 是 canonical `major_highs_lows` 的细分，`price_vs_ema20_50_200` 是 `daily_ema20_50_200` 的补充描述，不能替代审查完整度字段。

左侧高点/低点至少要记录日期或价格区域，并说明它是单次极值、反复测试、区间边界还是角色转换。多个相近价格的阻力要合并成一个阻力簇，不能用同一位置重复计算空间。

## 四、A/B/计数与位置

```text
local_A_origin:
local_A_end:
a_leg_quality: strong / ordinary / unclear / event_driven
b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear
special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none
b_leg_location:
lineage_status: same_lineage / reset / unclear / pending
setup_count_bar:
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
count_basis:
count_reset_reason:
primary_pattern: ABC_CONT / BOP
secondary_context:
```

本卡是当前日线候选记录模板，顶层主标签只使用 `ABC_CONT` 或 `BOP`；H1/H2/L1/L2/H3/L3 放在 `internal_label`，其他结构关系放在 `secondary_context`。历史独立 H/L、三推或其他模式记录遵循统一输出合同的历史/兼容口径，不应反过来扩展当前日线选股主标签。

强 A 只是优先级条件，不是入场信号。通常应看到约 3–4 根连续、实体较饱满、收盘靠方向极值、重叠较少的方向 K 线；缺口是加分项，不是必要条件，也不能让事件跳空替代普通 A 的证据。

B 段要单独判断反向压力是否收缩。大实体反向推进、越过关键极值或变成宽幅双向区间时，不能机械称为“受控 B”。如果出现新母腿或越过原回调关键极值，必须说明计数是否重置。

对 H1/H2/L1/L2，Daily EMA20 和 EMA50 的方向闸门与回调位置必须同时记录。均线走平、反向或不可见时，最多保留 `pattern_like / observation_only`；EMA 触碰本身不构成入场。

## 五、META 与空间：先写几何，再写结论

```text
meta_confluence: present / absent / unknown
meta_zone:
meta_components:

signal_bar:
confirmation_bar:
new_trigger:
order_price_or_zone:
trigger_status: not_triggered / pending / triggered / not_applicable
structural_stop:
structural_invalidation:
risk_per_share_or_unit:
first_independent_obstacle:
first_obstacle_zone:
distance_to_first_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
rough_R_R:
target_layers:
main_uncertainty_or_exclusion:
```

`META` 至少需要两个独立结构来源在同一价格区域汇聚，例如 EMA20、前期支撑和角色转换区；它只能增强合格候选的优先级，不能替代方向、触发、结构止损或第一障碍。

本卡的 `new_trigger`、`order_price_or_zone`、`structural_stop`、`first_independent_obstacle`、`pre_entry_space_R` 和 `space_status` 与统一输出合同同名；`first_obstacle_zone`、`distance_to_first_obstacle` 和 `risk_per_share_or_unit` 是日线审查阶段的补充字段。研究阶段允许 `structural_stop` 或障碍只写区域，但冻结回放前必须收敛为数值合同。

如果还没有可执行触发价，必须写 `pending`，不能用审查时的当前价格冒充历史入场价。若首障碍和几何已经可复核，但空间不足或只能通过缩窄结构止损制造 `1R`，记录 `valid_no_trade`；若关键图表、事件、触发或空间证据尚不完整，记录 `observation_only` 或 `pending`。两者都不建立订单，不能互换。

## 六、最终状态分轴

```text
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
failure_or_no_trade_reason:
main_uncertainty_or_exclusion:
```

本卡不再使用含义不明确的 `final_state` 别名；`research_state`、`trade_state` 和 `gate_result` 必须各自保留，批次汇总另用下方的分类列表表达。

建议按以下顺序输出，防止把形态和交易混成一个结论：

1. `pattern_like`：图形值得研究；
2. `research_candidate`：背景、位置和结构基本通过；
3. `conditional`：等待预先定义的触发或回踩确认；
4. `valid_no_trade`：形态可能成立，但空间、事件、数据或订单合同不适合；
5. `observation_only`：保留学习价值，但不作为当前候选。

批次最后分开列出：

```text
pattern_candidates:
conditional_candidates:
immediate_entry_candidates:
valid_no_trade_cases:
observation_only_cases:
event_or_gap_cases:
```

`immediate_entry_candidates` 可以为零。零个立即入场不表示筛选失败；在候选池覆盖不完整时，也不能反过来断言整个市场没有机会。

## 七、人工复核停止条件

满足以下任一条件，可以结束该标的深审并记录原因：

- 两年左侧背景或关键高低点不可见；
- 这是区间中部，不是趋势或成熟区间边缘；
- A 腿没有方向性，或 B 已经失控/区间化；
- 左侧主要阻力/支撑已经堵住首个独立障碍；
- 财报或重大事件改变了原始结构；
- 触发、结构止损或第一障碍无法在事前明确写出；
- 当前资料只能证明发现池，不能证明市值、流动性或事件闸门。

停止后仍保留案例和否决理由，不为了填满 3–5 个名额继续解释。

## 八、范围边界

- 本卡服务 PA Research 的人工候选研究和历史审计；
- 不从图表自动生成股票池，不替代人工看图；
- 不把 `pattern_like`、描述性胜率或单个成功案例写成已验证规则；
- 不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent；
- 当前整体研究结论仍由相关审计文件维护，若样本不足应保留 `no-new-positive` 和 `win_rate: not-computable`。

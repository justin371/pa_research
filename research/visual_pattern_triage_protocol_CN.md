# PA Pattern 视觉筛选协议 v0.3

日期：2026-08-23；发现池召回与排序修订：2026-09-01
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

日线候选的范围、流动性、两年背景、财报窗口和 ABC/BOP 主标签先遵循 [`PA Research 日线选股规则 v0.1`](../docs/pa_research_daily_selection_rules_v0_1_CN.md)；本协议负责通过前置闸门后的视觉快筛与深审，不把 4H/1H/15m 倒灌成日线选股证据。

当快筛同时像 H/L、BOP、三推或普通 ABC continuation 时，先按[`形态边界视觉决策卡`](../docs/morphology_boundary_decision_card_CN.md)判断状态迁移、区间/第三推、B 腿和 lineage，再冻结候选 family 与 H/L-like 计数。

输出字段统一遵循[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。快筛可以保留 `pending` 或 `unknown`，但不能省略方向字段或把快筛状态当作交易授权。

## 这份协议解决什么问题

PA Research 的第一阶段任务，是让助手从完整图表里筛出“看起来像”的 Price Action pattern。它不是扫描器，也不是胜率模型。第一轮不需要精确价格、固定阈值、完整 15m 触发或精确 R/R；这些内容只在候选值得深入时再补。

核心顺序：

```text
完整图表背景
    → 视觉上是否像某个 pattern
    → 记录候选与不确定点
    → 只挑少量候选优化订单/止损/目标
    → 形成可复核研究样本
```

## 当前默认执行模式：轻量视觉优先

为避免一个 ABC 候选被过早做成完整交易审计，后续新案例默认分两档处理：

1. **快筛档**：先看完整图表，只写背景、方向性 A、B 的压力变化、当前位置、像不像，以及一句不确定点。价格和日期可以用区域表示；不先打开低周期、不先查事件、不先算精确 MM 或 R/R。
2. **深审档**：只有快筛结论为 `pattern_like`，或这个边界样本对规则有特殊学习价值，才补信号 K、订单分支、结构止损、第一独立障碍和粗略 R/R。

如果 A 腿不清楚、B 已经区间化，或第一障碍肉眼就贴近触发位，快筛到此为止并记录原因；不为了“完成一个案例”继续填表。每批先挑少量最有代表性的正例和反例，避免用大量相似图形重复证明同一件事。

## 1. 第一轮：只做视觉筛选

第一轮要回答的是“像不像”，不是“能不能下单”。至少记录：

```text
symbol:
review_window:
contract_scope: stage_1_fast_screen
timeframes_seen:
data_status: historical / delayed / live_confirmed / incomplete
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
direction: long / short / no_valid_direction
pattern_candidate: ABC-CONT / H1-H2-H3 / L1-L2-L3 / range-edge / MTR / other
parent_leg:
local_A_B_C_or_attempts:
visual_reason:
main_uncertainty:
stage_1_status: pattern_like / boundary / not_this_pattern / pending
coverage_bucket:
shortlist_rank: positive_integer / not_ranked
rank_basis:
selection_disposition: deep_reviewed / deferred_capacity / wait_for_structure / rejected_gate / duplicate_lineage / event_boundary / insufficient_evidence
disposition_reason:
```

### 第一阶段字段与 canonical 合同映射

上面的 `pattern_candidate`、`stage_1_status`、`parent_leg` 和
`local_A_B_C_or_attempts` 是快筛的工作字段，不是新的主标签或交易状态。每个
标的/案例在快筛记录中还必须能回溯到下列 canonical 轴；缺失证据写
`pending`/`unknown`，不能用“like”或后续走势补齐：

```text
contract_scope: stage_1_fast_screen / historical_context_only
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
a_leg_quality: strong / ordinary / unclear / event_driven
b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear
b_leg_location:
special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none
h_l_pullback_location:
meta_confluence: present / absent / unknown
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
direction: long / short / no_valid_direction
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
secondary_context:
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

映射规则固定如下：`pattern_candidate` 只表示视觉候选；只有进入完整且已闭合的
研究合同后，才把它映射为 `primary_pattern`。`H1/H2/L1/L2/H3/L3` 只能进入
`internal_label`，三推方向进入 `attempt_direction`，而 `direction` 仍表示当前
研究合同方向。`attempt_or_count` 不能替代 `lineage_status`；同一 lineage 未被
证明时，计数保留 `pending`。`stage_1_status: pattern_like / boundary /
not_this_pattern / pending` 分别只可作为视觉阶段别名，不能直接写成交易授权；
通常映射为 `research_state: pattern_like / observation_only / valid_no_trade /
pending`，但具体状态仍须由证据决定。`directional_bias` 不能覆盖
`direction: no_valid_direction`。

### 快筛与完整闭合记录的硬边界

`contract_scope: stage_1_fast_screen` 只产生候选和显示层信息：
`pattern_candidate`、`stage_1_status`、背景、A/B 质量、位置和不确定项可以先记录，
但该阶段不实例化 active `primary_pattern`、`internal_label` 或 `lineage_id`，也不产生
订单、授权或胜率结论。canonical 映射块列出的是可能的轴，不代表快筛记录已经完成这些轴。

“完整且已闭合的研究记录”是逐案、逐截断时点的入场前证据封口：证据头、`direction`、
`primary_pattern`、`internal_label`、`lineage_status` 都必须有明确值或明确的
`pending`/`unknown`；如果记录声称某个父级/尝试依赖，必须同时有对应 `lineage_id`。
闭合不等于知道结果、实际成交或交易授权；未解决的记录仍只能是观察/未冻结状态。只有
独立冻结合同另行补齐数值触发、止损、首障碍和订单分支后，才可能进入回放准备。

`major_high_low_review`、`ema20_50_200_review` 和 `daily_context_window` 是证据
provenance，不是“图上出现一条线”的同义词。若图像没有两年 Daily 左侧、重要
高低点或 EMA20/50/200 复核，就保留对应缺失状态，不能仅凭局部图冻结 H/L、三推、
BOP 或 MTR。

### 发现池召回与深审交接

快筛的职责是保留发现和不确定性，深审的职责才是收紧资格。后续批次统一执行：

1. 发现池中的每个 symbol/window 都保留 `coverage_bucket`、`stage_1_status` 和 `selection_disposition`；不能只留下最终合同或漂亮正例。
2. `shortlist_rank` 只决定有限深审容量的先后，不改变硬闸门；排名采用事前定性比较，不建立复合分数或自动 pattern 评分。
3. 强 A 但尚无受控 B 的项目使用 `wait_for_structure`；事件或跳空主导的强 A 使用 `event_boundary`。两类都可以保留观察，但不能混入普通 H/L 统计。
4. 因容量没有深审的合格外形使用 `deferred_capacity`；不能写成 `rejected_gate`，否则无法判断是召回失败还是规则否决。
5. 同一 lineage 的重复窗口仍保留发现记录并标为 `duplicate_lineage`，只从独立回放分母排除；不能从召回账本中删除。
6. 批次结论若声称“没有 H2/L2”“没有多头”或“找不到好形态”，必须同时给出对应方向 × 形态覆盖桶的发现数、快筛数和深审数。发现池覆盖为 `partial/discovery_only` 时，只能说明已审查子集。

逐批字段和汇总模板见[`每日候选批次与图表审查卡`](../docs/daily_candidate_review_card_CN.md)。这些字段是流程审计层，不改变 canonical `primary_pattern/internal_label`，也不授权订单。

### 第一轮可以使用的证据

- 左侧是否有清楚的趋势、交易区间、过渡或高潮背景；
- 是否能看见一条方向性 A 腿，随后出现回调或反向尝试；
- B 是趋势回调，还是区间中部的双向摆动；
- C 或 H/L 尝试是否发生在有意义的支撑/阻力、EMA、缺口、通道边界附近；
- 价格行为是否有明显的买压/卖压变化，例如方向性实体、重叠、尾巴和跟随；
- 是否存在母腿与局部腿嵌套，不能因为窗口短就强行把局部腿当成独立 ABC。

### 计数与区间保护闸门

第一轮不冻结计数，但要先做两个保护判断：

1. **新极值优先触发计数重置。** 第一次 H/L 尝试之后，如果反向回调越过前一 B 的关键极值，或形成了明显的新局部母腿，默认先把后续尝试标成“计数重置后的新 H1/L1-like”。只有在明确采用嵌套计数时，才保留 H2/L2 解释；不能因为第二次方向相同就事后自动叫 H2/L2。
2. **宽幅重叠区间不当作开放趋势回调。** A 之后如果 B 变成多根 K 线的宽幅重叠、来回穿越均线、缺少清楚的反向压力衰减，就先标为 `trading_range / range-transition boundary`。后续在区间中部出现的 H/L 不能直接继承开放趋势 ABC 的计数；优先看区间上沿、下沿和二次入场逻辑。

这两个闸门只用于避免贴错标签，不是精确的量化阈值。视觉上仍像时可以保留候选，但必须把“计数重置”或“区间逻辑”写进不确定项。

### 第一轮不要求的内容

- 不要求精确到某个固定百分比；
- 不要求先确定唯一的 A 腿锚点；有歧义时可保留早锚点/晚锚点；
- 不要求先算出精确的 measured move、AB=CD 或 1R/2R；
- 不要求先判断最终是否盈利；
- 不要求先把每个 H1/H2/H3 或 L1/L2/L3 计数冻结；计数不清可以写 `unclear`；
- 不因为价格碰到 EMA 就单独创建 pattern；
- 不把后面的大涨/大跌倒灌成前面“本来就明显”。

## 2. 第一轮的三类输出

### `pattern_like`

图形的背景、方向腿和回调/尝试已经足以值得继续看，但订单、首个障碍或计数还没有审计。这个状态是正常的第一阶段成果，不代表入场。

### `boundary`

局部形状有些像，但存在会改变解释的边界，例如：

- 父级可能是交易区间而不是趋势；
- A 腿普通、过宽或不够方向性；
- B 反向压力扩张，可能已经形成新趋势；
- H3/L3 与三推楔形、区间二次测试混在一起；
- 事件跳空改变了原来的价格行为；
- 母腿和局部腿有多个合理尺度。

边界样本要保留。它们帮助助手学会“不确定时如何说”，不能为了得到正例而删除。

### `not_this_pattern`

图形主要是区间中部摆动、没有方向性 A 腿、计数已被新结构重置，或它明显属于另一个逻辑。此时不强行贴 ABC/H1/H2 标签；如果另一个 pattern 更合适，可另建候选。

## 3. 第二轮：只优化值得深入的候选

当第一轮标为 `pattern_like`，或者边界样本对某个规则特别有学习价值时，才进入第二轮：

```text
contract_scope: deep_review / historical_context_only
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
direction: long / short / no_valid_direction
primary_pattern: ABC_CONT / BOP / RFB / MTR / other
secondary_context:
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
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
event_context: raw pre-entry event note (examples: none / earnings / macro / gap / other / unknown; dated/compound qualifiers allowed)
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
sector_reference:
sector_state: aligned / mixed / counter / unknown
research_state: research_candidate / valid_no_trade / research_positive_conditional / observation_only / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
```

第二轮字段仍是研究记录，不是当前回放 CSV 的直接输入。`rough_space` 和
`stage_2_status` 是历史工作别名；其他历史工作字段 `trigger_zone`、
`structural_stop_zone`、`measured_move_or_AB_CD`、`event_filter` 和 `sector_or_market_context` 只按别名读取，分别映射到
`order_price_or_zone`、`structural_stop`、`rough_space_to_first_obstacle_R`、
`rough_R_R`、事件字段和板块字段；`stage_2_status` 映射到
`research_state`。新记录优先写 canonical 字段。`stop_limit` 和
`observation_only` 可以保留其独立语义；若要回放，必须先冻结为当前 engine
`0.3.9` 支持的三种 `order_branch`，不能静默转换订单合同。`gap_policy` 必须在
入场前冻结，不能由回放结果倒填。

第二轮仍然是人工研究，不是自动下单授权。第一障碍优先于 MM；结构止损不能为了改善 R/R 而任意缩窄。窄低周期止损和宽日线止损代表不同交易假设，不能混成一个结论。

## 4. 视觉筛选的统一判断顺序

### 多头 ABC / H1-H2-H3

1. 左侧是不是开放上涨趋势、趋势恢复，还是区间/过渡；
2. A 腿是否有方向性；强 A 只提高先看 H1 的优先级，普通 A 通常先观察 H2；
3. B 中卖压是否受控，后段是否在支撑或均线附近收缩；
4. 当前是第一次、第二次还是第三次有意义的多头尝试；
5. 第三次尝试不自动等于三推楔形反转，可能仍是延续；
6. 候选值得深入后，再看信号 K、订单、止损和第一阻力。

### 空头 ABC / L1-L2-L3

1. 左侧是不是开放下跌趋势、趋势恢复，还是区间/过渡；
2. A 腿是否有方向性；优先找连续阴线、收盘靠低位、重叠较少的清楚下跌；
3. B 中买压是否逐渐减弱，是否被前支撑转阻力、均线或主要高点压回；
4. 当前是第一次、第二次还是第三次有意义的空头尝试；
5. 第三次尝试不自动等于三推楔形反转，强度扩张时更可能是延续或高潮风险；
6. 候选值得深入后，再看信号 K、订单、止损和第一支撑。

## 5. 与现有研究文件的关系

- [`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)：逐图完整审计卡；
- [`ABC 视觉研究阶段性综合`](abc_visual_synthesis_v0_2_CN.md)：跨案例共性与边界；
- [`ABC 决策矩阵`](abc_decision_matrix_CN.md)：案例比较；
- [`Pattern inventory`](../strategy/pattern_inventory_candidates.md)：候选目录。

本协议只规定“先筛像不像，再决定是否优化”的入口，不替代上述文件里的订单、止损、首障碍和事件过滤规则。

## 6. 定性视觉语言：先描述质量，不先打分

为了让助手真正读懂图，而不是把图变成量化扫描器，第一轮统一使用定性标签。标签可以随着完整图表改变，但不要把它们强行换算成分数或固定百分比。

下列带连字符的写法只保留为历史显示别名，不能写入 canonical 字段：

| 历史显示词 | canonical 读取 |
| --- | --- |
| `strong-looking-A` / `ordinary-directional-A` / `unclear-A` | `a_leg_quality: strong / ordinary / unclear` |
| `controlled-B` / `deep-but-late-controlled-B` / `uncontrolled-B` | `b_leg_class: controlled / deep_but_late_controlled / uncontrolled` |
| `H2-like` / `L1/L2-like` | `internal_label: pending`，并在说明中保留候选方向 |
| `same-lineage provisional` / `lineage provisional` | `lineage_status: pending` |
| `three-push candidate` | `third_push_state: unclear`，除非已有可分流证据 |
| `rough_space` | `space_status`；未冻结触发/止损时通常为 `unknown` |

这些映射只收紧字段含义，不改变历史案例的原始描述或结果；`research_state`、
`trade_state` 和 `gate_result` 仍必须分别记录，不能把 `pattern_like` 当成交易许可。

### A 腿质量

- `strong-looking-A`：方向性推进清楚，连续性较好，收盘多靠近运动方向极值，重叠相对少；可以有少量反向 K 或缺口，不要求每根 K 都很大。
- `ordinary-directional-A`：方向和高低点推进能看见，但重叠较多或推进不够干脆；可以保留候选，通常降低优先级。
- `unclear-A`：更像区间摆动、宽通道或事件冲击后的单次反应；先不把它当作标准 ABC 母腿。

### B 腿质量

- `controlled-B`：反向压力没有持续扩张，回调仍守住母腿结构，后段出现收缩、支撑/阻力反应或均线附近重新获得控制。
- `deep-but-late-controlled-B`：回撤幅度较深，但没有收回 A 起点，也没有明显区间化；可以研究，但不与浅 B 混为一类。
- `uncontrolled-B`：反向推进持续增强、穿越关键极值，或变成高重叠宽区间；优先考虑计数重置、区间逻辑或另一个趋势，而不是机械等 C。

### 优质信号 K 的视觉描述

多头信号 K 可以是：

- 干净的阳线实体，收盘靠近高位，且位于关键支撑/EMA20/EMA50 上方或重新收回其上；
- 先向下测试，再以明显下影或小实体收回关键位，并有后续买方跟随。

空头对称地观察：干净阴线、收盘靠近低位，或先上探后以明显上影/小实体跌回关键阻力和均线下方。长尾本身不是信号，必须结合位置和跟随判断。

这些是“优质候选”的描述，不是必要条件。成交量萎缩、50% 回调、缺口回补、EMA 触碰等只作为 META 汇聚中的参考项，不能单独创造信号。

### 视觉升级顺序

```text
像不像
  → A/B 质量是否值得深入
  → 信号 K 是否有位置和跟随
  → 第一支撑/阻力是否给空间
  → 才审计订单、止损、粗略 R/R
```

所以 `research_positive_conditional` 的含义是“多个视觉优势同时存在，值得继续人工研究”，不是“达到某个分数就买入”。

## 7. 当前明确边界

- `pattern_like` 不是胜率，也不是买卖建议；
- `research_positive_conditional` 不是已验证策略；
- 研究阶段可以保留模糊候选，不为了精确而假装确定；
- 形态研究和量化实现分开。只有规则、例外、失败样本和研究证据足够成熟，才考虑移交 Codex Trading；
- Codex Trading 目前仍是只读参考库，PA Research 是本阶段唯一更新的研究库；
- 历史或收盘数据不能描述成实时行情；实时数据若未验证来源，直接标为未知。

# PA Research 日线选股规则 v0.1

日期：2026-08-24；合同修订：2026-08-25；三推与股票池修订：2026-08-26；H/L EMA 方向与 META 修订：2026-08-26；批次证据修订：2026-08-28
文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

这份文件是 PA Research 的日线候选筛选合同。它用于从美股日线图表中筛选少量值得继续研究的 ABC 和 BOP 候选，不是量化扫描器、生产交易规则或下单授权。

统一字段、方向、BOP 状态、订单枚举和状态分轴见[`PA Research 统一输出合同 v0.1`](pa_research_output_schema_v0_1_CN.md)。批次覆盖、数据来源、两年左侧图表和逐标的审查使用[`每日候选批次与图表审查卡`](daily_candidate_review_card_CN.md)。本文件规定日线筛选内容；统一合同和审查卡规定如何记录，三者不能互相省略。

## 0. 本次采纳前修正

在采纳用户初版前，补充或修正以下边界：

- “日成交额 5,000 万美元”冻结为完整日线的 20 日平均，而不是单日事件尖峰；
- “B 段不能过深/过长”改为控制权分层，保留深但后段受控的条件样本；
- 区分突破接受观察、真正 BOP 回踩、失败突破、牛旗 BOP 和事件/缺口 BOP；
- 财报前三个交易 session 的新仓排除扩大到所有候选，不只 BOP；
- 两年 Daily 左侧、重要高低点、支撑阻力和 EMA20/50/200 纳入选股前置证据；
- 4H/1H/15m 从日线选股中移除，只能在候选入选后做独立深审或订单确认；
- 将“足够空间”具体化为到第一独立障碍约至少 1R 的粗略几何闸门；
- 将 H1/H2/L1/L2、H3/L3、普通 BOP 和特殊事件分支明确分层，避免重复统计。
- 将“强 A → 受控 B → H1/L1 优先”和“普通/偏弱 A → 多次回调 → 区间边缘三推”明确为两条不同筛选路径；后者不因 A 腿不够强而自动否决。
- 将成熟交易区间的第三推分成“区间边缘候选”和“区间中部观察”；区间边缘反转候选仍须等待反向确认，不能把第三推本身当作入场。
- 将 H1/H2/L1/L2 的日线 EMA20/50 方向纳入高质量候选闸门：多头两条均向上，空头两条均向下；走平或反向时最多保留为 `pattern_like / observation_only`，不进入普通高质量 H/L。
- 将多区域共振明确记录为 META（Multiple Edge Trading Area）质量增强项：至少两个独立结构来源在同一回调区域汇聚；META 只能提高合格候选的优先级，不能替代方向、信号、空间或结构止损。

## 1. 选股范围与阶段边界

### 1.1 标的范围

- 默认只筛选美国交易所上市的普通股票；股票代码、ETF、指数控制标的不能混在同一候选统计中。
- 当前股票池默认限定为市值约 30 亿至 1,000 亿美元（`$3B–$100B`，按复核时点）；市值、时间戳和来源必须记录。市值低于/高于范围，或市值证据缺失的标的，不进入高质量每日候选。
- ETF 或指数可以作为大盘/板块背景对照，但不能替代个股候选。
- 只使用已经完成的 Daily K 线进行选股；未完成的当日 K 线只能标为观察，不得当作收盘确认。
- 选股阶段不使用 4H、1H 或 15m 参与候选入选、形态计数或日线主标签。
- 如果后续需要低周期确认，必须在选股完成后另立字段和合同；低周期不能创造日线没有的背景、空间或 BOP/ABC 标签。

### 1.2 左侧背景前置条件

默认先看同一标的至少两年的 Daily 左侧背景，再看当前窗口。必须记录：

- 两年窗口内的重要高点、低点及其日期/价格区域；
- 仍有效或反复测试的支撑、阻力、前高、前低和角色转换区；
- Daily EMA20、EMA50、EMA200 的相对位置、斜率和价格所在侧；
- 当前属于开放趋势、成熟区间、区间边缘、过渡还是高潮；
- 个股所属板块和大盘是否支持、混合或明显反向。

对于 H1/H2/L1/L2，高质量方向还必须满足日线 EMA 斜率闸门：多头 H1/H2 要求 EMA20 和 EMA50 都向上；空头 L1/L2 要求 EMA20 和 EMA50 都向下。任一均线走平、反向或斜率不可见时，不能把该 H/L 当作普通高质量候选；斜率不可见记为 `pending`，走平/反向最多记为 `pattern_like / observation_only`。EMA 触碰本身仍不是形态或触发。

两年背景、重要高低点或 EMA20/50/200 不可见时，最多输出 `pattern_like / pending`，不能进入高质量候选列表。EMA 只提供背景和汇合，不单独构成形态或触发。

### 1.3 流动性与数量

- 默认流动性闸门为：截至复核日前最近 20 个完整交易日的平均日成交额不低于 5,000 万美元。
- 日成交额按 `Daily close × Daily volume` 计算，并记录计算截止日和数据来源。
- 单日因财报、新闻或异常波动产生的成交额尖峰，不能代替 20 日平均值。
- 20 日平均成交额缺失或低于门槛的标的，可以作为边界研究样本保存，但不进入高质量每日候选输出。
- 每天最多输出 3–5 只；没有同时通过全部硬闸门的标的时，可以少于 3 只，不能为了凑数放宽标准。

### 1.4 当前重点

每日优先筛选两类主标签：

1. `ABC-CONT`：方向性 A 腿、受控 B 回调、C 恢复原方向；
2. `BOP`：事前可见边界被日线接受，回踩守住后重新离开。

ABC 内部优先使用“强 A → 受控 B → H1/L1 → 必要时 H2/L2”的路径；三推/H3-L3 另设“区间边缘三推”研究分支。后者允许 A 腿普通、重叠较多或经历多次回调，但第三推必须到达已确认的区间上沿/下沿，不能只是区间中部摆动。

ABC、H1/H2、L1/L2、三推 H3/L3 和 BOP 的结果必须分层记录。`ABC + H2` 是母结构与内部尝试的关系，不是两个独立优势；突破接受后主标签必须切换为 BOP，不再按普通 ABC-H1/H2 统计。

## 2. 共同硬闸门

在进入 3–5 只每日候选前，必须完成以下检查：

1. 标的是美国上市普通股票，且数据为完成的 Daily K 线；
2. 两年 Daily 背景、重要高低点、支撑阻力和 EMA20/50/200 可复核；
3. 20 日平均日成交额达到 5,000 万美元；
4. 已核对未来三个交易 session 内的财报和已知重大事件；
5. 父级状态和当前位置清楚，不是成熟区间中部的任意摆动；
6. 结构止损和入场方向可以用当时已知的日线结构说明；
7. 触发位置到第一独立障碍至少有大致 1R 空间；不足约 1R 时为 `valid_no_trade` 或 `observation_only`；
8. 主标签能在当时识别，不能依赖后续涨跌结果倒推；
9. 没有把事件跳空、缺口重订、同日回测或低周期合同混入普通日线样本。

板块和大盘是方向许可与降级信息，不是单独的入场信号。顺板块不能取消首障碍、财报禁做或结构止损；逆板块也不是绝对禁止，但必须有更清楚的位置、结构和空间，否则降级为观察。

## 3. ABC 趋势延续

### 3.1 A 腿：必须有推动力

普通高质量 ABC 的 A 腿应同时表现出大部分以下特征：

- 方向清楚，净推进明显；
- 波幅或方向性有扩张；
- 收盘多数朝推进方向，且有跟随；
- K 线重叠有限，反向压力没有持续接受。

强 A 的优先视觉条件是：多头约 3–4 根连续阳线、空头约 3–4 根连续阴线，实体相对饱满，收盘持续靠近推进方向极值，重叠有限并有跟随；推进之间出现跳空时方向证据更强，但跳空不是必要条件，也不能用财报/异常事件跳空冒充普通 A。

缓慢爬升、重叠严重、频繁双向回撤或宽慢通道，不作为普通强 A。可以保留为 `ordinary-A / boundary`，但不应进入强 A→H1/L1 优先路径。强 A 只改变 H1/L1 的研究优先级，不单独授权交易；A 腿普通时，优先等待 H2/L2，或转入下方的区间边缘三推分支。

### 3.2 B 腿：看控制权变化，不只看深度

B 默认应是受控回调：价格回到前期高点/低点、突破位或明确支撑/阻力，回调 K 线实体相对较小、重叠或影线增加、表现出犹豫，反向压力后段减弱；同时没有形成成熟双向交易区间，也没有完全吞没 A 的结构意义。

深度或持续时间本身不是自动否决条件，必须分层：

- `controlled-B`：浅回调或时间整理，优先研究 H1/L1；
- `deep-but-late-controlled-B`：前段较深或较强，后段明显稳定，降级研究 H2/L2 或条件 ABC；不能与普通 B 混合统计；
- `uncontrolled-B`：反向压力继续扩张、关键结构被接受、A 几乎被吞没，或已经形成新趋势/宽区间；旧 ABC 结束，排除。

B 进入成熟交易区间后，后续区间中部摆动不能继续继承原 ABC 或 H/L 计数；区间中部仍应观察。若多次推进最终到达已确认的区间上沿/下沿，则可以切换到区间边缘三推/失败突破逻辑，而不是因为已经区间化就自动排除。

### 3.3 C 腿：必须恢复方向

C 必须重新朝 A 腿方向推进，并在有意义的位置出现明确的日线继续信号。应记录：

- C 恢复的方向和位置；
- 信号 K、触发位和是否已有日线跟随；
- 前方第一独立阻力/支撑；
- 结构失效点和粗略空间。

只有“看起来像 C”但没有恢复或跟随时，保留为 `pattern_like / pending`，不作为高质量候选。

### 3.4 背景与标签切换

- 普通 ABC 优先要求 Daily 父级开放趋势与 A、C 方向一致。
- 逆趋势、区间边缘或过渡中的 ABC 可以保存为条件案例，但不进入普通优先列表。
- 如果 A/C 到达左侧前高或前低后停顿，H1/L1 不自动入场；首障碍贴近触发时直接 `valid_no_trade`。
- 如果价格有效突破并接受左侧前高/前低，主标签切换为 BOP，旧 ABC-H1/H2 合同结束。

### 3.5 H1/H2/L1/L2 的 EMA 方向、回调位置与 META

- 多头 H1/H2 必须位于开放上涨趋势中，且 Daily EMA20、EMA50 均向上；空头 L1/L2 必须位于开放下跌趋势中，且 Daily EMA20、EMA50 均向下。任一均线走平或向反方向运动时，不进入普通高质量 H/L。
- 多头 B 回调结束/尝试位置，优先靠近向上运行的 EMA20 或 EMA50，或靠近前期低点、支撑、前高突破后的角色转换区；空头 L1/L2 的回调结束/尝试位置，优先靠近向下运行的 EMA20 或 EMA50，或靠近前期高点、阻力、前低跌破后的角色转换区。
- “靠近 EMA”必须同时看到价格在该区域得到支撑/阻力、拒绝或方向性收复；单纯触碰 EMA、远离 EMA 追价或一根 K 线短暂穿越，不能单独成立 H/L。
- 如果 EMA、前高/前低、支撑/阻力、角色转换、缺口边缘或其他独立结构在同一回调区域重合，应在图上标出 META 区域并记录组成来源。META 是质量增强和排序因素，不是自动触发器，也不能覆盖 EMA 斜率闸门、首障碍、事件或结构止损。
- 同一价格簇中的多个标签只算一个 META 位置；不能把同一前高、EMA 和支撑重复计成多个独立优势。

## 4. ABC 内部计数

- H1、H2 是同一 Daily 回调 lineage 内向上的第一次、第二次有意义尝试；L1、L2 对称。
- “有意义”必须结合位置、反向尝试、失败/不足和跟随判断，不能按每一根 K 机械计数。
- 新极值、结构性穿越、父级重建或 B 区间化时，先检查计数是否重置；不能用后续走势把新 H1/L1 追记成旧 H2/L2。
- H3/L3 按三推楔形/第三次压力状态单独识别和统计，不作为普通第三次 H/L 尝试。
- 在证据尚未冻结时使用 `H1-like / H2-like / L1-like / L2-like`，不要把候选标签写成已经确认的交易合同。

### 4.1 区间边缘三推分支（不要求强 A）

这是与强 A→H1/L1 路径并列的独立研究路径：

- A 腿可以普通、偏弱、重叠较多，或经历较多次回调；不能用强 A 标准把它自动排除；
- 必须先确认父级是成熟交易区间，并且第三推到达可由两年以上 Daily 左侧确认的上沿/下沿、前期支撑/阻力或角色转换区；
- 第三推在区间中部时仍是 `range_middle_no_trade / observation_only`，不能因为“数到三”提高等级；
- 第三推在上沿附近可研究空头反转候选，在下沿附近可研究多头反转候选，但必须出现拒绝、假突破重新回区间或反向信号 K；
- 第一反向确认可以建立 `range_edge_three_push_candidate`，不必先把它升级为 MTR；MTR/主要趋势反转仍需结构破坏、第二次确认和接受；
- 若第三推强势收在区间外并获得接受，原反转假设失效，切换为 BOP/趋势延续研究；
- 结构止损放在第三推极端/区间边界外，第一目标先看区间中线或最近独立障碍；首障碍不足约 1R 时记为 `valid_no_trade`。

区间边缘三推必须与趋势/通道三推、区间中部重复测试分开记录和统计。它是位置优势候选，不是已经验证的高胜率规则。

## 5. BOP 突破回踩

### 5.1 突破对象与接受

必须先有事前可见的突破对象，例如：

- 成熟区间边缘；
- 左侧前高/前低；
- 清楚的水平阻力/支撑；
- 经过足够分离测试的趋势线或结构边界。

突破日线必须收盘在关键位外，不能只靠盘中刺穿。一次影线、没有跟随或很快重新收回原区间，不能称为已接受 BOP。

### 5.2 BOP 状态分层

| 状态 | 必要证据 | 输出处理 |
| --- | --- | --- |
| `acceptance_watch` | 日线强收盘越过边界，但尚未形成有效回踩 | 观察候选，不称为完整 BOP 回踩交易 |
| `ordinary_pullback` | 突破后至少有后续日线接受；价格回到实际被突破区域，守住后重新向突破方向离开 | 可进入普通 BOP 候选，重建入场、止损、首障碍和空间 |
| `failed_breakout` | 影线、无跟随或收盘重新接受回原区间 | 切换失败突破/区间边缘，不沿用 BOP thesis |
| `gap_event` | 缺口或事件造成的突破、接受和重订 | 单独标记，不能与普通 BOP 混合统计 |

日线突破后只有同日盘中回测、单根影线测试或低周期回测时，记录为同日/低周期合同，不能称为“多日 BOP 回踩”。

回踩必须回到实际被突破的区域，而不是机械寻找某一根旧 K 线。回踩守住后要有重新离开和方向跟随；如果只是触及旧位但没有重新启动，保持 `research_state: pattern_like`、`trade_state: pending`。

### 5.3 趋势线与牛旗分支

- 三个逐步降低的高点可以形成趋势线候选，但三个点本身不自动证明成熟趋势线；必须确认测试有分离、位置有意义且不是区间噪音。
- 突破趋势线后形成牛旗，牛旗向上突破可以单独标记为 `bull_flag_continuation`。
- 牛旗分支必须确认价格没有日线收回趋势线下方；一旦重新接受到趋势线下方，原 BOP 观察失效或切换为其他状态。
- 趋势线突破后，左侧最高点仍是重要首阻力。趋势线提前突破只有在到左侧最高点仍有足够空间时才保留；真正突破并守住左侧最高点后，才称为更完整的大级别 BOP。

### 5.4 BOP 的合同重建

突破接受后，原来的 H/L、三推、MTR 或区间合同必须废弃或重建。重新记录：

```text
bop_state:
breakout_boundary:
acceptance_close:
follow_through:
retest_zone:
role_reversal_held:
new_trigger:
new_structural_stop:
first_independent_obstacle:
rough_space_to_first_obstacle:
```

## 6. 财报、缺口与异常事件

- 已知财报在未来三个交易 session 内，所有新仓候选原则上排除；不只排除 BOP。记录 `event_context: earnings`、`earnings_next_three_sessions: yes`、`gate_result: valid_no_trade` 和 `trade_state: valid_no_trade`。
- 财报后的大涨或大跌可以研究，但必须标记为 `earnings-driven` 或 `event-driven`，与普通 ABC、普通 BOP 分开记录和统计。
- 异常跳空、重定价、宏观冲击、监管消息、并购或产品发布若改变了原有结构，不能直接套用普通 ABC/BOP；应重新核对边界、成交、止损、首障碍和 R/R。
- 开盘跳过原触发时，原合同记为未成交或未知，不能沿用原价；只有实际回到旧结构区才另立 limit-retest/reprice 合同。
- 事件日期或影响不清楚时，保留 `pending`，不能因为后续走势好看而删去事件字段。

## 7. 统一排除条件

下列任一项成立，原则上不进入高质量候选：

- A 腿推动力不足，或只能靠事后结果解释；
- B 腿失控、过度扩张、完全吞没 A，或三推发生在成熟区间中部；成熟区间本身不自动否决区间边缘三推，但必须切换到 4.1 分支；
- C 没有恢复方向、反复失败或没有可说明的日线信号；
- 突破只有影线、没有接受，或很快收回原区间；
- 前方第一独立障碍不足约 1R；
- 结构止损不清楚、必须人为压窄，或风险过宽；
- 20 日平均日成交额低于 5,000 万美元或数据缺失；
- 未来三个交易 session 内有财报，或重大事件未核对；
- 两年 Daily 左侧、EMA20/50/200 或重要高低点不可见；
- 依赖 4H/1H/15m 才能成立，而日线本身不支持；
- H1/H2 的 Daily EMA20/50 不是同时向上，或 L1/L2 的 Daily EMA20/50 不是同时向下；
- 事件跳空、重订价、同日回测或特殊订单合同未单独标记；
- 形态只能靠后见之明命名，无法在当时明确识别。

## 8. 每日候选输出合同

每日输出只保留通过共同硬闸门的 0–5 只。每只必须说明：

```text
symbol:
review_date:
contract_scope: daily_candidate
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_daily_bar_as_of:
universe_type: US_common_stock
market_cap_usd:
market_cap_as_of:
market_cap_source:
average_dollar_volume_20d:
earnings_next_three_sessions:
event_context:
event_source_as_of:
sector_reference:
sector_state: aligned / mixed / counter / unknown
market_reference:
market_state: aligned / mixed / counter / unknown
permission: long_allowed / short_allowed / both_allowed / no_direction / unknown
gate_result: pass / conditional / observation_only / valid_no_trade / pending
two_year_daily_context:
major_highs_lows:
support_resistance_and_role_zones:
daily_ema20_50_200:
daily_ema20_slope: up / flat / down / unknown
daily_ema50_slope: up / flat / down / unknown
h_l_ema_slope_gate: long_pass / short_pass / fail_flat_or_opposite / pending / not_applicable
h_l_pullback_location:
meta_confluence: present / absent / unknown
meta_zone:
meta_components:
parent_state:
direction: long / short / no_valid_direction
primary_pattern: ABC_CONT / BOP
secondary_context:
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
internal_label: H1 / H2 / L1 / L2 / H3_L3 / none / pending
range_edge_three_push: yes / no / pending
bop_state: acceptance_watch / ordinary_pullback / failed_breakout / gap_event / bull_flag_continuation / not_applicable
breakout_boundary:
acceptance_close:
follow_through:
retest_zone:
role_reversal_held: yes / no / unclear / not_occurred
special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none
key_breakout_or_structure_location:
why_it_meets_the_rule:
possible_daily_entry_trigger:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R:
signal_bar:
confirmation_bar:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
document_status: draft / adopted / historical / research_only
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
thesis_state: working / failed / invalidated / replaced / pending
handoff_status: research_only / not_ready / ready_for_system
main_uncertainty_or_exclusion:
```

`direction` 是每只候选必填字段；若父级、空间、事件或合同使当前没有可授权方向，写 `no_valid_direction`，不能只写“看多/看空倾向”。输出文字必须区分事实和解释；历史或收盘后数据不能写成实时。形态很像但首障碍、事件、成交或止损不合格时，应保留为 `research_state: observation_only` 或 `trade_state: valid_no_trade`，而不是进入 3–5 只名单。

## 9. 统计边界

这份规则只定义选股和分层，不宣称胜率。后续结果必须至少分开统计：

- `ABC-CONT`、H1、H2、L1、L2；
- H/L 的 EMA20/50 方向通过、走平/反向边界，以及 META 共振存在/缺失；
- 趋势/通道三推 H3/L3、区间边缘三推、区间中部重复测试；
- 普通 BOP、牛旗延续 BOP、财报/事件 BOP、缺口重订；
- `filled`、`no-fill`、`opening-skip`、`valid_no_trade` 和不同走势 lineage。

只有在入场、结构止损、目标/时间边界和实际成交都提前冻结后，才可进入胜率和 realized R 统计。`第一障碍约 1R` 是入场前几何过滤，不等于实际盈利；`valid_no_trade` 不是亏损样本。当前统计状态继续保持 PA Research 的 `not-statistical / no-new-positive`。

## 10. 与现有研究合同的关系

- [PA 图表视觉复核卡](visual_pa_review_card_CN.md)：完整图表、两年背景和统一字段；
- [ABC 趋势延续](../patterns/03_abc_continuation/README.md)：A/B/C 与深但后段受控 B 的分层；
- [BOP 突破回踩](../patterns/06_breakout_pullback_bop/README.md)：突破接受、真实回踩和失败突破；
- [财报/事件/板块/大盘前置闸门](../foundations/05_event_sector_market_gate/README.md)：事件与市场背景；
- [BOP 真实多日回踩候选审计](../research/bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)：普通多日 BOP 的当前证据缺口；
- [ABC + H/L 分层历史结果审计](../research/abc_hl_stratified_outcome_audit_2026-08-24_CN.md)：结果字段和统计边界。
- [三推/H3-L3 压力状态框架](../research/three_push_pressure_state_framework_CN.md)：区间边缘三推与区间中部重复测试的分流。

研究边界：只更新 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

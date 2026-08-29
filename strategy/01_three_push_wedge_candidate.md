# 三推楔形候选规则（v0.1）

> 状态：研究假设，尚未进入生产规则或程序化回测。

本页只保存 PA Research 的视觉研究假设和案例分流，不是量化扫描器、交易授权或 Execution Agent 输入。当前没有冻结的三推/H3/L3 回放合同；结论仍为 `no-new-positive`，`validated win-rate: not-computable`。

## 研究目标

把“连续三次向同一方向推进”与“真正的三推楔形反转结构”区分开，并进一步区分：

1. 有机会形成主要反转；
2. 只适合期待一次短线反弹/回调；
3. 只是趋势中的三段推进，不应逆势交易。

## 形态定义

### 1. 三个独立推进

- 必须能辨认出三个同方向的推进，每一推之间有可见的回调、横向停顿或反向尝试。
- 不能把一根连续扩张的趋势腿内部随意切成三个点。
- 三个极值点应处于同一个可解释的结构级别；如果一个点来自日线、另一个来自很小的盘中噪音，不能混为同一形态。

### 2. 推进逐步失去效率

至少应看到以下证据中的两项，理想状态是第三推最明显：

- 后一推的价格距离小于前一推，或新极值只略微超越前一个极值；
- 每一推需要更多 K 线才能取得更小的进展；
- 重叠增加、回调加深、通道变宽；
- 收盘不再持续靠近极端，影线或反向实体增加；
- 第三推出现超调，但没有获得强劲跟随。

如果实体扩大、收盘靠近极端、成交和跟随同时扩张，应视为趋势加速或高潮候选，而不是自动称为楔形衰竭。

### 3. 成熟度与位置

- 主要级别的三推楔形最好有约 20 根或更多 K 线，或者已有清楚的通道和足够的双方反复；
- 少于这个长度的结构可以标为“小型三推/短线楔形”，预期只能是反弹或回调，不能直接升级为主要趋势反转；
- 第三推若同时到达高周期支撑/阻力、旧突破点、测量移动目标、整数位或通道边界，结构质量提高；
- META 的含义是多重优势汇聚，不是入场信号。三推本身必须先成立，其他优势只用于提高位置质量。

## 交易触发

第三推的极值点本身不构成入场。候选触发应满足以下之一：

### 早期触发

- 第三推出现明确反向信号棒，随后突破信号棒高点/低点；
- 适合小仓位，因为空间较好但反转概率仍较低。

### 保守触发

- 第三推后形成第二次入场；
- 或价格突破最近的微型更低高点/更高低点，并出现跟随；
- 回踩不重新跌破第三推极值，形成更高低点/更低高点。

保守触发优先用于“优质机会”识别。若只有一个反向影线、没有跟随，就只能记录为潜在反应，不能称为确认反转。

## 三种结果分类

### A. 高质量反转候选

三推独立、推进衰竭、位于 META 区域，并且出现反向触发和跟随；前方第一阻力仍有足够空间，结构止损后至少有合理的风险回报。

### B. 短线反弹/回调候选

三推和位置较好，但形态太短、前方空间有限，或只突破了微型结构。目标应先看最近磁铁或前一摆动，不预设主要趋势反转。

### C. 形态拒绝

三个点虽然存在，但后一推没有减弱，或者出现强扩张、连续收盘和跟随。此时是趋势推进或失败楔形，不能因为“数到了三推”而逆势。

## 止损、目标与失效

- 多头止损放在第三推极值和必要的结构缓冲之外；空头反之。
- 第一目标看最近的反向摆动、均线、区间中线或明显支撑阻力；第二目标才考虑测量移动或区间另一侧。
- 到达测量目标只说明目标完成，不等于反转确认。
- 若原方向以强实体突破第三推极值并获得跟随，候选反转失效。
- 不使用固定百分比止损，也不把保本移动当作默认规则；仓位由结构止损距离决定。

这里的“第一目标”不自动等于统一合同的 `first_independent_obstacle`：首障碍必须是入场前可见、独立且位于方向路径上的结构；EMA 可以作为背景或路径证据，但不能单独制造首障碍空间。第三推案例仍须另记 `structural_stop`、`pre_entry_space_R`、`space_status` 和实际订单分支，不能用后续目标或盈利补齐入场几何。

## 第一批代表性样本

### TSLA 日线：2026-05-19 至 2026-06-26

候选低点为：

- 05-19：393.63；
- 06-10：380.15；
- 06-25：371.22；06-26 延伸至 368.60。

第一段推进约 13.48，第二段到第三推约 11.55，第三推在 06-25/26 只是小幅延伸，符合“推进效率下降”的初步特征。该区域同时对应左侧支撑（需在图表上标注具体支撑带），属于 META 候选位置。

价格在 06-26 收于约 379.71，06-29 之后确实出现强反弹；但不能只根据后续涨幅把它升级为可交易正例。按入场时可见的几何，`06-26` 约 `379.12` 上方的保守确认，结构止损在 `368.60` 下方，最近的 `385.20–387.80` 阻力区只提供约 `0.63R–0.83R`。因此更准确的标签是：**B 类三推/第三次测试短线反应候选；反向触发有跟随，但 Daily/波段新仓首障碍不足，`valid_no_trade`**。它不能证明更大级别趋势永久反转。

低周期可以提出更早的 `374.75` 上方触发研究分支，但不能用更窄止损或后续 `06-29` 的上涨制造当时不存在的空间；该分支仍先遇 `379.12` 和 `385.20`。

来源： [TSLA Historical Prices（ChartExchange）](https://chartexchange.com/symbol/nasdaq-tsla/historical/)。

### TSLA 日线：2026-07-02 至 2026-07-29

可看到从 07-02 高点区域向下的多段推进：07-20 低点约 369.43，07-23 低点约 315.74，07-29 低点约 297.38。它在表面上有“三段下跌”，但 07-23 出现约 14.5% 的大幅扩张并放量，收盘接近低位，缺少逐推减弱的关键证据。

因此先标为“普通三段推进/空头延续”，而不是三推楔形反转。07-29 后 07-30、07-31 的反弹幅度有限，也说明第三推到位不等于立即反转。

来源： [TSLA Historical Prices（ChartExchange）](https://chartexchange.com/symbol/nasdaq-tsla/historical/)。

## 当前候选定义

```text
三推楔形候选 =
    三个独立同向推进
    + 至少两项推进衰竭证据
    + 结构级别和位置一致
    + 第三推接近可解释的支撑/阻力或 META 区域
    + 反向触发和跟随
```

其中前三项用于判断“形态是否存在”，反向触发用于判断是否出现反应，第一障碍和 R/R 才决定是否值得交易。即使有反向触发和跟随，如果首障碍太近，也必须保留为 `valid_no_trade`；没有反向触发时，最多只能叫潜在反应区。

## 与统一输出合同的对应

本页的 A/B/C 是解释性分流，不是新的状态枚举。新研究记录统一使用以下字段；字段值必须来自统一合同：

`primary_pattern` 是当前合同的主标签，`internal_label` 只记录 H1/H2/L1/L2/H3/L3；若 `contract_scope: daily_candidate`，主标签只能是 `ABC_CONT` 或 `BOP`，三推/H3/L3 只能作为内部标签或 `secondary_context`。

```text
contract_scope: deep_review / daily_candidate / historical_context_only
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
lineage_status: same_lineage / reset / unclear / pending
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
direction: long / short / no_valid_direction
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
first_independent_obstacle:
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

- A 类只有在 `third_push_state=exhaustion_candidate` 且反向证据、订单、首障碍和空间都完成时，才可写 `research_state: research_positive_conditional`；它仍不是生产规则或已验证胜率。
- B 类通常保留为 `pattern_like`、`observation_only` 或 `valid_no_trade`；若是成熟区间边缘，使用 `third_push_state: range_repeat_test` 并填写 `range_edge_side`，不把边缘方向旗标当作授权方向。
- C 类通常写 `third_push_state: continuation_or_climax` 或 `channel_continuation`；它只表示压力分流，不自动生成反向 `direction`、订单或目标。
- `attempt_direction` 是三次尝试的朝向，`direction` 是当前研究合同方向；触发、首障碍或合同未冻结时，`direction` 可以是 `no_valid_direction`。A/B/C 分流不建立统计分母，当前三推/H3/L3 仍保持 `no-new-positive`。

## 待验证

- 先收集日线和 15 分钟图表中的正例、短线反弹例、失败例，分别标注，避免只收集成功案例。
- 验证“20 根 K 线”对主要楔形与小型楔形是否应使用不同阈值。
- 将推进衰竭拆成可测量字段：价格距离、推进所用 K 线数、重叠比例、收盘位置、突破后的跟随。
- 在规则进入回测前，不把任何单个案例的结果当作胜率或交易优势。

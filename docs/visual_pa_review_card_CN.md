# PA 图表视觉复核卡

状态：`visual-first / research tool`

这是一张给“看懂完整图表的 PA 助手”使用的复核卡。它的用途是先筛选出**看起来像**某个 Price Action pattern 的候选，再用更完整的背景、位置、触发、风险和结果去优化。它不是量化扫描器、不是胜率评分器，也不是自动下单授权。

第一轮筛选与第二轮交易优化的边界，先看[`PA Pattern 视觉筛选协议`](../research/visual_pattern_triage_protocol_CN.md)。本卡是进入第二轮后使用的完整复核卡；没有必要为每个“看起来像”的图形一开始就填满所有价格和 R/R 字段。

## 快速视觉初筛：先判断像不像

在进入下面的完整复核卡之前，先用完整图表做一个定性初筛。第一轮只需要回答：

```text
背景：趋势 / 区间 / 过渡 / 高潮 / 不清楚
候选 pattern：ABC / H1-H2-H3 / L1-L2-L3 / 区间边缘 / 其他
A 腿：强方向 / 普通方向 / 不清楚
B 腿：受控 / 深但后段受控 / 反向压力强 / 区间化 / 不清楚
位置：主要支撑阻力、区间边缘、EMA、缺口、通道或中部
第一阶段结论：值得深入 / 形态像但先观望 / 不是这个 pattern
仍不确定：一句话写出计数、尺度或事件疑问
```

这一轮允许价格、日期和端点只写区域，不要求测量 MM、精确 R/R 或冻结唯一 H1/H2/L1/L2。只有“值得深入”的候选，才继续填写本卡的订单、结构止损、第一障碍和粗略止盈；“形态像但先观望”也要保留，但不必为了它补齐所有数值。这样 PA Research 才是图表理解助手，而不是先把每张图压成量化输入。

## 使用原则

1. 先看完整图表，再看形态名称。
2. 先重建当时能看到的背景和位置，再使用后来发生的结果做审计。
3. 可以先用 `pattern_like` 记录模糊候选；不需要一开始就精确到固定阈值。
4. 形态质量和交易可行性分开：一个形态可以很像，但因为第一障碍太近而是 `valid_no_trade`。
5. 同一张图可以有多个嵌套结构；记录局部腿和母腿，不为了短窗口强行切割市场。
6. Daily、4H/60m、15m 的背景、计数和触发分开记录；不能把不同周期的 H2/L2 合成一个计数。

## 0. 图表证据头

开始分析前先写清楚：

```text
symbol:
review_date:
data_source:             # Futu OpenD / after-close public data / chart screenshot / other
data_status:             # historical / delayed / live-confirmed / incomplete
timeframes_seen:         # Daily / 4H or 60m / 15m / other
chart_scope:             # full context / partial context
event_context:           # earnings / macro / gap / none known / unknown
sector_context:
```

如果只有结构化历史数据，没有足够的完整图表上下文，结论必须标为候选或数据审计，不能写成已经完成的视觉判断。历史数据也不能描述成实时行情。

## 1. 背景：左边发生了什么？

先用一句话描述市场状态：

```text
market_state: trend / trading_range / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
left_context:
```

重点观察：

- 左侧是否有清楚的主要高点、主要低点、突破区、前支撑转阻力或前阻力转支撑；
- 价格是在趋势腿、区间边缘，还是区间中部；
- 当前位置是否接近 EMA20/EMA50/EMA200、缺口、通道边界或其他磁铁；
- 个股所在板块和大盘是否支持这个方向；
- 财报前三个交易日内原则上不新开仓；财报造成的跳空和波动要单独标记，不与普通 K 线证据混在一起。

成熟交易区间中，不要把每一次摆动都强行解释成 ABC 或 H/L 延续。区间边缘的交易与区间中部的交易是两种不同逻辑。

## 2. 先找母腿，再找局部腿

不要等到行情走完才从结果倒推 A 腿。看到方向性压力开始形成，就先标出：

```text
parent_leg_origin / parent_leg_end:
local_A_origin / local_A_end:
leg_scope: parent / local / both
```

### A 腿的视觉等级

- `strong`：方向性实体明显、收盘接近极值、重叠少、有连续跟随或有效突破；
- `ordinary`：方向存在，但实体、跟随和结构推进一般；
- `unclear`：混合收盘、重叠很多、宽通道或明显处在区间中部。

强 A 腿只提高 H1/L1 的研究优先级，不自动授权交易。普通或不清楚的 A 腿，优先观察 H2/L2，或者保留为 no-trade 对照。

如果 A 腿包含财报跳空，记录为 `event-driven strong`，不能直接当成普通趋势样本。

## 3. B 回调：卖压/买压是否受控？

### 多头候选

观察 B 中的卖压是否逐渐减弱：

- 下跌实体和收盘力度是否减弱；
- 重叠是否增加；
- 是否在主要支撑、EMA、缺口边缘或突破区获得反应；
- 是否出现第二腿陷阱风险，或回调已经变成双向交易区间；
- 回调量能是否萎缩。量缩是重要参考项，但不是必要条件。

### 空头候选

观察 B 中的买压是否逐渐减弱：

- 反弹实体和收盘力度是否减弱；
- 是否不断被前支撑转阻力、EMA、缺口或主要高点压回；
- 回调是否过深、过宽，已经破坏空头背景；
- 是否出现第二腿陷阱，或已经变成双向交易区间。

```text
B_quality: controlled / controlled-late / strong-counterpressure / range-like / unclear
B_leg_count: 1 / 2 / 3+ / unclear
pressure_asymmetry:
location_of_B_end:
```

## 4. H/L 计数：只数有意义的尝试

在同一周期、同一回调背景下记录：

```text
attempt: H1 / H2 / H3 / L1 / L2 / L3 / unclear
count_basis:
count_reset_reason:
```

- H1/L1 是第一次有意义的原方向尝试；
- H2/L2 是第一次尝试失败或回调再走一腿后的第二次尝试；
- H3/L3 是第三次有意义的尝试，不等于三推楔形，也不等于自动反转；
- 不能因为一根小 K 线略过前高/前低，就机械增加一次计数；
- 如果出现新趋势腿、新区间或计数被结构打断，要说明 reset 原因；
- `setup/count bar`、`signal bar`、`confirmation/trigger bar` 必须分开。

### H3/L3 三分流

如果当前尝试被标为 H3/L3，额外填写：

```text
same_lineage: yes / no / unclear
third_push_efficiency: weaker / similar / expanding / unclear
third_push_follow_through: weakening / mixed / strengthening / unclear
third_push_location:
reverse_trigger_present: yes / no / unclear
h3_l3_state: exhaustion_candidate / short_reaction_candidate / continuation_or_climax / not_h3_l3
```

- `exhaustion_candidate` 需要同一 lineage、压力效率下降、重要位置和反向触发；它也必须通过结构止损与第一障碍审计；
- `short_reaction_candidate` 只表示支撑/阻力可能带来一次反应，不能升级成主要趋势反转；
- `continuation_or_climax` 表示第三推仍在扩张或获得跟随，不能因为计数到 3 就逆势交易；
- 若 lineage 不清楚、已经进入区间或结构被重置，使用 `not_h3_l3`，转回区间/过渡逻辑。

## 5. Pattern 分类

用最少的标签描述当前候选，允许并列：

```text
pattern_family: TPB-H1/H2/H3 | L1/L2/L3 | ABC-CONT | RFB-SECOND | MTR-ABC | BOP-ABC | other
abc_mode: continuation / range-edge reaction / reversal candidate / complex / unknown
pattern_like_reason:
```

使用以下判断顺序：

1. 趋势中，A 明显、B 受控、原方向恢复：优先看 ABC 延续和 H/L；
2. 区间边缘出现失败突破和二次尝试：优先看区间边缘反转/二次入场，不强行称趋势 H2/L2；
3. 成熟趋势末端出现多次推进、动能减弱和反向触发：可记录反转候选；
4. 突破交易单独开分支，不把突破接受和普通回调延续混在一起。

## 6. 信号 K 与触发

### 优质信号 K 的视觉参考

- 方向实体清楚，收盘接近高点或低点；
- 在关键位置拒绝反向价格，带有有意义的下影线/上影线；
- 不是单纯碰到 EMA；
- 没有被异常长的反向实体、事件跳空或主要障碍立即否定；
- 后续有合理的跟随预期。

```text
setup_bar:
signal_bar:
confirmation_bar:
trigger_price:
trigger_logic:
signal_quality: strong / acceptable / weak / unclear
follow_through_expected: yes / mixed / no / unknown
```

不要让后面一根漂亮的确认 K 线，反过来把前面一个很差的信号 K 线改写成优质信号。

## 7. 订单分支：把“怎么看”和“怎么进”分开

订单分支的可复用规则和跳空处理见 [`订单分支视觉协议`](../research/order_branch_visual_protocol_CN.md)。本卡只保留逐图填写字段，避免把 stop、stop-limit、limit-retest、收盘确认和观望混成一个入场结论。

```text
order_branch: stop / stop-limit / limit-retest / market-close / observation-only
order_price_or_zone:
why_this_order_branch:
```

- H1/H2/L1/L2 的默认研究分支是：信号 K 后用 stop 等待确认；
- 结构支撑/阻力上的回测可以作为独立的 limit/retest 分支研究；
- 市价或收盘进场适用于强突破后的特殊情况，但要接受滑点和更宽止损；
- 多头回调下沿的 limit、空头反弹上沿的 limit，必须说明它是在等回测，不能和突破 stop 分支混算；
- 不要把“已经发生的后续大涨/大跌”当成当时必然应该挂单的理由。

## 8. 止损与失效

先写结构失效，再写价格：

```text
structural_invalidation:
stop_zone:
stop_price_or_area:
normal_test_room:
gap_or_event_adjustment:
```

止损通常放在 setup 结构、支撑/阻力簇或正常测试应到达的位置之外；不能把止损放在结构区内部，也不能因为想得到更好的 R/R 而任意缩窄止损。Daily 结构止损和 15m 短线止损是不同交易假设，不能自动互换。

## 9. 第一障碍先于 MM

按顺序记录：

```text
first_independent_obstacle:
first_obstacle_zone:
obstacle_type: major_high / major_low / range_edge / gap / EMA / channel / other
mm_or_abcd_target:
target_zone:
space_to_first_obstacle: clearly_positive / borderline / blocked / unknown
```

第一道独立支撑/阻力优先于一个孤立的 measured move。MM、AB=CD、50% 回调和缺口可以提供目标或汇合优势，但不能覆盖近端主要障碍，也不能互相重复计数。若 MM 和前高落在同一价格簇，只算一个主要障碍。

支撑/阻力的视觉强度排序见[`共同上下文：Support/resistance strength hierarchy`](common_context.md#supportresistance-strength-hierarchy-visual-working-version)。排序只表示结构优先级；实际 R/R 仍按入场方向上的最近独立区域计算。

`1R`、`2R` 只作为粗略几何检查，不是精确评分：

- 第一障碍不到约 `1R`：通常是 `valid_no_trade` 或只做观察；
- 第一障碍大致有空间：才值得继续检查触发和管理；
- 完整波段目标通常希望有更充足空间，但不能为达到某个数字而事后改锚点。

## 10. 结果状态

每个候选最后只选一个当前状态：

| 状态 | 含义 |
| --- | --- |
| `pattern_like` | 视觉上像，但还没有完成位置、触发或空间审计 |
| `research_ready` | 背景、A/B、计数、触发、止损和第一障碍已基本可复核 |
| `valid_no_trade` | 形态存在，但事件、第一障碍、计数不清或风险几何阻止交易 |
| `research_positive` | 入场前证据和空间结构较好，可作为正向研究样本；不代表胜率 |
| `invalidated` | 在当时可见证据下结构已经失效 |
| `pending` | 仍需另一周期、事件资料或图表上下文 |

`research_positive` 只描述研究几何，不等于赢单、不等于经过统计验证，更不等于真实下单授权。

## 输出模板

```text
### [symbol] [date range] [timeframe] — [pattern]

状态：pattern_like / research_ready / valid_no_trade / research_positive / invalidated / pending

背景：
左侧主要支撑/阻力：
母腿与局部 A 腿：
A 强度：strong / ordinary / unclear
B 回调质量：
H/L 计数及依据：
形态分类：
信号 K 与确认：
订单分支与触发：
结构止损与失效：
第一障碍：
MM/AB=CD/缺口/EMA 等辅助：
粗略空间判断：
为什么值得研究或为什么不做：
仍不确定的地方：
```

## 明确禁止的 shortcuts

- 不用一个案例声称“高胜率”；
- 不用后面的结果证明前面的判断本来就清楚；
- 不把 EMA 触碰、MM 到位或缺口回补单独当成入场信号；
- 不把区间中部摆动强行计成趋势 ABC；
- 不把 H3/L3 自动写成三推楔形反转；
- 不把历史或延迟数据说成实时；
- 不修改 Codex Trading 参考库，不把未成熟研究交给 Execution Agent；
- 不因为用户鼠标读数或日期差一点，就创造无关的纠正记录；只有会改变结构或交易结论的误差才需要回查。

## 相关文件

- [共同上下文](common_context.md)
- [ABC 决策矩阵](../research/abc_decision_matrix_CN.md)
- [视觉候选目录](../strategy/pattern_inventory_candidates.md)
- [H1/H2 质量定义](../research/h1_h2_quality_definition_CN.md)
- [H3/L3 研究门](../research/h3_l3_research_gate_CN.md)

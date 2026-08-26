# PA Research — Common Context

This document is the shared working context for the PA Research project. It records the current research boundaries, definitions, and unresolved questions so that future discussions do not depend on repeatedly reconstructing the same background.

## Project purpose

PA Research is the research and visual-structure layer. Its job is to study charts, organize Al Brooks Price Action concepts, compare examples, and turn observations into clear, testable hypotheses.

It is not the live trading system and does not place orders. PA Research may use its local, research-only `backtesting.py` replay harness for manually frozen contracts; production implementation and execution automation remain outside this repository.

## Visual-first research doctrine

完整图表的视觉判断是本项目最重要的能力和主要工作流。研究必须先回答“左侧发生了什么、当前处在趋势/区间/过渡的哪一部分、支撑阻力和压力如何组织”，再讨论 ABC、H/L 计数和订单。

- 日线选股阶段只使用完成的 Daily K 线；4H/60m/15m 只在候选入选后的独立深审或订单合同中使用，不能改变日线候选主标签。能看到的范围、周期和数据完整性必须写清楚。
- 多周期复核遵循[`Daily / 4H / 1H / 15m 分层框架`](../research/multitimeframe_visual_review_framework_CN.md)：Daily/4H/1H 先决定背景、父级结构、主要位置和结构止损，15m 默认只做确认；若低周期自成交易，必须另立合同，不能用窄止损改写高周期 thesis。
- Futu OpenD、历史 K 线和计算结果只用于测量、核对时间顺序、量价、R/R 和执行细节；它们不能替代完整图表的结构解释。
- 扫描器、指标或单个 K 线标签不能单独证明 ABC、H1/H2/H3、L1/L2/L3 或“高胜率”。
- 如果只能取得结构化数据而没有足够的图表上下文，结论必须标为“数据审计/候选”，不能写成完整视觉判断。
- 研究文件应把“视觉结构判断”和“数值核验”分栏记录，避免为了方便回测而把主观结构偷偷改写成伪精确阈值。

## Research phases: visual discovery before quantification

当前阶段不是量化建模，而是建立一个真正看得懂 Price Action 图表的研究助手。研究顺序分三层：

1. **视觉发现层**：在完整图表上先筛选“看起来像”的候选，优先判断背景、左侧结构、A/B/C、H/L1-3、位置和压力变化。此阶段允许保留模糊边界，粗略画出可能的入场、结构止损和目标区域，不宣称胜率。
2. **结构优化层**：对筛出的优质候选，再核对同周期计数、信号 K、触发、主要支撑/阻力、事件边界和大致 R/R；把相似形态、失败形态和不应交易的形态并排比较。
3. **程序验证层**：只有当视觉规则已经稳定、边界足够清楚，才把少数人工冻结合同交给 PA Research 的 research-only `backtesting.py` 回放器做结果审计；这不等于自动识别或生产回测。任何 Codex Trading 交接仍需单独通过研究交接规范。

因此，候选文件可以先用 `visual_candidate` 或 `pattern_like` 状态进入研究库；“看起来像”是筛选入口，不是最终规则，也不需要一开始就精确到固定阈值。

后续每张图先按 [`视觉 PA 复核卡`](visual_pa_review_card_CN.md) 走一遍：它把完整图表、背景、母腿与局部腿、A/B/C、H/L 计数、信号 K、订单、结构止损、第一障碍和 MM 按视觉优先顺序串起来。复核卡是研究助手的工作顺序，不是量化评分器。

当前阶段的跨案例视觉综合见 [`ABC / H-L 视觉研究阶段性综合`](../research/abc_visual_synthesis_v0_2_CN.md)。它用于快速区分“可以直接作为筛图依据”的共性、“仍需继续观察”的候选，以及不能声称已经验证的结论。

## Repository boundaries

- `PA Research`: research notes, source-aligned definitions, chart reviews, hypotheses, frozen-contract replay, and validated rule specifications.
- `Codex Trading`: separate programmatic research tools, Trading System implementation, and any future execution-related work; it is not modified by this replay harness.
- The reference material in the existing Codex Trading knowledge base is read-only during research unless a rule has matured and transfer work is explicitly in scope.
- The one-way research-to-system boundary, status vocabulary, handoff fields, and promotion gates are defined in [`docs/research_to_system_handoff_CN.md`](research_to_system_handoff_CN.md). Creating a research file does not mean that the rule is ready for Codex Trading.

## Market-data source policy

- Real-time intraday data: use the user's Futu OpenD connection as the preferred source. It is faster and more direct than repeatedly reading a browser chart.
- After-close and historical data: use the most reliable suitable source available, including structured public data or local frozen data. The source, timestamp, session definition, and any delay must be recorded.
- Fallback rule: if Futu OpenD is unavailable or the requested subscription/data is not returned, switch to public after-close data only. Never describe delayed, partial, or historical data as live market data.
- Browser charts remain useful for visual confirmation and educational material, but they are not the default real-time data pipeline.
- Build 4H candles from 1H data when the source does not expose a native 4H interval, and record the aggregation convention.
- Never mix a live Futu stream with historical bars from another source without checking symbol, timezone, adjustment, session, and price-scale consistency.

## Core framework

The primary framework is Al Brooks Price Action. Elliott Wave theory is not part of the main framework. ABC is used only as an operational Price Action description when useful: a first leg, a pullback, and a resumption leg.

The main context questions are:

1. Is the market trending, ranging, or transitioning?
2. Where are the major and minor support/resistance zones?
3. What is the current pressure: continuation, failed breakout, climax, or reversal attempt?
4. Which Price Action pattern is forming?
5. What is the entry trigger, stop, first obstacle, target, and invalidation?

## Immediate research scope: Daily ABC/BOP selection and H/L1-3

For the current daily-selection phase, prioritize two separate primary families: ABC continuation and BOP breakout-pullback. The ABC pullback framework still owns H1/H2/H3 and L1/L2/L3 attempt studies; BOP remains a separate contract and must not be mixed into ABC/H-L counts or outcome statistics. Lower timeframes can only be reviewed after a Daily candidate is selected and must not change the Daily screening label.

所有新记录的方向、BOP 状态、订单分支、事件闸门和研究/交易/交接状态统一按[`PA Research 统一输出合同 v0.1`](pa_research_output_schema_v0_1_CN.md)填写。`directional_bias` 只描述背景；当前研究合同必须另写 `direction: long / short / no_valid_direction`。

当前日线股票池先限定为美国普通股、市值约 `$3B–$100B`，并通过 20 日平均成交额门槛；市值和时间戳必须进入证据头。ETF 只作市场/板块背景，不替代个股候选。

- `A` is the directional impulse or trend leg; `B` is the pullback; `C` is the possible resumption leg.
- `A` is also a retrospective structural label, not the date when live research begins. Once directional pressure is recognizable, immediately evaluate the next B pullback and H/L attempts. Do not wait for C to finish or for the whole ABC to become visually complete. Every case should record both the earliest recognizable A date and the actual decision/trigger date.
- `H1`, `H2`, and `H3` are successive bull attempts within the same pullback context. `L1`, `L2`, and `L3` are the symmetric bear attempts.
- A count is only meaningful when it belongs to the same timeframe and the same pullback leg. Do not combine a Daily H2 with a 15m H2 as if they were one count.
- H3/L3 are the third-attempt research category. When the three attempts weaken, occur at a meaningful edge, and show pressure exhaustion, they may overlap with a three-push wedge/reversal. A mature trading-range upper/lower edge is a separate `range_edge_three_push` route: its A leg may be ordinary or weak, while a range-middle third push remains observation-only. The number `3` alone does not prove a wedge or a reversal; in a strong trend, a third attempt can still continue.
- For visual triage, classify a third attempt into three provisional states: **衰竭候选** (efficiency falls, follow-through weakens, location is meaningful, and a reverse trigger appears), **短线反应候选** (support/resistance produces a bounce or rejection but space or scale is limited), or **延续/高潮候选** (the third push expands, closes near the extreme, or gains follow-through). Only the first state can enter a reversal research audit, and even then it still needs a structural stop and first-obstacle check. The detailed gate and cases are in [`H3/L3 research gate`](../research/h3_l3_research_gate_CN.md) and [`H3/L3 visual comparison`](../research/h3_l3_visual_comparison_CN.md).
- Inside a mature trading range, do not force ABC or H/L leg continuity onto every swing. Use the range's upper edge, lower edge, failed breakouts, tests, and second entries first. A third push at the upper/lower edge can be a `range_edge_three_push` candidate after rejection and a reverse trigger; a range-middle third push remains observation-only. A range-edge reaction that visually resembles H2/L2 is not automatically a trend H2/L2.
- The dedicated range-edge working framework is [`交易区间边缘二次入场与失败突破`](../research/range_edge_second_entry_framework_CN.md). It separates edge reversal, failed-breakout re-entry, range swing/second-leg trap, and range-middle no-trade; it is still provisional and not a production rule.
- Only after a clear directional breakout/acceptance and a subsequent pullback/retest should a new first leg and second leg be evaluated as a trend-continuation structure. The initial range-edge trade and the later post-breakout second leg must remain separate hypotheses.
- Do not count every small intrabar high/low. A count should represent a meaningful attempt at a relevant location, followed by a signal and confirmation review.
- Keep setup/count bars separate from confirmation/trigger bars. H1/H2/H3 or L1/L2/L3 identify the attempt sequence; they do not authorize an order by themselves.
- The current study order is: larger background → A pressure → B pressure → major/minor support-resistance → H/L attempt count → signal K → trigger → stop/invalidation → first obstacle and measured-move space.
- For a live review, the sequence is not “find the completed A/B/C first.” It is: recognize A pressure while it is developing, start scanning the B pullback immediately, then decide whether the next H/L attempt is tradable. A later retrospective label must not erase an earlier valid decision window.
- Candidate priority follows A-leg quality: when the trend and A leg are strong—preferably around 3–4 consecutive, full-bodied directional Daily bars with clear follow-through, with a gap as an optional plus—the first valid H1/L1 signal K after a controlled pullback may be researched; when A is ordinary, overlapping, or ambiguous, H1/L1 is observation-only and preference shifts to H2/L2 after the first attempt fails or lacks follow-through. A mature-range edge is an explicit exception: ordinary A can still feed a range-edge three-push candidate, but only after edge rejection, trigger, structural stop and space review. This is a research priority, not a guaranteed probability rule.
- A complete chart may be used to audit the case, but the entry decision must be reconstructed from the bars, levels, event information, and space available at that timestamp. Later C-leg strength, measured-move completion, final target, or profit cannot upgrade an earlier setup retroactively. If the setup was not clear at the decision time, record a valid no-trade or hypothesis.

### Strong bearish A-leg filter

For bearish ABC studies, prioritize an A leg that shows genuine downside pressure rather than a slow, highly overlapping broad channel:

- large bear bodies, closes near the low, and range expansion;
- consecutive bear bars or an accepted break/gap with follow-through;
- clean lower-low/lower-high progress with limited overlap;
- a pullback that returns to a meaningful prior support-turned-resistance, EMA zone, or break area.

These are quality evidences, not rigid all-or-none requirements. A financial-results gap must be marked separately: it can prove strong movement, but it is event-driven evidence and must not be counted as an ordinary Price Action bar or silently merged into the baseline sample. A wide, slow channel is a downgrade for the first clean ABC sample, even if three downward swings can be labeled.

### Strong-A versus ordinary-A entry priority

Use the same distinction symmetrically for bullish and bearish studies:

- Strong A: directional closes, limited overlap, consecutive pressure, clear follow-through, and a trend context rather than a mature range middle. After B becomes controlled and reaches a meaningful location, H1/L1 can be the first candidate to evaluate.
- Ordinary A: mixed closes, heavy overlap, shallow or unclear progress, wide channel behavior, or conflict with a trading range. Do not force H1/L1; wait for a clearer second attempt H2/L2, or mark the setup as no-trade.
- The signal K, trigger, structural stop, first obstacle, and R/R still decide whether the candidate is tradable. Strong A only changes which attempt deserves priority; it does not authorize an order by itself.

## Priority concepts

- 当前主动实现的 pattern 目录总览见 [`PA Research 核心 Pattern 目录`](../patterns/README.md)。当前范围固定为 H1/L1、H2/L2、ABC 延续、区间边缘二次入场、失败突破/高潮、突破回踩/BOP、MTR 和三推/H3-L3；其他形态暂不扩展。
- 八个核心 pattern 的统一字段、切换顺序和状态词汇见[`核心八个 Pattern 交叉一致性审计`](../research/core_pattern_cross_audit_CN.md)；多个标签可以是同一父级中的不同层，不重复计作多个独立优势。
- ABC 趋势延续的当前入口见[`ABC 趋势延续`](../patterns/03_abc_continuation/README.md)：先判市场状态，再判 A/B/C；区间内部不强行数趋势腿。
- H1/H2/H3 and L1/L2/L3, understood as context-dependent pullback attempts rather than rigid labels；当前 H1/L1 入口见[`H1/L1 第一次入场`](../patterns/01_h1_l1_first_entry/README.md)，H2/L2 入口见[`H2/L2 第二次入场`](../patterns/02_h2_l2_second_entry/README.md)。
- Trading-range top shorts and bottom longs, especially second entries.
- 区间边缘研究入口见[`交易区间边缘二次入场`](../patterns/04_range_edge_second_entry/README.md)：区间中部不继承趋势 ABC 腿计数，second-leg trap 单独审计。
- Major trend reversals, now organized by the [`MTR visual framework`](../research/mtr_visual_framework_CN.md); they remain provisional and are not a production rule.
- MTR 的主动入口见[`MTR 趋势反转`](../patterns/07_mtr_reversal/README.md)：成熟趋势、主要位置、结构破坏、第二次确认和空间必须分开审计。
- 三推/H3-L3 的主动入口见[`三推 / H3-L3 压力状态`](../patterns/08_three_push_h3_l3/README.md)：先确认同一 lineage 或同一成熟区间边缘，再分流衰竭、扩张、区间边缘候选、区间中部重复测试和通道延续。
- Head-and-shoulders and rounded tops/bottoms are organized by the [`头肩顶/底与圆顶/圆底视觉边界框架`](../research/head_shoulders_rounded_top_bottom_visual_framework_CN.md)：头肩先作为复杂双顶/双底或 MTR 候选，圆顶/圆底先作为控制权转移警报，不因外形自动入场。
- Final flags, breakouts, channels, wedges, measured moves, opening reversals, failed breakouts, climaxes, double tops/bottoms, three-push variations, inside bars, triangles, and magnets/support-resistance, following Brooks' flexible pattern language. Final Flag 的工作框架见[`Final Flag visual framework`](../research/final_flag_visual_framework_CN.md)；开盘反转的视觉框架见[`Opening Reversal visual framework`](../research/opening_reversal_visual_framework_CN.md)；紧/宽通道的视觉框架见[`Channel visual framework`](../research/channel_visual_framework_CN.md)；失败突破与高潮反转的视觉框架见[`Failed breakout / climax reversal visual framework`](../research/failed_breakout_climax_visual_framework_CN.md)；双顶/双底、MTR 与 Final Flag 的对照入口见[`Double top/bottom, MTR and Final Flag comparison`](../research/double_top_bottom_mtr_final_flag_comparison_CN.md)；三推/H3-L3 的压力状态见[`Three-push / H3-L3 pressure-state framework`](../research/three_push_pressure_state_framework_CN.md)；Inside Bar / 两根 K 线反转的视觉框架见[`Inside Bar / two-bar reversal visual framework`](../research/inside_bar_two_bar_reversal_visual_framework_CN.md)；三角形与扩张三角形的视觉框架见[`Triangle / expanding triangle visual framework`](../research/triangle_expanding_range_visual_framework_CN.md)。
- Measured Move and AB=CD are space and target tools, not standalone entry signals. The cross-pattern target order is [`Measured Move、磁铁与目标层级视觉管理框架`](../research/measured_move_magnet_target_hierarchy_CN.md)：先看第一独立障碍，只有结构被接受后才把 MM 当主要延伸目标。
- 趋势后段入场是上述所有 pattern 共用的时机/空间过滤层，入口见[`Late Trend Entry / 追价过滤`](../foundations/03_late_trend_entry_filter/README.md)，既有框架见[`趋势后段入场视觉框架`](../research/late_trend_entry_visual_framework_CN.md)，专项审计见[`趋势后段入场视觉证据审计`](../research/late_trend_entry_visual_evidence_gap_audit_2026-08-24_CN.md)：区分受控回调、高潮风险、突破接受和后段无空间，不把强趋势自动等同为可追价。
- Daily/4H/1H/15m 的统一职责、低周期确认与独立短线合同见[`Multi-timeframe Review`](../foundations/04_multitimeframe_review/README.md)，既有框架见[`Daily / 4H / 1H / 15m 分层框架`](../research/multitimeframe_visual_review_framework_CN.md)，专项审计见[`多周期视觉复核证据审计`](../research/multitimeframe_visual_evidence_gap_audit_2026-08-24_CN.md)。低周期不能创造高周期没有的背景、空间或主要障碍。
- 财报、重大事件、板块/大盘许可与事件订单重订见[`Event / Sector / Market Gate`](../foundations/05_event_sector_market_gate/README.md)，既有闸门见[`财报、板块与多周期前置过滤`](../research/event_sector_multitimeframe_cross_pattern_audit_CN.md)，专项审计见[`事件/板块/大盘视觉证据审计`](../research/event_sector_market_gate_visual_evidence_audit_2026-08-24_CN.md)。财报前三个交易 session 不新开仓；顺板块是许可，不是信号；事件后强 A 必须单列。
- stop、limit-retest、market-close、stop-limit、实际成交、结构止损和 R/R 的统一语义见[`Order / Risk Contracts`](../foundations/06_order_risk_contracts/README.md)，既有协议见[`订单分支视觉协议`](../research/order_branch_visual_protocol_CN.md)，专项审计见[`订单类型与风险合同视觉证据审计`](../research/order_risk_contract_visual_evidence_audit_2026-08-24_CN.md)。订单类型改变时，入场、止损、首障碍、目标、仓位和结果必须一起重算。
- 开放趋势、成熟区间、区间边缘、过渡、高潮和 second-leg trap 的父级分类见[`Market State / Context`](../foundations/07_market_state_context/README.md)，专项审计见[`市场状态与父级背景视觉证据审计`](../research/market_state_context_visual_evidence_audit_2026-08-24_CN.md)。先判状态再数 H/L 或 ABC；区间中部默认观望，突破接受后重建新合同。
- 强 A、B 回调压力、优质 signal K 与买卖压力不对称见[`Leg Pressure / Signal Quality`](../foundations/08_leg_pressure_signal_quality/README.md)，专项审计见[`强 A 腿与信号 K 视觉证据审计`](../research/leg_pressure_signal_quality_visual_evidence_audit_2026-08-24_CN.md)。深 B 不自动否决，量缩只是非必要参考；setup、signal、trigger 和 follow-through 必须分开。
- 突破回踩/BOP 的主动入口见[`突破回踩 / BOP`](../patterns/06_breakout_pullback_bop/README.md)：突破接受后必须建立新合同，不能沿用突破前的反转或区间合同。
- EMA 触碰本身不是 pattern；但对高质量日线 H1/H2/L1/L2，EMA20/50 的方向性斜率是方向闸门：多头两条均向上，空头两条均向下。走平、反向或不可见时只能保留为边界/待定，不能进入普通高质量 H/L。
- 失败突破/高潮的主动 pattern 入口见[`失败突破与高潮`](../patterns/05_failed_breakout_climax/README.md)；它必须把测试、失败候选、小反转/区间、MTR 候选和 BOP 接受分开。
- MTR 与三推/H3-L3 的边界复核见[`MTR 与三推/H3-L3 视觉边界复核`](../research/mtr_three_push_visual_boundary_audit_2026-08-24_CN.md)：三推描述原方向尝试，MTR 只在反向结构破坏、二次确认和空间同时成立时升级。
- H1/L1 第一次入场的边界复核见[`H1/L1 第一次入场视觉边界复核`](../research/h1_l1_first_entry_visual_boundary_audit_2026-08-24_CN.md)：设置 K、确认 K、触发、首障碍与 H2/L2 fallback 必须分开。
- H2/L2 第二次入场的边界复核见[`H2/L2 第二次入场视觉边界复核`](../research/h2_l2_second_entry_visual_boundary_audit_2026-08-24_CN.md)：第二次是同一回调中的有意义位置测试；区间边缘、状态重建和低周期合同不能混算。
- ABC 趋势延续的边界复核见[`ABC 趋势延续视觉边界复核`](../research/abc_continuation_visual_boundary_audit_2026-08-24_CN.md)：先判父级和 A/B lineage，再用 H/L 触发 C；MM 不能替代首障碍。
- BOP / 突破接受与突破回踩的边界复核见[`BOP 视觉边界复核`](../research/bop_visual_boundary_audit_2026-08-24_CN.md)：影线不等于接受，gap-and-go、真实回踩和失败突破必须分别建立合同。
- 失败突破与高潮反转的边界复核见[`失败突破与高潮反转视觉边界复核`](../research/failed_breakout_climax_visual_boundary_audit_2026-08-24_CN.md)：高潮先预期小反转/区间；失败突破需回到原侧并有反向确认；BOP 接受会否定旧 thesis。
- 交易区间边缘二次入场边界复核见[`交易区间边缘二次入场视觉边界复核`](../research/range_edge_second_entry_visual_boundary_audit_2026-08-24_CN.md)：先冻结上下沿/中线，再记录边缘尝试；区间中部不继承 ABC/H-L 计数。
- Final Flag 最终旗形边界复核见[`Final Flag 最终旗形视觉边界复核`](../research/final_flag_visual_boundary_audit_2026-08-24_CN.md)：最终来自趋势末端背景，不来自窄整理外观；接受切 BOP，失败才研究反向二次确认。

## Probability principles

- Opening Reversal 开盘反转边界复核见[`Opening Reversal 开盘反转视觉边界复核`](../research/opening_reversal_visual_boundary_audit_2026-08-24_CN.md)：先看盘前位置和第一波接受/失败，再决定反向 H/L；开盘跳过必须重订合同。
- Channel 通道边界复核见[`Channel 通道视觉边界复核`](../research/channel_visual_boundary_audit_2026-08-24_CN.md)：两点连线不等于成熟通道；紧通道、宽通道、扩张、区间过渡和 BOP 接受必须分开。
- Inside Bar / 两根 K 线边界复核见[`Inside Bar / 两根 K 线反转视觉边界复核`](../research/inside_bar_two_bar_reversal_visual_boundary_audit_2026-08-24_CN.md)：严格整根范围、两根压力转换、H/L setup—signal—trigger、区间中部和跳空重订必须分开。
- Triangle / 三角形边界复核见[`Triangle / 三角形视觉边界复核`](../research/triangle_expanding_range_visual_boundary_audit_2026-08-24_CN.md)：收缩、扩张、区间内区间、BOP 接受、失败突破和父级状态必须分开。
- Double Top / Double Bottom 双顶双底边界复核见[`双顶双底视觉边界复核`](../research/double_top_bottom_visual_boundary_audit_2026-08-24_CN.md)：两次有分离测试、区间边缘、普通延续、Final Flag、MTR、BOP 否定和首障碍必须分开。
- Head-and-Shoulders / Rounded 头肩与圆顶圆底边界复核见[`头肩与圆顶圆底视觉边界复核`](../research/head_shoulders_rounded_visual_boundary_audit_2026-08-24_CN.md)：复杂双顶/底、真实颈线、圆形状态转移、普通旗形和 BOP 否定必须分开。
- 跨 Pattern 视觉优先级与冲突复核见[`Cross-Pattern 视觉优先级与冲突消解审计`](../research/cross_pattern_visual_priority_audit_2026-08-24_CN.md)：先判父级和位置，再选一个主标签，次标签只记录结构关系，订单与首障碍单独否决。
- 完整图表统一复核卡见[`PA 图表视觉复核卡`](visual_pa_review_card_CN.md)，工作流边界演练见[`完整图表视觉复核工作流边界审计`](../research/visual_review_workflow_boundary_audit_2026-08-24_CN.md)：先快筛，只有有新信息或候选值得深入时才深审。

The probability table is treated as conditional experience-based guidance, not guaranteed win rates. It is a user-supplied educational heuristic, not a PA Research measurement; the source locator and validation boundary are recorded in [`probability principles`](../strategy/probability_principles_pages_1_7.md).

```text
source_type: user_supplied_educational_reference
source_locator: Brooks Price Action probability table, pages 1-7
source_version: not_provided
source_as_of: unknown
evidence_status: external_heuristic_not_validated
```

In particular:

- In a trend, most reversal attempts fail; the working Brooks heuristic is about 80% failure.
- In a trading range, most breakout attempts fail; the working Brooks heuristic is about 80% failure.
- Strong trends commonly pull back toward the EMA.
- Large or surprising moves often produce a measured move, but the target is not an automatic reversal.
- A probability never replaces location, signal-bar quality, risk/reward, and invalidation.

## Pattern interpretation principles

- Brooks patterns are flexible and can overlap. One chart may simultaneously show a failed breakout, a channel, a measured-move target, and a final-flag reversal.
- A pattern is not defined by shape alone. Market context, location, pressure, and follow-through matter.
- Three-push wedges can have variations. They need not be perfectly convergent, and the third push does not always exceed the second.
- A strong trend bar is evidence, not an automatic entry. Avoid chasing late climax behavior; prefer a suitable pullback or confirmation.
- When the first entry is uncertain, a second entry often provides better confirmation, but it still requires adequate space and risk/reward.
- Do not force the market into an overly short time window. A visible leg can be a nested leg inside a larger impulse, and two apparent legs can later be reinterpreted as one larger leg when the broader structure becomes clear.
- Leg segmentation is provisional until enough context develops. Record the local leg and the parent leg separately rather than treating them as competing truths.
- A measured move can be calculated from a local leg for a near-term target and from the larger parent leg for a later target. Both are valid only if their anchors were available and clearly defined before the relevant decision.
- When a prior breakout area, EMA50, gap, or pause zone is retested after a larger leg, evaluate it as a possible support/resistance role reversal and nested pullback, not automatically as a new unrelated trend.

## H1/H2 quality definition (research candidate)

- Separate the H1/H2 count from the quality of a tradable setup. A small local high break in the middle of a range may be recorded as a low-quality count, but it is not automatically a trade.
- Give priority to higher-timeframe background, structural location, and pressure asymmetry. For Daily H1/H2, require Daily EMA20 and EMA50 to slope upward; for Daily L1/L2, require both to slope downward. The preferred bullish pullback location is a rising EMA20/EMA50, prior low/support or prior-high role reversal; the preferred bearish pullback location is a falling EMA20/EMA50, prior high/resistance or prior-low role reversal. A pre-existing breakout retest, range edge, gap edge, or META confluence zone can add context, but an EMA touch alone is not a setup.
- META（Multiple Edge Trading Area）表示至少两个独立来源在同一价格区域汇聚，例如方向一致的 EMA、前高/前低、支撑/阻力、角色转换或缺口边缘。把它画成一个区域并记录组成来源；它只增强合格候选的质量，不覆盖 EMA 方向闸门、信号、首障碍、事件或结构止损。
- A stronger candidate has weak, overlapping pullback selling and a signal K that either closes strongly near its high or rejects lower prices at support and then confirms above its high. A doji or long lower tail alone is insufficient.
- Keep the setup/count bar separate from the confirmation/trigger bar. A strong confirmation bar cannot retroactively make a large opposite-direction setup bar a high-quality bullish signal; classify that sequence as conditional until the bar sequence, location, and follow-through are reviewed together.
- Treat a strong bear pullback, range-middle location, late climax, nearby major resistance, poor space, and event risk as downgrade or no-trade evidence.
- This is a research definition, not yet a fixed production rule. See `research/h1_h2_quality_definition_CN.md`.
- The first three TSLA ABC/H1-H2 comparisons are recorded in `research/tsla_abc_h1_h2_comparison_matrix.md`. The current common finding is that pattern quality and Daily tradeability must be scored separately; the first obstacle can invalidate an otherwise attractive setup.
- The KLAC visual pair is recorded in `research/klac_h2_case_study_2025-05-07_2025-06-03.md` and `research/klac_h1_case_study_2025-10-14_2025-10-24.md`: the former is a repeated-support H2 candidate, while the latter preserves two branches—strict nearby-high no-trade and a conditional strong-trend/magnet branch. The latter requires strong A, one-day shallow B, weak follow-through from sellers and nested trend context; it does not delete the first-obstacle rule. They are comparison evidence, not a fixed rule or a duplicated Codex Trading implementation.
- The first symmetric TSLA short sample is recorded in `research/tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md`: the corrected structural timeline starts with A candidate `2025-01-31`–`2025-02-11`, B `2025-02-12`–`2025-02-19`, and an early L2/second-attempt candidate on `2025-02-20`; the later `2025-03-03`–`2025-03-10` section is a continuation subcase. L1/L2 still follow the same location, trigger, first-obstacle, and R/R discipline; L3 is not an automatic reversal label.
- The stronger TSLA bearish ABC/L1-L2 case is recorded in `research/tsla_bearish_abc_case_2024-07-11_2024-08-05.md`: the A direction is strong but partly earnings-driven, the `233–235` zone acts as resistance, and `2024-07-30`/`2024-08-01` provide the L1/L2 comparison. The `2024-08-01` L2 research branch is roughly `1.5R` to the first `214.71–215` support, so it is a useful positive-space benchmark, but not a clean no-event baseline.
- The clean no-earnings TSLA local ABC case is recorded in `research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md`: three strong bear bars form A, a weak bounce forms B, `2024-03-12` is a failed L1, and `2024-03-13` provides the clearer L2. It occurs near a local range top, so it is a range-edge reversal sample rather than a mid-trend continuation sample. The pre-entry left support at `2023-04-26/27` (`152.37–153.75`) gives roughly `1.6–1.9R` research space from the audited trigger/stop geometry; the `153.93` measured move overlaps that same support cluster and is not a second independent edge. This is a no-event positive-space benchmark, not a validated win-rate or production rule.
- The TSLA `2025-12-12` H2-like study is recorded in `research/tsla_h1_h2_case_study_2025-12-08_2025-12-12.md`: strong A, two EMA20-area tests, and a visually acceptable H2-like signal, but the visible `467–474` left-side high cluster leaves less than about `0.5R` even under an aggressively narrow stop assumption. It is a multi-timeframe visual no-trade filter, not a failed pattern.
- The independent MAR `2026-06-18`–`2026-06-25` 4H-like review is recorded in `research/mar_4h_l1_case_study_2026-06-18_2026-06-25.md`: an upside-to-downside transition, strong A, B rebound and L1/L2-like continuation are visually plausible, but pre-entry `377.8–380.8` support leaves only about `0.04–0.3R`. It is a cross-symbol first-support no-trade sample; the 4H attempt count remains pending rather than copied from Codex Trading.
- The independent ANET `2024-05-16`–`2024-06-10` H3/L3 boundary is recorded in `research/anet_h3_l3_case_study_2024-05-16_2024-06-10.md`: the second push expands rather than weakens, while the third push later slows near `72.3–72.8` support. Keep it as C-class continuation/climax risk plus support-reaction evidence, not a confirmed three-push reversal.
- The TSLA bearish ABC comparison matrix is recorded in `research/tsla_bearish_abc_comparison_matrix.md`: it ranks the clean range-edge sample, the event-driven strong sample, the strongest mid-trend sample, and the weaker/overlapping candidates so the next review does not treat every three-part decline equally.
- The next TSLA bearish ABC candidate screen is recorded in `research/tsla_bearish_abc_candidate_screen_2026-08-22.md`: `2026-02-11` → `2026-03-03` → `2026-03-11` → `2026-03-30` is structurally clear and reaches a first measured-move projection near `365`, but its visible `389.95–385.39` support cluster leaves only about `0.22–0.61R` at the L1/L2 decision points. Treat it as a strong-pattern / no-trade filter study, not a ready-made trade.
- The post-climax continuation is recorded in `research/tsla_range_after_sell_climax_2025-03-11_2025-05-13.md`: a broad parent range, lower/upper edge tests, second-leg trap risk, and breakout acceptance must be separated.

## Order and risk principles

八个主动 pattern 的订单合同与 R/R 分支见[`八个 Pattern 的订单合同与 R/R 审计`](../research/order_contract_cross_pattern_audit_CN.md)；形态、触发、成交和结果必须分开记录。

- Initial default for H1/H2/L1/L2 and breakout-pullback setups: use a stop entry after a valid signal.
- Market or close entry may be considered after a strong breakout, but slippage and wider stops must be accepted.
- A sell stop waits for price to move down through the trigger; a sell limit waits for price to rebound up to the limit. A limit order placed below the live market is marketable and may fill immediately; it is not a substitute for a downside sell stop.
- Limit/retest entries at a structural resistance or support edge can be researched as a separate branch, but the order must be placed only after the retest context is known. Do not merge its statistics with the original breakout-stop branch.
- A gap through a stop trigger changes the actual fill, risk, and first-obstacle geometry. Recalculate the trade; do not backfill the intended trigger price.
- Limit entries at range edges, measured-move targets, or reversal points are advanced and remain a later research topic. The TSLA `2025-03-04` post-gap resistance retest is an example for research, not a fixed production rule.
- Every setup must specify the stop, first obstacle, target, and failure condition before it can be considered for backtesting.

## Trade-plan checklist

For every candidate trade, record all of the following before entry:

- Entry: exact trigger price and order type; a signal bar alone is not an entry.
- Stop: structural invalidation level, with enough room for a normal test; do not place it inside a known support/resistance zone.
- First obstacle: the nearest independent support/resistance or measured-move area.
- Risk/reward: at least 1R of space to the first obstacle for a viable candidate; a complete swing idea should normally offer at least 2R.
- Target: first scale/management target and larger measured-move or structural target.
- Signal-bar quality: close, tail, overlap, follow-through expectation, and whether it is a climax or shock bar.
- Volatility and position size: the stop distance must match current volatility and the planned account risk.
- Sector/background filter: for a stock, check the relevant sector ETF or broader market. Prefer alignment and avoid taking a strong single-stock trade directly against a weak sector without a specific reason.
- Event risk: earnings, major economic releases, gaps, and other known events can invalidate ordinary chart geometry.
- Earnings rule: do not open a new position within the three trading sessions before a scheduled earnings release. The purpose is to avoid gambling on the report and the event-driven gap. Management of an already-open position is a separate decision and must not be silently treated as a new entry.
- 财报、板块和 Daily/4H/60m/15m 的统一前置闸门见[`财报、板块与多周期前置过滤`](../research/event_sector_multitimeframe_cross_pattern_audit_CN.md)，八个 pattern 进入形态审计前先记录数据状态和许可结果。
- Invalidation: state what price action proves the setup wrong before entering.

The `72.00` stop used in the KLAC H2 study is a structural research example, not a universal price rule. The same checklist must be recalculated for each instrument and timeframe.

## Support/resistance strength hierarchy (visual working version)

支撑和阻力按**区域**而不是单一价格线记录。下面是研究时的默认强度顺序；它是视觉优先级，不是保证价格一定在那里反转。

所有 pattern 共用的基础位置层见[`Support / Resistance`](../foundations/01_support_resistance/README.md)；跨 pattern 分流见[`支撑/阻力强度与八个 Pattern 的位置审计`](../research/support_resistance_cross_pattern_audit_CN.md)，专项证据审计见[`Support / Resistance 专项视觉证据审计`](../research/support_resistance_visual_evidence_gap_audit_2026-08-24_CN.md)。

| 层级 | 优先观察的结构 | 说明 |
| --- | --- | --- |
| `major` | 大周期主要摆动高/低点、成熟交易区间上沿/下沿、明显的支撑转阻力/阻力转支撑、多个周期重合且离开力度大的区域 | 最先检查；如果与入场方向之间空间不足，通常直接否决或降级交易 |
| `intermediate` | 清楚的次要摆动点、失败突破区、缺口边缘/起涨起跌区、通道边界、得到价格反复验证的 EMA20/EMA50 区域 | 可作为第一道独立障碍或 META 汇合项，但要看是否真的被价格接受/拒绝 |
| `local` | 单个局部高低点、单根 K 线极值、孤立 EMA 触碰、未经价格反应确认的趋势线或数学投影 | 主要用于低周期管理和触发，不应单独压过 major/intermediate 结构 |

补充纪律：

- 同一价格簇中的前高、MM、缺口边缘和 EMA 只算一个主要障碍，不能重复计数；
- 强度排序不等于距离排序。第一障碍仍是从入场方向看**最先遇到的独立区域**，不能跳过近端 local/intermediate 区域直接使用更远的 major/MM；
- 低周期局部位不能自动替代 Daily/4H 结构止损或主要障碍；若采用低周期 thesis，必须单独记录交易假设；
- 区域被有效接受后，原支撑/阻力角色可能转换；影线刺破但收盘收回，先记录为测试，不自动视为结构穿越；
- 缺口、50% 回调、EMA 或 MM 只有在价格结构和位置共同支持时才提高质量，不能单独构成入场理由。

## Profit management around measured moves

- The cross-pattern visual contract is [`Measured Move / AB=CD / 磁铁目标管理`](../foundations/02_measured_move_targets/README.md); its evidence audit is [`Measured Move / AB=CD / 磁铁视觉证据审计`](../research/measured_move_visual_evidence_gap_audit_2026-08-24_CN.md).
- A measured move is a target zone, not a price that must be touched exactly.
- When price enters the target area and momentum weakens, partial profit-taking is reasonable even if the exact projection has not been reached.
- Useful weakening evidence includes smaller bodies, more overlap, failed follow-through, repeated upper tails, and a mature channel near resistance.
- A practical research template is to reduce part of the position near the first target zone, keep a smaller remainder for the exact target or extension, and exit the remainder on a clear reversal or structural failure.
- Do not hold the entire position solely to capture the last few cents of a measured move when the first obstacle and risk geometry already justify reducing exposure.

## Resistance-first hierarchy before measured moves

This is a current research hypothesis and operating principle, not yet a statistically validated production rule:

- Rank a pre-existing major support/resistance zone before using a measured move. A measured move is a projection; it does not erase a known obstacle.
- If the current leg approaches a prior major high and forms a double top, especially where an older high/low role reversal created resistance, assume a reaction is more likely than a clean break until acceptance is demonstrated.
- A strong trend can break that resistance, but the exception needs observable evidence: strong closes beyond the zone, follow-through, and preferably a pullback that holds above it. An intrabar wick or one isolated breakout bar is not enough.
- If the breakout outcome is uncertain, do not open a new position solely because the measured move points through the resistance. For an existing position, treat the zone as the first management area: consider partial reduction, keep only a defined remainder, or wait for acceptance/retest before adding.
- Position-management actions must be predeclared for the setup; this principle does not create a universal breakeven or time-stop rule.
- If the first major resistance leaves inadequate R/R, the correct action is no trade or reduced exposure. Only after the obstacle is cleared should the measured move become the next primary target.

## Failed breakout versus climactic reversal

The compact visual framework is [`Failed breakout / climax reversal visual framework`](../research/failed_breakout_climax_visual_framework_CN.md).

- A failed breakout requires a pre-existing boundary and evidence that price was not accepted beyond it. A wick or one opposite bar is only a test or candidate, not confirmation.
- A climax is late expansion or acceleration; it can lead to a small reversal, a trading range, or continuation. Do not fade a climax without location, structural damage, follow-through and space.
- The first reverse move is usually evidence of a reversal attempt, not proof of MTR. Keep waiting for a second entry, a retest that holds, or equivalent structural confirmation.
- If the original direction closes strongly beyond the boundary and follows through, reclassify the setup as BOP/acceptance and invalidate the failed-breakout thesis.
- The first independent support/resistance and structural stop still outrank the measured move. If the first obstacle is too close, record `valid_no_trade` even when the pattern looks visually clean.

## Pre-breakout resistance versus post-breakout acceptance

The compact visual framework for BOP, gap-and-go, and breakout pullbacks is [`BOP / gap acceptance visual framework`](../research/bop_gap_acceptance_framework_CN.md).

A resistance setup and a breakout setup are different states of the market:

- Before acceptance above a major resistance, a double top or three/four-push approach is a reason to expect a reaction and remain flat. A short is a separate hypothesis and still requires an actual bearish trigger; the shape alone is not a short entry.
- When price closes decisively beyond the pre-identified resistance, has limited upper rejection, and shows 15m/1H follow-through or a successful hold above the zone, reclassify the idea as a breakout-pullback/acceptance setup. Do not keep treating it as the old double top after the market has invalidated that premise.
- A strong breakout can justify a new entry even if the anticipated pullback never arrives. That entry is a separate BOP decision, not a retroactive H1/H2 entry.
- If the breakout bar is unusually wide relative to recent volatility, use a lower-timeframe trigger or reduced initial risk. Do not use normal size simply because the close is strong.
- If the next session gaps into another major resistance zone, recompute the actual fill, stop, and first-obstacle R/R. If the gap removes the space, skip the new trade rather than carrying forward the old theoretical entry.
- A breakout thesis is working while price accepts above the zone and produces follow-through; it is warning when price repeatedly returns to the zone; it is invalid when price accepts back below it.

## Retracement-depth confluence

- A 50% retracement of a prior impulse is an important observation level in Brooks-style analysis, but it is not a mandatory entry rule by itself.
- Its value increases when it overlaps with repeated prior lows/highs, a known support/resistance zone, an EMA test, a measured-move reference, and a clear H1/H2 or L1/L2 attempt.
- In the KLAC study, the `2025-05-23` and `2025-05-30` lows were near the same support area; the first test was near EMA20 and the later test approached the 50% retracement before recovering above EMA20.
- This is best recorded as confluence: impulse + retracement depth + repeated level + moving-average recovery + second attempt. The 50% measurement remains an important but non-required reference.

## Research status

### Relatively clear

- The role of PA Research versus Codex Trading.
- The importance of market context and major support/resistance.
- H1/H2, L1/L2, second entries, 80/20 context, and measured-move use.
- The ten-pattern article as a useful Brooks research index.

### Still unresolved

- A precise operational definition of ABC for our own use.
- The exact conditions that distinguish valid H3/L3 setups from ordinary range noise.
- The minimum quality standard for a high-quality or high-probability setup.
- How to grade location, space, signal-bar quality, and follow-through consistently across a sufficiently large sample.
- Which patterns should be promoted from research hypothesis to programmatic rule.

## Working agreement

When a definition is uncertain, state the uncertainty instead of silently assuming. Distinguish Brooks' original wording, our interpretation, and any untested hypothesis. Use chart examples to resolve ambiguity, then update this document and the relevant strategy note.

优先 Pattern 的代表性候选与对照矩阵见[`优先 Pattern 代表性视觉候选矩阵`](../research/priority_pattern_visual_candidate_matrix_2026-08-24_CN.md)：完整图表先快筛，跨 pattern 只保留一个主标签，再审计订单、首障碍、状态切换和过程路径。

BOP 的多日回踩必须与同日盘中回调、gap-and-go 和缺口重订分开；专项审计见[`BOP 真实多日回踩候选审计`](../research/bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)。

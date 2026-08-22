# PA Research — Common Context

This document is the shared working context for the PA Research project. It records the current research boundaries, definitions, and unresolved questions so that future discussions do not depend on repeatedly reconstructing the same background.

## Project purpose

PA Research is the research and visual-structure layer. Its job is to study charts, organize Al Brooks Price Action concepts, compare examples, and turn observations into clear, testable hypotheses.

It is not yet the live trading system and does not place orders. Mature rules may later be transferred to Codex Trading for implementation and backtesting, and only then considered for execution automation.

## Visual-first research doctrine

完整图表的视觉判断是本项目最重要的能力和主要工作流。研究必须先回答“左侧发生了什么、当前处在趋势/区间/过渡的哪一部分、支撑阻力和压力如何组织”，再讨论 ABC、H/L 计数和订单。

- Daily、4H/60m、15m 等周期用于建立层级背景和触发上下文；能看到的范围、周期和数据完整性必须写清楚。
- Futu OpenD、历史 K 线和计算结果只用于测量、核对时间顺序、量价、R/R 和执行细节；它们不能替代完整图表的结构解释。
- 扫描器、指标或单个 K 线标签不能单独证明 ABC、H1/H2/H3、L1/L2/L3 或“高胜率”。
- 如果只能取得结构化数据而没有足够的图表上下文，结论必须标为“数据审计/候选”，不能写成完整视觉判断。
- 研究文件应把“视觉结构判断”和“数值核验”分栏记录，避免为了方便回测而把主观结构偷偷改写成伪精确阈值。

## Research phases: visual discovery before quantification

当前阶段不是量化建模，而是建立一个真正看得懂 Price Action 图表的研究助手。研究顺序分三层：

1. **视觉发现层**：在完整图表上先筛选“看起来像”的候选，优先判断背景、左侧结构、A/B/C、H/L1-3、位置和压力变化。此阶段允许保留模糊边界，粗略画出可能的入场、结构止损和目标区域，不宣称胜率。
2. **结构优化层**：对筛出的优质候选，再核对同周期计数、信号 K、触发、主要支撑/阻力、事件边界和大致 R/R；把相似形态、失败形态和不应交易的形态并排比较。
3. **程序验证层**：只有当视觉规则已经稳定、边界足够清楚，才考虑把少数规则交给 Codex Trading 做数据回放或量化测试。它不是当前阶段的默认工作流。

因此，候选文件可以先用 `visual_candidate` 或 `pattern_like` 状态进入研究库；“看起来像”是筛选入口，不是最终规则，也不需要一开始就精确到固定阈值。

## Repository boundaries

- `PA Research`: research notes, source-aligned definitions, chart reviews, hypotheses, and validated rule specifications.
- `Codex Trading`: programmatic research tools, Trading System implementation, backtesting, and Execution Agent work.
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

## Immediate research scope: ABC and H/L1-3

For the current research phase, temporarily prioritize the ABC pullback framework and H1/H2/H3, L1/L2/L3 attempts. Breakout trading remains a separate later topic and should not be mixed into the current H/L count studies.

- `A` is the directional impulse or trend leg; `B` is the pullback; `C` is the possible resumption leg.
- `A` is also a retrospective structural label, not the date when live research begins. Once directional pressure is recognizable, immediately evaluate the next B pullback and H/L attempts. Do not wait for C to finish or for the whole ABC to become visually complete. Every case should record both the earliest recognizable A date and the actual decision/trigger date.
- `H1`, `H2`, and `H3` are successive bull attempts within the same pullback context. `L1`, `L2`, and `L3` are the symmetric bear attempts.
- A count is only meaningful when it belongs to the same timeframe and the same pullback leg. Do not combine a Daily H2 with a 15m H2 as if they were one count.
- H3/L3 are the third-attempt research category. When the three attempts weaken, occur at a meaningful edge, and show pressure exhaustion, they may overlap with a three-push wedge/reversal. The number `3` alone does not prove a wedge or a reversal; in a strong trend, a third attempt can still continue.
- Inside a mature trading range, do not force ABC or H/L leg continuity onto every swing. Use the range's upper edge, lower edge, failed breakouts, tests, and second entries first. A range-edge reaction that visually resembles H2/L2 is not automatically a trend H2/L2.
- Only after a clear directional breakout/acceptance and a subsequent pullback/retest should a new first leg and second leg be evaluated as a trend-continuation structure. The initial range-edge trade and the later post-breakout second leg must remain separate hypotheses.
- Do not count every small intrabar high/low. A count should represent a meaningful attempt at a relevant location, followed by a signal and confirmation review.
- Keep setup/count bars separate from confirmation/trigger bars. H1/H2/H3 or L1/L2/L3 identify the attempt sequence; they do not authorize an order by themselves.
- The current study order is: larger background → A pressure → B pressure → major/minor support-resistance → H/L attempt count → signal K → trigger → stop/invalidation → first obstacle and measured-move space.
- For a live review, the sequence is not “find the completed A/B/C first.” It is: recognize A pressure while it is developing, start scanning the B pullback immediately, then decide whether the next H/L attempt is tradable. A later retrospective label must not erase an earlier valid decision window.
- Candidate priority follows A-leg quality: when the trend and A leg are strong, the first valid H1/L1 signal K after a controlled pullback may be researched; when A is ordinary, overlapping, or ambiguous, H1/L1 is observation-only and preference shifts to H2/L2 after the first attempt fails or lacks follow-through. This is a research priority, not a guaranteed probability rule.
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

- H1/H2/H3 and L1/L2/L3, understood as context-dependent pullback attempts rather than rigid labels.
- Trading-range top shorts and bottom longs, especially second entries.
- Major trend reversals, recorded now but analyzed in depth later.
- Final flags, breakouts, channels, wedges, measured moves, opening reversals, and magnets/support-resistance, following Brooks' flexible pattern language.
- Measured Move and AB=CD are space and target tools, not standalone entry signals.
- EMA is supporting context only; touching the EMA is not a pattern by itself.

## Probability principles

The probability table is treated as conditional experience-based guidance, not guaranteed win rates. In particular:

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
- Give priority to higher-timeframe background, structural location, and pressure asymmetry. The preferred location is a pre-existing support, EMA20/EMA50 test with directional acceptance, breakout retest, range edge, gap edge, or META confluence zone.
- A stronger candidate has weak, overlapping pullback selling and a signal K that either closes strongly near its high or rejects lower prices at support and then confirms above its high. A doji or long lower tail alone is insufficient.
- Keep the setup/count bar separate from the confirmation/trigger bar. A strong confirmation bar cannot retroactively make a large opposite-direction setup bar a high-quality bullish signal; classify that sequence as conditional until the bar sequence, location, and follow-through are reviewed together.
- Treat a strong bear pullback, range-middle location, late climax, nearby major resistance, poor space, and event risk as downgrade or no-trade evidence.
- This is a research definition, not yet a fixed production rule. See `research/h1_h2_quality_definition_CN.md`.
- The first three TSLA ABC/H1-H2 comparisons are recorded in `research/tsla_abc_h1_h2_comparison_matrix.md`. The current common finding is that pattern quality and Daily tradeability must be scored separately; the first obstacle can invalidate an otherwise attractive setup.
- The first symmetric TSLA short sample is recorded in `research/tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md`: the corrected structural timeline starts with A candidate `2025-01-31`–`2025-02-11`, B `2025-02-12`–`2025-02-19`, and an early L2/second-attempt candidate on `2025-02-20`; the later `2025-03-03`–`2025-03-10` section is a continuation subcase. L1/L2 still follow the same location, trigger, first-obstacle, and R/R discipline; L3 is not an automatic reversal label.
- The stronger TSLA bearish ABC/L1-L2 case is recorded in `research/tsla_bearish_abc_case_2024-07-11_2024-08-05.md`: the A direction is strong but partly earnings-driven, the `233–235` zone acts as resistance, and `2024-07-30`/`2024-08-01` provide the L1/L2 comparison. It is a strong-pattern case, not the clean no-event baseline.
- The clean no-earnings TSLA local ABC case is recorded in `research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md`: three strong bear bars form A, a weak bounce forms B, `2024-03-12` is a failed L1, and `2024-03-13` provides the clearer L2. It occurs near a local range top, so it is a range-edge reversal sample rather than a mid-trend continuation sample.
- The TSLA bearish ABC comparison matrix is recorded in `research/tsla_bearish_abc_comparison_matrix.md`: it ranks the clean range-edge sample, the event-driven strong sample, the strongest mid-trend sample, and the weaker/overlapping candidates so the next review does not treat every three-part decline equally.
- The next TSLA bearish ABC candidate screen is recorded in `research/tsla_bearish_abc_candidate_screen_2026-08-22.md`: `2026-02-11` → `2026-03-03` → `2026-03-11` → `2026-03-30` is structurally clear and reaches a first measured-move projection near `365`, but its Daily L1/L2 first-obstacle R/R is not automatically adequate. Treat it as a pattern-and-filter study, not a ready-made trade.
- The post-climax continuation is recorded in `research/tsla_range_after_sell_climax_2025-03-11_2025-05-13.md`: a broad parent range, lower/upper edge tests, second-leg trap risk, and breakout acceptance must be separated.

## Order and risk principles

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
- Invalidation: state what price action proves the setup wrong before entering.

The `72.00` stop used in the KLAC H2 study is a structural research example, not a universal price rule. The same checklist must be recalculated for each instrument and timeframe.

## Profit management around measured moves

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

## Pre-breakout resistance versus post-breakout acceptance

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

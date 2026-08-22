# PA Research — Common Context

This document is the shared working context for the PA Research project. It records the current research boundaries, definitions, and unresolved questions so that future discussions do not depend on repeatedly reconstructing the same background.

## Project purpose

PA Research is the research and visual-structure layer. Its job is to study charts, organize Al Brooks Price Action concepts, compare examples, and turn observations into clear, testable hypotheses.

It is not yet the live trading system and does not place orders. Mature rules may later be transferred to Codex Trading for implementation and backtesting, and only then considered for execution automation.

## Repository boundaries

- `PA Research`: research notes, source-aligned definitions, chart reviews, hypotheses, and validated rule specifications.
- `Codex Trading`: programmatic research tools, Trading System implementation, backtesting, and Execution Agent work.
- The reference material in the existing Codex Trading knowledge base is read-only during research unless a rule has matured and transfer work is explicitly in scope.

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
- `H1`, `H2`, and `H3` are successive bull attempts within the same pullback context. `L1`, `L2`, and `L3` are the symmetric bear attempts.
- A count is only meaningful when it belongs to the same timeframe and the same pullback leg. Do not combine a Daily H2 with a 15m H2 as if they were one count.
- H3/L3 are the third-attempt research category. When the three attempts weaken, occur at a meaningful edge, and show pressure exhaustion, they may overlap with a three-push wedge/reversal. The number `3` alone does not prove a wedge or a reversal; in a strong trend, a third attempt can still continue.
- Do not count every small intrabar high/low. A count should represent a meaningful attempt at a relevant location, followed by a signal and confirmation review.
- Keep setup/count bars separate from confirmation/trigger bars. H1/H2/H3 or L1/L2/L3 identify the attempt sequence; they do not authorize an order by themselves.
- The current study order is: larger background → A pressure → B pressure → major/minor support-resistance → H/L attempt count → signal K → trigger → stop/invalidation → first obstacle and measured-move space.

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
- The first symmetric TSLA short sample is recorded in `research/tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md`: L1/L2 follow the same location, trigger, first-obstacle, and R/R discipline; L3 is not an automatic reversal label.

## Order and risk principles

- Initial default for H1/H2/L1/L2 and breakout-pullback setups: use a stop entry after a valid signal.
- Market or close entry may be considered after a strong breakout, but slippage and wider stops must be accepted.
- Limit entries at range edges, measured-move targets, or reversal points are advanced and remain a later research topic.
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

# PA Research — Common Context

This document is the shared working context for the PA Research project. It records the current research boundaries, definitions, and unresolved questions so that future discussions do not depend on repeatedly reconstructing the same background.

## Project purpose

PA Research is the research and visual-structure layer. Its job is to study charts, organize Al Brooks Price Action concepts, compare examples, and turn observations into clear, testable hypotheses.

It is not yet the live trading system and does not place orders. Mature rules may later be transferred to Codex Trading for implementation and backtesting, and only then considered for execution automation.

## Repository boundaries

- `PA Research`: research notes, source-aligned definitions, chart reviews, hypotheses, and validated rule specifications.
- `Codex Trading`: programmatic research tools, Trading System implementation, backtesting, and Execution Agent work.
- The reference material in the existing Codex Trading knowledge base is read-only during research unless a rule has matured and transfer work is explicitly in scope.

## Core framework

The primary framework is Al Brooks Price Action. Elliott Wave theory is not part of the main framework. ABC is used only as an operational Price Action description when useful: a first leg, a pullback, and a resumption leg.

The main context questions are:

1. Is the market trending, ranging, or transitioning?
2. Where are the major and minor support/resistance zones?
3. What is the current pressure: continuation, failed breakout, climax, or reversal attempt?
4. Which Price Action pattern is forming?
5. What is the entry trigger, stop, first obstacle, target, and invalidation?

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
- Invalidation: state what price action proves the setup wrong before entering.

The `72.00` stop used in the KLAC H2 study is a structural research example, not a universal price rule. The same checklist must be recalculated for each instrument and timeframe.

## Profit management around measured moves

- A measured move is a target zone, not a price that must be touched exactly.
- When price enters the target area and momentum weakens, partial profit-taking is reasonable even if the exact projection has not been reached.
- Useful weakening evidence includes smaller bodies, more overlap, failed follow-through, repeated upper tails, and a mature channel near resistance.
- A practical research template is to reduce part of the position near the first target zone, keep a smaller remainder for the exact target or extension, and exit the remainder on a clear reversal or structural failure.
- Do not hold the entire position solely to capture the last few cents of a measured move when the first obstacle and risk geometry already justify reducing exposure.

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
- How to grade location, space, signal-bar quality, and follow-through consistently.
- Which patterns should be promoted from research hypothesis to programmatic rule.

## Working agreement

When a definition is uncertain, state the uncertainty instead of silently assuming. Distinguish Brooks' original wording, our interpretation, and any untested hypothesis. Use chart examples to resolve ambiguity, then update this document and the relevant strategy note.

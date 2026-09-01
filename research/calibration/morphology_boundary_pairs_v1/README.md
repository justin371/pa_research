# 形态边界正反例对校准包 v1

日期：2026-09-01
状态：`curated / reused-prior-blind-images / label-hidden / outcome-hidden / calibration-only`

```text
contract_scope: historical_context_only
data_status: historical
as_of_time: per-source-sample cutoff in the original frozen manifest
timezone: America/New_York where preserved by the source snapshot
session_state: historical_close
timeframes_seen: Daily
chart_scope: full
daily_context_window: >=2y
major_high_low_review: visually_available
ema20_50_200_review: visually_available
direction: no_valid_direction
lineage_status: pending
internal_label: pending
research_state: observation_only
trade_state: observation_only
gate_result: observation_only
handoff_status: not_ready
```

本包复用此前已经冻结、未来隐藏的 12 张中性编号 Daily 图，不新增或筛选市场标的。它是根据旧盲审暴露出的边界问题人工策划的教学/校准 cohort，不是新 holdout，也不能用于报告识别准确率或泛化能力。

Reviewer-first 顺序：

1. 先逐图独立填写 `parent_state / direction / A / B / breakout acceptance / lineage / family / attempt / EMA / stage / disposition`；
2. 两张图的逐图标签冻结后，才填写同一 pair 的最小决定性差异；
3. 不打开旧盲审、裁决、来源 manifest、未来价格或交易结果；
4. 不把 pair 中任一张预设为“正确例”，也不假设两张一定属于不同 family。

Pair 清单只显示中性编号：

- `PB1-001A / PB1-001B`
- `PB1-002A / PB1-002B`
- `PB1-003A / PB1-003B`
- `PB1-004A / PB1-004B`
- `PB1-005A / PB1-005B`
- `PB1-006A / PB1-006B`

具体图路径保存在 [manifest](manifest.json)；manifest 不包含方向、family、B 腿答案、结果或未来路径。

```text
PA Research only
no Codex Trading
no quantitative scanner
no automatic pattern detector
no Futu/OpenD
no Execution Agent
conclusion: no-new-positive
validated win-rate: not-computable
```

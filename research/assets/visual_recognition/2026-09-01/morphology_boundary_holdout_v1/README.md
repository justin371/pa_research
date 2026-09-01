# 形态边界决策卡 Holdout v1（reviewer package）

日期：2026-09-01
状态：`label_hidden=yes / outcome_hidden=yes / future_bars_hidden=yes / selection_frozen_before_view=yes`

```text
cohort_id: deterministic_boundary_holdout
contract_scope: historical_context_only
data_source: repository historical Daily OHLCV snapshots listed in manifest.json
data_status: historical
as_of_time: per-sample cutoff in manifest.json
timezone: America/New_York where preserved by the source snapshot
session_state: historical_close
timeframes_seen: Daily
chart_scope: full
daily_context_window: >=2y
major_high_low_review: visually_available
ema20_50_200_review: visually_available
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
direction: no_valid_direction
lineage_status: pending
internal_label: pending
label_hidden: yes
outcome_hidden: yes
future_bars_hidden: yes
selection_frozen_before_view: yes
human_expert_status: not_performed
research_state: observation_only
trade_state: observation_only
gate_result: observation_only
handoff_status: not_ready
```

本目录用于测试形态边界视觉决策卡。12 个 symbol-date 样本由固定 seed 在满足两年 Daily 左侧和至少 40 根隐藏未来 K 线的价格行中确定性选出；exact symbol-date 不与前两批盲测重叠。选择不读取 pattern、候选标签、未来路径或回放结果。

Reviewer 只打开分配到的 PNG，不打开 manifest、旧研究报告、合同、未来价格或其他 reviewer 答案。每张图先按以下顺序判断：

```text
证据完整度
  -> parent_state
  -> BOP breakout acceptance
  -> range edge / third push
  -> A/B quality and lineage
  -> ordinary H1/H2/L1/L2 attempt
  -> selection disposition
```

图表清单：

- `BH1-001.png`
- `BH1-002.png`
- `BH1-003.png`
- `BH1-004.png`
- `BH1-005.png`
- `BH1-006.png`
- `BH1-007.png`
- `BH1-008.png`
- `BH1-009.png`
- `BH1-010.png`
- `BH1-011.png`
- `BH1-012.png`

本批次只测模型 reviewer 之间的视觉一致性，不建立人工专家真值，不查看结果，不计算交易胜率或盈亏比。

```text
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
conclusion: no-new-positive
validated win-rate: not-computable
```

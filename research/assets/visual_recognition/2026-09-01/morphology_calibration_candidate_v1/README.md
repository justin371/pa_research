# PA Research 形态覆盖盲审候选集 v1

日期：2026-09-01
状态：`historical / outcome-hidden / label-hidden / candidate-not-ground-truth / calibration-only`

```text
cohort_id: curated_morphology_cohort
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
expert_adjudication: pending
research_state: observation_only
trade_state: observation_only
gate_result: observation_only
handoff_status: not_ready
```

本目录保存 16 张中性编号的历史 Daily 图。上图显示最多 504 根已完成 Daily K 线，下图放大最后 120 根；EMA20/50/200、原始成交量、两年内主要高低点和支撑阻力位置都可直接观察。截止日之后至少 40 根 Daily 被隐藏。

这是一组**形态覆盖候选图**，不是标准答案集。候选来源与类别信息和本目录隔离；旧合同只负责提出可能值得复核的日期，不能替代独立专家裁决。主 Agent 在构造候选集时接触过旧标签，因此其本轮视觉笔记属于 `knowledge_contaminated`，不能进入严格一致率分母。

请只看图，按[`盲审表`](review_form.md)记录父级、方向、A/B 质量、H/L-like、三推变形、EMA、位置、第一障碍和主要不确定性。不要打开回放结果或旧案例文字。文件名含中性 sample ID；symbol/date 可见不构成协议定义的标签泄漏，但若你记得同一 symbol/date 的旧结论，应标记 `possibly_contaminated` 或 `contaminated`。

## 图表入口

| Sample | Chart | Sample | Chart |
| --- | --- | --- | --- |
| MC2-001 | [chart](MC2-001.png) | MC2-009 | [chart](MC2-009.png) |
| MC2-002 | [chart](MC2-002.png) | MC2-010 | [chart](MC2-010.png) |
| MC2-003 | [chart](MC2-003.png) | MC2-011 | [chart](MC2-011.png) |
| MC2-004 | [chart](MC2-004.png) | MC2-012 | [chart](MC2-012.png) |
| MC2-005 | [chart](MC2-005.png) | MC2-013 | [chart](MC2-013.png) |
| MC2-006 | [chart](MC2-006.png) | MC2-014 | [chart](MC2-014.png) |
| MC2-007 | [chart](MC2-007.png) | MC2-015 | [chart](MC2-015.png) |
| MC2-008 | [chart](MC2-008.png) | MC2-016 | [chart](MC2-016.png) |

重现命令：

```powershell
py -3 .\scripts\render_pa_blind_daily_batch.py `
  --manifest .\research\assets\visual_recognition\2026-09-01\morphology_calibration_candidate_v1\manifest.json `
  --repo-root . `
  --output-dir .\research\assets\visual_recognition\2026-09-01\morphology_calibration_candidate_v1
```

渲染器只画 manifest 已冻结的历史窗口，不选择股票、不识别 pattern、不评分、不读取未来结果，也不连接 Execution Agent。

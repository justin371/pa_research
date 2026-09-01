# PA Research 选股质量盲测 Batch 1 图表资产

日期：2026-09-01  
状态：`historical / outcome-hidden / label-hidden / calibration-only`

```text
contract_scope: historical_context_only
data_source: repository historical Daily OHLCV snapshots listed in manifest.json
data_status: historical
as_of_time: per-sample cutoff in manifest.json
timezone: America/New_York where preserved by the source snapshot
session_state: historical_close
timeframes_seen: Daily
chart_scope: full
daily_context_window: >=2y
major_high_low_review: visually_available; per-case completion belongs to the frozen prediction record
ema20_50_200_review: visually_available; per-case completion belongs to the frozen prediction record
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
direction: no_valid_direction
lineage_status: pending
internal_label: pending
third_push_state: unclear
range_edge_three_push: pending
range_edge_side: pending
research_state: observation_only
trade_state: observation_only
gate_result: observation_only
handoff_status: not_ready
```

本目录保存 12 张确定性抽样的历史 Daily 图表。每张图只包含截止日以前的 OHLC、原始成交量、EMA20/50/200、约两年 Daily 窗口和 120 根 Daily 局部放大；不包含形态标签、方向、入场、止损、目标、结果或胜负标记。

本批用于测量“从未标注完整图表中发现候选并说明边界”的能力，不是当前选股结果、胜率样本、量化扫描器或交易授权。

本批是**固定历史 symbol 池内的确定性截止日基线**，属于校准协议下的“确定性发现 cohort”基线，但不是全市场随机发现 cohort，也不是按 H1/H2/L1/L2/三推/负例配平的形态 cohort；它可以暴露看图、误选和深审处置问题，但不能单独估计全市场召回率、类别召回率或“识别准确率”。旧资产中存在文件名、README 或图内文字泄漏标签的情况，不能直接拼接成严格类别盲测；后续若建立配平 cohort，必须重新使用中性 sample ID 渲染，并把答案 sidecar 与识别者隔离。

## 抽样与泄漏边界

- 抽样清单：[`manifest.json`](manifest.json)；
- 固定种子：`pa-selection-quality-v1`；
- 每个合格标的截止索引：`SHA256(seed|symbol)` 在合法索引区间内确定；
- 最少事前历史：600 根 Daily；图中最多显示最近 504 根；
- 最少隐藏未来：40 根 Daily；未来数据不进入图像；
- 12 个标的来自仓库既有 PA Research 历史价格资产，不是全市场随机 symbol cohort；每个标的的截止日不根据形态、结果或回放胜负挑选；
- 使用仓库既有历史价格 CSV；没有联网、没有调用 Futu/OpenD，也不能描述为实时行情。

若复核者已经阅读与某个 symbol/date 对应的旧合同、案例或结果，应把该行标记为 `knowledge_contaminated`，不能计入严格盲测一致率。主 Agent 的首次视觉答案已单独冻结在研究记录中；后续专家裁决和结果回放不得反向修改该答案。

## 图表入口

| Sample | Symbol | Cutoff | Chart |
| --- | --- | --- | --- |
| BQ1-CBOE | CBOE | 2025-01-13 | [chart](BQ1-CBOE.png) |
| BQ1-COHR | COHR | 2024-01-04 | [chart](BQ1-COHR.png) |
| BQ1-DDOG | DDOG | 2026-05-28 | [chart](BQ1-DDOG.png) |
| BQ1-MAR | MAR | 2025-11-14 | [chart](BQ1-MAR.png) |
| BQ1-MCHP | MCHP | 2023-02-03 | [chart](BQ1-MCHP.png) |
| BQ1-NDAQ | NDAQ | 2022-12-20 | [chart](BQ1-NDAQ.png) |
| BQ1-RBLX | RBLX | 2024-08-20 | [chart](BQ1-RBLX.png) |
| BQ1-ROST | ROST | 2025-04-23 | [chart](BQ1-ROST.png) |
| BQ1-TOL | TOL | 2022-11-02 | [chart](BQ1-TOL.png) |
| BQ1-TSLA | TSLA | 2024-09-03 | [chart](BQ1-TSLA.png) |
| BQ1-VEEV | VEEV | 2026-04-21 | [chart](BQ1-VEEV.png) |
| BQ1-ZS | ZS | 2022-11-28 | [chart](BQ1-ZS.png) |

重现命令：

```powershell
py -3 .\scripts\render_pa_blind_daily_batch.py `
  --manifest .\research\assets\visual_recognition\2026-09-01\selection_quality_blind_batch1\manifest.json `
  --repo-root . `
  --output-dir .\research\assets\visual_recognition\2026-09-01\selection_quality_blind_batch1
```

该渲染器只复现图像，不选择股票、不识别 pattern、不计算候选分数，也不连接 Execution Agent。

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
daily_context_window: <2y (conservative batch status; see per-sample date spans below)
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

本目录保存 16 张中性编号的历史 Daily 图。上图显示最多 504 根已完成 Daily K 线，下图放大最后 120 根；可观察图窗内的 EMA20/50/200、原始成交量、主要高低点和支撑阻力位置。单张图只画自身截止日及之前的数据，源记录在其后保留至少 40 根 Daily；这不代表多图组合仍保持盲态。

2026-09-03 更正：原先统一写作 `>=2y`，实际 504 根是交易日数量，不保证首末日期跨满两个日历年。本地按 manifest 的 symbol/cutoff 对源 CSV 排序、截取最后 504 行核对如下；该比较不判断交易日是否缺失，也不改变冻结 PNG/manifest。整批按最短跨度保守标记 `<2y`，不能据此宣称所有图都有完整两年背景。

| Sample | 首根可见日期 | 截止日期 | 根数 | 首末日期跨度 |
| --- | --- | --- | --- | --- |
| MC2-001 | 2023-04-20 | 2025-04-23 | 504 | >=2y |
| MC2-002 | 2021-01-19 | 2023-01-18 | 504 | <2y |
| MC2-003 | 2023-03-06 | 2025-03-07 | 504 | >=2y |
| MC2-004 | 2021-04-27 | 2023-04-26 | 504 | <2y |
| MC2-005 | 2021-08-17 | 2023-08-17 | 504 | >=2y |
| MC2-006 | 2023-01-10 | 2025-01-13 | 504 | >=2y |
| MC2-007 | 2020-06-16 | 2022-06-14 | 504 | <2y |
| MC2-008 | 2022-08-18 | 2024-08-20 | 504 | >=2y |
| MC2-009 | 2022-01-14 | 2024-01-18 | 504 | >=2y |
| MC2-010 | 2022-06-21 | 2024-06-21 | 504 | >=2y |
| MC2-011 | 2022-08-31 | 2024-09-03 | 504 | >=2y |
| MC2-012 | 2020-12-21 | 2022-12-20 | 504 | <2y |
| MC2-013 | 2021-03-08 | 2023-03-07 | 504 | <2y |
| MC2-014 | 2020-06-23 | 2022-06-22 | 504 | <2y |
| MC2-015 | 2021-02-04 | 2023-02-03 | 504 | <2y |
| MC2-016 | 2022-01-03 | 2024-01-04 | 504 | >=2y |

这些历史图的上方日期轴被下方价格面板部分遮挡；局部日期和右端 K 线仍可读。新渲染器已修复布局，冻结图不回写。同一 symbol 的多个截止图存在重叠及跨图未来暴露风险，不能将 16 个文件当作 16 次独立盲测；本目录只用于历史校准，不作为无污染准确率研究包。

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

重现命令（仅输出到新的非冻结目录；目标文件已存在时会拒绝，不提供覆盖开关）：

```powershell
py -3 .\scripts\render_pa_blind_daily_batch_bound.py `
  --manifest .\research\assets\visual_recognition\2026-09-01\morphology_calibration_candidate_v1\manifest.json `
  --repo-root . `
  --output-dir .\.codex\artifacts\morphology-candidate-review-20260903
```

渲染器只画 manifest 已冻结的历史窗口，不选择股票、不识别 pattern、不评分、不读取未来结果，也不连接 Execution Agent。

重现指同一历史窗口，不承诺新布局 PNG 与旧 PNG 字节相同。manifest 逐样本冻结源 CSV SHA-256、规范化 504-bar OHLCV 窗口 SHA-256 和行数，并在批次级冻结**当前重现 renderer** 的源码 SHA-256；该值不是旧冻结 PNG 的原始生成程序哈希。每个源 CSV 只打开并读取一次，文件哈希、窗口哈希和 K 线解析都使用同一份不可变字节快照；任一绑定不一致都会在首张图编码前失败。全部样本、截止边界和目标路径先通过校验才开始渲染；已有目标不会覆盖。`MC2/EH1/BH1` 使用纯数字中性编号；身份可见的旧 `BQ1-代码` 仅在后缀与规范化股票代码完全一致时兼容，不能附加形态或结果词。

整批先在目标同卷的临时目录完成编码，再用平台原生的原子 no-replace 目录操作发布到全新的输出目录。若目标目录在预检前已经存在，或在编码期间（包括发布瞬间）被其他进程创建，即使它是空目录也会拒绝，且不会把任何本批文件暴露到目标目录；不支持可靠 no-replace 的平台会关闭发布而不是降级覆盖。设计中没有逐文件回滚，因此不会误删同路径上的外部替换文件。失败批次不能直接作为完整可交付包。

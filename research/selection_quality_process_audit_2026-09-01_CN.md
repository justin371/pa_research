# PA Research 选股质量：发现召回、视觉分层与盲测基线审计（2026-09-01）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only`
结论：`no-new-positive`；`validated win-rate: not-computable`

```text
audit_scope: discovery_recall_visual_triage_and_blind_baseline
current_visual_asset_readmes: 12
current_visual_png_assets: 117
blind_batch_size: 12
blind_batch_type: deterministic_discovery_cohort
expert_adjudication: pending
strict_class_balanced_calibration: not_started
```

## 1. 发现的问题

此前规则已经能够拒绝 EMA 方向不符、强 A 缺失、B 腿失控、父级大区间中部、第一障碍过近和事件未分层的候选；真正影响每日选股质量的剩余问题，是发现池到深审名单之间缺少可审计的召回链：

1. 历史批次多为预先挑选的 H/L 子集，不能证明全市场发现召回；
2. 强 A 但尚未形成 B 的标的容易被误报为 H1/H2，或直接从记录中消失；
3. 深审容量不足与规则硬拒绝没有分开，无法判断“没发现”还是“发现后暂缓”；
4. 旧视觉资产中有些文件名、README 或图内文字泄漏标签，不适合直接组成严格类别盲测；
5. 确定性发现 cohort 与按类别配平的形态 cohort 职责不同，不能用同一个 accuracy 数字混在一起。

这些问题不足以支持放宽规则。应先提高候选召回和记录完整性，再由两年 Daily 深审维持精度。

## 2. 已完成的合同修订

[`每日候选批次与图表审查卡`](../docs/daily_candidate_review_card_CN.md)和[`PA Pattern 视觉筛选协议`](visual_pattern_triage_protocol_CN.md)现在要求每个发现项保留：

- `coverage_bucket`：说明它来自哪个发现覆盖桶；
- `shortlist_rank` 与 `rank_basis`：只做无分数、事前、序数排序；
- `selection_disposition` 与 `disposition_reason`：明确 `deep_reviewed`、`deferred_capacity`、`wait_for_structure`、`rejected_gate`、`duplicate_lineage`、`event_boundary` 或 `insufficient_evidence`；
- 总发现数、Stage 1 数、深审数和各处置数必须对账；
- 强 A 但还没有受控 B 的标的保留为 `wait_for_structure`，不能提前冻结 H1/H2/L1/L2；
- 同一 lineage 的重复窗口仍计入发现流水，但不能重复进入独立样本分母。

[`视觉识别校准协议 v0.1`](../docs/visual_calibration_protocol_v0_1_CN.md)进一步把两类 cohort 分开：确定性发现 cohort 用来测候选召回和误选；类别配平 morphology cohort 用来测 H/L 与三推边界一致性，但不能代表市场 prevalence。

## 3. 首个 outcome-hidden 基线批次

新增[`Batch 1 图表资产`](assets/visual_recognition/2026-09-01/selection_quality_blind_batch1/README.md)、[`固定 manifest`](assets/visual_recognition/2026-09-01/selection_quality_blind_batch1/manifest.json)、[`首次视觉答案`](selection_quality_blind_batch1_predictions_2026-09-01_CN.md)和只负责画图的[`确定性渲染器`](../scripts/render_pa_blind_daily_batch.py)。

12 个标的来自仓库既有 PA Research 历史价格资产，因此不是全市场随机 symbol cohort；每个 symbol 各按 `SHA256(seed|symbol)` 在“至少 600 根事前 Daily、至少 40 根隐藏未来”的合法区间中确定一个截止日。图中只有截止日前 OHLC、成交量、EMA20/50/200、最多 504 根 Daily 全景和 120 根局部放大；没有标签、方向、入场、止损、目标或结果。

首次视觉答案在读取未来路径、回放结果或专家裁决前冻结。初步发现为：4 个优先深审、2 个等待结构、2 个区间边缘观察、4 个硬闸门拒绝。它证明“强 A 发现”和“已经出现可入场 H/L”必须分开，但没有形成新正例、严格内部标签或胜率分母。

## 4. 严格盲测边界

本批不能被描述为最终识别准确率测试：

- 它是固定历史 symbol 池内的确定性截止日基线，既不代表全市场自然发生率，也不保证 H1/H2/L1/L2/三推/负例类别配平；
- symbol 与 cutoff 可见，复核者若记得旧案例必须标记 `knowledge_contaminated`；
- 专家裁决尚未完成，因此不计算一致率、precision、recall 或 confusion matrix；
- 旧资产只有在中性 sample ID 重新渲染、隐藏类别 sidecar、确认图内无 trigger/stop/target/result 后，才能进入严格 morphology cohort；
- 视觉标签一致性与交易结果必须使用不同分母。

下一轮严格校准应优先补足不泄漏的 H1、H2、L1、L2、三推变形和负控，并保留 lineage 独立性。大约 30 张图只能暴露主要识别错误，不能证明交易 edge；胜率仍需要结果发生前冻结、可比、独立的完成交易。

## 5. 当前资产与历史审计口径

新增本批后，仓库当前共有 12 个视觉资产 README、117 张 PNG。2026-08-29/30 的旧审计中“11 个 README / 105 张 PNG”是当时的历史快照，不应事后改写；当前动态 inventory 由本报告和测试守卫。

## 6. 边界结论

```text
discovery_reconciliation_contract: adopted
qualitative_ordinal_ranking: adopted
strong_A_without_B: wait_for_structure
outcome_hidden_discovery_baseline: frozen
expert_adjudication: pending
strict_class_balanced_calibration: not_started
conclusion: no-new-positive
validated win-rate: not-computable
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

本轮没有修改 Codex Trading，没有创建量化扫描器，没有连接 Execution Agent，也没有把历史随机图当成当前交易候选。

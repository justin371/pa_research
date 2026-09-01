# PA Research 形态覆盖候选集 v1 审计（2026-09-01）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only`
结论：`no-new-positive`；`validated win-rate: not-computable`

```text
audit_scope: label_hidden_morphology_candidate_cohort
cohort_id: curated_morphology_cohort
candidate_samples: 16
daily_context_window: >=2y
minimum_hidden_future_bars: 40
candidate_answer_status: isolated_not_ground_truth
main_agent_review_status: knowledge_contaminated_descriptive_only
expert_adjudication: pending
strict_agreement_metrics: not_computable
```

## 完成内容

新增[`形态覆盖盲审候选集 v1`](assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/README.md)、[`中性 manifest`](assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/manifest.json)和[`盲审表`](assets/visual_recognition/2026-09-01/morphology_calibration_candidate_v1/review_form.md)。16 张图均使用 `MC2-###` 中性编号，显示最多 504 根截止日前 Daily 和 120 根局部放大，包含 EMA20/50/200 与原始成交量，并隐藏至少 40 根未来 Daily。

渲染器新增 `explicit_cutoff` 模式，只复现预先指定日期；旧 Batch 1 显式保留 `deterministic_cutoff`。两种模式都要求 `label_hidden=true`、`outcome_hidden=true`，并验证事前历史和隐藏未来数量。该工具不自动找图、不识别 pattern，也不是量化扫描器。

## 覆盖与证据边界

候选源在隔离记录中提出 H1-like、H2-like、L1-like、L2-like、三推变形和相似负控；这里不公开类别分配，避免污染首次盲审。旧冻结合同是**候选发生器**，不是专家真值。尤其是带跳空、扩张段、EMA 转换、父级区间或第一障碍拥挤的样本，必须允许裁决为 `both_reasonable_boundary` 或 `insufficient_chart_evidence`，不能为了类别配平强行判为正例。

主 Agent 在渲染前已接触候选来源标签，因此后续直接看图只完成泄漏、两年背景、EMA 和主要高低点的质量检查；这些读法统一标记 `knowledge_contaminated`，不进入 strict agreement、precision、recall 或 confusion matrix。下一道有效门是由未接触答案的复核者先填写盲审表，再独立裁决。

KLAC 的标准 H3 候选没有进入本批：仓库本地对应价格文件在该截止日前不足 500 根，或截止日后不足 40 根，不能满足本批严格资格。SLB 也没有可复现的 PA Research 本地 Daily 源，因此没有借用外部图或 Codex Trading 资产补数。该缺口如实保留。

## 统计边界

本批按形态覆盖目的挑选，不代表市场自然发生率；16 张图也不是 16 笔冻结交易。专家裁决前不计算识别准确率；触发、结构止损、第一障碍、事件和独立 lineage 未冻结前不进入交易回放。因此本轮没有新的胜率或盈亏比证据。

```text
expert_adjudication: pending
strict_class_coverage_truth: pending
identification_accuracy: not-computable
precision_recall: not-computable
trade_outcome_denominator: 0
conclusion: no-new-positive
validated win-rate: not-computable
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

本轮只修改 PA Research；没有修改 Codex Trading，没有创建自动 pattern detector 或量化扫描器，也没有连接 Execution Agent。

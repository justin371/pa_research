# PA Research 形态覆盖候选集 v1 审计（2026-09-01）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only`
结论：`no-new-positive`；`validated win-rate: not-computable`

```text
audit_scope: label_hidden_morphology_candidate_cohort
cohort_id: curated_morphology_cohort
candidate_samples: 16
daily_context_window: <2y
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

主 Agent 在渲染前已接触候选来源标签，因此后续直接看图只完成泄漏、实际可见背景、EMA 和主要高低点的质量检查；这些读法统一标记 `knowledge_contaminated`，不进入 strict agreement、precision、recall 或 confusion matrix。下一道有效门需要独立的事前冻结、来源隔离和跨图未来隔离，不能仅靠复核者填写 `clean` 后再裁决。

KLAC 的标准 H3 候选没有进入本批：仓库本地对应价格文件在该截止日前不足 500 根，或截止日后不足 40 根，不能满足本批严格资格。SLB 也没有可复现的 PA Research 本地 Daily 源，因此没有借用外部图或 Codex Trading 资产补数。该缺口如实保留。

### 2026-09-03 可见窗口与来源重用更正

504 根交易日不等于两个日历年。源 CSV 对照显示 7/16 张首末日期距满两年少 1–2 天，逐图日期见已有候选集 README，整批保守标记 `<2y`；这不是源数据缺失交易日的结论。股票代码和截止日期可见，中性 sample ID 不等于身份隐藏。

与 `selection_quality_blind_batch1` 的 manifest 逐项比对，以下 7 组使用相同的规范化 symbol、cutoff 和 504-bar OHLCV 源窗口；校验不依赖 CSV 文件名，因此复制或改名同一源窗口仍会被识别：

| 本批 | 先前批次 |
| --- | --- |
| MC2-001 | BQ1-ROST |
| MC2-006 | BQ1-CBOE |
| MC2-008 | BQ1-RBLX |
| MC2-011 | BQ1-TSLA |
| MC2-012 | BQ1-NDAQ |
| MC2-015 | BQ1-MCHP |
| MC2-016 | BQ1-COHR |

这是已确认的历史来源重用，不能算作新增独立样本；不能仅由文件改名或 `clean` 自述证明未接触先前结论。另有同一标的不同截止图的跨图未来暴露风险。它们不证明每个 reviewer 实际受到污染，但足以阻止把本批描述为已验证的无污染独立准确率研究。冻结 PNG、manifest、评审 JSON 与历史统计原样保留，仅作历史模型校准。

### 2026-09-04 来源绑定与事务修复

MC2 manifest 现已逐样本冻结源 CSV SHA-256、规范化 504-bar OHLCV 窗口 SHA-256 和窗口行数，并在批次级冻结当前**重现 renderer** 源码 SHA-256；这不是旧冻结 PNG 的原始生成程序哈希。renderer 对每个源 CSV 只读取一次，文件哈希、窗口哈希与 K 线解析共享同一份不可变字节快照，并在首张图编码前核对全部绑定；只改 OHLCV、复制后改名、替换源文件或使用不同 renderer 都不能静默冒充同一可复现批次。冻结 PNG 不重绘，新增哈希用于证明其声明的输入窗口和重现程序边界，不把图片文件哈希误当成来源独立性证明。

同轮修复还把 `label_hidden` 的中性显示 ID 约束从 `identity_hidden` 解耦；纯数字 `MC2/EH1/BH1` 为中性命名，身份可见的旧 `BQ1-代码` 只允许后缀与规范化 symbol 完全一致，不能追加形态或结果词。源路径拒绝 NTFS alternate stream、设备名、UNC/反斜杠和非 CSV 输入；批次提交改为同卷 staging 后以平台原生原子 no-replace 操作一次性发布到全新的输出目录。目标目录在预检前、编码期间或发布瞬间已存在（包括空目录）都会拒绝；不支持可靠 no-replace 的平台会关闭发布而不是降级覆盖。设计中没有逐文件回滚，因此不会误删同路径上的外部替换文件。

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

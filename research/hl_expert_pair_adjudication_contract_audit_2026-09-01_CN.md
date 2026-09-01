# 普通 H/L 双专家比较、裁决与无推断转录合同审计（2026-09-01）

状态：`document_status=completed / internal_contracts=ready / external_human_execution=not_started`

## 一、结论

PA Research 已完成外部人工 H1/H2/L1/L2 采集前最后一组内部工具：

- 机器可读 pair adjudication schema；
- 先复用单专家 validator 的只读双记录 comparator；
- 空白 Markdown 表到单专家 schema JSON 的逐字段无推断转录合同和机器映射；
- 只使用临时合成记录的回归测试。

这些工具不创建专家答案或 ground truth。16 张身份/日期隐藏图、隔离 curation key 和专家可见 21 文件 allowlist 均未改变；真实 annotation JSON/CSV 仍为 0。

## 二、pair adjudication schema

[`pair_adjudication_schema_v1.json`](calibration/external_human_hl_v1/pair_adjudication_schema_v1.json)固定：

- 两份原始专家记录 SHA-256、不同 annotator identifier 和 `clean_eligible` 状态；
- 16 个精确 `EH1-###` 样本；
- 两专家原始 label、primary exclusion、evidence usable snapshot；
- 所有机器字段的 `disagreement_fields`；
- `experts_agree / both_reasonable_boundary / adjudicator_choice / insufficient_evidence / contaminated` 五种人工裁决结果；
- 第三位裁决者的独立、盲态和污染声明；
- 最终单一标签、模型预测事前冻结状态和逐样本 accuracy denominator eligibility；
- `completed_trade_denominator=0 / validated_win_rate=not-computable / conclusion=no-new-positive`。

schema 不允许 boundary、insufficient evidence 或 contaminated 样本产生最终单一标签或进入准确率分母。JSON Schema 不能跨字段证明“最终标签等于两专家一致标签”，因此仍要求人工双人复核；不能把 schema 解析成功当作裁决正确。

## 三、只读 pair comparator

[`compare_pa_hl_expert_annotations.py`](../scripts/compare_pa_hl_expert_annotations.py)按以下顺序运行：

1. 分别调用既有单专家 validator；
2. 任一 invalid 即 exit 1，不比较样本；
3. 任一 valid_ineligible，或两个 identifier 大小写/首尾空白规范化后相同，即 exit 2，不比较样本；
4. 两份 clean 且 identifier 不同才返回 16 行精确比较并 exit 0；
5. 逐行报告所有字段的精确分歧，不对自由文本做语义等价推断；
6. 固定不创建裁决，`final_label=null`、`accuracy_denominator=0`。

comparator 输出中的原始 label/exclusion 只是复制输入，不能读成工具生成的新标签。它也没有图像读取、pattern detector、网络、行情、账户或订单能力。

## 四、无推断转录

[`transcription_mapping_CN.md`](calibration/external_human_hl_v1/transcription_mapping_CN.md)和 [`transcription_mapping_v1.json`](calibration/external_human_hl_v1/transcription_mapping_v1.json)覆盖 schema 的 3 个固定头字段、8 个声明字段和每个样本 20 个字段。

本轮修复了一个真实契约缺口：单专家 schema 要求 `annotator.independent`，原空白表没有显式问题。表单现要求专家填写 `annotator_independent: no / yes`；只有字面 `no -> false`、`yes -> true`，不能从文件名、姓名、协调人说明或另一份记录推断独立性。

空白、枚举外值、含糊 yes/no、缺失/重复/冲突 ID、无时区时间戳或不可辨认文本都必须停止转录并退回人工确认。证据文本逐字保留，不摘要、润色或修复逻辑。

## 五、隔离与统计边界

安全导出器仍只复制原 5 个专家可见合同文件和 16 张身份中性 PNG；内部 pair schema、映射、政策、协调清单、hash inventory、审计和 comparator 不进入导出目录。来源 hypothesis key 继续只保存在 Git 忽略区。

```text
expert-facing allowlist: 21 files
identity-neutral charts: 16
real annotation artifacts: 0
ground_truth_status: not_established
overall_accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

视觉标签准确率即使未来可计算，也不产生交易胜率、盈亏比、扫描器性能或执行授权。

## 六、验证证据

```text
single-record + pair/comparator/transcription focused tests: 21 passed
full repository unittest suite: 406 passed
document validation: 336 Markdown files / 2297 links passed
Draft 2020-12 schema check + synthetic valid/invalid semantic probes: passed
JSON parse, compileall and git diff --check: passed
safe exporter allowlist: exact 5 documents + 16 charts passed
real annotation artifacts: 0
```

本工作只修改 PA Research；不修改 Codex Trading，不创建量化扫描器或自动 pattern detector，不连接 Futu/OpenD，不连接 Execution Agent，也不请求、推断或伪造专家标签。

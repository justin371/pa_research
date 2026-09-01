# 普通 H/L 双专家裁决与分母政策 v1

状态：`policy_ready / real_annotations_absent / no_ground_truth_yet`

## 一、输入门槛

每位专家必须返回一份符合 `annotation_schema_v1.json` 的独立 JSON。先运行只读 validator：

```powershell
python .\scripts\validate_pa_hl_expert_annotations.py `
  --manifest .\research\calibration\external_human_hl_v1\manifest.json `
  --annotations <expert-json>
```

validator 结果分三类：

- `clean_eligible`，exit 0：结构正确、manifest/hash/16 个 ID 完整、冻结顺序正确、独立且无污染；
- `invalid`，exit 1：schema、枚举、分母、时间顺序、证据字段或标签一致性错误；
- `valid_ineligible`，exit 2：记录结构完整，但专家非独立、看过来源假设/未来/结果，或 knowledge status 不是 clean。

exit 2 记录可以留作污染研究，但不能进入 clean 专家一致率、裁决或准确率分母。

## 二、两位专家比较

只有两份 `clean_eligible` 记录才能逐样本比较。比较字段至少包括：

- `expert_ordinary_hl_label`；
- `primary_exclusion`；
- parent state、方向、EMA20/50、A、B、lineage；
- evidence usable 与 confidence。

先运行只读 pair comparator：

```powershell
python .\scripts\compare_pa_hl_expert_annotations.py `
  --manifest .\research\calibration\external_human_hl_v1\manifest.json `
  --expert-a <expert-a-json> `
  --expert-b <expert-b-json>
```

comparator 结果分三类：`comparison_ready`（exit 0）、`invalid`（exit 1）和 `valid_ineligible`（exit 2）。它会先调用上节单专家 validator；同一标注人 identifier 即使两份记录各自声称 independent，也属于 pair ineligible。只有 `comparison_ready` 才返回 16 行逐字段精确比较。

comparator 只报告两份冻结记录的 label/exclusion/evidence snapshot、逐字段 `disagreement_fields` 和当前分母排除原因。它固定写 `adjudication_state=not_recorded`、`final_label=null`、`accuracy_denominator=0`，不判断谁对、不把一致直接升级为真值，也不创建裁决记录。

裁决状态：

```text
experts_agree
both_reasonable_boundary
adjudicator_choice
insufficient_evidence
contaminated
```

- 标签和主要排除项一致、两人 evidence usable，且一致标签属于 `H1/H2/L1/L2/not_ordinary_HL` 时可写 `experts_agree`；两人都写 `unclear` 或证据不可用时应转为 `insufficient_evidence`，不能制造最终单一标签；
- 标签不同但两套证据均合理时保留 `both_reasonable_boundary`，不能强制制造单一真值；
- 需要第三位专家时，第三人只看截止图、标准和两份已冻结记录，不看 curation key、未来或结果；
- 图不可用或两份证据均不足时写 `insufficient_evidence`；
- 任一进入裁决的记录发现污染时写 `contaminated` 并退出 clean 分母。

正式裁决记录必须符合 [`pair_adjudication_schema_v1.json`](pair_adjudication_schema_v1.json)。该 schema 固定两份原始记录 hash、标注人 identifier、逐样本原始 snapshot、精确分歧、裁决状态、第三人冻结声明、最终单一标签和逐样本准确率分母资格。`both_reasonable_boundary`、`insufficient_evidence` 和 `contaminated` 不允许产生最终单一标签或进入准确率分母；`adjudicator_choice` 必须有第三位 clean、独立且未看来源/未来/结果的人工裁决者。

表单转录必须遵守[无推断转录合同](transcription_mapping_CN.md)和机器映射 `transcription_mapping_v1.json`。空白、含糊或冲突值只能退回人工确认，不能由模型、转录人或 comparator 补齐。

## 三、视觉准确率分母

只有在专家标签冻结并完成裁决后，才允许揭示事前冻结的模型预测。必须同时报告：

```text
packet_total
clean_expert_pair_count
adjudicated_single_label_count
boundary_or_unclear_count
contaminated_count
model_prediction_coverage
accuracy_denominator
excluded_reasons
```

准确率分母只包含：

- 两专家 clean；
- evidence usable；
- 有最终单一 H1/H2/L1/L2/not_ordinary_HL 标签；
- 模型预测在专家结果揭示前已经冻结。

`both_reasonable_boundary`、`unclear`、`insufficient_evidence`、污染、缺失模型预测或事后补写预测均排除，并逐类报告数量。不得静默删除困难样本。

普通 H/L 的 sensitivity/specificity 还必须把 `not_ordinary_HL` 作为 hard-negative 类，不能只在四个 H/L 标签之间计算命中率。样本来源是策划 cohort，因此结果只能描述本 cohort，不能声称市场泛化。

## 四、与交易统计隔离

视觉标签一致或准确不产生交易分母。不得从本包计算：

- 胜率、盈亏比、期望值；
- 入场授权或当前候选；
- 扫描器性能；
- production handoff readiness。

交易统计仍需事前冻结合同、执行假设、隐藏结果回放和独立 lineage。当前保持：

```text
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

本政策只属于 `PA Research only`；不修改 Codex Trading，不创建量化扫描器或自动 pattern detector，不连接 Futu/OpenD，不连接 Execution Agent。

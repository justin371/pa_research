# 普通 H/L 双专家裁决记录 Validator 审计（2026-09-01）

状态：`document_status=completed / validator_ready / real_adjudication_absent`

## 一、结论

PA Research 已为未来的 `pair_adjudication_schema_v1.json` 记录增加只读跨字段 validator。它不接受孤立裁决 JSON：必须同时提供冻结 manifest 和两份原始专家 JSON，先通过既有单专家 validator 与 pair comparator，再验证裁决记录。

当前只使用临时合成 fixtures；两位真实外部专家尚未开始，真实 annotation 和 pair adjudication 仍为 0。

## 二、验证链

[`validate_pa_hl_expert_pair_adjudication.py`](../scripts/validate_pa_hl_expert_pair_adjudication.py)按以下顺序执行：

1. 两份源记录分别通过单专家 validator；
2. 两份记录组成 `comparison_ready` 且 annotator identifier 不同；
3. 裁决记录中的 source SHA-256、identifier、packet ID 和 manifest hash 与原始 bytes 一致；
4. `EH1-001` 至 `EH1-016` 精确按 manifest 顺序出现；
5. 每行 expert snapshot 与源记录一致，`disagreement_fields` 与 comparator 精确一致；
6. comparison freeze 不早于两份专家 freeze，adjudication start 不早于 comparison freeze，adjudication freeze 晚于 start，全部时间含时区；
7. 裁决状态、最终标签和第三人声明符合政策；
8. 逐行重算 accuracy eligibility/excluded reason，再独立重算整个 summary。

validator 输出 `valid`（exit 0）、`invalid`（exit 1）或全局裁决冻结污染但结构完整的 `valid_ineligible`（exit 2）。输出只到 stdout，`records_created_or_modified=0`。

## 三、关键不变量

- `experts_agree` 只能复制两份一致且 evidence usable 的冻结标签；不能把 `unclear` 修复为单一标签；
- `adjudicator_choice` 必须有第三位 identifier 不同、clean、独立、未看来源 hypothesis/未来/outcome 的人工裁决者；
- `both_reasonable_boundary / insufficient_evidence / contaminated` 的 final label 必须为 null；
- 模型预测只有在专家揭示前冻结、样本有最终单一标签、两份证据可用且记录 clean 时才进入准确率分母；
- 单一 excluded reason 使用政策固定优先级，summary 的 bucket、coverage、denominator 和 exclusion counts 全部从 16 行重算；
- 任何 hash、snapshot、分歧、状态或汇总不一致只报错，不改写、推断或补齐。

JSON Schema 继续负责结构边界；validator 负责跨文件 identity 和跨字段关系。两者都不能证明 PA 图形标签在视觉上正确，不能替代外部人工专家。

## 四、安全和隔离

身份/日历日期隐藏图、隔离 curation key 和安全导出器均未改变。专家可见 allowlist 仍只有原 5 份文件与 16 张图；validator、pair schema、内部政策、映射和审计都不导出。

```text
expert-facing allowlist: 21 files
real annotation artifacts: 0
real pair adjudication artifacts: 0
ground_truth_status: not_established
overall_accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
PA Research only
no Codex Trading
no quantitative scanner
no automatic pattern detector
no Futu/OpenD
no Execution Agent
```

## 五、验证证据

```text
pair-adjudication validator synthetic tests: 15 passed
full repository unittest suite: 421 passed
document validation: 337 Markdown files / 2299 links passed
compileall and git diff --check: passed
safe exporter allowlist: exact 5 documents + 16 charts passed
```

本工作只属于 PA Research；不修改 Codex Trading，不创建量化扫描器或自动 pattern detector，不连接 Futu/OpenD，不连接 Execution Agent，不请求、创建、推断或伪造真实专家标签/裁决。

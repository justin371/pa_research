# 普通 H/L 专家标注回收 Validator 审计（2026-09-01）

状态：`document_status=completed / validator_status=ready / real_annotations=absent / human_expert_status=not_performed`

## 一、结论

PA Research 已为未来外部人工专家返回的 H1/H2/L1/L2 记录建立机器 schema、只读 validator 和双专家裁决/分母政策。本 goal 只用临时目录中的合成测试数据，没有创建、推断或伪造真实专家标签。

validator 对一份未来记录给出三种互斥结果：

- `clean_eligible`，exit 0：结构、manifest hash、16 个样本、冻结顺序、证据和标签一致性全部通过，且专家独立、knowledge clean、未看来源假设/未来/结果；
- `invalid`，exit 1：文件、schema、枚举、样本 ID、时间、证据或标签逻辑不成立；
- `valid_ineligible`，exit 2：记录结构完整，但专家不独立或在冻结前接触来源假设、未来、结果，或 knowledge status 不是 clean。

`valid_ineligible` 不会被悄悄删除：它可以保留为污染研究，但不得进入 clean 专家一致率、裁决或准确率分母。

当前真实状态保持：

```text
real annotation artifacts: 0
human_expert_status: not_performed
ground_truth_status: not_established
overall accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

## 二、产物

- [机器 annotation schema v1](calibration/external_human_hl_v1/annotation_schema_v1.json)；
- [双专家裁决与分母政策](calibration/external_human_hl_v1/adjudication_and_denominator_policy_CN.md)；
- [`validate_pa_hl_expert_annotations.py`](../scripts/validate_pa_hl_expert_annotations.py)：只读 JSON validator；
- [外部人工专家包](calibration/external_human_hl_v1/README.md)仍只包含标准、空白表、中性 manifest 和本合同，没有真实 annotation artifact。

使用方式：

```powershell
python .\scripts\validate_pa_hl_expert_annotations.py `
  --manifest .\research\calibration\external_human_hl_v1\manifest.json `
  --annotations <expert-json>
```

validator 只读取输入并把 JSON 报告写到 stdout；不修改 manifest、annotation 文件或仓库，不打开图表，不识别 pattern，不访问网络或行情。

## 三、硬校验

### 文件与冻结

- UTF-8 JSON 可读；
- `schema_version`、`packet_id` 和 manifest SHA-256 精确匹配；
- 专家角色、identifier 和独立状态存在；
- started/frozen 时间均含时区，且 frozen 严格晚于 started；
- 来源/模型假设、未来/结果接触状态和 knowledge status 显式记录。

### 分母与字段

- manifest 自身必须精确包含 16 个格式为 `EH1-###` 的唯一 ID，annotation 必须逐项完整覆盖；
- duplicate、missing、extra 或 cardinality 不一致均失败；
- 所有枚举与 schema 同源；
- confidence 必须是 1–5 的整数；
- 高低点、A、B、lineage/attempt、第一障碍/空间、与 BOP/三推/区间的排除和主要不确定性均必须为非空证据。

### 普通 H/L 一致性

H1/H2/L1/L2 只有在以下条件同时成立时通过：

- evidence usable；
- parent state 为 open trend；
- same lineage；
- A 为 strong/ordinary 非事件推动；
- B 为 controlled/controlled-late/deep-but-late-controlled；
- H 方向 long 且 EMA20/50 rising；L 方向 short 且 EMA20/50 falling；
- `primary_exclusion=not_applicable`。

`not_ordinary_HL` 必须给出一个主要排除项；`unclear` 必须写 `insufficient_evidence` 或 `other`。不可用证据不能获得普通 H/L 标签。

## 四、双专家和准确率边界

只有两份 `clean_eligible` 记录才能进入逐样本比较。标签相同不自动成为真值；政策允许：

```text
experts_agree
both_reasonable_boundary
adjudicator_choice
insufficient_evidence
contaminated
```

第三位 adjudicator 也必须看不到 curation key、未来和结果。模型预测只能在专家标签冻结后揭示。准确率分母必须报告 coverage 和所有排除原因，不能静默移除困难样本；策划 cohort 的结果不能外推为市场泛化。

视觉准确率仍与交易结果完全隔离。即使未来有 clean ground truth，也不能由本 validator 计算胜率、盈亏比、候选授权或生产交接。

## 五、验证范围

12 项合成测试覆盖：

- clean 完整记录；
- contamination 与非独立 expert 的 exit 2；
- manifest hash、时区与冻结顺序；
- manifest 固定 16 项与 `EH1-###` ID 格式；
- duplicate/missing/extra ID；
- 枚举、confidence 和空证据；
- H/L 方向、EMA、lineage、A/B 一致性；
- not-ordinary/unclear 排除项；
- unusable evidence；
- CLI 0/1/2 exit code 与只读性；
- schema/validator 枚举 parity；
- 真实 packet 中 annotation artifact 仍为 0。

## 六、仓库边界

本轮只修改 PA Research。没有修改 Codex Trading，没有创建量化扫描器或自动 pattern detector，没有连接 Futu/OpenD，没有连接 Execution Agent，也没有加入任何真实或伪造人工标注。

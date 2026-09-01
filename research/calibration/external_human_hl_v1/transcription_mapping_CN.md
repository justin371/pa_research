# 普通 H/L 专家表到 JSON 无推断转录合同 v1

状态：`contract_ready / synthetic_only / real_transcription_not_started`

本合同把已冻结的 `annotation_form.md` 逐字段转成 `annotation_schema_v1.json`。转录人只复制，不看图判断、不解释专家意思、不修复标签、不补空白。机器映射见 [`transcription_mapping_v1.json`](transcription_mapping_v1.json)。

## 一、固定头字段

以下三项由协调人机械取得，不要求专家重写：

| JSON 字段 | 唯一来源 |
|---|---|
| `schema_version` | 固定字面值 `pa_hl_expert_annotations_v1` |
| `packet_id` | `manifest.json.packet_id` 原值 |
| `manifest_sha256` | `manifest.json` 原始 bytes 的 SHA-256 |

不得改写 manifest、重新序列化后再计算 hash，或从其他报告复制 hash。

## 二、冻结声明映射

| 表单字段 | JSON 字段 | 转换 |
|---|---|---|
| `annotator_role` | `annotator.role` | 必须原样为 `external_human_expert` |
| `signature_or_identifier` | `annotator.identifier` | 非空原文复制 |
| `annotator_independent` | `annotator.independent` | 只允许 `no -> false`、`yes -> true` |
| `annotation_started_at` | `freeze.annotation_started_at` | 原样复制，必须含时区 |
| `annotation_frozen_at` | `freeze.annotation_frozen_at` | 原样复制，必须含时区 |
| `source_or_model_hypotheses_seen_before_freeze` | 同名 freeze 字段 | 只允许 `no -> false`、`yes -> true` |
| `future_or_outcome_evidence_seen_before_freeze` | 同名 freeze 字段 | 只允许 `no -> false`、`yes -> true` |
| `knowledge_status` | `freeze.knowledge_status` | 只复制表单允许枚举 |

`annotator_independent` 是本轮补齐的显式字段。不得因为两份表来自不同文件、不同姓名或协调人说“独立”就推断为 `true`。

## 三、16 项逐字段映射

表格中的 13 个字段逐格复制到同一 `expert_sample_id` 的 JSON row。`confidence_1_to_5` 只允许把单个十进制字符 `1`–`5` 转为整数；其余枚举不得改大小写、翻译或同义替换。

每个样本的 7 个自由文本字段原文复制：

```text
major_high_low_reading
A_leg_evidence
B_leg_evidence
lineage_and_attempt_evidence
first_obstacle_and_space
why_not_BOP_or_third_push_or_range_repeat
main_uncertainty
```

换行可按 JSON 转义保存，但文字、数字、否定词和不确定性不得摘要、润色或重写。表格 ID 与自由文本块 ID 必须完全一致。

## 四、必须停止的情况

以下任一情况都不能自动处理，转录状态应保持 incomplete，并把原表退回人工确认：

- 必填格或证据文本为空；
- `yes/no` 含糊、打勾位置不明或同时出现两个答案；
- 值不在表单打印的允许集合；
- ID 缺失、重复、冲突或不是 `EH1-001` 至 `EH1-016`；
- 时间戳无时区；
- 手写内容不可辨认、被覆盖或看似自相矛盾。

禁止用图形识别、上下文字义、其他专家记录、来源 hypothesis、未来或 outcome 来“猜”字段。validator 报错也只能退回原专家/协调人更正，转录人不能替专家修复。

## 五、双人复核与边界

转录后由第二人逐字段核对原表和 JSON，再运行单专家只读 validator。两份原始专家 JSON 不覆盖、不合并；pair comparator 只报告精确分歧，不生成裁决或答案。

测试只允许使用临时合成表单值和 JSON，不得创建冒充真实专家的 annotation 文件。当前保持：

```text
real annotations: 0
ground_truth_status: not_established
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

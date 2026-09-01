# 普通 H/L 外部专家安全交接清单 v1

状态：`coordinator_status=ready / expert_handoff_started=no / real_annotations=absent`

本文件只给交接协调人，不属于专家可见 allowlist。它不会请求专家、创建标签或把来源假设当成答案。

## 一、交接前机器核验

- 当前 checkout 必须为 PA Research，不得从 Codex Trading 复制规则或文件；
- `manifest.json` SHA-256 必须为 `d1616e568bceebbe605d498548ffc5c346cec1365831ba9035ab131ad9765b23`；
- manifest 必须精确包含 `EH1-001` 至 `EH1-016`、16 个唯一图路径，且文件全部存在；
- `annotation_form.md` 的 16 行必须保持空白；
- packet 中真实 annotation JSON/CSV 必须为 0；
- `.codex/goals/` 必须继续被 Git 忽略，curation key 不得进入导出包。

## 二、专家可见 allowlist

`expert-facing allowlist: 21 files`

只复制以下 5 个合同文件和 manifest 指向的 16 张 PNG 到独立目录：

1. `README.md`；
2. `expert_criteria_CN.md`；
3. `annotation_form.md`；
4. `annotation_schema_v1.json`；
5. `manifest.json`；
6. `manifest.json` 中的 16 张唯一截止图。

推荐使用仓库的安全导出器，输出目录必须不存在或为空：

```powershell
python .\scripts\export_pa_hl_expert_packet.py --repo-root . --output-dir <isolated-empty-directory>
```

导出器先验证 manifest 和 16 张图的冻结 SHA-256，再只复制这 21 个文件；不复制内部 hash inventory、协调清单、审计、来源资料或 annotation。

不要把整个 repo、Git 历史或父目录交给专家。使用安全导出器复制后，应从隔离目录重新确认总文件数为 21；必须保持 manifest bytes 不变并重建其中的 `charts/` 相对目录，不能加入股票、日期、候选 family、来源标签或未来结果。

## 三、明确禁止导出

- `.codex/` 及任何 `curation_key.json`；
- 来源 cohort 的 manifest、README、旧盲审、旧模型判断或裁决；
- 截止日之后的 K 线、结果、回放、收益或交易统计；
- `adjudication_and_denominator_policy_CN.md`、validator、内部审计和本协调清单；
- 内部完整性文件 `neutral_chart_sha256.json`；
- 任何预填 H1/H2/L1/L2、排除项、方向、confidence 或证据文本。

## 四、两位专家冻结顺序

1. 两位外部人工专家分别获得各自隔离副本，互不看答案、不讨论样本；
2. 每人打开第一张图前记录 `annotation_started_at`；
3. 按标准完成 16 项和证据字段，再记录 `annotation_frozen_at`；
4. 如实记录是否在冻结前看到来源/模型假设、未来或结果，以及 knowledge status；
5. 人工表到 JSON 的转录只能逐字段复制，不能由模型推断或补齐空白；
6. 分别运行只读 validator。只有两份 `clean_eligible` 才能进入逐样本比较；
7. 按裁决政策处理分歧，最后才允许揭示隔离 curation key。

## 五、当前门槛

```text
internal_packet_and_contract_work: complete
collection_handoff_readiness: ready
independent_agent_work_remaining_before_requesting_humans: pair_adjudication_contract_and_transcription_mapping
external_human_expert_A: not_started
external_human_expert_B: not_started
adjudication: not_started
ground_truth_status: not_established
overall_accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

安全采集包已经可交接，但按“先完成独立工作”的顺序，下一独立 goal 先补 pair-level 裁决机器合同/只读比较器和表到 JSON 的无推断转录边界；之后才由用户/协调人选择两位真正独立的外部人工专家。本 repo 不自动联系专家，也不代表任何人完成标注。

边界：`PA Research only / no Codex Trading / no quantitative scanner / no automatic pattern detector / no Futu/OpenD / no Execution Agent`。

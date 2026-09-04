# 普通 H/L 外部专家安全交接清单 v1

状态：`coordinator_status=blocked_for_accuracy_study / expert_handoff_started=no / real_annotations=absent`

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

推荐使用仓库的安全导出器，输出目录必须尚不存在，并且不能位于冻结源包内部：

```powershell
python .\scripts\export_pa_hl_expert_packet.py --repo-root . --output-dir <new-isolated-directory>
```

导出器先在同一文件系统的私有暂存目录复制并核对完整 21 文件 allowlist，全部哈希一致后才以平台原生 atomic no-replace 目录操作发布。目标目录已存在、复制/校验失败、发布竞态或平台缺少等价原语时都拒绝；不能留下半包、覆盖外来内容或向冻结源包写入。

导出器先验证 canonical manifest、独立固定的 chart inventory 及 5 个文档哈希，并检查 16 张图；复制后再次核对全部 21 个目标文件哈希。空白表的原始字节被固定，预填后不能导出。不复制内部 hash inventory、协调清单、审计、来源资料或 annotation。

导出仅用于内部完整性验收。成功时返回 `status=integrity_verified_handoff_blocked`、`human_handoff_ready=false`、`accuracy_study_ready=false`；CLI exit 0 只表示复制与哈希核验成功，不授权发送给专家。历史冻结 README 的 `packet_ready` 不是当前交接许可。

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
7. 按内部 `transcription_mapping_CN.md` 逐字段双人复核，再运行 pair comparator；
8. 按 `pair_adjudication_schema_v1.json` 和裁决政策由人工处理分歧；
9. 裁决冻结后运行内部只读 pair-adjudication validator，只有记录一致性通过后才允许揭示隔离 curation key。

## 五、当前门槛

```text
internal_packet_and_contract_work: integrity_hardened_prediction_receipt_and_blind_packet_pending
collection_handoff_readiness: blocked_for_accuracy_study
independent_agent_work_remaining_before_requesting_humans: independent_pre_reveal_commitment, cross_sample_future_isolation
cross_sample_future_exposure: confirmed_in_frozen_packet
blind_packet_handoff: blocked_until_new_nonleaking_design_validated
external_human_expert_A: not_started
external_human_expert_B: not_started
adjudication: not_started
ground_truth_status: not_established
overall_accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

2026-09-03 复核更正：包导出完整性和 canonical 绑定已加固，但独立模型预测的事前承诺尚未验收，因此不能沿用 2026-09-01 的“内部工作全部闭合”结论来启动准确率研究。先完成[专家证据链加固审计](../../expert_evidence_chain_hardening_audit_2026-09-03_CN.md)中的剩余门槛，再由用户/协调人选择两位真正独立的外部人工专家。本 repo 不自动联系专家，也不代表任何人完成标注。

边界：`PA Research only / no Codex Trading / no quantitative scanner / no automatic pattern detector / no Futu/OpenD / no Execution Agent`。

## 六、跨图未来泄露门槛（2026-09-03）

本地来源核验确认冻结包包含同一标的不同截止日的重叠图窗；较晚图含较早截止日之后的走势。逐图删除自身未来、使用不同 ID 或不同 SHA，均不能证明整包对同一审核者保持盲态。该风险独立于预测事前承诺，后者补齐也不会自动解除此门槛。

冻结 v1 只保留作内部完整性/图像可用性校准，不作为无污染准确率研究包发送。未来版本须在专家不可见的来源层核对 symbol、截止日、完整可见窗口及分组：同一审核者不能看到会泄露其他样本未来的图窗；训练/校准与独立评估也须隔离。单纯改顺序、改编号、删掉困难样本或分开文件夹不能证明无泄露。不得改写当前冻结图/manifest 或伪造未见过的记录；新包和分组协议须单独验收。独立专家目前仍未开始。

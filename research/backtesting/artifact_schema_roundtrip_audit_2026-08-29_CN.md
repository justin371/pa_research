# 回放 artifact schema round-trip 审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 当前回放 engine、CLI 输出的 `results.csv`、`summary.json`、`run_metadata.json`、输出 schema 和本机已有历史 artifact<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计边界与结论

本轮只使用仓库自带 example 合同/价格文件和本机已经存在的历史 artifact 做验证，不抓取新行情、不新增冻结合同、不把临时 round-trip 输出写回仓库、不改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。重点是检查新增事前 provenance 与 mismatch 字段是否能从结果行进入摘要，再由独立运行元数据绑定到同一次运行。

盘点发现：engine `0.3.8` 的 `results.csv` 已包含 `pre_entry_provenance_status` 和 `pre_entry_provenance_missing_fields`，`summary.json` 已包含 provenance 状态计数与三类事前派生字段 mismatch；但独立 `run_metadata.json` 只有运行/输入/结果文件指纹，没有摘要级计数，无法单独核对摘要的分母和 mismatch 状态。

当前 engine `0.3.9` 已补上 `summary_provenance`：

- 记录实际 `results.csv` 列名，确认新 provenance 列确实写出；
- 复制 `pre_entry_provenance` 完整/不完整计数、状态计数、`completed_trade_count`、互斥结果 bucket 和各类 eligibility/事前派生字段 mismatch 计数；
- 让 `summary.json` 内嵌的 `run_metadata` 与独立 `run_metadata.json` 保持一致；
- 不重新解释旧结果、不把重新运行当作新样本，也不覆盖旧 artifact。

## 二、example round-trip 结果

使用仓库现有 `prices.example.csv` 与 `contracts.example.csv` 在临时目录运行当前 CLI，结果为：

| 检查 | 结果 |
| --- | --- |
| engine | `0.3.9` |
| `results.csv` 行数 | 1 |
| provenance 完整 / 不完整 | 1 / 0 |
| `completed_trade_count` | 1 |
| `contract_eligibility_mismatch_count` | 0 |
| `event_bucket_mismatch_count` | 0 |
| `contract_space_bucket_mismatch_count` | 0 |
| `results_file_sha256` | 与实际 `results.csv` 字节一致 |
| `summary.json.run_metadata` 与独立 metadata | 完全一致 |
| CSV 重新读入后重建摘要 | 关键计数与胜率字段一致 |

`results.csv` 的实际列名包含 `pre_entry_provenance_status`、`pre_entry_provenance_missing_fields`、`planned_entry_trigger`；`summary_provenance.result_columns` 与 CSV 列名完全一致。该检查只证明 artifact 链路自洽，不证明样本独立或长期胜率。

## 三、只读校验器对现有输入的复核

用当前 engine `0.3.9` 对仓库已有的 7 组合同/价格快照在临时目录生成输出，再运行 `scripts/validate_pa_research_artifact.py` 的同一校验逻辑。临时目录在检查后删除，没有把输出写回仓库：

| 检查 | 结果 |
| --- | --- |
| 校验组数 | 7 |
| 结果行数 | 60 |
| `current_valid` | 7 / 7 |
| `invalid` | 0 |
| `historical_incomplete` | 0（当前 engine 生成的临时输出） |
| 结果文件 hash | 7 / 7 与实际 `results.csv` 一致 |
| summary/metadata 嵌套一致性 | 7 / 7 |
| CSV round-trip 关键摘要字段 | 7 / 7 |

`result_set_sha256` 沿用 engine 的规范：对写出的 CSV 内容统一换行符后计算；这样 Windows 的 CRLF 与其他平台的 LF 不会被误报为结果集变化，实际结果文件的原始字节仍由 `results_file_sha256` 单独锁定。

## 四、历史 metadata 处理

本机现有 13 份 PA Research `run_metadata.json` 均缺少当前必需的 engine/依赖版本、源码指纹、输入文件指纹、结果文件指纹和 `summary_provenance`。它们继续标记为 `historical / incomplete provenance`，不能因为对应 `summary.json` 有旧 engine 版本或有结果数字就升级为当前验证结果；不删除、不回写、不与当前输出拼接。

同一输入曾存在不同旧输出的情况仍按前一份[`回放 provenance 与再现性审计`](replay_provenance_reproducibility_audit_2026-08-29_CN.md)处理：保留报告明确指定的 artifact，其他版本只做历史冲突记录。任何未来重跑都必须由新 `result_set_sha256`、实际结果文件 hash、当前 engine/source hash 和 `summary_provenance` 绑定；重跑本身不是新样本。

## 五、统计与范围结论

本轮没有新增结果分母、没有把 example 行并入正式样本，也没有把 ABC/BOP/H3/L3 与 H/L 混算。现有 PA Research 结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

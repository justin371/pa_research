# 回放 artifact 全仓库 inventory 审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 当前 checkout 中的 `results.csv`、`summary.json`、`run_metadata.json`、回放输入 CSV、审计报告与 Git 路径记录<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、只读盘点结果

本轮对当前 checkout 做递归文件盘点，并检查 Git 历史中是否曾跟踪同名输出文件。结果如下：

| 项目 | 结果 |
| --- | --- |
| 当前 checkout 中的 `results.csv` | 0 |
| 当前 checkout 中的 `summary.json` | 0 |
| 当前 checkout 中的 `run_metadata.json` | 0 |
| 三件套 artifact 目录 | 0 |
| Git 历史中同名输出路径 | 0 |
| 可配对的回放合同/价格输入组 | 7 |

因此，当前仓库没有可供 `scripts/validate_pa_research_artifact.py` 直接读取的持久化 artifact。不存在“校验通过但未登记”的输出，也不存在缺一件却应被当成完整结果的目录。

## 二、输入与 artifact 的边界

以下 7 组文件是合同与历史价格快照输入，不是回放 artifact，也不应单独当作结果或胜率分母：

1. `hl_contracts_2026-08-26.csv` + `hl_contract_batch_prices_2026-08-26.csv`
2. `hl_contracts_batch2_2026-08-26.csv` + `hl_contract_batch2_prices_2026-08-26.csv`
3. `hl_large_contracts_2026-08-27.csv` + `hl_large_prices_2026-08-27.csv`
4. `hl_next_contracts_2026-08-27.csv` + `hl_next_prices_2026-08-27.csv`
5. `hl_next2_contracts_2026-08-27.csv` + `hl_next2_prices_2026-08-27.csv`
6. `hl_next4_contracts_2026-08-27.csv` + `hl_next4_prices_2026-08-27.csv`
7. `hl_next5_contracts_2026-08-27.csv` + `hl_next5_prices_2026-08-27.csv`

`abc_bop_contract_intake_2026-08-28.csv`、`bop_contract_intake_2026-08-28.csv` 等候选/intake 文件同样不是 `results.csv`，不具备结果阶段的成交、horizon、`realized_R` 和 artifact provenance，不得被重命名或推断成回放结果。对应的 `*_replay_*.md` 是人工研究报告，不替代三件套文件。

## 三、历史边界与后续规则

此前审计曾记录 13 份旧 `run_metadata.json` 的历史 provenance 不完整状态；这些文件不在当前 checkout 中，本轮不虚构路径、不重新解释数字，也不把它们当作当前 artifact。即使未来发现旧文件，也必须由 validator 返回 `historical_incomplete`，不能与当前 engine `0.3.9` 输出拼接。

未来只有在明确输出目录同时包含 `results.csv`、`summary.json`、`run_metadata.json` 时，才运行只读校验器：当前 schema、hash、`summary_provenance`、嵌套 metadata 和 CSV round-trip 全部一致才可标记 `current_valid`；旧 engine/缺字段标记 `historical_incomplete`；当前格式但 hash 或字段矛盾标记 `invalid`。inventory 本身不下载行情、不重跑回放、不写回 artifact。

## 四、结论与范围声明

本轮没有新增样本、没有新增结果分母、没有混算 ABC/BOP/H1/H2/L1/L2/H3/L3，也没有把输入 CSV 当成胜率证据。当前结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

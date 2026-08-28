# 冻结合同字段覆盖与分层完整性审计（2026-08-29）

日期：2026-08-29<br>
范围：现有冻结 H/L 合同 CSV、ABC/BOP intake、当前 schema/回放 engine 和研究索引<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、结论

本轮只审计仓库中已有记录，没有下载新行情、重新选股、重画图表或新增回放样本。审计对象是 7 个非示例冻结合同 CSV，共 60 条 H1/H2/L1/L2 合同；当前 engine `0.3.7` 可以加载全部 60 条。核心身份、方向、Pattern/内部标签、订单字段、事件字段、人工审查字段、`contract_frozen` 和 `lineage_id` 没有发现跨文件重复或 H/L/ABC/BOP 混算。

发现和处理的边界如下：

- 60/60 条核心必需字段完整，`lineage_id` 为 60/60；没有发现大小写变化造成的重复 `sample_id` 或合同族。
- 50 条旧合同没有 `contract_state`、`space_status` 和 `pre_entry_space_R`。它们保留为未知，不能从回放结果倒推成严格 `>=1R`；10 条最新合同才有这组字段，其中 9 条为 `strict_ge_1R`、1 条为 `borderline_ge_1R`。
- 55 条 H/L 合同通过 EMA 方向闸门（多头 `long_pass` 27 条、空头 `short_pass` 28 条）；5 条明确记录为 `fail_flat_or_opposite`，属于 `observation_only`，不是可交易样本，也不是字段错误。
- 现有冻结合同没有 `ABC_CONT`、`BOP` 或 H3/L3；ABC/BOP intake 仍是 `contract_frozen=no`，不进入回放分母。H/L、ABC、BOP 和三推统计继续分开。
- `market_context_id` 在 60 条中均为空，因此不能计算 independence-adjusted 胜率。现有结果的 `validated win-rate` 仍为 `not-computable`，结论保持 `no-new-positive`。

## 二、逐文件覆盖

| 冻结合同文件 | 条数 | Long/Short | H1/H2/L1/L2 | H1_L1/H2_L2 | EMA pass / observation-only | 空间字段 |
| --- | ---: | ---: | --- | --- | --- | --- |
| `hl_contracts_2026-08-26.csv` | 5 | 3/2 | 1/2/1/1 | 2/3 | 4/1 | 5 unknown |
| `hl_contracts_batch2_2026-08-26.csv` | 3 | 1/2 | 0/1/2/0 | 2/1 | 3/0 | 3 unknown |
| `hl_large_contracts_2026-08-27.csv` | 37 | 20/17 | 15/5/12/5 | 27/10 | 33/4 | 37 unknown |
| `hl_next_contracts_2026-08-27.csv` | 5 | 4/1 | 4/0/1/0 | 5/0 | 5/0 | 5 unknown |
| `hl_next2_contracts_2026-08-27.csv` | 2 | 2/0 | 2/0/0/0 | 2/0 | 2/0 | 1 strict / 1 borderline |
| `hl_next4_contracts_2026-08-27.csv` | 2 | 2/0 | 2/0/0/0 | 2/0 | 2/0 | 2 strict |
| `hl_next5_contracts_2026-08-27.csv` | 6 | 0/6 | 0/0/6/0 | 0/6 | 6/0 | 6 strict |
| **合计** | **60** | **32/28** | **24/8/22/6** | **46/14** | **55/5** | **9 strict / 1 borderline / 50 unknown** |

`observation-only` 的 5 条记录是首批 CRWD H2，以及大批次 RBLX 的 3 条和 MAR 的 1 条。它们的方向、EMA 斜率和失败原因相互一致；当前回放只保留审计行，不把它们当作成交或胜率分母。

## 三、字段完整性与分层边界

| 字段/关系 | 覆盖 | 审计判断 |
| --- | ---: | --- |
| 核心必需列 | 60/60 | 可由当前 engine 加载 |
| `contract_frozen=yes` | 60/60 | 全部是冻结合同 |
| `lineage_id` | 60/60 | 可做依赖审计；其中 53 个唯一 lineage、7 个共享组 |
| `event_context` | 60/60 | 37 条含未核实事件过滤，11 条含普通非事件标记，1 条为 `none`，其余为事件/缺口相关标记；不能直接合并为同质普通样本 |
| Daily EMA20/EMA50 斜率和 H/L gate | 60/60 | 27 多头 pass、28 空头 pass、5 条失败并保留 observation-only |
| `meta_confluence` | 60/60 | 49 条有 `meta_zone/meta_components`；其余 11 条明确为 `absent`，不是缺失性误判 |
| `contract_state` | 10/60 | 仅最新 3 个批次有 `frozen_pre_outcome`；旧 50 条不回填 |
| `space_status` / `pre_entry_space_R` | 10/60 | 9 条严格、1 条边界；旧 50 条按 `unknown_contract_space` 处理 |
| `market_context_id` | 0/60 | 独立性调整胜率不可计算 |
| 冻结 `ABC_CONT` / `BOP` / `H3` / `L3` | 0 | 不从空缺推导胜率为零；intake 继续隔离 |

已有的[`人工冻结合同覆盖审计`](contract_coverage_audit_2026-08-28_CN.md)记录了同一批 60 条合同的方向、标签、事件、空间和 lineage 总览；本报告补充逐文件字段分区、EMA 失败行性质和校验器的明确约束。

## 四、校验修复

本轮只修复记录完整性防护，不改变交易规则或历史数值：

1. engine `0.3.7` 要求显式 `strict_ge_1R`、`clearly_positive` 或 `blocked` 必须同时提供数值 `pre_entry_space_R`；缺数值不能把状态当作可审计证据。
2. 文档校验器现在检查方向、Pattern、内部标签、H/L 方向映射、EMA 斜率与 gate 的一致性、H3/L3 的方向/Pattern 关系、可选 `contract_state` 枚举以及严格/阻断空间状态的数值证据。
3. 合同身份键在校验器中统一按不区分大小写的 canonical key 检查，避免只因大小写不同而漏报重复。

这些检查没有改写 7 个 CSV。旧合同的可选字段仍为空；新增字段应在下一批人工看图冻结时、结果发生前一次性填写。

## 五、统计结论和范围声明

当前合同覆盖证明了“哪些字段已经记录、哪些层可以安全分开”，不能证明 H1/H2/L1/L2 的真实胜率。尤其是 50 条空间未知、37 条事件过滤未核实、7 个共享 lineage 组和缺失 `market_context_id`，都不足以支持独立样本外推。继续保留：

```text
research_state: provisional
validated win-rate: not-computable
conclusion: no-new-positive
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

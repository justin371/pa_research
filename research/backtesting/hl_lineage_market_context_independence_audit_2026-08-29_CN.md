# H/L lineage、市场状态与独立性分母审计（2026-08-29）

状态：`research_only / audit_only / no-new-positive`

## 结论

本次只审计 PA Research 当前 7 份 H/L 冻结合同、对应的 selection/replay 报告、统一字段说明和现有独立性防护。没有下载行情、没有看新图、没有运行回放、没有增加样本或结果，也没有修改 Codex Trading。

当前 60 条 H/L 合同中有 53 个规范化 `lineage_id`，7 个共享 lineage 组、共 14 条依赖行；7 份 CSV 都没有 `market_context_id` 列，60/60 条也没有可记录的市场状态 ID。因此：

- 共享 lineage 的 H1/H2 或 L1/L2 只能作为同一父级/局部尝试的描述性路径，不能按相互独立样本解释；
- 不同 `lineage_id` 只说明人工记录没有把它们登记为同一已知局部结构，不能证明市场状态、结果 artifact 或独立同分布；
- 缺失 `market_context_id` 不是“市场环境已独立”，不能生成或暗示 independence-adjusted 胜率；
- selection 的入场前证据、replay 的事后路径和外部 artifact provenance 仍是不同层，不能把任何一层的数量当成独立性分母。

当前研究结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

## 一、7 份 H/L 合同的机器盘点

规范化 lineage 比较大小写和首尾空格；精确合同身份检查使用 `symbol + decision_date + direction + primary_pattern + internal_label`，不是用结果或收益选择代表行。

| 合同文件 | 行数 | unique lineage | 共享组 | 共享行 | `market_context_id` 非空 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hl_contracts_2026-08-26.csv` | 5 | 4 | 1 | 2 | 0 |
| `hl_contracts_batch2_2026-08-26.csv` | 3 | 3 | 0 | 0 | 0 |
| `hl_large_contracts_2026-08-27.csv` | 37 | 31 | 6 | 12 | 0 |
| `hl_next_contracts_2026-08-27.csv` | 5 | 5 | 0 | 0 | 0 |
| `hl_next2_contracts_2026-08-27.csv` | 2 | 2 | 0 | 0 | 0 |
| `hl_next4_contracts_2026-08-27.csv` | 2 | 2 | 0 | 0 | 0 |
| `hl_next5_contracts_2026-08-27.csv` | 6 | 6 | 0 | 0 | 0 |
| **合计** | **60** | **53** | **7** | **14** | **0** |

7 个共享 lineage 组及其依赖路径为：

| lineage | 记录 |
| --- | --- |
| `COHR-2022-04-bear-leg` | COHR 2022-04-08 L1；2022-04-14 L2 |
| `COHR-2022-06-bear-leg` | COHR 2022-06-14 L1；2022-06-22 L2 |
| `COHR-2024-06-bull-leg` | COHR 2024-06-10 H1；2024-06-21 H2 |
| `MAR-2023-01-recovery` | MAR 2023-01-11 H1；2023-01-18 H2 |
| `RBLX-2023-08-bear-leg` | RBLX 2023-08-11 L1；2023-08-17 L2 |
| `RBLX-2025-11-bear-leg` | RBLX 2025-11-13 L1；2025-11-20 L2 |
| `TSLA-2025-08-local` | TSLA 2025-08-18 H1；2025-08-21 H2 |

60 条合同没有精确的 `symbol/date/direction/pattern/label` 身份重复。这个结果不改变共享 lineage 的依赖性：没有精确重复，不等于每行是独立样本。

## 二、分母和字段边界

`lineage_id` 是必填的局部结构依赖标识。相同 ID 的行不能因为决策日期不同或标签从 H1 变成 H2、从 L1 变成 L2，就在 independence-adjusted 统计中拆成独立观察。不同 ID 也不能自动证明独立；同一标的不同局部段、公共市场状态、相同数据重审和结果 artifact 复制都需要另行审计。

`market_context_id` 是可选的人工市场状态依赖标识，不由回放器或图表程序推断。当前 60 条合同没有该字段，所以 engine 可以保留逐行描述性结果和现有依赖诊断，但不能输出经市场状态控制的独立性调整胜率。缺失值必须保持缺失，不能写成 `independent`、`independence-adjusted` 或普通非事件的替代语义。

selection 文件仍只承担冻结前的方向、pattern、lineage 和入场几何；replay/result 才承担成交、退出和 `realized_R`。回放结果不能反向创建 `lineage_id` 或 `market_context_id`，也不能因为结果较好而选择某个共享组的代表行。

外部 `results.csv`/`summary.json` 的重复 sample、合同族、共享市场状态和持仓区间由[`回放 lineage 与样本独立性审计`](replay_lineage_independence_audit_2026-08-29_CN.md)统一隔离；本审计不把 artifact 的重复副本重新加入 H/L 合同分母，也不重写历史结果。

## 三、报告表述修正

本次发现并修正了“不同 lineage”容易被标题或简写读成“独立样本”的地方：

1. 首批报告改为“使用不同的 lineage 标识”，并明确 5 条合同均没有 `market_context_id`。
2. 第二批报告将“三个独立 lineage”改为“三个记录了不同 lineage 的冻结合同”，并把“各自独立”改为“各自记录了不同的 `lineage_id`”。
3. 大样本 selection/replay 报告补上 31 个 lineage、6 个共享组、12 条依赖行和 `market_context_id=0/37`，不让 31 被误读成 31 个独立市场样本。
4. 下一批报告把“独立性”改为“依赖记录”，并明确不同 lineage 与缺失市场状态不能推出独立性；next5 同样保留“本批内唯一”而不写成跨市场独立。

这些修正只改可读性和证据边界，没有修改 CSV、engine 有效语义、历史成交结果、胜率分母、空间分层或任何 pattern 规则。

## 四、最终范围声明

当前 7 份 H/L 合同可用于按行、按标签、按方向和按 lineage 的描述性研究；共享 lineage 和缺失 `market_context_id` 使 independence-adjusted 胜率不可计算。下一批如果要声称独立性，必须在回放前冻结唯一 `sample_id`、规范 `lineage_id`、可比较的 `market_context_id` 以及输入/结果 provenance；即使这些字段齐全，也不能跳过市场状态和持仓重叠审计。

本文件只属于 **PA Research**（PA Research only）。范围声明：**no Codex Trading**、**no quantitative scanner**、**no Execution Agent**；不连接 Futu/OpenD，不新增回放分母。

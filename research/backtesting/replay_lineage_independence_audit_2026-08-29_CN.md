# 回放 lineage 与样本独立性审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 的冻结合同、历史 `results.csv/summary.json` artifact、回放 engine 和索引文档<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计边界

本次只检查仓库已有合同、已有历史回放 artifact 和已有价格结果，不抓取新行情、不新增标的、不新增冻结合同、不改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。外部 artifact 只读检查，不覆盖、不修写；旧结果不会被静默改成新版本。

本审计把“独立”拆成四个必须分别记录的轴：

1. 同一父级结构、A/B 回调或局部尝试是否共享 `lineage_id`；
2. 是否是同一 `sample_id`、同一合同族或重复 artifact；
3. 不同标的是否共享已记录的市场状态 `market_context_id`；
4. 同一标的的实际持仓区间是否重叠。

不同 `lineage_id` 只能说明人工记录使用了不同 ID，不能自动证明父级结构、市场环境或结果 artifact 独立。回放器不自动识别图表结构或市场 regime。

## 二、冻结合同盘点

| 范围 | 数量 | 结果 |
| --- | ---: | --- |
| 冻结 H/L 合同 | 7 个 CSV、60 条 | 全部 `contract_frozen=yes`；53 个规范化 lineage |
| 共享 lineage | 7 组、14 条 | 是同一父级中的 H1→H2 或 L1→L2 依赖，不是输入错误 |
| 重复 sample/合同族（跨冻结 CSV） | 0 组 | 现有冻结文件没有同一合同族的重复行 |
| 冻结 ABC_CONT、BOP、H3/L3 | 0 条 | intake/视觉案例不进入回放分母 |
| ABC/BOP intake | 6 条 ABC、4 条 BOP | 全部 `contract_frozen=no`，不与 H/L 结果混算 |
| `market_context_id` | 0/60 条已记录 | 当前冻结合同没有可机器审计的共享市场状态标识 |

7 个共享 lineage 为：

| lineage | 依赖记录 |
| --- | --- |
| `COHR-2022-04-bear-leg` | L1 2022-04-08；L2 2022-04-14 |
| `COHR-2022-06-bear-leg` | L1 2022-06-14；L2 2022-06-22 |
| `COHR-2024-06-bull-leg` | H1 2024-06-10；H2 2024-06-21 |
| `MAR-2023-01-recovery` | H1 2023-01-11；H2 2023-01-18 |
| `RBLX-2023-08-bear-leg` | L1 2023-08-11；L2 2023-08-17 |
| `RBLX-2025-11-bear-leg` | L1 2025-11-13；L2 2025-11-20 |
| `TSLA-2025-08-local` | H1 2025-08-18；H2 2025-08-21 |

这些共享组同时解释了现有 `cross_pattern_lineage_group_count`：它们跨 `H1_L1`/`H2_L2` 主标签，但没有把 ABC、BOP 或 H3/L3 混入 H/L。它们可以保留为连续尝试的路径材料，但不能按两条相互独立的样本解释。

## 三、历史 artifact 重复与冲突

在本机 PA Research artifact 目录只读盘点到 13 份 `results.csv` 和 13 份 `summary.json`：

- 13 份 `results.csv` 共 88 行、63 个不同 `sample_id`；其中 13 个 sample-id 组重复，共 38 行重复副本，额外副本 25 行；
- 精确字节重复有两组：首批 H/L `replay` 与 `replay-final` 的 5 行结果，以及 next5 的 `results_final` 与 `results_repo_inputs` 的 6 行结果；
- 旧 summary 使用 engine `0.2.0`–`0.3.1`，没有当前 `duplicate_result`、市场上下文和持仓区间依赖字段，不能和新摘要拼接成一份验证统计；
- 3 个重复 sample-id 还存在内容冲突，而不只是字节重复：

| sample_id | 冲突 | 处理 |
| --- | --- | --- |
| `PA-HL-NEXT4-CBOE-H1-20250522` | 一个 artifact 是 `decision-date-missing/unproven`，另一个是 `filled/loss` | 不能择优保留；重复结果全部隔离 |
| `PA-HL-NEXT4-ROST-H1-20260107` | 一个 artifact 是 `symbol-data-missing/unproven`，另一个是 `filled/time_exit/loss` | 不能把成功运行结果回写覆盖失败运行结果 |
| `PA-HL-NEXT5-NDAQ-L1-20220510` | 执行结果相同，但一个标为 `ordinary_non_event`，另一个标为 `earnings_adjacent` | 事件分类版本不同，不能合并 |

另有 `PA-EX-001` 冒烟样本和两个不在当前 60 条冻结合同中的 MCHP 结果（2024-08-06、2024-12-06）。它们不能并入当前冻结 H/L 研究分母。

若把 13 份 artifact 直接拼接，旧逻辑会把重复副本当作普通结果行；当前 engine `0.3.9` 会识别重复 sample/合同族并把全部副本标为 `duplicate_result`，不任意选择其中一份。该修复是统计防护，不是对旧结果进行重算或删改。

## 四、同一标的局部段与共享市场状态

对去重后的历史结果按实际 `entry_date`–`exit_date` 检查：

- 没有发现同一标的的实际持仓区间重叠；这只能说明当前这些已成交结果的持仓时间没有相交，不能证明它们来自完全不同的父级结构；
- 发现 3 组跨标的共享交易日区间：COHR 2022-08-23–24 与 MAR 的持仓区间重合；RBLX 2026-01-26 与 ROST 重合；RBLX 2026-01-27–29 与 ADBE 重合；
- 这些共同交易日不是“同一 pattern”的证明，也不自动等于统计依赖，但当前合同没有 `market_context_id`，因此无法把共享市场状态纳入可验证的独立性分组；
- NDAQ 的多条 L1 记录使用不同 lineage 且时间不重叠，但“同一标的不同日期”本身仍不能自动升级为独立样本。

因此，当前报告可以给出按合同/lineage 的描述性行数和结果，但不能给出经过市场状态和 artifact provenance 控制的 independence-adjusted 胜率。

## 五、已落实的防护

engine `0.3.4` 首次增加了统计隔离字段；当前 engine `0.3.9` 在其基础上继续保留并补充：

1. `sample_id` 与规范化合同族（symbol/date/direction/pattern/label/lineage）的重复检测；重复行全部排除出 `completed_trade_count`，并通过 `duplicate_result` bucket 保留；
2. `lineage_id` 的大小写/首尾空格规范化用于依赖统计；共享 lineage 时撤回 independence-adjusted 胜率；
3. 可选人工字段 `market_context_id`，缺失或共享时撤回 independence-adjusted 胜率；回放器不自行推断市场状态；
4. 同一标的已成交持仓区间重叠检测，报告 `exposure_overlap_group_count` 和 `exposure_overlap_row_count`；
5. 输出 `unique_sample_id_count`、重复 sample/合同族计数、市场上下文计数、独立性状态和结果 bucket；
6. `run_metadata.json` 增加 `engine_version`、`backtesting_version`、Python/pandas/numpy 运行时版本、`engine_source_sha256`、`price_file_sha256`、`contract_file_sha256`、`result_set_sha256`、`results_file_sha256` 和结果行数，用于识别同一输入的重复 artifact、同一输入的不同版本和未锁定执行代码/运行时的旧结果。

这些字段只做 provenance 和统计隔离，不创建量化扫描器、不自动识别 PA pattern、不连接 Execution Agent。

## 六、结论与边界

本次确认了真实的 artifact 重复/冲突，并将其从回放完成分母中隔离；同时把“共享 lineage”“共享市场状态”和“持仓重叠”分成不同依赖轴。当前冻结合同没有市场状态标识，历史 summary 又存在旧版本和重复副本，所以不能把合并后的漂亮点估计当成独立样本胜率。

本次没有新增 ABC、BOP、H3/L3 或 H/L 正向样本，没有改变 PA Research 规则，也没有扩大有效分母。结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

下一批若要研究跨标的或同一标的的独立样本，必须在回放前明确 `lineage_id`、唯一 `sample_id`、可比较的 `market_context_id`、合同/价格文件指纹，并保留事件、空间和结果口径；不能事后从结果好坏选择代表 artifact。

本文件只属于 PA Research，不修改 Codex Trading，不导入其规则，不创建量化扫描器，不连接 Execution Agent 或 Futu/OpenD。

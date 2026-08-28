# PA Research 报告、索引与 inventory 一致性审计（2026-08-29）

结论：当前 PA Research 的报告索引、validator 必需文件、冻结合同 CSV inventory、replay 报告状态和 engine/dependency 版本声明相互一致，没有发现需要改写当前合同、价格输入或历史结果的事实错误。本轮增加动态一致性回归测试，固定这些边界；没有新增样本、没有运行正式回放。当前结论继续为 `no-new-positive`，`validated win-rate: not-computable`。

## 1. 当前 checkout 的事实基线

只读取 `research/backtesting/` 和当前 engine，得到：

| 项目 | 当前值 |
| --- | ---: |
| CSV 总数 | 18 |
| 非示例冻结合同 CSV / 行数 | 7 / 60 |
| 示例合同 CSV / 行数 | 1 / 1 |
| ABC/BOP intake CSV / 行数 | 2 / 25 |
| 价格快照 CSV | 8 |
| 冻结合同方向 | long 32、short 28 |
| 冻结合同内部标签 | H1 24、H2 8、L1 22、L2 6 |
| 冻结合同主标签 | H1_L1 46、H2_L2 14 |
| 冻结合同订单分支 | stop_confirmation 60 |
| 冻结合同 lineage | 53 个，7 个共享组、14 条记录 |
| 冻结合同空间字段 | strict_ge_1R 9、borderline_ge_1R 1、未知 50 |
| ABC/BOP intake 主标签 | ABC_CONT 6、BOP 4 |

这些值与合同 inventory、人工冻结合同覆盖、字段分层和 lineage 审计中的当前数据相符。intake 仍全部为 `contract_frozen=no`，使用 `intake_id` 而非 `sample_id`，不进入回放分母。

## 2. 报告、索引和版本交叉核对

- `research/README.md` 与 `research/backtesting/README.md` 均有当前 inventory、parity 和本审计入口；validator 的必需文件清单包含本审计报告。
- 当前文件名含 `replay` 的 Markdown 报告共 11 份；每份都包含 `no-new-positive`、`validated win-rate: not-computable` 和当前维护 engine `0.3.9` 的历史/当前边界说明。
- 当前 engine 为 `0.3.9`；本次审计读取的 `pa_research_backtest/engine.py` SHA-256 为 `49afdf1649d33a911397509a1a9431edcab1ce4519399e8be18bd22129688c3a`。研究依赖仍固定为 `backtesting==0.6.6` 与 `matplotlib==3.10.9`。
- 当前 checkout 没有 `results.csv`、`summary.json` 或 `run_metadata.json`；artifact inventory 中的 7 组合同/价格输入与当前 7 个冻结合同文件对应。此前在本机 artifact 目录发现的 13 组历史结果三件套属于外部历史 provenance，不是当前 checkout，也没有被本轮重新写入或混入。
- 历史审计中的测试数量和 Markdown/link 数量（例如早期报告的 73/63 个测试、263/1232 个文档统计）保留为各自审计时的快照；本轮不把它们冒充当前值，也不因当前测试增长而重写历史审计证据。

## 3. 已固化的防回归

新增 `tests/test_pa_research_report_inventory_consistency.py`，只读取文件并检查：

1. CSV 分类、行数、方向/标签/订单/空间/EMA/lineage/event 字段分布与现有审计表一致；
2. ABC/BOP intake 的数量和冻结边界没有进入正式合同；
3. 11 份 replay 报告均保留当前版本语境和两项总体验证边界；
4. 当前 checkout 的 artifact 数量为零，engine 版本、源码 hash、依赖版本和索引/validator 入口一致。

测试不下载行情、不读取交易账户、不运行正式回放、不写 artifact，也不改变任何 engine 有效语义或 pattern 规则。

## 4. 验证记录

本轮专项一致性测试、全套单元测试、文档 validator、Python 编译检查和 `git diff --check` 均通过；最终记录为 1 个一致性专项测试、`76` 个单元测试、`265` 个 Markdown 文件和 `1236` 个链接。临时历史 artifact 只读检查和所有测试 fixture 均不写回仓库。

## 5. 统计结论与范围

本轮没有发现可以支持新增正向结论的证据；没有新增回放分母，没有把历史 artifact、intake、H/L、ABC、BOP 或 H3/L3 混算。当前状态保持：

```text
research_state: provisional
validated win-rate: not-computable
conclusion: no-new-positive
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

# PA Research 合同 CSV inventory 与资格边界审计（2026-08-29）

结论：本轮只读盘点现有 CSV，没有发现需要改写的真实合同数据错误。已把 loader、方向/标签/订单/入场几何和 intake 隔离边界加入回归测试；没有下载行情、运行正式回放或增加胜率分母。当前结论继续为 `no-new-positive`，`validated win-rate: not-computable`。

## 1. 审查范围与分类

对照[`PA Research 日线选股规则`](../../docs/pa_research_daily_selection_rules_v0_1_CN.md)、[`统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)、[`冻结合同回放器`](README.md)和 engine `0.3.9`，盘点 `research/backtesting/` 下现有 18 个 CSV：

| 类型 | 文件数 | 记录数 | 处理方式 |
| --- | ---: | ---: | --- |
| 非示例冻结合同 | 7 | 60 | 用 `load_contracts` 读取，并检查 entry 几何 |
| 回放示例合同 | 1 | 1 | 单独验证为可加载的最小示例，不计研究分母 |
| ABC/BOP intake | 2 | 25 | 只作候选/缺口记录，必须 `contract_frozen=no`，不送回放 |
| 价格快照 | 8 | — | 只作历史行情输入，不计合同样本 |

## 2. 冻结合同盘点

7 个非示例冻结合同文件全部被当前 loader 接受，60/60 行为 `contract_frozen=yes`，且没有改写：

| 字段 | 当前分布 | 判断 |
| --- | --- | --- |
| `direction` | `long=32`、`short=28` | 只使用 engine 支持的方向 |
| `primary_pattern` | `H1_L1=46`、`H2_L2=14` | 历史/兼容 H/L 合同；不是当前日线候选主标签扩展 |
| `internal_label` | H1 24、H2 8、L1 22、L2 6 | 与方向和 H1/H2、L1/L2 规则一致 |
| `order_branch` | `stop_confirmation=60` | 全部是当前 engine 支持的分支 |
| `contract_state` | 空 50、`frozen_pre_outcome` 10 | 旧合同缺失的可选字段不无证据回填 |
| `space_status` | 空 50、`strict_ge_1R=9`、`borderline_ge_1R=1` | 空间未知不能从结果倒推为合格 |
| H/L EMA gate | `long_pass=27`、`short_pass=28`、失败 5 | 失败行保留 observation-only，不作为字段错误 |

现有冻结合同没有 `ABC_CONT`、`BOP` 或 H3/L3 样本。H/L 文件中的 `H1_L1/H2_L2` 是既有历史兼容合同语义；当前日线规则仍要求新候选顶层使用 `ABC_CONT/BOP`，H/L 通过内部标签记录。为了避免篡改历史合同语义，本轮不把旧 CSV 的主标签批量改写。

## 3. Intake 与回放边界

两个 intake CSV 共 25 行，均为 `contract_frozen=no`；按 `symbol + decision_date + source_case` 归并后是 22 个底层案例键，其中 3 个案例同时出现在两种 intake 视图中，不能把 25 行当成 25 个独立案例：

- `abc_bop_contract_intake_2026-08-28.csv`：10 条，主标签为 `ABC_CONT/BOP`，保留分支选择、事件、空间、lineage 或数值字段缺口；
- `bop_contract_intake_2026-08-28.csv`：15 条，保留接受、同日回测、缺口/事件和多日回踩边界；其中 `order_branch` 可能是研究层的复合或 `observation_only` 状态。

两者使用 `intake_id` 而不是 `sample_id`，不能通过回放合同的必需列检查。测试明确要求 intake 仍为 `contract_frozen=no`，并确认调用 `load_contracts` 会拒绝它们；因此它们不会被误送入当前回放器或胜率分母。

## 4. 组合与几何检查

对 60 条冻结合同进行只读组合检查：

- `sample_id` 重复数：0；合同族重复数：0；
- 多空与 H/L 方向映射错误：0；
- `H1_L1/H2_L2` 与内部标签映射错误：0；
- `stop_confirmation` 下的 stop、首障碍、目标相对入场方向错误：0；
- 当前回放支持的订单分支之外的冻结输入：0。

这证明当前 inventory 可被安全地区分为“冻结回放合同”“运行示例”“候选 intake”和“价格文件”，但不证明任何 pattern 的胜率或独立性。旧合同的空白空间字段、共享 lineage、事件过滤状态和缺失市场上下文仍按既有审计规则隔离。

## 5. 已完成的防回归修正

在[`test_pa_research_contract_consistency.py`](../../tests/test_pa_research_contract_consistency.py)中新增：

1. 所有非示例 `*contracts*.csv` 必须通过当前 loader、支持的枚举和入场几何校验；
2. 所有 `*intake*.csv` 必须保留 `intake_id`、`contract_frozen=no`，且不能被当作回放合同；
3. 示例合同继续固定为 `ABC_CONT + H1 + stop_confirmation + frozen=yes`。

没有修改 `pa_research_backtest/engine.py`、任何 CSV 的历史值或有效执行语义；没有创建量化扫描器、没有连接 Execution Agent、没有修改 Codex Trading。

## 6. 验证与统计结论

本轮使用 6 个合同一致性回归测试，并运行全套仓库测试、文档 validator、Python 编译检查和 `git diff --check`：全套 `73` 个单元测试通过，文档校验通过（`263` 个 Markdown 文件、`1232` 个链接）。这些检查不下载数据、不运行正式回放、不产生新的统计样本。当前状态保持：

```text
document_maturity: provisional
validated win-rate: not-computable
conclusion: no-new-positive
```

# H/L 报告空间、版本与结论表述一致性审计（2026-08-29）

日期：2026-08-29<br>
范围：H/L selection/replay 报告、`research/backtesting/README.md`、`research/README.md` 及相关研究索引<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计目的与当前基准

本轮只读核对 H/L 报告中 `>=1R`、strict-space、validated win-rate、60% 目标、历史 engine 版本和 `no-new-positive` 的语义。没有下载行情、没有看新图、没有运行回放、没有新增样本，也没有改变 pattern 规则或 engine 有效语义。

当前维护基准是 `pa_research_backtest.engine.ENGINE_VERSION = 0.3.9`。当前正式空间资格只能从事前合同中的 `pre_entry_space_R` 与 `space_status` 派生：`strict_ge_1R` 表示显式严格空间，`borderline_ge_1R` 表示显式边界空间；缺少这组字段时，engine 必须保留 `unknown_contract_space`。由 `entry_trigger`、`structural_stop` 和 `first_obstacle` 计算出的数值仍有研究价值，但在旧合同中只是历史几何审计值，不能回填成当前显式空间状态。

## 二、覆盖和机器事实

本轮覆盖 6 份 H/L selection 报告和 8 份 H/L replay 报告。首批、第二批的 replay 文件同时保留冻结前段和结果段；其余批次分别有 selection/replay 文件。相关索引与回放 README 也逐项核对。

| 合同输入分组 | 行数 | 显式空间字段 | 当前 engine 空间语义 |
| --- | ---: | --- | --- |
| 首批、第二批、大样本、下一批 | 50 | 没有 `pre_entry_space_R/space_status` | 全部 `unknown_contract_space` |
| 下一批（二）、下一批（四）、下一批（五） | 10 | 有两列 | 9 条 `strict_ge_1R`、1 条 `borderline_ge_1R` |
| 合计 | 60 | — | 9 strict / 1 borderline / 50 unknown |

旧合同中的历史几何数量为：大样本 `5/32`（`>=1R/<1R`），下一批为全部 `>=1R`；这些数值不等于当前显式 `space_status`。当前 60% 仍是待检验目标，不是生产规则；历史点估计、胜率和实现 R 仍只能是描述性结果。所有 H/L replay 报告继续保留 `validated win-rate: not-computable` 和 `no-new-positive`。

## 三、发现和修正

### 1. 旧大样本选择报告的空间标签

`hl_large_selection_2026-08-27_CN.md` 原把 32 条历史几何 `<1R` 直接称为 `borderline`。但该 CSV 没有显式 `space_status`，按当前 engine 只能得到 `unknown_contract_space`。现改为“冻结时历史几何空间 `>=1R/<1R`”，并明确这只是历史几何分组；低于 `1R` 的行可以做路径审计，但不是当前严格可入场资格。

### 2. 大样本 replay 的严格子集名称

`hl_large_replay_2026-08-27_CN.md` 原使用“严格空间子集/严格合同”描述 4 条历史几何达到 `>=1R` 且 EMA 通过的行。报告本身已经说明旧 CSV 的当前 bucket 全部未知，因此该名称容易与当前显式 `strict_ge_1R` 混淆。现统一改为“历史几何空间 `>=1R` 且 EMA 通过的敏感性子集”，保留原有 4 条、1 条完成和全部统计数字不变。

### 3. 旧首批/第二批结果表的空间标签

旧首批和第二批 replay 表原使用 `positive/borderline`，虽然上方已经说明合同缺少显式空间字段。现改为“历史几何 `>=1R/<1R`”，并保留 `valid_no_trade` 等研究裁决；没有改写任何成交、胜负、`realized_R` 或 Wilson 区间。

### 4. 1.40R/1.50R 自定义切片

下一批（二）的 `>=1.40R`、下一批（四）和下一批（五）的 `>=1.50R` 都是报告内部的附加敏感性分层，不是当前 canonical `strict_ge_1R` 的替代阈值，也不是新的 `space_status` 枚举。现将表格标签和说明统一改为“敏感性子集”；下一批（二）保留 TOL=`strict_ge_1R`、VEEV=`borderline_ge_1R`，下一批（四）和（五）的显式合同状态仍分别为 2 条和 6 条 `strict_ge_1R`。

## 四、版本与结论核对

- 8 份 H/L replay 均保留“历史 engine 版本”和当前维护 engine `0.3.9` 的区分；旧 `0.3.0`、`0.3.1` 只代表对应历史 artifact 或运行口径，不因文档修订而变成当前回放结果。
- selection 报告继续是 `frozen_pre_outcome` 或候选边界记录，不要求写入 `validated win-rate`；replay 报告继续明确 `validated win-rate: not-computable`。
- 60% 点估计没有被升级成规则验证，`no-new-positive` 没有被任何历史 2/2、3/5 或 13/17 结果覆盖。
- 本轮没有新增回放分母、没有把历史几何改写成显式 strict-space、没有把任何 `unknown/pending` 升级成普通非事件或已验证胜率。

## 五、索引和回归保护

本审计已加入 `research/README.md`、`docs/README.md`、`strategy/README.md`、`patterns/README.md` 和 `research/backtesting/README.md`，并加入文档 validator 的必需文件清单。回归测试固定以下边界：

1. 无显式空间列的旧合同必须在相关报告中保留 `unknown_contract_space` 与历史几何说明；
2. `1.40R`/`1.50R` 只能作为敏感性切片，不能再标成 canonical strict-space；
3. H/L replay 必须保留当前 engine 语境、60% 待检验目标、`no-new-positive` 和 `validated win-rate: not-computable`；
4. 60 条冻结合同的显式空间分布、版本边界和索引入口必须与机器文件一致。

## 六、结论和范围

修正后，H/L 报告已把历史几何、当前显式空间状态、附加敏感性分层、描述性胜率和 validated win-rate 清楚分开。历史结果数字、合同身份、engine 有效语义和 `no-new-positive` 均保持不变。

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 **PA Research**（PA Research only）。范围声明：**no Codex Trading**、**no quantitative scanner**、**no Execution Agent**；不连接 Futu/OpenD，不创建新回放分母。

# 事件、空间与独立性字段引用一致性审计（2026-08-29）

状态：`research_only / audit_only / no-new-positive`

## 结论

本次只读取 PA Research 已提交的冻结合同、选择记录、回放报告和索引，未下载行情、看新图、运行回放、增加样本或改变 pattern/engine 有效语义。审计确认：`event_context`、空间字段和身份字段必须保留各自的来源；`event_bucket` 与 `contract_space_bucket` 是由入场前字段保守派生的报告轴，不是可以由结果回填的事实。

发现并修正一处明确的跨文件表述问题：`hl_next_contracts_2026-08-27.csv` 的旧表头没有 `pre_entry_space_R` 或 `space_status`，所以其中按触发、止损和第一障碍算出的 `>=1R` 只是冻结时历史几何，不能称为显式事前 strict-space 字段。原 `research/backtesting/README.md` 把它写成“全部通过事前空间字段”，选择和 replay 报告也容易让读者只看到 `>=1R`；现在统一标注为历史几何，当前 engine 的 `contract_space_bucket` 保留为 `unknown_contract_space`。

## 一、盘点范围与机器事实

| 范围 | 数量 | 结果 |
| --- | ---: | --- |
| 非示例冻结合同 | 7 个 CSV / 60 条 | 方向、标签、`event_context`、`lineage_id` 均有记录 |
| 旧空间合同 | 4 个 CSV / 50 条 | 没有显式 `pre_entry_space_R/space_status`，空间为 `unknown_contract_space` |
| 新空间合同 | 3 个 CSV / 10 条 | 9 条 `strict_ge_1R`、1 条 `borderline_ge_1R` |
| `market_context_id` | 0/60 | 不能计算市场状态控制后的独立性调整胜率 |
| `lineage_id` | 60/60 | 53 个唯一 lineage、7 个共享组、共享组共 14 条 |
| 选择记录 / replay 报告 | 6 / 11 | 选择记录事前，replay 报告承担结果；没有把结果写回合同 |

当前 engine `0.3.9` 对 60 条原始 `event_context` 的保守 `event_bucket` 分布为：

| `event_bucket` | 条数 |
| --- | ---: |
| `ordinary_non_event` | 11 |
| `event_reviewed_non_event` | 3 |
| `event_driven` | 4 |
| `earnings_adjacent` | 1 |
| `event_unverified_or_pending` | 40 |
| `unknown` | 1 |

`event_unverified_or_pending`、`unknown`、`sector_context_pending`、`public_price_reaudit` 等状态没有被升级为 `ordinary_non_event`。同样，50 条旧合同的缺失空间字段没有被历史价格几何或 replay 结果反向升级为 `strict_ge_1R`。这些数量与现有[`事件与首障碍空间资格审计`](event_space_eligibility_audit_2026-08-29_CN.md)、[`冻结合同字段覆盖与分层完整性审计`](frozen_contract_field_partition_audit_2026-08-29_CN.md)及[`批次报告数字与分层一致性审计`](batch_report_numeric_consistency_audit_2026-08-29_CN.md)一致。

## 二、字段来源和组合边界

### 1. 事件

`event_context` 是冻结合同中的事前原始说明；`event_bucket` 由 engine 根据该字段派生，用于隔离普通非事件、事件驱动、财报邻近、未核实/待定和未知状态。replay/result 中的派生副本只能用于报告 mismatch，不能覆盖合同中的 `event_context`。本次没有发现 `unknown/pending` 被结果字段反向改成普通非事件的记录漂移。

### 2. 空间

显式 `pre_entry_space_R` 与 `space_status` 才能形成当前可审计的 `strict_ge_1R` 或 `borderline_ge_1R`。`hl_next` 的 5 条记录只有合同价格字段，冻结时历史几何为 `>=1R`，但 CSV 没有这两个显式字段，必须保留 `unknown_contract_space`。首障碍到达、成交、胜负或 `realized_R` 都不能反向生成事前空间资格。

### 3. 独立性

`lineage_id` 控制同一父级结构、A/B 回调或局部尝试的依赖关系；共享 lineage 不能被当成独立统计样本。不同 `lineage_id` 也不自动证明市场环境独立，因为当前 60 条合同的 `market_context_id` 为 0/60。重复 sample/合同族、共享市场状态和持仓重叠仍需分别审计，不能用结果好坏选择代表记录。详细背景见[`回放 lineage 与样本独立性审计`](replay_lineage_independence_audit_2026-08-29_CN.md)。

## 三、已修正内容与防回归

1. `research/backtesting/README.md` 不再把 `hl_next` 的历史几何写成显式事前空间字段，并明确 `unknown_contract_space`。
2. `hl_next_selection_2026-08-27_CN.md` 将表头改为“冻结时历史几何空间（未写入显式 CSV 字段）”，并声明不能由回放结果补写 `pre_entry_space_R/space_status`。
3. `hl_next_replay_2026-08-27_CN.md` 将 `5/5 >=1R` 改为“冻结时历史几何空间审计（非当前显式 strict-space）”，保留原有成交和描述性结果，不改结果数值。
4. 文档 validator 增加旧合同字段缺失时的跨文件文案保护；回归测试固定事件、空间、lineage 的数量和索引入口。

本次没有改写 CSV、结果 artifact、事件分类函数、空间计算函数、lineage 记录或任何 pattern 规则。没有结果字段反向推导 `event_context`、`space_status`、`lineage_id` 或 `market_context_id`。

## 四、统计结论与范围声明

本审计只证明字段来源和报告表述边界，不能增加胜率分母，也不能把历史几何或不同 lineage 解释成独立验证样本。当前 `validated win-rate: not-computable`，总体结论保持 `no-new-positive`。

本文件只属于 **PA Research**（PA Research only）。范围声明：**no Codex Trading**、**no quantitative scanner**、**no Execution Agent**；不调用 Futu/OpenD，不连接任何执行系统。

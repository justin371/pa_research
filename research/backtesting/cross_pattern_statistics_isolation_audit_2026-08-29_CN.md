# 跨 Pattern 统计隔离审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 的 ABC_CONT、BOP、H1/L1、H2/L2、H3/L3 机器可读输入、冻结合同和回放摘要边界<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计口径

本次只检查仓库已有合同 CSV、回放适配层和研究索引，不重新选股、不重画历史图表、不把 Codex Trading 的规则带入 PA Research。`contract_frozen=yes` 才能进入回放；intake CSV 只记录候选和缺口，不是交易样本。

统计必须同时区分：

- 主 Pattern：`ABC_CONT`、`BOP`、`H1_L1`、`H2_L2`、`H3_L3`；
- 内部标签：H1、H2、L1、L2、H3、L3；H3 和 L3 不再使用合并标签；
- 订单分支、事件状态和 `lineage_id`；
- 已成交结果、开盘跳过、观察样本、未完成 horizon 和同 K 线止损/目标冲突。

## 二、当前仓库盘点

| 范围 | 记录 | 结论 |
| --- | ---: | --- |
| 冻结 H/L 合同 | 7 个 CSV、60 条 | `contract_frozen=yes`；32 条多头、28 条空头 |
| 冻结 H/L lineage | 53 个 | 7 组共享 lineage、共 14 条；主要是同一父级中的 H1→H2 或 L1→L2 |
| 冻结 ABC_CONT | 0 条 | 只有视觉案例和未冻结 intake，不进入回放分母 |
| 冻结 BOP | 0 条 | 只有接受/同日回测/缺口/多日回踩边界 intake，不进入回放分母 |
| 冻结 H3/L3 | 0 条 | 当前没有三推机器合同，不能把空缺解释为零胜率 |
| ABC/BOP intake | 6 条 ABC、4 条 BOP | 全部 `contract_frozen=no`，不与 H/L 结果混算 |

现有冻结文件没有发现重复的合同族：同一 `symbol + decision_date + direction + primary_pattern + internal_label + lineage_id` 没有两条替代订单分支同时进入同一文件。共享 lineage 不是错误，但它表示依赖，不能当作相互独立样本。

## 三、发现与修复

### 1. 冻结合同缺少 lineage 防护

此前 loader 只检查 `sample_id` 是否重复，`lineage_id` 可以缺失；因此相同父级走势可能在统计上看起来像独立样本。现已将 `lineage_id` 纳入冻结合同必填字段，并在 loader 中拒绝同一合同族的重复行。现有 60 条冻结合同均已填写 lineage，未触发迁移删除。

### 2. 摘要没有显式显示依赖状态

此前摘要保留并按 `lineage_id` 分层，但顶层 `win_rate_pct` 仍是记录行数口径，容易被误读成独立样本胜率。现已增加：

- `unique_lineage_count`；
- `missing_lineage_count`；
- `shared_lineage_group_count` 和 `shared_lineage_row_count`；
- `cross_pattern_lineage_group_count`；
- `independence_status`；
- `independence_adjusted_win_rate_pct` 与 `independence_statistics_status`。

有共享或缺失 lineage 时，摘要保留行数口径的描述性结果，但不输出 independence-adjusted 胜率；这不是把共享 lineage 粗暴删掉，而是避免未经预先规则选择代表合同。

### 3. H3/L3 不能合并成一个内部标签

`primary_pattern=H3_L3` 仍表示三推研究家族，但 `internal_label` 现在必须明确为 `H3` 或 `L3`；`internal_label=H3_L3` 被视为含混输入并拒绝。H3 只能配 `direction=long`，L3 只能配 `direction=short`，两者的方向统计和结果统计因此可以分开。当前没有 H3/L3 冻结样本，所以本修复没有增加任何胜率分母。

### 4. 主标签与内部标签必须保持边界

回放 loader 现在还会拒绝以下混入：

- `H1_L1` 搭配 H2/L2；
- `H2_L2` 搭配 H1/L1；
- `BOP` 使用 H/L 或 H3/L3 作为内部标签；BOP 相关信息应放在 `secondary_context`；
- 同一合同族用不同订单分支重复计数。

这不是新增交易 setup，而是把已有 PA Research 规则中的主合同、内部计数和角色转换落实为输入完整性检查。

## 四、统计解释边界

现有 H/L 回放批次的历史描述性胜率仍按各自报告保存；本审计不重算、不合并，也不把不同批次的点估计升级为验证胜率。共享 lineage 的 H1/H2 或 L1/L2 可以用于观察连续尝试的路径，但必须在结果解释中标记依赖。

`ABC_CONT`、BOP 和 H3/L3 目前没有冻结回放分母，因此不能回答这些 Pattern 的胜率或盈亏比。`no-new-positive` 与 `validated win-rate: not-computable` 保持不变。

## 五、范围声明

本审计只属于 PA Research。它不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD，也不把 ABC、BOP、H/L、三推或事件分支混成一个统计分母。

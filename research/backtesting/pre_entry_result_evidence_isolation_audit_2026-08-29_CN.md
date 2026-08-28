# 事前证据与结果证据隔离审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 当前回放 engine、60 条冻结 H/L 合同、已有回放报告/摘要口径和输出 schema<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、结论

本轮只审计已有合同、代码和报告，不抓取新行情、不新增样本、不重写历史 artifact，也不改变 ABC/BOP/H/L/H3/L3 交易规则。审计重点是确认“入场前已经知道的证据”不会被“入场后的价格路径结果”反向写回资格字段。

审计确认并落实了三条隔离边界：

1. `event_context`、`space_status`、`pre_entry_space_R`、EMA20/50 斜率和 `h_l_ema_slope_gate` 属于事前合同证据；`first_obstacle_hit`、`space_to_first_obstacle_R`、`fill_status`、`trade_result`、`realized_R` 和 `win_rate_eligible` 属于回放结果或结果旗标。
2. `event_bucket` 和 `contract_space_bucket` 是派生分层字段。当前 engine `0.3.8` 总是从原始事前字段重算它们；结果文件中同名的旧/手工派生值只用于 mismatch 诊断，不能把实际路径上的空间或事件结果改写成事前合格条件。
3. 结果行带有 H/L EMA gate 时，`contract_eligibility` 由内部标签和 gate 重算；失败或 pending gate 即使被手工写成 `eligible`，也不能进入完成交易分母。

因此，`first_obstacle_hit=yes` 不会自动产生 `win`，`space_to_first_obstacle_R>=1` 不会自动产生合同的 `strict_ge_1R`，正的 `realized_R` 也不会自动产生 `win_rate_eligible=yes`。现有统计仍只是描述性结果，保持：

```text
no-new-positive
validated win-rate: not-computable
```

## 二、字段 provenance 矩阵

| 字段 | 所属阶段 | 当前用途 | 是否能单独进入完成分母 |
| --- | --- | --- | --- |
| `event_context` | 入场前合同 | 由人工事件审查记录，派生 `event_bucket` | 否 |
| `space_status` / `pre_entry_space_R` | 入场前合同 | 派生 `contract_space_bucket`，严格空间子集只认这一组 | 否 |
| `daily_ema20_slope` / `daily_ema50_slope` / `h_l_ema_slope_gate` | 入场前合同 | 决定 H/L 是否 eligible、observation-only 或 pending | 否 |
| `first_obstacle` | 入场前合同 | 冻结首障碍价格位置 | 否 |
| `first_obstacle_hit` | 入场后路径 | 记录持仓有效期间是否触及首障碍 | 否；不等于 win |
| `space_to_first_obstacle_R` | 入场后重算 | 使用实际成交价和实际结构风险的路径几何诊断 | 否；不能覆盖事前空间 |
| `trade_result` / `realized_R` | 入场后结果 | 记录完成路径的结果和净 R | 只能和所有完成/证据硬闸门同时成立 |
| `win_rate_eligible` | 结果旗标 | 结果行的可比性声明 | 不是单独分母 |

`first_obstacle` 仍来自冻结合同；回放后的 `space_to_first_obstacle_R` 只是使用实际成交价重新计算的过程/结果字段。两者都保留，不能把后者回填到前者。

## 三、发现的实现问题与修复

### 1. 派生 bucket 曾经信任结果文件副本

旧路径在 `summary` 已有 `event_bucket` 或 `contract_space_bucket` 时，只填充空值。这样，外部结果文件如果带有错误、旧版本或由结果路径计算出的派生值，就可能影响事件/严格空间分层。

现在的路径是：

```text
raw event_context --------------------> event_bucket
space_status + pre_entry_space_R -----> contract_space_bucket
```

已有 bucket 只与重算值比较并累加 `event_bucket_mismatch_count` 或 `contract_space_bucket_mismatch_count`；摘要后续分组只使用重算值。

### 2. H/L eligibility 曾经可以被结果行声明覆盖

结果字段中的 `contract_eligibility` 不是独立证据。当前 engine 在结果行含有 H/L gate 时从 `internal_label + h_l_ema_slope_gate` 重算它，并记录 `contract_eligibility_mismatch_count`。完成交易 mask 还要求重算后为 `eligible`，所以 `fail_flat_or_opposite`、`pending` 或方向 gate 不一致的行不能靠 `win_rate_eligible=yes` 进入分母。

对缺少 H/L gate 列的旧/最小结果 fixture，engine 不伪造 EMA 证据；这类历史描述应继续视为 provenance 不完整，不能据此升级验证统计，并以 `pre_entry_provenance_incomplete` bucket 保留描述性记录。

### 3. 严格完成分母仍然独立于结果收益

完成分母要求结果路径满足成交、可比 evidence、无歧义、horizon 完整、非重复、有限 `realized_R`、结果标签和 `win_rate_eligible` 等条件；`contract_space_bucket` 只来自事前字段，`first_obstacle_hit` 只做路径记录。正/负 `realized_R` 不参与生成事前空间或 EMA gate。

### 4. 现有价格快照的内存 smoke check

使用仓库已有的 7 组价格快照与对应 60 条冻结合同做只读内存复核：7/7 合同文件成功加载，产生 34 条完整回放行和 5 条 EMA observation-only 行；`pre_entry_provenance_status=incomplete` 为 0，`contract_eligibility_mismatch_count`、`event_bucket_mismatch_count`、`contract_space_bucket_mismatch_count` 均为 0。该次运行没有写出新的 `results.csv` 或 `summary.json`，34 条完成行也不加入任何新的官方统计分母，只用于验证当前实现不会把结果字段反向变成事前资格。

## 四、现有合同和报告边界

- 7 个冻结 H/L 合同 CSV 共 60 条，当前可由 engine `0.3.8` 加载；没有新增合同或结果分母。
- 60 条的 `event_context`、EMA gate、lineage 等合同字段仍按前一份[`冻结合同字段覆盖与分层完整性审计`](frozen_contract_field_partition_audit_2026-08-29_CN.md)分层；旧 50 条的空间字段继续是 unknown，不从结果反推严格空间。
- 现有 provenance 审计记录的历史 `summary.json/results.csv` 内部数值对应关系仍保留，但历史 engine/运行元数据缺失时只能作为描述性 evidence；不能因为重新计算出派生字段就把旧结果变成当前验证样本。
- ABC/BOP intake 与冻结 H/L 继续分开，H3/L3 没有因为本轮结果字段审计而进入 H/L 分母。

## 五、验证证据与状态

本轮新增回归测试覆盖：错误的 `event_bucket`、错误的 `contract_space_bucket`、手工升级失败 EMA gate 的 `contract_eligibility`；同时保留空间状态缺数值、重复身份、H/L 方向/EMA gate、歧义、horizon 和结果分母测试。文档 validator 也要求本报告和三个 mismatch 字段进入 canonical schema 入口。

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

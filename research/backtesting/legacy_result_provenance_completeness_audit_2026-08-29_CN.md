# 旧结果事前 provenance 完整性审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 回放结果的事前合同字段完整性、当前 engine/摘要分母路径、现有冻结合同和历史报告口径<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、问题和结论

本轮只检查已有代码、测试、合同、价格快照和报告，不下载新行情、不新增样本、不改 PA 交易规则。发现旧/最小结果行缺少 H/L EMA gate 或其他合同字段时，旧摘要路径会把它们当作普通结果字段处理；虽然最终仍标为 descriptive-only，但缺少一个明确的事前 provenance 状态，容易让 `completed_trade_count` 被误读为可比较分母。

当前 engine `0.3.9` 已补上这条边界：

- 每个结果行写出 `pre_entry_provenance_status` 和 `pre_entry_provenance_missing_fields`；
- 非 `market_close` 分支还必须保留冻结的 `planned_entry_trigger`；
- 完成分母要求 `pre_entry_provenance_status=complete`；缺少身份、合同风险/订单、人工审查、事件、冻结状态、lineage 或 H/L 必需 EMA 字段的行标记为 `incomplete`；
- `event_context` 缺失不能被 `event_bucket` 或收益结果补齐；H/L gate 缺失不能被 `contract_eligibility` 或 `win_rate_eligible` 补齐；
- 旧合同可选的 `space_status/pre_entry_space_R` 空白仍按 `unknown_contract_space` 处理，不因缺少空间字段而伪造严格资格，也不反向用 `space_to_first_obstacle_R` 补齐；显式严格/阻断状态仍必须有数值证据；
- 缺证据行进入互斥 bucket `pre_entry_provenance_incomplete`，只保留描述性记录。

因此本轮没有新增可验证胜率，仍保持：

```text
no-new-positive
validated win-rate: not-computable
```

## 二、事前 provenance 最小集合

对结果摘要而言，下列字段必须在结果发生前已经存在；它们不能由 `first_obstacle_hit`、`space_to_first_obstacle_R`、`trade_result` 或 `realized_R` 反推：

| 类别 | 字段 |
| --- | --- |
| 合同身份 | `sample_id`、`symbol`、`decision_date`、`direction`、`primary_pattern`、`internal_label`、`lineage_id` |
| 订单和风险合同 | `order_branch`、`structural_stop`、`first_obstacle`、`target_price`、`max_hold_bars`、`gap_policy` |
| 人工审查和冻结 | `label_source`、`daily_context_window`、`major_high_low_review`、`ema20_50_200_review`、`contract_frozen` |
| 事件 | `event_context` |
| H/L 专属 | H1/H2/L1/L2 的 `daily_ema20_slope`、`daily_ema50_slope`、`h_l_ema_slope_gate`、`h_l_pullback_location`、`meta_confluence` |

`space_status` 和 `pre_entry_space_R` 是严格空间子集的事前证据，但旧合同允许这两个字段为空；这时只能进入未知空间分层，不能进入显式 `strict_ge_1R` 子集。结果阶段的 `space_to_first_obstacle_R` 永远不属于事前 provenance。

## 三、分母保护

当前完成 mask 在原有成交、结果、证据、horizon、歧义、重复和有限 `realized_R` 条件之外，增加：

```text
pre_entry_provenance_status == complete
```

如果存在 H/L EMA gate 列，`contract_eligibility` 仍从内部标签与 gate 重算；gate 缺失或 pending/failed 时不能依靠结果行旗标进入分母。摘要会报告：

- `pre_entry_provenance_complete_count`；
- `pre_entry_provenance_incomplete_count`；
- `pre_entry_provenance_status_counts`；
- `pre_entry_provenance_incomplete` 互斥结果 bucket；
- 已有的 `contract_eligibility_mismatch_count`、`event_bucket_mismatch_count` 和 `contract_space_bucket_mismatch_count`。

这把“没有事前证据”和“有完整事前合同但结果亏损”分开：前者不是 loss，也不是 win，而是不能进入验证分母的 provenance exclusion。

## 四、验证结果

对仓库已有 7 组价格快照和 60 条冻结 H/L 合同做只读内存复核：7/7 合同文件成功加载，`pre_entry_provenance_status=incomplete` 为 0；34 条完整回放行和 5 条 EMA observation-only 行的三类派生字段 mismatch 均为 0。缺少 H/L gate、缺少 `event_context` 的回归案例均被排除出 `completed_trade_count`，并落入 `pre_entry_provenance_incomplete`。

本轮没有写出新的历史结果 artifact，也没有把 34 条内存复核完成行并入官方分母。现有历史 `summary.json/results.csv` 若缺少新字段，仍只能按历史描述读取；重新生成时必须使用当前 engine 和完整冻结合同，不能将旧/新结果拼成验证样本。

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

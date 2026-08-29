# H/L `event_context` 与 canonical `event_bucket` 标签一致性审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 现有 H/L 冻结合同 CSV、selection/replay 报告、回放索引和当前 engine `0.3.9`<br>
状态：`research_only / audit_only / no-new-positive`

## 结论

本次只读取现有合同、报告、索引和 engine，实现了对 7 个冻结合同 CSV、60 条合同的 raw `event_context` 与 canonical `event_bucket` 的重算。事件映射没有把未核实、待定或未知状态升级为普通非事件；当前分布仍为：`ordinary_non_event=11`、`event_reviewed_non_event=3`、`event_driven=4`、`earnings_adjacent=1`、`event_unverified_or_pending=40`、`unknown=1`。

发现一处明确的报告显示问题：`hl_next5_replay_2026-08-27_CN.md` 的成交表和统计表混用了 `ordinary`、`earnings-driven`、`earnings-adjacent` 这些 raw/叙述标签，而同一报告的 canonical 统计已经使用 `ordinary_non_event`、`earnings_adjacent`。这会让读者误以为存在额外事件 bucket。现已把 replay 分层列统一为 canonical 名称，并在 selection 记录中明确 raw 标签与 canonical bucket 的对应关系。

报告正文中的 `earnings-adjacent` 只作为人类可读别名；当前冻结 CSV 的 raw 值是 `earnings_adjacent`，不是一个新的 bucket。没有改写合同 CSV、历史结果 artifact、胜率、实现 R、样本数量、pattern 规则或当前 engine 的有效语义。

## 一、当前 engine 的映射口径

`event_bucket` 只能从冻结合同的事前 raw `event_context` 派生；结果文件中的同名字段不能覆盖它。匹配按当前 engine 的保守优先级执行：

| raw `event_context` 特征 | canonical `event_bucket` | 当前 60 条合同 |
| --- | --- | ---: |
| 含 `historical_event_filter_not_verified`、`event_context_pending`、`sector_context_pending` 或 `public_price_reaudit` | `event_unverified_or_pending` | 40 |
| 含 `event_driven`、`earnings-driven`/`earnings_driven` 或 `aftershock` | `event_driven` | 4 |
| 含 `earnings_adjacent` | `earnings_adjacent` | 1 |
| 含 `ordinary_non_event` 且没有 `gap_reprice` | `ordinary_non_event` | 11 |
| 只有事件核对/窗口外证据，如 `earnings_filter_passed`、`outside_10bar_horizon`、`setup_window_no_known_event` | `event_reviewed_non_event` | 3 |
| raw 值为 `none` | `unknown` | 1 |

第一行优先于后续行。因此带有 `sector_context_pending` 或 `public_price_reaudit` 的记录即使同时出现 earnings window 通过文字，也仍然是 `event_unverified_or_pending`；不能升级为 `ordinary_non_event`。同样，`none` 没有足够的事件核实证据，不能当作普通非事件。

## 二、逐批机器事实

| 批次 | 合同数 | canonical event bucket 分布 |
| --- | ---: | --- |
| 首批 | 5 | `event_reviewed_non_event=3`; `event_driven=1`; `unknown=1` |
| 第二批 | 3 | `event_unverified_or_pending=3` |
| 大样本 | 37 | `event_unverified_or_pending=37` |
| 下一批 | 5 | `ordinary_non_event=3`; `event_driven=2` |
| 下一批（二） | 2 | `ordinary_non_event=2` |
| 下一批（四） | 2 | `ordinary_non_event=2` |
| 下一批（五） | 6 | `ordinary_non_event=4`; `event_driven=1`; `earnings_adjacent=1` |
| **合计** | **60** | **`ordinary_non_event=11`; `event_reviewed_non_event=3`; `event_driven=4`; `earnings_adjacent=1`; `event_unverified_or_pending=40`; `unknown=1`** |

这与[`事件与首障碍空间资格审计`](event_space_eligibility_audit_2026-08-29_CN.md)、[`事件、空间与独立性字段引用一致性审计`](event_space_lineage_consistency_audit_2026-08-29_CN.md)和[`批次报告数字与分层一致性审计`](batch_report_numeric_consistency_audit_2026-08-29_CN.md)的机器事实一致。

## 三、selection/replay 与索引核对

1. selection 报告保留 raw `event_context`，因为它是入场前人工事件说明；`hl_next5_selection` 已明确写出：`earnings-driven -> event_driven`，`earnings_adjacent -> earnings_adjacent`，`ordinary_non_event -> ordinary_non_event`。选择报告中的 `earnings-adjacent` 不再被解释为新的 canonical bucket。
2. replay 的事件分层表使用 canonical `event_bucket`：`ordinary_non_event`、`event_driven`、`earnings_adjacent`。事件驱动的 aftershock 仍可在 raw 说明中保留，但不能另造统计 bucket。
3. `hl_next`、`hl_next2`、`hl_next4` 和 `hl_next5` 的 replay 表格已统一 canonical 分组名；自然语言叙述可以使用“普通非事件/事件驱动”，但凡是统计表或分组列都必须能直接对应 engine bucket。
4. 大样本 37 条合同仍明确写为 `historical_event_filter_not_verified;exploratory_only`，不生成普通非事件分母。第二批的 `sector_context_pending`/`public_price_reaudit` 仍是待定/未闭合，不生成普通非事件分母。

## 四、验证与范围边界

新增回归检查固定：7 个 CSV 共 60 条、上述 canonical 计数、pending/unknown 的保守映射、`hl_next5` canonical 分层显示和相关索引入口。未下载行情、未看新图、未运行回放、未复制或修改外部 artifact，也没有增加胜率分母。

本审计只属于 **PA Research**（`PA Research only`）。范围声明：`no Codex Trading`、`no quantitative scanner`、`no Execution Agent`、`no Futu/OpenD`。当前结论继续是 `no-new-positive`，`validated win-rate: not-computable`。

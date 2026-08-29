# H/L selection/replay 状态计数一致性审计

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

审计日期：`2026-08-29`（只读取仓库已有 CSV、selection/replay 文档和当前已记录的 artifact 选择说明；未下载行情、未看新图、未运行回放）

## 1. 结论

本审计核对 7 份有冻结合同的 H/L CSV、对应 selection/replay 文档，以及没有冻结合同的 `hl_next3` 控制批次。7 份 CSV 合计 60 条，合同数、订单分支和缺口政策沿用既有审计结果；本次只核对报告中的 `eligible`、`filled`、`no-fill`、`opening-skip`、`observation_only`、完成交易和 win/loss 计数，不新增样本或重算结果。

结论是：已有报告的主计数可以逐批对上，没有发现需要改写历史结果或统计分母的数字 mismatch。需要明确修正的是计数语义：旧报告中的 `eligible`/EMA gate 是“允许进入该历史回放层”的计数，不等同于高质量候选、严格空间通过或交易授权；`filled` 只表示历史路径有成交，不等同于 win。严格胜率分母仍只取完成、可比、事前 provenance 完整且 `trade_result=win/loss/scratch` 的交集。

当前研究结论保持 `no-new-positive`，`validated win-rate: not-computable`。

## 2. 七个冻结批次的状态对照

| 批次与证据 | CSV / selection 合同 | replay 合同 | eligible/EMA gate | filled | opening-skip | no-fill | observation-only / 其他 | completed | win / loss |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [`hl_contract_batch_replay_2026-08-26_CN.md`](hl_contract_batch_replay_2026-08-26_CN.md) | 5 | 5 | 4 | 3 | 1 | 0 | 1 `observation_only` | 3 | 1 / 2 |
| [`hl_contract_batch2_replay_2026-08-26_CN.md`](hl_contract_batch2_replay_2026-08-26_CN.md) | 3 | 3 | 3 | 3 | 0 | 0 | 0（KLAC 是空间不足的 `valid_no_trade`，不是 observation-only；旧 engine 层仍记录路径） | 3 | 3 / 0 |
| [`hl_large_selection_2026-08-27_CN.md`](hl_large_selection_2026-08-27_CN.md) / [`hl_large_replay_2026-08-27_CN.md`](hl_large_replay_2026-08-27_CN.md) | 37 | 37 | 33 | 17 | 15 | 1 | 4 `observation_only` | 17 | 13 / 4 |
| [`hl_next_selection_2026-08-27_CN.md`](hl_next_selection_2026-08-27_CN.md) / [`hl_next_replay_2026-08-27_CN.md`](hl_next_replay_2026-08-27_CN.md) | 5 | 5 | 5 | 2 | 3 | 0 | 0 | 2 | 1 / 1 |
| [`hl_next2_selection_2026-08-27_CN.md`](hl_next2_selection_2026-08-27_CN.md) / [`hl_next2_replay_2026-08-27_CN.md`](hl_next2_replay_2026-08-27_CN.md) | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 2 | 2 / 0 |
| [`hl_next4_selection_2026-08-27_CN.md`](hl_next4_selection_2026-08-27_CN.md) / [`hl_next4_replay_2026-08-27_CN.md`](hl_next4_replay_2026-08-27_CN.md) | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 2 | 0 / 2 |
| [`hl_next5_selection_2026-08-27_CN.md`](hl_next5_selection_2026-08-27_CN.md) / [`hl_next5_replay_2026-08-27_CN.md`](hl_next5_replay_2026-08-27_CN.md) | 6 | 6 | 6 | 5 | 1 | 0 | 0 | 5 | 3 / 2 |
| **合计（7 个冻结批次）** | **60** | **60** | — | **34** | **20** | **1** | **5** | **34** | **23 / 11** |

合计列只作报告状态计数的加总：`34 filled + 20 opening-skip + 1 no-fill + 5 observation_only = 60`。其中第二批的 3 条历史路径虽然记为 `filled`，但 KLAC 的当前空间裁决是 `valid_no_trade`；这是“历史路径有成交”与“当前交易资格”两层字段，不能用简单的 filled/未成交二分替代逐批说明。严格胜率分母不能由这张合计表直接计算，也不能把 60 条当成 60 个独立交易。

## 3. 无合同控制批次

[`hl_next3_selection_2026-08-27_CN.md`](hl_next3_selection_2026-08-27_CN.md) 记录 18 个候选、0 条冻结合同；[`hl_next3_replay_2026-08-27_CN.md`](hl_next3_replay_2026-08-27_CN.md) 同样记录 0 条回放成交分母、描述性胜率不可计算。它是“没有达到冻结资格”的控制状态，不是失败交易，也不能被并入 60 条冻结合同或写成 0% 胜率。

## 4. 计数语义与历史 artifact 边界

### 4.1 `eligible`、`filled` 与严格分母不是同一层

- `eligible`/EMA gate 只表示该历史报告采用的回放层允许继续检查；旧 CSV 没有显式 `pre_entry_space_R`/`space_status` 时，它可能包括历史几何不足约 `1R` 的合同。
- `filled` 只表示原冻结订单路径在该历史价格快照下被记录为成交；它不代表空间合格、事件过滤完成、图像 provenance 完整或结果为正。
- `opening-skip`、`no-fill`、`observation_only`、`valid_no_trade`、`unproven` 和不完整路径都不是 win/loss。完成交易还必须通过 `evidence_status`、`pre_entry_provenance_status`、`path_result`、horizon、intrabar 和重复/lineage 等严格检查。

第二批明确把 KLAC 的首障碍约 `0.70R` 写为 `valid_no_trade`，但历史 engine 层仍将其列在 `eligible=3 / filled=3` 的路径统计中；这不是把它升级为当前高质量正样本，而是说明“回放可检查”与“当前交易资格”必须分列显示。

### 4.2 `next4` 的旧 artifact 冲突

`hl_next4_replay` 明确指定 `replay2` 为当前报告采用的历史路径：两条合同是 `filled`，结果为 0 胜 2 负；同一 artifact 根目录下旧 `replay` 记录为两条 `unproven`，已被报告排除，不能与 `replay2` 合并。版本、输入和结果指纹冲突属于 provenance 边界，不是把两套结果择优平均，也不能增加样本。

### 4.3 版本标签

各 replay 报告保留当时运行的旧 engine `0.3.1`/`backtesting.py 0.6.6` 作为历史 provenance，同时在报告开头标明当前维护 engine `0.3.9`；旧数字不会因版本升级自动重写。selection 报告只保存事前合同，不承载成交和胜率结果。

## 5. 本次修正与边界

1. 在回放 README 中补充 `eligible`/`filled`/`completed` 的分层定义，避免把历史回放层计数读成交易授权或严格空间资格。
2. 增加本审计、索引、validator 检查和回归测试，锁定 7 个冻结批次的合同数、关键状态计数、`next3` 的零合同控制边界和 `next4` 的 artifact 选择。
3. 不修改 CSV、engine 有效语义、历史报告数字、结果 artifact 或统计分母；不重新运行回放，不创建量化扫描器，不连接 Execution Agent，不修改 Codex Trading。

当前结论仍是 `no-new-positive`；`validated win-rate: not-computable`。

范围声明：`PA Research only`；`no Codex Trading`；`no quantitative scanner`；`no Execution Agent`。

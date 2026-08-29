# H/L 订单分支、缺口政策与结果状态边界审计

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

审计日期：`2026-08-29`（只检查仓库已有文件；未下载行情、未看新图、未运行回放）

## 1. 结论

本审计只覆盖 PA Research 的 7 份 H/L 冻结合同、对应的 selection/replay 报告、当前回放 engine 和文档 validator。目标是把 `order_branch`、`gap_policy`、`entry_trigger`、`structural_stop`、`first_obstacle`、`target_price` 与订单状态分开，避免把 `opening-skip`、`no-fill`、`accepted-open` 或需要重订的缺口路径误写成成交、胜负或独立胜率分母。

机器复核得到：60/60 行都是 `stop_confirmation`；59 行预先冻结为 `gap_policy=skip`，1 行预先冻结为 `gap_policy=accept_open`；60/60 行的触发、结构止损、首障碍和目标都是有限数值，方向几何错误为 `0`，`first_obstacle=target_price` 为 60/60，`max_hold_bars=10` 为 60/60。当前没有因为这次边界审计新增可比正样本，结论仍是 `no-new-positive`，`validated win-rate: not-computable`。

## 2. 审计范围与证据

### 2.1 七份冻结合同

| 合同文件 | 行数 | `order_branch` | `gap_policy` | 数值几何 | 备注 |
| --- | ---: | ---: | ---: | ---: | --- |
| [`hl_contracts_2026-08-26.csv`](hl_contracts_2026-08-26.csv) | 5 | `stop_confirmation` 5 | `skip` 5 | 5/5 | 第一批 H/L |
| [`hl_contracts_batch2_2026-08-26.csv`](hl_contracts_batch2_2026-08-26.csv) | 3 | `stop_confirmation` 3 | `skip` 2、`accept_open` 1 | 3/3 | 含 TSM 的预冻结 accepted-open 路径 |
| [`hl_large_contracts_2026-08-27.csv`](hl_large_contracts_2026-08-27.csv) | 37 | `stop_confirmation` 37 | `skip` 37 | 37/37 | 大批次 |
| [`hl_next_contracts_2026-08-27.csv`](hl_next_contracts_2026-08-27.csv) | 5 | `stop_confirmation` 5 | `skip` 5 | 5/5 | 后续批次 |
| [`hl_next2_contracts_2026-08-27.csv`](hl_next2_contracts_2026-08-27.csv) | 2 | `stop_confirmation` 2 | `skip` 2 | 2/2 | 后续批次 |
| [`hl_next4_contracts_2026-08-27.csv`](hl_next4_contracts_2026-08-27.csv) | 2 | `stop_confirmation` 2 | `skip` 2 | 2/2 | 后续批次 |
| [`hl_next5_contracts_2026-08-27.csv`](hl_next5_contracts_2026-08-27.csv) | 6 | `stop_confirmation` 6 | `skip` 6 | 6/6 | 后续批次 |
| **合计** | **60** | **60** | **skip 59 / accept_open 1** | **60/60** | 不增加样本 |

所有 60 行还具备非空 `entry_trigger`、`structural_stop`、`first_obstacle`、`target_price` 和 `max_hold_bars`。多头遵守 `structural_stop < entry_trigger < first_obstacle/target_price`，空头遵守反向几何；本审计没有发现几何方向错误。

### 2.2 当前 engine 的状态分层

当前 `engine 0.3.9` 的可回放 `order_branch` 是 `stop_confirmation`、`limit_retest` 和 `market_close`；`gap_policy` 的允许值是 `accept_open`、`skip`、`flag_only`、`not_applicable`。`market_close` 只能使用 `not_applicable`，其他可回放分支不能使用它。

- `no-fill`：没有出现合同规定的触发/回测机会；不是亏损，也不能进入胜率分母。
- `opening-skip`：开盘越过原触发/订单区，且冻结政策是 `skip`；原合同不成交，不能沿用原触发价，也不是亏损。
- `accept_open`：只有在入场前已经冻结该政策，并且实际开盘价通过方向、结构止损和空间的重新检查时，才可以记录实际开盘成交；成交价是实际开盘价，不是原触发价。
- `flag_only`：可以记录实际开盘路径，但必须保留缺口旗标；若实际价格使几何失效，则标为需要重订/未证实，不能假定成交。
- `unproven`：缺口重定价或路径证据不足以证明合同可成交；不是 loss，不进入严格完成成交数。
- `filled`：只有实际触发/成交路径成立时才记录；`trade_result=win/loss/scratch` 还必须同时满足完整 horizon、路径、provenance 和其他严格分母条件。

结果字段 `fill_status` 与选择记录字段 `actual_fill_or_open_skip` 分开维护。任何结果都不能反向改变事前冻结的 `gap_policy`、触发、止损、首障碍、目标或 `order_branch`。

### 2.3 已有 accepted-open 案例

合同 [`hl_contracts_batch2_2026-08-26.csv`](hl_contracts_batch2_2026-08-26.csv) 中的 `PA-HL2-TSM-L1-20250325` 是唯一一条 `gap_policy=accept_open`：空头 `stop_confirmation`，原触发 `179.80`，结构止损 `184.00`，首障碍/目标 `170.43`。对应历史报告[`hl_contract_batch2_replay_2026-08-26_CN.md`](hl_contract_batch2_replay_2026-08-26_CN.md)记录次日开盘约 `179.23` 低于原触发，并明确按预先冻结的 accepted-open 路径使用实际开盘价；它没有把旧触发价写成成交价，也没有把这条路径和 59 条 `skip` 合同混为同一分支。

这只是已有历史记录的状态审计，不是本次新增回放或新增样本。

## 3. 本次修正

1. 在统一输出合同、日线候选卡、视觉复核卡和日线选股合同中补充 `gap_policy` 字段，要求订单政策在入场前冻结。
2. 在回放 README、订单风险合同、跨周期复核和订单分支视觉协议中明确：`skip` 才产生 `opening-skip`；预先冻结且重验证通过的 `accept_open` 才能产生实际开盘成交；`no-fill`、`opening-skip` 和 `unproven` 不得写成 win/loss。
3. 保持 `order_branch` 与 `branch_role` 分离；缺口重订仍是研究分支，不会静默改写为普通 stop 或把后来的回测合并到原合同。
4. 增加回归测试与索引/validator 检查，锁定 7 份合同的 60 行计数、59/1 缺口政策分布、数值几何和状态边界。

没有修改 CSV、engine 有效语义、历史结果、统计分母或样本；没有创建量化扫描器，没有连接 Execution Agent，也没有修改 Codex Trading。

## 4. 统计边界与当前研究结论

本审计确认的是订单状态和证据边界，不是胜率回测。`opening-skip`、`no-fill`、`unproven` 和缺少完整事前 provenance 的记录不构成严格胜率分母；共享 lineage、市场状态缺失和历史图表证据不足仍按既有审计规则处理。因此不能从这 60 条合同推出 60 条独立交易，也不能推出达到 60% 胜率或任何收益保证。

当前研究结论保持：`no-new-positive`；`validated win-rate: not-computable`。

范围声明：`PA Research only`；`no Codex Trading`；`no quantitative scanner`；`no Execution Agent`。

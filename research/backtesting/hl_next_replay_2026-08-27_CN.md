# H/L 下一批分层回放审计（2026-08-27）

状态：`research_only / descriptive_only / not-validated / no-new-positive`

本报告保留当时历史回放的运行口径；其中的旧 engine 版本不是当前维护版本。当前 PA Research engine 为 `0.3.9`，历史数字不会因版本升级自动变成当前验证结果。

## 结论

本批 5 条人工看图冻结合同，按冻结的 `entry_trigger`、`structural_stop` 和 `first_obstacle` 做事前价格几何计算，均达到 `>=1R`；它们也均通过对应的 Daily EMA20/EMA50 方向闸门。但旧合同 CSV 没有显式 `pre_entry_space_R/space_status`，所以当前 engine 的 `contract_space_bucket` 仍应视为 `unknown_contract_space`，不能把这段历史几何值当成当前显式 strict-space 字段。只有 2 条实际成交并完成，且全部属于事件驱动分组；3 条普通非事件合同都因 `gap_policy=skip` 在开盘跳过旧触发位。完成成交为 1 胜 1 负，描述性胜率 `50.00%`，Wilson 95% 区间约为 `9.45%–90.55%`。这不是对 H1/H2/L1/L2 规则的验证，60% 目标没有被验证，结论保持 `no-new-positive`。

本报告只审计 PA Research 的人工冻结合同，不自动识别形态、不自动发现股票、不创建量化扫描器、不连接 Execution Agent，也不修改 Codex Trading。

## 回放配置和证据边界

- 引擎：PA Research backtesting engine `0.3.1`；`backtesting.py 0.6.6`。
- 输入合同：[`hl_next_contracts_2026-08-27.csv`](hl_next_contracts_2026-08-27.csv)。
- 输入价格：[`hl_next_prices_2026-08-27.csv`](hl_next_prices_2026-08-27.csv)。
- 人工选择和事件证据：[`hl_next_selection_2026-08-27_CN.md`](hl_next_selection_2026-08-27_CN.md)。
- 图像证据：[`H/L 下一批人工看图回放资产`](../assets/visual_recognition/2026-08-27/hl_next_backtest/README.md)。每张图都在决策日截断，包含至少两年 Daily 背景、OHLC、EMA20/50/200 和原始成交量，不显示事后标签或结果。
- 数据：公开 Yahoo Chart API 历史 Daily OHLCV，经 agent-reach 的 Jina 公开路由读取；源时区 `America/New_York`，复核时间 `2026-08-27 Asia/Shanghai`，最新完整 RTH 日线为 `2026-08-26`。本 session 未成功调用 Futu MCP，因此不是实时或 Futu 数据。
- 成本：commission `0`、spread `0`；结果是研究回放，不是净执行估计。
- 订单分支：全部为 `stop_confirmation`，`max_hold_bars=10`，`gap_policy=skip`。

## 合同和结果

| 合同 | 方向 / 标签 | 分组 | 结果 | 实现 R |
| --- | --- | --- | --- | ---: |
| ZS 2021-07-19 | long / H1 | `ordinary_non_event` | opening-skip | — |
| DDOG 2021-07-19 | long / H1 | `ordinary_non_event` | opening-skip | — |
| DDOG 2023-07-24 | long / H1 | `ordinary_non_event` | opening-skip | — |
| ZS 2023-09-19 | long / H1 | `event_driven` | 2023-09-20 成交，2023-09-21 止损 | `-1.2169R` |
| DDOG 2023-03-07 | short / L1 | `event_driven`（raw aftershock） | 2023-03-08 成交，2023-03-13 到达目标 | `+2.6232R` |

`opening-skip` 是冻结的跳空处理路径，不追价补成交；它既不是胜利，也不是已成交亏损，不进入已完成交易的胜率分母，但必须作为失败/不可成交路径保留。没有 ambiguous intrabar 结果。

## 分层统计

| 分层 | 合同 | 成交 | 完成 | 胜 / 负 | 描述性胜率 | 总实现 R | 统计状态 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 全部 | 5 | 2 | 2 | 1 / 1 | 50.00% | `+1.4063R` | not-validated |
| `ordinary_non_event` | 3 | 0 | 0 | 0 / 0 | 不可计算 | — | 无成交分母 |
| `event_driven`（含 aftershock） | 2 | 2 | 2 | 1 / 1 | 50.00% | `+1.4063R` | not-validated |
| H1 | 4 | 1 | 1 | 0 / 1 | 0.00% | `-1.2169R` | 样本不足 |
| L1 | 1 | 1 | 1 | 1 / 0 | 100.00% | `+2.6232R` | 样本不足 |

完成交易的平均和中位数均为 `+0.7031R`，profit factor 约为 `2.1556`。这两个完成交易是一条事件驱动多头亏损和一条事件后冲空头盈利，不能外推为普通 H/L 胜率。H2/L2 本批没有合格冻结合同，不能用空缺冒充零胜率。

## 闸门检查

- 冻结时历史几何空间审计（非当前显式 strict-space）：`5/5` 条合同的 `space_R >= 1.00`；旧 CSV 缺少 `pre_entry_space_R/space_status`，因此当前 `contract_space_bucket` 仍是 `unknown_contract_space`。历史几何为正不等于会成交，也不等于已验证有利可交易性。
- EMA 方向：4 条多头 H1 均为 Daily EMA20/EMA50 `up/up`、`long_pass`；1 条空头 L1 为 `down/down`、`short_pass`。
- 两年背景、重要高低点、EMA20/50/200 和支撑阻力审查：5/5 完整记录。
- 事件隔离：普通组 3 条、事件组 2 条；事件组没有混入普通非事件统计。
- 依赖记录：5 条各有不同的 `lineage_id`，本批没有用同一已登记行情段重复制造 H1/H2 或 L1/L2 样本；但 5 条均没有 `market_context_id`，不同 lineage 不能证明市场状态或结果 artifact 独立，数量也远不足以验证。

## 对 60% 目标的判断

本批完成成交的点估计为 `50%`，低于用户设定的 `60%` 待检验目标；其 Wilson 区间极宽，且普通组没有成交分母。因此不能作出“规则达到或未达到长期 60%”的结论，只能记录为：当前批次未提供支持 60% 的验证证据，继续保持 `no-new-positive`。后续必须继续增加人工冻结、事件分层、失败路径和独立 lineage 样本，并在同一合同口径下回放。

```text
validated win-rate: not-computable
```

## 复核限制

1. 标签来自人工图表识别，Matplotlib 只渲染证据图，不承担 pattern recognition。
2. 结果只对应本批冻结的触发、结构止损、第一障碍、最大持有期和跳空政策；改变任一合同字段都应视为新的研究批次。
3. 3 条 opening-skip 说明 stop-confirmation 合同对历史跳空敏感；不能把未成交样本强行当作止损或盈利。
4. 事件组的 2 条完成交易不能与普通组混算，也不能支持 H1/L1 的普遍胜率。
5. 交易成本为零，未包含实际滑点、税费或点差影响；价格数据也没有被宣称为实时数据。

机器可读的原始回放输出保存在本批外部审计目录；仓库内保留输入快照、图像资产和本报告，确保研究结果可复核且不把运行缓存或外部临时输出提交为代码。

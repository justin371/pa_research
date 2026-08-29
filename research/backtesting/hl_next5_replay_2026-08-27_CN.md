# H/L 下一批（五）分层回放审计（2026-08-27）

状态：`research_only / descriptive_only / not-validated / no-new-positive`

本报告保留当时历史回放的运行口径；其中的旧 engine 版本不是当前维护版本。当前 PA Research engine 为 `0.3.9`，历史数字不会因版本升级自动变成当前验证结果。

## 结论

本批回放 6 条人工冻结合同，全部是**空头 L1**；其中 5 条成交并完成，1 条因开盘跳过旧触发位而未成交。完成交易为 **3 胜 2 负，描述性胜率 `60.00%`，总实现 `+3.4812R`，平均 `+0.6962R`，Profit Factor `3.1762`**。这个 60% 只是在极小样本上的合并描述值，不能把 `ordinary_non_event`、`earnings_adjacent` 和 `event_driven` 样本混成一个胜率；本批仍是 `no-new-positive`，没有验证 H1/H2/L1/L2 的长期胜率。

按 canonical `event_bucket` 分层后：`ordinary_non_event` 完成交易为 2 胜 1 负（`66.67%`，`n=3`）；`earnings_adjacent` 为 0 胜 1 负；`event_driven` 为 1 胜 0 负（raw `event_context=earnings-driven`）。报告正文中的 `earnings-adjacent` 只可作为 `earnings_adjacent` 的可读别名。每个 lineage 只有一个样本，且没有多头 H2、空头 L2 或多标的同质重复样本。95% Wilson 区间很宽，目标 `60%` 仍只能作为下一批待检验目标。

## 回放配置与证据边界

- 引擎：PA Research backtesting engine `0.3.1`；依赖 `backtesting.py 0.6.6`。
- 冻结合同：[`hl_next5_contracts_2026-08-27.csv`](hl_next5_contracts_2026-08-27.csv)。
- 历史价格：[`hl_next5_prices_2026-08-27.csv`](hl_next5_prices_2026-08-27.csv)。
- 冻结前审查：[`hl_next5_selection_2026-08-27_CN.md`](hl_next5_selection_2026-08-27_CN.md)。
- 数据：公开 Yahoo Chart API 历史 Daily OHLCV，经 agent-reach 的 Jina 公共路由读取；源时区 `America/New_York`，数据截止 `2026-08-26`，复核时间 `2026-08-27 Asia/Shanghai`。本 session 未成功调用 Futu MCP，因此不是实时或 Futu 回放。
- 合同：全部 `stop_confirmation`、`max_hold_bars=10`、`gap_policy=skip`；无手续费、无 spread；开盘跳过旧触发位不追价。
- 结果：没有 `ambiguous_intrabar`；止损和目标在入场 K 线完成后才挂入。第一障碍空间是事前几何字段，不等于已经实现的收益。
- 图像：Matplotlib `3.10.9` 只用于两年 Daily 背景和局部 OHLC/EMA20/50/200/成交量人工审阅；没有自动识别 pattern 或股票扫描。

回放输出 `results.csv`、`summary.json` 和 `run_metadata.json` 保留在本机外部审计目录：

`C:\Users\lwang\.codex\artifacts\pa-research-hl-next5-20260827\replay\results_final`

该目录是本报告的正式 artifact。`results_clean` 只差 NDAQ `2022-05-10` 的事件分类（`earnings_adjacent` 修正前为 `ordinary_non_event`），`results_repo_inputs` 与正式结果字节相同但价格文件封装不同，均不与本报告合并为新增样本；详细输入/结果指纹见[`回放 provenance 与再现性审计`](replay_provenance_reproducibility_audit_2026-08-29_CN.md)。

## 成交和结果

| 合同 | 方向 / 标签 | 事件分组 | 入场 | 出场 | 结果 | 实现 R | 首障碍 |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| MCHP 2022-06-14 | `short / L1` | `ordinary_non_event` | 未成交 | — | `opening-skip` | — | 6/16 开盘 `59.84` 低于旧触发 `59.99`，按规则跳过 |
| NDAQ 2022-01-06 | `short / L1` | `ordinary_non_event` | 1/7 @ `63.73` | 1/14 @ `61.50` | `win / target` | `+1.1925R` | 已触及 `61.50` |
| NDAQ 2022-04-25 | `short / L1` | `event_driven`（raw `earnings-driven`） | 4/26 @ `54.89` | 5/2 @ `52.00` | `win / target` | `+2.3884R` | 已触及 `52.00` |
| NDAQ 2022-05-10 | `short / L1` | `earnings_adjacent`（raw `earnings_adjacent`；正文别名 `earnings-adjacent`） | 5/11 @ `48.06` | 5/26 @ `49.4033` | `loss / time_exit` | `-0.5997R` | 未触及 `45.00` |
| NDAQ 2022-12-19 | `short / L1` | `ordinary_non_event` | 12/20 @ `60.08` | 12/21 @ `61.20` | `loss / stop` | `-1.0000R` | 未触及 `57.50` |
| NDAQ 2026-06-22 | `short / L1` | `ordinary_non_event` | 6/24 @ `81.48` | 6/25 @ `78.00` | `win / target` | `+1.5000R` | 已触及 `78.00` |

`time_exit` 的 `-0.5997R` 是观察十根完整 post-entry K 线后、在下一根开盘按市场价退出的实际路径，不改写成止损或 scratch；因此该旧产物的 `bars_held=11` 是执行索引距离，不是额外自由持仓。`opening-skip` 不进入胜负分母，也不把跳空后的价格事后填回旧合同。当前 engine 还会把数据末尾无法执行的时间退出保留为 `incomplete-horizon`。

## 分层统计

胜率定义为：

`wins / (wins + losses + scratches)`

`opening-skip`、未成交、`observation_only`、pending 和无法确定的同 K 线冲突不进入胜负分母。

| 分层 | 合同 | 完成交易 | 胜 / 负 | 描述性胜率 | 总实现 R | 95% Wilson 区间 | 状态 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 全部合同 | 6 | 5 | 3 / 2 | `60.00%` | `+3.4812R` | `23.07%–88.24%` | not-validated |
| ordinary_non_event | 4 | 3 | 2 / 1 | `66.67%` | `+1.6925R` | `20.77%–93.85%` | descriptive_only |
| earnings_adjacent | 1 | 1 | 0 / 1 | `0.00%` | `-0.5997R` | `0.00%–79.35%` | descriptive_only |
| event_driven（raw `earnings-driven`） | 1 | 1 | 1 / 0 | `100.00%` | `+2.3884R` | `20.65%–100.00%` | descriptive_only |
| 事前空间 `>=1.50R` 敏感性子集 | 4 | 3 | 2 / 1 | `66.67%` | `+2.8884R` | `20.77%–93.85%` | 附加敏感性分层；not-validated |
| short | 6 | 5 | 3 / 2 | `60.00%` | `+3.4812R` | `23.07%–88.24%` | not-validated |
| L1 | 6 | 5 | 3 / 2 | `60.00%` | `+3.4812R` | `23.07%–88.24%` | not-validated |
| H2 / L2 / long | 0 | 0 | — | 不可计算 | — | — | 未形成样本 |

表中的 `>=1.50R` 只是本批对事前数值空间做的附加敏感性切片，不是当前 canonical `strict_ge_1R` 的替代阈值或新的 `space_status` 枚举；6 条合同的 CSV `space_status` 均为 `strict_ge_1R`。

本批 6 个 `lineage_id` 在本批内均唯一；这只说明没有登记为同一局部结构，不能证明市场状态或结果 artifact 独立，因为 6 条均没有 `market_context_id`。META 只有 NDAQ 2022-12-19 一条，且该条止损。不能据此宣称 META 提高胜率，也不能把 `60%` 作为规则参数写回生产合同。

## 对 60% 目标的判断

合并后的 3/5 恰好等于用户修正后的 `60%`，但合并不满足可比性：

- 普通组只有 3 条完成交易；
- `earnings_adjacent` 和 `event_driven` 各只有 1 条，且结果相反；前者正文有时写作 `earnings-adjacent`，后者 raw `event_context` 为 `earnings-driven`；
- 5 条完成交易中有 4 条来自 NDAQ；
- 全部标签都是 L1，没有 H2、L2 或多头对照；
- 每个 lineage 只有一次触发，不能检验重复尝试是否真正独立；
- 事件状态、B 质量和父级背景仍存在敏感性差异。

因此本批的正确结论是：**观察到的合并描述胜率为 60%，但目标没有被验证，研究状态保持 `no-new-positive`。** 这批数据不足以放宽强 A、controlled-B、EMA20/50 同向、事件隔离、lineage 或首障碍空间条件，也不足以证明 L1 优于 L2。

## 失败路径与下一步

- MCHP 的普通 L1 结构满足事前空间，但旧触发被开盘缺口跳过；不能用更低的开盘价补出一个漂亮结果。
- NDAQ 2022-05-10 的近期财报邻近窗口最终时间退出为负，说明“距离财报超过三个 session”不等于事件影响已经可忽略；继续保留 `earnings_adjacent` 分层。
- NDAQ 2022-12-19 虽有支撑与 EMA200 的 META，仍在下一交易日触及结构止损；META 不是方向授权。
- 需要下一批继续增加未使用标的、同质 ordinary lineage 和真正的 H2/L2；不得把事件样本、宽 B 或转换段为凑数量混入普通统计。

本文件只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

```text
validated win-rate: not-computable
```

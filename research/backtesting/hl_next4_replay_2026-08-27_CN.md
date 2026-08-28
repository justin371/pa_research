# H/L 下一批（四）分层回放审计（2026-08-27）

状态：`research_only / descriptive_only / not-validated / no-new-positive`

本报告保留当时历史回放的运行口径；其中的旧 engine 版本不是当前维护版本。当前 PA Research engine 为 `0.3.9`，历史数字不会因版本升级自动变成当前验证结果。

## 结论

本批只有 2 条人工冻结合同，均为普通非事件口径下的 `long / H1`，均满足事前第一障碍空间 `>=1R`。两条都成交，但都没有到达第一障碍：CBOE 触发后止损，ROST 在十根 K 线合同结束时退出。描述性结果为 **0 胜 2 负、胜率 `0.00%`、总实现 `-1.5090R`、平均 `-0.7545R`**。

这不是在证明 H1 长期胜率为 0%，而是本批两个冻结样本的历史结果。95% Wilson 区间约为 `0.00%–65.76%`；样本只有两个不同 lineage，不能验证用户修正后的 `60%` 目标。结论保持 `no-new-positive`，不据此修改生产规则或放宽筛选条件。

若采用更保守的事件口径，把所有 post-earnings lineage 都从 ordinary 组剔除，则本批 ordinary 分母为 `0`，胜率不可计算；不能把它伪装成更好的结果或把事件边界混入普通组。

## 回放配置与证据边界

- 引擎：PA Research backtesting engine `0.3.1`；依赖 `backtesting.py 0.6.6`。
- 输入合同：[`hl_next4_contracts_2026-08-27.csv`](hl_next4_contracts_2026-08-27.csv)。
- 输入价格：[`hl_next4_prices_2026-08-27.csv`](hl_next4_prices_2026-08-27.csv)。
- 冻结前人工审查：[`hl_next4_selection_2026-08-27_CN.md`](hl_next4_selection_2026-08-27_CN.md)。
- 回放输出：`C:\Users\lwang\.codex\artifacts\pa-research-hl-next4-20260827\replay2`，包含 `results.csv`、`summary.json` 和 `run_metadata.json`。
- 同一 artifact 根目录下另有旧 `replay` 输出；它使用相同输入文件但记录为两条 `unproven`，与本报告不一致。当前报告只认上述明确指定的 `replay2`，两个旧结果不合并；版本/指纹冲突见[`回放 provenance 与再现性审计`](replay_provenance_reproducibility_audit_2026-08-29_CN.md)。
- 数据：公开 Yahoo Chart API 历史 Daily OHLCV，经 agent-reach 的 Jina 公共路由读取；源时区 `America/New_York`，复核时间 `2026-08-27 Asia/Shanghai`，最新完整 RTH 日线为 `2026-08-26`。本 session 未成功调用 Futu MCP，因此不是实时或 Futu 回放。
- 成本：commission `0`、spread `0`；结果是研究路径结果，不是净执行收益估计。
- 合同：全部 `stop_confirmation`、`max_hold_bars=10`、`gap_policy=skip`。开盘越过触发位则跳过，不追价。
- 图像：使用 Matplotlib `3.10.9` 生成至少两年 Daily 背景、局部 OHLC、EMA20/50/200 和原始成交量图；图上没有事后标签、入场、止损、目标或结果。Matplotlib 只渲染，不识别 pattern、不扫描股票。

## 成交和结果

| 合同 | 方向 / 标签 | 入场 | 出场 | 结果 | 实现 R | 首障碍 |
| --- | --- | --- | --- | --- | ---: | --- |
| CBOE 2025-05-22 | `long / H1` | 2025-05-23 @ 229.24 | 2025-05-28 @ 225.50 | `loss / stop` | `-1.0000R` | 236.00，未触及 |
| ROST 2026-01-07 | `long / H1` | 2026-01-08 @ 189.59 | 2026-01-26 @ 187.61 | `loss / time_exit` | `-0.5090R` | 200.00，未触及 |

CBOE 的 5/23 开盘价 `226.58` 低于触发位，盘中上破 `229.24` 后成交；5/28 触发结构止损。ROST 的 1/8 开盘价 `186.99` 低于触发位，盘中上破后成交；观察十根完整的 post-entry 日线后，下一根 K 线开盘按时间规则退出。回放器结果中 ROST 的 `bars_held=11` 是 `backtesting.py` 的 entry/exit bar 索引距离：十根完整观察 K 线之后还要等下一根开盘执行，并不表示合同获得了额外的自由持仓。2026-08-29 的结果分母审计已把这一口径写入当前 engine 文档，并增加了数据末尾无法执行时间退出时标为 `incomplete-horizon` 的保护。

## 胜率定义和分层统计

描述性胜率只以完成成交且结果为 `win`、`loss` 或 `scratch` 的合同作为分母：

`win rate = wins / (wins + losses + scratches)`

opening-skip、未成交、`observation_only`、pending 和 ambiguous intrabar 不进入胜负分母。本批没有 opening-skip、未成交或 ambiguous intrabar。

| 分层 | 合同 | 成交 | 完成 | 胜 / 负 | 描述性胜率 | 总实现 R | 状态 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 全部 | 2 | 2 | 2 | 0 / 2 | 0.00% | -1.5090R | not-validated |
| ordinary non-event（按当前隔离口径） | 2 | 2 | 2 | 0 / 2 | 0.00% | -1.5090R | descriptive_only |
| event-driven | 0 | 0 | 0 | 0 / 0 | 不可计算 | — | 未形成分母 |
| long | 2 | 2 | 2 | 0 / 2 | 0.00% | -1.5090R | not-validated |
| short | 0 | 0 | 0 | 0 / 0 | 不可计算 | — | 未形成样本 |
| H1 | 2 | 2 | 2 | 0 / 2 | 0.00% | -1.5090R | not-validated |
| H2 | 0 | 0 | 0 | 0 / 0 | 不可计算 | 未形成样本 |
| L1 | 0 | 0 | 0 | 0 / 0 | 不可计算 | 未形成样本 |
| L2 | 0 | 0 | 0 | 0 / 0 | 不可计算 | 未形成样本 |
| `space_R >= 1.00` | 2 | 2 | 2 | 0 / 2 | 0.00% | -1.5090R | not-validated |
| strict `space_R >= 1.50` | 2 | 2 | 2 | 0 / 2 | 0.00% | -1.5090R | not-validated |
| META present | 2 | 2 | 2 | 0 / 2 | 0.00% | -1.5090R | not-validated |
| META absent | 0 | 0 | 0 | 0 / 0 | 不可计算 | 未形成样本 |

按 lineage 分层：`CBOE-2025-05-reset-h1` 为 1 负、`ROST-2026-01-post-earnings-reset-h1` 为 1 负。每个 lineage 只有一个样本，不能据此区分标的效应、市场状态或独立性。

## 对 60% 目标的判断

本批完成交易胜率低于 `60%` 目标，但 `n=2` 且只有多头 H1，不能把它当作规则的长期估计。更有用的结论是：即使同时满足强 A 偏好、受控小 B、EMA20/50 向上、META 记录和 `>=1R` 首障碍，单靠这些条件仍不能保证触发后的跟随。

- CBOE 在真实突破触发后快速失守，提示“盘中上破”与“收盘/跟随确认”可能需要在新独立批次中分支比较；本批不凭一个失败样本改规则。
- ROST 没有止损但也没有在约定窗口内到达整数位障碍，说明时间退出与目标定义应继续单独记录；不能把未达目标的时间退出改写成 scratch 或 win。
- 两条合同均来自事件后的隔离窗口；若事件隔离标准继续收紧，本批将没有 ordinary 分母，而不是得到更高胜率。

既有批次不在这里合并：不同标的、事件状态、标签、空间质量和 lineage 的合同混合后会掩盖失败路径，不能制造更大的有效样本。

## 失败路径是否保留

- **CBOE**：合同冻结时已经写明 `225.50` 下方接受或不能站上 `229.24` 为失效，`236.00` 为最近独立障碍；回放按止损结束，没有事后把 5/7 的高点移走。
- **ROST**：合同冻结时已经写明 `185.70` 下方接受或不能站上 `189.59` 为失效，`200.00` 为保守整数位障碍；回放按持有期结束，没有用后续高点替换事前目标。

## 研究边界与下一步

本批只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。下一步应继续增加新的、相互独立的普通股和 lineage，并优先寻找空头 L1/L2 和 H2/L2，而不是为了提高样本量放宽 strong-A、controlled-B、EMA 方向、事件隔离或首障碍空间。只有在合同质量和样本量足够后，才有资格重新检验 `60%`。

```text
validated win-rate: not-computable
```

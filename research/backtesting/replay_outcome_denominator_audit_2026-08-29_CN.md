# 回放结果分母与 horizon 审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 回放 engine、现有单元测试、仓库内冻结合同、已有 `results.csv/summary.json` 和人工回放报告<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计边界

本次只检查已有回放结果的语义和分母，不抓取新行情、不新增股票、不新增冻结合同，也不重算新的市场样本。为确认 horizon 边界，使用仓库中已有的历史价格快照在内存中复核；没有覆盖或改写外部 artifact。PA Research 规则、ABC/BOP/H/L/H3/L3 的分层和 lineage 约束保持不变。

本审计不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

## 二、统一结果口径

| 字段/状态 | 当前含义 | 是否进入胜率分母 |
| --- | --- | --- |
| `win_rate_eligible=yes` | 结果行声明具备可比资格的旗标 | 不是单独分母，仍需通过全部硬条件 |
| `trade_result=win/loss/scratch` | 已完成成交的结果标签 | 只有与资格、成交和证据状态同时成立才进入 |
| `opening-skip` / `no-fill` | 冻结订单没有形成可比成交 | 否 |
| `ambiguous_intrabar` | 同一根后续 K 线同时触及止损和目标，先后不可判定 | 否；若首障碍只在该歧义路径上出现，`first_obstacle_hit=unknown` |
| `incomplete-horizon` | 数据结束或时间退出没有在预期市场时间执行 | 否，`trade_result=pending` |
| `first_obstacle_hit` | 路径过程字段，不是胜负标签 | 不决定分母，也不自动等于 `win` |
| `realized_R` | 净 PnL 除以实际结构风险 | 必须为有限数值，并与完整可比结果同时存在 |

当前 `summary` 的 `completed_trade_count` 只统计同时满足以下条件的行：

```text
win_rate_eligible=yes
trade_result in {win, loss, scratch}
evidence_status=comparable
fill_status=filled
ambiguous_intrabar != yes
path_result not in {ambiguous, incomplete-horizon}
realized_R is finite
```

`win_rate_eligible_count` 只报告旗标数量；若旗标和结果标签不一致，摘要另外报告 `win_rate_eligibility_mismatch_count`。旗标虽为 `yes`、但被成交/证据/horizon/歧义/R 值硬闸门挡住的行计入 `win_rate_guard_exclusion_count`。`outcome_bucket_counts` 为互斥的结果/排除状态，防止把未成交或未完成路径从分母悄悄丢掉。

当前 engine `0.3.9` 还把事前证据与结果派生字段分开：`event_bucket` 和 `contract_space_bucket` 从原始 `event_context`、`space_status`、`pre_entry_space_R` 重算，结果行中已有的同名字段只做 mismatch 诊断；若结果行带 H/L EMA gate，`contract_eligibility` 也从该 gate 重算，失败或 pending gate 不能靠结果行旗标进入完成交易分母。缺少合同、事件、非收盘入场触发价或 H/L gate 必需字段的行标记为 `pre_entry_provenance_status=incomplete`，不能进入完成分母。对应的 `contract_eligibility_mismatch_count`、`event_bucket_mismatch_count` 和 `contract_space_bucket_mismatch_count` 必须保留。

## 三、发现与修复

### 1. summary 的分母防护不足

此前摘要主要用 `trade_result in {win, loss, scratch}` 形成 `completed`，对手工或旧产物中可能出现的资格旗标、证据状态、成交状态不一致没有显式防护。在本审计对应的历史中间版本 engine `0.3.3` 中已统一准备结果字段，并以严格交集计算顶层和每个分组的完成交易；当前 engine `0.3.9` 延续并保留这套防护，同时保留资格旗标、mismatch、guard exclusion 和互斥 outcome bucket。

这不会把旧的 `opening-skip`、`observation_only`、`pending` 或 `incomplete-horizon` 变成负数，也不会把首障碍到达改写为胜利。

### 2. time-exit 的 bar 计数需要区分“观察窗口”和“执行索引”

现有 13 份历史 `results.csv` 中，有 6 份产物重复记录了 3 个唯一合同的 `bars_held=11`、`max_hold_bars=10`。逐条核对 `backtesting.py` 的订单时序后，结论不是把 H/L 的历史结果提前一根 bar：

- `max_hold_bars=10` 表示 entry 之后观察十根完整 K 线；
- 非 `market_close` 的 `Trade.close()` 是下一根 K 线开盘成交，所以 `ExitBar - EntryBar` 这个技术索引距离可以是 11；
- 这不表示合同多获得一根自由持仓，报告必须把两种计数分开说明；
- `market_close` 现在以 `backtesting.py` 的实际 `trade.entry_bar` 计时，不再把“策略第一次看到持仓的 bar”误当作入场 bar；
- 如果时间退出请求发生在数据末尾、没有预期的市场执行 bar，则保留为 `incomplete-horizon`，不因 `finalize_trades=True` 的合成收尾而制造完成交易。

因此历史中间版本 engine `0.3.3` 保留既有 H/L 合同的“观察十根完整 K 线后下一根开盘退出”语义，并修复实际 entry-bar 和数据末尾边界；当前 engine `0.3.9` 延续该语义。相关回归测试已覆盖普通订单、`market_close`、末尾不完整 horizon 以及时间退出后 bar 不应制造首障碍/歧义的情况。

### 3. 首障碍、歧义和 realized_R 的隔离

同 K 线止损/目标冲突仍是 `pending`、`excluded_ambiguous`，不会进入胜率分母。若该歧义 bar 同时触及首障碍，结果字段不再无条件写成 `yes`，而是写 `unknown`；首障碍字段仍只用于路径审计。

对于完整成交，`realized_R` 继续使用实际成交价、实际结构风险和回放成本后的净 PnL。时间退出的负值仍是时间退出，不改写成止损；`opening-skip` 不补成交、不产生 `realized_R`。

## 四、已有仓库价格快照的复核

以下只使用已有仓库合同和历史价格文件，通过当时的历史中间版本 engine `0.3.3` 做语义复核；当前维护版本为 engine `0.3.9`。不新增行情样本，也不把复核结果写成新的验证批次：

| 批次 | 合同 | 完成交易 | 胜 / 负 | 时间退出核对 |
| --- | ---: | ---: | ---: | --- |
| H/L 大样本 | 37 | 17 | 13 / 4 | RBLX 记录为十根完整观察 K 线后下一根开盘；`bars_held=11` 是执行索引距离 |
| H/L 下一批（四） | 2 | 2 | 0 / 2 | ROST 同一口径；时间退出不改写为 scratch 或 win |
| H/L 下一批（五） | 6 | 5 | 3 / 2 | NDAQ 同一口径；`opening-skip` 仍不进分母 |

三批复核没有新增合同、没有扩大胜率分母，原报告的 descriptive 数值仍只代表各自历史合同口径，不能升级为长期验证。旧 `summary.json` 是历史引擎产物；需要机器读取新增字段时，应在同一冻结输入上重新生成，不得把旧 JSON 与新字段拼接成一份“验证结果”。

## 五、结论

本次修复了结果摘要的严格分母防护、`market_close` 的实际 entry-bar 计时、数据末尾时间退出的 incomplete 边界，以及歧义路径上的首障碍不确定性。现有 H/L 结果没有因此增加样本；ABC、BOP、H3、L3 仍没有新的冻结回放合同。

`no-new-positive` 与 `validated win-rate: not-computable` 保持不变。任何 60% 胜率或盈亏优势的判断，仍必须在事件已核实、空间字段事前冻结、失败路径完整、lineage 独立且使用同一合同口径的更大样本上重新验证。

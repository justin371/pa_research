# H/L EMA 闸门、回调位置与报告分母一致性审计（2026-08-29）

## 审计范围

本次只审计 PA Research 已冻结的 7 份 H/L 合同 CSV、对应 selection/replay 报告、当前 `backtesting.py` engine 的 EMA 闸门边界和文档 validator。没有下载行情、没有看新图、没有运行回放、没有增加样本，也没有修改 Codex Trading。

审计字段为：

- `daily_ema20_slope`
- `daily_ema50_slope`
- `h_l_ema_slope_gate`
- `h_l_pullback_location`
- 报告中的 `eligible`、`observation_only`、`pending` 与胜率分母

## 冻结合同的机器事实

7 份 CSV 共 60 行，当前 gate 计数为：

| 合同文件 | `long_pass` | `short_pass` | `fail_flat_or_opposite` | 行数 |
| --- | ---: | ---: | ---: | ---: |
| `hl_contracts_2026-08-26.csv` | 2 | 2 | 1 | 5 |
| `hl_contracts_batch2_2026-08-26.csv` | 1 | 2 | 0 | 3 |
| `hl_large_contracts_2026-08-27.csv` | 16 | 17 | 4 | 37 |
| `hl_next_contracts_2026-08-27.csv` | 4 | 1 | 0 | 5 |
| `hl_next2_contracts_2026-08-27.csv` | 2 | 0 | 0 | 2 |
| `hl_next4_contracts_2026-08-27.csv` | 2 | 0 | 0 | 2 |
| `hl_next5_contracts_2026-08-27.csv` | 0 | 6 | 0 | 6 |
| **合计** | **27** | **28** | **5** | **60** |

逐行方向核对结果：

- H1/H2 共 32 行，方向均为 `long`；其中 27 行为 `up/up + long_pass`，5 行为已知不满足多头均线条件的 `fail_flat_or_opposite`。
- L1/L2 共 28 行，方向均为 `short`；28 行均为 `down/down + short_pass`。
- `h_l_pullback_location` 在 60/60 行非空；它是人工位置说明，不被当作 EMA 闸门或独立 B 位置字段。
- 当前冻结合同没有 `pending` 或未知 EMA 斜率行；缺失证据的允许状态仍必须使用 `unknown`/`pending`，不能默认为 pass。

对应报告的摘要计数与合同事实一致：首批为 `contract_count=5 / eligible_contract_count=4 / observation_only_count=1`；第二批为 3/3；large 批为 16/17/4 的 `long_pass/short_pass/observation`；next 批为 4/1；next2 为 2 条多头通过；next4 为 2 条多头通过；next5 为 6 条空头通过。next3 没有冻结合同，保持 no denominator。报告没有把 `observation_only`、`pending`、opening-skip 或未完成路径写入胜率分母。

## 发现的 validator 漏洞与修复

engine 原本已经要求：

- H1/H2 只能使用 `long_pass`，L1/L2 只能使用 `short_pass`；
- `long_pass`/`short_pass` 必须与对应的 EMA20/EMA50 方向一致；
- 有未知 EMA 斜率时应使用 `pending`，不能写成 `fail_flat_or_opposite`。

文档 validator 之前只在 gate 等于“本方向 expected gate”时检查斜率，因而可能放过 `H1/H2 + short_pass` 或 `L1/L2 + long_pass`。它也没有完全复制 engine 对“未知斜率 + `fail_flat_or_opposite`”的保护。当前真实 60 行没有触发这两个漏洞，但这会让未来错误合同绕过文档层检查。

本次修复：

1. validator 现在拒绝与 H/L 内部标签方向相反的 pass gate；
2. validator 现在拒绝带未知 EMA 斜率的 `fail_flat_or_opposite`，并要求改为 `pending`；
3. 回归测试在隔离副本中同时覆盖 H1 反向 pass、L1 反向 pass 和未知斜率 fail 三类边界。

## 统计与结论边界

本次没有改 CSV、engine 有效语义、历史成交结果、报告数字或胜率分母；没有新增样本，也没有新正向证据。`fail_flat_or_opposite` 仍是 observation-only，不进入胜率分母；`pending` 仍不是可交易合同。当前审计结论继续为 `no-new-positive`，`validated win-rate: not-computable`。

这是 PA Research only；不修改 Codex Trading，不创建 quantitative scanner，不连接 Execution Agent，也不连接 Futu/OpenD。

Scope boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent; no Futu/OpenD.

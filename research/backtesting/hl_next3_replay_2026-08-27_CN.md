# H/L 下一批（三）回放状态审计（2026-08-27）

状态：`research_only / no-eligible-contracts / no-new-positive`

本报告保留当时历史回放的运行口径；其中的旧 engine 版本不是当前维护版本。当前 PA Research engine 为 `0.3.9`，历史数字不会因版本升级自动变成当前验证结果。

## 结果

本批人工审阅 18 个候选，但没有任何一条同时通过 ordinary non-event、清晰 H1/H2/L1/L2 lineage、匹配的 EMA20/50 方向闸门和首障碍 `>=1R` 空间。因此没有冻结交易合同，也没有可以合法交给 `backtesting.py` 的交易样本。

| 项目 | 数值 / 状态 |
| --- | --- |
| 新候选图表 | 18 个决策日 |
| 新 ordinary H1/H2/L1/L2 合同 | 0 |
| 事件/边界合同 | 0 |
| 回放成交分母 | 0 |
| 描述性胜率 | 不可计算 |
| 实现 R | 不适用 |
| 60% 目标 | 继续待检验 |
| 当前结论 | `no-new-positive` |

## 为什么没有强行运行交易回放

PA Research 的回放器只接受人工冻结合同；它不是图表识别器，也不负责把 rejected candidate 转换成交易。当前引擎对空合同 CSV 会主动报错 `contract CSV contains no rows`，避免把无样本误报为 `0%`、`100%` 或“已经验证”。因此本批没有生成占位合同、伪造 entry/stop/target，也没有把事件边界混入普通统计。

已完成的历史回放仍保留在独立批次中：

- [`hl_next_replay_2026-08-27_CN.md`](hl_next_replay_2026-08-27_CN.md)；
- [`hl_next2_replay_2026-08-27_CN.md`](hl_next2_replay_2026-08-27_CN.md)；
- [`hl_large_replay_2026-08-27_CN.md`](hl_large_replay_2026-08-27_CN.md)。

这些批次不与本批合并，因为合同质量、事件状态、标签、空间和 lineage 不同；跨批合并不能制造独立样本，也不能证明 `60%`。

## 复核证据

人工选择与拒绝理由见 [`hl_next3_selection_2026-08-27_CN.md`](hl_next3_selection_2026-08-27_CN.md)。使用的无标签两年 Daily 图表位于本机外部审计资产：

`C:\Users\lwang\.codex\artifacts\pa-research-hl-next2-20260827`

图表由 Matplotlib `3.10.9` 渲染，包含 EMA20/50/200 和原始成交量，但不含事后标签或结果。回放引擎版本为 `0.3.1`，依赖 `backtesting.py 0.6.6`；本批没有 Futu 实时证据。

本报告只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

```text
validated win-rate: not-computable
```

# H/L 视觉前置证据与冻结资格审计（2026-08-29）

## 审计范围

本次只检查 PA Research 已冻结的 7 份 H/L 合同、仓库内视觉资产 README、已记录的外部 artifact provenance，以及对应 selection/replay 报告。没有下载行情、没有看新图、没有运行回放、没有增加样本或结果，也没有修改 Codex Trading。

审计区分两个边界：一是 CSV 中两年背景、重要高低点和 EMA20/50/200 的字段是否完整；二是决策日无标签图是否仍可由 checkout 或已登记 artifact 独立复核。`contract_frozen=yes` 只表示前者的合同字段和订单几何已经冻结，不自动证明后者，也不等于交易授权或验证通过。

## 7 份冻结合同的机器核对

7 份 CSV 共 60 行，以下五个前置字段均为完整值：

| 文件 | 行数 | `label_source` | `daily_context_window` | `major_high_low_review` | `ema20_50_200_review` | `contract_frozen` |
| --- | ---: | --- | --- | --- | --- | --- |
| `hl_contracts_2026-08-26.csv` | 5 | 5/5 `human_chart_review` | 5/5 `>=2y` | 5/5 `complete` | 5/5 `complete` | 5/5 `yes` |
| `hl_contracts_batch2_2026-08-26.csv` | 3 | 3/3 `human_chart_review` | 3/3 `>=2y` | 3/3 `complete` | 3/3 `complete` | 3/3 `yes` |
| `hl_large_contracts_2026-08-27.csv` | 37 | 37/37 `human_chart_review` | 37/37 `>=2y` | 37/37 `complete` | 37/37 `complete` | 37/37 `yes` |
| `hl_next_contracts_2026-08-27.csv` | 5 | 5/5 `human_chart_review` | 5/5 `>=2y` | 5/5 `complete` | 5/5 `complete` | 5/5 `yes` |
| `hl_next2_contracts_2026-08-27.csv` | 2 | 2/2 `human_chart_review` | 2/2 `>=2y` | 2/2 `complete` | 2/2 `complete` | 2/2 `yes` |
| `hl_next4_contracts_2026-08-27.csv` | 2 | 2/2 `human_chart_review` | 2/2 `>=2y` | 2/2 `complete` | 2/2 `complete` | 2/2 `yes` |
| `hl_next5_contracts_2026-08-27.csv` | 6 | 6/6 `human_chart_review` | 6/6 `>=2y` | 6/6 `complete` | 6/6 `complete` | 6/6 `yes` |

没有发现字段层面的 `partial`、`unavailable`、`<2y`、空值或非人工来源行。当前 validator 已把这些条件作为冻结合同硬检查；若未来出现缺失，不能继续留在冻结合同中。

## 视觉资产映射与 provenance

仓库内当前有 11 个视觉资产 README、105 张 PNG，既有测试确认清单、PNG 头部/尺寸和本地链接完整。与冻结合同的映射边界为：

- 首批 5 条合同对应 5 张决策日 `Daily_2y_cutoff` 图；第二批 3 条对应 3 张；`hl_next` 5 条对应 5 张；`hl_next2` 2 条对应 2 张，另有 1 张 PHM 边界图不属于冻结合同；
- `hl_large` 有 37 条合同和 23 个局部窗口，README 明确说明不是逐合同一张图，不能把窗口数当样本数；
- `hl_next4` 和 `hl_next5` 的图像在 checkout 外部 artifact 中，分别登记 114 张和 78 张。CBOE 2025-05-22 有匹配决策日图；ROST 2026-01-07 没有匹配图，只有 1/8 和 1/13 的 post-decision 图；`hl_next5` 六条合同均有匹配决策日 candidate-review 图。

ROST 的缺口是实际 provenance gap，不是文件名小问题。后一天图不能补写成 1/7 的入场前视觉证据。ROST 的字段和历史回放数字可以原样保留为 descriptive research record，但在恢复决策日无标签图并重新核对前，不能称为完整视觉证据、新的可交易候选或已验证样本。

## selection/replay 边界

`hl_next4_selection_2026-08-27_CN.md` 已记录 ROST 缺少决策日 artifact；本次把边界进一步写清为历史回放描述保留、未来候选和验证资格暂停。`hl_next4_replay_2026-08-27_CN.md` 已记录后一天图不能替代 pre-entry visual evidence，且报告状态仍是 `research_only / not-validated / no-new-positive`。其他本地和外部资产 README/报告均把图像标为无标签、事前证据，不把 Matplotlib 当作 pattern 识别器。

因此，字段完整、合同冻结、历史回放成交和视觉 provenance 是四个不同轴：任一后续结果都不能修复缺失的左侧背景或决策日图，也不能把 `partial`/`pending` 升级为完整证据。视觉缺口不增加胜率分母，也不改变历史回放结果。

## 结论

本次没有发现 60 条 CSV 的前置字段异常；发现并固定了 ROST 外部决策日图缺失的“可复核性”边界。当前研究结论继续为 `no-new-positive`，`validated win-rate: not-computable`。后续只有恢复正确图像并完成新的事前复核，才可讨论 ROST 是否重新进入候选；本轮不重新冻结、不补图、不重跑。

Scope boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent; no Futu/OpenD.

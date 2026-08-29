# 历史回放结果、交易日志与分母 provenance 审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 当前 checkout、当前回放 engine/validator、已有历史 `results.csv`/`summary.json`/`run_metadata.json`、冻结合同及其索引<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计边界与结论

本次只读检查 PA Research 当前仓库和本机已有的历史回放 artifact，不下载行情、不重跑回放、不新增样本、不重写外部文件，也不改变 ABC、BOP、H1、H2、L1、L2、H3、L3 的识别或统计规则。检查重点是：旧 engine、外部结果、结果摘要和所谓“交易日志”是否被误写成当前验证胜率或新的独立样本。

本次不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

结论先行：

- 本机 `pa-research-*` artifact 目录中找到 13 份 `results.csv`、13 份 `summary.json` 和 13 份 `run_metadata.json`；结果共 88 行、63 个不同 `sample_id`。13 个 `sample_id` 组重复，重复组包含 38 行，额外副本为 25 行。
- 13 组结果的旧摘要都能与各自 CSV 的旧字段在行数、成交数、完成数和胜负上对齐；这只证明单个旧 artifact 内部自洽，不证明当前 schema、样本独立性或长期胜率。
- 当前 `validate_pa_research_artifact.py` 对这 13 组全部返回 `status=historical_incomplete`、退出码 `2`；没有一组是当前 `current_valid`。它们使用旧 engine `0.2.0`–`0.3.1`，缺少当前结果/metadata provenance 字段，不能与当前结果拼成一个验证分母。
- 当前 PA Research checkout 没有持久化的 `results.csv`、`summary.json`、`run_metadata.json`，也没有独立的 `journal/`、`trade_log/`、`transaction/` 或 `ledger/` 交易日志目录。回放 `results.csv` 是模拟结果记录，不是券商订单、成交、持仓或账户交易日志。
- 历史报告中保留的 `33.33%`、`50.00%`、`60.00%`、`76.47%` 等均为旧 artifact 的描述性点估计；不能被重命名为当前验证胜率，也不能把重复变体相加成新样本。

机器核对摘要：`external_results_files=13`；`external_result_rows=88`；`unique_sample_ids=63`；`duplicate_sample_id_groups=13`；`rows_in_duplicate_groups=38`；`extra_duplicate_rows=25`；`current_valid=0`；`historical_incomplete=13`；`invalid=0`；`historical_exit_code=2`。

当前 checkout 的交易日志 inventory 也做了递归核对（不把 `.git`、`.codex`、`.venv`、`node_modules` 和 `__pycache__` 等控制/环境目录当作研究记录）：

| 路径/类别 | 当前数量 | 语义 |
| --- | ---: | --- |
| `journal/` | 0 | 不存在研究日志根目录 |
| `journal/plans/` | 0 | 没有独立交易计划日志 |
| `journal/reviews/` | 0 | 没有独立交易复盘日志 |
| `trade_log/` | 0 | 没有券商/账户交易日志目录 |
| `transaction/` | 0 | 没有交易流水目录 |
| `ledger/` | 0 | 没有账户账本目录 |
| `strategy/reviews/` | 1 个研究文件 | `2026-06-25-tsla-meta-example.md` 是 observation-only 历史研究笔记，不是交易日志 |
| 持久化回放三件套 | 0 | 当前 checkout 没有 `results.csv`、`summary.json`、`run_metadata.json` |

因此，`strategy/reviews/` 的存在不改变“没有真实交易日志”的结论；目录名 `reviews` 不能把其中的研究观察笔记升级成成交、持仓或账户 P&L 记录。

因此结论继续保持：

```text
no-new-positive
validated win-rate: not-computable
```

## 二、历史 artifact 数值盘点

下表的“完成/胜负”沿用各旧 `summary.json` 的历史口径，仅用于 provenance 对账；它们没有通过当前 artifact schema 验收，不是当前胜率分母。

| 外部 artifact 逻辑组 | artifact 数 | 行数/完成 | 胜/负 | 旧摘要描述性胜率 | 当前状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| `backtest-smoke-20260826` | 1 | 1/1 | 1/0 | 100.00% | 历史不完整 |
| `hl-batch-replay-20260826` 与 `-final` | 2 | 各 5/3 | 各 1/2 | 各 33.33% | 历史不完整；结果字节相同 |
| `hl-batch2-replay-20260826` | 1 | 3/3 | 3/0 | 100.00% | 历史不完整 |
| `hl-large-replay-20260827` | 1 | 37/17 | 13/4 | 76.47% | 历史不完整 |
| `hl-next-20260827/replay` | 1 | 5/2 | 1/1 | 50.00% | 历史不完整 |
| `hl-next2-20260827/replay` | 1 | 2/2 | 2/0 | 100.00% | 历史不完整 |
| `hl-next4-20260827/replay` | 1 | 2/0 | — | 不可计算 | 历史不完整；两行未证实 |
| `hl-next4-20260827/replay2` | 1 | 2/2 | 0/2 | 0.00% | 历史不完整；报告指定变体 |
| `hl-next5-20260827/replay/results` | 1 | 8/6 | 3/3 | 50.00% | 历史不完整；隔离 |
| `hl-next5-20260827/replay/results_clean` | 1 | 6/5 | 3/2 | 60.00% | 历史不完整；隔离变体 |
| `hl-next5-20260827/replay/results_final` | 1 | 6/5 | 3/2 | 60.00% | 历史不完整；报告指定变体 |
| `hl-next5-20260827/replay/results_repo_inputs` | 1 | 6/5 | 3/2 | 60.00% | 历史不完整；输入封装变体 |

历史结果内部检查还确认：6 行出现 `bars_held=11`，涉及 3 个唯一合同，均为 `max_hold_bars=10` 的旧非 `market_close` 时间退出索引。它是“观察十根完整 K 线后下一根开盘执行”的索引差异，不是增加持仓自由度，也不是增加 3 个样本。

## 三、当前 validator 与旧 artifact 的边界

当前维护 engine 是 `0.3.9`。对上述 13 个 artifact 逐个运行只读校验器，结果为：

| 检查 | 结果 |
| --- | ---: |
| 结果三件套组数 | 13 |
| `current_valid` | 0 |
| `historical_incomplete` | 13 |
| `invalid` | 0 |
| `historical_incomplete` 退出码 | 2 |

共同历史原因包括：

- `results.csv`、`summary.json` 和 `run_metadata.json` 均早于当前 artifact schema；
- `run_metadata.json` 没有当前要求的 engine/依赖版本、源码及输入/结果指纹、`summary_provenance` 等字段，且其 `engine_version` 缺失；
- 结果行缺少当前的 `pre_entry_provenance_status`、`pre_entry_provenance_missing_fields`；
- 摘要缺少当前的结果 bucket、事前 provenance 计数、方向/事件/空间 mismatch 计数等字段。

`historical_incomplete` 表示“可保留为历史描述，但不能当作当前完整 artifact”，不是“结果为负”，也不是“结果可以择优升级”。如果以后要得到当前口径的结果，必须在同一冻结合同上使用当前 engine 和完整 provenance 重新生成；不能把旧 JSON 的胜率和新 CSV 的字段拼接。

## 四、结果分母与事前字段的逐轴隔离

当前完成交易分母必须是严格交集，而不是 `trade_result` 的行数：

```text
pre_entry_provenance_status=complete
win_rate_eligible=yes
trade_result in {win, loss, scratch}
fill_status=filled
evidence_status=comparable
path_result 非空且不属于 ambiguous/incomplete-horizon
ambiguous_intrabar != yes
realized_R 为有限数值
```

每个轴的来源和禁止反推关系如下：

| 轴 | 必须来自哪里 | 不能由什么反推 |
| --- | --- | --- |
| `direction`、`primary_pattern`、`internal_label` | 入场前人工冻结合同 | 不能由盈利方向、结果标签或后验走势改写 |
| `daily_ema20_slope`、`daily_ema50_slope`、`h_l_ema_slope_gate` | 入场前 Daily 图表审查 | 不能由回放收益或事后均线位置补齐 |
| `event_context`/`event_bucket` | 入场前事件核实及其保守派生 | 不能由是否盈利或跳空结果倒推普通非事件 |
| `pre_entry_space_R`、`space_status`/`contract_space_bucket` | 入场前首障碍几何 | 不能由 `space_to_first_obstacle_R`、`first_obstacle_hit` 或 `realized_R` 倒推严格空间 |
| `lineage_id`、`sample_id` | 冻结合同身份与依赖记录 | 不能因为日期不同或结果不同就宣称独立 |
| `fill_status`、`path_result`、`trade_result`、`realized_R` | 回放执行与结果阶段 | 不能反向修改上述事前标签或创造新合同 |

旧 artifact 虽然保留了部分方向、Pattern、EMA、事件、空间和 lineage 字段，但缺少当前完整 provenance 与重复/结果 bucket，故只能作为对应历史报告的描述性记录。特别是 `lineage_id` 不是独立性证明；同一 `sample_id` 的不同运行也不能同时进入分母。

## 五、报告指定变体与重复处理

当前报告指定的历史来源保持如下，不把隔离变体合并：

| 报告 | 指定的历史 artifact | 其他变体处理 |
| --- | --- | --- |
| 首批 H/L | `hl-batch-replay-20260826` | `-final` 与其结果字节相同，不算第二批 |
| 第二批 H/L | `hl-batch2-replay-20260826` | 无 |
| H/L 大样本 | `hl-large-replay-20260827` | 无 |
| H/L 下一批 | `hl-next-20260827/replay` | 无 |
| H/L 下一批（二） | `hl-next2-20260827/replay` | 无 |
| H/L 下一批（四） | `hl-next4-20260827/replay2` | `replay` 为同输入但未证实的旧运行，不能择优覆盖 |
| H/L 下一批（五） | `hl-next5-20260827/replay/results_final` | `results_clean`、`results_repo_inputs` 和 8 行 `results` 均隔离；事件字段或输入封装不同 |

这张表是报告 provenance 映射，不是“官方当前有效结果”清单。所有来源仍受上一节 `historical_incomplete` 状态约束。

## 六、冻结合同、回放结果和交易日志不是同一类记录

| 记录 | 记录的事实 | 是否是实际交易日志 |
| --- | --- | --- |
| 冻结合同 CSV | 入场前的方向、Pattern、EMA gate、事件、空间、lineage、触发/止损/目标和持有合同 | 否；没有实际成交 |
| `results.csv` | 回放器对冻结合同的模拟成交、退出、路径、`trade_result` 和 `realized_R` | 否；它是模拟结果记录 |
| `summary.json` | 单次 artifact 的聚合计数、分层和描述性统计 | 否；不能替代逐笔日志 |
| `run_metadata.json` | engine/依赖、输入、结果文件和 provenance 指纹 | 否；它是运行元数据 |
| `journal/`、`trade_log/`、`transaction/`、`ledger/` | 当前 checkout 不存在这些独立日志目录；`strategy/reviews/` 只有 1 个 observation-only 研究文件 | 没有可声称的 broker/Execution Agent 记录 |

因此，当前 PA Research 没有实际订单、实际成交、持仓、账户 P&L 或 Execution Agent 交易日志。任何把 `results.csv` 的一行称为“真实交易日志”的表述都应改为“历史回放结果行”；任何把冻结合同称为已成交记录的表述都应改为“入场前研究合同”。

## 七、已落实的修复与剩余边界

本次新增本审计及回归测试，并把它加入 PA Research 研究索引、`docs/README.md`、`strategy/README.md`、回放 README、研究交接规范和文档 validator。修复内容只固化历史结果/交易日志/当前分母的语义边界，并把当前 checkout 的交易日志 inventory 纳入递归防回归检查；没有改写旧报告数字、没有新增合同、没有修改 engine 有效语义。

当前可接受的读取顺序是：先看冻结合同的事前证据，再看当前 artifact validator 状态，最后才看旧 `results.csv` 的描述性路径；不能从旧结果反向补合同字段或选择胜率更好的一份变体。

本文件只属于 PA Research；不修改 Codex Trading，不导入其规则，不创建量化扫描器，不连接 Execution Agent 或 Futu/OpenD。

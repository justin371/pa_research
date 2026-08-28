# PA Research ABC/BOP intake schema 一致性审计（2026-08-29）

结论：对统一 ABC/BOP intake 与 BOP 专项 intake 做逐行 CSV 解析、字段完整性、来源引用、方向/Pattern、BOP 状态和冻结边界核对后，发现并修正了三类真实问题：统一 intake 的 NKE 行缺少一个 CSV 字段、TSLA 2025-09-11 的统一 BOP 行方向写反、统一 intake 的 NKE `intake_id` 与 BOP 专项视图重复。修正后两份 CSV 均为结构完整、字段非空、来源可追溯且全局 `intake_id` 唯一；两种视图仍保持独立，不把 intake 当成回放合同。没有新增案例、没有下载行情、没有运行正式回放，结论保持 `no-new-positive`，`validated win-rate: not-computable`。

## 一、审计范围和方法

本轮只读取仓库内的：

- [`abc_bop_contract_intake_2026-08-28.csv`](abc_bop_contract_intake_2026-08-28.csv)；
- [`bop_contract_intake_2026-08-28.csv`](bop_contract_intake_2026-08-28.csv)；
- 两份 intake 的审计、冻结复核、backtesting README、研究索引和现行统一输出合同；
- 每一行 `source_case` 指向的既有 PA Research Markdown。

检查使用 CSV 解析器按实际字段数读取，不把分号分隔的 `missing_fields` 当成 CSV 列；同时检查 source path 在仓库内存在、行字段非空、日期可解析、方向和 Pattern 边界，以及 intake 不含 `sample_id`、不含冻结回放结果字段。没有读取行情或外部 artifact，也没有调用回放器。

## 二、两种 intake 的 schema 和字段基线

| 文件 | 列数 | 行数 | 必填字段非空 | source_case 可解析 | contract_frozen | 全局 intake_id |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| 统一 ABC/BOP intake | 18 | 10 | 10/10 | 10/10 | 10 条 `no` | 10/10 唯一 |
| BOP 专项 intake | 20 | 15 | 15/15 | 15/15 | 15 条 `no` | 15/15 唯一 |
| 合计 | 两种 schema | 25 | 25/25 | 25/25 | 25 条 `no` | 25/25 唯一 |

统一 intake 的 18 列是 `intake_id`、身份/来源、`direction`、`primary_pattern`、`internal_label`、`contract_branch`、`intake_state`、事件和事前证据字段、`missing_fields`、`freeze_recommendation`。BOP 专项 intake 的 20 列增加 `classification`、`bop_state`、旧边界、突破接受、回踩和角色转换字段，但没有统一 CSV 的 `primary_pattern`/`internal_label`；这是独立 schema 的设计，不是漏列。两者都不是当前 `backtesting.py` 的冻结合同输入。

## 三、逐行方向、Pattern 和状态核对

统一 intake 的分布为：

| 维度 | 结果 |
| --- | --- |
| 多空 | `long=6`、`short=4` |
| `primary_pattern` | `ABC_CONT=6`、`BOP=4` |
| `ABC_CONT` 内部标签 | `L1=2`、`H2=4` |
| `BOP` 内部标签 | `none=4` |
| `contract_branch` | `branch_choice_pending=5`、`reprice_branch_choice_pending=1`、`limit_retest=3`、`gap_reprice=1` |
| 冻结状态 | 10/10 为 `contract_frozen=no` |

统一 BOP 行的方向现在与来源一致：TSLA 2025-03-04 为 `short`，TSLA 2025-09-11 为 `long`，NKE 2025-10-28 为 `short`，WMT 2024-06-27 为 `long`。尤其 TSLA 2025-09-11 的来源明确描述为突破旧阻力后的多头 BOP acceptance；它不能在统一 intake 中继续写成 `short`。

BOP 专项 intake 的分布为：

| 维度 | 结果 |
| --- | --- |
| 多空 | `long=12`、`short=3` |
| `retest_class` | `intraday-only=3`、`single-session=2`、`not-occurred=10` |
| `bop_state` | `breakout_acceptance=2`、`breakout_pullback=1`、`gap_event=5`、`role_reversal_watch=1`、`failed_breakout_watch=1`、`not_bop=4`、`range_edge=1` |
| 冻结状态 | 15/15 为 `contract_frozen=no` |
| 多日正例声明 | 0 条；没有 `multi-day` 回踩或 `multi_day_bop_positive` 正向声明 |

当前 BOP 专项行仍全部属于接受、同日回测、缺口/开盘重订、首障碍或相邻形态边界；`freeze_recommendation` 均保留 `do_not_replay`，没有把“接受”或“同日回测”升级成日线级多日 BOP。

## 四、跨 schema 案例键和 lineage 边界

25 行 intake 按 `symbol + decision_date + source_case` 归并后是 22 个底层案例键；有 3 个案例同时出现在两种 intake 视图中：

| 底层案例键 | 统一 intake | BOP 专项 intake | 方向一致性 |
| --- | --- | --- | --- |
| TSLA / 2025-03-04 / `tsla_abc_playbook_2025-03-04_284_retest.md` | `BOP-TSLA-20250304-284` | `BOP-TSLA-RETEST-20250304` | `short / short` |
| TSLA / 2025-09-11 / `tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md` | `BOP-TSLA-20250911` | `BOP-TSLA-ACCEPT-20250911` | `long / long` |
| NKE / 2025-10-28 / `nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md` | `BOP-UNIFIED-NKE-20251028` | `BOP-NKE-20251028` | `short / short` |

这 3 组是同一来源案例的两种研究视图，不是 3 个新的交易样本。此前统一 intake 的 NKE 行与 BOP 专项行共用 `BOP-NKE-20251028`，会造成合并读取时的 ID 冲突；现将统一视图改为 `BOP-UNIFIED-NKE-20251028`。底层案例仍只计一个案例键，两个视图也都不进入回放分母。

## 五、发现并修正的真实问题

1. **NKE CSV 行宽错误**：统一 intake 表头有 18 列，但 NKE 行只有 17 个值，造成 `lineage_evidence` 和 `missing_fields` 错位、`freeze_recommendation` 缺失。现补齐 `ABC/L1 episode;not independent BOP lineage`、完整 `missing_fields` 和边界裁决，恢复为 18 列。
2. **TSLA 2025-09-11 方向错误**：统一 intake 该行原写 `short`，与来源中的多头 BOP acceptance 及 BOP 专项 `long` 行冲突。现改为 `long`；未改变 Pattern、订单状态或冻结边界。
3. **跨文件 `intake_id` 冲突**：NKE 两种视图原使用同一 ID。现为统一视图加上 `UNIFIED` 标识；3 个跨 schema alias 仍由底层案例键显式记录，不被误算为独立样本。
4. **validator 盲区**：原 validator 只检查 intake 表头、`source_case` 是否有值和 `missing_fields` 是否有值，没有检查每行必填字段、source path 是否存在或跨文件 ID 冲突。现已补上这些只读边界检查；动态测试同时检查 CSV 实际列数，防止末列缺失再次被 `Import-Csv` 静默接受。

## 六、结论和研究边界

修正后，intake 的正确解释是：统一视图 10 行、BOP 专项视图 15 行、合计 25 行；底层来源案例键 22 个，其中 3 个跨 schema alias。全部 25 行仍为 `contract_frozen=no`，没有 `sample_id`，没有冻结合同级精确订单/结果字段，不能送入当前回放器，也不增加 ABC/BOP/H/L/H3/L3 的胜率分母。

没有发现可以把任一 ABC/BOP 行升级为冻结正向合同的证据。BOP 日线级多日回踩正例仍为 0，ABC 候选仍处于人工冻结复核层；`no-new-positive` 和 `validated win-rate: not-computable` 保持不变。

```text
research_state: provisional
validated win-rate: not-computable
conclusion: no-new-positive
```

本审计只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

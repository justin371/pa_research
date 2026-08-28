# PA Research 合同权威与字段一致性审计（2026-08-29）

结论：发现的是研究记录层与当前回放输入层的文档边界缺口，不是有效回放语义 bug。已在 PA Research 内补齐说明和回归测试；没有下载行情、增加正式回放样本或改变 pattern 规则。当前验证结论继续保持 `no-new-positive`，`validated win-rate: not-computable`。

## 1. 审查范围

本次逐项对照：

- [`PA Research 日线选股规则`](../../docs/pa_research_daily_selection_rules_v0_1_CN.md)；
- [`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)；
- [`每日候选批次与图表审查卡`](../../docs/daily_candidate_review_card_CN.md) 与 [`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)；
- [`冻结合同回放器 README`](README.md)；
- [`contracts.example.csv`](contracts.example.csv)；
- `pa_research_backtest/engine.py` 的 `0.3.9` 常量、合同解析与校验分支。

## 2. 发现的边界问题

### 2.1 研究记录枚举比回放输入更宽

统一输出、视觉复核和订单协议需要保留 `no_valid_direction`、`stop_limit`、`observation_only`、价格区域和 `pending/unknown` 等研究状态；当前 engine 只接受 `long/short`、三种订单分支和冻结的有限数值价格。如果不显式区分，使用者可能把观察记录或区域描述直接写入回放 CSV。

### 2.2 日线候选主标签与历史回放兼容值混在模板中

当前日线选股规则的顶层主标签是 `ABC_CONT/BOP`，H1/H2/L1/L2/H3/L3 通过内部标签和关系字段记录。engine 仍支持 `H1_L1`、`H2_L2`、`H3_L3`、`RFB`、`MTR`、`other`，这是历史/兼容冻结合同的输入能力，不能被解释为日线选股规则扩展。每日候选审查卡原先把这些兼容值并列在 `primary_pattern`，已收窄为当前日线主标签。

### 2.3 记录成交状态与回放结果状态不是同一字段

研究记录的 `actual_fill_or_open_skip` 使用下划线枚举；engine 结果的 `fill_status` 使用 `no-fill`、`opening-skip`、`unproven`、`not-traded` 等结果状态。两者不能互相覆盖，也不能从记录状态直接推导胜率资格。

## 3. 已完成的修正

- 在统一输出合同中增加“研究记录超集—当前回放输入子集”的边界说明，明确方向、pattern、订单、数值字段和成交状态映射；
- 在日线规则、每日候选卡和视觉/订单协议中明确当前日线主标签及当前回放器的三种订单分支；
- 在回放 README 中固定 engine `0.3.9` 的方向、pattern、订单和数值输入边界，并明确历史/兼容 pattern 不会改变日线选股规则；
- 保留 `contracts.example.csv` 的 `ABC_CONT + H1 + stop_confirmation + frozen=yes` 作为当前可回放合同示例；
- 新增 `tests/test_pa_research_contract_consistency.py`，覆盖 engine 枚举、example 合同、日线主标签和研究记录/回放输入边界文案；
- foundation 与 strategy 模板补充同一边界提示，避免概念合同被误读为当前回放能力。

本次没有修改 `pa_research_backtest/engine.py` 的有效执行语义，没有创建量化扫描器，没有连接 Execution Agent，也没有修改 Codex Trading。

## 4. 验证与统计边界

使用仓库既有测试、文档校验、Python 编译检查和 `git diff --check` 验证：`71` 个单元测试通过，文档校验通过（`262` 个 Markdown 文件、`1229` 个链接）。测试只验证字段/文档边界，不生成市场数据，不产生新的胜率分母。任何 `stop_limit`、`observation_only`、`no_valid_direction` 或未冻结的区域记录仍不进入当前回放器或胜率统计。

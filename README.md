# PA_Research

PA Research 是一个只读、视觉优先的 Price Action 研究仓库。它记录背景、支撑阻力、EMA20/50/200、ABC/H1-H2/L1-L2、BOP、三推及边界样本，不提供生产交易授权。

当前日线选股合同：[`PA Research 日线选股规则 v0.1`](docs/pa_research_daily_selection_rules_v0_1_CN.md)。

统一输出字段：[`PA Research 统一输出合同 v0.1`](docs/pa_research_output_schema_v0_1_CN.md)。

每日候选批次与两年图表证据记录：[`每日候选批次与图表审查卡`](docs/daily_candidate_review_card_CN.md)。

## 目录

- [`docs/`](docs/README.md)：日线规则、视觉复核卡、共同上下文和研究交接边界；
- [`patterns/`](patterns/README.md)：核心八个 PA pattern 与独立视觉主题；
- [`foundations/`](foundations/README.md)：支撑阻力、事件闸门、订单合同和市场状态基础层；
- [`research/`](research/README.md)：专项审计、历史案例、视觉验收资产与当前研究结论；
- [`strategy/`](strategy/README.md)：研究优先级和候选案例清单；
- [`knowledge/`](knowledge/README.md)：学习资料与方法论摘要；
- [`pahubcn_courses/`](pahubcn_courses/README.md)：课程学习笔记与阅读边界。

## 当前边界

- 当前仓库包含一个仅供研究使用的 `backtesting.py` 冻结合同回放器；它不自动识别图形、不扫描股票、不获取行情、不提供生产交易授权，也不连接 Execution Agent。
- 回放器只接受已经由人工完整看图并在结果发生前冻结的合同；当前已有案例尚未形成经过验证的胜率证据。
- Codex Trading 只作为明确标注的只读历史参考；PA Research 不复制其规则，不修改其仓库。
- 当前结果审计保持 `no-new-positive`、`validated win-rate: not-computable`；形态候选不是胜率或下单授权。
- 聚合矩阵、Strategy inventory 与历史案例入口的逐案合同边界见[`Pattern 案例矩阵、策略入口与历史别名合同审计`](research/backtesting/pattern_case_matrix_strategy_entry_contract_audit_2026-08-29_CN.md)。
- 矩阵之外的历史 case-study、candidate-screen 与专题案例入口清单见[`历史案例入口合同盘点审计`](research/backtesting/historical_case_entry_inventory_contract_audit_2026-08-29_CN.md)；它只登记逐案合同边界，不把历史路径升级为新样本或胜率证据。
- 顶层 research 历史正向条件入口的 scope/status 与结果隔离见[`顶层 research 历史正向条件入口边界审计`](research/backtesting/top_level_research_entry_boundary_audit_2026-08-30_CN.md)；条件性研究状态不等于当前候选或授权。
- canonical index、requiredFiles、报告/资产/模板与 inventory 的交叉覆盖见[`PA Research canonical 入口交叉覆盖审计`](research/backtesting/canonical_entry_cross_coverage_audit_2026-08-30_CN.md)；覆盖守卫不等于候选、交易或胜率证据。
- canonical schema、活动模板、validator 与回放 engine 的字段/枚举/版本边界见[`schema / engine / validator 漂移审计`](research/backtesting/schema_engine_validator_drift_audit_2026-08-30_CN.md)；不新增样本或结果。

统一边界：`v0.x` 规则/合同与回放引擎 `0.3.9` 均只属于 PA Research 研究层（`PA Research only`），不是 Codex Trading 生产规则；`no-new-positive` 和 `validated win-rate: not-computable` 保持不变，`60%` 仅是待检验目标；不创建量化扫描器，不连接 Execution Agent。

## 文档校验

只读运行本地合同、索引、链接和边界校验：

```powershell
powershell -NoProfile -File .\scripts\validate_pa_research_docs.ps1
```

# PA Research 视觉识别能力与图表 provenance 边界审计（2026-08-29）

日期：2026-08-29<br>
范围：视觉识别报告、视觉协议、资产 README、ABC/三推 strategy 与统一 docs 中的能力表述和前置图表证据<br>
状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`<br>
结论：`no-new-positive`；`validated win-rate: not-computable`

## 一、审计边界

本轮只读检查 PA Research 现有 Markdown、validator 和回归测试，不下载或查询行情，不连接 Futu/OpenD，不看新图，不运行回放，不增加样本，不修改 CSV、历史结果或 engine 有效语义。本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

这里的“视觉识别能力”只指：在人工查看可读图表时，能够大体记录父级、位置、A/B/C、H1/H2/L1/L2、BOP 或三推的候选形状，并把不确定性写出来。它不是每张图都准确识别的保证，不是识别准确率，不是自动扫描器，也不是交易授权。

## 二、当前 canonical 能力边界

所有前置图表证据都按 `daily_context_window`、`major_high_low_review` 和
`ema20_50_200_review` 记录；字段缺失时保留保守状态，不从局部图或后续走势补写。

| 证据层 | 可以记录什么 | 缺失时的保守状态 | 不能推导出的结论 |
| --- | --- | --- | --- |
| 完整 Daily 左侧、主要高低点、支撑阻力 | 父级趋势/区间、位置和首障碍候选 | `daily_context_window: <2y / unavailable` 或相应 review 缺失 | 不能把局部图当成完整背景 |
| EMA20/50/200 及其 review | 趋势背景、汇合和 H/L 方向闸门线索 | `ema20_50_200_review: partial / unavailable`、slope/gate `unknown/pending` | EMA 触碰本身不是 pattern 或触发 |
| A/B/C 与 H/L-like | `pattern_like`、`research_candidate` 或边界说明 | `pending` / `observation_only` | 不能直接得到冻结合同、胜率或订单 |
| 三推/H3-L3、BOP-like、MTR-like | `third_push_state`、`state_transition` 和不确定性 | `unclear` / `observation_only` | 三次测试或一张突破图不自动生成反向/回踩交易 |
| 订单、结构止损、首障碍和空间 | 只有在独立深审且事前证据完整时才可进入合同 | `valid_no_trade`、`observation_only` 或 `pending` | 低周期触发不能补齐缺失的 Daily 背景 |

`pattern_like` 表示值得研究的外形；`research_positive_conditional` 表示多个视觉优势同时存在、值得继续深审。二者都不是准确率、已验证策略或真实下单许可。`ready_for_system` 仍是完整研究交接后的枚举，不因图表“看起来像”而自动成立。

## 三、检查结果

### 1. 能力表述已限定到人工研究层

以下历史 ABC/MTR/区间材料原本使用“稳定识别/稳定分辨/工作版已经可以使用”等容易脱离上下文的说法，现已明确为“在人工完整图表、统一字段和停止条件下可复用的研究流程”：

- [`ABC 趋势延续专项视觉证据审计`](../abc_visual_evidence_gap_audit_2026-08-24_CN.md)；
- [`ABC 研究状态与工作边界`](../abc_research_status_v0_3_CN.md)；
- [`ABC Pattern 覆盖审计`](../abc_pattern_coverage_audit_CN.md)；
- 空头 ABC 对照、MTR 视觉框架和区间边缘边界审计。

修改只收紧自然语言，没有改变任何 pattern 标签、案例判断、价格、订单、统计结果或研究优先级。现在这些文件明确写出：可做大体候选识别，但不保证每张图准确、不代表自动识别、不代表胜率或交易授权。

### 2. 图表 provenance 的职责保持不变

现有视觉资产与配对审计已经区分：

- Round2/Round3/TSLA 等配对资产可以帮助人工理解局部形状，但局部 `chart_scope: partial` 不能替代配对 Daily；
- Round4 的两年背景为 `<2y`/`partial`，公开冒烟图中部分两年背景、主要高低点和 EMA review 为 `unavailable`；
- Round5、合同资产和配对复核中记录的 `>=2y`、主要高低点、EMA review 只说明 provenance 已记录，不代表 pattern 或结果已验证。

缺少这些字段时，必须保留 `pending`、`observation_only` 或 `no_valid_direction`，不能用文件名、后续走势、低周期画面或“看起来像”补写入场前证据。

### 3. Pattern 覆盖仍是条件性研究覆盖

当前可以大体复核 H1/H2/L1/L2、ABC、BOP-like 和三推候选的外形与边界，但不同 pattern 的证据完整度、父级位置、lineage、事件、首障碍和订单分支不同。H3/L3、三推衰竭、干净多日 BOP 和 MTR 仍保留 `conditional`/`observation_only`/`no-new-positive` 边界，不能因为视觉上能认出一个近似外形就合并统计或下单。

## 四、结论与回归守卫

```text
visual_capability: human_chart_review / approximate_pattern_like_only
validated win-rate: not-computable
conclusion: no-new-positive
document_status: research_only
trade_state: not_authorized
```

本轮只修复能力表述的限定语和审计入口，并固定旧能力措辞的回归检查；没有新增视觉正例、回放分母或交易规则。PA Research 可以作为图表理解和人工筛选研究层使用，但不能被理解为准确率已测、自动扫描已实现、规则已验证或 Execution Agent 已连接。

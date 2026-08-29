# Round4、Round5 与 TSLA 视觉资产 canonical 边界审计（2026-08-29）

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

## 审计范围

本轮只审计三组剩余视觉资产及其配对历史记录：

- [`Round4 历史图表视觉练习资产`](../assets/visual_recognition/2026-08-24/round4_historical_practice/README.md)；
- [`Round4 历史图表视觉练习与 H/L/ABC 复核`](../visual_recognition_round4_historical_practice_2026-08-24_CN.md)；
- [`Round5 两年 Daily 左侧背景视觉练习资产`](../assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md)；
- [`Round5 两年 Daily 左侧背景与 ABC/H-L/三推视觉练习`](../visual_recognition_round5_two_year_daily_2026-08-24_CN.md)；
- [`TSLA 多周期视觉识别资产`](../assets/visual_recognition/2026-08-24/tsla_public_mtf/README.md)；
- 以及配对的[`PA 图表视觉识别冒烟验收`](../visual_recognition_smoke_test_2026-08-24_CN.md)。

核对内容包括 `contract_scope`、`data_status`、`as_of_time`、`timezone`、
`session_state`、`timeframes_seen`、`chart_scope`、`daily_context_window`、
`major_high_low_review`、`ema20_50_200_review`、EMA slope/gate、重要高低点、
多周期职责、方向、主次 pattern、H1/H2/L1/L2、三推、BOP、MTR、lineage、订单/空间、
状态和统计边界。

本轮没有下载或查询行情，没有访问 Futu/OpenD，没有查看新图，没有运行回放，没有增加样本，
没有修改 CSV、历史结果或 engine 有效语义；不修改 Codex Trading，不创建量化扫描器，
不连接 Execution Agent。

## 发现与修复

### 1. Round4 短窗口字段需要使用 canonical 读取

Round4 只有约 `2025-08-11`–`2026-08-10` 的 Daily 数据，不能声称完成两年左侧背景。
资产 README 和历史复核原来用 `two_year_daily: pending`，案例中还用
`lineage: provisional`、`lineage: unclear-to-range` 和 `parent_state: mixed/transition`。
现已明确：

```text
contract_scope: historical_context_only
data_status: historical
as_of_time: per-case cutoff; dataset end 2026-08-10
timezone: unavailable_in_original_snapshot
session_state: historical_close
timeframes_seen: Daily / 4H / 15m (case-specific)
chart_scope: partial
daily_context_window: <2y
major_high_low_review: partial
ema20_50_200_review: partial
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
direction: long / short / no_valid_direction
lineage_status: same_lineage / reset / unclear / pending
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
first_independent_obstacle: visual candidate only; not a frozen order field
pre_entry_space_R: unknown unless trigger and structural stop are independently frozen
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
handoff_status: not_ready
```

历史显示词仍可在案例解释中保留，但只能按别名读取：
`two_year_daily: pending` → `daily_context_window: <2y`；`lineage: provisional`
或 `lineage: unclear-to-range` → `lineage_status: pending` 或 `unclear`；
`parent_state: mixed/transition` → 依据主导证据写 `transition`。`ABC-like`、
`H1-like`、`L1/L2-like` 和 `three-push-like` 不会因此变成冻结的
`primary_pattern`、`internal_label` 或 `third_push_state`。

Round4 来源中的 Codex Trading 历史 OHLC 只作为只读素材来源，不导入 Codex Trading
规则、代码、实现状态或执行能力。

### 2. Round5 资产 README 需要与已规范的历史报告对齐

Round5 历史报告已经记录 `contract_scope: historical_context_only`、4 个标的、8 个
案例的 `daily_context_window: >=2y`、重要高低点和 EMA20/50/200，但资产 README
只有自然语言窗口说明，没有独立的证据头。现已补充：

- `data_status: historical`、每案例 cutoff、原日志时间戳缺失和 `historical_close`；
- `chart_scope: partial`，因为 SPY/QQQ/IWM 缺 15m，COHR 的 15m 只覆盖局部；
- `daily_context_window: >=2y`、`major_high_low_review` 和 `ema20_50_200_review` 的
  配对复核来源；
- `daily_ema20_slope`、`daily_ema50_slope` 为 `unknown`，`h_l_ema_slope_gate` 为
  `pending`，不把 EMA 位置当成 H/L gate；
- 未标注资产的 `direction: no_valid_direction`、`internal_label: pending`、
  `research_state/trade_state/gate_result: observation_only` 和 `handoff_status: not_ready`。

这些字段只描述资产与配对报告的证据关系，不把 8 个练习案例改成严格 H/L、三推、BOP
或 MTR 合同；原报告的 `lineage_status`、`third_push_state` 和 `space_status: unknown`
保持不变。

### 3. TSLA 资产 README 需要明确与冒烟报告的配对边界

TSLA 资产已经有公开历史来源、约两年 Daily、EMA20/50/200 和 4H-like 的聚合说明，
但没有结构化写出 `as_of_time`、`session_state`、review 完成度、EMA slope/gate、
未标注状态和配对报告入口。现已补充同一 canonical provenance header，并明确：

- `4H-like` 仍是 60m RTH bar 聚合，不冒充原生 4H；
- 资产本身不冻结 `primary_pattern`、H1/H2/L1/L2、三推、BOP、MTR、订单或空间；
- 多周期的 `MTR/recovery candidate`、ABC/H2-like 和 BOP-like 只能按冒烟报告的
  历史视觉候选读取；
- `daily_ema20_slope`/`daily_ema50_slope` 未从资产说明中冻结，`h_l_ema_slope_gate`
  保持 `pending`，因此不能把它升级为严格 H/L 样本。

## 统计、回放和安全边界

- Round4：42 个筛选标的、7 个 targeted 案例、3 个额外多周期练习和 1 个 MRVL 直接
  Daily 复核；`round4_strict_same_lineage_freezes: 0`、两年完整案例为 0、新可比正样本为 0；
- Round5：4 个标的、8 个两年背景案例；`round5_strict_same_lineage_freezes: 0`，没有
  新可比正样本；
- TSLA：静态多周期资产只支持历史视觉候选，冒烟报告仍是 `acceptance-pending`，干净
  多日 BOP 保持 `no-new-positive-for-clean-multiday-BOP`；
- 本轮没有新增 CSV、冻结合同或结果；`no-new-positive` 保持；
- `validated win-rate: not-computable`，不能从图像资产数量、近似 pattern 或练习状态推出胜率；
- `PA Research only`；`no Codex Trading`；`no quantitative scanner`；`no Execution Agent`。

## 验证结论

本轮只修复了 Round4/Round5/TSLA 资产与历史记录的 provenance、canonical 字段映射和
索引边界。Round4 的短窗口仍是 `<2y`，Round5 的背景完成不等于计数完成，TSLA 的
多周期候选不等于交易合同；H/L、三推、BOP、MTR 的严格确认和统计仍按现有
`no-new-positive`/`validated win-rate: not-computable` 结论保留。

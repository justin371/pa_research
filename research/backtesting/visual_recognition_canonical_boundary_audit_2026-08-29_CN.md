# 视觉识别冒烟、快筛协议与 Round2/Round3 资产 canonical 边界审计（2026-08-29）

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

## 审计范围

本轮只审计 PA Research 的视觉识别入口和配对资产说明：

- [`PA 图表视觉识别冒烟验收`](../visual_recognition_smoke_test_2026-08-24_CN.md)；
- [`PA Pattern 视觉筛选协议`](../visual_pattern_triage_protocol_CN.md)；
- [`第二轮多标的多周期视觉资产`](../assets/visual_recognition/2026-08-24/round2_multisymbol/README.md)；
- [`H1/H2 与 L1/L2 局部盲测资产`](../assets/visual_recognition/2026-08-24/round3_hl_drills/README.md)；
- [`MAR 空头 L1/L2-like 视觉资产`](../assets/visual_recognition/2026-08-24/round3_l1_l2_mar/README.md)；
- 以及它们链接的当前 canonical schema、视觉复核卡和历史 Round2/Round3 复核记录。

核对的轴包括：`contract_scope`、`data_status`、`as_of_time`、`timezone`、
`session_state`、`timeframes_seen`、`chart_scope`、两年 Daily 左侧、重要高低点、
EMA20/50/200、父级状态、方向、主次 pattern、H1/H2/L1/L2、三推、BOP、MTR、
lineage、状态轴、订单/空间和 handoff 边界。

本轮没有下载或查询行情，没有访问 Futu/OpenD，没有看新图，没有运行回放，没有增加样本，
没有修改 CSV、历史结果或 engine 有效语义；不修改 Codex Trading，不创建量化扫描器，
不连接 Execution Agent。

## 发现与修复

### 1. 快筛工作字段与 canonical 字段缺少显式映射

冒烟记录的 `visual_pattern_label`、`pattern_candidate`、`attempt_or_count`、
`recognition_result` 和协议的 `stage_1_status` 是合理的阶段性工作字段，但如果
没有映射，容易被误读成统一合同中的 `primary_pattern`、`internal_label` 或交易状态。
现在已在冒烟记录和快筛协议中明确：

| 历史/快筛字段 | canonical 边界 |
| --- | --- |
| `visual_pattern_label`、`pattern_candidate` | 视觉候选展示；只有完整且闭合的研究合同才映射到 `primary_pattern` |
| `H1-like`、`H2-like`、`L1/L2-like` | 在同一周期、同一回调 lineage 和必要分流证据完成前，保留 `internal_label: pending` |
| `three-push candidate` | 保留 `third_push_state: unclear`，不能仅凭次数升级 H3/L3 或 MTR |
| `attempt_or_count`、`count-pending` | 计数备注；另填 `lineage_status: same_lineage / reset / unclear / pending` |
| `stage_1_status` | 视觉阶段结果；分别映射 `research_state`、`trade_state`、`gate_result`，不直接授权 |
| `rough_space`、`stage_2_status` | 历史工作别名；新记录优先使用 `space_status`、`research_state` 等 canonical 字段 |

冒烟文件继续不冻结自由文本的 `primary_pattern`，保留原来的 stage-1 研究边界；
第二轮表格中的旧 `primary_pattern:` 展示词已改成 `visual_pattern_label:`，避免
把自然语言描述误认为统一合同字段。

### 2. 历史 evidence header 不足以判断覆盖完整度

TSLA 和第二轮原有 `data_status`、请求窗口、最新完整 bar、周期和 `>=2y` 记录，
但缺少 `as_of_time`、`timezone`、`session_state`、`major_high_low_review`、
`ema20_50_200_review` 和 slope/gate 的显式边界。Round3 的 H/L 局部复核及 MAR
资产 README 还需要明确：局部图不能替代配对的两年 Daily，60m proxy 不能冒充 15m。

现已补齐或明确为保守状态：

```text
data_status: historical
session_state: historical_close
chart_scope: full / partial
daily_context_window: >=2y（局部资产通过配对 Daily）
major_high_low_review: complete（配对复核已记录）
ema20_50_200_review: complete（Daily EMA；斜率不足时保持 unknown）
daily_ema20_slope: unknown
daily_ema50_slope: unknown
h_l_ema_slope_gate: pending
```

前五张公开网页图片因原图的标的、周期、时间和完整左侧背景不完整，仍明确为
`chart_scope: partial`、`daily_context_window: unavailable`、两项 review 为
`unavailable`、`direction: no_valid_direction` 和 `observation_only`。这不是把
缺失资料改成通过，而是把缺失本身写进 provenance。

### 3. 方向、父级、三推和状态转换的显示词已收紧

Round2/Round3 原有记录能够描述多头/空头，但历史写法中存在 `same-lineage
provisional`、`lineage provisional`、`unclear-to-range`、`A_quality` 和
`15m-evidence-missing` 等容易与 canonical 枚举混用的显示词。现已按证据保守读取：

- `same-lineage provisional`、`lineage provisional` → `lineage_status: pending`；
- `unclear-to-range` → `lineage_status: unclear`，父级按证据写
  `trading_range / range_edge / transition`；
- 区间内多次上推 → `third_push_state: range_repeat_test`，不是自动的衰竭楔形；
- `A_quality: directional but late...` → `a_leg_quality: ordinary`，原解释保留为历史说明；
- `15m-evidence-missing` → 覆盖限制说明，不是 `research_state`、`trade_state` 或
  `gate_result` 的新值；
- BOP-like、MTR/recovery candidate 和 failed-reclaim 仍是视觉候选或状态说明，
  不自动成为已接受的 `primary_pattern`、订单或授权。

Round3 H/L 证据头还明确 `direction: no_valid_direction` 是未标注局部资产的汇总值；
逐案例的多空视觉解释不因此变成冻结方向。MAR 的空头读法保留为配对历史候选，
但在缺少 15m 和 EMA slope gate 时仍是 `observation_only`。

### 4. 资产 README 与配对研究记录边界已固定

Round2、Round3 H/L 和 MAR 的 README 现在都声明：

- `contract_scope: historical_context_only`，且数据为公开历史、不是 Futu、不是实时授权；
- 资产生成/可用 bar 的时间、时区和 session 状态；
- Daily 左侧、重要高低点、EMA20/50/200 的完成度及其来自配对复核记录；
- 未标注资产本身不冻结 `primary_pattern`、`internal_label`、三推、BOP、MTR 或订单；
- 局部 `chart_scope: partial`、配对 Daily 的职责和 `handoff_status: not_ready`。

因此图像资产的“可用于研究”与研究合同的“已闭合”分开：资产可以帮助视觉识别，
但不会因为文件名、标题或后续复核文字而自动产生交易方向、触发、止损、空间或成交结果。

## 统计、回放和安全边界

- 本轮没有新增视觉样本，也没有修改 7 份 CSV、60 行冻结合同、历史结果或 engine 语义；
- 没有新的可比正样本，`no-new-positive` 保持不变；
- 当前 `validated win-rate: not-computable`，不能从冒烟计数、`pattern_candidate`、
  `H2-like`、`L1/L2-like` 或三推候选推出胜率；
- 订单分支、`gap_policy`、结构止损、第一独立障碍和 `space_status` 仍需在独立的
  深审/冻结合同中填写，不能从视觉 asset README 倒填；
- `PA Research only`；`no Codex Trading`；`no quantitative scanner`；`no Execution Agent`。

## 验证结论

本轮修复的是字段和 provenance 的可读性，不是 pattern 识别算法，也没有把视觉候选
升级为规则。现在的最小边界是：先记录历史证据头和两年 Daily/重要高低点/EMA 复核，
再记录方向、父级、A/B、lineage 和 H/L/三推/BOP/MTR 候选；证据不足时保持
`pending`、`observation_only` 或 `no_valid_direction`。严格计数、订单、空间和统计
仍需后续独立合同，当前 acceptance 仍未完成。

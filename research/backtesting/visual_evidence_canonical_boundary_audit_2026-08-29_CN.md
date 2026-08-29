# 历史视觉证据与 canonical 边界审计（2026-08-29）

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

## 审计范围

本轮只审计三份 PA Research 历史视觉记录及其索引：

- [`三推 / H3-L3 视觉证据缺口审计`](../three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md)；
- [`H/L lineage 与三推状态视觉边界复核`](../h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)；
- [`Round5 两年 Daily 左侧背景与 ABC/H-L/三推视觉练习`](../visual_recognition_round5_two_year_daily_2026-08-24_CN.md)。

核对内容是：历史数据状态和左侧两年背景、主要高低点与 EMA20/50/200、三推/区间重复、lineage、方向、订单/空间文字，以及它们是否仍与[`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)一致。

本轮没有下载行情、访问 Futu/OpenD、查看新图、运行回放、增加样本、修改 CSV、历史结果或 engine 有效语义；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

## 发现与修复

### 1. 历史标签不能冒充 canonical 字段

H/L 协议和 Round5 原来把 `same-lineage-provisional`、`unclear-to-range`、`same-pressure-zone-provisional`、`provisional` 等历史说明直接放在 `lineage_status` 位置。它们不是当前枚举，且会把“仍待核对”误读成 `same_lineage`。

现已按证据保守映射：

| 历史显示词 | canonical 读取 |
| --- | --- |
| `same-lineage-provisional`、`same-pressure-zone-provisional`、`provisional` | `lineage_status: pending` |
| `unclear-to-range` | `lineage_status: unclear`；必要时另写 `parent_state: trading_range` 或 `range_edge` |
| `range-repeat` | `third_push_state: range_repeat_test` |
| `expansion-or-climax` | `third_push_state: continuation_or_climax`；若仍无法分流则写 `unclear` |
| `first_obstacle_candidate`、`first-obstacle-boundary` | 说明性的 `first_independent_obstacle` 候选；没有触发/结构止损时 `space_status: unknown` |
| `research_positive_candidate` | 当前记录使用 `research_positive_conditional`，并保持 `trade_state: not_authorized` |

原始自然语言仍可保留作历史解释，但新字段不再用连字符或 `provisional` 拼接出新枚举。H/L 协议已补齐 `attempt_direction`、`third_push_state`、`first_reverse`、`second_confirmation`、`range_edge_side`、状态迁移和研究/交易/gate 轴；三推审计的 KLAC 条件候选也已改用 canonical 状态轴。

### 2. Round5 的两年 Daily 证据头和逐案边界

Round5 原来在每个案例中写了 `>=2y`、主要高低点和 EMA 数值，但没有统一说明原始查询时间和时区缺失，也没有把低周期覆盖不对称写成 `chart_scope`。现已补充聚合证据头：

```text
contract_scope: historical_context_only
data_status: historical
as_of_time: per-case cutoff; query timestamp unavailable in original log
timezone: unavailable_in_original_log
session_state: historical_close
timeframes_seen: Daily / 4H / 15m (case-specific)
chart_scope: partial
daily_context_window: >=2y (8/8 cases)
major_high_low_review: complete (8/8 cases)
ema20_50_200_review: complete (8/8 cases)
```

这只确认历史视觉背景字段的记录状态，不把历史数据变成实时数据，也不把 `daily_ema20_50_200` 的位置数值当作 EMA 斜率闸门。Round5 没有冻结 `daily_ema20_slope`、`daily_ema50_slope` 或 `h_l_ema_slope_gate`，所以其中的 H1/H2/L1/L2-like 仍是练习标签。

Round5 新增逐案 canonical 摘要，明确区分 `parent_state`、`direction`、`lineage_status`、`internal_label`、`attempt_direction`、`third_push_state`、`range_edge_three_push/range_edge_side`、`state_transition` 和研究状态轴。八个案例均保持 `order_branch: observation_only` 的视觉边界；首障碍只是视觉候选，未从历史文字倒推 `strict_ge_1R`，`space_status` 均保留 `unknown`。

### 3. 三推、区间边缘和订单空间仍是不同轴

三推审计继续把原方向的第三次尝试与反方向 H1/H2 或 L1/L2 分开。区间上沿/下沿的三次测试可以进入 `range_edge_three_push` 研究分支，但不能仅凭次数升级 H3/L3 或 MTR；外侧被接受时仍切换到 BOP/趋势延续解释。

订单文字（`sell-stop`、`gap-reprice`、首支撑/首阻力和粗略 R/R）继续只是历史案例边界。需要建立回放合同时，必须另行冻结：

```text
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
gap_policy: accept_open / skip / flag_only / not_applicable
structural_stop:
first_independent_obstacle:
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
```

跳空重订、首障碍拥挤、`no-fill` 或 `opening-skip` 都不是 win/loss；本轮三份历史视觉记录没有新增冻结订单，也没有进入胜率分母。

## 结论和统计隔离

- H/L 视觉协议的 provisional lineage 现在显式降为 `pending`，RBLX 等区间重复样本显式使用 `range_repeat_test`，不再把模糊标签当作严格计数；
- Round5 仍有 4 个标的、8 个 targeted 案例、8/8 两年背景完整记录，但严格同 lineage 冻结为 0；
- Round5 没有新增可比正样本，三推/H3/L3 冻结合同仍为 0；
- 当前冻结合同集合仍是 7 份 CSV、60 行；本轮不修改 CSV、不改变历史结果、不建立新的统计分母；
- `no-new-positive` 和 `validated win-rate: not-computable` 保持不变。

正式边界：`PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。

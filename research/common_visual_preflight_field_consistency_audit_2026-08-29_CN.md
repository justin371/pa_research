# PA Research 共同视觉前置字段一致性审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 目的与范围

本次审计核对以下 PA Research 文档是否对共同视觉前置要求使用同一套字段和语义：

- [`PA Research 统一输出合同`](../docs/pa_research_output_schema_v0_1_CN.md)；
- [`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)；
- [`每日候选批次与图表审查卡`](../docs/daily_candidate_review_card_CN.md)；
- [`PA Research 日线选股规则`](../docs/pa_research_daily_selection_rules_v0_1_CN.md)；
- [`PA Research — Common Context`](../docs/common_context.md)；
- [`patterns/README.md`](../patterns/README.md) 与 16 个 pattern README。

审计只处理文档字段、状态枚举和模板边界。不下载行情、不查看新图、不运行正式回放、不新增样本、不改变 pattern 规则或 engine 有效语义。

`scope_boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。

## 1. Canonical 共同视觉前置

所有完整案例先使用统一输出合同。以下字段是共同前置的 canonical 名称：

```text
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
major_highs_lows:
daily_ema20_50_200:
a_leg_quality: strong / ordinary / unclear / event_driven
b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear
b_leg_location:
first_independent_obstacle:
```

两年 Daily 左侧是 `daily_context_window`；重要高低点和 EMA 是否真的看全，分别由两个 `*_review` 字段记录。`chart_scope` 只表示整张图表的可见完整度，不能代替两年窗口。`a_leg_quality`/`b_leg_class` 是共同的 A/B 质量字段；独立主题可以把它们作为背景对照，但不能因此继承 ABC/H-L 计数。

批次级 `two_year_chart_coverage` 只表示一批候选的覆盖摘要；它不能替代逐标的 `daily_context_window`。`major_highs`/`major_lows` 是 `major_highs_lows` 的展示拆分，`price_vs_ema20_50_200` 是 `daily_ema20_50_200` 的补充描述，不是完整度字段的替代品。

## 2. 本次发现与修复

### 2.1 Common Context 缺少共同前置的明确字段

原文强调视觉优先和左侧结构，但没有把“两年 Daily、重要高低点、EMA20/50/200、A/B 质量、数据状态”集中写成所有入口共享的前置。现在已补充 `Common visual preflight`，并明确缺失证据只能保留为部分/待定，不能用局部图或后续走势补写。

### 2.2 统一合同缺少 A/B 质量字段

日线候选卡已经使用 `a_leg_quality` 和 `b_leg_class`，视觉卡则使用过 `A_quality`/`B_quality` 形式，统一合同没有对应公共字段。现在统一合同、视觉卡、日线卡和 pattern 索引统一使用：

- `a_leg_quality: strong / ordinary / unclear / event_driven`；
- `b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear`；
- `b_leg_location:`。

这只是记录字段统一，不把强 A 或受控 B 变成自动入场信号。

### 2.3 `chart_scope` 与事件字段枚举漂移

视觉卡原来使用 `full context / partial context`，日线卡使用 `full_2y_plus_local_zoom`；视觉卡的事件示例还有 `none known`。现在三份模板统一为：

```text
chart_scope: full / partial / unavailable
event_context: none / earnings / macro / gap / other / unknown
```

两年覆盖由 `daily_context_window` 表达，不能把 `full` 自动解释为已经看满两年。

### 2.4 日线卡缺少 EMA 审查完整度字段

日线卡原有 `daily_ema200_context` 和 `price_vs_ema20_50_200`，但没有 canonical `ema20_50_200_review` 和 `daily_ema20_50_200`。现已补齐，并保留原两个字段作为细节描述；它们不能替代完整度判断。

### 2.5 日线规则模板与统一合同的旧字段名

日线选股规则模板中的以下字段已映射为统一名称：

| 旧字段 | canonical 字段 |
| --- | --- |
| `completed_daily_bar_as_of` | `completed_bar_as_of` |
| `average_dollar_volume_20d` | `avg_20d_dollar_volume_usd` |
| `two_year_daily_context` | `daily_context_window` |
| `why_it_meets_the_rule` | `why_it_meets_or_fails_the_rule` |
| `possible_daily_entry_trigger` | `possible_entry_trigger` |

同时补齐 `timeframes_seen`、`chart_scope`、两个视觉 review 完整度字段以及 A/B 质量字段。没有改变日线选股规则本身。

### 2.6 Pattern-specific 的 `final_state` 歧义

05 号失败突破/高潮 README 的最小审计卡曾用未定义的 `final_state` 和带连字符的混合值。现改为 `breakout_climax_state`，明确这是该 pattern 的分流字段；最终研究、交易、闸门和交接仍必须分别使用 canonical `research_state`、`trade_state`、`gate_result` 和 `handoff_status`。

验证过程中还发现研究索引中的 VCP 审计链接缺少日期后缀，已修正为仓库中实际存在的 `vcp_minervini_visual_evidence_gap_audit_2026-08-24_CN.md`。这只是链接修复，不是内容或结论变更。

## 3. 16 个 pattern 入口状态

以下目录均保留自己的 pattern-specific 定义，同时在进入定义前明确记录 `data_status`、`as_of_time`、`chart_scope`、`timeframes_seen`、至少两年的 Daily 左侧、重要高低点、EMA20/50/200、位置、首障碍和缺证据时的 `pending`/`observation_only`：

1. [`H1/L1`](../patterns/01_h1_l1_first_entry/README.md)
2. [`H2/L2`](../patterns/02_h2_l2_second_entry/README.md)
3. [`ABC`](../patterns/03_abc_continuation/README.md)
4. [`交易区间边缘二次入场`](../patterns/04_range_edge_second_entry/README.md)
5. [`失败突破与高潮`](../patterns/05_failed_breakout_climax/README.md)
6. [`BOP`](../patterns/06_breakout_pullback_bop/README.md)
7. [`MTR`](../patterns/07_mtr_reversal/README.md)
8. [`三推/H3-L3`](../patterns/08_three_push_h3_l3/README.md)
9. [`VCP`](../patterns/09_vcp_minervini/README.md)
10. [`Final Flag`](../patterns/10_final_flag/README.md)
11. [`Opening Reversal`](../patterns/11_opening_reversal/README.md)
12. [`Channel`](../patterns/12_channel/README.md)
13. [`Inside Bar / Two-Bar Reversal`](../patterns/13_inside_bar_two_bar_reversal/README.md)
14. [`Triangle / Expanding Range`](../patterns/14_triangle_expanding_range/README.md)
15. [`Double Top/Bottom`](../patterns/15_double_top_bottom/README.md)
16. [`Head & Shoulders / Rounded`](../patterns/16_head_shoulders_rounded/README.md)

核心八个继续遵守当前日线主标签边界；独立主题不因为共享视觉前置而获得 ABC/H-L 主标签。08 号区间边缘三推仍允许普通 A，但不能省略边缘位置、拒绝、触发、首障碍和空间。

## 4. 结论与研究边界

- 共同视觉前置字段现在在统一合同、两张审查卡、日线规则、Common Context、pattern 索引和 16 个入口之间有明确 canonical 映射。
- `data_status` 只描述证据状态；历史、延迟、实时已确认和不完整不能互换。它不表示行情已在本次审计中获取。
- 两年背景、重要高低点、EMA 位置/斜率、强 A、受控 B、方向、位置和第一独立障碍仍是人工视觉证据，不是量化扫描器条件。
- `no-new-positive` 与 `validated win-rate: not-computable` 保持不变。本次没有新增样本、结果或胜率统计。
- 本次只更新 PA Research 文档、索引和回归测试：不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

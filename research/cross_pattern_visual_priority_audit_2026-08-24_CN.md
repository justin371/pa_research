# Cross-Pattern / 跨 Pattern 视觉优先级与冲突消解审计

日期：`2026-08-24`  
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。

同一段行情可能同时像 ABC、H2、双顶、三推、通道或 Final Flag。PA Research 的目标不是把所有名字都贴上去，而是选出一个主标签，保留必要的次标签，最后单独判断订单和空间是否允许交易。

## 1. 总原则：状态优先于形状，合同优先于标签

```text
完整图表与周期
→ parent_state / 主要支撑阻力
→ A/B 压力与 lineage
→ pattern 主标签
→ 次标签/关系标签
→ 接受/失败/状态切换
→ 订单、结构止损、第一障碍、R/R
→ research_candidate / observation_only / valid_no_trade
```

### 1.1 主标签、次标签和输出状态

- `primary_pattern`：当前最能解释父级市场状态和交易合同的一个 pattern；
- `secondary_context`：辅助解释，例如 `H2_within_ABC`、`three_push_evidence_for_MTR`、`range_edge_with_double_bottom`；
- 若 `contract_scope: daily_candidate`，`primary_pattern` 只允许 `ABC_CONT` 或 `BOP`；H1/H2/L1/L2/H3/L3 只能写入 `internal_label`，不能把内部计数或独立主题名称写回日线主标签；
- `state_transition`：BOP、失败突破、区间过渡或 MTR 候选；它描述市场从一个状态转到另一个状态，不应与旧状态同时作为当前合同；
- `trade_state`：无论形状多漂亮，空间、事件、成交或止损不成立时，输出 `valid_no_trade`。

共存标签不能重复计算优势。一个 H2、一个双底和一个 50% 回撤如果都落在同一价格簇，不能被当成三个独立胜率来源；它们只是同一个位置的不同描述。

## 2. 五步优先级协议

### 第一步：先判父级市场状态

| 父级状态 | 优先逻辑 | 降级逻辑 |
| --- | --- | --- |
| `open_trend` | A/B、ABC、H1/H2、L1/L2、通道/旗形 | 反向形状先记 reversal attempt |
| `trading_range` | 上沿/下沿、二次入场、失败突破 | 区间中部只观察 |
| `transition` | 先观察压力是否真正转移 | 不强行计 ABC、MTR 或头肩 |
| `climax` | 小反转/平衡/Final Flag 候选 | 不凭一根反向 K 做主要反转 |
| `open_trend`（边界已接受） | BOP/新趋势/旧边界回测 | 旧区间或旧 MTR thesis 失效 |

若父级是成熟区间，区间边缘优先级高于区间内部趋势计数；若边界外已经接受，BOP 优先于原来的双顶、三推或 MTR 叙事。

表中的“边界已接受”不是新的 `parent_state` 值；当前合同用 `parent_state: open_trend` 配合 `state_transition: breakout_acceptance` 表示。早期材料中的 `mature_range`、`climax_or_exhaustion` 和 `accepted_breakout` 只按历史显示语义读取，不能写入新的统一模板。

### 第二步：再看主要位置

先排序左侧主要高点/低点、区间上下沿、突破回测区、缺口边缘、通道边界，再看 EMA、50% 回撤、MM 和形状。主要位置不清楚时，形状最多是 `pattern_like`。

### 第三步：审计 A/B 压力和 lineage

- 强方向、少重叠、跟随清楚的 A：优先 H1/L1 或 ABC 延续；
- 普通 A 或深但后段稳定 B：可保留 H2/L2；
- B 反向压力继续扩张、穿越关键极值或变成宽重叠：切到区间/新趋势/状态过渡；
- 新极值和结构性接受出现后，旧计数不无限延续。

### 第四步：选择一个主标签

主标签应能回答“如果要研究订单，当前最先研究哪一份合同”。选择顺序通常为：

1. 已接受的 BOP/新趋势；
2. 成熟区间边缘或失败突破；
3. 开放趋势的 ABC/H1/H2/L1/L2；
4. 三推、双顶/底、头肩等形状候选；
5. Channel、Final Flag、Inside Bar、Triangle 作为父级/子结构描述；
6. VCP 作为独立的强势股收缩体系，不与 Brooks H/L 自动合并。

这不是固定胜率排序，而是防止把一个已发生的状态切换继续用旧名称解释。

### 第五步：最后审计交易合同

主标签成立不等于可交易。必须另外记录 signal/trigger、实际成交或开盘跳过、结构止损、第一独立障碍、粗略 R/R、事件/板块/市场和失效条件。首障碍不足约 `1R`、结构止损过宽、财报前三个交易日或订单无法冻结时，直接 `valid_no_trade`。

## 3. 典型冲突矩阵

| 冲突 | 主标签选择 | 次标签保留 | 何时切换 |
| --- | --- | --- | --- |
| 双顶/底 vs H3/MTR | 先按双顶/底或区间边缘 | `three_push_evidence` | 反向结构破坏+第二次确认+空间后才 `MTR_candidate` |
| 三角形 vs Inside Bar/IOI | 多级别双向测试优先 Triangle | `inside_compression` | 只有母子 K 范围时不升级三角形 |
| 三角形 vs 旗形/Channel | 单方向 A/B 且原趋势控制，优先旗形/通道 | `triangle_like` | 双向多次测试和收窄真正形成后才改 Triangle |
| Channel vs Trading Range | 边界有坡度且仍有同向跟随，优先 Channel | `range_transition` | 边界趋平、中线频繁穿越后改区间 |
| Final Flag vs 普通旗形 | 趋势成熟、末端压缩才考虑 Final Flag | `ordinary_flag` | 原趋势早/中段或空间足则普通旗形 |
| Final Flag vs BOP | 已强收盘接受边界，优先 BOP | `final_flag_context` | BOP 接受会废弃旧反向假设 |
| H2 vs 区间边缘二次入场 | 父级成熟区间时优先区间边缘 | `H2_like` | 区间外接受后重建开放趋势 H2/ABC |
| Opening Reversal vs BOP | 开盘方向被接受，优先 BOP/开盘延续 | `opening_context` | 第一波失败并回原侧后才研究开盘反向 |
| 头肩 vs 双顶/底 | 没有清楚颈线时优先双顶/底候选 | `head_shoulder_like` | 颈线、右肩和第二次确认清楚后才升级 |
| 圆顶/底 vs MTR | 圆形只作过渡背景 | `rounded_transition` | 结构破坏、二次确认和空间齐全才 MTR |
| VCP vs PA pattern | VCP 保留独立体系主标签 | `PA_context` | 不把收缩次数、pivot 和 H2 计数混成一套规则 |

## 4. 状态切换的硬边界

### BOP 接受

边界外强收盘、后续跟随、回测守住后，输出：

```text
primary_pattern: BOP
secondary_context: former_range / former_double_top / former_triangle
state_transition: breakout_acceptance
old_thesis: invalidated
next_contract: breakout-continuation or limit-retest
```

不能同时把旧双顶空头、旧 MTR 和新 BOP 当作当前三个机会。

### 失败突破

只有越界后重新进入原结构、出现反向压力和第二次确认，才输出失败突破候选。第一根影线只是 test。若随后原方向重新接受，失败突破 thesis 再次失效。

### 计数重置

当 B 穿越关键极值、父级从趋势变区间、或新 A 腿已经建立时，H1/H2/L1/L2 和 ABC 计数重置。不能为了保留一个漂亮的 H2，把区间中部摆动硬接回旧回调 lineage。

## 5. 现有案例的统一裁决

### TSLA `2025-09-08–09-12`

早期看起来可以有阻力下双高、三推、Final Flag 或 MTR 空头候选；但 `09-11` 强收盘突破并有跟随、回测守住。主标签应改为 `BOP`，并以 `state_transition=breakout_acceptance` 记录接受；旧反向标签只做历史背景。

### TSLA `2024-03-04–03-14`

双顶、H3-like 和 MTR 都可以作为次要描述，但父级区间上沿和失败突破更重要。L2 方向条件存在，过程却先触发结构止损；最终状态 `range_edge / MTR_candidate / process_stop_first / valid_no_trade`。

### RBLX `2024-03-18–04-05`

双底、逆头肩、Triangle 和 ABC 都有外观，但父级宽区间、区间中部首磁铁和信号失败决定主标签是 `range_edge / failed_breakout`，不是趋势延续或 MTR。

### KLAC `2025-10-14–10-24`

两根反向 K、Inside-like、Triangle-like、右肩和 H1 都可以被看到；但强多头趋势、浅 B、原方向跟随更直接解释为 `ordinary_flag / H1-continuation`。第一阻力过近，仍 `valid_no_trade`。

### ASML `2025-05-19–06-13`

双底、圆底、逆头肩和三推样都只能做次要描述。父级下沿重复测试后进入重叠区间，主标签是 `range_transition / range_inside_range`，没有 MTR 或开放趋势 ABC 合同。

### XOM/COIN `2024`

多次测试、H3-like、Triangle-like 和宽通道可以共存，但第三次范围扩张、跳空重订和首支撑拥挤决定主标签为 `expanding_boundary / valid_no_trade`，不升级为衰竭反转。

### VCP

VCP 的连续波动收缩、pivot、相对强度和市场环境属于独立 Minervini/SEPA 体系。可以在 PA 图表中记录 `PA_context`，但不能把 VCP 的形态外观当作 Brooks H2、三推或 BOP 的证明，也不能重复计算收缩优势。

## 6. 统一输出模板

```text
contract_scope: deep_review / daily_candidate / historical_context_only
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
direction: long / short / no_valid_direction
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
secondary_context: zero_or_more relationship labels
location_and_left_structure
A_pressure / B_pressure / lineage
acceptance_or_failure_state
signal_bar / trigger / follow_through
order_branch: stop_confirmation / limit_retest / market_close / observation_only
actual_fill_or_open_skip
structural_stop / invalidation
first_independent_obstacle / rough_R_R / MM_after_obstacle
event_context / event_bucket / sector_reference / market_reference
pre_entry_space_R / space_status
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
unresolved_conflict: one sentence
```

推荐一句话输出顺序：

> “主标签是 X，因为父级是 Y、位置在 Z；A/B 和接受/失败证据支持它。另有次标签 W，但不重复计分。订单用 Q；由于首障碍/事件/成交几何，当前是候选或 `valid_no_trade`。”

## 7. 当前结论与缺口

1. PA Research 的视觉助手应先选主状态和主合同，再附带次标签；不要输出一串没有优先级的 pattern 名称。
2. 父级成熟区间和已接受 BOP 是最强的分流闸门；它们会重置旧 ABC/H-L/MTR/双顶叙事。
3. H/L 与 ABC 可以共存，三推/双顶/头肩只能提供压力或位置证据；MTR 需要额外的结构破坏和第二次确认。
4. Channel、Triangle、Inside Bar、Final Flag 是不同尺度的描述，不能因外观相似而互换。
5. 现有 TSLA、KLAC、RBLX、ASML、NFLX、XOM、COIN 已覆盖主要冲突边界；下一步有价值的新增案例应填补无事件、空间宽裕、合同完整的正例，而不是重复 no-trade。

本审计只服务 PA Research 的视觉分流与人工复核；不建立量化评分器，不修改 Codex Trading，不连接 Execution Agent。

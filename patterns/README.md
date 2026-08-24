# PA Research 核心 PA Pattern 与独立体系目录

状态：`visual-research / provisional / not-quantitative`

这里是 PA Research 当前阶段的核心研究入口。目标是让视觉助手能够在完整图表上：

1. 先识别背景、位置和左侧结构；
2. 再识别 pattern 是否真的成立；
3. 最后给出入场、结构止损、第一独立障碍、R/R 和 no-trade 分支。

“高胜率”在本项目中不是固定百分比，也不是看到标签就下单。每个 pattern 都必须经过背景、位置、信号 K、触发、空间、事件和失效条件的共同审计。

## 当前核心范围

| 顺序 | Pattern 目录 | 当前定位 |
| --- | --- | --- |
| 1 | [`H1/L1 第一次入场`](01_h1_l1_first_entry/README.md) | 强 A 腿后的第一次方向尝试；优先级低于 H2/L2，但必须实现 |
| 2 | [`H2/L2 第二次入场`](02_h2_l2_second_entry/README.md) | 当前最优先的趋势延续研究主线 |
| 3 | [`ABC 趋势延续`](03_abc_continuation/README.md) | A 腿、B 回调、C 恢复；区间中部不强行使用 |
| 4 | [`区间边缘二次入场`](04_range_edge_second_entry/README.md) | 区间顶部卖出、底部买入，以及失败突破后的二次机会 |
| 5 | [`失败突破与高潮`](05_failed_breakout_climax/README.md) | 失败接受、高潮后小反转/区间和 no-trade 分流 |
| 6 | [`突破回踩 / BOP`](06_breakout_pullback_bop/README.md) | 突破被接受后的回踩与新交易合同 |
| 7 | [`MTR 趋势反转`](07_mtr_reversal/README.md) | 高级形态；需要位置、结构破坏和第二次确认 |
| 8 | [`三推 / H3-L3 压力状态`](08_three_push_h3_l3/README.md) | 第三次测试的衰竭、扩张、区间重复测试和延续分流 |

## 独立体系主题

| 主题 | 目录 | 当前定位 |
| --- | --- | --- |
| VCP / Volatility Contraction Pattern（Minervini） | [`VCP / Minervini`](09_vcp_minervini/README.md) | 独立的强势股整理、连续收缩与 pivot 突破研究；不计入 Brooks 核心八个，不与 ABC/H-L/三推合并 |
| Final Flag / 最终旗形 | [`Final Flag`](10_final_flag/README.md) | 独立的趋势末端压缩与最后尝试分流；与普通旗形、MTR、BOP 和 VCP 分开 |
| Opening Reversal / 开盘反转 | [`Opening Reversal`](11_opening_reversal/README.md) | 独立的开盘第一波失败/接受与反向确认研究；与 BOP、区间边缘和普通 H/L 分开 |
| Channel / 紧通道、宽通道与状态切换 | [`Channel / 通道`](12_channel/README.md) | 独立的通道边界、紧/宽通道、扩张、突破接受与区间过渡研究；不把画线当成自动交易信号 |
| Inside Bar / 两根 K 线反转 | [`Inside Bar / 两根 K 线反转`](13_inside_bar_two_bar_reversal/README.md) | 独立区分严格内包、二内包/IOI、两根反转与 H/L 信号序列；不把小实体当成自动信号 |
| Triangle / 三角形与区间内区间 | [`Triangle / 三角形`](14_triangle_expanding_range/README.md) | 独立区分收缩三角形、扩张三角形、区间内区间、突破接受与失败；不把两点连线当成三角形 |
| Double Top / Double Bottom / 双顶双底 | [`Double Top / Double Bottom`](15_double_top_bottom/README.md) | 独立区分两次有分离测试、区间边缘、MTR、Final Flag 与普通延续；不把相近高低点自动当反转 |
| Head-and-Shoulders / Rounded / 头肩与圆顶圆底 | [`Head-and-Shoulders / Rounded`](16_head_shoulders_rounded/README.md) | 独立区分头肩、圆顶/圆底、复杂双顶双底、颈线接受与普通旗形；不把三个点自动当反转 |

## 基础视觉层

| 基础层 | 目录 | 当前定位 |
| --- | --- | --- |
| Support / Resistance / 支撑阻力 | [`Support / Resistance`](../foundations/01_support_resistance/README.md) | 所有 pattern 共用的位置、结构止损、首障碍与角色转换过滤；不是独立交易形态 |
| Measured Move / AB=CD / 磁铁目标 | [`Measured Move / targets`](../foundations/02_measured_move_targets/README.md) | 所有 pattern 共用的空间、第一独立障碍、目标层级和持仓管理；不是独立交易形态 |
| Late Trend Entry / 趋势后段过滤 | [`Late Trend Entry / 追价过滤`](../foundations/03_late_trend_entry_filter/README.md) | 所有 pattern 共用的时机、空间、高潮、突破接受和新增仓位过滤；不是独立交易形态 |
| Multi-timeframe Review / 多周期复核 | [`Multi-timeframe Review`](../foundations/04_multitimeframe_review/README.md) | 所有 pattern 共用的 Daily/4H/1H/15m 职责、确认、独立低周期合同和跳空重订；不是独立交易形态 |
| Event / Sector / Market Gate / 事件板块闸门 | [`Event / Sector / Market Gate`](../foundations/05_event_sector_market_gate/README.md) | 所有 pattern 共用的财报、重大事件、板块/大盘许可和订单重订前置过滤；不是独立交易形态 |
| Order / Risk Contracts / 订单风险合同 | [`Order / Risk Contracts`](../foundations/06_order_risk_contracts/README.md) | 所有 pattern 共用的 stop、limit、market-close、stop-limit、实际成交、结构止损和 R/R 语义；不是独立交易形态 |
| Market State / Context / 市场状态与父级背景 | [`Market State / Context`](../foundations/07_market_state_context/README.md) | 所有 pattern 共用的趋势/区间/边缘/过渡/高潮分类、second-leg trap 与突破接受后的状态重建；不是独立交易形态 |
| Leg Pressure / Signal Quality / 腿与信号 K 质量 | [`Leg Pressure / Signal Quality`](../foundations/08_leg_pressure_signal_quality/README.md) | 所有 pattern 共用的强 A、B 压力变化、setup/signal/trigger/follow-through 与 EMA/量价汇合；不是独立交易形态 |

## 统一研究字段

每个目录都按同一套视觉顺序研究：

```text
timeframe
parent_state / market_context
left_structure_and_location
directional_leg_or_range_edge
lineage_and_attempt_count
pattern_family / pattern_like_reason
signal_bar_and_trigger / follow_through
order_branch / actual_fill_or_open_skip
structural_stop / invalidation
first_independent_obstacle / rough_R_R
event_and_sector_context
final_state / failure_or_no_trade_reason
```

## 范围边界

- 这些目录是视觉研究和历史复核入口，不是量化扫描器，也不直接连接 Execution Agent。
- `research/` 根目录中的案例正文暂不搬迁；目录只负责导航和研究合同。
- Measured Move、AB=CD、EMA、缺口回补和 META 是位置、空间或汇合因素，不单独构成 pattern。
- VCP、Final Flag、Opening Reversal、Channel、Inside Bar 与 Triangle 已建立独立研究目录，但都处于 `visual-research / provisional`，不计入核心八个。三推虽然可以成为 MTR 的证据，但在这里作为独立 pattern 单独实现。

## 共同规则

先看背景和左侧，再看形态；先看第一独立障碍，再看 MM；强趋势不等于可以在趋势末端追价。统一背景见 [`docs/common_context.md`](../docs/common_context.md)，覆盖状态见 [`research/abc_pattern_coverage_audit_CN.md`](../research/abc_pattern_coverage_audit_CN.md)。

## 核心 pattern 交叉审计

八个目录的共存关系、切换条件、状态词汇和共同否决层见[`核心八个 Pattern 交叉一致性审计`](../research/core_pattern_cross_audit_CN.md)。使用时先判父级市场状态，再判结构/计数，最后判状态转换和交易合同；不要因为多个标签同时出现就重复计算优势。

订单语义和 R/R 的跨 pattern 规则见[`八个 Pattern 的订单合同与 R/R 审计`](../research/order_contract_cross_pattern_audit_CN.md)。

MTR 与三推/H3-L3 的边界复核见[`MTR 与三推/H3-L3 视觉边界复核`](../research/mtr_three_push_visual_boundary_audit_2026-08-24_CN.md)：三推是压力观察入口，MTR 需要控制权改变和反向二次确认。

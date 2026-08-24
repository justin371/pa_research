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
- Opening Reversal、通道、Inside Bar、三角形暂不列入当前主动实现队列；已有研究文件保留为参考，不继续扩展。VCP 与 Final Flag 已建立独立研究目录，但都处于 `visual-research / provisional`，不计入核心八个。三推虽然可以成为 MTR 的证据，但在这里作为独立 pattern 单独实现。

## 共同规则

先看背景和左侧，再看形态；先看第一独立障碍，再看 MM；强趋势不等于可以在趋势末端追价。统一背景见 [`docs/common_context.md`](../docs/common_context.md)，覆盖状态见 [`research/abc_pattern_coverage_audit_CN.md`](../research/abc_pattern_coverage_audit_CN.md)。

## 核心 pattern 交叉审计

八个目录的共存关系、切换条件、状态词汇和共同否决层见[`核心八个 Pattern 交叉一致性审计`](../research/core_pattern_cross_audit_CN.md)。使用时先判父级市场状态，再判结构/计数，最后判状态转换和交易合同；不要因为多个标签同时出现就重复计算优势。

订单语义和 R/R 的跨 pattern 规则见[`八个 Pattern 的订单合同与 R/R 审计`](../research/order_contract_cross_pattern_audit_CN.md)。

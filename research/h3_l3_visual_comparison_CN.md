# H3/L3 视觉比较：像不像、值不值得深入、什么时候不要交易

状态：`visual-research / not-production / no-new-positive / validated win-rate: not-computable`

这份比较不是评分表，也不是胜率统计。它的目的，是把完整图表上“看起来像 H3/L3”的几种不同情况放在一起，帮助视觉助手先做正确分类，再决定是否值得补低周期、订单和 R/R。

本表的结构化回填统一使用：

```text
lineage_status: same_lineage / reset / unclear / pending
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
direction: long / short / no_valid_direction
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
first_independent_obstacle:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

案例横向表的“当前状态”保留历史结论说明；它不等同于结构化字段，也不构成胜率统计分组。

## 案例横向对照

| 案例 | 视觉结构 | 第三次尝试/压力 | 反向触发 | 首障碍空间 | 当前状态 |
| --- | --- | --- | --- | --- | --- |
| KLAC `2025-03-17`–`03-26` | 熊旗内三次向上测试，第三推靠近主要阻力 | 第三推没有接受，随后空头扩张 | `03-25` 低点约 `71.16` 下方 sell stop；`03-26` 首根 15m 触发，无开盘跳空 | 粗略 `1.4–1.9R` 到 `66.6–65.1` | 当前最值得深入的 H3 研究候选；SOXX 顺势，`04-30` 财报过滤通过；仍受 A 腿重叠限制 |
| COIN `2024-01-04`–`01-09` | B 腿内三次上探，第三次回到 `161` 附近 | 第三次范围扩大，未见清楚效率衰竭 | `01-09` 15m 有向下反应，但 `01-10` 跳空改变成交 | `01-09` 触发下方最近支撑约 `0.25R` | provisional H3-like；C 类扩张/延续边界，valid_no_trade |
| NFLX `2024-08-05`–`09-26` | 强多头 A 后高位多次测试，外形接近三推顶部 | 测试超过三次且重叠多，不能冻结严格 H3；`09-03` 空头反应后仍有上方接受 | `09-06 10:15` 低周期跌破 `67.10`，无开盘跳过 | `66.54–65.98` 首支撑约 `0.1–0.25R`；`09-24` 高点越过顶部 | provisional three-push-top / valid_no_trade / later-structure-invalidated |
| XOM `2024-07-25`–`08-02` | 空头 A 后三次上探，第三次更高且范围扩张 | 第三推没有效率衰竭，偏 C 类扩张/延续 | `08-01` 低点下方 sell stop；`08-02` 跳空重订成交 | 原始约 `1R`，跳空后约 `0.7R` 到 `105.20` | provisional H3-like；valid_no_trade / event-context-pending |
| UBER `2024-07-19`–`07-26` | 强空头 A 后三次上探候选；`07-25` 再次抬高并扩大范围，计数变复杂 | `07-23` 可作 H3-like 观察；`07-25` 扩张削弱衰竭解释 | `07-25` 低点 `64.40` 下方 L2-like sell stop；`07-26` 15m 未从开盘跳过触发价，但触发后收回 | 左侧 `62.90–63.30`；相对结构止损约 `0.2–0.3R` | provisional H3-like / count-ambiguous / C-class boundary / valid_no_trade / earnings-filter-passed |
| NOW `2025-09-19`–`10-21` | 高位区域多次测试，外形接近 H3-like | `10-10` 扩张、`10-13` 恢复和重叠使 lineage 歧义；`10-17` 低周期触碰后无跟随 | `10-16` 低点约 `177.61` 下方 sell-stop 分支；`10-17 09:45` 触碰约 `177.59` 后收回 | 首障碍和事件状态未冻结；IGV/QQQ 同期走强 | pattern_like / provisional H3-like / count-ambiguous / low-cycle-touch-no-follow-through / sector-not-aligned / valid_no_trade |
| DELL `2025-10-24`–`11-04` | 向上推进后在 `165–166` 区域重复测试，外形接近 H3-like | `11-03` 高开摸高后回落；`10-28/29` 相邻使计数仍有歧义 | `11-03` 低点约 `158.41` 下方 sell-stop；`11-04` 开盘约 `154.06` 跳过原触发 | 原价分支需重订；开盘重订后约 `147.8–145.4` 首支撑拥挤 | pattern_like / opening-skip / gap-reprice-geometry-boundary / valid_no_trade |
| TSLA `2026-05-19`–`06-26` | 三个下探逐步下移，间距收窄，第三次落在支撑 | 有衰竭和支撑反应，但反转级别有限 | 反弹触发和跟随存在 | 约 `0.63–0.83R` 到 `385.2–387.8` | B 类短反应；日线新仓 `valid_no_trade` |
| ANET `2024-05-16`–`06-10` | 三次下探候选，第三次靠近支撑 | 第二推明显扩张，第三推只局部减速 | 没有足够清楚的反向订单证据 | 支撑靠近 | C 类延续/高潮边界，不确认楔形 |
| ASML `2025-05-23`–`06-11` | 下沿两次测试，随后区间重叠和向上扩张 | 没有第三次同级别衰竭推进 | 不存在可冻结的 H3/L3 反向触发 | 未冻结 | `not_h3_l3 / range-transition` |
| TSLA `2025-03-07`–`03-10` | 空头延续中的第三次下探 | 第三推加速、波动扩张，不是减弱 | 不能因为 L3 反向做多 | 结果附近有支撑，但不能倒灌 | C 类延续/卖出高潮反例 |
| TSLA `2026-03-25`–`03-30` | L2 后有新反弹，再出现 provisional L3 | 低开和下压更像延续，没有两项明确衰竭 | 低周期触发可审计 | 约 `1.0–1.1R`，但延续风险高 | provisional L3，不是楔形反转 |

## 复核卡字段回填审计

以下把新复核卡的字段回填到五个已有案例。这里验证的是分类能力，不是重新计算胜率或建立评分器。

| 案例 | `lineage_status` | 第三推效率 / `third_push_state` | 位置 | `first_reverse` | `second_confirmation` | 复核结果 |
| --- | --- | --- | --- | --- | --- | --- |
| KLAC `2025-03-17–03-26` | `same_lineage` | 效率下降、第三推未获接受，随后空头跟随；`exhaustion_candidate` | 熊旗顶部 / 主要阻力 | `structural_break` | `yes` | 字段能表达“形态正向但仍需首障碍/R/R”的候选 |
| TSLA `2026-05-19–06-26` | `unclear` | 推进间距收窄，第三推后出现反弹，但级别有限；`exhaustion_candidate` | 左侧支撑汇合 | `touch` | `no` | 字段阻止把支撑反应升级成主要反转 |
| ANET `2024-05-16–06-10` | `pending` | 第二推扩张，第三推只在支撑处局部减速；`continuation_or_climax` | 支撑区，但事件/放量边界存在 | `pending` | `pending` | 字段保留“局部减速”但否决楔形反转升级 |
| XOM `2024-07-25–08-02` | `pending` | 第三推抬高并扩大范围，压力没有递减；`continuation_or_climax` | 高位修正 / 左侧阻力附近 | `touch` | `no` | 字段把第三推扩张与订单重订分开处理 |
| ASML `2025-05-23–06-11` | `reset` | 重叠区间和边界测试，不是三次同级别推进；`range_repeat_test` | 区间下沿 | `none` | `no` | 字段把旧 L3 标签降级为区间/过渡逻辑 |

### 回填结论

1. `same_lineage` 和 `third_push_efficiency` 能把 KLAC 与 ANET/XOM 的“第三次但性质不同”分开；
2. `first_reverse`、`second_confirmation` 与 `first_independent_obstacle` 分栏，能把 TSLA 的短线反应与可交易反转分开；
3. `not_h3_l3` 对 ASML 这类旧标签/区间误读是必要的，不能强迫所有三段波动进入 H3/L3；
4. 字段目前没有发现需要增加的必填项；事件/跳空、首障碍和 R/R 继续沿用订单协议的独立字段。

## 从这些图中暂时得到的视觉共同点

### 1. 先确认“同一组尝试”，再数到三

H3/L3 不能由三个相邻高点或低点自动生成。至少要确认：

- 三次尝试属于同一高周期背景和同一回调/修正；
- 每次尝试之间有足够的反向反应或停顿，不能只是连续跟随 K 线；
- 计数没有在区间中部、C 腿已经启动或新的父级腿出现后继续沿用。

### 2. 第三推的关键不是“第三”，而是压力如何变化

目前看到三种压力状态：

- **衰竭型**：推进效率降低、跟随变弱、位置接近主要阻力/支撑，并出现反向触发；KLAC 是当前候选。
- **延续型**：第三推实体扩大、收盘更靠极端、跟随增强；TSLA `2025-03-07/10` 和 XOM `2024-07-25/30/31` 都属于这一类边界。
- **区间型**：多次测试同一边界，价格重叠并在边界之间来回；ASML 属于这一类。

因此“三推”只是观察入口，压力状态决定下一步是反转候选、延续候选，还是区间交易逻辑。

### 3. 反向触发和首障碍共同决定能不能深入

即使形态看起来像三推，也要分开问：

1. 有没有当时可见的反向信号 K 和下一步确认？
2. 结构止损是否放在 thesis 失效位置，而不是人为压窄？
3. 触发前最近的支撑/阻力是否给出真实空间？

TSLA `2026-05-19`–`06-26` 有反向反应但首障碍太近，所以是 `valid_no_trade`；XOM 的空头反应方向清楚，但第三推扩张、跳空成交和首支撑空间不足，使它仍是 `valid_no_trade`；KLAC 的下方结构空间更宽，才进入正向研究队列。

NOW 补充了另一种边界：高位区域的多次测试可能在视觉上像 H3，但若低周期只是触碰触发位、没有跟随，且板块方向反向，就不能升级为可交易候选。

DELL 补充了订单层面的边界：形态判断可以保留为 `pattern_like`，但次日开盘跳过原触发后，原订单不算成交；重订价格必须重新面对首支撑和结构止损。

## 当前视觉助手的暂行分流

```text
完整图表
  → 同一背景/同一修正？
      否 → 区间、过渡或新父级腿；不强行 H3/L3
      是
        → 三次有意义尝试？
            否 → 普通 H1/H2/L1/L2 或连续腿
            是
              → 压力递减且有位置？
                  否 → 延续/高潮候选
                  是
                    → 反向触发 + 首障碍有空间？
                        否 → pattern_like / valid_no_trade
                        是 → research_positive_conditional
```

这是视觉复核顺序，不是量化评分器。用户当前要求的是先把像样的图筛出来，因此允许先记录粗略候选；只有进入 `research_positive_conditional` 后，才值得补 15m、事件、订单成交和 R/R。表中案例状态是历史结论的说明文字；新记录必须使用 canonical 字段，不能把 `pattern_like`、`valid_no_trade` 或后续盈利当作胜率分母。

## 当前边界

- KLAC 不是已验证胜率样本，仍受 A 腿重叠、其他新闻风险和低周期成交细节限制；财报前三日过滤已通过。
- ANET、ASML 和 TSLA 的反例不能被删除；它们是防止视觉助手把“有三段”误认为“有三推反转”的必要训练材料。
- XOM `2024-07-18`–`08-02` 是“第三推更强 + L1-like 反应 + 跳空重订订单”的边界，不能因后续空头腿而倒灌成衰竭正例。
- NOW `2025-09-19`–`10-21` 是“同高区域反复测试 + 低周期触碰无跟随 + 板块不一致”的边界，不能把触发触碰写成确认。
- DELL `2025-10-24`–`11-04` 是“高位测试像 H3 + 开盘跳过原触发 + 重订后空间恶化”的边界，不能用事后路径替代原始订单成交。
- 不把 H3/L3 写成固定三推楔形公式，不把 MM、EMA 或后续盈利当作入场证据。
- 这份比较只服务 PA Research 的视觉筛选和人工决策，暂不交给 Codex Trading。

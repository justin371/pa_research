# 失败突破与高潮反转：专项视觉证据审计（2026-08-24）

日期：2026-08-24  
状态：`visual-research / conditional / no-new-positive / not-statistical`

## 1. 本轮要解决的问题

“失败突破”和“高潮反转”经常在图上同时出现，但它们不是同一件事：

- **失败突破**先有一个决策时已经存在的支撑、阻力、区间边缘或角色转换位，价格越过后没有被接受，重新回到原来的价格一侧；
- **高潮**先描述原趋势后段的扩张、加速、跳空或大实体，说明原方向走得很远，之后可能小反转、进入区间，也可能继续延伸；
- **高潮反转候选**还需要第一反向结构、第二次确认、结构止损和首障碍空间，不能由一根大反向 K 自动升级。

本轮重点不是再收集“后来反转了”的图，而是按决策时点审计状态：测试、失败候选、确认失败、小反转/区间、MTR 候选、BOP 接受和延续/高潮必须分开。

## 2. 最小状态机

```text
事前边界 / 趋势极端
    -> 越过或扩张
    -> 收盘接受？
       ├─ 是 + 跟随       -> continuation / BOP acceptance
       └─ 否或不清楚
          -> 回到原侧？
             ├─ 否         -> test / observation-only
             └─ 是
                -> 第一反向破坏局部结构？
                   ├─ 否     -> small-reversal-or-range
                   └─ 是
                      -> 第二次确认 + 首障碍空间？
                         ├─ 否 -> reversal-attempt / valid-no-trade
                         └─ 是 -> MTR-candidate / conditional contract
```

“没有被接受”不是“已经确认失败”。至少要看到收回原侧、反向跟随或下一次尝试再次被边界拒绝；盘中影线、单根小 K 和事后盈利都不能单独完成确认。

## 3. 统一审计字段

每个候选只冻结以下字段，先于最终结果：

```text
contract_scope: historical_context_only
primary_pattern: RFB / MTR / other
direction: long / short / no_valid_direction
preexisting_boundary:
parent_state: open_trend / mature_range / channel / transition
break_or_climax_attempt:
close_acceptance: accepted / rejected / unclear
reentry_to_original_side:
first_reverse_structure:
second_confirmation:
order_branch: stop_confirmation / limit_retest / market_close / observation_only
branch_role: reverse_stop / role_reversal_retest / gap_reprice / management
actual_fill_or_reprice:
structural_stop:
first_independent_obstacle:
rough_R_R:
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
event_context:
event_bucket:
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
```

如果父级已经是成熟区间，优先使用区间上沿/下沿和 second-leg trap 逻辑；不能把区间内部的反向运动强行改成开放趋势中的 MTR。若突破被强收盘接受，旧的失败突破或反转合同必须结束，改为 BOP 新合同。

## 4. 多空案例对照

| 案例 | 决策时可见的状态 | 订单、止损与首障碍 | 当前裁决 |
| --- | --- | --- | --- |
| [`TSLA 2024-03-04–03-14`](tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | 区间上沿失败后出现强空头 A；L1 失败，L2 形成更清楚的反向确认 | `172.41` 下方 sell-stop；结构止损约 `182.87` 上方；左侧支撑 `152.37–153.75`，静态约 `1.6R–1.9R`；但后续先破结构止损 | `failed-breakout / MTR-candidate / process-stop-first`；最接近条件样本，但不是过程正例 |
| [`RBLX 2024-03-18–04-05`](rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md) | 父级是宽区间；`04-04` 开盘上冲越过前高后收回，开盘多头方向未被接受 | Buy-stop 被开盘越过需重订；区间结构止损约 `35.79` 下方；先看区间中部 `37.3–37.8`，不是远端 MM | `failed-breakout-candidate / range-edge-reaction / valid-no-trade`；信号 K 和事件过滤未通过 |
| [`TSLA 2025-03-07–03-10`](tsla_range_after_sell_climax_2025-03-11_2025-05-13.md) | 连续强下跌后卖出高潮，低点与 MM/左侧支撑重叠；第一反应是卖压耗尽和平衡 | 高潮末端不追空、不直接抄底；先看 `214–230` 下沿和后续区间，目标顺序为中线/边缘 | `climax -> small-reversal-or-range`；不是 MTR 正例 |
| [`COST 2024-07-11–07-18`](cost_bearish_abc_climax_boundary_2024-07-11_2024-07-18.md) | 上涨末端出现巨大空头反转 K，属于高潮型强 A；随后 L1-like 下破 | 触发约 `832.3` 下方，结构止损约 `847.4` 上方；首支撑 `828–834` 贴近触发，明显不足 `1R`；事件仍待核验 | `strong-A-climax-boundary / valid-no-trade`；强 A 不等于有交易空间 |
| [`TSLA 2025-09-08–09-12`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | `09-08`–`09-10` 阻力下影线越过但收盘未接受；`09-11` 强收盘越过并由 15m 跟随 | 突破前空头仅是观察/失败候选；接受后必须重建 BOP 合同，不能继续沿用反向止损 | `failed-thesis -> BOP-acceptance`；最清楚的失效状态切换样本 |
| [`XOM 2024-07-18–08-02`](xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md) | 空头 A 后上探第三次反而扩大，原方向压力没有衰竭确认 | `08-02` 开盘改变原 sell-stop；结构止损约 `111.43–111.60`，首支撑约 `105.20`，重订后约 `0.7R` | `continuation-or-climax / gap-reprice / valid-no-trade`；不是失败突破正例 |
| [`COIN 2024-01-02–01-10`](coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md) | 强 A 带跳空，第三次上探范围扩大；开盘反向反应存在但不是逐步减弱 | 日线首支撑约 `0.25R`，低周期约 `0.5R`；`01-10` 开盘越过原 L2 触发，不能假设原价成交 | `opening-reaction / expansion-boundary / valid-no-trade` |
| [`UBER 2024-07-17–07-26`](uber_bearish_h3_l2_first_support_boundary_2024-07-17_2024-07-26.md) | 三次上探后更高、更宽，属于扩张而不是高潮衰竭确认 | 财报过滤通过，但左侧首支撑仅约 `0.2R–0.3R`；原触发没有被开盘跳过 | `H3-like / expansion-boundary / valid-no-trade` |

## 5. 两个最接近失败突破的案例

### 5.1 TSLA 2024-03：失败突破与 MTR 候选重叠

在 `2024-03-04` 之前，价格已经在约 `190–205` 附近反复交易。强空头 A 说明上沿没有被接受；随后 `03-07`–`03-11` 的反弹没有收复 `182.87`，`03-12` 的第一次下破失败，`03-13` 的 L2-like 下破提供了更清楚的反向确认。

这段满足“位置 + 失败 + 第二次确认 + 静态空间”的研究条件，因此可以保留为 `MTR-candidate`。但过程审计改变了结论：`03-26` 反弹到约 `184.25`，先越过结构止损，之后才到达 `152.37–153.75` 左侧支撑。也就是说，方向和静态 R/R 都不能代替路径顺序。

可复用结论：

- 失败突破可以提供反向研究背景，但不自动提供过程正例；
- 结构止损必须按母级反转结构放置，不能为了躲过后续波动把止损事后放宽；
- “先到首障碍”必须是路径审计字段，不能只记最终是否到达；
- 区间上沿的失败和开放趋势中段的趋势反转不能合并成一个胜率类别。

### 5.2 RBLX 2024-04：开盘失败但父级区间优先

`2024-03-18`–`03-28` 的上涨发生在约 `35.8–39.0` 的宽区间内。`04-01`–`04-03` 回到区间下沿和前面上涨起点，`04-04` 开盘越过 `04-03` 高点后冲高回落，收盘接近日内低位。

这不是一个干净的开放趋势 H1，也不是可以直接买入的失败突破反向正例。它首先是区间下沿/内部的开盘反应：

- Buy-stop 被开盘越过，不能按理想触发价记账；
- 收盘质量差，盘中冲高不能覆盖反转 K 形态；
- 区间中部很快成为第一磁铁，宽结构止损使空间不足；
- `04-05` 的恢复是后来信息，不能回写 `04-04` 已经是优质多头信号。

因此，RBLX 更适合训练“失败突破候选 + 父级区间优先 + 观望”的视觉分流，而不是训练反向下单。

## 6. 高潮不是自动反转：三类边界

### 6.1 高潮后先进入区间

TSLA `2025-03-07`–`03-10` 说明，强下跌到达 `220–224` 支撑/MM 后，第一合理预期是卖压减弱、反弹和平衡。之后的 `2025-04-22` 必须按区间下沿反应处理，不能把区间内部上涨倒灌成旧 ABC 的第二腿。高潮的第一反向运动通常只支持小反转或区间假设。

### 6.2 高潮型 A 后形态像，但首障碍否决

COST `2024-07-11` 的强空头反转 K 和后续 L1-like 下破方向都很清楚，但首支撑在触发区附近。这里的问题不是看不出空头，而是订单几何不支持新仓。更远的支撑或 MM 不能拯救首障碍不足的合同。

### 6.3 第三推扩张或突破接受

XOM、COIN、UBER 的第三次测试变宽、变快，说明原方向或反向压力仍有控制，不应写成逐步衰竭。TSLA `2025-09-11` 则更直接：阻力下的失败候选被强收盘和 15m 跟随否定，必须切换 BOP。两种情况都要求停止坚持“它应该失败”的叙事。

## 7. 订单合同与风险分流

| 分支 | 何时允许研究 | 失效/限制 |
| --- | --- | --- |
| `reverse-stop` | 失败边界收回后，反向信号 K 外再确认 | 触发前原方向重新接受，或跳空越过触发，旧合同作废/重订 |
| `limit-retest` | 旧支撑转阻力、旧阻力转支撑、失败边界或缺口边缘事前明确 | 价格没有真实回测就没有成交；不能把当前价下方的 marketable limit 当作等待卖出 |
| `market-close` | 反向收盘强、局部结构已破坏、首障碍仍有空间 | 大 K 可能已经接近磁铁或被事件驱动；需要实际成交和新 R/R |
| `observation-only` | 首障碍拥挤、事件未清、只有一根反向 K、接受状态不清或父级为区间 | 观望是有效结论，不是漏掉交易 |

结构止损应放在失败边界/高潮极端/母级反转结构外；第一独立支撑或阻力必须先于 MM 检查。首障碍粗略不足约 `1R` 时，当前工作版默认 `valid_no_trade`；接近 `2R` 只是波段研究的较好空间，不是固定阈值或胜率承诺。

财报前三个交易日内按共同纪律不建立新仓。COST、RBLX、COIN 等案例的事件日历没有在本轮完成独立闭环，所以不能把它们当作事件干净正例；事件过滤通过也不能替代结构和空间审计。

## 8. 本轮结论

| 研究问题 | 当前结论 |
| --- | --- |
| 失败突破是否已有可用视觉语言？ | 有：事前边界 → 越过 → 未接受 → 回到原侧 → 反向跟随；但必须与测试和 BOP 接受分开。 |
| 高潮是否可以直接反向交易？ | 不可以。高潮后优先预期小反转/区间；只有第二次确认和空间齐全，才进入 MTR 候选。 |
| 是否有标准空头或多头过程正例？ | `no-new-positive`。TSLA 2024-03 最接近，但过程先破结构止损；RBLX、COST 首障碍/信号或事件否决；TSLA 2025-09 转 BOP。 |
| 当前最重要的边界是什么？ | “后续跌/涨得很远”不能修复原始 no-trade；“一根强反向 K”不能替代第二次确认；“突破越过”不能替代接受。 |

正式记录：

> `failed-breakout / climax-reversal / second-confirmation / first-obstacle-space-positive / process-complete`：**no-new-positive**。

这不表示该 pattern 没有价值。当前已经可以用它筛出：何时只观察、何时转区间、何时必须转 BOP、何时才值得进入 MTR 审计。下一轮只在出现新的方向、订单合同或状态边界时增加案例，不重复堆叠同质的高潮图。

## 9. 入口

- [`失败突破与高潮 pattern 目录`](../patterns/05_failed_breakout_climax/README.md)
- [`失败突破与高潮反转视觉框架`](failed_breakout_climax_visual_framework_CN.md)
- [`MTR 主要趋势反转专项视觉证据审计`](mtr_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`BOP 突破接受专项视觉证据审计`](bop_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`三推/H3-L3 专项视觉证据审计`](three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md)

研究边界：只更新 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

# 三推 / H3-L3：压力状态

状态：`visual-research / provisional / primary`

## 研究目的

把第三次推进或第三次测试单独研究，不把它自动叫成三推楔形反转，也不把 H3/L3 和 MTR 混为一谈。三推首先是一个视觉压力状态，之后才判断它是衰竭、扩张/高潮、区间重复测试，还是通道延续。

## 图表范围前置

三推或 H3/L3 命名前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录主要高点、主要低点、支撑阻力和 EMA20/50/200，再回到局部周期分隔三次推进。统一的母腿、lineage 和 reset 账本见[`H/L lineage 与三推状态视觉边界复核`](../../research/h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)；两年背景或主周期分隔缺失时不得冻结三推/H3/L3。

## 视觉定义

- 三次推进属于同一父级和同一结构 lineage；
- 每次推进的起点、终点、重叠、推进效率和收盘质量可在当时观察；
- 第三推位于主要支撑/阻力、区间边缘或通道边界时，反转解释更有意义；
- 第三推减弱、扩张和普通重复测试必须并列记录；
- 只有反向结构被接受并有第二次确认，才升级为 MTR 候选。

## 最小视觉协议

```text
parent_state: open_trend / mature_range / channel / transition
direction: bullish_attempts / bearish_attempts
timeframe:
lineage_status: same-lineage / reset / unclear
push_1: origin -> extreme / quality / separation
push_2: origin -> extreme / quality / separation
push_3: origin -> extreme / quality / separation
pressure_change: weakening / expanding / mixed / unknown
location_and_left_structure:
third_push_state: exhaustion / expansion-or-climax / range-repeat / channel-continuation
first_reverse: none / touch / structural-break
second_confirmation: yes / no / pending
order_branch: stop / limit-retest / market-close / observation-only
structural_stop:
first_obstacle:
rough_R_R: wide / borderline / insufficient / not-frozen
status: research-candidate / short-reaction / continuation / valid-no-trade
```

研究记录必须先填完 `lineage_status` 和 `third_push_state`，再讨论 H3/L3。若三次推进不能在当时被分开识别，标签写成 `not_h3_l3` 或 `new_lineage_pending`，不得用最终走势反推计数。

## 同一 lineage 的计数纪律

| 检查 | 仍可计入同一组三推 | 需要重置或降级 |
| --- | --- | --- |
| 父级背景 | 同一方向的趋势、同一回调或同一压力区 | 已进入成熟双向区间，或建立了新的母级 A 腿 |
| 推进分隔 | 每次之间有可见回调、停顿或失败尝试 | 只是连续三根同向 K 线，或没有可辨认的反应 |
| 位置关系 | 三次仍围绕同一主要高点/低点、通道边界或区间边缘 | 第一次边界已被接受，价格在外侧建立新结构 |
| 周期关系 | 在同一主周期内可复核，低周期只补触发 | 只能从更低周期事后拼出三段，主周期看不到 |
| 计数质量 | 前两次在当时已有意义，第三次不是噪音 | 前两次只是影线或局部微摆动，无法支持 H3/L3 |

H3/L3 描述的是第三次有意义的方向尝试；“三推”描述的是压力状态。两者可以重叠，但不能互相替代。

## 四种状态

| 状态 | 视觉特征 | 默认处理 |
| --- | --- | --- |
| `exhaustion-candidate` | 推进效率下降、位置重要、第三次尝试后反向压力出现 | 等反向 stop 或第二次确认；不要凭“三次”直接反向 |
| `expansion-or-climax` | 第三推更长、更快、实体扩大或跳空 | 优先考虑趋势延续/高潮后区间；不把扩张误叫衰竭 |
| `range-retest` | 三次测试落在双向区间边缘，方向没有持续接受 | 切换区间逻辑，边缘二次入场优先，中部观望 |
| `channel-continuation` | 推进沿宽/紧通道继续，边界尚未被破坏 | 顺势等待 H1/H2 或 L1/L2；不自动做 MTR |

### 状态分流的核心

- `exhaustion-candidate` 要求“效率变差 + 重要位置 + 第一反向压力”，不是只要求第三次出现；
- `expansion-or-climax` 看到实体扩大、跳空、收盘靠极值和跟随增强时，默认原方向仍有控制权；
- `range-repeat` 先使用区间上沿/下沿和 second-leg trap 逻辑，不能继承趋势中的 ABC 腿数；
- `channel-continuation` 先问通道是否仍被接受，通道内的第三次触碰不能自动升级为反转；
- 只有状态判断之后，才把 H3/L3 作为订单候选；没有第二次反向确认就保留为 `pattern_like` 或 `observation-only`。

## H3/L3、三推楔形和 MTR 的边界

| 观察对象 | 它回答的问题 | 不能自动推出的结论 |
| --- | --- | --- |
| H3/L3 | 当前回调或压力中的第三次有意义尝试在哪里？ | 不代表第三推减弱，也不代表马上反转 |
| 三推压力状态 | 三次推进的效率、重叠、收盘和接受是否变化？ | 不代表三推一定是楔形，扩张时可能是延续/高潮 |
| 三推楔形候选 | 位置和压力是否支持一次反向研究？ | 不代表已经改变主要趋势 |
| MTR | 原趋势控制权是否被结构性破坏并被反向接受？ | 不因三个点、双顶/双底或一根反向大 K 自动成立 |
| 区间边缘二次入场 | 价格是否在已知上沿/下沿反复失败？ | 不应使用开放趋势的 H3/L3 腿计数 |

如果三推之后原方向强收盘突破并持续接受，优先切换到 BOP；如果只在区间边缘刺破后回到区间，优先切换到区间边缘/失败突破；如果反向结构尚未被接受，只记录反转尝试。

## 反向确认、订单与风险

1. **第一反向**：只有影线或一根小反向 K 时，标记 `reversal-attempt-1`，不自动入场。
2. **Stop 分支**：默认等反向信号 K 外的 stop-confirmation；第三推极端重新被接受时，反向合同失效。
3. **Limit-retest 分支**：只有失败边界、颈线或角色转换区已明确，且价格确实回测时才成立；未回测不能假设成交。
4. **第二次确认**：第一次反向后有小回调/失败，再次形成反向 H1/H2-like 或 L1/L2-like，并得到跟随，才可升级为完整研究合同。
5. **结构止损**：看空放在第三推/主要测试高点外，看多放在第三推/主要测试低点外；不能用单根信号 K 的窄止损掩盖母级风险。
6. **首障碍**：先看最近独立左侧支撑/阻力、区间中线、通道边界和角色转换区，再看 MM；首障碍不足约 `1R` 时记录 `valid-no-trade`。
7. **事件与跳空**：财报窗口、跳空改变触发价或实际成交后，重新审计风险；不能沿用理想价格。

## 当前案例对照

| 案例 | 视觉分类 | 当前结论 |
| --- | --- | --- |
| [`KLAC 2025-03-12–03-28`](../../research/klac_h3_bear_flag_case_2025-03-12_2025-03-28.md) | H3-like 熊旗顶部，第三推受阻后有空头接受 | 条件性研究正例；仍需把首阻力、结构止损和过程触发分开记录 |
| [`TSLA 2025-03-07–03-10`](../../research/tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md) | L3 扩张/卖出高潮 | 说明第三推可以更强；不能把 L3 自动叫成楔形反转 |
| [`TSLA 2026-05-19–06-26`](../../research/h3_l3_research_gate_CN.md) | 三次低点收窄、支撑反应 | 只能作为短线反应候选；首障碍拥挤，不升级为日线反转交易 |
| [`XOM 2024-07-18–08-02`](../../research/xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md) | 第三推扩张/高潮边界 | 原方向压力仍强，跳空后需要重订订单；valid-no-trade |
| [`UBER 2024-07-17–07-26`](../../research/uber_bearish_h3_l2_first_support_boundary_2024-07-17_2024-07-26.md) | 三次上探后更高、更宽，第三推扩张 | 财报过滤通过但首支撑仅约 0.2R–0.3R；H3-like / valid-no-trade |
| [`ANET 2024-05-16–06-10`](../../research/anet_h3_l3_case_study_2024-05-16_2024-06-10.md) | 第二推扩张，第三次在支撑处减速 | 事件/跳空未闭环；不是逐推减弱的标准 L3 |
| [`ASML 2025-05-19–06-13`](../../research/asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md) | 区间重复测试 | 重置趋势腿计数，使用区间/过渡逻辑 |
| [`NFLX 2024-08-05–09-26`](../../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | 高位多次测试、超过三次且首障碍拥挤 | 形态像但路径不值得交易；不能用后续顶部反推第三推 |

## 当前目标验收

- 能说明三次推进为什么属于同一 lineage，或明确记录为什么必须重置；
- 能把衰竭、扩张/高潮、区间重复测试和通道延续分开；
- 能区分 H3/L3 计数、三推压力、三推楔形候选和 MTR；
- 能记录第一反向、第二次确认、stop/limit-retest、结构止损、第一障碍和粗略 R/R；
- 至少保留一个条件性正例、一个扩张反例、一个区间/通道边界和一个首障碍否决样本；
- 明确三推/H3-L3 仍是视觉研究层，不进入量化扫描器、Codex Trading 或 Execution Agent。

## H3/L3 边界

- H3/L3 是第三次方向尝试，不等同于“三推楔形”；
- 三推可以是 H3/L3 的一个形状来源，但计数重置、嵌套周期和区间状态必须单独说明；
- 三推反转需要位置、衰竭/失败证据、第二次确认和首障碍空间；
- 如果第三推是强扩张并被接受，默认不是反转信号。

## 与 MTR 的关系

三推回答“第三次推进的压力状态是什么”；MTR 回答“趋势控制权是否已经改变”。三推可以作为 MTR 的证据，但没有结构破坏和接受，三推只停留在 `pattern_like` 或 `observation-only`。

## 现有入口

- [`三推/H3-L3 压力状态框架`](../../research/three_push_pressure_state_framework_CN.md)
- [`H3/L3 范围与计数`](../../research/abc_h1_h2_h3_l1_l2_l3_scope_CN.md)
- [`TSLA H3/L3 研究闸门`](../../research/h3_l3_research_gate_CN.md)
- [`NFLX 三推顶部边界`](../../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)
- [`XOM 三推扩张边界`](../../research/xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md)
- [`MTR 与三推证据缺口审计`](../../research/mtr_three_push_evidence_gap_audit_2026-08-23_CN.md)：BKNG/PM 最接近 L3 衰竭但被首障碍否决；本轮没有新增合格 L3 正例。
- [`三推/H3-L3 专项视觉证据审计`](../../research/three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md)：KLAC 保留为唯一 H3 条件候选；L3 为 `no-new-positive`，扩张、区间重复和通道延续分别记录。

本轮专项审计的工作结论是：三推/H3-L3 的视觉分流已经可用，但反向交易仍须通过第二次确认、结构止损和首障碍空间审计；不能因为第三推数量到三次就自动获得反向授权。

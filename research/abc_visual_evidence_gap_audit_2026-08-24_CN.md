# ABC 趋势延续：专项视觉证据审计（2026-08-24）

日期：2026-08-24  
状态：`visual-research / conditional / visual-workable / not-statistical`

## 1. 本轮结论先行

ABC 的视觉研究工作版可以在人工完整图表和既定边界内使用，但必须把“形态覆盖”和“普通无事件正向基准”分开：

- **空头**：NFLX `2025-03-28` 是无缺口、强 A、深但后段受控 B 后的 L1 条件候选；TSM `2025-03-26` 是缺口后重订合同的条件候选；
- **多头**：KLAC `2025-06-02/03`、CRWD `2024-10-02` 提供支撑/深 B 后段稳定的 H2 条件覆盖，但首阻力和事件/事故背景仍限制可迁移性；
- **边界**：TSLA `2025-03`、QCOM `2025-02`、RBLX `2024-04` 说明区间、过渡或重叠多时必须重置 ABC；NVDA、LRCX、NKE 等说明跳空会改变原订单合同；
- **目标**：MM/AB=CD 可以帮助找空间和目标层，但不能越过第一独立支撑/阻力，也不能单独授权入场。

因此当前最准确的状态是：**在人工完整图表、统一字段和停止条件下，ABC 的视觉判断已达到可复用的研究工作版；这不表示每张图都能准确识别，也不表示自动识别、规则验证或胜率成立。普通无事件、双向、首障碍宽裕且过程完整的“通用正例”仍不冻结为规则或胜率。**

## 2. 统一决策顺序

```text
完整背景/左侧
    -> parent_state: open_trend / range_edge / range_middle / transition
    -> A 腿方向性与跟随
    -> B 是受控回调，还是新趋势/区间
    -> B 后段压力是否收缩、位置是否有意义
    -> C 的 H1/H2 或 L1/L2 恢复
    -> 订单、结构止损、第一独立障碍
    -> MM/AB=CD 作为后续目标
```

顺序不能反过来。先看到目标或后续大行情，再倒推 A/B/C，会把区间摆动、高潮和跳空后的新合同误判成趋势延续。

### 2.1 A 腿：强不等于可交易

强 A 的视觉证据是方向性收盘、较少重叠、连续推进和跟随；单根大 K、跳空或财报重定价只能先标为 `strong-looking`，不能自动当成普通趋势 A。强 A 主要决定优先看 H1/L1，普通 A 或宽通道 A 更适合等待 H2/L2。

### 2.2 B 腿：深浅不是唯一变量

| B 状态 | 视觉描述 | 默认处理 |
| --- | --- | --- |
| `controlled-B` | 浅或时间整理，反向压力逐步收缩 | H1/L1 优先评估 |
| `deep-but-late-controlled-B` | 前段反向压力强，后段在结构位稳定，未破坏 A 起点 | H1/L1 降级，H2/L2 保留 |
| `uncontrolled-B` | 反向扩张、接受穿越关键结构，或父级变成区间/新趋势 | 旧 ABC 结束，重建状态 |

成交量缩小、EMA20/50 站稳、50% 回调和 META 汇合都可以加分，但不是任何一个 pattern 的单独必要条件。它们不能覆盖 B 已经失控或首障碍不足。

### 2.3 C 腿和 H/L 计数

C 是原方向恢复，不是“后面又涨/跌了几根 K”。第一次有意义的恢复可记 H1/L1；第一次失败后出现新的反向 B 和独立尝试，才讨论 H2/L2。C 展开、新母腿产生、B 被结构性接受或父级切换后，旧计数重置。

## 3. 多空案例对照

| 案例 | A/B/C 视觉 | 订单与首障碍 | 当前层级 |
| --- | --- | --- | --- |
| [`NFLX 2025-02-14–03-28`](nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md) | 方向性空头 A；深但后段受控 B；`03-28` 第一次空头恢复 | 无缺口；盘中刺破与收盘确认分开；结构止损约 `100.8–101.2`，首支撑 `90.10–88.75` 约 `1.4R–1.9R` | `research_positive_conditional / L1 / process-target-reached`；不能直接冻结 |
| [`TSM 2025-02-14–03-28`](tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) | 强空头 A；受控 B；`03-26` L1-like | 原 `177.22` stop 被开盘越过，旧 limit 未回测；重订约 `176.66` 后首支撑 `167.99–165.05` 约 `1.6R+` | `research_positive_conditional / gap-reprice-only`；不是原 stop 正例 |
| [`KLAC 2025-05-07–06-03`](klac_h2_case_study_2025-05-07_2025-06-03.md) | 多头强 A；支撑/EMA 附近深 B；第二次恢复为 H2-like | `06-02/03` 触发与结构止损已分；前高/目标层仍需优先审计 | 多头 H2 条件覆盖，不代表普通 H1 基准 |
| [`CRWD 2024-09-11–10-11`](crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md) | 强 A 后深 B，后段在支撑稳定；H2-like 恢复 | 低周期触发可分开；首阻力约 `1.5R–1.9R`，但不宽；事件/事故背景单列 | 多头深 B 条件候选 |
| [`TSLA 2025-08-06–08-22`](tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) | 多头 A/B/H1-H2-like 外形 | 位置与通道/前高阻力使日线合同拥挤；短线分支与波段分开 | `pattern_like / first-obstacle-boundary` |
| [`QCOM 2025-02-21–03-28`](qcom_bearish_abc_range_b_boundary_2025-02-21_2025-03-28.md) | A 后 B 变宽、均线反复穿越，父级向区间过渡 | 区间中部没有可靠首方向；不能拿后续下跌增加 L2 | `range-transition / count-reset / observation-only` |
| [`RBLX 2024-03-18–04-05`](rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md) | 局部 A/B/C 可画，但 B 回到 A 起点和区间下沿 | 开盘上冲失败，信号 K 质量差；目标先看中线而不是 MM | `range-edge / not-ABC-continuation / valid-no-trade` |
| [`TSLA 2025-03-11–05-13`](tsla_range_after_sell_climax_2025-03-11_2025-05-13.md) | 卖出高潮后宽区间；下沿到上沿是摆动 | `04-22` 不能叫趋势 H2；`05-08` 后才重建突破/新 lineage | `second-leg-trap-control / range` |
| [`LRCX 2024-07-10–07-24`](lrcx_bearish_abc_l1_gap_first_support_2024-07-10_2024-07-25.md) | 强空头 A、短 B、L1-like | `07-24` 开盘跳过原 stop；重订后首支撑约 `0.9R–1.1R`，边界 | `gap-reprice / first-support-borderline / no-trade` |

## 4. 条件正向样本与真正缺口

### 4.1 NFLX：无缺口空头 L1 条件样本

NFLX 的价值在于它补足了空头第一次入场的无缺口合同：A 腿方向性清楚，B 虽然深但没有回到 A 起点，后段反向压力没有继续扩张；`03-28` 的 L1-like 触发可以在低周期拆成“盘中刺破”和“收盘确认”。

它仍不是生产正例：第一根 15m 刺破后先回收，说明触发不是无风险；首障碍虽有 `1.4R–1.9R` 的粗略空间，但这只是静态过滤，不能代替路径和跨案例证据。

### 4.2 TSM：重订后的空头 L1 条件样本

TSM 说明小缺口会否决原 stop，但不一定否决整个 ABC thesis。如果计划事先允许接受缺口后重订，`176.66` 附近或 15m 确认可以是新合同；`177.22` 的旧 limit 没有回测，不能假设成交。重订后首支撑空间仍可研究，但它必须独立于原合同记录。

这条规则与用户的订单纪律一致：订单先于结果，成交价、止损和 R/R 都必须按实际状态重建。

### 4.3 KLAC/CRWD：多头深 B 后段稳定

KLAC 和 CRWD 共同说明深 B 不必自动否决多头 ABC：如果没有破坏 A 起点，且后段在结构支撑/EMA 附近稳定，H2-like 恢复仍可研究。但两者的首阻力、事件/事故和低周期触发都需要分栏，不能把深 B 直接写成高胜率。

## 5. MM、AB=CD 与 R/R

### 5.1 目标的顺序

入场前按以下顺序：

1. 结构止损和实际订单成交价；
2. 第一独立支撑/阻力或角色转换区；
3. 区间中线、缺口边缘或左侧磁铁；
4. 最后才是 MM、AB=CD、区间高度投影或更远目标。

同一价格簇里的前高、EMA、缺口边缘和 MM 不能重复计成多个独立优势。MM 到位可以是第一目标或停顿区，但不自动反转，也不能救回首障碍不足的入场。

### 5.2 路径审计

每个候选都要区分：

```text
static_RR_at_decision:
first_obstacle_reached_before_stop:
process_stop_first:
actual_fill_or_not_filled:
gap_reprice_or_original_contract:
later_MM_reached:
```

TSLA `2024-03` 与 NFLX 的对照最重要：前者静态空间可研究但过程先破结构止损，后者首支撑后来到达但仍只是条件候选。不能把两种路径混成“ABC 成功”。

## 6. ABC 订单分支

| 分支 | 何时研究 | 不能做什么 |
| --- | --- | --- |
| `same-contract-stop` | C 信号 K 外确认，父级结构和空间仍有效 | 不能用低周期窄止损替换母级结构止损 |
| `low-cycle-confirmation` | 低周期确认同一高周期 C | 不能把短线成交冒充日线合同 |
| `limit-retest` | 旧支撑/阻力、缺口或角色转换区真实回测 | 没回测就没有成交；不能把当前价下方的 marketable limit 当等待订单 |
| `reprice-after-gap` | 原触发被跳过，且事前允许按实际价格重建 | 不能保留原成交、原止损和原 R/R |
| `market-close` | C 收盘强、首障碍有空间且等待风险可接受 | 不能因大 K 很强就追入高潮 |
| `observation-only` | 区间、首障碍拥挤、事件/板块冲突、B 失控或计数不清 | 不能用后续方向正确把它改成合格交易 |

## 7. 本轮收口结论

| 研究问题 | 当前结论 |
| --- | --- |
| ABC 是否已经能用于视觉筛选？ | 在人工完整图表和证据字段可读时，可以按统一流程复核开放趋势、区间/过渡、A 强度、B 压力状态、C 的 H/L-like 恢复和首障碍；证据缺失时必须保留 `pending`/`observation_only`，不代表准确率或自动化能力。 |
| 是否有多空条件性覆盖？ | 有：NFLX/TSM 空头，KLAC/CRWD 多头；它们的订单合同和事件/空间条件不同。 |
| 是否有可直接冻结的通用高胜率规则？ | 没有。普通无事件、双向、首障碍宽裕、过程完整基准仍不足，保持 `conditional / not-statistical`。 |
| 最大误读风险是什么？ | 区间摆动当第二腿、深 B 自动否决、后续低点增加 L2、跳空沿用旧成交、MM 覆盖首障碍。 |

正式记录：

> `ABC / parent-clear / strong-A-or-justified-A / controlled-B / C-confirmed / first-obstacle-space-positive / process-complete`：**conditional coverage; no general freeze**。

ABC 的视觉语言已经足够支撑受限的后续筛图和人工决策研究；下一阶段只在出现新方向、新订单合同、新周期或新的状态边界时补案例，不再为了“彻底”而重复同质深审。它仍不是准确率测试、自动识别器或交易授权。

## 8. 入口

- [`ABC 趋势延续目录`](../patterns/03_abc_continuation/README.md)
- [`ABC 研究状态与工作边界`](abc_research_status_v0_3_CN.md)
- [`ABC / H1-H2 / L1-L2 视觉综合`](abc_visual_synthesis_v0_2_CN.md)
- [`H1/L1、H2/L2 与 ABC 证据缺口审计`](h1_h2_abc_evidence_gap_audit_2026-08-23_CN.md)
- [`Measured Move、磁铁与目标层级框架`](measured_move_magnet_target_hierarchy_CN.md)

研究边界：只更新 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

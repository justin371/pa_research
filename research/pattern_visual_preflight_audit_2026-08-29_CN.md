# PA Research Pattern 视觉复核前置证据审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 目的与范围

本次审计检查 16 个 pattern README 是否把完整图表的前置证据写清楚：至少两年的 Daily 左侧背景、重要高点/低点、支撑阻力、EMA20/50/200、父级位置、适用路径下的 A/B 质量、第一独立障碍和缺证据时的 `pending`/`observation_only` 边界。这里的“适用路径”很重要：强 A 是开放趋势 H1/L1 与延续研究的优先条件，不是所有 pattern 或区间边缘三推的统一硬要求。

本次只修复 PA Research 的视觉复核入口和文档一致性。不下载行情、不查看新图、不运行正式回放、不增加样本、不改变 pattern 定义或 engine 有效语义。`validated win-rate: not-computable` 和现有 `no-new-positive` 结论保持不变。

`scope_boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。本审计不把视觉前置证据变成自动筛选器或交易授权。

Canonical shorthand：`daily_context_window: >=2y / <2y / unavailable`；`major_highs`；`major_lows`；`daily_ema20_50_200`；`A_quality: strong`；`B_quality: controlled`；`first_independent_obstacle`。

## 1. 审计发现与修复

统一使用的[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)已经定义了完整字段：`daily_context_window`、`major_highs`、`major_lows`、`support_zones`、`resistance_zones`、`daily_ema20_50_200`、EMA 斜率、H/L EMA 方向闸门、META 区域和 `left_context_review`。

在本次修复前，01、02、08 号目录已经明确引用两年 Daily 前置；03–07 号核心目录和 09–16 号独立主题主要描述各自形态，未在本目录入口统一提醒左侧背景。现在这些目录均新增“共同图表范围前置”，直接引用同一张复核卡，并明确：

- 先看同一标的至少两年的 Daily 左侧（若窗口支持），记录重要高点/低点、支撑阻力、前高/前低、EMA20/50/200、父级状态和第一独立障碍；
- 对开放趋势 ABC/H-L、需要原趋势压力背景的 MTR 等适用路径检查 A/B 质量：强 A 优先服务 H1/L1，受控 B 支持延续研究；H2/L2 可以承接普通 A 后的第二次有意义尝试，但不能用编号挽救区间中部或失控回调。成熟区间边缘三推是明确例外，允许普通/偏弱 A，改查已确认的上沿/下沿、第三推位置、反向证据和空间；
- BOP、失败突破和独立主题按各自的突破接受/失败或结构定义审查；VCP、Final Flag、Opening Reversal、Channel、Inside Bar、Triangle、Double Top/Bottom、Head & Shoulders/Rounded 等只把 A/B 当背景对照，不强行添加 ABC/H-L 计数；
- 涉及 H1/H2/L1/L2 时，Daily EMA20/50 必须与方向一致；走平、反向、不可见或左侧/位置/空间证据不足时，保持 `pending`/`observation_only`，不把局部外形升级为可交易候选。

01、02、08 保留原有更具体的“图表范围前置”段落，没有重复添加一段同义文本；其内容已经覆盖本次最低要求。

## 2. 16 个入口的最低证据状态

| # | 目录入口 | 文档层级 | 当前索引状态 | 最低视觉前置 |
| --- | --- | --- | --- | --- |
| 01 | [`H1/L1 第一次入场`](../patterns/01_h1_l1_first_entry/README.md) | 核心八个 | `adopted / provisional`；普通开放趋势纯净基准 `no-new-positive` | 两年 Daily、重要高低点、EMA20/50/200、强 A→H1/L1 优先、受控 B、首障碍 |
| 02 | [`H2/L2 第二次入场`](../patterns/02_h2_l2_second_entry/README.md) | 核心八个 | `adopted / provisional`；条件性覆盖、尚未通用冻结 | 两年 Daily、lineage、EMA20/50/200、A/B 质量、第一次失败/不足、首障碍 |
| 03 | [`ABC 趋势延续`](../patterns/03_abc_continuation/README.md) | 核心八个 | `adopted / provisional`；`visual-workable / no-general-freeze` | 两年 Daily、A/B/C、EMA20/50/200、父级和空间 |
| 04 | [`交易区间边缘二次入场`](../patterns/04_range_edge_second_entry/README.md) | 核心八个 | `adopted / provisional / no-new-positive` | 两年 Daily、上下沿、重要高低点、EMA20/50/200、首磁铁/首障碍 |
| 05 | [`失败突破与高潮`](../patterns/05_failed_breakout_climax/README.md) | 核心八个 | `adopted / provisional / no-new-positive` | 两年 Daily、失败边界、接受/失败和空间；若有原 A/B 则分开记录质量 |
| 06 | [`突破回踩 / BOP`](../patterns/06_breakout_pullback_bop/README.md) | 核心八个 | `adopted / provisional / no-new-positive` | 两年 Daily、突破对象、EMA20/50/200、接受/回踩和首障碍 |
| 07 | [`MTR 趋势反转`](../patterns/07_mtr_reversal/README.md) | 核心八个 | `adopted / provisional / no-new-positive` | 两年 Daily、成熟趋势极端、控制权变化、结构破坏/第二次确认和空间；原 A/B 仅作背景 |
| 08 | [`三推 / H3-L3 压力状态`](../patterns/08_three_push_h3_l3/README.md) | 核心八个 | `adopted / provisional / no-new-positive` | 两年 Daily、重要高低点、lineage、第三推位置和首障碍 |
| 09 | [`VCP / Minervini 独立主题`](../patterns/09_vcp_minervini/README.md) | 独立主题 | `research_only / provisional / no-new-positive` | 两年 Daily、趋势背景、EMA20/50/200、收缩 lineage、pivot 和空间 |
| 10 | [`Final Flag 独立主题`](../patterns/10_final_flag/README.md) | 独立主题 | `research_only / provisional / no-clean-positive-yet` | 两年 Daily、成熟趋势、末端位置和首障碍；若有 A/B 背景则分开记录质量 |
| 11 | [`Opening Reversal 独立主题`](../patterns/11_opening_reversal/README.md) | 独立主题 | `research_only / provisional / no-clean-positive-yet` | 两年 Daily、开盘前重要高低点、EMA20/50/200、磁铁和空间 |
| 12 | [`Channel 独立主题`](../patterns/12_channel/README.md) | 独立主题 | `research_only / provisional / no-clean-positive-yet` | 两年 Daily、通道父级、重要高低点、EMA20/50/200和边界空间 |
| 13 | [`Inside Bar / Two-Bar Reversal 独立主题`](../patterns/13_inside_bar_two_bar_reversal/README.md) | 独立主题 | `research_only / provisional / no-clean-positive-yet` | 两年 Daily、母级位置、EMA20/50/200、适用时的 A/B 背景和首障碍 |
| 14 | [`Triangle / Expanding Range 独立主题`](../patterns/14_triangle_expanding_range/README.md) | 独立主题 | `research_only / provisional / no-clean-positive-yet` | 两年 Daily、两侧边界、重要高低点、EMA20/50/200和空间 |
| 15 | [`Double Top/Bottom 独立主题`](../patterns/15_double_top_bottom/README.md) | 独立主题 | `research_only / provisional / no-new-positive` | 两年 Daily、两次分离测试、重要高低点、EMA20/50/200和首障碍 |
| 16 | [`Head & Shoulders / Rounded 独立主题`](../patterns/16_head_shoulders_rounded/README.md) | 独立主题 | `research_only / provisional / no-new-positive` | 两年 Daily、主要极端、颈线、EMA20/50/200和空间 |

这里的“当前索引状态”是研究导航语境，不是胜率或策略授权；独立主题仍不属于统一输出合同的核心主标签。

## 3. 强 A 与受控 B 的共同解释

对开放趋势 ABC/H1/L1 及需要原趋势压力背景的路径，强 A 是研究优先条件：通常表现为约 3–4 根连续同方向 Daily K 线、实体相对饱满、收盘靠近极值、重叠少并有跟随；跳空是加分项，不是必要条件。B 优先要求受控、后段压力收缩或在结构位置稳定；大实体反向扩张、接受性穿越关键结构或双向区间化时必须降级。H2/L2 可以承接普通 A 后的第二次有意义尝试，但仍需方向、lineage、位置、EMA 闸门和空间证据。

成熟交易区间边缘三推是明确例外：它不走这条“强 A → 受控 B”的趋势优先路径，A 腿可以普通、偏弱或重叠较多；最低前置是已确认的上沿/下沿、第三推到达边缘、反向拒绝/假突破回区间或信号 K，以及结构止损和首障碍空间。区间中部三推仍为观察。BOP、失败突破和其他独立主题使用各自的接受/失败或结构边界，不能从本段推导出强 A 硬闸门。

独立主题不因这段共同说明而获得 ABC/H-L 语义。它们可以用强 A/受控 B 判断父级质量，但 VCP 的 T1/T2/T3、Final Flag 的末端压缩、Opening Reversal 的开盘第一波、Channel 的边界、Inside Bar 的母 K、Triangle 的两侧测试、双顶/双底的分离测试和头肩/圆底的颈线仍分别按目录定义。

## 4. 结论与后续边界

- 16 个 pattern README 现在都明确引用同一视觉复核卡，并要求先完成左侧两年、重要高低点、EMA20/50/200、位置和空间复核；缺证据时不升级。
- `strong A` 提高开放趋势 H1/L1 或延续研究优先级；普通 A 仍可在证据完整时承接 H2/L2，成熟区间边缘三推则明确不要求强 A。A/B 质量不替代父级、事件、订单、结构止损和首障碍；独立主题不强行套 ABC/H-L 计数。
- `no-new-positive`、`no-clean-positive-yet` 和 `no-general-freeze` 仍是研究状态描述，不是胜率结论；`validated win-rate: not-computable`。
- 本次只更新 PA Research 文档/索引/测试：不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

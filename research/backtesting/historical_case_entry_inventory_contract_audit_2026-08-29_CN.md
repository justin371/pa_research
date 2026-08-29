# 矩阵外历史案例、候选筛选与专题入口合同审计（2026-08-29）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

```text
inventory_scope: historical_case_entry_inventory_only
matrix_coverage_basis: five aggregate matrices only
row_contract_source: linked_entry_file
row_contract_scope: per_entry
row_result_boundary: independent_replay_or_result_only
historical_alias_policy: display_only_until_mapped
```

## 1. 范围与发现

本轮只读取 PA Research checkout 的历史 Markdown、canonical schema、validator、回归测试和
回放 engine 接口；没有查询行情、查看新图、运行回放、增加样本、修改 CSV/engine，也没有
修改 Codex Trading、创建量化扫描器或连接 Execution Agent。这个文件是入口 inventory 和
合同边界审计，不是新案例、交易日志或结果报告。

“矩阵外”按以下五个聚合入口定义：

- [`核心八个 Pattern 代表性案例矩阵`](../core_pattern_case_matrix_CN.md)；
- [`ABC 决策矩阵`](../abc_decision_matrix_CN.md)；
- [`优先 Pattern 代表性视觉候选矩阵`](../priority_pattern_visual_candidate_matrix_2026-08-24_CN.md)；
- [`TSLA 三案例比较矩阵`](../tsla_abc_h1_h2_comparison_matrix.md)；
- [`TSLA 空头 ABC 案例比较矩阵`](../tsla_bearish_abc_comparison_matrix.md)。

以当前 checkout 中可识别的 42 个 ticker 前缀和日期命名记录为盘点集合，共有 66 个
ticker-like 历史 case 记录：31 个被上述矩阵直接链接，35 个没有被上述矩阵直接承载。
“没有被矩阵直接承载”不等于没有任何引用，也不等于它们是合格样本；它只说明需要一个
独立的历史入口来说明来源、字段完整度和不晋级边界。

盘点还发现一个具体的文档一致性问题：ADBE、CME、MDT、PM 四份较新的视觉筛选记录有
清楚的历史来源和研究结论，却没有自包含的 canonical 证据范围/状态块，容易被读者把
文件标题中的 `ABC`、`H1/H2-like`、`L1-like` 当成已闭合的主标签或订单合同。本轮只补了
这四份记录的最小历史边界；没有臆造缺失的 `primary_pattern`、`internal_label`、lineage、
精确止损、精确空间或成交结果。

## 2. 每个入口必须分开的 canonical 轴

下列是将来把某个历史入口提升为可复核逐案记录时的字段清单。本报告只记录“已存在、缺失
或故意未激活”，不从文件名、后续走势或矩阵行替某个案例补值。

| 轴 | canonical 字段 | 当前读取规则 |
| --- | --- | --- |
| 证据头 | `symbol`、`review_date`、`data_source`、`data_status`、`as_of_time`、`timezone`、`session_state`、`completed_bar_as_of`、`timeframes_seen`、`chart_scope` | 区分来源、截止时点、时区、session 和实际看过的周期；历史资料缺失时写 `unknown`/`unavailable`/`incomplete`，不写成实时 |
| 左侧前置 | `daily_context_window`、`major_high_low_review`、`ema20_50_200_review`、`daily_ema20_slope`、`daily_ema50_slope`、`h_l_ema_slope_gate` | 两年 Daily、重要高低点、EMA20/50/200 必须逐案判断；批次级完整图不能替代单案证据 |
| 结构解释 | `parent_state`、`direction`、`primary_pattern`、`internal_label`、`state_transition`、`lineage_status`、`lineage_id` | `direction` 不等于标题方向；stage-1 只保留 `pattern_candidate`，不激活主标签/内部计数；历史 case 未闭合时保留 pending/未分配 |
| 模式补充 | `secondary_context`、`a_leg_quality`、`b_leg_class`、`b_leg_location`、`range_edge_three_push`、`range_edge_side`、`third_push_state` | `strong-looking-A`、`deep-B`、`H1/H2-like`、`H3-like` 等是历史显示别名；不能越过 lineage、方向和首障碍闸门 |
| 订单 | `signal_bar`、`confirmation_bar`、`new_trigger`、`order_branch`、`branch_role`、`gap_policy`、`order_price_or_zone`、`actual_fill_or_open_skip` | 历史叙述中的 stop、opening-skip 或低周期穿越不是 broker/account fill；未冻结合同使用 `observation_only`、`fill_unknown` 或 `not_applicable` |
| 风险/空间 | `structural_stop`、`structural_invalidation`、`first_independent_obstacle`、`pre_entry_space_R`、`space_status`、`rough_R_R`、`target_layers` | 固定顺序是失效/止损 → 首独立障碍 → 入场前空间 → 粗略 R/R；区域、pending 和 unknown 不能伪装成数值合同 |
| 状态/交接 | `research_state`、`trade_state`、`gate_result`、`thesis_state`、`handoff_status` | `pattern_like`、`research_positive_conditional`、`valid_no_trade`、`observation_only` 各自有含义；没有交易授权或系统交接 |

## 3. 未被五个聚合矩阵直接承载的 35 个历史入口

下表的链接本身只是可追溯性修复。`primary_pattern`、`internal_label`、订单和空间是否闭合，
仍以每个入口自己的 canonical 记录为准；没有自包含合同的旧文件继续按历史叙述读取。

### 3.1 candidate / screen 入口（11 个）

| 入口 | 当前范围读取 | 保留的显示语义与限制 |
| --- | --- | --- |
| [`ADBE 空头 ABC/L1 视觉筛选`](../adbe_bearish_abc_l1_visual_screen_2026-01-12_2026-01-27.md) | `historical_context_only`；本轮补最小证据头；`direction=short`；lineage 和订单不冻结 | `ABC continuation`、`L1-like`、`strong-looking-A` 仍是历史显示；`research_positive_conditional` 不等于统计正例 |
| [`CME 空头 ABC/L1 视觉快筛`](../cme_bearish_abc_l1_visual_screen_2026-05-20_2026-06-17.md) | `historical_context_only`；本轮补最小证据头；`direction=short`；只看 Daily | `transition / range-to-bear` 和 `L1-like` 不激活主标签，首支撑拥挤保留为边界 |
| [`CRM 空头 ABC L1/L2 候选`](../crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md) | 原记录已有 `historical_context_only`，但只是候选范围 | `L1-low-cycle-confirmed` 与 `L2-count-pending` 不构成冻结合同 |
| [`MDT 多头 ABC/H2 视觉快筛`](../mdt_bullish_abc_h2_visual_screen_2025-05-23_2025-07-02.md) | `historical_context_only`；本轮补最小证据头；`direction=long`；只看 Daily | `ordinary A`、`H2-like`、过渡背景和首阻力仍是视觉对照，不是高质量正例 |
| [`META 多头 H1/H2 候选`](../meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md) | 原记录已有 `stage_1_fast_screen`；`direction=long`；主标签/内部标签不激活 | `nested-count-unclear`、`first-obstacle-crowded` 只服务快筛 |
| [`MSFT 空头 ABC L1/L2 候选`](../msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md) | 原记录已有 `stage_1_fast_screen`；`direction=short`；EMA/事件等保留 pending | `gap-trigger-boundary` 不等于已接受的普通订单 |
| [`NVDA 多头 ABC/H1 候选`](../nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md) | 原记录已有 `stage_1_fast_screen`；`direction=long`；主标签/内部标签不激活 | `gap-trigger-reprice` 仍是历史路径说明 |
| [`PM 多头 ABC/H1-H2 视觉筛选`](../pm_bullish_abc_h1_visual_screen_2026-01-05_2026-01-23.md) | `historical_context_only`；本轮补最小证据头；`direction=long`；首阻力 `valid_no_trade` | `H1/H2-like` 仍是计数候选；两份低周期订单分支不能混成真实成交 |
| [`SPY 多头 H1/H2 指数控制案例`](../spy_bullish_h1_h2_index_control_first_resistance_2025-07-07_2025-07-18.md) | 旧式历史筛选；缺自包含 canonical 证据头 | `index-control`、`count-pending` 和首阻力阻塞不能升级为个股样本 |
| [`TSLA 空头 ABC 候选筛选`](../tsla_bearish_abc_candidate_screen_2026-08-22.md) | 原记录已有 `historical_context_only`；`direction=short`；A 锚点歧义保留 | `pattern_like` 不能解决 A 终点、lineage 和 L1/L2 计数分支 |
| [`TSLA H1/H2 候选筛选`](../tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md) | 原记录已有 `historical_context_only`；`direction=long`；候选级不冻结订单 | 候选筛选、低周期分支和后续结果保持分开 |

ADBE、CME、MDT、PM 四个文件新增加的是 evidence/status boundary，不是四个新样本。其余
已有范围块的候选文件也没有因为被本 inventory 链接而改变 scope 或统计资格。

### 3.2 single case / boundary 入口（24 个）

这些文件的日期、标的、A/B/H-L/三推或事件/缺口事实继续保留，但它们原本没有完整的
自包含 canonical header。本轮不强行从自然语言重建缺失字段；需要重新使用时，应另立
逐案记录并在入场前封口。

| 入口 | 历史显示层分类 | 当前处理 |
| --- | --- | --- |
| [`AMZN 空头 ABC/L1 首支撑边界`](../amzn_bearish_abc_l1_no_gap_first_support_boundary_2024-09-23_2024-10-15.md) | ordinary/directional A、deep B、L1-like、首障碍边界 | legacy narrative；不自动赋 `primary_pattern`/订单 |
| [`AMZN 多头 H2 浅 B 边界`](../amzn_bullish_h2_shallow_b_boundary_2024-12-09_2024-12-11.md) | H2-like、浅 B、历史边界 | legacy narrative；空间和结果不回填 |
| [`ANET 空头 L2 事件边界`](../anet_bearish_l2_event_boundary_2024-02-12_2024-02-21.md) | L2、事件/方向边界 | legacy narrative；事件 provenance 不升级为普通样本 |
| [`ANET 多头 H2 视觉边界`](../anet_bullish_h2_visual_boundary_2023-11-15_2023-11-22.md) | H2-like、视觉 no-trade | legacy narrative；不从标题推断 EMA gate |
| [`ANET H3/L3 案例研究`](../anet_h3_l3_case_study_2024-05-16_2024-06-10.md) | 三推/H3-L3 边界 | legacy narrative；第三推别名不替代 `third_push_state` |
| [`BKNG 多头 H2 缺口触发边界`](../bkng_bullish_h2_gap_trigger_boundary_2024-06-12_2024-06-18.md) | gap trigger、H2、首障碍边界 | legacy narrative；原价触发和重订路径不合并 |
| [`COIN 空头 L1/L2 缺口边界`](../coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md) | L1/L2、opening-skip、事件边界 | legacy narrative；过程到达不等于胜负 |
| [`COST 多头 ABC/H2 视觉边界`](../cost_bullish_abc_h2_visual_boundary_2025-04-21_2025-05-16.md) | ordinary A、deep B、H1/H2-like、首障碍边界 | legacy narrative；不把 H2-like 直接送入回放 |
| [`DIS 空头 ABC/L1 opening-skip`](../dis_bearish_abc_l1_opening_skip_first_support_2024-07-16_2024-08-02.md) | gap-A、deep B、opening-skip、财报窗口 | legacy narrative；事件/缺口和订单分支分开 |
| [`JNJ 多头 H1 opening-skip 边界`](../jnj_bullish_h1_opening_skip_first_obstacle_boundary_2025-08-01_2025-09-02.md) | strong-looking A、H1、首障碍边界 | legacy narrative；opening-skip 不是 loss |
| [`LLY 多头 ABC/H1-H2 首障碍边界`](../lly_bullish_abc_h1_h2_first_obstacle_boundary_2024-06-06_2024-06-13.md) | deep/volatile B、H1/H2-like | legacy narrative；首障碍和事件字段未冻结 |
| [`LRCX 空头 ABC/L1 缺口首支撑`](../lrcx_bearish_abc_l1_gap_first_support_2024-07-10_2024-07-25.md) | gap impulse A、L1、首支撑边界 | legacy narrative；缺口重订不是普通 L1 |
| [`MAR 4H L1 视觉复核`](../mar_4h_l1_case_study_2026-06-18_2026-06-25.md) | 4H-like proxy、L1/L2-like、首支撑 no-trade | legacy narrative；60m proxy 不改写 Daily 合同 |
| [`MCD 空头 ABC/L1 首支撑`](../mcd_bearish_abc_l1_counter_market_first_support_2025-05-19_2025-06-27.md) | strong-looking A、受控 B、市场混合、首支撑阻塞 | legacy narrative；形态像不等于空间通过 |
| [`NVDA 多头 H1 触发分支`](../nvda_bullish_h1_trigger_branch_first_obstacle_2025-04-21_2025-05-08.md) | strong-looking A、H1、触发分支/首障碍边界 | legacy narrative；订单分支不能从结果反推 |
| [`NVDA 多头 H2 60m 条件案例`](../nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md) | H2、60m 条件研究 | legacy narrative；低周期研究不能补写日线两年证据 |
| [`TSLA 空头 ABC 案例（2024-07）`](../tsla_bearish_abc_case_2024-07-11_2024-08-05.md) | bearish ABC 历史案例 | legacy narrative；与 2024-03 案例的 lineage 不自动合并 |
| [`TSLA H1/H2 深度复核（2025-08）`](../tsla_h1_h2_case_study_2025-08-28_2025-09-05.md) | H1/H2、缺口/首阻力边界 | legacy narrative；理想价不能代替实际 gap path |
| [`TSLA H2-like 视觉反例（2025-12）`](../tsla_h1_h2_case_study_2025-12-08_2025-12-12.md) | H2-like、首阻力 no-trade | legacy narrative；后续上涨不能改写 no-trade |
| [`TSLA H1/H2 深度复核（2026-05）`](../tsla_h1_h2_case_study_2026-05-15_2026-05-22.md) | strong A、深 B、支撑反转、首阻力边界 | legacy narrative；强信号 K 仍需结构空间 |
| [`TSLA provisional L3 案例`](../tsla_l3_case_study_2026-03-25_2026-03-30.md) | provisional L3、continuation-risk | legacy narrative；未确认三推，不建立 L3 分母 |
| [`V 多头 ABC/H2 首障碍边界`](../v_bullish_abc_h2_no_gap_first_obstacle_boundary_2024-05-06_2024-05-17.md) | ordinary/directional A、H2、首障碍边界 | legacy narrative；事件和空间未闭合 |
| [`VRT 多头 ABC/H1 深 B 首障碍`](../vrt_bullish_abc_h1_deep_b_first_obstacle_boundary_2026-04-14_2026-04-20.md) | gap impulse A、deep/volatile B、H1-like | legacy narrative；不把 signal quality 直接当 gate pass |
| [`XOM 空头 H3 熊旗扩张边界`](../xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md) | H3-like、C-class expansion、gap reprice | legacy narrative；`H3-like` 不替代 `third_push_state` |

### 3.3 已被矩阵链接但仍应从入口 inventory 看到的对照

以下案例已经在聚合矩阵中出现，故不计入上面的 35 个 direct-only 数量；它们仍是本轮
核对旧别名边界的重要参照：[`KLAC H1`](../klac_h1_case_study_2025-10-14_2025-10-24.md)、
[`KLAC H2`](../klac_h2_case_study_2025-05-07_2025-06-03.md)、[`KLAC H3`](../klac_h3_bear_flag_case_2025-03-12_2025-03-28.md)、
[`NFLX 空头 L1`](../nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md)、
[`TSM 空头 L1`](../tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) 和
[`TSLA 空头 L1/L2/L3`](../tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md)。矩阵出现不等于
结果独立；这些案例仍受各自逐案合同、lineage、订单/空间和结果边界约束。

## 4. 矩阵/专题/框架入口不是逐案合同

以下专题文件可以帮助发现或比较历史图，但不是单一标的的入场合同；它们的批次方向、
`pattern_like`、`strong-looking-A`、`range-transition` 或 `no-trade` 不能复制成逐案的
`primary_pattern`、`internal_label`、`direction`、订单或胜率资格：

- [`空头 ABC 视觉控制对照`](../abc_bearish_visual_control_comparison_nflx_tsm_mcd_amzn_CN.md)；
- [`空头开放趋势视觉筛选日志`](../bearish_open_trend_visual_screen_2026-08-23_CN.md)；
- [`双顶/双底、MTR 与 Final Flag 对照`](../double_top_bottom_mtr_final_flag_comparison_CN.md)；
- [`H3/L3 独立候选筛选日志`](../h3_l3_candidate_screen_2025-08_2025-11_CN.md)；
- [`H3/L3 Futu 定向候选筛选`](../h3_l3_candidate_screen_futu_targeted_2024_2026_CN.md)；
- [`H3/L3 视觉比较`](../h3_l3_visual_comparison_CN.md)；
- [`大盘股视觉筛选`](../largecap_visual_screen_2024_CN.md)；
- [`普通 A 腿视觉筛选`](../ordinary_a_visual_screen_2024-05_2024-07_CN.md)；
- [`VCP 首轮视觉案例审计`](../vcp_visual_case_audit_round1_2026-08-24_CN.md)；
- [`成长股视觉筛选`](../visual_screen_growth_universe_2024q3_CN.md)；
- [`宏观与跨行业视觉筛选`](../visual_screen_macro_universe_2025h2_CN.md)；
- [`普通 ABC 视觉复筛`](../visual_screen_ordinary_abc_2025h1_followup_CN.md)；
- [`多周期视觉复核框架`](../multitimeframe_visual_review_framework_CN.md)；
- [`Strategy pattern inventory`](../../strategy/pattern_inventory_candidates.md)。

这些入口的职责是导航、样本发现、对照或协议说明。若专题表格未来要加入某个逐案结果，
必须链接独立 case contract 和 independent replay/result；不能在专题表中新增全局胜率或把
后续路径倒灌到入场前证据。

## 5. 事前/事后和历史别名边界

### 5.1 事前证据

事前证据只包括在研究 cutoff 前已可见的完整图表范围、两年 Daily 左侧、重要高低点、
EMA20/50/200、父级状态、方向、A/B、lineage、信号/确认、结构失效、首独立障碍、空间、
事件/缺口政策和订单合同。`direction` 可以因证据不足写 `no_valid_direction`；不能从标题
或后续方向强行填 `long`/`short`。

### 5.2 事后结果

`fill_status`、`trade_result`、`path_result`、`first_obstacle_hit`、`realized_R`、
`bars_held`、退出日期和胜率旗标只属于独立 replay/result。历史 case 正文即使描述“后来到达
支撑”“过程目标达到”或“后续继续上涨”，也不能因此补写 `pre_entry_space_R`、`space_status`、
EMA gate、主标签或胜率分母。`actual_fill_or_open_skip` 只描述研究/回放订单路径，不是实际
broker/account transaction log。

### 5.3 历史别名

下列写法在旧入口中可以保留，但只作为 display alias：

```text
H1-like / H2-like / L1-like / H3-like
strong-looking-A / strong A / ordinary A / deep B / controlled B
opening-skip / gap-trigger-reprice / first-obstacle-boundary
transition / range-to-bear / continuation-risk / process-target-reached
valid no-trade / research_positive conditional
```

新记录必须分别映射到 `parent_state`、`direction`、`primary_pattern`、`internal_label`、
`state_transition`、`order_branch`、`actual_fill_or_open_skip`、`space_status` 和状态轴；
映射前不允许把连字符、标题或文件名当作 canonical 值。特别是 `H3-like` 不等于确认的
`primary_pattern: H3_L3`，`valid_no_trade` 也不等于亏损结果。

## 6. 本轮实际修复

1. 新增本 inventory 作为 35 个矩阵外历史入口的统一索引，逐项列出链接、范围、显示别名
   和不晋级理由；不重写旧案例事实。
2. 为 ADBE、CME、MDT、PM 增加最小 historical evidence/status block：明确
   `contract_scope`、来源、截止时间、时区、session、周期、图表范围、两年窗口、重要高低点、
   EMA review、父级、方向、lineage pending、订单/空间和三条状态轴；缺失字段保持 pending/
   unknown，不激活主标签或计数。
3. validator 现在要求 inventory 报告和 35 个链接入口存在，并拒绝这些历史入口出现活动
   的结构化结果字段；同时守护四个新补边界的最小 evidence/status token。
4. 新增回归测试，固定 direct-only 数量、入口链接、历史结果隔离、四份最小边界块和本报告
   的 PA Research scope。
5. 七个 canonical index 均链接本报告；原有 matrix、Strategy inventory、历史案例和结果
   文件的职责不变。

## 7. 验证与统计结论

本轮没有新增图表样本、冻结合同、成交、CSV 行、回放结果或统计分母。验证只检查文档、
链接和边界；它不能证明 pattern 识别准确率或胜率。当前结论仍为：

```text
no-new-positive
validated win-rate: not-computable
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

这份审计完成的是“矩阵外历史入口可追溯、旧别名不误当 canonical、事前/事后不混淆”。
若以后要把某个入口变成可回放样本，必须另立独立目标，重新封口图表 provenance、方向、
lineage、触发、结构止损、首障碍、空间、事件和结果合同，不能由本 inventory 自动晋级。

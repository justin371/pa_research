# 优先 Pattern 代表性视觉候选矩阵（2026-08-24）

日期：2026-08-24  
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

本矩阵使用[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)；每个案例必须单独填写 `direction: long / short / no_valid_direction`，矩阵级别的状态不能替代行级状态。

## 1. 这张矩阵解决什么问题

PA Research 已经分别审计了 H1/L1、H2/L2、ABC、BOP、MTR/三推和交易区间边缘。下一步不再为了“看过更多图”而重复相似案例，而是把现有材料压缩成一组可以反复使用的代表性候选：

- **正向条件候选**：形态、背景、位置、订单、结构止损和第一障碍可以组成一个研究合同，但仍有事件、周期、路径或样本限制；
- **有效不交易对照**：形态看得出来，方向后来也可能正确，但入场前已经被父级、首障碍、事件、跳空或实际成交否决；
- **状态切换对照**：原来的 MTR、三推、H/L 或区间叙事被新的 BOP、区间或高潮状态取代；
- **过程失败对照**：静态 MM/RR 看起来足够，但实际路径先破结构止损，不能用结果补救。

这不是胜率表，也不是自动下单清单。矩阵只记录在完整历史图表上可以观察到的视觉合同，严格区分“形态识别”“可交易性”和“事后路径”。

## 2. 统一字段与主标签规则

每个案例只允许一个 `primary_pattern`。其他结构写成 `secondary_context`，避免同一组 K 线被 H2、ABC、三推、双顶和 MTR 重复计分。

```text
primary_pattern
secondary_context
direction
parent_state
state_transition
A/B pressure
signal_or_confirmation
order_branch / branch_role / actual_fill_or_open_skip
structural_stop
first_independent_obstacle
rough_RR
event_sector_timeframe_gate / permission / gate_result
research_state
trade_state
handoff_status
```

主标签的裁决顺序：

1. **先看父级状态**：开放趋势、成熟区间、区间边缘、过渡或高潮；
2. **再看主要位置**：主要高点/低点、旧边界、角色转换区、区间上沿/下沿；
3. **再看 A/B 压力**：A 是否有方向性，B 是浅/时间整理、深但后段受控，还是已经失控；
4. **再看接受或失败**：突破被接受时优先改成 BOP，回到区间时优先改成失败突破/区间；
5. **最后才用 H/L、ABC、三推等描述局部顺序**；
6. **订单和首障碍可以否决交易，但不能反过来创造一个形态**。

同一价格簇里的前高、EMA、缺口边缘、50% 回调和 MM 不重复计成五个独立优势。它们可以作为同一位置簇的不同观察，但必须避免把“多个名称”误认为“多个独立证据”。

## 3. 代表性候选矩阵

| 案例 | 主标签 | 次标签/关系 | 父级与位置 | A/B 与状态变化 | 订单、止损、首障碍 | 当前裁决 |
| --- | --- | --- | --- | --- | --- | --- |
| [`KLAC 2025-05-07–06-03`](klac_h2_case_study_2025-05-07_2025-06-03.md) | `H2` | `ABC continuation / support-EMA cluster` | 多头趋势回调，重复支撑与 EMA20 附近 | 强 A；B 较深但后段稳定；`2025-06-02` 的第二次恢复比 `2025-05-23` 更有意义 | `2025-06-02` 高点上方 buy-stop；结构止损约 `72`；首阻力约 `79.03–79.79`，约 `0.8R–1.0R`；MM 约 `87` 只能放在首障碍之后 | `research_positive_conditional`；位置和合同最清楚，但不是宽空间日线基准 |
| [`CRWD 2024-09-11–10-11`](crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md) | `H2` | `ABC / deep-but-late-controlled-B` | 多头父级，回调落在支撑附近 | A 有方向性；B 前段卖压较强，后段在约 `68.17` 稳定后才保留 H2 | `2024-10-02`/`2024-10-03` 触发分开；结构止损约 `67.4–67.8`；首阻力约 `75.11–75.54`，约 `1.5R–1.9R`；低周期只作确认 | `research_positive_conditional / incident-context-pending`；说明深 B 不自动失效，但不能等同浅 B |
| [`NFLX 2025-02-14–03-28`](nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md) | `L1` | `ABC continuation / no-gap bear` | 空头趋势中的回调，不是区间中部追空 | 空头 A 方向性清楚；B 深但后段受控；`2025-03-28` 第一次空头恢复 | 盘中刺破与收盘确认分开；结构止损约 `100.8–101.2`；首支撑约 `90.10–88.75`，约 `1.4R–1.9R`；无缺口，但路径仍需独立审计 | `research_positive_conditional`；当前最有价值的无缺口 L1 条件覆盖，不冻结通用规则 |
| [`TSM 2025-02-14–03-28`](tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) | `L1` | `ABC / reprice-after-gap` | 空头趋势，原触发被事件/小缺口改变 | 强 A；B 仍受控；原 stop 被开盘越过，旧 limit 没有真实回测 | 原约 `177.22` 合同失效；重订约 `176.66`；首支撑约 `167.99–165.05`，约 `1.6R+`；必须按实际价格重算 | `research_positive_conditional / gap-reprice-only`；证明重订可以保留 thesis，但不是原订单正例 |
| [`TSLA 2025-08-06–08-22`](tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) | `H2` | `ABC / low-cycle-contract-separate` | 多头回调靠近前高、通道和 EMA，但日线首阻力拥挤 | A 清楚；B 前段卖压强，后段在支撑与 EMA20/50 附近稳定；`2025-08-22` H2-like 恢复 | 日线完整结构止损约 `314.60`、最近阻力约 `340.25–340.55`，空间拥挤；15m 可另立约 `1.7R` 的短线合同 | `pattern_like / daily-valid-no-trade`；低周期合同不能替换日线母级风险 |
| [`KLAC 2025-03-12–03-28`](klac_h3_bear_flag_case_2025-03-12_2025-03-28.md) | `H3 / MTR-candidate` | `bear flag / exhaustion-candidate` | 空头父级中的熊旗上沿，主要阻力约 `74–75` | 三次上探仍属同一 lineage；第三推没有接受，随后出现空头跟随 | `2025-03-25` 低点下方 sell-stop；结构止损约 `74.50`；首支撑约 `66.6–65.1`，约 `1.4R–1.9R`；SOXX 同向 | `research_positive_candidate / not-production`；目前最有价值的 H3 条件样本，但仍需第二个独立方向样本 |
| [`TSLA 2025-03-07–03-10`](tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md) | `L3 / climax-boundary` | `continuation-or-climax` | 下跌末端靠近支撑/MM，父级状态不支持直接抄底 | 第三推反而加速、卖压扩张，非“一推比一推弱”的衰竭三推 | 第三推末端没有可靠反向订单；`220–224` 只是目标/支撑观察区，不能事后把止跌写成入场证据 | `valid_no_trade / continuation-risk`；保留为 L3 反转的反例 |
| [`TSLA 2024-03-04–03-14`](tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | `range-edge second-entry` | `L2 / MTR-candidate / ABC` | 局部空头结构发生在区间上沿失败后 | 强空头 A；B 后 `2024-03-12` L1 失败，`2024-03-13` L2-like 更清楚 | 约 `172.41` 下方 sell-stop；结构止损约 `182.87`；首支撑约 `152.37–153.75`，静态约 `1.6R–1.9R`，但实际先破结构止损 | `process-stop-first / range-edge-boundary`；不能用后来到达支撑替代过程审计 |
| [`TSLA 2025-09-08–09-12`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | `BOP / breakout-acceptance` | `prior MTR / three-push pressure` | 主要阻力约 `355.39–357.54`，由反转观察切换为接受 | 突破前多次影线测试但未接受；`2025-09-11` 强收盘站上阻力，15m 有跟随且未回到旧区间 | 15m 触发、日线收盘追入和次日追入是不同合同；突破 K 很宽，结构止损/首障碍尚未闭合 | `research_positive_conditional / state-transition`；验证状态切换，不验证“必然等回踩” |
| [`TSLA 2025-03-04 284 回测`](tsla_abc_playbook_2025-03-04_284_retest.md) | `BOP / breakout-pullback` | `gap-and-go / role-reversal` | 空头 gap-and-go 后，旧低点转为阻力 | 原 `277` sell-stop 被开盘跳过；价格回测约 `283.8–284.3` 后再次受阻 | 约 `284` sell-limit/retest 是独立合同；结构止损约 `304`；首支撑约 `261.84–262.24`，约 `1.1R`；MM `220–224` 仅第二层目标 | `research_positive_conditional / reprice-contract`；最清楚的真实回测路径，但空间和事件闭环仍有限 |
| [`RBLX 2024-03-18–04-05`](rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md) | `range-edge / failed-breakout` | `not-ABC continuation / double-bottom-like` | 完整日线是约 `35.8–39.0` 区间，反应在下沿附近 | B 回到 A 起点和下沿；`2024-04-04` 上冲越过前高后收回，突破不被接受 | 信号 K 失败；结构止损覆盖区间测试，首目标先看中线约 `37.3–37.8`；宽止损使空间不足 | `valid_no_trade`；用来阻止把区间局部外形写成 ABC/H2 |
| [`TSLA 2025-03-11–05-13`](tsla_range_after_sell_climax_2025-03-11_2025-05-13.md) | `range-bottom reaction` | `second-leg-trap control / H2-like` | 卖出高潮后形成宽交易区间 | `2025-04-21/22` 是下沿反应，不是趋势第二腿；`2025-04-22–04-29` 只是从下沿摆到上沿；`2025-05-08` 后才重建新 lineage/BOP | 区间目标先看中线/上沿；开盘跳过原触发时必须重订；不能用 MM 把中部首磁铁隐藏 | `observation_only / count-reset`；这是防止错误计数的核心对照 |

## 4. 这组样本真正支持什么

### 4.1 当前最可用的“优先筛图”组合

在完整图表上，以下组合最值得先进入候选，而不是直接下单：

```text
父级开放趋势
→ A 腿方向性清楚
→ B 没有破坏 A 起点，且后段压力收缩或在结构位稳定
→ H1/L1 或 H2/L2 在主要位置出现
→ 信号 K 与 confirmation/trigger 分开
→ 结构止损能覆盖正常测试
→ 第一独立障碍不明显拥挤
→ 事件、板块、开盘和周期合同通过
```

如果 A 普通、B 重叠多、父级接近区间或第一障碍过近，默认从 H1/L1 降级到 H2/L2，或直接 `observation_only / valid_no_trade`。这只是研究优先级，不是概率承诺。

### 4.2 当前最可靠的“否决”组合

以下任一项足以令候选降级，即使后续方向判断正确：

- 区间中部仍把局部上涨/下跌叫成 ABC 第二腿；
- 第三推扩张、跳空或卖出/买入高潮，却把它美化成衰竭三推；
- 主要前高/低点就在触发外侧，首障碍不足以容纳结构止损；
- 原 stop 被开盘跳过，仍沿用理想成交、旧止损和旧 R/R；
- limit 没有真实回测，却把“挂在下方/上方”当成已成交；
- 用 15m 窄止损掩盖 Daily/4H 没有空间；
- 财报前三个交易 session 内新开合同，或事件 gap 被当作普通 A；
- 只凭后续达到 MM、到达支撑或最终突破，倒灌证明入场当时的形态。

## 5. 按优先级的当前状态

| Pattern / 层 | 当前视觉状态 | 代表性条件候选 | 代表性否决/反例 | 下一步只需寻找什么新信息 |
| --- | --- | --- | --- | --- |
| H1/L1 | `conditional / visual-workable` | NFLX L1、TSM 重订 L1、KLAC H1 边界 | COST/HD/JNJ 首障碍或开盘边界 | 事件干净、开放趋势、首障碍宽裕的多空普通基准 |
| H2/L2 | `conditional` | KLAC H2、CRWD 深 B 后段稳定 | TSLA 日线拥挤、TSLA 2024-03 过程先止损 | 空头 L2 的同等干净条件样本 |
| ABC | `visual-workable / no-general-freeze` | NFLX/TSM、KLAC/CRWD | RBLX/TSLA 区间、QCOM 过渡 | 新方向或新订单合同，不再重复同质图 |
| BOP | `conditional` | TSLA 2025-09 接受、TSLA 2025-03 回测 | GOOGL/WMT/BKNG/QCOM 跳空重订边界 | 事件干净、多日真实回踩、角色转换和首障碍宽裕 |
| MTR | `provisional / advanced` | TSLA 2024-03 仅候选 | TSLA 2025-09 被 BOP 否定、NFLX 首障碍拥挤 | 反向二次确认、结构破坏、首障碍和过程完整同时成立 |
| 三推/H3-L3 | `conditional / no-new-positive` | KLAC H3 条件候选 | TSLA L3 扩张/高潮、ASML 区间重复 | 事件干净且第三推确实减弱的另一方向样本 |
| 区间边缘 | `visual-workable / no-new-positive` | TSLA 下沿反应、IWM 订单对照 | RBLX、TSLA 区间中部/开盘边界 | 上下沿双向、真实订单和中线空间完整的样本 |

## 6. 视觉助手的最终输出示例

以后遇到一张新图，先用下面这种短输出，而不是先讲一长串形态名称：

```text
primary_pattern: H2
secondary_context: ABC continuation / support-EMA cluster
parent_state: open bull trend, not range-middle
state_transition: none
A/B: strong A; deep but late-controlled B
signal: setup/count bar and confirmation/trigger separated
order: buy-stop above confirmation bar; low-cycle trigger separate
structural_stop: below support cluster, not below one signal-K tail
first_independent_obstacle: prior-high cluster; space is borderline
rough_RR: first obstacle about 0.8R–1.0R; extended MM is not used to rescue it
gate: event/sector/timeframe must be checked
direction: long
research_state: research_positive_conditional
trade_state: conditional / valid_no_trade if strict obstacle branch
gate_result: conditional
handoff_status: research_only
```

如果父级已经是区间，则主标签改成 `range-edge reaction`；如果旧边界被强收盘接受，则改成 `BOP`；如果第三推扩张，则写 `continuation-or-climax`，不自动写成 MTR。每次只保留一个主标签。

## 7. 本轮结论

这组矩阵说明：PA Research 的视觉工作已经能够把优先 pattern 组织成可复用的筛选语言，但还没有理由把任何一组材料称为“高胜率自动规则”。当前最有价值的不是再堆同类图，而是：

1. 用 KLAC/NFLX/CRWD/TSM 说明条件正向合同如何形成；
2. 用 TSLA 2024-03、TSLA L3、RBLX 和 TSLA 区间样本阻止后见之明与错误计数；
3. 用 TSLA 2025-09 与 284 回测样本区分突破接受和真实回踩；
4. 把 H1/H2、ABC、MTR、三推和区间边缘按一个主标签组织，避免重复计分；
5. 下一轮只寻找新的方向、订单、状态切换或首障碍几何，不为了数量继续复制边界图。

正式状态：

> `priority-patterns / visual-candidates / parent-clear / contract-separated / first-obstacle-first`：**conditional coverage; no general freeze**。

本文件只更新 PA Research 的视觉研究层；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

## 8. 相关入口

- [`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)
- [`完整图表视觉复核工作流边界审计`](visual_review_workflow_boundary_audit_2026-08-24_CN.md)
- [`核心八个 Pattern 代表性案例矩阵`](core_pattern_case_matrix_CN.md)
- [`H1/L1 第一次入场专项证据审计`](h1_l1_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`H2/L2 第二次入场专项视觉证据审计`](h2_l2_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`ABC 趋势延续专项视觉证据审计`](abc_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`BOP 突破回踩专项视觉证据审计`](bop_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`MTR 主要趋势反转专项视觉证据审计`](mtr_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`三推/H3-L3 专项视觉证据审计`](three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`交易区间边缘二次入场专项视觉证据审计`](range_edge_second_entry_visual_evidence_gap_audit_2026-08-24_CN.md)

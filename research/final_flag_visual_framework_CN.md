# 最终旗形（Final Flag）：视觉工作框架 v0.1

状态：`visual-research / provisional / not-quantitative`

课程资料把 Final Flag 描述为：一段持续较久的趋势接近末端时，出现的小型回调或窄区间。最后一次突破可能失败，随后更容易进入区间或反转；但第一次反向运动通常只能期待小反转，不能直接假设整条趋势已经反转。

本文件把 Final Flag 与普通回调、通道、MTR、交易区间边缘和 BOP 突破接受分开。它是 PA Research 的视觉筛选语言，不是胜率规则或自动下单规则。

## 1. 先看什么：Final Flag 不是一个单独图案

完整图表上的顺序是：

```text
持续趋势/连续推进
→ 趋势接近极端或明显变晚
→ 小型反向回调/窄区间
→ 最后一尝试或突破
→ 接受并延续，或失败后出现小反转/区间
→ 再决定是否存在第二次反向入场
```

“旗形”只描述压缩结构；“最终”来自它在趋势末端的位置和趋势已经走了多远。没有趋势背景的窄区间，不叫 Final Flag。

## 2. 最小视觉条件

### 2.1 趋势已经走了一段

- 左侧有多次方向性推进、通道或明显的高点/低点序列；
- 价格靠近趋势极端、通道边界、重要支撑/阻力或过度延伸区域；
- 趋势中已经出现较长的单向运行、连续扩张 K、跳空或高潮迹象；
- 不能因为一根大 K 之后出现一天小回调，就马上把它叫成 Final Flag。

趋势很强但还处在中段的普通旗形，应先归为 `trend_flag / continuation`，不要过早使用“最终”这个标签。

### 2.2 旗形内部是压缩，而不是强反向趋势

典型观察项包括：

- K 线重叠增加、实体缩小、推进距离变短；
- 反向回调较短，或在一个窄区间内来回；
- 反向压力存在，但还没有形成连续的强反向 A 腿；
- 两内包、局部双顶/双底、小三角或微型通道都可能是外形，但形状本身不够；
- 回调若变成宽幅双向区间，应改用区间逻辑；若形成强反向趋势，则应改用 MTR/新趋势逻辑。

### 2.3 最后一次尝试必须单独审计

在多头 Final Flag 中，最后一次向上突破可能：

- 收盘接受、继续跟随，成为趋势延续或 BOP；
- 只有影线越过，随后收回，成为潜在空头反转/区间边缘失败；
- 突破过宽或直接跳空，形态仍可记录，但原订单可能失去交易几何。

空头方向完全对称。必须记录当时是“接受”“失败”还是“尚未确认”，不能用后面的结果选择其中一个叙事。

## 3. 三种状态

| 状态 | 视觉含义 | 研究处理 |
| --- | --- | --- |
| `trend_flag_continuation` | 趋势中段或末端压缩后，原方向突破并接受 | 另开 BOP/延续分支，不称为反转 |
| `final_flag_reversal_candidate` | 趋势末端压缩、最后突破失败、反向信号出现 | 等反向第二次尝试，再做订单和空间审计 |
| `final_flag_range_transition` | 窄区间破坏后双方仍反复，方向未接受 | 先按小型交易区间或过渡处理，观望优先 |

首次反向运动通常只对应小反转、回到均线或区间中部。只有出现新的高低点结构、第二次反向确认和跟随，才逐步提高为 MTR 候选。

## 4. 与相邻结构的边界

| 相邻结构 | 识别重点 | 不能混淆的地方 |
| --- | --- | --- |
| 普通趋势旗形 | 趋势仍有空间，压缩后原方向恢复 | 没有趋势末端证据时，不加“Final”标签 |
| 宽通道 | 反向推进多、重叠多、上下边界反复 | 宽通道不是小型最终旗形；优先按通道/区间管理 |
| MTR | 主要趋势极端、反向尝试、第二次确认和接受 | Final Flag 只提供背景；失败突破和反向触发才进入 MTR 审计 |
| 区间边缘 | 成熟区间上沿/下沿的测试或失败突破 | 区间中部的小压缩不能叫 Final Flag；边缘反应先用区间二次入场逻辑 |
| BOP | 旗形边界或主要阻力被强 K 突破并接受 | BOP 是新的状态和订单合同，不能继续沿用原反转假设 |
| 三推/楔形 | 多次同向推进、效率变化和位置 | 三推可以发生在 Final Flag 内，但三推本身不证明最终反转 |

## 5. H/L 二次确认与订单

把反向交易拆成两个阶段：

1. **第一次反向尝试**：例如多头 Final Flag 顶部出现 L1-like，或空头 Final Flag 底部出现 H1-like。它只说明有人开始反向，不自动授权。
2. **第二次反向尝试**：第一次反向没有跟随或只形成小回调后，第二次 L2-like/H2-like 出现，并突破第一次信号 K 或局部结构；这通常比直接猜最后高点/低点更可审计。

订单分支：

- `stop`：在反向信号 K 的低点/高点外等待确认；
- `limit-retest`：仅在已知旗形边界、失败突破边缘或角色转换区回测时研究；
- `market-close`：只有反向收盘极强、等待会明显错过且首障碍仍有空间时才保留；
- `observation-only`：旗形像，但第一次反向还没有跟随、计数不清楚、跳空或首障碍拥挤。

### 信号 K 的最低要求

- 方向实体清楚，收盘靠近反向极值；或在关键位置出现长影线拒绝后收回；
- 不是仅仅刺破 EMA 或趋势线；
- 下一根 K 或低周期有合理的确认路径；
- 设置信号 K、实际触发 K 和后续跟随分开记录。

## 6. 结构止损、第一障碍和 R/R

### 看空 Final Flag 顶部

- 结构止损通常放在旗形上沿、最后一次测试高点和趋势极端上方；
- 不能把止损压在反向信号 K 的局部高点内，来制造一个虚假的高 R/R；
- 第一目标先看旗形下沿、最近左侧支撑或区间中部；第一次反向只预期小反转。

### 看多 Final Flag 底部

- 结构止损通常放在旗形下沿、最后一次测试低点和趋势极端下方；
- 第一目标先看旗形上沿、最近左侧阻力或区间中部；不能直接跳到远端 MM；
- 突破旗形后若回测守住，才可另开延续/BOP 管理。

### 空间审计

1. 冻结决策时点和订单合同；
2. 放置覆盖 Final Flag 失效点的结构止损；
3. 找触发方向上第一道独立支撑/阻力；
4. 第一障碍贴近或不足以覆盖结构风险时，记 `valid_no_trade`；
5. 只有第一障碍有基本空间，才看 AB=CD/MM 的后续延伸。

`1R/2R` 只是粗略视觉沟通，不是固定阈值。Final Flag 反向交易尤其不能用远端 MM 掩盖近端旗形边界或左侧磁铁。

## 7. Canonical 最小复核卡

`final_flag_state`、`last_attempt_state` 和 `breakout_state` 是 Final Flag 专用补充字段；
它们不能替代统一合同的方向、状态转换、订单和空间字段。

```text
contract_scope: deep_review / historical_context_only
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
direction: long / short / no_valid_direction
primary_pattern: ABC_CONT / BOP / RFB / MTR / other
secondary_context: final_flag / trend_flag / range_transition / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
final_flag_state: trend_flag_continuation / final_flag_reversal_candidate / final_flag_range_transition / unclear
last_attempt_state: continuation / failed / not_confirmed / mixed
breakout_state: not_confirmed / accepted / failed / gap_repriced
signal_bar:
confirmation_bar:
new_trigger:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
gap_policy: accept_open / skip / flag_only / not_applicable
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
structural_stop:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
rough_R_R:
event_context: raw pre-entry event note (examples: none / earnings / macro / gap / other / unknown; dated/compound qualifiers allowed)
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
failure_condition:
```

本框架旧文中的 `stop`、`limit-retest`、`market-close` 和 `observation-only` 只是显示别名，
新记录分别写入 `order_branch` 的 canonical 值；`actual_fill_or_open_skip` 只表示研究/回放
路径，不表示真实交易日志。

## 8. 历史案例对照

### A. KLAC 2025-10-14–10-24：多头浅旗/延续控制样本

- `2025-10-14–10-20` 是低重叠、带缺口、EMA20/50/200 向上的强多头腿；`2025-10-22` 只有一天回调，外形可先记为短旗。
- `2025-10-22` 是较强空头回调 K，但没有连续卖方跟随；`2025-10-23` 以强多头实体和接近高位收盘确认突破。
- 订单研究：`114.26` 上方 buy stop；大周期结构止损约 `104` 下方；触发上方 `115.49–115.63` 是第一高点障碍。
- 严格障碍分支会因第一阻力过近而 `valid_no_trade`；强趋势磁铁分支允许先观察是否接受高点区，再另开 BOP 分支。
- 标签：`trend_flag_continuation / final-flag-like-but-not-proven / first-resistance-conditional`。

它说明：强趋势中的短旗可以继续上破，但不能仅凭后续 MM 到位把它证明成 Final Flag 反转或无条件买点。

### B. NFLX 2024-08-05–09-26：高位最终旗形反转边界

- `2024-08-05–08-20` 强多头腿到约 `71.13`；随后 `08-22/27/30` 和 `09-03` 在高位窄幅重叠、多次测试。
- `09-03` 出现明显空头反应，`09-06 10:15` 低周期跌破 `67.10`，可研究 L1-like 空头 stop；结构止损应在 `71.60–71.70` 上方。
- 入场前最近支撑 `66.54–65.98` 只给约 `0.1–0.25R`，因此第一反向动作虽存在，仍应观望或只作小反转研究。
- `09-24` 后价格重新越过顶部，说明原 Final Flag/MTR 反向 thesis 失败。
- 标签：`final-flag-reversal-candidate / H3-like-boundary / valid_no_trade / later-invalidated`。

### C. TSLA 2025-09-08–09-12：Final Flag 假设被 BOP 接受否定

- `09-08–09-10` 在 `355.39–357.54` 阻力下多次试探、影线越过但收盘不能接受；当时可以保留高位 Final Flag/反转候选。
- `09-11` 强势收盘站上阻力，15m 出现突破、跟随和回测守住；状态切换为 `BOP acceptance`。
- 因此，反转方向不能在没有触发时提前下注；一旦接受发生，原 Final Flag 反转假设必须失效，不能继续因为“三推/高位压缩”而逆势做空。
- 标签：`final-flag-reversal-attempt / failed-thesis / BOP-acceptance`。

### D. KLAC 2025-03-12–03-28：熊旗延续控制样本

- 空头父级下，`03-17/19/24` 三次向上测试形成熊旗顶部；第三次没有突破接受，`03-26` 低周期卖出触发并有空头跟随。
- 结构止损约 `74.50` 上方；第一支撑 `66.6–65.1`，粗略约 `1.4–1.9R`。
- 它更适合作为“旗形压缩后原趋势延续”的对照，不直接叫 Final Flag；如果父级趋势已经非常成熟，才另开 Final Flag 解释。
- 标签：`trend_flag / H3-like / continuation-control / research-positive-candidate`。

## 9. 当前可迁移结论

1. Final Flag 的核心不是“小旗形”，而是“小旗形发生在已经走了很久的趋势末端”。
2. 最后一次突破失败后，第一反向运动通常只先看小反转或区间；等待第二次反向尝试比直接猜极值更符合 PA。
3. 窄旗突破并接受时，必须切换到 BOP/延续分支；不能把原来的反转叙事保留到突破之后。
4. 旗形外观、信号 K、订单是否成交、第一障碍空间是四个独立判断；漂亮的压缩形态也可以是 `valid_no_trade`。
5. 通道、三推、双顶/双底和 Final Flag 可以同时出现，但不能重复计算优势，也不能让名称替代跟随和失效条件。

## 10. 当前边界与后续最小任务

本轮已经形成多空对照和订单/风险工作语言，但还没有一组无事件、双向、首障碍宽裕、过程完整的 Final Flag 正向样本。因此当前结论保持为 `provisional`，不移交 Codex Trading。

只在出现以下新信息时继续补图：

- 一个事件干净、趋势明显成熟、旗形压缩清楚、最后突破失败且第二次反向触发不跳空的案例；
- 一个相同外形但突破被接受、明确属于延续的反例；
- 一个可以区分 Final Flag 与成熟区间边缘的案例。

没有这些新边界时，不重复堆叠同质案例，直接进入下一个 PA pattern。

## 参考

- [`PAHubCN 23A–23B Final Flags`](../pahubcn_courses/03_reversals_patterns_probability.md)
- [`MTR 视觉工作框架`](mtr_visual_framework_CN.md)
- [`KLAC 多头浅回调案例`](klac_h1_case_study_2025-10-14_2025-10-24.md)
- [`NFLX 高位多次测试案例`](nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)
- [`TSLA 突破接受跟踪`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)
- [`KLAC 熊旗延续案例`](klac_h3_bear_flag_case_2025-03-12_2025-03-28.md)

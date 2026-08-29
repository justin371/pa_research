# BOP、Gap-and-Go 与突破回踩：视觉研究框架 v0.1

日期：2026-08-23  
状态：`framework / partial / provisional / not-quantitative`

这是一份视觉研究框架，不是自动交易规则。它只解决一个问题：当价格突破已知阻力/支撑或区间边界后，什么时候应从“原来的反转/区间假设”切换到 BOP（Breakout Pullback）或 gap-and-go 假设。

## 1. 最小定义

一个可研究的 BOP 至少需要四件事：

1. 突破前的主要阻力、支撑或区间边界已能在左侧图表上标出；
2. 价格以实体收盘或连续低周期跟随离开该区域，而不是只有影线越过；
3. 突破后要么回踩旧边界并守住，要么没有回踩但继续强势接受；
4. 入场时的结构止损、第一独立障碍和实际 R/R 仍然成立。

`gap-and-go` 是“突破后直接继续接受”的分支；`breakout-pullback` 是“突破后回测旧边界、守住、再离开”的分支。没有接受、没有跟随或重新收回旧区间时，应转入失败突破/区间逻辑，而不是继续持有 BOP 故事。

## 2. 无后见之明的判断顺序

| 顺序 | 观察内容 |
| --- | --- |
| 1 | 先标出旧区间上沿/下沿、主要高低点、角色转换位和远端磁铁；不要先看 MM。 |
| 2 | 判断突破 K 是实体收盘离开，还是只有盘中刺破；记录突破时的开盘、收盘、影线和重叠。 |
| 3 | 看后续是否有跟随：连续收在突破区外、低周期继续推进，还是立即回到旧区域。 |
| 4 | 若发生回踩，检查旧阻力是否变成支撑、旧支撑是否变成阻力；回踩失败与回踩守住是两个方向。 |
| 5 | 冻结 stop、limit-retest 或收盘确认的实际成交价，再计算第一障碍和结构风险。 |

在成熟交易区间中，突破失败的先验风险较高；强突破可以改变这个先验，但需要接受和跟随证据。不能因为一根大阳/大阴或一个测量目标，就把区间中部的小摆动升级成 BOP。

### 三个临时状态

- `breakout-acceptance`：收盘有效离开旧区域，后续继续在外部交易；原来的双高、三推或区间反转假设失效。
- `breakout-pullback`：突破后回到旧边界附近，测试不重新接受旧区域，再次离开；这是最清楚的 BOP 研究分支。
- `failed-breakout`：突破后重新收回旧区域，或突破 K 没有跟随；先按失败突破/区间二次入场研究。

## 3. Gap-and-Go 与普通突破回踩

- 跳空并不自动等于强 BOP。跳空后若连续收在边界外、远离前方磁铁，才提高 `gap-and-go` 可信度。
- 跳空直接越过原 stop 时，原计划的成交价、止损和 R/R 必须重订；不能保留理想触发价。
- 如果不追跳空，等待旧边界回测的 limit-retest 是新合同；价格没有回到区域，就没有成交。
- 突破后若第一波回踩很深、重新进入旧区间，不能继续用“突破已完成”的剧本；要重新判断失败突破或区间过渡。
- 普通趋势中的 H1/H2 或 L1/L2 回调，如果没有新突破和角色转换，仍然是趋势回调，不改名为 BOP。

## 4. 订单、止损与第一障碍

| 分支 | 研究用法 | 主要边界 |
| --- | --- | --- |
| `stop-confirmation` | 突破 K 或回踩后的重新离开点上方/下方挂 stop | 触发被开盘跳过时重算；晚触发可能已经贴近下一个障碍 |
| `limit-retest` | 旧阻力/支撑角色转换区预先等待回测 | 未触及不算成交；不能把事后希望价格写成成交价 |
| `market/close` | 强突破收盘、跟随明确、空间仍足够 | 突破 K 过宽时减仓或改低周期触发；不能用正常仓位追高潮 |
| `observation-only` | 只有影线、跟随弱、回到旧区间、首障碍太近或事件未清 | 记录失败/边界，不追价 |

结构止损通常放在回踩低点/高点、旧边界失效侧或突破前最后一个结构点外；不能为了制造漂亮 R/R 把止损压到突破 K 内部。第一目标先看入场前已知的左侧高低点、下一层支撑/阻力或缺口边缘，再看区间高度、A 腿等距或 MM。研究上首障碍最好至少提供约 1R，完整波段通常希望接近 2R；这是过滤参考，不是固定胜率承诺。

## 5. 与相邻形态的边界

| 形态 | 与 BOP 的区别 |
| --- | --- |
| 区间边缘反转/失败突破 | 突破没有被接受，价格重新进入区间；先用区间边缘和二次入场逻辑 |
| Opening Reversal | 开盘第一方向失败后反向；若第一方向反而被接受，应改判为 BOP/gap-and-go |
| 普通 H1/H2、L1/L2 | 趋势回调延续，没有新的旧边界突破和角色转换 |
| Final Flag | 趋势末端压缩；原方向接受是 BOP 分支，反向失败才可能进入 Final Flag/MTR 分支 |
| MTR | 更大级别趋势线/通道破坏和反向结构；BOP 接受可以直接否定原来的 MTR 假设 |

## 6. 少量案例对照

### TSLA：2025-09-11，阻力下反转假设切换为 BOP

- `2025-09-08–10` 多次上探 `355.39–357.54` 后收回，继续做空或观望仍有依据；影线越过不算接受。
- `2025-09-11` 收盘约 `368.81`，强 K 接受在阻力区上方；15m `10:30` 收在约 `358.88`，`11:00` 继续到约 `360.55`，形成“突破 → 接受 → 跟随 → 回踩不回旧阻力”的完整路径。
- 这时原来的三推/多次测试反转假设失效，市场改标为 BOP。若收盘追入，必须以新成交、宽 K 风险和后续磁铁重算；`2025-09-12` 再追已经是更晚的延伸，不与 `09-11` 合并。
- 结论：`breakout-acceptance / BOP-candidate / pre-breakout-no-trade`。方向确认清楚，但未把它冻结为自动交易正例。

### TSLA：2025-03-04，空头跳空延续后的角色转换回测

- `2025-03-03` 低点约 `277.30`；`03-04` 约 `270.93` 低开，原 sell stop 被跳过。
- 下午反弹回测 `283.8–284.3`，旧低点/反转区转成阻力；约 `284.0` 的 sell-limit/retest 是独立的 BOP 延续分支，不能写成原 `277` sell stop 成交。
- 结构止损约 `304` 上方，第一支撑约 `261.84–262.24`，研究空间约 `1.1R`；后面的 `220–224` 只是第二层 MM 目标。
- 结论：`gap-and-go / breakout-retest / limit-retest-candidate`；形态和订单分支可研究，但不使用后续大跌倒灌成交质量。

### QCOM：2024-07-24，空头突破方向正确但实际成交后空间变差

- `2024-07-17–19` 强空头 A 带缺口，`07-22/23` 反弹到 `187.35–188.06`，`07-23` 低点 `184.14` 下方原本可研究 sell stop。
- `07-24` 开盘约 `181.44`，已经低于原触发；理想入场到 `178.01` 第一支撑约 `1.37R`，但按实际开盘接受重订后只约 `0.48R`。
- 回测到 `184.14` 没有发生，不能假设 limit 成交；后续 L2 又接近财报前 3 天，直接禁止交易。
- 结论：`gap-breakout / opening-reprice / first-support-boundary / valid_no_trade`。这是“方向对但 BOP 合同不合格”的控制样本。

### GOOGL：2024-03-18，强 A/浅 B 但跳空追价边界

- `2024-03-04–14` 方向性上涨，`03-15` 浅 B；`03-18` 开盘约 `147.30`，跳过原 `141.92` buy stop 区域。
- 原触发附近左侧高点约 `142.32` 很近；跳空后实际成交、结构止损和首障碍都需重算，limit-retest 没有回到区域就不算成交。
- 结论：`gap-trigger-reprice / observation-only / valid_no_trade`。形态方向正确，却没有足够的可审计首段空间。

## 7. 最小复核卡

```text
contract_scope: deep_review / historical_context_only
symbol:
review_date:
data_source:
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
primary_pattern: BOP / ABC_CONT / RFB / MTR / other
secondary_context: gap_acceptance / breakout_pullback / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
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
bop_state: acceptance_watch / ordinary_pullback / failed_breakout / gap_event / bull_flag_continuation / not_applicable
breakout_boundary:
acceptance_close:
follow_through:
retest_zone:
role_reversal_held: yes / no / unclear / not_occurred
event_context: raw pre-entry event note (examples: none / earnings / macro / gap / other / unknown; dated/compound qualifiers allowed)
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
failure_condition: reacceptance_inside_old_range
```

`breakout_boundary`、`acceptance_close`、`follow_through`、`retest_zone` 和
`role_reversal_held` 是 BOP 专用补充字段；它们不能合并回
`parent_state`、`state_transition`、`order_branch` 或
`first_independent_obstacle`。`actual_fill_or_open_skip` 只记录研究/回放订单
路径，不代表券商或账户的真实成交。

当前结论：BOP 的可复用核心是“旧边界先明确、突破接受再分类、回踩合同单独记账、首障碍优先于 MM”。下一轮只在出现新的方向、订单或边界问题时补案例，不再重复堆叠相同的 ABC/缺口样本。

参考资料：[`PAHubCN Trading the Open`](../pahubcn_courses/05_advanced_trading_modules.md)、[`range-edge framework`](range_edge_second_entry_framework_CN.md)、[`TSLA BOP follow-up`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)、[`TSLA 284 retest`](tsla_abc_playbook_2025-03-04_284_retest.md)、[`QCOM gap boundary`](qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md)、[`GOOGL gap trigger boundary`](googl_bullish_h1_gap_trigger_boundary_2024-03-04_2024-03-22.md)。

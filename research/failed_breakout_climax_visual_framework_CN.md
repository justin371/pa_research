# 失败突破与高潮反转：视觉研究框架 V0.1

状态：`framework / partial / provisional / visual-first / not-quantitative`

本文件研究两个经常被混在一起的现象：

1. 价格突破了一个事先可见的支撑、阻力或交易区间边缘，但没有被接受，随后回到原来的价格一侧；
2. 趋势后段出现大 K 线、跳空、连续扩张或加速，买方/卖方可能暂时耗尽，并出现反向运动。

它们可以同时出现，但不是同一个 pattern。失败突破可以发生在普通区间边缘，并不一定有高潮；高潮之后也可能只是小区间或两腿回调，并不一定反转。第一阶段的目标是让视觉助手先识别状态和边界，不建立扫描器，也不把“高潮”当成自动做反向交易的理由。

## 1. 最小定义

### 1.1 失败突破

失败突破必须有一个在决策时已经存在的结构边界：主要高点/低点、交易区间上沿/下沿、支撑阻力转换区、缺口边缘或通道边界。价格先越过边界，但随后出现以下至少一种证据：

- 收盘重新回到原区间或原结构一侧；
- 突破后没有跟随，下一次尝试又被边界拒绝；
- 反向 K 线形成方向性压力，并突破失败突破附近的局部结构。

只有影线刺破、盘中回测或单根小阴/阳线，不足以确认失败突破。要把“测试”“失败候选”和“已经确认失败”分开记录。

### 1.2 高潮

高潮是趋势后段的压力扩张或加速状态，常见视觉证据包括：

- 连续大实体、重叠减少、收盘靠近极值；
- 跳空或远离均线的扩张；
- 连续推进后，最后一段速度明显加快；
- 突破主要高/低点后仍继续扩张，但已经靠近大的左侧结构或 measured move 目标。

高潮说明原方向已经走得很远，可能产生获利了结、第一次反向运动或短暂平衡；它不等于“马上反转”。强趋势可以在高潮后继续走，尤其当突破被接受且有跟随时。

### 1.3 高潮反转候选

只有在下面几项同时出现时，才把高潮升级为“高潮反转候选”：

1. **成熟背景**：原趋势已经延续较久，或价格处于主要支撑/阻力、区间边缘、通道边界或 MM 目标附近；
2. **原方向出现失败或明显减速**：突破没有接受，或连续扩张后出现强反向 K 线；
3. **反向有跟随**：第一反向运动不是单根偶然 K 线，而是能破坏局部结构；
4. **第二次确认**：反向 H1/H2、L1/L2、失败突破后的二次入场，或同等强度的回测确认；
5. **有空间**：结构止损外到第一独立支撑/阻力至少有可接受空间。

前三项只足以形成“反转尝试”。没有第二次确认和空间时，默认分类是 `small_reversal_or_range` 或 `valid_no_trade`，不是 MTR。

## 2. 无后见之明的观察顺序

每个案例只按当时已经完成的 K 线推进：

| 阶段 | 只回答一个问题 | 不允许做的事 |
| --- | --- | --- |
| 背景 | 这是开放趋势、成熟区间、通道还是状态转换？ | 不能因为后来反转就把原来的趋势改写成“必然衰竭” |
| 位置 | 哪个主要边界或磁铁在事前可见？ | 不能把事后形成的支撑倒灌成入场依据 |
| 扩张/测试 | 原方向是在正常推进、高潮，还是突破测试？ | 不能把每根大 K 都叫高潮 |
| 接受/失败 | 收盘和后续跟随接受了边界，还是回到原侧？ | 不能把盘中刺破直接当成失败突破 |
| 第一反向运动 | 反向是否形成结构性破坏？ | 不能把第一根反向 K 当成整段趋势反转 |
| 第二次确认 | 是否出现第二次入场或回测守住？ | 不能用后面的盈利结果替代当时的触发 |
| 交易审计 | 止损、第一障碍、订单合同和粗略 R/R 是否合理？ | 不能用更窄的事后止损制造好看的 R/R |

建议用下面四种状态代替过早贴标签：

- `continuation_or_climax`：原方向仍有接受和跟随；高潮只作风险提示；
- `failed_breakout_candidate`：边界被越过但尚未被接受，等待回到原侧和反向跟随；
- `small_reversal_or_range`：已有第一反向运动，但更可能先形成小区间或两腿回调；
- `MTR_candidate`：位置、失败、结构破坏、第二次确认和空间均初步齐全。

## 3. 与相邻 pattern 的边界

| 相邻概念 | 什么时候可以重叠 | 什么时候不能合并 |
| --- | --- | --- |
| MTR | 高潮/失败突破可以是 MTR 的早期证据 | 没有主要结构破坏、第二次确认和空间时，只能叫反转尝试或小反转 |
| Final Flag | 趋势末端压缩后，最后一次突破失败可能形成 Final Flag 反转 | 普通高潮大 K、宽区间或趋势中段旗形不能自动叫 Final Flag |
| Opening Reversal | 失败突破发生在开盘第一波、前日高低点或开盘磁铁附近时 | 没有开盘时段特征的日内/日线失败突破不归入 Opening Reversal |
| BOP / Gap-and-Go | 突破收盘强、回踩守住、后续跟随时，原失败假设必须切换为 BOP | 不能一边看到强接受突破，一边继续用旧的失败突破逻辑做空 |
| 交易区间边缘 | 已知区间上沿/下沿刺破后回区间，可直接使用区间边缘二次入场框架 | 区间中部的局部高低点，不应被包装成边缘失败突破 |
| H3/L3 | 第三次推进变宽、变快，可能是高潮/延续边界 | 第三次推进不自动等于楔形衰竭；要看是否减弱、位置和反向确认 |

详细相邻框架：[`MTR`](mtr_visual_framework_CN.md)、[`Final Flag`](final_flag_visual_framework_CN.md)、[`Opening Reversal`](opening_reversal_visual_framework_CN.md)、[`BOP`](bop_gap_acceptance_framework_CN.md)、[`交易区间边缘`](range_edge_second_entry_framework_CN.md)、[`通道状态`](channel_visual_framework_CN.md)。

## 4. 订单分支

### 4.1 Stop-confirmation：默认研究分支

在失败突破后等待反向信号 K，使用信号 K 的另一侧作为 stop 触发。它牺牲一部分价格，换取“失败已经被市场确认”的证据。适用于第一反向运动后仍有空间、原方向没有重新跟随的情况。

### 4.2 Limit-retest：结构回测分支

当价格回到失败边界、前支撑转阻力或前阻力转支撑时，可以研究 limit-retest，但要单独记录：

- limit 放在结构回测区域，不是为了追求更窄的止损；
- 如果价格尚未回到该区域，订单不应被假设已经成交；
- 跳空穿过原计划价位后，必须按实际成交重建风险，旧合同作废。

### 4.3 Market/close：强反向分支

只有在反向收盘很强、已经破坏局部结构且第一障碍仍有空间时才保留。强反向 K 若同时是冲击/事件 K，宁可降仓或观望，不能因为它很大就无条件市价追入。

### 4.4 Observation-only：优先级很高的结果

下列情况不下单：

- 高潮后只有一根反向 K，没有跟随；
- 第一反向运动已经碰到左侧主要障碍；
- 结构止损太远，第一障碍不足约 1R；
- 原方向重新接受突破，失败假设被否定；
- 财报/重大事件使普通 K 线几何失真。

## 5. 止损、第一障碍和粗略 R/R

- **结构止损**：空头高潮反转通常放在失败突破极端、高潮高点或主要反向结构高点外；多头反向则对称处理。不要把止损放在信号 K 的微小尾巴内，除非研究的就是低周期独立合同。
- **第一障碍**：从实际入场方向看，优先记录最近的独立左侧支撑/阻力。MM、缺口边缘、EMA 和同一价格簇的前高/前低不能重复计数。
- **空间纪律**：第一障碍不足约 1R 时，默认 `valid_no_trade`；完整波段计划可把约 2R 作为参考，但两者都不是胜率保证或固定程序阈值。
- **高潮后的目标**：第一目标通常先看最近磁铁、区间中线或第一独立边界；只有价格接受穿越后，才把 MM 当作后续路径。高潮到位本身不是必须反转的价格点。
- **管理**：靠近 MM 或主要障碍而动能减弱时，可以分批止盈，不必机械等精确点；若突破继续接受，剩余仓位才有理由看更远目标。

## 6. 案例对照

### A. TSLA 2025-03-10：卖出高潮后先进入大区间

- 2025-03-07–03-10 出现强烈下跌和卖出高潮，低点约在 `220` 附近；左侧支撑与 MM 也集中在约 `220–224`。
- 当时合理的第一判断是“卖压暂时耗尽，先预期反弹/平衡”，不是直接宣布主要趋势反转。
- 后续价格进入约 `214–230` 的低位区域，并最终发展成更大的父级交易区间；2025-04-22 的行为必须按区间下沿逻辑看，不能倒灌成 ABC 的第二腿延续。

结论：`climax -> small_reversal_or_range`。这是“高潮后先平衡”的基准，不是 MTR 正例。

### B. COST 2024-07-11–07-18：强 A 也可能没有交易空间

- 2024-07-11 上涨末端出现巨大的空头反转 K，约从 `879.8` 开始，低点/收盘约在 `836`；它更像“高潮型强 A”，不是普通开放趋势 A。
- 2024-07-15–07-17 的 B 较浅、重叠增加；2024-07-17 的 L1-like 下破后，若按结构高点约 `847.4` 上方放止损，前方第一支撑约 `828–834`，距离很近。
- 2024-07-18 虽有先上冲后下破，但第一障碍几乎贴着触发区，粗略小于 1R；更远的 `815` 不能事后拯救这笔交易。

结论：`pattern_like / valid_no_trade / strong-A-climax-boundary`。强方向、L1-like 形态和事后下跌都不能替代第一障碍审计。

### C. TSLA 2025-09-08–09-12：失败突破假设被接受突破否定

- 2025-09-08 和 2025-09-10 在 `355.39–357.54` 一带多次上影和收盘回落，可以记录为主要阻力下的失败突破/反转候选；当时不应提前把它当成确定空头。
- 2025-09-11 出现强阳线，约 `350.17/368.99/347.60/368.81`，收盘接近高位并越过阻力；随后低周期跟随，回踩守住旧阻力上方。

结论：原来的 `failed_breakout/MTR` 假设失效，市场状态切换为 `BOP acceptance`。这条边界很重要：当突破被接受时，不能继续用“它应该失败”的想法逆势交易。

### D. XOM 2024-07-18–08-02：第三推扩张属于延续/高潮边界

- 空头 A 后出现多次向上测试；第三次测试没有明显收窄，反而范围扩大，靠近 `111.43–111.60` 阻力。
- 2024-08-01 的空头信号低点约 `108.26`，2024-08-02 开盘约 `107.90`，原 sell-stop 被跳空改变；若按重订价处理，结构止损仍在阻力上方，第一支撑约 `105.20`，空间约只有 `0.7R`。

结论：第三推扩张不等于楔形衰竭；原方向可以继续，且跳空重订和第一障碍共同把它降为 `valid_no_trade`。

## 7. 当前工作结论

1. 高潮反转最可靠的第一步不是“猜反转”，而是识别原方向是否已经减速、是否到达主要位置，以及市场是否开始形成小区间。
2. 失败突破的核心不是越过边界，而是**没有被接受并回到原侧**；反向交易仍要等待跟随和第二次确认。
3. 第一反向运动通常只能支持小反转、区间或两腿回调的预期；没有结构破坏和第二次确认，不升级为 MTR。
4. 强 A、巨大 K、跳空、第三推扩张都是方向性证据，同时也是风险提示；它们不会自动授权订单。
5. 先看主要支撑/阻力和第一障碍，再看 MM。后续实际走到 MM 不能倒灌成入场依据。
6. 目前已有足够的边界样本形成工作版，但还没有无事件、双向、首障碍宽裕且过程完整的“标准高潮反转正例”。因此本框架保持 `provisional`，用于视觉筛选和观望纪律，不进入 Codex Trading 或 Execution Agent。

## 8. 复核卡

每次遇到“失败突破/高潮反转”候选，只需先回答：

1. 事前可见的边界在哪里？
2. 这是开放趋势、区间、通道还是状态转换？
3. 原方向是被接受、减速，还是仅仅出现一根大 K？
4. 第一反向运动破坏了哪个局部结构？
5. 有没有第二次确认或回测守住？
6. 结构止损放在哪个极端外？
7. 入场后第一独立支撑/阻力在哪里，是否至少有大致 1R？
8. 原方向重新跟随时，哪一个假设失效？

如果第 4、5 或 7 项答不清楚，默认先观望；把它记为边界案例，而不是强行交易。

### Canonical 输出映射

问题卡只负责引导观察；形成研究记录时必须另外保留以下统一字段。`breakout_boundary`、
`breakout_state`、`first_reverse`、`second_confirmation` 和 `third_push_state` 是本框架
的补充字段，不能合并成一个自由文本状态。

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
primary_pattern: RFB / MTR / BOP / ABC_CONT / other
secondary_context: failed_breakout_climax / range_edge / final_flag / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
breakout_boundary:
breakout_state: not_confirmed / accepted / failed / gap_repriced
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
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

`actual_fill_or_open_skip` 只表示研究/回放路径；`filled` 不能被解释为券商或账户的真实
成交。若问题卡只能回答到局部形态，保留 `observation_only` 或 `pending`，不要补写订单
或结果字段。

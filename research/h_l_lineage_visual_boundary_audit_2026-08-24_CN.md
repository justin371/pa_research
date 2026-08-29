# H/L lineage 与三推状态视觉边界复核（2026-08-24）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`；边缘三推修订：`2026-08-26`

统一字段、方向和状态分轴见[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。本阶段只做视觉识别，不冻结订单合同。

## 目的与范围

第二阶段只优化三件事：

1. H1/H2/L1/L2 是否属于同一主周期、同一回调 lineage；
2. 第一次尝试失败后，第二次尝试如何被看见、记录和失效；
3. 三推/H3-L3 如何在 `衰竭候选`、`扩张/高潮`、`区间重复` 和 `通道延续` 之间分流。

本文件只处理图像中的背景、位置、推动腿、计数和视觉边界。不填写订单、止损、R/R、评分或自动化字段，不把任何候选升级为 Codex Trading 规则。

统一复核卡见[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)；本轮未标注图像见[`PA 图表视觉识别验收记录`](visual_recognition_smoke_test_2026-08-24_CN.md)。

本文件是跨案例的历史视觉协议，不是逐标的订单合同；下方例子只支持
`contract_scope: historical_context_only` 的背景、lineage 和状态研究。若以后把某个
例子转入深审，必须重新填写该标的的证据头、方向、触发、结构止损、首独立障碍和空间，不能把本文件的视觉标签直接当作成交合同。

本文件中的历史自然语言标签（例如 `same-lineage-provisional`、`unclear-to-range`、
`range-repeat` 和 `H2-like`）只作为显示别名。字段位置一律按当前 canonical 轴读取；
缺少严格证据时使用 `pending`/`unclear`，而不是用“provisional”拼接出新的枚举。

只有逐案、完整且已闭合的研究记录，才可以在该案例的证据范围内填写
`primary_pattern`、`internal_label` 和必要的 `lineage_id`；本跨案例账本不替任何案例
冻结这些值，也不把聚合记录当作独立样本。

## 零、所有局部识别共用的左侧两年基准

先看至少两年的 Daily 左侧背景（来源窗口支持时），再看局部 4H/1H/15m 图；同一标的的多周期图像共用这份背景。先标主要高点、主要低点、支撑、阻力、前高/前低角色转换区，再记录 Daily EMA20/50/200 的位置和价格在其上/下关系。局部形状不得覆盖或事后改写这些左侧事实。

```text
daily_context_window: >=2y / <2y / unavailable
major_highs:
major_lows:
support_zones:
resistance_zones:
daily_ema20_50_200:
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
left_context_review: complete / partial / unavailable  # 汇总说明，不替代上面两个 review 字段
```

两年窗口、EMA 或重要高低点缺失时，写明缺失范围并保持 `pending`；不能用更短局部窗口制造完整的 lineage、三推或 H3/L3 结论。

## 一、统一 lineage 账本

每一张图先填这一段，再决定 H/L 或三推标签。`lineage_status` 不是置信度分数，而是“能否把几次尝试放在同一结构故事中”的审计结果。

```text
symbol:
contract_scope: historical_context_only
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: historical_close / unknown
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
count_timeframe:                  # 只允许一个主计数周期；timeframes_seen 记录全部可见周期
direction: long / short / no_valid_direction
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
secondary_context:
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
lineage_anchor:                   # 使尝试仍属于同一组的母腿、回调或压力区
parent_leg: origin -> extreme
local_A: origin -> extreme / quality
local_B: origin -> extreme / quality

attempt_1: origin -> extreme / meaningful_reason / separation
attempt_1_failure_or_insufficient: yes / no / unclear
attempt_2: origin -> extreme / meaningful_reason / separation
attempt_2_failure_or_insufficient: yes / no / unclear
attempt_3: origin -> extreme / meaningful_reason / separation

internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
historical_count_label: H1 / H2 / H3 / L1 / L2 / L3 / not_h_l / pending
reset_event: none / new_extreme / accepted_breakout / range_acceptance / new_A / timeframe_change / unclear
visual_invalidation:               # 重新接受哪一侧会使当前结构解释失效
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
gap_policy: accept_open / skip / flag_only / not_applicable
structural_stop:
first_independent_obstacle:
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

### 聚合协议与完整闭合逐案记录的边界

这里的字段块是跨案例的 canonical 轴清单，不是给当前历史聚合记录填写一组主标签。
“完整且已闭合”只表示该案例在预先确定的截断时点已经封口了入场前证据；它不表示
已经知道后续结果、已经成交，或已经具备交易授权。逐案记录必须显式处理证据头、
`direction`、`primary_pattern`、`internal_label` 和 `lineage_status`；只有在记录主张
具体父级/尝试依赖时才填写对应 `lineage_id`。证据或 lineage 未解决时，保留
`pending`/`unknown`，并把案例留在 `observation_only` 或未冻结状态；不能用聚合 README、
后续走势或结果反填。冻结回放另需独立的数值订单字段，本协议不创建回放输入。

本协议实际只冻结视觉字段；`order_branch`、`gap_policy`、`structural_stop`、
`first_independent_obstacle`、`pre_entry_space_R` 和 `space_status` 在这些历史例子中不因
图形相似而自动赋值。没有独立触发和结构止损时，空间只能保持 `unknown`，表中的“首障碍边界”
是说明性观察，不是 `strict_ge_1R` 或交易许可。

### 同一 lineage 的五项门槛

| 检查 | 可以保留同一 lineage | 必须 reset 或降级 |
| --- | --- | --- |
| 主周期 | A、B、尝试在同一主周期可见；低周期只补充结构细节 | 只能把 15m 事后拼成 Daily/1H 看不到的三段 |
| 父级状态 | 同一开放趋势、同一回调或同一压力区 | 价格已在双向区间中被接受，或建立新母级 A |
| 尝试分隔 | 之间有可见回调、停顿、失败或重新测试 | 只是连续同向 K 线或微小影线 |
| 边界接受 | 旧边界仍未被方向性接受，尝试仍围绕同一结构 | 突破外侧被接受、旧角色结束，或新结构取代旧结构 |
| 事前可见性 | 在第三次/第二次发生时，前次失败或不充分已可见 | 只有看完后续结果才知道应该数几次 |

若五项中任一项明确落入右栏，`lineage_status` 不写 `same_lineage`。不确定时写 `unclear`，而不是用“看起来顺”替代证据。

## 二、H1/H2/L1/L2 的计数规则

- `H1/L1`：同一 B 回调中第一次有意义的原方向恢复；不是 EMA 后第一根顺向 K。
- `H2/L2`：第一次有意义尝试已经失败、无跟随或不足，B 在同一 lineage 中继续发展，随后出现第二次有意义尝试。
- 第一次尝试如果没有被分开看见，不能仅凭后面的更高高点/更低低点补写 H2/L2。
- 新极值、突破接受、父级进入成熟区间或新 A 腿出现时，旧计数必须写 `reset_event`。
- 低周期的 `15m-H2` 和高周期的 `Daily-H2` 必须分别命名，不能相加。

### H/L 结果分层

| 结果 | 允许的表述 | 不允许的表述 |
| --- | --- | --- |
| `H2/L2` | 同一回调内第一次失败后出现第二次尝试 | “第二根阳/阴线就是 H2/L2” |
| `H2/L2-like` | 外形和顺序可读，但 lineage 或第一次失败仍有疑问 | 已确认的生产规则 |
| `new-lineage H1/L1-like` | 父级状态切换后重新开始的第一次尝试 | 把旧 H1/H2 延续到新父级 |
| `pending` | 周期、分隔、父级或失败证据缺失 | 用最终盈利/亏损替代计数证据 |
| `not_h_l` | 区间重复、通道连续或没有有意义尝试 | 为了得到 H3/L3 强行继续数 |

## 三、三推/H3-L3 状态分流

三推先回答“第三次有意义推进的压力状态”，再决定是否与 H3/L3 重叠：

| 状态 | 必须从图上看到 | 当前标签方向 |
| --- | --- | --- |
| `exhaustion_candidate` | 同一 lineage、效率下降、重要位置、第一反向压力 | `three-push / H3-L3 candidate`，等待更强反向证据 |
| `continuation_or_climax` | 第三推更长/更快、实体或跳空扩大、收盘和跟随增强 | 原方向仍有控制；不是自动反转 |
| `range_repeat_test` | 三次测试都在双向边缘附近，外侧没有持续接受 | 若第三推在上沿/下沿并有拒绝，可写 `range_edge_three_push_candidate`；中部或 lineage 不清仍写 `not_h3_l3` 或观察 |
| `channel_continuation` | 推进沿通道继续，边界未破坏 | 顺势结构候选；不自动升级 MTR |
| `unclear` | 三段无法在主周期独立分开 | `pending`，不得用三点命名楔形 |

`H3/L3`、三推楔形候选和 MTR 是三个不同层级：第三次尝试不等于衰竭，三推候选不等于控制权改变，MTR 还需要反向结构接受和第二次确认。

## 四、未标注图像逐例套用

这些结论先来自图像直接观察，再用图中价格轴和历史数据作交叉核对；图像本身没有预先写入 H/L 或三推标签。

| 样本与资产 | 主周期 / 母结构 | lineage 账本结果 | 视觉边界与状态分流 | 结论 |
| --- | --- | --- | --- | --- |
| [SPY H/L drill](assets/visual_recognition/2026-08-24/round3_hl_drills/SPY/SPY_drill_montage.png) | 1H/15m；8-03–04 多头 A，8-05–06 回调 | `lineage_status: pending`；历史显示标签为 `same-lineage (provisional)`；8-05 的第一次恢复/突破尝试失败，8-07 是第二次恢复候选 | 重新接受 `767` 下方削弱这组多头计数；强收盘接受 `776.85` 上方则转新突破状态 | `H2-like / pattern_candidate / count-pending` |
| [NVDA H/L drill](assets/visual_recognition/2026-08-24/round3_hl_drills/NVDA/NVDA_drill_montage.png) | 1H/15m；8-05–07 推进，8-10–11 回调 | `lineage_status: pending`；历史显示标签为 `same-lineage: provisional`；8-10 第一次恢复到约 `224.14` 后失败，8-12 再次推进至约 `225.10` | `216.30` 下方破坏本局部恢复；`224–225` 外侧重新接受会重建为新状态；更早 8-03–07 结构不能混入当前计数 | `H2-like / pattern_candidate / count-pending` |
| [AAPL 多周期图](assets/visual_recognition/2026-08-24/round2_multisymbol/AAPL/AAPL_MTF_montage.png) | 1H/15m；8-19 多头突破尝试后失败 | `lineage_status: reset`；失败突破后空头腿是新 lineage，不把原多头尝试继续数成 H2 | 重新接受 `319–320` 上方废弃失败突破后的空头解释；8-20/21 的低点不足以自动冻结 L2 | `new-lineage L1/L2 boundary / pending` |
| [MAR 空头多周期图](assets/visual_recognition/2026-08-24/round3_l1_l2_mar/MAR_MTF_montage.png) | 4H-like/60m；6-15–22 空头 A，6-23–24 反弹 B | `lineage_status: pending`；历史显示标签为 `same-lineage: provisional`；6-24 后段第一次空头恢复，6-25/26 是后续第二次/跟随候选 | 重新接受 `392.63–400` 反弹区废弃当前空头恢复；15m 历史不可得，不能把 60m 当作 15m 确认 | `L1/L2-like / count-pending / 15m-evidence-missing` |
| [RBLX 三推图](assets/visual_recognition/2026-08-24/round2_multisymbol/RBLX/RBLX_MTF_montage.png) | 15m；Daily 空头背景，局部 `35–40` 区间 | `lineage_status: unclear`；历史显示标签为 `unclear-to-reset`；三段上推可见，但父级先是区间/过渡，不是开放趋势回调 | `third_push_state: range_repeat_test`；反复回到区间内，不能称衰竭楔形或升级 MTR | `three-push boundary / not_h3_l3 / observation-only` |

### 逐例优化后的固定写法

以后遇到类似图形，摘要必须先写：

> 主周期是 `[周期]`，父级是 `[趋势/区间/过渡]`；A/B 锚点为 `[范围]`。第 1 次尝试是 `[事实]`，其失败/不足是 `[事实]`，第 2 次尝试是 `[事实]`。因此 `lineage_status` 为 `[same_lineage/reset/unclear/pending]`，计数只能写 `[H2-like/L2-like/pending/not_h_l]`。若出现 `[边界]`，当前状态切换为 `[新状态]`。

这句话先于任何订单或风险字段；当前阶段如果这句话写不完整，就停在 `pending` 或 `observation_only`。

## 五、当前优化结论

1. **H2/L2 的核心改进是“前次失败证据先行”。** 只看见第二次顺向波动，不足以称 H2/L2。
2. **计数和状态切换分开。** AAPL 证明失败突破后要 reset；RBLX 证明区间重复测试不能继承开放趋势 H3/L3。
3. **三推状态先于三推名称。** RBLX 只能是 `range_repeat_test` 边界；扩张/高潮和通道延续必须保留对称分支。
4. **低周期证据不能填补高周期 lineage 缺口。** MAR 的 15m 缺失被明确保留；SPY/NVDA 的 1H/15m 只支持局部候选，不改变 Daily/4H 父级。
5. **当前仍是研究层优化。** 本审计不生成阈值、扫描器、订单合同、止损、R/R 或评分；干净正例和严格计数冻结仍需新的可追溯图像证据。

当前阶段状态：`research_state: pattern_like / trade_state: observation_only / gate_result: pending / strict-count-promotion pending / no-new-positive`。

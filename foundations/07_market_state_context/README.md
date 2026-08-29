# 市场状态与父级背景

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)。

这是所有 PA pattern 的上游过滤层。先判断市场处于开放趋势、成熟交易区间、区间边缘、过渡还是高潮，再决定能否使用 ABC、H1/H2/L1/L2、MTR、失败突破或三推语言。

## 1. 五种工作状态

| 状态 | 视觉特征 | 首选逻辑 |
| --- | --- | --- |
| `open_trend` | 方向腿有跟随、重叠较少、回调没有接受反向结构 | ABC、旗形、H1/H2 或 L1/L2 |
| `trading_range` | 上下沿反复、双方突破尝试失败、重叠和反向摆动多 | 上沿/下沿反应、失败突破、区间二次入场 |
| `range_edge` | 价格靠近上沿或下沿，已有反复测试和反向反应 | 边缘 limit/stop、二次入场、失败突破、区间边缘三推候选 |
| `transition` | 趋势、区间、角色转换和新方向混合，父级尚未接受 | 保守标记、等待接受/失败，不强行继承计数 |
| `climax` | 后段扩张、跳空、远离均线/结构，随后可能小反转或平衡 | 管理/观望，等待二次确认；不自动做反向 |

## 2. 交易区间不是单一根数定义

成熟区间的核心是：

- 价格在上沿和下沿之间反复往返；
- 多头和空头都在边缘尝试突破，但没有持续接受；
- K 线重叠、反向摆动和失败跟随增加；
- 区间中部通常没有清楚的方向优势。

20 根左右或更多 K 线可以作为成熟度提示，但不能脱离结构机械定义区间。先标区域：

```text
range_upper_zone:
range_lower_zone:
range_midpoint:
major_left_levels:
range_state: mature / developing / transition / not_range
```

## 3. 区间内不能强行使用趋势腿

从区间下沿强力上涨到上沿，外观可能像 ABC 的第二上涨腿；只要父级仍是区间，它首先是区间摆动。`H2-like` 也只能记为边缘或区间尝试，不能自动升级为开放趋势 H2。

区间中部优先 `observation_only`；若形态、方向和入场几何已足够复核但首障碍或其他硬闸门否决，则使用 `valid_no_trade`。若区间边缘出现第三次有意义测试、拒绝或假突破回区间，可进入 `range_edge_three_push` 候选；若边缘反应后走到中线或另一边缘，旧边缘合同的目标已到达，不能继续用“第二腿”追价。中部再出现的局部突破通常没有足够位置优势。

## 4. Second-leg trap

Second-leg trap 风险出现在：

1. 价格从一侧边缘或支撑强力反弹；
2. 到达中部/另一侧边缘；
3. 交易者把内部摆动误判为趋势第二腿；
4. 在第二次追入时，前方主要障碍已经很近。

只有出现区间外强收盘、跟随和回测守住，才重新建立新的趋势 A 腿；此前的区间交易和之后的突破延续必须分开记录。

## 5. 状态切换

### 区间 → 新趋势

需要边界外强收盘、后续跟随、没有快速收回，最好还有回测守住。一次影线或单根孤立大 K 只记测试候选。

### 趋势 → 区间

趋势腿出现重叠、反向尝试增加、前高/前低反复、跟随失败或突破不被接受时，旧 ABC/H-L lineage 不能无限延续；重建上下沿、中线和边缘逻辑。

### 高潮 → 小反转/区间

高潮后的第一反向波通常只是反转尝试、小区间或两腿回调。需要位置、结构破坏、跟随和第二次确认，才能升级为 MTR。

## 6. 统一父级复核卡

本卡是父级状态的补充记录，不单独建立订单。`parent_timeframe`、`range_state`、`decision_path` 等局部字段必须与完整案例的 canonical 证据头、结构、订单和状态轴一起保存；`parent_state` 使用统一枚举，不使用 `mature_range` 或 `climax_or_exhaustion` 作为替代值。

```text
contract_scope: deep_review / daily_candidate / historical_context_only
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
parent_timeframe:
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
range_upper_zone:
range_lower_zone:
range_midpoint:
left_major_levels:
directional_leg_quality:
current_location: upper_edge / lower_edge / middle / outside
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
abc_allowed: yes / conditional / no
second_leg_trap_risk: low / medium / high
breakout_acceptance_evidence:
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
direction: long / short / no_valid_direction
first_independent_obstacle:
decision_path: trend_contract / range_contract / wait_for_acceptance / no_trade
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
state_reset_condition:
```

`attempt_lineage`、`breakout_acceptance` 和 `decision` 不再作为活动 canonical 字段；分别使用 `lineage_status`/`lineage_id`、`breakout_acceptance_evidence`/`state_transition` 和 `decision_path` 加三条状态轴。订单分支、结构止损和空间由统一合同或订单基础层补填，不能因为父级状态卡写了 `direction` 就假设已授权。

## 7. 证据入口

区间边缘与失败突破框架见 [`交易区间边缘二次入场与失败突破`](../../research/range_edge_second_entry_framework_CN.md)，专项证据审计见 [`市场状态与父级背景视觉证据审计`](../../research/market_state_context_visual_evidence_audit_2026-08-24_CN.md)。本层只服务视觉研究，不把状态分类变成量化阈值、不修改 Codex Trading、不连接 Execution Agent。

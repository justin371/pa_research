# Daily / 4H / 1H / 15m 多周期视觉复核

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)。

这是 PA Research 的多周期基础层。它不把低周期当成高周期的“放大镜答案”，而是先确定父级背景、位置和结构，再判断低周期是在确认同一笔交易、重新定价原订单，还是形成一笔独立短线。

## 1. 四层职责

| 周期 | 主要职责 | 不能单独完成 |
| --- | --- | --- |
| Daily | 父级趋势/区间/过渡/高潮、主要高低点、事件、板块和主要位置 | 不能只用日线标签冻结精确成交 |
| 4H-like / 60m | A/B lineage、中间支撑阻力、回调是否受控、角色转换 | 不能把局部波动改写成 Daily H/L 计数 |
| 1H / 60m | 接受、跟随、回测和较宽的中间周期合同 | 不能用窄止损替代父级失效区 |
| 15m | 信号 K 穿越、开盘跳过、触发时序和局部跟随 | 不能创造高周期没有的背景、空间或主要障碍 |

如果没有原生 4H，使用 1H 聚合时写成 `4H-like / 60m aggregated proxy`，记录聚合口径；不能把它当作未经说明的原生 4H。

## 2. 先定父级，再下钻

```text
Daily 背景与主要位置
→ 4H-like/1H 是否仍属同一 A/B lineage
→ 高周期信号 K、边界和结构失效区
→ 1H/15m 确认、跟随或回测
→ 实际订单与成交
→ 父级止损、第一障碍、路径 R/R
```

不能从 15m 的漂亮 K 线开始，再为它寻找一个高周期故事。Daily 在宽区间中部时，15m H2-like 首先是区间内短线候选；Daily 的首阻力贴近触发时，低周期确认不能把高周期交易变成好交易。

## 3. 三种关系

### A. 低周期确认同一笔交易

高周期已经提供方向、位置、信号 K/结构边界、父级止损和首障碍，低周期只改善成交时序。此时：

- 15m/1H 没有穿过触发就没有成交；
- 低周期的跟随或回测支持确认，但不重写 thesis；
- 结构止损仍按高周期合同记录；
- 实际成交明显晚于触发时，重算首障碍和 R/R。

### B. 低周期自成交易

若高周期形态仍像，但日线空间太近、止损太宽或高周期触发尚未确认，低周期若要做，必须另立合同：

```text
parent_thesis: Daily/4H pattern-like
lower_thesis: 15m/1H local reaction
lower_entry / lower_stop / lower_target:
time_horizon: intraday / short-term
```

它不能被称为“低周期确认后，日线自然变合格”。两笔交易的入场、止损、目标、仓位、持有时间和结果分开。

### C. 周期冲突与重建

Daily/4H 在主要阻力下形成双高、三推或高潮警报，而 15m 只有一次刺破；或者高周期在区间中部、低周期短暂扩张；或者低周期止损明显窄于父级结构风险时，默认 `observation_only / valid_no_trade`。

等高周期接受/失败后再重建新合同。低周期不能悄悄覆盖父级方向、空间或止损。

## 4. 计数与订单协议

H1/H2/L1/L2 计数必须属于同一周期、同一回调 lineage。`Daily-H2`、`4H-H2` 和 `15m-H2` 分开记录，不能相加。

### 多头

```text
Daily/4H：强 A + 受控 B + 支撑/回测位置 + H1/H2 候选
1H：恢复接受、跟随或回测守住
15m：突破信号 K 高点，确认 buy-stop 时序
止损：Daily/4H 结构失效区；独立短线才可用低周期止损
目标：先看 Daily/4H 第一阻力，再看 MM
```

### 空头

```text
Daily/4H：强 A + 受控 B + 阻力/回测位置 + L1/L2 候选
1H：反弹失败、低点被接受
15m：跌破信号 K 低点，确认 sell-stop 或回测
止损：Daily/4H 结构失效区；不能用第一根阴线高点替代
目标：先看 Daily/4H 第一支撑，再看 MM
```

## 5. 开盘跳过、缺口和回测

订单合同必须先冻结 `gap_policy: accept_open / skip / flag_only / not_applicable`。如果开盘已经越过原 stop：

1. `gap_policy=skip` 时标记 `opening-skip / original-not-filled-or-fill-unknown`，原合同不成交；
2. `gap_policy=accept_open` 或 `flag_only` 时，记录实际可能成交价，不沿用理想触发，并重新计算止损、第一障碍和风险；
3. 只有实际开盘价通过方向、止损和空间复核，才可记录实际开盘路径；空间恶化或几何未通过就标为 `unproven`/观望；
4. 回到旧边界才另立 `limit-retest`；缺口被接受并跟随时，另立 BOP/gap-and-go 合同。

没有回到预先定义的结构区，就没有 limit-retest 成交。后来发生过的回测不能写回原来的 15m stop。

## 6. 止损、首障碍与 R/R

Daily/4H 的 H/L、ABC、MTR、BOP 或区间边缘交易，止损要覆盖父级失效区和正常测试空间；第一障碍按 Daily/4H 左侧结构排序；低周期局部位只能做管理信息。首障碍不足约 1R 时，父级合同降级或否决。

15m/1H 短线可以使用局部结构止损和局部第一障碍，但必须明确交易周期、仓位和失效条件。一旦低周期结构失效，不能用“Daily 还没反转”继续持有；结果也不能回写成 Daily pattern 的胜负。

## 7. 数据纪律

每次复核先写：

```text
contract_scope: deep_review
data_source: Futu OpenD / after-close public data / screenshot / other
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:
timeframes_seen: Daily / 4H-like / 60m / 15m
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
direction: long / short / no_valid_direction
```

实时、延迟和历史数据不能混称；低周期不完整时可以做 `pattern_like` 初筛，但不能声称实际触发或成交已经确认。

## 8. 统一字段

本层把父级与低周期的层级差异保留为补充字段，但完整记录仍必须使用统一合同的 canonical 字段。`parent_*`、`lower_*` 只说明证据来自哪个周期；它们不能替代顶层 `primary_pattern`、`signal_bar`、`structural_stop`、`first_independent_obstacle`、空间字段或分轴状态。

```text
parent_timeframe:
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
secondary_context:
parent_location:
left_structure_and_location:
parent_signal_bar:
signal_bar:
confirmation_bar:
new_trigger:
follow_through:
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
parent_structural_stop:
structural_invalidation:
structural_stop:
parent_first_independent_obstacle:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
parent_rough_R_R:
rough_R_R:
lower_timeframe:
lower_role: confirmation / independent-trade / reprice / observation
lower_signal_bar:
lower_trigger:
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
gap_policy: accept_open / skip / flag_only / not_applicable
lower_stop_if_independent:
lower_first_obstacle_if_independent:
lower_rough_R_R_if_independent:
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
failure_condition:
```

本补充卡中的 `actual_fill_or_open_skip` 只表示研究合同或历史回放的订单路径，不是券商或账户的真实交易日志；真实交易日志若存在，必须来自独立来源。

旧字段 `parent_pattern`、`actual_or_assumed_fill`、`gap_state` 和 `decision` 不再作为活动 canonical 输出；历史说明可保留，但新记录分别使用 `primary_pattern`、`actual_fill_or_open_skip`、`gap_policy` 以及 `research_state`/`trade_state`/`gate_result`。

## 9. 证据入口与边界

既有框架见 [`多周期 Price Action 视觉复核框架`](../../research/multitimeframe_visual_review_framework_CN.md)，事件/板块共同闸门见 [`财报、板块与多周期前置过滤`](../../research/event_sector_multitimeframe_cross_pattern_audit_CN.md)，专项审计见 [`多周期视觉复核证据审计`](../../research/multitimeframe_visual_evidence_gap_audit_2026-08-24_CN.md)。

本层只服务 PA Research 的视觉筛选与历史复核，不进入 Codex Trading，不创建量化扫描器，也不连接 Execution Agent。

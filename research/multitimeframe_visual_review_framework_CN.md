# 多周期 Price Action 视觉复核：Daily / 4H / 1H / 15m 分层框架 V0.1

状态：`visual-research / provisional / cross-timeframe / not-quantitative`

这份文件解决一个执行中很容易混淆的问题：高周期看到了一个 PA 候选，低周期出现了触发，到底是同一笔交易的确认，还是已经变成另一笔低周期交易。

核心原则是：**高周期决定背景、父级结构、主要位置和结构止损；低周期只负责确认时序，除非明确另立一个低周期交易合同。**

## 1. 四层职责

| 层级 | 主要任务 | 可以回答的问题 | 不能单独完成的事 |
| --- | --- | --- | --- |
| Daily | 父级状态、主要趋势/区间、主要高低点、事件和板块背景 | 这是开放趋势、区间、过渡、高潮还是主要位置？ | 不能只用日线标签决定成交价格 |
| 4H / 60m | 中间结构、A/B lineage、局部支撑阻力、趋势或区间过渡 | 日线候选内部的回调是否仍属于同一结构？ | 不能把中间周期的局部波动自动改写成日线 H/L 计数 |
| 1H / 60m | 确认突破、回测、压力变化和较宽的低周期合同 | 触发是否被接受？有没有跟随？ | 不能用 1H 窄止损替代日线父级失效区 |
| 15m | 具体时序、信号 K 突破、开盘重订、低周期跟随 | 订单是否真的穿过触发？是否从开盘跳过？ | 不能创造高周期没有的背景、空间或主要支撑阻力 |

如果数据源没有原生 4H，使用 1H 聚合时必须明确写成 `4H-like / 60m aggregated proxy`，记录聚合口径；不能把它称成未经说明的原生 4H，也不能把 Daily、4H 和 15m 的 H2 计数混在一起。

## 2. 先定父级，再下钻

每个候选按下面顺序复核：

```text
Daily 背景与主要位置
→ 4H/1H 是否仍是同一条 A/B lineage
→ Daily 或 4H 的信号 K / 结构边界
→ 1H/15m 是否出现真实确认
→ 订单合同与实际成交
→ 高周期结构止损、第一障碍、粗略 R/R
```

不能反过来从 15m 的一根漂亮 K 线开始，再为它寻找一个高周期故事。若 Daily 在宽区间中部，15m 的 H2-like 仍首先是区间内短线候选；若 Daily 已有主要阻力贴近触发，低周期确认不能把日线交易变成好交易。

## 3. 三种多周期关系

### 3.1 低周期确认：同一笔交易

这是默认分支。高周期已经提供：

- 可解释的背景和方向；
- 明确的支撑/阻力或回调位置；
- 已形成的信号 K、结构失效区和第一障碍；
- 低周期只等待触发、跟随或回测。

此时 15m/1H 的作用是改善时序和成交，而不是重新定义 thesis。结构止损仍按高周期合同记录；低周期提前触发、开盘跳过或没有跟随时，重新评估是否成交，但不能悄悄换成更窄的止损。

### 3.2 低周期自成交易：另一笔合同

当高周期形态仍然像，但日线第一障碍太近、日线止损太宽或高周期触发尚未确认时，低周期若要交易，必须明确改写为另一笔交易：

```text
parent_thesis: Daily/4H pattern-like
lower_thesis: 15m/1H local support-resistance reaction
lower_entry: 独立的低周期触发
lower_stop: 低周期结构失效区
lower_target: 低周期第一障碍
time_horizon: 短线/日内
```

它不能被称作“日线 H2 已经被低周期确认后自然变得合格”。两笔交易的入场、止损、目标、仓位和结果必须分开记录。

### 3.3 周期冲突：观望或重建

出现以下情况时，低周期信号不能强行覆盖高周期：

- Daily/4H 正在主要阻力下形成双高、三推或圆顶警报，但 15m 只有一次向上刺破；
- Daily/4H 仍在区间中部，15m 短暂出现趋势形状；
- 低周期向上确认，但高周期第一阻力只剩很小空间；
- 低周期向下确认，但高周期支撑已经贴近触发；
- 高周期结构止损远大于低周期局部波动，低周期入场只是人为压缩风险。

默认输出是 `pattern_like / valid_no_trade`，或者等高周期接受/失败后重建新合同。

## 4. 高周期信号与低周期触发的分工

### 多头 H1/H2 示例协议

```text
Daily/4H：强 A + 受控 B + 支撑位置 + H1/H2 候选
1H：价格重新站回确认区，出现跟随或回测守住
15m：突破信号 K 高点，确认 buy-stop 的真实时序
止损：Daily/4H 结构失效区；若改为低周期交易，另列窄止损合同
目标：先看 Daily/4H 第一阻力，再看 MM
```

### 空头 L1/L2 示例协议

```text
Daily/4H：强 A + 受控 B + 阻力位置 + L1/L2 候选
1H：反弹失败，低点结构开始接受
15m：跌破信号 K 低点，确认 sell-stop 或回测合同
止损：Daily/4H 结构失效区；不能用 15m 第一根阴线高点替代
目标：先看 Daily/4H 第一支撑，再看 MM
```

H1/H2 或 L1/L2 的计数必须属于同一个周期和同一个回调 lineage。15m 的 H2 不会自动成为 Daily 的 H2；如果两个周期各自都形成 H2，要写成 `Daily-H2` 与 `15m-H2`，不能相加。

## 5. 订单分支与跳空重订价

### A. 高周期 stop，低周期确认

- 高周期信号 K 已冻结，15m/1H 只用于确认是否穿过触发；
- 触发价、结构止损和第一障碍在高周期决策时先记录；
- 15m 没有触发就是没有成交；后续上涨/下跌不能证明原订单成交；
- 若实际成交明显晚于触发，重算第一障碍和 R/R。

### B. 开盘跳过原触发

如果 15m 或日线开盘已经越过原 stop：

1. 原合同标记 `opening-skip / original-not-filled-or-fill-unknown`；
2. 记录实际可能成交价，不沿用理想触发；
3. 重算结构止损、首障碍和风险；
4. 若空间恶化，观望；
5. 若价格回到旧边界，再另立 `limit-retest`；
6. 若接受跳空并继续跟随，可另立 BOP/gap-and-go 合同。

### C. 低周期回测 limit

低周期回测只有在结构区事先存在时才有效，例如旧阻力转支撑、旧支撑转阻力、缺口边缘或信号 K 的明确回测。没有回到区域就没有成交；不能把后来发生过的回测写回原来的 15m stop。

## 6. 止损、第一障碍与 R/R 的分层

### 6.1 日线/父级合同

若 thesis 是 Daily 或 4H 的 H1/H2、L1/L2、MTR、BOP 或区间边缘反转：

- 止损覆盖父级结构失效区和正常测试空间；
- 第一障碍按 Daily/4H 左侧主要结构排序；
- 15m 的局部障碍只能作为管理信息，不能替代高周期首障碍；
- 若首障碍不足约 1R，日线合同降级为 `borderline` 或 `valid_no_trade`；
- MM 只能在障碍被接受后作为后续目标。

### 6.2 低周期独立合同

若明确改成 15m/1H 的短线交易：

- 止损可以放在低周期局部结构外；
- 第一障碍必须从低周期方向重新排序；
- 目标、持有时间和仓位按短线合同定义；
- 结果不能回写成 Daily 形态的胜负；
- 一旦低周期结构失效，不能用“Daily 还没反转”来继续持有。

这两种合同可以在同一张图上并列，但不能共用一个 R/R 数字。

## 7. 多空案例审计

| 案例 | 高周期 thesis | 低周期作用 | 订单/风险结论 |
| --- | --- | --- | --- |
| [`TSLA 2025-08-06–08-22`](tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) | Daily 强-looking A、深但后段受控 B、支撑簇 H2；父级仍在更大恢复区间内 | 15m/60m 确认 H2 触发和跟随，没有创造高周期空间 | 日线结构止损宽、`340.25–340.55` 和 `348.68–357.54` 阻力近，标记 `daily-no-trade`；低周期可另列条件合同，不能合并 |
| [`NVDA 2024-09-11–09-25`](nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md) | Daily 强 A、深但后段受控 B、支撑处 H2 | `09-24` 60m/15m 先回测再越过 `116.81`，确认顺序清楚 | Daily 宽止损到 `120.6` 约 `0.9R`，低周期窄止损约 `1.9R`；这是两种合同的对照，不把窄 R/R 冒充日线 R/R |
| [`TSLA 2024-03-04–03-14`](tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | 区间上沿失败后的强空头 A、弱 B、Daily L2 | 15m/60m 证明 `2024-03-13` 的 L2 确实跌破触发并有跟随 | 15m 是确认，不是独立短线；结构止损约在 `182.87` 上方，后来先失效而左侧支撑晚到，记 `process-stop-first` |
| [`TSM 2025-02-14–03-28`](tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) | Daily 强 A、受控 B、L1-like 空头恢复 | 原 stop 被 `03-26` 开盘小缺口跳过；15m 用于开盘重订或确认重订 | `177.22` 原 stop 与旧价 limit 均不能假设成交；`176.66` 附近的 gap-reprice 是新合同，首支撑仍约 `1.6R+`，需独立记录 |
| [`QCOM 2024-07-17–07-30`](qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md) | 强空头 A 后 L1/L2-like，但事件和首支撑限制空间 | 低周期可以重建触发，但开盘重订后成交价恶化 | 理想触发约 `1.37R`，实际重订约 `0.48R`，且靠近财报前三天，正确输出是 `valid_no_trade` |
| [`GOOGL 2024-03-04–03-22`](googl_bullish_h1_gap_trigger_boundary_2024-03-04_2024-03-22.md) | 多头 A、浅 B、H1-like | 开盘跳空越过原 buy-stop，低周期不能恢复旧合同 | 实际成交、止损和首障碍必须重算；若不回测旧区，limit 不成交，保留观望 |

这些案例形成方向对称的结论：低周期确认可以提高时序清晰度，但不能消除高周期首障碍；跳空会改变订单合同，而不是自动否定整个视觉形态；低周期若要“救活”日线交易，必须明确承认已经换成另一笔交易。

## 8. 最小多周期复核卡

```text
contract_scope: deep_review / historical_context_only
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: historical_close / unknown
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
parent_timeframe: Daily / 4H-like / 1H
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
primary_pattern: ABC_CONT / BOP / RFB / MTR / other
secondary_context: parent_pattern_display / multi_timeframe_review
direction: long / short / no_valid_direction
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
parent_location: major support-resistance / range edge / middle / gap / channel
parent_signal_bar:
parent_structural_stop:
parent_first_independent_obstacle:
parent_pre_entry_space_R:
parent_space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
parent_rough_R_R:
structural_stop:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
rough_R_R:

lower_timeframe: 1H / 60m / 15m
lower_role: confirmation / independent-trade / reprice / observation
lower_signal_bar:
lower_trigger_or_zone:
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
gap_state: none / opening-skip / gap-accepted / retest / unknown
lower_structural_stop_if_independent:
lower_first_independent_obstacle_if_independent:
lower_rough_R_R_if_independent:

signal_bar:
confirmation_bar:
new_trigger:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
gap_policy: accept_open / skip / flag_only / not_applicable
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
failure_condition:
```

`parent_timeframe`、`parent_location`、`lower_timeframe`、`lower_role` 和
`gap_state` 是多周期复核的补充字段。旧的 `parent_pattern`、
`parent_first_obstacle`、`actual_or_assumed_fill` 和 `decision` 只作为历史显示
语义，新的复核卡分别使用 `primary_pattern`、
`parent_first_independent_obstacle`、`actual_fill_or_open_skip` 和三条状态轴。

## 9. 可迁移结论

1. Daily/4H/1H 先决定背景、父级结构、主要位置和风险；15m 先默认只是触发确认。
2. 低周期 H/L 计数不与高周期计数相加；每个计数必须属于同一周期、同一回调 lineage。
3. 低周期窄止损只能说明另一笔短线交易的几何，不能把高周期宽止损压窄。
4. 高周期第一障碍优先于低周期局部目标和 MM；低周期确认不能创造不存在的空间。
5. 开盘跳过 stop 后，旧合同立即进入未成交/成交未知状态；重订价、回测和 BOP 是不同合同。
6. 如果低周期方向与高周期冲突，默认观望；只有明确改变持有周期、止损、目标和订单分支，才可以建立低周期独立交易。
7. 实时数据、历史收盘数据和浏览器图表的可靠程度要写清楚；不能把低周期不完整数据说成已经看到了完整触发。

## 10. 当前状态与停止条件

当前框架保持 `provisional`。它可用于视觉筛选、历史复核和人工交易计划，不进入 Codex Trading 或 Execution Agent。

只有在后续案例提供以下新信息时才继续增加深审：

- 同一高周期 pattern 的多空对照，且低周期确认和父级止损均可重建；
- 一个低周期独立交易与同图高周期交易的明确对照；
- 一个原 stop 被跳空改变、回测 limit 未成交或 BOP 重建的路径样本；
- 能清楚证明首障碍、实际成交和 R/R，而不是只凭日线收盘结果。

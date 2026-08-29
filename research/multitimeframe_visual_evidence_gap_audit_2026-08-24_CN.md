# Daily / 4H / 1H / 15m 多周期视觉证据审计

日期：`2026-08-24`  
状态：`visual-research / cross-timeframe / provisional / not-statistical`

## 审计目的

检查低周期信息是否真正服务高周期 PA 判断，还是被用来制造更漂亮的成交价和更窄的止损。核心顺序是：

```text
父级背景/位置 → 高周期结构与订单 → 低周期确认或独立合同
→ 实际成交/跳空重订 → 父级或低周期 R/R → 路径结果
```

## 工作合同

### C1：高周期决定父级

Daily/4H 负责趋势、区间、A/B lineage、主要高低点、事件/板块背景、结构止损和首障碍；15m 不能创造不存在的空间。

### C2：低周期默认是确认

高周期 thesis、信号 K 和风险已冻结时，低周期只确认穿越、跟随、回测或真实成交。没有穿越就是没有成交；后续结果不回写原订单。

### C3：独立低周期必须改名

高周期 no-trade 但低周期另有交易时，必须记录 lower thesis、低周期止损、目标、持有时间和仓位。不能把窄低周期 R/R 叫成日线 R/R，也不能把低周期结果算进日线 pattern。

### C4：周期计数不混合

`Daily-H2`、`4H-H2` 和 `15m-H2` 分开记录；同一回调 lineage 只有在同一周期内才可数 H1/H2/L1/L2。周期转换、区间重置或结构接受后必须重建计数。

### C5：开盘/跳空重订

原 stop 被开盘跳过时，旧合同进入 `opening-skip`；按实际价格重算。回测 limit、gap-and-go、BOP 和原 stop 是不同合同，不能混算。

## 案例矩阵

| 案例 | 高周期合同 | 低周期角色 | 审计结论 |
| --- | --- | --- | --- |
| TSLA `2025-08-06`–`2025-08-22` | Daily H2-like、支撑处恢复，但高周期阻力 `340.25–340.55`、`348.68–357.54` 近 | 15m/60m 核对触发与跟随 | 低周期不能修复日线首障碍；`daily-no-trade`，若做短线必须另立合同 |
| NVDA `2024-09-11`–`2024-09-25` | Daily 强 A、深 B 后 H2，父级结构清楚 | `60m/15m` 回测后越过 `116.81`，确认时序 | 低周期约 `1.9R` 与 Daily 约 `0.9R` 是两种几何，不能合并成一个胜负 |
| TSLA `2024-03-04`–`2024-03-14` | 区间上沿失败后的强空头 A、弱 B、Daily L2 | 15m/60m 证明 `2024-03-13` 下破和跟随 | 低周期是同一 Daily 合同的确认；结构止损后来先失效，记 `process-stop-first` |
| TSM `2025-02-14`–`2025-03-28` | Daily 强空头 A、受控 B、L1-like | 原 stop 被 `2025-03-26` 开盘小缺口跳过；低周期用于重订/确认 | `177.22` 不能假设成交；`176.66` 附近是新 gap-reprice 合同，首支撑仍需独立重算 |
| QCOM `2024-07-17`–`2024-07-30` | Daily 空头 L1/L2-like，首支撑和财报窗口拥挤 | 低周期可重建触发，但不能改变事件/空间 | 理想几何约 `1.37R`，重订后约 `0.48R`；正确状态 `valid_no_trade` |
| GOOGL `2024-03-04`–`2024-03-22` | Daily 多头 A、浅 B、H1-like | 开盘跳空越过原 buy-stop；低周期不能恢复旧合同 | 需要实际成交/重算；不回测旧区就没有 limit 成交 |
| VRT `2026-04-14`–`2026-04-20` | Daily/4H-like 深 B 后 H1-like，父级含缺口冲击 | `2026-04-17` 15m 重新触发 | 晚触发到 `310.94–312.40` 只有约 `0.42–0.53R`；低周期确认仍被高周期首障碍否决 |
| MAR `2026-06-18`–`2026-06-25` | 4H-like A/B/L1-L2-like，但父级转弱 | 低周期只能补局部顺序 | `377.8–380.8` 支撑簇离触发太近，约 `0.04–0.3R`；标记跨周期首支撑 no-trade |

## 四个必须保留的对照

### 1. 高周期合同被低周期确认

TSLA `2024-03` 和 NVDA `2024-09` 都可以把低周期写成确认层，但结论不同：TSLA 的确认不改变父级结构止损，后续路径仍先失效；NVDA 的低周期窄风险看起来更好，却不能被称为 Daily 合同的 R/R。这说明确认提高的是时序清晰度，不是自动提高父级空间。

### 2. 低周期独立交易不能替代高周期

TSLA `2025-08` 和 VRT `2026-04` 都有低周期恢复外观，但高周期首障碍太近。若低周期确实形成短线，只能用 lower thesis、lower stop、lower target 另记；不能把结果倒灌成日线 H2 已经合格。

### 3. 开盘/跳空导致订单重订

TSM 和 GOOGL 说明原 stop 被跳过时，旧合同不能按理想价补成交。可以等实际回测、允许 gap-reprice 或建立 BOP，但每种分支都要重新计算成交、止损、第一障碍和 R/R。

### 4. 高周期首障碍先否决低周期

QCOM、VRT 和 MAR 说明低周期越精细，越容易把入场放在首障碍附近；如果高周期首障碍空间不足，正确输出是 no-trade，而不是继续找更窄止损。

## 统一记录字段

```text
contract_scope: deep_review / historical_context_only
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: historical_close / unknown
timeframes_seen:
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
parent_timeframe:
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
parent_location:
direction: long / short / no_valid_direction
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
parent_signal_bar:
parent_order_branch:
parent_actual_fill_or_open_skip:
parent_structural_stop:
parent_first_independent_obstacle:
parent_pre_entry_space_R:
parent_space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
lower_timeframe:
lower_role: confirmation / independent-trade / reprice / observation
lower_signal_and_trigger:
lower_actual_fill_or_open_skip:
lower_stop_and_first_obstacle_if_independent:
gap_or_opening_skip:
event_context:
event_bucket:
sector_reference:
market_reference:
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
failure_condition:
```

## 当前结论

可迁移原则是：高周期先决定背景、位置、父级风险和首障碍；低周期默认只确认时序；独立低周期必须重建合同；计数不能跨周期相加；跳空必须重订；低周期窄止损不能修复高周期坏 R/R；后续结果不能倒灌当时的判断。

本层仍为 `provisional`，不产生胜率、不进入 Codex Trading、不连接 Execution Agent。只有在同一高周期 pattern 有多空、确认/独立交易/重订/否决的对称可重建路径时，才继续增加深审。

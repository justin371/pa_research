# 财报、板块与多周期前置过滤 V0.1

日期：2026-08-23  
文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。

## 目的

这是一层进入八个 pattern 之前的共同背景过滤，不是新的 pattern，也不是评分器。它回答三个问题：

1. 这段 K 线是不是被财报或重大事件重新定价？
2. 个股方向是否得到所属板块和大盘的许可？
3. Daily/4H/60m 的父级结构，是否真的被 15m 的触发确认，而不是被低周期噪音倒推出来？

## 前置闸门顺序

```text
数据状态与来源
→ 财报/重大事件窗口
→ 板块与大盘方向许可
→ Daily 父级背景和主要位置
→ 4H/60m A/B lineage 与中间结构
→ 15m 触发、回测和实际成交
→ pattern-specific 审计
```

前置闸门不替代 pattern 判断：它只决定候选是否可以进入下一层，以及需要降级、拆成事件样本或直接观望。

## 数据状态

每次复核先写：

```text
contract_scope: deep_review
data_source: Futu OpenD / after-close public data / chart screenshot / other
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:
timeframes_seen: Daily / 4H-like / 60m / 15m
direction: long / short / no_valid_direction
```

- 收盘后公开数据可以做历史视觉复核，但不能写成实时行情；
- Futu OpenD 只有在连接、权限和具体返回周期都确认后，才可标记 `live_confirmed`；
- 浏览器或图表卡片只显示概览时，不能假装已经获得完整 15m/60m 触发；
- 数据不完整时可以做 `pattern_like` 初筛，但不能声称实际订单已触发或成交。

## 财报与重大事件规则

- 已知财报在未来三个交易 session 内：不新开仓，不赌财报；候选直接进入 `valid_no_trade` 或 `event_pending`；
- 已有仓位的管理是另一个问题，不得把持仓管理悄悄当成新入场；
- 财报后的跳空可以说明买压/卖压很强，但要标成 `event_driven`，不能与普通 PA K 线混成基准；
- 宏观数据、监管消息、并购、产品发布等重大事件也要单独标记；如果事件时间和影响不清楚，保留 `pending`；
- 事件窗口不能只因为方向后来正确就被删除。事件是证据质量和订单几何的一部分。

## 板块与大盘许可

### 最小记录

```text
sector_reference: SOXX / SMH / XLV / XLF / XLY / other / unknown
sector_state: aligned / mixed / counter / unknown
market_reference: SPY / QQQ / relevant_index / unknown
market_state: aligned / mixed / counter / unknown
permission: long_allowed / short_allowed / both_allowed / no_direction / unknown
```

- 半导体个股优先参考 SOXX 或 SMH；不要把两者的短线不同步假装成完全一致；
- 其他行业使用最相关的 ETF 或指数；不知道对应关系时写 `unknown`，不凭感觉补；
- 板块和大盘顺势是许可/加分项，不是单独入场信号；
- 个股逆板块并非绝对禁止，但需要更清楚的主要位置、结构、二次确认和空间；若证据不足，降级为 `observation_only`；
- 板块走弱不能自动否定个股多头，但它会降低 H1/L1 的优先级，要求 H2、支撑反应或更强确认；反向同理。

## 多周期职责

| 周期 | 必须负责 | 不能替代 |
| --- | --- | --- |
| Daily | 父级趋势/区间/过渡、主要高低点、事件和板块背景、主要位置 | 不能单独冻结精确成交价 |
| 4H-like / 60m | A/B lineage、中间支撑阻力、回调是否仍受控、角色转换 | 不能把局部波动改写成 Daily H/L 计数 |
| 1H / 60m | 接受、回测、跟随和较宽的低周期合同 | 不能用窄止损替代 Daily/4H 结构风险 |
| 15m | 信号 K 穿越、开盘跳过、实际触发顺序 | 不能创造高周期没有的背景、空间或主要障碍 |

默认关系是“低周期确认同一高周期合同”。如果低周期有自己的入场、止损、目标和持有周期，必须写成另一笔合同；它的结果不能回写成 Daily pattern 的结果。

## 对八个 Pattern 的影响

| Pattern | 财报/事件处理 | 板块/市场处理 | 多周期重点 |
| --- | --- | --- | --- |
| H1/L1 | 财报前三个 session 不新开；事件后强 A 标记 `event_driven` | 逆板块时不把第一次尝试当默认优先 | Daily 强 A/B/位置；15m 只确认信号 K |
| H2/L2 | 事件污染时等待事件后重新建立回调 lineage | 板块逆向时更倾向等 H2/L2 而非 H1/L1，或观望 | 60m/15m 确认第二次尝试；不能改变父级止损 |
| ABC 延续 | 财报跳空不能直接当普通 A；B/C 需重新标记 | 板块顺势支持延续，但不取消首障碍 | Daily A/B/C；低周期仅确认 C 或另立短线合同 |
| 区间边缘 | 事件前区间边缘不新开；事件跳空需单列失败/BOP | 板块方向不是区间边缘的独立入场信号 | Daily 确认上下沿；低周期只确认边缘反应/回测 |
| 失败突破/高潮 | 财报造成的扩张先标事件，不直接叫普通高潮反转 | 逆板块失败突破需要更强第二次确认 | 高周期边界接受/拒绝优先；15m 不单独定义失败 |
| BOP | 事件 gap-and-go 是独立 BOP 合同，不能沿用旧 stop | 板块同步有助于接受判断；不顺势时等回踩和跟随 | Daily/4H 旧边界接受；15m 确认回踩、实际成交和重订价 |
| MTR | 事件反向跳空不能单独证明控制权改变 | 逆板块 MTR 要求主要位置、结构破坏和二次确认 | Daily/4H 结构破坏优先；低周期只补触发 |
| 三推/H3-L3 | 事件扩张不计作普通衰竭证据 | 板块同步/反向帮助区分扩张延续与短线反应，但不是决定条件 | 同一周期数 lineage；低周期不能凭结果补第三推 |

## 统一降级规则

出现以下任一项时，不把候选直接升级为可交易：

- 财报前三个交易 session 内；
- 事件跳空与普通 K 线证据尚未分开；
- 板块/大盘方向明显相反，而 pattern 只有一次尝试；
- Daily/4H 在主要阻力或支撑下，15m 才出现相反方向信号；
- 15m/60m 数据不完整，无法确认是否真实穿过触发价；
- 低周期止损比父级结构窄，却没有明确声明已经换成独立低周期合同；
- 实际开盘已跳过原 stop，成交、首障碍或 R/R 未重新计算。

输出可以是 `pattern_like / observation_only`、`valid_no_trade` 或 `pending`，而不是强行给出入场。

## 案例对照

| 案例 | 前置过滤教训 |
| --- | --- |
| [`AAPL 2024-05-03–05-09`](aapl_bullish_h1_event_driven_a_2024-05-03_2024-05-09.md) | 事件后强 A 可以作为条件候选，但必须与普通 A 分组，并保留事件字段 |
| [`LRCX 2024-07-10–07-25`](lrcx_bearish_abc_l1_gap_first_support_2024-07-10_2024-07-25.md) | SOXX/SMH 同步增强方向，但开盘重订和首支撑仍使合同偏边界 |
| [`QCOM 2024-07-17–07-30`](qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md) | 方向和板块可以同向，实际重订价与财报窗口仍能否决交易 |
| [`NVDA 2024-09-11–09-25`](nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md) | SOXX 同向、低周期触发清楚，但低周期窄 R/R 不能冒充日线宽止损 |
| [`JNJ 2025-08-01–09-02`](jnj_bullish_h1_opening_skip_first_obstacle_boundary_2025-08-01_2025-09-02.md) | XLV 顺势也不能取消开盘跳过、前高簇和首阻力拥挤 |

## 最小前置卡

```text
data_source:
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
earnings_next_three_sessions: yes / no / unknown
event_context: none / earnings / macro / gap / other / unknown
sector_reference:
sector_state: aligned / mixed / counter / unknown
market_reference:
market_state: aligned / mixed / counter / unknown
parent_timeframe: Daily / 4H-like / 60m
lower_timeframe: 1H / 60m / 15m / none
lower_role: confirmation / independent-contract / reprice / observation
permission: long_allowed / short_allowed / both_allowed / no_direction / unknown
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

## 边界

本框架只服务视觉研究和人工交易计划。它不预测财报、不替代风险管理、不创建量化分数、不修改 Codex Trading，也不连接 Execution Agent。

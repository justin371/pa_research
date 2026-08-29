# Channel / 通道

文档状态：`document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补通道边界、推进/回调和状态切换。通道线不能替代结构止损、第一独立障碍或 `direction`。

Channel 研究的是有方向的价格运行及其状态变化。它不是把任意两点连成两条线，也不是把交易区间中部的摆动重新命名为趋势。先判断通道是否已经被当时的证据确认，再决定 H/L、边缘交易、突破或反向分支。

## 共同图表范围前置

该入口的证据头还必须记录 `data_status: historical / delayed / live_confirmed / incomplete`、`as_of_time`、`chart_scope`、`daily_context_window` 和 `timeframes_seen`；历史、延迟、实时已确认与不完整不能互换。

状态边界：关键图表、事件、触发或空间证据尚不完整时使用 `pending`/`observation_only`；形态、方向和入场几何已可复核但已知硬闸门否决交易时使用 `valid_no_trade`。两者都不建立订单，不能互换。

统一合同映射：本目录的 Channel 是独立通道状态研究语义；若 `contract_scope: daily_candidate`，`primary_pattern` 仍只写 `ABC_CONT` 或 `BOP`，H1/L1/H2/L2/H3/L3 写入 `internal_label`，其他关系写入 `secondary_context`，`range_edge_three_push` 仅作位置分支。通道名称只在深审/历史记录的独立主题字段或兼容 `other` 中保留，不能扩展日线选股主标签。

BOP 状态迁移：若事前可见边界被日线强收盘越过、获得跟随并在回踩中守住，统一合同改写为 `primary_pattern: BOP`、`state_transition: breakout_acceptance`；本目录的原 pattern/反向 thesis 与旧订单合同失效，必须重建 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间，不能沿用旧 entry/stop/target 或把旧结果并入 BOP。

进入 Channel 判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。强 A 与受控 B 用于判断通道的方向性和压力变化；通道边界仍按本目录独立定义。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能凭两点连线或局部通道升级为可交易候选。

## 最小定义

```text
方向性运行
→ 多次同向推进与回调
→ 上下边界大致平行、价格反复在其中运行
→ 判断紧通道 / 宽通道 / 区间 / 状态过渡
→ 选择顺势、边缘、突破或观望合同
```

### 紧通道

- 方向性压力持续，回调浅，重叠少，收盘常靠趋势方向一侧；
- 反向尝试容易快速失败，默认尊重趋势惯性；
- 中途出现的 H1/L1 可以研究，但不能忽略信号 K、止损和第一独立障碍；
- 只要回调变深、重叠明显增加或反向价格开始被接受，就降低“紧通道延续”的把握。

### 宽通道

- 仍有坡度和方向，但回调更深、重叠更多，上下边界被反复测试；
- 上沿、下沿和中线的交易含义不同；中部通常不追单；
- 宽通道可能是宽旗形，也可能逐步转成交易区间；不能自动等同 MTR 或三推楔形；
- 三次测试若第三次扩张，不记录为“逐推减弱”的反转形态，而记录为扩张/延续边界。

### 尚未确认的通道

- 只有两点连线、没有平行的另一侧边界：先称为趋势线候选；
- 只有一根强 K 或一次跳空：先称为冲量/重新定价；
- 区间边界水平化、双方反复穿越中线：优先使用区间逻辑；
- 不能用后面画出的漂亮通道，倒推当时已经存在成熟通道。

## 状态与处理

| 状态 | 当时可见证据 | 默认处理 |
| --- | --- | --- |
| `tight-trend-channel` | 浅回调、少重叠、同向收盘和跟随 | 优先顺势；边界或有意义支撑/阻力处研究 H1/H2、L1/L2 |
| `broad-channel` | 深回调、重叠增加、上下沿反复但仍有坡度 | 位置优先；边缘可研究，中部观望 |
| `channel-end-expansion` | 末端推进变宽、第三次测试更强或范围扩张 | 不宣称衰竭；等待失败/第二次确认，首障碍近则 no-trade |
| `channel-breakout-acceptance` | 强收盘离开边界、后续跟随、回踩守住旧边界 | 转 BOP/新趋势合同，旧通道反向假设失效 |
| `channel-to-range-transition` | 边界趋平、双方反复、价格频繁穿越中线 | 改用区间边缘逻辑；中部 H/L 不交易 |
| `channel-break-failure` | 只刺破边界、没有跟随，又回到通道内 | 只保留观察或失败突破候选，不立即反向追单 |

“通道变宽”是状态变化证据，不是空头或多头反转信号本身。主要反转仍需要强反向压力、结构破坏、第二次确认和足够空间。

## H/L 与订单

- 紧通道中的浅回调恢复，可保留顺势 H1/L1；两腿或更深回调，H1/L1 降级，才考虑位置良好的 H2/L2。
- 宽通道边缘的 H2/L2 不能自动当作开放趋势二次入场；必须先说明它是边缘反应、通道内延续，还是突破后的新趋势。
- 中线或宽通道中部的局部 H/L 通常只记为观察，避免把普通摆动计数成方向性回调。
- 通道末端反向交易需要边界失败、反向压力、第二次确认和足够空间；第一次趋势线刺破不是 MTR 授权。

订单分支：

1. `stop-confirmation`：信号 K 外等确认，适合边缘反应、紧通道回调恢复或边界外接受；
2. `limit-retest`：只有旧边界已经完成角色转换，且等待回测的价格和失效点事前冻结时使用；
3. `market/close-confirmation`：通道外强收盘和跟随已经出现，但要接受更宽止损；
4. `observation_only`：通道未确认、中部、扩张不清、开盘跳过但尚未重建合同，或首障碍/止损尚未确认。

结构止损必须放在最近有意义回调、通道边界和最后一次测试极端外，而不是单根小 K 线里面。目标先看入场前已知的独立支撑/阻力或另一侧通道边界，再看 MM/AB=CD。即使方向后来正确，只要第一障碍不足约 1R，仍记为 `valid_no_trade`；完整波段约 2R 只是研究参考，不是固定胜率规则。

## 与相邻 pattern 的边界

- **ABC/H1-H2**：通道中段的局部 A/B 若逐渐变宽，应降级为宽通道，不强行维持简单 ABC；区间中不继承趋势腿数。
- **交易区间**：边界趋平、双方反复和中线穿越占主导时，通道状态结束，边缘优先。
- **BOP**：边界外强收盘、跟随和回踩接受后，改用突破合同。
- **MTR / 三推**：通道破坏和第二次确认才支持 MTR；第三次测试要区分减弱与扩张。
- **Final Flag**：趋势末端的小压缩可能是最终旗形，但通道变窄本身不等于 Final Flag。

## 当前案例入口

- [`KLAC 2025-03-17–03-26`](../../research/klac_h3_bear_flag_case_2025-03-12_2025-03-28.md)：宽熊旗上沿的条件性空头恢复；支持边缘顺势，不支持中部追空；
- [`TSLA 2025-08-22–08-25`](../../research/tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md)：强趋势和上方趋势线候选，但平行下边界未确认，不能事后命名成熟通道；
- [`XOM 2024-07-25–08-02`](../../research/xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md)：宽通道/旗形第三次测试扩张，订单跳空与首支撑共同否决；
- [`UBER 2024-07-17–07-26`](../../research/uber_bearish_h3_l2_first_support_boundary_2024-07-17_2024-07-26.md)：H3-like 计数复杂、通道扩张和首支撑拥挤；
- [`COIN 2024-01-02–01-12`](../../research/coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md)：宽旗/通道与开盘重订、首支撑边界对照。

专项证据审计见 [`Channel 专项视觉证据审计`](../../research/channel_visual_evidence_gap_audit_2026-08-24_CN.md)，基础框架见 [`通道视觉研究框架`](../../research/channel_visual_framework_CN.md)。

本目录只服务 PA Research 的视觉识别、案例复核、订单语义和 no-trade 判断，不建立量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

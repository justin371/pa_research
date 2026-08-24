# 完整图表视觉复核工作流边界审计

日期：`2026-08-24`  
状态：`workflow / visual-first / provisional / not-quantitative`

这份文件验证更新后的 review card 是否能把“图形像不像”和“是否值得建立交易合同”分开。它不测试胜率，也不创建扫描器；它只检查视觉助手的输出顺序、主/次标签、多周期职责和停止条件。

## 1. 标准工作流

```text
完整图表
→ 快筛：父级、主要位置、A/B、lineage、候选形态
→ 选一个 primary_pattern
→ 记录 secondary_context 与 state_transition
→ 若新信息值得投入，再深审信号/订单/止损/首障碍
→ 输出 research_candidate / research_positive_conditional / observation_only / valid_no_trade
```

### 快筛必须回答

1. 当前是开放趋势、成熟区间、边缘、通道、过渡、高潮还是已接受突破？
2. 左侧最重要的主要高点/低点和支撑阻力在哪里？
3. A 是否有方向性？B 是受控、深但后段受控、失控还是区间化？
4. 当前形状最合理的一个主标签是什么？是否存在计数重置或尺度歧义？
5. 首障碍是否肉眼已近、事件/开盘是否会重订合同？

### 深审只在以下情况下触发

- 快筛明确为 `pattern_like`，且主标签和父级没有根本冲突；
- 案例能补当前证据缺口，例如订单重订、状态切换、低周期确认或首障碍几何；
- 形态虽然有边界，但能帮助定义“为什么不做”。

若只是又一张同质“强 A + H2-like + 首阻力太近”的图，保留引用，不重复建立深审文件。

## 2. 主/次标签验收规则

| 观察到的内容 | 主标签 | 次标签 | 不能做的事 |
| --- | --- | --- | --- |
| 成熟区间上沿二次测试 | `range_edge_second_entry` | `double_top`、`H2_like` | 不把区间中部后续摆动接回开放趋势 ABC |
| 边界外强收盘、跟随、回测守住 | `BOP_acceptance` | `former_double_top`、`former_triangle` | 不继续使用旧反向合同 |
| 强 A、受控 B、第一次恢复 | `H1/L1` 或 `ABC` | `signal_sequence` | 不因 EMA 触碰自动入场 |
| 第一次尝试失败后同一回调第二次尝试 | `H2/L2` | `ABC` | 不把区间边缘第二次机会和开放趋势 H2 混写 |
| 第三次压力测试 | `three_push/H3/L3` | `MTR_candidate` 或 `channel_continuation` | 不因次数到三自动做反向 |
| 三次测试范围外扩 | `expanding_boundary` | `H3_like`、`climax_candidate` | 不改写成逐推衰竭 |
| 头部/肩部和真实颈线 | `head_shoulders_candidate` | `double_top_bottom`、`MTR_candidate` | 不把三个点或圆弧当确认 |
| 连续波动收缩、pivot 和相对强度 | `VCP` | `PA_context` | 不和 H2/三推/ABC 合并计数 |

## 3. 多周期工作流

```text
Daily: parent_state / 主要位置 / 主要高低点 / 事件与板块
4H or 60m: A-B lineage / 中间结构 / 过渡
1H: 接受、回测、较宽确认
15m: 触发时序、开盘跳过、低周期跟随
```

高周期决定 thesis 和结构止损，低周期默认只确认时序。若低周期自成一笔交易，必须另立：

```text
parent_thesis
lower_thesis
lower_entry / lower_stop / lower_first_obstacle
holding_horizon
```

不同周期的 H2/L2 不相加；15m 不能创造 Daily 没有的空间。原 stop 被开盘跳过时，原合同标为 `open_skip`，必须重算新成交、止损、首障碍和 R/R。

## 4. 案例演练

### 4.1 TSLA `2025-09-08–09-12`

快筛：阻力下双高/三推/Final Flag-like 压缩。  
主标签：早期 `resistance_test`，突破后切换 `BOP_acceptance`。  
次标签：`former_double_top`、`former_three_push`。  
关键状态：`09-11` 强收盘、15m 跟随、回测守住。  
输出：旧反向合同失效；后续交易必须用 BOP/回踩合同。不能把完整图表的后续上涨倒灌成 `09-08` 已经是买点。

### 4.2 KLAC `2025-05-30–06-03`

快筛：上涨背景、深但后段稳定 B、支撑和 EMA20 汇聚，H2-like。  
主标签：`H2_within_ABC`。  
次标签：`support_retest`、`EMA_confluence`、可能的 `inside_like_pending_ohlc`。  
深审：`06-03` 越过 `06-02` 高点的确认路径清楚，但结构止损约 `72`，第一阻力约 `79.03–79.79`，日线空间边界明显。  
输出：`research_positive_conditional` 或 `valid_no_trade` 取决于所选周期合同；不能把低周期确认冒充日线宽 R/R。

### 4.3 RBLX `2024-03-18–04-05`

快筛：宽区间下沿双底/逆头肩/三角形/ABC-like 外观。  
主标签：`range_edge_second_entry / failed_breakout`。  
次标签：`double_bottom_like`、`triangle_like`。  
深审：`04-04` 上冲后收弱，区间中部 `37.3–37.8` 成为首磁铁，开盘还跳过原 buy stop。  
输出：`valid_no_trade`。不能为获得一个正例而选择最有利的标签。

### 4.4 ASML `2025-05-19–06-13`

快筛：两个低位测试、圆底/逆头肩/三推样和区间过渡同时出现。  
主标签：`range_transition / range_inside_range`。  
次标签：`double_bottom_like`、`rounded_bottom_like`。  
输出：`observation_only`，因为颈线、第三结构点和反向二次确认不完整。不能用 60m 小摆动制造 Daily MTR。

### 4.5 XOM/COIN `2024`

快筛：多次高位测试、H3-like、宽通道/三角形-like。  
主标签：`expanding_boundary / continuation_or_climax`。  
次标签：`H3_like`、`channel_edge`。  
深审：第三次范围扩张、跳空重订、首支撑拥挤。  
输出：`valid_no_trade`；扩张不能倒灌成三推衰竭。

### 4.6 VCP 独立体系

快筛：连续波动收缩、pivot、相对强度、市场环境和成交量行为符合 Minervini/SEPA 研究入口。  
主标签：`VCP`。  
次标签：`PA_context`，例如趋势、支撑阻力或 BOP。  
输出：不把 VCP 收缩次数转换成 H2/三推计数；订单和目标按 VCP 自己的研究合同与共同风险层复核。

## 5. 统一停止条件

在以下任一条件出现时，review card 可以停止深审：

- 主标签无法在父级状态和位置上自洽，只能依赖后见之明；
- 多个标签只是同一价格簇的不同说法，不能找到主合同；
- 第一独立支撑/阻力不足约 `1R`；
- 结构止损必须放在正常测试范围内部；
- 财报前三个交易日、重大事件或开盘跳空使原合同不可靠；
- 低周期触发存在，但高周期 thesis 没有空间，或实际成交已被跳空重订；
- 形态像，但尚无母 K/颈线/边界/lineage 等关键证据。

停止时的输出必须说明“为什么不做”，而不是只写“形态不够漂亮”。

## 6. 当前结论

这张 review card 的最小工作合同已经固定为：

```text
full_context → primary_pattern → secondary_context
→ state_transition → order_contract → first_obstacle
→ trade_state → unresolved_question
```

它能把“视觉识别”与“交易可行性”分开，也能保留模糊候选而不假装精确。当前仍是研究工具，不是自动下单规则、量化评分器或实时行情接口。

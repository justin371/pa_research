# Inside Bar / 两根 K 线反转视觉边界复核

日期：`2026-08-24`  
状态：`visual-research / provisional / not-statistical`

这份复核把四种容易混淆的现象分开：严格 Inside Bar、二内包/IOI、两根 K 线反转，以及 H1/H2 或 L1/L2 的 setup—signal—trigger 序列。它不把小实体、长影线或“看起来被包住”直接当成交易信号。

## 1. 严格定义与边界

母 K 为 `mother`，内包 K 为 `inside` 时，严格 Inside Bar 至少满足：

```text
inside.high <= mother.high
inside.low  >= mother.low
```

比较的是整根 K 的高低点，不是实体。影线越过母 K 时，不是严格 Inside Bar；母 K 或内包高低点没有冻结时，只能记为 `inside-like / pending-ohlc`。

- `ii`：连续两根内包，描述更长的平衡/压缩；
- `ioi`：内包—外包—内包，描述范围重新扩张后再次收缩；
- 两根 K 线反转：第一根推动/测试某方向，第二根在有意义的位置拒绝该方向并向另一侧收盘；它不要求存在母 K 包含关系；
- H1/H2、L1/L2：数的是回调中的有意义尝试，不是内包数量。

这四者可以重叠，但名称不能替代父级状态、位置、触发、跟随和空间。

## 2. 决策时点状态机

```text
完整背景
→ 冻结母 K/内包或两根 K 的整根范围
→ 判断趋势、通道、区间、边缘或过渡
→ 区分 setup/count、signal、trigger
→ 等待突破接受、反向跟随或第二次确认
→ 冻结订单、结构止损、首障碍与 R/R
```

| 状态 | 证据 | 默认处理 |
| --- | --- | --- |
| `pause-continuation` | 趋势中压缩，原方向收盘和跟随仍占优 | 顺势等待突破/回测，不逆势猜反转 |
| `two-bar-reversal-candidate` | 关键位置的测试/推动后，第二根明显拒绝并收回 | 先等 stop 或第二次确认，不直接称 MTR |
| `inside-breakout-candidate` | 母 K/内包范围冻结，某侧突破并开始接受 | 分开记录延续、回踩和失败突破 |
| `range-middle-noise` | 区间中部压缩或两根相反 K | 默认观望，不把局部波动当趋势启动 |
| `pending-ohlc` | 只有图形外观，没有完整母 K 高低点 | 只保留候选，不升级严格定义 |

内包的方向由哪一侧突破后被接受决定，而不是由内包本身决定。第一根反向 K 也只是反转尝试；需要结构破坏、跟随/二次确认和空间，才可升级为 MTR 候选。

## 3. 与相邻 pattern 的边界

### H1/H2、L1/L2

一根内包可能是 H2/L2 的 setup，也可能是信号 K 的压缩部分，但必须分别记录：

```text
回调尝试次数 → setup/count bar → signal bar → trigger/confirmation
```

不能因为内包范围小，就跳过信号 K 质量、触发价和实际跟随。趋势中浅压缩更偏延续；区间边缘的内包要先按边缘逻辑；区间中部的内包不继承趋势腿数。

### 旗形、通道与三角形

- 一根或两根内包是局部压缩，不自动是旗形；需要父级推进和回调 lineage；
- 多次边界收缩才可能进入三角形候选，但两点连线、一个 inside bar 或一个 IOI 不够；
- 通道中部的内包通常只是暂停；宽通道边缘才有位置意义；
- 区间边界的内包突破若没有接受，只能保留失败突破分支。

### BOP 与 Opening Reversal

内包向边界外突破后强收盘并有跟随，是 BOP/新合同候选；它不再是原来的区间反转或 H/L setup。开盘直接跳过母 K 边缘时，必须按实际成交重订，不能假设原 stop 价成交。缺口或第一根 K 不自动等于开盘反转。

## 4. 订单、止损和首障碍

| 合同 | 适用条件 | 限制 |
| --- | --- | --- |
| `stop-confirmation` | 母 K/信号 K 一侧突破，等待接受或跟随 | 触发价必须事前冻结；宽 K、跳空或首障碍近要重算 |
| `limit-retest` | 旧边界、母 K 边缘或角色转换区已明确，等待回测 | 未回测不算成交；回测后重新检查首障碍 |
| `market/close-confirmation` | 强反向收盘、结构已破坏且等待代价明显 | 小内包突破不自动授权追入 |
| `observation-only` | 母 K 未冻结、区间中部、事件/跳空重订或首障碍拥挤 | 输出 `valid_no_trade` |

结构止损不能只放在第二根 K 的小尾巴外：

- 延续多头通常放在母 K/回调结构低点或支撑区外；
- 延续空头通常放在母 K/反弹结构高点或阻力区外；
- 两根反转要覆盖反向测试极端；
- 宽母 K 的极值只是触发参考，不一定是完整 thesis 的失效点。

目标顺序是第一独立支撑/阻力、通道中线/另一侧边界或最近磁铁，然后才是 MM/AB=CD。第一障碍不足约 `1R` 时，即使方向后来正确，也记为 `valid_no_trade`；约 `2R` 只是波段参考。

## 5. 案例裁决

### 5.1 KLAC `2025-10-22/23`：两根反向序列，不升级严格内包

`2025-10-22` 是强上涨腿后的空头回调，低点约 `108.57`、收盘约 `110.96`；`2025-10-23` 形成强多头实体，收盘约 `115.41`，越过前一日高点约 `114.26`，随后 `10-24` 有接受。

这更准确是 `two-bar-reversal / trend-continuation-candidate`：第二根确认 K 比 setup K 更有价值，但现有资料没有冻结母 K 高低点关系，不能叫严格 Inside Bar。研究 buy stop 约 `114.26` 上方、结构止损约 `104` 下方时，第一阻力约 `115.49–115.63` 过近，严格日线分支仍是 `valid_no_trade`。

### 5.2 AAPL `2024-05-08/09`：小实体和下影线不等于内包

`2024-05-08` 小实体、下影线明显，位于事件跳空后的浅回调支撑区；`2024-05-09` 15m 上穿 `181.10`，提供低周期确认。它是“回调减弱 + 支撑拒绝 + 后续突破”的 H1-like 序列。

没有冻结母 K 整根高低点，就保持 `strict_inside = pending-ohlc`。结构止损研究区约 `178.20–178.40` 下方，第一阻力约 `184.98`，粗略约 `1.1–1.4R`；财报跳空使它只是事件驱动条件候选。小实体/长下影是汇合因素，不改变 Inside Bar 的范围定义。

### 5.3 RBLX `2024-04-04/05`：区间中部两根反向 K 的否决

父级约为 `35.8–39.0` 的宽区间。`2024-04-04` 盘中冲高至约 `38.09` 后收约 `36.80`，`2024-04-05` 收复到约 `37.82`。即使把两天描述为两根反转，区间中部、收盘承接和第一目标都不支持新仓。

原 buy stop 约 `36.66` 已被 `04-04` 开盘约 `36.97` 跳过；结构止损应在 `35.79` 下方，中部 `37.3–37.8` 已是第一目标区域，因此结论为 `valid_no_trade`。后一天的恢复不能倒灌成前一天的优质 H1。

### 5.4 KLAC `2025-05-30/06-03`：H2 setup—确认序列，内包关系待核

`2025-05-30` 深测重复支撑；`2025-06-02` 收回 EMA20，可作为 H2 signal K；`2025-06-03` 越过其高点约 `75.90`，15m 有跟随。这是一条清楚的 `setup/count → signal → confirmation` 序列，支撑、EMA 和回调压力变化形成 META 汇聚。

当前资料没有完整冻结 `05-30` 母 K 与 `06-02` 的整根范围，因此不补写“严格 Inside Bar”，保持 `pending-ohlc`。结构止损约 `72.00`；第一阻力约 `79.03–79.79`，约 `0.8–1.0R`，日线直接新仓仍是边界。即便未来确认内包，它也只是 H2 的压缩子结构。

### 5.5 TSLA `2025-03-03/04`：跳空延续，非 Inside Bar/两根反转

`2025-03-03` 空头信号低点约 `277.30`，`2025-03-04` 约 `270.93` 低开，直接越过原 sell stop。它既不是母 K 内部平衡，也不是第二根 K 有序拒绝第一根，而是重新定价/缺口延续。

订单必须按实际开盘或新回测合同重订：价格约 `284.65` 时，下方 `284.50` sell limit 可能立即成交；等待向下突破应使用 sell stop，等待反弹回测才是新的 limit-retest。这个案例明确区分形态名称和成交语义。

## 6. 统一视觉复核卡

```text
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
mother_bar: frozen / approximate / missing
pattern_type: strict_inside / ii / ioi / two_bar_reversal / signal_sequence / not_confirmed
location: major_sr / range_edge / ema_or_gap / middle / unknown
directional_bias: continuation / reversal_candidate / both_sides / none
setup_signal_trigger_and_follow_through
order_branch / actual_fill / open_skip
structural_stop / invalidation
first_independent_obstacle / MM_after_obstacle
rough_R_R / event / sector / market
status: research_candidate / continuation / valid_no_trade / pending_ohlc
```

## 7. 当前结论与研究缺口

1. 严格 Inside Bar 的核心是整根高低点范围；没有冻结 OHLC 时，不把小实体、长影线或 H2 setup 改写成内包。
2. 两根反转的核心是关键位置上的压力转换、触发和跟随；区间中部相反 K 只是噪音。
3. Inside Bar 描述平衡/压缩，突破接受后才决定延续或失败；它不是自动方向信号。
4. 当前有 KLAC、AAPL、RBLX、TSLA 的多空和边界样本，但尚无事件干净、母 K OHLC 已冻结、突破接受清楚、首障碍宽裕且路径完整的标准正例。
5. 新案例只在填补严格范围、ii/ioi、突破失败、事件/跳空订单或首障碍几何之一时继续深审；同质小实体不重复收集。

Inside Bar 保持 `provisional`，只服务 PA Research 的视觉筛选、订单语义和观望纪律；不修改 Codex Trading，不建立量化扫描器，不连接 Execution Agent。

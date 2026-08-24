# Inside Bar / 两根 K 线专项视觉证据缺口审计

日期：2026-08-24  
状态：`framework / partial / provisional / no-new-positive`

这份审计的目的不是收集更多“小实体”图，而是把严格范围关系、两根压力转换、H/L 信号序列和普通停顿分开。没有母 K 的整根高低点，就不把图形升级成严格 Inside Bar。

## 1. 当前合同

| 合同 | 最低证据 | 当前结论 |
| --- | --- | --- |
| 严格 Inside Bar 延续 | 母 K 高低点冻结，inside 整根被包住，父级趋势清楚，突破有接受 | 视觉定义已形成；尚无事件干净、首障碍宽裕且完整成交路径的独立正例 |
| 两根 K 线反转 | 关键位置、第一根测试/推动、第二根明显拒绝、触发和跟随 | KLAC 可作条件性延续/压力转换候选；不自动升级 MTR |
| H1/H2 + 内包子结构 | 回调计数、支撑/阻力位置、setup—signal—trigger 分离 | KLAC 2025-06 可作条件性序列；严格内包仍待 OHLC |
| 区间中部压缩 | 内包/相反 K 存在，但没有边缘优势 | RBLX 提供 `valid_no_trade` 边界 |
| 跳空重定价 | 第二根越过母 K/触发区，开盘改变原成交 | TSLA 提供非 Inside Bar 对照；必须重订合同 |

## 2. 案例审计

### 2.1 KLAC 2025-10-22/23：两根反向序列的条件候选

- `2025-10-22` 是强上涨腿后的较大空头回调，低点约 `108.57`、收盘约 `110.96`；它更像 setup/count bar，不是漂亮的多头信号 K。
- `2025-10-23` 形成强多头实体，收盘约 `115.41`，越过前一日高点约 `114.26`；这才是确认/触发 K，`10-24` 的接受提供后续跟随。
- 当前证据没有冻结 `10-22` 与前一根母 K 的完整高低点关系，因此不能称严格 Inside Bar；准确标签是 `two-bar-reversal / trend-continuation-candidate`。
- 研究 buy stop 可放在 `114.26` 上方，结构止损约 `104` 下方；第一阻力约 `115.49–115.63` 过近，严格日线新仓是 `valid_no_trade`，强趋势磁铁分支仅 `research_positive_conditional`。

它证明的是“确认 K 比设置 K 更重要，首阻力仍然先于形状”，不是 Inside Bar 胜率证据。

### 2.2 AAPL 2024-05-08/09：小实体/下影线不等于内包

- `2024-05-08` 约 `180.88 / 181.10 / 179.49 / 180.77`，实体小、下影明显，处于事件跳空后的浅回调支撑区。
- `2024-05-09` 15m 从约 `180.59` 上穿 `181.10`，提供低周期确认，未从开盘跳过原触发。
- 这是“回调减弱 + 支撑拒绝 + 后续突破”的 H1-like 序列；现有材料没有冻结母 K 高低点，因此 `strict_inside = pending-ohlc`。
- 结构止损研究区约 `178.20–178.40` 下方，第一阻力约 `184.98`，粗略约 `1.1–1.4R`；财报跳空使其只能作为事件驱动条件候选。

边界：小实体、长下影和 EMA/支撑汇聚可以是 META 加分项，但不改变 Inside Bar 的范围定义。

### 2.3 RBLX 2024-04-04/05：区间中部两根反向 K 的否决

- 父级约为 `35.8–39.0` 的宽区间，不是开放上涨趋势。
- `2024-04-04` 盘中冲至约 `38.09` 后收约 `36.80`，上冲失败；`2024-04-05` 收复到约 `37.82`。
- 即使把两天描述成两根反转，区间位置、收盘承接和首目标都不支持新仓；`04-05` 的恢复不能倒灌成 `04-04` 的优质 H1。
- 原 buy stop 约 `36.66` 已被 `04-04` 开盘约 `36.97` 跳过；止损应在 `35.79` 下方，区间中部 `37.3–37.8` 已是第一目标区域，结论为 `valid_no_trade`。

边界：两根 K 线在区间中部可以只是区间摆动，不因为看起来像拒绝就变成反转 pattern。

### 2.4 KLAC 2025-05-30/06-03：H2 序列，严格内包待核

- `2025-05-30` 深测重复支撑；`2025-06-02` 收回 EMA20，可作为 H2 signal K；`2025-06-03` 越过其高点约 `75.90`，15m 有跟随。
- 这是一条清楚的 `setup/count → signal → confirmation` 序列，且支撑、EMA 和回调压力变化提供 META 汇聚。
- 当前案例文件没有完整冻结 `05-30` 母 K 与 `06-02` 的整根高低点关系，因此不能补写“严格 Inside Bar”；保持 `pending-ohlc`。
- 结构止损约 `72.00`；第一阻力约 `79.03–79.79`，到上沿约 `0.8–1.0R`，日线直接新仓仍是边界。

这里的主要教训是：如果未来确认它是内包，也只是 H2 的压缩子结构；方向和订单由位置、触发和接受决定。

### 2.5 TSLA 2025-03-03/04：跳空延续，非 Inside Bar 对照

- `2025-03-03` 空头信号低点约 `277.30`；`2025-03-04` 约 `270.93` 低开，直接越过原 sell stop。
- 第二根 K 没有在母 K 内平衡，也没有有序地拒绝第一根，而是重新定价/缺口延续；因此不是严格 Inside Bar，也不是两根反转。
- 订单必须按实际开盘或新回测合同重订。价格约 `284.65` 时，下方 `284.50` 的 sell limit 可能立即成交；等待向下突破应使用 sell stop，等待反弹回测才是新的 limit-retest。

这个对照防止把“第二根很强”误写成两根反转，也防止用后见之明保留理想成交价。

## 3. 可复用视觉规则

1. **整根范围优先**：实体被包住而影线越界，不是严格 Inside Bar；母 K 未冻结时只记 `pending-ohlc`。
2. **形态和位置分开**：内包在趋势中多半先按暂停/延续看，在区间中部默认观望，在边缘才研究反向。
3. **确认比 setup 重要**：setup/count bar、signal bar、trigger/confirmation bar 分开写；突破母 K 不等于接受。
4. **两根反转不能代替 MTR**：要有位置、结构破坏、跟随/二次确认和空间，才可升级反转候选。
5. **订单必须事前冻结**：stop、limit-retest、market-close 和开盘重订是不同合同；下方的 sell limit 可能是可立即成交单。
6. **首障碍先于 MM**：母 K 高低点只提供触发参考，不自动提供完整止损；首支撑/阻力太近仍是 no-trade。
7. **事件和跳空单独处理**：财报或缺口可以造成小实体/范围压缩外观，但不能用形态名称掩盖重新定价风险。
8. **后续不能倒灌**：后面的突破、盈利或反转只用于路径审计，不证明当时严格 Inside Bar 已经成立。

## 4. 最小视觉复核卡

```text
parent_state: trend / channel / range / transition
mother_bar: frozen / approximate / missing
pattern_type: strict_inside / ii / ioi / two_bar_reversal / signal_sequence / not_confirmed
location: major_sr / range_edge / ema_or_gap / middle / unknown
directional_bias: continuation / reversal_candidate / both_sides / none
signal_bar_and_trigger
order_branch / actual_fill / open_skip
structural_stop / invalidation
first_independent_obstacle / MM_after_obstacle
rough_R_R / event / sector / market
status: research_candidate / continuation / valid_no_trade / pending_ohlc
```

## 5. 当前缺口与停止条件

- 尚无事件干净、严格母 K OHLC 已冻结、突破接受清楚、首障碍宽裕且实际路径完整的标准 Inside Bar 正例；不为填数量把 AAPL 或 KLAC 改写成严格内包。
- 两根反转已有 KLAC 条件候选和 RBLX 否决边界，但尚缺一个无事件、父级明确、第二次确认清楚且首障碍宽裕的多空对称样本。
- 新案例只有在填补严格范围、IOI/二内包、突破失败、事件/跳空订单或首障碍几何之一时才值得深审；同质小实体不再重复收集。

专项目录：[`Inside Bar / 两根 K 线反转`](../patterns/13_inside_bar_two_bar_reversal/README.md)。基础框架：[`Inside Bar / 两根 K 线反转视觉研究框架`](inside_bar_two_bar_reversal_visual_framework_CN.md)。

# Triangle / 三角形视觉边界复核

日期：`2026-08-24`  
状态：`visual-research / provisional / not-statistical`

本复核把三角形当作“区间里面的区间”来研究：先识别父级和双方试探，再判断收缩、扩张、突破接受或失败。它不把两点连线、Inside Bar、普通旗形或后续上涨倒灌成三角形。

## 1. 最小视觉定义

### 收缩三角形

当时至少要看到：

- 同一父级背景内有双向摆动，而不是单方向 A 腿后的普通回调；
- 上方高点逐步降低、下方低点逐步抬高，或两侧边界有明确收窄；
- 两侧各有多次可见测试/反应，不是只用两个点画线；
- 摆动幅度收缩，但双方仍在试探；
- 位置、边界、突破前磁铁和失效区在决策时可见。

只有一个高点和一个低点时，记录为 `trendline_candidate`，不升级为三角形。

### 扩张三角形

高点更高、低点更低、边界向外扩张，说明双方都能把价格推得更远，方向优势可能下降。扩张不是自动反转；如果范围扩大、收盘靠极端、跟随增强，仍要防范原方向延续、高潮或波动放大。

### 区间内区间

成熟大区间内部出现小型双向压缩时，先记 `range_inside_range`。内部突破可以失败；只有小区间外强收盘、跟随和回测守住，才逐步重建新趋势或 BOP 合同。重新回到小区间或父级中部时，原突破合同失效。

## 2. 状态与边界

| 状态 | 当时可见证据 | 默认处理 | 禁止的跳跃 |
| --- | --- | --- | --- |
| `triangle-candidate` | 双向测试、边界收窄、父级尚未决定 | 观察边界和位置 | 不提前押方向 |
| `range-inside-range` | 大区间内的小型双向压缩 | 先按子区间和父级边缘处理 | 不让子结构覆盖父级 |
| `expanding-triangle-boundary` | 高低点外扩、范围放大、后段测试更强 | 防扩张/高潮/延续 | 不因扩张直接做反向 |
| `breakout-acceptance` | 强收盘离开边界、跟随、回测守住 | 转 BOP/新趋势合同 | 不沿用旧反向假设 |
| `failed-breakout` | 越界后回到结构内并有反向压力 | 等第二次失败或反向确认 | 一根影线不够 |
| `triangle-middle-no-trade` | 中线附近、首磁铁近、测试不清 | 观察 | 不在中部追单 |

三角形突破前不能假设结果。第一根刺破只是测试；突破接受需要收盘、外侧停留、跟随或成功回测。主要反转还需要结构破坏、反向压力、第二次确认和空间。

## 3. 与相邻 pattern 的分流

- **Inside Bar / IOI**：微观母子 K 范围压缩；三角形需要更大级别的双向摆动和多次边界测试。
- **普通旗形/通道**：单方向趋势和反向小回调占主导时，优先叫旗形或通道；没有双方试探不叫三角形。
- **交易区间**：成熟区间的上下沿、中线和 second-leg trap 优先；区间内三角形只是子结构。
- **BOP**：边界外强收盘、跟随和回测接受后才切换；接受会废弃旧区间/反向假设。
- **失败突破/高潮**：刺破后重新进入才开启失败分支；扩张本身不等于高潮或 MTR。
- **H1/H2、L1/L2**：三角形内部局部 H/L 必须重新解释，不能自动继承开放趋势腿数。

## 4. 无后见之明的复核顺序

1. 判父级是开放趋势、成熟区间、通道还是过渡；
2. 标出上沿、下沿和中线/磁铁；
3. 确认两侧测试是否足够、是否真正分离；
4. 记录当前位于上沿、下沿还是中部；
5. 判断第一突破是接受、失败还是尚未确认；
6. 若失败，等待重新进入后的第二次边界失败或反向信号；
7. 冻结订单、结构止损、首独立支撑/阻力和粗略 R/R；
8. 后续走势和 MM 只用于结果审计，不回写当时结构。

## 5. 订单合同与风险

| 合同 | 用法 | 关键限制 |
| --- | --- | --- |
| `stop-confirmation` | 上沿外 buy stop、下沿外 sell stop，或失败后反向信号 K 外确认 | 触发价必须事前冻结；跳空后原价作废 |
| `limit-retest` | 边界、突破区或角色转换区明确，等待回测 | 未回测不算成交；穿过边界后必须重建合同 |
| `market/close-confirmation` | 强突破收盘且等待代价明显 | 大突破 K 贴近首阻力时不追 |
| `observation-only` | 测试不足、中部、事件重订或首障碍拥挤 | 记录 `valid_no_trade` |

结构止损至少要覆盖突破边界和最近有效摆动；扩张三角形反向要放在最后一次测试极端外；区间内区间要明确是小区间失效还是父级边缘失效，不能混写。目标顺序是最近独立支撑/阻力、另一侧边界或父级中线，再看三角形高度/MM。首障碍不足约 `1R` 时不交易，约 `2R` 只是波段参考。

## 6. 案例裁决

### 6.1 TSLA `2025-09-08–09-12`：压缩后 BOP 接受

`09-08–10` 在 `355.39–357.54` 主要阻力下多次试探，影线越过但收盘没有接受，可以记为高位压缩/triangle-like boundary。`09-11` 强阳线收在约 `368.81`，越过阻力并有 15m 跟随，随后回测守住旧阻力。

裁决：`breakout-acceptance / BOP`。原失败突破或三角形反向假设失效，新交易必须使用突破接受合同。它是状态切换候选，不是事前已冻结的无条件三角形正例；左侧更远阻力和实际首障碍仍优先。

### 6.2 ASML `2025-05-23–06-11`：父级区间重复测试

`05-23` 和 `05-30` 在 `715–718` 下沿附近重复测试，随后高重叠并向上扩张。局部可以画收窄边界，但完整图表更像父级区间下沿的二次测试和过渡，没有清楚的两侧三角形边界、触发和独立首障碍。

裁决：`range_inside_range / not_triangle_frozen / observation-only`。后续上涨不能证明事前已经存在三角形多头突破。

### 6.3 RBLX `2024-03-18–04-05`：区间内压缩与失败突破

父级约为 `35.8–39.0` 的宽区间。`03-18–28` 上涨后，`04-01–03` 回到下沿，局部有压缩；`04-04` 盘中冲至约 `38.09` 后收约 `36.80`，向上突破没有被接受，`04-05` 的恢复不能倒灌成顺势突破。

原 buy stop 约 `36.66` 被开盘约 `36.97` 越过；结构止损应在 `35.79` 下方，区间中部 `37.3–37.8` 很快成为首障碍。裁决：`range_inside_range / failed_breakout / valid_no_trade`。

### 6.4 COIN `2024-01-04–01-10`：扩张边界不是收缩正例

空头 A 后的 B 腿中，`01-04/05/08` 多次上探，第三次范围扩大并回到约 `161` 阻力，高点和范围没有逐步收缩。`01-09` 低周期有空头反应，但下方 `148.81` 首支撑相对 `161.38` 结构止损只提供约 `0.25–0.5R`；`01-10` 开盘重订又改变原 L2 合同。

裁决：`expanding-triangle-boundary / continuation-or-climax / valid_no_trade`。扩张表示波动加剧，不自动授权空头反转。

### 6.5 XOM `2024-07-18–08-02`：扩张与跳空重订

`07-25/30/31` 三次上探约 `109.82/110.34/111.43`，第三次抬高并扩大范围，更像扩张/延续边界而非收缩三角形。`08-01` 出现空头反应，`08-02` 开盘约 `107.90` 跳过原 sell stop；首支撑约 `105.20`，重订后粗略空间约 `0.7R`。

裁决：`expanding-boundary / gap-reprice / valid_no_trade`。形态方向、实际成交和空间必须分开。

### 6.6 KLAC `2025-10-14–10-24`：趋势旗形/微型压缩对照

强多头腿后 `10-22` 单日回调，`10-23` 强阳线突破并在 `10-24` 接受前高，视觉上可观察小型压缩。但没有两侧多次分离测试，父级趋势旗形解释更直接；触发上方 `115.49–115.63` 左侧高点贴近，严格日线分支为 `valid_no_trade`，强趋势磁铁分支仅条件性研究。

结论：不是每个收窄平台都升级成三角形。

## 7. 统一视觉复核卡

```text
contract_scope: historical_context_only
primary_pattern: other
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
triangle_status: candidate / range_inside_range / expanding_boundary / not_frozen
direction: long / short / no_valid_direction
upper_lower_boundary: source and confidence
tests: enough / insufficient / ambiguous
location: upper_edge / lower_edge / middle / unknown
breakout_state: not_confirmed / accepted / failed / gap_repriced
second_entry: pending / present / not_applicable
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
structural_stop:
structural_invalidation:
first_independent_obstacle:
rough_R_R:
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
event_context:
event_bucket:
sector_reference:
market_reference:
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
triangle_state: continuation / BOP / failed_breakout / range_reaction / not_frozen
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

## 8. 当前结论与缺口

1. 三角形首先是双向压缩和双方试探，第一突破不能默认成功；
2. 扩张三角形表示波动外扩，不自动等于衰竭或反转；
3. Inside Bar/IOI 是微观压缩，普通旗形是趋势回调，成熟区间是父级状态，三者不能互相替代；
4. 突破接受要看收盘、跟随和回测守住；失败突破要看重新进入和第二次尝试；
5. ASML、TSLA、RBLX、COIN、XOM、KLAC 提供区间、接受、失败、扩张和旗形对照，但没有事件干净、两侧边界确认、首障碍宽裕的标准收缩三角形正例；
6. Triangle 保持 `provisional`，只服务 PA Research 的视觉筛选、订单重建和观望纪律，不进入 Codex Trading 或 Execution Agent。

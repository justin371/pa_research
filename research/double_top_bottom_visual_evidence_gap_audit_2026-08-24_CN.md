# Double Top / Double Bottom 双顶双底专项视觉证据缺口审计

日期：2026-08-24  
状态：`framework / partial / provisional / no-new-positive`

本审计把双顶/双底从自动反转标签降回“位置 + 两次有分离测试”的视觉描述，再判断它属于区间边缘、MTR、Final Flag、普通回调或状态过渡。

## 1. 当前合同

| 合同 | 当时需要看到的证据 | 当前结论 |
| --- | --- | --- |
| 区间边缘双顶/双底 | 成熟父级区间、边缘第二次测试、反向触发和中部/另一边界空间 | TSLA/RBLX 提供条件或否决边界；不等同开放趋势 MTR |
| MTR 候选 | 成熟趋势极端、双测试/失败突破、结构破坏、第二次确认、跟随和空间 | 目前只有条件候选，尚无事件干净、过程完整的标准正例 |
| Final Flag 候选 | 长趋势末端、压缩/窄区间、最后一次原方向尝试 | NFLX 提供高位边界；被接受时转延续/BOP |
| 普通延续 | 原趋势仍强，双测试未破坏主要结构 | KLAC/PLTR 提供非反转对照 |
| 双顶/双底被否定 | 原方向强收盘越过第二次测试并接受 | TSLA 2025-09 提供 BOP 状态切换 |
| 区间过渡 | 两次测试后高重叠、父级边界优先、反向确认不足 | ASML 提供双底样但不冻结 MTR |

## 2. 案例审计

### 2.1 TSLA 2024-03-04–03-14：区间上沿双顶/失败突破条件候选

- 入场前价格在约 `190–205` 反复交易，`2024-02-27` 上探约 `205.60`；因此父级更接近局部区间上沿，而非开放趋势中段。
- `03-04` 之后空头反应，第一次下行尝试失败后，`03-11`–`03-13` 形成第二次向下尝试；这可以写成区间上沿失败突破后的 L2/双顶反向候选。
- 研究 sell stop 约在 `172.41` 下方，结构止损约 `182.87` 上方；静态到 `152.37–153.75` 约 `1.6–1.9R`，但过程中先触发结构止损。
- 结论：`range-edge-double-top / MTR-candidate / process-stop-first`。它是条件候选，不是无条件 MTR 正例；首障碍、区间反向和实际路径必须保留。

### 2.2 RBLX 2024-03-18–04-05：双底样但区间逻辑否决

- 父级约 `35.8–39.0` 宽区间；`03-18` 低点约 `35.95`，`04-02/03` 再测试 `35.90/35.79`，外形像双底。
- 但反弹中有较多重叠，`04-04` 盘中冲高约 `38.09` 后收约 `36.80`；信号质量和区间中部位置都不支持把它升级趋势反转。
- 若按区间下沿 thesis，结构止损在 `35.79` 下方，第一目标约 `37.3–37.8` 中部，很快到达；原 buy stop 约 `36.66` 还被开盘约 `36.97` 越过。
- 结论：`range-edge-double-bottom-like / failed-signal / valid_no_trade`。后续恢复不能倒灌成高质量双底买点。

### 2.3 NFLX 2024-08-05–09-26：高位多次测试与 Final Flag/MTR 边界

- 强多头 A 后高位压缩、多次测试，可以先标为 `final_flag_or_MTR-candidate`；但测试次数超过三次、重叠明显，计数并不干净。
- 低周期卖出触发约 `67.10` 下方可审计，结构止损约 `71.60–71.70` 外；入场前第一支撑 `66.54–65.98` 过近，只有约 `0.1–0.25R`。
- `09-24` 后高位重新被接受，说明原反向 thesis 后续失效；不能用后续下跌/上涨选择性证明双顶成立。
- 结论：`high-test / final-flag-boundary / valid_no_trade`，不是标准双顶 MTR 正例。

### 2.4 TSLA 2025-09-08–09-12：双高观察被 BOP 否定

- `09-08–10` 在 `355.39–357.54` 阻力下多次试探，影线越过但收盘没有接受，双顶/三推/反转可以作为观察，不提供提前做空授权。
- `09-11` 强收盘越过阻力并在 15m 跟随，后续回测守住角色转换区；状态切换为 BOP/突破接受。
- 反向订单假设应取消；新交易必须按新的 BOP 成交、结构止损和第一障碍重新计算。

它是双顶/双底最重要的失败分支：原方向接受极端后，旧反转名字失效。

### 2.5 KLAC 2025-10-14–10-24：普通趋势旗形对照

- 强多头趋势中 `10-22` 只有浅回调，`10-23` 强阳线恢复并在 `10-24` 接受前高；没有两次有分离的高位测试。
- 触发上方 `115.49–115.63` 第一阻力贴近；严格日线分支 `valid_no_trade`，强趋势磁铁分支只是条件性延续。
- 结论：`ordinary-trend-flag / continuation`，不把任何相邻高点改名为双顶。

### 2.6 ASML 2025-05-19–06-13：双底样进入区间过渡

- `05-23` 和 `05-30` 在 `715–718` 下沿附近二次测试，随后 `06-02–06` 高重叠，`06-09–11` 向上扩张。
- 两次低点确实提供双底样位置证据，但缺少清楚的颈线接受、第二次确认和首障碍空间；低周期切出的更多摆动不能机械变成 MTR。
- 结论：`double-bottom-like / range-transition / observation-only`，不冻结反向订单。

### 2.7 PLTR 2024-12-24–2025-01-08：B 内双顶不是独立反转

- 普通空头 A 后出现反向 B，B 内有近似双顶/二次测试，但买方仍有反弹能力；主要合同仍是普通 A 后 L1，而不是独立双顶 MTR。
- 结构止损要放在 B 顶部约 `80.06` 上方，不能因为局部双顶而缩窄；双顶只是增加空头结构可读性，不能替代 A 腿、位置和首障碍。

这个案例说明局部双顶可以嵌套在 ABC/H-L 中，但不能与父级 pattern 重复计为独立优势。

## 3. 可复用视觉规则

1. **两次测试必须有分离**：连续影线或高重叠不等于双顶/双底。
2. **父级优先**：成熟区间边缘先按区间；开放趋势中先问是否只是普通回调；末端压缩才考虑 Final Flag。
3. **第一反向不是 MTR**：需要结构破坏、第二次确认、接受/跟随和空间。
4. **原方向接受就重置**：强收盘越过第二次测试并跟随后，双顶/双底反向 thesis 切换为 BOP/延续。
5. **颈线是确认/管理位置**：不是自动必到目标；左侧第一独立障碍优先于 MM。
6. **订单合同分开**：反向 stop、颈线回测 limit 和 market-close 不能共用理想成交价；跳空后必须重订。
7. **局部标签不重复计分**：双顶/双底、H3、Final Flag、MTR 和区间边缘可能共存，但必须选父级和主要合同。
8. **完整图表不能倒灌**：后续成功或失败只做路径审计，不能回写当时的反转确定性。

## 4. 最小视觉复核卡

```text
parent_state: open_trend / mature_range / channel / transition
test_type: double_top / double_bottom / near_equal / expanded / ambiguous
first_test / second_test: levels and separation
location: major_sr / range_edge / trend_extreme / middle / unknown
reversal_state: attempt / structure_break / second_confirmation / failed_thesis
related_family: ordinary_pullback / range_edge / final_flag / MTR / H3_L3
order_branch / actual_fill / open_skip
structural_stop / invalidation
neckline_or_mid_swing
first_independent_obstacle / MM_after_obstacle
rough_R_R / event / sector / market
status: candidate / continuation / range_transition / BOP / valid_no_trade
```

## 5. 当前缺口与停止条件

- 尚无事件干净、成熟趋势极端、两次测试分离清楚、反向二次确认不跳空、首障碍宽裕且过程完整的标准双顶/双底 MTR 正例。
- 现有 TSLA 是条件候选但过程先止损，RBLX/NFLX/ASML 是区间或首障碍边界，KLAC/PLTR 是普通延续对照；不重复堆叠相似案例。
- 新案例只有在填补无事件双向正例、颈线回测合同、区间边缘与开放趋势分界或 BOP 否定之一时才值得深审。

专项目录：[`Double Top / Double Bottom`](../patterns/15_double_top_bottom/README.md)。比较框架：[`双顶/双底、MTR 与 Final Flag 视觉边界对照`](double_top_bottom_mtr_final_flag_comparison_CN.md)。

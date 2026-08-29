# Head-and-Shoulders / Rounded 头肩与圆顶圆底专项视觉证据缺口审计

日期：2026-08-24  
状态：`framework / partial / provisional / no-new-positive`

本审计把头肩顶/底降为复杂双顶/双底或 MTR 候选，把圆顶/圆底降为控制权转移背景。颈线、第二次确认和第一障碍决定能否进入交易研究。

## 1. 当前合同

| 合同 | 当时需要看到的证据 | 当前结论 |
| --- | --- | --- |
| 头肩顶/底候选 | 成熟趋势极端、肩/头分离、真实颈线、右肩效率下降 | 视觉定义已形成；当前无事件干净、颈线和路径完整的标准正例 |
| 圆顶/圆底过渡 | 推进逐步减弱、重叠增加、斜率趋平、区间/边界形成 | ASML/NFLX 提供背景边界；不在弧线中部猜反转 |
| 颈线接受 | 强收盘越过颈线、跟随、回测守住 | TSLA 提供 BOP 否定；原反向 thesis 必须重置 |
| 颈线失败 | 越界后重新进入、反向跟随和第二次确认 | 目前多为区间/首障碍边界，缺标准正例 |
| 普通旗形/回调 | 强趋势和浅 B，缺成熟肩头肩和颈线 | KLAC 提供非头肩对照 |

## 2. 案例审计

### 2.1 TSLA 2024-03-04–03-14：区间上沿复杂双顶/MTR 候选

- 入场前约 `190–205` 的反复交易和 `02-27` 约 `205.60` 上探，使它更接近区间上沿反应，而不是开放趋势中的标准头肩顶。
- `03-04` 后空头反应，第一次下行失败后再出现 L2-like 下破，可以作为复杂双顶/头肩-like 的条件候选；颈线/局部结构破坏需要以当时价位冻结。
- 研究 sell stop 约 `172.41` 下方，结构止损约 `182.87` 上方；静态到 `152.37–153.75` 约 `1.6–1.9R`，但过程先触发结构止损。
- 结论：`range-edge / head-shoulder-like / MTR-candidate / process-stop-first`，不是开放趋势标准正例。

### 2.2 NFLX 2024-08-05–09-26：高位 H&S-like 与首障碍否决

- 强多头 A 后出现高位压缩和多次测试，可以观察左肩/头/右侧测试，但测试超过三次且肩部不对称，颈线并不干净。
- 低周期卖出触发约 `67.10` 下方，结构止损约 `71.60–71.70` 外；第一支撑 `66.54–65.98` 过近，只有约 `0.1–0.25R`。
- 后续顶部重新被接受，说明反向 thesis 失效；不能用后续走势选择性证明头肩成立。
- 结论：`H&S-like / final-flag-boundary / valid_no_trade`，不是标准头肩 MTR 正例。

### 2.3 ASML 2025-05-19–06-13：双底/圆底/逆头肩-like 过渡

- `05-23` 与 `05-30` 在 `715–718` 下沿附近二次测试，之后 `06-02–06` 重叠增加，`06-09–11` 向上扩张。
- 可以把这段看成双底样、圆底背景或逆头肩-like，但没有清楚的第三结构点、颈线接受和反向二次确认；60m 小摆动不能机械叠加成 Daily 头肩。
- 结论：`rounded-bottom-like / range-transition / observation-only`；不冻结 buy stop 或 MTR 合同。

### 2.4 LOW 2024-06-11–06-24：低位逆头肩候选但空间拥挤

- 急跌后出现双底样恢复，可以观察左侧反应、低点测试和右侧恢复，但父级仍在过渡，右肩/颈线确认不完整。
- `221.92–223.01` 第一阻力紧贴，结构止损与第一障碍不配；方向正确也不能用头肩高度/MM 掩盖空间不足。
- 结论：`inverse-HS-like / parent-transition / valid_no_trade`。

### 2.5 TSLA 2025-09-08–09-12：颈线/阻力接受否定反向

- `09-08–10` 在 `355.39–357.54` 阻力下多次试探，可以作为头肩/双顶/三推观察；但没有提前做空授权。
- `09-11` 强阳线越过阻力并得到 15m 跟随，随后回测守住，状态切换为 BOP/突破接受。
- 原头肩或 MTR 空头订单应取消；若继续交易必须用新 BOP 合同、实际成交和新风险。

### 2.6 RBLX 2024-03-18–04-05：区间复杂双底而非逆头肩

- 父级宽区间，`03-18` 和 `04-02/03` 有下沿测试，但肩部、头部和颈线并不独立；局部上推仍是区间摆动。
- `04-04` 上冲后收弱，区间中部 `37.3–37.8` 是第一磁铁；宽结构止损使 stop/limit 分支都不合格。
- 结论：`range-edge / complex-double-bottom-like / valid_no_trade`，不升级为逆头肩。

### 2.7 KLAC 2025-10-14–10-24：普通旗形非右肩

- 强多头趋势中只有浅回调，`10-23` 强阳线恢复并在 `10-24` 接受前高；缺少成熟高位、清楚肩部与颈线。
- 触发上方 `115.49–115.63` 第一阻力贴近，严格日线是 `valid_no_trade`，强趋势磁铁只是条件性延续。
- 结论：`ordinary-flag / continuation`；不能因为右侧出现一个小高点就命名右肩。

## 3. 可复用视觉规则

1. **先看父级和位置**：区间中部的头肩外形优先按区间，强趋势浅回调优先按 ABC/旗形。
2. **颈线必须真实**：来自两个中间摆动并有实际验证；后见之明重画的线不算当时证据。
3. **头肩只是复杂双顶/双底**：肩部不等高可以，但分离、效率下降和第二次确认不能缺。
4. **圆顶/圆底是背景警报**：推进减慢和重叠增加不等于已反转；先等边界/颈线与跟随。
5. **第一反向不等于 MTR**：要有结构破坏、第二次确认、接受/跟随和空间。
6. **原方向接受就重置**：强收盘越过头部/肩部或颈线并跟随后，旧反向 thesis 转 BOP/延续。
7. **首障碍先于高度投影**：颈线或头肩高度不是必到目标；左侧独立支撑/阻力优先。
8. **局部标签不重复计分**：头肩、双顶、三推、Final Flag、MTR 可能共存，但要选父级和主要合同。

## 4. 最小视觉复核卡

```text
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
shape_status: head_shoulder_like / candidate / rounded_transition / not_frozen
left_shoulder / head / right_shoulder: levels and separation
neckline: source / slope / accepted_or_not
location: major_sr / range_edge / trend_extreme / middle / unknown
reversal_state: attempt / structure_break / second_confirmation / failed_thesis
related_family: double_top_bottom / three_push / final_flag / MTR / ordinary_pullback
order_branch / actual_fill / open_skip
structural_stop / invalidation
first_independent_obstacle / MM_after_obstacle
rough_R_R / event / sector / market
status: candidate / continuation / BOP / range_transition / valid_no_trade
```

## 5. 当前缺口与停止条件

- 尚无事件干净、颈线清楚、右肩/第二次确认明确、结构止损合理、首障碍宽裕且路径完整的标准头肩顶/底正例。
- 尚无纯粹可冻结的圆顶/圆底正例；现有 ASML/NFLX 更适合作为状态转移和首障碍边界。
- 新案例只有在填补真实颈线回测、无事件标准正例、圆顶/圆底边界或 BOP 否定之一时才值得深审；不重复收集高位多次测试 no-trade。

专项目录：[`Head-and-Shoulders / Rounded`](../patterns/16_head_shoulders_rounded/README.md)。基础框架：[`头肩顶/底与圆顶/圆底视觉边界框架`](head_shoulders_rounded_top_bottom_visual_framework_CN.md)。

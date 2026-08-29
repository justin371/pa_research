# Head-and-Shoulders / Rounded 头肩与圆顶圆底视觉边界复核

日期：`2026-08-24`  
状态：`visual-research / provisional / not-statistical`

头肩顶/底是把成熟趋势极端、复杂双顶/双底和颈线结构组织在一起的视觉语言；圆顶/圆底描述推进效率下降和控制权逐步转移。两者都不是“三个点”或一条弧线的自动反转信号。

## 1. 最小定义

### 头肩顶/底

```text
成熟趋势/主要极端
→ 左肩或第一次反应
→ 头部（更高高点或更低低点）
→ 颈线附近回落/反弹
→ 右肩或第二次测试，不能有效恢复头部
→ 颈线接受、失败或重新进入
```

最低条件：

- 父级趋势或成熟极端清楚；
- 头部与肩部之间有可见分离，不是连续影线；
- 颈线来自两个中间摆动并被实际验证，可以略倾斜；
- 右肩显示原方向效率下降，并出现反向触发或结构破坏候选；
- 颈线突破后有跟随/回测守住，或失败后重新进入原结构。

肩部不必等高，但必须解释相对位置。只能画出复杂双顶/底而没有真实颈线时，保持 `head-shoulder-like`。

### 圆顶/圆底

- 原方向推进逐步变慢，单位价格推进效率下降；
- K 线重叠增加、实体变小、双方交易变多；
- 斜率趋平，随后形成小区间或更大交易区间；
- 最后的方向突破、失败突破或二次入场才决定延续、区间或反转。

圆形本身不提供方向；不能在弧线中部猜顶/底。

## 2. 状态与边界

| 状态 | 证据 | 默认处理 |
| --- | --- | --- |
| `head-shoulder-like` | 肩/头外形存在，但颈线或父级不完整 | 观察，不授权反向 |
| `head-shoulder-candidate` | 颈线、右肩/第二测试和主要位置较清楚 | 等颈线 stop 或第二次确认 |
| `rounded-transition` | 推进变慢、重叠增加、斜率趋平 | 先看小区间/状态转移，不猜拐点 |
| `neckline-break-acceptance` | 强收盘越过颈线、跟随、回测守住 | 转 BOP/MTR 新合同 |
| `neckline-failure` | 越界后重新回到原结构 | 开失败突破/区间边缘分支 |
| `ordinary-flag-or-pullback` | 原趋势强，右侧只是浅回调 | 按 ABC/H1/H2 延续，不命名右肩 |
| `valid-no-trade` | 首障碍贴近、区间中部或事件改变几何 | 观察，保留标签但不交易 |

形状名称放在最后，顺序固定为：**父级状态 → 主要位置 → 压力变化 → 接受/失败 → 订单几何**。

## 3. 与相邻 pattern 的分流

- **双顶/双底**：头肩是更复杂的双顶/底叙事；两次测试与颈线尚不完整时，优先使用双顶/底候选。
- **MTR**：头肩只是位置证据；成熟趋势、结构破坏和第二次确认才支持 MTR。
- **三推/H3-L3**：三个高低点不自动是肩/头/肩；次数与压力状态另行审计。
- **Final Flag**：末端压缩可以出现头肩-like 外观；接受则是延续/BOP，失败才看反向。
- **普通 ABC/H1-H2**：强趋势中的浅回调没有成熟极端和颈线，优先按延续。
- **圆顶/圆底**：是效率下降和状态转移背景，不是精确几何或独立入场。

## 4. 无后见之明的审计顺序

1. 标出当时已经存在的趋势、通道、区间和主要高低点；
2. 只把第一次高/低反应标为肩部候选，不提前知道右肩是否出现；
3. 头部出现后冻结颈线候选及其来源，不用后面更漂亮的点重画；
4. 右肩出现时区分效率下降与真正反向；
5. 第一反向只记 `reversal_attempt`，等待第二次入场、颈线回测或结构确认；
6. 原方向强势越过头部/肩部边界并跟随时，标记 `failed-thesis / BOP-acceptance`；
7. 最后才计算结构止损、第一支撑/阻力和 rough R/R。

## 5. 订单、止损和目标

- **颈线 stop**：头肩顶在颈线下方等待 sell stop，头肩底对称等待 buy stop；冻结触发价、实际成交和是否跳空越过。
- **颈线回测 limit**：只有颈线已真实突破、角色转换清楚且价格回测时才单列；未回测不假设成交。
- **market/close**：只给强反向收盘、结构已破坏且首障碍仍有空间的分支；事件/高潮大 K 优先降级。
- **observation-only**：颈线不真实、父级中部、第一反向无跟随、首障碍不足约 `1R` 或原方向重新接受时使用。

交易止损可以放在右肩极端外，但若它远窄于头部/母级结构失效位置，必须明确是低周期短线合同；不能把窄止损包装成日线 MTR。目标顺序是颈线/最近磁铁、第一独立支撑/阻力，然后才是头肩高度或 MM。约 `2R` 只是完整波段参考。

## 6. 案例裁决

### 6.1 TSLA `2024-03-04–03-14`：区间上沿复杂双顶/MTR 候选

入场前约 `190–205` 反复交易，`2024-02-27` 上探约 `205.60`，父级更接近区间上沿而非开放趋势中的标准头肩顶。`03-04` 后空头反应，第一次下行失败后 `03-11–13` 出现 L2-like 下破，可以作为复杂双顶/头肩-like 条件候选。

研究 sell stop 约 `172.41` 下方、结构止损约 `182.87` 上方；静态到 `152.37–153.75` 约 `1.6–1.9R`，但过程中先触发结构止损。裁决：`range-edge / head-shoulder-like / MTR-candidate / process-stop-first`，不是开放趋势标准正例。

### 6.2 NFLX `2024-08-05–09-26`：高位 H&S-like 与首障碍否决

强多头 A 后高位压缩、多次测试，可以观察左肩/头/右侧测试；但测试超过三次、肩部不对称、颈线不干净。低周期卖出约 `67.10` 下方，结构止损约 `71.60–71.70` 外，第一支撑 `66.54–65.98` 仅约 `0.1–0.25R`。

裁决：`H&S-like / final-flag-boundary / valid_no_trade`，不是标准头肩 MTR 正例；后续高位接受不能倒灌成反转证明。

### 6.3 ASML `2025-05-19–06-13`：双底/圆底/逆头肩-like 过渡

`05-23` 与 `05-30` 在 `715–718` 下沿附近二次测试，之后重叠增加并向上扩张。可以称双底样、圆底背景或逆头肩-like，但没有清楚的第三结构点、颈线接受和反向二次确认；低周期小摆动不能拼成 Daily 头肩。

裁决：`rounded-bottom-like / range-transition / observation-only`，不冻结 buy stop 或 MTR 合同。

### 6.4 LOW `2024-06-11–06-24`：低位逆头肩候选但空间拥挤

急跌后出现双底样恢复，可以观察左侧反应、低点测试和右侧恢复，但父级仍在过渡，右肩/颈线确认不完整。`221.92–223.01` 第一阻力紧贴，结构止损与首障碍不配；裁决：`inverse-HS-like / parent-transition / valid_no_trade`。

### 6.5 TSLA `2025-09-08–09-12`：颈线/阻力接受否定反向

`09-08–10` 在 `355.39–357.54` 阻力下多次试探，可以作为头肩/双顶/三推观察；`09-11` 强阳线越过阻力并得到 15m 跟随，随后回测守住。原头肩或 MTR 空头订单应取消，状态切换为 `BOP-acceptance`。

### 6.6 RBLX `2024-03-18–04-05`：区间复杂双底而非逆头肩

父级宽区间，`03-18` 和 `04-02/03` 有下沿测试，但肩部、头部和颈线并不独立；`04-04` 上冲后收弱，区间中部 `37.3–37.8` 是第一磁铁，宽结构止损使 stop/limit 都不合格。裁决：`range-edge / complex-double-bottom-like / valid_no_trade`。

### 6.7 KLAC `2025-10-14–10-24`：普通旗形，不是右肩

强多头趋势中只有浅回调，`10-23` 强阳线恢复并在 `10-24` 接受前高；缺少成熟高位、清楚肩部与颈线。`115.49–115.63` 第一阻力贴近，严格日线为 `valid_no_trade`，强趋势分支只是条件性延续。

## 7. 统一视觉复核卡

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

## 8. 当前结论与缺口

1. 头肩顶/底先归入复杂双顶/底或 MTR 候选；左右肩不必等高，但需要分离、父级位置和真实颈线。
2. 圆顶/圆底主要表示推进效率下降和控制权转移，是等待结构确认的背景，不是单独入场形态。
3. 区间中部优先按区间处理；普通趋势浅回调优先按 ABC/旗形；成熟极端、反向破坏和第二次确认同时出现，才升级 MTR。
4. 颈线突破必须分为接受、失败或区间内部摆动；颈线高度/MM 不能越过触发前已知的首障碍。
5. 当前没有事件干净、颈线清楚、第二次确认明确、首障碍宽裕且路径完整的标准头肩正例，也没有纯粹可冻结的圆顶/圆底正例。

Head-and-Shoulders / Rounded 保持 `provisional`，只服务 PA Research 的视觉筛选、订单重建和观望纪律；不修改 Codex Trading，不建立量化扫描器，不连接 Execution Agent。

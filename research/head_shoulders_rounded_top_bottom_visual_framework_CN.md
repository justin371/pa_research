# 头肩顶/底与圆顶/圆底：视觉边界框架 V0.1

状态：`visual-research / partial / provisional / comparison-layer / not-quantitative`

这份文件把 PA 图表里很容易被过度命名的四类外形放在一起：头肩顶、头肩底、圆顶和圆底。它不是新的胜率规则，也不把“出现三个高点/低点”自动升级成反转。

## 1. 最小定义

### 1.1 头肩顶与头肩底

头肩顶可以先看成**上涨背景中的复杂双顶或 MTR 候选**：

```text
前置上涨/成熟高位
→ 左肩（第一次高位反应）
→ 头部（更高的测试）
→ 颈线附近回落
→ 右肩（不能有效恢复头部高度的第二次反应）
→ 颈线突破、回测或失败
```

头肩底是对称版本：前置下跌或成熟低位，头部创出更低低点，左右肩在更高的位置形成，之后观察颈线接受或失败。

最低视觉条件不是肩膀必须等高，而是同时看：

- 有可识别的父级趋势或成熟极端；
- 头部与肩部之间有可见分离，不能只是连续几根 K 的影线；
- 颈线由两个中间摆动组成，哪怕略倾斜，也必须是实际被价格反复验证的结构区域；
- 右肩/右侧测试显示原方向效率下降，且有反向触发或结构破坏的候选；
- 颈线突破后有跟随、回测守住，或失败后重新进入原结构。

因此，头肩是组织信息的方式，不是独立于双顶/双底、MTR、区间边缘和 BOP 之外的第四种自动信号。课程中的最小共识也是：头肩可视为更复杂的双顶/双底或 MTR，颈线突破可能只是区间内部运动，不能机械套用目标。

### 1.2 圆顶与圆底

圆顶/圆底描述的是**控制权逐步转移**，不是精确的三点形态：

- 原方向推进逐步变慢，单位价格推进的效率下降；
- K 线重叠增多，实体变小，双向交易增加；
- 斜率从方向性变成趋平，随后进入小区间或更大交易区间；
- 最后的方向突破、失败突破或二次入场，才决定是延续、区间还是反转。

圆顶/圆底更适合作为“不要抢最早拐点”的背景警报。没有边界突破、跟随和空间时，不把圆形本身当作入场图案，也不把所有缓慢回调都叫圆底。

## 2. 外形相似时的优先级

| 视觉外形 | 先问什么 | 默认分类 | 不能直接做什么 |
| --- | --- | --- | --- |
| 头肩顶/底候选 | 父级是成熟趋势/极端，还是区间中部？颈线是否真实？ | 复杂双顶/双底、MTR 候选或区间边缘反应 | 不能因肩膀出现就直接反向下单 |
| 圆顶/圆底候选 | 推进是否逐步减弱，重叠是否增加，边界是否已经形成？ | 状态转移警报、成熟区间候选或 Final Flag 边界 | 不能在圆弧中部猜顶/猜底 |
| 两次测试 | 两次测试之间是否有分离和反应？ | 双顶/双底或区间边缘二次测试 | 不能只数两个影线 |
| 颈线/区间边界 | 突破是否被接受？是否有跟随或回测守住？ | BOP、失败突破、MTR 或区间摆动 | 不能默认颈线高度就是必到目标 |
| 强趋势中的浅回调 | 原方向是否仍有强收盘和跟随？ | 普通 ABC、旗形或嵌套回调 | 不能把右侧小高点命名为右肩来做空 |
| 高潮后的平台 | 高潮后是小反转、两腿区间，还是继续扩张？ | 失败突破/高潮框架、Final Flag 或 MTR 候选 | 不能把高潮的第一根反向 K 当成完整反转 |

形状名称放在最后，顺序固定为：**父级状态 → 主要位置 → 压力变化 → 接受/失败 → 订单几何**。这和已有的[`双顶/双底、MTR 与 Final Flag 对照`](double_top_bottom_mtr_final_flag_comparison_CN.md)以及[`失败突破与高潮反转框架`](failed_breakout_climax_visual_framework_CN.md)保持一致。

## 3. 无后见之明的审计顺序

在看到完整图表时，研究记录仍必须切回实际决策时点：

1. 先标出当时已经存在的趋势、通道、交易区间和主要高低点；
2. 只把第一次高位/低位反应标成肩部候选，不提前知道右肩会不会出现；
3. 头部出现后，冻结颈线候选和它的来源，不用后面更漂亮的低点/高点重画；
4. 右肩或右侧第二次测试出现时，区分“效率下降”与“真正反向”；
5. 第一反向运动只记为 `reversal_attempt`，等待第二次入场、颈线回测守住或等价结构确认；
6. 若原方向强势越过头部/肩部边界并获得跟随，立刻标记 `failed-thesis / BOP-acceptance`；
7. 最后才计算结构止损、第一独立支撑/阻力和粗略 R/R。后续走势只能放在结果栏，不能回填入场理由。

## 4. 订单与风险分支

### 分支 A：颈线反向 stop

这是默认研究分支。头肩顶在颈线下方出现信号 K 后，等待 sell-stop；头肩底则对称等待 buy-stop。触发前要冻结：

- 颈线位置和允许的区域宽度；
- 信号 K 的高低点与真实触发价；
- 是否跳空越过触发；
- 触发下方/上方的第一独立支撑或阻力；
- 是否有足够空间让交易至少先走过一个有意义的风险单位。

### 分支 B：颈线回测 limit

只有颈线已被真实突破、角色转换已经出现，且价格后来回测到该区域时，才单列 `limit-retest`。不能因为完整图上后来发生过回测，就假设当时已经挂单成交；跳空越过原触发时要重建新的合同。

### 分支 C：market/close

只有反向收盘很强、结构已被破坏、等待会显著错过，而第一障碍仍有空间时才研究。若大 K 同时带有财报、重大事件或高潮特征，优先降级为观察，不把强收盘自动等同于低风险。

### 分支 D：observation-only

出现以下任一项时保留观察：颈线还不真实、父级在区间中部、第一反向没有跟随、首障碍太近、肩部只是普通回调，或原方向已经接受突破。

## 5. 结构止损、目标与 R/R

头肩研究必须同时记录两种几何，不能混成一个数字：

1. **交易止损**：为了让具体颈线触发合同可执行，可能放在右肩极端外；
2. **结构失效止损**：若价格重新接受头部/主要极端，原来的反转叙事失效，通常要参考头部或母级主要高低点外的区域。

如果交易止损远窄于结构失效范围，必须明确它是低周期短线合同，不能用它包装成日线 MTR 的低风险交易。

目标顺序固定为：

```text
颈线/最近磁铁
→ 第一独立支撑或阻力
→ 只有在前一层被接受后，才看头肩高度投影或 MM
```

头部到颈线的高度可以作为后续测量目标，但不能越过触发前已经可见的主要支撑/阻力。目标区是区域，不是必须精确打到的价格；接近目标后若出现重叠、尾巴、缺口回补或买卖压减弱，可以分批管理。

### Canonical 最小复核卡

`shape_type`、`neckline`、`shoulder_separation`、`rounded_phase` 和 `breakout_state` 是
头肩/圆形的专用观察字段；它们不能合并成一个 pattern 名称，也不能替代统一合同。

```text
contract_scope: deep_review / historical_context_only
data_status: historical / delayed / live_confirmed / incomplete
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
completed_bar_as_of:
timeframes_seen:
chart_scope: full / partial / unavailable
daily_context_window: >=2y / <2y / unavailable
major_high_low_review: complete / partial / unavailable
ema20_50_200_review: complete / partial / unavailable
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
direction: long / short / no_valid_direction
primary_pattern: MTR / RFB / BOP / ABC_CONT / other
secondary_context: head_shoulders / rounded_top_bottom / double_top_bottom / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
shape_type: head_shoulders / inverse_head_shoulders / rounded_top / rounded_bottom / unclear
neckline:
shoulder_separation: clear / partial / absent / unknown
rounded_phase: deceleration / compression / boundary_formed / unclear
breakout_state: not_confirmed / accepted / failed / gap_repriced
signal_bar:
confirmation_bar:
new_trigger:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
gap_policy: accept_open / skip / flag_only / not_applicable
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
structural_stop:
structural_invalidation:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
rough_R_R:
event_context: raw pre-entry event note (examples: none / earnings / macro / gap / other / unknown; dated/compound qualifiers allowed)
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
failure_condition:
```

## 6. 现有案例的边界审计

| 案例 | 视觉上可以怎么叫 | 为什么不能升级为干净的头肩/圆形正例 | 订单与风险结论 |
| --- | --- | --- | --- |
| [`TSLA 2024-03-04–03-14`](tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | 区间上沿的复杂双顶/MTR 候选 | 更主要是区间边缘失败和 L1 失败后的 L2，不是开放趋势中的完整头肩顶 | 有静态空间，但过程先触发结构止损；继续按区间边缘与 MTR 边界使用 |
| [`NFLX 2024-08-05–09-26`](nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | H&S-like / 多次高位测试 / 圆顶警报 | 测试次数超过三次、肩部不对称、首支撑 `66.54–65.98` 太近，后来顶部又被接受 | `67.10` 下方空头触发可重建，但结构止损约 `71.60–71.70`；首障碍约 `0.1–0.25R`，有效 no-trade |
| [`ASML 2025-05-19–06-13`](asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md) | 双底样、圆底/逆头肩的视觉候选 | 只有两次主要下沿测试，随后是重叠与区间过渡，没有清楚的第三结构点和颈线接受 | 不冻结逆头肩订单；先按区间下沿、状态转换和后续 BOP 观察 |
| [`LOW 2024-06-11–06-24`](low_bullish_h1_h2_first_obstacle_boundary_2024-06-11_2024-06-24.md) | 逆头肩-like 的低位恢复候选 | 父级仍是急跌后的过渡，右肩/第二次恢复并未完成主要结构确认，`221.92–223.01` 首阻力拥挤 | 方向上可以研究 buy-stop，但日线结构 R/R 不足，保留 valid no-trade |
| [`TSLA 2025-09-08–09-12`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | 阻力下多次测试，早期可标反转候选 | `2025-09-11` 强收盘越过阻力并得到跟随，原头肩/MTR 空头假设被 BOP 接受否定 | 取消旧的反向订单；若交易，必须按突破接受与回踩的新合同重建 |
| [`RBLX 2024-03-18–04-05`](rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md) | 区间下沿复杂双底/逆头肩-like | 父级宽区间，局部肩部计数不能替代区间边缘逻辑，首目标是中部磁铁 | 区间中部空间和结构止损不配，stop/limit 分支均降级观察 |
| [`KLAC 2025-10-14–10-24`](klac_h1_case_study_2025-10-14_2025-10-24.md) | 普通强趋势旗形，可能被误看成右肩 | 浅 B 后原方向仍有跟随，尚未出现成熟高位和颈线；右肩名称会制造后见之明 | 按 H1/BOP 延续审计，不能因为形状像肩部就反向做空 |

这些案例提供的是边界，不是头肩胜率。当前没有一个事件干净、颈线清楚、第二次反向确认明确、首障碍宽裕且过程完整的标准头肩正例；也没有一个纯粹、独立、可冻结的圆顶/圆底正例。这个缺口必须保留，不能用“看起来像”填成成功样本。

## 7. 可迁移结论

1. 头肩顶/底先归入复杂双顶/双底或 MTR 候选；左右肩不需要等高，但需要分离、父级位置和颈线结构。
2. 圆顶/圆底主要表示推进效率下降和控制权转移，是等待结构确认的背景，不是单独入场形态。
3. 区间中部的头肩外形优先按区间处理；普通趋势中的浅回调优先按 ABC/旗形处理；只有成熟极端、反向破坏和第二次确认同时出现，才升级 MTR。
4. 颈线突破有三种结果：被接受并延续、失败后回到区间、或只是区间内部摆动。三者必须分开记录。
5. 第一反向运动只证明“可能有小反转/区间”，不证明主要趋势已经反转；头肩高度和 MM 只能在第一障碍被接受后作为后续目标。
6. 首障碍、结构止损和实际订单几何优先于形态名称；静态目标看起来很远，不代表路径上能交易。

## 8. 当前停止条件

在找到以下新证据前，本框架保持 `provisional`，不交给 Codex Trading 或 Execution Agent：

- 一个事件干净的头肩顶或底，颈线、第二次确认和结构止损都能在当时冻结；
- 一个与之相似但原方向 BOP 接受的对照；
- 一个真正显示推进减弱、重叠增加、边界形成并在边界突破后有跟随的圆顶或圆底案例。

后续若只找到更多“高位多次测试但首障碍拥挤”的案例，应更新边界总结，而不是继续重复建立同类深审文件。

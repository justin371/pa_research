# Head-and-Shoulders / Rounded Top-Bottom / 头肩顶底与圆顶圆底

文档状态：`document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补头肩/圆顶圆底、颈线和状态转移。三个点本身不产生方向或交易授权。

头肩顶/底是把成熟趋势极端、复杂双顶/双底和颈线结构组织在一起的视觉语言，不是“三个高点/低点”的自动反转信号。圆顶/圆底则描述推进效率下降和控制权逐步转移，更像背景警报；两者都必须经过结构、确认和空间审计。

## 共同图表范围前置

该入口的证据头还必须记录 `data_status: historical / delayed / live_confirmed / incomplete`、`as_of_time`、`chart_scope`、`daily_context_window` 和 `timeframes_seen`；历史、延迟、实时已确认与不完整不能互换。

状态边界：关键图表、事件、触发或空间证据尚不完整时使用 `pending`/`observation_only`；形态、方向和入场几何已可复核但已知硬闸门否决交易时使用 `valid_no_trade`。两者都不建立订单，不能互换。

方向字段边界：完整研究记录统一写 `direction: long / short / no_valid_direction`；方向字段是当前研究合同的方向，不是交易授权。

统一合同映射：本目录的 Head-and-Shoulders/Rounded 是独立复杂结构研究语义；若 `contract_scope: daily_candidate`，`primary_pattern` 仍只写 `ABC_CONT` 或 `BOP`，H1/L1/H2/L2/H3/L3 写入 `internal_label`，其他关系写入 `secondary_context`，`range_edge_three_push` 仅作位置分支。头肩/圆顶名称只在深审/历史记录的独立主题字段或兼容 `other` 中保留，不能扩展日线选股主标签。

BOP 状态迁移：若事前可见边界被日线强收盘越过、获得跟随并在回踩中守住，统一合同改写为 `primary_pattern: BOP`、`state_transition: breakout_acceptance`；本目录的原 pattern/反向 thesis 与旧订单合同失效，必须重建 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间，不能沿用旧 entry/stop/target 或把旧结果并入 BOP。

进入 Head-and-Shoulders/Rounded 判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。强 A 与受控 B 作为成熟趋势和回调质量对照；头肩/圆顶圆底的颈线与控制权边界仍按本目录独立定义。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能凭三个点或局部圆弧升级为可交易反转。

## 最小定义

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
- 颈线来自两个中间摆动并被价格实际验证，可以略倾斜；
- 右肩显示原方向效率下降，并出现反向触发或结构破坏候选；
- 颈线突破后有跟随/回测守住，或失败后重新进入原结构。

肩部不必等高，但必须解释其相对位置。若只能画出复杂双顶/双底而没有真实颈线，保持 `head-shoulder-like`。

### 圆顶/圆底

- 原方向推进逐步变慢，单位价格推进效率下降；
- K 线重叠增加、实体变小、双方交易变多；
- 斜率趋平，随后形成小区间或更大交易区间；
- 最后的方向突破、失败突破或二次入场才决定延续、区间或反转。

圆形本身不提供入场方向，不能在弧线中部猜顶/底。

## 状态分流

| 状态 | 证据 | 默认处理 |
| --- | --- | --- |
| `head-shoulder-like` | 肩/头外形存在，但颈线或父级不完整 | 只做观察，不授权反向 |
| `head-shoulder-candidate` | 颈线、右肩/第二测试和主要位置较清楚 | 等颈线 stop 或第二次确认 |
| `rounded-transition` | 推进变慢、重叠增加、斜率趋平 | 先看小区间/状态转移，不猜拐点 |
| `neckline-break-acceptance` | 强收盘越过颈线、跟随、回测守住 | 转 BOP/MTR 新合同 |
| `neckline-failure` | 越过颈线后重新回到原结构 | 开失败突破/区间边缘分支 |
| `ordinary-flag-or-pullback` | 原趋势强，右侧只是浅回调且无成熟极端 | 按 ABC/H1/H2 延续，不命名右肩 |
| `valid_no_trade` | 首障碍贴近、父级区间中部或事件改变几何 | 观察，保留形态标签但不交易 |

## 颈线、订单与风险

- 默认研究分支是颈线外的 `stop-confirmation`：头肩顶卖出，头肩底买入；触发价、研究/回放中的成交路径和跳空必须分开记录，真实券商/账户成交日志必须来自独立来源。
- 颈线已被真实突破、角色转换清楚且价格回测时，才单列 `limit-retest`；不能因事后发生过回测就假设事前已成交。
- 反向收盘很强、结构已破坏、等待会明显错过且首障碍仍有空间时，才研究 `market/close`。
- 颈线尚未真实、第一反向无跟随、父级在区间中部、首障碍/止损尚未确认或原方向重新接受时，使用 `observation_only`；若首障碍和几何已确认但空间不足，使用 `valid_no_trade`。

交易止损可以放在右肩极端外，但要明确它是低周期短线合同；结构失效止损还要覆盖头部/母级主要极端。目标顺序是颈线/最近磁铁 → 第一独立支撑/阻力 → 颈线高度或 MM 延伸。第一障碍不足约 1R 记为 `valid_no_trade`，约 2R 只是完整波段参考。

## 与相邻 pattern 的边界

- **双顶/双底**：头肩是更复杂的双顶/双底叙事；两次测试与颈线尚不完整时，优先用双顶/双底候选，不强行升级。
- **MTR**：头肩外形只是位置证据；成熟趋势、结构破坏和第二次确认才支持 MTR。
- **三推/H3-L3**：三个高低点不自动是肩/头/肩；次数、压力收缩/扩张和位置应分开。
- **Final Flag**：末端压缩可以形成头肩-like 外观，但突破接受则是延续/BOP，失败才审计反向。
- **普通 ABC/H1-H2**：强趋势中的浅回调没有成熟高位/低位和颈线，优先按延续。
- **圆顶/圆底**：是效率下降和状态转移背景，不是精确的头肩几何或独立入场。

## 当前案例入口

- [`TSLA 2024-03-04–03-14`](../../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md)：区间上沿复杂双顶/MTR 候选，静态空间有但过程先止损；
- [`NFLX 2024-08-05–09-26`](../../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)：H&S-like/高位多次测试，颈线首支撑拥挤；
- [`ASML 2025-05-19–06-13`](../../research/asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md)：双底/圆底/逆头肩-like 过渡，不冻结反转；
- [`LOW 2024-06-11–06-24`](../../research/low_bullish_h1_h2_first_obstacle_boundary_2024-06-11_2024-06-24.md)：低位恢复候选，父级和第一阻力否决；
- [`TSLA 2025-09-08–09-12`](../../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)：阻力下反转观察被 BOP 接受改写；
- [`KLAC 2025-10-14–10-24`](../../research/klac_h1_case_study_2025-10-14_2025-10-24.md)：普通旗形/浅回调对照，不是右肩反转。

专项证据审计见 [`Head-and-Shoulders / Rounded 专项视觉证据审计`](../../research/head_shoulders_rounded_visual_evidence_gap_audit_2026-08-24_CN.md)，基础框架见 [`头肩顶/底与圆顶/圆底视觉边界框架`](../../research/head_shoulders_rounded_top_bottom_visual_framework_CN.md)。

本目录只服务 PA Research 的视觉识别、案例复核、订单语义和 no-trade 判断，不建立量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

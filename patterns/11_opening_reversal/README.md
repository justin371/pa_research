# Opening Reversal / 开盘反转

文档状态：`document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补开盘第一波、事前位置和反向确认。订单、方向和事件状态必须单独记录。

Opening Reversal 研究的是开盘第一波在事前可见的磁铁或结构位失败后，形成反向确认的交易机会。它不是“第一根 K 线反向”，不是“缺口必补”，也不是所有开盘后的 H1/L1。

## 共同图表范围前置

该入口的证据头还必须记录 `data_status: historical / delayed / live_confirmed / incomplete`、`as_of_time`、`chart_scope` 和 `timeframes_seen`；历史、延迟、实时已确认与不完整不能互换。

状态边界：关键图表、事件、触发或空间证据尚不完整时使用 `pending`/`observation_only`；形态、方向和入场几何已可复核但已知硬闸门否决交易时使用 `valid_no_trade`。两者都不建立订单，不能互换。

统一合同映射：本目录的 Opening Reversal 是独立开盘事件研究语义；若 `contract_scope: daily_candidate`，`primary_pattern` 仍只写 `ABC_CONT` 或 `BOP`，H1/L1/H2/L2/H3/L3 写入 `internal_label`，其他关系写入 `secondary_context`，`range_edge_three_push` 仅作位置分支。开盘反转名称只在深审/历史记录的独立主题字段或兼容 `other` 中保留，不能扩展日线选股主标签。

BOP 状态迁移：若事前可见边界被日线强收盘越过、获得跟随并在回踩中守住，统一合同改写为 `primary_pattern: BOP`、`state_transition: breakout_acceptance`；本目录的原 pattern/反向 thesis 与旧订单合同失效，必须重建 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间，不能沿用旧 entry/stop/target 或把旧结果并入 BOP。

进入 Opening Reversal 判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。强 A 与受控 B 作为开盘前背景对照；开盘第一波、事件和反向确认仍按本目录独立定义。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能凭开盘局部 K 线升级为可交易候选。

## 最小定义

```text
盘前背景与关键位置
→ 开盘第一方向推进
→ 在前日高低点 / 区间边缘 / 缺口 / 主要 S/R 处失败
→ 反向 H1/L1，最好有 H2/L2 或第二次确认
→ 结构止损、第一独立障碍和可执行订单
```

开盘方向若被强收盘、跟随和回测接受，应归入 `opening-drive-continuation` 或 BOP；早期双方反复则归入 `opening-range-transition`。只有失败、反向触发和空间同时存在，才进入 `opening-reversal-candidate`。

## 必须先看

- 前日高低点、主要支撑/阻力、区间边缘和隔夜缺口；
- 大盘、板块和财报/事件背景；
- 开盘是跳空、越过结构、区间内还是直接重叠；
- 第一波是接受、失败还是尚未确认；
- 反向信号 K、触发 K、实际成交和后续跟随必须分开记录。

## 订单与风险

- 默认研究分支是信号 K 外的 `stop-confirmation`；
- 已确认角色转换后的回测，才可另开 `limit-retest`；
- 强反向收盘可研究 `market/close-confirmation`，但要接受更宽止损和滑点；
- 开盘跳过原 stop 时，按实际可成交价格重订，不保留理想价格；
- 结构止损放在开盘极端、前日结构位或真正失效点外；
- 先看第一独立支撑/阻力，再看 MM；首障碍拥挤就是 `valid_no_trade`；
- 财报前三个交易日不新开仓，这是用户覆盖规则，不是本形态的原始定义。

特别注意：价格在 `284.65` 时，挂在 `284.50` 的卖出限价通常是可立即成交的 marketable limit，不是等待价格下跌；等待下破用 sell stop，等待反弹回测才是新的 sell-limit/retest 合同。

## 与相邻 pattern 的边界

- **BOP / gap-and-go**：第一方向被接受时优先归 BOP，不能一边接受一边做旧的反转假设；
- **Final Flag**：开盘可能触发最后一次失败，但 Final Flag 还要求趋势末端背景；
- **失败突破/高潮**：开盘失败可以是失败突破证据，但需要开盘时段和反向触发；
- **区间边缘二次入场**：成熟区间边缘优先用区间逻辑，Opening Reversal 只记录开盘触发层；
- **H1/L1**：普通趋势回调没有开盘第一方向失败，不事后改名 Opening Reversal；
- **MTR**：开盘反转至多是 MTR 的早期证据，不能凭一根开盘反向 K 宣布大级别反转。

## 当前案例入口

- [`RBLX 2024-04-04`](../../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)：开盘上冲失败，但区间中部和信号质量使其 no-trade；
- [`COIN 2024-01-09`](../../research/coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md)：空头开盘反应，首支撑拥挤；
- [`VRT 2026-04-17`](../../research/vrt_bullish_abc_h1_deep_b_first_obstacle_boundary_2026-04-14_2026-04-20.md)：开盘接受/原 stop 被跳过，不是反转；
- [`TSLA 2025-03-04`](../../research/tsla_abc_playbook_2025-03-04_284_retest.md)：跳空延续、订单重订与回测语义。

专项证据审计见 [`Opening Reversal 专项视觉证据审计`](../../research/opening_reversal_visual_evidence_gap_audit_2026-08-24_CN.md)，基础框架见 [`开盘反转视觉研究框架`](../../research/opening_reversal_visual_framework_CN.md)。

本目录只服务 PA Research 的视觉识别、订单语义和 no-trade 判断，不建立量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

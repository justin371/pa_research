# Final Flag / 最终旗形

文档状态：`document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补趋势末端、最后一次原方向尝试和状态分流。没有完整合同的内容只能标为 `historical_context_only`。

Final Flag 是 Al Brooks PA 中的背景型结构：趋势已经走了相当一段，接近末端时出现小型反向回调或窄区间，最后一次原方向尝试可能失败，随后先出现小反转、平衡或交易区间。它不是“所有小旗形”的名称，也不是自动反转信号。

## 共同图表范围前置

该入口的证据头还必须记录 `data_status: historical / delayed / live_confirmed / incomplete`、`as_of_time`、`chart_scope` 和 `timeframes_seen`；历史、延迟、实时已确认与不完整不能互换。

状态边界：关键图表、事件、触发或空间证据尚不完整时使用 `pending`/`observation_only`；形态、方向和入场几何已可复核但已知硬闸门否决交易时使用 `valid_no_trade`。两者都不建立订单，不能互换。

进入 Final Flag 判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。强 A 与受控 B 用于判断趋势是否成熟、回调是否受控；Final Flag 仍按本目录独立定义，不自动改写成 H/L、ABC 或 MTR。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能凭末端小旗形升级为可交易候选。

## 最小定义

```text
持续趋势 / 多次推进
→ 趋势变晚、接近极端或主要磁铁
→ 小型回调或窄区间
→ 最后一次原方向尝试
→ 接受并延续，或失败后反向/进入区间
```

必须同时看到：

- 左侧趋势已经运行较久，或已接近重要位置；
- 旗形内部是压缩、重叠增加、推进变慢，而不是一条强反向 A 腿；
- 最后一次突破的接受/失败能够在当时判断；
- 反向交易有跟随、第二次确认、结构止损和第一独立障碍。

没有末端背景的普通趋势旗形，归入 `trend_flag_continuation`；有成熟区间背景的窄平台，先按区间；形成强反向趋势，则转 MTR/新趋势。

## 三种状态

| 状态 | 含义 | 默认处理 |
| --- | --- | --- |
| `trend_flag_continuation` | 原方向突破并接受 | 转 BOP/延续合同，不做反向猜测 |
| `final_flag_reversal_candidate` | 趋势末端、最后尝试失败、反向出现结构证据 | 等 L2/H2 或第二次反向确认 |
| `final_flag_range_transition` | 窄区间被破坏但双方仍反复 | 先按小交易区间或观望 |

## 订单和风险

- 反向默认用 signal bar 外的 `stop` 等确认；第一根反向 K 不是主要反转授权；
- `limit-retest` 只用于已确认的边界/角色转换回测，不能在尚未失败时猜极值；
- 原方向强收盘越过边界并有跟随时，原反转假设失效，必须新建 BOP 合同；
- 止损覆盖旗形上/下沿、最后测试极端和真正失效位置，不能用局部影线制造虚假 R/R；
- 第一目标先看旗形边界、最近左侧支撑/阻力或区间中部，再看 MM；首障碍过近时 `valid_no_trade`；
- 财报前三个交易日不新开仓；板块、市场、跳空和事件先于形态标签。

## 与相邻 pattern 的边界

- **普通旗形 / ABC / H1-H2**：趋势中段的受控回调仍是延续；不要因为后来失败就事后改叫 Final Flag。
- **MTR**：Final Flag 只提供末端压缩背景；只有结构破坏、第二次确认和空间齐全才升级 MTR。
- **BOP**：原方向突破接受后，Final Flag 反向 thesis 结束，转 BOP。
- **失败突破/高潮**：失败突破或高潮可以触发 Final Flag 审计，但两者并不等价。
- **VCP**：VCP 是 Minervini 的独立收缩/pivot 体系；Final Flag 不使用 VCP 的 T1/T2/T3 语言。

## 当前案例入口

- [`KLAC 2025-10-14–10-24`](../../research/klac_h1_case_study_2025-10-14_2025-10-24.md)：强趋势浅旗，延续/首阻力边界；
- [`NFLX 2024-08-05–09-26`](../../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)：高位压缩、反向 L1-like，但首支撑拥挤；
- [`TSLA 2025-09-08–09-12`](../../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)：反转假设被突破接受改写为 BOP；
- [`KLAC 2025-03-12–03-28`](../../research/klac_h3_bear_flag_case_2025-03-12_2025-03-28.md)：熊旗延续控制，不自动升级 Final Flag；
- [`COST 2024-07-11–07-18`](../../research/cost_bearish_abc_climax_boundary_2024-07-11_2024-07-18.md)：强 A/高潮边界，首障碍不足。

专项证据审计见 [`Final Flag 专项视觉证据审计`](../../research/final_flag_visual_evidence_gap_audit_2026-08-24_CN.md)，基础框架见 [`最终旗形视觉工作框架`](../../research/final_flag_visual_framework_CN.md)。

本目录只服务 PA Research 的视觉识别、案例复核和 no-trade 判断，不建立量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

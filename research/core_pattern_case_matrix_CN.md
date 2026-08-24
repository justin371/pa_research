# 核心八个 Pattern 代表性案例矩阵 V0.1

日期：2026-08-23  
状态：`visual-research / case-matrix / not-statistical`

## 使用方式

这张矩阵只做导航和缺口管理，不是胜率表。每个 pattern 至少保留：

- 一个值得继续审计的条件性候选；
- 一个形态像但被首障碍、事件、计数、跳空或状态否决的边界；
- 一个能够防止误读的反例或缺口说明。

案例的结论只依据入场决策时可见的结构。后续达到 MM、反转或盈利，只能作为路径审计，不能回写成原始入场证据。

## 八个 pattern 矩阵

| Pattern | 条件性候选 | 边界 / no-trade | 反例或当前缺口 |
| --- | --- | --- | --- |
| [`H1/L1 第一次入场`](../patterns/01_h1_l1_first_entry/README.md) | [`AAPL 2024-05-03–05-09`](aapl_bullish_h1_event_driven_a_2024-05-03_2024-05-09.md)：事件后强 A、浅 B、H1-like，作为 event-driven 条件候选；[`KLAC 2025-10-14–10-24`](klac_h1_case_study_2025-10-14_2025-10-24.md)：强 A、一天浅 B、setup/confirmation 分离，财报过滤通过但事件临近 | [`COST 2024-05-13–05-16`](cost_bullish_h1_first_obstacle_boundary_2024-05-13_2024-05-16.md)：信号 K 和 A 都像，但首阻力贴近，`valid_no_trade` | [`JNJ 2025-09-18–10-08`](jnj_bullish_h1_first_obstacle_2025-09-18_2025-10-08.md)、[`JPM 2025-08-22–09-05`](jpm_bullish_h1_first_obstacle_failure_2025-08-22_2025-09-05.md)：形态恢复清楚但首阻力阻塞；本轮专项审计仍为 `no-new-positive`，缺事件干净、开放趋势、首障碍宽裕的普通基准 |
| [`H2/L2 第二次入场`](../patterns/02_h2_l2_second_entry/README.md) | [`KLAC 2025-05-07–06-03`](klac_h2_case_study_2025-05-07_2025-06-03.md)、[`CRWD 2024-09-11–10-11`](crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md)：前者是支撑/EMA 汇合，后者补深 B 后段稳定与低周期确认 | [`SNOW 2026-08-14–08-21`](snow_bullish_h2_first_obstacle_boundary_2026-08-14_2026-08-21.md)：H2-like 清楚但第一阻力不足；低周期也不能替日线空间；[`TSLA 2025-08-06–08-22`](tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) 的日线合同同样 no-trade | [`TSLA 2024-03-04–03-14`](tsla_bearish_abc_case_2024-03-04_2024-03-14.md)：无事件且 L2 计数清楚，但父级偏区间边缘、过程先止损；空头开放趋势中首障碍宽裕的对称正例仍缺 |
| [`ABC 趋势延续`](../patterns/03_abc_continuation/README.md) | [`NFLX 2025-02-14–03-28`](nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md)、[`TSM 2025-02-14–03-28`](tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md)：方向性 A、受控 B、分别提供无缺口与缺口重订的 L1 合同；[`CRWD 2024-09-11–10-11`](crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md) 补多头深 B/H2 分支 | [`QCOM 2025-02-21–03-28`](qcom_bearish_abc_range_b_boundary_2025-02-21_2025-03-28.md)：B 变宽、重叠多，后续不能自动继承开放趋势 ABC | [`RBLX 2024-03-18–04-05`](rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)：区间边缘而非趋势 ABC；仍缺事件干净、开放趋势、A/B/C 路径清楚且空间宽裕的普通 H1/L1 对称基准 |
| [`区间边缘二次入场`](../patterns/04_range_edge_second_entry/README.md) | [`RBLX 2024-03-18–04-05`](rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)：区间边缘与趋势腿计数分开，适合研究 second-leg trap | [`TSLA 2025-03-11–05-13`](tsla_range_after_sell_climax_2025-03-11_2025-05-13.md)：卖出高潮后进入区间，不能把早期冲量继续当 ABC | [`QCOM 2025-02-21–03-28`](qcom_bearish_abc_range_b_boundary_2025-02-21_2025-03-28.md)：宽 B/过渡边界；仍缺事件干净、上下沿都清楚且首目标空间宽裕的双向对照 |
| [`失败突破与高潮`](../patterns/05_failed_breakout_climax/README.md) | [`TSLA 2024-03-04–03-14`](tsla_bearish_abc_case_2024-03-04_2024-03-14.md)：区间上沿失败后 L1/L2 反向确认，静态空间较好但过程先破结构止损，条件候选 | [`TSLA 2025-03-11–05-13`](tsla_range_after_sell_climax_2025-03-11_2025-05-13.md)、[`RBLX 2024-03-18–04-05`](rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)：高潮后区间/区间边缘失败，首障碍或信号质量否决 | [`TSLA 2025-09-08–09-12`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)、[`COST 2024-07-11–07-18`](cost_bearish_abc_climax_boundary_2024-07-11_2024-07-18.md)：前者转 BOP，后者强 A 但空间不足；专项审计仍为 `no-new-positive` |
| [`突破回踩 / BOP`](../patterns/06_breakout_pullback_bop/README.md) | [`TSLA 2025-09-08–09-12`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)：阻力外强收盘接受，旧 MTR/区间合同废弃；[`TSLA 2025-03-04 284 回测`](tsla_abc_playbook_2025-03-04_284_retest.md)：旧位回测形成独立 limit-retest 条件合同 | [`GOOGL 2024-03-04–03-22`](googl_bullish_h1_gap_trigger_boundary_2024-03-04_2024-03-22.md)、[`WMT 2024-06-24–06-27`](wmt_bullish_h1_gap_pullback_boundary_2024-06-24_2024-06-27.md)：方向或形态正确，但跳空/首障碍/信号质量使其 no-trade | [`QCOM 2024-07-24`](qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md)、[`NKE 2025-10-28`](nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md)：空头重订/回测边界；仍缺事件干净、回踩守住、首障碍宽裕的多空普通基准 |
| [`MTR 趋势反转`](../patterns/07_mtr_reversal/README.md) | [`TSLA 2024-03-04–03-14`](tsla_bearish_abc_case_2024-03-04_2024-03-14.md)：区间上沿重叠的 MTR candidate，L1 失败后 L2 清楚但过程止损优先 | [`NFLX 2024-08-05–09-26`](nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)、[`LOW 2024-06-11–06-24`](low_bullish_h1_h2_first_obstacle_boundary_2024-06-11_2024-06-24.md)：反向证据存在，但首支撑/阻力或父级状态否决 | [`ASML 2025-05-19–06-13`](asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md)、[`PLTR 2024-12-24–2025-01-08`](pltr_bearish_abc_l1_ordinary_a_boundary_2024-12-24_2025-01-08.md)：双底/双顶样外观分别落入区间过渡或普通回调；仍缺无事件、结构破坏、二次确认和首障碍宽裕的双向正例 |
| [`三推 / H3-L3`](../patterns/08_three_push_h3_l3/README.md) | [`KLAC 2025-03-12–03-28`](klac_h3_bear_flag_case_2025-03-12_2025-03-28.md)：熊旗顶部第三推受阻后有空头接受，唯一保留的条件性 H3 候选 | [`NFLX 2024-08-05–09-26`](nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)、[`UBER 2024-07-17–07-26`](uber_bearish_h3_l2_first_support_boundary_2024-07-17_2024-07-26.md)：形态或第三推外观存在，但首障碍拥挤/第三推扩张否决 | [`TSLA 2025-03-07–03-10`](tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md)、[`ASML 2025-05-19–06-13`](asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md)：L3 扩张或区间重复；L3 仍为 `no-new-positive` |

## 本轮补充

H1/L1、H2/L2 与 ABC 的证据缺口审计见[`H1/L1、H2/L2 与 ABC 证据缺口审计`](h1_h2_abc_evidence_gap_audit_2026-08-23_CN.md)。本轮新增的是 CRWD 的深 B/H2 及 TSM 的 gap-reprice 订单分支；H1/L1 普通开放趋势纯净基准仍记为 `no-new-positive`，不再复制同质边界。

H2/L2 的独立专项审计见[`H2/L2 第二次入场专项视觉证据审计`](h2_l2_visual_evidence_gap_audit_2026-08-24_CN.md)。最新结论是：多头 H2 为条件性覆盖，空头 L2 仍为 `no-new-positive`；低周期窄止损、高周期结构止损、静态 R/R 和真实路径必须分开。

H1/L1 的独立专项审计见[`H1/L1 第一次入场专项证据审计`](h1_l1_visual_evidence_gap_audit_2026-08-24_CN.md)。KLAC 只新增 setup/confirmation 与事件窗口边界，不改变 `no-new-positive` 结论。

BOP 的独立专项审计见[`突破回踩 / BOP 专项视觉证据审计`](bop_visual_evidence_gap_audit_2026-08-24_CN.md)。TSLA 2025-09 主要是突破接受，TSLA 2025-03 才是旧位回测；当前 `event-clean / parent-clear / first-obstacle-space-positive / process-complete` 仍为 `no-new-positive`。

三推/H3-L3 的独立专项审计见[`三推/H3-L3 专项视觉证据审计`](three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md)。本轮保留 KLAC 的 H3 条件候选，确认 L3 尚无完整衰竭正向合同，并把扩张/高潮、区间重复和通道延续作为独立边界。

失败突破与高潮的独立专项审计见[`失败突破与高潮专项视觉证据审计`](failed_breakout_climax_visual_evidence_gap_audit_2026-08-24_CN.md)。TSLA 2024-03 是最接近的失败突破/MTR 条件候选，但过程先破结构止损；TSLA 2025-03 先进入区间，TSLA 2025-09 转 BOP，COST/RBLX 被首障碍、信号或事件边界否决。

## 跨矩阵的共同结论

1. **候选与可交易性必须分栏**：AAPL、KLAC、TSLA 等可以进入条件性研究，不代表可以直接下单。
2. **首障碍是最常见的否决**：COST、SNOW、GOOGL、NFLX 的形态并不一定差，问题在于触发后先遇到的结构不留空间。
3. **状态切换比标签更重要**：TSLA 2025-09 从反转假设切到 BOP；TSLA 2025-03 从高潮进入区间；ASML 从三推样外观切到区间过渡。
4. **第三推要与扩张并列**：KLAC 提供受阻候选，TSLA L3 和 XOM/COIN 研究提供扩张/高潮边界，不能只收集“第三推变弱”的图。
5. **真正的空白不是再找更多相似图**：当前最有价值的缺口是事件干净、双向、第二次确认明确、首障碍宽裕的开放趋势反转/三推正例，以及 BOP 回踩守住的清楚对照。

## 下一轮案例选择规则

只有出现以下一种新信息，才值得增加案例：

- 填补某个方向缺口（例如 L3 衰竭，或区间底部多头）；
- 填补订单缺口（原 stop、开盘重订、limit-retest 或低周期确认的独立分支）；
- 填补状态转换缺口（失败突破转 BOP、三推转 MTR、ABC 转区间）；
- 填补首障碍几何缺口（清楚的空间正例或首障碍先到的反例）。

若只是另一张同样的“强 A + H2-like + 首阻力过近”图，保留引用即可，不再复制深审。

## 边界

MTR/L3 的最新缺口审计见[`MTR 与三推证据缺口审计`](mtr_three_push_evidence_gap_audit_2026-08-23_CN.md)。

MTR 的独立专项审计见[`MTR 主要趋势反转专项视觉证据审计`](mtr_visual_evidence_gap_audit_2026-08-24_CN.md)。当前仍把 `reversal_attempt`、`MTR-candidate`、`failed-MTR-thesis` 和 `valid_no_trade` 分开，不把三推/双顶或后续结果自动升级为反转正例。

矩阵只服务 PA Research 的视觉筛选和人工复核，不建立统计胜率、不创建量化扫描器、不修改 Codex Trading，也不连接 Execution Agent。

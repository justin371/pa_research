# Round4 历史图表视觉练习与 H/L/ABC 复核（2026-08-24）

状态：`visual-research / practice-and-boundary-only / not-statistical`

## 一、范围与口径

本轮只研究历史图表。pattern、lineage、reset、两年左侧背景和字段缺失，统一按 PA Research 当前的[`H/L lineage 与三推状态视觉边界复核`](h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)、[`完整图表视觉复核工作流边界审计`](visual_review_workflow_boundary_audit_2026-08-24_CN.md)和[`视觉 pattern 快筛协议`](visual_pattern_triage_protocol_CN.md)执行。Codex Trading 只提供历史 OHLC 图表素材，不提供规则。

本轮不把图上的近似外形直接写成严格 H1/L1/H2/L2，不把图表练习写成胜率、交易许可或生产结论。

## 二、图表练习资产

资产入口：[`Round4 历史图表视觉练习资产`](assets/visual_recognition/2026-08-24/round4_historical_practice/README.md)。

本轮先看 42 个标的的无标签 Daily 筛选板，再放大 7 个旧登记日期和 8 张额外选取的 Daily/4H/15m 图；其中 5 个标的与 targeted 组重叠，实际新增 3 个不同标的（GOOGL、MSFT、XOM）。筛选板和局部图都在截断日期停止，避免把后续走势倒灌到识别时点。MRVL 另有独立 Daily 复核图。

重要限制：Round4 的 cohort3 Daily 只从 `2025-08-11` 开始，新增案例均不能诚实地声称完成两年左侧背景；统一写为 `two_year_daily: pending`。PA Research 之前已有的两年资产（AAPL、NVDA、SPY、RBLX、MAR、TSLA）仍是完整背景参考，不能与 Round4 的短窗口样本混成同一证据层。

## 三、7 个 targeted 历史日期

下表先记录图上可见字段，再给出保守的 pattern 读法。EMA 是在截断日期用该 bars 的收盘递推重算，20/60 日高低区间是位置参照，不是自动支撑阻力线。

| 案例与图 | 两年 Daily、EMA20/50/200、重要高低点与支撑阻力 | 母腿/尝试/lineage 与图形读法 | 首障碍候选与关键限制 |
| --- | --- | --- | --- |
| [`NKE 2026-04-22`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_NKE_targeted_unlabeled.png) | 可见 Daily `2025-08-11`–`2026-04-22`，两年不足；EMA 约 `46.68/51.57/61.22`；近 20 日约 `41.72–53.74`，近 60 日约 `41.72–67.43`。`41.7–45` 是近端低位支撑，`51.6–53.7` 和 `61` 附近是反向压力。 | Daily/4H 是长期偏空、后段继续走低；15m 是低位反弹，不足以把前面多次下跌强行计成 L2。读作 `bearish continuation / L1-like boundary`，`lineage: late-trend-unclear`，不冻结 H/L。 | 近端 `41.7` 支撑可作空头路径的障碍候选，但没有冻结成交、结构止损和独立首障碍；两年背景缺失、局部反弹与主周期不一致。旧登记的 L1 标签不覆盖图上缺口。 |
| [`COP 2026-04-28`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_COP_targeted_unlabeled.png) | 可见 Daily 至 `2026-04-28`；EMA 约 `121.81/118.56/103.76`；近 20 日约 `111.38–134.20`，近 60 日约 `98.99–134.87`。`118–122` 是 EMA/回撤汇合区，`134–135` 是明显前高压力。 | Daily 母腿保持多头，4H 可见强推进后的一次回撤与恢复，15m 后段继续向上；最接近 `ABC-like + H1-like`，但第一次尝试是否独立、是否同一 lineage 仍为 provisional。 | `134–135` 是首个可见压力候选；低周期没有在本记录中冻结独立 signal/follow-through。结果：`pattern_candidate / same-lineage-provisional / two_year_daily-pending`。 |
| [`AMZN 2026-03-04`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_AMZN_targeted_unlabeled.png) | 可见 Daily 至 `2026-03-04`；EMA 约 `212.94/220.72/225.09`；近 20 日约 `196.00–238.86`，近 60 日约 `196.00–248.94`。`196–200` 是低位支撑，`220–225` 及 `238–249` 是上方压力/磁铁。 | Daily 父级不是清楚的开放多头趋势，4H 仍偏空，15m 只是缺口后的恢复；图上没有足够证据支持旧登记的 H2 读法。`parent_state: mixed/transition`，`lineage: unclear`，结果 `not_abc / boundary_candidate`。 | `220–225` 是多头恢复首先面对的压力候选；没有明确同一回调的第一次失败和第二次有意义尝试，也没有两年左侧背景。 |
| [`DE 2026-05-11`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_DE_targeted_unlabeled.png) | 可见 Daily 至 `2026-05-11`；EMA 约 `579.41/576.22/534.64`；近 20 日约 `556.32–600.88`，近 60 日约 `548.25–670.49`。`556–580` 是回撤/EMA 支撑带，`600–617` 是近端压力，`670` 附近是更高前高。 | Daily 母级偏多，但 4H/15m 是宽幅双向、重叠较多；可以练习 `ABC-like + H2-like boundary`，不能冻结为同一 lineage 的 H2。`lineage: unclear-to-range`。 | `600–617` 为最近阻力候选；宽幅、重复测试和局部周期不一致是主要限制。旧登记 H2 只作待复核线索。 |
| [`JNJ 2026-05-13`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_JNJ_targeted_unlabeled.png) | 可见 Daily 至 `2026-05-13`；EMA 约 `226.54/229.70/211.89`；近 20 日约 `219.11–236.78`，近 60 日约 `219.11–250.27`。`219–224` 是回撤支撑，`236–250` 是上方阻力簇。 | Daily 长期多头，但 4H 先下行，15m 末段强力恢复；形状可作为 `ABC-like + H2-like hypothesis` 练习，却缺少可分离的第一次失败/第二次尝试和跨周期一致性。`lineage: provisional`。 | `236–250` 是恢复后首先面对的阻力簇；两年背景、清楚的 H2 计数和低周期确认均不足。旧登记的结果不用于提升该图的等级。 |
| [`NFLX 2026-05-15`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_NFLX_targeted_unlabeled.png) | 可见 Daily 至 `2026-05-15`；EMA 约 `90.33/92.28/100.29`；近 20 日约 `85.10–97.60`，近 60 日约 `75.01–108.94`。`85` 与 `75` 是下方支撑候选，`97–100` 是反弹压力。 | Daily/4H 都显示偏空母级，期间有反弹再下行；可练习 `bearish ABC-like + L1/L2-like`，但第一次失败和第二次尝试的分离质量不足，`lineage: provisional`，不能冻结 L2。 | `85` 是最近空头路径的首个支撑候选，空间是否足够未按统一合同冻结；两年背景不足、15m 混合、旧登记 L2 不替代图上计数。 |
| [`META 2026-05-26`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_META_targeted_unlabeled.png) | 可见 Daily 至 `2026-05-26`；EMA 约 `615.94/623.91/662.01`；近 20 日约 `592.05–677.55`，近 60 日约 `519.78–690.88`。`592–605` 是近端低位，`624–662` 是反弹压力带。 | Daily 偏空/过渡；4H 从下跌转为底部横向，15m 主要是重叠区间。没有清楚的 A→B→第一次失败→第二次尝试，故 `not_clean_h2 / boundary_candidate`，`lineage: unclear-to-range`。 | `624` 附近是多头恢复首先面对的压力，`592` 是下方边界候选；区间重叠、两年缺失和计数不清楚。 |

## 四、额外 3 个不同标的练习

Round4 还直接看了 GOOGL、MSFT、XOM 的截断到 `2026-07-29` 的 Daily/4H/15m 图。它们不是旧登记行的结果复核，而是为了增加不同背景的练习：

| 标的 | 图上读法 | PA Research 处置 |
| --- | --- | --- |
| [`GOOGL`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_GOOGL_MTF_unlabeled.png) | Daily `2025-08-11`–`2026-07-29`；EMA 约 `344.69/352.00/321.86`；近 20 日约 `314.90–375.27`，近 60 日约 `314.90–408.37`。`315–322` 是回撤/EMA200 支撑，`352–375` 与 `408` 是上方阻力。Daily 长期多头但截止点回到 EMA20/50 下方；4H 仍有下行段，15m 只是低位恢复。 | `ABC-like boundary / lineage unclear / two_year_daily-pending`；像“多头 A 后深回撤/状态切换”，不是可直接冻结的 H2。首个反向磁铁先看 `EMA50/352` 与近期反弹高点；不能把低周期恢复倒灌成 Daily H2。 |
| [`MSFT`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_MSFT_MTF_unlabeled.png) | Daily `2025-08-11`–`2026-07-29`；EMA 约 `389.76/394.21/427.01`；近 20 日约 `373.35–405.99`，近 60 日约 `349.20–466.32`。`349–373` 是支撑带，`394–427` 是反弹压力。Daily 从高位转为偏空，4H 下行后横向，15m 出现反弹但仍有反复。 | `bearish continuation / L1-like boundary`；父级从趋势转过渡，`lineage: unclear-to-range`。首个空头路径障碍候选是 `373` 附近低点，但未冻结结构止损或空间；计数应保守，不能把局部反弹叫作新 L2。 |
| [`XOM`](assets/visual_recognition/2026-08-24/round4_historical_practice/US_XOM_MTF_unlabeled.png) | Daily `2025-08-11`–`2026-07-29`；EMA 约 `149.06/147.23/138.41`；近 20 日约 `135.63–159.07`，近 60 日约 `134.95–163.68`。`135–149` 是支撑/汇合带，`159–164` 是高位阻力。Daily 长期上行，后段宽幅震荡；4H/15m 多次来回穿越 EMA，局部 H1 外形存在但位置和重复测试混杂。 | `H1-like / mature-range boundary`，`lineage: unclear-to-range`；首障碍候选是 `159–164`，但重复测试和父级成熟度不允许冻结开放趋势 ABC 或同一 lineage H1。 |

三者的 Daily 数值背景均只覆盖约 `2025-08-11`–`2026-07-29`，所以两年字段继续是 `pending`；它们的作用是练习“何时不计数”。

## 五、练习结论

1. **最有帮助的近似形状**：COP 的 `ABC-like + H1-like`、NFLX 的 bearish `ABC/L1-L2-like`、JNJ 的 `H2-like hypothesis` 和 DE 的 `H2-like boundary`。它们都只能停在 `pattern_candidate`、`boundary_candidate` 或 `count-pending`。
2. **最有帮助的反例**：AMZN、META、NKE、GOOGL、MSFT、XOM 展示了父级转区间/过渡、局部周期冲突、晚趋势和重复测试如何阻止强行贴 H/L 标签。
3. **PA Research 的两年规则仍有效**：Round4 增加了图形练习数量，但没有增加一个完成两年左侧背景、同一 lineage、完整字段和可比较结果的样本；短窗口统一保留 `two_year_daily: pending`。
4. **结果不倒灌**：本轮没有把旧登记的 win/loss 或后续走势写成视觉证据；也没有把近似形状升级为胜率、规则或授权结论。

```text
daily_screen_symbols: 42
targeted_multitimeframe_cases: 7
additional_multitimeframe_practice_cases: 3
directly_reconstructed_mrvl_case: 1
round4_strict_same_lineage_freezes: 0
round4_two_year_daily_complete_cases: 0
new_comparable_positive_samples: 0
no_new_positive: maintained
```

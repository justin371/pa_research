# 常用高质量候选形态清单 V0.1

状态：研究候选；尚未证明“高胜率”，尚未进入生产规则或程序化回测。

本文件的目标是先建立形态目录，不急着把任何一个形态包装成自动交易系统。严格的三推楔形反转规则暂不冻结，但 H3/L3 的视觉候选、延续反例、区间边界和 no-trade 样本可以继续收集。

## 1. 先统一几个名字

### H1/H2/H3 与 L1/L2/L3

本项目先采用 Price Action 的操作性语言：

| 标签 | 含义 |
| --- | --- |
| H1 | 多头背景中，回调结束后的第一次向上尝试 |
| H2 | 第一次向上尝试失败或回调再走一腿后的第二次向上尝试 |
| H3 | 第三次向上尝试；常提示复杂回调、迟到的延续或压力变化 |
| L1 | 空头背景中，回调结束后的第一次向下尝试 |
| L2 | 第一次向下尝试失败或反弹再走一腿后的第二次向下尝试 |
| L3 | 第三次向下尝试；常提示复杂回调、迟到的延续或压力变化 |

H2/L2 往往比第一次尝试更值得优先研究，但这不是无条件的胜率结论。H3/L3 也不是“三推楔形”的同义词；严格的三推楔形规则暂不冻结，但 H3/L3 的视觉候选、延续反例和边界样本仍可继续研究。

参考库中的扫描器还使用 H1/H2/H3、L1/L2/L3 表示“冲量之后的一、二、三条逆趋势腿”的描述性 proxy。这个 proxy 只能帮助召回样本，不能替代因果的信号、触发、止损和空间判断。

### ABC 与几何 AB=CD 不是同一套字母

- **本项目的 ABC**：A 是第一条方向腿，B 是回调，C 是原方向恢复；它是 Price Action 的操作性结构标签，不依赖外部波段体系。
- **几何 AB=CD**：A→B 是第一段方向腿，C 是回调后的第二段起点，D 是从 C 投影出的目标；它描述价格距离。

以后案例中分别记录 `A_leg/B_pullback/C_resumption` 和 `measure_A/B/C/D`，避免把结构标签和测量锚点混为一谈。

## 2. 什么才算“高质量候选”

“高胜率”暂时只作为研究目标。一个形态至少要同时检查：

1. **背景**：趋势、区间、转换或高潮是否清楚；
2. **位置**：前高/前低、结构区、突破区、通道边界或其他可事先看到的磁铁；
3. **形态**：A 腿、B 回调、C 恢复和 H/L 尝试次数能否按当时已完成的 K 线定义；
4. **触发**：信号 K 线、下一根确认和执行价格是否事先冻结；
5. **空间**：第一独立障碍、AB=CD 或 measured move 目标是否给出足够空间；
6. **风险**：结构止损、跳空、成本和失效条件是否明确。

只看到一个 H2、一个 ABC、一个比例或一根漂亮的 K 线，不能单独称为高质量交易机会。

## 3. 第一批优先研究的候选

| 优先级 | ID | 候选形态 | 结构定义 | 研究触发 | 测量/目标 | 主要失效 |
| --- | --- | --- | --- | --- | --- | --- |
| A | `TPB-H2-L2` | 强趋势中的二次入场（目录见 [`H2/L2 第二次入场`](../patterns/02_h2_l2_second_entry/README.md)） | 方向性 A 腿之后，B 回调出现两次有意义的反向尝试；多头看 H2，空头看 L2 | 关键支撑/阻力被触及并守住；信号 K 后由下一根 K 线确认方向 | 前一腿等距、AB=CD 或下一道结构磁铁；先看第一障碍 | 区间中部、回调已接受反向结构、没有跟随、障碍太近 |
| A | `ABC-CONT` | 强趋势 ABC 延续（目录见 [`ABC 趋势延续`](../patterns/03_abc_continuation/README.md)） | A 是可见的方向腿，B 是受控回调，C 恢复原方向；B 尚未演化成双向交易区间 | C 在结构位置形成方向性信号并得到确认 | `Leg1 = Leg2`、AB=CD、或 A 腿终点后的下一个独立磁铁 | A 其实是高潮/区间内脉冲；B 过度重叠；C 未恢复或重新跌回区间 |
| A | `BOP-ABC` | 突破后的 ABC 回踩（目录见 [`突破回踩 / BOP`](../patterns/06_breakout_pullback_bop/README.md)） | 先有被接受的突破，随后 B 回踩突破区，C 再次离开突破区；gap-and-go 作为无回踩的独立分支 | 多头回踩守住旧高上方、空头守住旧低下方，并出现重新突破/确认；详见[`BOP / gap acceptance visual framework`](../research/bop_gap_acceptance_framework_CN.md) | 突破前区间高度、A 腿等距、下一道结构障碍 | 收盘重新接受回旧区间；突破没有跟随；回踩变成失败突破；开盘跳过后仍沿用旧成交价 |
| A | `RFB-SECOND` | 区间边缘失败突破后的二次入场（目录见 [`区间边缘二次入场`](../patterns/04_range_edge_second_entry/README.md)；框架见 [`range-edge framework`](../research/range_edge_second_entry_framework_CN.md)） | 价格在已知区间边缘刺破后重新进入区间；反向尝试再次失败 | 区间边缘重新收回后，出现方向一致的 H2/L2 或等价确认 | 区间边缘、区间高度和中点是目标参考，不预设一定到达 | 发生在区间中部；重新进入后没有跟随；区间边缘未被事先确认 |
| A | `MTR-ABC` | 主要位置上的反转 ABC | 成熟趋势/通道出现 A-B-C 反转结构，同时有双顶/双底、趋势线破坏或失败突破证据 | 第二次反向尝试突破信号 K，并在结构失效点外设止损 | 先看最近磁铁，再看 AB=CD 或 measured move；目标是区域而非单点 | 只是趋势中的普通回调；反向突破没有接受；止损空间过大；详细视觉框架见[`MTR visual framework`](../research/mtr_visual_framework_CN.md) |
| A | `FAILED-BREAKOUT-CLIMAX` | 失败突破与高潮反转候选（目录见 [`失败突破与高潮`](../patterns/05_failed_breakout_climax/README.md)） | 事前可见边界被越过但未被接受，或成熟趋势后出现扩张/高潮；只有叠加位置、反向结构破坏、第二次确认和空间时才升级为反转候选 | 默认等待反向 stop-confirmation；结构回测可作为独立 limit-retest 分支；若原方向重新接受突破，切换为 BOP；详见[`Failed breakout / climax reversal visual framework`](../research/failed_breakout_climax_visual_framework_CN.md) | 先看失败边界、最近磁铁和第一独立支撑/阻力；MM 只作接受后的后续目标 | 影线测试被误叫失败；高潮后直接摸顶/抄底；第一反向无跟随；第三推扩张被误叫楔形衰竭；原方向已 BOP 接受；首障碍太近 |
| A | `DOUBLE-TOP-BOTTOM-BOUNDARY` | 双顶/双底与 MTR、Final Flag 的视觉边界 | 两次有分离的测试首先是位置/形状；父级状态、接受/失败、第二次确认和空间决定归入区间边缘、Final Flag、MTR 或普通回调；详见[`Double top/bottom, MTR and Final Flag comparison`](../research/double_top_bottom_mtr_final_flag_comparison_CN.md) | 先记录 reversal-attempt；反向 stop 或结构回测 limit 需第二次确认；原方向接受则切 BOP | 先看颈线/最近磁铁和第一独立障碍，再看 MM；双顶/双底本身不提供目标 | 只数两个影线；区间中部；把 Final Flag 当 MTR；第一反向无跟随；原方向重新接受；首障碍太近 |
| A | `HEAD-SHOULDERS-ROUNDED` | 头肩顶/底与圆顶/圆底的视觉边界 | 头肩先按复杂双顶/双底或 MTR 候选；圆形先按控制权转移警报；必须检查父级、颈线、接受/失败、第二次确认和空间；详见[`头肩顶/底与圆顶/圆底视觉边界框架`](../research/head_shoulders_rounded_top_bottom_visual_framework_CN.md) | 颈线反向 stop、已确认角色转换后的 limit-retest、强结构收盘或 observation-only 分支分开；目标先看首障碍，后看高度/MM | 先看主要极端/颈线外结构止损和第一独立支撑/阻力；头肩高度不是自动目标；圆弧中部不交易 | 肩部不对称就被否定；三个高低点就叫头肩；圆底中途抄底；区间中部；右肩只是普通回调；原方向 BOP 接受；首障碍太近 |
| A | `TARGET-HIERARCHY-MM-MAGNET` | MM、AB=CD、区间高度、缺口/角色转换与第一障碍的目标层级 | 先冻结结构和测量锚点；第一独立障碍优先，接受后才看 MM；局部腿和父级腿可并存但不得事后移动；详见[`Measured Move、磁铁与目标层级视觉管理框架`](../research/measured_move_magnet_target_hierarchy_CN.md) | 入场前审计首障碍和 R/R；持仓到目标区按动能管理；障碍接受后重建后续目标合同；MM 不单独产生入场 | 近端前高/前低、区间边界、角色转换和通道边界优先于孤立数学投影；目标区可分批止盈 | 跳过首障碍直接看远端 MM；同一价簇重复计数；用后续低点美化首支撑；局部/父级锚点混淆；结构止损先失效仍记目标完成 |
| A | `MULTITIMEFRAME-VISUAL-LAYERS` | Daily/4H/1H 背景与 15m 触发的层级分工 | 高周期决定父级状态、主要位置和结构止损；15m 默认只确认；低周期自成交易、开盘跳过、回测和重订价必须另立合同；详见[`Daily / 4H / 1H / 15m 分层框架`](../research/multitimeframe_visual_review_framework_CN.md) | 同一合同用低周期 stop/确认；独立低周期合同重新冻结入场、止损、首障碍和持有周期；冲突时观望或重建 | 高周期首障碍和结构止损优先；低周期窄止损不能美化日线 R/R；不同周期计数不相加 | 15m K 线倒推 Daily thesis；把 Daily H2 与 15m H2 相加；开盘跳过仍沿用旧价；低周期确认被当成新形态；低周期独立交易结果回写父级 |
| B | `LATE-TREND-ENTRY-FILTER` | 趋势后段的追价、受控回调、高潮风险、突破接受和后段无空间过滤；不是独立 K 线形态 | 先看趋势运行长度、主要磁铁、最后推进、回调/二次入场和第一障碍；详见[`趋势后段入场视觉框架`](../research/late_trend_entry_visual_framework_CN.md) | 等回调/H1-H2/L1-L2；低周期确认；突破接受后建立新合同；或记录 observation-only | 第一障碍、结构止损和交易类型优先；接近 MM 不自动追；后段空间不足直接 no-trade | 把强趋势 K 自动当成入场；用远端 MM 美化 R/R；用低周期窄止损覆盖高周期风险；事后把错过改写成原合同应该追 |
| B | `FINAL-FLAG` | 趋势末端小回调/窄区间 | 持续趋势接近极端后压缩；最后一次突破可能失败并先形成小反转/区间，也可能被接受后延续 | 原方向突破接受走 BOP；反向方向等待失败后的 H1/H2 或 L1/L2-like 二次确认 | 先看旗形边界和最近磁铁，再看 MM；第一次反向不预设整条趋势反转；详细框架见[`Final Flag visual framework`](../research/final_flag_visual_framework_CN.md) | 趋势中段普通旗形；已变成宽区间；原方向强势接受；首障碍太近 |
| B | `OPEN-REVERSAL` | 开盘第一方向失败后的反向机会 | 开盘前背景清楚；第一波到达磁铁/结构位后未被接受；反向形成 H1/L1，最好有 H2/L2 或同等第二次确认 | 反向信号 K 后 stop-confirmation、预先冻结的 limit-retest，或强收盘分支；开盘接受/缺口延续不归入本项 | 先看开盘区间、前日高低点和第一独立障碍，再看 MM；结构止损放在开盘极端/失效位外；详见[`Opening Reversal visual framework`](../research/opening_reversal_visual_framework_CN.md) | 第一方向仍有跟随；只是普通趋势 H/L 回调；区间中部无位置；事件窗口；首障碍太近；原订单被跳空改变 |
| B | `CHANNEL-STATE` | 紧通道、宽通道与趋势状态切换 | 紧通道尊重单向惯性；宽通道承认双方交易与上下边界；重叠、回调深度、边界接受和跟随决定是否切换为区间、BOP 或 MTR | 紧通道回调的 H1/L1、宽通道边缘的 H2/L2、通道外突破接受或失败回到通道；详见[`Channel visual framework`](../research/channel_visual_framework_CN.md) | 紧通道看下一推进/边界；宽通道先看中线/另一边界；MM 只能在障碍被接受后使用 | 两点趋势线被误叫通道；通道中部追单；扩张第三推被误叫衰竭；第一次刺破就反向；首障碍太近 |
| B | `TPB-H1-L1` | 强趋势中的第一次尝试（目录见 [`H1/L1 第一次入场`](../patterns/01_h1_l1_first_entry/README.md)） | A 腿强、B 浅或以时间整理为主，第一次恢复就形成 H1/L1 | 位置、信号 K 和跟随质量都很强时才保留 | 以前一腿或下一道障碍为主；避免追在大腿末端 | A 腿不强、B 很深、H1 太晚、第一障碍太近 |
| B | `H3-L3-COMPLEX` | 第三次尝试/复杂回调 | 前两次恢复未能离开区域，第三次才出现方向尝试 | 只作观察样本；需更严格的结构、空间和跟随确认 | 可记录等距投影，但不能把 MM 当作反转证明 | 计数重置不清、区间中部、三推/楔形解释混入；本轮暂缓 |
| A | `THREE-PUSH-PRESSURE-STATE` | 三推/H3-L3 的衰竭、扩张、区间重复测试与通道延续分流 | 先确认三次尝试属于同一 lineage，再比较推进效率、K 线质量、结构接受和位置；详见[`Three-push / H3-L3 pressure-state framework`](../research/three_push_pressure_state_framework_CN.md) | 衰竭候选等待反向 stop 或二次确认；扩张优先顺势/观望；区间重复测试切换区间逻辑 | 先看第三推极端外结构止损和第一独立障碍，再看 MM；首障碍不足约 1R 记 no-trade | 只数到三就反向；第三推扩张误叫衰竭；区间中部/通道触碰误叫 H3/L3；忽略跳空和首障碍 |
| A | `INSIDE-BAR-TWO-BAR-REVERSAL` | 严格 Inside Bar、二内包/IOI、两根 K 线反转与 H/L setup-confirmation 的边界 | 先冻结母 K 高低点和背景；小实体/下影不自动叫内包；突破接受、反向收回和跟随决定延续或反转；详见[`Inside Bar / two-bar reversal visual framework`](../research/inside_bar_two_bar_reversal_visual_framework_CN.md) | 多头/空头均默认以母 K 或信号 K 外 stop 确认；结构回测 limit 单独研究；中部噪音和首障碍拥挤直接观望 | 首先看母 K/结构失效外止损和第一独立支撑/阻力，再看 MM；严格 Inside Bar 状态未冻结时不得强行交易 | 小实体被误叫内包；两根相反 K 被误叫反转；区间中部突破；把 setup bar 当 entry bar；跳空后沿用理想触发价 |
| A | `TRIANGLE-EXPANDING-RANGE` | 收缩三角形、扩张三角形与区间内区间 | 先确认两侧边界、足够测试和父级状态；三角形是压缩中的双向市场，扩张三角形是波动扩大；详见[`Triangle / expanding triangle visual framework`](../research/triangle_expanding_range_visual_framework_CN.md) | 默认等待突破接受、跟随或失败后的第二次机会；第一下刺破不直接追，原突破和反向合同分开 | 先看三角形边界/父级中线与第一独立支撑阻力，再看高度/MM；结构止损不能压进局部内包 | 两点趋势线被叫三角形；Inside Bar 被放大成三角形；扩张误叫衰竭；区间中部追单；忽略首障碍和跳空重订价 |

### 当前优先顺序

当前核心实现队列是 `TPB-H1-L1`、`TPB-H2-L2`、`ABC-CONT`、`RFB-SECOND`、`FAILED-BREAKOUT-CLIMAX`、`BOP-ABC`、`MTR-ABC` 和 `THREE-PUSH-PRESSURE-STATE`。它们共同覆盖第一次/第二次入场、趋势 ABC、区间边缘、失败突破、突破回踩、主要反转和三推压力状态；三推仍不冻结成自动反转规则。

## 3A. 视觉发现候选目录

这一节是视觉筛选目录，不是胜率表，也不是量化输入。先在完整图表上判断“像不像”，再决定哪些候选值得做精细 R/R 或低周期核验。详细案例只保存在各自的研究文件中，这里只保留入口和视觉问题，避免两个 Repo 或多个文件重复搬运同一套内容。第一轮与第二轮的边界见[`PA Pattern 视觉筛选协议`](../research/visual_pattern_triage_protocol_CN.md)。

统一的逐图复核顺序见 [`docs/visual_pa_review_card_CN.md`](../docs/visual_pa_review_card_CN.md)。

当前各 pattern 家族的覆盖程度和真正缺失的视觉对照见 [`PA Pattern 覆盖审计`](../research/abc_pattern_coverage_audit_CN.md)。这份审计用于防止重复堆叠相似案例，不代表任何胜率或量化结论。

| 视觉候选 ID | 先看什么 | 代表性入口 | 当前状态 |
| --- | --- | --- | --- |
| `VIS-ABC-BULL-H2-REPEATED-SUPPORT` | 强 A 后回调两次；两个低点落在同一支撑簇；第二次反应更清楚 | [`KLAC 2025-05-07–06-03`](../research/klac_h2_case_study_2025-05-07_2025-06-03.md) | `visual_candidate / tradeability borderline`：第一阻力 `79.03`–`79.79` 仅约 `0.8R`–`1.0R`，MM 不能替代近端阻力审计 |
| `VIS-ABC-BULL-H2-LOW-CYCLE-CONDITIONAL` | 深但后段受控 B；支撑簇/EMA20/EMA50 处出现强 H2；15m 先确认再推进；过程路径后来到达第一阻力 | [`TSLA 2025-08-06–08-22`](../research/tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) | `research_positive_conditional / earnings-filter-passed / sector-aligned / low-cycle-trigger-confirmed / first-resistance-reached / process-target-reached / daily-no-trade`：窄低周期止损到入场前第一阻力约 `1.7R`，宽日线止损不足 `1R` |
| `VIS-ABC-BULL-H1-SHALLOW-PULLBACK` | 强 A 后只有一天浅回调；前一根回调 K 不漂亮，但下一根确认很强；触发上方前高近，且存在强趋势磁铁分支 | [`KLAC 2025-10-14–10-24`](../research/klac_h1_case_study_2025-10-14_2025-10-24.md) | `research_positive conditional / strict-first-resistance-no-trade` |
| `VIS-ABC-BULL-H2-LATE-RESISTANCE` | 强 A 后 EMA20 附近两次回测；H1 跟随不足后出现宽幅 H2-like 强阳线，但左侧高点簇就在触发上方 | [`TSLA 2025-12-08–12-12`](../research/tsla_h1_h2_case_study_2025-12-08_2025-12-12.md) | `visual_candidate / first-resistance no-trade` |
| `VIS-ABC-BULL-DEEP-SUPPORT-REVERSAL` | 大周期上涨背景中的深 B；EMA/主要支撑汇聚；低周期出现反转过程 | [`TSLA 2026-05-15–05-22`](../research/tsla_h1_h2_case_study_2026-05-15_2026-05-22.md) | `visual_candidate` |
| `VIS-ABC-BEAR-L2-EARLY-TRIGGER` | 强空头 A 后 B 反弹；低点二次跌破，但第一支撑很近 | [`TSLA 2025-02-20`](../research/tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md) | `visual_candidate / no-trade filter` |
| `VIS-ABC-BEAR-L1-L2-FIRST-OBSTACLE` | 空头推进后快速反弹到 EMA200 附近；C 内部有 L1/L2，但 `03-09` 下破旧 A 低点使 A 锚点待定，第一支撑也很近 | [`TSLA 2026-02-11–03-20`](../research/tsla_bearish_abc_anchor_ambiguity_l1_l2_2026-02-11_2026-03-20.md) | `pattern_like / anchor-ambiguity / valid-no-trade`：L1/L2 触发可重建，但不能把后续 MM 或下跌倒灌成入场授权 |
| `VIS-ABC-BEAR-L2-RANGE-EDGE` | 区间上沿失败后，强阴线 A、弱反弹 B、L1 失败再到 L2；静态空间约 `1.6–1.9R`，但首支撑晚于结构止损失效 | [`TSLA 2024-03-04–03-14`](../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | `visual_candidate / no-event / process-stop-first / first-support-late / range-edge-boundary` |
| `VIS-ABC-BEAR-4H-FIRST-SUPPORT` | 上涨后的空头 A；反弹 B 后 L1/L2-like 下破，但触发下方立即遇左侧支撑 | [`MAR 2026-06-18–06-25`](../research/mar_4h_l1_case_study_2026-06-18_2026-06-25.md) | `visual_candidate / valid no-trade / 4H count pending` |
| `VIS-ABC-BEAR-L2-RESISTANCE-RETEST` | 强 A 后反弹回前支撑转阻力；第一次失败后再次测试，L2 信号更清楚，第一支撑仍有空间 | [`TSLA 2024-07-30–08-01`](../research/tsla_bearish_abc_case_2024-07-11_2024-08-05.md) | `event-driven positive / ~1.5R research benchmark` |
| `VIS-ABC-BEAR-GAP-RETEST` | 原始破位被跳空改变；不要沿用旧 stop，重新等待反弹回测 | [`TSLA 2025-03-04 284 回测`](../research/tsla_abc_playbook_2025-03-04_284_retest.md) | `audited branch` |
| `VIS-L3-CONTINUATION-CLIMAX` | 第三次尝试没有减弱，反而扩张；L3 不等于楔形反转 | [`TSLA 2025-03-07/10`](../research/tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md) | `counterexample` |
| `VIS-H3-L3-SECOND-PUSH-EXPANSION` | 第一推后第二推明显扩张；第三推在支撑处减速，但不能自动视为楔形反转 | [`ANET 2024-05-16–06-10`](../research/anet_h3_l3_case_study_2024-05-16_2024-06-10.md) | `independent boundary / C-class continuation-or-climax risk` |
| `VIS-H3-L3-RANGE-TRANSITION-BOUNDARY` | 旧三腿标签对应下沿二次测试、区间重叠和后段向上扩张；没有清楚的第三次衰竭推进 | [`ASML 2025-05-19–06-13`](../research/asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md) | `not_h3_l3 / range-transition / visual boundary` |
| `VIS-H3-BEAR-FLAG-RESUMPTION` | 空头背景熊旗中的三次向上测试；第三推在主要阻力下失败，随后出现空头接受；SOXX 同步走弱，15m 无跳空触发；事后到达第一、第二支撑 | [`KLAC 2025-03-12–03-28`](../research/klac_h3_bear_flag_case_2025-03-12_2025-03-28.md) | `pattern_like / research_positive_candidate / process-target-reached / first-and-second-support-reached / earnings-filter-passed / sector-aligned / low-cycle-confirmed` |
| `VIS-ABC-BEAR-L2-EVENT-BOUNDARY` | 跳空强 A 后两次较低反弹；L2 方向清楚但第一支撑太近 | [`ANET 2024-02-12–02-21`](../research/anet_bearish_l2_event_boundary_2024-02-12_2024-02-21.md) | `pattern_like / valid_no_trade / event-context-pending` |
| `VIS-ABC-BEAR-L1-ORDINARY-A` | 普通 A 后反向 B/近似双顶，L1 方向清楚但第一支撑近 | [`PLTR 2025-01-06–01-08`](../research/pltr_bearish_abc_l1_ordinary_a_boundary_2024-12-24_2025-01-08.md) | `pattern_like / valid_no_trade / ordinary_A_boundary` |
| `VIS-L3-RETEST-CONTINUATION` | L2 跟随后先有新反弹分隔，再出现低周期回测和 L3 触发 | [`TSLA 2026-03-25–03-30`](../research/tsla_l3_case_study_2026-03-25_2026-03-30.md) | `provisional` |
| `VIS-H3-THREE-PUSH-SUPPORT-REACTION` | 三个低点逐步下移但推进间距收窄；第三次测试落在支撑候选，之后出现反弹但未确认主要反转 | [`TSLA 2026-05-19–06-26`](../research/h3_l3_research_gate_CN.md) | `pattern_like / B-class short-reaction or no-trade` |
| `VIS-RESISTANCE-MULTI-PUSH-NO-TRADE` | 多次测试主要阻力；没有反向触发不提前做空；突破接受后另开分支 | [`TSLA 2025-09-04–09-12`](../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | `no-trade boundary` |
| `VIS-MTR-TSLA-RANGE-TOP-L2` | 局部区间上沿失败、强空头 A、弱 B、L1 失败后 L2；静态首支撑有空间，但结构止损先于首支撑失效 | [`TSLA 2024-03-04–03-14`](../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | `MTR-candidate / range-edge-overlap / process-stop-first` |
| `VIS-MTR-NFLX-TOP-BOUNDARY` | 强多头后高位多次测试、空头反应和低周期触发存在，但首支撑拥挤且后续重新突破顶部 | [`NFLX 2024-08-05–09-26`](../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | `MTR-like / H3-like / valid_no_trade / later-invalidated` |
| `VIS-MTR-TSLA-BOP-INVALIDATION` | 主要阻力下的双高/多次测试先构成反转尝试；强突破收盘接受后，MTR thesis 失效并切换为 BOP | [`TSLA 2025-09-08–09-12`](../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | `reversal-attempt / failed-MTR-thesis / BOP-acceptance` |
| `VIS-FAILED-BREAKOUT-CLIMAX-BOUNDARIES` | 失败突破、高潮后小反转/区间、强 A 首障碍边界，以及被接受突破否定的反转假设 | [`失败突破与高潮反转框架`](../research/failed_breakout_climax_visual_framework_CN.md) | `framework / partial / provisional / no-clean-positive-yet` |
| `VIS-DOUBLE-TOP-BOTTOM-MTR-FINAL-FLAG` | 双顶/双底作为位置形状，分别与区间边缘、Final Flag、MTR、普通回调和 BOP 对照 | [`双顶/双底、MTR 与 Final Flag 对照`](../research/double_top_bottom_mtr_final_flag_comparison_CN.md) | `comparison / provisional / no-clean-positive-yet` |
| `VIS-HEAD-SHOULDERS-ROUNDED-BOUNDARIES` | 头肩顶/底、圆顶/圆底、复杂双顶/双底、区间过渡、普通旗形和 BOP 否定的视觉边界 | [`头肩顶/底与圆顶/圆底视觉边界`](../research/head_shoulders_rounded_top_bottom_visual_framework_CN.md) | `framework / partial / provisional / no-clean-positive-yet` |
| `VIS-TARGET-HIERARCHY-MM-MAGNETS` | 近端主要障碍、角色转换、缺口/通道磁铁与局部/父级 MM 的先后关系；包含首障碍先到、障碍接受后切换和分批止盈路径 | [`Measured Move、磁铁与目标层级`](../research/measured_move_magnet_target_hierarchy_CN.md) | `framework / cross-pattern / provisional / no-fixed-threshold` |
| `VIS-MULTITIMEFRAME-ORDER-LAYERS` | Daily/4H/1H 父级背景、15m 确认、低周期独立交易、开盘跳过与缺口重订的分层对照 | [`Daily / 4H / 1H / 15m 分层框架`](../research/multitimeframe_visual_review_framework_CN.md) | `framework / partial / provisional / contract-separation-required` |
| `VIS-LATE-TREND-ENTRY-BOUNDARIES` | 受控回调、高潮、突破接受新合同与后段无空间的对照；跨 H/L、ABC、BOP 和 MTR 使用 | [`趋势后段入场视觉框架`](../research/late_trend_entry_visual_framework_CN.md) | `framework / cross-pattern / provisional / no-FOMO-rule` |
| `VIS-MTR-BULL-TRANSITION-BOUNDARIES` | ASML 双底样区间过渡、LOW 急跌后多头恢复；两者说明低位反应不等于已确认多头 MTR | [`MTR visual framework`](../research/mtr_visual_framework_CN.md) | `bullish-reversal-attempt / range-transition / valid_no_trade` |
| `VIS-ABC-BULL-H2-RESISTANCE-BOUNDARY` | 支撑反应和 H2-like 尝试都存在，但左侧高点就在触发上方 | [`ANET 2023-11-15–11-22`](../research/anet_bullish_h2_visual_boundary_2023-11-15_2023-11-22.md) | `valid_no_trade / pattern_like` |
| `VIS-ABC-BEAR-GAP-FIRST-SUPPORT-BOUNDARY` | 强 A、反向 B、L1/L2-like 下破；低周期 L1 可成交但首支撑先到，L2 原触发被开盘跳过 | [`COIN 2024-01-02–01-12`](../research/coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md) | `valid_no_trade / L1-low-cycle-confirmed / first-support-reached-before-stop / L2-opening-skip / event-context-pending` |
| `VIS-H3-COIN-BEAR-FLAG-EXPANSION` | 空头 A 后三次上探候选；第三次回到阻力但范围扩张；后续低周期 L1 先到首支撑 | [`COIN 2024-01-04–01-09`](../research/coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md#h3-like-熊旗顶部补审-2024-01-04–2024-01-09) | `provisional H3-like / C-class boundary / first-support-reached / L2-opening-skip / valid_no_trade` |
| `VIS-H3-NFLX-THREE-PUSH-TOP` | 强多头 A 后高位多次测试；空头反应和低周期触发存在，但首支撑拥挤、后来顶部被越过 | [`NFLX 2024-08-05–09-26`](../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | `provisional three-push-top / L1-like-low-cycle-confirmed / first-support-reached / later-structure-invalidated / valid_no_trade` |
| `VIS-THREE-PUSH-PRESSURE-STATE` | 把 H3/L3 案例按第三推压力状态分成衰竭、扩张/高潮、区间重复测试和通道延续 | [`三推/H3-L3 压力状态框架`](../research/three_push_pressure_state_framework_CN.md) | `framework / provisional / no-clean-positive-yet` |
| `VIS-INSIDE-BAR-TWO-BAR-BOUNDARIES` | 严格内包、两根反转、H/L setup-confirmation、普通停顿和跳空非内包的对照 | [`Inside Bar / 两根 K 线反转`](../research/inside_bar_two_bar_reversal_visual_framework_CN.md) | `framework / partial / provisional / strict-ohlc-pending` |
| `VIS-TRIANGLE-EXPANDING-RANGE-BOUNDARIES` | 收缩三角形、扩张三角形、区间内区间、旗形与突破接受/失败的对照 | [`三角形 / 扩张三角形视觉框架`](../research/triangle_expanding_range_visual_framework_CN.md) | `framework / partial / provisional / no-clean-positive-yet` |
| `VIS-H3-XOM-BEAR-FLAG-EXPANSION` | 空头 A 后三次上探；第三次抬高并扩张，随后出现 L1-like 反应但触发日跳空 | [`XOM 2024-07-18–08-02`](../research/xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md) | `provisional H3-like / C-class expansion boundary / valid_no_trade / event-context-pending` |
| `VIS-H3-UBER-COUNT-SPACE-BOUNDARY` | 强空头 A 后三次上探候选；第三次之后出现更高、更宽的扩张；后续 L2-like 低周期未从开盘跳过原触发但首支撑太近 | [`UBER 2024-07-17–07-26`](../research/uber_bearish_h3_l2_first_support_boundary_2024-07-17_2024-07-26.md) | `pattern_like / provisional-H3-like / count-ambiguous / C-class-expansion-boundary / earnings-filter-passed / valid_no_trade` |
| `VIS-H3-SCREEN-2025-08_11` | AVGO/MSFT/PANW/MRVL/DELL/LULU/TXN/TGT/DIS 的独立筛选：强趋势重复回调、事件恢复、宽 B 或区间过渡外形；没有冻结为同一 lineage 的正向 H3/L3 | [`H3/L3 候选筛选日志`](../research/h3_l3_candidate_screen_2025-08_2025-11_CN.md) | `visual-screen / boundary-log / event-gap-boundary / range-transition / not-quantitative / no-new-positive` |
| `VIS-H3-NOW-COUNT-FOLLOW-THROUGH-BOUNDARY` | 同一高位区域的多次测试，但 `10-10` 扩张、重叠和计数歧义削弱 H3；`10-17` 低周期只触碰触发位而没有空头跟随，且 IGV/QQQ 与 NOW 不同向 | [`NOW 2025-09-19–10-21`](../research/h3_l3_candidate_screen_2025-08_2025-11_CN.md#9-now第三次高位测试候选但计数板块和低周期跟随不足) | `pattern_like / provisional-H3-like / count-ambiguous / low-cycle-touch-no-follow-through / sector-not-aligned / valid_no_trade` |
| `VIS-H3-DELL-GAP-REPRICE-BOUNDARY` | 高位测试接近 H3；`11-03` 空头反应后，`11-04` 开盘跳过原 sell-stop，若按开盘重订则首支撑拥挤、结构止损较远 | [`DELL 2025-10-01–11-20`](../research/h3_l3_candidate_screen_2025-08_2025-11_CN.md#10-dell高位测试像-h3但低开跳过原触发且重订后空间不足) | `pattern_like / provisional-H3-like / count-ambiguous / opening-skip / gap-reprice-geometry-boundary / valid_no_trade` |
| `VIS-ABC-BULL-H1-GAP-PULLBACK` | 顺畅上涨背景中的深 gap pullback；次日强收回形成 H1-like，但信号 K 和首阻力不理想 | [`WMT 2024-06-24–06-27`](../research/wmt_bullish_h1_gap_pullback_boundary_2024-06-24_2024-06-27.md) | `pattern_like / valid_no_trade / signal-quality-pending / first-obstacle-boundary / event-context-pending` |
| `VIS-ABC-BULL-LARGECAP-SCREEN-2024` | 多个大盘股窗口出现强 A、B、H1/H2-like 再推，但首障碍或冲击背景阻止升级 | [`AAPL/MSFT/GOOGL/META 视觉筛选`](../research/largecap_visual_screen_2024_CN.md) | `visual_screen / no_clean_positive_yet` |
| `VIS-ABC-BULL-SNOW-DEEP-B-H2` | 上涨背景中的深但后段受控 B；支撑/EMA20 处出现 H2-like 反应，但触发上方左侧高点过近 | [`SNOW 2026-08-14–08-21`](../research/snow_bullish_h2_first_obstacle_boundary_2026-08-14_2026-08-21.md) | `pattern_like / bullish-H2-like / deep-but-late-controlled-B / first-obstacle-crowded / low-cycle-branch-reviewed / valid_no_trade / event-unknown` |
| `VIS-ABC-BEAR-CLIMAX-A-L1-BOUNDARY` | 上涨末端剧烈反转形成强 A；浅但偏弱 B 后出现 L1-like 下破；触发下方已有支撑簇 | [`COST 2024-07-11–07-18`](../research/cost_bearish_abc_climax_boundary_2024-07-11_2024-07-18.md) | `pattern_like / valid_no_trade / strong-A-climax-boundary / event-context-pending` |
| `VIS-ABC-BULL-DEEP-VOLATILE-B` | 上涨背景中出现方向性恢复；B 含大范围反向冲击；H1/H2-like 形态和低周期跟随存在，但信号 K 与首障碍不合格 | [`LLY 2024-06-06–2024-06-13`](../research/lly_bullish_abc_h1_h2_first_obstacle_boundary_2024-06-06_2024-06-13.md) | `pattern_like / valid_no_trade / deep-volatile-B / signal-quality-pending / first-obstacle-boundary` |
| `VIS-ABC-BULL-H2-GAP-TRIGGER` | 方向性 A、浅受控 B、重复支撑和优质信号 K；触发日跳空越过原 buy stop，首阻力又贴近 | [`BKNG 2024-06-12–2024-06-18`](../research/bkng_bullish_h2_gap_trigger_boundary_2024-06-12_2024-06-18.md) | `pattern_like / morphology-positive / valid_no_trade-on-original-order / gap-trigger-reprice / first-obstacle-boundary` |
| `VIS-RANGE-EDGE-NOT-ABC-RBLX` | 局部 A/B/C 外形，但 B 回到 A 起点和父级区间下沿；C 盘中冲高后收盘失败，后续恢复不能倒灌 | [`RBLX 2024-03-18–04-05`](../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md) | `pattern_like / range-edge-reaction / not-ABC-continuation / signal-quality-failure / valid_no_trade` |
| `VIS-ABC-BULL-H1-GAP-GOOGL` | 强 A、浅 B 后跳空越过原 buy stop；方向正确但成交重订后首障碍拥挤，limit-retest 未成交 | [`GOOGL 2024-03-04–03-22`](../research/googl_bullish_h1_gap_trigger_boundary_2024-03-04_2024-03-22.md) | `pattern_like / bullish-H1-like / gap-trigger-reprice / first-obstacle-boundary / valid_no_trade` |
| `VIS-ABC-BULL-H1-DEEP-B-EMA200-HD` | 深 B 回到左侧支撑簇；第一次多头尝试可画成 H1-like，但信号 K 一般，EMA200 贴近触发，XLY/SPY 同期转弱 | [`HD 2024-07-01–07-31`](../research/hd_bullish_h1_ema200_sector_boundary_2024-07-01_2024-07-31.md) | `pattern_like / bullish-H1-like / deep-B / signal-quality-boundary / EMA200-first-obstacle / sector-filter-warning / valid_no_trade` |
| `VIS-ABC-BEAR-L1-GAP-QCOM` | 强空头 A 与 SOXX 同向；B 反弹后 L1 下破，但开盘跳过理想触发，实际成交使第一支撑空间不足；limit-retest 未成交 | [`QCOM 2024-07-17–07-30`](../research/qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md) | `pattern_like / strong-A-gap-impulse / L1-gap-trigger-reprice / sector-aligned / valid_no_trade` |
| `VIS-ABC-BEAR-L2-FIRST-SUPPORT-QCOM` | L1 后反弹再下破，L2-like 触发可在低周期重建；第一支撑约 `0.87R`，且进入财报前 3 天 | [`QCOM 2024-07-17–07-30`](../research/qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md) | `pattern_like / L2-first-support-boundary / earnings-window-invalid / valid_no_trade` |
| `VIS-ABC-BULL-H1-EVENT-DRIVEN-A` | 财报后跳空产生强局部 A；浅 B 后出现小实体/长下影 H1-like，低周期从触发下方上穿 | [`AAPL 2024-05-03–05-09`](../research/aapl_bullish_h1_event_driven_a_2024-05-03_2024-05-09.md) | `research_positive_conditional / event-driven-A / earnings-filter-passed / low-cycle-confirmed / first-obstacle-borderline` |
| `VIS-ABC-BULL-ORDINARY-A-SCREEN` | 多个图上未见明显事件跳空启动的人工窗口出现普通 A、B 和 H1/H2-like 恢复，但触发附近前高拥挤 | [`MSFT / AMZN / META / NFLX / CAT 2024-05–07`](../research/ordinary_a_visual_screen_2024-05_2024-07_CN.md) | `pattern_like / ordinary-A / first-obstacle-crowded / valid_no_trade / event_check_pending`；用于补强普通 A 的空间过滤，不是量化筛选或胜率样本 |
| `VIS-ABC-BULL-META-NESTED-H1-H2` | 强 A 后多层回踩和 H1/H2-like 恢复；计数存在嵌套尺度，触发上方主要高点太近 | [`META 2024-09-11–10-11`](../research/meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md) | `pattern_like / bullish-H1-H2-like / nested-count-unclear / first-obstacle-crowded / observation-only` |
| `VIS-ABC-BULL-TRANSITION-LOW` | 急跌后的方向性 A、回调和 H1/H2-like 恢复；父级过渡，信号 K/计数边界，前高簇贴近触发 | [`LOW 2024-06-11–06-24`](../research/low_bullish_h1_h2_first_obstacle_boundary_2024-06-11_2024-06-24.md) | `pattern_like / bullish-ABC-candidate / H1-H2-like / first-obstacle-crowded / valid_no_trade / event_context_pending` |
| `VIS-ABC-BULL-NVDA-H1-VISUAL` | 上涨父级中的强方向腿、短但偏深 B、随后 H1-like 恢复；形态正向但原 stop 被跳空越过 | [`NVDA 2025-06-23–07-03`](../research/nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md) | `pattern_like / morphology-positive / original-stop-invalidated-by-gap / reprice-pending` |
| `VIS-ABC-BULL-NVDA-H2-60M-CONDITIONAL` | 强 A 后深但后段受控 B；H1 失败后支撑处 H2；原触发未被开盘跳过，低周期确认分支有空间但日线宽止损偏拥挤 | [`NVDA 2024-09-11–09-25`](../research/nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md) | `research_positive_conditional / bullish-H2 / low-cycle-trigger-confirmed / daily-space-borderline / event-check-pending` |
| `VIS-ABC-BEAR-MSFT-L1-L2-VISUAL` | 高位转弱后的空头 A、反弹 B、再下行 L1/L2-like；原 sell-stop 被跳空越过 | [`MSFT 2025-10-28–11-20`](../research/msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md) | `pattern_like / bearish-ABC-candidate / L1-L2-like / gap-trigger-boundary / pending` |
| `VIS-ABC-BEAR-CRM-RESET-L1-VISUAL` | 空头父级、反弹 B、第一次 L1 后反弹越过前 B 高点；后续更像计数重置后的新 L1；15m 触发可重建；首支撑仍偏近；IGV/QQQ/SPY 同步走弱 | [`CRM 2025-03-10–03-28`](../research/crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md) | `pattern_like / sector-aligned / L1-first-support-crowded / reset-L1-conditional-space / non-gap-trigger / pending` |
| `VIS-ABC-BEAR-QCOM-RANGE-B-BOUNDARY` | 强 A 后 B 变宽、重叠多、反复穿越均线；后续向下运动应按区间逻辑而非自动 L2 | [`QCOM 2025-02-21–03-28`](../research/qcom_bearish_abc_range_b_boundary_2025-02-21_2025-03-28.md) | `boundary / range-transition / not-open-trend-ABC / observation-only` |
| `VIS-ABC-BEAR-NKE-L1-GAP-RETEST` | 强 A 后 B 仍低于 A 起点；L1-like 恢复，但小缺口使原 sell-stop 未按原价成交；`10-28 13:15` 旧低点回测可另列 sell-limit/retest，`10-29` 低开不自动数 L2；回测分支 `10-30` 进入首支撑 | [`NKE 2025-10-03–10-29`](../research/nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md) | `pattern_like / strong-A / controlled-B-conditional / minor-gap-trigger / original-stop-not-filled / limit-retest-process-target-reached / first-obstacle-borderline / sector-mixed / event-context / pending` |
| `VIS-ABC-BEAR-TSM-L1-GAP-REPRICE` | 强 A、受控 B、L1-like 恢复；原 stop 被小缺口越过，旧低点 limit 未回测；接受缺口后的重订仍有第一支撑空间，且重订路径后来到达首支撑 | [`TSM 2025-02-14–03-28`](../research/tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) | `pattern_like / research_positive_conditional / strong-A / controlled-B / gap-reprice-space-positive / process-target-reached / original-stop-not-filled / sector-aligned / earnings-filter-passed / pending` |
| `VIS-ABC-BEAR-AMZN-L1-NO-GAP-BOUNDARY` | 普通/方向性 A 后深 B；`10-15` 无缺口、低周期顺序清楚的 L1-like 下破，但第一支撑只有边界空间且 XLY 不弱 | [`AMZN 2024-09-23–10-15`](../research/amzn_bearish_abc_l1_no_gap_first_support_boundary_2024-09-23_2024-10-15.md) | `pattern_like / ordinary-or-directional-A / deep-B / no-gap-trigger / first-obstacle-borderline / sector-mixed / earnings-filter-passed / pending` |
| `VIS-ABC-BEAR-NFLX-L1-NO-GAP-SPACE` | 方向性强 A、深但后段受控 B；无开盘缺口；盘中刺破与收盘确认均可重建，首支撑有条件空间；事后首支撑到达 | [`NFLX 2025-02-14–03-28`](../research/nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md) | `pattern_like / research_positive_conditional / strong-looking-A / deep-but-controlled-B / no-gap-trigger / first-obstacle-space-positive / process-target-reached / sector-aligned / earnings-filter-passed / pending` |
| `VIS-ABC-BULL-CRWD-H2-DEEP-B` | 强 A 后深 B，后段在 `68.17` 附近稳定；`09-23` 首次尝试/失败突破有计数歧义，`10-02` H2-like，`10-03` 15m 可重建买入；首阻力有但不宽，财报过滤通过，`2024-07-19` incident 单列 | [`CRWD 2024-09-11–10-11`](../research/crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md) | `pattern_like / research_positive_conditional / low-cycle-trigger-confirmed / first-obstacle-space-positive-but-not-wide / earnings-filter-passed / incident-context-pending` |
| `VIS-ABC-BULL-AMZN-H2-SHALLOW-B` | 强上涨背景中的嵌套 A；`12-09` 第一次高位尝试未被持续接受，`12-10` 浅 B，`12-11` H2-like；15m 可重建 buy-stop，但 60m 接受和首段空间仍混合 | [`AMZN 2024-12-09–12-11`](../research/amzn_bullish_h2_shallow_b_boundary_2024-12-09_2024-12-11.md) | `pattern_like / strong-looking-A / controlled-B / bullish-H2-like / low-cycle-trigger-confirmed / follow-through-mixed / event-context-pending` |
| `VIS-ABC-BULL-COST-H1-FIRST-OBSTACLE` | 强-looking A 后两日 B；`05-15` 强多头信号 K / H1-like，15m 可重建触发；但 `05-13/05-10` 高点簇贴着触发，`05-16` 开盘越过原价 | [`COST 2024-05-13–05-16`](../research/cost_bullish_h1_first_obstacle_boundary_2024-05-13_2024-05-16.md) | `pattern_like / strong-looking-A / controlled-after-first-pressure-B / bullish-H1-like / low-cycle-trigger-confirmed / first-obstacle-crowded / opening-skip / sector-mixed / valid_no_trade / event-context-pending` |
| `VIS-ABC-BULL-JNJ-H1-OPENING-SKIP` | `08-01–15` strong-looking A、`08-18–28` controlled B、`08-29` bullish H1-like；XLV 顺势，但 15m 只触碰触发、`09-02` 小缺口越过原价；B 内高点 `176.74` 形成首阻力 | [`JNJ 2025-08-01–09-02`](../research/jnj_bullish_h1_opening_skip_first_obstacle_boundary_2025-08-01_2025-09-02.md) | `pattern_like / strong-looking-A / controlled-B / bullish-H1-like / sector-aligned / opening-skip / first-obstacle-crowded / valid_no_trade / event-context-pending` |
| `VIS-ABC-BULL-GROWTH-UNIVERSE-2024Q3` | SHOP/PLTR/DDOG/UBER 的完整日线视觉筛选：多头 ABC/H1-H2-like 外形与事件跳空、嵌套计数、缺口状态和首障碍边界并列 | [`2024 Q3 成长股视觉筛选`](../research/visual_screen_growth_universe_2024q3_CN.md) | `visual-screen / boundary-log / no-new-positive / not-quantitative / no-low-cycle-audit` |
| `VIS-ABC-MACRO-UNIVERSE-2025H2` | JPM/GS/BAC/SPY 等完整日线窗口的人工视觉筛选；SPY 已单独完成一段低周期与首阻力复核，同时保留 XOM/CVX/MCD/KO/PG/WMT/LLY/UNH 的区间、事件、过渡和 lineage 边界 | [`2025 H2 宏观与跨行业视觉筛选`](../research/visual_screen_macro_universe_2025h2_CN.md) | `visual-screen / pattern-like-first / SPY-first-resistance-boundary / JPM-next / event-boundary / range-boundary / not-quantitative` |
| `VIS-ABC-ORDINARY-2025H1-FOLLOWUP` | MSFT/AMZN/ORCL/BKNG 与 AVGO/LRCX/AMAT/CSCO/TXN/IBM 的完整日线复筛；强 A、状态切换、缺口污染和过渡边界并列 | [`2025 H1 普通 ABC 视觉复筛`](../research/visual_screen_ordinary_abc_2025h1_followup_CN.md) | `visual-screen / pattern-like-first / event-state-boundary / nested-lineage-boundary / no-new-conditional-positive / not-quantitative / no-low-cycle-audit` |
| `VIS-ABC-BULL-VRT-DEEP-B` | `04-14` 缺口冲击型强 A；`04-15/16` 深且前强后弱 B；`04-17` 低周期第一次多头恢复，视觉上 H1-like，但原 stop 被开盘跳过，重新触发后第一阻力拥挤 | [`VRT 2026-04-14–04-20`](../research/vrt_bullish_abc_h1_deep_b_first_obstacle_boundary_2026-04-14_2026-04-20.md) | `pattern_like / bullish-H1-like / gap-impulse-A / deep-volatile-B / original-stop-opening-skip / re-arm-branch / first-obstacle-boundary / valid_no_trade / event-context-pending` |
| `VIS-ABC-BULL-V-H2-NO-GAP` | `05-06/10` 普通方向性 A；`05-13` 冲高失败后 `05-14` 深回调并在低点稳定；`05-15` H2-like，低周期触发真实越过，但第一阻力簇不足 | [`V 2024-05-06–05-17`](../research/v_bullish_abc_h2_no_gap_first_obstacle_boundary_2024-05-06_2024-05-17.md) | `pattern_like / ordinary-or-directional-A / deep-but-stabilizing-B / bullish-H2-like / low-cycle-trigger-confirmed / daily-opening-skip / first-obstacle-boundary / valid_no_trade / earnings-context-pending` |
| `VIS-ABC-BULL-TXN-H1-FIRST-OBSTACLE` | `05-01–22` 普通方向性 A；`05-23–06-04` B；`06-05/06` H1-like 恢复，15m/60m 触发顺序清楚；但 `05-20/21` 高点簇在触发上方很近，首障碍不足 `1R` | [`TXN 2024-05-01–06-06`](../research/ordinary_a_visual_screen_2024-05_2024-07_CN.md) | `pattern_like / ordinary-A / bullish-H1-like / low-cycle-trigger-confirmed / first-obstacle-crowded / valid_no_trade / event_check_pending` |
| `VIS-ABC-BULL-MA-DEEP-B-TRANSITION` | `06-17–24` 可画 A；`06-25–07-01` 深且前强后弱 B；`07-02` 强恢复像 H1-like，但 B 跌破早期 A 起点附近；`07-03` 开盘越过原触发，lineage 与订单分支仍待核对 | [`MA 2024-06-17–07-03`](../research/ordinary_a_visual_screen_2024-05_2024-07_CN.md) | `pattern_like / deep-B / A-origin-and-lineage-pending / opening-skip / gap-reprice-boundary / event_check_pending` |
| `VIS-ABC-BEAR-DIS-L1-OPENING-SKIP` | `07-16/25` 局部方向性空头 A；`07-29/31` 深且反向压力强的 B；`08-01` L1-like，但 `08-02` 开盘越过原 sell-stop，首支撑 `87.18–88.13` 过近，且进入 `08-07` 财报前 3 天 | [`DIS 2024-07-16–08-02`](../research/dis_bearish_abc_l1_opening_skip_first_support_2024-07-16_2024-08-02.md) | `pattern_like / parent-range-transition / strong-looking-gap-A / deep-counterpressure-B / opening-skip / first-support-boundary / earnings-window-invalid / valid_no_trade` |
| `VIS-ABC-BEAR-LRCX-L1-GAP-REPRICE` | `07-10/19` 强方向、缺口强化的空头 A；`07-22/23` 短且后段转弱的 B；`07-24` L1-like 但开盘低于原触发，回测 limit 未成交；SOXX/SMH 同向，首支撑边界 | [`LRCX 2024-07-10–07-25`](../research/lrcx_bearish_abc_l1_gap_first_support_2024-07-10_2024-07-25.md) | `pattern_like / strong-A-gap-impulse / controlled-B-conditional / L1-gap-trigger-reprice / sector-aligned / first-support-borderline / earnings-filter-passed / valid_no_trade` |
| `VIS-ABC-BULL-JNJ-H1-FIRST-OBSTACLE` | `09-18` 低点后的方向性恢复；`10-07` 深探后长下影收回，视觉上 H1-like；`10-08` 低周期未跳过原触发，但 `10-03` 高点贴近 | [`JNJ 2025-09-18–10-08`](../research/jnj_bullish_h1_first_obstacle_2025-09-18_2025-10-08.md) | `pattern_like / ordinary-to-directional-A / deep-but-position-controlled-B / bullish-H1-like / low-cycle-triggered / first-obstacle-blocked / event-context-pending / valid_no_trade` |
| `VIS-ABC-BULL-JPM-H1-FOLLOW-THROUGH-FAILURE` | `08-22/29` 上涨；`09-02/03` B；`09-04` 强恢复并有 15m 触发；`09-05` 先冲高后重挫；H1 首阻力与突破分支分开 | [`JPM 2025-08-22–09-05`](../research/jpm_bullish_h1_first_obstacle_failure_2025-08-22_2025-09-05.md) | `pattern_like / bullish-H1-like / deep-but-controlled-B / sector-aligned-at-entry / first-obstacle-blocked / breakout-branch-separate / follow-through-failure / valid_no_trade / event-context-pending` |
| `VIS-ABC-BULL-NVDA-H1-TRIGGER-BRANCH` | `04-21/05-02` 强方向 A；`05-05/06` 偏深但后段稳定 B；`05-07` H1-like 恢复；早期触发上方首阻力拥挤，晚一日触发被开盘跳过 | [`NVDA 2025-04-21–05-08`](../research/nvda_bullish_h1_trigger_branch_first_obstacle_2025-04-21_2025-05-08.md) | `pattern_like / strong-looking-A / deep-but-late-controlled-B / bullish-H1-like / sector-aligned / trigger-branch-ambiguous / first-obstacle-blocked / valid_no_trade / event-context-pending` |
| `VIS-ABC-BULL-COST-H2-DEEP-B-BOUNDARY` | `04-21` 低点后的普通方向 A；`05-05/14` 深 B 后 `05-15` 先探后收的 H2-like；15m 触发清楚但 `05-02` 高点压住首段空间 | [`COST 2025-04-21–05-16`](../research/cost_bullish_abc_h2_visual_boundary_2025-04-21_2025-05-16.md) | `pattern_like / ordinary-directional-A / deep-B / bullish-H1-H2-like / low-cycle-triggered / first-obstacle-borderline / sector-aligned / valid_no_trade / event-context-pending` |
| `VIS-ABC-BEAR-MCD-L1-FIRST-SUPPORT` | `05-20` 后方向性空头 A；`06-23/24` 短而受控 B；`06-25` 无开盘跳过、15m 可重建 L1；但 `06-20` 主要低点是触发后的第一支撑，XLY/SPY 许可混合 | [`MCD 2025-05-20–06-27`](../research/mcd_bearish_abc_l1_counter_market_first_support_2025-05-19_2025-06-27.md) | `pattern_like / strong-looking-directional-A / controlled-B / bearish-L1-like / no-gap-trigger / first-support-blocked / sector-mixed / market-not-aligned / valid_no_trade / event-context-pending` |
| `VIS-ABC-BULL-SPY-INDEX-FIRST-RESISTANCE` | `07-07/10` 普通方向性 A；`07-11/16` 深但后段稳定 B；`07-17` 多头恢复，H1/H2 计数保留歧义；指数与 QQQ 同步 | [`SPY 2025-07-07–07-18`](../research/spy_bullish_h1_h2_index_control_first_resistance_2025-07-07_2025-07-18.md) | `pattern_like / index-control / bullish-H1-H2-like / count-pending / low-cycle-trigger-confirmed / first-resistance-blocked / valid_no_trade / event-context-pending` |
| `VIS-ABC-BULL-PM-H1-H2-VISUAL` | `01-05/16` 局部方向性 A；`01-20/21` 两日回压仍留在母腿内；`01-22/23` 多头恢复；第一合同开盘跳过，第二合同可重建 | [`PM 2026-01-05–01-23`](../research/pm_bullish_abc_h1_visual_screen_2026-01-05_2026-01-23.md) | `pattern_like / ordinary-open-trend-candidate / bullish-H1-H2-like / low-cycle-branch-audited / first-obstacle-blocked / valid_no_trade / event-context-pending` |
| `VIS-ABC-BEAR-ADBE-L1-VISUAL` | 父级从高位过渡转空；`01-12/20` 局部方向性空头 A；`01-21/26` 反弹仍低于 A 起点；`01-27` 跌破前低；15m/60m 触发顺序可重建，第一支撑暂有空间 | [`ADBE 2026-01-12–01-27`](../research/adbe_bearish_abc_l1_visual_screen_2026-01-12_2026-01-27.md) | `research_positive_conditional / transition-to-open-bear / strong-looking-A / controlled-B / bearish-L1-like / no-gap-trigger / sector-aligned / market-countertrend / first-support-space-positive / earnings-filter-passed` |
| `VIS-ABC-BEAR-CME-L1-FIRST-SUPPORT` | `05-20/06-02` 方向性空头 A；`06-03/16` 较深、后段才稳定的 B；`06-17` L1-like 外形；父级带区间/过渡色彩，首支撑贴近 | [`CME 2026-05-20–06-17`](../research/cme_bearish_abc_l1_visual_screen_2026-05-20_2026-06-17.md) | `pattern_like / boundary / transition-to-open-bear / deep-B / opening-skip-boundary / first-support-crowded / no-low-cycle-audit / observation-only` |
| `VIS-ABC-BULL-MDT-H2-TRANSITION` | `05-23/06-16` 普通到有方向性的多头 A；`06-17/25` 深但后段稳定 B；`06-27/07-02` 恢复并越过前高，H2-like 候选；父级仍有过渡色彩 | [`MDT 2025-05-23–07-02`](../research/mdt_bullish_abc_h2_visual_screen_2025-05-23_2025-07-02.md) | `pattern_like / bullish-ABC / H2-like / transition-to-open-bull / ordinary-A / deep-but-late-controlled-B / first-resistance-borderline / no-low-cycle-audit / observation-only` |

### 视觉筛选的最小流程

1. 先看完整 Daily/4H/60m 图表，不先找标签；标出左侧主要高低点、区间边缘和明显阻力/支撑。
2. 再问它是否真的有方向性 A 腿，B 是否是回调而不是区间中部摆动，C 是否已经开始。
3. 只要“看起来像”就先进入候选：粗略画出可能的信号 K、入场区域、结构止损和第一目标区；不要求一开始精确到固定阈值。
4. 把候选分成“值得深入”“形态像但不值得交易”“明显不是这个 pattern”三类。
5. 只对第一类候选补 15m 触发、事件过滤、实际 R/R 和失败状态；第二类本身也保留为过滤样本。

## 4. 用户确认的长期形态主线

后续形态研究以以下清单为主，不把“触碰 EMA”本身当作形态：

1. **H1 / H2 / H3**：多头背景中的第一次、第二次、第三次向上尝试；
2. **L1 / L2 / L3**：空头背景中的第一次、第二次、第三次向下尝试；
3. **交易区间顶部卖出**：优先寻找区间顶部的二次入场或失败突破；
4. **交易区间底部买入**：优先寻找区间底部的二次入场或失败突破；
5. **趋势反转**：保留为高级形态，先记录，稍后再详细定义、复盘和验证。

EMA、AB=CD 和 measured move 都只能作为背景、位置、空间或目标的辅助字段，不能因为价格碰到 EMA 或达到一个测量值，就单独创建交易信号。

## 4. AB=CD 与 measured move：测量层，不是独立形态

### 5.1 方向腿等距

先冻结第一段 A→B 和回调终点 C，再投影第二段：

```text
多头目标 D = C + (B - A)
空头目标 D = C - (A - B)
```

允许记录“接近等距”“明显扩展”“明显不足”，不要为了得到漂亮的 1:1 而事后移动锚点。AB=CD 到位通常意味着第一目标或获利/停顿区域，不自动意味着反转。

### 5.2 其他常用 measured move

- **Leg 1 = Leg 2**：第一条方向腿、回调、第二条方向腿；常用于 ABC 延续；
- **Trading-range height**：突破区间后投影区间高度；
- **Breakout height / measuring gap**：从被接受的突破结构投影；
- **既有结构磁铁**：前高、前低、区间边缘、通道边界；它们优先于一个孤立的数学目标。

每个目标都要记录 `target_type`、锚点、计算时点、附近障碍和到达后的价格反应。测量目标是空间与管理工具，不是买卖方向的充分条件。

## 5. 每个案例统一记录的字段

```text
symbol
timeframe
market_state              # trend / range / transition / climax
direction
A_leg_origin / A_leg_end
B_correction_start / B_correction_end
B_leg_count
abc_mode                   # continuation / reversal / complex / unknown
H_or_L_attempt             # H1 / H2 / H3 / L1 / L2 / L3
location_and_left_structure
signal_bar / confirmation_bar
AB_equals_CD               # absent / approximate / present / unknown
measured_move_type
first_obstacle
structural_stop
invalidation
outcome                    # continuation / reversal / failure / no-trade / pending
evidence_status             # descriptive / research-candidate / replayed / validated
```

## 6. 研究边界与下一步

- 本文件不声称任何固定胜率；胜率必须来自预先定义、跨标的、按时间切分的回放或回测。
- `H1/H2/H3`、`L1/L2/L3`、操作性 ABC、AB=CD 和 measured move 先分栏记录，不能压成一个分数。
- 先从 `TPB-H2-L2`、`ABC-CONT`、`BOP-ABC` 各挑代表性多空案例，做因果标注；再决定哪些值得程序化。
- 严格三推楔形反转规则保持暂停；继续保留 `H3-L3-COMPLEX` 的视觉候选、延续样本、区间边界和 no-trade 样本，不能把它们偷换成自动反转规则。这里的工作目标是视觉筛选与人工优化，不是建立量化扫描器。
- 任何候选要进入交易系统，还必须通过现有市场许可、15 分钟触发、结构止损、第一障碍、成本和审计门槛。

## 参考资料

- [Al Brooks — Bar Counting: High and Low 1, 2, 3, and 4 Patterns and ABC Corrections](https://www.oreilly.com/library/view/trading-price-action/9781118172339/OEBPS/9781118172339_epub_c_17.htm)
- [Al Brooks — Measured Moves Based on the Size of the First Leg](https://www.oreilly.com/library/view/trading-price-action/9781118172339/OEBPS/9781118172339_epub_c_07.htm)
- [Brooks Trading Course — Price Action Trading Terms Glossary](https://www.brookstradingcourse.com/price-action-trading-terms-glossary/)
- [Codex Trading — Pullback and leg definitions](https://github.com/justin371/codex-trading/blob/main/docs/pullback-leg-patterns_CN.md)
- [Codex Trading — ABC continuation research contract](https://github.com/justin371/codex-trading/blob/main/research/abc-continuation-tpb-hypothesis_CN.md)
- [Codex Trading — H1/H2 and measured-move review](https://github.com/justin371/codex-trading/blob/main/research/klac-daily-high1-high2-mm-20260816_CN.md)

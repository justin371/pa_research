# PA Pattern 覆盖审计（视觉研究阶段）

日期：2026-08-23  
状态：`visual-research / coverage-audit / not-quantitative`

## 目的

这份审计用来回答一个实际问题：PA Research 目前到底已经看过哪些 Price Action pattern，哪些只是有零散案例，哪些仍然缺少能帮助视觉助手学习的对照图。

它不是胜率表、评分器或量化输入。第一阶段只要求在完整图表上判断“像不像”；只有视觉上值得深入的候选，才继续检查低周期触发、订单、结构止损、第一道独立支撑/阻力和粗略 R/R。这样可以避免把 PA Research 重新做成 Codex Trading 的程序化研究层。

当前 ABC 的阶段边界与停止同质深审的条件见[`ABC 研究状态与工作边界 v0.3`](abc_research_status_v0_3_CN.md)。

最新一轮 `AMD/QCOM/MU/HD/JPM/NKE/LLY/AVGO/AMAT/CSCO/TXN/NOW` 的轻量筛选见[`2024–2025 候选网格轻量视觉筛选`](visual_screen_candidate_grid_2024_2025_CN.md)。本轮没有新增普通开放趋势正向基准，主要补充了事件/跳空/嵌套尺度的过滤对照。

## 目标逐项证据审计（2026-08-23）

| 目标要求 | 当前证据 | 判断 |
| --- | --- | --- |
| 无后见之明地描述 A/B/C | `abc_h1_h2_h3_l1_l2_l3_scope_CN.md`、`docs/common_context.md`、视觉复核卡，以及 TSLA/NFLX/TSM/CRWD 等案例都要求按决策时点切片，禁止用后续 C、MM 或盈利倒灌 | **已形成工作框架** |
| H1/H2/H3 与 L1/L2/L3 | H1/H2、L1/L2 有多空条件样本；H3/L3 有 KLAC 候选和 TSLA、ANET、COIN、XOM、UBER、NFLX、ASML、NOW、DELL 等反例 | **条件性可用；H3/L3 未冻结** |
| 订单类型 | `order_branch_visual_protocol_CN.md` 已分开 stop、stop-limit、limit-retest、market-close、observation-only，并把跳空重订作为新合同 | **研究协议已形成；stop-limit 尚无独立成交样本** |
| 结构止损、第一支撑/阻力与 R/R | 决策矩阵和案例普遍先记录结构失效区，再找第一独立障碍；KLAC、NFLX、TSM、TSLA 等提供正向与 no-trade 对照 | **视觉原则稳定；不设固定阈值** |
| 足够的多空历史对照 | 已有多空、开放趋势、区间、过渡、事件/跳空、首障碍否决和计数重置样本；不是统计抽样，也不声称胜率 | **足以支持视觉助手当前工作版** |
| 成熟结论沉淀到 PA Research | 共同上下文、范围定义、视觉综合、决策矩阵、订单协议和案例文件均已同步；Codex Trading 未修改 | **已完成研究层沉淀** |

这张表的含义是：普通 ABC 的视觉识别已经可以作为后续筛图的工作能力使用；剩余问题集中在 H3/L3 的衰竭与延续边界、不同订单合同的统计口径，以及是否存在更干净的开放趋势正向样本。它们是未决研究问题，不应再迫使每个普通 ABC 候选重复完整深审。

案例状态的含义：

- `covered`：已经有多个案例或正反对照，视觉语言相对稳定；
- `conditional`：有可研究的正向路径，但计数、事件、缺口或首障碍仍限制结论；
- `boundary`：形态外形存在，但区间、高潮、计数重置、首障碍或订单合同否决了升级；
- `gap`：当前还缺少足够清楚的视觉对照，不代表该 pattern 不存在。

## 覆盖矩阵

| Pattern 家族 | 当前覆盖 | 已有视觉证据 | 仍缺少的关键对照 | 下一步优先级 |
| --- | --- | --- | --- | --- |
| 普通趋势中的 ABC 延续 | `conditional` | KLAC、TSLA、CRWD、AMZN、NVDA、MDT 过渡型多头，以及 NFLX/TSM 的空头对照 | 更干净的样本仍可作为补充，但不再阻塞当前视觉工作版；仅在新边界或指定案例出现时补审 | P2（条件触发） |
| H1/H2 多头 | `conditional / boundary` | [`H2/L2 第二次入场目录`](../patterns/02_h2_l2_second_entry/README.md)；KLAC H2、CRWD H2、AMZN H2、TSLA H2、NVDA H1、MDT 过渡型 H2-like、SPY 指数控制、SNOW 近期 H2-like | 普通开放趋势正向基准仍是条件性缺口；不主动重复寻找，遇到新的订单/首阻力边界时再补 | P2（条件触发） |
| L1/L2 空头 | `conditional` | NFLX L1、TSM L1 重订、AMZN L1、MCD L1、TSLA L2、NKE/QCOM/LRCX，ADBE 过渡转空 L1-like，CME 视觉边界，以及 QQQ/IWM/DIA 指数控制 | ADBE 仍不是纯开放趋势；更干净的样本可补充，但不再作为扩大股票池的默认任务 | P2（条件触发） |
| H3/L3 与复杂回调 | `boundary / conditional` | KLAC 熊旗、TSLA L3、ANET、ASML、COIN、NFLX、XOM、UBER、NOW、DELL；Futu 定向筛选的 BKNG、PM、AMD、GOOGL、NKE、WMT | H3 有 KLAC 条件候选，但 L3 尚无同等质量的“衰竭 + 反向触发 + 首障碍有空间”候选；最新定向筛选仍被首障碍、事件、趋势延续或背景方向否决，继续区分衰竭、延续和区间，只有新边界或订单分支才加样本 | P1 |
| 三推/H3-L3 压力状态 | `framework / comparison / provisional` | KLAC 衰竭候选、TSLA 卖出高潮与支撑反应、XOM/COIN/UBER 第三推扩张、ASML 区间重复测试、NFLX 高位多次测试；统一压力分流见[`Three-push / H3-L3 pressure-state framework`](three_push_pressure_state_framework_CN.md) | 仍缺无事件、双向、第二次确认清楚且首障碍宽裕的标准三推反转正例；继续优先区分衰竭、扩张延续、区间重复测试和通道延续 | P1 |
| 三推/楔形视觉形状 | `covered as boundary, not frozen` | TSLA 2026-05、NFLX 高位、多个 H3/L3 研究 | 保持“第三推减弱”与“第三推扩张”并排，不把 H3/L3 自动等同三推楔形反转 | P1 |
| 区间顶部/底部二次入场 | `framework / partial` | TSLA 区间边缘、RBLX、QCOM、TSLA 2024-03 区间上沿 L2、IWM 2024-04 指数控制，以及 [`交易区间边缘二次入场与失败突破`](range_edge_second_entry_framework_CN.md) | 仍缺一个空间真正宽裕的事件干净顶部/底部正向样本，以及失败突破重新进入的独立对照；保持区间逻辑，不能借用趋势腿计数 | P1 |
| 主要趋势反转 / MTR | `framework / partial / provisional` | TSLA 2024-03 区间上沿空头候选、NFLX 高位多次测试、TSLA 2025-09 突破否定、PLTR 普通 A 边界、ASML 双底样区间过渡、LOW 低位多头反转尝试；统一框架见[`MTR visual framework`](mtr_visual_framework_CN.md) | 仍缺无事件、双向、首障碍宽裕且过程完整的标准正例；继续区分反转尝试、普通回调、区间反应和三推延续，不升级为生产规则 | P1（条件触发） |
| 双顶/双底视觉边界 | `comparison / partial / provisional` | TSLA 2024-03 区间顶部、RBLX 区间下沿、NFLX 高位多次测试、ASML 双底样过渡、TSLA 2025-09 被 BOP 否定；统一对照入口见[`Double top/bottom, MTR and Final Flag comparison`](double_top_bottom_mtr_final_flag_comparison_CN.md) | 仍缺无事件、第二次确认清楚、首障碍宽裕且过程完整的双顶/双底反向正例；保持与普通回调、区间边缘、Final Flag、MTR 分开 | P1 |
| 头肩顶/底与圆顶/圆底 | `framework / partial / provisional` | NFLX 高位多次测试、TSLA 2024-03 复杂双顶边界、ASML/LOW 低位过渡候选、TSLA 2025-09 BOP 否定，以及 KLAC 普通旗形的“假右肩”对照；统一入口见[`头肩顶/底与圆顶/圆底视觉边界`](head_shoulders_rounded_top_bottom_visual_framework_CN.md) | 仍缺事件干净、颈线清楚、第二次确认明确、首障碍宽裕的标准头肩正例；也缺纯粹可冻结的圆顶/圆底正例；保持与复杂双顶/双底、MTR、区间过渡和普通回调分开 | P1（条件触发） |
| 失败突破 / 高潮反转 | `framework / partial / provisional` | TSLA 2025-03 卖出高潮后进入大区间、COST 2024-07 高潮型强 A 但首障碍拥挤、TSLA 2025-09 失败突破假设被 BOP 接受否定、XOM 2024-07 第三推扩张边界；统一框架见[`Failed breakout / climax reversal visual framework`](failed_breakout_climax_visual_framework_CN.md) | 仍缺无事件、双向、第二次确认清楚且首障碍宽裕的标准高潮反转正例；继续区分小反转/区间、MTR、Final Flag、Opening Reversal 与 BOP | P1 |
| 最终旗形 / Final Flag | `framework / partial / provisional` | KLAC 2025-10 多头浅旗延续控制、NFLX 2024-08 高位压缩反转边界、TSLA 2025-09 阻力下反转假设被 BOP 接受否定、KLAC 2025-03 熊旗延续控制；统一框架见[`Final Flag visual framework`](final_flag_visual_framework_CN.md) | 仍缺事件干净、第二次反向触发不跳空且首障碍宽裕的标准反转样本；保持与普通旗形、MTR、区间边缘和 BOP 分开 | P1（条件触发） |
| 开盘反转 / Opening Reversal | `framework / partial / provisional` | RBLX 2024-04-04 开盘上冲失败、COIN 2024-01-09 空头开盘反应、VRT 2026-04-17 开盘接受边界、TSLA 2025-03-04 跳空延续/回测订单边界；统一框架见[`Opening Reversal visual framework`](opening_reversal_visual_framework_CN.md) | 仍缺事件干净、反向确认清楚且首障碍宽裕的多空标准正例；继续与 BOP、Final Flag、MTR、区间边缘和普通 H/L 回调分开 | P1 |
| BOP / Gap-and-Go / 突破回踩 | `framework / partial / provisional` | TSLA 2025-09-11 阻力接受、TSLA 2025-03-04 跳空后 284 回测、QCOM 2024-07-24 开盘重订价、GOOGL 2024-03-18 跳空追价边界；统一框架见[`BOP / gap acceptance visual framework`](bop_gap_acceptance_framework_CN.md) | 需要更多事件干净、突破后回踩守住且首障碍宽裕的多空正例；暂不把 gap-and-go、BOP 回踩和失败突破合并 | P1 |
| 紧通道 / 宽通道 / 状态切换 | `framework / partial / provisional` | KLAC 2025-03 宽熊旗上沿空头恢复、TSLA 2025-08 强趋势/通道线候选、XOM 2024-07 宽旗扩张边界；统一框架见[`Channel visual framework`](channel_visual_framework_CN.md) | 仍缺一个平行边界已确认、事件干净、首障碍宽裕的紧通道正向样本；继续区分强趋势腿、趋势线候选、宽通道、区间和 MTR | P1 |
| 缺口后的订单分支 | `covered as boundary` | TSM 重订、NKE、QCOM、LRCX、GOOGL、BKNG、COIN、NVDA、VRT | 不再增加同质案例；只在新 pattern 同时出现缺口时，记录原 stop、开盘重订、limit-retest、观望四个合同的区别 | P3 |
| 多周期视觉复核 | `framework / partial / provisional` | TSLA、NVDA 的低周期确认，TSM 的缺口后重订，TSLA 2024-03 的 Daily L2 与 15m 跟随，QCOM/GOOGL 的开盘跳过边界；统一入口见[`Daily / 4H / 1H / 15m 分层框架`](multitimeframe_visual_review_framework_CN.md) | 继续补充“同一高周期合同的低周期确认”与“低周期自成交易”的对称对照；保持高周期首障碍、结构止损和低周期窄止损分开，不把不同合同结果合并 | P1（条件触发） |
| 趋势后段入场 / 追价过滤 | `framework / cross-pattern / provisional` | TSLA、KLAC、NFLX、TSLA 空头等受控回调、高潮风险、BOP 接受和后段无空间对照；统一入口见[`趋势后段入场视觉框架`](late_trend_entry_visual_framework_CN.md) | 继续把“等回调/二次入场、低周期确认、突破接受新合同、观望”与各 pattern 连接；不另造一个独立 K 线形态，也不把追价规则量化冻结 | P1（条件触发） |
| 第一独立障碍与 MM | `framework / cross-case stable principle` | 几乎所有已审计案例都记录了首阻力/首支撑与 MM 的先后关系；统一顺序见[`Measured Move、磁铁与目标层级视觉管理框架`](measured_move_magnet_target_hierarchy_CN.md) | 继续用视觉样本确认“先看左侧障碍，MM 只作后续路径”；补充不同路径的分批止盈和障碍接受对照；不要把精确 R/R 当成第一阶段入口 | P2（条件触发） |
| 强信号 K、压力收缩、EMA/META 汇聚 | `qualitative / reusable` | KLAC、CRWD、TSLA、NFLX、TSM 等 | 需要在更多不同背景下观察，而不是设固定实体、百分比或成交量阈值；回调缩量保持为重要参考、非必要条件 | P3 |
| Inside Bar / 两根 K 线反转 | `framework / partial / provisional` | KLAC 2025-10 两根反向序列、AAPL 2024-05 小实体/下影 H1-like、RBLX 2024-04 区间失败、KLAC 2025-06 H2 setup-confirmation、TSLA 2025-03 跳空非内包对照；统一框架见[`Inside Bar / two-bar reversal visual framework`](inside_bar_two_bar_reversal_visual_framework_CN.md) | 当前尚无一组严格母 K OHLC 已冻结、事件干净、首障碍宽裕的标准 Inside Bar 正例；继续区分严格内包、两根反转、H/L 信号序列和普通停顿 | P1 |
| 三角形 / 扩张三角形 / 区间内区间 | `framework / partial / provisional` | ASML 区间重复测试、TSLA 阻力下压缩后 BOP 接受、RBLX 宽区间内失败、COIN/XOM 扩张边界、KLAC 趋势旗形对照；统一框架见[`Triangle / expanding triangle visual framework`](triangle_expanding_range_visual_framework_CN.md) | 当前尚无严格、事件干净、两侧边界清楚、突破跟随和首障碍宽裕的标准三角形正例；继续区分普通压缩、Inside Bar/IOI、旗形、成熟区间、接受与失败突破 | P1 |

## 当前主动实现范围

用户已确认当前不继续扩展其他形态，先把以下 pattern 作为独立研究单元建立并逐项实现：

- H1/L1 第一次入场；
- H2/L2 第二次入场；
- ABC 趋势延续；
- 交易区间边缘二次入场；
- 失败突破与高潮；
- 突破回踩 / BOP；
- MTR 趋势反转；
- 三推 / H3-L3 压力状态。

目录入口见 [`patterns/README`](../patterns/README.md)。这不是把每个单元变成量化规则，而是先为视觉识别、案例、订单分支、首障碍和 no-trade 边界建立稳定容器。

## 课程交叉覆盖结论

PAHubCN 已读到用户指定的空章节停止点。课程中的趋势、突破、区间、反转、二次入场、概率、执行和风险内容已映射到上述研究单元或共同上下文；Swing/Scalp、Trader's Equation、订单、止损和仓位管理属于跨形态执行层，不另建 pattern 家族。当前唯一需要单独补足的视觉跨形态过滤层是“趋势后段入场”，已由[`趋势后段入场视觉框架`](late_trend_entry_visual_framework_CN.md)承接。VCP 仍是独立主题，不属于 PAHubCN 课程映射。

## 目前可以暂时认为已经形成的视觉语言

近期的 `SNOW 2026-08-14–08-21` 已经把“深但后段受控 B + H2-like 反应”补到多头侧，但它的第一阻力几乎贴着日线触发，因此仍是边界，不是正向样本。它和 PM 的差别在于：SNOW 的低周期短线分支也不足以消除首障碍；PM 则明确展示了第一合同开盘跳过、第二合同重建后仍被首阻力否决。

1. **背景先于标签。** 先看开放趋势、交易区间、区间边缘、过渡或高潮；区间中部的小波动不能因为有两次高点/低点就强行标成 ABC。
2. **A 腿决定第一轮筛选方向。** 强方向、少重叠、跟随清楚时优先看 H1/L1；普通 A 或宽通道时先观察，等待 H2/L2；这只是优先级，不是胜率承诺。
3. **B 腿看压力变化，不只看深浅。** 前强后弱、在支撑/阻力处稳定的深 B 仍可以保留 H2/L2；反向压力继续扩张、接受性穿越关键结构时，应降级为新趋势或区间。
4. **计数属于局部回调。** C 已经展开或旧回调被结构性破坏后，旧 H/L 计数不能无限延续；第三次推进也不自动等于楔形反转。
5. **形态和交易位置分开。** 形态可以 `pattern_like`，但前方第一道独立支撑/阻力太近时仍然是 `valid_no_trade`；不能用后见之明的 MM 或窄低周期止损把它救回来。
6. **视觉初筛不需要精确测量。** 日期、价格、腿端点可以先近似标注；精确测量只服务于第二阶段审计，不应阻止助手先召回候选。
7. **强 A、B 和信号 K 已有定性工作闸门。** 先确认方向性与跟随，再看 B 后段压力是否收缩，最后检查信号 K 是否位于有意义的位置；这套闸门不设固定数值，也不覆盖首障碍、订单或事件过滤。规范见[`H1/H2 优质定义（研究版）`](h1_h2_quality_definition_CN.md)，跨案例连接见[`ABC / H-L 统一决策矩阵`](abc_decision_matrix_CN.md)。

`ADBE 2026-01-12–01-27` 补了一个“父级过渡转空、局部形态清楚”的空头候选：`01-12/20` 方向性下行、`01-21/26` 受控反弹、`01-27` L1-like 跌破；低周期顺序、第一支撑和财报窗口已经通过初步审计，但市场逆势与父级过渡使它只能作为条件样本。它不被当作纯开放趋势基准，也不被写成胜率或量化输入。下一步仍需寻找更纯净的开放趋势空头样本，而不是继续堆叠同一类过渡案例。

2026-08-23 的新一轮视觉筛选进一步排除了 `XOM`、`PG`、`MCD` 的区间/重叠型外形，以及 `IBM`、`INTU`、`CAT`、`WMT` 的重新定价或状态切换型强下跌。它们保留为过滤对照，没有进入低周期审计；详见[`空头开放趋势视觉筛选日志`](bearish_open_trend_visual_screen_2026-08-23_CN.md)。

同日的 `CME 2026-05-20–06-17` 只做了轻量快筛：局部 A→B→L1-like 外形成立，但左侧过渡/区间色彩、较深 B、开盘跳过和 `249.98–243.30` 支撑簇拥挤，使它停在 `boundary / observation-only`。它补的是“看起来像但不值得继续深审”的空头控制样本，不是新的正向基准；详见[`CME 空头 ABC/L1-like 视觉快筛`](cme_bearish_abc_l1_visual_screen_2026-05-20_2026-06-17.md)。

紧接着的 `MDT 2025-05-23–07-02` 是多头侧的普通 A 对照：`05-23/06-16` 方向性 A、`06-17/25` 深但后段稳定 B、`06-27/07-02` 恢复并越过前高，视觉上可记为 H2-like；但父级仍是过渡，`06-16` 前高也压在早期恢复上方，因此只保留为 `pattern_like / first-resistance-borderline`，没有做低周期订单深审。它补的是“形态像、位置有意义，但还不是干净正向基准”的多头边界；详见[`MDT 多头 ABC/H2-like 视觉快筛`](mdt_bullish_abc_h2_visual_screen_2025-05-23_2025-07-02.md)。

## 研究缺口与停止条件

### 当前只在什么情况下继续找图

不再把“找到一张完美的普通开放趋势正例”作为默认任务。只有出现以下情况之一，才增加新的图表案例：

- 用户指定了新的标的、周期或订单问题；
- 新图可能填补 H3/L3 的衰竭、延续或区间边界；
- 新图出现当前尚未覆盖的订单合同、跳空状态或第一障碍结构。

新案例仍先标为 `pattern_like`，只写背景、A/B、位置和“为什么像”；只有四项都通过，才补低周期和订单合同。

### 什么时候可以说一个 pattern“研究得差不多”

不是出现一个漂亮例子就结束，而是至少有：

- 两个方向相同但背景不同的视觉候选；
- 一个形态相似、但被第一障碍或事件过滤否决的边界；
- 一个计数、区间或订单合同容易误判的反例；
- 明确写出仍不能从图表判断的部分。

满足这些条件后，才考虑把结论移交 Codex Trading 做实现审阅；在此之前，PA Research 只负责视觉研究、规则语言和案例证据，不修改 Codex Trading，也不连接 Execution Agent。

## 证据入口

- [`常用高质量候选形态清单`](../strategy/pattern_inventory_candidates.md)
- [`ABC / H1-H2 / L1-L2 视觉研究阶段性综合`](abc_visual_synthesis_v0_2_CN.md)
- [`ABC 决策矩阵`](abc_decision_matrix_CN.md)
- [`PA Pattern 视觉筛选协议`](visual_pattern_triage_protocol_CN.md)
- [`视觉复核卡`](../docs/visual_pa_review_card_CN.md)

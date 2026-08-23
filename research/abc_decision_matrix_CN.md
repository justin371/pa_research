# ABC / H-L1-3 统一决策矩阵

## 目的

把目前已经研究过的多空案例放进同一套决策字段，检查哪些变量可以跨案例重复，哪些只是区间边缘、跳空、财报或低周期特殊情况。矩阵用于研究和筛选，不是胜率表，也不是自动交易规则。

所有案例都遵守同一条边界：用完整图表寻找样本，但每个入场判断只使用当时已经可见的背景、位置、信号、订单、结构止损和第一障碍。后来出现的 C 腿、MM 到位和盈利不能反推入场质量。

## 统一字段

| 字段 | 研究问题 |
| --- | --- |
| 背景 | 是开放趋势、区间边缘，还是区间中部？ |
| A 腿 | 是否有方向性、扩张、低重叠和跟随？ |
| B 腿 | 是受控回调，还是前强后弱/宽通道/反向趋势？ |
| 计数 | H/L1、H/L2、H/L3 是否在同一回调内；C 启动后是否重置？ |
| 位置 | 是否靠近主要支撑/阻力、均线、缺口或角色转换区？ |
| 订单 | stop、limit/retest、确认单是否分别定义且真实可成交？ |
| 止损 | 是该 thesis 的结构失效位，还是被人为压窄？ |
| 第一障碍 | 入场时最近的独立支撑/阻力在哪里？ |
| R/R | 到第一障碍是否至少达到当前研究门槛约 `1R`；若未达到，是否应跳过？ |
| 状态 | 入场后如何定义 Working、Warning、Invalid？ |

## 当前案例矩阵

| 案例/分支 | 方向与计数 | 背景与 A/B | 订单与结构风险 | 第一障碍 / 研究 R/R | 当前结论 |
| --- | --- | --- | --- | --- | --- |
| `TSLA 2025-03-04` `284` 回测 | 空头 L1 回测分支 | 强 A；B 反弹/回测；EMA200 反应后空头恢复 | `283.8–284.3` sell-limit；结构止损约 `304` 上方 | `261.84–262.24`；约 `1.1R` | 当前最清楚的空头 PlayBook 候选；独立于原 `277.30` sell stop |
| `TSLA 2025-03-03/04` `277.30` sell stop | 空头 L1 原始突破 | 同一强 A/B 背景，但次日跳空越过触发价 | 实际成交约 `270.93`，旧计划几何失效；风险约到 `304` | 当时可见支撑约 `262.24`；约 `0.25R` | 方向可能正确，但不应按完整风险追入；需重算或取消 |
| `TSLA 2025-02-20` | 空头早期 L2 | 强 A 后 B 反弹；低点跌破后短暂收回 | `353.67` 下方 sell stop；15m `10:00` 触发候选；结构风险约到 `367.34` | `350.02–347.50`；约 `0.27–0.45R` | 低周期触发存在但第一障碍太近；Daily 全风险新仓跳过 |
| `TSLA 2025-03-05/06` | 空头后段 L2 | 后段延续；已靠近支撑 | 约 `267.71` 下方；结构风险约到 `279.55` | `261.84`；约 `0.5R` | 形态成立但第一障碍太近，跳过 |
| `TSLA 2026-03-12/18` | 空头 L1/L2 | 强 A；B 反弹到 EMA200 附近；C 内部两次空头尝试 | `2026-03-12` 约 `394.65` 下方、`2026-03-18` 约 `392.31` 下方；结构止损分别参考 `416.38`/`403.73` | 可见支撑 `389.95–385.39`；L1 约 `0.22–0.43R`，L2 约 `0.21–0.61R` | 强视觉候选；第一障碍过滤，Daily 新仓跳过；后续 `3/19` 跳空不能倒灌 |
| `TSLA 2026-05-19/06-10/06-25/26` | B 类三推/第三次测试候选；反向短线反应 | 三个低点逐步下移但间距缩小；位置有支撑候选；同一回调计数尚未证明 | 保守买入确认约 `379.12` 上方；结构止损约 `368.60` 下方；早期 15m 分支约 `374.75` 上方 | `385.20–387.80` 是先到阻力；保守分支约 `0.63–0.83R`，早期分支也先遇 `379.12/385.20` | 形态像、第三推后确有反应；保留为 B 类短线/no-trade 样本，不确认 H3 或主要反转 |
| `ANET 2024-05-16/06-10` | 独立 H3/L3-like 边界 | 第一推后第二推明显扩张；第三推在 `72.3–72.8` 支撑附近减速；`05-23` 跳空/放量待核对 | 反向订单未冻结；支撑处只保留短线反应分支 | 支撑区过近，且无后见之明反向触发不足 | C 类延续/高潮风险与支撑反应边界；不确认三推楔形 |
| `ASML 2025-05-23/06-11` | 旧 4H `L3` 标签的视觉边界 | 深回撤后 `715–718` 下沿两次测试；随后区间重叠，`06-09/11` 向上扩张 | 没有第三次同级别衰竭推进、反向触发和可审计订单几何 | 未冻结 R/R；不能把 `06-13` 后续下跌倒灌为早期 L3 | `not_h3_l3 / range-transition`；旧 correction-leg proxy 不等于视觉三推 |
| `KLAC 2025-03-24/26` | 熊旗顶部 H3 / 空头恢复 | 父级空头背景；`03-17/19/24` 三次向上测试逐步抬高；第三推未接受后向下扩张；SOXX 同期走弱 | `03-25` 低点约 `71.16` 下方 sell stop；`03-26` 首根 15m 触发且未跳空；结构止损主变体约 `74.50` | `66.6–65.1` 约 `1.4–1.9R`；`64.8` 约 `1.9–2.0R`；事后 `03-28/31` 分别到达第一、第二支撑；更远 MM 不作首障碍 | `pattern_like / research_positive_candidate / process-target-reached / first-and-second-support-reached / earnings-filter-passed / sector-aligned / low-cycle-confirmed`；H3 仍是视觉候选，不是验证规则 |
| `ANET 2024-02-13/16` | 空头 L2 / 强 A 后两次反弹 | `02-12/13` 跳空冲击形成强 A；`02-14`、`02-16` 两次反弹高点降低 | L2 研究 sell stop；止损主看 `67.85` 上方，不把跳空后的事后低点当触发 | `63.99–63.27` 先到支撑；以约 `65.4` 触发代理粗略不足 `1R` | `pattern_like / valid_no_trade / event-context-pending`；方向结构清楚但事件与空间阻塞 |
| `PLTR 2025-01-06/07` | 空头 ABC/L1；普通 A 边界 | `12-24` 后回落到 `01-02`；`01-03/06` 反弹/近似双顶；A 重叠较多 | `74.61` 下方 sell stop 研究分支；结构止损约 `80.06` 上方 | `69.75` 先到支撑；粗略不足约 `1R` | `pattern_like / valid_no_trade / ordinary_A_boundary`；后续下跌不能升级前面入场 |
| `TSLA 2026-03-25` 之后 | provisional 空头 L3 | A/B/C 候选；`2026-03-12` L1、`2026-03-18` L2；`3/19–3/20` 是 L2 跟随，`3/25` 反弹后重新计数 | `2026-03-26` 15m `10:15` 信号 K；`381.39` 下方 sell stop；结构止损代理约 `397.0` | `364.46–365.42`；约 `1.0–1.1R`；不能使用 `352.14` 后续低点 | 触发分支已审计；仍是延续风险候选，不是楔形衰竭或验证规则 |
| `TSLA 2024-03-13` | 空头 L2；形态清楚但过程边界 | 无事件；强 A、弱 B；局部区间上沿失败；L1 后 L2 触发顺序清楚 | `172.41` 下方 sell stop；结构止损约到 `182.87` 上方；`03-26` 高约 `184.25` 先破坏结构 | 入场前可见 `2023-04-26/27` 左侧支撑约 `152.37–153.75`；静态约 `1.6–1.9R`；MM `153.93` 与该支撑重叠，但 `04-16` 才到达，晚于止损失效 | `pattern_like / process-stop-first / first-support-late / range-edge-boundary`；不能称为原始 L2 过程正例 |
| `TSLA 2024-08-01` | 空头 L2 | 强 A；前支撑转阻力；同一 `233–235` 阻力二次失败；A 受财报跳空污染 | `226.79` 下方 sell stop；结构止损约 `235.0` 上方；总风险需按事件后波动调整 | 第一支撑 `214.71–215`；约 `1.5R`（研究近似） | 当前较清楚的事件驱动 L2 正例；可作有空间对照，但不作为无事件基准 |
| `MAR 2026-06-25` | 4H-like 空头 L1/L2 候选 | 上涨后的转弱；`2026-06-22` 强 A，`06-23/24` 反弹 B 后收弱 | 约 `381.39` 下方 sell stop；结构止损参考 `391.83` 上方 | 入场前可见 `2026-05-27/28` 支撑 `377.8–380.8`；约 `0.04–0.3R` | 跨标的视觉候选；第一支撑过近，valid no-trade；4H 计数仍待冻结 |
| `TSLA 2025-08-22` `327–328` 短线分支 | 多头 H2 低周期确认 | A-；B 深且前强后弱；支撑簇/EMA 汇合；更大区间上沿在上方；SPY/QQQ/XLY 同日偏强 | `326.64` 上方 buy stop；`10:15` 未从开盘跳过触发；窄低周期止损约 `318.68` 下方，宽日线结构止损约 `313.5–314` | 入场前第一主要阻力 `340.55`；窄止损约 `1.7R`，宽结构止损不足 `1R`；`2025-08-25` 路径到达 `340.55`，随后触及 `346.64–348.98` 阻力簇 | `research_positive_conditional / earnings-filter-passed / sector-aligned / low-cycle-trigger-confirmed / first-resistance-reached / process-target-reached / daily-no-trade`；不是无条件波段规则 |
| `NVDA 2024-09-24` | 多头 H2；深但后段受控 B；60m/15m 确认 | `09-11/12` 强 A；`09-19` 第一次尝试未越 `120.6`，`09-20/23` 再测 `114.7` 后 `09-24` H2；SOXX 同向 | `116.81` 上方 buy stop，`09-24` 未从开盘跳过；`11:30` 60m/15m 收回触发位，`12:30` 跟随；宽结构止损约 `112.5` 下方，低周期研究止损约 `114.8` 下方 | `120.6–121.6` 首阻力簇；宽止损约 `0.9R`，低周期分支约 `1.9R`；后续 `124.75` 只作结果审计 | `research_positive_conditional / bullish-H2 / low-cycle-trigger-confirmed / daily-space-borderline / event-check-pending`；两种止损是不同 thesis |
| `AMZN 2024-12-11` | 多头 H2-like；强上涨背景、浅 B；`12-09` 第一次尝试未被持续接受，`12-11` 第二次尝试 | `11-21` 低点约 `195.75` 到 `12-09` 高点约 `230.08`；`12-10` 回调到 `224.20`；XLY 同向 | `230.08` 上方 buy stop；`12-11` 未从开盘跳过，15m `10:15` 附近上穿；Daily 结构止损观察 `223.5–224.2` 下方，低周期窄止损另列；60m 接受度混合 | 触发前没有冻结出独立的更高左侧阻力，空间先记 potentially-open；`12-16` 后来约 `233`、`12-18` 后来最低约 `220` 只作过程审计 | `pattern_like / research_positive_conditional / strong-looking-A / controlled-B / bullish-H2-like / low-cycle-trigger-confirmed / follow-through-mixed / event-context-pending`；形态、订单可研究，但结构风险与首段空间不能用后见之明替代 |
| `COST 2024-05-15/16` | 多头 H1-like；strong-looking A 后两日 B；优质强多头信号 K | `05-02–10` 方向性上涨；`05-13` 首日下压较强，`05-14` 收窄；`05-15` 收盘靠高位；XLP 同日横向 | `779.96` 上方 buy stop；`05-15` 15m 约 `14:15–14:30` 可重建越过；`05-16` 开盘约 `782.08` 已越过原触发，精确成交与开盘重订分开；结构止损观察 `761.95` 下方 | `05-13`/`05-10` 高点簇约 `777.52–779.78` 几乎覆盖触发，第一段空间不足 `1R`；`05-16` 后续高点只作过程审计 | `pattern_like / bullish-H1-like / low-cycle-trigger-confirmed / first-obstacle-crowded / opening-skip / sector-mixed / valid_no_trade / event-context-pending`；信号 K 好不能取消第一阻力 |
| `JNJ 2025-08-29/09-02` | 多头 H1-like；strong-looking A、controlled B；板块顺势 | `08-01–15` 方向性上涨；`08-18–28` 回调后段收缩；`08-29` 强恢复；XLV 同期向上 | `174.35` 上方 buy stop；`08-29` 15m 约 `15:15` 只触碰 `174.35`；`09-02` 开盘约 `174.41` 越过原触发；结构止损观察 `171.62` 下方 | `08-22` B 内高点约 `176.74` 是触发上方首阻力；约 `2.39`，按日线结构风险粗略不足 `1R` | `pattern_like / strong-looking-A / controlled-B / bullish-H1-like / sector-aligned / opening-skip / first-obstacle-crowded / valid_no_trade / event-context-pending`；板块配合不能取消订单与首阻力 |
| `TSLA 2025-08-22` 日线高点追入 | 多头 H2 日线分支 | 形态有反应，但大 K 使风险宽；主要阻力近 | `340.25` 上方追入；合理结构止损较远 | `340.55`/`348.68–357.54`；不足 `1R` | 形态成立、交易跳过 |
| `TSLA 2025-12-12` | 多头 H2-like | 强 A 后两次回测 EMA20；`2025-12-09` H1 跟随不足，`2025-12-12` 强反应 | 约 `463.10` 上方 buy stop；结构止损参考 `435.25` 下方 | 左侧 `467–474` 高点簇；约 `0.2–0.4R`，即使压缩到 `441` 下方也不足约 `0.5R` | 视觉形态成立候选；第一阻力过近，日线 no-trade |
| `TSLA 2025-09-04` | 多头 H2-like | A 后深回调；支撑拒绝；主要阻力近 | 日线信号后次日跳空，原计划需重算 | 第一阻力约 `0.59R` | 形态可研究；日线直接交易几何不足 |
| `TSLA 2026-05-20` | 多头 H1/H2-like | 强 A 后深 B；EMA50/EMA200 与主要支撑汇合；低周期出现二次反应 | 日线高点 `417.46` 上方；结构止损约 `393.63` 下方 | `434.66` 首障碍约 `0.72R`；低周期路径另行研究 | 无事件多头基准；视觉质量高但日线直接追入跳过，Daily 计数不冻结为 H2 |
| `KLAC 2025-06-02/03` | 多头 H2 | 强 A；重复支撑簇；第二次测试后收回 EMA20；`2025-06-03` 15m 有跟随 | 研究触发约 `75.90`；结构止损约 `72` | 第一阻力 `79.03`–`79.79`，约 `0.8R`–`1.0R`（未计成本）；MM 约 `87` 仅作阻力突破后的延伸目标 | 视觉形态质量高；直接日线入场几何边界，需低周期管理或跳过，不把 MM 当授权 |
| `KLAC 2025-10-23` | 多头 H1 | 强 A；一天浅 B；15m 强确认；前高在触发上方，但有嵌套强趋势背景 | `2025-10-22` 高点 `114.13` 上方 buy stop；结构止损约 `104` 或低周期窄止损 | 严格分支：`115.49–115.63` 不足约 `1R`；磁铁分支：先看高点区接受，再看 MM `124.77` | `research_positive conditional / strict-first-resistance-no-trade`；需要用更多样本验证前高角色 |
| `ANET 2023-11-16/17` | 多头 H2-like | 局部 A 普通/不清楚；支撑反应明显，但背景含横向过渡 | 约 `53.7` 上方 buy-stop 研究分支；结构止损约 `52` 下方 | `2023-11-14` 高点约 `54.22`；明显不足约 `1R` | 跨标的视觉形态边界；形态像但首障碍过近，valid no-trade |
| `COIN 2024-01-09/10` | 空头 L1-like / L2-like | A 强但跳空/市场冲击污染；B 反向力度不弱；低点二次下破被跳空改变；低周期 L1 可重建 | L1 日线约 `151.32` 下方、15m 信号 K 低点约 `153.29` 下方；止损约 `161.38` 上方；L2 原触发被 `01-10` 开盘跳过 | 触发前第一支撑约 `148.81`；15m 分支约 `0.5R`，日线分支约 `0.25R`；`01-10` 早盘先触及首支撑 | `valid_no_trade / L1-low-cycle-confirmed / first-support-reached-before-stop / L2-opening-skip / event-context-pending` |
| `COIN 2024-01-04/05/08/09` | provisional H3-like 熊旗顶部 | 同一空头 A 后三次上探候选；第三次日内范围扩张，衰竭证据不足 | `01-09` 15m 反向信号 K 低点下方可成交；`01-10` L2 原触发被开盘跳过 | 15m 触发约 `153.29`、止损约 `161.38`；首支撑 `148.81` 约 `0.5R`；日线 `151.32` 分支约 `0.25R` | C 类扩张/延续边界；首支撑先到但空间拥挤；valid no-trade，不确认三推楔形 |
| `NFLX 2024-08-05/09-03/09-06` | 高位三推 / H3-like 顶部边界；空头 L1-like 反应 | 强多头 A 后多次高位测试；测试超过三次且重叠多；`09-03` 偏空信号 K，但顶部接受未完全失败 | `09-06 10:15` 15m 跌破 `67.10`，无开盘跳过；结构止损约 `71.60–71.70` 上方 | 触发前可见 `66.54–65.98` 首支撑约 `0.1–0.25R`；`09-06` 先到首支撑，`09-24` 高约 `72.24` 后续越顶 | `provisional-three-push-top / L1-like-low-cycle-confirmed / first-support-reached / later-structure-invalidated / valid_no_trade` |
| `SNOW 2026-08-14/17/21` | 多头 H2-like setup | 上涨背景；`08-14` 第一次回调，`08-17` H1-like 失败，`08-18`–`08-20` 深 B 后段受控，`08-21` 强反应 | 日线 buy stop 约 `333.50`；结构止损约 `313.50` 下方；低周期早触发不可与日线混算 | `334.45` 首阻力约 `0.05R`；`339.75–341.95` 高点簇约 `0.3R`；低周期分支到首阻力约 `0.8R` | `pattern_like / valid_no_trade / first-obstacle-crowded / confirmation-pending`；形态像但不值得按日线新仓执行 |
| `COST 2024-07-11/18` | 空头 ABC / L1-like；强反转型 A 边界 | 上涨末端 `07-11` 强烈反转空头 A；`07-15–17` 浅但偏弱的 B；`07-18` 跌破前低后扩张 | `07-17` 低点约 `832.3` 下方 sell stop；结构止损约 `847.4` 上方；不能使用 `07-18` 后见之明低点 | `07-12` 低点约 `828.1`，近端 `828–834` 支撑簇贴近/覆盖触发；首障碍明显不足 `1R` | `pattern_like / valid_no_trade / strong-A-climax-boundary / event-context-pending`；方向和 L1-like 结构存在，但空间与事件背景未通过 |
| `LLY 2024-06-06/13` | 多头 ABC / H1-H2-like；深 B 边界 | 上涨背景；`06-06–10` 局部 A 方向明确但非教科书强 A；`06-11/12` B 深且波动剧烈；`06-13` 恢复强但日线计数和信号 K 质量未冻结 | 研究 `06-12` 高点约 `858.8` 上方 buy stop；结构止损参考 `840.9`/`839.3` 下方；不能用低周期局部低点压窄风险 | `06-11` 高点约 `868.7` 是触发前可见首阻力；粗略仅约 `0.5R–0.6R`；`06-13` 高点不能倒灌 | `pattern_like / valid_no_trade / deep-volatile-B / signal-quality-pending / first-obstacle-boundary / event-context-pending`；恢复存在但不升级为优质 H2 正例 |
| `BKNG 2024-06-12/18` | 多头 ABC / H2-like；形态正向但跳空订单边界 | `06-12` 方向明确 A；`06-13/14` 浅且受控 B、重复支撑；`06-14` 优质多头信号 K；`06-17` 开盘跳过原触发 | 原始 `06-14` 高点约 `152.05` 上方 buy stop；实际开盘约 `152.66`，结构止损约 `149.8` 下方；回测/重订合同必须另列 | `06-12` 高点约 `153.96` 是触发前首阻力；按跳空成交粗略不足 `0.5R`，无跳空也约 `0.8R–1.0R`；MM 约 `154.2` 与近端阻力重叠 | `pattern_like / morphology-positive / valid_no_trade-on-original-order / gap-trigger-reprice / first-obstacle-boundary / event-context-pending`；形态比 LLY 清楚，但原始订单不通过 |
| `XOM 2024-07-25/30/31/08-01` | 空头 ABC / provisional H3-like；第三推扩张边界 | `07-18` 后强反转型 A；`07-25/30/31` 三次上探且第三次抬高；`08-01` 空头反应 K | `08-01` 低点约 `108.26` 下方 sell stop；结构止损约 `111.43–111.60` 上方；`08-02` 开盘约 `107.90` 后必须重算成交 | `07-24` 低点约 `105.20`；原始约 `1R`，跳空成交后约 `0.7R`；`08-05` 及后续低点不能倒灌 | `pattern_like / provisional-H3-like / C-class-expansion-boundary / valid_no_trade / gap-trigger-reprice / event-context-pending`；第三推不是衰竭型三推 |
| `WMT 2024-06-25/26` | 多头 ABC / H1-like；gap pullback 边界 | 上涨背景；`06-17–24` 方向性推进；`06-25` 深且放量的向下跳空回调；`06-26` 强收回 | `06-25` 高点约 `66.19` 上方 buy stop；结构止损参考 `64.8–64.9` 下方；窄止损不能与主结构分支混算 | `06-24` 高点约 `67.47–67.61`；主结构止损下粗略约 `1R`；后续上涨不能倒灌 | `pattern_like / bullish-H1-like / gap-pullback / signal-quality-pending / first-obstacle-boundary / valid_no_trade / event-context-pending` |
| `RBLX 2024-03-18/04-05` | 多头 ABC-like 外形；区间边缘反应，不是趋势延续 ABC | `03-18–28` 上涨发生在宽区间内；`04-01–03` 回到 A 起点和区间下沿；`04-04` 盘中冲高后收盘很差；`04-05` 后续恢复不能倒灌 | `04-03` 高点约 `36.66` 上方 buy stop 会被 `04-04` 开盘约 `36.97` 越过；结构止损看 `35.79` 测试低点下方；信号 K 质量失败 | 区间中部约 `37.3–37.8` 先到，区间上沿约 `39.0–39.2`；宽止损下不能只看远端 MM | `pattern_like / range-edge-reaction / not-ABC-continuation / signal-quality-failure / valid_no_trade / event-context-pending` |
| `GOOGL 2024-03-04/18` | 多头 ABC / H1-like；强 A、浅 B、跳空 C 边界 | `03-04–14` 方向性强 A；`03-15` 浅 B；`03-18` 开盘跳过前高和原 buy stop；后续上涨不能倒灌 | 原始约 `141.92` 上方 buy stop；实际开盘约 `147.30`，结构止损参考 `138.80` 下方；`limit-retest` 未回测即无成交 | 原始前高约 `142.32` 已近；跳空后首障碍空间被消耗，后续 `150.8` 不能倒灌 | `pattern_like / bullish-H1-like / strong-A-shallow-B / gap-trigger-reprice / first-obstacle-boundary / valid_no_trade / event-context-pending` |
| `HD 2024-07-25/26` | 多头 ABC / H1-like；深 B 到左侧支撑 | `07-01–18` 方向性 A；`07-19–24` 深回调至 `332.27–333.59` 支撑簇；`07-25` 第一次多头尝试，但信号 K 收盘质量一般 | `07-25` 高点 `341.31` 上方 buy stop；结构止损研究约 `331.50` 下方；`07-26 09:45` 15m 越过触发，未发生开盘跳过 | EMA200 约 `341.57` 几乎贴着触发；跳过它后前高 `357.39` 约 `1.64R`；若等 `07-26` 高点 `344.01` 上方，前高只约 `1.07R` | `pattern_like / bullish-H1-like / deep-but-position-controlled-B / signal-quality-boundary / EMA200-first-obstacle / sector-filter-warning / valid_no_trade / earnings-filter-passed` |
| `QCOM 2024-07-24 L1` | 空头 ABC / L1；强 A 后前强后弱 B | `07-17–19` gap-impulse A；`07-22/23` 反弹到 `188.06` 后回落；SOXX 同向下跌 | 理想 `184.14` 下方 sell stop；07-24 开盘约 `181.44` 跳过触发；结构止损约 `188.60` 上方；limit-retest 未成交 | 理想首支撑 `178.01` 约 `1.37R`；实际开盘成交后约 `0.48R` | `pattern_like / strong-A-gap-impulse / L1-gap-trigger-reprice / sector-aligned / valid_no_trade` |
| `QCOM 2024-07-30 L2-like` | 空头 ABC / L2-like；L1 后反弹再下破 | `07-26/29` 反弹到 `175.02`；07-30 低点二次下破；同周期计数仍保留 L2-like 边界 | `170.43` 下方 sell stop；结构止损约 `175.50` 上方；15m 约 10:00 触发，无开盘跳过 | `166.04` 第一支撑约 `0.87R`；EMA200 约 `165.24` 只是后续磁铁 | `pattern_like / L2-first-support-boundary / sector-aligned / earnings-window-invalid / valid_no_trade` |
| `UBER 2024-07-23/26` | 空头 A 后 H3-like 计数歧义；L1 后 L2-like | `07-17/18` 强反转型 A；`07-19/22/23` 三次上探候选；`07-25` 再抬高并扩张；XLY 同期偏弱 | `64.40` 下方 sell stop；`07-26` 15m 未从开盘跳过触发价但触发附近收回；结构止损约 `69.70–70.00` 上方 | 左侧 `62.90–63.30`；约 `0.2–0.3R`；MM/后续低点不能越级 | `pattern_like / provisional-H3-like / L2-like / C-class-expansion-boundary / earnings-filter-passed / valid_no_trade` |
| `AAPL 2024-05-08/09` | 多头 H1-like；事件驱动 A 后浅 B | `05-03` 财报后跳空形成方向性 A；`05-06/08` 浅 B 后段收缩；`05-08` 小实体/长下影，`05-09` 低周期恢复 | `181.10` 上方 buy stop；`05-09` 15m 从开盘下方上穿，未跳过；结构止损约 `178.20–178.40` 下方 | `184.98` 为入场前第一独立阻力；约 `1.1R–1.4R`，视止损分支而定 | `pattern_like / research_positive_conditional / event-driven-A / earnings-filter-passed / sector-aligned / low-cycle-confirmed / first-obstacle-borderline` |
| `NVDA 2025-06-23/07-03` | 多头 ABC / H1-like；形态正向、订单待重订 | 上涨父级中 `06-23/27` 方向性推进；`06-30/07-01` 短但偏深的 B；`07-02/03` 恢复并有跟随 | 若以 `07-02` 高点约 `157.39` 挂 buy stop，`07-03` 15m 首根开盘约 `158.16` 已跳过原触发；不得假定原价成交 | 第一轮尚未计算 R/R；先确认主要阻力、事件/板块和重订后的风险几何 | `pattern_like / morphology-positive / original-stop-invalidated-by-gap / reprice-pending` |
| `MSFT 2025-10-28/11-20` | 空头 ABC / L1-L2-like；空头边界候选 | 高位转弱后出现方向性下跌 A；`11-10/14` 反弹 B；`11-18/21` 再次向下 | 若以 `11-17` 低点约 `500.79` 挂 sell stop，`11-18` 开盘约 `491.32` 已跳过原触发；父级和事件背景也待核对 | 第一轮不计算 R/R；先确认事件、主要支撑、L1/L2 计数和重订订单 | `pattern_like / bearish-ABC-candidate / L1-L2-like / gap-trigger-boundary / pending` |
| `CRM 2025-03-10/28` | 空头 ABC；`03-13` L1-like，`03-26` 更像计数重置后的新 L1 | `02-20/03-10` 父级空头推进；`03-11/12` 反弹 B；`03-13` 首次向下恢复；`03-14/25` 反弹越过前 B 高点；`03-26` 新局部向下恢复 | 两个触发都能在 15m 按盘中顺序重建，未从开盘跳过；`03-13` 触发约 `275.88`，`03-26` 新局部触发约 `282.32` | `03-13` 首支撑约 `267–272`、空间拥挤；`03-26` 首支撑约 `273–276`，只有条件空间；结构止损分别参考各自 B 高点上方；`IGV/QQQ/SPY` 同步走弱 | `pattern_like / sector-aligned / L1-first-support-crowded / reset-L1-conditional-space / non-gap-trigger / pending` |
| `QCOM 2025-02-21/03-28` | 强 A 后宽 B / 交易区间边界；不冻结为开放趋势 L1/L2 | `02-21/27` 方向性下跌 A；`02-28/03-25` 多次反弹与回落，重叠多、区间感强；`03-28` 再次下探 | 第一轮不挂订单；区间内向下运动不能自动继承 ABC continuation 计数 | `146–149` 支撑簇在局部下破附近偏近；先用区间边缘/接受逻辑，暂不计算 R/R | `boundary / range-transition / not-open-trend-ABC / observation-only` |
| `NKE 2025-10-03/29` | 空头 ABC；强 A 后受控但不浅的 B；`10-28` L1-like，`10-29` 更像缺口跟随而非 L2 | `10-02` 高点约 `75.30` 到 `10-10` 低点约 `63.48` 的方向性 A；`10-13/27` 反弹至约 `68.91`，仍低于 A 起点；A 紧接财报，标记 event-context；XLY 在 `10-28` 未同步走弱 | 原始 `66.78` sell-stop 被 `10-28` 开盘约 `66.64` 略过；`10-28 13:15` 重新越过 `66.78`，sell-limit/retest 可研究但不能由 OHLC 证明成交；开盘重订与追入另列 | `63.48` 为入场前可见第一支撑；回测分支约 `1.2R` 且 `10-30` 进入首支撑；接受开盘约 `1.1R`；追入约 `0.5R`；结构止损看 `69.5` 上方 | `pattern_like / strong-A / controlled-B-conditional / minor-gap-trigger / original-stop-not-filled / limit-retest-process-target-reached / first-obstacle-borderline / sector-mixed / event-context / pending` |
| `TSM 2025-02-14/03-28` | 空头 ABC；强 A 后受控 B；`03-26` L1-like，后续仅为跟随 | `02-14` 高点约 `202.51` 到 `03-11` 低点约 `165.05` 的方向性 A；`03-12/25` 反弹至 `180.30`，仍低于 A 起点；SOXX/SMH/SPY/QQQ 同步走弱 | 原始 `177.22` sell-stop 被 `03-26` 开盘约 `176.66` 越过；`177.22` sell-limit 未回测（当日高约 `176.98`）；接受缺口后的重订约 `176.66` 或 15m 确认是独立分支；重订路径 `03-27` 到达首支撑 | 左侧首支撑簇 `167.99–165.05`；以结构止损约 `181.0–181.5` 粗略约 `1.6R+`；通过财报前三天过滤；过程审计只适用于重订分支 | `pattern_like / research_positive_conditional / strong-A / controlled-B / gap-reprice-space-positive / sector-aligned / earnings-filter-passed / process-target-reached / original-stop-not-filled / pending` |
| `AMZN 2024-09-23/10-15` | 空头 ABC；普通/方向性 A、深 B；`10-15` 无缺口 L1-like | `09-23/24` 高点约 `195.37` 后低点推进到 `10-03` 约 `180.88`；`10-04/11` 反弹到 `189.93`，仍低于 A 起点；`10-14` 未破前低，不能提前算 L1 | `10-15` 约 `10:45` 15m 才跌破 `10-11` 低点约 `186.30`；无开盘跳过；结构止损约 `190.7–191.2` 上方 | 左侧首支撑 `180.25–180.88`；约 `1.1R–1.4R`，边界；XLY 不弱，SPY/QQQ 偏弱；财报前三天过滤通过 | `pattern_like / ordinary-or-directional-A / deep-B / no-gap-trigger / first-obstacle-borderline / sector-mixed / earnings-filter-passed / pending` |
| `NFLX 2025-02-14/03-28` | 空头 ABC；方向性强 A、深但后段受控 B；`03-28` L1-like | `02-14` 高点约 `106.45` 到 `03-10` 低点约 `85.45`；`03-11/25` 反弹至约 `99.87`，仍低于 A 起点；`03-28` 无开盘跳过，09:45 盘中刺破、10:15 收盘确认 | 原始 `96.63664` 下方 sell-stop 可在 09:45 盘中触发；保守确认分支看 10:15；结构止损约 `100.8–101.2` 上方；limit-retest 需另记 | 左侧首支撑 `90.10–88.75`；粗略约 `1.4R–1.9R`，比 AMZN 更宽裕；事后 `03-31` 最低约 `90.06` 到达首支撑；XLC/SPY/QQQ 偏弱；财报前三天过滤通过 | `pattern_like / research_positive_conditional / strong-looking-A / deep-but-controlled-B / no-gap-trigger / first-obstacle-space-positive / process-target-reached / sector-aligned / earnings-filter-passed / pending` |
| `CRWD 2024-10-02` | 多头 H2-like；强 A 后深 B 后段稳定；`09-23` 首次尝试/失败突破歧义，`10-02` 第二次位置测试 | `09-11/20` 方向性 A，但含开盘跳空；`09-23/10-01` 深 B，`10-01/02` 在 `68.17` 附近稳定；SOXX `10-02/04` 配合 | `10-02` 高点约 `70.54` 上方 buy-stop；`10-03` 未跳过，15m 可重建；结构止损约 `67.4–67.8` 下方；收盘确认另计 | `75.11–75.54` 前高/失败突破阻力；盘中分支粗略约 `1.5R–1.9R`，不算宽裕；MM 锚点待定；财报过滤通过，`2024-07-19` incident 单列 | `pattern_like / research_positive_conditional / strong-looking-A / deep-B-late-stabilization / bullish-H2-like / low-cycle-trigger-confirmed / first-obstacle-space-positive-but-not-wide / earnings-filter-passed / incident-context-pending` |
| `VRT 2026-04-17` | 多头 ABC / H1-like 候选；深 B 后第一次恢复 | `04-14` 方向性冲击 A，开盘约 `306.94`、高约 `312.40`；`04-15/16` 深且前强后段才稳定的 B，低约 `292.61`；`04-17` 15m 恢复 | `04-16` 尾段约 `296.46` 上方原 buy-stop 被 `04-17` 开盘约 `298.64` 跳过；若重新以 `04-17` 15m 高点约 `305.53` 触发，结构止损参考 `292.61` 下方 | `310.94–312.40` 第一阻力簇；`305.53` 触发分支约 `0.42–0.53R`；开盘重订约 `2R` 但属于不同合同，接受条件未冻结 | `pattern_like / gap-impulse-A / deep-volatile-B / bullish-H1-like / original-stop-opening-skip / re-arm-or-open-acceptance-branch / first-obstacle-boundary / event-context-pending / valid_no_trade` |
| `V 2024-05-15` | 多头 ABC / H2-like；普通/方向性 A 后深但后段稳定 B | `05-06/10` 方向性 A；`05-13` 冲高后未接受，可视为第一次尝试失败；`05-14` 下探至 `269.15` 后下午稳定；`05-15` 形成优质恢复 K | 低周期以 `05-14` 尾段约 `273.338` 上方 buy-stop，`05-15 09:45` 15m 越过；日线 `276.48` 上方 buy-stop 被 `05-16` 开盘约 `277.00` 略过；结构止损参考 `269.15` 下方 | `276.89–277.72` 第一阻力簇；低周期分支粗略约 `0.85–1.05R`，更远 `282.69–285.54` 不能越过近端阻力 | `pattern_like / ordinary-or-directional-A / deep-but-stabilizing-B / bullish-H2-like / low-cycle-trigger-confirmed / daily-opening-skip / first-obstacle-boundary / earnings-context-pending / valid_no_trade` |
| `DIS 2024-07-16/08-02` | 空头 ABC / L1-like；父级区间过渡中的局部空头腿 | `07-16/25` 方向性下跌但 `07-23` 缺口强化；`07-29/31` 深且反向压力强的 B，仍低于 A 起点；`08-01` 第一次空头恢复 | `08-01` 低点约 `90.49` 下方 sell-stop；`08-02` 开盘约 `90.06` 跳过原触发；`90.49` limit-retest 未回测；结构止损约 `93.1–93.4` 上方 | `87.18–88.13` 第一支撑；理想/开盘重订粗略约 `0.6R–1.0R`；`08-02` 进入 `08-07` 财报前三个交易日禁做窗口 | `pattern_like / parent-range-transition / strong-looking-gap-A / deep-counterpressure-B / opening-skip / first-support-boundary / earnings-window-invalid / valid_no_trade` |
| `LRCX 2024-07-10/07-24` | 空头 ABC / L1-like；上涨父级后的强 A、短 B | `07-10/19` 强方向下跌且 `07-17` 缺口强化；`07-22/23` B 短、未回到 A 起点且后段转弱；SOXX/SMH 同向 | `07-23` 低点约 `93.98` 下方 sell-stop；`07-24` 开盘约 `93.39` 跳过原价；limit-retest 未回测；结构止损约 `96.9–97.2` 上方 | `07-19` 低点约 `90.00` 为第一支撑；理想约 `1.1R–1.3R`，开盘接受约 `0.9R–1.1R`；MM `75.38` 只能作后续目标 | `pattern_like / strong-A-gap-impulse / controlled-B-conditional / L1-gap-trigger-reprice / sector-aligned / first-support-borderline / earnings-filter-passed / valid_no_trade` |
| `JNJ 2025-09-18/10-08` | 多头 ABC / H1-like；方向性恢复后单日深回调，第一阻力过近 | `09-18` 低点约 `170.88` 后恢复；`09-30/10-03` 推进至约 `186.52`；`10-07` 下探约 `179.79` 后以长下影和高位收盘恢复 | `10-07` 高点约 `185.97` 上方 buy-stop；`10-08` 开盘约 `185.62` 未跳过；15m 首段高约 `186.25` 可重建触发；结构止损研究在 `179.79` 下方 | `10-03` 高点约 `186.52` 是触发前第一阻力，空间约 `0.55`，相对结构风险远低于 `1R`；XLV 仅轻微配合 | `pattern_like / ordinary-to-directional-A / deep-but-position-controlled-B / bullish-H1-like / low-cycle-triggered / first-obstacle-blocked / event-context-pending / valid_no_trade` |
| `JPM 2025-08-22/09-05` | 多头 ABC / H1-like；板块顺势但首阻力拥挤，次日跟随失败 | `08-22/29` 上涨背景；`09-02/03` 深但仍在母腿内的 B；`09-04` 强恢复并越过 `09-03` 高点 | H1 分支：`09-03` 高点约 `294.93` 上方 buy-stop，`09-04 09:45` 15m 触发；结构止损约 `288.97` 下方；另有 `08-29` 高点约 `297.26` 上方的独立突破分支 | H1 触发到 `08-29` 高点约 `297.26` 只有约 `2.33`，相对结构风险约 `0.39R`；XLF 入场时顺势；`09-05` 先冲高后跌回 B 区域 | `pattern_like / bullish-H1-like / deep-but-controlled-B / sector-aligned-at-entry / first-obstacle-blocked / breakout-branch-separate / follow-through-failure / valid_no_trade / event-context-pending` |
| `NVDA 2025-04-21/05-08` | 多头 ABC / H1-like；强方向 A、短但偏深且后段稳定 B；板块顺势 | `04-21/05-02` 恢复上涨；`05-05/06` 回调到约 `110.67` 后收回；`05-07` 强恢复 | 早期 H1 分支：`05-06` 高点约 `114.58` 上方 buy-stop，15m 后段可重建越过；晚盘宽幅推进使精确成交不清楚。若以 `05-07` 为新 setup bar，`05-08` 开盘约 `118.09` 跳过 `117.52` 原价，属于独立重订分支 | 早期触发上方 `05-02` 高点约 `115.24` 只差约 `0.66`，相对 `05-06` 低点下方风险约 `0.17R`；晚盘重订分支未冻结 | `pattern_like / strong-looking-A / deep-but-late-controlled-B / bullish-H1-like / sector-aligned / trigger-branch-ambiguous / first-obstacle-blocked / valid_no_trade / event-context-pending` |
| `COST 2025-04-21/05-16` | 多头 ABC / H1-H2-like；普通方向 A、深 B 后段稳定；板块配合但父级带过渡 | `04-21` 低点后至 `05-02` 恢复；`05-05/14` 深回调；`05-15` 先探约 `975.95` 后强力收回 | `05-14` 高点约 `992.68` 上方 buy-stop，`05-15 10:15` 15m 可重建触发且未开盘跳过；若等 `05-15` 高点则成为另一份突破合同 | `05-02` 高点约 `1010.69`；早期低周期分支约 `0.8R` 左右，日线晚分支首阻力几乎覆盖触发 | `pattern_like / ordinary-directional-A / deep-B / bullish-H1-H2-like / low-cycle-triggered / first-obstacle-borderline / sector-aligned / valid_no_trade / event-context-pending` |
| `MCD 2025-05-20/06-25` | 空头 ABC / L1-like；方向性 strong-looking A、短而受控 B；无缺口触发但首支撑阻挡 | `05-20` 高约 `312.33` 至 `06-20` 低约 `278.81`；`06-23/24` 反弹至 `285.18`；`06-25` 第一次空头恢复 | `06-24` 低约 `281.75` 下方 sell-stop；`06-25 10:45` 15m 实际穿越；`06-26` 跌破 `277.57` 是 L1 跟随，不自动是 L2 | B 高点上方研究止损 `285.5–286.2`；`06-20` 低点 `278.81` 是第一支撑，约 `0.66R–0.78R`；更低历史簇不能越级 | `pattern_like / strong-looking-directional-A / controlled-B / bearish-L1-like / no-gap-trigger / first-support-blocked / sector-mixed / market-not-aligned / valid_no_trade / event-context-pending` |
| `SPY 2025-07-17` | 指数多头 H1/H2-like 控制样本；计数待定 | `07-07/10` 普通方向性 A；`07-11/16` 深但后段稳定 B；`07-17` 第一次/第二次恢复均可解释 | `07-16` 高点约 `617.884` 上方 buy-stop；`07-17 09:45` 15m 可重建触发，开盘未跳过；日线结构风险看 `611.10–611.28` 下方 | `07-03/10` 高点 `619.42–620.00` 是触发上方第一阻力；粗略约 `0.2R–0.35R`，不能用后续 MM 或低周期窄止损救回 | `pattern_like / index-control / bullish-H1-H2-like / count-pending / low-cycle-trigger-confirmed / first-resistance-blocked / valid_no_trade / event-context-pending` |
| `PM 2026-01-22/23` | 多头 ABC / H1-H2-like；普通局部 A、两日 B、恢复计数待定；第二信号 K 质量较好 | `01-05` 附近低点约 `152.5` 到 `01-16` 高点约 `171.3`；`01-20/21` 回压低约 `160.4`；`01-22` 先探后收；`01-23` 继续恢复 | 以 `01-21` 高点约 `166.15` 的第一合同被 `01-22` 开盘约 `166.21` 略过；以 `01-22` 高点约 `167.27` 的第二合同在 `01-23 11:15` 15m 可重建，60m 随后接受 | `01-16` 高点约 `171.32` 是近端第一阻力；以 B 低点下方作母级结构风险时空间不足，不计算成正向 R/R | `pattern_like / ordinary-open-trend-candidate / bullish-H1-H2-like / low-cycle-branch-audited / first-obstacle-blocked / valid_no_trade / event-context-pending` |
| `ADBE 2026-01-12/27` | 空头 ABC / L1-like；父级从高位过渡转空；局部方向性 A、受控 B；低周期顺序可重建，个股/板块顺势但市场逆势 | `01-12` 高点约 `330.67` 到 `01-20` 低点约 `288.33`；`01-21/26` 反弹至约 `306.30`，未收回 A 起点；`01-27` 跌破 `01-26` 低点约 `301.40` | `01-27` 开盘约 `303.81` 未跳过；09:45 15m 首段和 10:30 60m 首段都向下穿过约 `301.40`；结构止损观察在 `306.30` 上方 | `01-20/21` 低点约 `288.33` 暂作第一支撑；粗略空间先记为明显优于拥挤边界，但不冻结精确 R/R；IGV 偏弱，QQQ/SPY 偏强；财报窗口已通过 | `research_positive_conditional / transition-to-open-bear / strong-looking-A / controlled-B / bearish-L1-like / no-gap-trigger / sector-aligned / market-countertrend / first-support-space-positive / earnings-filter-passed` |
| `CME 2026-05-20/06-17` | 空头 ABC / L1-like 视觉边界；父级过渡/区间；A 方向性但 B 较深 | `05-20/06-02` 下行至最低约 `243.30`；`06-03/16` 反弹至约 `270` 后段才稳定；`06-17` 再走弱，局部 L1-like | 本轮不冻结低周期订单；`06-17` 开盘约 `252.18` 已低于 `06-16` 低点约 `254.01`，原 sell-stop 属开盘跳过边界；结构止损和实际成交未审计 | `249.98–243.30` 支撑簇就在潜在触发下方，首障碍拥挤；不计算精确 R/R | `pattern_like / boundary / transition-to-open-bear / deep-B / opening-skip-boundary / first-support-crowded / observation-only` |
| `MDT 2025-05-23/07-02` | 多头 ABC / H2-like 视觉边界；普通到有方向性 A，深但后段稳定 B | `05-23` 低点约 `76.78` 到 `06-16` 高点约 `85.27`；`06-17/25` 回压至约 `81.24` 后稳定；`06-27/07-02` 恢复并越过前高；父级仍有过渡色彩 | 本轮不冻结 60m/15m 订单；早期恢复上方的 `06-16` 前高是首障碍边界；结构止损和实际成交未审计 | `85.27` 在早期 C/H2-like 触发附近，空间先记 borderline；不计算精确 R/R | `pattern_like / bullish-ABC / H2-like / transition-to-open-bull / ordinary-A / deep-but-late-controlled-B / first-resistance-borderline / observation-only` |

`?` 表示已有研究文件没有把该分支的精确成交价冻结为统一字段；在进入统计前必须补齐，不能用估计值替代。

## 当前跨案例结论

### 已有重复支持的研究假设

1. **先判背景，再判 A。** 区间中部不能因为出现三段波动就强行定义趋势 ABC；区间边缘反转要单独分组。
2. **强 A 决定优先级，不决定授权。** 强 A 后的第一次有效 H1/L1 值得优先观察；A 普通或 B 前段卖压很强时，等待 H2/L2 的信息价值更高。
3. **B 腿要看时间结构。** 前强后弱的 B 仍可能给出 H2/L2，但不能把深回调自动当作弱回调；宽通道和反向趋势要降级。
4. **计数是局部的。** H/L1-3 必须在同一回调内数；C 腿一旦展开，旧回调计数重置。第三根上涨/下跌 K 线不是自动 H3/L3。
5. **形态、订单和几何必须分开。** `284` 回测与 `277` 破位方向相近，但订单、成交和第一障碍完全不同，必须分别统计。
6. **第一障碍优先于 MM。** 近端支撑/阻力不足约 `1R` 时，Daily 新仓通常跳过；远端 MM 不能替代近端障碍。
7. **跳空是状态切换。** 跳过原触发价后，不保留原来的成交价和 R/R；重新回测可以形成新分支，但必须重新签订执行合同。
8. **“形态成立、交易跳过”是有效结果。** 这能防止把所有漂亮形态都硬转成交易。
9. **视觉形态与入场位置必须分栏。** `KLAC 2025-10-23` 的 H1 形态和确认都很清楚；严格障碍分支会因 `115.49–115.63` 太近而跳过，但强趋势磁铁分支认为强 A、浅 B 和嵌套背景可能让前高被快速穿越。两种解释必须并列保留，不能把任一分支直接推广。
10. **缺口后的订单要分层。** `TSM 2025-03-26` 说明原 stop 失效后，若重订仍保留足够首障碍空间，可以作为条件正向分支；`NKE 2025-10-28` 说明同样的小缺口在空间被压缩时应倾向 no-trade。回测 limit、缺口重订和观望不能合并。
11. **连续下跌不自动增加 L2。** 没有新的反向 B、独立第二次尝试或明确的同一回调 lineage 时，后续低点先记为 L1 后跟随；若 B 越过前极值或变成宽区间，默认重置/切换市场状态。

## 强 A、B 腿与信号 K 的工作闸门 v0.1

这一节把跨案例已经重复出现的视觉语言压缩成筛选顺序。它不是评分器，也不是固定胜率条件；“强”只表示值得优先观察，不表示自动下单。

### 1. A 腿：先看压力是否真正占优

工作上，只有同时看见**方向性**和**跟随/接受**，A 才能进入 `strong-A candidate`；低重叠、范围扩张或连续推进是额外加分项。

- **方向性**：推进 K 线的收盘方向清楚，收盘不经常被完全反向吞回；不能只凭一根孤立大 K 线贴上“强 A”。
- **跟随/接受**：后续 K 线没有立刻完全回到 A 起点，价格对新高/新低有接受，或继续沿方向推进。
- **低重叠/扩张**：多根 K 线之间重叠较少，实体或波动有方向性扩张；跳空可以增强视觉强度，但必须标为事件/缺口分组。
- **背景完整性**：A 不是区间中部的脉冲，也不是已经明显高潮后的最后一冲；若父级背景、A 端点或事件状态不清，降为 `strong-looking-A` 或 `A-unclear`。

因此，`strong-A`、`strong-looking-A` 和 `ordinary-A` 必须分开：事件跳空、财报冲击或单根大 K 可以很强，但不能直接与普通开放趋势 A 合并。

### 2. B 腿：看后段压力变化，不只看回撤百分比

- **受控 B**：回调可以有深度，但后段推进变慢、重叠增加或在支撑/阻力/EMA 处拒绝；关键结构没有被反向接受。
- **深但后段受控 B**：前段反向压力明显，后段开始收缩。这类窗口 H1/L1 降级，但 H2/L2 仍可研究。
- **未受控 B**：反向推进继续扩张，收盘持续接受穿越关键结构，或已经形成新的趋势方向；不要用 H2/L2 标签挽救。
- **区间化 B**：双方在同一带反复穿越、重叠很高；此时优先使用区间上沿/下沿逻辑，计数可能重置。

量能萎缩是“卖压/买压减弱”的重要参考项，但不是必要条件；价格位置、收盘质量和后段压力变化优先于单独的成交量解释。

### 3. 信号 K：局部质量与交易可行性分开

优质信号 K 的工作参考包括：

- 在有意义的支撑/阻力或 EMA 汇合区出现方向性实体，收盘接近方向极值；
- 先试探反向、随后收回的 K 线，或带明显下影/上影的 doji/小实体，并且重新站回关键结构；
- 信号 K 不是单独漂在区间中部，且下一根 K 线的触发方向与它一致。

信号 K 只能证明局部反应，不能取消前方第一障碍，也不能把 setup/count bar 事后改写成优质信号。H1/H2/L1/L2 仍要分别记录 `signal K → trigger → follow-through`；H3/L3 还要先通过第三次尝试的分流。

### 4. 现有案例的最小对照

| 案例 | A/B/信号 K 视觉判断 | 交易层结论 |
| --- | --- | --- |
| `NFLX 2025-02-14–03-28` | 方向性 A；深但后段受控 B；低周期空头信号与跟随顺序清楚 | 无缺口且首支撑有条件空间，保留为条件正向样本 |
| `TSM 2025-02-14–03-28` | 强 A；受控 B；L1-like 恢复可见 | 原 stop 被缺口跳过，只有重订分支可研究，不能沿用原成交价 |
| `NVDA 2024-09-11–09-25` | 强 A；深但后段受控 B；H1 失败后 H2 信号 K 和低周期确认清楚 | 低周期 thesis 有空间，日线结构止损首障碍偏近，两个分支不能混算 |
| `COST 2024-05-13–05-16` | 强-looking A；B 后段收缩；强多头信号 K | 前高簇贴近触发，形态可见但 `valid_no_trade` |
| `LLY 2024-06-06–06-13` | A 有方向但不够干净；B 深且波动大；恢复 K 不足以修复结构 | 首障碍约 `0.5R–0.6R`，作为深 B/信号质量边界 |
| `QCOM 2025-02-21–03-28` | A 后 B 扩张并区间化，后续低点不能自动当 L2 | 切换为区间逻辑，不作为开放趋势 ABC |

这组对照支持一个实用的视觉顺序：**先确认 A 是否真的占优，再看 B 后段是否收缩，最后才评价信号 K；首障碍和订单合同仍可否决交易。**

### 尚未达到可冻结程度的部分

- “强 A”这套定性闸门在更多市场状态下是否仍可迁移；当前不冻结数值阈值；
- B 腿的回撤深度、时间整理和前强后弱之间如何分档；
- 第一障碍约 `1R` 是否应按 Daily、60m、15m 和波动率分档；
- H3/L3 何时是动能衰竭，何时只是强趋势延续；
- sell stop、sell limit/retest、stop-limit 的滑点和未成交样本如何统一统计；当前案例只有 stop/limit-retest/跳空重订证据，stop-limit 仍是协议层的样本缺口；
- 低周期止损与大周期结构止损如何在同一研究数据库中分层；
- 跨标的、跨市场状态后是否仍然成立。

## 统计前的最小数据要求

每个案例至少记录：

1. 最早可识别 A 日期，以及实时决策日期；
2. 当时可见的 B 结束区和 H/L 计数；
3. 信号 K、触发价和订单类型；
4. 结构止损、实际/理论成交和滑点；
5. 第一障碍及其 R/R；
6. 事件风险、市场/板块许可是否已核对；
7. Working、Warning、Invalid；
8. 结果、MAE/MFE 和过程评级；
9. 是否为执行案例、有效 no-trade 或错过的合格机会。

在这些字段完成之前，研究结论保持 Hypothesis，不进入 Codex Trading 的生产规则，也不交给 Execution Agent。

## 下一步

无事件多头基准已经补入：`TSLA 2026-05-20` 视觉质量高，但日线首障碍不足；H3/L3 对照现在包含 KLAC `2025-03-24/26` 的正向候选、TSLA/ANET 的延续或支撑反应边界，以及 ASML 的区间过渡边界。普通 ABC/H1/H2/L1/L2 已有足够的工作版对照，不再主动扩大同质股票池；只有出现新的边界、订单分支或用户指定案例时，才做针对性补审。当前重点转为 H3/L3 的衰竭/延续区分，并保持不修改 Codex Trading。

## 普通 A 腿筛选日志（2024-05 至 2024-07）

本轮人工筛选的 `MSFT`、`AMZN`、`META`、`NFLX`、`CAT` 都能画出普通 A → B → 恢复尝试的外形，但触发前第一独立阻力分别贴近或覆盖订单附近，因此保留为 `pattern_like / valid_no_trade`，不把后续突破倒灌成正例。详细证据见 [`ordinary_a_visual_screen_2024-05_2024-07_CN.md`](ordinary_a_visual_screen_2024-05_2024-07_CN.md)。这批样本的作用是补强“普通 A 也必须过空间闸门”的负向对照；事件检查未在该日志中作为正向证据使用。

## LOW 过渡背景与首障碍边界

`LOW 2024-06-11–06-24` 形成了急跌后的方向性多头 A、回调、H1/H2-like 恢复；但父级仍偏过渡，Daily 信号 K 不够干净，且 `2024-02-23/26` 高点簇约 `221.92–223.01` 在触发上方很近。低周期可以重建越过触发的过程，却不能创造 Daily 结构止损下不存在的空间。该案例保留为 `pattern_like / bullish-ABC-candidate / H1-H2-like / first-obstacle-crowded / valid_no_trade / event-context-pending`，详见 [`low_bullish_h1_h2_first_obstacle_boundary_2024-06-11_2024-06-24.md`](low_bullish_h1_h2_first_obstacle_boundary_2024-06-11_2024-06-24.md)。

# PA 图表视觉识别冒烟验收（2026-08-24）

状态：`smoke-test / acceptance-pending / visual-first`

## 目的与边界

本记录只验收一件事：能否从实际图表图像中先识别背景、位置和主要 Price Action pattern，并明确不确定性。它不是胜率测试、交易建议、量化扫描器或 Execution Agent 接口。

本轮使用公开网页中的历史图表图片作为能力冒烟样本；图片只在本地临时查看，没有复制进仓库。公开图片有的带有作者画线或文字标注，所以本轮不是盲测，也不能作为最终验收集。所有图片的周期、标的、事件和完整左侧背景，以图中直接可见内容为准；图中看不到的字段按缺失处理。

## 识别输出合同

每张图先输出以下字段，暂不填写订单、结构止损、第一障碍、R/R、评分或管理规则：

```text
primary_pattern:
secondary_context:
state_transition:
market_state:
location:
attempt_or_count:
directly_visible_facts:
uncertainty_or_invalidation:
recognition_result:
```

`recognition_result` 只允许：`pattern_candidate`、`boundary_candidate`、`observation_only`、`not_enough_image_evidence`。只有在未标注、周期和价格轴清晰、父级与局部结构均可复核的图像集上重复通过，才可以从 `smoke-test` 升级为 `acceptance`。

## 本轮图像结果

| 样本 | 图上直接可见事实 | 视觉识别 | 仍不能从图上确认的内容 | 结果 |
| --- | --- | --- | --- | --- |
| [TSLA wedge 图](https://www.tradingview.com/symbols/NASDAQ-TSLA/ideas/?sort=recent) | K 线在两条向外分离的白色边界之间反复摆动；上边界上斜、下边界下斜；当前价格仍在边界内部 | `primary_pattern: expanding-triangle / broadening-range candidate`；有多次摆动，但不能仅凭这张图冻结为三推 H3/L3 | 图片本身缺少清晰的完整标题、周期和左侧父级；不能确认是收敛楔形，也不能确认三次尝试属于同一 lineage | `boundary_candidate` |
| [Breakout–Pullback 图](https://ftv.com.vn/price-action-la-gi) | 价格跌破水平支撑；随后向上回测旧支撑附近；回测后再次向下推进 | `primary_pattern: bearish BOP-like`；`state_transition: BOP candidate`；旧支撑转为潜在阻力的视觉关系清楚 | 事件、周期、完整父级、接受条件和真实订单合同不可见；来源文字标注不能替代图上证据 | `pattern_candidate` |
| [IOI / BO PB 图](https://www.brookstradingcourse.com/support-forum/general-trading-discussion/question-ioi/) | 上涨腿突破水平位；突破后出现小实体和重叠；随后价格继续向上 | `primary_pattern: bullish breakout-pullback candidate`；可记为 `H2-like`，但不冻结 H2 计数 | 图中没有完整周期、标的、事件背景；作者的 `ioi, BO PB` 标注不能直接当作 PA 计数证据 | `pattern_candidate` |
| [失败收复图](https://internationaltradinginstitute.com/blog/liquidity-grabs-institutional-trading-strategy/) | 水平线标出前低；价格下破后反弹，但没有重新站稳该水平，随后继续走弱 | `primary_pattern: failed-reclaim / failed-breakout boundary`；可作为 RFB/失败突破的视觉边界样本，但不强行命名为完整 RFB | 图中无法确认区间父级、周期、事件和触发合同；“流动性”解释不作为 PA 事实 | `boundary_candidate` |
| [TSLA 三推标注图](https://www.tradingview.com/u/tickeron/) | 日线标题可见；三段摆动被画在两条边界之间，并标出 `#1/#2/#3`；后段向下离开 | `primary_pattern: three-push / wedge candidate`；`state_transition: possible range-transition or reversal candidate` | 这是折线图而非完整 OHLC 图，且三次计数已由作者标注；不能据此冻结 H3/L3、反转触发或交易合同 | `observation_only` |

## 冒烟测试结论

- 图像层面可以识别出候选形态，并能把“像某个 pattern”与“已经具备交易合同”分开。
- 可以看出 BOP-like 的突破—回踩—重新离开，也可以看出失败收复、三推/楔形和 expanding-range 的边界。
- 可以识别 `H2-like`，但不会因为图上写着 H2 就自动冻结 H2；H1/H2/L1/L2 必须在同一周期、同一回调 lineage 和完整左侧背景内确认。
- 本轮 5 张图中，`pattern_candidate` 2 张、`boundary_candidate` 2 张、`observation_only` 1 张；这只是能力冒烟计数，不是胜率或质量评分。
- 最终图像验收仍为 `acceptance-pending`：本轮样本含作者标注，且多数缺少完整周期、事件、父级和低周期证据。不能把本轮结果写成“所有 pattern 已稳定自动识别”。

## 优化闸门

在获得一组未标注、可读、包含 ticker/周期/价格轴和足够左侧背景的 Daily/4H/1H/15m 图像，并逐张记录上述输出合同之前，暂停以下工作：

1. 订单规则、结构止损、第一障碍和 R/R 优化；
2. 固定阈值、评分、胜率或量化扫描器；
3. Codex Trading 生产规则修改；
4. Execution Agent、账户、订单或任何执行连接。

下一轮应使用未标注的正例、边界例和反例，先复核 `H1/L1`、`H2/L2`、三推/H3-L3、ABC、BOP、失败突破、MTR、区间边缘二次入场，再决定是否进入交易层优化。

## 同标的多周期与两年左侧背景复核：TSLA（截至 2026-08-21）

这一轮把新增的左侧背景要求落实到同一标的：先看约两年 Daily，再看嵌套的 4H-like、1H 和 15m。四张无 pattern 标签的派生图已保存到：

- [`TSLA Daily ~2Y`](assets/visual_recognition/2026-08-24/tsla_public_mtf/TSLA_Daily_2y.png)
- [`TSLA 4H-like`](assets/visual_recognition/2026-08-24/tsla_public_mtf/TSLA_4H_like.png)
- [`TSLA 1H`](assets/visual_recognition/2026-08-24/tsla_public_mtf/TSLA_1H.png)
- [`TSLA 15m`](assets/visual_recognition/2026-08-24/tsla_public_mtf/TSLA_15m.png)
- [图像来源与聚合说明](assets/visual_recognition/2026-08-24/tsla_public_mtf/README.md)

### 证据头

```text
symbol: TSLA
data_source: public Yahoo Finance Chart API via Jina Reader
data_status: historical public data; not Futu; not live authorization
latest_complete_rth_bar: 2026-08-21 16:00 America/New_York
timeframes_seen: Daily (~2Y left context) / 4H-like / 1H / 15m
event_context: unknown; this round does not declare event-clean
chart_scope: full two-year Daily context plus nested recent intraday windows
```

`4H-like` 是同一来源 60m RTH bar 按每个交易日连续四根聚合，不冒充原生 4H。Daily 图显示 EMA20/50/200；这些均为背景层，不能创造 setup、trigger 或 authorization。

### 直接可见事实与识别

| 周期 | 直接可见事实 | 背景/位置 | 主识别与计数 | 视觉失效边界 | 结果 |
| --- | --- | --- | --- | --- | --- |
| Daily ~2Y | 2025-12 高点后经历宽幅回落；2026-07-29 在约 `297.38` 附近出现明显低点，随后恢复至 2026-08-21 收盘约 `362.86` | 当前收盘高于 EMA20 `342.10` 与 EMA50 `358.78`，但低于 EMA200 `382.90`；上方先看 `366–386`，再看 `405–413`、`430–453` 和 `485–499` 压力区 | `primary_pattern: MTR / recovery candidate`；`market_state: transition / broad-range recovery`；不能把这段恢复直接冻结成 Daily H2 | 回到最近恢复的约 `330–337` higher-low 区会削弱局部恢复；跌破 `297.38` 则破坏这次晚七月反转腿；不把 EMA 当止损 | `pattern_candidate` |
| 4H-like | 由约 `410` 一路下行到约 `297`，随后形成较清楚的 higher-low / higher-high 恢复；8 月中旬后推进加速，8 月 20–21 再次上行 | 价格已离开 `297–310` 低位带和 `330–350` 恢复基座，正在接近 Daily 的 `366–386` 与 EMA200 背景 | `primary_pattern: bullish recovery continuation / ABC-H2-like candidate`；`secondary_context: late-July sell-climax reversal`；多层嵌套，H2 计数不冻结 | 失守最近 `330–350` 恢复结构会先破坏局部延续；回到 `297–310` 下方则回到原低位边界 | `pattern_candidate / count-pending` |
| 1H | 8 月初低位后阶梯式上行；8-12 附近回压后重新推进，8-14 扩张，8-18/19 再次整理后越过约 `349–351`，8-20/21 推进至 `360–366` | 当前接近最近局部高点，且上方受 Daily `366–386` 位置约束；不是在开放空间中首次出现的低位 H1 | `primary_pattern: bullish ABC continuation / H2-like candidate`；`attempt_or_count: nested attempts, unclear`；不能把 1H 计数与 Daily 计数相加 | 接受跌回约 `337–342` 会破坏这段低周期恢复；低于约 `330` 则转回更宽的过渡/区间解释 | `pattern_candidate / count-pending` |
| 15m | 8-19 后段从约 `340–342` 推进至 `349–351`；8-20 反复测试后，8-21 以强推进越过约 `349–351`，随后在 `360–366` 高位窄幅整理 | 旧的短线阻力可能转成支撑，但 8-21 的跳跃式强推进使订单合同和多日 retest 不能从这张图直接冻结 | `primary_pattern: bullish BOP-like / breakout-acceptance candidate`；`state_transition: BOP-like, not clean multi-day BOP`；H2/L2 不冻结 | 重新接受到 `348` 下方会削弱角色转换；回到 `342` 下方则 BOP-like 的短线接受边界失效；这些是视觉边界，不是订单止损 | `boundary_candidate / no-new-positive-for-clean-multiday-BOP` |

### 两年重要高低点与位置复核

以下数值用于确认图上的重要锚点，不是把支撑阻力机械化：

- 两年可见主要低点：`2024-08-28` 低约 `202.59`；`2025-04-07` 低约 `214.25`；它们构成远端历史低位背景。
- 两年可见主要高点：`2025-12-22` 高约 `498.83`；`2026-05-13` 高约 `453.40`；它们构成上方长期压力背景。
- 当前窗口的重要中间点：`2026-07-20` 高约 `386.61`；`2026-07-29` 低约 `297.38`；`2026-08-21` 高约 `366.50`、收约 `362.86`。
- 视觉上可先保留的区域：`297–310` 低位支撑、`335–350` 恢复基座、`366–386` 当前近端压力、`405–413` 旧高点/压力、`430–453` 更高压力、`485–499` 两年高位区。区域可重叠，不能把每个区间中间价当成精确 level。
- EMA 位置：最新 Daily 收盘在 EMA20/50 上方、EMA200 下方；因此短线恢复已经出现，但两年背景仍不是无条件的开放多头趋势。

### 本轮多周期裁决

1. **看图识别层：通过一轮。** 能从同一标的的两年 Daily 背景与嵌套低周期中分开识别 `MTR/recovery candidate`、bullish continuation/H2-like candidate 和 15m BOP-like 状态。
2. **计数层：未通过最终验收。** Daily、4H-like、1H、15m 的推动腿和尝试没有被混加；但 1H/15m 的 H1/H2/L1/L2 仍因嵌套腿、强扩张和跳跃式推进而保留 `count-pending`。
3. **BOP 层：保留边界。** 15m 有突破—旧位附近接受—继续离开的外形，但 8-21 的强跳跃和缺少多日 retest 不足以升级为干净的多日 BOP 正例，结论保持 `no-new-positive-for-clean-multiday-BOP`。
4. **两年背景层：已纳入。** 重要高低点、支撑阻力区域和 EMA20/50/200 已作为视觉背景记录；没有把任何 EMA 交叉或单一 level 当成 pattern 或交易许可。

最终状态仍为 `acceptance-pending`：这一轮证明了在可读、无 pattern 标签的派生多周期图上可以先做结构识别，但还需要更多标的、正例、边界例和反例重复验收，才能声称 H1/H2/L1/L2 与三推/H3-L3 在所有图表上稳定识别。优化层继续冻结。

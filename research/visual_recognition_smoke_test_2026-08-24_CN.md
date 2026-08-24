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

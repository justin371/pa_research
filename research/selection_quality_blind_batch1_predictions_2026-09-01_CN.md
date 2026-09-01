# PA Research 选股质量盲测 Batch 1：首次视觉答案冻结

日期：2026-09-01  
状态：`research_only / frozen_visual_answer / outcome-hidden / expert-adjudication-pending / no-new-positive`

## 一、冻结边界

本文件记录主 Agent 在逐张查看[`Batch 1 无标签图表资产`](assets/visual_recognition/2026-09-01/selection_quality_blind_batch1/README.md)后、接触这些截止日之后的价格路径或对应回放结果之前给出的首次视觉答案。抽样由固定种子和合法索引区间决定，不根据形态漂亮程度或事后盈利挑选。

本批只测图形发现和候选排序，不是当前行情选股：

- 数据为仓库既有历史 Daily，不是实时行情；
- 没有在本轮核验截止日市值、20 日成交额、财报、市场或板块许可；
- 没有冻结订单、结构止损、精确第一障碍或回放目标；
- `H1-like/H2-like/L1-like/L2-like/three-push-like` 均是视觉候选显示，不写入冻结 `internal_label`；
- 专家裁决、事件补核和未来价格只能进入独立文件，不能改写本文件。

因此本文件的 `direction` 是图表研究方向，不是交易授权；`shortlist_rank` 只表示在这 12 张图内值得先深审的相对顺序。

## 二、首次视觉答案

| Sample | 方向 / 父级 | 首次视觉读法 | A、B 与 EMA | 两年位置和第一障碍 | 处置 / 排名 | 主要不确定性 |
| --- | --- | --- | --- | --- | --- | --- |
| `BQ1-VEEV` | `short / open_bear_trend` | `L1-like conditional` | 下跌 A 清楚；从约 150 反弹至 168–172 后 K 线收缩；EMA20/50 均明显向下 | 回调靠近下降 EMA20；下方先看 150 附近旧低，粗看仍有空间 | `deep_reviewed / shortlist_rank=1` | A 已运行较久；必须确认当前是同一受控 B，而不是末端卖出高潮后的区间 |
| `BQ1-MAR` | `long / open_bull_to_high_range` | `H1-like conditional` | 约 262 至 292 的连续推进较强；随后三根回调 K 小于 A；EMA20/50 向上，EMA200缓升 | B 回到约 280 的突破/EMA20区域；292 是近端高点，305 左右是两年主要高点 | `deep_reviewed / shortlist_rank=2` | 截止日仍是回调阴线，没有向上 signal/follow-through；到 292 的近障碍空间需精确重算 |
| `BQ1-TOL` | `short / open_bear_trend` | `L2-like conditional` | EMA20/50/200 均向下；8月末后 A 下跌，第一次到约 40 后反弹至 44，再次向下像第二次尝试 | 40–41 是近端支撑；44–46 是反弹阻力 | `deep_reviewed / shortlist_rank=3` | 第一支撑较近，可能只有约 1R；需确认第一次/第二次尝试属于同一 lineage |
| `BQ1-ZS` | `short / open_bear_trend` | `L1/L2-like event-boundary` | EMA20/50/200 均向下；约 180 至 115 的 A 很强，反弹至 145 后再次走弱 | 145–150 是回调阻力，115–120 是第一明显支撑 | `event_boundary / shortlist_rank=4` | A 中有明显大跳空/重订，普通非事件与事件型必须分开；L1/L2计数仍 pending |
| `BQ1-DDOG` | `long / breakout-expansion` | `event-driven strong-A / wait-for-B` | 突破后连续上行很强，EMA20/50陡升；截止日只出现一根较大阴线，不足以证明受控 B | 200 左右是突破/支撑簇；上方没有近距离两年旧高，但价格已明显延伸 | `deferred_wait_for_B / shortlist_rank=5` | 跳空和重订明显；当前不是可冻结 H1，必须等待小K、犹豫和位置确认 |
| `BQ1-MCHP` | `long / late-bull-at-major-resistance` | `strong-A plus terminal/three-push watch` | EMA20/50 向上；最后几根连续上推且放量，但尚无受控 B | 85–90 对应两年主要高点/阻力 | `deferred_wait_for_B_or_rejection / shortlist_rank=6` | 当前更像趋势末端强推或第三推，而不是 H1；既不能追多，也不能因数到三直接做空 |
| `BQ1-RBLX` | `no_valid_direction / mature_range_edge` | `range-edge repeat-test / three-push-like` | EMA20/50上弯但EMA200近乎走平；局部从30上推后多次测试40–42 | 40–42是反复测试的区间上沿，45–47是更高两年阻力 | `range_edge_observation / shortlist_rank=7` | 第三推分隔和反向确认不足；强收在区间外应转 BOP，不应继续坚持反转 |
| `BQ1-NDAQ` | `no_valid_direction / transition-at-support` | `downward multi-push / range-edge-bottom watch` | 最近下跌 A 明显，但 EMA50 仍上行/走平，空头 L1/L2 硬闸门不完整 | 60附近是EMA200与左侧支撑；上方63–65为近阻力 | `range_edge_observation / shortlist_rank=8` | 更像下跌到支撑后的观察，而不是高质量追空；尚无可靠多头反转信号 |
| `BQ1-CBOE` | `no_valid_direction / bull-to-bear transition` | `late L1-like at support / no-trade` | EMA20/50 已向下，但长周期背景刚从上升转弱；局部下跌延续 | 190–195 是 EMA200 与两年支撑簇，200以上为近阻力 | `rejected_gate / support_too_close` | 追空第一障碍过近；做多又不满足 EMA20/50 向上 |
| `BQ1-COHR` | `no_valid_direction / broad transition` | `ordinary-A H1-like boundary` | 从29到45的上涨较慢、重叠较多；EMA20向上，EMA50刚转上，EMA200仍平/下 | 40附近是EMA50/200簇，45和50是明显左侧阻力 | `rejected_gate / A_quality_and_resistance` | 不是用户偏好的3–4根饱满强A；父级仍是宽幅转换 |
| `BQ1-ROST` | `no_valid_direction / transition` | `rebound-pullback boundary` | 从123到143的反弹明显，但EMA50/200仍向下；当前回落K线偏大 | 140–145是EMA200和左侧阻力；125–130是下方支撑 | `rejected_gate / EMA_conflict` | 多空EMA闸门都不完整，不能把反弹强度单独当成多头A |
| `BQ1-TSLA` | `no_valid_direction / wide_range` | `H2-like shape inside range / no-trade` | 局部可画出上推、深回调和再尝试，但EMA20/50走平并互相缠绕 | 200–205支撑，220–230近阻力，260为主要高点 | `rejected_gate / range_middle_and_flat_EMA` | 计数容易因父级区间与深B重置；不能因局部外形升级成高质量H2 |

## 三、批次级发现结果

```text
batch_size: 12
deep_review_priority: 4
deferred_wait_for_structure: 2
range_edge_observation: 2
rejected_gate: 4
ordinary_non_event_status: unverified
event_boundary_visible: DDOG / ZS; MCHP possible but unverified
strict_H1_H2_L1_L2_freeze: pending
three_push_variant_freeze: pending
expert_adjudication: pending
trade_state: not_authorized
```

这次固定历史 symbol 池内的确定性截止日基线没有被要求一定含有 H1/H2/L1/L2 或三推正例，也不代表全市场自然发生率。`VEEV/MAR/TOL` 只是最值得继续深审的视觉候选；`DDOG/MCHP` 证明强 A 发现与可入场 H/L 必须分开；`RBLX/NDAQ` 提供区间边缘/多推观察；其余四张用于检查是否会为了凑数量而误选。

## 四、后续一致率与胜率必须分开

专家裁决前不计算“识别准确率”。裁决后只比较以下事前字段：父级、方向、是否存在强/普通 A、B 是否受控、H/L-like 或三推-like 候选、位置、EMA闸门、处置和主要否决原因。

交易结果另立冻结合同后才可计算；视觉一致不等于盈利，盈利也不能把错误标签改成正确识别。本批保持：

```text
conclusion: no-new-positive
validated win-rate: not-computable
```

本批只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

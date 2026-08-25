# 趋势后段入场与追价过滤

文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)。

这不是新的 K 线形态，而是所有 PA pattern 共用的时机与空间过滤层。它回答：趋势可能继续时，当前价格是否仍值得新增仓位；如果不值得，应该等回调、改成突破接受合同，还是观望。

## 1. 最小定义

趋势后段不是由固定根数或固定百分比定义。完整图表上，以下证据越集中，越应提高“后段/追价风险”的权重：

- 趋势已经离开最近一次合理回调较远；
- 连续大实体、跳空或收盘靠极值，价格明显远离均线和结构回调区；
- 价格接近主要高点/低点、区间边缘、通道边界或 MM 目标；
- K 线重叠增加、实体变小、跟随减弱，或出现最后一段扩张/高潮；
- 新交易的结构止损较远，而第一独立障碍很近；
- 交易动机变成“怕错过”，而不是新的结构和订单合同。

趋势很强不等于当前价格值得追。强度、位置、空间和订单时序必须分开。

## 2. 四种状态

| 状态 | 视觉特征 | 默认处理 |
| --- | --- | --- |
| `early-or-mid-controlled-pullback` | 强 A 仍有跟随，回调回到结构位，H1/H2 或 L1/L2 在同一回调 lineage 内重新出现 | 研究 stop/确认；冻结结构止损和第一障碍 |
| `late-but-controlled-pullback` | 趋势已运行较远，但回调仍短/受控，卖方没有连续跟随，位置和空间仍合理 | 可以保留条件候选；不能因为“晚”就自动否决，也不能无条件追 |
| `late-expansion-or-climax-risk` | 连续扩张、跳空、远离均线/目标、实体放大或到目标后减速 | 不追极端；等两腿回调、二次入场、小区间或明确接受 |
| `breakout-acceptance` | 主要阻力/支撑被强收盘越过，有跟随，回测守住新角色 | 旧合同结束，重新建立 BOP/回踩合同并重算成交、止损、首障碍和 R/R |

另设 `late-no-space`：方向判断可能正确，但首障碍不足约 1R、结构止损过宽、事件/跳空改变成交，或父级在区间中部。此时 `observation_only / valid_no_trade` 是完整输出，不是漏判。

## 3. 视觉顺序

```text
父级背景与左侧结构
→ 趋势运行阶段与最后一段压力
→ 是否接近主要磁铁/第一独立障碍
→ 是否有新的受控回调与 H/L 二次入场
→ 是否出现突破接受与跟随
→ 订单、结构止损、实际成交和路径 R/R
→ 追入、等回调、改 BOP、减仓或观望
```

不能从“最后一根 K 很强”直接跳到“必须追”。强 K 可能是趋势延续开始、后段高潮、突破尝试或区间最后一次扩张。

## 4. 四个交易分支

### A. 等回调或二次入场

这是后段最优先的分支：

1. 等价格回到 EMA、前高/前低、突破区、通道边界或其他结构区；
2. 判断回调是受控还是反向压力已经扩张并接受新结构；
3. 在同一回调 lineage 内重新数 H1/H2 或 L1/L2；
4. 确认信号 K、订单触发和结构止损；
5. 重新审计第一障碍和空间。

如果回调已经演变成成熟交易区间，不再强行继承旧趋势腿，也不把区间中部小突破叫成新的 ABC。

### B. 低周期确认

Daily/4H 已经提供方向和位置，但高周期信号 K 太大或入场过晚时，1H/15m 可以改善时序。低周期不能改变高周期父级止损和首障碍；若采用低周期窄止损，必须另立独立合同，不得用它凭空制造高周期 R/R。

### C. 突破接受后的新合同

主要阻力被强收盘越过，并有跟随或回测守住时，市场状态可以由“阻力前观望”切换为 `breakout-acceptance`。此时：

- 用新的实际成交价；
- 重新计算结构止损、第一障碍和目标；
- 可研究收盘、stop 或 limit-retest，但订单类型必须单独记录；
- 不能把原来阻力下没有空间的交易事后改写成“本来就应该追”；
- 等回调可能错过，是机会成本，不是旧合同的错误。

### D. 观望与管理

以下任何一项都足以把新增仓位降为观察：

- 最后一根趋势 K 已进入主要高低点、区间边缘或 MM 目标区；
- 第一障碍太近，或结构止损必须压入正常波动；
- 只有一根孤立大 K，没有跟随/接受；
- 价格连续扩张后出现重叠、上影/下影和跟随失败；
- 财报前三个交易日、重大事件、跳空或板块/市场背景使普通几何失真；
- 高周期在区间中部，低周期扩张只是局部噪音。

已有仓位与新增仓位必须分开：已有盈利仓可在目标/障碍区分批减仓，不能因为不想错过延伸而全仓等待精确 MM；新增仓位要有新的合同和新的 R/R。

## 5. 止损、目标与交易类型

后段追价最常见的错误，是用信号 K 的局部极值做过窄止损。研究时至少分别记录：

- `parent_structural_stop`：趋势、回调或突破 thesis 真正失效的位置；
- `low_cycle_stop`：明确独立的 1H/15m 短线合同才可使用；
- `profit_protection_stop`：形成新结构、减仓后才讨论，不是初始止损。

目标顺序仍为：第一独立障碍 → 角色转换/下一结构区 → MM 或更大延伸。后段越接近磁铁，越不能只看远端目标。进入目标区后若实体变小、重叠增加、冲高失败或通道成熟，可以分批止盈；MM 是区域，不是必须触及的精确点。

波段和短线不能在交易不顺时临时互换：波段允许较大回调，短线使用低周期结构和较近目标，但持有时间、仓位、止损与失效条件都要另写。一笔短线失效后，不能因为“大周期也许还会涨”就自动变成长线。

## 6. 与相邻 pattern 的边界

| 外形 | 不要直接叫成 | 先检查 |
| --- | --- | --- |
| 连续大趋势 K | 自动突破、自动高胜率入场 | 是否已经接近主要障碍/目标，是否有跟随 |
| 后段浅回调 | 自动新的 A 腿或新的 ABC | 是否仍是同一父级趋势，是否在同一回调 lineage |
| 主要阻力下的大阳线 | 自动必须追 | 收盘接受、跟随、回测和实际空间 |
| 趋势末端小平台 | 自动 Final Flag、圆顶或 MTR | 边界是否清楚，哪一边被接受/失败 |
| 低周期强推进 | 自动修复日线 R/R | 是否另立低周期合同，是否仍受高周期障碍约束 |

## 7. 统一复核字段

```text
timeframe:
parent_state:
trend_age_and_left_structure:
late_location_or_magnet:
last_push: continuation | climax-risk | accepted-breakout | mixed
pullback_available: yes | no
same_contract_or_new_contract:
signal_and_trigger:
order_branch: stop_confirmation | limit_retest | market_close | observation_only
branch_role: same_contract / role_reversal_retest / gap_reprice / management
actual_fill_assumption:
parent_structural_stop:
low_cycle_stop_if_independent:
first_independent_obstacle:
rough_R_R_to_first_obstacle:
event_sector_multitimeframe_gate:
management: hold | partial | protect | exit | rebuild
failure_condition:
final_state:
```

## 8. 证据入口

详细框架见 [`趋势后段入场视觉框架`](../../research/late_trend_entry_visual_framework_CN.md)，专项审计见 [`趋势后段入场视觉证据审计`](../../research/late_trend_entry_visual_evidence_gap_audit_2026-08-24_CN.md)。它们与 H1/L1、H2/L2、ABC、BOP、MTR、三推、通道和 Final Flag 交叉使用，但不把该过滤层变成新的 K 线 pattern。

本层只服务 PA Research 的视觉筛选与历史复核，不进入 Codex Trading，不创建量化扫描器，也不连接 Execution Agent。

# MTR 与三推/H3-L3 证据缺口审计：2026-08-23

状态：`visual-research / gap-audit / no-new-positive`

## 审计目标

本轮只寻找同时满足以下条件的新增案例：

- 无财报前三个交易 session 的污染；
- 三次推进/主要趋势反转的父级与 lineage 在当时可识别；
- 第三推有衰竭或主要位置证据，而不是单纯扩张；
- 有反向信号、第二次确认和跟随；
- 结构止损可放置，且第一独立障碍对实际订单仍有空间。

已有筛选日志见[`2025-08 至 2025-11 H3/L3 候选日志`](h3_l3_candidate_screen_2025-08_2025-11_CN.md)和[`2024–2026 L3 定向候选筛选`](h3_l3_candidate_screen_futu_targeted_2024_2026_CN.md)。本文件只汇总它们的缺口结论，不把结果倒灌成新交易样本。

## L3 / 三推新增候选审计

| 候选 | 形态为何值得看 | 否决点 | 当前结论 |
| --- | --- | --- | --- |
| BKNG 2026-07 | 三次回压逐步收窄，第三次后有多头反应，最接近 L3 衰竭 | `2026-07-17` 高点约 `184.36` 在触发方向上形成首障碍，空间不足约 `1R` | `pattern_like / valid_no_trade`，不是新增正向样本 |
| PM 2025-02–03 | 三次回压外形和第三次减弱较清楚 | 约 `145.78` 研究入场、`140.81` 结构风险、`150.38` 首障碍，粗略约 `0.93R` | `pattern_like / first-obstacle-borderline / valid_no_trade` |
| AMD 2024-10–11 | 第三次下探幅度收缩 | 母级仍偏空，信号没有持续接受，且 `2024-10-29` 财报切断普通 lineage | `continuation_or_failure / event-boundary / not-positive-L3` |
| GOOGL 2026-02–03 | 三次低点接近，第三点没有明显创新低 | 更像区间/过渡；`2026-02-04` 财报刚发生，首障碍也不宽 | `range-transition / count-ambiguous / valid_no_trade` |
| NKE 2024-06–07 | 数据形状提名第三次回压 | `2024-06-27` 财报跳空切断前后 lineage | `event-gap-boundary / not-admissible` |
| NOW 2025-10 | 高位区域反复测试 | 15m 只触碰触发而无跟随；IGV/QQQ 同期走强，板块不许可 | `pattern_like / valid_no_trade` |
| DELL 2025-11 | 高位三次测试外形存在 | 次日开盘跳过原 sell-stop，重订后首支撑拥挤 | `pattern_like / opening-skip / valid_no_trade` |
| WMT 2024-08–09 | 三个高点看似逐步上移 | 父级明显上行，属于强趋势延续，不是空头 H3 | `continuation-not-reversal / not-H3-short` |

这些案例补强了过滤边界，但没有一个同时通过“同一 lineage + 衰竭 + 二次确认 + 首障碍空间”。因此不能为了满足“找一个正例”而把 BKNG、PM 或 WMT 升级。

## MTR 新增候选审计

| 候选 | MTR 证据 | 否决点 |
| --- | --- | --- |
| TSLA 2024-03 | 区间上沿、强空头 A、弱 B、L1 后 L2；主要位置和反向结构值得研究 | 过程上结构止损先于远端支撑到达，属于 process-stop-first |
| NFLX 2024-08–09 | 高位多次测试、空头反向触发存在 | 首支撑拥挤，后来原顶部重新接受；不成为宽空间 MTR |
| ASML 2025-05–06 | 低位多次测试和支撑反应 | 更像区间过渡，缺少结构接受和第二次确认 |
| TSLA 2025-09 | 阻力下有反转假设 | `2025-09-11` 强收盘突破并接受，原 MTR thesis 转 BOP |

因此，本轮没有新的无事件、双向、二次确认清楚且首障碍宽裕的 MTR 正例。

## 正式结论

本轮结论是 `no-new-positive`，不是“L3 或 MTR 不存在”。当前保留：

- KLAC 2025-03：已有条件性 H3/熊旗顶部研究基准；
- TSLA 2024-03：已有 MTR candidate，但保留过程止损先失效边界；
- 其余样本作为首障碍、事件、区间、扩张、板块和订单反例。

下一次只在出现新的方向、订单合同或状态转换证据时补样本。重复同一类首障碍拥挤案例，不再进行深审。

## 边界

本审计使用 PA Research 已有的历史筛选和 Futu OpenD 收盘后记录，不声称完成全市场统计搜索；不创建量化扫描器，不修改 Codex Trading，也不连接 Execution Agent。

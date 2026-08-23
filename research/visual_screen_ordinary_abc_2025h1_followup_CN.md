# 2025 H1 普通 ABC 视觉复筛：成长股与半导体组

状态：`visual-screen / pattern-like-first / no-new-conditional-positive / event-state-boundary`

这是 PA Research 第一阶段的人工视觉复筛。目标是先看图形是否“像”普通 ABC、H1/H2 或 L1/L2，不是量化扫描、胜率统计或交易授权。只有视觉结构稳定的候选，才进入 60m/15m、订单、止损和首障碍审计。

## 证据边界

- 主要窗口：`2025-01-02`–`2025-06-30` Daily；
- 标的：`MSFT`、`AMZN`、`ORCL`、`CRM`、`BKNG`、`AVGO`、`LRCX`、`AMAT`、`CSCO`、`TXN`、`IBM`；
- 数据：Futu OpenD 历史 QFQ 收盘数据；本轮只读，不是实时行情；
- 图上的后续上涨或下跌只用来理解状态是否改变，不能倒灌成入场理由；
- 本轮没有为候选补低周期订单，也没有冻结精确 R/R。

## 视觉总表

| 标的 | 图上首先看到的外形 | 主要边界 | 当前处置 |
| --- | --- | --- | --- |
| `MSFT` | 年初下行后，4 月出现恢复并进入较强上涨段；局部可以画出 A—B—再推进 | 4 月的状态切换很明显，之后的 B 可能是新父级中的嵌套回调，不宜直接继承年初计数 | `pattern_like / state-transition / nested-lineage-unclear` |
| `AMZN` | 年初下跌，3 月低位后出现恢复；局部有多次上涨—回撤—再上涨 | 4 月附近的波动和缺口改变了状态，普通趋势 ABC 与过渡反转不能混写 | `pattern_like / transition-boundary / no-low-cycle-audit` |
| `ORCL` | 长时间整理/走弱后出现向上跳变，随后高位横向 | 向上跳变是重新定价，不是可直接复制的普通 A；B 尚未形成清楚的开放趋势 lineage | `pattern_like / event-gap-boundary / observation-only` |
| `CRM` | 大部分时间是下行后横向，局部有反弹和再回落 | 方向腿不够干净，反复重叠使 B 更像区间或过渡，而不是受控回调 | `boundary / range-transition / not-clean-ABC` |
| `BKNG` | 5 月至 7 月先有上行，随后出现明显下挫，再恢复到新高 | 大幅下挫/缺口造成状态重置；不能把恢复段直接当成原 A 后的 C 腿 | `pattern_like / gap-state-boundary` |
| `AVGO` | 4 月 9 日后出现很强的上行 A，之后短暂停顿并继续推进 | A 的起点来自冲击后的跳空和快速重新定价；它像强 A，但不是普通无事件 A | `pattern_like / event-driven-A / no-low-cycle-audit` |
| `LRCX` | 4 月 9 日后快速收复，随后出现方向性延续 | 与 AVGO 类似，冲击缺口、恢复腿和后续回调混在一起；不能直接冻结 H1/H2 | `pattern_like / event-driven-A / lineage-unclear` |
| `AMAT` | 4 月低位后的恢复和后续上行较明显 | 恢复前有剧烈冲击，局部回调尺度不稳定；先不当作普通 ABC | `pattern_like / transition-boundary` |
| `CSCO` | 4 月以后有恢复和上行，但夹杂多次暂停 | A/B 的边界不清，重叠较多；更适合做“总体方向对、计数不清”的训练图 | `pattern_like / ordinary-A-unclear` |
| `TXN` | 先下跌，再筑底，随后逐步恢复 | 父级从空头转为过渡，恢复腿不是开放趋势中的明确第二腿 | `boundary / transition-not-continuation` |
| `IBM` | 4 月附近先剧烈下挫，随后逐步修复并转强 | 冲击缺口和状态切换主导窗口；普通 A、B、C 不能直接连成一条线 | `pattern_like / event-gap-boundary` |

## 这轮视觉上真正学到的东西

### 1. “强 A”与“普通趋势 A”要先分开

`AVGO`、`LRCX` 和 `AMAT` 的方向腿视觉上很强，足以进入 `pattern_like` 候选；但强度来自冲击后的跳空和快速重新定价。它们可以训练“强 A 长什么样”，不能直接作为普通趋势 ABC 的正样本。

### 2. 状态切换会重置计数

如果价格从长期下跌/区间突然跳到新的价位，再连续推进，第一步应先问“市场状态是否已经换了”，而不是立即把它数成原结构的 H1、H2 或 C。只有状态稳定后形成的新回调，才重新开始计数。

### 3. 视觉助手第一阶段不需要精确数字

本轮只需要判断：

- 有没有方向明确的 A；
- B 是回调、区间中部摆动，还是状态转换；
- 触发附近是否已经贴着明显前高/前低；
- 是否值得放大到更低周期。

这一步的输出可以是 `pattern_like`、`边界` 或 `不属于开放趋势 ABC`。不需要为了得到一个 H2 标签而提前精确计算止损和 R/R。

## 裁决

本轮没有新增可以无争议升级为 `research_positive_conditional` 的普通 ABC/H1-H2/L1-L2 样本。新增价值是把“事件/缺口造成的强方向腿”与“普通开放趋势中的强 A”分开，避免视觉上很漂亮的图形污染普通样本。

下一轮继续优先使用已有的 `NFLX`、`TSM`、`CRWD`、`NVDA` 条件对照，并寻找没有大缺口、同一 lineage 清楚、B 后段受控的独立窗口；不把本轮的事件型候选直接推进低周期订单审计。


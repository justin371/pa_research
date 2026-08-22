# PA Pattern 视觉筛选协议 v0.1

日期：2026-08-23  
状态：`visual-first / research protocol / not quantitative`

## 这份协议解决什么问题

PA Research 的第一阶段任务，是让助手从完整图表里筛出“看起来像”的 Price Action pattern。它不是扫描器，也不是胜率模型。第一轮不需要精确价格、固定阈值、完整 15m 触发或精确 R/R；这些内容只在候选值得深入时再补。

核心顺序：

```text
完整图表背景
    → 视觉上是否像某个 pattern
    → 记录候选与不确定点
    → 只挑少量候选优化订单/止损/目标
    → 形成可复核研究样本
```

## 1. 第一轮：只做视觉筛选

第一轮要回答的是“像不像”，不是“能不能下单”。至少记录：

```text
symbol:
review_window:
timeframe_seen:
data_status: historical / delayed / live-confirmed / incomplete
chart_scope: full / partial
market_state: trend / trading_range / transition / climax / unclear
directional_bias: bull / bear / balanced / changing
pattern_candidate: ABC-CONT / H1-H2-H3 / L1-L2-L3 / range-edge / MTR / other
parent_leg:
local_A_B_C_or_attempts:
visual_reason:
main_uncertainty:
stage_1_status: pattern_like / boundary / not_this_pattern / pending
```

### 第一轮可以使用的证据

- 左侧是否有清楚的趋势、交易区间、过渡或高潮背景；
- 是否能看见一条方向性 A 腿，随后出现回调或反向尝试；
- B 是趋势回调，还是区间中部的双向摆动；
- C 或 H/L 尝试是否发生在有意义的支撑/阻力、EMA、缺口、通道边界附近；
- 价格行为是否有明显的买压/卖压变化，例如方向性实体、重叠、尾巴和跟随；
- 是否存在母腿与局部腿嵌套，不能因为窗口短就强行把局部腿当成独立 ABC。

### 第一轮不要求的内容

- 不要求精确到某个固定百分比；
- 不要求先确定唯一的 A 腿锚点；有歧义时可保留早锚点/晚锚点；
- 不要求先算出精确的 measured move、AB=CD 或 1R/2R；
- 不要求先判断最终是否盈利；
- 不要求先把每个 H1/H2/H3 或 L1/L2/L3 计数冻结；计数不清可以写 `unclear`；
- 不因为价格碰到 EMA 就单独创建 pattern；
- 不把后面的大涨/大跌倒灌成前面“本来就明显”。

## 2. 第一轮的三类输出

### `pattern_like`

图形的背景、方向腿和回调/尝试已经足以值得继续看，但订单、首个障碍或计数还没有审计。这个状态是正常的第一阶段成果，不代表入场。

### `boundary`

局部形状有些像，但存在会改变解释的边界，例如：

- 父级可能是交易区间而不是趋势；
- A 腿普通、过宽或不够方向性；
- B 反向压力扩张，可能已经形成新趋势；
- H3/L3 与三推楔形、区间二次测试混在一起；
- 事件跳空改变了原来的价格行为；
- 母腿和局部腿有多个合理尺度。

边界样本要保留。它们帮助助手学会“不确定时如何说”，不能为了得到正例而删除。

### `not_this_pattern`

图形主要是区间中部摆动、没有方向性 A 腿、计数已被新结构重置，或它明显属于另一个逻辑。此时不强行贴 ABC/H1/H2 标签；如果另一个 pattern 更合适，可另建候选。

## 3. 第二轮：只优化值得深入的候选

当第一轮标为 `pattern_like`，或者边界样本对某个规则特别有学习价值时，才进入第二轮：

```text
signal_bar / confirmation_bar:
order_branch: stop / limit-retest / market-close / observation-only
trigger_zone:
structural_stop_zone:
first_independent_obstacle:
rough_space: clearly_positive / borderline / blocked / unknown
measured_move_or_AB_CD:
event_filter:
sector_or_market_context:
stage_2_status: research_ready / valid_no_trade / research_positive_conditional / pending
```

第二轮仍然是人工研究，不是自动下单授权。第一障碍优先于 MM；结构止损不能为了改善 R/R 而任意缩窄。窄低周期止损和宽日线止损代表不同交易假设，不能混成一个结论。

## 4. 视觉筛选的统一判断顺序

### 多头 ABC / H1-H2-H3

1. 左侧是不是开放上涨趋势、趋势恢复，还是区间/过渡；
2. A 腿是否有方向性；强 A 只提高先看 H1 的优先级，普通 A 通常先观察 H2；
3. B 中卖压是否受控，后段是否在支撑或均线附近收缩；
4. 当前是第一次、第二次还是第三次有意义的多头尝试；
5. 第三次尝试不自动等于三推楔形反转，可能仍是延续；
6. 候选值得深入后，再看信号 K、订单、止损和第一阻力。

### 空头 ABC / L1-L2-L3

1. 左侧是不是开放下跌趋势、趋势恢复，还是区间/过渡；
2. A 腿是否有方向性；优先找连续阴线、收盘靠低位、重叠较少的清楚下跌；
3. B 中买压是否逐渐减弱，是否被前支撑转阻力、均线或主要高点压回；
4. 当前是第一次、第二次还是第三次有意义的空头尝试；
5. 第三次尝试不自动等于三推楔形反转，强度扩张时更可能是延续或高潮风险；
6. 候选值得深入后，再看信号 K、订单、止损和第一支撑。

## 5. 与现有研究文件的关系

- [`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)：逐图完整审计卡；
- [`ABC 视觉研究阶段性综合`](abc_visual_synthesis_v0_2_CN.md)：跨案例共性与边界；
- [`ABC 决策矩阵`](abc_decision_matrix_CN.md)：案例比较；
- [`Pattern inventory`](../strategy/pattern_inventory_candidates.md)：候选目录。

本协议只规定“先筛像不像，再决定是否优化”的入口，不替代上述文件里的订单、止损、首障碍和事件过滤规则。

## 6. 当前明确边界

- `pattern_like` 不是胜率，也不是买卖建议；
- `research_positive_conditional` 不是已验证策略；
- 研究阶段可以保留模糊候选，不为了精确而假装确定；
- 形态研究和量化实现分开。只有规则、例外、失败样本和研究证据足够成熟，才考虑移交 Codex Trading；
- Codex Trading 目前仍是只读参考库，PA Research 是本阶段唯一更新的研究库；
- 历史或收盘数据不能描述成实时行情；实时数据若未验证来源，直接标为未知。


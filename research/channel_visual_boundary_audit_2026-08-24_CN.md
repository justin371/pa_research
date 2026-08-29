# Channel / 通道视觉边界复核

日期：`2026-08-24`  
状态：`visual-research / provisional / not-statistical`

这份复核只研究完整图表中的通道识别与状态切换。它不是趋势线画法教程，也不是量化扫描规则。通道必须先作为一个父级市场状态被当时的证据支持，然后才允许在边界上研究 H/L、突破、回测或反向交易。

## 1. 决策时点的最小定义

```text
先判 parent_state
→ 找到同向推进与回调的 lineage
→ 检查上/下边界是否大致平行、是否多次被测试
→ 区分 tight channel / broad channel / trendline candidate / range
→ 再看边界反应、H1/H2/L1/L2、BOP 或 MTR
→ 冻结订单、结构止损、第一独立障碍和 no-trade
```

### 1.1 两点连线不是成熟通道

- 两个高点或两个低点只足以形成 `trendline_candidate`；没有另一侧边界、第三次反应或平行关系，不能称为已经确认的通道。
- 一根大 K、一次跳空或一次强趋势推进不是通道证据，只能先记为强 A、重新定价或 BOP 候选。
- 后见之明中可以画出漂亮平行线，不代表当时已经可以用这条线下单。
- 如果价格在水平边界之间反复穿越中线，优先使用交易区间逻辑；不要把区间摆动重新命名为宽通道，也不要继承旧 ABC 腿数。

### 1.2 紧通道

紧通道的视觉证据包括：

- 单方向压力持续，回调浅，重叠少；
- 收盘经常靠趋势方向一侧，反向尝试很快失去跟随；
- 多次推进仍保持相似的坡度，而不是每一推都明显扩张；
- 边界附近的第一次反应更可能是顺势恢复，而不是自动反向。

紧通道不等于“任何位置都能追”。越接近主要高点/低点、通道末端、事件窗口或第一独立障碍，越要降低追价优先级。回调变深、重叠增多、反向价格被接受时，紧通道状态应降级为 `transition`，而不是继续套用紧通道惯性。

### 1.3 宽通道

宽通道仍有坡度，但回调深、重叠多、上下沿反复测试。它通常更接近宽旗形、宽幅趋势或逐步转区间的状态。

- 上沿、下沿和中线有不同交易含义；中部通常只观察；
- 边界上的 H2/L2 先标为边缘反应，不能自动当作开放趋势的第二次入场；
- 三次测试若范围越来越宽，优先记录为 `expansion / continuation-risk`，不改写成逐推减弱的三推楔形；
- 边界趋平、双方频繁穿越中线后，旧通道结束，转用区间边缘合同。

## 2. 状态机与失效条件

| 状态 | 当时可见证据 | 下一步 | 不能做的事 |
| --- | --- | --- | --- |
| `tight-channel-continuation` | 浅回调、少重叠、同向跟随、边界未失效 | 顺势回调恢复，研究 H1/L1 或位置良好的 H2/L2 | 不在末端/首障碍前机械追价 |
| `broad-channel-edge` | 多次边界反应、仍有坡度、边缘出现拒绝或恢复 | 边缘顺势、观察或等待第二次确认 | 不在中部把局部波动数成 ABC |
| `channel-line-candidate` | 只有一侧两点或一次趋势线反应 | 等另一侧结构和后续测试 | 不把线当自动订单触发 |
| `channel-end-expansion` | 末端推进变宽、第三/第四次测试更强 | 观察延续、高潮、小反转或新平衡 | 不因次数达到三就宣布衰竭反转 |
| `channel-break-failure` | 越界后没有跟随，价格回到原通道 | 失败突破观察；等待反向二次确认 | 不凭一根刺破直接做 MTR |
| `channel-breakout-acceptance` | 强收盘离开边界、跟随、旧边界回测守住 | 改用 BOP/新趋势合同 | 不继续沿用旧通道反向假设 |
| `channel-to-range-transition` | 边界水平化、双方反复、中线穿越频繁 | 改用区间边缘；中部观望 | 不继承原趋势腿数 |

通道被破坏只说明原状态受到挑战。要升级为主要趋势反转，还需要反向压力、结构破坏、第二次确认和足够空间；要升级为 BOP，则需要边界外接受、跟随和回测证据。

## 3. 通道与 H/L、ABC、三推的边界

### 紧通道中的顺势 H/L

紧通道里，浅回调快速恢复可以作为 H1/L1-like 候选；若第一次尝试失败且回调仍属于同一 lineage，再观察 H2/L2。信号 K 必须有方向性、位置合理、结构止损可放置，且第一独立障碍不能把空间压缩到约 `1R` 以下。

### 宽通道中的 H/L

宽通道边缘出现两次反应，不自动等于开放趋势 H2/L2。先回答它属于哪一种：

1. 边缘顺势恢复；
2. 边界失败后的反向尝试；
3. 突破后的旧位回测；
4. 区间边缘的第二次机会。

若价格已在中线附近来回穿越，局部的 H/L 只记为 `observation`。区间中的 second-leg trap 不能被通道标签掩盖。

### ABC 与三推

- 强 A 后的受控 B 可以保留 ABC 研究；当 B 变成宽幅、重叠多、反复穿越时，降级为宽通道或区间过渡。
- 三次边界测试不等于三推楔形。第三次收缩、压力衰竭和反向跟随，必须与第三次扩张、通道延续分开。
- 通道中出现的反向第一次压力只说明状态变化候选，不自动授权 MTR；若原方向重新接受边界外，旧 MTR 假设失效。

## 4. 订单合同

| 合同 | 适用条件 | 关键限制 |
| --- | --- | --- |
| `stop-confirmation` | 边缘出现优质信号 K，或边界外收盘等待跟随 | 触发价、结构止损和实际成交必须在当时冻结 |
| `limit-retest` | 旧边界已完成角色转换，等待回测到预设区域 | 未回测不算成交；不能用后来触碰倒灌成交 |
| `market/close-confirmation` | 通道外强收盘、跟随已出现且错过回测 | 接受更宽结构风险；第一障碍太近就不追 |
| `reverse-after-failure` | 边界失败、回到原侧、反向 H/L 与第二次确认出现 | 一次影线刺破不够；需要新的反向合同 |
| `observation-only` | 中部、线未确认、扩张不清、首障碍拥挤或事件临近 | `valid_no_trade` 是正确输出 |

结构止损放在能破坏 thesis 的位置：紧通道顺势单放在最近有意义回调/通道结构外；宽通道边缘单放在边界和最后一次测试极端外；反向单放在边界失败和主要测试极端外。不能把止损压到单根小 K 内部来制造虚假 R/R。

目标顺序固定为：

1. 入场前已知的第一独立支撑/阻力；
2. 通道中线、另一侧边界或最近可见磁铁；
3. 结构被接受后，再看 MM、AB=CD 或通道扩展。

MM 是目标区域，不是把前方阻力抹掉的理由。若第一障碍不足约 `1R`，即使通道方向后来正确，也记录为 `valid_no_trade`；完整波段接近 `2R` 只是研究参考，不是固定胜率承诺。

## 5. 案例裁决

### 5.1 TSLA `2025-08-20–08-22`：保留一个紧趋势延续候选，但不虚构成熟通道

`2025-08-20–08-22` 买方推进强，回调浅，低周期越过 `2025-08-21` 高点约 `324.90`，可保留为 `tight-trend-continuation / low-cycle-conditional`。若研究 buy stop 约 `326.65`、结构止损约 `318.68` 下方，第一阻力约 `340.55`，低周期空间约 `1.7R`。

但是 `2025-07-21` 与 `2025-08-11` 只有上方高点连线候选，没有决策时已经确认的平行下边界。因此它是本轮“紧趋势延续”候选，不是成熟通道正例。若日线已经靠近 `340` 主要阻力，低周期合同也不能替代日线空间。

### 5.2 KLAC `2025-03-17–03-26`：宽熊旗上沿的条件性顺势边缘

父级 `2025-02-20–03-11` 偏空，`2025-03-17/19/24` 多次上探 `71.78/72.36/72.87`，更适合宽熊旗/宽熊通道上沿。`03-25` 低点下方 sell stop、`03-26` 低周期触发，结构止损约 `74.50` 上方，第一管理区约 `66.6–65.1`，粗略约 `1.4R–1.9R`。

它支持“宽通道上沿顺势做空”的条件分支，不支持中部追空，也不证明第三推必然反转。第三次测试仍有扩张因素，所以保持 `research-positive-conditional`。

### 5.3 XOM `2024-07-25–08-02`：宽通道扩张不是衰竭证明

`07-25/30/31` 三次上探 `109.82/110.34/111.43`，第三次范围扩大而不是收缩；`08-01` 的空头反应被 `08-02` 跳空重新定价。结构止损约 `111.43–111.60` 上方，第一支撑约 `105.20`，理想触发约只有 `1R`，实际跳空成交约 `0.7R`。

结论是 `broad-channel/flag-expansion / valid_no_trade`：扩张与后续下跌可以同时存在，但不能事后把扩张改写成衰竭三推；跳空后的实际成交必须重新签订合同。

### 5.4 UBER `2024-07-17–07-26`：通道扩张、计数歧义与首支撑拥挤

强空头 A 后出现多个上探，`07-23` 可以先记 H3-like；但 `07-25` 又向上扩张到约 `69.37`，使第三/第四次计数变得含混。`07-25/26` 的 L2-like 方向虽然有板块许可，但第一支撑约 `62.90–63.30`，粗略只有 `0.20–0.27R`，所以是 `valid_no_trade`。

这说明“计数像、通道有坡度、方向正确”仍不足以交易；扩张、订单质量和首障碍必须同时通过。

### 5.5 ASML `2025-05-23–06-11`：区间过渡，不是通道内第三推

两个下沿测试接近 `715–718`，中间重叠和横向平衡明显，后段向上扩张。更准确的读法是“深回撤 → 下沿二次测试/双底样结构 → 区间过渡 → 向上扩张”，而不是三次逐步衰竭的空头通道。低周期小摆动不能拼成高周期第三推。

## 6. 当前可复用输出

```text
contract_scope: historical_context_only
primary_pattern: other
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
channel_type: tight / broad / trendline_candidate / none / unclear
channel_status: candidate / confirmed / broken / rejected
direction: long / short / no_valid_direction
direction_and_pressure:
upper_boundary / lower_boundary / midline
boundary_test_count_and_expansion_or_contraction
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
signal_bar:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
structural_stop:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
handoff_status: research_only / not_ready / ready_for_system
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

本轮结论：保留 TSLA 作为紧趋势延续候选，KLAC 作为宽通道边缘条件候选，XOM/UBER 作为扩张与首障碍否决，ASML 作为区间过渡反例。当前仍没有事件干净、两侧平行边界确认、首障碍宽裕且路径完整的成熟通道正例，因此 Channel 保持 `provisional`，不建立固定胜率规则。

本文件只服务 PA Research 的视觉判断、案例复核和订单语义；不创建量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

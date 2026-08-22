# 常用高质量候选形态清单 V0.1

状态：研究候选；尚未证明“高胜率”，尚未进入生产规则或程序化回测。

本文件的目标是先建立形态目录，不急着把任何一个形态包装成自动交易系统。三推楔形本轮暂停，保留已有候选文件，但不在本清单中继续扩展。

## 1. 先统一几个名字

### H1/H2/H3 与 L1/L2/L3

本项目先采用 Price Action 的操作性语言：

| 标签 | 含义 |
| --- | --- |
| H1 | 多头背景中，回调结束后的第一次向上尝试 |
| H2 | 第一次向上尝试失败或回调再走一腿后的第二次向上尝试 |
| H3 | 第三次向上尝试；常提示复杂回调、迟到的延续或压力变化 |
| L1 | 空头背景中，回调结束后的第一次向下尝试 |
| L2 | 第一次向下尝试失败或反弹再走一腿后的第二次向下尝试 |
| L3 | 第三次向下尝试；常提示复杂回调、迟到的延续或压力变化 |

H2/L2 往往比第一次尝试更值得优先研究，但这不是无条件的胜率结论。H3/L3 也不是“三推楔形”的同义词，本轮不对三推做进一步研究。

参考库中的扫描器还使用 H1/H2/H3、L1/L2/L3 表示“冲量之后的一、二、三条逆趋势腿”的描述性 proxy。这个 proxy 只能帮助召回样本，不能替代因果的信号、触发、止损和空间判断。

### ABC 与几何 AB=CD 不是同一套字母

- **本项目的 ABC**：A 是第一条方向腿，B 是回调，C 是原方向恢复；它是 Price Action 的操作性结构标签，不依赖外部波段体系。
- **几何 AB=CD**：A→B 是第一段方向腿，C 是回调后的第二段起点，D 是从 C 投影出的目标；它描述价格距离。

以后案例中分别记录 `A_leg/B_pullback/C_resumption` 和 `measure_A/B/C/D`，避免把结构标签和测量锚点混为一谈。

## 2. 什么才算“高质量候选”

“高胜率”暂时只作为研究目标。一个形态至少要同时检查：

1. **背景**：趋势、区间、转换或高潮是否清楚；
2. **位置**：前高/前低、结构区、突破区、通道边界或其他可事先看到的磁铁；
3. **形态**：A 腿、B 回调、C 恢复和 H/L 尝试次数能否按当时已完成的 K 线定义；
4. **触发**：信号 K 线、下一根确认和执行价格是否事先冻结；
5. **空间**：第一独立障碍、AB=CD 或 measured move 目标是否给出足够空间；
6. **风险**：结构止损、跳空、成本和失效条件是否明确。

只看到一个 H2、一个 ABC、一个比例或一根漂亮的 K 线，不能单独称为高质量交易机会。

## 3. 第一批优先研究的候选

| 优先级 | ID | 候选形态 | 结构定义 | 研究触发 | 测量/目标 | 主要失效 |
| --- | --- | --- | --- | --- | --- | --- |
| A | `TPB-H2-L2` | 强趋势中的二次入场 | 方向性 A 腿之后，B 回调出现两次有意义的反向尝试；多头看 H2，空头看 L2 | 关键支撑/阻力被触及并守住；信号 K 后由下一根 K 线确认方向 | 前一腿等距、AB=CD 或下一道结构磁铁；先看第一障碍 | 区间中部、回调已接受反向结构、没有跟随、障碍太近 |
| A | `ABC-CONT` | 强趋势 ABC 延续 | A 是可见的方向腿，B 是受控回调，C 恢复原方向；B 尚未演化成双向交易区间 | C 在结构位置形成方向性信号并得到确认 | `Leg1 = Leg2`、AB=CD、或 A 腿终点后的下一个独立磁铁 | A 其实是高潮/区间内脉冲；B 过度重叠；C 未恢复或重新跌回区间 |
| A | `BOP-ABC` | 突破后的 ABC 回踩 | 先有被接受的突破，随后 B 回踩突破区，C 再次离开突破区 | 多头回踩守住旧高上方、空头守住旧低下方，并出现重新突破/确认 | 突破前区间高度、A 腿等距、下一道结构障碍 | 收盘重新接受回旧区间；突破没有跟随；回踩变成失败突破 |
| A | `RFB-SECOND` | 区间边缘失败突破后的二次入场 | 价格在已知区间边缘刺破后重新进入区间；反向尝试再次失败 | 区间边缘重新收回后，出现方向一致的 H2/L2 或等价确认 | 区间边缘、区间高度和中点是目标参考，不预设一定到达 | 发生在区间中部；重新进入后没有跟随；区间边缘未被事先确认 |
| A | `MTR-ABC` | 主要位置上的反转 ABC | 成熟趋势/通道出现 A-B-C 反转结构，同时有双顶/双底、趋势线破坏或失败突破证据 | 第二次反向尝试突破信号 K，并在结构失效点外设止损 | 先看最近磁铁，再看 AB=CD 或 measured move；目标是区域而非单点 | 只是趋势中的普通回调；反向突破没有接受；止损空间过大 |
| B | `TPB-H1-L1` | 强趋势中的第一次尝试 | A 腿强、B 浅或以时间整理为主，第一次恢复就形成 H1/L1 | 位置、信号 K 和跟随质量都很强时才保留 | 以前一腿或下一道障碍为主；避免追在大腿末端 | A 腿不强、B 很深、H1 太晚、第一障碍太近 |
| B | `H3-L3-COMPLEX` | 第三次尝试/复杂回调 | 前两次恢复未能离开区域，第三次才出现方向尝试 | 只作观察样本；需更严格的结构、空间和跟随确认 | 可记录等距投影，但不能把 MM 当作反转证明 | 计数重置不清、区间中部、三推/楔形解释混入；本轮暂缓 |

### 当前优先顺序

先研究 `TPB-H2-L2`、`ABC-CONT` 和 `BOP-ABC`。它们最容易把用户已有的 H1/H2、ABC、左侧支撑/阻力和 MM 观察写成可复核字段。`TPB-H1-L1` 作为对照组；`H3-L3-COMPLEX` 先留在目录中，不作为本轮工作主线。

## 4. AB=CD 与 measured move：测量层，不是独立形态

### 5.1 方向腿等距

先冻结第一段 A→B 和回调终点 C，再投影第二段：

```text
多头目标 D = C + (B - A)
空头目标 D = C - (A - B)
```

允许记录“接近等距”“明显扩展”“明显不足”，不要为了得到漂亮的 1:1 而事后移动锚点。AB=CD 到位通常意味着第一目标或获利/停顿区域，不自动意味着反转。

### 5.2 其他常用 measured move

- **Leg 1 = Leg 2**：第一条方向腿、回调、第二条方向腿；常用于 ABC 延续；
- **Trading-range height**：突破区间后投影区间高度；
- **Breakout height / measuring gap**：从被接受的突破结构投影；
- **既有结构磁铁**：前高、前低、区间边缘、通道边界；它们优先于一个孤立的数学目标。

每个目标都要记录 `target_type`、锚点、计算时点、附近障碍和到达后的价格反应。测量目标是空间与管理工具，不是买卖方向的充分条件。

## 5. 每个案例统一记录的字段

```text
symbol
timeframe
market_state              # trend / range / transition / climax
direction
A_leg_origin / A_leg_end
B_correction_start / B_correction_end
B_leg_count
abc_mode                   # continuation / reversal / complex / unknown
H_or_L_attempt             # H1 / H2 / H3 / L1 / L2 / L3
location_and_left_structure
signal_bar / confirmation_bar
AB_equals_CD               # absent / approximate / present / unknown
measured_move_type
first_obstacle
structural_stop
invalidation
outcome                    # continuation / reversal / failure / no-trade / pending
evidence_status             # descriptive / research-candidate / replayed / validated
```

## 6. 研究边界与下一步

- 本文件不声称任何固定胜率；胜率必须来自预先定义、跨标的、按时间切分的回放或回测。
- `H1/H2/H3`、`L1/L2/L3`、操作性 ABC、AB=CD 和 measured move 先分栏记录，不能压成一个分数。
- 先从 `TPB-H2-L2`、`ABC-CONT`、`BOP-ABC` 各挑代表性多空案例，做因果标注；再决定哪些值得程序化。
- 三推楔形保持暂停，不把 `H3-L3-COMPLEX` 偷换成三推反转规则。
- 任何候选要进入交易系统，还必须通过现有市场许可、15 分钟触发、结构止损、第一障碍、成本和审计门槛。

## 参考资料

- [Al Brooks — Bar Counting: High and Low 1, 2, 3, and 4 Patterns and ABC Corrections](https://www.oreilly.com/library/view/trading-price-action/9781118172339/OEBPS/9781118172339_epub_c_17.htm)
- [Al Brooks — Measured Moves Based on the Size of the First Leg](https://www.oreilly.com/library/view/trading-price-action/9781118172339/OEBPS/9781118172339_epub_c_07.htm)
- [Brooks Trading Course — Price Action Trading Terms Glossary](https://www.brookstradingcourse.com/price-action-trading-terms-glossary/)
- [Codex Trading — Pullback and leg definitions](https://github.com/justin371/codex-trading/blob/main/docs/pullback-leg-patterns_CN.md)
- [Codex Trading — ABC continuation research contract](https://github.com/justin371/codex-trading/blob/main/research/abc-continuation-tpb-hypothesis_CN.md)
- [Codex Trading — H1/H2 and measured-move review](https://github.com/justin371/codex-trading/blob/main/research/klac-daily-high1-high2-mm-20260816_CN.md)

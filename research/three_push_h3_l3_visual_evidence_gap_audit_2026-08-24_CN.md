# 三推 / H3-L3 视觉证据缺口审计（2026-08-24）

日期：2026-08-24  
状态：`visual-research / conditional / no-new-positive / validated win-rate: not-computable / not-statistical`

本文件是跨案例的历史视觉审计，不是单一标的的完整订单合同。链接案例的日期、来源、周期和
`data_status` 以各自记录为准；本文件不提供当前行情，也不把聚合表中的自然语言直接当作统一字段。
案例进入深审时使用以下 canonical 轴：

```text
contract_scope: historical_context_only
direction: long / short / no_valid_direction
lineage_status: same_lineage / reset / unclear / pending
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
gap_policy: accept_open / skip / flag_only / not_applicable
structural_stop:
first_independent_obstacle:
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

`research_positive_candidate`、`same-lineage`、`range-repeat`、`expansion-or-climax`、
`first-obstacle-crowded` 和 `gap-reprice` 在本文件中仅保留为历史说明别名；新记录分别映射到
`research_positive_conditional`、`same_lineage`/`pending`、`range_repeat_test`、
`continuation_or_climax`、`space_status` 和 `branch_role: gap_reprice`。若没有独立触发、结构止损和
首障碍空间，不能从这些别名推导交易授权或胜率分母。

## 1. 本轮核心问题

三推不是一个自动反转信号。它首先回答：同一父级、同一 lineage 中，第三次有意义的推进或测试，压力是在减弱、扩张、区间重复，还是通道延续？只有当第三推状态、主要位置、反向二次确认、首障碍和订单合同同时成立，才有资格进入 H3/L3 或 MTR 研究。

本轮特别把两套计数分开：

- `H3/L3`：原方向在同一回调/压力中的第三次有意义尝试；
- 反向 `H1/H2` 或 `L1/L2`：第三推之后，反方向的第一次和第二次确认。

“原方向第三次”与“反方向第二次”不是同一个数字，不能把 H3/L3 直接写成三推楔形反转。

## 2. 先过 lineage 闸门

### 可以保留为同一组三推

- 父级仍是同一趋势、同一压力区或同一回调结构；
- 每次推进之间有可见停顿、回调或失败尝试；
- 三次尝试在同一主周期上可见，低周期只补确认；
- 前两次在当时已经有意义，不是事后挑出的局部影线。

### 必须重置或降级

- 价格已进入成熟双向交易区间，局部腿失去趋势延续性；
- 区间边界被接受后建立了新的母级方向；
- 只有低周期才能拼出三段，主周期看不到；
- 第三推只是连续三根同向 K 线，没有分离的尝试；
- 前两次本身没有清楚的起点、终点和反应。

如果 lineage 不清楚，输出必须是 `not_h3_l3 / range_repeat_test / new_lineage_pending`，不能使用最终走势补齐计数。

## 3. 四种第三推状态

| 状态 | 视觉证据 | 默认处理 |
| --- | --- | --- |
| `exhaustion_candidate` | 第三推距离/效率下降，实体缩小或重叠增加，位于主要位置，并出现第一反向压力 | 先等反向 stop 或第二次确认；不能仅凭第三推反向 |
| `continuation_or_climax` | 第三推更快、更远、更宽，实体扩大、跳空或收盘更靠极值，后续仍有跟随 | 默认原方向仍有控制；等回调或失败，不在第三推末端直接逆势 |
| `range_repeat_test` | 三次测试围绕区间同一边界，重叠高，价格反复回到区间内部 | 用区间边缘/second-leg trap 逻辑，重置趋势 ABC/H3 计数 |
| `channel_continuation` | 三次触碰沿着可见通道运行，通道未被破坏或反向接受 | 顺势观察 H1/H2、L1/L2；不自动升级 MTR |

第三推减弱必须同时结合位置或反向证据；距离缩短本身可能只是波动降低。第三推扩张也不能被事后叫成衰竭。

## 4. 多空案例对照

| 案例 | 第三推状态 | 订单/首障碍 | 当前裁决 |
| --- | --- | --- | --- |
| [`KLAC 2025-03-17–03-26`](klac_h3_bear_flag_case_2025-03-12_2025-03-28.md) | 熊旗顶部第三次上探接近 `74–75` 阻力但没有接受；第三推后出现空头跟随 | `03-25` 低点下方 sell-stop；结构止损约 `74.50`；首支撑 `66.6–65.1`，约 `1.4R–1.9R`；SOXX 同向，财报过滤通过 | `research_state: research_positive_conditional / third_push_state: exhaustion_candidate / trade_state: not_authorized`；当前最有价值的 H3 条件样本，但 A 重叠、单案例和其他新闻风险仍未冻结 |
| [`TSLA 2025-03-07–03-10`](tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md) | 第三推加速并形成卖出高潮，属于 `continuation_or_climax` | `220–224` 支撑/MM 只能作目标层；第三推末端不能用后续止跌倒灌抄底 | `provisional L3 / continuation-risk`，不是楔形衰竭正例 |
| [`TSLA 2026-05-19–06-26`](h3_l3_research_gate_CN.md) | 三次低点收窄并落在支撑区，属于短级别 `exhaustion_candidate` | `379.12` 确认、`368.60` 结构风险；首阻力 `385.20–387.80` 约 `0.63R–0.83R` | 可研究短线反应，日线/波段 `valid_no_trade`；不升级 MTR |
| [`XOM 2024-07-18–08-02`](xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md) | 第三次上探抬高并扩大，明显偏 `continuation_or_climax` | `08-02` 开盘跳过原 sell-stop；首支撑约 `105.20`，重订后约 `0.7R` | `gap-reprice / valid_no_trade`，不是衰竭三推 |
| [`COIN 2024-01-04–01-09`](coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md) | 第三次上探范围扩大，C 类延续/扩张边界 | 日线首支撑约 `0.25R`，低周期约 `0.5R`；次日开盘重订 | `provisional H3-like / valid_no_trade` |
| [`UBER 2024-07-17–07-26`](uber_bearish_h3_l2_first_support_boundary_2024-07-17_2024-07-26.md) | 三次上探后更高、更宽，第三推扩张；不是逐步衰竭 | 财报过滤通过、XLY 偏弱，但首支撑约 `0.2R–0.3R`；低周期没有开盘跳过原触发 | `H3-like / L2-like / expansion-boundary / valid_no_trade` |
| [`ASML 2025-05-19–06-13`](asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md) | 下沿重复测试、重叠增多，属于 `range_repeat_test` | 没有可冻结的第三次同级别推进、反向二次触发和 R/R | `not_h3_l3 / range-transition` |
| [`NFLX 2024-08-05–09-26`](nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | 高位测试超过三次且重叠多；衰竭外观存在但计数不干净 | `67.10` 下方触发，首支撑 `66.54–65.98` 仅约 `0.1R–0.25R` | `three-push-top-like / valid_no_trade / later-invalidated` |
| [`ANET 2024-05-16–06-10`](anet_h3_l3_case_study_2024-05-16_2024-06-10.md) | 第二推明显扩张，第三次才在支撑附近减速；不是“一推比一推弱” | 事件/跳空背景未闭环；支撑反应可研究但不能冻结普通 L3 反转 | `continuation-or-climax / support-reaction-boundary` |

表中的 canonical 代表值为：KLAC `third_push_state: exhaustion_candidate`、ASML
`third_push_state: range_repeat_test`；TSLA 2025-03 的第三推属于
`third_push_state: continuation_or_climax`。其余案例若状态仍依赖后续分流，保持
`third_push_state: unclear`，不能用历史别名替代判断。

## 5. KLAC：当前唯一可保留的 H3 条件正向分支

`2025-03-17`、`03-19`、`03-24` 三次上探发生在同一空头父级的熊旗顶部，第三次接近主要阻力却没有被接受。`2025-03-25`–`03-26` 的空头恢复在 60m/15m 上有跟随，这比“第三推之后出现一根反向 K”更接近完整研究合同。

### 5.1 入场与风险

```text
方向：空头
研究触发：2025-03-25 低点外的 sell-stop
结构止损：约 74.50 上方
第一检查区：约 66.6–65.1
粗略空间：约 1.4R–1.9R
板块：SOXX 同期走弱
财报：KLA FY2025 Q3 为 2025-04-30，不在触发前三个交易日
```

这使 KLAC 的几何明显优于 NFLX、COIN、UBER 等首障碍拥挤样本。事后价格到达第一、第二支撑只能说明过程目标兑现，不能证明 H3 胜率或自动规则。

### 5.2 仍未冻结的地方

- 父级 A 内部仍有一定重叠，不是最干净的强 A；
- 第三推是熊旗上沿的三次测试，既有 H3 压力，也带有通道/旗形语义，不能只用“三推”解释；
- 15m 精确成交、止损 buffer 和收盘确认合同还没有标准化；
- 事件过滤通过只解决财报闸门，不排除其他新闻风险；
- 只有一个方向、一个主要案例，不能镜像成 L3 规则。

因此当前状态轴保持 `research_state: research_positive_conditional / trade_state: not_authorized / gate_result: conditional`；
它仍是 `not-production / not-statistical`，且 `validated win-rate: not-computable`。

## 6. L3：当前没有干净衰竭正例

当前 L3 材料主要分成三类：

1. `TSLA 2025-03-07–03-10`：第三推明显加速，卖出高潮后才反应，属于延续/高潮；
2. `TSLA 2026-03-25` 之后：L2 跟随后才提名 provisional L3，但逐推衰竭证据不足，第一支撑约 `1.0R–1.1R`，延续风险更高；
3. `TSLA 2026-05-19–06-26`：第三次下探收窄且支撑汇合，但第一阻力只有约 `0.63R–0.83R`，只适合短线反应研究。

这三类不能合并为一个 L3 反转规则。当前最重要的缺口是：一个事件过滤通过、第三推确实减弱、反向第二次确认清楚、首障碍宽裕且路径未先止损的空头 L3。

## 7. 三推与 MTR/区间/BOP 的状态切换

### 7.1 三推 → MTR

只有在第三推减弱、主要位置明确、第一反向破坏局部结构、第二次反向得到接受并且首障碍有空间时，才升级为 MTR candidate。KLAC 接近这一条件；NFLX 因首障碍不合格，不能升级。

### 7.2 三推 → 区间

如果三次测试围绕同一边界反复，价格频繁回到区间内部，先用区间边缘和 second-leg trap。ASML 不能因为旧研究标签叫 L3，就改写成视觉三推反转。

### 7.3 三推 → BOP

如果原方向强收盘越过主要边界并得到跟随，原反转假设失效，切换到 BOP。TSLA 2025-09 是这一硬边界：阻力下的三推观察没有提供提前做空授权，突破接受后更不能继续逆势。

### 7.4 三推 → 通道延续/高潮

第三推更快、更宽、收盘更靠极值，通常说明原方向仍有控制；TSLA、XOM、COIN、UBER 都是这一类的不同边界。高潮风险增加，不等于下一根 K 必然反转。

## 8. 订单与 R/R 纪律

- **反向 stop**：在第三推极端或第一反向信号 K 外等待确认；实际触发和低周期确认分开记录；
- **limit-retest**：只有失败边界、颈线或角色转换区事前清楚且真实回测才可能成交；
- **market-close**：反向收盘很强时可以研究，但必须用新的成交价和母级结构止损重算；
- **结构止损**：覆盖第三推/主要测试极端外，不用单根反向 K 的窄低点或高点制造 R/R；
- **第一障碍**：先看左侧主要支撑/阻力、区间中线、通道边界，MM 只作后续目标；
- **路径审计**：首障碍之前先破结构止损，记 `process-stop-first`；首障碍不足约 `1R`，记 `valid_no_trade`；
- **事件/跳空**：财报窗口直接禁止新合同，跳空越过触发则按实际成交重订，不保留理想价格。

## 9. 本轮结论

| 方向/状态 | 当前结论 |
| --- | --- |
| H3 衰竭候选 | KLAC 2025-03 是条件性研究候选，当前不冻结生产规则；需要第二个独立、事件干净、首障碍宽裕的衰竭样本。 |
| L3 衰竭候选 | `no-new-positive`；现有 TSLA 样本分别是扩张/高潮、延续风险或短线支撑反应，尚无完整正向合同。 |
| 扩张/高潮 | TSLA、XOM、COIN、UBER 覆盖了“第三推更强”边界；不能把 H3/L3 名称当作反转授权。 |
| 区间/通道 | ASML 和通道样本说明 lineage 必须重置或降级；区间内三次测试不能继承开放趋势腿数。 |
| 交易几何 | NFLX、COIN、UBER 和 TSLA 2026-05 说明反向形态存在但首障碍不足；静态 MM 不能救回入场层。 |

正式记录：

> `third_push_state: exhaustion_candidate / second_confirmation: pending / space_status: unknown / research_state: research_positive_conditional`：**no-new-positive**。

这不是说三推或 H3/L3 没有价值，而是当前 PA Research 已经能可靠区分压力状态，尚未有足够双向、事件干净、空间宽裕的反转样本。下一次只在出现新方向、真实订单分支或新的状态边界时增加案例。

## 10. 入口

- [`三推 / H3-L3 目录`](../patterns/08_three_push_h3_l3/README.md)
- [`三推/H3-L3 压力状态框架`](three_push_pressure_state_framework_CN.md)
- [`H3/L3 研究闸门`](h3_l3_research_gate_CN.md)
- [`MTR 与三推证据缺口审计`](mtr_three_push_evidence_gap_audit_2026-08-23_CN.md)
- [`MTR 主要趋势反转专项视觉证据审计`](mtr_visual_evidence_gap_audit_2026-08-24_CN.md)

研究边界：只更新 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

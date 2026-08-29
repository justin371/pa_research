# 三推 / H3-L3 的压力状态框架 V0.1

状态：`visual-research / provisional / pressure-state-layer / not-quantitative`；修订：`2026-08-26`

这份文件是 [`H3/L3 研究闸门`](h3_l3_research_gate_CN.md) 和 [`H3/L3 视觉比较`](h3_l3_visual_comparison_CN.md) 的补充层。它不重新定义 H3/L3，而是回答更重要的视觉问题：

> 同样出现三次推进或三次测试时，压力是在减弱、扩张，还是只是在区间/通道内重复运行？

三推是观察入口，不是反转授权。第三推的性质、位置、反向跟随和第一障碍共同决定是否值得深入。开放趋势/通道三推与成熟交易区间边缘三推是两条不同路径：后者可以不要求强 A，但必须把区间中部重复测试排除在候选之外。

## 1. 先确认是不是同一组推进

在数 H3/L3 之前，先确认：

- 三次尝试属于同一高周期背景和同一条修正/回调 lineage；
- 每次尝试之间有可见反应、停顿或失败，而不是连续三根同方向 K 线；
- 趋势/通道路径不能已经进入成熟交易区间中部，也不能建立新的母级 A 腿；若是区间边缘路径，则必须确认成熟区间、同一上沿/下沿和第三推位置，而不是把中部摆动硬接成趋势 lineage；
- 前两次尝试在当时已经是有意义的高点/低点，而不是事后挑出来的局部极值。

如果这些条件不满足，标签优先写成 `not_h3_l3`、`range_repeat_test` 或 `new_lineage_pending`。

## 2. 压力变化的四个视觉维度

不设固定数值，只做定性比较：

| 维度 | 可能的衰竭证据 | 可能的延续/扩张证据 |
| --- | --- | --- |
| 推进效率 | 每次推进距离缩短，或需要更多 K 才走同样距离 | 第三推更快、更远、更少重叠 |
| K 线质量 | 实体变小、影线增多、收盘离极值、跟随变差 | 实体扩大、收盘靠极值、连续跟随 |
| 结构接受 | 越过高/低点后回到原侧，边界反复拒绝 | 越过高/低点后留在外侧并继续接受 |
| 位置与空间 | 接近主要支撑/阻力、通道边界、区间边缘或 MM；反向有空间 | 仍处开放趋势或突破空间，最近障碍不近 |

“第三推减弱”至少要和重要位置或反向证据结合；单纯距离缩短可能只是波动下降。反过来，第三推扩张时，即使价格看起来很晚，也不应自动做反向。区间边缘本身提供位置优势，但不替代反向触发和空间审计。

## 3. 四种压力状态

### A. `exhaustion_candidate`：衰竭候选

视觉特征：第三推效率降低、重叠增加、收盘质量变差，且落在主要位置；随后出现方向明确的第一反向运动。

默认预期：先看小反转、均线回归或两腿回调。只有反向结构被破坏、第二次入场出现、第一障碍有空间，才进入 MTR/楔形反转审计。

### B. `continuation_or_climax`：扩张/延续

视觉特征：第三推更宽、更快、收盘更靠极端，或出现跳空、连续大 K 和强跟随。

默认预期：原方向仍占优；高潮风险增加，但不等于马上反转。不要在第三推末端仅凭 H3/L3 标签逆势交易，优先等回调或接受/失败的后续证据。

### C. `range_repeat_test`：区间重复测试

视觉特征：多次测试同一上沿/下沿，K 线重叠明显，价格回到区间内部；推进之间没有清楚的趋势腿 lineage。

默认预期：不要把区间内的三次测试写成开放趋势 H3/L3。若第三推位于已确认的上沿/下沿，并出现拒绝、假突破重返区间或反向信号，可进一步标记 `range_edge_three_push_candidate`；若位于中部，则保持 `range_middle_no_trade / observation_only`。

#### 区间边缘三推候选

这条分支允许 A 腿普通、偏弱或重叠较多，因为它研究的是成熟区间边缘的第三次压力，而不是强 A 后的趋势延续。候选至少需要：

1. 两年以上 Daily 左侧可确认区间上沿/下沿、重要支撑/阻力和当前角色；
2. 第三推确实到达上沿或下沿，而不是只在区间中部重复摆动；
3. 顶部只研究空头反转方向，底部只研究多头反转方向；
4. 第三推后有拒绝、假突破重新收回区间或反向信号 K；
5. 结构止损覆盖边缘外正常噪声，第一目标先看中线/最近独立障碍，首障碍不足约 1R 时仍为 `valid_no_trade`。

第一次反向触发可以让它成为研究候选；第二次反向确认用于升级 MTR 或主要趋势反转，不是区间边缘候选的前置必要条件。如果第三推强收盘越过边缘并在外侧接受，反转候选失效，切换 BOP/趋势延续。

### D. `channel_continuation`：通道延续

视觉特征：价格沿着可见通道边界运行，回调和推进反复，第三次触碰仍受通道惯性支配；没有主要边界失败或反向接受。

默认预期：先按通道和趋势延续处理。只有通道破坏、回测失败、反向结构和空间同时成立，才转入反转审计。

## 4. 无后见之明的分流

```text
完整图表
  → 是否处在成熟交易区间上沿/下沿？
      是
        → 第三推是否到达边缘并出现拒绝/反向信号？
            是 → range_edge_three_push_candidate；按区间中线/首障碍审计
            否
              → 若强收盘越过边缘并外侧接受，切换 BOP；否则 observation
      否
        → 三次尝试是否同一趋势/通道 lineage？
            否 → 区间中部/新母级腿；不冻结 H3/L3
            是
              → 第三推压力是否扩张？
                  是 → continuation_or_climax；不直接反向
                  否
                    → 是否减弱且到达主要位置？
                        否 → ordinary H1/H2/L1/L2 或 observation
                        是 → exhaustion_candidate；等待反向确认
```

后续盈利、MM 到位、第四次推进或最终反转都不能回写到分流时点。每个阶段只记录当时能看到的状态。

## 5. 第一反向运动和二次入场

第三推后的第一根反向 K 只能标为 `reversal_attempt_1`。研究上分三档：

1. **反向触碰**：只出现影线或单根小实体，没有破坏局部结构；保持观察；
2. **第一反向突破**：突破第三推后的局部结构，但尚未经过回测或第二次确认；可研究小风险 stop；
3. **第二次确认**：第一次反向后出现小回调/失败，再次形成 H1/H2-like 或 L1/L2-like 反向触发，并有跟随；才可进入较完整的反转订单审计。

H3/L3 的“第三次”与反转方向的 H1/H2、L1/L2 是两套计数：前者描述原方向的尝试次数，后者描述反向的确认次数，不能混成一个数字。区间边缘三推的第一次反向触发可以先作为独立候选，不应因为尚未达到 MTR 的第二次确认就自动降为“无机会”。

## 6. 订单、结构止损和首障碍

### 6.1 Stop-confirmation

默认研究分支是在第一或第二反向信号 K 外等待 stop。记录原始触发、实际成交和是否跳空。若第三推极端被重新接受，反向合同失效。

### 6.2 Limit-retest

只在第三推失败边界、颈线、前支撑转阻力或前阻力转支撑已经明确时研究回测限价单。价格没有回到区域前不能假设成交；它与原 stop 合同分开记录。

### 6.3 结构止损

- 看空三推顶部：放在第三推/主要测试高点和失败边界外，覆盖正常测试；
- 看多三推底部：放在第三推/主要测试低点和失败边界外；
- 不把单根反向信号 K 的窄极值当成母级结构止损，除非明确研究的是独立低周期合同；
- 跳空改变实际成交后，按实际成交重算风险，旧的理想触发不再有效。

### 6.4 首障碍和粗略 R/R

从实际入场方向看，先找最近的独立左侧支撑/阻力、区间中线、通道边界或角色转换区，再看远端 MM。第一障碍不足约 1R 时，标记 `valid_no_trade`；约 2R 只作为完整波段的粗略参考，不是固定规则。

区间边缘三推的第一目标通常是区间中线或最近独立障碍；只有价格越过并接受中线后，才把另一侧边缘或 MM 作为后续目标。

## 7. 案例对照

| 案例 | 第三推状态 | 当时的交易含义 | 首障碍/订单结论 |
| --- | --- | --- | --- |
| [`KLAC 2025-03-17–03-26`](klac_h3_bear_flag_case_2025-03-12_2025-03-28.md) | `exhaustion_candidate`：熊旗顶部第三次上探没有接受，空头跟随清楚 | 当前 H3 候选，仍先标研究候选而非生产规则 | `03-25` 低点下方 sell-stop；首阻力下方到 `66.6–65.1` 约 `1.4–1.9R`，空间相对宽 |
| [`TSLA 2025-03-07–03-10`](tsla_l1_l2_l3_case_study_2025-02-19_2025-03-10.md) | `continuation_or_climax`：第三推加速、卖出高潮 | L3 不等于楔形反转；不能在第三推末端追空或立即抄底 | `220–224` 支撑/MM 是事后附近的目标区，不能倒灌；先预期反弹/区间 |
| [`TSLA 2026-05-19–06-26`](h3_l3_research_gate_CN.md) | `exhaustion_candidate` 但级别偏短：推进收窄、支撑汇合 | 可以研究一次短线反应，不能升级成主要趋势反转 | `379.12` 确认到 `368.60` 结构风险时，首阻力 `385.20–387.80` 约 `0.63–0.83R`，日线新仓 no-trade |
| [`XOM 2024-07-18–08-02`](xom_bearish_h3_flag_expansion_boundary_2024-07-18_2024-08-02.md) | `continuation_or_climax`：第三次上探抬高并扩张 | 空头反应存在，但不是逐推衰竭；跳空后重新审计 | `08-02` 开盘跳过原 sell-stop；首支撑约 `105.20`，重订后约 `0.7R`，valid no-trade |
| [`COIN 2024-01-04–01-09`](coin_bearish_l1_l2_gap_boundary_2024-01-02_2024-01-12.md) | `continuation_or_climax` / C 类边界：第三次范围扩大 | 第三次回到阻力不等于压力减弱 | 低周期反向可触发，但首支撑约 `0.25–0.5R`，且次日开盘重订，valid no-trade |
| [`ASML 2025-05-23–06-11`](asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md) | `range_repeat_test`：下沿重复测试后进入重叠区间 | 旧三腿标签重置，使用区间/过渡逻辑 | 无冻结 H3/L3 反向合同；不把后续上涨倒灌成双底或楔形 |
| [`NFLX 2024-08-05–09-26`](nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) | `exhaustion_candidate` 外形，但测试超过三次、重叠多 | 可记录高位反向尝试，但计数不冻结 | `67.10` 下方低周期可审计，首支撑约 `0.1–0.25R`，valid no-trade |

这组案例的价值是把“减弱”和“后续反向结果”拆开：KLAC 的反向跟随和空间使它值得深入；TSLA/XOM/COIN 说明扩张或订单几何会否决交易；ASML 说明区间重复测试不应强行计数；NFLX 说明形态和触发清楚仍可能首障碍拥挤。

## 8. 当前视觉输出格式

遇到三推/H3/L3 候选，先输出：

`primary_pattern` 是当前研究合同的主标签，`internal_label` 只记录 H1/H2/L1/L2/H3/L3；`contract_scope: daily_candidate` 时主标签仍只允许 `ABC_CONT` 或 `BOP`，压力状态不直接扩展日线白名单。

```text
contract_scope: deep_review / daily_candidate / historical_context_only
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
attempt_direction: bullish_attempts / bearish_attempts / unknown
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
lineage_status: same_lineage / reset / unclear / pending
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
direction: long / short / no_valid_direction
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
order_branch: stop_confirmation / limit_retest / market_close / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / management
gap_policy: accept_open / skip / flag_only / not_applicable
structural_stop: where and why
first_independent_obstacle: where and why
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

当 `range_edge_three_push=yes` 时，`range_edge_side` 必须是 `upper` 或 `lower`；上沿只建立空头研究方向，下沿只建立多头研究方向，但触发、空间或合同未冻结时仍可写 `direction: no_valid_direction`。这份输出允许“看起来像三推”与“值得交易”同时得到不同结论，符合视觉研究目标；`third_push_state`、`first_reverse` 和 `second_confirmation` 不替代订单分支或闸门结果。

## 9. 当前结论与研究缺口

1. 第三推减弱只有在重要位置、反向结构和空间共同出现时，才升级为 `exhaustion_candidate`；区间边缘三推可以先以独立位置候选记录，不必把它误写成开放趋势衰竭；
2. 第三推扩张通常优先归入延续/高潮，不逆势猜反转；
3. 区间中部重复测试和通道内第三次触碰，分别使用区间和通道逻辑，不强行套楔形；区间上沿/下沿的第三推可进入 `range_edge_three_push_candidate`，但仍需反向触发与空间；
4. 第一反向运动只是尝试，第二次确认和跟随才决定是否进入完整订单审计；
5. 当前 KLAC 是条件性的 H3 研究候选，L3 侧仍以延续、高潮、短线反应和首障碍边界为主；不能把 H3 条件镜像成 L3 规则；
6. 当前尚无无事件、双向、第二次确认清楚且首障碍宽裕的标准三推反转正例，因此本框架保持 `provisional`。

只有新增案例能填补方向、订单合同或压力状态缺口时，才继续加样本。框架只服务 PA Research 的视觉筛选，不进入 Codex Trading 或 Execution Agent。

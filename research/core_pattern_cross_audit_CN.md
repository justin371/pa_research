# 核心八个 Pattern 交叉一致性审计 V0.1

日期：2026-08-23  
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

## 目的

这份文件检查当前八个主动 pattern 目录是否使用同一套视觉判断顺序，并明确它们什么时候可以共存、什么时候必须切换。它不是第九个交易形态，也不把八个目录合并成一个评分器。

逐图执行时使用[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)；本文件只负责八个目录之间的分层、切换和状态一致性。

方向、BOP 专用字段、订单枚举和状态分轴统一见[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。本文件中的历史别名只用于解释，不作为新记录字段。

审计结果先固定一个重要分层：

1. **背景层**：趋势、交易区间、通道、过渡、高潮；
2. **结构/计数层**：ABC、H1/L1、H2/L2、三推/H3-L3、区间边缘尝试；
3. **状态转换层**：失败突破、BOP、MTR；
4. **合同与风险层**：方向、信号 K、触发、实际成交、结构止损、第一障碍、R/R、事件和 no-trade。

因此，H2 可以是 ABC 中的第二次尝试，三推可以是 MTR 的证据，失败突破之后也可以转成 BOP；这些是**有条件的交叉标注**，不是把多个 pattern 相加后就提高胜率。

## 审计结论

- 八个目录均已存在，且已从 `patterns/README.md`、`docs/common_context.md`、覆盖审计和候选清单建立入口；
- 八个目录的共同主线都是“背景 → 位置/左侧 → 结构 → 触发 → 风险 → 结果”，但各目录原有状态标签曾使用连字符、下划线和自然语言混写；本文件规定新记录优先使用下划线形式，历史案例可保留原标签并按下表解释；
- H1/L1、H2/L2 和 ABC 不是互斥形态：ABC 描述父级回调合同，H/L 描述其中第几次有意义的方向尝试；
- 三推/H3-L3 是压力状态，失败突破/BOP/MTR 是状态转换。一次“三推”不能自动生成 MTR，原方向被接受后必须切到 BOP；
- 区间边缘优先级高于区间内部的趋势腿计数。区间中部的摆动不能同时被算作开放趋势 ABC 和 H1/H2；
- 第一独立障碍、结构止损、事件和实际成交是所有目录的共同否决层，不能只在 H1/H2 案例里检查；
- 低周期只能确认同一高周期合同，除非重新冻结入场、止损、持有周期和第一障碍，才能另立低周期合同。

## 统一复核顺序

每张图先按以下顺序输出；如果前一步改变了父级状态，后面的旧合同立即失效：

```text
1. parent_state / timeframe / market_context
2. left_structure_and_location / major_support_resistance
3. directional_leg_or_range_edge
4. lineage_and_attempt_count
5. signal_bar / trigger / follow_through
6. order_branch / actual_fill / opening_skip
7. structural_stop / invalidation
8. first_independent_obstacle / rough_R_R
9. event_and_sector_context
10. final_state / no_trade_reason / next_contract
```

“先看什么”与“最后是否交易”必须分开：前四步决定它像哪个 pattern，后六步决定这个形态是否值得进入交易审计。

## Pattern 层级与切换矩阵

| 当前观察 | 首选目录 | 可以切换到 | 切换条件 | 不能做的事 |
| --- | --- | --- | --- | --- |
| 开放趋势中第一次有意义的恢复 | H1/L1 | H2/L2、ABC | 第一次无跟随并形成第二次尝试；或能明确 A-B-C 父级 | 不因 EMA 触碰或第一根顺向 K 自动计 H1/L1 |
| 同一回调中的第二次有意义尝试 | H2/L2 | 三推/H3-L3、ABC、区间边缘 | 出现第三次有意义尝试；B 被接受为区间；或父级结构被破坏 | 不用 H2 编号挽救区间中部或失控 B |
| 可见 A 腿、受控 B、C 恢复原方向 | ABC | H1/L1、H2/L2、区间边缘、BOP | H/L 作为 ABC 内的尝试标签；B 变成区间；突破被接受后重建 BOP 合同 | 不把 MM/AB=CD 当成 C 的充分入场信号 |
| 成熟区间上沿/下沿的反复测试 | 区间边缘二次入场 | 失败突破、BOP、MTR | 刺破后回区间；区间外收盘接受；反向结构真正破坏控制权 | 不在区间中部继承趋势 ABC 腿数 |
| 边界被越过但未被接受，或高潮后第一反向 | 失败突破/高潮 | 区间边缘、MTR、BOP、三推 | 回到原侧并有第二次确认；主要结构被破坏；原方向重新接受；第三推扩张 | 不把影线、单根反向 K 或事后盈利叫已确认失败 |
| 突破已在边界外被接受 | BOP | BOP 回踩、失败突破 | 回踩守住旧边界并再次离开；重新接受旧区间则旧 BOP 失效 | 不沿用突破前的 MTR、区间或 H/L 订单 |
| 成熟趋势在主要位置发生结构破坏 | MTR | 失败突破、三推、BOP | 反向第二次确认且首障碍有空间；失败或原方向接受则降级/切换 | 不因双顶、三推或大反向 K 单独称 MTR |
| 同一 lineage 的第三次推进/测试 | 三推/H3-L3 | MTR、失败突破、区间边缘、BOP | 压力减弱且反向结构被接受；边缘重复测试；原方向扩张并接受 | 不把第三次自动叫楔形衰竭或自动反向 |

### 优先级规则

当多个标签同时出现时，按“父级状态优先、状态转换次之、计数标签最后”的顺序处理：

1. 先判定是不是成熟区间；是，则区间边缘/失败突破优先于趋势 ABC/H1/H2；
2. 再判定突破是否被接受；已接受则 BOP 优先，旧反转 thesis 作废；
3. 在开放趋势中再审计 A/B/C 和 H1/H2；第三次尝试进入三推/H3-L3；
4. 只有成熟趋势、主要位置、反向结构破坏、第二次确认和空间同时出现时，才把 MTR 升为主要研究合同；
5. 无论标签是什么，首障碍太近、结构止损过宽、事件窗口或实际成交无法冻结，都输出 `valid_no_trade`。

## 互斥与可共存边界

| 组合 | 允许共存？ | 解释 |
| --- | --- | --- |
| ABC + H1/L1/H2/L2 | 是 | ABC 是父级 A-B-C，H/L 是 C 前后的尝试计数 |
| H2/L2 + 三推/H3-L3 | 有条件 | H2/L2 之后的第三次尝试可以标 H3/L3；计数必须来自同一 lineage |
| 三推/H3-L3 + MTR | 有条件 | 三推只提供压力证据；必须另有结构破坏、第二次确认和空间 |
| 区间边缘 + 失败突破 | 是 | 边缘刺破后重新回区间，失败突破是区间合同的状态分支 |
| 失败突破 + BOP | 不能同时作为当前方向合同 | 原方向重新接受后，失败突破 thesis 结束，改建 BOP 合同 |
| 区间边缘 + 开放趋势 ABC | 通常不同时成立 | 若价格在区间中部，趋势腿计数重置；只有边界外接受后才能重建趋势合同 |
| BOP + MTR | 只能按时间顺序 | BOP 接受会否定原 MTR；之后若新趋势再成熟，未来可另研究新的 MTR |
| MM/AB=CD + 任一 pattern | 是，但只是测量层 | 测量用于空间/目标，不改变父级状态，也不提供单独入场授权 |

## 统一状态词汇

新建或更新的核心目录记录优先使用以下状态；历史文件中的连字符或自然语言标签不要求一次性重写，但引用时要映射到这里：

| Canonical token | 历史别名/含义 |
| --- | --- |
| `pattern_like` | `visual_candidate`、形态像、候选 |
| `research_candidate` | `candidate`、条件性研究候选 |
| `research_positive_conditional` | `research_positive_candidate`、条件正向 |
| `observation_only` | `observation-only`、观察、不交易 |
| `valid_no_trade` | `valid-no-trade`、no-trade、形态像但合同否决 |
| `reversal_attempt` | `reversal-attempt`、第一次反向尝试 |
| `failed_thesis` | `failed-MTR-thesis`、原假设失效 |
| `mtr_candidate` | `MTR_candidate`、MTR candidate |
| `continuation_or_climax` | `continuation-or-climax`、扩张/高潮延续 |
| `range_repeat_test` | `range-repeat`、区间重复测试 |
| `channel_continuation` | `channel-continuation`、通道延续 |

订单字段也统一写成 `stop_confirmation`、`limit_retest`、`market_close`、`observation_only`；如果使用 `reprice_after_gap`，必须另记原始触发和实际可成交合同。

## 八个目录的覆盖检查

| 目录 | 主问题 | 共同字段已覆盖 | 主要切换出口 | 尚未冻结的点 |
| --- | --- | --- | --- | --- |
| [`H1/L1`](../patterns/01_h1_l1_first_entry/README.md) | 强 A 后第一次有意义恢复是否值得早做 | 背景、A/B、位置、信号、stop、首障碍、no-trade | H2/L2、ABC、区间边缘 | H1 与普通趋势噪音的边界 |
| [`H2/L2`](../patterns/02_h2_l2_second_entry/README.md) | 第一次失败后第二次是否更清楚 | 父级、首次失败、二次尝试、触发、结构止损、R/R | H3/L3、ABC、区间边缘 | 多空条件正例和首障碍空间 |
| [`ABC`](../patterns/03_abc_continuation/README.md) | A 腿、受控 B、C 恢复是否仍是趋势合同 | A/B/C、lineage、MM 分离、订单、重置 | H/L、区间、BOP | 深 B 与过渡状态 |
| [`区间边缘`](../patterns/04_range_edge_second_entry/README.md) | 边缘二次测试是否提供区间机会 | 上下沿、中点、边缘尝试、limit/stop、目标 | 失败突破、BOP、新趋势 | 成熟度和 second-leg trap 的视觉边界 |
| [`失败突破/高潮`](../patterns/05_failed_breakout_climax/README.md) | 边界失败与高潮后反应属于什么状态 | 边界、接受/拒绝、反向确认、合同、首障碍 | 区间、MTR、BOP、三推 | 干净双向正例 |
| [`BOP`](../patterns/06_breakout_pullback_bop/README.md) | 突破接受后的新合同是否成立 | 边界、收盘接受、回踩、角色转换、实际成交 | 失败突破、后续趋势 | 事件干净回踩正例 |
| [`MTR`](../patterns/07_mtr_reversal/README.md) | 主要趋势控制权是否改变 | 成熟趋势、位置、结构破坏、二次确认、止损、首障碍 | BOP、失败突破、区间、三推 | 无事件且空间宽裕的正例 |
| [`三推/H3-L3`](../patterns/08_three_push_h3_l3/README.md) | 第三次推进是衰竭、扩张、重复测试还是通道延续 | lineage、三次推进、压力状态、反向确认、订单、首障碍 | MTR、失败突破、区间、BOP | L3 衰竭和干净反转正例 |

## 研究和执行的共同否决层

任何目录在进入交易审计前都必须回答：

- 入场时可见的第一独立支撑/阻力在哪里？
- 结构止损覆盖了哪一个正常测试？
- 触发是否真实发生，还是只在图上碰到/被开盘跳过？
- 财报前三个交易日、重大事件和板块/市场方向是否已标记？
- 第一障碍是否给出足够空间？如果不清楚，是否应为 `valid_no_trade`？
- 后续盈利、MM 到位或最终反转是否被错误地倒灌回入场判断？

这些问题不产生分数，也不制造自动信号；它们只是保证八个 pattern 的视觉研究使用同一条安全底线。

## 本轮验收

- 八个目录均能从共同上下文和覆盖审计直接进入；
- 统一复核顺序和状态词汇已固定，历史别名有明确映射；
- 已明确 H1/H2/ABC 的共存关系，以及区间、失败突破、BOP、MTR、三推之间的切换条件；
- 所有切换都保留结构止损、第一障碍、实际成交和 no-trade 分支；
- 没有新增量化扫描器、Codex Trading 修改或 Execution Agent 连接。

这份审计完成的是研究层的一致性，不代表任何 pattern 已达到生产规则或真实交易授权。

# BOP 真实多日回踩候选审计（2026-08-24）

日期：2026-08-24
文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向、BOP 状态和订单分支见[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。本审计只修改 PA Research，不创建量化扫描器、不连接 Execution Agent。

本审计的机器可读后续准入清单见[`BOP 合同准入审计（2026-08-28）`](backtesting/bop_contract_intake_audit_2026-08-28_CN.md)及[`bop_contract_intake_2026-08-28.csv`](backtesting/bop_contract_intake_2026-08-28.csv)。

## 1. 本轮要找的不是哪一种突破

本轮只检查一种较完整的 BOP 合同：

```text
事前存在主要支撑/阻力或成熟区间边界
→ 强收盘离开旧边界并得到后续接受
→ 至少经过后续日线观察窗口
→ 价格回到旧边界附近，完成真实多日回测
→ 旧阻力转支撑或旧支撑转阻力仍被守住
→ 再次离开回测区并有跟随
→ 订单、结构止损、首障碍和事件过滤均可重建
```

“多日回踩”不是用固定根数定义的量化阈值。它的最低视觉要求是：不能只拿突破当天的 15m 小回调或下一根 K 的影线测试来命名；必须能在日线父级上看到接受、回到旧边界、守住/失败以及再次离开的过程。

这份审计不把 gap-and-go、盘中回调、单日影线测试、limit-retest 和多日 BOP 混成一类。它们可以共享“角色转换”的语言，但不是同一个订单合同。

## 2. 统一输出合同

每个候选只保留一个主标签：

```text
contract_scope: deep_review
primary_pattern: BOP / failed_breakout / range_edge / other
direction: long / short / no_valid_direction
secondary_context: gap-and-go / former-double-top / H1-H2 / channel / triangle
state_transition: none / breakout_acceptance / role_reversal / failed_breakout
bop_state: acceptance_watch / ordinary_pullback / failed_breakout / gap_event / bull_flag_continuation
acceptance: close outside + follow-through + hold/retest evidence
retest: intraday-only / single-session / multi-day / not-occurred
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / role_reversal_retest / gap_reprice / management
structural_stop: role-conversion zone or parent invalidation, with buffer
first_independent_obstacle: first independent left-side level after actual fill
gate_result: pass / conditional / observation_only / valid_no_trade / pending
trade_state: conditional / valid_no_trade / observation_only / pending
thesis_state: working / failed / invalidated / replaced / pending
```

同一价格簇中的旧边界、EMA、缺口边缘和 MM 不重复计分。MM 只能在角色转换被接受、第一独立障碍已处理后升级目标，不能替代回踩证据。

## 3. 候选筛选表

| 案例 | 主标签 | 已有证据 | 缺少或否决点 | 当前裁决 |
| --- | --- | --- | --- | --- |
| [`TSLA 2025-09-08–09-12`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | `BOP / breakout-acceptance` | `2025-09-08–10` 在 `355.39–357.54` 下方反复测试；`09-11` 强收盘越过；15m 有跟随，盘中回测没有重新跌回旧区间 | 回测主要发生在同一交易日的低周期；没有形成日线级别“数日后回到旧边界、再离开”的完整样本；突破 K 很宽，首障碍与结构止损尚未闭合 | `research_positive_conditional / intraday-retest-only` |
| [`TSLA 2025-03-04 284 回测`](tsla_abc_playbook_2025-03-04_284_retest.md) | `BOP / breakout-pullback` | 空头 gap-and-go 后，旧低点/反转区约 `283.8–284.3` 在同日被回测并再次受阻；`284` sell-limit/retest 是独立合同 | 原 `277` sell-stop 被开盘跳过；回测不是多日；首支撑约 `261.84–262.24`，约 `1.1R`，事件闭环仍需单列 | `research_positive_conditional / single-session-retest` |
| [`VRT 2026-04-14–04-20`](vrt_bullish_abc_h1_deep_b_first_obstacle_boundary_2026-04-14_2026-04-20.md) | `BOP-like / re-arm` | `04-14` 缺口后强 A；`04-17` 低周期重新确认，可研究开盘接受或 re-arm | A 含缺口、财报尚未独立核对；原 stop 被开盘越过；触发后第一阻力 `310.94–312.40` 太近；没有完成多日角色转换回踩 | `valid_no_trade / event-pending / not-BOP-baseline` |
| [`NKE 2025-10-03–10-29`](nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md) | `limit-retest-boundary` | `10-28` 小缺口后，盘中重新回到 `66.78` 附近，存在事前可定义的回测路径 | 主要是单日 limit-retest，不是多日回踩；板块混合，A 紧接事件背景；首支撑约 `1.2R`，仍属边界 | `pattern_like / pending / not-clean-BOP` |
| [`GOOGL 2024-03-04–03-22`](googl_bullish_h1_gap_trigger_boundary_2024-03-04_2024-03-22.md) | `gap-trigger-reprice` | 强 A、浅 B 后突破方向清楚 | 原 buy-stop 被开盘跳过，价格没有回到旧触发区；没有真实回测，不能假设成交；近端阻力拥挤 | `valid_no_trade / retest-not-occurred` |
| [`WMT 2024-06-24–06-27`](wmt_bullish_h1_gap_pullback_boundary_2024-06-24_2024-06-27.md) | `gap-pullback-boundary` | 深 gap pullback 后恢复，方向和局部回调可读 | 角色转换和独立 limit-retest 未冻结；结构止损到 `67.47–67.61` 首阻力约边界空间；事件状态需单列 | `pattern_like / valid_no_trade / not-clean-BOP` |

## 4. TSLA 2025-09：接受样本，不是多日回踩正例

这是当前最容易被误读的案例。`2025-09-08–10` 的多次阻力测试仍支持反转观察；`2025-09-11` 强收盘站上 `355.39–357.54`，15m 有跟随，随后回测守住旧阻力上方。它确实完成了：

```text
old resistance → strong close outside → follow-through → intraday hold/retest
```

所以主标签应该从旧的双高/三推/MTR 观察切换为 `BOP_acceptance`。但它不能被描述成“已经验证的多日回踩买点”：

- 回测主要在同日低周期完成；
- 日线没有先离开数日、再回到旧边界、再重新离开的完整序列；
- 日线突破 K 很宽，直接收盘追入、15m 触发和次日追入是三种不同合同；
- 结构止损和第一独立障碍尚未形成宽裕、可复核的同一 R/R。

它的主要贡献是**状态切换**，不是证明“突破后必然给回踩”或“盘中回调等于多日回踩”。

## 5. TSLA 2025-03：旧位回测样本，不是多日回踩正例

`2025-03-04` 跳空下破后，约 `283.8–284.3` 的旧低点/反转区在同日反弹中转为阻力。这个案例非常适合训练订单语义：

- 原 `277` sell-stop 被开盘跳过，旧成交价和旧 R/R 作废；
- `284` 附近 sell-limit/retest 是另一份合同；
- 如果等回测失败后再挂 sell-stop，又是第三份更晚合同；
- 结构止损约 `304`，第一支撑约 `261.84–262.24`，空间只有边界水平。

它证明“突破回测是新合同”，但回测发生在同一交易日，不足以填补多日 BOP 的证据缺口。

## 6. 事件、订单和多周期闸门

### 事件

财报前三个交易 session 不建立新合同。事件 gap 后的强 A 只能单列为事件驱动或重订分支，不能作为普通 BOP 基准。VRT 尚未完成事件核对，因此不能升级；TSLA 2025-09 的财报日期较远，但它仍缺少多日回踩，不因事件通过而自动合格。

### 订单

```text
突破收盘追入：确认最早，但可能撞首障碍
突破后 stop：必须冻结新的局部结构和实际触发
limit-retest：只有真实回到旧边界才可能成交
gap-reprice：原订单失效，按实际价格和新止损重算
多日回踩再离开：属于独立的 BOP continuation 合同
```

没有真实回到旧边界，就没有 limit-retest 成交；开盘越过原触发后，不能继续沿用原价。低周期确认可以提高时序，但不能把日线没有多日回踩的样本升级成多日 BOP。

### 多周期

- Daily：旧边界、突破接受、日线回测和父级空间；
- 4H/1H：接受是否持续、回测是否守住、低周期结构是否重建；
- 15m：实际触发与跟随；
- 15m 的盘中回调不能创造 Daily 的多日回踩，也不能用窄止损掩盖高周期首障碍。

## 7. 本轮结论：`no-new-positive`

本轮没有找到同时满足以下条件的普通 BOP 正例：

```text
event-clean
parent-clear
old-boundary-preidentified
daily-acceptance
multi-day-retest-and-hold
re-departure-follow-through
actual-order-reconstructable
first-obstacle-space-positive
process-complete
```

当前证据分层如下：

| 层级 | 案例 | 能证明什么 |
| --- | --- | --- |
| `state-transition` | TSLA 2025-09 | 旧反转 thesis 被强收盘、跟随和回测守住否定，必须切换 BOP |
| `single-session-retest` | TSLA 2025-03 | 旧位回测是新合同，原 stop/limit/重订不能合并 |
| `boundary` | VRT/NKE/WMT/GOOGL | 缺口、首障碍、事件或未回测会否决交易 |
| `multi-day-BOP-positive` | 暂无 | 仍是明确证据缺口 |

正式记录：

> `BOP / event-clean / daily-accepted / multi-day-retest-held / first-obstacle-space-positive / process-complete`：**no-new-positive**。

这不是说 BOP 没有研究价值。当前视觉助手已经能识别突破接受、角色转换和订单重订；下一步只在出现真正多日回踩、事件闭环和首障碍宽裕的新案例时继续补样本，不把同日盘中回调重复命名为多日 BOP。

## 8. 下一轮候选多周期复核（2026-08-24）

本轮证据边界：当前 PA Research 工作区没有图像资产，本 session 也没有 Futu/TradingView 连接。以下只复核仓库中已经保存的历史图表复核记录；各案例的来源、历史/收盘后状态以其文件为准，不能说成是本轮新抓取或实时数据。缺少周期、事件或订单字段时，按缺失处理，不用文字或后续走势补图。

| 案例 | 可读周期证据 | BOP 链条审计 | 主要否决 | 裁决 |
| --- | --- | --- | --- | --- |
| [`JPM 2025-08-22–09-05`](jpm_bullish_h1_first_obstacle_failure_2025-08-22_2025-09-05.md) | Daily；15m 触发；无可核验 4H/1H bar | `09-05` 开盘越过 `297.26` 后最高约 `299.42` 即回落，没有守住旧边界、再离开或跟随 | 事件 `pending`；首障碍约 `0.39R`；突破分支未冻结结构止损 | `boundary / valid_no_trade / no-new-positive` |
| [`KLAC 2025-10-14–10-24`](klac_h1_case_study_2025-10-14_2025-10-24.md) | Daily；15m 触发核验；无直接 4H/1H bar | `10-23` 越过 `115.63` 但收盘约 `115.4084`；`10-24` 首次日线接受，回踩为 `not-occurred` | 事件/板块未核验；触发约 `114.2` 到首障碍 `115.49–115.63` 仅约 `1.3` | `strict-first-resistance-no-trade / not-BOP-baseline` |
| [`META 2024-09-11–10-11`](meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md) | 只有 Daily；无可验收 4H/1H/15m | `593.4` 是可见阻力，但没有上方接受；多日浅回调属于嵌套 H1/H2-like，不是 BOP 回踩 | 事件未核验；订单、结构止损、R/R 未冻结；首障碍拥挤 | `observation-only / no-new-positive` |
| [`TSLA 2025-08-28–09-05`](tsla_h1_h2_case_study_2025-08-28_2025-09-05.md) | Daily；60m 聚合的 `4H-like`；15m | 15m 只有同日“反应—回测—再推进”；未形成接受后的多日回踩；次日开盘跳过理论触发 | `338.90–339.00` 到首阻力 `343.33` 约 `0.59R`；实际开盘约 `348.00` 进入阻力簇 | `valid_no_trade_after_gap / not-multiday-BOP` |
| [`TSLA 2025-05-08–05-13`](tsla_range_after_sell_climax_2025-03-11_2025-05-13.md) | Daily；无 4H/1H/15m | 只有区间上沿后的突破接受/第二腿候选；没有记录突破后的多日回踩、守住、再离开或新 15m 确认 | 上沿 `285–307` 的角色转换、订单、止损、首障碍和 R/R 未重建 | `conditional-breakout-acceptance / no-new-positive` |
| [`TSLA 2026-05-15–05-22`](tsla_h1_h2_case_study_2026-05-15_2026-05-22.md) | Daily；60m 聚合的 `4H-like`；15m | 这是深度支撑反转/H1-H2-like，不是旧边界被接受后的 BOP 回踩；后续上涨不能倒灌 | 日线触发到第一主要阻力约 `0.72R`；低周期窄止损只能另立短线合同 | `deep-pullback-reversal / valid_no_trade / not-BOP` |
| [`TSLA 2025-12-08–12`](tsla_h1_h2_case_study_2025-12-08_2025-12-12.md) | Daily；60m；15m | H2-like 的强反应和日内深回测，不是突破后多日角色转换 | 触发约 `463.10` 到首阻力约 `467` 只有约 `0.2R`；日线直接追入应跳过 | `pattern-like / first-resistance-no-trade / not-BOP` |

三角形候选池也没有新增正例：TSLA 2025-09 仍只是状态切换候选；ASML 是区间内重复测试，RBLX 是失败突破，COIN/XOM 是扩张与重订边界，KLAC 是趋势旗形且首障碍过近。它们都没有同时完成事件闭环、接受后的多日回踩、角色转换守住、再次离开跟随和足够首障碍空间。

### 8.1 本轮裁决

本轮新增筛选的有效候选数为 `0`。没有一个案例同时满足：

```text
event-clean
parent-clear
old-boundary-preidentified
daily-acceptance
multi-day-retest-and-hold
re-departure-follow-through
actual-order-reconstructable
first-obstacle-space-positive
process-complete
```

因此正式保持：

> `BOP / event-clean / daily-accepted / multi-day-retest-held / first-obstacle-space-positive / process-complete`：**no-new-positive**。

下一次只有在获得可读的 Daily/4H/1H/15m 图表或同等完整的历史周期记录，并能核对事件、实际订单和首障碍后，才升级候选；不把 `breakout-acceptance`、H1/H2、同日回测或后续上涨改名为多日 BOP。

## 9. 相关入口

- [`BOP 突破回踩目录`](../patterns/06_breakout_pullback_bop/README.md)
- [`BOP 视觉证据缺口审计`](bop_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`BOP 视觉边界复核`](bop_visual_boundary_audit_2026-08-24_CN.md)
- [`优先 Pattern 代表性视觉候选矩阵`](priority_pattern_visual_candidate_matrix_2026-08-24_CN.md)

研究边界：只更新 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

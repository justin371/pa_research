# 八个 Pattern 的订单合同与 R/R 审计 V0.1

日期：2026-08-23  
状态：`visual-research / order-contract-audit / not-production`

本文件保留为 2026-08-23 的 PA Research 研究层历史交叉审计，不是当前回放器的输入模板。
为避免旧字段继续被当作活动入口，下面的统一订单卡已经收敛到 canonical 字段；五种订单合同
仍包含研究层的 `stop_limit` 与 `observation_only`，但当前 engine 只接受其中的三种可回放分支。

## 目的

形态判断、订单是否成立、订单是否成交、成交后是否有空间，是四个不同问题。本文件把已有的[`订单分支视觉协议`](order_branch_visual_protocol_CN.md)映射到八个主动 pattern，防止用后续走势补写成交或用低周期窄止损美化高周期 R/R。

## 五种订单合同

| 合同 | 什么时候研究 | 成交条件 | 不能假设的事 |
| --- | --- | --- | --- |
| `stop_confirmation` | 信号 K 已出现，需要价格证明继续走 | 真实越过冻结的触发价 | 只碰到、后来盈利或下一日上涨不等于成交 |
| `limit_retest` | 已知支撑/阻力、旧边界或角色转换区可能回测 | 价格真实回到预先定义的区域 | 没回测不能记成交；不能把任意当前价叫回测 |
| `market_close` | 强收盘接受、继续等待会改变交易假设 | 在收盘/接近收盘按实际可得价格成交 | 强 K 自动授权市价；不能忽略滑点和首障碍 |
| `stop_limit` | 需要触发确认但限制最差成交价 | 先触发，随后仍在 limit 范围成交 | 跳过 limit 仍算成交；成交未知时不能按普通 stop 计算结果 |
| `observation_only` | 形态像但空间、事件、数据或结构不合格 | 没有交易合同 | 观望是失败；后续盈利不能改写当时不应交易 |

开盘跳过原触发时，研究记录写 `actual_fill_or_open_skip: opening_skip / fill_unknown / no_fill`，
结果记录另写 engine 的 `fill_status: opening-skip / unproven / no-fill`，然后按实际可成交价重建或取消；
不能保留旧入场价、旧止损和旧 R/R。

## 统一订单卡

```text
contract_scope: deep_review / historical_context_only
as_of_time:
timezone:
session_state: premarket / RTH / after_hours / historical_close / unknown
timeframes_seen:
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
direction: long / short / no_valid_direction
pattern_state:
signal_bar:
confirmation_bar:
new_trigger:
order_price_or_zone:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
gap_policy: accept_open / skip / flag_only / not_applicable
actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable
structural_invalidation:
structural_stop:
first_independent_obstacle:
rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown
pre_entry_space_R:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
rough_R_R:
event_context: raw pre-entry event note (examples: none / earnings / macro / gap / other / unknown; dated/compound qualifiers allowed)
event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified
main_uncertainty_or_exclusion:
research_state: pattern_like / research_candidate / research_positive_conditional / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
```

历史材料中的 `decision_time`、`timeframe_and_parent_contract`、`trigger_or_zone`、
`actual_or_assumed_fill`、`structural_stop_zone`、`space_to_first_obstacle` 和 `final_status`
只作为旧字段引用时按以下关系阅读：分别对应 `as_of_time`、`timeframes_seen`/`contract_scope`、
`new_trigger` + `order_price_or_zone`、`actual_fill_or_open_skip`、`structural_stop` +
`structural_invalidation`、`rough_space_to_first_obstacle_R` 和 `research_state`/
`trade_state`/`gate_result`。这些旧名称不再作为统一订单卡的活动字段，也不能被 loader 当作
当前回放输入列。

## 八个 Pattern 的默认分支

| Pattern | 默认合同 | 可选合同 | 主要成交/风险审计 |
| --- | --- | --- | --- |
| H1/L1 | `stop_confirmation` 越过信号 K | 已知结构回测 `limit_retest`；强收盘才考虑 `market_close` | 第一次尝试失败则等待 H2/L2；结构止损覆盖 B/父级，首障碍不能贴触发 |
| H2/L2 | `stop_confirmation` 越过第二次信号 K | 低周期确认、明确支撑/阻力回测 | 第一次尝试不能与第二次成交混算；低周期不能压窄父级止损 |
| ABC 延续 | C 信号后的 `stop_confirmation` | 缺口后重订、角色转换回测 | B 被接受成区间或新趋势时旧合同失效；MM 不能替代首障碍 |
| 区间边缘二次入场 | `limit_retest` 或边缘反应后的 `stop_confirmation` | 失败突破重返后的反向 stop | 上沿/下沿和中线目标分开；区间中部不交易；边界外接受后重建 BOP |
| 失败突破/高潮 | 反向 `stop_confirmation` | 失败边界/角色转换 `limit_retest` | 单根影线不是成交；原方向重新接受则失败 thesis 失效，切 BOP |
| BOP | 接受突破后的 `stop_confirmation` 或 `market_close` | 突破回踩 `limit_retest` | 旧边界外收盘和跟随先成立；回踩未发生不能假设 limit 成交 |
| MTR | 第二次反向 `stop_confirmation` | 颈线/失败边界回测 `limit_retest` | 双顶/三推只提供证据；结构破坏和第二次确认后才冻结母级止损 |
| 三推/H3-L3 | 反向 `stop_confirmation`，仅在衰竭候选 | 第三推边界回测 `limit_retest`；扩张时 `observation_only` | 第三次计数不等于反转；扩张/高潮、区间重复测试和通道延续分别处理 |

## R/R 审计顺序

1. 先冻结订单类型、决策时点、触发/回测区域和可能成交价；
2. 再放结构止损，覆盖正常测试和让 thesis 失效的结构；
3. 从实际入场方向找最近的独立支撑/阻力、区间中线、角色转换或磁铁；
4. 若第一障碍太近或实际成交后空间消失，输出 `valid_no_trade`，不跳到远端 MM；
5. 只有近端障碍被接受/穿越后，才研究 MM、AB=CD、区间高度或延伸目标；
6. 跳空、财报或板块/市场状态改变时，重算合同；旧 R/R 不继承。

`1R`、`2R` 只作粗略语言：第一障碍不足约 `1R` 通常不值得建立新仓；大约 `2R` 只是更完整波段的空间参考，不是固定胜率门槛。

## 订单状态转换

```text
pattern_like
  → signal_ready
  → order_pending
  → triggered / filled
  → working
  → target_or_management / failed_thesis
```

允许的分支：

- `order_pending → opening_skip → reprice_after_gap`：实际成交、止损和首障碍全部重算；
- `order_pending → not_filled → limit_retest`：只有回到预先存在的结构区才能建立新合同；
- `triggered → no_follow_through → observation_only`：没有跟随不能用后续结果补成交质量；
- `working → original_structure_reaccepted`：原 thesis 失效，转 BOP 或退出，不继续沿用旧目标；
- `working → first_obstacle_reached`：先管理近端障碍，之后再决定是否持有 MM 延伸。

## 案例对照

| 案例 | 订单问题 | 正确输出 |
| --- | --- | --- |
| [`TSLA 2025-03-04 284 回测`](tsla_abc_playbook_2025-03-04_284_retest.md) | 原 sell-stop 被跳空越过；284 附近回测是另一笔 limit | 原 stop 不按理想价成交；回测合同单独审计 |
| [`KLAC 2025-06-02/03 H2`](klac_h2_case_study_2025-05-07_2025-06-03.md) | H2 buy-stop 可定义，但日线结构止损到上方首阻力空间有限 | 形态候选与日线 no-trade/低周期独立合同分开 |
| [`TSLA 2025-09 BOP`](tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | 原 MTR/区间合同被突破接受否定 | 建立新 BOP 合同，不能继续用旧反向止损 |
| [`GOOGL 2024-03-18`](googl_bullish_h1_gap_trigger_boundary_2024-03-04_2024-03-22.md) | buy-stop 被开盘跳过，首阻力贴近 | 重订后空间不合格，`valid_no_trade` |
| [`QCOM 2024-07-24`](qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md) | 空头方向正确，但开盘重订价把约 `1.37R` 压到约 `0.48R` | 理想订单和实际合同分开，实际分支观望 |

## 验收标准

- 八个 pattern 都有明确默认订单分支和可选分支；
- `stop`、`limit`、`market-close`、`stop-limit` 的语义和成交条件不混淆；
- 原始触发、实际成交、开盘跳过、未回测和成交未知都有独立状态；
- 结构止损先于 R/R，首障碍先于 MM；
- 低周期确认与低周期独立交易不合并；
- “形态像但不交易”保留为有效输出；
- 本文件不生成订单、不连接 Execution Agent、不修改 Codex Trading。

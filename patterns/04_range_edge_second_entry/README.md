# 交易区间边缘二次入场

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补区间上沿/下沿、边缘尝试和区间目标。`first_magnet` 只作为历史别名，新记录统一写 `first_independent_obstacle`。

## 研究目的

研究区间顶部卖出、底部买入，以及边缘失败突破后的第二次机会。区间逻辑与趋势 ABC 逻辑分开：区间中部不追，不把区间摆动累计成趋势腿；同一边缘的第三次有意义测试可以转入独立的 `range_edge_three_push` 研究分支。

## 共同图表范围前置

该入口的证据头还必须记录 `data_status: historical / delayed / live_confirmed / incomplete`、`as_of_time`、`chart_scope` 和 `timeframes_seen`；历史、延迟、实时已确认与不完整不能互换。

进入区间边缘判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。对包含 A/B 语义的案例核对强 A 与受控 B；若涉及 H1/H2/L1/L2，Daily EMA20/50 还必须与方向一致。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能凭区间局部外形升级为可交易候选。

## 视觉定义

- 父级是成熟或至少可识别的双向交易区间；
- 价格位于上沿或下沿，而不是区间中部；
- 第一次边缘尝试失败，或刺破后重新接受回区间；
- 第二次方向尝试出现 H2/L2 或等价确认；
- 目标先看区间边缘、中点或另一侧磁铁，不能保证到达整段区间高度。

区间边缘三推是本目录与三推目录的交叉入口：A 腿可以普通或偏弱，但第三推必须在上沿/下沿而非中部，并出现拒绝、假突破回区间或反向信号 K。上沿只研究空头、下沿只研究多头；确认触发后仍需审计结构止损和到中线的空间。

## 最小视觉协议

```text
range_state: mature / developing / transition / not_range
upper_zone:
lower_zone:
midpoint:
edge_attempt_1:
edge_failure_or_reentry:
edge_attempt_2:
order_branch: limit_retest / stop_confirmation / market_close / stop_limit / observation_only
branch_role: role_reversal_retest / same_contract / management
structural_stop:
first_independent_obstacle:
target_path: midpoint / opposite_edge / independent_magnet
second_leg_trap_risk:
```

只有当上下沿有反复测试、双方突破缺少持续接受、K 线重叠和反向摆动明显时，才进入这个目录。20 根左右或更多 K 线可以作为成熟度提示，但不能单独定义区间。

## 区间 H/L 与趋势 H/L 的区别

- 区间底部的第一次多头反应可以记为 H1，失败后同一下沿的第二次有效反应可以记为 H2；
- 区间顶部的第一次空头反应可以记为 L1，失败后同一上沿的第二次有效反应可以记为 L2；
- 这些数字表示边缘尝试次数，不是开放趋势回调的连续腿；
- 价格进入中部、接受区间外或角色转换后，旧边缘计数重置；
- 从下沿走到上沿只是区间摆动，不能自动叫 ABC 第二腿。

## 订单与目标分支

1. `limit-edge`：边缘区域已由左侧结构确认，预先等待正常测试；止损在边缘外，首目标先看中线。
2. `stop-confirmation`：第一次反应不清楚，等第二次信号 K 外确认；成交后重新审计到中线/另一边缘的空间。
3. `failed-breakout-reentry`：价格先越过边缘又收回区间；原突破、重返区间和后续二次入场是不同合同。
4. `observation_only`：区间中部、第一目标太近、结构止损过宽、事件窗口或区间边界未确认。

只有区间外突破被收盘接受、出现跟随并且回测守住后，才可以重建新的趋势合同；不能把区间边缘止损与突破后止损合并。

## 主要陷阱

第二腿陷阱、边缘第一次刺破被误当突破、区间中部追单、把 EMA 触碰当成趋势形态、把后续突破结果倒写成原来的区间交易。

## 当前案例对照

| 案例 | 视觉分类 | 当前结论 |
| --- | --- | --- |
| [`TSLA 2025-03-11–05-13`](../../research/tsla_range_after_sell_climax_2025-03-11_2025-05-13.md) | 卖出高潮后形成宽区间；下沿反应到上沿是区间摆动 | `second-leg-trap-control`；`05-08` 后才重新审计突破接受 |
| [`RBLX 2024-03-18–04-05`](../../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md) | 下沿测试/开盘上冲失败 | 信号 K、开盘重订和首磁铁否决，`valid_no_trade` |
| [`TSLA 2024-03-04–03-14`](../../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md) | 上沿失败后的 L1/L2 空头反应 | 静态空间尚可但过程先破止损，`conditional / process-stop-first` |
| [`IWM 2024-04-17–04-30`](../../research/range_edge_second_entry_framework_CN.md) | 下沿二次测试、limit 与 stop 两种合同 | limit 约 1R 边界，stop 因开盘/前高拥挤，`valid_no_trade` |
| [`QCOM 2025-02-21–03-28`](../../research/qcom_bearish_abc_range_b_boundary_2025-02-21_2025-03-28.md) | 宽 B/过渡区 | 重置趋势计数，不能把区间内下跌叫 L2 |

专项审计见[`交易区间边缘二次入场专项视觉证据审计`](../../research/range_edge_second_entry_visual_evidence_gap_audit_2026-08-24_CN.md)。当前已经形成“先判区间、再判边缘、最后判订单”的工作语言，但尚无事件过滤通过、首磁铁宽裕且过程完整的标准上下沿正例；保持 `no-new-positive`。

## 现有入口

- [`区间边缘二次入场框架`](../../research/range_edge_second_entry_framework_CN.md)
- [`RBLX 区间边界案例`](../../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)
- [`TSLA 卖出高潮后的区间`](../../research/tsla_range_after_sell_climax_2025-03-11_2025-05-13.md)
- [`区间边缘二次入场专项视觉证据审计`](../../research/range_edge_second_entry_visual_evidence_gap_audit_2026-08-24_CN.md)

## 当前目标验收

- 能从完整图表先确认区间，而不是先寻找 H/L 标签；
- 能区分上沿/下沿二次入场、失败突破重返和区间中部 no-trade；
- 能把 second-leg trap 与趋势 ABC 分开；
- 能分别记录 limit、stop、retest 的成交和 R/R；
- 目标顺序固定为中线、另一侧边缘/独立磁铁，接受突破后才重新使用趋势 MM。

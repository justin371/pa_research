# 交易区间边缘二次入场

状态：`visual-research / provisional / primary`

## 研究目的

研究区间顶部卖出、底部买入，以及边缘失败突破后的第二次机会。区间逻辑与趋势 ABC 逻辑分开：区间中部不追，不把区间摆动累计成趋势腿。

## 视觉定义

- 父级是成熟或至少可识别的双向交易区间；
- 价格位于上沿或下沿，而不是区间中部；
- 第一次边缘尝试失败，或刺破后重新接受回区间；
- 第二次方向尝试出现 H2/L2 或等价确认；
- 目标先看区间边缘、中点或另一侧磁铁，不能保证到达整段区间高度。

## 最小视觉协议

```text
range_state: mature / developing / transition / not_range
upper_zone:
lower_zone:
midpoint:
edge_attempt_1:
edge_failure_or_reentry:
edge_attempt_2:
order_branch: limit-edge / stop-confirmation / retest / observation-only
structural_stop:
first_obstacle:
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
4. `observation-only`：区间中部、第一目标太近、结构止损过宽、事件窗口或区间边界未确认。

只有区间外突破被收盘接受、出现跟随并且回测守住后，才可以重建新的趋势合同；不能把区间边缘止损与突破后止损合并。

## 主要陷阱

第二腿陷阱、边缘第一次刺破被误当突破、区间中部追单、把 EMA 触碰当成趋势形态、把后续突破结果倒写成原来的区间交易。

## 现有入口

- [`区间边缘二次入场框架`](../../research/range_edge_second_entry_framework_CN.md)
- [`RBLX 区间边界案例`](../../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)
- [`TSLA 卖出高潮后的区间`](../../research/tsla_range_after_sell_climax_2025-03-11_2025-05-13.md)

## 当前目标验收

- 能从完整图表先确认区间，而不是先寻找 H/L 标签；
- 能区分上沿/下沿二次入场、失败突破重返和区间中部 no-trade；
- 能把 second-leg trap 与趋势 ABC 分开；
- 能分别记录 limit、stop、retest 的成交和 R/R；
- 目标顺序固定为中线、另一侧边缘/独立磁铁，接受突破后才重新使用趋势 MM。

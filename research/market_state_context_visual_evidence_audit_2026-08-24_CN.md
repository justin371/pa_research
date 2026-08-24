# 市场状态与父级背景视觉证据审计

日期：`2026-08-24`  
状态：`visual-research / cross-pattern / provisional / not-statistical`

## 审计目的

检查 pattern 是否被放在正确的父级状态中：开放趋势、成熟区间、区间边缘、过渡和高潮不能共享同一套计数和订单逻辑。

## 当前合同

### C1：先判状态，再数 H/L 或 ABC

完整左侧如果显示区间中部、上下沿反复或父级过渡，局部 H2/L2/ABC 只能是 `pattern_like`；不得因为后来走出一段方向波动，就倒推当时已经是趋势第二腿。

### C2：区间成熟度看结构，不只看根数

20 根左右可以提示成熟，但必须同时观察上下沿、双方失败突破、重叠、反向摆动和接受度。区间先标区域，不标一条精确线。

### C3：边缘与中部分开

区间边缘可研究反应、失败突破和二次入场；中部默认观望。区间内部摆动到另一边缘不是 ABC 第二腿，追入有 second-leg trap 风险。

### C4：突破接受后重建状态

边界外强收盘、跟随和回测守住后，才从区间合同切换到趋势/BOP 合同；旧边缘止损、计数和目标不能继续沿用。

## 案例矩阵

| 案例 | 父级状态 | 关键视觉问题 | 当前结论 |
| --- | --- | --- | --- |
| TSLA `2025-03-11`–`2025-05-13` | 卖出高潮后宽区间 `214–307` | `2025-04-22` 到上沿是区间摆动，不是 ABC 第二腿；`2025-05-08` 后才重新评估突破 | `range / second-leg-trap-control / state-reset-after-acceptance` |
| RBLX `2024-03-18`–`2024-04-05` | 宽区间与下沿反应 | 局部 H1-like、开盘上冲失败和中部磁铁不能叫开放趋势 | `range-edge / failed-breakout / valid_no_trade` |
| QCOM `2025-02-21`–`2025-03-28` | 强 A 后宽 B/过渡区间 | 均线反复穿越，后续下跌不能自动叫 L2 | `transition / count-reset / boundary` |
| TSLA `2024-03-04`–`2024-03-14` | 区间上沿反应 | L1 失败后 L2 有条件空间，但路径后来先破结构止损 | `range-top-L2 / process-stop-first / conditional` |
| IWM `2024-04-17`–`2024-04-30` | 区间下沿二次测试 | limit 有约 1R 边界；stop 因前高和开盘重订拥挤 | `range-bottom-second-test / valid_no_trade` |
| TSLA `2025-09-08`–`2025-09-12` | 阻力下反复测试后突破接受 | `09-11` 强收盘、跟随、回测守住，旧反向状态结束 | `failed-thesis → BOP acceptance` |
| KLAC `2025-10-14`–`2025-10-24` | 开放趋势中强 A、浅 B | 强 A 和嵌套趋势背景支持 H1，但近端前高仍是障碍 | `open_trend / late-controlled / strict-first-obstacle-branch` |

## 必须保留的五类对照

### 1. 开放趋势强 A

KLAC `2025-10` 的低重叠、缺口和连续收盘可以作为开放趋势强 A 参考，但触发上方前高仍需单独审计。强 A 只决定优先看延续，不取消首障碍。

### 2. 区间中部 second-leg trap

TSLA `2025-04-22` 后的强上涨首先是从下沿到上沿的区间摆动。把它写成第二腿会把区间中部/上沿的追价风险隐藏起来；只有 `2025-05-08` 后的接受证据出现，才可重建新的趋势合同。

### 3. 区间边缘反应

TSLA `2024-03` 和 IWM `2024-04` 都有边缘二次测试，但静态空间、成交路径和止损仍要单独审计。边缘位置提高质量，不保证交易一定成功。

### 4. 突破接受重建

TSLA `2025-09` 在 `09-08`–`09-10` 仍是阻力测试；`09-11` 后才建立 BOP 合同。不能把突破前的三推/失败突破假设继续带入突破后。

### 5. 高潮后转区间

TSLA `2025-03` 的卖出高潮与 MM/左侧支撑重合，随后进入宽区间。目标到位后先预期反弹/平衡，不自动预期大反转；父级状态改变时要重建目标和计数。

## 统一审计字段

```text
decision_time:
timeframe:
parent_state:
range_upper/lower/midpoint:
left_major_levels:
directional_leg_quality:
current_location:
attempt_lineage:
abc_or_hl_allowed:
second_leg_trap_risk:
breakout_acceptance:
order_contract:
structural_stop:
first_obstacle:
rough_R_R:
state_reset_condition:
final_status:
```

## 当前结论

可迁移原则是：先看完整左侧和父级状态；开放趋势优先研究强 A 后回调，成熟区间优先看上下沿，中部观望；区间内部不强行继承 ABC/趋势 H-L；second-leg trap 是状态误读而非单独 K 线形态；突破接受后重建合同；高潮后先考虑平衡/小反转再谈 MTR。

本层仍为 `provisional`，不产生胜率、不进入 Codex Trading、不连接 Execution Agent。只有新案例提供新的状态切换、边缘订单或对称路径时，才继续增加深审。

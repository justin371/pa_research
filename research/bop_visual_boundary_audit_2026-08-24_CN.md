# BOP / 突破接受与突破回踩视觉边界复核

日期：`2026-08-24`；状态：`visual-research / provisional / not-statistical`

## 状态机

```text
事前边界 → 影线测试/突破 K → 收盘接受 → 跟随
→ 是否回踩旧边界 → 角色转换守住/重新进入 → 新合同或失败突破
```

只有左侧事前可见的主要高低点、区间边界或角色转换区，才有资格成为 BOP 边界。影线越过不是接受；接受后原 MTR、三推、区间反转和 H/L 合同必须废弃或重建。

## 分流矩阵

| 视觉状态 | 合同 | 失效 |
| --- | --- | --- |
| 强收盘越过边界并跟随，无回踩 | `breakout-acceptance / gap-and-go` | 重新收回旧边界 |
| 越过后回测旧边界并守住 | `breakout-pullback / limit-or-stop-reentry` | 重新接受旧区间 |
| 只有影线或跟随不足 | `test / failed-breakout-candidate` | 需等待失败或接受 |
| 开盘跳过旧 stop | `opening-reprice` | 按实际价重算或取消 |
| 低周期先确认而高周期未改变 | `low-cycle-confirmation` | 不得冒充高周期 BOP |

## 案例裁决

- `TSLA 2025-09-08–09-12`：`09-08–10` 是阻力测试；`09-11` 强收、跟随和不回旧区间，切换到 BOP acceptance，不再保留旧 MTR 空头。
- `TSLA 2025-03-04`：`277` 原 sell-stop 被跳过，`283.8–284.3` 回测失败是独立 limit-retest；首支撑约 `1.1R`，不是宽裕标准。
- `QCOM 2024-07-24`：方向正确但开盘重订把首支撑空间压缩，且后续进财报窗口，`valid_no_trade`。
- `GOOGL/WMT/BKNG`：跳过原 buy-stop，未回测或首障碍过近；不能用后来延伸假设原订单成交。
- `NKE 2025-10-28`：真实回测存在，但仍是 ABC/L1 分支和事件/板块边界，不作为干净 BOP 基准。

## 统一输出

```text
prior_boundary:
prior_state:
breakout_bar: wick_only / accepted_close / gap_acceptance / unclear
follow_through:
pullback: none / real_retest / not_yet / reentered_old_range
role_reversal:
old_contract: preserved / invalidated / replaced
new_order: stop / limit-retest / market-close / observe
actual_fill_or_open_skip:
structural_stop:
first_obstacle:
rough_R_R:
decision: candidate / conditional / valid_no_trade / failed_breakout
```

当前结论：BOP 的核心是状态切换和合同重建，不是追逐大 K。TSLA 2025-09 是接受样本，TSLA 2025-03 是回测样本；两者不能合并成“每次突破都会回踩”。目前仍无事件干净、父级清楚、角色转换明确、首障碍宽裕且路径完整的普通 BOP 正例，保持 provisional。

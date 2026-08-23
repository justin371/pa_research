# 失败突破与高潮

状态：`visual-research / provisional / primary`

## 研究目的

把“边界未被接受的失败突破”和“成熟趋势后的高潮扩张”分开，再判断它们是小反转、交易区间、MTR 候选，还是原方向继续。

## 视觉定义

- 事前可见的区间边缘、主要高低点或角色转换位；
- 价格越过边界后没有接受，或出现强扩张后跟随减弱；
- 反向结构被第二次确认，且到第一障碍有空间；
- 原方向重新强收盘接受时，失败突破 thesis 失效，转入 BOP 分支。

## 四状态分流

| 状态 | 必须看到的证据 | 默认处理 |
| --- | --- | --- |
| `continuation_or_climax` | 原方向仍有收盘接受和跟随；扩张可能只是趋势延续 | 不逆势；把高潮当风险提示，等回调或新的结构 |
| `failed_breakout_candidate` | 事前边界被越过，但尚未被区间外接受 | 等收回原侧、反向跟随和第二次确认 |
| `small_reversal_or_range` | 第一反向运动出现，但尚未破坏主要结构 | 预期小反转、两腿回调或交易区间，不直接称 MTR |
| `MTR_candidate` | 主要位置、失败/减速、结构破坏、第二次确认和空间同时存在 | 才进入 MTR 目录的高级反转研究 |

单根影线、单根反向 K、盘中回测或事后盈利都不能单独把候选升级为已确认失败突破。

## 最小审计卡

```text
preexisting_boundary:
parent_state: trend / range / channel / transition
expansion_or_test:
close_acceptance: accepted / rejected / unclear
reentry_to_original_side:
first_reverse_structure:
second_confirmation:
structural_stop:
first_independent_obstacle:
rough_R_R:
order_branch: reverse-stop / limit-retest / market-close / observation-only
original_direction_reaccepted:
final_state: continuation / small-reversal / range / MTR-candidate / no-trade
```

## 与相邻 pattern 的边界

- 区间边缘失败突破优先连接[`区间边缘二次入场`](../04_range_edge_second_entry/README.md)；
- 主要结构真正改变控制权才连接[`MTR`](../07_mtr_reversal/README.md)；
- 原方向强收盘越过边界并跟随时，切换到[`突破回踩/BOP`](../06_breakout_pullback_bop/README.md)；
- 第三推扩大、跳空或加速时，连接[`三推/H3-L3`](../08_three_push_h3_l3/README.md)，不自动写成楔形衰竭。

## 订单与风险

- 默认先研究反向 stop-confirmation；牺牲价格换取失败被确认的证据；
- limit-retest 只放在已知结构回测区，未回测不得假设成交；
- market/close 只有在反向结构已破坏、跟随清楚且首障碍仍有空间时才保留；
- 止损放在失败边界/高潮极端或反向结构外，不能用单根信号 K 极值压窄；
- 第一独立障碍不足约 1R，或财报/重大事件扭曲几何时，记录 `valid_no_trade`。

## 订单与管理

默认研究反向 stop-confirmation；结构回测 limit 是独立分支。高潮后第一结果通常是小反转或区间，不自动升级为主要反转。止损放在失败边界/结构极端外，目标先看最近磁铁。

## 现有入口

- [`失败突破与高潮框架`](../../research/failed_breakout_climax_visual_framework_CN.md)
- [`TSLA 2025-03 高潮与区间`](../../research/tsla_range_after_sell_climax_2025-03-11_2025-05-13.md)
- [`COST 高潮边界`](../../research/cost_bearish_abc_climax_boundary_2024-07-11_2024-07-18.md)
- [`三推压力状态框架`](../../research/three_push_pressure_state_framework_CN.md)

## 当前目标验收

- 能把测试、失败候选、已确认失败和原方向接受分开；
- 能区分高潮后小反转/区间与真正 MTR；
- 能在 BOP 接受时主动废弃旧的失败突破 thesis；
- 能分开反向 stop、limit-retest、market/close 和观望的成交/R/R；
- 保留至少一个“形态像但首障碍否决”的边界，不把后续走势改写成高胜率样本。

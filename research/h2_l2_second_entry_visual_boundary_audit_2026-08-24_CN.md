# H2/L2 第二次入场视觉边界复核

日期：`2026-08-24`；状态：`visual-research / provisional / not-statistical`

## 第二次入场的因果链

```text
同一父级与回调 lineage → H1/L1 有意义但失败/无跟随
→ B 后段仍受控 → 第二次位置测试 → signal K/trigger
→ follow-through → 结构止损/首障碍 → H2/L2 或降级
```

若第一次只是连续 K 线中的局部波动，不能为了得到 H2/L2 而强行计数；若 B 已被反向接受、父级进入区间或出现新的母级极值，旧计数必须重置。

## 分流矩阵

| 情况 | 研究标签 | 处理 |
| --- | --- | --- |
| 同一回调、第一次失败、第二次在支撑/阻力确认 | `H2/L2-candidate` | 分开 setup、signal、trigger 和 follow-through |
| 区间同一边缘的第二次反应 | `range-edge-second-entry` | 用边缘/中线目标，不继承趋势腿计数 |
| 第一次失败后反向压力扩大 | `rebuild-or-no-trade` | 等新趋势/区间合同，不用 H2 挽救 |
| 形态清楚但首障碍拥挤 | `valid_no_trade` | 记录形态，跳过交易 |
| 开盘跳过或低周期另有窄止损 | `contract-reset` | 按实际成交重算，不能与日线合同合并 |

## 案例裁决

- `KLAC 2025-05-07–06-03`：支撑簇、EMA 汇合和第二次测试清楚，属于多头条件候选；`79.03–79.79` 首阻力仍需优先处理。
- `CRWD 2024-09-11–10-11`：深 B 前段卖压强，后段在 `68.17` 稳定后才恢复 H2；低周期触发与收盘确认是不同合同。
- `TSLA 2025-08-06–08-22`：形态成立候选，但日线首阻力拥挤；15m 可另立短线合同，不能修饰日线 R/R。
- `TSLA 2024-03-04–03-14`：L2 计数与静态空间清楚，实际路径先破结构止损；记 `process-stop-first / range-edge-boundary`。
- `TSLA 2024-07`：L2 结构和目标可研究，但财报缺口改变波动，记事件驱动条件样本，不与普通趋势合并。
- `QCOM/RBLX`：父级过渡或区间，局部 H2/L2-like 不足以继承旧 ABC；记 `count-reset / observation-only`。

## 统一输出

```text
parent_state:
lineage_status: same_lineage / reset / unclear / pending
lineage_id:
first_attempt: failed / no_follow_through / not_meaningful / accepted
second_location:
internal_label: H2 / L2 / none / pending
signal_quality:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
structural_stop:
first_independent_obstacle:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
fallback: continue / H3-L3 / MTR / range-edge / new-trend
```

当前结论：H2/L2 是失败信息和第二次位置测试的组合，不是数字标签。多头已有 KLAC/CRWD 条件候选，空头有计数与事件/路径边界但仍无事件干净、开放趋势、首障碍宽裕的标准正例；因此保持 provisional，不冻结生产规则。

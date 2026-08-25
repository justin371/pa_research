# 交易区间边缘二次入场视觉边界复核

日期：`2026-08-24`；状态：`visual-research / provisional / not-statistical`

本文件是`contract_scope: stage_1_fast_screen`的边界审计；完整候选仍必须补齐[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)中的方向、事件闸门、订单、结构止损和第一独立障碍字段。

## 区间先于计数

成熟区间不是只看根数，而看上下沿反复、双方突破失败、重叠、中线缺乏接受和价格回到内部。20 根左右只能作成熟度提示。先冻结：

```text
contract_scope: stage_1_fast_screen
direction: long / short / no_valid_direction
range_state / upper_zone / lower_zone / midpoint
edge_attempt_1 / edge_failure_or_reentry / edge_attempt_2
order_branch / structural_stop / first_independent_obstacle / target_path
```

区间内的 H1/H2/L1/L2 只描述同一边缘的尝试次数，不表示开放趋势的腿数；进入中部、接受区间外或建立新母级方向时计数重置。

## 分流矩阵

| 外观 | 准确标签 | 默认处理 |
| --- | --- | --- |
| 下沿第二次多头反应 | `range-bottom-second-entry` | 先看中线，再看上沿；limit/stop 分开 |
| 上沿第二次空头反应 | `range-top-second-entry` | 先看中线，再看下沿；不把影线当失败确认 |
| 越过边缘后收回区间 | `failed-breakout-reentry` | 等反向跟随或回测合同 |
| 下沿到上沿的强上涨 | `range-swing / second-leg-trap` | 不叫 ABC 第二腿，不在中部追 |
| 区间中部局部 H2/L2 | `observation-only` | 前方磁铁和双向风险通常否决 |

## 案例裁决

- `TSLA 2025-03-11–05-13`：卖出高潮后 `214–307` 宽区间；`04-22` 是下沿反应，`04-22–04-29` 是区间摆动，`05-08` 接受后才重建趋势合同。
- `RBLX 2024-03-18–04-05`：下沿上冲失败且信号 K 收弱，中线很快成为磁铁，`valid_no_trade`。
- `IWM 2024-04-17–04-30`：同一边缘同时展示 buy-limit 与 buy-stop；入场、止损、首磁铁不同，不能合并结果。
- `TSLA 2024-03-04–03-14`：上沿 L2-like 形态清楚、静态空间可看，但路径先破结构止损，`process-stop-first`。
- `QCOM 2025-02-21–03-28`：强 A 后进入过渡/宽区间，局部下跌不继承 L2，`count-reset`。

## 订单与目标纪律

- `limit-edge`：边缘区域事前清楚且允许测试；未触及不算成交，止损通常较宽。
- `stop-confirmation`：第二次 signal K 外确认；若接近中线/另一边缘，触发后空间可能已消失。
- `failed-breakout-reentry`：旧边界、重返区间和反向跟随是独立合同。
- 结构止损放在边缘测试极端外；第一磁铁优先中线/左侧独立结构，MM 只作后续目标。
- 首磁铁不足约 1R、事件未清、开盘跳过或区间状态不清时，输出 `valid_no_trade`。

当前结论：区间边缘逻辑可以稳定阻止“区间内部第二腿”误读，但本轮仍没有事件干净、上下沿清楚、首磁铁宽裕且过程完整的标准正例；保持 provisional，不把区间交易改写成趋势或量化规则。

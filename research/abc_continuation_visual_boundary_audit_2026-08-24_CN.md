# ABC 趋势延续视觉边界复核

日期：`2026-08-24`；状态：`visual-research / provisional / not-statistical`

## 统一 ABC 复核卡

```text
parent_state → A_quality → B_lineage/pressure → location
→ H1/H2 or L1/L2 C trigger → follow-through
→ structural_stop → first_obstacle → MM/AB=CD → decision
```

A、B、C 是决策时点的结构描述，不是事后把未来走势切成漂亮的三段。局部腿和父级腿同时存在时，保留 `local_anchor` 与 `parent_anchor`；区间中部的摆动不自动成为 ABC。

## B 腿与状态分流

| 观察 | 结论 |
| --- | --- |
| 浅或时间整理、反向压力后段收缩 | `controlled-B`，可先找 H1/L1 |
| 前段强反向压力，后段在结构位稳定 | `deep-but-late-controlled-B`，H1 降级、H2/L2 保留 |
| 反向推进扩张并接受关键结构 | `uncontrolled-B`，旧 ABC 结束，重建趋势/区间 |
| 父级成熟区间、价格从一边摆向另一边 | `range-swing / second-leg-trap`，不继承趋势第二腿 |
| 低点/高点被接受且 C 已展开 | 旧计数重置，不能把后续第三天叫 H3/L3 |

## 案例裁决

- `KLAC 2025-05-07–06-03`：强 A、支撑/EMA 汇合、深但后段稳定 B，H2/C 条件候选；首阻力先于 MM。
- `CRWD 2024-09-11–10-11`：A 有跳空加速，B 前强后稳，H2-like 可研究但非普通无事件基准。
- `TSLA 2025-08-06–08-22`：局部 ABC 外形成立，但父级仍带大区间恢复色彩；日线前高阻力拥挤，15m 短线合同必须独立。
- `MDT 2025-05-23–07-02`：普通 A、过渡父级、深但后段受控 B；保留 pattern_like，不升级无条件趋势样本。
- `NFLX/TSM 2025-02–03`：空头 A/L1-like 可读；TSM gap-reprice 改变订单，不能与普通 L1 合并。
- `CME 2026-05-20–06-17`：方向性空头 A 但父级过渡、B 较深、首支撑近；`observation-only`。
- `TSLA 2025-03-11–05-13`：卖出高潮后宽区间；`04-22` 到上沿是区间摆动，不是 ABC 第二腿，`05-08` 接受后才重建。

## 目标与交易合同

MM/AB=CD 只作空间和后续目标。入场前先看结构止损到第一独立障碍；首障碍过近时，即使 C 后来走到 MM，也记 `valid_no_trade`。stop、limit-retest、低周期确认和开盘重订是不同合同；实际成交改变后必须重算 R/R。

## 当前结论

ABC 的视觉语言已足以做第一轮筛选：先找有方向的 A，再判断 B 是否仍是同一回调，最后用 H1/H2 或 L1/L2 作为 C 的确认入口。当前没有事件干净、双向、开放趋势、首障碍宽裕且路径完整的通用正例，因此保持 provisional；优先价值是正确排除区间摆动、B 失控、事件重订和空间不足，而不是追求固定胜率。

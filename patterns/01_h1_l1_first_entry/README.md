# H1 / L1：第一次入场

状态：`visual-research / provisional / priority-required`

## 研究目的

实现强方向 A 腿后的第一次恢复：多头看 H1，空头看 L1。H1/L1 不是“碰到 EMA 后的第一根 K”，而是回调结束、方向尝试重新出现并位于有意义结构位置的候选。

## 视觉定义

- 背景是开放趋势、方向许可清楚，而不是交易区间中部；
- A 腿方向性明显：收盘有压力、重叠较少、有跟随；
- B 回调较浅，或主要以时间整理完成；
- 第一次方向恢复在支撑/阻力、前高/前低、突破区或 EMA 汇合处出现；
- 信号 K 质量和后续确认足够，且第一障碍不贴着触发价。

## 研究分支

- `candidate`：强 A + 受控 B + 位置清楚 + 有空间；
- `boundary`：形态像，但 A 普通、位置模糊、首障碍拥挤或触发被跳空；
- `no_trade`：区间中部、第一尝试太晚、结构止损过宽或事件过滤失败。

## 入场审计

默认先研究 signal K 高/低点外的 stop-confirmation。若使用低周期确认，必须说明它是在确认同一高周期合同，还是另立短线合同。止损放在父级结构失效处，不因为想提高 R/R 而压进正常波动。

## 现有入口

- [`H1/H2 优质定义`](../../research/h1_h2_quality_definition_CN.md)
- [`ABC 与 H/L 统一范围`](../../research/abc_h1_h2_h3_l1_l2_l3_scope_CN.md)
- [`COST H1 首障碍边界`](../../research/cost_bullish_h1_first_obstacle_boundary_2024-05-13_2024-05-16.md)
- [`TSLA ABC/H1/H2 比较`](../../research/tsla_abc_h1_h2_comparison_matrix.md)

## 暂不冻结

不设固定实体百分比、成交量阈值或 EMA 距离；先用强 A、B 后段压力变化、位置和首障碍做视觉判断。

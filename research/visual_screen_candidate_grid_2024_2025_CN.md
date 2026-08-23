# 2024–2025 候选网格轻量视觉筛选

日期：2026-08-23  
状态：`visual-screen / pattern-triage / no-deep-audit`

## 目的与数据边界

本轮只用完整日线做第一阶段视觉快筛，目的不是扫描胜率，也不是寻找必须交易的正例。数据来自 Futu OpenD 的历史 QFQ 日线，窗口覆盖 `2024-01-02`–`2025-12-29`；数据是收盘后历史数据，不是实时行情。本轮没有使用低周期、财报公告核验或精确 R/R，也没有下单。

筛选的标的：`AMD`、`QCOM`、`MU`、`HD`、`JPM`、`NKE`、`LLY`、`AVGO`、`AMAT`、`CSCO`、`TXN`、`NOW`。

## 快筛结果

| 标的 | 第一眼看到的结构 | 主要否决或保留点 | 处置 |
| --- | --- | --- | --- |
| `JPM` | 长期开放上涨骨架，局部有 A→B→再推进 | 多个嵌套尺度；部分关键恢复靠近财报窗口，不能直接冻结成普通 ABC | `pattern_like / nested-lineage-and-event-boundary` |
| `CSCO` | 2024 年中后段逐步恢复、后续走强 | 早期 A 与 B 重叠较多，父级更像过渡/宽区间，不够干净 | `boundary / ordinary-A-unclear` |
| `QCOM` | 高位后有明显空头推进，外形可画出反弹再下行 | 大跳空和状态变化切断前后 lineage；强度更像重新定价，不是普通开放 A | `pattern_like / gap-state-boundary` |
| `AMD` | 多段方向性上涨和下跌都很明显 | 多个跳空、波动扩张和事件/状态切换；同一 A/B/C 锚点不稳定 | `pattern_like / event-volatile-boundary` |
| `MU` | 2024 年有强上行腿与回撤后再推 | 强 A 大量由跳空和重新定价构成，不能作为普通趋势基准 | `pattern_like / event-gap-boundary` |
| `AVGO` | 上行趋势清楚，局部有回调再推 | 冲击缺口和大尺度状态变化主导窗口；与已有事件型样本同质 | `boundary / event-driven-A` |
| `AMAT` | 低位恢复后出现向上段 | 恢复起点和后续推进含明显冲击，B 尺度不稳定 | `boundary / transition-repricing` |
| `HD` | 多段上涨与下跌，局部可见回调 | 财报附近波动、多个状态切换和深回撤，普通 A/B 不够清楚 | `pattern_like / event-transition-boundary` |
| `NKE` | 长期下行中有反弹和再次下行 | 反向腿多、重叠高，部分区间边缘和缺口混在一起 | `boundary / range-and-lineage-unclear` |
| `LLY` | 大级别上涨后多次高位回撤，再重新走强 | 大尺度波动和事件跳空使局部计数容易重置，首阶段不适合深审 | `pattern_like / nested-event-boundary` |
| `TXN` | 2024 年出现下跌、恢复与再次推进 | 关键恢复段伴随跳空，普通开放趋势与状态转换不能混写 | `boundary / event-gap-state-change` |
| `NOW` | 2024 年有强空头腿和后续反弹 | A 很强，但 B/父级包含大波动和状态转换，不能直接冻结 L1/L2 | `pattern_like / strong-A-but-transition` |

## 本轮结论

这 12 个窗口没有新增足够干净的普通开放趋势 ABC 正向基准。这个结果不是研究失败，而是一次有效的视觉过滤：

1. **强 A 不等于普通 A。** 如果方向性来自跳空、财报或重新定价，先单独分组，不能污染无事件样本。
2. **完整图表会暴露计数问题。** JPM 这类“看起来一直很强”的图，局部可以画出多条 A→B→C，但不同尺度会互相嵌套；不能为了得到 H1/H2 标签而强行选一个。
3. **边界样本不需要再做完整审计。** 本轮没有哪张图同时满足开放背景、lineage 稳定、B 后段受控和首障碍明显有空间，因此按视觉协议在第一阶段停止。
4. **下一轮应换未重复的历史窗口，而不是继续深挖这 12 个标的。** 目标仍是找到一个事件更干净、A 清楚、B 受控且第一障碍有空间的多空对照。

## 相关协议

- [`ABC 研究状态与工作边界 v0.3`](abc_research_status_v0_3_CN.md)
- [`PA Pattern 视觉筛选协议`](visual_pattern_triage_protocol_CN.md)
- [`ABC 覆盖审计`](abc_pattern_coverage_audit_CN.md)


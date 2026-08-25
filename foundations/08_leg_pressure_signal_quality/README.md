# 强 A 腿、回调压力与优质信号 K

文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)。

这是 H1/H2、L1/L2、ABC、MTR 和三推共用的质量层。它不替代父级市场状态、位置、首障碍、事件或订单合同，而是回答：方向是否真的有力，反向压力是否减弱，信号 K 是否值得触发。

## 1. 强 A 腿

优先观察方向明确、收盘靠近极值、实体有连续性、K 线重叠较少、回调没有立即收回关键突破的 A。跳空或连续强 K 可以增加方向证据，但单根大 K 也可能是高潮，必须看左侧位置和后续接受。

普通小腿、重叠宽通道、反复穿越 EMA 或靠近主要障碍的 A，先标为 `ordinary_or_boundary`，不因为后续结果倒推为强 A。

## 2. B 回调压力

### 受控 B

回调可以很深，但若后段实体缩小、重叠增加、关键支撑/EMA20/EMA50 附近稳定、反向突破没有接受，仍可保留 H2/L2 或 ABC 延续候选。深度本身不是否决条件。

### 扩张 B

反向 K 线扩大、收盘持续靠近反向极值、穿越主要位置并获得跟随，说明卖压/买压没有收缩；降级为 `new_trend_or_range`，不要机械数 H2/L2。

## 3. 信号 K 与触发

分开记录 `setup`、`signal_bar`、`trigger`、`follow_through`。优质多头信号 K 可以是收盘扎实的阳线，或先下探后收回的长下影/doji；空头反之。更有价值的是它发生在关键支撑/阻力或 EMA20/50 附近，并且没有被首障碍立即抵消。

EMA 只是汇合项，不是形态本身。成交量回调收缩是重要参考、不是必要条件；没有量也不能自动否决，有量也不能自动证明方向。

## 4. 工作复核卡

```text
parent_state:
leg_direction:
A_quality: strong / ordinary / wide_channel / climax / unclear
pressure_asymmetry: favorable / mixed / unfavorable
B_shape: shallow_controlled / deep_stable / expanding / unclear
setup:
signal_bar_quality:
trigger_and_follow_through:
EMA20_50_location:
volume_reference: supportive / neutral / adverse / unavailable
direction: long / short / no_valid_direction
first_independent_obstacle:
decision: candidate / conditional / wait / valid_no_trade
```

本层只做视觉研究，不设固定实体、百分比、成交量或 EMA 距离阈值，不修改 Codex Trading，不连接 Execution Agent。专项对照见[`强 A 腿与信号 K 视觉证据审计`](../../research/leg_pressure_signal_quality_visual_evidence_audit_2026-08-24_CN.md)。

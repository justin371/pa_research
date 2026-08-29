# 强 A 腿、回调压力与优质信号 K

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)。

这是 H1/H2、L1/L2、ABC、MTR 和三推共用的质量层。它不替代父级市场状态、位置、首障碍、事件或订单合同，而是回答：方向是否真的有力，反向压力是否减弱，信号 K 是否值得触发。强 A 的优先级规则主要服务 ABC/H1/L1；区间边缘三推是例外路径，不要求 A 腿达到强 A。

## 1. 强 A 腿

优先观察方向明确、收盘靠近极值、实体有连续性、K 线重叠较少、回调没有立即收回关键突破的 A。对强 A→H1/L1 路径，优先寻找同方向约 3–4 根连续 Daily K 线、实体相对饱满、收盘持续推进且有跟随；中间出现跳空时方向证据更强，但跳空不是必要条件。

跳空或连续强 K 可以增加方向证据，但单根大 K 也可能是高潮，财报/异常事件跳空必须单独标记，不能直接并入普通强 A。

普通小腿、重叠宽通道、反复穿越 EMA 或靠近主要障碍的 A，先标为 `ordinary_or_boundary`，不因为后续结果倒推为强 A。若此类 A 后经过多次回调抵达成熟区间上沿/下沿，可转入 `range_edge_three_push` 研究，不应因不满足强 A 而直接丢弃，也不能把它当成强 A 后 H1/L1。

## 2. B 回调压力

### 受控 B

回调可以很深，但若后段实体缩小、重叠增加、关键支撑/EMA20/EMA50 附近稳定、反向突破没有接受，仍可保留 H2/L2 或 ABC 延续候选。深度本身不是否决条件。

### 扩张 B

反向 K 线扩大、收盘持续靠近反向极值、穿越主要位置并获得跟随，说明卖压/买压没有收缩；降级为 `new_trend_or_range`，不要机械数 H2/L2。

## 3. 信号 K 与触发

分开记录 `setup`、`signal_bar`、`trigger`、`follow_through`。优质多头信号 K 可以是收盘扎实的阳线，或先下探后收回的长下影/doji；空头反之。更有价值的是它发生在关键支撑/阻力或 EMA20/50 附近，并且没有被首障碍立即抵消。

EMA 触碰只是汇合项，不是形态本身；但高质量日线 H1/H2/L1/L2 采用方向性斜率闸门：多头 EMA20/50 均向上，空头 EMA20/50 均向下。成交量回调收缩是重要参考、不是必要条件；没有量也不能自动否决，有量也不能自动证明方向。

## 4. 工作复核卡

下面的卡只记录腿与信号质量；它不是独立 pattern，也不替代完整案例的证据头、主标签、订单合同和状态轴。字段直接采用统一合同名称，质量层的补充描述另用 `pressure_asymmetry`、`B_shape` 等字段承载。

```text
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
leg_direction:
a_leg_quality: strong / ordinary / unclear / event_driven
pressure_asymmetry: favorable / mixed / unfavorable
B_shape: shallow_controlled / deep_stable / expanding / unclear
b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear
setup:
signal_bar:
confirmation_bar:
new_trigger:
follow_through:
daily_ema20_50_200:
daily_ema20_slope: up / flat / down / unknown
daily_ema50_slope: up / flat / down / unknown
h_l_ema_slope_gate: long_pass / short_pass / fail_flat_or_opposite / pending / not_applicable
h_l_pullback_location:
b_leg_location:
meta_confluence: present / absent / unknown
meta_zone:
meta_components:
volume_reference: supportive / neutral / adverse / unavailable
direction: long / short / no_valid_direction
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
lineage_status: same_lineage / reset / unclear / pending
first_independent_obstacle:
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
```

`B_shape`、`pressure_asymmetry` 和 `leg_direction` 是本基础层的解释性补充；`a_leg_quality`、`b_leg_class`、`b_leg_location`、`direction`、`signal_bar`、`new_trigger`、`follow_through` 和分轴状态才是完整记录应回填的 canonical 字段。历史 `A_quality`、`EMA20_slope`、`EMA50_slope`、`pullback_location` 和 `decision` 不得作为新合同字段使用。

本层只做视觉研究，不设固定实体、百分比、成交量或 EMA 距离阈值，不修改 Codex Trading，不连接 Execution Agent。专项对照见[`强 A 腿与信号 K 视觉证据审计`](../../research/leg_pressure_signal_quality_visual_evidence_audit_2026-08-24_CN.md)。

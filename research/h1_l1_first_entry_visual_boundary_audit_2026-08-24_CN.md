# H1/L1 第一次入场视觉边界复核

日期：`2026-08-24`；状态：`visual-research / provisional / not-statistical`

## 统一合同

```text
父级状态 → A 方向质量 → B 后段压力 → 位置 → H1/L1 signal K
→ stop/confirmation → follow-through → 结构止损 → 第一障碍 → fallback H2/L2
```

H1/L1 是回调中的第一次有意义恢复，不是第一根顺方向 K，也不是碰到 EMA 后的机械突破。强 A、受控 B 和关键位置使它值得优先审计；普通 A、区间中部或压力扩张时只保留 `H1/L1-like`。

## 案例分流

| 案例 | 当时可见的优势 | H1/L1 裁决 |
| --- | --- | --- |
| KLAC `2025-10-14–10-24` | 强 A、浅 B、确认 K 强；设置 K 与触发 K 分开 | `candidate / first-obstacle-conditional`；不能把近端前高用 MM 隐藏 |
| NFLX `2025-02-14–03-28` | 空头 A 清楚，B 后段受控，L1-like 位置可读 | `conditional`；需独立核对触发与首支撑，不能事后增加 L2 |
| NVDA `2025-04-21–05-08` | 强-looking A、深但后段稳定 B、H1 恢复清楚 | `valid_no_trade`；前高首阻力先否决早分支，跳空分支另立合同 |
| LOW `2024-06-11–06-24` | 低位方向性反弹和 H1/H2-like | `transition / valid_no_trade`；父级未确认，信号 K 和首障碍不足 |
| COST `2024-05-13–05-16` | 形状与信号 K 都像 | `valid_no_trade`；触发上方障碍过近 |

## 关键边界

1. **H1 失败不等于形态错误。** 若第一次恢复没有跟随、但 B 仍属于同一回调且后段稳定，转为 H2/L2 研究；若反向压力扩张或结构被接受性破坏，则重建新趋势/区间状态。
2. **设置 K 与确认 K 分开。** KLAC 的回调 K 可以是 setup/count bar，下一根强实体 K 才是实际确认；不能把强空头设置 K 美化成优质多头信号。
3. **优质信号 K 也会被空间否决。** COST、LOW、NVDA 说明信号形状、EMA 汇合和后续方向都不能取消第一独立障碍。
4. **低周期不能制造高周期空间。** 15m 只确认同一合同，或另立短线合同；不能用窄止损把日线坏 R/R 修漂亮。
5. **事件与跳空重订。** 财报前三个交易 session 不新开仓；开盘跳过原 stop 时，原价不算成交，必须按实际价重算或观望。

## 统一输出

```text
parent_state:
a_leg_quality: strong / ordinary / unclear / event_driven
b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear
internal_label: H1 / L1 / none / pending
signal_bar: quality / mixed / poor / setup-only
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
first_independent_obstacle:
space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

当前结论：H1/L1 最适合做早期趋势筛选，但不应追求“所有第一尝试都交易”。强 A + 受控 B + 位置 + 优质确认 K 只是候选入口；首障碍、结构止损、事件和实际成交仍可直接否决。研究保持 provisional，不产生胜率或生产规则。

# 突破回踩 / BOP

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补突破接受、回踩、角色转换和跟随。`BOP` 是唯一主标签，ABC/H-L 只能作为 `secondary_context`。

## 研究目的

研究主要阻力/支撑被接受后的新交易合同：突破、回踩突破区、再次离开并得到跟随。它与失败突破、gap-and-go 和旧趋势合同分开。

## 共同图表范围前置

进入 BOP 判断前，先按[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)查看同一标的至少两年的 Daily 左侧背景（若窗口支持），记录重要高点、主要低点、支撑阻力、前高/前低、EMA20/50/200、当前父级状态和第一独立障碍。再核对突破前 A 的推动力与回踩 B 的受控程度；涉及 H/L 时，Daily EMA20/50 必须与方向一致。缺少左侧、EMA 或位置/空间证据时保留 `pending`/`observation_only`，不能把局部突破或影线单独升级为 BOP。

## 视觉定义

- 突破前边界事先可见；
- 收盘真正越过边界，后续有跟随或回踩守住；
- 回踩不能重新被旧区间接受；
- 重新离开突破区时，重新计算入场、结构止损、第一障碍和 R/R；
- 如果直接强收盘突破且没有回踩，记录为 breakout-acceptance，不事后假设一定会给回踩。

## 三种突破状态

| 状态 | 视觉条件 | 默认处理 |
| --- | --- | --- |
| `breakout-acceptance` | 实体收盘越过旧边界，后续仍在边界外交易 | 建立新 BOP 合同；可研究收盘/stop/低周期确认 |
| `breakout-pullback` | 突破后回到旧边界附近，回测守住，再次离开 | 研究 limit-retest 或重新离开时的 stop；重新计算风险 |
| `failed-breakout` | 只有影线、无跟随或重新接受回旧区间 | 切换失败突破/区间边缘，不继续沿用 BOP thesis |

“强 K”本身不是 BOP。必须先有一个事前可见的边界，再有接受和跟随；若没有回踩，不把缺少回踩当作错误，而是记录为 `breakout-acceptance/gap-and-go` 新合同。

## 最小复核卡

```text
prior_boundary:
prior_market_state: range / trend / transition
breakout_bar_quality:
close_outside_boundary:
follow_through:
pullback_to_old_level: yes / no / not_yet
role_reversal_accepted:
order_branch: stop_confirmation / market_close / limit_retest / stop_limit / observation_only
branch_role: same_contract / role_reversal_retest / gap_reprice / management
actual_fill_or_open_skip:
structural_stop:
first_independent_obstacle:
rough_R_R:
failure: reacceptance_inside_old_range / no_follow_through / event-risk
```

## 交易合同纪律

- 突破前的 H1/H2、三推或 MTR 假设，在突破被接受后必须重新分类，不把旧合同继续套用；
- 开盘跳过旧 stop 时，成交价、止损、首障碍和 R/R 全部按实际可成交状态重算；
- limit-retest 只有价格真正回到旧边界才可能成交，未回测不记成交；
- 突破 K 过宽、已接近下一个主要磁铁或首障碍不足约 1R 时，记录 `valid_no_trade`；
- 低周期 BOP 只能确认高周期合同，或明确创建独立低周期合同，不能把两个周期的 R/R 合并。

## 主要陷阱

阻力下大阳线自动追、把一次影线叫接受、用远端 MM 跳过首障碍、开盘跳过后仍沿用旧订单、把低周期 BOP 当成日线新形态。

## 现有入口

- [`BOP / Gap acceptance 框架`](../../research/bop_gap_acceptance_framework_CN.md)
- [`TSLA BOP 后续案例`](../../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)
- [`多周期视觉复核框架`](../../research/multitimeframe_visual_review_framework_CN.md)
- [`订单分支协议`](../../research/order_branch_visual_protocol_CN.md)
- [`BOP 突破回踩专项视觉证据审计`](../../research/bop_visual_evidence_gap_audit_2026-08-24_CN.md)
- [`BOP 真实多日回踩候选审计`](../../research/bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)

## 当前案例对照

| 案例 | 状态 | 研究结论 |
| --- | --- | --- |
| [`TSLA 2025-09-08–09-12`](../../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md) | 阻力下多次测试后强收盘接受 | 反转/MTR 假设失效，切换 BOP；次日再追是更晚的新合同 |
| [`TSLA 2025-03-04 284 回测`](../../research/tsla_abc_playbook_2025-03-04_284_retest.md) | 缺口延续后回测旧位 | 原 sell-stop 被跳过，284 附近 sell-limit/retest 独立研究 |
| [`GOOGL 2024-03-18`](../../research/googl_bullish_h1_gap_trigger_boundary_2024-03-04_2024-03-22.md) | 强 A/浅 B 后跳空越过原 buy-stop | 方向正确但实际重订后首障碍拥挤，记录 no-trade |
| [`QCOM 2024-07-24`](../../research/qcom_bearish_abc_l1_l2_gap_sector_boundary_2024-07-17_2024-07-30.md) | 空头突破方向正确但开盘重订 | 理想触发空间被实际开盘价压缩，说明方向对不等于合同合格 |
| [`NKE 2025-10-28`](../../research/nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md) | 小缺口后旧低点真实回测，出现 BOP-like limit-retest 路径 | 回测约 `1.2R`、板块混合且事件背景未清；保留为订单边界，不当作干净 BOP 基准 |

## 当前目标验收

- 能从左侧明确旧边界，并区分影线测试与收盘接受；
- 能分别识别 gap-and-go、突破回踩和失败突破；
- 能在突破接受后重建成交、止损、首障碍和 R/R；
- 能把旧 MTR/区间/趋势合同废弃或转换，而不是事后混用；
- 保留至少一个“突破方向正确但交易几何不合格”的 no-trade 案例。

本轮专项审计结论：TSLA 2025-09 主要验证“突破接受后的状态切换”，TSLA 2025-03 的 `284` 回测才是最清楚的真实回踩合同；两者不能混成同一个入场模式。当前仍缺事件干净、父级清楚、角色转换明确、首障碍宽裕且路径完整的普通 BOP 正例，因此状态保持 `conditional / no-new-positive`。

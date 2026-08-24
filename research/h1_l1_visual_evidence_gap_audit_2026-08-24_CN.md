# H1/L1 第一次入场专项证据审计（2026-08-24）

日期：2026-08-24  
状态：`visual-research / h1-l1 / no-new-positive / boundary-audit / not-statistical`

## 1. 本轮目标

本轮为 H1/L1 单独建立审计，寻找同时满足以下条件的多空历史视觉案例：

- 父级是开放趋势，而不是区间中部或过渡转向；
- A 腿方向性清楚，B 腿浅或主要通过时间整理完成；
- 第一次恢复发生在有意义的支撑/阻力或 EMA 汇合处；
- 优质信号 K、stop/收盘确认和低周期触发可以分开重建；
- 结构止损自然，触发到第一独立障碍有基本空间；
- 触发不在用户设定的财报前三个交易日内。

这不是胜率统计，也不把“后来上涨”当成入场前证据。

## 2. 最接近的多头案例：KLAC 2025-10-23

来源：[`KLAC H1 强势上涨腿与浅回调案例`](klac_h1_case_study_2025-10-14_2025-10-24.md)。

### 2.1 形态本身值得保留

- `2025-10-14`–`2025-10-20` 是低重叠、连续推进并带有上涨缺口的强 A；EMA20/50/200 向上排列。
- `2025-10-22` 只有一天回调，深度约 `43.6%`；它本身是一根较强空头 K，不能美化成“卖压很轻”，但没有形成连续空头跟随。
- `2025-10-22` 更适合叫 `H1 setup/count bar`，不是优质多头信号 K。
- `2025-10-23` 才出现强实体、收盘靠近高点并突破 setup bar 高点的 `confirmation/trigger bar`；15m 触发可以独立复核。

这补充了一个可复用的 H1 语言：**setup/count bar 与实际 confirmation/trigger bar 不一定是同一根 K。**不能为了满足“优质信号 K”而把前一根空头回调 K 改写成阳线信号。

### 2.2 首阻力的两种解释必须并列

触发参考约为 `114.13` 上方，入场前可见的主要高点簇约为 `115.49–115.63`，结构止损观察约在 `104` 附近。

- 严格障碍分支：前高簇是第一阻力，空间不足约 `1R`，日线新仓应 `valid_no_trade`；
- 强趋势磁铁分支：在强 A、一天浅 B、卖方无连续跟随且存在更大级别嵌套上涨时，前高可作为接受检查点，而不是机械否决；但这只是 `research_positive_conditional`，需要接受、管理和仓位证据，不能用 MM `124.77` 把近端风险藏起来。

两种分支都保留，不能因为“强趋势可能穿越前高”就删除主要阻力规则。

### 2.3 事件临近，但不落入三交易 session 禁区

KLA 官方公告显示，Q1 FY2026 财报安排在 `2025-10-29` 收盘后发布。按仓库现行规则“财报前三个 trading session 不新开”，紧邻的三个交易 session 是 `2025-10-24`、`2025-10-27`、`2025-10-28`；`2025-10-23` 不在这三个 session 内，因此财报过滤记为 `passed`。但事件已经临近，仍应保留 `event-proximity`，不能把它当作完全无事件背景。

来源：[`KLA Announces First Quarter Fiscal Year 2026 Earnings Date`](https://ir.kla.com/news-events/press-releases/detail/504/kla-announces-first-quarter-fiscal-year-2026-earnings-date)。

所以 KLAC 的最终标签应写为：

```text
pattern_like / strong-A / one-day-B / confirmation-quality-positive
/ strict-first-resistance-no-trade / strong-trend-magnet-conditional
/ earnings-filter-passed / event-proximity / not-a-clean-no-event-baseline
```

后续 `2025-10-29` 的财报结果不能倒灌成 `10-23` 的 H1 证据。

## 3. 其他候选的筛选结果

| 候选 | 形态价值 | 不能升级为普通 H1/L1 基准的原因 |
| --- | --- | --- |
| [`V 2024-05-15`](v_bullish_abc_h2_no_gap_first_obstacle_boundary_2024-05-06_2024-05-17.md) | 普通/方向性 A、深但后段稳定、低周期真实触发 | 实际是 H2-like；第一阻力约 `0.85R–1.05R`，财报背景尚未核对，保留边界。 |
| [`HD 2024-07-25`](hd_bullish_h1_ema200_sector_boundary_2024-07-01_2024-07-31.md) | 多头 H1-like，深 B 落在支撑簇，财报过滤通过 | EMA200 几乎贴着触发，XLY/SPY 逆风，信号 K 收盘质量一般，`valid_no_trade`。 |
| [`LRCX 2024-07-24`](lrcx_bearish_abc_l1_gap_first_support_2024-07-10_2024-07-25.md) | 空头强 A、短 B、L1 顺序和板块配合清楚 | A 为缺口冲击，原 stop 被开盘越过，重订后首支撑只有边界空间，`valid_no_trade`。 |
| [`AMZN 2024-10-15`](amzn_bearish_abc_l1_no_gap_first_support_boundary_2024-09-23_2024-10-15.md) | 无缺口 L1，财报过滤通过 | A 普通、B 深且持续时间长，XLY/市场许可混合，首支撑约 `1.1R–1.4R`，仅边界。 |
| [`NVDA 2025-05-06/07`](nvda_bullish_h1_trigger_branch_first_obstacle_2025-04-21_2025-05-08.md) | 强-looking A、H1-like 恢复、订单分支可拆 | B 深且前段卖压强，触发分支含糊，首阻力阻塞，`valid_no_trade`。 |
| [`JNJ 2025-08-29`](jnj_bullish_h1_opening_skip_first_obstacle_boundary_2025-08-01_2025-09-02.md) | 强 A、controlled-B、板块顺势 | 原触发被开盘越过，按结构止损首阻力不足，不能把后续路径倒灌。 |
| [`CRM 2025-03-13/26`](crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md) | 空头 L1 顺序和计数重置有研究价值 | 父级/局部尺度并存，首支撑拥挤，L2 计数未冻结。 |

## 4. 本轮结论：`no-new-positive`

本轮没有找到同时通过“事件干净 + 开放趋势 + H1/L1 计数清楚 + 第一障碍有基本空间”的新基准。

这不是说 H1/L1 不存在，而是当前证据更适合形成以下工作边界：

1. **H1/L1 的优先筛选仍是强 A + 浅/时间型 B**，但形态优先不等于交易优先；
2. **setup/count bar 与 confirmation/trigger bar 必须分开**；
3. **近端前高既可能是阻塞性第一阻力，也可能在强趋势中成为接受检查点**，两种解释必须按当时背景并列；
4. **财报过滤先于形态升级**，KLAC 说明一张视觉上很漂亮的 H1 也可能被事件窗口降级；
5. **H1/L1 不能借 H2/L2 的后续结果证明自己**；第一次尝试失败时，应保留等待 H2/L2 的分支；
6. **没有新信息就不再复制同类边界图**，下一张图只有在填补空头/多头方向、订单合同或首障碍几何时才值得深审。

## 5. H1/L1 当前状态

```text
形态识别：conditional / visual-workable
事件干净普通基准：no-new-positive
多头：AAPL 事件型、KLAC 事件窗口边界、HD/ V/ JNJ 首阻力边界
空头：NFLX/TSM 仍是 ABC/L1 主要对照，AMZN/LRCX/CRM 为边界
生产规则：未冻结
```

本文件只更新 PA Research 的视觉研究层，不修改 Codex Trading，不创建量化扫描器，也不连接 Execution Agent。

## 6. 相关入口

- [`H1 / L1 第一次入场目录`](../patterns/01_h1_l1_first_entry/README.md)
- [`H1/L1、H2/L2 与 ABC 证据缺口审计`](h1_h2_abc_evidence_gap_audit_2026-08-23_CN.md)
- [`核心八个 Pattern 代表性案例矩阵`](core_pattern_case_matrix_CN.md)

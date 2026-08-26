# H/L 首批真实样本准入审计（2026-08-26）

状态：`research_only / intake_audit / no-contract-frozen / no-new-positive`

## 目的与范围

这是回测合同升级后的第一轮真实样本准入检查。目标是从 PA Research 已有的人工图表案例中，筛出可以进一步冻结为 H1/H2/L1/L2 回放合同的案例；本轮不自动识别 pattern，不全市场扫描，不把后续走势倒灌为入场前证据，也不连接 Execution Agent。

准入顺序固定为：

1. 先看至少两年 Daily 左侧、EMA20/50/200、重要高低点和支撑阻力；
2. 再确认 A/B、H/L 计数和同一 lineage；
3. 对 H1/H2 要求 Daily EMA20、EMA50 均向上；对 L1/L2 要求两者均向下；
4. 记录回调位置和 META 区域，但 META 不能替代信号、空间或结构止损；
5. 最后才冻结触发、成交分支、结构止损、第一障碍、目标、最大持有 K 线数、事件和结果边界。

缺少最后一项的案例只能保留为 `pattern_candidate`、`valid_no_trade` 或 `pending`，不能写入回测合同 CSV。

## 数据来源边界

- Round5 的 COHR、IWM、QQQ 图像来自仓库内的两年 Daily/局部周期历史资产；来源和截断边界见 [`Round5 两年 Daily 资产说明`](../assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md)。
- TSLA `2026-05-20` 使用已有的人工案例记录，并在本 session 通过 agent-reach 的公开网页/Jina 路由读取 Yahoo Chart API 历史 Daily OHLC 做数值交叉核对；来源时区为 `America/New_York`，数据为历史收盘，不是实时行情。公开数据只用于指定案例的复核，不作为扫描器输入。
- 公开数据复核得到 TSLA `2026-05-13` 到 `2026-05-20` 的 EMA20 约从 `402.81` 升至 `408.81`，EMA50 约从 `395.30` 升至 `399.57`；这支持 `daily_ema20_slope=up`、`daily_ema50_slope=up` 的记录，但不自动证明 H1/H2 计数成立。

## 首轮准入表

| 案例 | 方向/近似标签 | EMA20/50 闸门 | 回调位置与 META | 首障碍/合同状态 | 准入决定 |
| --- | --- | --- | --- | --- | --- |
| [TSLA 2026-05-20](../tsla_h1_h2_case_study_2026-05-15_2026-05-22.md) | `long / H1-H2-like`；强上涨腿后深回撤 | `long_pass` 候选；两条 EMA 均向上 | `393–399` 附近有 `2026-05-19` 低点、EMA50/EMA200 的支撑簇，可记录 META；但 B 腿较深 | 触发约 `417.46` 上方，前方 `434.66` 约 `0.72R`；H1/H2 计数、目标和 15m 合同仍未冻结 | `valid_no_trade / no-contract-frozen` |
| [COHR 2026-05-13](../assets/visual_recognition/2026-08-24/round5_two_year_daily/US_COHR_MTF_cutoff_2026-05-13_unlabeled.png) | `long / ABC + H1-like` | 图上方向偏上，但本轮没有独立数值合同证明 | 旧支撑远离当前触发区；不能把孤立 EMA 触碰写成 META | 左侧当前高点约 `413`，触发区贴近前高；精确触发/止损/目标缺失 | `pattern_candidate / pending` |
| [IWM 2026-05-28](../assets/visual_recognition/2026-08-24/round5_two_year_daily/US_IWM_MTF_cutoff_2026-05-28_unlabeled.png) | `long / ABC + H2-like` | Daily EMA20/50 视觉上向上，方向闸门可继续核对 | `269–278` 支撑和上行 EMA 可组成位置候选；需要去除同一价格簇的重复计分 | 触发接近 `292.05` 前高，第一障碍拥挤；精确订单合同缺失 | `valid_no_trade / no-contract-frozen` |
| [QQQ 2026-07-17](../assets/visual_recognition/2026-08-24/round5_two_year_daily/US_QQQ_MTF_cutoff_2026-07-17_unlabeled.png) | `short / bearish L1-L2-like`；Daily 多头转 4H 过渡 | EMA20 有向下迹象，但 EMA50 未确认同步向下；不能写 `short_pass` | `686–701` 是支撑而非已确认的空头回调阻力；父级仍在过渡/区间化 | 首支撑很近，且缺 15m；不满足普通 L1/L2 空头合同 | `observation_only / slope-gate-pending` |
| [TSLA 2025-09-04](../tsla_h1_h2_case_study_2025-08-28_2025-09-05.md) | `long / H2-like`；拒绝型信号 K | 方向背景可继续核对 | EMA20/50 附近位置可读，但与 `2025-08-22` 属同一更大 lineage | `2025-09-05` 跳空跟随，原合同需重订；不能与同一 lineage 的其他尝试独立计数 | `dependent-lineage / no-contract-frozen` |

## 本轮结论

```text
reviewed_cases: 5
two_year_daily_context_available: 5
strict_h_l_contracts_frozen: 0
comparable_backtest_samples_added: 0
valid_no_trade_or_boundary_cases: 3
observation_only_or_pending_cases: 2
no-new-positive: maintained
```

这不是回测失败，而是准入闸门正常工作：

- TSLA 的 EMA 方向和支撑 META 较清楚，但第一独立阻力不足，不能为了得到一个漂亮的后续结果而冻结日线入场；
- COHR、IWM 的外形有帮助，但触发、结构止损和空间还没有达到合同级别；
- QQQ 的空头近似形状发生在 Daily 多头向过渡状态切换期间，EMA50 方向和首支撑都不足；
- TSLA `2025-09-04` 与 `2025-08-22` 共享更大行情 lineage，必须作为依赖样本处理。

因此本轮没有新增 `filled`、`win`、`loss` 或 `realized_R` 样本，也没有改变 PA Research 的 `no-new-positive` 结论。

## 下一步准入动作

只继续补充能填补缺口的案例，不复制同样的“强 A + 前高过近”边界：

1. 先选一例事件已核对、两年 Daily 完整、EMA20/50 方向明确、第一障碍至少有基本空间的多头 H1/H2；
2. 为同一例补齐真实历史 OHLC CSV、精确触发价、结构止损、第一障碍、预设目标和最大持有 K 线数；
3. 冻结后再运行 `backtesting.py`，并将 `H1/H2/L1/L2`、EMA 闸门、META、成交/未成交和 lineage 分开统计；
4. 若候选再次被首障碍、事件或合同不完整否决，保留否决记录，不降低标准凑样本。

回放器入口见 [`PA Research 冻结合同回放器`](README.md)。本审计不创建量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

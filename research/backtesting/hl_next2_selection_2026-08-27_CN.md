# H/L 下一批（二）人工合同冻结记录（2026-08-27）

状态：`research_only / frozen_pre_outcome / descriptive_only / not-validated`
contract_scope: historical_context_only
timeframes_seen: Daily

## 结论边界

本批继续只做 PA Research 的人工图表研究。标签、A/B 结构、H1 计数、两年 Daily 背景、重要高低点、支撑阻力、EMA20/50/200、事件分组、META、触发、结构止损和第一障碍均在回放前由人工看图冻结；没有自动识别形态、自动扫描股票或执行连接。

用户修正后的 `60%` 是待检验目标，不是生产规则、胜率承诺或收益保证。结果必须按事件、方向、H/L 标签和 `lineage_id` 分层；本批没有合格的 H2/L2，因此不能把 H2/L2 的空缺写成零胜率。

## 数据和股票池准入

| 项目 | TOL | VEEV |
| --- | ---: | ---: |
| 研究市值快照 | `$13.69B`（2026-08-26） | `$39.78B`（2026-08-26） |
| 20 日平均日成交额 | 约 `$132.65M` | 约 `$398.56M` |
| 市值来源 | [StockAnalysis TOL market cap](https://stockanalysis.com/stocks/tol/market-cap/) | [StockAnalysis VEEV market cap](https://stockanalysis.com/stocks/veev/market-cap/) |
| 成交额计算 | 2026-07-30 至 2026-08-26 的 Daily `Close × Volume` | 同左 |

两只都是美国普通股，满足当前研究池 `$3B–$100B` 和日成交额原则上不低于 `$50M`。市值和流动性是当前准入快照，不是把历史决策日的市值回填成已知信息。

价格快照使用公开 Yahoo Chart API 历史 Daily OHLCV，经 agent-reach 的 Jina 公开路由读取；源时区为 `America/New_York`，复核时间为 `2026-08-27 Asia/Shanghai`，最新完整 RTH 日线为 `2026-08-26`。本 session 未成功调用 Futu MCP，因此这些资产不是 Futu 或实时数据。

机器可读输入：[`hl_next2_contracts_2026-08-27.csv`](hl_next2_contracts_2026-08-27.csv) 和 [`hl_next2_prices_2026-08-27.csv`](hl_next2_prices_2026-08-27.csv)。人工图像见 [`H/L 下一批（二）人工看图回放资产`](../assets/visual_recognition/2026-08-27/hl_next2_backtest/README.md)。

## 冻结合同

空间按多头 `(first_obstacle - entry_trigger) / (entry_trigger - structural_stop)` 计算；`>=1R` 是最低空间门槛，不代表高质量或已验证优势。

| 合同 | 方向 / 标签 | 决策日 | 触发 | 止损 | 第一障碍 | 事前空间 | A/B、位置与质量 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| TOL 2023-04-26 | `long / H1` | 2023-04-26 | 62.30 | 61.05 | 64.28 | 1.5840R | 普通 A 段的净推进；4/21–4/26 为回到向上 EMA20/前期支撑的受控时间回调；META 为 EMA20 与 4 月支撑簇；不是最强的连续 3–4 根满实体 A，按 ordinary_A 降级。 |
| VEEV 2024-01-18 | `long / H1` | 2024-01-18 | 204.70 | 200.00 | 209.44 | 1.0085R | 1/8–1/12 为强 A 段，随后 1/17 较大阴线、1/18 恢复；B 记为 deep_late_controlled_B。EMA20/50 方向通过，但回调没有直接触碰均线，且空间仅略高于 1R，保留为 borderline，不升级为高质量正例。 |

方向分布：`long=2`、`short=0`；标签分布为 `H1=2`。

两条合同均使用 `stop_confirmation`、`max_hold_bars=10`、`gap_policy=skip`。开盘越过旧触发位时不追价补成交；`target_price` 取第一道独立障碍，所有字段在结果发生前冻结。

## 人工视觉复核

### TOL 2023-04-26：普通 A / 受控 B / H1

- 两年左侧 Daily 先显示 2022 年大幅下跌后的修复，以及 2021 年约 75 一带的长期高点；截至决策日，价格仍在长期高点下方，64.28 是当前局部首先可见的独立阻力。
- 局部 A 不是用户偏好的最强 3–4 根连续满实体推进，但 4/10–4/20 形成清楚的净上移，4/18 和 4/20 有较明显的推动；不把普通 A 误记成 strong_A。
- 4/21–4/26 的 K 线相对收缩并重叠，低点 61.17 靠近 EMA20 60.56 和 4 月支撑簇；没有把回调低点机械改到更窄的位置。
- 决策日 EMA20=`60.5580`、EMA50=`59.0285`、EMA200=`53.8547`；EMA20/50 均向上，H1 的 `long_pass` 通过。
- 失败路径：价格不能有效站上 62.30，或接受在 61.05 下方；即使结构成立，64.28 前没有新的独立障碍，不能把更远目标事后加入合同。

### VEEV 2024-01-18：强 A / 边界 B / H1

- 两年左侧 Daily 覆盖 2022 年约 230 一带高点、2022 年末约 155 一带低点和 2023 年的宽幅修复；当前仍属于宽背景中的上行转折，不是无争议的开放趋势，因此降低质量等级。
- 1/8–1/12 连续上行，1/11、1/12 实体和收盘推进明显；1/17 的大阴线之后，1/18 收复部分跌幅，属于可辨认但不理想的 deep_late_controlled_B。
- 决策日 EMA20=`194.2579`、EMA50=`189.9206`、EMA200=`190.2733`；EMA20/50 均向上，H1 的 `long_pass` 通过。
- 回调低点 200.74 没有直接到 EMA20/50；合同只记录为近期突破簇/局部支撑附近，并把该缺点和 1.0085R 空间明确降级。META 记为 absent，不人为拼接不同价格区间。
- 失败路径：跌破并接受在 200.00 下方，或失守 1/17 低点附近 201.51；第一障碍是已知的 1/12 高点 209.44。

## 事件隔离

- TOL：公司 2023 年季度结果页记录 Q1/Q2 结果在 2 月和 5 月下旬公布；Q2 事件在 4/26 决策后的十根 Daily 回放窗口之外。来源：[Toll Brothers 2023 quarterly results](https://investors.tollbrothers.com/financials-and-filings/quarterly-results/2023)。
- VEEV：公司 IR 明确 Q4 FY2024 结果于 2024-02-29 美股收盘后发布；该事件在 1/18 后十根 Daily 回放窗口之外。来源：[Veeva Q4 FY2024 results date](https://ir.veeva.com/news/news-details/2024/Veeva-to-Release-Fiscal-2024-Fourth-Quarter-and-Full-Year-Results-on-February-29-2024/default.aspx)。
- 两条合同的 A、B 和十根 K 线窗口内没有已识别的财报事件或明显财报跳空，因此暂归 ordinary non-event；这不等于宣称不存在任何未检索到的新闻。

## H2/L2 和边界排除记录

本批的研究重点是补 H2/L2，但严格闸门没有形成可冻结新正例：

| 候选 | 方向 / 类别 | 处理 | 主要原因 |
| --- | --- | --- | --- |
| PHM 2023-05-31 | `long / H2-like` | observation/boundary | 形态上有强 A 后的二次回调，但决策日 EMA20 约 66.61，较前几日走平并转弱；不满足 H2 多头 EMA20/50 同时向上的硬闸门。图像保留为 [`PHM_2023-05-31_boundary.png`](../assets/visual_recognition/2026-08-27/hl_next2_backtest/PHM_2023-05-31_boundary.png)。 |
| TOL 2023-02-13 | `long / H1-like` | event-risk separate | 形态和空间曾接近候选，但 2023-02-21 的财报落入之后十根 K 线附近，不能混进 ordinary non-event。 |
| VST / TOST / PWR 多个局部 | 多空混合 | reject / event-boundary | 强腿附近包含财报跳空、重定价或较大实体回调；无法在当前规则下把普通 B 与事件腿清楚分离。 |
| 既有 MAR/COHR/RBLX 边界 | `H2/L2-like` | 不重复制样 | 既有大样本中多条 H2/L2 的首障碍空间低于 1R，或事件证据/独立 lineage 不足；不因本批需要 H2/L2 而重复计数。 |

因此，本批冻结 2 条 H1，H2/L2 为 `n=0`；这是研究结果，不是规则放宽，也不是 H2/L2 失败率为 0%。

## 研究边界

这份记录只保存人工冻结前的可观察事实和排除理由。Matplotlib 仅渲染两年 Daily、局部 OHLC、EMA20/50/200 与原始成交量；它不承担 pattern recognition。回放器只回答冻结后的触发、结构止损、首障碍、持有期与跳空合同在历史路径下如何结束。

本批只属于 PA Research，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。若后续要改变触发、止损、第一障碍、事件口径或把 VEEV 的边界等级升级，必须建立新的独立合同批次，不能覆盖本记录。

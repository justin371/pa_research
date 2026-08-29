# H/L 下一批（四）人工合同冻结记录（2026-08-27）

状态：`research_only / frozen_pre_outcome / descriptive_only / not-validated / no-new-positive`
contract_scope: historical_context_only
timeframes_seen: Daily

## 结论边界

本批按 PA Research 当前规则切换到尚未用于前几批合同的美国普通股，先人工查看至少两年 Daily 图表，再决定是否冻结 H1/H2/L1/L2 合同。每个候选都复核了左侧重要高点和低点、支撑阻力、EMA20/50/200、A/B 同一 lineage、事件隔离、入场触发、结构止损和第一障碍空间。

24 个候选中只有 2 条合同按选择时记录同时通过全部硬闸门：CBOE 和 ROST，均为 `long / H1`。没有满足全部条件的新 H2、L1 或 L2。两条合同的 CSV 状态均为回放前冻结；但 ROST 缺少决策日视觉 artifact，仓库不能独立复核其完整 pre-entry 图证据，不能把该缺口与合同已冻结混为一谈。ROST 因此只能保留为历史回放的 descriptive research record，不能作为新的可交易候选或已验证视觉样本，直到恢复准确的决策日无标签图并重新核对。结果见[`H/L 下一批（四）分层回放审计`](hl_next4_replay_2026-08-27_CN.md)。

方向分布：`long=2`、`short=0`；标签分布为 `H1=2`。

本批没有形成“大样本”：严格筛选后只有两个可合法回放的合同。其余候选被保留为排除证据，不能为了凑数量降低 strong-A、controlled-B、EMA 方向、事件或 `>=1R` 空间要求。`60%` 继续是待检验目标，不是本批规则或收益承诺。

## 股票池与数据边界

以下为 2026-08-26 最新完整 RTH 数据截止时的市值和近 20 个交易日成交额快照。市值是当前准入快照，不回填成历史决策日已知信息；成交额按 `Close × Volume` 计算。24 只均为美国普通股，满足约 `$3B–$100B` 和原则上不低于 `$50M` 的流动性要求。

| 股票 | 市值快照 | 20 日平均成交额 | 处理 |
| --- | ---: | ---: | --- |
| APPF | `$7.90B` | `$80.5M` | reject：强动腿含明显事件跳空；当前延伸 |
| HIMS | `$6.96B` | `$406.0M` | reject：2024-02-28 重定价事件，后续波动不能当普通 A/B |
| NRG | `$24.41B` | `$394.7M` | reject：当前宽幅下行，没有清晰多头 H1/H2 |
| CARR | `$48.42B` | `$355.5M` | reject：强动腿和转折含跳空/事件痕迹 |
| MNDY | `$3.91B` | `$139.0M` | reject：事件后弱势，普通 A/B 不清晰 |
| GDDY | `$12.10B` | `$203.7M` | reject：事件动腿后进入下行/底部，非干净 ordinary H/L |
| XPO | `$22.53B` | `$183.5M` | reject：事件反弹和宽幅回撤，B 不受控 |
| WAB | `$50.76B` | `$269.7M` | reject：深而宽的回撤/转折，不能冻结小 B |
| ITT | `$18.81B` | `$186.6M` | reject：局部 H1-like 的左侧第一障碍空间不足 |
| RSG | `$68.03B` | `$302.8M` | reject：回撤过深过宽，H1/L1 与区间转换难分 |
| FLEX | `$41.31B` | `$416.0M` | reject：强腿后宽幅回撤，后段进入区间 |
| KNSL | `$8.82B` | `$85.2M` | reject：背景由趋势转为宽幅下行/转换 |
| CMI | `$79.59B` | `$593.0M` | reject：候选强腿带事件/重定价，普通 A/B 不独立 |
| WSM | `$27.96B` | `$240.3M` | reject：强段附近有大实体、跳空和财报边界 |
| LEN | `$20.99B` | `$190.4M` | reject：下行强段接近事件，B 宽且背景转弱 |
| EOG | `$75.97B` | `$405.2M` | reject：整体区间/走平，没有强 A |
| PYPL | `$52.88B` | `$599.1M` | reject：反弹处于下行 EMA200/转换背景 |
| HAL | `$28.69B` | `$344.9M` | reject：强腿含跳空，EMA200 背景和后续结构不配合 |
| ROST | `$75.79B` | `$664.3M` | **freeze：2026-01-07 long H1** |
| KR | `$35.87B` | `$345.2M` | reject：多个候选窗口为明显事件重定价 |
| DPZ | `$11.40B` | `$256.6M` | reject：下行/反弹转换，缺少清晰 ordinary A/B |
| DECK | `$12.18B` | `$217.0M` | reject：强下行腿后 B 宽，另有事件跳空 |
| FAST | `$58.69B` | `$357.5M` | reject：强腿多为事件边界；普通窗口没有确认触发 |
| CBOE | `$32.60B` | `$293.8M` | **freeze：2025-05-22 long H1** |

市值参考为公开市场数据页面，例如 [StockAnalysis market-cap pages](https://stockanalysis.com/)。价格快照来自公开 Yahoo Chart API，经 agent-reach 的 Jina 公共路由读取；源时区为 `America/New_York`，复核时间为 `2026-08-27 Asia/Shanghai`，最新完整 RTH 日线为 `2026-08-26`。本 session 未成功调用 Futu MCP，因此本批不是实时或 Futu 回放。

机器可读输入：[`hl_next4_contracts_2026-08-27.csv`](hl_next4_contracts_2026-08-27.csv) 和 [`hl_next4_prices_2026-08-27.csv`](hl_next4_prices_2026-08-27.csv)。无标签图像、原始下载文本和数据缓存保留在本机外部审计目录：

`C:\Users\lwang\.codex\artifacts\pa-research-hl-next4-20260827`

图像使用 Matplotlib `3.10.9` 渲染，`requirements-backtesting.txt` 已固定同一版本。Matplotlib 只负责两年 Daily、局部 OHLC、EMA20/50/200 和原始成交量的人工审阅图；不识别 pattern、不扫描股票、不生成合同，也不连接 Execution Agent。

### 2026-08-29 外部图像 provenance 注记

外部 PNG 的逻辑清单和哈希见[`外部视觉 artifact manifest`](external_visual_artifact_manifest_2026-08-29.json)及[`外部视觉 artifact provenance 审计`](external_visual_artifact_provenance_audit_2026-08-29_CN.md)。审计发现 CBOE `2025-05-22` 有同日 candidate-review 图，但 ROST 合同决策日是 `2026-01-07`，artifact 没有 `ROST_2026-01-07_*.png`；最近的 `ROST_2026-01-08_candidate_review.png` 与 `ROST_2026-01-13_candidate_review.png` 属于 post-decision 图，不能作为该合同的 `pre-entry visual evidence`。原合同和历史结果不改写；ROST 的这一可复核性缺口不能用后一天图静默补齐。

## 冻结合同

空间按多头 `(first_obstacle - entry_trigger) / (entry_trigger - structural_stop)` 计算。`>=1R` 是最低几何门槛，不等于已验证优势。全部合同使用 `stop_confirmation`、`max_hold_bars=10`、`gap_policy=skip`；开盘越过触发位时不追价。

| 合同 | 方向 / 标签 | 决策日 | 触发 | 止损 | 第一障碍 | 事前空间 | A/B 与位置 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| CBOE 2025-05-22 | `long / H1` | 2025-05-22 | 229.24 | 225.50 | 236.00 | 1.8075R | 5/19–5/21 为连续上行推动；5/22 为小实体犹豫 B，位于上行 EMA20 和 5/12–5/14 支撑回测上方；5/7 左侧高点 236.00 是第一独立阻力。 |
| ROST 2026-01-07 | `long / H1` | 2026-01-07 | 189.59 | 185.70 | 200.00 | 2.6761R | 1/2–1/6 为三交易日净推进 A；1/7 小幅犹豫 B，回到上行 EMA20/前期突破簇附近；左侧近端没有更近的独立高点，200.00 作为事前可观察的保守整数位障碍。 |

两条合同的 `lineage_id` 不同，均标记 `same_lineage`；同一 lineage 内不重复计数。两条都满足 Daily EMA20、EMA50 同时向上和 `h_l_ema_slope_gate=long_pass`，EMA200 只作为背景，不替代入场条件。META 仅记录 EMA20 与独立价格支撑/突破簇的共振，不能单独触发交易。

## CBOE 视觉审查

- 两年 Daily 背景显示上行结构和左侧重要高点；5/7 的 `236.00` 在决策日已经可见，不能把决策日之后的新高当作第一障碍。
- 5/19–5/21 连续收盘推进，实体和净位移明显强于普通重叠爬升；5/22 的实体显著收缩，低点 `225.51` 未破坏前一段支撑，收盘仍在 EMA20 上方。
- 2025-05-22 EMA20=`223.16`、EMA50=`219.17`、EMA200=`206.88`；EMA20/50 均向上，长向 H1 闸门通过。
- 触发取 B 高点 `229.23 + 0.01`。5/23 开盘为 `226.58`，没有开盘跳过触发位；盘中上破后成交。若跌破并接受在 `225.50` 下方，或不能站上 `229.24`，合同失效。
- CBOE 2025-05-02 的 Q1 结果来自 [SEC filing](https://www.sec.gov/Archives/edgar/data/1374310/000162828025021670/cboe-20250502xex991.htm) 和 [公司业绩公告](https://s202.q4cdn.com/174824971/files/doc_financials/2025/q1/Cboe-1Q25-Earnings-Press-Release-Final.pdf)。该事件跳空不纳入 A/B；5/12–5/14 的回撤构成可观察的重置。A、B 和十根 K 线窗口内没有已知新财报，因此本合同归入 `ordinary_non_event`，同时保留事件隔离字段供敏感性复核。

## ROST 视觉审查

- 两年 Daily 左侧显示此前的重要高低点和从 2025 年末开始的上行背景；截至 2026-01-07，价格没有紧贴一个已知左侧高点，第一障碍采用保守的 `200.00` 整数位，而不是使用决策日之后才出现的高点。
- 1/2、1/5、1/6 形成连续净推进，1/6 实体较前两根收缩但收盘仍保持推进；1/7 实体很小、低点 `185.74`，属于可辨识但不完美的 controlled B，不把它升级成 H2。
- 2026-01-07 EMA20=`181.61`、EMA50=`174.04`、EMA200=`155.88`；EMA20/50/200 均向上，长向 H1 闸门通过。META 只记录 EMA20 与前期突破簇的共振。
- 触发取 A 高点 `189.58 + 0.01`。2026-01-08 开盘为 `186.99`，没有开盘跳过触发位；盘中上破后成交。跌破 `185.70` 或不能站上 `189.59` 即为失效。
- ROST 的 Q3 FY2025 结果日期为 2025-11-20（公开历史记录见 [Ross Stores earnings history](https://www.nextearningsdate.com/rost-earnings-history.html)）。事件跳空不纳入 2026-01-02–01-07 的 A/B，setup 与事件相隔超过六周，十根 K 线窗口内没有已知新财报，因此本合同归入 `ordinary_non_event`；若未来研究决定把所有 post-earnings lineage 都排除，应将它作为事件边界敏感性而不是普通样本。

## 事件、空间和排除闸门

1. **事件**：强跳空、重定价和财报反应没有直接混入 ordinary A/B。CBOE 和 ROST 的事件证据均记录在合同中，并通过后续回撤/时间间隔隔离；这不是把事件样本隐瞒掉。
2. **强 A**：只接受连续同向推动和明显净位移。事件腿、慢速爬升或连续宽幅震荡均在候选阶段排除。ROST 的 A 有一根相对收缩的推动 K，因此保留为合格但非完美 strong-A 边界，不把它描述成最高质量样本。
3. **受控 B**：B 需要小实体、重叠/犹豫和可解释的位置；大反转、深宽回撤或区间化均拒绝。两条冻结合同都没有把大 K 线回撤改写成“小 B”。
4. **EMA**：H1/H2 多头必须 EMA20、EMA50 同时向上；L1/L2 对称要求同时向下。不能确认时不冻结。
5. **Lineage**：只有在同一时间框架内能解释 A、B、第一次尝试和当前尝试，才保留 H1；没有为了增加 H2/L2 数量而重复同一父级走势。
6. **空间**：两条冻结合同均达到 `>=1R`，并把障碍和止损在回放前写入 CSV。第一障碍不是回放结果反推。

本批没有冻结 H2/L2。空缺不等于 H2/L2 胜率为零，也不表示 H1 规则已经被验证。

## 研究边界

本文件只属于 PA Research。它不修改 Codex Trading，不导入 Codex Trading 的规则，不创建量化扫描器，不把 Matplotlib 变成图形识别器，不连接 Execution Agent。若要改变 strong-A、controlled-B、事件隔离、整数位障碍或持有期，必须建立新的独立合同批次，不能覆盖本记录。

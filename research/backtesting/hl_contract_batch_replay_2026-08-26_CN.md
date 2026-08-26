# H/L 首批人工看图合同回放审计（2026-08-26）

状态：`research_only / descriptive_only / not-validated / no-new-positive`

## 目的与硬边界

本批把已有的人工图表读法冻结成第一批可回放的 H1/H2/L1/L2 研究合同。标签允许是“约等于”某个 PA pattern，但限制条件不能用后见之明放宽：先看至少两年 Daily 左侧，再看重要高低点、支撑阻力、EMA20/50/200、A/B/lineage、回调位置和 META，最后才冻结触发、结构止损、第一障碍、目标、持有期和缺口处理。

本文件只属于 PA Research。它不修改 Codex Trading，不创建量化扫描器，不自动识别股票或 pattern，也不连接 Execution Agent。回放器只读取人工冻结合同和历史 OHLCV；它不是图表识别器。

## 冻结顺序与数据边界

冻结顺序是：

1. 完成两年 Daily 图像复核；
2. 在不读取结果的前提下写入合同 CSV；
3. 提交冻结合同、图像和历史价格快照；
4. 再运行 `backtesting.py` 回放，并把结果单独写入本审计。

价格快照为 Yahoo Chart API 历史 Daily OHLCV，通过 agent-reach 的 Jina 公开路由读取；源时区为 `America/New_York`，资产和快照在 `2026-08-26` 复核，状态为 historical/after-close，不是实时数据。本 session 没有成功调用 Futu MCP，因此不把该快照称为 Futu 或 live。图像和数据入口见[`H/L 首批人工看图合同资产`](../assets/visual_recognition/2026-08-26/hl_contract_batch/README.md)及[`hl_contract_batch_prices_2026-08-26.csv`](hl_contract_batch_prices_2026-08-26.csv)。

已有案例记录中 AAPL、TSM、JNJ 的公共历史价格与旧记录存在明显尺度/数值不一致，本批不把它们强行混入。选择 TSLA 与 CRWD 是因为局部价格、两年 Daily 图和已有人工记录可以在当前历史快照下交叉核对；这不等于跨数据源完全等价。

`max_hold_bars=10` 是本批在回放前固定的研究参数，不是 PA Research 生产规则，也不代表用户实际持仓周期。H2 的 `326.64` 来自已有案例的 15m 确认记录；本批 Daily 回放把它作为预先冻结的触发价代理，不声称 Daily OHLC 可以重建 15m 的成交顺序，因此该行的结果只能做条件/描述性审计。

## 五个冻结合同

合同原始字段见[`hl_contracts_2026-08-26.csv`](hl_contracts_2026-08-26.csv)。以下的 R/R 只是在合同冻结时用第一障碍计算的几何，不是胜率或收益保证。

| 合同 | 方向/标签 | lineage | EMA20/50 闸门 | 回调位置与 META | 触发 / 结构止损 / 第一障碍 | 冻结前判断 |
| --- | --- | --- | --- | --- | --- | --- |
| [`TSLA 2025-08-18`](../assets/visual_recognition/2026-08-26/hl_contract_batch/TSLA_Daily_2y_cutoff_2025-08-18.png) | `long / H1` | `TSLA-2025-08-local` | `up/up / long_pass` | EMA20 重测、前期支撑；`absent` | `336.27 / 326.50 / 340.47`；约 `0.43R` | 第一次尝试外形成立，但第一阻力太近，属于边界/不宜直接入场 |
| [`TSLA 2025-08-21`](../assets/visual_recognition/2026-08-26/hl_contract_batch/TSLA_Daily_2y_cutoff_2025-08-21.png) | `long / H2` | `TSLA-2025-08-local`（与 H1 共享） | `up/up / long_pass` | EMA20、EMA50、重复支撑；`present` | `326.64 / 313.50 / 340.55`；约 `1.06R` | 第一次失败后的支撑簇第二次尝试；低周期确认条件成立才有研究价值 |
| [`TSLA 2025-03-03`](../assets/visual_recognition/2026-08-26/hl_contract_batch/TSLA_Daily_2y_cutoff_2025-03-03.png) | `short / L1` | `TSLA-2025-03-L1` | `down/down / short_pass` | 向下 EMA20、前支撑转阻力；`present` | `277.30 / 304.00 / 273.60`；约 `0.14R` | 强空头 A 后第一次空头尝试，但第一支撑过近；次日跳空使原 stop 分支必须跳过 |
| [`TSLA 2024-03-12`](../assets/visual_recognition/2026-08-26/hl_contract_batch/TSLA_Daily_2y_cutoff_2024-03-12.png) | `short / L2` | `TSLA-2024-03-L2` | `down/down / short_pass` | 向下 EMA20、前期阻力；`present` | `172.41 / 182.87 / 153.75`；约 `1.78R` | L1 失败后在区间上沿反转背景下的第二次空头尝试；过程仍需看先止损还是到支撑 |
| [`CRWD 2024-10-02`](../assets/visual_recognition/2026-08-26/hl_contract_batch/CRWD_Daily_2y_cutoff_2024-10-02.png) | `long / H2` | `CRWD-2024-10-local` | `up/flat / fail_flat_or_opposite` | EMA20、重复支撑；`present` | `70.54 / 67.40 / 75.11`；约 `1.46R` | 形态和空间可研究，但 EMA50 走平，按当前硬规则只作 observation-only |

### 人工图表复核摘要

- TSLA `2025-08-18`：两年背景是从低位恢复后进入更大恢复区间；局部 H1 在 EMA20/50 上方出现，但前方 `340.47` 左侧高点距离很近。后续 `8/19–8/20` 的下探证明它不能仅凭一根收强阳线升级为高质量入场。
- TSLA `2025-08-21`：左侧 `348.68–357.54` 是更大阻力簇，`314.60–320.11` 是局部支撑簇；H1 失败后，支撑附近的第二次恢复可近似读成 H2。大级别止损会压低空间，故只保留条件研究。
- TSLA `2025-03-03`：两年图显示高位回落后的空头背景，EMA20/50 同步向下；`2/27–2/28` 的 `280.88–273.60` 是触发附近的支撑带。原始 `277.30` sell-stop 在 `3/4` 开盘 `270.93` 下方跳过，不能回填为按 `277.30` 成交。
- TSLA `2024-03-12`：两年图显示较大的空头/区间上沿失败背景，EMA20/50 向下；`3/12` 的第一次下探失败后，`3/13` 跌破 `172.41` 并收在低位，构成 L2 研究合同。`152.37–153.75` 是入场前可见左侧支撑，但后续路径先越过 `182.87`，所以过程是 stop-first 边界。
- CRWD `2024-10-02`：两年背景从事件冲击后恢复，局部 H2-like 位于 EMA20/重复支撑附近；但 EMA50 数值变化很小且图上近似走平，不能写成多头 `long_pass`。该案例保留为硬闸门反例，不进入交易胜率分母。

## 依赖、分层与结果口径

TSLA `2025-08-18` H1 和 `2025-08-21` H2 共享一个局部行情 lineage，不能因为两个日期或两个标签就当成两个独立样本。TSLA `2025-03-03` L1、TSLA `2024-03-12` L2、CRWD `2024-10-02` H2 使用独立 lineage 标识，但样本仍太少，且存在边界合同，不能验证规则。

回放结果在合同冻结并提交后生成，运行元数据必须保留数据源、历史状态、成本和范围声明。回放器的 `results.csv` / `summary.json` / `run_metadata.json` 生成目录不提交为仓库运行产物；本报告在回放后补写实际结果。预期解释顺序是：先看合同是否有资格交易，再看是否成交，再看退出路径，最后才看描述性 `win_rate_pct`、`realized_R` 和分层结果；共享 lineage、空间 `blocked`、缺口跳过、观察样本和未完成路径不混入普通胜率。

## 当前结论

在回放完成前，本批只能声明：`5` 个合同已完成冻结前字段，`4` 个通过 EMA 方向闸门，`1` 个因 EMA50 走平保留为 `observation_only`；H1/H2 的共享 lineage 和 H1/L1 的第一障碍空间不足已经显式记录。即使后续路径出现盈利，也不会把这五行升级为验证样本；当前总体验证结论继续是 `no-new-positive`。

下一步只是在冻结合同之后运行分层回放并把真实 `fill_status`、`exit_reason`、`trade_result`、`realized_R` 写入本文件；不修改规则、不扩展成扫描器、不连接执行层。

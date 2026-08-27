# PA Research 冻结合同回放器

状态：`research_only / descriptive_only / not-validated / no-new-positive`

这里是 PA Research 的 `backtesting.py` 适配层（当前引擎版本 `0.3.1`）。它只回放已经由人工完整看图后冻结的合同，不自动筛选股票、不识别三推/H1/L1、不下载行情，也不连接 Execution Agent。

## 运行

在仓库根目录创建临时虚拟环境或使用已准备好的 Python 环境，安装固定依赖：

```powershell
py -3 -m pip install -r .\requirements-backtesting.txt
py -3 .\scripts\pa_research_backtest.py `
  --prices .\research\backtesting\prices.example.csv `
  --contracts .\research\backtesting\contracts.example.csv `
  --output-dir .\research\backtesting\example-output
```

程序写出：

- `results.csv`：每个冻结合同一行，包含成交、退出、空间、`realized_R` 和证据状态；
- `summary.json`：按 pattern、方向、订单分支、事件状态、`lineage_id`、EMA 斜率闸门和 META 的描述性分层；
- `run_metadata.json`：数据源、时间状态、成本和 PA Research 范围声明。

## 输入合同

价格文件必须包含 `Date,Open,High,Low,Close`，可以包含 `Symbol,Volume`。多标的文件用 `Symbol` 分组；单标的文件必须在命令行传 `--symbol`。程序不会替代数据源、复权、公司行动或两年图表审查。

合同文件的通用字段必须包含：

```text
sample_id,symbol,decision_date,direction,primary_pattern,internal_label,
order_branch,entry_trigger,structural_stop,first_obstacle,target_price,
max_hold_bars,gap_policy,label_source,daily_context_window,
major_high_low_review,ema20_50_200_review,event_context,contract_frozen,lineage_id
```

对于 `internal_label=H1/H2/L1/L2`，还必须填写以下人工看图字段：

```text
daily_ema20_slope,daily_ema50_slope,h_l_ema_slope_gate,
h_l_pullback_location,meta_confluence,meta_zone,meta_components
```

多头 H1/H2 只有在 Daily EMA20、EMA50 都为 `up` 且
`h_l_ema_slope_gate=long_pass` 时才进入回放；空头 L1/L2 对称要求两条均线都为
`down` 且闸门为 `short_pass`。`fail_flat_or_opposite` 会保留为
`observation_only` 并跳过成交，不进入胜率分母；`pending` 会保留为未证实状态。
`meta_confluence=present` 时，`meta_zone` 和至少两个以分号、逗号、`|` 或 `+`
分隔的独立来源必须同时存在。META 只用于记录和结果分层，不能代替触发、空间或结构止损。

第一版支持：

- `stop_confirmation`：在 `decision_date` 收盘后提交 stop；
- `limit_retest`：在 `decision_date` 收盘后提交 limit；
- `market_close`：在 `decision_date` 收盘成交；此分支的 `gap_policy` 必须为 `not_applicable`。

`label_source` 必须为 `human_chart_review`，并且必须有 `>=2y` Daily 背景、完整重要高低点审查和完整 EMA20/50/200 审查。`target_price`、结构止损、最大持有 K 线数必须在结果发生前冻结，否则不能进入胜率分母。

`lineage_id` 是可选但建议填写的依赖控制字段：共享同一父级行情、A/B 回调或局部尝试 lineage 的合同可以分别保留，但不能因为触发日期不同就当成独立统计样本。回放器只保留并分层该字段，不替研究者决定哪些样本独立。

本批冻结合同见 [`hl_contracts_2026-08-26.csv`](hl_contracts_2026-08-26.csv)，历史价格快照见 [`hl_contract_batch_prices_2026-08-26.csv`](hl_contract_batch_prices_2026-08-26.csv)，人工图表资产和来源边界见 [`H/L 首批人工看图合同资产`](../assets/visual_recognition/2026-08-26/hl_contract_batch/README.md)。

第二批冻结合同见 [`hl_contracts_batch2_2026-08-26.csv`](hl_contracts_batch2_2026-08-26.csv)，历史价格快照见 [`hl_contract_batch2_prices_2026-08-26.csv`](hl_contract_batch2_prices_2026-08-26.csv)，人工图表资产和来源边界见 [`H/L 第二批人工看图合同资产`](../assets/visual_recognition/2026-08-26/hl_contract_batch2/README.md)。第二批仍是独立研究批次，不与首批结果合并为已验证胜率。

本轮大样本冻结合同见 [`hl_large_contracts_2026-08-27.csv`](hl_large_contracts_2026-08-27.csv)，历史价格快照见 [`hl_large_prices_2026-08-27.csv`](hl_large_prices_2026-08-27.csv)，冻结前人工筛选记录见 [`hl_large_selection_2026-08-27_CN.md`](hl_large_selection_2026-08-27_CN.md)，图表资产和来源边界见 [`H/L 大样本回测人工看图资产`](../assets/visual_recognition/2026-08-27/hl_large_backtest/README.md)。本轮仍是独立研究批次；目标胜率为用户修正后的 `60%`，不是生产规则或已验证结果。

本轮大样本回放审计见 [`hl_large_replay_2026-08-27_CN.md`](hl_large_replay_2026-08-27_CN.md)。其 `76.47%` 仅是 17 条完成成交的描述性胜率；严格空间合格完成样本只有 1 条，当前 `validated win-rate` 仍为 `not-computable`，结论保持 `no-new-positive`。

下一批 H/L 人工冻结合同见 [`hl_next_contracts_2026-08-27.csv`](hl_next_contracts_2026-08-27.csv)，历史价格快照见 [`hl_next_prices_2026-08-27.csv`](hl_next_prices_2026-08-27.csv)，冻结前人工选择和事件分层记录见 [`hl_next_selection_2026-08-27_CN.md`](hl_next_selection_2026-08-27_CN.md)，图表资产和来源边界见 [`H/L 下一批人工看图回放资产`](../assets/visual_recognition/2026-08-27/hl_next_backtest/README.md)。本批包含 5 条合同：3 条普通非事件、2 条事件驱动；全部通过事前 `>=1R` 空间字段，但只有 2 条成交完成，1 胜 1 负，描述性胜率 `50.00%`，60% 目标仍未验证。

下一批分层回放审计见 [`hl_next_replay_2026-08-27_CN.md`](hl_next_replay_2026-08-27_CN.md)。普通非事件组 3 条均为 opening-skip、没有完成成交分母；事件组 2 条为 1 胜 1 负。事件组与普通组不混算，当前结论继续为 `no-new-positive`。

下一批（二）人工冻结合同见 [`hl_next2_contracts_2026-08-27.csv`](hl_next2_contracts_2026-08-27.csv)，历史价格快照见 [`hl_next2_prices_2026-08-27.csv`](hl_next2_prices_2026-08-27.csv)，冻结前人工选择和 H2/L2 边界记录见 [`hl_next2_selection_2026-08-27_CN.md`](hl_next2_selection_2026-08-27_CN.md)，图表资产和来源边界见 [`H/L 下一批（二）人工看图回放资产`](../assets/visual_recognition/2026-08-27/hl_next2_backtest/README.md)。本批冻结 2 条普通非事件 H1（TOL、VEEV）；H2/L2 没有合格新正例，未为凑样本加入。

下一批（二）分层回放审计见 [`hl_next2_replay_2026-08-27_CN.md`](hl_next2_replay_2026-08-27_CN.md)。2 条合同均成交并到达第一障碍，描述性结果 2 胜 0 负、100.00%、总计 +2.5925R；95% Wilson 区间约 34.24%–100.00%，样本不足，60% 仍未验证，结论保持 `no-new-positive`。

## 关键执行边界

1. 订单只从 `decision_date` 之后开始生效；程序不读取未来结果来创建 pattern 标签。
2. `gap_policy=skip` 遇到第一根 K 线开盘跳过触发位时记录 `opening-skip`；`accept_open` 记录实际开盘成交；两者不混算。
3. 止损和目标在入场 K 线完成后才挂入，避免把入场 K 线内无法确定的先后顺序伪装成结果。
4. 后续 K 线同时触及止损和目标时，结果标记为 `ambiguous_intrabar`，不进入胜率分母。
5. 结果使用 `backtesting.py` 的交易记录，并以净 PnL 除以结构风险计算 `realized_R`；手续费和 spread 由命令行传入并写入元数据。
6. 第一障碍空间只做事前几何字段，不自动授权、不自动排除，也不把首障碍到达改写成胜利。
7. 回放器不计算 EMA 斜率或自动寻找 META；这些字段必须来自回放前的人工图表审查，并在结果中原样保留。

## 目前不能说明什么

这个工具不是图表识别器、量化扫描器或生产交易系统。它只能回答：在人工冻结的同一入场/止损/目标/时间合同下，历史价格路径如何结束。样本不足、合同不一致、共享 lineage、事件分层或未解决的同 K 线冲突，都只能做描述性统计；当前 PA Research 的总体验证状态仍是 `no-new-positive`、`validated win-rate: not-computable`。

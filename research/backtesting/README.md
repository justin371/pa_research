# PA Research 冻结合同回放器

状态：`research_only / descriptive_only / not-validated / no-new-positive`

这里是 PA Research 的 `backtesting.py` 适配层（当前引擎版本 `0.3.9`）。它只回放已经由人工完整看图后冻结的合同，不自动筛选股票、不识别三推/H1/L1、不下载行情，也不连接 Execution Agent。

当前人工冻结合同的方向、H/L 标签、事件、空间和 lineage 覆盖见[`人工冻结合同覆盖审计`](contract_coverage_audit_2026-08-28_CN.md)。研究记录与当前回放输入的字段边界见[`合同权威与字段一致性审计`](contract_authority_consistency_audit_2026-08-29_CN.md)；现有 CSV inventory 与资格隔离见[`合同 CSV inventory 与资格边界审计`](contract_csv_inventory_audit_2026-08-29_CN.md)；validator 与 engine 的合同 parity 见[`文档 validator 与 engine 合同 parity 审计`](validator_engine_contract_parity_audit_2026-08-29_CN.md)；报告、索引与 inventory 的当前一致性见[`报告、索引与 inventory 一致性审计`](report_index_inventory_consistency_audit_2026-08-29_CN.md)；各批次报告数字、方向/标签、事件/空间和 lineage 的逐批重算见[`批次报告数字与分层一致性审计`](batch_report_numeric_consistency_audit_2026-08-29_CN.md)。这些审计只检查合同记录/边界完整性，不代表胜率验证。

视觉资产、冻结合同截止图与事前/结果证据隔离见[`视觉资产与事前证据边界审计`](visual_asset_pre_entry_evidence_audit_2026-08-29_CN.md)。该审计区分仓库内 105 张 PNG 与 `hl_next4/hl_next5` 的外部 artifact，不把人工画面抽查当作自动识别或胜率证据。外部 PNG 的逻辑文件清单、哈希和 ROST 决策日图缺失边界见[`外部视觉 artifact provenance 审计`](external_visual_artifact_provenance_audit_2026-08-29_CN.md)及[`外部视觉 artifact manifest`](external_visual_artifact_manifest_2026-08-29.json)。

ABC/BOP 的视觉案例准入清单见[`ABC/BOP 合同准入审计`](abc_bop_contract_intake_audit_2026-08-28_CN.md)及[`abc_bop_contract_intake_2026-08-28.csv`](abc_bop_contract_intake_2026-08-28.csv)。该 CSV 明确标记 `contract_frozen=no`，不是回放输入，不增加胜率分母。NFLX/TSM 的逐字段冻结复核见[`ABC 候选合同冻结复核`](abc_bop_candidate_freeze_review_2026-08-28_CN.md)；V、NVDA、KLAC、CRWD 的多头候选复核见[`多头 ABC/H1/H2 候选合同审计`](abc_bullish_candidate_contract_audit_2026-08-28_CN.md)。

跨 Pattern 统计隔离见[`跨 Pattern 统计隔离审计`](cross_pattern_statistics_isolation_audit_2026-08-29_CN.md)；事件与首障碍空间资格见[`事件与首障碍空间资格审计`](event_space_eligibility_audit_2026-08-29_CN.md)；事件、空间与独立性字段引用见[`事件、空间与独立性字段引用一致性审计`](event_space_lineage_consistency_audit_2026-08-29_CN.md)；H/L raw `event_context` 与 canonical `event_bucket` 标签一致性见[`H/L event bucket 标签一致性审计`](event_bucket_label_consistency_audit_2026-08-29_CN.md)；`special_subtype` 与事件轴边界见[`H/L special subtype 与事件轴一致性审计`](special_subtype_event_axis_consistency_audit_2026-08-29_CN.md)；H/L A/B 质量、位置和 EMA 字段边界见[`H/L A/B 质量、位置与 EMA 字段一致性审计`](hl_leg_quality_location_axis_consistency_audit_2026-08-29_CN.md)；H/L EMA 闸门、回调位置和报告分母见[`H/L EMA 闸门、回调位置与报告分母一致性审计`](hl_ema_gate_report_consistency_audit_2026-08-29_CN.md)；H/L 回调位置文本语义与方向边界见[`H/L 回调位置文本语义与方向边界审计`](hl_pullback_location_semantics_audit_2026-08-29_CN.md)；冻结合同字段覆盖与分层见[`冻结合同字段覆盖与分层完整性审计`](frozen_contract_field_partition_audit_2026-08-29_CN.md)；事前证据与结果证据隔离见[`事前证据与结果证据隔离审计`](pre_entry_result_evidence_isolation_audit_2026-08-29_CN.md)；旧结果事前 provenance 完整性见[`旧结果事前 provenance 完整性审计`](legacy_result_provenance_completeness_audit_2026-08-29_CN.md)；artifact schema round-trip 见[`回放 artifact schema round-trip 审计`](artifact_schema_roundtrip_audit_2026-08-29_CN.md)；全仓库 artifact inventory 见[`回放 artifact 全仓库 inventory 审计`](artifact_inventory_audit_2026-08-29_CN.md)；版本与结论表述一致性见[`回放版本与结论表述一致性审计`](version_conclusion_consistency_audit_2026-08-29_CN.md)；H/L 报告空间、版本与结论表述一致性见[`H/L 报告空间、版本与结论表述一致性审计`](hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md)；范围隔离与依赖边界见[`回放范围隔离与依赖边界审计`](scope_boundary_dependency_audit_2026-08-29_CN.md)；输入边界与 provenance bug 见[`回放输入边界与 provenance bug 审计`](input_boundary_bug_audit_2026-08-29_CN.md)；结果分母与 horizon 语义见[`回放结果分母与 horizon 审计`](replay_outcome_denominator_audit_2026-08-29_CN.md)；lineage、重复 artifact 与样本独立性见[`回放 lineage 与样本独立性审计`](replay_lineage_independence_audit_2026-08-29_CN.md)；历史 artifact 版本/数值对应和再现性见[`回放 provenance 与再现性审计`](replay_provenance_reproducibility_audit_2026-08-29_CN.md)；历史回放结果、交易日志与当前分母边界见[`历史回放结果、交易日志与分母 provenance 审计`](historical_replay_result_log_provenance_audit_2026-08-29_CN.md)。这些审计都不增加回放分母。

H/L META 状态、组件与空间/授权边界见[`H/L META 字段与授权边界审计`](hl_meta_boundary_audit_2026-08-29_CN.md)。

H/L 视觉前置字段、资产映射与决策日 provenance 边界见[`H/L 视觉前置证据与冻结资格审计`](hl_visual_preflight_contract_audit_2026-08-29_CN.md)。

BOP 多日回踩的独立准入清单见[`BOP 合同准入审计`](bop_contract_intake_audit_2026-08-28_CN.md)及[`bop_contract_intake_2026-08-28.csv`](bop_contract_intake_2026-08-28.csv)。该 CSV 只记录现有人工案例的接受、回测和边界状态，全部为 `contract_frozen=no`，不是回放输入。两类 intake 合计 25 行，按底层案例键归并为 22 个案例，其中 3 个案例同时出现在统一和 BOP 专项视图中；详细 schema、方向和引用核对见[`ABC/BOP intake schema 一致性审计`](abc_bop_intake_schema_consistency_audit_2026-08-29_CN.md)。

## 运行

在仓库根目录创建临时虚拟环境或使用已准备好的 Python 环境，安装固定依赖：

```powershell
py -3 -m pip install -r .\requirements-backtesting.txt
py -3 .\scripts\pa_research_backtest.py `
  --prices .\research\backtesting\prices.example.csv `
  --contracts .\research\backtesting\contracts.example.csv `
  --output-dir .\research\backtesting\example-output
```

对已经存在的回放输出做只读 provenance 校验：

```powershell
py -3 .\scripts\validate_pa_research_artifact.py .\research\backtesting\example-output
```

该校验器不下载行情、不重跑回放、不写回 artifact，并会核对 metadata 记录的 engine 源文件 hash。返回码固定为 `0=current_valid`、`2=historical_incomplete`、`1=invalid`；`current_valid` 只表示 artifact schema/provenance 链路完整，不等于胜率已经验证。缺失当前字段或旧 engine 的输出保留为 `historical_incomplete`，文件解析失败、源码文件不可用、hash 或 round-trip 不一致则为 `invalid`。

程序写出：

- `results.csv`：每个冻结合同一行，包含成交、退出、空间、`realized_R`、`win_rate_eligible`、`sample_id`、`lineage_id`、可选 `market_context_id` 和证据状态；
- `summary.json`：按 pattern、方向、订单分支、事件状态、`lineage_id`、EMA 斜率闸门和 META 的描述性分层，并显式报告重复结果、共享 lineage/市场状态、持仓区间重叠、事前 `pre_entry_provenance_status`、严格胜率分母、事前派生字段 mismatch 和互斥结果 bucket；
- `run_metadata.json`：引擎/依赖/运行时版本、引擎源码 SHA-256、数据源、时间状态、成本、输入文件 SHA-256、结果集和实际 `results.csv` SHA-256，以及 `summary_provenance`（实际结果列名、事前 provenance 状态计数、完成分母和各类 mismatch 计数）和 PA Research 范围声明；`summary.json` 内嵌的 metadata 应与独立文件一致。

## 输入合同

价格文件必须包含 `Date,Open,High,Low,Close`，可以包含 `Symbol,Volume`。多标的文件用 `Symbol` 分组；单标的文件必须在命令行传 `--symbol`。程序不会替代数据源、复权、公司行动或两年图表审查。

`contract_scope`、`data_status`、`chart_scope` 和 `timeframes_seen` 属于上游视觉/研究记录的证据 provenance，不从价格 CSV 推断，也不会被回放器补写；输入 CSV 只保留冻结合同需要的 `daily_context_window` 及其余机器字段。`daily_context_window` 不是“CSV 有两年价格”这一事实的别名，必须来自逐标的人工看图记录；缺失时按合同不完整处理。

合同文件的通用字段必须包含：

```text
sample_id,symbol,decision_date,direction,primary_pattern,internal_label,
order_branch,entry_trigger,structural_stop,first_obstacle,target_price,
max_hold_bars,gap_policy,label_source,daily_context_window,
major_high_low_review,ema20_50_200_review,event_context,contract_frozen,lineage_id
```

`market_context_id` 是可选的人工依赖标识，不是扫描器推断的市场状态。缺失时仍可回放逐行结果，但不能据此宣称跨标的市场环境独立。

### 选择记录与结果记录的边界

`*_selection_*.md`、候选卡和视觉资产 README 属于入场前记录：可以冻结 `direction`、`primary_pattern`/`internal_label`、`signal_bar`、`new_trigger`、`structural_invalidation`、`structural_stop`、`first_independent_obstacle`、`space_status`、`event_context` 和 `lineage_id`，但不能写入实际成交、退出、胜负、完成成交数、胜率或 `realized_R`。这些事后字段只属于独立 replay/result 记录；结果不得反向改写入场前字段。该边界的逐文件复核见[`选择记录与回放结果证据边界审计`](pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md)。

### 研究记录与回放输入的边界

统一输出合同和视觉复核卡为了保留边界案例，允许比当前回放器更宽的记录状态。当前 engine `0.3.9` 的回放输入边界如下，必须在冻结合同时显式收敛：

- `direction` 只接受 `long` 或 `short`；`no_valid_direction` 是研究记录状态，不能进入回放。
- `primary_pattern` 接受 `ABC_CONT`、`BOP`、`H1_L1`、`H2_L2`、`H3_L3`、`RFB`、`MTR`、`other`。其中额外的 H/L、三推和旧模式值是历史/兼容冻结合同的支持，不改变当前日线候选顶层只用 `ABC_CONT/BOP` 的规则。
- `order_branch` 只接受 `stop_confirmation`、`limit_retest`、`market_close`。研究记录中的 `stop_limit` 和 `observation_only` 不能直接传给当前回放器；`observation_only` 不建立交易合同，`stop_limit` 不能静默当作普通 stop。
- `entry_trigger`（非 `market_close`）、`structural_stop`、`first_obstacle` 和 `target_price` 必须是有限数值；研究卡中的价格区域、`pending`、`unknown` 或说明性文字必须先冻结为数值合同，不能直接传入。
- 记录字段 `actual_fill_or_open_skip` 与结果字段 `fill_status` 分开维护。结果字段使用 `filled`、`no-fill`、`opening-skip`、`unproven`、`not-traded` 等 engine 状态，不能用记录字段反推成交或胜率资格。

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

`meta_confluence` 的冻结合同枚举只有 `present`、`absent`、`unknown`；`pending` 只能出现在整体审查、触发或 gate 状态，不能写进该字段。若 META 证据不足，用 `unknown`，不能用 META 推导 `pre_entry_space_R`、`space_status`、成交资格或结果。

`contract_frozen=yes` 只证明冻结 CSV 的字段和几何已闭合，不证明仓库或外部 artifact 仍有可独立复核的决策日无标签图。若视觉资产缺失、只有 partial 或只有 post-decision 图，保留 provenance gap，历史回放只能是 descriptive research record；不能把它升级为新的可交易候选或 validated sample。

`h_l_pullback_location` 是自由文本的位置说明，不是 gate、空间或方向枚举。`rising`/`falling`、`support`/`resistance` 和 `role_reversal` 只提供人工上下文；空头的 `support` 必须结合前期/破位角色转换或事件位置阅读，不能把当前未破支撑当成空头资格。位置文字不能覆盖 `direction`、EMA20/50 斜率、`h_l_ema_slope_gate` 或 `space_status`，也不能把其中的历史 `controlled_B`/`deep_late_controlled_B` 词当成独立 `b_leg_class`/`b_leg_location`。

`a_leg_quality`、`b_leg_class`、`b_leg_location` 是上游视觉记录的分开字段，不属于当前 H/L 回放最小必需列；当前 H/L 回放只消费 `h_l_ema_slope_gate` 与 `h_l_pullback_location` 等已列出的合同字段。历史 CSV 可能缺少 A/B 字段，或含 `strong_A`、`ordinary_A`、`controlled_B`、`deep_late_controlled_B` 旧别名；它们只按登记映射用于说明，不由 engine 静默标准化，也不能由 `h_l_pullback_location` 或结果补齐 `b_leg_location`。

`primary_pattern=H3_L3` 时，`internal_label` 必须明确为 `H3` 或 `L3`，不能使用合并的 `H3_L3`；H3/L3 的方向和结果必须分开统计。`primary_pattern=BOP` 不得用 H1/H2/L1/L2/H3/L3 充当内部标签，相关 ABC、H/L 或三推信息只能作为 `secondary_context` 保留。

第一版支持：

- `stop_confirmation`：在 `decision_date` 收盘后提交 stop；
- `limit_retest`：在 `decision_date` 收盘后提交 limit；
- `market_close`：在 `decision_date` 收盘成交；此分支的 `gap_policy` 必须为 `not_applicable`。

`label_source` 必须为 `human_chart_review`，并且必须有 `>=2y` Daily 背景、完整重要高低点审查和完整 EMA20/50/200 审查。`target_price`、结构止损、最大持有 K 线数必须在结果发生前冻结，否则不能进入胜率分母。

`pre_entry_space_R` 和 `space_status` 是建议冻结的首障碍空间证据；旧合同缺失时必须按 `unknown_contract_space` 处理，不能从回放后的价格路径倒推为 `strict_ge_1R`。回放摘要中的 `event_bucket` 是对原始 `event_context` 的保守分类：未核实、待定、未知和未分类状态不能升级为普通非事件。摘要会从原始事前字段重算 `event_bucket`、`contract_space_bucket`；结果文件中携带的派生副本只用于报告 mismatch，不能覆盖事前字段。`special_subtype` 是上游视觉/日线候选的辅助注释，不属于当前 H/L 最小回放合同，也不参与 `event_bucket` 派生；其缺失不能被当作 `ordinary` 或由结果回填。

回放摘要的 `completed_trade_count` 不是简单的 `trade_result` 行数。它要求 `pre_entry_provenance_status=complete`、`win_rate_eligible=yes`、`trade_result` 为 `win/loss/scratch`、`fill_status=filled`、`evidence_status=comparable`、非空 `path_result`、没有 `ambiguous_intrabar` 或 `incomplete-horizon`，并且有有限的 `realized_R`；缺失 `path_result` 的结果没有足够路径审计证据，只能保留在排除 bucket。`win_rate_eligible_count` 只是旗标数量，二者不一致时以严格交集为分母并保留 mismatch/guard 计数。缺少合同、事件、非收盘分支的 `planned_entry_trigger` 或 H/L EMA 事前字段的结果行标为 `incomplete`，只保留描述性记录。`first_obstacle_hit` 只表示路径过程，不能把首障碍到达自动改写成胜利。

`lineage_id` 是冻结合同的必填依赖控制字段：共享同一父级行情、A/B 回调或局部尝试 lineage 的合同可以分别保留，但不能因为触发日期不同就当成独立统计样本。回放器会保留并分层该字段，并在共享 lineage 时撤回 independence-adjusted 胜率；它不替研究者决定哪些样本独立。

回放摘要还会从结果行中的 H/L EMA gate 重算 `contract_eligibility`；当 gate 字段存在时，手工改写的 eligibility 不得进入完成交易分母，并以 `contract_eligibility_mismatch_count` 留痕。摘要还会对相同 `sample_id`、相同合同族（symbol/date/direction/pattern/label/lineage）和同一标的重叠持仓区间做依赖诊断。重复结果全部标记为 `duplicate_result`，不任意保留一份；持仓区间重叠、缺失或共享 `market_context_id`、缺失 sample identity 或共享 lineage 时，只保留描述性行数结果，并撤回 independence-adjusted 胜率。不同 `lineage_id` 也不自动证明市场状态独立。

本批冻结合同见 [`hl_contracts_2026-08-26.csv`](hl_contracts_2026-08-26.csv)，历史价格快照见 [`hl_contract_batch_prices_2026-08-26.csv`](hl_contract_batch_prices_2026-08-26.csv)，人工图表资产和来源边界见 [`H/L 首批人工看图合同资产`](../assets/visual_recognition/2026-08-26/hl_contract_batch/README.md)。

第二批冻结合同见 [`hl_contracts_batch2_2026-08-26.csv`](hl_contracts_batch2_2026-08-26.csv)，历史价格快照见 [`hl_contract_batch2_prices_2026-08-26.csv`](hl_contract_batch2_prices_2026-08-26.csv)，人工图表资产和来源边界见 [`H/L 第二批人工看图合同资产`](../assets/visual_recognition/2026-08-26/hl_contract_batch2/README.md)。第二批仍是独立研究批次，不与首批结果合并为已验证胜率。

本轮大样本冻结合同见 [`hl_large_contracts_2026-08-27.csv`](hl_large_contracts_2026-08-27.csv)，历史价格快照见 [`hl_large_prices_2026-08-27.csv`](hl_large_prices_2026-08-27.csv)，冻结前人工筛选记录见 [`hl_large_selection_2026-08-27_CN.md`](hl_large_selection_2026-08-27_CN.md)，图表资产和来源边界见 [`H/L 大样本回测人工看图资产`](../assets/visual_recognition/2026-08-27/hl_large_backtest/README.md)。本轮仍是独立研究批次；目标胜率为用户修正后的 `60%`，不是生产规则或已验证结果。

本轮大样本回放审计见 [`hl_large_replay_2026-08-27_CN.md`](hl_large_replay_2026-08-27_CN.md)。报告中的 `76.47%` 是由旧 engine `0.3.1` 产物计算的历史描述值；其中 `bars_held=11` 按当前定义是十根完整观察 K 线后的下一根开盘执行索引，不是额外自由持仓。engine `0.3.9` 保留该合同语义，并增加重复结果、市场上下文/持仓重叠、输入指纹、源码指纹、显式空间证据和事前 provenance/派生字段防护；历史 artifact 未静默重写。按冻结价格几何计算的严格空间子集只有 1 条完成样本，但旧 CSV 没有显式 `pre_entry_space_R/space_status`，当前 engine 将其 37 条合同都视为 `unknown_contract_space`；因此该子集不能读成当前显式 strict-space 胜率。当前 `validated win-rate` 仍为 `not-computable`，结论保持 `no-new-positive`。

下一批 H/L 人工冻结合同见 [`hl_next_contracts_2026-08-27.csv`](hl_next_contracts_2026-08-27.csv)，历史价格快照见 [`hl_next_prices_2026-08-27.csv`](hl_next_prices_2026-08-27.csv)，冻结前人工选择和事件分层记录见 [`hl_next_selection_2026-08-27_CN.md`](hl_next_selection_2026-08-27_CN.md)，图表资产和来源边界见 [`H/L 下一批人工看图回放资产`](../assets/visual_recognition/2026-08-27/hl_next_backtest/README.md)。本批包含 5 条合同：3 条普通非事件、2 条事件驱动；按冻结时合同中的触发、止损和第一障碍计算的历史几何均为 `>=1R`，但该旧 CSV 没有显式 `pre_entry_space_R/space_status`，当前 engine 必须将其保留为 `unknown_contract_space`，不能当作当前显式 strict-space 字段。只有 2 条成交完成，1 胜 1 负，描述性胜率 `50.00%`，60% 目标仍未验证。

下一批分层回放审计见 [`hl_next_replay_2026-08-27_CN.md`](hl_next_replay_2026-08-27_CN.md)。普通非事件组 3 条均为 opening-skip、没有完成成交分母；事件组 2 条为 1 胜 1 负。事件组与普通组不混算，当前结论继续为 `no-new-positive`。

下一批（二）人工冻结合同见 [`hl_next2_contracts_2026-08-27.csv`](hl_next2_contracts_2026-08-27.csv)，历史价格快照见 [`hl_next2_prices_2026-08-27.csv`](hl_next2_prices_2026-08-27.csv)，冻结前人工选择和 H2/L2 边界记录见 [`hl_next2_selection_2026-08-27_CN.md`](hl_next2_selection_2026-08-27_CN.md)，图表资产和来源边界见 [`H/L 下一批（二）人工看图回放资产`](../assets/visual_recognition/2026-08-27/hl_next2_backtest/README.md)。本批冻结 2 条普通非事件 H1（TOL、VEEV）；H2/L2 没有合格新正例，未为凑样本加入。

下一批（二）分层回放审计见 [`hl_next2_replay_2026-08-27_CN.md`](hl_next2_replay_2026-08-27_CN.md)。2 条合同均成交并到达第一障碍，描述性结果 2 胜 0 负、100.00%、总计 +2.5925R；95% Wilson 区间约 34.24%–100.00%，样本不足，60% 仍未验证，结论保持 `no-new-positive`。

下一批（三）人工候选边界审计见 [`hl_next3_selection_2026-08-27_CN.md`](hl_next3_selection_2026-08-27_CN.md)，回放状态见 [`hl_next3_replay_2026-08-27_CN.md`](hl_next3_replay_2026-08-27_CN.md)。本批人工复核 18 个决策日，但没有同时通过普通非事件、清晰 H/L lineage、EMA20/50 闸门和 `>=1R` 首障碍空间的新合同；因此交易回放分母为 0，胜率不可计算，结论继续为 `no-new-positive`。Matplotlib `3.10.9` 已安装并固定，不为本批重复安装。

下一批（四）人工冻结合同见 [`hl_next4_contracts_2026-08-27.csv`](hl_next4_contracts_2026-08-27.csv)，历史价格快照见 [`hl_next4_prices_2026-08-27.csv`](hl_next4_prices_2026-08-27.csv)，冻结前人工选择和 24 只新普通股的两年 Daily 审查见 [`hl_next4_selection_2026-08-27_CN.md`](hl_next4_selection_2026-08-27_CN.md)。本批只冻结 CBOE、ROST 两条普通非事件口径下的 `long / H1`；H2/L1/L2 没有合格新正例。

下一批（四）分层回放审计见 [`hl_next4_replay_2026-08-27_CN.md`](hl_next4_replay_2026-08-27_CN.md)。两条合同均成交但均未到达第一障碍，0 胜 2 负、描述性胜率 `0.00%`、总计 `-1.5090R`；95% Wilson 区间约 `0.00%–65.76%`，60% 目标继续待检验，结论保持 `no-new-positive`。Matplotlib `3.10.9` 只用于人工图表渲染，不识别 pattern、不创建扫描器、不连接 Execution Agent。

下一批（五）人工冻结合同见 [`hl_next5_contracts_2026-08-27.csv`](hl_next5_contracts_2026-08-27.csv)，历史价格快照见 [`hl_next5_prices_2026-08-27.csv`](hl_next5_prices_2026-08-27.csv)，冻结前人工选择记录见 [`hl_next5_selection_2026-08-27_CN.md`](hl_next5_selection_2026-08-27_CN.md)。本批从 12 只新市值约 `$3B–$100B` 的美国普通股中，仅冻结 MCHP、NDAQ 两个标的的 6 条 `short / L1` 合同；没有为凑数量加入 H2 或 L2。

下一批（五）分层回放审计见 [`hl_next5_replay_2026-08-27_CN.md`](hl_next5_replay_2026-08-27_CN.md)。6 条合同中 5 条成交并完成，3 胜 2 负，合并描述性胜率 `60.00%`、总计 `+3.4812R`；普通非事件组为 2 胜 1 负，财报邻近与财报驱动样本单独统计。样本极小、4/5 完成交易来自 NDAQ，且无 H2/L2 对照，60% 仍未验证，结论保持 `no-new-positive`。Matplotlib `3.10.9` 只用于两年 Daily 图表人工审阅和渲染，回放使用固定的 `backtesting.py 0.6.6`；不识别 pattern、不创建扫描器、不连接 Execution Agent。

## 关键执行边界

1. 订单只从 `decision_date` 之后开始生效；程序不读取未来结果来创建 pattern 标签。
2. `gap_policy=skip` 遇到第一根 K 线开盘跳过触发位时记录 `opening-skip`；`accept_open` 记录实际开盘成交；`flag_only` 也按实际开盘成交，但把 `gap_adjustment` 保留为 `flag_only`；三者不混算。
3. 止损和目标在入场 K 线完成后才挂入，避免把入场 K 线内无法确定的先后顺序伪装成结果。
4. 后续 K 线同时触及止损和目标时，结果标记为 `ambiguous_intrabar`，不进入胜率分母；歧义路径上的首障碍若不能确认在持仓仍有效时到达，则标为 `unknown`。
5. 时间退出以实际 `entry_bar` 计数；`max_hold_bars` 表示 entry 之后允许观察的完整 K 线数，非 `market_close` 的时间退出在观察窗口结束后的下一根开盘成交，因此 backtesting.py 的 `bars_held` 索引距离可能比 `max_hold_bars` 多 1，这不是额外的自由持仓。`market_close` 按收盘时间索引计数；若数据末尾没有可执行的时间退出价格则标为 `incomplete-horizon`。
6. 结果使用 `backtesting.py` 的交易记录，并以净 PnL 除以结构风险计算 `realized_R`；手续费和 spread 由命令行传入并写入元数据。
7. 第一障碍空间只做事前几何字段，不自动授权、不自动排除，也不把首障碍到达改写成胜利。
8. 回放器不计算 EMA 斜率或自动寻找 META；这些字段必须来自回放前的人工图表审查，并在结果中原样保留。
9. `engine_source_sha256`、运行时版本、`price_file_sha256`、`contract_file_sha256`、`result_set_sha256` 和 `results_file_sha256` 只用于 artifact provenance；重复输入或结果版本不能合并成更大的独立样本。

## 目前不能说明什么

这个工具不是图表识别器、量化扫描器或生产交易系统。它只能回答：在人工冻结的同一入场/止损/目标/时间合同下，历史价格路径如何结束。样本不足、合同不一致、共享 lineage、事件分层或未解决的同 K 线冲突，都只能做描述性统计；当前 PA Research 的总体验证状态仍是 `no-new-positive`、`validated win-rate: not-computable`。

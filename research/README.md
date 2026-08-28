# PA Research 研究索引

状态：`document_status=adopted / research_state=research_only / handoff_status=not_ready`

本目录保存 PA Research 的专项审计、历史案例、视觉验收记录和图像资产入口。它不是行情数据库、量化扫描器或执行层。新记录先使用[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)，方向必须明确写为 `long`、`short` 或 `no_valid_direction`。

## 当前 authority 与工作流

- [`ABC 研究状态与工作边界`](abc_research_status_v0_3_CN.md)：ABC 的快筛/深审边界；
- [`ABC + H/L 分层历史结果审计`](abc_hl_stratified_outcome_audit_2026-08-24_CN.md)：当前结果口径、样本分层和 `no_new_positive`；
- [`BOP 真实多日回踩候选审计`](bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)：普通 BOP、同日回测、事件/缺口分支和多日正例缺口；
- [`核心八个 Pattern 交叉一致性审计`](core_pattern_cross_audit_CN.md)：主标签、状态转换和历史状态别名；
- [`PA Pattern 视觉筛选协议`](visual_pattern_triage_protocol_CN.md)：快筛与深审的执行顺序；
- [`每日候选批次与图表审查卡`](../docs/daily_candidate_review_card_CN.md)：候选池覆盖、数据来源、两年 Daily 左侧、事件、流动性和空间证据的统一记录；
- [`流程改进审计（2026-08-28）`](process_improvement_audit_2026-08-28_CN.md)：记录本轮独立修复、验证证据和仍需用户决定的研究设计事项；
- [`人工冻结合同覆盖审计（2026-08-28）`](backtesting/contract_coverage_audit_2026-08-28_CN.md)：统计现有 H/L 合同的方向、标签、事件、空间和 lineage 覆盖，不把它解释为胜率；
- [`PA 图表视觉识别冒烟验收`](visual_recognition_smoke_test_2026-08-24_CN.md)：图表识别能力、两年背景和当前 acceptance-pending 状态。

## 冻结合同回放

- [`PA Research 冻结合同回放器`](backtesting/README.md)：使用固定版本 `backtesting.py` 回放人工冻结的入场、止损、目标和时间合同；不自动识别 pattern，不创建扫描器，不连接 Execution Agent。
- [`H/L 首批真实样本准入审计`](backtesting/first_hl_sample_intake_2026-08-26_CN.md)：前一阶段的两年 Daily 案例、EMA20/50 闸门、META、首障碍和合同冻结检查；该文件记录的当时状态为 `strict_h_l_contracts_frozen: 0`，现由下方首批合同回放审计承接。
- [`H/L 首批合同回放审计`](backtesting/hl_contract_batch_replay_2026-08-26_CN.md)：第一批人工冻结的 H1/H2/L1/L2 合同、两年 Daily 图和分层回放；共享 lineage、空间闸门和失败 EMA 闸门均单独保留，结论仍为 `no-new-positive`。
- [`H/L 第二批合同回放审计`](backtesting/hl_contract_batch2_replay_2026-08-26_CN.md)：第二批三个独立 lineage 的 H2/L1 合同、两年 Daily 图、EMA 闸门、空间边界和分层回放；结论继续单独维护 `no-new-positive`。
- [`H/L 第二批人工看图合同资产`](assets/visual_recognition/2026-08-26/hl_contract_batch2/README.md)：KLAC、TSM、ADBE 三张两年 Daily 图及公共历史数据来源边界。
- [`H/L 首批人工看图合同资产`](assets/visual_recognition/2026-08-26/hl_contract_batch/README.md)：本批五张两年 Daily 图及来源、时区和历史数据边界。
- [`H/L 大样本人工合同冻结记录`](backtesting/hl_large_selection_2026-08-27_CN.md)：COHR、RBLX、MAR 三标的、37 条人工冻结 H1/H2/L1/L2 合同和用户修正后的 60% 待检验目标。
- [`H/L 大样本回测人工看图资产`](assets/visual_recognition/2026-08-27/hl_large_backtest/README.md)：23 张 Matplotlib 两年 Daily 背景/局部序列图；无 pattern 标签和结果标记。
- [`H/L 大样本回放审计`](backtesting/hl_large_replay_2026-08-27_CN.md)：37 条冻结合同的描述性回放、60% 目标检验、严格 `>=1R` 空间子集和 `no-new-positive` 结论。
- [`H/L 下一批人工合同冻结记录`](backtesting/hl_next_selection_2026-08-27_CN.md)：ZS、DDOG 两个中等至大型市值标的的 5 条 H1/L1 人工冻结合同；包含两年 Daily 背景、EMA20/50 闸门、重要高低点、事件隔离和首障碍空间。
- [`H/L 下一批分层回放审计`](backtesting/hl_next_replay_2026-08-27_CN.md)：3 条普通非事件与 2 条事件驱动合同的独立回放；2 条完成成交为 1 胜 1 负，60% 目标仍未验证，结论保持 `no-new-positive`。
- [`H/L 下一批（二）人工合同冻结记录`](backtesting/hl_next2_selection_2026-08-27_CN.md)：TOL、VEEV 两条普通非事件 H1 合同、两年 Daily 视觉背景、EMA20/50 闸门、事件隔离、首障碍空间和 H2/L2 边界排除记录。
- [`H/L 下一批（二）分层回放审计`](backtesting/hl_next2_replay_2026-08-27_CN.md)：2 条 H1 合同均成交并到达第一障碍，描述性 2 胜 0 负；只有两个 lineage，Wilson 下界约 34.24%，60% 目标仍未验证，结论保持 `no-new-positive`。
- [`H/L 下一批（二）人工看图回放资产`](assets/visual_recognition/2026-08-27/hl_next2_backtest/README.md)：TOL、VEEV 的冻结前两年 Daily 图，以及 PHM H2-like/EMA 闸门拒绝边界图；Matplotlib 只负责渲染。
- [`H/L 下一批（三）人工候选边界审计`](backtesting/hl_next3_selection_2026-08-27_CN.md)：18 个候选的两年 Daily、重要高低点、支撑阻力、EMA20/50/200、事件、lineage、B 质量和空间复核；新合格交易合同为 0。
- [`H/L 下一批（三）回放状态审计`](backtesting/hl_next3_replay_2026-08-27_CN.md)：无合格合同，不创建占位回放分母；胜率不可计算，60% 继续待检验，结论保持 `no-new-positive`。
- [`H/L 下一批（四）人工合同冻结记录`](backtesting/hl_next4_selection_2026-08-27_CN.md)：24 个新市值约 `$3B–$100B` 美国普通股的两年 Daily 人工复核；仅 CBOE、ROST 的 2 条 `long / H1` 通过全部 strong-A、controlled-B、EMA、事件、lineage 和 `>=1R` 闸门。
- [`H/L 下一批（四）分层回放审计`](backtesting/hl_next4_replay_2026-08-27_CN.md)：2 条合同均成交但均未到达第一障碍，0 胜 2 负、`-1.5090R`；95% Wilson 区间约 `0.00%–65.76%`，60% 目标未验证，结论保持 `no-new-positive`。
- [`H/L 下一批（五）人工合同冻结记录`](backtesting/hl_next5_selection_2026-08-27_CN.md)：12 只新市值约 `$3B–$100B` 美国普通股的两年 Daily 人工复核；仅冻结 MCHP、NDAQ 的 6 条 `short / L1` 合同，没有合格的新 H2 或 L2 正例。
- [`H/L 下一批（五）分层回放审计`](backtesting/hl_next5_replay_2026-08-27_CN.md)：6 条人工合同中 5 条成交并完成，3 胜 2 负、合并描述性 `60.00%`、`+3.4812R`；普通、财报邻近和财报驱动分层不混算，60% 目标未验证，结论保持 `no-new-positive`。

## 优先研究矩阵与专项框架

- [`ABC 决策矩阵`](abc_decision_matrix_CN.md)；
- [`优先 Pattern 代表性视觉候选矩阵`](priority_pattern_visual_candidate_matrix_2026-08-24_CN.md)；
- [`事件/板块/大盘视觉证据审计`](event_sector_market_gate_visual_evidence_audit_2026-08-24_CN.md)；
- [`订单类型与风险合同视觉证据审计`](order_risk_contract_visual_evidence_audit_2026-08-24_CN.md)；
- [`H/L lineage 与三推状态视觉边界复核`](h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)；
- [`三推/H3-L3 压力状态框架`](three_push_pressure_state_framework_CN.md)：区间边缘三推、区间中部重复测试、趋势/通道延续和反向确认的分流；
- [`跨 Pattern 视觉优先级与冲突消解审计`](cross_pattern_visual_priority_audit_2026-08-24_CN.md)。

## 已归档但仍可复核的独立案例入口

这些文件此前没有 Markdown 入链；它们都是历史研究材料，不代表生产规则或统计样本：

- [`Codex Trading H1/H2/L1/L2 只读导入摘要`](codex_trading_h1_h2_l1_l2_import.md)：只读图表参考，PA Research 规则优先；
- [`TSLA 空头 ABC 候选筛选`](tsla_bearish_abc_candidate_screen_2026-08-22.md)；
- [`TSLA 空头 ABC 比较矩阵`](tsla_bearish_abc_comparison_matrix.md)；
- [`TSLA H1/H2 候选筛选`](tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md)。

## 图像资产入口

- [`第二轮多标的多周期视觉资产`](assets/visual_recognition/2026-08-24/round2_multisymbol/README.md)；
- [`H1/H2 与 L1/L2 局部盲测资产`](assets/visual_recognition/2026-08-24/round3_hl_drills/README.md)；
- [`Round4 历史图表视觉练习资产`](assets/visual_recognition/2026-08-24/round4_historical_practice/README.md)；
- [`Round5 两年 Daily 视觉练习资产`](assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md)；
- [`TSLA 多周期视觉识别资产`](assets/visual_recognition/2026-08-24/tsla_public_mtf/README.md)。

Round4 的 5 个直接 MTF PNG 之前没有索引入链，现统一列在其资产 README 中；它们仍因 Daily 左侧不足两年而保持 `two_year_daily: pending`。

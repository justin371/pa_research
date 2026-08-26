# PA Research 研究索引

状态：`document_status=adopted / research_state=research_only / handoff_status=not_ready`

本目录保存 PA Research 的专项审计、历史案例、视觉验收记录和图像资产入口。它不是行情数据库、量化扫描器或执行层。新记录先使用[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)，方向必须明确写为 `long`、`short` 或 `no_valid_direction`。

## 当前 authority 与工作流

- [`ABC 研究状态与工作边界`](abc_research_status_v0_3_CN.md)：ABC 的快筛/深审边界；
- [`ABC + H/L 分层历史结果审计`](abc_hl_stratified_outcome_audit_2026-08-24_CN.md)：当前结果口径、样本分层和 `no_new_positive`；
- [`BOP 真实多日回踩候选审计`](bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)：普通 BOP、同日回测、事件/缺口分支和多日正例缺口；
- [`核心八个 Pattern 交叉一致性审计`](core_pattern_cross_audit_CN.md)：主标签、状态转换和历史状态别名；
- [`PA Pattern 视觉筛选协议`](visual_pattern_triage_protocol_CN.md)：快筛与深审的执行顺序；
- [`PA 图表视觉识别冒烟验收`](visual_recognition_smoke_test_2026-08-24_CN.md)：图表识别能力、两年背景和当前 acceptance-pending 状态。

## 冻结合同回放

- [`PA Research 冻结合同回放器`](backtesting/README.md)：使用固定版本 `backtesting.py` 回放人工冻结的入场、止损、目标和时间合同；不自动识别 pattern，不创建扫描器，不连接 Execution Agent。

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

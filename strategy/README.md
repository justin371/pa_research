# PA Research Strategy 研究索引

文档状态：`document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

本目录只保存研究框架、候选清单和历史复盘入口，不是 Codex Trading 实现队列。所有新案例必须使用[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)，并明确 `direction`、`research_state`、`trade_state` 和 `handoff_status`。

统一边界：`v0.x` 规则/合同与回放引擎 `0.3.9` 均只属于 PA Research 研究层（`PA Research only`），不是 Codex Trading 生产规则；`no-new-positive` 和 `validated win-rate: not-computable` 保持不变，`60%` 仅是待检验目标；不创建量化扫描器，不连接 Execution Agent。

## 入口

- [`候选形态清单`](pattern_inventory_candidates.md)：当前研究优先级、共同字段和边界案例；
- [`Trading Framework`](00_trading_framework.md)：背景到风险的研究顺序；
- [`三推楔形候选规则`](01_three_push_wedge_candidate.md)：三推压力/衰竭/延续的研究假设；
- [`META 多重优势区域`](meta_multiple_edge.md)：位置汇聚背景，不是独立触发器；
- [`概率原则学习参考`](probability_principles_pages_1_7.md)：外部启发式，只作学习材料，不进入胜率或回测基准；
- [`TSLA/META 历史复盘`](reviews/2026-06-25-tsla-meta-example.md)：历史案例，不是实盘授权。

### 当前审计追踪的历史视觉候选

以下五个入口属于历史 `stage_1_fast_screen`/`historical_context_only` 记录，保留各自的方向、周期和缺失闸门；它们不是 `daily_candidate`、冻结合同、交易授权或胜率样本：

- [`CRM 空头 ABC L1/L2 历史视觉候选`](../research/crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md)；
- [`META 多头 ABC H1/H2 历史视觉候选`](../research/meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md)；
- [`MSFT 空头 ABC L1/L2 历史视觉候选`](../research/msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md)；
- [`NVDA 多头 ABC H1 历史视觉候选`](../research/nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md)；
- [`2024–2025 视觉候选网格`](../research/visual_screen_candidate_grid_2024_2025_CN.md)：批次级混合记录，`direction=no_valid_direction`，不代表逐标的候选。

- [`候选、视觉复核与交易日志边界一致性审计`](../research/candidate_visual_record_consistency_audit_2026-08-29_CN.md)：核对方向、候选状态、事前证据和事后路径的分轴边界。
- [`历史回放结果、交易日志与分母 provenance 审计`](../research/backtesting/historical_replay_result_log_provenance_audit_2026-08-29_CN.md)：区分冻结合同、模拟回放结果、运行 metadata 与实际交易日志；当前没有真实成交日志，结论仍为 `no-new-positive` / `validated win-rate: not-computable`。
- [`Pattern 索引、别名与主次标签边界审计`](../research/pattern_index_alias_boundary_audit_2026-08-29_CN.md)：核对 16 个 pattern 目录入口、核心/独立层级和 canonical 主次标签边界。
- [`Pattern 视觉复核前置证据审计`](../research/pattern_visual_preflight_audit_2026-08-29_CN.md)：核对完整图表左侧、EMA、适用路径的 A/B 质量（强 A→H1/L1 优先；区间边缘三推不要求强 A）、位置与首障碍的共同前置证据。
- [`Pattern 案例入口与状态一致性审计`](../research/pattern_case_entry_status_audit_2026-08-29_CN.md)：核对 16 个 pattern 的案例入口、条件/边界/no-trade 文案和状态别名。
- [`共同视觉前置字段一致性审计`](../research/common_visual_preflight_field_consistency_audit_2026-08-29_CN.md)：统一两年 Daily 左侧、重要高低点、EMA、A/B 质量、位置/空间和 `data_status` 的字段边界。
- [`Pattern 状态轴、字段与枚举一致性审计`](../research/pattern_state_axis_field_enum_audit_2026-08-29_CN.md)：核对统一状态轴、字段命名和 pattern-specific 模板边界。
- [`三推/H3-L3 与区间边缘合同边界审计`](../research/backtesting/three_push_h3_l3_contract_boundary_audit_2026-08-29_CN.md)：统一三推压力状态、区间边缘方向和订单/统计隔离。
- [`三推策略与历史案例合同一致性审计`](../research/backtesting/three_push_strategy_case_contract_audit_2026-08-29_CN.md)：统一 A/B/C 解释层、历史案例状态和订单/首障碍/空间边界。
- [`H3/L3 历史候选筛选日志证据与统计边界审计`](../research/backtesting/h3_l3_candidate_screen_provenance_audit_2026-08-29_CN.md)：区分历史数据状态、事件来源覆盖、候选字段与 no-new-positive 结论。
- [`历史视觉证据与 canonical 边界审计`](../research/backtesting/visual_evidence_canonical_boundary_audit_2026-08-29_CN.md)：统一三推/H-L 历史显示标签、两年背景证据头、方向、订单/空间和统计隔离。
- [`视觉识别冒烟、快筛协议与 Round2/Round3 资产 canonical 边界审计`](../research/backtesting/visual_recognition_canonical_boundary_audit_2026-08-29_CN.md)：核对视觉冒烟/快筛的 canonical 映射、配对资产 provenance 和候选/授权边界。
- [`Round4、Round5 与 TSLA 视觉资产 canonical 边界审计`](../research/backtesting/visual_asset_canonical_boundary_audit_2026-08-29_CN.md)：核对短窗口、两年 Daily 与 TSLA 多周期资产的 provenance、pattern 状态和 no-new-positive 边界。
- [`全部视觉资产 README canonical provenance 覆盖审计`](../research/backtesting/visual_asset_provenance_coverage_audit_2026-08-29_CN.md)：核对 11 个视觉资产目录、105 张 PNG 的 provenance、配对职责、历史别名与统计隔离。
- [`视觉历史报告与 canonical authority schema 对齐审计`](../research/backtesting/visual_authority_schema_alignment_audit_2026-08-29_CN.md)：核对视觉框架、历史报告、配对复核记录与 canonical 字段/状态轴，区分当前模板修复和历史事实别名。
- [`Pattern README 与基础视觉框架 canonical 输出覆盖审计`](../research/backtesting/pattern_foundation_canonical_contract_audit_2026-08-29_CN.md)：核对 16 个 pattern README、8 个基础层和局部模板的 canonical 字段/枚举覆盖与索引入口。
- [`requiredFiles 与研究报告索引覆盖审计`](../research/backtesting/required_report_index_coverage_audit_2026-08-29_CN.md)：核对 validator requiredFiles 中研究报告与 canonical 索引的映射，不新增样本或结果。
- [`统计结论、正例表述与授权边界一致性审计`](../research/backtesting/conclusion_boundary_consistency_audit_2026-08-29_CN.md)：统一统计状态别名、60% 待检验目标与研究/交接边界，不新增样本或结果。
- [`视觉识别能力与图表 provenance 边界审计`](../research/backtesting/visual_capability_boundary_audit_2026-08-29_CN.md)：限定人工大体识别的研究用途，核对两年 Daily、重要高低点和 EMA 前置证据，不新增样本或结果。
- [`入场几何与不交易状态边界审计`](../research/entry_geometry_state_boundary_audit_2026-08-29_CN.md)：统一首障碍、结构止损、入场前空间、粗略 R/R 和不交易状态边界。
- [`Pattern 主标签映射与 BOP 状态迁移审计`](../research/pattern_label_transition_audit_2026-08-29_CN.md)：核对日线主标签白名单、H/L 内部标签、三推/区间边缘分隔及 BOP 接受后的旧合同失效。
- [`证据范围与数据状态一致性审计`](../research/evidence_scope_status_boundary_audit_2026-08-29_CN.md)：核对多周期证据范围、逐标的两年 Daily 覆盖、数据状态与历史 session 的字段边界。
- [`选择记录与回放结果证据边界审计`](../research/backtesting/pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md)：核对选择报告、候选卡、视觉记录和 replay/result 的事前/事后字段边界；不新增样本或结果。
- [`事件、空间与独立性字段引用一致性审计`](../research/backtesting/event_space_lineage_consistency_audit_2026-08-29_CN.md)：核对事件、空间、lineage 和市场状态字段的来源与跨文件表述；修正历史几何与显式空间资格的边界。
- [`H/L event bucket 标签一致性审计`](../research/backtesting/event_bucket_label_consistency_audit_2026-08-29_CN.md)：重算 raw `event_context` 与 canonical `event_bucket`，统一 selection/replay 的事件分层显示并保留 pending/unknown 隔离。
- [`H/L special subtype 与事件轴一致性审计`](../research/backtesting/special_subtype_event_axis_consistency_audit_2026-08-29_CN.md)：区分上游 `special_subtype` 与回放合同字段，固定其不能替代 `event_context/event_bucket` 的范围。
- [`H/L A/B 质量、位置与 EMA 字段一致性审计`](../research/backtesting/hl_leg_quality_location_axis_consistency_audit_2026-08-29_CN.md)：核对 A/B 质量、B 位置、H/L EMA 闸门与回调位置的历史覆盖和 canonical 边界。
- [`H/L EMA 闸门、回调位置与报告分母一致性审计`](../research/backtesting/hl_ema_gate_report_consistency_audit_2026-08-29_CN.md)：核对 EMA 方向、回调位置、eligible/observation/pending 与报告分母，并固定 validator 的反向 gate/未知斜率边界。
- [`H/L 回调位置文本语义与方向边界审计`](../research/backtesting/hl_pullback_location_semantics_audit_2026-08-29_CN.md)：固定自由文本位置、support/role-reversal、事件位置与 canonical 方向/EMA gate 的阅读边界。
- [`H/L META 字段与授权边界审计`](../research/backtesting/hl_meta_boundary_audit_2026-08-29_CN.md)：核对 META 状态、组件、空间和授权边界，并固定 `pending` 不属于 `meta_confluence` 枚举。
- [`H/L 视觉前置证据与冻结资格审计`](../research/backtesting/hl_visual_preflight_contract_audit_2026-08-29_CN.md)：核对两年 Daily、重要高低点、EMA20/50/200 和决策日图像 provenance，不把字段冻结误当成完整视觉证据或验证通过。
- [`H/L lineage、市场状态与独立性分母审计`](../research/backtesting/hl_lineage_market_context_independence_audit_2026-08-29_CN.md)：区分共享 lineage、不同 lineage、缺失 `market_context_id` 与逐行描述性结果，不把它们误读为独立胜率证据。
- [`H/L 报告空间、版本与结论表述一致性审计`](../research/backtesting/hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md)：核对 H/L selection/replay 的历史几何、显式空间状态、自定义敏感性阈值、engine 版本和结论边界；不新增样本或结果。
- [`H/L 订单分支、缺口政策与结果状态边界审计`](../research/backtesting/hl_order_gap_contract_audit_2026-08-29_CN.md)：区分预冻结的 `gap_policy`、实际开盘路径、`no-fill`、`opening-skip`、`unproven` 与严格胜率分母；不新增样本或结果。
- [`H/L selection/replay 状态计数一致性审计`](../research/backtesting/hl_report_state_count_consistency_audit_2026-08-29_CN.md)：核对每批合同数、成交/未成交/观望状态、完成结果和 artifact 选择，不把 `eligible`/`filled` 读成交易授权或验证统计。

Codex Trading 的链接或历史材料只作为用户指定的只读参考；本目录不导入其规则、代码、实现状态或执行能力。

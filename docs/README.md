# PA Research Docs 索引

- [PA Research authority 与隔离边界审计](../research/authority_boundary_index_audit_2026-08-29_CN.md)

- [`PA Research 日线选股规则 v0.1`](pa_research_daily_selection_rules_v0_1_CN.md)
- [`PA Research 统一输出合同 v0.1`](pa_research_output_schema_v0_1_CN.md)
- [`PA 图表视觉复核卡`](visual_pa_review_card_CN.md)
- [`形态边界视觉决策卡`](morphology_boundary_decision_card_CN.md)：按 BOP 状态迁移、区间/第三推、B 腿和 lineage 固定顺序分流 H1/H2/L1/L2、三推与 ABC；
- [`每日候选批次与图表审查卡`](daily_candidate_review_card_CN.md)
- [`视觉识别校准协议 v0.1`](visual_calibration_protocol_v0_1_CN.md)：分开确定性发现 cohort、类别配平 morphology cohort、专家裁决和交易结果分母。
- [`共同上下文`](common_context.md)

统一边界：`v0.x` 规则/合同与回放引擎 `0.3.15` 均只属于 PA Research 研究层（`PA Research only`），不是 Codex Trading 生产规则；`no-new-positive` 和 `validated win-rate: not-computable` 保持不变，`60%` 仅是待检验目标；不创建量化扫描器，不连接 Execution Agent。

- [`共同视觉前置字段一致性审计`](../research/common_visual_preflight_field_consistency_audit_2026-08-29_CN.md)
- [`入场几何与不交易状态边界审计`](../research/entry_geometry_state_boundary_audit_2026-08-29_CN.md)
- [`候选、视觉复核与交易日志边界一致性审计`](../research/candidate_visual_record_consistency_audit_2026-08-29_CN.md)
- [`历史案例入口合同盘点审计`](../research/backtesting/historical_case_entry_inventory_contract_audit_2026-08-29_CN.md)（逐案区分历史叙述、canonical 字段、事前空间与事后路径）
- [`顶层 research 历史正向条件入口边界审计`](../research/backtesting/top_level_research_entry_boundary_audit_2026-08-30_CN.md)（隔离条件性研究状态、历史 scope 与结果字段）
- [`PA Research canonical 入口交叉覆盖审计`](../research/backtesting/canonical_entry_cross_coverage_audit_2026-08-30_CN.md)（核对报告、资产、模板、requiredFiles 与 inventory 的入口守卫）
- [`schema / engine / validator 漂移审计`](../research/backtesting/schema_engine_validator_drift_audit_2026-08-30_CN.md)（核对字段、枚举、版本和研究记录到回放输入的显式边界）
- [`Pattern 主标签映射与 BOP 状态迁移审计`](../research/pattern_label_transition_audit_2026-08-29_CN.md)
- [`三推/H3-L3 与区间边缘合同边界审计`](../research/backtesting/three_push_h3_l3_contract_boundary_audit_2026-08-29_CN.md)
- [`三推策略与历史案例合同一致性审计`](../research/backtesting/three_push_strategy_case_contract_audit_2026-08-29_CN.md)
- [`H3/L3 历史候选筛选日志证据与统计边界审计`](../research/backtesting/h3_l3_candidate_screen_provenance_audit_2026-08-29_CN.md)
- [`历史视觉证据与 canonical 边界审计`](../research/backtesting/visual_evidence_canonical_boundary_audit_2026-08-29_CN.md)
- [`视觉识别冒烟、快筛协议与 Round2/Round3 资产 canonical 边界审计`](../research/backtesting/visual_recognition_canonical_boundary_audit_2026-08-29_CN.md)
- [`Round4、Round5 与 TSLA 视觉资产 canonical 边界审计`](../research/backtesting/visual_asset_canonical_boundary_audit_2026-08-29_CN.md)
- [`全部视觉资产 README canonical provenance 覆盖审计`](../research/backtesting/visual_asset_provenance_coverage_audit_2026-08-29_CN.md)（聚合资产不冻结 `primary_pattern`/`lineage_id`）
- [`视觉历史报告与 canonical authority schema 对齐审计`](../research/backtesting/visual_authority_schema_alignment_audit_2026-08-29_CN.md)（六个活动视觉框架及 canonical label 映射）
- [`remaining visual frameworks 合同边界审计`](../research/backtesting/remaining_visual_framework_contract_audit_2026-08-29_CN.md)（补齐其余视觉框架、订单分支和 pattern-specific 字段边界）
- [`Pattern 案例矩阵、策略入口与历史别名合同审计`](../research/backtesting/pattern_case_matrix_strategy_entry_contract_audit_2026-08-29_CN.md)（区分聚合展示、逐案合同、事前空间与事后路径）
- [`Pattern README 与基础视觉框架 canonical 输出覆盖审计`](../research/backtesting/pattern_foundation_canonical_contract_audit_2026-08-29_CN.md)（含活动视觉复核卡）
- [`requiredFiles 与研究报告索引覆盖审计`](../research/backtesting/required_report_index_coverage_audit_2026-08-29_CN.md)
- [`统计结论、正例表述与授权边界一致性审计`](../research/backtesting/conclusion_boundary_consistency_audit_2026-08-29_CN.md)
- [`视觉识别能力与图表 provenance 边界审计`](../research/backtesting/visual_capability_boundary_audit_2026-08-29_CN.md)
- [`证据范围与数据状态一致性审计`](../research/evidence_scope_status_boundary_audit_2026-08-29_CN.md)
- [`选择记录与回放结果证据边界审计`](../research/backtesting/pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md)
- [`历史回放结果、交易日志与分母 provenance 审计`](../research/backtesting/historical_replay_result_log_provenance_audit_2026-08-29_CN.md)：区分冻结合同、模拟回放结果、运行 metadata 与实际交易日志；当前没有真实成交日志，结论仍为 `no-new-positive` / `validated win-rate: not-computable`。
- [`事件、空间与独立性字段引用一致性审计`](../research/backtesting/event_space_lineage_consistency_audit_2026-08-29_CN.md)
- [`H/L event bucket 标签一致性审计`](../research/backtesting/event_bucket_label_consistency_audit_2026-08-29_CN.md)
- [`H/L special subtype 与事件轴一致性审计`](../research/backtesting/special_subtype_event_axis_consistency_audit_2026-08-29_CN.md)
- [`H/L A/B 质量、位置与 EMA 字段一致性审计`](../research/backtesting/hl_leg_quality_location_axis_consistency_audit_2026-08-29_CN.md)
- [`H/L EMA 闸门、回调位置与报告分母一致性审计`](../research/backtesting/hl_ema_gate_report_consistency_audit_2026-08-29_CN.md)
- [`H/L 回调位置文本语义与方向边界审计`](../research/backtesting/hl_pullback_location_semantics_audit_2026-08-29_CN.md)
- [`H/L META 字段与授权边界审计`](../research/backtesting/hl_meta_boundary_audit_2026-08-29_CN.md)
- [`H/L 视觉前置证据与冻结资格审计`](../research/backtesting/hl_visual_preflight_contract_audit_2026-08-29_CN.md)
- [`H/L lineage、市场状态与独立性分母审计`](../research/backtesting/hl_lineage_market_context_independence_audit_2026-08-29_CN.md)
- [`H/L 报告空间、版本与结论表述一致性审计`](../research/backtesting/hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md)
- [`H/L 订单分支、缺口政策与结果状态边界审计`](../research/backtesting/hl_order_gap_contract_audit_2026-08-29_CN.md)
- [`H/L selection/replay 状态计数一致性审计`](../research/backtesting/hl_report_state_count_consistency_audit_2026-08-29_CN.md)
- [`PA Research → Codex Trading 研究交接规范`](research_to_system_handoff_CN.md)
- [`冻结合同回放器（backtesting.py）`](../research/backtesting/README.md)

这些文件只定义 PA Research 的研究、记录和边界合同；回放器仍是人工合同的离线研究工具，不包含量化扫描器、生产交易规则或 Execution Agent 连接。

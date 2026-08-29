# PA Research 研究索引

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only`

本目录保存 PA Research 的专项审计、历史案例、视觉验收记录和图像资产入口。它不是行情数据库、量化扫描器或执行层。新记录先使用[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)，方向必须明确写为 `long`、`short` 或 `no_valid_direction`。

统一边界：`v0.x` 规则/合同与回放引擎 `0.3.9` 均只属于 PA Research 研究层（`PA Research only`），不是 Codex Trading 生产规则；`no-new-positive` 和 `validated win-rate: not-computable` 保持不变，`60%` 仅是待检验目标；不创建量化扫描器，不连接 Execution Agent。

## 当前 authority 与工作流

- [`ABC 研究状态与工作边界`](abc_research_status_v0_3_CN.md)：ABC 的快筛/深审边界；
- [`ABC + H/L 分层历史结果审计`](abc_hl_stratified_outcome_audit_2026-08-24_CN.md)：当前结果口径、样本分层和 `no-new-positive`；
- [`BOP 真实多日回踩候选审计`](bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)：普通 BOP、同日回测、事件/缺口分支和多日正例缺口；
- [`核心八个 Pattern 交叉一致性审计`](core_pattern_cross_audit_CN.md)：主标签、状态转换和历史状态别名；
- [`PA Pattern 视觉筛选协议`](visual_pattern_triage_protocol_CN.md)：快筛与深审的执行顺序；
- [`每日候选批次与图表审查卡`](../docs/daily_candidate_review_card_CN.md)：候选池覆盖、数据来源、两年 Daily 左侧、事件、流动性和空间证据的统一记录；
- [`流程改进审计（2026-08-28）`](process_improvement_audit_2026-08-28_CN.md)：记录本轮独立修复、验证证据和仍需用户决定的研究设计事项；
- [`候选、视觉复核与交易日志边界一致性审计（2026-08-29）`](candidate_visual_record_consistency_audit_2026-08-29_CN.md)：核对选择记录的方向汇总、冻结前/回放后状态、两年 Daily/EMA/A-B/空间字段、ROST 视觉 provenance 和历史三推笔记；不新增样本或结果；
- [`统一输出、视觉字段与状态轴审计（2026-08-29）`](unified_output_state_axis_audit_2026-08-29_CN.md)：区分文档成熟度与案例状态，补齐历史摘要的 `gate_result`，统一 BOP/H3-L3 的方向、lineage、事件、空间和多周期字段；不新增样本或结果；
- [`Pattern 索引、别名与主次标签边界审计（2026-08-29）`](pattern_index_alias_boundary_audit_2026-08-29_CN.md)：逐项核对 16 个目录、核心/独立层级、canonical `primary_pattern`/`internal_label`/`state_transition` 与本地入口；不新增样本或结果；
- [`Pattern 视觉复核前置证据审计（2026-08-29）`](pattern_visual_preflight_audit_2026-08-29_CN.md)：核对 16 个目录是否先看两年 Daily 左侧、重要高低点、EMA20/50/200、适用路径的 A/B 质量（强 A→H1/L1 优先；区间边缘三推不要求强 A）、位置和首障碍；不新增样本或结果；
- [`Pattern 案例入口与状态一致性审计（2026-08-29）`](pattern_case_entry_status_audit_2026-08-29_CN.md)：核对 16 个目录的案例链接、条件/边界/no-trade 文案和 `valid_no_trade`/`no-new-positive` 状态；不新增样本或结果；
- [`共同视觉前置字段一致性审计（2026-08-29）`](common_visual_preflight_field_consistency_audit_2026-08-29_CN.md)：统一两年 Daily 左侧、重要高低点、EMA、A/B 质量、位置/空间、方向和 `data_status` 的 canonical 字段；不新增样本或结果；
- [`Pattern 状态轴、字段与枚举一致性审计（2026-08-29）`](pattern_state_axis_field_enum_audit_2026-08-29_CN.md)：核对 16 个目录、统一输出合同和视觉复核卡的字段命名、状态轴与 pattern-specific 边界；不新增样本或结果；
- [`Pattern README 与基础视觉框架 canonical 输出覆盖审计（2026-08-29）`](backtesting/pattern_foundation_canonical_contract_audit_2026-08-29_CN.md)：核对 16 个 pattern README、8 个基础层、局部模板的 canonical 字段/枚举与索引入口；不新增样本或结果；
- [`requiredFiles 与研究报告索引覆盖审计（2026-08-29）`](backtesting/required_report_index_coverage_audit_2026-08-29_CN.md)：核对 validator requiredFiles 中研究报告与 canonical 索引的映射，确认没有孤立报告；不新增样本或结果；
- [`统计结论、正例表述与授权边界一致性审计（2026-08-29）`](backtesting/conclusion_boundary_consistency_audit_2026-08-29_CN.md)：统一 `validated win-rate: not-computable`、`no-new-positive`、60% 待检验目标与研究/交接边界，清理旧状态别名；不新增样本或结果；
- [`视觉识别能力与图表 provenance 边界审计（2026-08-29）`](backtesting/visual_capability_boundary_audit_2026-08-29_CN.md)：把人工大体识别、两年 Daily/重要高低点/EMA 前置证据与准确率、自动扫描、交易授权分开；不新增样本或结果；
- [`入场几何与不交易状态边界审计（2026-08-29）`](entry_geometry_state_boundary_audit_2026-08-29_CN.md)：统一首障碍、结构止损、入场前空间、粗略 R/R 与 pattern-specific 短字段映射，并区分 `observation_only` 与 `valid_no_trade`；不新增样本或结果；
- [`Pattern 主标签映射与 BOP 状态迁移审计（2026-08-29）`](pattern_label_transition_audit_2026-08-29_CN.md)：核对 16 个 pattern 入口、日线 `ABC_CONT`/`BOP` 白名单、H/L 内部标签、三推/区间边缘分隔、BOP 接受后的旧合同失效和视觉冒烟字段；不新增样本或结果；
- [`三推/H3-L3 与区间边缘合同边界审计（2026-08-29）`](backtesting/three_push_h3_l3_contract_boundary_audit_2026-08-29_CN.md)：统一 `third_push_state`、`range_edge_side`、多空研究方向、订单/状态分轴，并确认当前没有冻结 H3/L3 统计分母；不新增样本或结果；
- [`三推策略与历史案例合同一致性审计（2026-08-29）`](backtesting/three_push_strategy_case_contract_audit_2026-08-29_CN.md)：统一 A/B/C 解释层、三推案例状态、订单/首障碍/空间字段与统计结论；不新增样本或结果；
- [`H3/L3 历史候选筛选日志证据与统计边界审计（2026-08-29）`](backtesting/h3_l3_candidate_screen_provenance_audit_2026-08-29_CN.md)：核对两份历史候选日志的数据状态、事件来源、canonical 字段和 no-new-positive 边界；不新增样本或结果；
- [`证据范围与数据状态一致性审计（2026-08-29）`](evidence_scope_status_boundary_audit_2026-08-29_CN.md)：统一 `contract_scope`、`data_status`、`chart_scope`、逐标的两年 Daily 覆盖和 `timeframes_seen`，修复历史状态/周期字段漂移；不新增样本或结果；
- [`人工冻结合同覆盖审计（2026-08-28）`](backtesting/contract_coverage_audit_2026-08-28_CN.md)：统计现有 H/L 合同的方向、标签、事件、空间和 lineage 覆盖，不把它解释为胜率；
- [`冻结合同字段覆盖与分层完整性审计（2026-08-29）`](backtesting/frozen_contract_field_partition_audit_2026-08-29_CN.md)：逐文件核对方向、Pattern/内部标签、EMA gate、事件、空间、合同状态和 lineage；旧合同缺失字段不回填，继续隔离 ABC/BOP/H3/L3；
- [`事前证据与结果证据隔离审计（2026-08-29）`](backtesting/pre_entry_result_evidence_isolation_audit_2026-08-29_CN.md)：确认事件、空间和 EMA 资格只能来自入场前合同，回放结果不得反向改写派生分层或胜率分母；记录 mismatch 防护与 `no-new-positive`；
- [`选择记录与回放结果证据边界审计（2026-08-29）`](backtesting/pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md)：逐文件核对选择报告、候选卡、视觉记录、冻结合同和 replay/result 记录的 pre-entry/post-outcome 分界；修复 `hl_next3` 选择报告中混入的空结果汇总，不新增样本或结果；
- [`旧结果事前 provenance 完整性审计（2026-08-29）`](backtesting/legacy_result_provenance_completeness_audit_2026-08-29_CN.md)：为缺少合同、事件或 H/L EMA gate 的旧/最小结果建立 `pre_entry_provenance_status`，缺证据行只保留描述性记录，不进入完成交易分母；
- [`回放 artifact schema round-trip 审计（2026-08-29）`](backtesting/artifact_schema_roundtrip_audit_2026-08-29_CN.md)：核对 `results.csv → summary.json → run_metadata.json` 的 provenance/mismatch 链路和旧 metadata 的历史状态；当前运行必须保留 `summary_provenance`，不把旧 artifact 或重复回放当成新样本；
- [`回放 artifact 全仓库 inventory 审计（2026-08-29）`](backtesting/artifact_inventory_audit_2026-08-29_CN.md)：确认当前 checkout 没有持久化回放三件套，区分合同/价格输入与结果 artifact，避免缺文件或旧 metadata 进入统计分母；
- [`回放范围隔离与依赖边界审计（2026-08-29）`](backtesting/scope_boundary_dependency_audit_2026-08-29_CN.md)：核对 executable code、依赖和配置没有接入 Futu/OpenD、Codex Trading、量化扫描器或 Execution Agent；边界守卫测试固定研究依赖；
- [`回放输入边界与 provenance bug 审计（2026-08-29）`](backtesting/input_boundary_bug_audit_2026-08-29_CN.md)：修复非有限合同/行情数值、无效回放成本参数、空 CSV 和源码 hash 双文件篡改边界，并补回归测试；不改变有效合同语义；
- [`回放 artifact 状态与 CLI 返回码审计（2026-08-29）`](backtesting/artifact_validator_state_exit_audit_2026-08-29_CN.md)：用最小损坏/历史/当前 fixture 固化 `current_valid`、`historical_incomplete`、`invalid` 及 `0/2/1` 返回码边界；不把 artifact 完整性误读成胜率验证；
- [`回放结果分母边界 bug 审计（2026-08-29）`](backtesting/result_denominator_boundary_bug_audit_2026-08-29_CN.md)：修复缺失 `path_result` 仍可能进入完成交易分母的问题，并把该结果列纳入当前 artifact schema；不增加样本或改变有效回放语义；
- [`回放执行语义审计（2026-08-29）`](backtesting/execution_semantics_audit_2026-08-29_CN.md)：用合成 K 线核对多空、订单分支、三种 gap policy、保护性退出和 horizon；补充对称回归覆盖，不改变有效回放语义；
- [`PA Research authority 与隔离边界审计（2026-08-29）`](authority_boundary_index_audit_2026-08-29_CN.md)：确认当前 authority、历史来源和禁止接入声明没有被 Codex Trading 或外部生产版本标记混入，并增加版本文案防回归检查；
- [`合同权威与字段一致性审计（2026-08-29）`](backtesting/contract_authority_consistency_audit_2026-08-29_CN.md)：区分研究记录超集与当前回放输入子集，收窄日线候选主标签，明确方向、订单、数值价格和成交状态边界；不增加样本或改变有效回放语义；
- [`合同 CSV inventory 与资格边界审计（2026-08-29）`](backtesting/contract_csv_inventory_audit_2026-08-29_CN.md)：只读盘点冻结合同、示例合同、intake 和价格快照，固化 loader、入场几何、标签组合及 `contract_frozen` 隔离；不改写历史 CSV 或增加样本；
- [`文档 validator 与 engine 合同 parity 审计（2026-08-29）`](backtesting/validator_engine_contract_parity_audit_2026-08-29_CN.md)：补齐 validator 与 engine 的必需列、订单/gap、有限数值、入场几何、META 和研究字段校验，并用合成负例验证拒绝边界；不改变 engine 语义或增加样本；
- [`报告、索引与 inventory 一致性审计（2026-08-29）`](backtesting/report_index_inventory_consistency_audit_2026-08-29_CN.md)：交叉核对当前 CSV、冻结合同、intake、replay 报告、engine/dependency 版本和历史 artifact 边界，并增加动态防回归检查；不改写历史结果；
- [`批次报告数字与分层一致性审计（2026-08-29）`](backtesting/batch_report_numeric_consistency_audit_2026-08-29_CN.md)：重算各 H/L 批次的方向、内部标签、EMA gate、事件/空间 bucket、几何空间和 lineage，并核对回放结论；明确 25 条 intake 总量和旧合同空间字段边界；不新增样本；
- [`ABC/BOP intake schema 一致性审计（2026-08-29）`](backtesting/abc_bop_intake_schema_consistency_audit_2026-08-29_CN.md)：逐行核对两种 intake schema、字段完整性、source_case、方向/Pattern、跨 schema alias 和冻结边界；修复已证实的 CSV 行宽、方向和 ID 冲突，不新增样本；
- [`视觉资产与事前证据边界审计（2026-08-29）`](backtesting/visual_asset_pre_entry_evidence_audit_2026-08-29_CN.md)：核对 11 个视觉资产目录、105 张 PNG、冻结合同截止图、两年 Daily/EMA/重要高低点字段、结果隔离和外部 artifact 边界；不新增样本，不把人工抽查升级为胜率证据；
- [`外部视觉 artifact provenance 审计（2026-08-29）`](backtesting/external_visual_artifact_provenance_audit_2026-08-29_CN.md)：固定 `hl_next4/hl_next5` 的外部 PNG 数量、哈希和合同映射，明确 ROST 2026-01-07 缺少决策日图、后一天图不能替代；不复制外部缓存或改写历史结果；
- [`回放版本与结论表述一致性审计（2026-08-29）`](backtesting/version_conclusion_consistency_audit_2026-08-29_CN.md)：统一当前 engine `0.3.9`、历史版本与 `no-new-positive`/`validated win-rate: not-computable` 的语境，保留历史点估计但不升级为验证统计；
- [`H/L 报告空间、版本与结论表述一致性审计（2026-08-29）`](backtesting/hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md)：区分旧合同历史几何与当前显式 `space_status`，将 1.40R/1.50R 标为敏感性分层，并统一 H/L 报告的版本、60% 目标和 `no-new-positive` 边界；不新增样本或结果；
- [`ABC/BOP 合同准入审计（2026-08-28）`](backtesting/abc_bop_contract_intake_audit_2026-08-28_CN.md)：把现有 ABC/BOP 视觉案例分成条件准入和边界案例；intake 清单不进入回放分母；
- [`ABC 候选合同冻结复核（2026-08-28）`](backtesting/abc_bop_candidate_freeze_review_2026-08-28_CN.md)：逐字段复核 NFLX/TSM 是否具备冻结条件；两者仍未冻结，不增加回放分母；
- [`多头 ABC/H1/H2 候选合同审计（2026-08-28）`](backtesting/abc_bullish_candidate_contract_audit_2026-08-28_CN.md)：逐字段复核 V、NVDA、KLAC、CRWD；当前没有可冻结的新多头合同，不增加回放分母；
- [`跨 Pattern 统计隔离审计（2026-08-29）`](backtesting/cross_pattern_statistics_isolation_audit_2026-08-29_CN.md)：检查 ABC/BOP、H/L、三推的标签、订单分支和 lineage 依赖；当前没有冻结 ABC/BOP 或 H3/L3 合同，保持 `no-new-positive`；
- [`事件与首障碍空间资格审计（2026-08-29）`](backtesting/event_space_eligibility_audit_2026-08-29_CN.md)：隔离事件未核实、财报邻近、空间边界和旧合同未知空间，避免把它们读成普通非事件证据；
- [`事件、空间与独立性字段引用一致性审计（2026-08-29）`](backtesting/event_space_lineage_consistency_audit_2026-08-29_CN.md)：核对 `event_context/event_bucket`、`space_status/pre_entry_space_R`、`lineage_id/market_context_id` 的来源、派生和跨文件表述；修正 `hl_next` 历史几何不等于显式 strict-space 的文案，不新增样本或结果；
- [`H/L event bucket 标签一致性审计（2026-08-29）`](backtesting/event_bucket_label_consistency_audit_2026-08-29_CN.md)：重算 60 条合同的 raw `event_context` 与 canonical `event_bucket`，统一 selection/replay 分层标签，确认 pending/unknown 未升级为普通非事件；不新增样本或结果；
- [`H/L special subtype 与事件轴一致性审计（2026-08-29）`](backtesting/special_subtype_event_axis_consistency_audit_2026-08-29_CN.md)：区分上游 `special_subtype` 注释与 H/L 回放最小合同，确认 subtype 缺失不等于普通非事件，且不能替代 `event_context/event_bucket`；不新增样本或结果；
- [`H/L A/B 质量、位置与 EMA 字段一致性审计（2026-08-29）`](backtesting/hl_leg_quality_location_axis_consistency_audit_2026-08-29_CN.md)：核对 A/B 质量、B 位置与 H/L EMA/回调位置字段的覆盖、历史别名和回放边界；不回填缺失字段、不新增样本或结果；
- [`H/L EMA 闸门、回调位置与报告分母一致性审计（2026-08-29）`](backtesting/hl_ema_gate_report_consistency_audit_2026-08-29_CN.md)：核对 7 批 H/L 合同的 EMA 方向、位置字段、eligible/observation/pending 与报告分母；修复 validator 对反向 pass gate 和未知斜率 fail 的遗漏，不新增样本或结果；
- [`H/L 回调位置文本语义与方向边界审计（2026-08-29）`](backtesting/hl_pullback_location_semantics_audit_2026-08-29_CN.md)：核对 60 条位置文本与多空/EMA gate 的方向语义，固定 support/role-reversal、事件位置和历史 B 词不能替代 canonical 字段的边界；不新增样本或结果；
- [`H/L META 字段与授权边界审计（2026-08-29）`](backtesting/hl_meta_boundary_audit_2026-08-29_CN.md)：核对 60 条合同的 `present/absent/unknown/pending` 分层、组件数量、EMA gate 和空间独立性；修正 META 文档的空间边界，不新增样本或结果；
- [`H/L 视觉前置证据与冻结资格审计（2026-08-29）`](backtesting/hl_visual_preflight_contract_audit_2026-08-29_CN.md)：核对 60 条冻结合同的两年背景、重要高低点、EMA20/50/200、图像资产和 ROST 决策日 provenance gap；不新增样本或结果；
- [`H/L lineage、市场状态与独立性分母审计（2026-08-29）`](backtesting/hl_lineage_market_context_independence_audit_2026-08-29_CN.md)：核对 7 份 H/L 合同的 53 个 lineage、7 个共享组、`market_context_id=0/60` 和报告措辞，避免把不同 lineage 或缺失市场状态写成独立胜率证据；不新增样本或结果；
- [`H/L 订单分支、缺口政策与结果状态边界审计（2026-08-29）`](backtesting/hl_order_gap_contract_audit_2026-08-29_CN.md)：核对 7 份 H/L 合同的 `order_branch`、`gap_policy`、触发/止损/首障碍/目标和 `no-fill`、`opening-skip`、accepted-open 状态，固定成交与胜率分母边界；不新增样本或结果；
- [`H/L selection/replay 状态计数一致性审计（2026-08-29）`](backtesting/hl_report_state_count_consistency_audit_2026-08-29_CN.md)：逐批核对 60 条冻结合同的 `eligible`、`filled`、`opening-skip`、`no-fill`、`observation_only`、完成交易与 win/loss 计数，区分历史回放层资格、当前空间资格和严格胜率分母；不新增样本或结果；
- [`回放结果分母与 horizon 审计（2026-08-29）`](backtesting/replay_outcome_denominator_audit_2026-08-29_CN.md)：检查胜率旗标、完成 horizon、opening-skip、intrabar 歧义、首障碍过程字段和 `realized_R` 的结果隔离；旧产物的 time-exit 偏差不增加验证分母；
- [`回放 lineage 与样本独立性审计（2026-08-29）`](backtesting/replay_lineage_independence_audit_2026-08-29_CN.md)：检查共享父级/局部结构、重复 artifact、共享市场状态和持仓区间重叠；重复结果不进入分母，当前独立性证据仍不足；
- [`回放 provenance 与再现性审计（2026-08-29）`](backtesting/replay_provenance_reproducibility_audit_2026-08-29_CN.md)：核对历史报告与 artifact 数值、输入/结果指纹和旧运行冲突；当前仍不能把历史描述升级为验证胜率；
- [`历史回放结果、交易日志与分母 provenance 审计（2026-08-29）`](backtesting/historical_replay_result_log_provenance_audit_2026-08-29_CN.md)：确认 13 组外部历史结果全部是 `historical_incomplete`，区分模拟 `results.csv`、冻结合同、运行 metadata 与实际交易日志，固定重复样本和当前胜率分母边界；不新增样本；
- [`BOP 合同准入审计（2026-08-28）`](backtesting/bop_contract_intake_audit_2026-08-28_CN.md)：逐案隔离接受、同日回测、缺口重订和相邻 H/L/ABC 案例；当前没有日线级多日 BOP 正向候选；
- [`PA 图表视觉识别冒烟验收`](visual_recognition_smoke_test_2026-08-24_CN.md)：图表识别能力、两年背景和当前 acceptance-pending 状态。
- [`三推/H3-L3 视觉证据缺口审计`](three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md)：区分衰竭、扩张/高潮、区间重复和通道延续，并保留 KLAC 条件候选与 L3 `no-new-positive` 边界。
- [`Round5 两年 Daily 左侧背景视觉练习`](visual_recognition_round5_two_year_daily_2026-08-24_CN.md)：4 个标的、8 个历史截断案例的两年背景、重要高低点、EMA 和 H/L/三推边界。
- [`历史视觉证据与 canonical 边界审计`](backtesting/visual_evidence_canonical_boundary_audit_2026-08-29_CN.md)：统一三推/H-L 历史显示标签、两年背景证据头、方向、订单/空间和统计隔离。
- [`视觉识别冒烟、快筛协议与 Round2/Round3 资产 canonical 边界审计`](backtesting/visual_recognition_canonical_boundary_audit_2026-08-29_CN.md)：核对冒烟/快筛字段映射、两年 Daily/重要高低点/EMA provenance、Round2/Round3 局部资产和 `no-new-positive` 边界；不新增样本或结果。
- [`Round4、Round5 与 TSLA 视觉资产 canonical 边界审计`](backtesting/visual_asset_canonical_boundary_audit_2026-08-29_CN.md)：补齐短窗口 Round4、两年 Daily Round5 与 TSLA 多周期资产的 canonical provenance、重要高低点/EMA、多周期职责和状态边界；不新增样本或结果。
- [`全部视觉资产 README canonical provenance 覆盖审计`](backtesting/visual_asset_provenance_coverage_audit_2026-08-29_CN.md)：覆盖 11 个视觉资产目录、105 张 PNG 的 README provenance、配对职责、历史别名和索引边界；不新增样本或结果。
- [`视觉历史报告与 canonical authority schema 对齐审计`](backtesting/visual_authority_schema_alignment_audit_2026-08-29_CN.md)：核对视觉框架、历史报告、配对复核记录与 canonical 字段/状态轴，区分当前模板修复和历史事实别名；不新增样本或结果。

## 冻结合同回放

- [`PA Research 冻结合同回放器`](backtesting/README.md)：使用固定版本 `backtesting.py` 回放人工冻结的入场、止损、目标和时间合同；不自动识别 pattern，不创建扫描器，不连接 Execution Agent。
- [`H/L 首批真实样本准入审计`](backtesting/first_hl_sample_intake_2026-08-26_CN.md)：前一阶段的两年 Daily 案例、EMA20/50 闸门、META、首障碍和合同冻结检查；该文件记录的当时状态为 `strict_h_l_contracts_frozen: 0`，现由下方首批合同回放审计承接。
- [`H/L 首批合同回放审计`](backtesting/hl_contract_batch_replay_2026-08-26_CN.md)：第一批人工冻结的 H1/H2/L1/L2 合同、两年 Daily 图和分层回放；共享 lineage、空间闸门和失败 EMA 闸门均单独保留，结论仍为 `no-new-positive`。
- [`H/L 第二批合同回放审计`](backtesting/hl_contract_batch2_replay_2026-08-26_CN.md)：第二批三个独立 lineage 的 H2/L1 合同、两年 Daily 图、EMA 闸门、空间边界和分层回放；结论继续单独维护 `no-new-positive`。
- [`H/L 第二批人工看图合同资产`](assets/visual_recognition/2026-08-26/hl_contract_batch2/README.md)：KLAC、TSM、ADBE 三张两年 Daily 图及公共历史数据来源边界。
- [`H/L 首批人工看图合同资产`](assets/visual_recognition/2026-08-26/hl_contract_batch/README.md)：本批五张两年 Daily 图及来源、时区和历史数据边界。
- [`H/L 大样本人工合同冻结记录`](backtesting/hl_large_selection_2026-08-27_CN.md)：COHR、RBLX、MAR 三标的、37 条人工冻结 H1/H2/L1/L2 合同和用户修正后的 60% 待检验目标。
- [`H/L 大样本回测人工看图资产`](assets/visual_recognition/2026-08-27/hl_large_backtest/README.md)：23 张 Matplotlib 两年 Daily 背景/局部序列图；无 pattern 标签和结果标记。
- [`H/L 大样本回放审计`](backtesting/hl_large_replay_2026-08-27_CN.md)：37 条冻结合同的描述性回放、60% 目标检验、严格 `>=1R` 空间子集和 `no-new-positive` 结论；旧产物的 time-exit 索引口径见 2026-08-29 分母审计。
- [`H/L 下一批人工合同冻结记录`](backtesting/hl_next_selection_2026-08-27_CN.md)：ZS、DDOG 两个中等至大型市值标的的 5 条 H1/L1 人工冻结合同；包含两年 Daily 背景、EMA20/50 闸门、重要高低点、事件隔离和首障碍空间。
- [`H/L 下一批分层回放审计`](backtesting/hl_next_replay_2026-08-27_CN.md)：3 条普通非事件与 2 条事件驱动合同的独立回放；2 条完成成交为 1 胜 1 负，60% 目标仍未验证，结论保持 `no-new-positive`。
- [`H/L 下一批（二）人工合同冻结记录`](backtesting/hl_next2_selection_2026-08-27_CN.md)：TOL、VEEV 两条普通非事件 H1 合同、两年 Daily 视觉背景、EMA20/50 闸门、事件隔离、首障碍空间和 H2/L2 边界排除记录。
- [`H/L 下一批（二）分层回放审计`](backtesting/hl_next2_replay_2026-08-27_CN.md)：2 条 H1 合同均成交并到达第一障碍，描述性 2 胜 0 负；只有两个 lineage，Wilson 下界约 34.24%，60% 目标仍未验证，结论保持 `no-new-positive`。
- [`H/L 下一批（二）人工看图回放资产`](assets/visual_recognition/2026-08-27/hl_next2_backtest/README.md)：TOL、VEEV 的冻结前两年 Daily 图，以及 PHM H2-like/EMA 闸门拒绝边界图；Matplotlib 只负责渲染。
- [`H/L 下一批（三）人工候选边界审计`](backtesting/hl_next3_selection_2026-08-27_CN.md)：18 个候选的两年 Daily、重要高低点、支撑阻力、EMA20/50/200、事件、lineage、B 质量和空间复核；新合格交易合同为 0。
- [`H/L 下一批（三）回放状态审计`](backtesting/hl_next3_replay_2026-08-27_CN.md)：无合格合同，不创建占位回放分母；胜率不可计算，60% 继续待检验，结论保持 `no-new-positive`。
- [`H/L 下一批（四）人工合同冻结记录`](backtesting/hl_next4_selection_2026-08-27_CN.md)：24 个新市值约 `$3B–$100B` 美国普通股的两年 Daily 人工复核；仅 CBOE、ROST 的 2 条 `long / H1` 通过全部 strong-A、controlled-B、EMA、事件、lineage 和 `>=1R` 闸门。
- [`H/L 下一批（四）分层回放审计`](backtesting/hl_next4_replay_2026-08-27_CN.md)：2 条合同均成交但均未到达第一障碍，0 胜 2 负、`-1.5090R`；95% Wilson 区间约 `0.00%–65.76%`，60% 目标未验证，结论保持 `no-new-positive`；time-exit 的完整观察窗口与执行索引已在后续审计中明确。
- [`H/L 下一批（五）人工合同冻结记录`](backtesting/hl_next5_selection_2026-08-27_CN.md)：12 只新市值约 `$3B–$100B` 美国普通股的两年 Daily 人工复核；仅冻结 MCHP、NDAQ 的 6 条 `short / L1` 合同，没有合格的新 H2 或 L2 正例。
- [`H/L 下一批（五）分层回放审计`](backtesting/hl_next5_replay_2026-08-27_CN.md)：6 条人工合同中 5 条成交并完成，3 胜 2 负、合并描述性 `60.00%`、`+3.4812R`；普通、财报邻近和财报驱动分层不混算，60% 目标未验证，结论保持 `no-new-positive`；time-exit 的完整观察窗口与执行索引已在后续审计中明确。

## 优先研究矩阵与专项框架

- [`ABC 决策矩阵`](abc_decision_matrix_CN.md)；
- [`优先 Pattern 代表性视觉候选矩阵`](priority_pattern_visual_candidate_matrix_2026-08-24_CN.md)；
- [`事件/板块/大盘视觉证据审计`](event_sector_market_gate_visual_evidence_audit_2026-08-24_CN.md)；
- [`订单类型与风险合同视觉证据审计`](order_risk_contract_visual_evidence_audit_2026-08-24_CN.md)；
- [`H/L lineage 与三推状态视觉边界复核`](h_l_lineage_visual_boundary_audit_2026-08-24_CN.md)；
- [`三推/H3-L3 压力状态框架`](three_push_pressure_state_framework_CN.md)：区间边缘三推、区间中部重复测试、趋势/通道延续和反向确认的分流；
- [`跨 Pattern 视觉优先级与冲突消解审计`](cross_pattern_visual_priority_audit_2026-08-24_CN.md)。

## 当前审计追踪的历史视觉候选入口

以下五个入口是[`候选、视觉复核与交易日志边界一致性审计（2026-08-29）`](candidate_visual_record_consistency_audit_2026-08-29_CN.md)明确追踪的历史视觉候选。它们的 `stage_1_fast_screen`/`historical_context_only` 范围、方向和缺失闸门均保留在原记录中，不代表 `daily_candidate`、冻结合同、交易授权或胜率样本：

- [`CRM 空头 ABC L1/L2 历史视觉候选`](crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md)；
- [`META 多头 ABC H1/H2 历史视觉候选`](meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md)；
- [`MSFT 空头 ABC L1/L2 历史视觉候选`](msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md)；
- [`NVDA 多头 ABC H1 历史视觉候选`](nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md)；
- [`2024–2025 视觉候选网格`](visual_screen_candidate_grid_2024_2025_CN.md)：批次级混合记录，`direction=no_valid_direction`，不代表逐标的候选。

## 已归档但仍可复核的独立案例入口

以下四个额外归档入口此前没有 Markdown 入链；它们都是历史研究材料，不代表生产规则或统计样本：

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

Round4 的 5 个直接 MTF PNG 之前没有索引入链，现统一列在其资产 README 中；它们仍因 Daily 左侧不足两年而保持 `daily_context_window: <2y`。

# PA Research Strategy 研究索引

文档状态：`document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

本目录只保存研究框架、候选清单和历史复盘入口，不是 Codex Trading 实现队列。所有新案例必须使用[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)，并明确 `direction`、`research_state`、`trade_state` 和 `handoff_status`。

## 入口

- [`候选形态清单`](pattern_inventory_candidates.md)：当前研究优先级、共同字段和边界案例；
- [`Trading Framework`](00_trading_framework.md)：背景到风险的研究顺序；
- [`三推楔形候选规则`](01_three_push_wedge_candidate.md)：三推压力/衰竭/延续的研究假设；
- [`META 多重优势区域`](meta_multiple_edge.md)：位置汇聚背景，不是独立触发器；
- [`概率原则学习参考`](probability_principles_pages_1_7.md)：外部启发式，只作学习材料，不进入胜率或回测基准；
- [`TSLA/META 历史复盘`](reviews/2026-06-25-tsla-meta-example.md)：历史案例，不是实盘授权。
- [`候选、视觉复核与交易日志边界一致性审计`](../research/candidate_visual_record_consistency_audit_2026-08-29_CN.md)：核对方向、候选状态、事前证据和事后路径的分轴边界。
- [`Pattern 索引、别名与主次标签边界审计`](../research/pattern_index_alias_boundary_audit_2026-08-29_CN.md)：核对 16 个 pattern 目录入口、核心/独立层级和 canonical 主次标签边界。
- [`Pattern 视觉复核前置证据审计`](../research/pattern_visual_preflight_audit_2026-08-29_CN.md)：核对完整图表左侧、EMA、强 A/受控 B、位置与首障碍的共同前置证据。
- [`Pattern 案例入口与状态一致性审计`](../research/pattern_case_entry_status_audit_2026-08-29_CN.md)：核对 16 个 pattern 的案例入口、条件/边界/no-trade 文案和状态别名。
- [`共同视觉前置字段一致性审计`](../research/common_visual_preflight_field_consistency_audit_2026-08-29_CN.md)：统一两年 Daily 左侧、重要高低点、EMA、A/B 质量、位置/空间和 `data_status` 的字段边界。
- [`Pattern 状态轴、字段与枚举一致性审计`](../research/pattern_state_axis_field_enum_audit_2026-08-29_CN.md)：核对统一状态轴、字段命名和 pattern-specific 模板边界。
- [`入场几何与不交易状态边界审计`](../research/entry_geometry_state_boundary_audit_2026-08-29_CN.md)：统一首障碍、结构止损、入场前空间、粗略 R/R 和不交易状态边界。
- [`Pattern 主标签映射与 BOP 状态迁移审计`](../research/pattern_label_transition_audit_2026-08-29_CN.md)：核对日线主标签白名单、H/L 内部标签、三推/区间边缘分隔及 BOP 接受后的旧合同失效。
- [`证据范围与数据状态一致性审计`](../research/evidence_scope_status_boundary_audit_2026-08-29_CN.md)：核对多周期证据范围、逐标的两年 Daily 覆盖、数据状态与历史 session 的字段边界。
- [`选择记录与回放结果证据边界审计`](../research/backtesting/pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md)：核对选择报告、候选卡、视觉记录和 replay/result 的事前/事后字段边界；不新增样本或结果。
- [`事件、空间与独立性字段引用一致性审计`](../research/backtesting/event_space_lineage_consistency_audit_2026-08-29_CN.md)：核对事件、空间、lineage 和市场状态字段的来源与跨文件表述；修正历史几何与显式空间资格的边界。
- [`H/L event bucket 标签一致性审计`](../research/backtesting/event_bucket_label_consistency_audit_2026-08-29_CN.md)：重算 raw `event_context` 与 canonical `event_bucket`，统一 selection/replay 的事件分层显示并保留 pending/unknown 隔离。
- [`H/L special subtype 与事件轴一致性审计`](../research/backtesting/special_subtype_event_axis_consistency_audit_2026-08-29_CN.md)：区分上游 `special_subtype` 与回放合同字段，固定其不能替代 `event_context/event_bucket` 的范围。
- [`H/L 报告空间、版本与结论表述一致性审计`](../research/backtesting/hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md)：核对 H/L selection/replay 的历史几何、显式空间状态、自定义敏感性阈值、engine 版本和结论边界；不新增样本或结果。

Codex Trading 的链接或历史材料只作为用户指定的只读参考；本目录不导入其规则、代码、实现状态或执行能力。

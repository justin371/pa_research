# PA Research Foundations 基础层索引

文档状态：document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative

范围：PA Research only。v0.x 规则/合同与回放引擎 0.3.9 都只属于研究层；基础层只提供共用的背景、位置、订单和风险语义，不是 Codex Trading 生产规则、量化扫描器、交易授权或 Execution Agent 输入；当前统计结论仍为 no-new-positive，validated win-rate: not-computable，60% 只是待检验目标。

本索引的 authority 与隔离复核见[PA Research authority 与隔离边界审计](../research/authority_boundary_index_audit_2026-08-29_CN.md)。

基础层是所有 pattern 共用的背景、位置、订单和风险语义，不是独立交易形态：

- [`Support / Resistance`](01_support_resistance/README.md)
- [`Measured Move / Targets`](02_measured_move_targets/README.md)
- [`Late Trend Entry Filter`](03_late_trend_entry_filter/README.md)
- [`Multi-timeframe Review`](04_multitimeframe_review/README.md)
- [`Event / Sector / Market Gate`](05_event_sector_market_gate/README.md)
- [`Order / Risk Contracts`](06_order_risk_contracts/README.md)
- [`Market State / Context`](07_market_state_context/README.md)
- [`Leg Pressure / Signal Quality`](08_leg_pressure_signal_quality/README.md)

所有新案例的方向、订单和状态字段统一遵循[`PA Research 统一输出合同`](../docs/pa_research_output_schema_v0_1_CN.md)。

所有基础层文档中的“成交/实际成交/成交路径”均指研究合同或历史回放中可复核的订单路径，不是券商或账户的真实交易日志。真实交易日志若存在，必须来自独立来源；订单卡或回放结果都不能代替它。

## Canonical 输出边界

8 个基础层都是共用视觉补充，不是额外 pattern，也不各自定义一套状态枚举。完整案例先使用统一合同和[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)，再按需要填写基础层字段；`contract_scope`、`data_status`、`as_of_time`、`timeframes_seen`、两年 Daily/重要高低点/EMA 复核、`direction`、`primary_pattern`、`internal_label`、`lineage_status`、`state_transition`、`order_branch`、`structural_stop`、`first_independent_obstacle`、`pre_entry_space_R`、`space_status`、`research_state`、`trade_state`、`gate_result` 和 `handoff_status` 不能被基础层的局部字段替代。

- `01`/`02` 主要提供位置与目标层观察，不单独冻结 pattern 或订单；
- `03`/`04`/`06`/`07`/`08` 的工作卡保留后段、多周期、订单、父级状态和 A/B 质量等补充语义，但活动模板使用 canonical 字段；
- `05` 的 `permission` 与 `gate_result` 只表示前置闸门，不能代替方向、几何或交易状态。

逐项覆盖、枚举和旧字段边界见[`Pattern README 与基础视觉框架 canonical 输出覆盖审计`](../research/backtesting/pattern_foundation_canonical_contract_audit_2026-08-29_CN.md)。

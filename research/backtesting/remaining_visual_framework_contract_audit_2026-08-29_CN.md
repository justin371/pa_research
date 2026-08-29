# remaining visual frameworks 合同边界审计（2026-08-29）

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

## 1. 审计范围

本轮只读核对 PA Research 的 remaining visual frameworks、pattern-specific 案例入口、统一输出合同、
validator 和回归测试。上一轮已覆盖的六个视觉入口与本轮其余入口一起按同一套 canonical 字段复核；
本轮没有查行情、没有查看新图、没有运行回放、没有新增样本，也没有修改 CSV、历史结果或 engine。

覆盖入口：

- `market_state_context_visual_evidence_audit_2026-08-24_CN.md`
- `inside_bar_two_bar_reversal_visual_framework_CN.md`
- `triangle_expanding_range_visual_framework_CN.md`
- `late_trend_entry_visual_framework_CN.md`
- `multitimeframe_visual_review_framework_CN.md`
- `channel_visual_framework_CN.md`
- `bop_gap_acceptance_framework_CN.md`
- `order_branch_visual_protocol_CN.md`
- `failed_breakout_climax_visual_framework_CN.md`
- `final_flag_visual_framework_CN.md`
- `mtr_visual_framework_CN.md`
- `head_shoulders_rounded_top_bottom_visual_framework_CN.md`
- `opening_reversal_visual_framework_CN.md`
- `three_push_pressure_state_framework_CN.md`
- `visual_pattern_triage_protocol_CN.md` 的第二轮深审合同

## 2. 发现与修复

此前部分入口虽引用统一合同，但最小复核卡仍使用合并字段或只给问题清单，容易把视觉描述误读成
完整案例合同。本轮已：

1. 为 BOP 缺口接受、失败突破/高潮、Final Flag、MTR、头肩/圆形和开盘反转补上完整证据头、
   `parent_state`、`direction`、`primary_pattern`、`internal_label`、`state_transition`、lineage、
   订单、结构失效、第一独立障碍、空间和三条状态轴；
2. 为 Inside Bar、后段入场、市场状态、三推和多周期入口补齐遗漏的 canonical 字段；
3. 将 `order_branch_and_actual_fill`、`first_obstacle / measured_move`、`decision_time`、
   `trigger_price_or_zone`、`actual_or_assumed_fill`、`structural_stop_zone`、
   `rough_space_to_obstacle`、`gap_or_event_state`、`outcome_at_decision_time` 等合并/旧字段
   限定为历史显示别名或移除；新记录分别使用 `order_branch`、`actual_fill_or_open_skip`、
   `first_independent_obstacle`、`rough_space_to_first_obstacle_R`、事件字段和结果字段；
4. 将 ABC 入口的跳空重订明确写成 `branch_role: gap_reprice`，不再把 `reprice_after_gap` 当作
   订单分支枚举；
5. 将优先 Pattern 矩阵的示例改成 canonical 的独立字段。矩阵示例仍是历史/解释性展示，不能
   直接成为冻结合同或统计分母。
6. 将视觉快筛协议第二轮的 `trigger_zone`、`structural_stop_zone`、`rough_space` 等工作别名
   映射到统一合同，保留第一轮 `stage_1_fast_screen` 不冻结主标签和订单的边界。

## 3. 当前边界

`primary_pattern`、`internal_label`、`state_transition`、`order_branch`、`space_status`、
`research_state`、`trade_state`、`gate_result` 和 `handoff_status` 仍各自表示不同问题；
pattern-specific 状态（如 `mtr_state`、`final_flag_state`、`breakout_state`、`third_push_state`）
只能作为补充字段。`actual_fill_or_open_skip` 只表示研究/回放订单路径，不是券商或账户的真实交易日志。

`stage_1_fast_screen` 仍只能用 `pattern_candidate`，不能冻结 `primary_pattern` 或 `lineage_id`；
`daily_candidate` 的主标签仍只允许 `ABC_CONT` 或 `BOP`。历史别名不能反向改变当前合同，也不能
用后续走势填补当时缺失的两年 Daily、重要高低点、EMA、空间或订单证据。

## 4. 统计与交接结论

本轮只是合同和防回归修复，没有产生新的冻结交易合同或新的结果分母。结论继续保持
`no-new-positive`，`validated win-rate: not-computable`；60% 仍只是待检验目标。

范围固定为 `PA Research only`：不修改 Codex Trading，不创建量化扫描器，不连接 Futu/OpenD，
不连接 Execution Agent。English boundary: `PA Research only`; `no Codex Trading`; `no quantitative scanner`;
`no Execution Agent`. 后续若要新增样本，必须另立独立目标并完成图表 provenance、事前合同、
订单几何和回放资格审计。

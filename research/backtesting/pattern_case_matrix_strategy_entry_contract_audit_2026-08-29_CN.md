# Pattern 案例矩阵、策略入口与历史别名合同审计（2026-08-29）

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 审计范围

本轮只读核对以下 PA Research 文档、索引、validator 和回归测试：[`ABC 决策矩阵`](../abc_decision_matrix_CN.md)、[`核心八个 Pattern 案例矩阵`](../core_pattern_case_matrix_CN.md)、两份 TSLA 聚合比较矩阵、[`Strategy 候选 inventory`](../../strategy/pattern_inventory_candidates.md)、[`TSLA/META 历史复盘`](../../strategy/reviews/2026-06-25-tsla-meta-example.md)，以及 [`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)。

本轮不查行情、不看新图、不运行回放、不增加样本、不修改 CSV 或 engine，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。所有方向、结构、订单和空间结论都只作为文档合同边界核对，不构成交易授权。

## 发现

### 1. 聚合矩阵此前容易被误读为逐案合同

矩阵正文已经说明“行不替代案例合同”，但 ABC 矩阵又要求“每行方向归一”，而实际列把方向、计数、订单和结果路径合并在自然语言单元格中。核心八个矩阵和两份 TSLA 比较矩阵也没有明确说明一个全局 `primary_pattern` 或全局订单/空间字段不能代表每一行。

这不是数据或回放错误，而是显示层与 canonical 层的边界不够机器可检查。现已在四份矩阵声明：

```text
matrix_scope: aggregate_display_only
row_contract_source: linked_case_file
row_contract_scope: per_row
row_contract_fields: contract_scope; evidence_header; parent_state; direction; primary_pattern; internal_label; state_transition; order_branch; actual_fill_or_open_skip; structural_stop; structural_invalidation; first_independent_obstacle; pre_entry_space_R; space_status; rough_R_R; research_state; trade_state; gate_result
row_result_boundary: independent_replay_or_result_only
historical_alias_policy: display_only_until_mapped
```

因此，矩阵里的方向、H/L/ABC/三推文字和后续“到达阻力/支撑/MM”的描述，必须回到链接案例逐行解释；缺少案例合同的行只能导航或记录路径，不能进入候选、冻结合同或胜率分母。

### 2. Strategy inventory 的方向和状态是索引提示，不是授权字段

inventory 的视觉候选表只有索引层 `direction`、代表性入口和“当前状态”。其中 `process-*`、`*-reached`、`opening-skip`、`pattern_like` 等词可能同时描述事前候选和事后路径，若没有显式边界，容易被复制成 `research_state` 或结果。

现已增加 `inventory_scope: visual_navigation_only` 及逐列映射：代表性入口才是 canonical 字段来源；`direction` 只是研究方向提示；“当前状态”不能替代 `research_state`、`trade_state`、`gate_result` 或 `handoff_status`；候选 ID 中的 pattern 词不能替代 `primary_pattern`、`internal_label`、`parent_state` 或 `state_transition`。inventory 仍不冻结新案例。

### 3. META 历史复盘头缺少可审计的父状态与空间字段

[`TSLA/META 历史复盘`](../../strategy/reviews/2026-06-25-tsla-meta-example.md) 原本已经正确保留 `historical_context_only`、不完整数据、`no_valid_direction`、`other`、`pending` 和 `observation_only`，但没有显式写出 `parent_state`、`structural_stop`、`pre_entry_space_R`、`space_status`、`rough_R_R` 和 `thesis_state`。现已按已有证据补为 `unclear` 或 `pending`/`unknown`，没有用后续目标或形态描述反推方向、空间或结果，也没有添加 `outcome`。

### 4. 历史显示别名保留，但不再越过映射边界

矩阵和历史案例中的 `H1/H2-like`、`L1/L2-like`、`B 类三推`、`process-target-reached` 等原始叙述仍保留，便于复核当时的视觉语言；它们只是 display/path 语义。新记录必须使用 `primary_pattern`、`internal_label`、`parent_state`、`state_transition`、`order_branch`、`structural_stop`、`first_independent_obstacle`、`pre_entry_space_R` 和 `space_status` 等 canonical 字段。`actual_fill_or_open_skip` 仍只表示研究/回放路径，不是真实交易日志。

## 修复与自动守卫

- 为四份聚合矩阵和 Strategy inventory 增加显示范围、逐行合同来源、字段清单、事前/事后结果边界和历史别名策略；
- 为 META 历史复盘补齐缺失的父状态、订单/空间和 thesis 字段，并保持 `unknown`/`pending`；
- 将本审计加入根目录、docs、research、backtesting、patterns、foundations 和 strategy 的 canonical 索引；
- validator 现在检查五个聚合入口的边界声明、META 历史复盘的完整 canonical 头，以及本报告的范围/统计/隔离声明；
- 增加回归测试，防止聚合表重新出现“全局字段冒充逐案字段”、META 复盘漏写边界字段或历史路径进入事前结果层。

## 结论边界

本轮只修复文档、索引、validator 和测试，没有新增样本、图表判断、订单结果、回放分母或胜率证据。`no-new-positive` 保持不变；`validated win-rate: not-computable` 保持不变；`60%` 仍只是待检验目标。聚合矩阵、Strategy inventory 和历史案例都不构成生产规则、交易授权或 Execution Agent 输入。

本文件只属于 `PA Research only`，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

## 验证记录

- 定向回归：39 tests passed；全量测试：322 tests passed；
- 文档 validator：passed，检查 310 个 Markdown 文件和 2157 条本地链接；
- `git diff --check`：passed；
- 验证只使用 PA Research 本地文件；Trading checkout 仅做只读隔离确认；
- 最终提交和远端 `main` SHA 以本轮完成后的 Git 记录为准。

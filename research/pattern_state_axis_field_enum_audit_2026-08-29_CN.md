# Pattern 状态轴、字段与枚举一致性审计（2026-08-29）

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only`

## 审计目的与边界

本轮以[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)为字段 authority，核对[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)、`patterns/README.md` 和 16 个 pattern README 的字段命名、状态枚举与模板边界。pattern-specific 字段可以补充形态语义，但不能重载统一合同的状态字段。

`scope_boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`

本轮不下载行情、不查看新图、不运行正式回放、不新增样本，不改变 pattern 规则或 engine 有效语义。`stop_limit` 在统一合同中仍是研究记录分支，不是当前回放器的可输入分支。

## 统一字段与状态轴

当前 canonical 状态轴保持分离：

```text
primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other
internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending
state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate
research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
handoff_status: research_only / not_ready / ready_for_system
```

`BOP` 是 `primary_pattern` 或 `bop_state` 的语义，不是 `state_transition` 的值；`observation_only`、`valid_no_trade`、`pending` 也不能互相替代。Daily 选股模板只把 `ABC_CONT` 和 `BOP` 作为当前顶层日线主标签，其他值是历史/兼容冻结合同或研究记录语境，不能据此扩展日线规则。

## 16 个目录覆盖

本轮实际核对的完整目录集合如下；前八个是核心目录，后八个是独立研究主题：

| 层级 | 目录 README |
| --- | --- |
| core | [`01_h1_l1_first_entry`](../patterns/01_h1_l1_first_entry/README.md) |
| core | [`02_h2_l2_second_entry`](../patterns/02_h2_l2_second_entry/README.md) |
| core | [`03_abc_continuation`](../patterns/03_abc_continuation/README.md) |
| core | [`04_range_edge_second_entry`](../patterns/04_range_edge_second_entry/README.md) |
| core | [`05_failed_breakout_climax`](../patterns/05_failed_breakout_climax/README.md) |
| core | [`06_breakout_pullback_bop`](../patterns/06_breakout_pullback_bop/README.md) |
| core | [`07_mtr_reversal`](../patterns/07_mtr_reversal/README.md) |
| core | [`08_three_push_h3_l3`](../patterns/08_three_push_h3_l3/README.md) |
| independent | [`09_vcp_minervini`](../patterns/09_vcp_minervini/README.md) |
| independent | [`10_final_flag`](../patterns/10_final_flag/README.md) |
| independent | [`11_opening_reversal`](../patterns/11_opening_reversal/README.md) |
| independent | [`12_channel`](../patterns/12_channel/README.md) |
| independent | [`13_inside_bar_two_bar_reversal`](../patterns/13_inside_bar_two_bar_reversal/README.md) |
| independent | [`14_triangle_expanding_range`](../patterns/14_triangle_expanding_range/README.md) |
| independent | [`15_double_top_bottom`](../patterns/15_double_top_bottom/README.md) |
| independent | [`16_head_shoulders_rounded`](../patterns/16_head_shoulders_rounded/README.md) |

## 发现与修复

### 1. 快筛的 `state_transition` 别名已移除

视觉复核卡的快速初筛曾写成 `none / pending / BOP / failed_breakout / ...`，这同时混入了未冻结状态和主标签别名。现在与统一合同对齐为 `none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate`。快筛的不确定性继续通过第一阶段结论和后续 `research_state: pending` 表达。

### 2. Pattern 总索引改用 canonical 字段名

`patterns/README.md` 的统一研究字段已把 `lineage_and_attempt_count`、`signal_bar_and_trigger`、`invalidation` 和合并式 `event_sector_market_gate` 展开为 `lineage_status`/`lineage_id`、`signal_bar`/`confirmation_bar`/`new_trigger`、`structural_invalidation`、`event_context`/`event_bucket`/`sector_state`/`market_state`/`permission`/`gate_result` 等字段，同时补上 Daily 左侧背景与 EMA 复核字段。各目录的最小协议仍是差异字段，不替代完整输出合同。

### 3. Pattern README 的状态别名已归一

`01` 的 `no_trade` 已改为 `valid_no_trade`；`04`、`07`、`08`、`09`、`12`、`13`、`15`、`16` 中的 `observation-only` 已改为 `observation_only`。`04–08` 的 order-branch 最小协议同时显式保留研究用 `stop_limit`，不把它误读成当前 engine 可直接回放的普通 stop。

### 4. MTR 专属状态不再重载统一 `thesis_state`

`07_mtr_reversal/README.md` 曾把 `reversal-attempt`、`MTR-candidate` 等 pattern-specific 状态写在统一字段 `thesis_state` 下。现在改为 `mtr_state: reversal_attempt / mtr_candidate / mtr_confirmed_for_research / failed_mtr_thesis`，并保留 canonical `thesis_state: working / failed / invalidated / replaced / pending`，避免把 MTR 视觉阶段误当成通用 thesis 状态。

### 5. 未发现需要改动 canonical schema 的冲突

统一输出合同本身的上述状态轴和字段已经正确；`primary_pattern` 中保留 H/L、H3/L3、RFB、MTR 等历史/兼容值有明确说明，和 Daily 选股只使用 `ABC_CONT`/`BOP` 并不矛盾。`observation-only`、`no_trade` 等旧写法仍可在视觉卡的“旧写法映射”说明中出现，但活动 pattern README 的新状态字段不再使用它们。

## 验收口径与结论

1. 16 个 pattern README、总索引和视觉复核卡均指向同一组 canonical 状态轴；
2. 统一字段与 pattern-specific 字段分开，不能用 `BOP` 替代 `breakout_acceptance`，也不能用 `mtr_state` 替代 `thesis_state`；
3. 旧别名、模板缺项和 `stop_limit` 的研究/回放边界有回归检查；
4. `research_state`、`trade_state`、`gate_result`、`handoff_status` 继续分别记录；
5. `no-new-positive` 与 `validated win-rate: not-computable` 继续成立，本轮没有新增统计正例或胜率结论。

本轮只完成 PA Research 文档/测试一致性修复，不产生交易授权、量化扫描器或 Execution Agent 连接。

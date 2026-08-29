# PA Research Pattern 主标签映射与 BOP 状态迁移审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 目的与范围

本轮只读审计统一输出合同、日线选股规则、视觉复核卡、[`patterns/README.md`](../patterns/README.md) 和 16 个 pattern README 的 `direction`、`primary_pattern`、`secondary_context`、`state_transition`、`lineage_id` 映射。重点是确认日线候选白名单、H/L 内部标签、三推与区间边缘三推的分隔，以及 BOP 接受后旧合同是否真正失效。

本轮不下载行情、不看新图、不运行回放、不新增样本、不计算胜率，不改变 pattern 规则或 engine 有效语义。`no-new-positive` 与 `validated win-rate: not-computable` 保持不变。

## 1. 统一裁决

### 1.1 日线候选的主标签白名单

当 `contract_scope: daily_candidate` 时：

- `primary_pattern` 只允许 `ABC_CONT` 或 `BOP`；
- H1/H2/L1/L2 只能写入 `internal_label`，不能写入主标签、`pattern_family` 或自由文本主标签；
- H3/L3 在日线候选中也只写入 `internal_label`，并用 `secondary_context` 说明三推压力状态；
- `range_edge_three_push` 是成熟区间上沿/下沿的独立位置分支旗标，不是 `primary_pattern`，也不等同于 `H3_L3`；
- `H1_L1`、`H2_L2`、`H3_L3`、`RFB`、`MTR`、`other` 以及独立主题名称，只能在 `deep_review`/`historical_context_only` 的兼容或观察记录中按其合同语义使用，不能扩展日线选股白名单。

### 1.2 BOP 状态迁移

若事前可见边界被日线强收盘越过、获得跟随并在回踩中守住，统一合同必须改写为：

```text
primary_pattern: BOP
state_transition: breakout_acceptance
```

原 pattern 或反向 thesis 与旧订单合同同时失效。必须重新冻结 `new_trigger`、`structural_stop`、`first_independent_obstacle` 和空间；不能沿用旧 entry/stop/target，也不能把旧合同结果并入 BOP。只有突破接受而尚未形成回踩时，仍按 `bop_state: acceptance_watch` 记录，不补写不存在的回踩。

### 1.3 三推与区间边缘三推

`H3_L3` 只表示同一主周期、同一 lineage 下已能分隔的第三次尝试；`internal_label` 必须是明确的 `H3` 或 `L3`。`range_edge_three_push: yes` 只表示第三推到达成熟区间边缘，仍需拒绝/假突破回区间、反向触发和空间；它不把区间边缘自动改名为开放趋势 H3/L3，也不因“数到三”产生方向授权。若突破边缘并在外侧接受，优先进入 BOP 新合同。

## 2. 16 个入口映射

| 入口 | 日线候选映射 | 深审/历史兼容边界 |
| --- | --- | --- |
| [`01_h1_l1_first_entry`](../patterns/01_h1_l1_first_entry/README.md) | `primary_pattern: ABC_CONT` 或 `BOP`；`internal_label: H1/L1` | H1/L1 是第一次内部尝试，不是日线主标签 |
| [`02_h2_l2_second_entry`](../patterns/02_h2_l2_second_entry/README.md) | `primary_pattern: ABC_CONT` 或 `BOP`；`internal_label: H2/L2` | H2/L2 是同一回调中的第二次内部尝试，不是独立主标签 |
| [`03_abc_continuation`](../patterns/03_abc_continuation/README.md) | `primary_pattern: ABC_CONT`；H/L 放 `internal_label` | `ABC + H/L` 是母结构与内部关系，不能重复统计 |
| [`04_range_edge_second_entry`](../patterns/04_range_edge_second_entry/README.md) | 未闭合区间分支不进入日线主标签；接受后才可为 `BOP` | 已闭合的历史失败突破/二次确认可用兼容 `RFB` |
| [`05_failed_breakout_climax`](../patterns/05_failed_breakout_climax/README.md) | 失败/高潮观察不扩展日线主标签；接受后转 `BOP` | 闭合失败突破可用 `RFB`，其余保留 `other`/状态 |
| [`06_breakout_pullback_bop`](../patterns/06_breakout_pullback_bop/README.md) | `primary_pattern: BOP` | 接受、回踩、角色转换写入 `state_transition`/`bop_state`，不拼接主标签 |
| [`07_mtr_reversal`](../patterns/07_mtr_reversal/README.md) | MTR 观察不扩展日线主标签；日线候选仍只用 `ABC_CONT`/`BOP` | 只有成熟趋势、结构破坏、二次确认和空间闭合才用兼容 `MTR` |
| [`08_three_push_h3_l3`](../patterns/08_three_push_h3_l3/README.md) | H3/L3 只作 `internal_label` 与 `secondary_context`；区间边缘用 `range_edge_three_push` | 闭合同一 lineage 的三推才可用兼容 `H3_L3`，且 `internal_label` 不能写 `H3_L3` |
| [`09_vcp_minervini`](../patterns/09_vcp_minervini/README.md) | 独立主题不扩展日线主标签；必要时保留为 `secondary_context`/`other` | VCP 的 T1/T2/T3 与 PA H/L 不互换 |
| [`10_final_flag`](../patterns/10_final_flag/README.md) | 独立末端背景不扩展日线主标签；接受后转 `BOP` | 反向合同必须单独闭合，不能把 Final Flag 当 MTR |
| [`11_opening_reversal`](../patterns/11_opening_reversal/README.md) | 开盘事件不扩展日线主标签；接受后转 `BOP` 或新合同 | 开盘触发、事件和订单合同单独记录 |
| [`12_channel`](../patterns/12_channel/README.md) | 通道背景不扩展日线主标签；局部 H/L 仍放 `internal_label` | 通道突破接受后转 BOP，通道本身不创造 H/L/MTR |
| [`13_inside_bar_two_bar_reversal`](../patterns/13_inside_bar_two_bar_reversal/README.md) | K 线结构不扩展日线主标签；与 H/L 重叠时按内部标签记录 | 母 K/两根反转未冻结时保持 `other`/观察 |
| [`14_triangle_expanding_range`](../patterns/14_triangle_expanding_range/README.md) | 三角形/扩张区间不扩展日线主标签；接受后转 `BOP` | 区间内区间、失败突破和新 BOP 合同必须分开 |
| [`15_double_top_bottom`](../patterns/15_double_top_bottom/README.md) | 双顶/双底不扩展日线主标签；普通趋势延续可回到 `ABC_CONT` | 根据父级、结构破坏和接受分流到兼容 `RFB`/`MTR` 或观察 |
| [`16_head_shoulders_rounded`](../patterns/16_head_shoulders_rounded/README.md) | 头肩/圆顶不扩展日线主标签；接受后转 `BOP` | 颈线、结构破坏和二次确认闭合后才可进入兼容反转记录 |

16 个入口都补上同一套“日线白名单 + BOP 旧合同失效”边界，避免只写“转 BOP”却遗漏旧 entry、stop、target 不能继续沿用的执行含义。`lineage_id` 仍只用于依赖识别，不会替研究者自动证明三个推进属于同一组三推。

## 3. 已修复的明确问题

1. 视觉复核卡的 `pattern_family` 速记枚举曾直接列出 `TPB_H1_H2_H3`、`L1_L2_L3`，现在改为 `ABC_CONT`、`BOP`、`RFB_SECOND`、`H3_L3`、`MTR`、`other`，并把 H/L 明确放入 `internal_label`。
2. 统一输出合同、日线规则、patterns 索引和 16 个入口现在都明确 `daily_candidate` 的 `ABC_CONT/BOP` 白名单，以及 H3/L3 与 `range_edge_three_push` 的关系边界。
3. 16 个 pattern README 都明确：边界被接受后要写 `primary_pattern: BOP` 与 `state_transition: breakout_acceptance`，原 pattern/反向 thesis 和旧订单合同失效并重新冻结几何。
4. 视觉识别冒烟报告中的自由文本 `primary_pattern:` 会被误读为统一合同字段，已改为 `visual_pattern_label:`，并声明只有进入完整研究记录后才按统一合同收敛。
5. 16 个 pattern README 现在都在入口处明确写出 `direction: long / short / no_valid_direction`；三推目录另行声明 `attempt_direction` 不能替代 canonical `direction`。
6. adopted 的 ABC 决策矩阵、优先候选矩阵、订单分支协议和大盘筛选记录已把当前状态统一为 `research_positive_conditional`/`valid_no_trade`；历史别名仍只留在明确的别名说明中。

## 4. 验证与结论

- 16 个 pattern 入口均存在，并包含统一映射和 BOP 状态迁移边界；
- 16 个 pattern 入口均显式声明 canonical `direction` 枚举；
- 日线候选卡与日线规则保持 `primary_pattern: ABC_CONT / BOP`；
- `H1/H2/L1/L2` 不再作为视觉卡的 pattern family 主标签，`H3/L3` 与 `range_edge_three_push` 保持独立字段；
- 冒烟报告不再把自由文本视觉名称伪装成统一 `primary_pattern`；
- 当前决策/订单入口不再把正向条件或有效不交易写成旧别名；
- 本轮没有新增样本、成交或统计分母，`validated win-rate: not-computable`，结论保持 `no-new-positive`。

范围声明：`PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。本轮只修复文档映射和回归守卫，不改变回放 engine 的有效语义。

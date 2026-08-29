# 三推/H3-L3 与区间边缘合同边界审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 1. 范围与目的

本轮只审计 PA Research 内部 H3/L3、三推压力状态和成熟区间边缘三推的字段边界。对照[`PA Research 统一输出合同`](../../docs/pa_research_output_schema_v0_1_CN.md)、[`PA 图表视觉复核卡`](../../docs/visual_pa_review_card_CN.md)、[`PA Research 日线选股规则`](../../docs/pa_research_daily_selection_rules_v0_1_CN.md)、[`三推/H3-L3 pattern README`](../../patterns/08_three_push_h3_l3/README.md)、[`三推压力状态框架`](../three_push_pressure_state_framework_CN.md)和[`核心 Pattern 交叉一致性审计`](../core_pattern_cross_audit_CN.md)。

本轮不下载行情、不看新图、不运行回放、不增加样本、不改写 CSV、历史结果或 engine 有效语义；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent 或 Futu/OpenD。

## 2. 发现的问题

### 2.1 区间边缘方向字段缺失

视觉卡、三推 pattern 和压力框架已经使用 `range_edge_side: upper / lower / none / pending`，但统一输出合同和日线候选模板只有 `range_edge_three_push`，没有保存上沿/下沿。只复制位置旗标会丢失最关键的方向来源：上沿只能研究空头，下沿只能研究多头。

这不是把位置变成自动信号。`range_edge_side` 只保存位置和研究方向假设；触发、结构止损、首障碍、空间和合同未冻结时，canonical `direction` 仍可以是 `no_valid_direction`。本轮已把 `range_edge_side` 加入统一合同和日线模板，并写明以下条件：

- `range_edge_three_push=yes` → side 必须是 `upper` 或 `lower`；
- `upper` → 只建立空头研究方向，`lower` → 只建立多头研究方向；
- `range_edge_three_push=no` → side 写 `none`；`pending` → side 写 `pending`。

### 2.2 三推状态字段和枚举漂移

此前三处使用了不同字段/枚举：视觉卡使用 `h3_l3_state`，三推 pattern 使用 `third_push_state`，压力框架输出使用 `push_state`；同一含义还出现 `exhaustion`、`expansion-or-climax`、`range-repeat` 和 `channel-continuation`。这会让人工记录和后续分层无法稳定归类。

现统一为 `third_push_state`，只使用以下 canonical 值：

```text
exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
```

`third_push_state` 只描述第三推的压力状态；`research_state` 负责候选/观察/不交易等研究结论，`first_reverse` 与 `second_confirmation` 负责反向证据，`order_branch`、`trade_state` 和 `gate_result` 负责订单/状态/闸门。它们不能互相替代。历史审计中的连字符自然语言保留为别名解释，新记录统一使用 canonical 字段。

### 2.3 H3/L3、区间边缘三推和可交易方向必须分层

- H3/L3 是同一主周期、同一 lineage 中的第三次有意义尝试；三推压力状态是对效率、收盘、接受和位置的描述，两者可以重叠但不是同义词。
- `range_edge_three_push` 是成熟区间上沿/下沿的位置分支，不把区间边缘自动命名成开放趋势 H3/L3；区间中部仍是观察。
- 第三推极值不构成入场。即使区间边缘方向假设已经明确，也必须另外记录第一反向、触发、结构止损、第一独立障碍和空间；外侧强接受则重建 BOP 合同，旧反向合同失效。
- `second_confirmation=yes` 是升级 MTR/主要趋势反转研究的更高层证据，不是所有区间边缘候选的默认入场条件。

### 2.4 当前回放输入没有静默承载三推位置字段

当前 `backtesting.py` engine `0.3.9` 支持兼容的 `primary_pattern: H3_L3` 和明确的 `internal_label: H3/L3`，但冻结合同 CSV 的最小列没有 `range_edge_three_push`、`range_edge_side` 或 `third_push_state`。这里的边界是订单/状态分轴，不是缺陷：三推位置和压力状态必须先保留在人工研究记录，只有经过人工闭合、方向和数值订单字段收敛后，才能决定是否进入兼容回放合同；回放器不会从 OHLC 自动识别三推或区间边缘。

## 3. 当前冻结合同和统计事实

只读取 `research/backtesting/*contracts*.csv`（排除 `contracts.example.csv`）得到：

| 项目 | 当前事实 |
| --- | ---: |
| 冻结合同 CSV | 7 份 |
| 冻结合同总行数 | 60 |
| `primary_pattern` | `H1_L1` 46、`H2_L2` 14 |
| `internal_label` | H1 24、H2 8、L1 22、L2 6 |
| H3/L3 冻结行 | 0 |
| `range_edge_three_push` / `third_push_state` CSV 列 | 0 |

当前没有可用于三推/H3/L3 的冻结回放合同，因此本轮不产生 H3/L3 胜率、盈亏比或新分母。现有 60 行仍然只是 H/L 历史回放集合；ABC/BOP intake 仍是 `contract_frozen=no`，也不进入分母。

## 4. 修复后的统一记录格式

三推相关的新研究记录按以下字段填写：

```text
attempt_direction: bullish_attempts / bearish_attempts / unknown
third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
first_reverse: none / touch / structural_break
second_confirmation: yes / no / pending
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
direction: long / short / no_valid_direction
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending
gate_result: pass / conditional / observation_only / valid_no_trade / pending
```

`attempt_direction` 不是 canonical `direction`；上沿/下沿也不是订单授权。只有图表范围、lineage、反向证据、订单几何和硬闸门都完成后，才可以把研究方向收敛到可回放的 long/short 合同。

## 5. 结论

本轮修复了统一输出合同、日线模板、视觉卡、三推 pattern 和压力框架之间的字段/枚举漂移，并增加了回归守卫。没有新增图表、合同、成交或统计样本；`no-new-positive` 和 `validated win-rate: not-computable` 保持不变。

本审计只属于 PA Research：`PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。

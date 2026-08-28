# PA Research 统一输出、视觉字段与状态轴审计（2026-08-29）

日期：`2026-08-29`  
文档状态：`document_status=research_only / document_maturity=provisional / handoff_status=not_ready / not-quantitative`

本审计只检查 PA Research 内部的统一输出字段、视觉协议、ABC/BOP/H1/H2/L1/L2/H3/L3 研究记录和索引。依据是[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)与[`PA 图表视觉复核卡`](../docs/visual_pa_review_card_CN.md)。不下载行情、不运行正式回放、不新增样本，不修改 pattern 规则或 engine 有效语义，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

## 一、审计结论

本轮发现并修复了两类字段语义问题：

1. 旧文档头和 7 个回放审计结论块把文档成熟度 `provisional` 写成了案例状态轴 `research_state`；现统一改为 `document_maturity: provisional`。案例 `research_state` 仍只使用 `pattern_like`、`research_candidate`、`research_positive_conditional`、`observation_only`、`valid_no_trade`、`failed_thesis` 或 `pending`。
2. H3/L3 最小视觉协议把 `bullish_attempts / bearish_attempts` 写在 canonical `direction` 下，容易与 `long / short / no_valid_direction` 混淆；现改为 `attempt_direction`，并补齐多周期背景、事件、空间和四条状态轴的映射。

另外，6 个历史案例摘要原来已有 `contract_scope`、`direction`、`research_state`、`trade_state`、`handoff_status`，但没有 `gate_result`。现按正文裁决补齐：

| 记录 | direction | research_state | gate_result | 依据 |
| --- | --- | --- | --- | --- |
| QCOM 宽 B 区间边界 | `no_valid_direction` | `observation_only` | `observation_only` | 宽幅区间、L1/L2 未冻结、首支撑偏近 |
| TSLA ABC/H1-H2 三案例矩阵 | `long` | `observation_only` | `observation_only` | 用于比较假设，日线直接交易被首障碍否决 |
| TSLA 空头 ABC 候选筛选 | `short` | `research_candidate` | `pending` | A/B 锚点有歧义，尚待独立冻结 |
| TSLA 空头 ABC 比较矩阵 | `short` | `observation_only` | `observation_only` | 比较/排序材料，不是交易合同 |
| TSLA H1/H2 候选筛选 | `long` | `research_candidate` | `pending` | 尚未完成低周期、事件、空间和触发复核 |
| TSLA 卖出高潮后区间 | `no_valid_direction` | `observation_only` | `observation_only` | 父级交易区间取代趋势 ABC 解释 |

这些补全只修复状态映射，不把任何记录升级为交易授权或统计样本。

## 二、文档成熟度与案例状态分层

`document_status`、`document_maturity`、`handoff_status` 是文档生命周期元数据；`research_state`、`trade_state`、`gate_result`、`thesis_state` 是案例/合同状态轴。它们不能合并成一个 `status`，也不能因为文档被 `adopted` 就推导出可交易或已验证胜率。

本次清理覆盖 49 个文档头和 7 个回放审计结论块。之后全仓库不再把 `provisional` 或 `research_only` 填入案例的 `research_state` 作为文档元数据。`provisional` 仍可在正文中描述研究成熟度或某个 pattern-like 观察，但不冒充案例状态枚举。

## 三、多周期与左侧背景映射

- `Daily` 负责父级趋势/区间/过渡、两年左侧主要高低点、EMA20/50/200、事件和主要位置。
- `4H` 或 `4H-like`/`60m` 负责 A/B lineage、中间结构、回调是否受控和角色转换；`4H-like` 不冒充原生 4H。
- `1H` 可补充接受、回测或独立低周期合同；若独立交易，必须与高周期合同分开。
- `15m` 只负责信号 K、穿越、开盘跳过、实际触发和低周期回测，不能创造高周期背景、首障碍或方向。
- H1/H2/L1/L2 的计数周期必须写清楚，且只在同一回调 lineage 内计数；三推/H3/L3 也不能把不同周期拼成一组。
- 默认先看至少两年 Daily 左侧，记录重要高点、低点、支撑、阻力、角色转换区和 EMA 方向。历史摘要缺少完整两年或低周期证据时，保持 `historical_context_only`、`pending` 或 `observation_only`，不以局部图补写缺失证据。

因此，`timeframe` 是 H3/L3 协议中的计数周期，`context_timeframes_seen` 是背景覆盖；两者不应混成一个“多周期已确认”结论。

## 四、A/B、lineage、事件与空间

- A 腿、B 腿、C 腿和第一次/第二次/第三次尝试是视觉结构描述；A 很强不等于 C 必然成功，B 的深度和前后段压力必须单独记录。
- `lineage_status` 与 `lineage_id` 用于防止把同一父级结构、同一回调或嵌套尝试重复当成独立样本。缺失或不清楚时只能写 `pending`/`unclear`，不能为了完整性编造 ID。
- `event_context`/`event_bucket` 是入场前事件证据；财报、异常跳空和重定价必须单独分层，不能由后来走势覆盖。
- `space_status`、`pre_entry_space_R`、首障碍和 `rough_R_R` 是入场前几何；`first_obstacle_hit`、`realized_R` 和结果状态属于事后路径，不能回填或改善原来的空间判断。
- `gate_result` 表示研究闸门，`trade_state` 表示是否形成交易状态，`handoff_status` 表示能否交接；任何一个轴都不等于胜率、成交或授权。

## 五、BOP 与 H3/L3 协议修正

### BOP

[`BOP 真实多日回踩候选审计`](bop_multiday_pullback_candidate_audit_2026-08-24_CN.md)的协议块现在保持 `primary_pattern: BOP / other`。`failed_breakout_boundary`、`range_edge_boundary` 等是 `candidate_class` 或 `state_transition`，不是把观察边界标成 BOP 主合同。协议块同时显式列出 `contract_scope`、方向、父级状态、时间覆盖、lineage、事件、空间及 `research_state`/`trade_state`/`gate_result`/`handoff_status`。

### H3/L3

[`三推 / H3-L3：压力状态`](../patterns/08_three_push_h3_l3/README.md)现在用 `attempt_direction` 描述三次尝试朝向；完整案例仍必须在统一合同中填写 canonical `direction: long / short / no_valid_direction`。`parent_state`、`lineage_status`、`event_bucket` 和 `space_status` 使用统一枚举；三推仍先判断衰竭、扩张/高潮、区间重复或通道延续，再决定是否有 H3/L3 研究价值。

H/L 的公共 lineage 账本也已将 `same-lineage` 规范为 `same_lineage`，并补出 `lineage_id` 占位字段；`review_timeframe` 仍只表示计数周期，不能把低周期尝试拼成高周期 H1/H2/L1/L2。

## 六、未改变的边界与结论

- 本轮没有新增视觉样本、回放结果、交易日志或胜率分母。
- 没有把任何 `pattern_like`、`research_candidate` 或 `research_positive_conditional` 改成验证正例。
- BOP 多日正例缺口、H3/L3 衰竭正例缺口和当前历史结果的 provenance 限制仍然存在。
- 统一统计结论继续是 `no-new-positive`；`validated win-rate: not-computable`。
- 所有记录仍只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

## 七、验收证据

本次修改后应通过：

1. `python -m unittest discover -s tests -v`；
2. `python -m compileall -q pa_research_backtest scripts`；
3. `pwsh -NoProfile -File .\scripts\validate_pa_research_docs.ps1`；
4. `git diff --check`；
5. PA Research 工作树与 `origin/main` 同步，Codex Trading 工作树无变化。

本审计是字段和状态轴的一致性修复，不是新的 pattern 规则或量化实现。

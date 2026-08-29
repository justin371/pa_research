# PA Research 证据范围与数据状态一致性审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 目的与范围

本轮只读审计统一输出合同、日线候选卡、视觉复核卡、16 个 pattern README、视觉筛选协议、回放 README、候选目录和现有历史报告中的 `contract_scope`、`data_status`、`chart_scope`、`daily_context_window`、`timeframes_seen`。重点是确认：日线选股只使用完成 Daily；两年左侧背景按逐标的记录；低周期只能作为深审或独立订单合同；历史、延迟、实时已确认和不完整状态不被混成一个字段。

本轮不下载行情、不看新图、不运行回放、不新增样本、不计算胜率，不改变 pattern 规则或 engine 有效语义。`no-new-positive` 与 `validated win-rate: not-computable` 保持不变。

## 1. Canonical 裁决

### 1.1 范围、周期和覆盖

- `contract_scope: daily_candidate` 只允许使用完成的 Daily K 线，且 `timeframes_seen: Daily`；4H/1H/15m 只能出现在候选入选后的 `deep_review` 或另立的订单合同中。
- `daily_context_window` 描述单个标的的 Daily 左侧是否覆盖至少两年；批次级 `two_year_chart_coverage` 不能替代它。
- `chart_scope` 只描述整张图表的可见完整度，使用 `full / partial / unavailable`；`full` 不自动等于两年覆盖，仍必须填写 `daily_context_window`。
- `timeframes_seen` 是已实际查看的周期集合，不是“数据文件理论上能生成的周期”；低周期不能倒灌成为日线主标签或补写缺失的左侧结构。

### 1.2 数据状态和 session 分工

`data_status` 的 canonical 值只有 `historical`、`delayed`、`live_confirmed`、`incomplete`。`historical_close` 是 `session_state` 的值，不是数据状态；“after-close”“not live”“public data”“not Futu”等来源/时效说明放在 `data_source` 或专门说明字段中，不拼进 `data_status`。

`live_confirmed` 只在当前来源、时间戳、周期和实时状态确实被确认时使用；历史数据不能因为报告写作时间接近当前日期而升级为实时。若完整图表、两年背景、事件或触发证据缺失，保持 `partial`/`unavailable` 与 `pending`/`observation_only`，不能靠后续结果补齐。

### 1.3 回放边界

回放 CSV 的 `daily_context_window` 是冻结合同的人工证据闸门，不等于价格 CSV 有两年数据。`contract_scope`、`data_status`、`chart_scope` 和 `timeframes_seen` 留在上游视觉/研究记录与 provenance 中；回放器不从价格路径推断或补写它们。回放结果也不能把 `daily_context_window`、图表完整度或数据状态倒推回候选记录。

## 2. 已修复的明确漂移

| 位置 | 明确问题 | 修复 |
| --- | --- | --- |
| 16 个 `patterns/*/README.md` | 文字要求查看两年 Daily，但共同证据头没有明确 `daily_context_window` | 统一补入该字段，并继续要求缺失时保留 `pending`/`observation_only` |
| `research/visual_pattern_triage_protocol_CN.md` | 使用单数 `timeframe_seen`，且 `chart_scope` 缺少 `unavailable`；stage-1 字段没有把范围和两年覆盖写全 | 改为 `contract_scope`、`timeframes_seen`、完整 `chart_scope` 枚举和 `daily_context_window` |
| 四份旧的 H/L 视觉案例 | `timeframe_seen` 与 `data_status: historical / after-close; not live` 把周期和时效说明混在非 canonical 字段 | 改为 `timeframes_seen`、`data_status: historical`，将 after-close/not-live 保留在 `data_source`，并明确图表/两年证据不可用 |
| 两份 TSLA 历史候选筛选 | `data_status: historical_close` 把 session 状态写进数据状态 | 改为 `data_status: historical`，另写 `session_state: historical_close`，并显式记录周期、图表范围和两年窗口 |
| `research/visual_recognition_smoke_test_2026-08-24_CN.md` | 公共历史图像的 `data_status` 含来源、非 Futu 和非实时说明，`chart_scope` 也不是 canonical 值 | 改为 `data_status: historical`，另列说明字段，`chart_scope: full` 与 `daily_context_window: >=2y` 分开记录；仍保持 `stage_1_fast_screen`，不升级为交易合同 |
| 回放 README 与候选目录 | 上游视觉字段和机器回放字段的边界说明不够直接，候选模板仍使用 `timeframe` 简写 | 补充“不可从 CSV 推断/补写”的边界，并改用 canonical `timeframes_seen`、`chart_scope` 和 `daily_context_window` |
| 两份旧顶层历史案例：[`NFLX 三推顶部`](nflx_three_push_top_boundary_2024-08-05_2024-09-26.md) 与 [`TSLA 卖出高潮后区间`](tsla_range_after_sell_climax_2025-03-11_2025-05-13.md) | 正文是历史/事后研究，但原始记录没有自包含的数据源、截止时间、时区、图表范围和两年 Daily provenance；NFLX 还把“完整图表”写在标题式叙述中，容易被误读为仓库内完整 artifact | 增加 `contract_scope: historical_context_only`；缺失项明确写 `data_status: incomplete`、`unknown`/`unavailable_in_original_log`、`chart_scope: partial` 和 `daily_context_window: unavailable`，不臆造 Futu、实时或完整两年证据，并把 NFLX 的“完整图表”改为记录范围表述 |

## 3. 有意保留的非逐标的文档

`abc_hl_stratified_outcome_audit`、`event_sector_multitimeframe_cross_pattern_audit`、`h_l_lineage_visual_boundary_audit`、`order_risk_contract_visual_evidence_audit`、`range_edge_second_entry_visual_boundary_audit` 以及 TSLA 比较矩阵是协议、汇总或跨案例导航，不是一个标的的一份完整候选合同。它们可以展示字段枚举或审计范围，但不能凭一个全局 `contract_scope` 伪造每个案例的 `data_status`、图表范围或两年覆盖；进入实际案例记录时仍必须逐标的填写 canonical 字段。

这类文档的“缺少字段”不被静默补成 `full` 或 `>=2y`，因为那会把框架级说明误读为视觉证据。现有局部案例若没有可复核的完整图表，继续使用 `unavailable`、`partial`、`pending` 或 `observation_only`。

### 3.1 顶层历史案例的 legacy provenance 复核

本轮逐一检查 `research/` 顶层历史案例和视觉资产 README，而不是把所有旧文件强行改造成同一格式。判断结果分为两类：

- 多数旧案例虽然没有结构化 `data_status` 字段，但正文已经明确写出 Futu/公开历史来源、收盘后复核、不是实时行情和没有下单；例如 HD 与 QCOM 的旧式证据头保留为自然语言，不把缺少字段误报成实时证据；
- NFLX 三推顶部与 TSLA 卖出高潮后区间没有足够的自包含 source/provenance 说明。两份文件现在明确降为 `historical_context_only`、`data_status: incomplete`，并把截止时间、时区、图表范围和两年窗口写成未知/不可用。`incomplete` 表示证据链不完整，不是新的结果状态，也不增加任何回放分母。

全部 `research/assets/visual_recognition/*/README.md` 继续保留历史来源、最新可用 bar、时区、`chart_scope` 与 `daily_context_window` 的分工；局部图的 `partial` 不被两年 Daily 资产或配对复核文字覆盖。扫描没有发现活动的 `data_status: live_confirmed`、当前交易授权或把后验结果写回这两份历史案例的字段。

## 4. 验证与结论

- 16 个 pattern 入口均显式包含 `daily_context_window`、`timeframes_seen`、`chart_scope` 和 canonical `data_status` 边界；
- 日线候选仍严格保持 `contract_scope: daily_candidate`、`timeframes_seen: Daily`，低周期不能改写日线选股证据；
- `historical_close` 不再作为 `data_status`，非实时/来源说明没有被删除，只被放回正确字段；
- 两份 provenance 不完整的旧顶层案例现在显式标记 `data_status: incomplete`，不把缺失来源、时区或两年窗口默认为完整历史/实时证据；
- 回放仍只接受人工冻结合同，不从价格 CSV 生成视觉证据或自动补写两年覆盖；
- 本轮没有新增样本、成交或统计分母，`validated win-rate: not-computable`，结论保持 `no-new-positive`。

范围声明：`PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。本轮只修复文档字段映射、历史状态表达和回归守卫，不修改交易系统或回放 engine 有效语义。

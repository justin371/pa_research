# 全部视觉资产 README canonical provenance 覆盖审计（2026-08-29）

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

## 审计范围与硬边界

本轮只检查 PA Research checkout 中 11 个视觉资产目录的 README、配对历史复核/合同记录、索引和文档 validator。现有资产合计 105 张 PNG；本轮不下载或查询行情、不连接 Futu/OpenD、不查看新图、不运行回放、不增加样本、不修改 CSV、历史结果或 engine 有效语义。

本轮只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。资产 provenance、图表视觉判断、冻结合同、回放结果和交易授权继续分层保存。

## 11 个资产目录的覆盖结果

| 资产目录 | PNG | canonical Daily / review 边界 | 配对职责 |
| --- | ---: | --- | --- |
| `2026-08-24/round2_multisymbol` | 20 | `>=2y`；重要高低点/EMA 在配对冒烟复核中 complete | 无标签多标的 Daily/4H-like/1H/15m 背景 |
| `2026-08-24/round3_hl_drills` | 6 | `>=2y`（由配对 Daily 提供）；局部图 `partial` | H/L 局部计数练习，不在图上冻结标签 |
| `2026-08-24/round3_l1_l2_mar` | 4 | `>=2y`；15m 缺失，保留 `partial` | MAR 空头 L1/L2-like 对照 |
| `2026-08-24/round4_historical_practice` | 19 | `<2y`；重要高低点/EMA `partial` | 约一年 Daily 的边界练习 |
| `2026-08-24/round5_two_year_daily` | 13 | `>=2y`；配对复核 complete | 两年 Daily 与局部练习，不冻结合同 |
| `2026-08-24/tsla_public_mtf` | 4 | `>=2y`；配对冒烟复核 complete | TSLA Daily/4H-like/1H/15m 视觉验收 |
| `2026-08-26/hl_contract_batch` | 5 | `>=2y`；配对合同复核 complete | 首批人工 H/L 合同的 Daily 事前图 |
| `2026-08-26/hl_contract_batch2` | 3 | `>=2y`；配对合同复核 complete | 第二批人工 H/L 合同的 Daily 事前图 |
| `2026-08-27/hl_large_backtest` | 23 | `>=2y`；配对冻结合同复核 complete | 23 个窗口对应 37 条合同，不是一对一样本 |
| `2026-08-27/hl_next_backtest` | 5 | `>=2y`；配对冻结合同复核 complete | 5 条 H/L 合同的 Daily 事前图 |
| `2026-08-27/hl_next2_backtest` | 3 | `>=2y`；合同/边界复核 complete | 2 条冻结 H1 与 1 张 PHM H2-like 拒绝图 |
| **合计** | **105** | — | — |

## canonical provenance 结果

五个 2026-08-26/27 合同资产 README 原先只有自然语言来源和图像说明，现补齐独立的 canonical evidence header；11 个资产 README 均明确 `contract_scope: historical_context_only`，至少包括：

- `contract_scope: historical_context_only`、`data_status: historical`、`as_of_time`、`timezone`、`session_state` 和 `timeframes_seen: Daily`；
- `chart_scope: full`、逐资产 `daily_context_window: >=2y`、`major_high_low_review`、`ema20_50_200_review`；
- 多案例资产的 `direction: no_valid_direction`、`lineage_status: pending`、`internal_label: pending` 和 `h_l_ema_slope_gate: pending` 只表示聚合 README 不替代逐行合同；实际 long/short、H1/H2/L1/L2、EMA gate、lineage、事件和空间仍在配对 CSV/研究记录中；
- `research_state`、`trade_state`、`gate_result`、`order_branch`、`space_status` 和 `handoff_status` 不从图像资产推导交易授权；资产本身不冻结 `primary_pattern`、订单或结果。

11 个 README 的 evidence header 都是资产级聚合 provenance，不是逐案闭合研究合同。
因此 active `primary_pattern` 和 `lineage_id` 故意不写在这些 README 中；逐案完整记录或
冻结合同才负责填写主标签、内部标签和依赖 ID。资产目录、配对图或 README 缺少
`lineage_id`，不表示样本彼此独立，也不能把资产数量当作 pattern 样本数。

Round4 的短窗口仍明确为 `daily_context_window: <2y`，`major_high_low_review` 与 `ema20_50_200_review` 为 `partial`，EMA slope 和 H/L gate 为 `unknown/pending`。Round5、TSLA 和五个合同资产的两年背景/EMA 完整度只说明配对视觉 provenance 已记录，不把 H/L、三推、BOP 或 MTR 自动升级为已验证样本。

## 历史别名与索引修复

1. Round4 资产和复核报告的有效读取统一为 `daily_context_window: <2y`；`two_year_daily: pending` 只在明确的历史别名映射中保留。Round3 H/L 局部资产统一写 `daily_context_window: >=2y`，配对 Daily 的职责改在正文说明。旧的《视觉资产与事前证据边界审计》同步改为 canonical 表述。
2. 冒烟报告的旧汇总字段 `two_year_daily_context: pass` 改为按资产范围说明的 `daily_context_window_review: saved assets >=2y; public five unavailable`；前五张公开图仍保持 `unavailable`，不被保存资产覆盖。
3. 交接文档中的 `no_new_positive` 改为 canonical 结论 `no-new-positive`。批次级 `two_year_chart_coverage`、历史报告的 `round4_two_year_daily_complete_cases` 和显式 alias mapping 仍按各自用途保留，不冒充逐标的 provenance 字段。
4. 五个新增 header、Round4/Round5/TSLA 资产和本审计已加入 `docs/README.md`、`research/README.md`、`strategy/README.md`、`patterns/README.md`、`research/backtesting/README.md` 及 validator 必需文件/字段检查。

## 资产 README 与外部 manifest 入口复核

11 个视觉资产 README 均被至少一个 canonical index 实际直接链接；当前入口由
`research/README.md`、`research/backtesting/README.md` 和 `patterns/README.md`
共同承载，不要求每个 README 重复列出全部资产。外部
`external_visual_artifact_manifest_2026-08-29.json` 也有 canonical index 实际链接。
validator 现在会解析这些真实本地链接，拒绝新增后没有 canonical 入口的资产 README，
并拒绝外部视觉 manifest 失去 canonical 入口；这只是 provenance/可发现性守卫，不把
资产升级为 pattern、结果、统计样本或执行输入。

## 统计与安全结论

- 本轮只改善 README、配对入口、历史别名、索引、validator 和回归覆盖；没有新增图像、CSV 行、冻结合同、回放结果或统计分母。
- 视觉资产文件清单和 PNG 完整性仍由现有静态测试检查；资产数量、近似 pattern、H/L 标签或历史回放数字都不能推出胜率。
- `validated win-rate: not-computable` 保持；`no-new-positive` 保持。任何需要把视觉候选提升为生产规则、量化扫描或执行连接的工作都不在本轮范围内。

```text
asset_readme_count: 11
asset_png_count: 105
new_samples: 0
new_comparable_positive_samples: 0
no-new-positive: maintained
validated win-rate: not-computable
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

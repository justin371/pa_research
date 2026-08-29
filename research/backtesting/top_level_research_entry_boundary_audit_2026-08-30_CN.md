# 顶层 research 历史正向条件入口边界审计（2026-08-30）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

```text
inventory_scope: top_level_research_entry_boundary_audit_only
scan_scope: research_root_markdown_non_readme
case_like_selection: filename_and_header_heuristic
row_contract_source: linked_entry_file
row_contract_scope: per_entry
row_result_boundary: independent_replay_or_result_only
historical_alias_policy: display_only_until_mapped
```

## 1. 范围与发现

本轮只读取 PA Research checkout 的顶层 `research/*.md`、canonical schema、validator、回归
测试和 engine 接口；没有查询行情、查看新图、运行回放、增加样本、修改 CSV/engine，也没有
修改 Codex Trading、创建量化扫描器或连接 Execution Agent。本报告是历史入口边界审计，不是
候选名单、交易日志、结果报告或生产规则。

当前顶层 `research/` 有 171 个历史研究报告（不含 README）。其中 58 个文件已经出现明确的
`contract_scope`，其余 113 个主要是框架、矩阵、协议或旧式历史叙述；不能因为没有统一块就
把它们全部强行改造成逐案合同。

扫描出一个更窄且可复现的缺口：9 份 ticker-like 历史案例仍在自然语言状态中使用
`research_positive_conditional`，但没有自包含的 historical `contract_scope`、截止时点、
数据状态、状态轴和事前/事后边界。它们没有活动的结构化结果字段，也没有活动的授权状态；
问题是容易被读者把“条件性研究正向”误读成当前候选或已验证正例。

## 2. 统一的逐案边界

本轮为 9 个入口补的是最小历史边界，不是重新判图，也不是把标题中的 H1/H2/L1/H3-like
变成 canonical 主标签：

| 轴 | 本轮统一处理 |
| --- | --- |
| 来源与时效 | `data_source` 保留 Futu OpenD 历史 QFQ；`data_status: historical`；`session_state: historical_close`；原始查询时间不可得时明确写明 |
| 周期与左侧 | 记录实际涉及的 `Daily / 60m / 15m`；这些原始窗口不足两年，因此写 `chart_scope: partial`、`daily_context_window: <2y`、`major_high_low_review: partial`；EMA 未形成完整 canonical 复核时保持 `partial` 或 `unavailable` |
| 结构与方向 | 只登记有原文支持的 `parent_state`、`direction`、`state_transition`；`lineage_status: pending`；不激活 `primary_pattern` 或 `internal_label` |
| 订单与空间 | `order_branch: observation_only`、`actual_fill_or_open_skip: not_applicable`；止损、失效、入场前空间和 R/R 保持 `pending`/`unknown`；首障碍只保留视觉区域且注明未冻结 |
| 状态与交接 | `research_state: research_positive_conditional` 与 `trade_state`/`gate_result` 分开；除明确的日线首阻力否决外，不把历史研究升级为授权；`handoff_status: research_only` |
| 结果隔离 | 不增加 `outcome`、`fill_status`、`trade_result`、`realized_R`、`path_result`、`win_rate_eligible` 或真实交易日志字段；后续路径只能留在原文的事后说明 |

## 3. 补齐的 9 个历史入口

下列链接是逐案追溯入口。表中的形态词仍是历史显示语义；每个文件自身的 canonical boundary
才是范围、方向、订单和空间的读取依据。

| 入口 | 历史截止 | 方向 | 原文显示语义 | 首障碍/否决边界 |
| --- | --- | --- | --- | --- |
| [`AAPL 事件驱动 H1-like`](../aapl_bullish_h1_event_driven_a_2024-05-03_2024-05-09.md) | 2024-05-09 | `long` | 事件驱动 A、浅 B、H1-like | 184.98 附近视觉阻力；事件驱动，不是普通趋势正例 |
| [`AMZN H2-like 浅 B`](../amzn_bullish_h2_shallow_b_boundary_2024-12-09_2024-12-11.md) | 2024-12-11 | `long` | strong-looking-A、controlled-B、H2-like | 230.08 触发/磁铁区；空间未证实 |
| [`CRWD H2-like 深 B 后段稳定`](../crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md) | 2024-10-03 | `long` | strong-looking-A、deep-B-late-stabilization、H2-like | 75.11–75.54 视觉阻力区；空间不宽且事件背景仍需分开 |
| [`KLAC H1 强上涨腿`](../klac_h1_case_study_2025-10-14_2025-10-24.md) | 2025-10-23 | `long` | 强 A、浅回调、H1-like | 115.49–115.63 高点区；原文保留严格障碍分支 |
| [`KLAC 熊旗内 H3-like`](../klac_h3_bear_flag_case_2025-03-12_2025-03-28.md) | 2025-03-26 | `short` | 熊旗内三推、H3-like、空头恢复 | 66.6–65.1 视觉管理区；不冻结为 H3 结果 |
| [`NFLX 空头 ABC/L1-like`](../nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md) | 2025-03-28 | `short` | strong-looking-A、deep-but-controlled-B、L1-like | 88.75–90.10 视觉支撑区；首障碍到达不等于胜率结果 |
| [`NVDA H2 低周期条件候选`](../nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md) | 2024-09-24 | `long` | strong-looking-A、deep-but-late-controlled-B、H2 | 120.6–121.6 视觉阻力簇；日线空间边界保留 |
| [`TSLA ABC/H1-H2 复核`](../tsla_abc_h1_h2_case_study_2025-08-06_2025-08-22.md) | 2025-08-22 | `long` | H1/H2-like、支撑反应 | 340.55 主要阻力；日线直接追入为 `valid_no_trade` |
| [`TSM 空头 ABC/L1-like 缺口重订`](../tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md) | 2025-03-26 | `short` | strong-A、controlled-B、L1-like、gap-reprice | 167.99–165.05 视觉支撑簇；重订分支不等于原始 stop 成交 |

9 个文件现在都明确使用 `contract_scope: historical_context_only`。这只说明它们是历史研究
入口；不表示它们已形成 `daily_candidate`、冻结订单、可回放合同或正例统计分母。

## 4. 为什么不批量改写其余旧文件

以下情况继续按既有职责读取：

1. 框架、矩阵、比较表和协议文件没有单一标的的逐案合同，不能用一个全局
   `contract_scope` 假装覆盖每一行；
2. 只写 `valid_no_trade`、普通视觉边界或没有条件正向状态的旧案例，若正文已经说明历史
   来源、没有下单、不能用后续走势反推，则保留自然语言，不为格式而制造新的事实；
3. 已经在历史入口 inventory、候选/视觉一致性审计或 provenance 审计中有明确范围块的案例，
   不重复创建另一套状态轴；
4. `research_positive_conditional` 仍只是人工研究状态。它和 `trade_state`、`gate_result`、
   `handoff_status`、回放结果及真实交易日志始终分开。

## 5. 本轮修复与验证守卫

1. 为上述 9 个历史入口补充最小 evidence/status block，缺失的左侧、EMA、lineage、订单、
   止损和空间信息保持 `partial`、`unavailable`、`pending` 或 `unknown`；
2. 新增本审计报告，并加入七个 canonical index；
3. validator 固定 9 个入口清单，要求报告链接、historical boundary token 存在，并拒绝入口
   出现活动的结构化结果字段或授权状态；
4. 新增回归测试，固定 9 个入口、canonical 字段、结果隔离和仓库范围；
5. 没有新增图表样本、CSV 行、回放结果、成交、交易日志或统计分母。

验证后的统计结论仍是：

```text
no-new-positive
validated win-rate: not-computable
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

本审计解决的是“顶层历史正向条件入口不会被误读成当前/已验证交易合同”；如果以后要把其中
任何一个案例纳入回放，必须另立目标，在入场前重新封口图表 provenance、两年 Daily、重要高低点、
EMA、lineage、触发、结构止损、首障碍、空间、事件和结果合同。

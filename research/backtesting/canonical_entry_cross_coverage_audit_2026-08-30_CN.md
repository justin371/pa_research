# PA Research canonical 入口交叉覆盖审计（2026-08-30）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

```text
inventory_scope: canonical_entry_cross_coverage_audit_only
canonical_index_count: 7
report_link_resolution: real_local_markdown_and_machine_target
section_entry_policy: direct_canonical_for_active_sections
research_root_policy: non_self_markdown_reachable
asset_png_policy: README_manifest_exact_inventory
template_inventory: Markdown_authority_cards_and_section_readmes
```

## 1. 范围与读取口径

本轮只读取 PA Research checkout 的七个 canonical index、`requiredFiles`、文档
validator、回归测试、历史 inventory、视觉资产 README、机器输入和实现入口；不查询行情、
不看新图、不运行回放、不增加样本、不修改 CSV/engine。该报告只做入口、索引和守卫交叉核对，
不是候选名单、交易日志、回放结果或生产规则。

七个 canonical index 固定为：根 `README.md`、`docs/README.md`、`research/README.md`、
`research/backtesting/README.md`、`patterns/README.md`、`foundations/README.md` 和
`strategy/README.md`。真实本地 Markdown 链接按目标路径解析；代码块中的文件名、正文提及和
资产 README 内的 PNG 名称不被误当作 canonical index 链接。

## 2. 当前覆盖结果

| 类别 | 当前数量 | 覆盖/守卫结论 |
| --- | ---: | --- |
| canonical index | 7 | 全部存在，且保留 PA Research 与统计/执行边界 |
| `docs/` Markdown 活动入口/模板 | 7 | 7/7 由 canonical index 直接链接 |
| `foundations/**/README.md` | 9 | 9/9 由 canonical index 直接链接 |
| `patterns/**/README.md` | 17 | 17/17 由 canonical index 直接链接 |
| `strategy/**/*.md` | 7 | 7/7 由 canonical index 直接链接 |
| `research/backtesting/` 非 README 报告 | 76 | 76/76 由 canonical index 直接链接；validator 与测试均动态检查 |
| `$requiredFiles` 中的 research 报告 | 62 | 62/62 由 canonical index 直接链接；文件存在性和真实链接均检查 |
| 视觉资产 README | 11 | 11/11 由 canonical index 直接链接 |
| 视觉 PNG 资产 | 105 | 不逐图伪造 index 链接；11 个资产 README 精确列出 105/105，回归测试核对 manifest |
| backtesting CSV / JSON | 18 / 1 | 19/19 由 canonical index 直接链接；不等于结果或胜率分母 |
| backtesting 实现入口 | 3 | CLI、engine、artifact validator 均由回放 README 直接链接 |
| 顶层 `research/*.md`（不含 README） | 171 | 55 个 canonical 直接承载、116 个专题间接承载；171/171 被另一个 Markdown 非自引用链接 |

顶层 `research/README.md` 自身是 canonical index，因此根 `README.md` 没有入链是预期的根
入口例外，不构成孤立报告。其余 `docs/`、`foundations/`、`patterns/`、`strategy/` 活动
卡和模板没有发现未被直接索引的文件；研究根目录的历史文件则继续采用“精选 canonical 入口
+专题非自引用可达”的既有政策，避免把 171 个历史叙述全部伪装成当前合同。

供 validator/test 复核的当前计数如下：

```text
docs_markdown_entries: 7
foundations_readme_entries: 9
patterns_readme_entries: 17
strategy_markdown_entries: 7
backtesting_reports: 76
required_research_reports: 62
visual_asset_readmes: 11
png_assets: 105
backtesting_csv: 18
backtesting_json: 1
backtesting_executable_entries: 3
top_level_research_reports: 171
canonical_direct_top_level: 55
topical_only_top_level: 116
all_top_level_research_reachable: yes
```

## 3. 历史 inventory 与结果边界

`historical_case_entry_inventory_contract_audit_2026-08-29_CN.md` 的 35 个矩阵外入口、
`top_level_research_entry_boundary_audit_2026-08-30_CN.md` 的 9 个条件性历史入口，以及
视觉资产/回放 artifact inventory 均已进入 canonical index 和相应回归测试。入口文件的
历史 scope、显示别名、`parent_state`、方向、订单/空间和事前/事后边界仍按各自合同读取；
历史显示词不自动变成当前候选、`primary_pattern`、成交、回放结果或统计分母。

PNG 是资产 README 的逐目录 manifest 对象，而不是七个 index 的逐图对象。CSV/JSON 是冻结
合同、价格、intake 或外部 manifest 的机器输入/清单对象；它们由 index 链接和 schema/asset
测试守护，但不因此成为 `results.csv`、真实交易日志或已验证胜率。

## 4. 本轮发现与修复

发现一处真实的交叉守卫不对称：回归测试已经动态要求所有 backtesting 报告进入 canonical
index，但文档 validator 原来只检查 `$requiredFiles` 中的 research 报告，没有对新增的、
尚未列入 `$requiredFiles` 的 backtesting 报告执行同一动态检查；活动 section 模板也没有一个
统一的动态直接索引守卫。

已完成的最小修复：

1. validator 新增 `$backtestingReportPaths`，拒绝任何未被 canonical index 直接链接的
   backtesting 非 README 报告；
2. validator 新增 `$canonicalSectionEntryPaths`，对 `docs/` Markdown、
   `foundations/**/README.md`、`patterns/**/README.md` 和 `strategy/**/*.md` 做直接入口检查；
3. 回归测试同步检查两组动态路径、缺口信息和本审计报告的索引/requiredFiles 覆盖；
4. 没有新增样本、图表、成交、结果 artifact、交易日志、CSV 行或统计分母。

## 5. 结论与后续边界

当前交叉覆盖没有发现孤立的活动模板、backtesting 报告、required research 报告、视觉资产
README、机器输入或实现入口。PNG 的“非逐图 index 链接”是已记录且由 README manifest
守护的设计，不是遗漏。顶层历史 research 报告的 116 个专题入口也不是当前候选晋级路径。

验证后的统计结论保持：

```text
missing_backtesting_reports: 0
missing_section_entries: 0
missing_required_reports: 0
missing_asset_readmes: 0
missing_machine_artifacts: 0
missing_executable_entries: 0
png_manifest_gap: 0
no-new-positive
validated win-rate: not-computable
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

本报告只属于 PA Research。validator/测试的入口覆盖不会赋予行情访问、图表自动识别、交易
授权、Execution Agent 连接或胜率验证能力。

## 6. 2026-09-01 形态边界决策卡后的当前追加快照

上方 `7 / 9 / 17 / 7 / 41` 保留为审计建立时的历史快照。新增形态边界视觉决策卡并进入 canonical index 后，当前动态计数为：

```text
current_docs_markdown_entries: 9
current_foundations_readme_entries: 9
current_patterns_readme_entries: 17
current_strategy_markdown_entries: 7
current_section_entry_total: 42
current_backtesting_reports: 76
current_required_research_reports: 66
current_visual_asset_readmes: 13
current_png_assets: 133
current_top_level_research_reports: 175
current_missing_section_entries: 0
```

新增 docs 入口已由 `docs/README.md` 和 `research/README.md` 直接承载，活动 section entry 仍无缺口。本次没有新增图表、回放结果或交易分母，结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 7. 2026-09-01 形态边界 Holdout 后的当前追加快照

本段保留上方历史快照，只记录 12 张不重叠 holdout 图、24 份冻结复核、统计和审计进入当前 checkout 后的动态计数：

```text
current_docs_markdown_entries: 9
current_foundations_readme_entries: 9
current_patterns_readme_entries: 17
current_strategy_markdown_entries: 7
current_section_entry_total: 42
current_backtesting_reports: 76
current_required_research_reports: 67
current_visual_asset_readmes: 14
current_png_assets: 145
current_top_level_research_reports: 176
current_missing_section_entries: 0
```

Holdout 审计和资产 README 已由 canonical index 直接承载，活动 section、backtesting 报告、required report 和视觉资产入口仍无缺口。新增数据只测模型 reviewer 的视觉边界一致性，不建立人工专家真值，不产生交易结果或胜率分母；结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

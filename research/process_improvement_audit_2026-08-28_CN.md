# PA Research 流程改进审计（2026-08-28）

日期：2026-08-28<br>
范围：PA Research 候选筛选、完整图表审查和历史合同记录<br>
状态：`research_only / process-improvement / no-new-positive`

## 结论

本轮修复了记录层的主要缺口，但没有把 PA Research 变成扫描器，也没有新增或放宽形态规则。当前仍不能声称候选池覆盖了全部美股，也不能把描述性回放结果解释为已验证的胜率；`no-new-positive` 与 `win_rate: not-computable` 保持不变。

“没有立即入场候选”可以是严格闸门的正常结果；只有在候选池覆盖、数据来源和两年图表审查都清楚时，才能进一步判断这是市场状态还是筛选结果。

## 本轮独立完成的改进

### 1. 批次覆盖与发现池边界

新增[`每日候选批次与图表审查卡`](../docs/daily_candidate_review_card_CN.md)，要求每批记录：

- 市值范围、普通股过滤和 20 日平均成交额口径；
- 发现来源、数据截至时间、时区、session 和最后完整 K 线；
- `universe_coverage` 是 `complete`、`partial`、`discovery_only` 还是 `unknown`；
- 多头、空头、事件状态和两年图表的覆盖情况；
- 发现池数量与最终人工复核数量的区别。

这样不会再把一个发现页面或一小批人工图表误报成完整市场结果。

### 2. 两年左侧与强阻力记录

审查卡把两年 Daily 全图、近六个月局部图、重要高低点、支撑阻力角色转换、EMA20/50/200 和左侧首个独立障碍放入同一记录。特别要求在强 A 腿之后继续检查两年内主要阻力，避免把“强 A”误当作“空间充足”。

### 3. 形态、研究状态和交易状态分轴

审查卡固定记录 `research_state`、`trade_state` 和 `gate_result`，并分开列出：形态候选、条件候选、立即入场候选、有效不交易和观察样本。BOP 接受观察、回踩确认、事件/缺口和失败突破不能混成一个标签。

### 4. 证据缺失不再隐式通过

市值、流动性、事件、板块、大盘、两年背景、触发和空间缺失时必须写 `unknown` 或 `pending`。没有查到财报不等于 `none`，没有完整股票池不等于 `complete`。

### 5. 本地仓库清洁

新增最小 `.gitignore`，忽略 Python 缓存、测试缓存、虚拟环境和本地长任务状态；不忽略研究记录、合同 CSV 或图表资产。

## 验证证据

- `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\validate_pa_research_docs.ps1`：通过；239 个可提交 Markdown 文件、1175 个本地链接目标（忽略本地 `.codex/goals` 状态）；
- `py -3 -m unittest discover -s tests -v`：通过，18 个测试；
- `git diff --check`：通过；
- 本轮只修改 PA Research 工作树；没有修改 Codex Trading，没有创建扫描器，没有连接 Execution Agent。

## 仍待用户参与的事项

以下事项涉及规则冻结、研究设计或对外仓库状态，不在本轮擅自决定：

1. 是否把 `strong A`、`controlled B`、H1/H2/L1/L2 计数和首障碍几何进一步冻结成更具体的可重复定义；
2. 是否批准一个多空对称、事件分层、独立 lineage 和样本外的历史 cohort；
3. 是否接受本轮新增文档并 commit/push 到远端 `main`。

在这些决定完成前，PA Research 继续保持研究层 `provisional / not_ready`，不向 Codex Trading 交接。

# requiredFiles 与研究报告索引覆盖审计（2026-08-29）

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 审计范围

本轮只检查 PA Research 的 validator `$requiredFiles`、根目录与 section README 索引、以及 `research/backtesting/` 的报告入口。canonical 索引集合为根目录、`docs/README.md`、`research/README.md`、`research/backtesting/README.md`、`patterns/README.md`、`foundations/README.md` 和 `strategy/README.md`。研究报告按 `research/` 根目录或 `research/backtesting/` 直接子目录识别；视觉资产目录 README、CSV、JSON、脚本和 engine 不当作研究报告索引对象。

本轮只使用现有文件和只读文档检查：不下载或查询行情、不连接 Futu/OpenD、不看新图、不运行回放、不增加样本、不修改 CSV、历史结果或 engine 有效语义。`scope_boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。

## 事实核对

- validator 的 `$requiredFiles` 当前包含 89 个必需文件；排除 README 后，其中 62 个是 `research/` 或 `research/backtesting/` 直接子目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件，另 1 个是本 section README；
- 62 个 required research report paths 全部通过 canonical 索引中的真实本地 Markdown 链接覆盖；76 个 backtesting 报告文件也全部通过真实本地链接覆盖，没有孤立报告；
- `research/README.md` 是研究报告的综合重点入口，覆盖 requiredFiles 中的研究报告和本 section 的重点历史报告；`research/backtesting/README.md` 是回放/合同/版本边界的重点入口，不要求把全部历史审计报告逐条重复到每一个 section README；因此个别报告只在综合重点入口和相关专题入口出现，不属于遗漏；
- 已将本报告加入 `docs/README.md`、`research/README.md`、`research/backtesting/README.md`、`patterns/README.md`、`foundations/README.md` 和 `strategy/README.md`，并把覆盖规则加入文档 validator，后续新增 required research report 若未进入任一 canonical 索引会直接失败。

## 重复与断链边界

索引之间对同一审计报告的多入口是有意的导航冗余，不是重复样本或重复结果。`patterns/README.md` 中视觉复核卡和视觉识别验收记录的重复链接分别服务共同前置规则和历史资产入口，不改变文件身份。现有 validator 继续负责所有 Markdown 本地链接解析；本轮不改写这些有意的上下文链接。

## 验证与结论

- 本轮没有发现研究报告孤立、canonical 索引断链或 requiredFiles 漏列的事实问题；新增的是自动覆盖守卫和回归测试；
- 文档、索引与覆盖检查不产生行情、成交、回放结果或胜率分母；结论保持 `no-new-positive`，`validated win-rate: not-computable`；
- 本报告只属于 `PA Research only`，不修改 Codex Trading，不创建量化扫描器，不连接 Futu/OpenD，不连接 Execution Agent。

## 追加当前计数与真实链接复核（2026-08-29）

后续文档审计发现，本报告最初记录的 `83 / 56 / 69 / 68` 是前一时点快照；随着后续报告进入当前 checkout，实际基线已变为 `89` 个 requiredFiles、`62` 个 required research reports、`77` 个 backtesting Markdown 文件和 `76` 个 backtesting reports。上述事实计数已更新，研究结论没有变化。

同时，原覆盖守卫以报告文件名是否出现在索引文本中作为判断条件，存在“正文提到文件名但没有 Markdown 链接”的误判可能。现已改为解析 canonical 索引中的本地 Markdown 链接、按索引所在目录解析目标并与仓库内规范化路径比较；required research reports 与 tracked historical visual candidates 均使用该真实链接集合。回归测试同步采用同一语义。

当前复核仍确认没有孤立报告或 canonical 索引断链；本次只修正索引覆盖校验和事实快照，不增加样本、CSV、回放结果或 engine 有效语义。结论保持 `no-new-positive`、`validated win-rate: not-computable`；本文件仍只属于 `PA Research only`，不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

## 顶层 research 报告可达性复核（2026-08-29）

本次进一步盘点 `research/*.md`（不含 `research/README.md`）的完整入口图：当前 `research/` 顶层有 171 个历史研究报告，其中 55 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；171 个均至少被另一个 Markdown 文件实际链接，没有全局孤立报告。

因此，canonical index 是精选重点入口，不要求把 171 个历史文件逐条重复到每一个 README；但“精选”不等于“无入口”。validator 现在会解析全部仓库内 Markdown 的真实本地链接，并拒绝新增后没有任何其他 Markdown 入口的顶层 research 报告；回归测试采用相同的非自引用可达性语义。该策略不把历史报告升级为当前规则、交易日志、回放样本或统计证据。

## 2026-09-01 选股质量工作后的当前追加快照

本段追加当前 checkout 的真实 inventory；上方 2026-08-29 的 `89 / 62 / 171 / 55 / 116` 保留为当时快照。

- validator 的 `$requiredFiles` 当前包含 95 个必需文件，其中 64 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 173 个历史研究报告，其中 57 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 173 个顶层研究报告全部可从另一个 Markdown 文件到达；新增视觉协议、基线批次和报告不构成孤立入口。

这只是索引和可达性快照，不新增结果或胜率分母；结论仍为 `no-new-positive`、`validated win-rate: not-computable`、`PA Research only`、`no Codex Trading`、`no quantitative scanner`、`no Execution Agent`。

## 2026-09-01 形态覆盖候选集后的当前追加快照

本段继续保留上方历史计数，记录形态覆盖候选集加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 99 个必需文件，其中 65 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 174 个历史研究报告，其中 58 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 174 个顶层研究报告全部可从另一个 Markdown 文件到达；新审计、盲审资产和 review form 均有真实本地入口。

本次只增加标签隐藏、结果隐藏的候选图和守卫，不产生专家真值、交易结果或胜率分母；结论保持 `no-new-positive / validated win-rate: not-computable`。

## 2026-09-01 形态覆盖盲审与裁决后的当前追加快照

本段继续保留上方历史计数，记录盲审原始记录、盲裁决、机器统计与审计报告加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 103 个必需文件，其中 66 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 175 个历史研究报告，其中 59 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 175 个顶层研究报告全部可从另一个 Markdown 文件到达；新增 JSON 和审计报告均有真实本地入口。

本次只增加模型视觉校准证据，不产生人工专家真值、交易结果或胜率分母；结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 形态边界视觉决策卡后的当前追加快照

本段继续保留上方历史计数，记录决策卡及其 canonical 入口加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 104 个必需文件，其中 66 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 175 个历史研究报告，其中 59 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 175 个顶层研究报告全部可从另一个 Markdown 文件到达；新增 docs 决策卡已由 canonical index、validator 和活动视觉入口共同承载。

本次只收紧视觉分流和人工/模型裁决边界，不产生交易结果或胜率分母；结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 形态边界 Holdout 后的当前追加快照

本段继续保留上方历史计数，记录新 holdout 资产、冻结盲审、统计和审计报告加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 110 个必需文件，其中 67 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 176 个历史研究报告，其中 60 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 176 个顶层研究报告全部可从另一个 Markdown 文件到达；新增 holdout 审计、JSON 与资产入口没有形成孤立文件。

本次只测不重叠图上的模型视觉一致性，不产生人工专家真值、交易结果或胜率分母；结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 形态边界正反例对校准后的当前追加快照

本段继续保留上方历史计数，记录复用旧盲图的校准包、标准化复核、统计和审计报告加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 116 个必需文件，其中 68 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 177 个历史研究报告，其中 61 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 177 个顶层研究报告全部可从另一个 Markdown 文件到达；新增校准审计、JSON 和 packet 入口没有形成孤立文件。

本批是 reused calibration，不是新 holdout；它不产生人工专家真值、交易结果或胜率分母。结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 外部人工 H/L 盲标包后的当前追加快照

本段继续保留上方历史计数，记录专家标准、空白标注表、中性 manifest 和审计报告加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 121 个必需文件，其中 69 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 178 个历史研究报告，其中 62 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 178 个顶层研究报告全部可从另一个 Markdown 文件到达；新增专家 packet 和审计没有形成孤立文件。

本轮只准备 label/outcome/future-hidden 的空白专家包，没有人工标签、ground truth、准确率或交易分母。结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 专家标注回收 Validator 后的当前追加快照

本段继续保留上方历史计数，记录 schema、裁决/分母政策、只读 validator 和审计报告加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 125 个必需文件，其中 70 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 179 个历史研究报告，其中 63 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 179 个顶层研究报告全部可从另一个 Markdown 文件到达；新增 schema、policy、validator 和审计没有形成孤立文件。

测试输入只存在于临时目录，不进入仓库。真实专家标签、ground truth、准确率和交易分母仍为未形成状态。结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 外部人工安全交接就绪后的当前追加快照

本段继续保留上方历史计数，记录协调人 allowlist、交接审计和回归守卫加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 129 个必需文件，其中 71 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 180 个历史研究报告，其中 64 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 180 个顶层研究报告全部可从另一个 Markdown 文件到达；协调人清单和交接审计均有真实入口。

本轮没有真实 annotation 或人工结果。内部就绪状态不能进入准确率或交易分母，结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 双专家比较、裁决与无推断转录合同后的当前追加快照

本段继续保留上方历史计数，记录 pair schema、机器映射、只读 comparator 和审计报告加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 134 个必需文件，其中 72 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 181 个历史研究报告，其中 65 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 181 个顶层研究报告全部可从另一个 Markdown 文件到达；新增内部合同、脚本和审计均有真实入口。

本轮测试只使用临时合成记录；真实专家标签、ground truth、准确率和交易分母仍未形成。结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 2026-09-01 双专家裁决记录 Validator 后的当前追加快照

本段继续保留上方历史计数，记录只读 validator、合成测试和审计报告加入后的动态 inventory：

- validator 的 `$requiredFiles` 当前包含 136 个必需文件，其中 73 个是 `research/` 或 `research/backtesting/` 直接目录下的研究报告；
- 当前 `research/backtesting/` 有 77 个 Markdown 文件，其中 76 个是报告文件；
- 当前 `research/` 顶层有 182 个历史研究报告，其中 66 个由 7 个 canonical index 直接承载，另外 116 个由专题报告、Pattern 或 Strategy 入口承载；
- 182 个顶层研究报告全部可从另一个 Markdown 文件到达；新增 validator 和审计均有真实入口。

本轮没有真实 annotation/adjudication 或人工结果；跨字段校验不产生视觉 ground truth 或交易分母。结论保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

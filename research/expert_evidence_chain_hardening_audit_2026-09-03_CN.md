# 专家证据链加固审计（2026-09-03）

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only`

## 结论与范围

Sol Pro 对 25 个批准文本文件返回逐文件 EOF 和 SHA 清单，SHA 全部与当时批准版本匹配。主代理另用临时合成数据复现并校验以下问题；前期专项报告本身不是全仓签字。此后已经完成机器可读全仓清单、全部 161 张受版本管理 PNG 的逐张原生图像审查，以及本报告后续各阶段所列代码、数据和文档边界复核。最终修复版本仍须由 Sol Pro 做一次独立接受性复核后，才能把整项工作标记完成。

`PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。没有真实专家标注、预测、成交或新的结果样本；`completed_trade_denominator: 0 / validated win-rate: not-computable / conclusion: no-new-positive`。

## 已实施的控制

| 问题 | 修复与验收边界 |
| --- | --- |
| 替换 manifest 后重算自报 SHA，三层 validator 仍接受 | 单专家入口将解析的同一批字节绑定 canonical SHA；替代包即使自洽也不能进入 comparator/adjudication |
| 仅自报预测已在揭盲前冻结即可增加准确率分母 | v1 不支持独立冻结证明，因此失效安全地排除该预测；summary 的 eligible 来自重新计算，而非输入布尔值 |
| 替换 PNG 并同步修改 inventory 可以导出 | chart inventory 自身的 SHA 独立固定；固定 5 个文档字节，复制后验证全部 21 个目标文件 |
| 预填表或改写 criteria 未被导出器发现 | 当前空白表及原文哈希冻结，任何内容修改均拒绝，不修改历史冻结资产 |
| 不同 ID/文件名重复同一底层截止图 | 在渲染前拒绝同一标准化 symbol/cutoff，复制 CSV 或改名不能绕过；同一 symbol 不同日期仍允许 |
| 完整性导出仍自报可交接，忽略当前研究门槛 | 改为 `integrity_verified_handoff_blocked`，显式 `human_handoff_ready=false`、`accuracy_study_ready=false`；列出事前承诺和跨图未来泄露两个独立 blocker，exit 0 仅证明导出完整性 |
| validator/comparator/adjudicator 在一次调用中重复打开 canonical manifest 或专家记录 | 三个入口均先读取不可变字节快照，再把同一对象贯穿 canonical SHA、schema、逐项比较与裁决；路径在处理中被替换也不能形成“校验旧字节、计算新字节”的混合证据 |

合成反例不证明真实包已被篡改、真实样本已经重复或准确率受到实际污染。导出完整性通过不等于形态正确、专家独立或已具备准确率证据。

## 仍未完成的门槛

1. 独立预测文件及揭盲前外部承诺的合同和校验器仍待验收。文件内自报时间、单独 SHA 或事后 Git 提交都不能证明过去已经冻结。当前分母固定为 0，不补写真实预测。
2. 最终修复版本的 Sol Pro 接受性复核仍待完成；此前 Pro 结论不能自动覆盖本轮新增的单快照证据链修复和完整 161 张视觉清单。
3. 同一 symbol 不同 cutoff 的相关性、有效样本量及泛化统计需要单独研究设计，不能因为文件不同就宣称相互独立。进一步来源核验已确认冻结包有跨图未来暴露风险；原包不能仅凭补齐事前承诺就用于无污染准确率研究。
4. 两位真正独立的外部人工专家尚未开始；模型复核不冒充人工专家。

当前交接状态以[协调清单](calibration/external_human_hl_v1/coordinator_handoff_checklist_CN.md)和[裁决/分母政策](calibration/external_human_hl_v1/adjudication_and_denominator_policy_CN.md)为准。2026-09-01 的就绪审计保留为历史记录，不覆盖本次更正。

## 验证

回归位于 `tests/test_pa_research_expert_evidence_chain.py`、`tests/test_pa_research_hl_pair_adjudication_validator.py` 和 `tests/test_pa_research_blind_daily_batch.py`；fixture 全为临时合成记录。针对性 51 项、渲染 7 项通过；最终全套 479 项测试通过（257.703 秒），文档校验通过 338 篇 Markdown、2304 个链接。最初全套的 5 处失败涉及旧冻结断言及动态索引快照，修正后重新运行全套通过；未删除失败测试或修改冻结样本。

## 原生图片与数据读取验收

2026-09-03，Sol Pro 在 PA 专用六文件只读范围内报告完成 `workspace_info`、四份文本/数据的 EOF 读取以及 `read_image` 原生像素查看。主代理重新核对六个本地 SHA 全部匹配，并独立打开 `EH1-001.png`、`EH1-002.png`：前者局部呈阶梯式上行，后者有明显中段急跌后修复；504 根全景、120 根局部及 EMA20 蓝色、EMA50 橙色、EMA200 紫色等描述一致。验收以 Pro 可见报告、哈希/尺寸核对和独立看图一致性为证据，不把报告中的自述称为另行审计过的原始工具载荷。

冻结图仍有以下限制，不能因读取成功而忽略：

- 上方成交量刻度被下方价格面板部分挤压。当前渲染器已为未来新图保留间距；本轮复跑布局测试通过，冻结图不重绘。
- 标题的 504 根日线支持约两年的背景，但隐藏日历日期后，像素本身不能证明两个完整日历年或数据没有遗漏；未来数据边界仍须源记录证明。
- 未见显式股票代码、日历日期、形态标签或结果标注；价格/成交量尺度和历史路径仍可能被熟悉标的的人识别，身份隐藏不是完全匿名。
- `prices.example.csv` 是五行合成 OHLCV 示例，不是两张图的数据源。此轮不是新盲测、真实人工专家标注、形态准确率或交易胜率验收。

该六文件阶段的图片覆盖为 161 张中的 2 张显示/读取验收，当时其余 159 张仍待 Pro 查看；不扩大为完整语义审查。临时连接在返回后关闭，没有修改冻结 PNG、CSV、JSON，也没有增加执行或写入权限。

## 跨图未来暴露与导出状态更正

主代理逐张查看剩余 14 张专家图时发现重叠走势，随后只在本地核对隔离来源映射、来源 manifest 和日线 CSV：两张图来自同一标的和同一价格文件，截止日相差 29 根实际日线。较晚截止图向同一审核者暴露较早截止之后的走势，因此“各图只画自身截止前的数据”不足以证明整包盲态。具体身份/日期映射保留在 Git 忽略的内部证据中，不加入专家可见材料。

这是已确认的样本依赖和未来暴露风险，不是声称真实专家已被污染——外部专家尚未开始。本聊天也不是新盲测，未创建任何真实标签或预测。不同哈希只能证明字节不同，不能证明统计独立；改顺序、改编号或分开文件夹不足以解除风险。

独立复现还发现导出器在当前协调清单已阻止准确率交接的情况下仍返回 `ready_for_isolated_human_handoff`。新增两项测试先失败，修正后通过；现在复制原 21 个冻结文件只用于内部完整性检查，JSON 显式报告交接受阻。协调清单与分母政策加入独立的跨图未来隔离门槛；冻结 v1 图、README、manifest、hash inventory 和空白表均不改写。后续如需真正盲测，必须另行设计并验收不泄露未来的新包及分组协议。

## 剩余 14 张专家图的 Pro 复核结果

Sol Pro 在独立的 19 文件只读范围内完成 `EH1-003` 至 `EH1-016` 的原生像素查看，以及上下文、README、criteria、manifest、hash inventory 的 EOF 读取。主代理核对全部 19 个 SHA、5 份文本的行数和 14 张图的尺寸/字节均一致，并将逐图观察与此前本地看图记录对照：上下文面板、均线、主要价格路径、异常大 K 与图窗重叠等定性证据相符。证据为可见 Pro 报告加本地哈希/元数据和原生图像核对，不冒称另行审计过原始 MCP 载荷；也不把近似读数或“多年式”等措辞当作精确价格、日历跨度或识别准确率证明。

Pro 未获得内部来源映射，仍独立指出两张图的约 `156→123→140` 路径逐段接近，推测相差约 30 根 K。主代理的来源核验将其落实为同源不同 cutoff、相差 29 根实际日线。Pro 建议的依赖分组可以处理相关性，但仅分组不能消除同一审核者已经看到另一图未来的问题，因此本 repo 同时保留跨图盲态门槛，不能只做统计去重就恢复交接。

其余审查结果：14 张图可读、图例颜色与 EMA 可见，未发现新增的右端 K 线裁切或显式答案标签泄露；多张图存在可见跳空/异常大 K，只能记录价格结构，不能据此猜财报或新闻原因。旧图横轴拥挤、价格指纹、504 根 K 不等于日历两年证明等限制继续保留，冻结图不重绘。

本轮最终全套 **481 项测试通过（179.893 秒）**，文档校验 **338 篇 Markdown / 2305 个链接通过**，`git diff --check` 通过。首次全套仅因新增链接后的旧索引计数失败，更新当前快照后重跑全套通过，旧历史快照保留。临时连接已关闭，没有向专家发送包或产生新标签。

覆盖结论限于专家包 16 张图的显示/证据可用性审查；全仓穷尽审查未完成，仍为 `no-new-positive / validated win-rate: not-computable`。

## 候选图主代理复核与渲染器加固

主代理继续逐张打开 `MC2-001` 至 `MC2-016` 的原生 PNG，核对全景/局部、EMA、左右关键结构、可见跳空、日期遮挡和重复标的图窗。图像可读，但旧全景日期轴拥挤、同一标的不同 cutoff 暴露另一图后续走势的限制仍在。本轮 PA 专用只读连接未完成授权，Sol Pro 没有收到新问题，也没有读取本批文件；临时连接已关闭。这 16 张仅记主代理历史可用性审查，不能增加 Pro 覆盖数或充当新盲测标签。

主代理用临时合成 fixture 独立复现后修复：

- 旧渲染器直接覆盖同名 PNG，README 的重现命令又指向冻结目录。现在默认且始终禁止覆盖，先编码到内存，再独占创建目标文件；目标在预检后才出现也不会覆盖。重现命令改为非冻结新目录，不承诺新布局与旧 PNG 字节相同。
- 旧流程处理完一张才验证下一张，后续无效 ID、文件名或截止日会留下已输出前缀。现在整批来源、截止边界及目标都预检通过后才开始渲染，文件名重复检查忽略大小写。运行期 I/O 故障仍可能留下此前完成的新图，失败批次不被视为完整交付。
- 窗口参数用 `int()` 强转，布尔、小数、字符串和非正数缺少严格校验；直接调用的负索引可选择错误日期。现在窗口/最少背景/隐藏未来根数要求正整数，局部窗口不得大于全景窗口，截止索引必须是有效整数范围。
- 本地按源 CSV 的 symbol/cutoff 重算 504 根显示窗口：7/16 的首末日期跨度少于两个日历年 1–2 天。候选 README 改为逐样本日期表与保守整批状态；不把交易日根数等同日历跨度，也不据此断言源数据缺失交易日。旧测试名的“两年”改为其实际验证的“声明根数”，另加日期表对照回归。

初次 12 项渲染测试得到 32 个失败断言，修复后包含并发目标与编码故障场景的 14 项通过；候选集 7 项、布局 1 项通过。测试不重绘冻结图，不修改价格 CSV/manifest/专家答案，不产生真实交易或准确率分母。Pro 图像覆盖仍为 16/161，其余 145 张及未覆盖文本/数据仍待完成；`no-new-positive / validated win-rate: not-computable` 不变。

本次最终全套 **489 项测试通过（164.275 秒）**，文档检查 **338 篇 Markdown / 2305 个链接通过**，`git diff --check` 通过。所有受版本管理的 PNG/CSV/JSON 均无差异；未提交或推送，完整 Pro 审查未验收。

## Windows 文件名写入边界

继续本地审查时，以临时合成文件复现：`frozen.png:alternate.png` 通过旧的 basename/suffix 检查，并在已有合成文件上创建 NTFS 附加数据流；主数据流字节保持不变，普通 `*.png` 目录计数也不增加。因此主文件 SHA 和“目标不存在”检查不足以阻止这种附加写入。真实冻结图没有被修改。

已在批量和直接渲染入口统一限制为安全的 ASCII 中性 PNG 文件名，并拒绝冒号、路径分隔符、Windows 设备名及特殊字符。17 种反例只在临时 fixture 中检查；支持的中性命名、版本点号和正常非保留名保持可用。批量入口测试先出现 14 个失败断言，直接入口再复现 1 项失败，修复后 3 项新测试和 14 项原渲染测试通过；不读取账户、不产生选股或执行行为。

本次修复仍由主代理独立复现和验收，不冒称 Pro 复核：PA 临时连接的公开 OAuth 发现接口正常，但 ChatGPT 授权仍未建立，没有配对窗口或 Pro 新回复。连接已关闭，后续须恢复授权后再审查当前文件版本。CSV/JSON 的并行本地预审单独记账，也不增加 Pro EOF 或看图覆盖。

Windows 修复后的全套 **492 项测试通过（163.993 秒）**；文档检查 **338 篇 Markdown / 2305 个链接通过**，差异检查通过。新增测试纳入全仓清单后共 619 个文件路径，Pro 尚未覆盖的范围不因此缩减；未提交或推送。

## 数据预审验收与历史盲态表述更正

两个只读 Luna Max 预审覆盖指定的 17 份 CSV 和 15 份 JSON。主代理逐文件核对 SHA、CSV 行/列数、JSON 解析和行数，发现一处预审报告的哈希漏抄并在私有验收记录更正；源文件未变。子任务报告保留原样，不将其当作主代理重新执行全部检查，更不计作 Sol Pro EOF 或图像审查。

进一步核对确认，MC2 与先前 Batch 1 有 7 组相同 symbol/cutoff/price_file。旧候选审计和裁决审计又分别误称所有图均满两年、股票代码隐藏及 strict_eligible 已成立。现在两份审计记录实际日期跨度、7 组重用映射和可见身份，并明确旧 clean/strict_eligible 只是历史自述，不能证明事前盲态或独立准确率。PNG、CSV、原始评审 JSON 和旧统计字节均不重写。两项新增回归先失败、修正后候选/裁决 15 项测试通过。

三推来源标签的 `3/4` 在现有测试中可按四个 THREE_PUSH_like 来源候选重算，属于候选假设对照，不是全部 family 的总体比例，也不是准确率；文档补充这一分母定义。两份历史合同虽仅有 8/4 根后续数据，但短窗口本身不是引擎 bug：当前只读诊断中 CRWD 被 EMA gate 拒绝，ADBE 在数据结束前已达到目标；未能真实完成的持仓仍由 incomplete-horizon 规则排除。这次诊断不构成新增独立胜率证据。

CSV 字段顺序和合同日期顺序未构成当前读取器缺陷：价格按列名读取并按标的/日期排序，合同逐项独立回放，因此不为外观整齐重排冻结文件。外部 PNG 实物验证、完整 JSON Schema 实例验证以及全仓语义和 Pro 审查仍未包含在这份有限预审中。结论保持 `no-new-positive / validated win-rate: not-computable`。

追加更正后全套 **494 项测试通过（149.723 秒）**；619 个文件路径与覆盖清单一致，PNG/CSV/JSON 无版本差异。完整 Pro 审查和修复后版本验收仍未完成，未提交或推送。

## 全仓机器清单、161 张图与单快照证据链收尾（2026-09-04）

当前 checkout 清单为 614 个已跟踪路径和 5 个本轮待提交路径，共 619 个文件：338 Markdown、81 Python、161 PNG、18 CSV、17 JSON、2 TXT、1 PowerShell 和 1 `.gitignore`。主代理完成以下不替代语义判断的机械检查：全部文本严格 UTF-8 解码，81 个 Python 文件 AST 解析，17 个 JSON 解析，18 个 CSV 解析及行宽一致性，161 个 PNG 由 Pillow 解码，4 份 JSON Schema 通过 metaschema 检查；没有发现全文件 SHA 重复组，也没有发现 production broker、账户、订单、Execution Agent 或自动扫描器导入。

全部 161 张受版本管理 PNG 已使用原生图像查看逐张检查，不把文件可解码等同形态准确。Daily 长背景图可见 EMA20/50/200、主要高低点及左右结构；短周期或数据不可用处按各自资产说明保留。旧 `hl_large_backtest`、MC2、BQ1 和部分 EH1 冻结图存在标题、上方日期轴或面板边界拥挤/裁切，K 线、EMA 与成交量主体仍可读。该缺陷属于已冻结历史证据的显示限制，不回写 PNG。主代理另在系统临时目录用当前 renderer 和 MC2 manifest 原子生成 16/16 张非冻结复现图，并原生查看旧图问题较明显的 `MC2-014`、`MC2-016`；标题、日期轴、面板间距和本地说明均完整，确认当前新渲染链不再复现旧布局缺陷。临时复现不进入仓库，不改变冻结哈希或研究分母。

进一步合成回归先稳定复现三处 TOCTOU：单专家 validator 在解析后重读被替换 manifest 来报告哈希；comparator 在校验后重读被替换专家记录参与比较；pair adjudicator 对同一输入多次打开。修复后 canonical manifest、两份专家记录和裁决输入均各读取一次并以不可变快照贯穿调用。三组反例现在失效安全，相关 56 项测试通过；不创建真实专家答案、预测、形态标签或交易结果。

当前语义结论仍为：

```text
conclusion: no-new-positive
overall_accuracy: not-computable
validated win-rate: not-computable
completed_trade_denominator: 0
human_handoff_ready: false
accuracy_study_ready: false
```

全仓本地审查覆盖已收齐，但最终 Sol Pro 接受性复核、最终全套测试和提交/推送仍在本段记录时待完成；在这些门槛完成前不宣称整个 goal 已结束。

## Sol Pro 首轮全仓复核拒绝与 0.3.13 修复（2026-09-04）

Sol Pro 对当时发布的 43/43 个只读路径完成 EOF 审查后给出 `REJECT`，并提供两个可落地反例。主代理先在临时合成输入上将两项反例稳定复现为失败测试，再修改实现：

1. `internal_label=pending`，以及 `primary_pattern=H3_L3` 却使用 `internal_label=none` 的冻结合同，曾可通过校验并进入完成交易分母。0.3.13 现在拒绝冻结合同中的 `pending`，要求 `H3_L3` 只能配对 `H3` 或 `L3`，并在合同及结果资格重算两层把 `pending` 保持为不可计数状态。
2. 回放引擎和启用来源绑定的盲图渲染器，曾在执行代码加载后再从可变路径计算来源哈希。0.3.13 在运行前读取稳定源码字节并记录文件身份，在计算后及原子发布前再次核对身份、大小、时间戳与字节；运行期间源码被替换时失效安全，且不发布结果。

三项新增回归（合同分母、引擎源码切换、渲染器源码切换）修复前均失败，修复后通过；四个相关定向模块随后全部通过。首轮 `REJECT` 不能作为最终接受证据，修复后的当前字节仍须重新提交 Sol Pro 审查。

这些修复没有新增真实样本、形态判断、预测或成交。研究边界继续固定为：

```text
conclusion: no-new-positive
overall_accuracy: not-computable
validated win-rate: not-computable
completed_trade_denominator: 0
```

修复后的第二次全套运行 **523 项测试全部通过（151.973 秒）**；文档验证 **338 篇 Markdown / 2305 个链接通过**，`git diff --check` 通过。第一次全套的唯一失败是文档验证器仍要求旧活动版本 `0.3.12`，该版本漂移已同步为 `0.3.13`，孤立回归和第二次全套均通过。最终提交仍以修复后 Sol Pro 返回 `ACCEPT` 为门槛。

## Sol Pro 当前字节二次拒绝与 0.3.14 修复（2026-09-04）

Sol Pro 使用新只读连接 `asdk_app_6a9a8826a68c8191ad3dabb24d80e3ed`，先精确匹配 context、engine 和 renderer 三项 SHA，再重新读取 43/43 个批准路径到 EOF。它确认 P1 分母污染已闭合，但再次给出 `REJECT`：0.3.13 的源码快照仍发生在 Python 已经加载和编译模块之后，因此“内存执行 A、入口调用前路径恢复为 B”仍可把 B 的路径哈希错记为 A 的执行证明；同时旧的 `stat/read_bytes/stat` 不能保证字节与身份来自同一打开文件。

主代理复现该 A→B 反例后引入 0.3.14：

1. 新增独立[`单句柄源码绑定器`](../pa_source_binding.py)，以一次 `os.open()` 后的同一 fd `fstat/read/fstat` 固定字节与文件身份；
2. [`回放 CLI`](../scripts/pa_research_backtest.py)和[`盲图 source-bound CLI`](../scripts/render_pa_blind_daily_batch_bound.py)从这组不可变字节 `compile/exec` engine/renderer，并注入不可由普通 import 获得的绑定；
3. engine 和要求 `source_binding_required=true` 的 renderer 只接受该绑定，计算后和原子发布前继续复核当前路径；普通 import 后直接调用发布入口、A 已加载后路径变成 B、以及运行中替换源码均拒绝发布；
4. 新回归覆盖单描述符调用链、普通 import 失效安全、engine A→B 与 renderer A→B；官方渲染命令、活动版本、manifest 源码哈希、canonical 索引和 validator 同步更新。

Sol Pro 指出的 `pro_review_context` 中 `520-test` 遗留数字也已更正。该修复没有改变冻结合同、图片、CSV、真实样本或统计分母。0.3.14 最终全套运行 **527 项测试全部通过（182.639 秒）**；文档验证 **338 篇 Markdown / 2313 个链接通过**，`git diff --check`、renderer/manifest 哈希绑定和无 PNG/CSV 改动检查均通过。第三次 Sol Pro 当前字节验收仍是 commit/push 前门槛。研究边界继续是：

```text
conclusion: no-new-positive
overall_accuracy: not-computable
validated win-rate: not-computable
completed_trade_denominator: 0
```

## Sol Pro 当前字节三次拒绝与 0.3.15 修复（2026-09-04）

Sol Pro 使用新的只读连接 `asdk_app_6a9a95b1f2048191989cabb050bc8d21`，精确匹配 workspace 与四项源码/context SHA，并把 49/49 个批准路径全部读到 EOF。它再次确认 P1 冻结标签与完成分母为 `PASS`，同时发现两项 P2：

1. 0.3.14 的 `SourceSnapshot` 自带 token，公开 `read_source_snapshot()` 也能生成同类对象；普通 import 的模块可以把该对象注入全局，或移植另一 bound module 的快照，使“执行 A、路径/声明 B”的发布 provenance 仍可能被接受；
2. [`selection_quality_blind_batch1` 重现说明](assets/visual_recognition/2026-09-01/selection_quality_blind_batch1/README.md)把 `--output-dir` 指回已经存在的冻结资产目录，与 renderer 的“目标目录必须不存在”合同冲突，因此命令必然失败。

主代理复现后引入 0.3.15：

1. [`单句柄源码绑定器`](../pa_source_binding.py)不再向模块全局注入可复制的发布凭证；`load_source_module()` 只在私有 registry 中把快照绑定到它创建的精确 module object 与 `globals()` identity；
2. engine 与 renderer 通过自身 module object/namespace 从 registry 取回绑定。普通 import 即使注入公开 reader 返回的 B 快照也会拒绝，final artifact/chart directory 不存在；
3. 新增 engine 与 renderer 的 snapshot-transplant A→B 回归，并保留同一 fd、入口前路径替换、运行中源码替换和 atomic no-replace 回归；
4. Batch 1 重现命令改为尚不存在的 `.codex/artifacts` 目标，并明确只重现历史窗口、不覆盖冻结图、不承诺 PNG 字节相同；
5. 当前研究引擎版本、schema、核心索引、manifest renderer SHA 与文档 validator 同步为 0.3.15。

三个相关定向模块共 **52 项测试全部通过**；0.3.15 最终全套运行 **530 项测试全部通过（255.171 秒）**；文档验证 **338 篇 Markdown / 2315 个链接通过**。本次修复没有修改 PNG/CSV、真实样本、形态判断或统计分母。修复后的新字节原计划再次提交 Sol Pro；用户随后明确取消该额外复审并要求立即 commit/push，因此本次不宣称取得最终 Pro `ACCEPT`，提交依据为上述本地验证与用户的明确门槛变更。研究边界保持：

```text
conclusion: no-new-positive
overall_accuracy: not-computable
validated win-rate: not-computable
completed_trade_denominator: 0
```

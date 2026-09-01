# PA Research authority 与隔离边界审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 当前 README、docs、research、foundations、patterns、strategy、脚本、测试和依赖声明<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计目的

本轮只检查 PA Research 内部的 authority 表述、索引入口和隔离边界，不读取或修改 Codex Trading 工作树，不下载行情、不增加样本、不重跑回放，也不改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。

当前 authority 仍由仓库自己的：

- [`PA Research 日线选股规则 v0.1`](../docs/pa_research_daily_selection_rules_v0_1_CN.md)；
- [`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)；
- `research/` 下与当前回放版本相符的审计和 README。

## 二、扫描结果

- 全仓库 Markdown 没有外部 `V1.x` 生产版本标记；新增边界测试防止外部生产版本号重新进入 PA Research 文案；
- Codex Trading 的出现位置均有明确限定：只读历史图表/OHLC 参考、研究交接规范，或“不修改/不导入其规则”的禁止性声明；没有发现把 Codex Trading 规则写成 PA Research 当前 authority 的表述；
- Futu/OpenD 的出现位置是历史数据来源、可选数据来源或“未连接”的边界说明；回放 executable code 没有 Futu/OpenD、broker、网络、账户或订单导入；
- `量化扫描器`、`scanner` 和 `Execution Agent` 的出现位置是能力排除、交接边界或 schema/validator 检查，不是已实现的模块或运行时依赖；
- 文档校验继续拒绝不可移植的 Codex Trading checkout 路径，并确认根 README、docs README、research README 和回放 README 的索引可达；
- 未发现把参考材料写成当前 production authority 的既有断言；但三份直接从 Strategy 索引进入的框架/参考页以及基础层索引缺少自包含的状态、当前结论和执行隔离声明，已在本轮补齐；不修改现有历史案例引用，合法的历史来源和禁止性边界全部保留。

## 三、独立 Strategy 页面与基础层索引自描述边界复核

以下页面此前依赖上级索引才能看出其研究范围，单独打开时无法直接看到统一的状态、统计结论和生产/执行隔离：

- strategy/00_trading_framework.md：研究流程框架；
- strategy/meta_multiple_edge.md：位置汇聚框架，不是独立触发器；
- strategy/probability_principles_pages_1_7.md：用户提供的外部教育性参考，source_version 仍为 not_provided，不进入 PA Research 胜率或回测基准。
- foundations/README.md：8 个共用基础层入口。

四个入口现在都明确 research_only / provisional / not_ready、当前回放引擎 0.3.9、no-new-positive、validated win-rate: not-computable 和不连接量化扫描器/Execution Agent；概率页另外保留 external_reference 与 evidence_status: external_heuristic_not_validated。这只是可发现性与边界修复，不是新规则、新样本或新统计结论。

## 四、索引数量、版本与结论复核

当前 checkout 与七个 canonical 索引的数量/版本声明一致：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 11 个资产 README 和 105 张 PNG；
- research/ 顶层有 171 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 七个 canonical 索引均指向当前 PA Research 规则/合同，并保留回放引擎 0.3.9、no-new-positive、validated win-rate: not-computable 和研究/生产执行隔离；
- 文档 validator 已检查 311 个 Markdown 文件、2164 个 Markdown 链接；其中本地链接、动态 machine-artifact coverage 和核心边界检查全部通过。

这些数量是当前 checkout 快照，不把历史批次的 37 条、24 个、12 只、13 份等报告内数字改写成当前总量；历史回放、视觉资产、冻结合同和真实交易日志仍按各自 provenance 分层。

## 五、固化内容

- 为三个独立 Strategy 页面补充统一的研究状态、当前结论和执行隔离声明，并由 validator/回归测试守护；
- 将 foundations/README.md 纳入核心边界 validator/test，并补充同一组状态、结论和执行隔离声明；

- 在 `tests/test_pa_research_scope_boundary.py` 增加 PA Research Markdown 的外部 `V1.x` 版本标记防回归检查；
- 在 `research/README.md` 增加本审计入口；
- 不修改任何市场数据、合同 CSV、回放结果、pattern 定义或 Codex Trading 文件。

## 六、验证结果

```text
external V1.x authority-marker scan: 0 matches
full unittest suite: 328 passed
document validation: passed
compileall and git diff --check: passed
```

当前结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

## 七、当前 inventory 追加快照（2026-09-01）

本段只追加当前 checkout 的动态计数，不改写上方 2026-08-29 的历史快照，也不形成新样本或统计证据：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 12 个资产 README 和 117 张 PNG；
- research/ 顶层有 173 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 315 个 Markdown 文件、2193 个 Markdown 链接。

新增数量来自 2026-09-01 的视觉校准协议、选股质量审计、首次视觉答案和 12 张 outcome-hidden 图，不改变 `no-new-positive`、`validated win-rate: not-computable`、`PA Research only`、`no Codex Trading`、`no quantitative scanner`、`no Execution Agent`。

## 八、形态覆盖候选集追加快照（2026-09-01）

本段继续保留上方历史快照，只记录形态覆盖候选集加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 13 个资产 README 和 133 张 PNG；
- research/ 顶层有 174 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 318 个 Markdown 文件、2216 个 Markdown 链接。

新增的 16 张图只构成标签隐藏、结果隐藏的形态覆盖候选集；专家真值、识别准确率和交易结果仍未形成，结论继续保持 `no-new-positive / validated win-rate: not-computable`。

## 九、形态覆盖盲审与裁决追加快照（2026-09-01）

本段继续保留上方历史快照，只记录独立模型盲审、裁决和机器可读统计加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 13 个资产 README 和 133 张 PNG；
- research/ 顶层有 175 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 319 个 Markdown 文件、2224 个 Markdown 链接。

新增记录只验证盲审顺序、模型间一致率和形态边界混淆；它不是人工专家真值，不产生交易结果或胜率分母。结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十、形态边界视觉决策卡追加快照（2026-09-01）

本段继续保留上方历史快照，只记录决策卡、authority 入口和回归守卫加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 13 个资产 README 和 133 张 PNG；
- research/ 顶层有 175 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 320 个 Markdown 文件、2235 个 Markdown 链接。

新增决策卡只收紧 BOP、区间/第三推、B 腿、lineage 与普通 H/L 的判断顺序，并把独立模型裁决与人工专家真值分层；不产生新样本、交易结果或胜率分母。结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十一、形态边界 Holdout 追加快照（2026-09-01）

本段继续保留上方历史快照，只记录 12 张不重叠 holdout 图、冻结复核和审计加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 14 个资产 README 和 145 张 PNG；
- research/ 顶层有 176 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 323 个 Markdown 文件、2244 个 Markdown 链接。

最后一项链接数是本轮索引完成后的当前快照；如后续文档链接继续增加，动态回归守卫会要求本段同步。新增 holdout 只衡量模型 reviewer 的边界一致性，不建立人工专家真值，不产生交易结果或胜率分母。结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十二、形态边界正反例对校准追加快照（2026-09-01）

本段继续保留上方历史快照，只记录 6 对 reused calibration、标准化复核和审计加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 14 个资产 README 和 145 张 PNG；
- research/ 顶层有 177 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 326 个 Markdown 文件、2252 个 Markdown 链接。

本批只复用旧盲图做成对边界校准，不是新 holdout，不建立人工专家真值，不产生交易结果或胜率分母。结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十三、外部人工 H/L 盲标包追加快照（2026-09-01）

本段继续保留上方历史快照，只记录专家标准、空白表、中性 manifest 和 packet 审计加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 14 个资产 README 和 145 张 PNG；
- research/ 顶层有 178 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 330 个 Markdown 文件、2278 个 Markdown 链接。

本轮没有添加新 PNG，只把 16 张既有中性图组织成专家包。人工标注尚未执行，ground truth、准确率、交易结果和胜率分母仍未形成。结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十四、专家标注回收 Validator 追加快照（2026-09-01）

本段继续保留上方历史快照，只记录 annotation schema、裁决/分母政策、只读 validator 和审计加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 14 个资产 README 和 145 张 PNG；
- research/ 顶层有 179 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 332 个 Markdown 文件、2285 个 Markdown 链接。

本轮测试只创建临时合成 annotations；当前 expert packet 仍无真实 JSON/CSV 标注。ground truth、准确率、交易结果和胜率分母未形成，结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十五、外部人工安全交接就绪追加快照（2026-09-01）

本段保留上方历史快照，只记录协调人 allowlist、交接就绪审计和回归守卫加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 14 个资产 README 和 145 张 PNG；
- research/ 顶层有 180 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 334 个 Markdown 文件、2288 个 Markdown 链接。

本轮没有导出 packet、联系专家或创建 annotation。内部就绪只说明可按 21 文件 allowlist 安全交接；两位独立外部人工专家仍未开始，结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十六、双专家比较、裁决与无推断转录合同追加快照（2026-09-01）

本段保留上方历史快照，只记录 pair schema、只读 comparator、无推断转录合同/映射和审计加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 14 个资产 README 和 145 张 PNG；
- research/ 顶层有 181 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 336 个 Markdown 文件、2297 个 Markdown 链接。

本轮没有改变专家可见 21 文件 allowlist，没有创建真实 annotation 或裁决。ground truth、准确率、交易结果和胜率分母仍未形成，结论继续保持 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

## 十七、双专家裁决记录 Validator 追加快照（2026-09-01）

本段保留上方历史快照，只记录跨文件/跨字段只读 validator、合成测试和审计加入后的当前动态计数：

- patterns/ 下有 16 个 pattern 目录，foundations/ 下有 8 个基础层目录；
- research/assets/visual_recognition/ 下有 14 个资产 README 和 145 张 PNG；
- research/ 顶层有 182 个历史研究报告，research/backtesting/ 有 76 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 文档 validator 已检查 337 个 Markdown 文件、2299 个 Markdown 链接。

validator 不读取图表、不修改裁决、不建立人工真值。专家可见 21 文件 allowlist、隔离 key 和零真实 annotation/adjudication 保持不变，结论继续为 `no-new-positive / validated win-rate: not-computable / PA Research only / no Codex Trading / no quantitative scanner / no Execution Agent`。

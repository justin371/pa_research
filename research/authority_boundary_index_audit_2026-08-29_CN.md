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
- research/ 顶层有 171 个历史研究报告，research/backtesting/ 有 74 个报告文件、18 个 CSV 和 1 个 JSON 机器产物；
- 七个 canonical 索引均指向当前 PA Research 规则/合同，并保留回放引擎 0.3.9、no-new-positive、validated win-rate: not-computable 和研究/生产执行隔离；
- 文档 validator 已检查 309 个 Markdown 文件、2150 个 Markdown 链接；其中本地链接、动态 machine-artifact coverage 和核心边界检查全部通过。

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
full unittest suite: 316 passed
document validation: passed
compileall and git diff --check: passed
```

当前结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

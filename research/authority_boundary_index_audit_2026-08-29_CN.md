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
- 没有需要删除或改写的 stale/misleading authority 文案，因此不修改现有历史案例引用；合法的历史来源和禁止性边界全部保留。

## 三、固化内容

- 在 `tests/test_pa_research_scope_boundary.py` 增加 PA Research Markdown 的外部 `V1.x` 版本标记防回归检查；
- 在 `research/README.md` 增加本审计入口；
- 不修改任何市场数据、合同 CSV、回放结果、pattern 定义或 Codex Trading 文件。

## 四、验证结果

```text
external V1.x authority-marker scan: 0 matches
full unittest suite: 67 passed
document validation: passed
compileall and git diff --check: passed
```

当前结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

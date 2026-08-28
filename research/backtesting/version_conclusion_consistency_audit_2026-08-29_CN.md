# 回放版本与结论表述一致性审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 回放报告、`research/backtesting/README.md`、输出 schema、研究索引和当前 engine 版本声明<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计目的和当前基准

当前维护基准来自 `pa_research_backtest.engine.ENGINE_VERSION`：`0.3.9`。本轮只读检查版本号、历史/当前语境和结论标签，未下载行情、未新增合同、未重跑回放，也未修改任何 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。

需要区分三类内容：

1. `0.3.9` 是当前维护 engine/schema 版本；
2. `0.3.0`、`0.3.1`、`0.3.3`、`0.3.4` 和 `0.3.8` 只在历史 artifact、历史中间修复或版本演进说明中保留；
3. 历史点估计、`research_positive_conditional` 和 `process-target-reached` 都不是 `validated win-rate`，不能覆盖总状态 `no-new-positive`。

## 二、静态盘点结果

本轮检查 `research/backtesting` 下 11 份文件名含 `replay` 的 Markdown 报告，并核对回放 README、schema 和索引：

| 检查 | 结果 |
| --- | --- |
| 回放报告数 | 11 |
| 明确包含 `no-new-positive` | 11 / 11 |
| 明确包含 `validated win-rate: not-computable` | 11 / 11 |
| 当前维护版本 `0.3.9` 有明确语境 | 11 / 11 |
| 旧版本被标为历史/旧摘要/中间版本 | 通过逐份复核 |
| 历史统计数字被本轮改写 | 0 |
| 新增结果分母 | 0 |

`hl_contract_batch*`、`hl_large`、`hl_next*` 报告保留旧回放版本，是为了准确记录当时外部 artifact 或历史回放环境；它们现在都明确说明当前维护 engine 为 `0.3.9`，旧数字不会因版本升级自动变成当前验证结果。`artifact_schema_roundtrip` 中的 `0.3.8` 也只描述升级前的 metadata 缺口。

## 三、发现与修正

发现一处容易让读者误认当前版本的表述：`replay_outcome_denominator_audit` 原来三处直接写“engine `0.3.3`”，但没有在每处都说明这是该审计对应的历史中间版本。本轮仅补充上下文：

- 分母防护和 horizon 修复归属于当时的历史中间版本 `0.3.3`；
- 当前 engine `0.3.9` 延续这些语义和保护；
- 当时用 `0.3.3` 做的内存语义复核不是新的验证批次。

同时给 8 份旧批次回放报告补上统一版本边界说明，并把原本只写 `not-validated` 或中文“不可升级为已验证统计”的结论统一补充为：

```text
validated win-rate: not-computable
```

这些是文档澄清，不改变任何胜负、`realized_R`、Wilson 区间、合同、输入文件或样本身份。

## 四、结论与范围声明

当前 PA Research 文档的版本语义已统一：`0.3.9` 是当前 engine；旧 engine 只作为历史 provenance；所有回放报告都明确保留 `no-new-positive` 和 `validated win-rate: not-computable`。历史 60%/76.47%/100%/0% 等点估计仍只能按各自报告的描述性、依赖和事件/空间限制读取，不能拼成验证胜率，也不能移交生产交易系统。

本轮结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

# 回放 artifact 状态与 CLI 返回码审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research `artifact_validator.py`、`scripts/validate_pa_research_artifact.py` 及其最小临时 fixture 回归测试<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计目的

本轮只审计已有 artifact 的读取、schema 状态分类和 CLI 返回码，不下载行情、不增加合同或结果样本、不重跑正式回放，也不改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。审计目标是确保 artifact 完整性状态不会被误读为交易统计或胜率验证。

## 二、状态与返回码边界

| fixture 情况 | validator 状态 | CLI 返回码 | 处理含义 |
|---|---|---:|---|
| 当前 engine/schema、文件、hash 和 round-trip 均一致 | `current_valid` | `0` | artifact 链路完整；不代表胜率已验证 |
| 旧 engine、缺失当前 metadata/summary 字段或缺失结果列 | `historical_incomplete` | `2` | 只能作为历史描述，不能进入当前验证样本 |
| 文件缺失、JSON/CSV 解析失败、空 CSV、源码文件不可用、hash/嵌套 metadata/round-trip 不一致 | `invalid` | `1` | 当前 artifact 不可接受，不能进入统计 |

最小 fixture 矩阵实测覆盖了当前有效、缺失文件、坏 JSON、空 CSV、坏 CSV、缺失 `summary_provenance`、缺失必需结果列、源码文件不可用、源码 hash 篡改和旧 engine。结果与上述边界一致；没有发现需要改变生产语义的状态分类或 CLI 返回码 bug。

## 三、固化内容

- 在 artifact validator 测试中固化 `0=current_valid`、`2=historical_incomplete`、`1=invalid` 三条 CLI 路径；
- 固化缺失/坏文件和空/坏 CSV 返回 `invalid`，而缺失当前 provenance 或结果 schema 返回 `historical_incomplete`；
- 固化 `engine_source` 文件不可用和实际源码 hash 不匹配时不得返回 `current_valid`；
- README 与统一输出 schema 明确：`current_valid` 只描述 artifact schema/provenance 完整，不是胜率通过、交易授权或独立样本证明；
- 未修改正式回放语义、engine 版本、合同输入、价格数据和任何 pattern 统计分母。

## 四、验证结果

```text
targeted artifact-state tests: 9 passed
full unittest suite: 63 passed
document validation: passed
compileall and git diff --check: passed
```

## 五、结论与范围声明

本轮是 artifact 状态和接口契约审计，不产生新的市场结论。当前 PA Research 结论继续为：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

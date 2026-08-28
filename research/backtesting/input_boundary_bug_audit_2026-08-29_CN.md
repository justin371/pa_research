# 回放输入边界与 provenance bug 审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research `engine.py` 的合同/价格输入、回放成本参数、artifact validator 以及对应回归测试<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、发现的可复现问题

本轮只用最小内存 fixture 和仓库 example 合同做输入边界测试，没有下载行情、没有新增冻结合同、没有重跑正式回放，也没有改变任何 pattern 规则。

1. 直接构造 `BacktestContract` 时，`structural_stop`、`first_obstacle`、`target_price`、`entry_trigger` 的 `NaN/Inf` 以及非有限 `pre_entry_space_R` 原来可能绕过 CSV 解析层；非整数 `max_hold_bars` 也可能被放行。
2. 价格 CSV 的 `Open/High/Low/Close/Volume` 为 `Inf` 时，原 loader 只检查缺失值和 OHLC 关系，可能把非有限行情当成有效输入。
3. `run_contract` 的 `commission`、`spread`、`cash` 直接传入 `NaN/Inf` 或无效现金时，没有统一的项目级参数错误；CLI 对 `NaN` 也可能绕过原来的比较条件。
4. 空 CSV 原来直接泄露 pandas `EmptyDataError`，合同和价格输入没有统一的领域错误信息。
5. artifact validator 原来只核对 `summary.json` 和 `run_metadata.json` 内部的 `engine_source_sha256` 是否相等；如果两份文件一起被改成同一个假 hash，仍可能被判为 `current_valid`，没有和 metadata 指向的实际 engine 源文件核对。

## 二、修复内容

- `validate_contract` 现在拒绝非有限必需价格、非有限空间证据和非整数/无效 `max_hold_bars`，并在方向几何检查前避免对无效数值做比较；
- `load_prices` 现在把空文件、混合时区日期和非有限 OHLCV 统一拒绝；
- `load_contracts` 现在把空文件转换为明确的 `ContractValidationError`；
- `run_contract` 与 CLI 现在要求成本参数有限且非负、合成现金有限且为正；
- artifact validator 现在核对实际 `engine_source` 文件的 SHA-256，双文件同步篡改同一假 hash 会返回 `invalid`；
- 新增 8 个输入边界回归测试，并新增源码 hash 篡改回归测试。

这些修复只收紧无效输入和 provenance 证据链；对已有有效合同的交易规则、订单分支、horizon、结果分母和 pattern 分层不作改变。engine 版本继续为 `0.3.9`，因为本轮没有改变有效合同的回放语义。

## 三、验证结果

目标测试覆盖：非有限合同数值、空间证据、非整数 horizon、非有限成本/现金、非有限 OHLCV、空输入、混合时区日期和 artifact 源码 hash 篡改。完整回归结果为：

```text
targeted input/artifact tests: 13 passed
full unittest suite: 59 passed
```

同时保持文档、编译和 diff 空白检查通过；测试产生的 artifact 只在临时目录中使用，未写入仓库，也未成为统计样本。

## 四、结论与范围声明

本轮修复了输入数据和 provenance 的可复现边界问题，没有新增样本、没有扩大胜率分母、没有混算 ABC/BOP/H1/H2/L1/L2/H3/L3。结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

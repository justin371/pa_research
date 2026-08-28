# 回放范围隔离与依赖边界审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 的 `pa_research_backtest/`、`scripts/`、`tests/`、`requirements-backtesting.txt`、配置与文档引用<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计目标

本轮确认 PA Research 仍是只读、研究用途的人工冻结合同回放层，没有把 Codex Trading、Futu/OpenD、量化扫描器或 Execution Agent 接入执行路径。审计只读取现有代码、依赖和配置，不下载行情、不新增样本、不重跑回放、不改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。

## 二、可执行代码与依赖检查

对 `pa_research_backtest/` 和 `scripts/` 的 Python 文件做 AST import 盘点，得到的外部运行依赖只有：

- `backtesting`：用于本地历史合同模拟；
- `pandas`、`numpy`：用于输入/结果表和数值处理；
- `matplotlib` 只在仓库依赖说明中作为人工图表审查资产的可选渲染器。

没有发现 Futu/OpenD、Moomoo、IBKR、Binance、Alpaca、broker、MCP、HTTP、socket、websocket 或其他行情/券商连接器 import；没有发现网络请求、账户/凭证读取、解锁、下单、改单、撤单或订单发送路径。`engine.py` 中的 `self.position` 是 `backtesting.py` 模拟器内部的持仓对象，用于历史回放退出处理，不是券商账户或 Execution Agent 接口。

`requirements-backtesting.txt` 当前只有两条已锁定依赖：

```text
backtesting==0.6.6
matplotlib==3.10.9
```

本轮新增的 `tests/test_pa_research_scope_boundary.py` 固定了两条预防性检查：生产/脚本 Python 的 import 不得引入上述外部市场或执行模块，回放依赖必须保持上述研究用途版本。测试中的禁止词仅用于断言边界，不构成运行时连接。

## 三、文档引用与真实接入的区分

代码和文档中出现 `Execution Agent`、`Codex Trading` 或 `scanner` 的位置，均是 metadata 范围声明、文档 validator 的禁止性检查或审计报告的边界说明；它们没有对应模块、适配器、网络客户端、凭证文件或执行调用。Futu/OpenD 只在研究边界中被明确写成未连接，不能把这些说明误读为已获得 Futu 访问。

PA Research 回放器仍只接受人工冻结合同：它不自动发现股票、不自动识别三推/H1/H2/L1/L2、不连接实时行情，也不把回放结果发送给任何交易系统。输出中的 `results.csv`、`summary.json` 和 `run_metadata.json` 只服务 artifact provenance 和描述性审计。

## 四、结论与范围声明

本轮没有发现真实的跨系统依赖泄漏，因此没有修改 production replay 逻辑、合同字段、数据源或结果分母；只增加了可重复的范围守卫测试，并同步 README、索引和本报告。当前结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

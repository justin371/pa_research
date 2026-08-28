# PA Research 文档 validator 与 engine 合同 parity 审计（2026-08-29）

结论：发现并修复了文档 validator 相对 engine 0.3.9 的合同校验覆盖缺口。原 validator 可能只检查身份字段就放过 loader 会拒绝的冻结合同；现已补齐必需列、pandas 缺失标记、订单/gap、数值、日期、入场几何、研究字段、H/L 回调位置、EMA 和 META 校验，并用临时合成负例验证两者的拒绝边界。没有改动 engine 有效语义、历史 CSV 或统计样本；当前结论继续为 `no-new-positive`，`validated win-rate: not-computable`。

## 1. 审查范围

逐项对照：

- `scripts/validate_pa_research_docs.ps1` 的冻结合同检查；
- `pa_research_backtest/engine.py` 的 `REQUIRED_CONTRACT_COLUMNS`、支持枚举、`validate_contract` 和 `load_contracts`；
- [`冻结合同回放器 README`](README.md) 的当前输入边界；
- 现有冻结合同、示例合同和 intake 隔离记录。

## 2. 原有 parity 缺口

文档 validator 原先只要求冻结 CSV 含 8 个身份/标签列，并检查少量方向、Pattern、lineage、事件和空间状态。它没有同步覆盖 engine 已经执行的以下硬校验：

- engine 的完整 20 列合同 schema；
- `order_branch` 和 `gap_policy` 的支持组合；
- `entry_trigger`、结构止损、首障碍、目标和空间证据的有限数值；
- `max_hold_bars` 为正整数、日期可解析以及 stop/障碍/目标相对入场方向正确；
- `label_source`、`>=2y` Daily、重要高低点和 EMA 审查字段必须完整；
- H/L 的 `h_l_pullback_location`、EMA 闸门、`meta_confluence`、`meta_zone` 和至少两个独立 `meta_components`；
- engine 经 `pandas.read_csv` 默认处理的标准缺失值标记。

因此会出现“文档 validator 通过、实际 loader 拒绝”的潜在分叉。现有 60 条冻结合同本身没有触发这些缺口，但 validator 的防护不足需要修复。

## 3. 已完成修正

- validator 增加与 engine 对齐的完整冻结合同必需列和非空值检查；
- 增加日期、有限数值、正整数持有期、订单分支、gap policy、入场几何和研究审查字段检查；
- validator 对 pandas 默认缺失值标记统一按缺失处理，并覆盖 H/L 必需的 `h_l_pullback_location` 及所有非空 EMA slope 枚举；
- 增加 META 枚举、区域和独立来源数量检查；
- 统一 `internal_label` 的大小写/`none`/`pending` 规范化，减少 validator 与 loader 的解析分叉；
- 增加可选 `-RepoRoot` 参数，用于隔离副本测试，不改变默认仓库检查路径；
- 把本审计报告加入 validator 必需文件清单；
- 在现有合同一致性测试中加入临时副本负例矩阵：覆盖缺列、非有限数值、方向/Pattern/内部标签、订单/gap、H/L 回调位置、EMA、META、重复合同和入场几何；确认 engine 与文档 validator 都拒绝相应边界。另保留 `stop_limit` 订单分支的独立拒绝测试。

本轮没有修改 `pa_research_backtest/engine.py`、任何历史 CSV、回放 artifact 或有效 pattern 规则；没有下载行情、运行正式回放、创建量化扫描器、连接 Execution Agent 或修改 Codex Trading。

## 4. 验证与统计边界

验证包括 8 个合同 parity 专项测试、全套单元测试、文档链接/authority validator、Python 编译检查和 `git diff --check`：全套 `75` 个单元测试通过，文档校验通过（`264` 个 Markdown 文件、`1234` 个链接）。合成负例只写入临时目录，测试结束后清理；不进入研究数据或胜率分母。验证通过后，当前统计状态仍为：

```text
document_maturity: provisional
validated win-rate: not-computable
conclusion: no-new-positive
```

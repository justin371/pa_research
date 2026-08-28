# 回放 provenance 与再现性审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 已有回放 `results.csv`、`summary.json`、`run_metadata.json`、冻结合同、历史价格快照和当前回放 engine<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计边界与结论

本次只读取仓库和本机已有 artifact，不抓取新行情、不新增冻结合同、不重写外部结果、不改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。审计目的有两个：确认报告中的历史数字是否仍对应其指定 artifact；确认同一输入的不同运行能否由版本和文件指纹复现。

结论先行：

- 13 份历史 `summary.json` 的行数、成交数、完成数、描述性胜率和 `realized_R` 分布，均能与各自 `results.csv` 对上；这只证明 artifact 内部自洽，不证明独立样本或长期胜率。
- 当前报告指定的正式 artifact 数值可以复核；`hl_next4_replay` 指向的 `replay2` 与报告一致，不能把同目录下旧的 `replay` 版本混入。
- `next4/replay` 与 `next4/replay2` 使用相同合同/价格文件字节哈希、都标记 engine `0.3.1`，但一个记录 0 条成交、另一个记录 2 条成交。旧元数据没有源码指纹，因此 `replay` 不能被称为可再现结果；报告只采用明确指定的 `replay2`，不择优覆盖旧 artifact。
- `next5/results_final` 与 `results_repo_inputs` 的 6 行结果字节完全相同，但价格 CSV 的原始字节哈希不同：artifact 版本多了 `Adj Close/EMA20/EMA50/EMA200`，参与回放的 OHLCV 数值相同。它们是同一结果的不同输入封装，不是 12 个样本。
- `next5/results_clean` 与 `results_final` 只有 `PA-HL-NEXT5-NDAQ-L1-20220510` 的 `event_context` 不同：前者为 `ordinary_non_event`，后者为 `earnings_adjacent`。执行结果相同，但事件分层不同，正式报告使用后者，不能把两份合并。

因此本次仍没有新增正向样本或验证分母；结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

## 二、历史 artifact 盘点与指纹

以下哈希是对本机已有文件的只读计算。历史 summary 的 engine 版本保留在 `summary.json`，但 13 份旧 `run_metadata.json` 均没有单独的 engine/依赖版本、源码指纹或输入/结果文件指纹。

| artifact | summary engine | 行数 | 完成 | 胜/负 | 描述性胜率 | results.csv SHA-256 | price CSV SHA-256 | contract CSV SHA-256 |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| `backtest-smoke-20260826` | 0.2.0 | 1 | 1 | 1/0 | 100.00% | `ac34972568451f2671eb681b6deae206f913a0578af9045e5bc0c130554dbd7a` | `831ab36fd8c696873d53dbe28e1f15d8a8bfe9a2fdb4682f5d60e95478df8f3d` | `fbf1730208a377bde3e5f74d3f7415ab40e7dd69e05b588e4140a253da03aa03` |
| `hl-batch-replay-20260826` | 0.3.0 | 5 | 3 | 1/2 | 33.33% | `94fae4b049aca800d644931a5a4f726dfa530f186337ab8fd591e7ac0ba1aa40` | `c6d0f2415040ba2fe6dbd3e6b74156b552e552b00b7545c34700b9d914ca874b` | `878d107efed6483b5f6531c80e9f02ce0c8e93d31bdae47040d479511302b132` |
| `hl-batch-replay-20260826-final` | 0.3.0 | 5 | 3 | 1/2 | 33.33% | `94fae4b049aca800d644931a5a4f726dfa530f186337ab8fd591e7ac0ba1aa40` | `c6d0f2415040ba2fe6dbd3e6b74156b552e552b00b7545c34700b9d914ca874b` | `878d107efed6483b5f6531c80e9f02ce0c8e93d31bdae47040d479511302b132` |
| `hl-batch2-replay-20260826` | 0.3.0 | 3 | 3 | 3/0 | 100.00% | `3205a20a0aad62bab7e92a4d7889b9fe361df551d2b15f01caad64506f5a2268` | `cfe7c499d51064c9c98131443c27a3ca74e39d1805fbcb221e4e917b3b204ef5` | `5e030911e03de044c1aec7b839f39a27880d85769c68a64214649edd34565489` |
| `hl-large-replay-20260827` | 0.3.1 | 37 | 17 | 13/4 | 76.47% | `cd4fedf3d31df9ecb6d43a3a8c3860b84759cf0685b6eb12a6bf6cfb66520b5c` | `8a86fc0913a6df66551cef4875357c3ff37221787e181e9a840068c86c2b3b44` | `7faf77134998be5f14fb40ab823429be6d53b57f855d08d51048c849fa81fba2` |
| `hl-next/replay` | 0.3.1 | 5 | 2 | 1/1 | 50.00% | `97b821818b152b712f2057ad375e3204771f62f57af2e8f3cfcccdc371b174a4` | `938364d8fca1bd94d3d261126295871c49d87f8a77e46a51a2abdd6ee6400c7d` | `a0971c4d54bbbecc9cc4466bf6fdc00c13ccea59c47a47f8f038ccfff2e336e1` |
| `hl-next2/replay` | 0.3.1 | 2 | 2 | 2/0 | 100.00% | `ce39febc36de35228f4b2798708ce9682a6f88c309cfabb21aa8cefe7b700574` | `f1f0987e5685be34f1a405777563a74db655a86e2947ebcf7952b270992e9d4d` | `f34fecce5f74cb62409340511647a0516fc2a012f98ee972f112cfe65713bdc9` |
| `hl-next4/replay` | 0.3.1 | 2 | 0 | 0/0 | 不可计算 | `71b8bfaadd1e7aad17ad0e718fc5b15d6b4c45ac2e1c4761669b4ac2aca4ae96` | `c8e6c4bd725fc2717b06f77bc8244cc43ee8cd80d1e7865db17f517723e7c23f` | `18ba86742c1a88c8e586d4e76c9117b1903bf8d5653045eba7eeaca85bc80947` |
| `hl-next4/replay2` | 0.3.1 | 2 | 2 | 0/2 | 0.00% | `0805851fc7c19a486831e5ccf5177dcfd9fc6afbf656168d4f6f7ac375799424` | `c8e6c4bd725fc2717b06f77bc8244cc43ee8cd80d1e7865db17f517723e7c23f` | `18ba86742c1a88c8e586d4e76c9117b1903bf8d5653045eba7eeaca85bc80947` |
| `hl-next5/replay/results` | 0.3.1 | 8 | 6 | 3/3 | 50.00% | `947b2a8461778fa6aacfb0892ebe0ba58ebf8b510d3da1f1305dbad9ab2d76ae` | `da7330046034c00f51175d7dd3058d27266f14958913d6779fbf7e82d9902894` | `2cecf4020e475f7d6d1671945db28c29eb4bdb3b6c4ebf3483971e59b872f524` |
| `hl-next5/replay/results_clean` | 0.3.1 | 6 | 5 | 3/2 | 60.00% | `90aab93f95dc92ccf5107bad223832a5f7e195959d52463ab311faa710fd7185` | `da7330046034c00f51175d7dd3058d27266f14958913d6779fbf7e82d9902894` | `ac915dd404c72992a78d22bc964d1dba787099bcac11be32cd9ab221974da49e` |
| `hl-next5/replay/results_final` | 0.3.1 | 6 | 5 | 3/2 | 60.00% | `fa6375e2f13c0e74dca5444ac029f4051aa105feb3f15d9e8d2bc74fd910e3b6` | `da7330046034c00f51175d7dd3058d27266f14958913d6779fbf7e82d9902894` | `ac915dd404c72992a78d22bc964d1dba787099bcac11be32cd9ab221974da49e` |
| `hl-next5/replay/results_repo_inputs` | 0.3.1 | 6 | 5 | 3/2 | 60.00% | `fa6375e2f13c0e74dca5444ac029f4051aa105feb3f15d9e8d2bc74fd910e3b6` | `8e36b89a7708d11c904641ec79d5180935281afde0790bad4d1e0a17ed00999e` | `ac915dd404c72992a78d22bc964d1dba787099bcac11be32cd9ab221974da49e` |

13 份 summary 与各自 results 的 `contract_count`、`filled_count`、`completed_trade_count`、`win_rate_pct` 以及有限 `realized_R` 的 mean/median/min/max 均一致（允许 CSV 浮点序列化误差）。因此本次发现的主要问题是跨 artifact 的身份和可再现性，而不是某一份 summary 内部算错。

## 三、报告数值与正式 artifact 的对应关系

按仓库报告明确指定的 artifact 做现有输入的内存复核，未写出新的结果文件。下表中的“当前复核”使用 PA Research 当前 engine `0.3.6`；新增的事件/空间/独立性字段会比旧结果多，但成交、退出、结果标签和 `realized_R` 的核心历史路径保持一致。

| 报告 | 指定 artifact | 旧 summary | 当前输入复核 | 处理 |
| --- | --- | --- | --- | --- |
| 首批 H/L | `hl-batch-replay-20260826` | 5 合同，3 完成，1/2，33.33% | 5 合同，3 完成，1/2，33.33% | 数值对应；共享 TSLA lineage 不独立 |
| 第二批 H/L | `hl-batch2-replay-20260826` | 3 合同，3 完成，3/0，100.00% | 3 合同，3 完成，3/0，100.00% | 数值对应；空间/事件仍按报告限制解释 |
| H/L 大样本 | `hl-large-replay-20260827` | 37 合同，17 完成，13/4，76.47% | 37 合同，17 完成，13/4，76.47% | 只保留历史描述；事件未核实且共享 lineage |
| 下一批 | `hl-next/replay` | 5 合同，2 完成，1/1，50.00% | 5 合同，2 完成，1/1，50.00% | 数值对应；事件组与普通组不混算 |
| 下一批（二） | `hl-next2/replay` | 2 合同，2 完成，2/0，100.00% | 2 合同，2 完成，2/0，100.00% | 数值对应；n=2 不验证 60% |
| 下一批（四） | `hl-next4/replay2` | 2 合同，2 完成，0/2，0.00% | 2 合同，2 完成，0/2，0.00% | 以 `replay2` 为正式 artifact；同输入的 `replay` 版本不纳入 |
| 下一批（五） | `hl-next5/replay/results_final` | 6 合同，5 完成，3/2，60.00% | 6 合同，5 完成，3/2，60.00% | 以 `results_final` 为正式 artifact；clean/8-row 版本不混入 |

### 旧 artifact 的再现性冲突

`hl-next4/replay` 与 `hl-next4/replay2` 的 price/contract SHA-256 完全相同，summary 都写 engine `0.3.1`，但前者两行都是 `unproven`，后者是 CBOE 止损和 ROST 时间退出。旧 `run_metadata.json` 没有引擎源码、提交或结果文件指纹，无法从现有证据确定差异来自哪个未记录的运行状态。因此：

1. `hl_next4_replay_2026-08-27_CN.md` 指定的 `replay2` 保留为报告来源；
2. `replay` 只作为不可再现的历史 artifact 记录，不删除、不覆盖、不择优合并；
3. 未来相同输入必须同时记录 engine 版本、源码 SHA-256、输入 SHA-256、结果集 SHA-256 和实际结果文件 SHA-256。

### next5 的输入封装差异

`results_final` 和 `results_repo_inputs` 的结果文件 SHA-256 相同，合同文件 SHA-256 也相同；两份价格文件的 OHLCV 行按 `Symbol/Date/Open/High/Low/Close/Volume` 规范化后相同，artifact 版本仅额外带有 `Adj Close` 和 EMA 列。引擎不使用这些额外列，所以结果相同，但原始价格文件 SHA-256 仍应保留，不能把两个目录当作两批样本。

`results_clean` 与 `results_final` 的唯一结果字段差异是 NDAQ `2022-05-10` 的事件上下文：`ordinary_non_event` 对 `earnings_adjacent`。这不改变执行路径，却改变事件分层；正式报告选择 `results_final`，因此 60% 只能按最终事件隔离口径作描述。

## 四、已落实的修复

当前 engine 已升级为 `0.3.6`：

- 合同加载时对 `sample_id` 使用大小写不敏感的规范身份，对 `lineage_id` 使用规范化合同族键；大小写不同的重复身份不再被当成两条冻结合同放行；
- CLI 输出的 `summary.json` 与 `run_metadata.json` 都记录 `engine_version`、`backtesting_version`、Python/pandas/numpy 运行时版本和 `engine_source_sha256`；
- `run_metadata.json` 记录实际写出的 `results_file` 和 `results_file_sha256`，同时保留输入文件与 canonical `result_set_sha256`；
- 现有重复结果、共享 lineage、共享市场状态和重叠持仓的隔离逻辑保持不变；这些字段仍不能自动识别图表 pattern，也不能制造独立样本；
- schema、回放 README、历史报告索引和文档 validator 已同步说明旧 summary/metadata 的历史局限，并把本审计加入入口。

这些改动只属于 PA Research；没有修改 Codex Trading，没有创建量化扫描器，没有连接 Execution Agent，也没有连接 Futu/OpenD。

## 五、结论

报告数字与各自正式 artifact 基本对应，但历史 artifact 的版本/源码 provenance 不足，且存在同输入不同输出的旧运行冲突。当前可以保留各批次的描述性胜率和 `realized_R` 作为历史路径记录，不能把跨批合并数值或任意选择的 artifact 升级为独立验证统计。

```text
no-new-positive
validated win-rate: not-computable
```

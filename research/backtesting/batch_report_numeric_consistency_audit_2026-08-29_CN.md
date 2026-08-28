# PA Research 批次报告数字与分层一致性审计（2026-08-29）

结论：对现有 H/L 合同 CSV、冻结前选择记录、历史回放报告和两个研究索引做只读交叉核对后，核心合同数、方向/内部标签、EMA gate、lineage、历史结果数字和 `no-new-positive` 结论均能对上。发现并修正了两处容易误读的文案边界：全部 ABC/BOP intake 是 25 条而不是统一 intake 的 10 条；旧批次报告里的 `xR` 是冻结价格几何审计值，不等同于当前 CSV 的显式 `space_status`。没有新增样本、没有下载行情、没有运行正式回放，也没有改写历史结果。当前结论保持 `no-new-positive`，`validated win-rate: not-computable`。

## 一、审计范围与口径

本次只读取以下仓库事实：7 个非示例冻结 H/L 合同 CSV、2 个 intake CSV、各批次选择/回放 Markdown、研究索引、当前 engine `0.3.9` 以及此前已记录的历史 artifact 对照结果。合同数和方向/标签从 CSV 重算；事件 bucket 和显式空间 bucket 使用当前 engine 的保守分类；历史成交、胜负和 `realized_R` 只核对报告已指定的历史 artifact，不生成新的结果文件。

必须分开看两种空间信息：

1. **冻结价格几何**：用结果发生前已写入的 `entry_trigger`、`structural_stop` 和 `first_obstacle` 计算 `xR`。旧报告可以保留这一历史审计值。
2. **显式合同空间状态**：当前 engine 只从合同里的 `pre_entry_space_R`/`space_status` 读取 `strict_ge_1R`、`borderline` 或其他状态。旧 50 条合同没有这些列，因此当前 `contract_space_bucket` 必须是 `unknown_contract_space`，不能用几何值事后回填。

这两个口径都与 PA Research 的事前证据原则兼容，但不能在表述中混为同一字段。

## 二、冻结 H/L 合同逐批重算

字段顺序：`long/short`；`H1/H2/L1/L2`；`long_pass/short_pass/observation_only`；当前 engine 的事件 bucket；当前显式空间 bucket 的 `strict/borderline/unknown`；冻结价格几何 `>=1R/<1R`；规范化 lineage 数。

| 批次 | 合同 CSV | 合同数 | long/short | H1/H2/L1/L2 | EMA pass / observation | 当前 event bucket | 当前显式空间 bucket | 几何 `>=1R/<1R` | lineage |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: |
| 首批 | `hl_contracts_2026-08-26.csv` | 5 | 3/2 | 1/2/1/1 | 2/2/1 | event_reviewed_non_event=3; event_driven=1; event_unverified_or_pending=0; ordinary_non_event=0; earnings_adjacent=0; unknown=1 | explicit=0/0/5 | geometry=3/2 | lineages=4 |
| 第二批 | `hl_contracts_batch2_2026-08-26.csv` | 3 | 1/2 | 0/1/2/0 | 1/2/0 | event_reviewed_non_event=0; event_driven=0; event_unverified_or_pending=3; ordinary_non_event=0; earnings_adjacent=0; unknown=0 | explicit=0/0/3 | geometry=2/1 | lineages=3 |
| 大样本 | `hl_large_contracts_2026-08-27.csv` | 37 | 20/17 | 15/5/12/5 | 16/17/4 | event_reviewed_non_event=0; event_driven=0; event_unverified_or_pending=37; ordinary_non_event=0; earnings_adjacent=0; unknown=0 | explicit=0/0/37 | geometry=5/32 | lineages=31 |
| 下一批 | `hl_next_contracts_2026-08-27.csv` | 5 | 4/1 | 4/0/1/0 | 4/1/0 | event_reviewed_non_event=0; event_driven=2; event_unverified_or_pending=0; ordinary_non_event=3; earnings_adjacent=0; unknown=0 | explicit=0/0/5 | geometry=5/0 | lineages=5 |
| 下一批（二） | `hl_next2_contracts_2026-08-27.csv` | 2 | 2/0 | 2/0/0/0 | 2/0/0 | event_reviewed_non_event=0; event_driven=0; event_unverified_or_pending=0; ordinary_non_event=2; earnings_adjacent=0; unknown=0 | explicit=1/1/0 | geometry=2/0 | lineages=2 |
| 下一批（四） | `hl_next4_contracts_2026-08-27.csv` | 2 | 2/0 | 2/0/0/0 | 2/0/0 | event_reviewed_non_event=0; event_driven=0; event_unverified_or_pending=0; ordinary_non_event=2; earnings_adjacent=0; unknown=0 | explicit=2/0/0 | geometry=2/0 | lineages=2 |
| 下一批（五） | `hl_next5_contracts_2026-08-27.csv` | 6 | 0/6 | 0/0/6/0 | 0/6/0 | event_reviewed_non_event=0; event_driven=1; event_unverified_or_pending=0; ordinary_non_event=4; earnings_adjacent=1; unknown=0 | explicit=6/0/0 | geometry=6/0 | lineages=6 |
| **合计** | **7 个 CSV** | **60** | **32/28** | **24/8/22/6** | **27/28/5** | **event_reviewed_non_event=3; event_driven=4; event_unverified_or_pending=40; ordinary_non_event=11; earnings_adjacent=1; unknown=1** | **explicit=9/1/50** | **geometry=25/35** | **53** |

重算结果说明：方向、内部标签、EMA gate、事件 bucket、显式空间 bucket、几何空间和 lineage 数字均与现有字段覆盖、事件空间和 lineage 审计相符。`geometry=25/35` 不能替代 `explicit=9/1/50`；前者是从旧合同价格字段得出的历史几何，后者是当前合同 schema 中实际冻结的空间状态。

## 三、intake 与 Pattern 隔离

仓库当前有两类不同结构的 intake：

| 范围 | 文件数 | 行数 | 细分 | 是否进入回放 |
| --- | ---: | ---: | --- | --- |
| 统一 ABC/BOP intake | 1 | 10 | `ABC_CONT` 6、`BOP` 4 | 否，全部 `contract_frozen=no` |
| BOP 专项 intake | 1 | 15 | 使用 BOP 专项字段，不以统一 `primary_pattern` 计数 | 否，全部 `contract_frozen=no` |
| 全部 intake | 2 | 25 | 两类候选/边界记录 | 否 |

此前个别审计表中的“6 条 ABC、4 条 BOP”只描述统一 `abc_bop_contract_intake_2026-08-28.csv`，不是 25 条 intake 的总量。本轮已在跨 Pattern、lineage、coverage 和 inventory 相关文案中加上文件范围，避免把 BOP 专项 15 条漏掉，或把 intake 行误当成冻结样本。

当前 60 条冻结 H/L 中：冻结 `ABC_CONT=0`、冻结 `BOP=0`、冻结 `H3/L3=0`。因此没有把 H/L、ABC、BOP 或三推合并成一个胜率分母。

## 四、历史回放报告数字核对

下表只复核报告已经指定的历史 artifact；不在本轮重新运行回放。`完成`仍按各报告当时的 `win/loss/scratch` 完成口径，`胜/负`不包括 `opening-skip`、观察行或无成交行。

| 批次 | 报告中的核心结果 | 核对状态 |
| --- | --- | --- |
| 首批 | `contract_count=5`；`eligible_contract_count=4`；`filled_count=3`；`completed_trade_count=3`；1/2；`33.33%`；合计 `-0.9414R` | 对应指定 artifact；TSLA H1/H2 共享 lineage，不能当独立样本 |
| 第二批 | `contract_count=3`；`eligible=3`；`filled=3`；`completed=3`；3/3；`100.00%`；合计 `+4.8743R` | 对应指定 artifact；当前事件 bucket 全部为未核实/待定，不能升级普通事件干净证据 |
| 大样本 | 37 合同；17 成交；17 完成；13/4；`76.47%`；合计 `+1.9652R` | 对应指定 artifact；37 条事件过滤未核实，历史严格几何子集不等于当前显式空间分层 |
| 下一批 | 5 合同；2 成交/完成；1/1；`50.00%`；合计 `+1.4063R` | 对应指定 artifact；普通组 3 条均 opening-skip，事件组单独保留 |
| 下一批（二） | 2 合同；2 成交/完成；2/0；`100.00%`；合计 `+2.5925R` | 对应指定 artifact；只有 2 个 lineage，不能验证 `60%` |
| 下一批（四） | 2 合同；2 成交/完成；0/2；`0.00%`；合计 `-1.5090R` | 只采用报告指定的 `replay2`，不混入同目录旧 `replay` |
| 下一批（五） | 本批回放 6 条；5 成交/完成；3/2；`60.00%`；合计 `+3.4812R` | 只采用 `results_final`；ordinary、earnings-adjacent、earnings-driven 分开 |

`下一批（三）`没有合同 CSV：18 个候选、0 个冻结合同、0 个回放分母、胜率不可计算。它不能被当作 0% 或 100%，也不能补成占位样本。

各历史回放报告仍保留 `no-new-positive`、`validated win-rate: not-computable` 和当前 engine `0.3.9` 的历史版本边界。点估计和 `realized_R` 是路径描述，不是已经验证的长期胜率或收益优势。

## 五、修正与结论

本轮确认并修正的文案问题只有两类：

1. 把统一 10 行 ABC/BOP intake 的 6/4 分布误读成全部 25 行 intake；现已明确统一文件、BOP 专项文件和总量。
2. 把旧批次报告中的冻结价格几何 `xR` 与当前 engine 的显式 `space_status` 混读；现已明确旧 50 条合同的当前显式空间 bucket 是 unknown，历史几何仍可作为不回写结果的事前审计值。

没有发现需要改写的历史成交、胜负、`realized_R`、方向/内部标签或正式报告结论。没有新增 ABC、BOP、H3/L3 或 H/L 样本，没有改变 pattern 规则或 engine 有效语义。

```text
research_state: provisional
validated win-rate: not-computable
conclusion: no-new-positive
```

本审计只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

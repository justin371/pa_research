# 视觉资产与事前证据边界审计（2026-08-29）

状态：`research_only / visual_evidence_audit / pre-entry-boundary / no-new-positive`

## 审计范围

本审计只检查 PA Research checkout 中已经存在的视觉资产、资产 README、人工选择记录、冻结合同 CSV 和索引。检查没有下载行情、调用 Futu/OpenD、运行正式回放、修改 pattern 规则或 engine 有效语义，也没有修改 Codex Trading。审计不把图像文件变成量化扫描器输入，不连接 Execution Agent。

检查项目是：

1. README 中列出的 PNG 是否与实际文件一一覆盖，且本地 PNG 链接是否可解析；
2. 图像文件是否是可读取的 PNG，并具有有效尺寸；
3. 冻结合同的决策日、方向、标签与图像截止文件是否对应；
4. 两年 Daily 左侧、重要高低点、支撑阻力、EMA20/50/200、事件和空间字段是否仍保留在事前合同边界内；
5. 图像和合同是否把回放结果、胜负或事后标签倒灌到入场前证据；
6. 选择记录、回放记录、研究索引和文档 validator 是否明确区分仓库内资产与外部审计 artifact。

## 仓库内视觉资产盘点

当前 checkout 有 11 个视觉资产 README、105 张 PNG。README 中的 PNG 文件名与实际递归文件名完全相等，没有发现缺失清单项、陈旧清单项或断开的本地 PNG 链接；105 张 PNG 的签名、IHDR 尺寸字段和非零宽高均通过静态检查。

| 资产目录 | PNG | 事前证据用途 |
| --- | ---: | --- |
| Round2 多标的多周期 | 20 | 两年 Daily 背景与局部多周期盲看 |
| Round3 H/L 局部盲测 | 6 | H/L 局部序列，不在图上写标签 |
| Round3 MAR | 4 | 空头 L1/L2-like 对照 |
| Round4 历史练习 | 19 | 约一年 Daily 的明确 pending 边界 |
| Round5 两年 Daily | 13 | 两年 Daily 背景练习，不冻结合同 |
| TSLA 多周期 | 4 | 两年 Daily 与局部周期视觉验收 |
| 首批 H/L 合同资产 | 5 | 冻结合同决策日截断图 |
| 第二批 H/L 合同资产 | 3 | 冻结合同决策日截断图 |
| H/L 大样本局部窗口 | 23 | 23 个局部窗口对应 37 条人工合同，不作一对一映射 |
| H/L 下一批 | 5 | 5 条 H/L 冻结合同决策日截断图 |
| H/L 下一批（二） | 3 | 2 条冻结 H1 图和 1 张 PHM 边界图 |
| **合计** | **105** | — |

Round4 的 `two_year_daily: pending` 仍然正确：它的约一年 Daily 窗口不能被图像数量或局部周期误读为完整两年背景。相反，首批、第二批、`hl_next` 和 `hl_next2` 的合同图像文件分别按 symbol/decision date 与合同逐行匹配；`hl_large` 的 README 明确记录窗口资产与 37 条合同不是一对一关系，避免把局部窗口数误读成样本数。

## 合同与事前字段

首批、第二批、`hl_next` 和 `hl_next2` 的冻结合同与本地图像截止文件均通过逐行映射：

- `hl_contracts_2026-08-26.csv`：5 条合同、5 张 `Daily_2y_cutoff` 图；
- `hl_contracts_batch2_2026-08-26.csv`：3 条合同、3 张 `Daily_2y_cutoff` 图；
- `hl_next_contracts_2026-08-27.csv`：5 条合同、5 张决策日图；
- `hl_next2_contracts_2026-08-27.csv`：2 条合同、2 张决策日图，另有不属于冻结合同的 `PHM_2023-05-31_boundary.png`；
- `hl_large_contracts_2026-08-27.csv`：37 条合同、23 个窗口，COHR/RBLX/MAR 三个合同标的均有对应窗口。

所有冻结合同继续满足以下事前证据边界：`label_source=human_chart_review`、`daily_context_window=>=2y`、重要高低点审查和 EMA20/50/200 审查为 `complete`，并保留 `event_context`、H/L EMA gate、回调位置、META 和 lineage。已存在的空白 `space_status` 没有被回放结果回填；一旦空间状态被填写，合同同时保留 `pre_entry_space_R`。事件与空间仍是事前分层字段，不是结果派生字段。

冻结合同的 CSV 表头没有 `result`、`outcome`、`realized_R`、`fill_status`、`win_rate` 或 `exit` 等结果字段。结果 artifact 不在当前 checkout 中；回放报告中提到的历史结果不能反向改变这些 CSV 或图像。

## 图像中的事后泄漏检查

对仓库内首批、第二批、`hl_large`、`hl_next` 和 `hl_next2` 代表图，以及外部审计目录中的 CBOE/MCHP 代表图进行了人工画面抽查。抽查图显示的是 OHLC、EMA20/50/200、成交量、日期轴和两年背景/局部窗口，没有看到 H1/H2/L1/L2 标签、入场、止损、第一障碍或胜负标记。资产 README 也明确规定图像不写入 pattern 标签和回放结果。

这里的结论保持审慎：静态文件测试可以确认清单、PNG 完整性和合同字段隔离，但不能把像素级人工抽查宣称为对每一张图的 OCR 证明。因此后续若重新渲染图像，仍需在结果发生前完成无标签抽查；不能仅凭文件名或 CSV 表头自动宣称“无视觉泄漏”。

## 外部 artifact 边界

`hl_next4` 和 `hl_next5` 的选择记录明确将无标签图像放在本机外部审计目录，而不是 PA Research git checkout：

- `C:\Users\lwang\.codex\artifacts\pa-research-hl-next4-20260827`：114 张 PNG；
- `C:\Users\lwang\.codex\artifacts\pa-research-hl-next5-20260827`：78 张 PNG。

本次只读盘点时两个目录均存在，且代表图保留两年背景和 EMA20/50/200；但是它们不是仓库内可由 clone 单独复现的证据。选择/回放文档已经把这一点写成外部 artifact 边界，当前仓库测试不依赖该本机路径，也没有把这 192 张图伪装成仓库内资产。若未来要求完整可移植复核，需要另立 artifact 归档策略和 manifest；本审计不把外部文件复制进仓库、不添加原始下载缓存。

## 修复与结论

本轮没有发现需要改写历史合同、价格、标签或回放结果的 mismatch。新增的回归测试固定了视觉 README 清单、PNG 文件有效性、本地冻结合同映射、事前字段和外部 artifact 边界；本报告已加入 `research/README.md`、`research/backtesting/README.md` 及文档 validator 的索引/必需文件检查。

视觉资产证据完整性得到的是“文件与文档边界可复核”，不是 pattern 自动识别准确率，也不是胜率证据。研究结论继续保持：

```text
no-new-positive
validated win-rate: not-computable
```

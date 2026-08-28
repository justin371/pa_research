# 外部视觉 artifact provenance 审计（2026-08-29）

状态：`research_only / external_artifact_audit / pre-entry-boundary / no-new-positive`

## 范围与方法

本审计只处理 PA Research 的 `hl_next4`、`hl_next5` 外部视觉 artifact。检查对象是现有本机 artifact 的 PNG 清单、文件大小、PNG 头部/尺寸、聚合 SHA-256，以及它们和选择记录、冻结合同、回放报告的对应关系。没有下载行情、调用 Futu/OpenD、运行正式回放、修改 pattern 规则或 engine 有效语义，也没有修改 Codex Trading。

机器可读清单见[`外部视觉 artifact manifest`](external_visual_artifact_manifest_2026-08-29.json)。清单只覆盖 artifact 根目录顶层 PNG；原始 `raw_jina.txt`、Daily CSV、回放输出和 `__pycache__` 明确排除。`manifest_sha256` 是按排序后的文件名、单文件 SHA-256 和文件大小组合计算的提交值，`root_name` 是逻辑标识，不把本机绝对路径写进 manifest。

## 盘点结果

| artifact | PNG | 总字节 | 分类 | 无效 PNG | manifest SHA-256 |
| --- | ---: | ---: | --- | ---: | --- |
| `hl_next4` / `pa-research-hl-next4-20260827` | 114 | 19,313,991 | candidate 18 / target 21 / local 9 / unannotated 66 | 0 | `cb562710981aad627efa90f91ad325a87ca94f230aa47ca975b772db7b3ee4c2` |
| `hl_next5` / `pa-research-hl-next5-20260827` | 78 | 19,025,901 | candidate 66 / unannotated 12 | 0 | `ed9fc8f7a817e3749122745f2eec2f9d736b879b21f277faae65da7adfdf617a` |

两个 artifact 在本次只读盘点时均存在；所有清单 PNG 具有有效 PNG 签名和非零尺寸。manifest 还保留了每个 PNG 的逻辑文件名，因此后续若外部文件被替换，数量、字节总数或聚合指纹变化都能被识别。这个清单是 provenance 证据，不是 pattern 标签、结果 artifact、扫描器输入或执行输入。

## 冻结合同映射

### `hl_next4`

- CBOE 合同 `PA-HL-NEXT4-CBOE-H1-20250522` 的决策日为 `2025-05-22`，有精确的 `CBOE_2025-05-22_candidate_review.png`；该图适合作为该决策日的视觉证据候选。
- ROST 合同 `PA-HL-NEXT4-ROST-H1-20260107` 的决策日为 `2026-01-07`，manifest 状态为 `missing_decision_date_asset`，artifact 中没有 `ROST_2026-01-07_*.png`。最近的 `ROST_2026-01-08_candidate_review.png` 和 `ROST_2026-01-13_candidate_review.png` 都在决策日之后（`post-decision`）；它们不能替代 `2026-01-07` 的 pre-entry visual evidence。
- 同一目录还存在 CBOE `2025-05-23`/`2025-05-27` 等决策日之后的候选图。即使图上没有结果标记，也只能视为探索或事后复核资产，不得用来证明 `2025-05-22` 冻结时的视野。

这构成一个真实的证据 provenance gap，而不是可以用邻近日期图像静默修复的文件名小问题。原始合同 CSV 和历史回放报告没有被重写，也没有把 ROST 改成新标签或新结果；在恢复准确的 `2026-01-07` 无标签图、或建立新的冻结合同前，ROST 不能被称为具有可由仓库/manifest 独立复核的决策日视觉证据。

### `hl_next5`

MCHP `2022-06-14`、NDAQ `2022-01-06`、`2022-04-25`、`2022-05-10`、`2022-12-19` 和 `2026-06-22` 均有与合同决策日匹配的 candidate-review PNG；NDAQ `2026-06-22` 有两个同日版本，manifest 两个都保留，不把重复渲染误算为两个合同。六条合同的事件分组、L1 标签、EMA20/50 方向和空间字段仍来自回放前 CSV，不从图像或结果反推。

## 事后泄漏与视觉限制

人工抽查了 CBOE `2025-05-22`、CBOE `2025-05-23`、ROST `2026-01-08`、MCHP `2022-06-14` 和 NDAQ `2026-06-22` 代表图。抽查画面显示 OHLC、EMA20/50/200、成交量、两年背景或局部窗口，没有看到 H1/H2/L1/L2、入场、止损、第一障碍或胜负标记；但 `ROST_2026-01-08` 明确是 `target 2026-01-08`，所以即使没有结果文字，也不能作为 1 月 7 日冻结图。

像素抽查不是对全部 192 张 PNG 的 OCR 证明。今后重新生成或替换外部图像时，必须继续区分：决策日截断图可作为 pre-entry 复核候选，决策日后的 candidate/target/local 图只能作为探索或事后审阅，不能倒灌标签、触发、止损、空间或胜率分母。

## 修复与当前结论

本轮采取的修复是：

1. 新增不含绝对路径的 PNG 文件清单与聚合哈希 manifest；
2. 新增可选的本机 artifact 重算测试：artifact 存在时核对文件名、数量、分类、尺寸、字节总数和 SHA-256，artifact 不存在时不让仓库测试依赖用户本机路径；
3. 在 `hl_next4` 选择/回放文档中显式记录 ROST 决策日图缺失和后一天图不可替代，避免把它继续描述成完整的 pre-entry visual evidence；
4. 更新研究索引和文档 validator 的必需文件清单。

没有复制外部 PNG、原始下载文本或回放结果进仓库，没有增加样本，也没有重新计算历史胜率。当前研究结论仍为：

```text
no-new-positive
validated win-rate: not-computable
```

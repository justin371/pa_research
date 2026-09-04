# 普通 H/L 外部人工交接就绪审计（2026-09-01）

状态：`document_status=completed / internal_handoff_readiness=ready / external_human_execution=not_started`

## 一、判定

截至 `acc574c` 后的当前 checkout，PA Research 的 H1/H2/L1/L2 外部专家安全采集包已经内部就绪：中性 16 图 packet、隔离来源 key、冻结 manifest、空白表、专家标准、机器 schema、单专家只读 validator、双专家裁决/分母政策、索引和回归守卫均已存在且彼此一致。

这不是“识别准确率已经验证”。两位真正独立的外部人工专家尚未开始，因而没有 ground truth、准确率、交易结果或胜率分母。

```text
internal_packet_and_contract_work: complete
collection_handoff_readiness: ready
independent_agent_work_remaining_before_requesting_humans: pair_adjudication_contract_and_transcription_mapping
external_human_gate: two_clean_independent_experts_not_started
real annotation artifacts: 0
ground_truth_status: not_established
overall accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

## 二、复核证据

| 项目 | 当前证据 | 判定 |
|---|---|---|
| 中性 packet | manifest 精确为 16 个 `EH1-###`、16 个唯一现存 PNG | ready |
| manifest 冻结 | SHA-256 `d1616e568bceebbe605d498548ffc5c346cec1365831ba9035ab131ad9765b23` | ready |
| 左侧背景 | 来源合同要求至少 500 根 Daily、EMA20/50/200、原始成交量和重要高低点 | ready |
| 未来隐藏 | 来源合同要求至少 40 根未来 Daily 隐藏，label/outcome/future 均 hidden | ready |
| 身份中性副本 | 16 张图重新渲染为 `EH1-###` 标题和相对 `T-…/T0` 横轴；股票、日历日期、MC2/BH1 来源 ID 均不显示 | ready |
| 来源假设隔离 | curation key 只在被忽略的 `.codex/goals/`，不受 Git 跟踪 | ready |
| 专家输入 | 标准、16 行空白表、schema 与中性 manifest | ready |
| 回收门槛 | validator 硬校验 hash、固定 16 项、ID、枚举、证据、冻结顺序和污染 | ready |
| 分歧政策 | 两专家比较、第三人裁决、boundary/unclear/污染和准确率分母均已定义 | ready |
| 真实标注 | JSON/CSV 为 0，未请求、未模拟、未代填 | human-gated |

## 三、安全交接边界

[协调人安全交接清单](calibration/external_human_hl_v1/coordinator_handoff_checklist_CN.md)规定只导出 21 个专家可见文件：5 个合同文件和 manifest 指向的 16 张 PNG。[安全导出器](../scripts/export_pa_hl_expert_packet.py)会先验证 manifest/图哈希，只接受尚不存在且不位于冻结源包内部的目标；完整暂存并复核后才原子 no-replace 发布。它不复制内部 hash inventory、清单、审计、来源资料或 annotation，也不会在失败时留下半包。不能把整个 repo、Git 历史、`.codex/`、来源 manifests、旧盲审、未来或结果文件交给专家。

这是必要边界：原始来源图会显示 symbol、cutoff date 和 MC2/BH1 来源 ID，不能直接交给专家。本轮已用同一 OHLC/EMA/volume 窗口重新渲染身份与日历日期隐藏副本，并用 `neutral_chart_sha256.json` 固定 16 张图的 SHA-256。readiness 因此表示“可按 allowlist 交接这些中性副本”，不是“整个 checkout 可以分享”。

## 四、剩余工作分类

### 现在仍可由 Agent 独立完成

安全采集本身没有内部 blocker，但完整下游流程还有两项可提前完成、且不需要真实标签的非阻塞工具：

1. pair-level 裁决记录 schema 和只读双记录比较器；
2. Markdown 空白表到 schema JSON 的逐字段转录合同/测试，明确禁止模型推断或补齐。

按用户要求，这两项应放进下一个独立 goal，在真正请求专家前完成。它们不改变当前 packet 已可安全交接的判定，也不能替代人工标签。

### 必须由外部人工完成

1. 用户/协调人选择两位互相独立、理解 Daily PA 的外部人工专家；
2. 按 allowlist 分别交付隔离副本；
3. 两位专家独立完成并冻结全部 16 项；
4. 原样转录为 schema JSON，并分别通过 validator；
5. 对两份 `clean_eligible` 记录进行逐项比较，必要时请第三位独立专家裁决；
6. 裁决冻结后才揭示来源假设并计算本 cohort 的视觉识别指标。

招募、身份确认和真实标注都属于外部人类 gate，不能由本 goal 自动执行或伪造。

### 人工结果返回后 Agent 可继续

- 只读验证两份记录并报告 exit 0/1/2；
- 在不改写专家原始记录的前提下生成分歧清单；
- 根据既定政策生成裁决记录和 cohort-only 视觉指标；
- 继续保持视觉准确率与交易胜率、盈亏比、候选授权完全隔离。

## 五、结论边界

本审计没有新增视觉标签、positive case、交易合同或结果。内部交接准备完成，只说明研究流程已到外部人工 gate；不说明 PA pattern 已达到某个准确率，更不说明达到 60% 胜率目标。

本轮只修改 PA Research；不修改 Codex Trading，不创建量化扫描器或自动 pattern detector，不连接 Futu/OpenD，不连接 Execution Agent。

## 六、验证证据

```text
identity-neutral charts: 16, each >= 2000x1200, frozen SHA-256 matched
safe exporter: exact 5 documents + 16 charts; internal files and annotations excluded
focused packet / intake / handoff / renderer tests: 32 passed
full repository unittest suite: 397 passed
document validation: 334 Markdown files / 2288 links passed
compileall and git diff --check: passed
real annotation artifacts: 0
```

## 七、后续内部合同闭合（2026-09-01）

后续独立 goal 已补齐本审计第四节列出的两项非阻塞工具：pair-level 裁决 schema、先调用单专家 validator 的只读双记录 comparator，以及空白表到 schema JSON 的逐字段无推断转录合同/机器映射。协调清单现在把 `independent_agent_work_remaining_before_requesting_humans` 记为 `none`。

这不改变本审计的外部人工状态：两位专家仍未开始，真实 annotation 仍为 0，ground truth 和准确率仍未建立。身份中性专家包继续保持严格 21 文件 allowlist，没有把内部 comparator、裁决 schema、转录合同、来源 key 或审计暴露给专家。

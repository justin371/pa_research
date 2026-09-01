# 形态边界决策卡独立 Holdout 审计（2026-09-01）

状态：`document_status=completed / evidence_scope=visual_boundary_agreement_only / human_expert_status=not_performed / ground_truth_status=not_established`

## 一、结论先行

本轮在新的 12 张 Daily 截止图上完成了 24 份 reviewer-first 盲审。样本以确定性规则在看图前冻结，与此前两个盲测 cohort 的精确“股票代码 + 截止日”重叠为 `0/12`；reviewer 看不到代码、来源标签、未来 K 线或交易结果。两份冻结记录 SHA-256 完全一致。

决策卡在本批次下呈现出两个不同方向的信号：

- `b_leg_class` 两 reviewer 精确一致率为 `5/12 = 41.67%`，高于旧批次的 `4/16 = 25.00%`；`visual_family` 为 `66.67%`，高于旧批次的 `56.25%`；
- 但 `stage_1_status` 只有 `41.67%`，`attempt_label` 只有 `50.00%`，且没有任何一张图被两名 reviewer 共同归为普通 `H_L_like`；只有 `1/12` 被共同升级到 `deep_reviewed`。

因此，当前最诚实的结论不是“识别率已经提高”，而是：决策卡让部分 B 腿和 family 分流更一致，同时暴露出普通 H/L 与 BOP、三推、普通 ABC continuation 之间仍缺少可稳定复现的正例边界。旧批次与本批次的样本和任务包不同，上述差值只能做描述性比较，不能证明决策卡产生了因果改进或已经泛化。

本轮没有人工专家 ground truth、没有结果回放、没有完成交易分母：

```text
overall accuracy: not-computable
validated win-rate: not-computable
conclusion: no-new-positive
```

## 二、样本冻结与盲法

1. 使用固定 seed `pa-morph-boundary-holdout-v1`，在看图前确定 12 个股票与截止日；
2. 每张图保留至少 500 根截止日前 Daily、隐藏至少 40 根未来 Daily，并显示 EMA20/50/200、原始成交量和局部放大；
3. reviewer 只看到 `BH1-001` 至 `BH1-012` 中性编号图和[形态边界视觉决策卡](../docs/morphology_boundary_decision_card_CN.md)；
4. 每张图由两名互相独立的 reviewer 先读，24 份记录全部在任何答案或结果揭示前冻结；
5. 本轮不做模型 adjudication，不把 reviewer 一致当作专家真值，也不查看未来结果。

冻结证据：

- [Holdout reviewer 资产包](assets/visual_recognition/2026-09-01/morphology_boundary_holdout_v1/README.md)；
- [中性 manifest](assets/visual_recognition/2026-09-01/morphology_boundary_holdout_v1/manifest.json)：SHA-256 `13d82d0065f4c1acc73f3e065e1412651cda63c252a66a82e0d7e0a0421c38dd`；
- [24 份原始盲审记录](morphology_boundary_holdout_blind_reviews_2026-09-01.json)：SHA-256 `c818f536ce6b38f04e57579bc15902773dd6434d8ca6ded72fd5a9dc531bdbfc`；
- [机器可读统计](morphology_boundary_holdout_metrics_2026-09-01.json)记录全部分母、精确一致数和边界样本。

reviewer-facing README 与 review form 不反向链接原始答案或本审计，继续保持可复用的结果隐藏状态。

## 三、字段一致率

| 字段 | 精确一致 | 分母 | 一致率 |
|---|---:|---:|---:|
| parent_state | 8 | 12 | 66.67% |
| direction | 9 | 12 | 75.00% |
| a_leg_quality | 10 | 12 | 83.33% |
| b_leg_class | 5 | 12 | 41.67% |
| breakout_acceptance_status | 8 | 12 | 66.67% |
| lineage_status | 9 | 12 | 75.00% |
| visual_family | 8 | 12 | 66.67% |
| attempt_label | 6 | 12 | 50.00% |
| three_push_variant | 7 | 12 | 58.33% |
| ema_gate | 10 | 12 | 83.33% |
| stage_1_status | 5 | 12 | 41.67% |
| selection_disposition | 9 | 12 | 75.00% |

“一致”只表示两个 reviewer 选择同一枚举，不表示该枚举正确。尤其本轮没有外部人工专家标签，不能计算 sensitivity、specificity、precision、recall 或整体 accuracy。

## 四、与旧 cohort 的描述性比较

| 字段 | 旧批次 16 张 | 新 holdout 12 张 | 描述性差值 |
|---|---:|---:|---:|
| A leg quality | 75.00% | 83.33% | +8.33pp |
| B leg class | 25.00% | 41.67% | +16.67pp |
| visual family | 56.25% | 66.67% | +10.42pp |
| attempt label | 62.50% | 50.00% | -12.50pp |
| EMA gate | 75.00% | 83.33% | +8.33pp |
| stage-1 status | 75.00% | 41.67% | -33.33pp |
| selection disposition | 68.75% | 75.00% | +6.25pp |

这不是同一批图的 before/after 试验，也没有随机分派同图使用旧卡与新卡，所以不能把正差值归因于决策卡，不能把负差值解释为能力退化。它只用于确定下一轮应优先修订哪些边界。

## 五、主要边界发现

### 1. 普通 H/L 仍未形成稳定正例

两 reviewer 共同 family 一致的 8 张图中，分流为 BOP 3 张、三推 3 张、ABC continuation 1 张、NONE 1 张；共同 `H_L_like` 为 0 张。这个结果支持“先做状态迁移、第三推和区间分流，再计数 H/L”的保守顺序，但不能证明系统能稳定找到 H1/H2/L1/L2。

### 2. B 腿进步信号仍不足以验收

`b_leg_class` 从旧批次 25.00% 到本批次 41.67% 是有价值的描述性信号，但仍有 7/12 分歧。分歧集中在：

- `controlled` 与 `controlled_late`；
- `controlled_late` 与 `deep_but_late_controlled`；
- `controlled_late` 与 `range_like`；
- `not_formed`、`uncontrolled`、`unclear` 的事件或状态转换边界。

下一步不应增加机械阈值，而应给每一组边界补“为什么不能归入相邻类”的同图对照。

### 3. 四张 family 边界图最值得复盘

- `BH1-004`：三推反转边界 versus 大区间内无有效方向；
- `BH1-006`：失败第三推 versus 事件/异常扩张导致的 NONE；
- `BH1-007`：趋势末端三推 versus 已接受突破后的 BOP；
- `BH1-011`：区间边缘三推 versus BOP 状态迁移。

这四张图的共同问题不是“有没有形状”，而是决策顺序中的状态迁移、事件边界和 parent state 会改写主 family。

### 4. 选股阶段判断比 family 更不稳定

`visual_family` 一致率为 66.67%，但 `stage_1_status` 只有 41.67%。即使 family 相同，reviewer 仍会在 `candidate / wait / reject` 之间分歧；这说明看出大体 pattern 还不等于可以进入深审。位置、空间、事件、EMA 和未完成结构必须继续独立设门。

## 六、下一步验收条件

下一轮应保持同样的 label-hidden、outcome-hidden 流程，重点建设小型“边界对”集合，而不是扩大市场扫描：

1. 为 BOP versus 三推、三推 versus 区间重复测试、普通 ABC continuation versus H1/H2 各准备同图反例对；
2. 为 `controlled / controlled_late / deep_but_late_controlled / range_like` 各补正反两例；
3. 在新 cohort 中必须出现由两 reviewer 共同识别的普通 H1/H2/L1/L2，才能开始讨论 H/L family 的 sensitivity；
4. 只有外部人工专家独立标注后，才能把一致性升级为准确率；只有事前冻结合同和结果回放后，才能讨论胜率与盈亏比。

## 七、仓库和执行边界

本审计只属于 `PA Research only`。它不修改 Codex Trading，不创建量化扫描器或自动 pattern detector，不连接 Futu/OpenD，不连接 Execution Agent，也不构成交易建议、候选授权或生产规则交接。

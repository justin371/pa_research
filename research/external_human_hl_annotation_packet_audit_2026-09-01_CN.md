# 普通 H1/H2/L1/L2 外部人工专家盲标包审计（2026-09-01）

状态：`document_status=completed / packet_status=ready / human_expert_status=not_performed / ground_truth_status=not_established`

## 一、结论

PA Research 已准备一份可交给外部人工专家的普通 H1/H2/L1/L2 盲标包，但本 goal 没有执行、模拟或代填任何专家标签。

包内有 16 张唯一历史 Daily 截止图，全部来自此前已冻结的中性视觉 cohort：每张图至少有 500 根左侧 Daily、至少 40 根隐藏未来 Daily，并显示 EMA20/50/200、原始成交量和重要高低点。专家可见文件只使用 `EH1-001` 至 `EH1-016`，不显示股票、截止日期、来源候选标签、旧模型判断、旧裁决、未来路径或回放结果。

构建时的隔离平衡为：

- 普通 H/L 来源假设 8 张：H1/H2/L1/L2 各 2 张；
- hard-negative 来源假设 8 张：accepted BOP 2、第三推 2、区间重复测试 1、事件边界 1、EMA gate 失败 1、空间不足 1。

这些只是策划 packet 的 model/source hypotheses，不是答案。具体 ID 映射只保存在 `.codex/goals/` 下的 ignored curation key，不进入专家可见包，也不进入 Git。即使外部专家完全否定全部 8 个 H/L 来源假设，也属于有效标注结果。

当前统计边界：

```text
human_expert_status: not_performed
ground_truth_status: not_established
overall accuracy: not-computable
completed_trade_denominator: 0
validated win-rate: not-computable
conclusion: no-new-positive
```

## 二、冻结证据

- [专家包入口](calibration/external_human_hl_v1/README.md)；
- [中性 manifest](calibration/external_human_hl_v1/manifest.json)：身份中性重渲染后的 SHA-256 `d1616e568bceebbe605d498548ffc5c346cec1365831ba9035ab131ad9765b23`；
- [专家标注标准](calibration/external_human_hl_v1/expert_criteria_CN.md)；
- [空白标注表](calibration/external_human_hl_v1/annotation_form.md)。

manifest 的每个 sample 只有 `expert_sample_id` 和 `chart_path`。初始构建时由两个已冻结来源 manifest 验证 16 张图的 500-bar context、40-bar hidden future 和 label/outcome/future 隐藏合同；来源映射随后只保留在被忽略的 curation key。当前回归测试不读取该 key，而是检查 16 张身份中性副本的路径、文件名、PNG 尺寸和冻结 SHA-256。

2026-09-01 后续交接审计发现原始来源 PNG 的标题和日期轴仍显示 symbol、cutoff date 与 MC2/BH1 来源 ID，因此原始图不再作为专家交付物。当前 manifest 已改为 16 张 `EH1-###` 身份中性重渲染副本：标题不含 symbol/date，横轴只用相对 `T-…/T0`，文件名和路径不含来源 ID；OHLC、EMA20/50/200、成交量和 504/120 bar 窗口保持不变。16 张副本的 SHA-256 另由内部完整性文件冻结。

## 三、专家判断顺序

专家不能直接“看着像 H1/H2 就投票”，必须按以下顺序给出证据：

1. 图表证据是否可用；
2. parent state、方向、EMA20/50 斜率和 EMA200 背景；
3. 是否已有 accepted BOP、第三推、区间重复测试或事件重定价；
4. A 是否有推动，B 是否小而犹豫、从属于 A；
5. lineage 是否延续，当前是第一还是第二次有意义尝试；
6. 左侧第一障碍和空间是否允许保留普通 H/L；
7. 最后填写 H1/H2/L1/L2、`not_ordinary_HL` 或 `unclear`。

如果不是普通 H/L，必须选择最先改变路由的 `primary_exclusion`，并写出高低点、A、B、lineage、EMA 和空间证据。`confidence_1_to_5` 只是标注信心，不是胜率。

## 四、推荐的人工作业流程

1. 最好由两名互相独立的外部专家分别复制空白表，不共享答案；
2. 两份记录先分别冻结，并填写是否看到来源假设、未来或结果；
3. contamination 为 `yes` 的记录不能进入 clean ground-truth 候选；
4. 只有独立标签冻结后，才允许比较两位专家分歧；
5. 分歧若需第三人 adjudication，第三人也不能先看到 curation key；
6. curation key 最后才揭示，而且只用于分析旧假设偏差，不能反向修改专家标签。

本 goal 到第 1 步之前即停止：包已就绪，但没有声称已经找到外部专家、完成标注或建立 ground truth。

## 五、何时才能讨论准确率

必须至少具备：

- clean 的外部人工专家冻结标签；
- 对专家分歧的独立处理规则；
- 对 `unclear`、污染记录和不可用图的明确分母政策；
- 将模型预测在专家标签冻结后再揭示。

即使形成视觉识别准确率，它也只衡量本 cohort 的标签识别，不等于交易胜率。胜率和盈亏比仍需要独立的事前合同、执行假设、结果回放和足够的独立 lineage。

## 六、仓库边界

本轮只增加 PA Research 的专家盲标包、审计和回归守卫。没有修改 Codex Trading，没有创建量化扫描器或自动 pattern detector，没有连接 Futu/OpenD，没有连接 Execution Agent，也没有产生交易建议或授权。

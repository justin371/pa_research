# PA Research 候选、视觉复核与交易日志边界一致性审计（2026-08-29）

结论：本轮只审计 PA Research 内的日线候选/冻结前选择记录、视觉复核索引、统一输出字段、策略候选目录和历史交易日志入口，没有下载行情、调用 Futu/OpenD、运行正式回放或新增样本。先前四类记录边界问题已保持修正；本轮追加修正了视觉候选目录缺少独立方向列、少数状态别名不规范、两批旧合同把人工 A/B 描述与 canonical 结构化字段完整度混在一起的歧义，以及日线候选输出链缺少显式合同/周期/许可和 BOP 边界的问题。修正后，形态、入场前证据、交易状态和事后路径保持分轴；结论保持 `no-new-positive`，`validated win-rate: not-computable`。

## 一、范围和判定方法

本轮检查对象包括：

- `research/backtesting/hl_*_selection_2026-08-27_CN.md` 六份选择/视觉冻结前记录，以及有冻结合同批次对应的合同 CSV；
- [`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)、每日候选卡和视觉复核卡；
- [`strategy/pattern_inventory_candidates.md`](../strategy/pattern_inventory_candidates.md) 候选目录；
- [`strategy/reviews/2026-06-25-tsla-meta-example.md`](../strategy/reviews/2026-06-25-tsla-meta-example.md) 历史三推/META 观察笔记；
- 既有视觉资产、回放报告、交易日志/历史复盘索引之间的引用边界。

判定顺序是：先确认方向和候选状态，再确认左侧两年 Daily、重要高低点、EMA20/50/200、A/B leg、计数和 lineage；最后才检查触发、结构失效、首障碍、空间、成交和结果。`pattern_like`、`candidate_pending`、`valid_no_trade`、`observation_only` 和视觉人工复核都不能直接等同于冻结合同或胜率结果。

## 二、选择记录的方向和数量核对

六份选择记录现在都把方向与 H/L 标签分开表达。合同 CSV 是冻结/回放输入的机器可读来源，选择记录只负责记录当时的人工证据和边界；没有合格合同的批次明确写 `long=0`、`short=0`，不把空缺当作零胜率。

| 选择记录 | 合同/候选数量 | 方向分布 | 标签分布 | 当前解释 |
| --- | ---: | --- | --- | --- |
| `hl_large_selection` | 37 | `long=20`、`short=17` | `H1=15`、`H2=5`、`L1=12`、`L2=5` | 方向、标签、EMA gate 和空间分层分开；边界行不等于高质量机会 |
| `hl_next_selection` | 5 | `long=4`、`short=1` | `H1=4`、`L1=1` | 表格和汇总均明确方向 |
| `hl_next2_selection` | 2 | `long=2`、`short=0` | `H1=2` | H2/L2 空缺不解释为失败率 |
| `hl_next3_selection` | 18 个候选、0 个合同 | `long=0`、`short=0`（冻结合同） | 无冻结标签 | 候选方向/标签与交易合同分开 |
| `hl_next4_selection` | 2 | `long=2`、`short=0` | `H1=2` | CSV 仍是回放前冻结状态，但 ROST 视觉证据有 provenance gap |
| `hl_next5_selection` | 6 | `long=0`、`short=6` | `L1=6` | 结果移回独立 replay 报告，不污染冻结前摘要 |

这项核对不改变任何 Pattern 规则：强 A、受控 B、EMA20/50 方向、左侧重要高低点、事件隔离、lineage 和首障碍仍是人工复核字段，不是程序识别或自动授权条件。

## 三、逐项修正

### 1. 方向必须显式记录

`hl_large_selection` 原来只在标的日期串中写 H1/H2/L1/L2，读者需要从标签反推多空方向；这不满足 PA Research “方向必须明确”的记录要求。现补入 `long=20`、`short=17`，并在 `hl_next`、`hl_next2`、`hl_next3`、`hl_next4`、`hl_next5` 统一补入方向/标签汇总。

### 2. 冻结前选择记录不能混入回放结果

`hl_next5_selection` 的状态是 `frozen_pre_outcome`，但原摘要同时写入“5 条成交并完成”、`3/5=60%`、事件分层胜负和实现结果。这会让选择记录看起来像是用结果回写了候选质量。现删除这些事后数字，仅保留 6 条冻结合同及方向、标签、A/B、EMA、事件、空间、触发和失效边界；成交、退出、胜率和实现 R 只在[`hl_next5_replay_2026-08-27_CN.md`](backtesting/hl_next5_replay_2026-08-27_CN.md)中保留。

这不是删除历史结果，而是恢复文件职责：回放报告可以引用冻结前选择记录，选择记录不能把回放结果伪装成入场前证据。`no-new-positive` 和 `validated win-rate: not-computable` 均保持不变。

### 3. ROST 的视觉 provenance 与合同状态分开

`hl_next4_selection` 现在明确说明：CBOE/ROST 两行的 CSV `contract_frozen=yes` 是历史记录状态，但 ROST 缺少 `2026-01-07` 决策日视觉 artifact，后一天图不能替代 pre-entry 图证据。因此，ROST 不能被描述为“仓库可独立复核的完整视觉证据”；这不会静默改写合同 CSV、历史回放数字或 Pattern 标签。具体 artifact 清单和哈希边界仍见[`外部视觉 artifact provenance 审计`](backtesting/external_visual_artifact_provenance_audit_2026-08-29_CN.md)。

### 4. 历史 TSLA/META 笔记补齐状态轴

`strategy/reviews/2026-06-25-tsla-meta-example.md` 原来只写“Potential Trigger”和反向观察，缺少 `contract_scope`、`direction`、数据完整性、两年 Daily/EMA 覆盖、`research_state`、`trade_state`、`gate_result` 和 `handoff_status`。现按实际证据补为：

- `contract_scope=historical_context_only`；
- `direction=no_valid_direction`、`permission=no_direction`；
- `research_state=pattern_like`、`trade_state=not_authorized`、`gate_result=observation_only`；
- `daily_context_window/EMA/事件/精确触发/首障碍` 缺失处明确写 `unavailable`、`unknown` 或 `pending`；
- `order_branch=observation_only`，没有实际成交、冻结订单或结果字段。

因此“三推楔形”仍是潜在 `H3_L3` 观察，不会被这条笔记升级成 L3 反转规则、交易日志或可回放样本。

### 5. 候选目录的状态标签不再冒充统一状态

`strategy/pattern_inventory_candidates.md` 的“当前状态”同时服务视觉目录和历史路径索引，少数条目含有 `process-*`、`*-reached` 或 `opening-skip` 等事后审计词。现补充说明：这些词只是路径/订单审计事实，不能复制成入场前 `research_positive_conditional`，也不能替代 `trade_state`、`gate_result`、`handoff_status` 或冻结合同。目录仍然不是胜率表、量化输入或交易授权。

## 四、证据字段和交易日志边界

现有冻结合同/视觉资产的已验证边界继续保留：

| 检查项 | 当前口径 |
| --- | --- |
| 左侧背景 | 本地冻结合同资产要求 `daily_context_window=">=2y"`；Round4 约一年图仍保持 pending，不被局部图补写 |
| 重要高低点 | 合同要求 `major_high_low_review=complete`；ROST 的问题是外部决策日 artifact provenance，不是用后一天图补写高低点 |
| EMA | 合同要求 EMA20/50/200 审查字段；H1/H2 的多头两条向上、L1/L2 的空头两条向下仍由人工冻结 |
| A/B | 强 A 提高优先级；B 必须区分小 K/受控、深但后段受控、强反向压力和区间化，不以结果倒推 |
| 触发/失效/首障碍/空间 | 只有冻结合同才写精确数值；`pending`、`unknown`、价格区域和 `valid_no_trade` 不能直接送回放 |
| 交易日志/结果 | 成交、退出、`realized_R`、胜率和路径状态只在独立 replay/result 记录中出现，不回填候选或冻结前字段 |
| 视觉人工复核 | `human_chart_review` 说明来源，不代表自动识别准确率；Matplotlib 只渲染，不识别 Pattern |

本轮没有把外部 PNG 复制进仓库，没有新增交易样本，没有改 Pattern 规则或 `backtesting.py` engine 有效语义。

## 五、追加字段覆盖与索引修复

### 1. 视觉候选目录的方向轴

原视觉候选表有 89 行，但方向主要藏在 `BULL`/`BEAR` ID、中文描述或 H/L 标签中；混合 universe、framework、状态转换和没有单一方向的行没有可直接读取的值。现已给表增加 canonical `direction` 列：单一研究方向保留 `long` 或 `short`，混合/框架/状态未冻结行明确写 `no_valid_direction`。这只是索引层研究方向，不是入场、成交或授权；完整候选卡和冻结合同仍必须逐标的填写方向。

同时把该索引内的 `research_positive conditional`、`valid no-trade` 和 `research_positive_candidate` 统一为当前状态轴的 `research_positive_conditional`、`valid_no_trade` 和 `research_positive_conditional`。其他历史汇总中的旧别名仅在明确的“历史说明别名”上下文中保留，不把历史叙述强行改写成新的结果或合同。

### 2. 旧合同的 A/B 与空间字段边界

现有 60 条冻结 H/L 合同仍是核心字段完整；其中 50 条旧合同没有 `a_leg_quality`、`b_leg_class`、`pre_entry_space_R`、`space_status`、`contract_state` 这组较新的结构化字段。`hl_large_selection` 的 37 条和 `hl_next_selection` 的 5 条现已明确写出这一点：报告中的人工 A/B、空间和两年背景复核不能当作 CSV 已经拥有同名 canonical 字段，也不能由结果倒推补齐。最新详细批次继续要求在结果发生前一次性冻结这些字段；旧 CSV 不回填。

25 条 ABC/BOP intake 仍全部为 `contract_frozen=no`，方向和缺失字段有记录但不进入回放分母；不存在实际 `journal/`、交易日志或券商成交记录。

## 六、日线候选输出链的周期和合同边界

本轮进一步核对了 `docs/daily_candidate_review_card_CN.md`、`strategy/pattern_inventory_candidates.md`、六份历史选择记录和五份较早的视觉 candidate 入口：

- 日线候选卡现显式要求 `contract_scope: daily_candidate`、`directional_bias`、`direction`、`permission`、`lineage_id`、`market_context_id` 以及 BOP 的边界/接受/回踩字段；该合同的 `timeframes_seen` 只能是 `Daily`。4H/1H/60m/15m 只能在日线闸门通过后进入独立 `deep_review` 或订单合同，不能补写日线缺失证据。
- 六份 `hl_*_selection_2026-08-27_CN.md` 现明确为 `contract_scope: historical_context_only`、`timeframes_seen: Daily`。它们是历史选择/冻结前记录，不是当前 `daily_candidate`；CSV 内既有的字段覆盖缺口和市场/事件证据边界保持原样，不通过本轮回填或改写。
- CRM、META、MSFT、NVDA 和候选网格五个较早入口现分别声明 `historical_context_only` 或 `stage_1_fast_screen`，并逐项标出方向、可见周期、图表完整度、两年 Daily 覆盖、事件/市场状态及 `research_state`/`trade_state`/`gate_result`。缺失项保留 `unknown`、`unavailable` 或 `pending`；这些记录不能因出现 H/L-like、低周期或后见之明而升级为授权。
- 本审计追踪的五个入口已在 `research/README.md` 和 `strategy/README.md` 建立直接索引：[`CRM`](crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md)、[`META`](meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md)、[`MSFT`](msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md)、[`NVDA`](nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md) 和[`候选网格`](visual_screen_candidate_grid_2024_2025_CN.md)。该索引修复只改善可追溯性，不改变任何历史字段、样本或结果状态。
- 候选目录的流程已固定为 Daily-first：`stage_1_fast_screen`/观察行不等于 `daily_candidate`；只有通过日线前置并补齐字段后，才可建立独立深审/订单合同。`outcome` 仅属于独立 replay/result 的事后字段，不能反向改变候选状态。

因此，本链条的可追溯路径是：

```text
Daily-first stage1 / historical inventory
  -> 方向、事件/市场状态、两年 Daily、重要高低点、EMA20/50/200、A/B 和空间字段
  -> 通过日线前置后才可提升为 daily_candidate
  -> 可选的独立 4H/1H/60m/15m deep_review 或订单合同
  -> 独立冻结合同
  -> replay / trade-log 结果分开记录
```

## 七、历史、视觉与回放后验语义扫描

本轮进一步对五个已索引的历史视觉候选入口及全部仓库 Markdown 做了只读语义扫描：

- CRM、META、MSFT、NVDA 和候选网格五个入口仍为 `research_state: pattern_like`、`trade_state: not_authorized`；没有把 `entry_price`、`fill_status`、`trade_result`、`realized_R`、`path_result` 等后验字段写入这些入场前记录；
- 全部 Markdown 没有活动字段 `research_state: validated`、`trade_state: authorized` 或 `handoff_status: ready_for_system`；`research_positive_conditional` 仍只表示条件性研究状态，不表示已验证正例；
- 回放结果、首障碍到达和历史路径继续只在独立 replay/result 或审计语境中出现；它们不能倒灌成 `daily_candidate`、生产规则或交易授权。

没有发现新的违规活动语句；本轮把上述检查固化到 validator 和回归测试，防止历史视觉候选或后验结果以后发生职责漂移。该修复不新增样本、不改变历史结果，也不改变 `no-new-positive` / `validated win-rate: not-computable`。

## 八、结论

修正后，PA Research 的记录链为：

```text
Daily-first 视觉复核/候选目录
  -> pattern_like 或 observation_only / valid_no_trade
  -> 只有通过日线前置后，补齐两年 Daily、重要高低点、EMA、A/B、lineage、触发、失效、首障碍和空间
  -> 低周期只进入独立 deep_review/订单合同
  -> 仅在独立冻结合同中出现精确订单字段
  -> 结果只进入独立 replay / trade-log 审计
```

本审计只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

```text
no-new-positive
validated win-rate: not-computable
```

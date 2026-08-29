# H/L `special_subtype` 与事件分层字段范围一致性审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 日线规则、统一输出 schema、视觉复核卡、每日候选卡、H/L 冻结合同和当前回放 engine `0.3.9`<br>
状态：`research_only / audit_only / no-new-positive`

## 结论

本次只读取现有规则、合同、报告和 engine，没有下载行情、看新图或运行回放。机器盘点确认：7 个 H/L 冻结合同 CSV 共 60 条记录均没有 `special_subtype` 列；当前 engine 的 `REQUIRED_CONTRACT_COLUMNS`、`BacktestContract` 和结果分层也不消费该字段。因此这 60 条不能产生 subtype 胜率或事件 subtype 交叉统计，更不能把 subtype 缺失推断为 `ordinary`。

发现并修正一处文档范围缺口：最新日线选股规则已经定义 `special_subtype`，但统一输出 schema、完整视觉复核卡和每日候选卡没有同步声明其枚举与边界。现在这些上游研究模板已补齐，并明确 `special_subtype` 只是结构/路径的补充注释，不能替代 raw `event_context` 或 canonical `event_bucket`，也不能把事件样本升级为普通非事件。

## 一、字段职责和范围

| 字段/位置 | 当前职责 | 是否进入 H/L 回放合同 |
| --- | --- | --- |
| `special_subtype` | 日线候选/视觉研究的补充 subtype，如 `ordinary`、`deep_late_controlled_B`、`earnings_driven`、`gap_reprice` | 否；60 条冻结合同均未提供 |
| `event_context` | 入场前人工记录的 raw 事件说明 | 是；60/60 非空 |
| `event_bucket` | engine 从 raw `event_context` 保守派生的 canonical 事件分层 | 是结果/摘要派生轴；不能由 subtype 或结果覆盖 |

`special_subtype=ordinary` 只表示研究者对结构/路径的 subtype 判断，不等价于 `event_bucket=ordinary_non_event`。反过来，`event_bucket=event_driven`、`earnings_adjacent` 或 `event_unverified_or_pending` 也不能仅靠 subtype 文案改写。事件资格仍必须由 `event_context` 及其事件核实证据承担；缺失 subtype 时保持未记录，不补写。

`earnings_driven` 是 subtype 的规范下划线写法；事件分层的 canonical 名称仍是 `event_driven`。`gap_reprice` 说明订单/结构路径，不自动代表某个 event bucket；同样要看 raw `event_context`。

## 二、现有 H/L 合同机器事实

### 字段覆盖

| 对象 | 数量 | 结果 |
| --- | ---: | --- |
| H/L 冻结合同 CSV | 7 个 | 全部可读取 |
| H/L 合同总行数 | 60 | 全部有 `event_context` |
| 含 `special_subtype` 表头的 H/L CSV | 0/7 | 回放输入没有该字段 |
| 含 `special_subtype` 值的 H/L 行 | 0/60 | 不生成 subtype 统计 |
| engine 最小合同所需 `special_subtype` | 否 | 不改变当前回放接口 |

### canonical `event_bucket` 分布

这部分继续只由 raw `event_context` 派生，与 subtype 是否存在无关：

| `event_bucket` | 合同数 |
| --- | ---: |
| `ordinary_non_event` | 11 |
| `event_reviewed_non_event` | 3 |
| `event_driven` | 4 |
| `earnings_adjacent` | 1 |
| `event_unverified_or_pending` | 40 |
| `unknown` | 1 |
| **合计** | **60** |

其中 40 条 `event_unverified_or_pending` 包括历史事件过滤未核实、板块待定或公开价格复核未闭合记录；1 条 `unknown` 的 raw 值为 `none`。它们都没有因为缺少 subtype 而被升级为 `ordinary_non_event`。普通非事件 11 条也不能反向证明其 subtype 一定填写为 `ordinary`。

## 三、selection/replay 与文档核对

1. 现有 H/L selection/replay 报告没有机器可读的 `special_subtype` 分组，也没有声称缺失 subtype 等于 ordinary；因此不补造 subtype 统计，不改写历史结果。
2. 事件分组继续使用 canonical `event_bucket`。`event_driven`、`earnings_adjacent`、`ordinary_non_event`、`event_unverified_or_pending` 和 `unknown` 必须与 raw `event_context` 的保守映射一致；自然语言 subtype 只能放在研究说明中。
3. 上游规则、统一输出 schema、视觉复核卡和每日候选卡现在都列出同一套 `special_subtype` 枚举，并写明它是辅助字段，不是事件资格字段。回放 README 也明确它不属于当前 H/L 最小合同。
4. subtype 缺失是当前历史合同的字段范围事实，不是回放错误；若未来要研究 subtype 交叉结果，必须建立新的、入场前冻结且逐条填写 subtype 的独立合同批次，不能回填本批 60 条。

## 四、验证与范围边界

新增回归检查固定 H/L 合同不把 `special_subtype` 当作必需回放列、上游模板保持同一枚举、canonical event bucket 不受 subtype 缺失影响，以及 pending/unknown 不升级为 ordinary。没有新增样本、结果、胜率分母、行情或图像。

本审计只属于 **PA Research**（`PA Research only`）。范围声明：`no Codex Trading`、`no quantitative scanner`、`no Execution Agent`、`no Futu/OpenD`。当前结论继续是 `no-new-positive`，`validated win-rate: not-computable`。

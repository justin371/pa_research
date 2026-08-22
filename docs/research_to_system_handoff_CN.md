# PA Research → Codex Trading：研究交接规范

## 目的

这份文件解决一个实际问题：PA Research 和 Codex Trading 不能继续做同一份研究的两份拷贝。

两者采用单向交接，而不是双向同步：

```text
PA Research（解释、定义、证据、反例）
        ↓ 只有成熟规则才交接
Codex Trading（实现、回测、系统测试）
        ↓ 通过系统验证且另行授权
Execution Agent（模拟/真实执行）
```

研究阶段只更新 PA Research；Codex Trading 作为只读参考。当前不会因为一个案例看起来有价值，就把它复制成程序规则或交给执行层。

## 两个 Repo 各自负责什么

### PA Research

负责回答“这是什么、什么时候成立、什么时候不成立”：

- 从完整图表识别市场背景、A/B/C、H/L1-3、支撑阻力和多重优势汇聚；
- 明确订单分支、结构止损、第一障碍、R/R、Warning/Invalid；
- 记录正例、失败例、跳过交易和计数边界；
- 区分源文档、观察、假设、复盘结论与尚未解决的问题；
- 维护可以交给程序实现的规则规格，但不承担生产实现。

### Codex Trading

负责回答“能不能稳定地计算和验证”：

- 数据读取、标准化、特征计算和候选扫描；
- 把已经冻结的规则翻译成确定的程序条件；
- 回测、滑点/跳空/事件处理、统计和稳健性测试；
- 在明确授权后，才考虑 Trading System 和 Execution Agent 的连接。

Codex Trading 中已有的研究、代码和案例不在 PA Research 中整份复制；需要引用时记录来源、版本或链接，并只提炼对当前规则有用的证据。

## 研究状态词汇

每个规则或案例必须有状态，避免“写进文件”被误解成“已经验证”：

| 状态 | 含义 | 能否进入 Codex Trading 实现 |
| --- | --- | --- |
| `observation` | 图表上的观察，尚未形成完整规则 | 否 |
| `hypothesis` | 有明确条件的研究假设 | 否 |
| `replayed` | 已用历史数据按当时可见信息重放 | 否，除非完成审计 |
| `audited` | 已检查无后见之明、订单、止损、第一障碍和事件边界 | 否，仍需跨案例 |
| `validated` | 多个独立样本和反例支持，规则边界已可重复 | 可提出交接 |
| `ready_for_system` | 程序员不需要再替规则做主观解释 | 可交给 Codex Trading |
| `system_implemented` | 已在 Codex Trading 中实现并通过系统测试 | 不等于可实盘 |
| `production_candidate` | 经过额外风险、模拟和用户明确授权 | 仍不自动授权真实下单 |

## 交接时必须携带的字段

成熟规则交接时，PA Research 必须提供一份完整规格，而不是只提供形态名称：

| 字段 | 最低要求 |
| --- | --- |
| `rule_id` | 稳定、唯一的规则编号 |
| `setup` | 例如 ABC 中的 H2/L2；明确不是 Elliott Wave 标签 |
| `context` | 趋势、交易区间或过渡；更大周期背景 |
| `A/B/C` | A 的起点和强度、B 的类型、C 是否已开始；不能用后续结果倒推 |
| `count` | H/L1-3 的同周期、同一回调计数；何时重置 |
| `location` | 主要高低点、支撑阻力、区间边缘、EMA、缺口、MM 和 META 汇合 |
| `signal_trigger_order` | 信号 K、触发价、订单类型、提交时点；跳空要单独分支 |
| `stop` | 结构失效位、缓冲、为何不是更近或更远的位置 |
| `first_obstacle_rr` | 入场时已经可见的第一道障碍、空间、风险和 R/R |
| `event_boundary` | 财报前三个交易日等禁做或隔离条件 |
| `states` | Working、Warning、Invalid 的可观察条件 |
| `evidence` | 数据源、周期、样本日期、独立 parent lineage |
| `counterexamples` | 失败、跳过、延续而非反转的案例 |
| `open_questions` | 仍需人工或数据验证的边界 |

## 晋级闸门

规则只有同时满足下面条件，才从 `audited` 提议晋级到 `validated` 或 `ready_for_system`：

1. 入场决定只使用触发前可见的信息；后续 MM、盈利、反转结果只能放在结果审计。
2. A/B/C、H/L 计数、交易区间与趋势背景有明确边界；区间内的摆动不能伪装成趋势第二腿。
3. 订单、实际成交、滑点/跳空、结构止损、第一障碍和 R/R 已冻结；第一障碍不能使用入场后的新高低点。
4. 有正例、跳过交易和失败/反例；不能只凭一张漂亮图表晋级。
5. 样本来自至少 3 个独立的 parent lineage；同一波行情的多周期或同一回调分支不能重复计数成独立样本。
6. 规则能被另一位研究者按文字重放，且不会需要补充“你应该知道我的意思”。
7. `ready_for_system` 还要求程序可以直接执行条件，不依赖视觉直觉词，例如“看起来很强”必须已经拆成可审计字段。

即使通过 `ready_for_system`，也只代表可以在 Codex Trading 中实现和回测；不代表收益保证，也不代表允许连接真实账户。

## 当前 PA Research 的交接状态

| 规则/主题 | 当前状态 | 说明 |
| --- | --- | --- |
| `ABC-CORE` | `hypothesis` / `replayed` | A 强度、B 类型、C 重新计数和第一障碍规则已形成，但跨样本未验证 |
| `TPB-H1/L1-STRONG-A` | `hypothesis` | 强 A 后受控 B 优先评估 H1/L1；仍需更多独立 lineage |
| `TPB-H2/L2-DEEP-LATE-CONTROLLED-B` | `hypothesis` | 深 B 但后段受控，可研究 H2/L2；不是自动授权 |
| `H3/L3` | `hypothesis` | L3 不等于三推衰竭；`2025-03-07/10` 与 `2026-03-26` 是延续风险反例/候选 |
| `GAP-RETEST-ORDER-BRANCH` | `audited` | 跳空后回测是新订单分支，不能沿用原始 stop 的 R/R；尚未转系统 |
| 三推楔形 | `hypothesis` | 需要逐推效率、位置和反向触发；不以“三次触碰”单独授权 |
| BOP/突破交易 | `observation` | 暂时隔离，不进入当前 ABC 主线 |

## 后续工作规则

- 新增研究文件时，优先新增一个独立案例或修正一个边界，不复制 Codex Trading 的整套文件。
- 若结论只是“这个案例不值得交易”，也要记录，因为它可以作为程序过滤条件；但不能把单个 no-trade 当成胜率证明。
- 只有当本文件的交接字段和晋级闸门完整，才创建面向 Codex Trading 的实现任务。
- 研究结论进入 Codex Trading 后，两个 Repo 的版本号和来源必须互相引用；实现结果不能反向改写原始研究结论。
- 真实订单、账户连接和 Execution Agent 永远需要另行确认，不由研究文件隐式授权。


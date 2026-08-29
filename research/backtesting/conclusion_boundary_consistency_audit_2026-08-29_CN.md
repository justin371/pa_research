# PA Research 统计结论、正例表述与授权边界一致性审计（2026-08-29）

日期：2026-08-29<br>
范围：`research/`、`strategy/`、`docs/` 和仓库 README 中的统计结论、胜率/正例表述、60% 待检验目标、状态别名与研究/交接边界<br>
状态：`research_only / document_maturity=provisional / no-new-positive`

## 一、审计边界

本轮只读检查现有 Markdown、validator 和回归测试，不下载或查询行情，不连接 Futu/OpenD，不看新图，不运行回放，不增加样本，不修改 CSV、历史结果或 engine 有效语义。本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent。

检查的重点是“文字是否会把研究状态误读成已验证胜率或可下单状态”，不是重新评价任何标的或交易机会。

## 二、当前 canonical 口径

| 表述 | 允许的含义 | 不能推导出的结论 |
| --- | --- | --- |
| `win_rate_eligible` | 结果记录中的资格/分层字段 | 不是胜率，也不是交易授权 |
| `validated win-rate: not-computable` | 当前统一的整体验证状态 | 不能被改写为已验证的正例或目标达成 |
| `no-new-positive` | 本轮没有新增可用于验证的正向证据 | 不等于所有历史路径都是失败 |
| `research_positive_conditional` | 值得继续人工研究的条件状态 | 不是生产规则、不是已验证策略 |
| `ready_for_system` | 交接枚举，只有完整晋级闸门通过才可使用 | 不等于收益保证，也不自动授权真实交易 |

`win_rate` 或 `validated_win_rate` 不是当前统一输出合同的胜率字段。历史文档中若出现旧的状态写法，只能在说明迁移时作为别名出现，不能继续作为活动字段。

## 三、检查结果

### 1. 发现并修复的状态别名

发现两类活动文案会让读者误以为它们是合同字段：

- `research/backtesting/contract_coverage_audit_2026-08-28_CN.md` 的 `validated_win_rate:` 是唯一残留的下划线形式；已改为统一叙述 `validated win-rate: not-computable`。
- 根 README、每日候选复核卡、ABC/H-L 历史结果审计和流程改进审计中的 `win_rate: not-computable` 已统一为同一 canonical 叙述。值仍然是 `not-computable`，没有新增、删除或重算任何结果。

### 2. 六个未重复写胜率状态的文件不是缺失

以下文件是 intake、视觉协议、冒烟验收或边界记录，不是回放结果报告：

1. `abc_bop_contract_intake_audit_2026-08-28_CN.md`；
2. `bop_contract_intake_audit_2026-08-28_CN.md`；
3. `h_l_lineage_visual_boundary_audit_2026-08-24_CN.md`；
4. `visual_recognition_round5_two_year_daily_2026-08-24_CN.md`；
5. `visual_recognition_smoke_test_2026-08-24_CN.md`；
6. `visual_pattern_triage_protocol_CN.md`。

它们已经分别写明 `intake_only`、`historical_context_only`、`observation_only`、`acceptance_pending`、`not-statistical` 或 `no-new-positive` 等边界。给这些流程文件机械补写“validated win-rate”反而会把视觉练习或准入清单误读成统计报告，因此保留原状态。

### 3. 60% 目标和正例表述未被升级

当前扫描到 60% 的 23 个 Markdown 文件，相关文本都属于待检验目标、历史描述性点估计或一致性审计；回放报告同时保留小样本、事件/空间/lineage 依赖和 `no-new-positive` 限定。没有发现把 60% 写成生产规则、长期验证胜率或收益保证的活动表述。`strategy/probability_principles_pages_1_7.md` 是学习参考，也明确不能直接换算成回测胜率。

历史 `100%`、`76.47%`、`60.00%`、`0%` 等数字继续只作各自批次的描述性结果；它们不能跨批次、跨事件、跨方向或跨 lineage 拼成验证分母。

### 4. 研究与授权边界仍然分开

`pattern_like`、`research_positive_conditional`、`valid_no_trade`、`observation_only`、`current_valid` 和 `ready_for_system` 在现有 schema、模板和审计中均有边界说明。人工图表识别、合同冻结、artifact 完整和历史回放结果都不能单独生成交易授权；缺少当前证据、触发、结构失效、首障碍、空间或完整交接闸门时，仍必须停留在研究层。

## 四、本轮修改与回归守卫

- 统一 5 处活动状态文案，未触碰 CSV、历史数值、engine 或回放有效语义；
- 将本审计加入 `research/`、`research/backtesting/`、`docs/` 和 `strategy/` 的入口索引；
- validator 现在拒绝 Markdown 中重新出现活动行 `validated_win_rate:` 或 `win_rate: not-computable`，并要求本审计和人工合同覆盖审计保留 canonical 结论与 PA Research 隔离声明；
- 回归测试检查旧活动别名、合同覆盖报告、60%/研究状态边界和本审计索引，防止“描述性结果 → 已验证胜率/交易授权”的文案漂移。

## 五、结论

```text
validated win-rate: not-computable
conclusion: no-new-positive
document_status: research_only
trade_state: not_authorized
```

本轮只修复统计状态的文字一致性和防回归检查，没有新增正向样本，也没有改变任何研究结论：PA Research 仍不能声称 H1/H2/L1/L2、ABC、BOP 或三推已经达到 60% 的验证目标，不能把历史描述性胜率当作生产规则，也不连接 Codex Trading、量化扫描器或 Execution Agent。

## 六、核心入口的统一摘要

本次版本/结论复核进一步把根 README、`docs/README.md`、`patterns/README.md`、`research/README.md`、`strategy/README.md` 和 `research/backtesting/README.md` 的共同摘要统一为：`v0.x` 规则/合同及研究引擎 `0.3.9` 只属于 PA Research 研究层（`PA Research only`），不是 Codex Trading 生产规则；`no-new-positive` 与 `validated win-rate: not-computable` 保持不变，`60%` 仅为待检验目标；不创建量化扫描器，不连接 Execution Agent。

回放 README 另将 `study_status`（`research_only / descriptive_only / not-validated`）与全局统计结论分开显示，避免把研究成熟度、统计状态和结果结论误读为同一枚举。该修复只改善入口可读性和防回归覆盖，不新增样本、结果或 engine 语义。

### 核心索引与活动模板追加复核

本轮继续检查 `docs/README.md`、`research/README.md`、`research/backtesting/README.md`、`strategy/README.md` 以及统一输出合同、日线候选卡、视觉复核卡和候选 inventory。发现并修正三处容易产生过度解读的文字边界：

- `research/README.md` 与 `research/backtesting/README.md` 现在直接写明当前 checkout 不含券商/账户真实交易日志；研究合同、历史回放结果和运行 metadata 不能代替真实交易日志；
- 回放 README 将 `results.csv` 的“成交/退出”明确改为回放器的模拟成交状态/模拟退出状态；
- `strategy/pattern_inventory_candidates.md` 与 `docs/common_context.md` 将 `validated evidence/specifications` 明确限定为未来或条件性状态，并保留当前 `validated win-rate: not-computable`。

统一输出合同、日线候选卡和视觉复核卡原有的事前/事后分界、canonical 状态轴和历史别名映射未发现残留问题，因此不作无证据改写。上述修复只涉及 PA Research 文档和防回归检查，不新增样本、成交、回放结果或 engine 语义；结论仍为 `no-new-positive`。

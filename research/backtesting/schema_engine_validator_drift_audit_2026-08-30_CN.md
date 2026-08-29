# PA Research schema / engine / validator 漂移审计（2026-08-30）

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`
结论：`no-new-positive`；`validated win-rate: not-computable`

```text
audit_scope: schema_engine_validator_drift_only
authority: PA Research canonical schema + current local engine/validator
engine_version: 0.3.9
backtesting_version: 0.6.6
matplotlib_version: 3.10.9
market_data_access: none
replay_run: none
csv_or_engine_change: none
```

## 1. 范围与事实

本轮只读取 PA Research 本地的统一 schema、活动模板、Markdown validator、回归测试、冻结
合同 CSV 的表头/字段、`pa_research_backtest/engine.py` 和固定依赖声明；不查询行情、不看新图、
不运行回放、不新增样本、不新增结果 artifact、不修改 CSV 或 engine，不读取或修改 Codex Trading。
本报告只处理字段、枚举、版本和研究记录/回放输入边界，不是候选名单、交易日志或胜率报告。

当前 engine 的事实接口如下：

- `ENGINE_VERSION` 为 `0.3.9`；固定回放依赖为 `backtesting==0.6.6`、`matplotlib==3.10.9`；
- `REQUIRED_CONTRACT_COLUMNS` 有 20 个字段，`BacktestContract` 有 30 个字段；多出来的字段是
  可选的市场依赖、EMA、H/L 位置、META 和入场前空间字段；
- engine 的支持集合包含 `direction`、兼容 `primary_pattern`、`internal_label`、EMA 斜率/闸门、
  空间、META、订单分支和缺口政策；当前回放订单分支仍只有 `stop_confirmation`、`limit_retest`
  和 `market_close`；
- engine 的基础非交易路径会输出 `evidence_status: not-a-trade`；已完成结果的
  `TRADE_RESULTS` 仍只有 `win / loss / scratch`；
- 当前冻结合同中的 `event_context` 已出现日期、复合限定、事件后重订价和核验状态等原始事前
  说明，`event_bucket` 才是回放摘要使用的闭合集合。

## 2. 已确认的漂移与最小修复

### 2.1 结果 evidence 枚举漏项

统一 schema 原来只列出 `comparable / excluded / excluded_incomplete_horizon / excluded_ambiguous /
observation_only`，漏掉 engine 对 no-fill、opening-skip 和 not-traded 基础路径使用的
`not-a-trade`。这会让文档读者误以为该结果值非法，或把非交易误读成 loss。

已将 `not-a-trade` 加入 schema，并明确它与研究者主动冻结的 `observation_only` 不同，也不进入
胜率分母；新增回归测试同时核对 engine 的实际字符串和 schema 声明。

### 2.2 BOP 非适用状态漏项

视觉卡和日线候选卡已经允许 `bop_state: not_applicable` 来表示非 BOP 记录，但统一 schema
的 BOP 字段列表漏掉了该值。已补齐，并写明 `not_applicable` 只能用于非 BOP 行；BOP 行仍必须
使用五种 BOP 专用状态之一。

### 2.3 `event_context` 被误写成封闭枚举

`event_context` 是原始事前事件笔记，不是有限枚举；当前 CSV 的真实值包括带日期、来源、复合
限定和审查状态的字符串。`event_bucket` 才负责 `ordinary_non_event`、`event_driven`、
`earnings_adjacent`、`event_unverified_or_pending` 等 canonical 分层。

已把统一 schema、日线/视觉卡、事件基础层、BOP/多周期/三推相关活动模板和事件字段审计中的
声明统一为“raw pre-entry event note”，并保留 `none / earnings / macro / gap / other /
unknown` 作为示例而不是封闭白名单。`event_context: none` 只表示没有事件说明，不自动证明
已经完成事件核验；未知、待定和未核实状态继续由 `event_bucket` 保守承接。

### 2.4 视觉兼容主标签漏列 H1/H2

`docs/visual_pa_review_card_CN.md` 的正文已经说明深审/历史记录可保留 `H1_L1`、`H2_L2` 等
兼容值，但 Pattern 分类模板原来漏列 `H1_L1` 和 `H2_L2`。已补齐 `primary_pattern` 和
`pattern_family` 的显示枚举，同时保留当前 `daily_candidate` 顶层只允许 `ABC_CONT / BOP`
的规则；具体 H1/H2/L1/L2 尝试仍写在 `internal_label`。

### 2.5 跨 Pattern 订单协议仍有活动旧字段

`research/order_contract_cross_pattern_audit_CN.md` 是 canonical 入口可达的历史研究层协议，
其统一订单卡原来仍以 `decision_time`、`timeframe_and_parent_contract`、`trigger_or_zone`、
`actual_or_assumed_fill`、`structural_stop_zone`、`space_to_first_obstacle` 和 `final_status`
作为活动字段，容易让读者把旧别名当作当前入口。

已将该卡迁移为 `as_of_time`、`timeframes_seen`/`contract_scope`、`new_trigger`、
`order_price_or_zone`、`actual_fill_or_open_skip`、`structural_invalidation`、`structural_stop`、
`rough_space_to_first_obstacle_R`、`research_state`、`trade_state` 和 `gate_result`。旧名称只留在
明确标注的历史映射说明中；validator 和回归测试现在拒绝这些旧名称以活动字段形式重新出现。

## 3. 研究字段与回放输入的显式边界

研究记录是回放合同的超集，不能因为字段相似就直接喂给 engine。冻结阶段必须显式投影：

| 研究记录 | 冻结回放输入 | 结果/摘要 | 约束 |
| --- | --- | --- | --- |
| `new_trigger` | `entry_trigger` | `planned_entry_trigger` | 触发价必须先冻结为有限数值；`market_close` 可留空 |
| `first_independent_obstacle` | `first_obstacle` | `first_obstacle` | 区域/文字必须先冻结为数值，不能由事后 `first_obstacle_hit` 回填 |
| `structural_stop` | `structural_stop` | `structural_stop` | 结果阶段不得反向改写入场前结构止损 |
| `pre_entry_space_R` / `space_status` | 同名可选字段 | 同名结果/摘要字段 | 不能由 `space_to_first_obstacle_R` 或 `realized_R` 倒推 |
| `actual_fill_or_open_skip` | 无直接映射 | `fill_status` | 研究注释不等于成交；结果状态由回放路径产生 |

`contract_scope`、`data_status`、`chart_scope`、`timeframes_seen`、`state_transition`、`bop_state`、
`branch_role`、`special_subtype`、`a_leg_quality`、`b_leg_class` 和 `b_leg_location` 是上游研究/
视觉字段，当前 engine 不把它们当作订单输入。loader 只构造 `BacktestContract` 声明的字段并忽略
未知 CSV 列；因此冻结 CSV 保留已登记的 provenance 超集，不代表 engine 已消费这些研究字段。
validator 允许该超集用于事前证据追踪，但回放输入仍以 20 个 required columns 和显式可选字段为准。

这一区分不改变当前冻结合同、价格文件、回放结果或统计分母；不把 `bop_state`、A/B 质量、
`special_subtype`、`state_transition` 或研究区间文字变成自动信号，也不创建量化扫描器。

## 4. 版本与历史快照口径

当前活动文档、engine、固定依赖和 validator 的版本声明均对齐 `0.3.9` / `0.6.6` / `3.10.9`。
仓库中较早的 engine 版本只保留在带有历史语境的审计报告或 artifact provenance 说明中；它们
不是当前 engine 入口，也不能覆盖本报告的 current snapshot。新增回归测试检查当前 engine 常量、
validator 支持集合和 canonical schema 的声明同时存在；不重写历史报告中的事实快照。

## 5. 验证与结论

本轮修复只涉及文档、validator 和回归测试；不修改 CSV、engine、价格、结果 artifact、交易日志
或任何胜率分母。提交前验证记录如下：

```text
targeted schema/contract/visual/index regression: 53 passed
full unittest suite: 328 passed
document validator: 311 Markdown files, 2164 links
compileall: passed
git diff --check: passed
```

```text
no-new-positive
validated win-rate: not-computable
PA Research only
no Codex Trading
no quantitative scanner
no Execution Agent
```

本审计不会赋予 PA Research 行情访问、自动图表识别、交易授权或 Execution Agent 连接能力。

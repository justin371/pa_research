# ABC 候选合同冻结复核（2026-08-28）

日期：2026-08-28<br>
范围：已进入 ABC/BOP intake 的 NFLX、TSM 两个 ABC/L1-like 候选<br>
状态：`research_only / candidate_freeze_review / contract_frozen=no / no-new-positive`

## 一、复核边界

本次只读取仓库已有的两份人工视觉案例、intake CSV 和回放合同说明，不重新下载行情、不引入新规则、不使用后续路径补写前置合同。只有在源记录对**同一订单分支**给出结果发生前的精确字段时，才把字段记为可冻结；价格区间、多个替代分支、研究代理和事后过程标签都不能直接变成冻结值。

回放合同要求的核心字段包括 `order_branch`、`entry_trigger`、`structural_stop`、`first_obstacle`、`target_price`、`max_hold_bars`、`gap_policy`、事件状态、`contract_frozen` 和 lineage。L1 还需要完整的 `>=2y` Daily 背景、重要高低点审查、EMA20/50/200 及 H/L EMA 闸门字段。`max_hold_bars` 不能从案例的日期窗口推断。

## 二、逐字段结果

| 合同字段 | NFLX 2025-03-28 | TSM 2025-03-26 | 冻结影响 |
| --- | --- | --- | --- |
| pattern / label / direction / decision date | `ABC_CONT / L1-like / short / 2025-03-28`，源记录一致 | `ABC_CONT / L1-like / short / 2025-03-26`，源记录一致 | 可保留为 intake 描述，不足以冻结合同 |
| 触发参考 | `96.63664` 下方可见；但盘中刺破与 `10:15` 收盘确认是不同成交假设 | 原 `177.22` 触发被开盘越过；`176.66` 开盘重订与更晚 15m 确认重订不同 | 触发参考存在，唯一成交分支未闭合 |
| `order_branch` / `gap_policy` | 源记录同时保留 sell-stop、收盘确认、limit-retest；不是单一 `stop_confirmation` | 原 stop 未按原价成交，旧 limit 未回测；开盘重订与 15m 确认重订必须分开 | 不能把一个候选行直接当成一个回放合同 |
| 结构止损 | B 高点 `99.87` 上方的研究区间 `100.8–101.2`，没有唯一精确值 | B 高点 `180.30` 上方的研究区间 `181.0–181.5`，没有唯一精确值 | 区间不是冻结的 `structural_stop` |
| 第一障碍 / `target_price` | 左侧支撑 `90.10–88.75`，粗略空间 `1.4R–1.9R`；没有选定唯一目标价 | 支撑簇 `167.99–165.05`，重订后粗略 `1.6R–2.5R`；没有选定唯一目标价 | 只能作空间证据，不能进入回放目标字段 |
| `max_hold_bars` | 源记录没有 | 源记录没有 | 不能从 `2025-03` 研究窗口倒推 |
| 事件 | 源记录有 Netflix 官方财报日期与过滤结论；不是 `none` | 源记录有 TSMC 官方财务日历与过滤结论；不是 `none` | 事件来源可追溯，但不能把它们与 ordinary-non-event 样本混写 |
| 结果 | 有首支撑到达的过程标签，但没有合同级 fill/exit/`trade_result`/`realized_R` | 有重订路径到达首支撑、原 stop/旧 limit 未成交的过程标签，但没有重订合同级 fill/exit/`trade_result`/`realized_R` | 事后路径不是冻结结果，也不增加胜率分母 |
| Daily / 左侧高低点 | 源窗口约为数月；有局部 A/B/支撑描述，不是完整 `>=2y` 审查 | 源窗口约为数月；有局部 A/B/支撑描述，不是完整 `>=2y` 审查 | `daily_context_window` 和 `major_high_low_review` 仍缺闭合证据 |
| EMA / H-L 人工字段 | 未给出 EMA20/50/200 审查及 `daily_ema20_slope`、`daily_ema50_slope`、`h_l_ema_slope_gate` 等 | 同样未给出 | L1 不能绕过这些必需字段 |
| lineage | 只有“同一 Daily ABC lineage”的叙述，没有 canonical `lineage_id` | 同样只有叙述；重订分支还需独立 lineage/合同标识 | 依赖控制尚未机器化 |
| 冻结状态 | `contract_frozen=no` | `contract_frozen=no` | 两者都不得进入回放 |

## 三、逐候选判定

### NFLX

源案例[`NFLX 空头 ABC/L1`](../nflx_bearish_abc_l1_no_gap_space_2025-02-14_2025-03-28.md)足以支持“方向性 A → 深但后段受控 B → L1-like 空头恢复”的视觉候选，也足以保留首支撑和粗略空间。但它同时记录了盘中 stop、收盘确认和 limit-retest 三种订单思路；intake 中原先的 `stop_confirmation` 会造成“分支已选定”的误读，现改为 `branch_choice_pending`。未补写精确止损、目标、最大持有期或结果。

判定：`candidate_pending / contract_frozen=no / do_not_replay`。

### TSM

源案例[`TSM 空头 ABC/L1`](../tsm_bearish_abc_l1_gap_reprice_space_2025-02-14_2025-03-28.md)清楚区分原始 stop 未按原价成交、旧价 limit 未回测，以及缺口接受后重订的研究路径。但 `176.66` 开盘重订和更晚 15m 确认重订仍是两个合同，intake 中原先的 `gap_reprice` 会造成“重订分支已经唯一确定”的误读，现改为 `reprice_branch_choice_pending`。未补写 gap policy、精确成交、止损、目标、最大持有期或重订合同结果。

判定：`candidate_pending / contract_frozen=no / do_not_replay`。

## 四、机器可读清单的变更

`abc_bop_contract_intake_2026-08-28.csv` 仍然是 intake-only，不是回放输入。此次只把 NFLX/TSM 的 `contract_branch` 改成待选状态，并把缺失字段扩展到 canonical contract 与 L1 人工字段；没有把任何行写成 `contract_frozen=yes`，没有新增 ABC/BOP 回放合同，也没有改变 H/L 统计。

下一次若要冻结，必须分别完成：

1. NFLX：在 sell-stop 与收盘确认之间选定唯一分支，并冻结精确成交、结构止损、首障碍目标、`max_hold_bars`、完整两年 Daily/EMA/H-L 字段和结果边界；
2. TSM：在开盘重订与 15m 确认重订之间选定唯一分支，冻结 `gap_policy` 及同一组字段；
3. 两者都要在结果发生前完成冻结，之后才可另写入正式回放 CSV；
4. 在此之前，`no-new-positive`、`validated win-rate: not-computable` 和“intake 不进分母”保持不变。

## 五、范围声明

本复核只属于 PA Research。它不创建量化扫描器、不自动识别图表、不连接 Execution Agent、不修改 Codex Trading，也不把历史路径审计冒充为胜率验证。

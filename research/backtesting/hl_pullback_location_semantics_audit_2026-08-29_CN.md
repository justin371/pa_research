# H/L 回调位置文本语义与方向边界审计（2026-08-29）

## 审计范围

本次只检查 PA Research 已冻结的 7 份 H/L 合同 CSV、对应 selection/replay 报告和统一字段文档，重点是 `h_l_pullback_location` 与方向、EMA 斜率、EMA gate、B-leg 字段的边界。没有下载行情、没有看新图、没有运行回放、没有增加样本，也没有修改 Codex Trading。

`h_l_pullback_location` 是人工可读的自由文本位置说明，不是受限枚举。它可以记录 EMA 重测、前期支撑/阻力、角色转换、事件后位置和其他历史上下文；它不能单独产生方向、EMA 闸门、首障碍空间或胜率资格。

## 60 条冻结合同的机器核对

7 份 CSV 共 60 行，位置字段 60/60 非空，当前没有 `unknown` 或 `pending` 位置值。明确方向词的覆盖如下：

| 位置文本家族 | 行数 | 方向分布 | 解释 |
| --- | ---: | --- | --- |
| `rising_EMA20` / `above_rising_EMA20` / `EMA20_retest` | 31 | `long=31` | 与多头 H1/H2 的 `long_pass` 或多头观察行一致 |
| `falling_EMA20` / `falling_EMA50` / `downward_EMA20` | 22 | `short=22` | 与空头 L1/L2 的 `short_pass` 一致 |
| 没有明确 EMA 方向词 | 7 | `long=1, short=6` | 由 gate 和价格位置上下文补充，不能反推 gate |

没有发现以下异常：

- 多头位置文本没有出现 `falling` 或 `downward`；
- 空头位置文本没有出现 `rising` 或 `upward`；
- 当前 60 行没有明确的 EMA 位置词与 `h_l_ema_slope_gate` 相反的记录；
- H1/H2、L1/L2 的方向和 EMA20/EMA50 斜率仍由 canonical 字段与 gate 决定，位置文本不覆盖它们。

## 支撑/阻力和历史 B 词的边界

7 条空头位置文本含 `support`：6 条明确写成 `role_reversal`、`turned_resistance` 或 `broken_support`，1 条是 `post_event_support_near_55`，并且该行的 raw/canonical 事件状态独立标为事件组。不能把这些词直接理解成“空头在未破支撑上追空”；应回到冻结的触发、结构止损、第一障碍和事件字段判断。

5 条位置文本含历史 B 质量词：

- DDOG `2023-07-24` 只在位置文本中出现 `controlled_B`，CSV 没有独立 `b_leg_class`；
- TOL、VEEV、CBOE、ROST 的位置文本分别重复了 `controlled_B` 或 `deep_late_controlled_B`，其中后四条另有独立的历史 `b_leg_class` 列。

这些词是历史可读描述，不是 `h_l_pullback_location` 的新枚举，也不把缺失的 `b_leg_location` 或 `b_leg_class` 自动补齐。质量、类别和位置仍是三个独立观察轴；`h_l_pullback_location` 不能替代 A/B 字段。

## selection/replay 报告核对

selection 报告把位置与 EMA、支撑阻力、事件和 B 质量作为解释性信息；replay 报告把 `h_l_ema_slope_gate` 用于资格，把触发/止损/第一障碍用于几何和结果。未发现报告把位置文本本身写成独立 B-leg 字段、EMA gate 或空间分母。

因此本次只补充统一文档的阅读规则和回归测试，不改历史 CSV、engine、结果或统计分母。位置字段缺失时仍保持 `pending`/观察边界；`fail_flat_or_opposite` 仍不进入胜率分母。

当前研究结论继续为 `no-new-positive`，`validated win-rate: not-computable`。这是 PA Research only；不修改 Codex Trading，不创建 quantitative scanner，不连接 Execution Agent，也不连接 Futu/OpenD。

Scope boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent; no Futu/OpenD.

# H/L A/B 质量、位置与 EMA 字段一致性审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 日线选股规则、统一输出 schema、共同视觉上下文、每日候选卡、视觉复核卡、`patterns/README.md` 与 16 个 pattern README、7 个 H/L 冻结合同 CSV、selection/replay 报告和当前回放 engine `0.3.9`<br>
状态：`research_only / audit_only / no-new-positive`

## 结论

本次只读取仓库内规则、模板、合同、报告和 engine，没有下载行情、看新图或运行回放。7 个 H/L 冻结合同共 60 条记录：A/B 质量字段只出现在 3 个较新 CSV 的 10 条记录中，使用的是历史写法；独立 `b_leg_location` 在 7 个 CSV 中均不存在；H/L 专属的 `h_l_pullback_location` 和 `h_l_ema_slope_gate` 则覆盖 60/60 条。当前 engine 的 H/L 最小回放合同不消费 A/B 质量或 `b_leg_location`，所以不能从结果、位置文本或缺失列倒推 A/B 质量。

发现的范围问题是字段职责和历史别名没有集中写清楚，而不是 engine 计算错误：

1. 当前 canonical 记录应分开使用 `a_leg_quality`、`b_leg_class`、`b_leg_location`；
2. `strong_A`、`ordinary_A`、`controlled_B`、`deep_late_controlled_B` 只存在于部分历史 H/L CSV 和对应选择说明中，必须作为登记过的历史别名解释，不能伪装成当前 canonical 枚举；
3. `h_l_pullback_location` 是 H/L 回调位置及历史说明字段，不能同时充当独立的 B 类别/位置字段；其中少数旧值把 `controlled_B`、`deep_late_controlled_B` 或 `event_aftershock` 混在位置文本中，也不能被机器静默拆回缺失列；
4. 16 个 pattern README 都继承统一输出 schema 和视觉复核卡，`patterns/README.md` 是共同字段索引；没有证据要求给每个 pattern README 复制一份不同的 A/B 枚举。

因此本次只补齐文档边界、历史别名登记、索引、validator 和回归测试；不改 CSV、不改 engine 有效语义、不新增样本或结果。

## 一、canonical 字段职责

| 字段 | 当前 canonical 口径 | 缺失/历史边界 |
| --- | --- | --- |
| `a_leg_quality` | `strong / ordinary / unclear / event_driven` | 历史 `strong_A`→`strong`、`ordinary_A`→`ordinary`；只用于解释，不回写 CSV |
| `b_leg_class` | `controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear` | 历史 `controlled_B`→`controlled`、`deep_late_controlled_B`→`deep_but_late_controlled`；只用于解释，不增加回放字段 |
| `b_leg_location` | 独立的 B 所在价格/结构位置说明 | 当前 60 条合同均无此列；不能由 `h_l_pullback_location` 或结果补齐 |
| `h_l_pullback_location` | H1/H2/L1/L2 的回调位置和已有人工说明 | 60/60 非空；它不是 A/B 质量枚举，历史混合说明保持原样 |
| `h_l_ema_slope_gate` | `long_pass / short_pass / fail_flat_or_opposite / pending / not_applicable`；H/L 需按方向使用 | 60/60 非空，其中 `long_pass=27`、`short_pass=28`、`fail_flat_or_opposite=5`；不把 gate 反推为强 A 或受控 B |

`event_driven` 在 `a_leg_quality` 中只是 A 腿受事件影响的质量说明；事件统计仍由 raw `event_context` 派生的 canonical `event_bucket` 负责。它与 `special_subtype`、`h_l_ema_slope_gate` 和 `b_leg_class` 都不是同一字段。

## 二、7 个 H/L 冻结合同的机器事实

| CSV | 行数 | `a_leg_quality` | `b_leg_class` | `b_leg_location` | `h_l_pullback_location` | `h_l_ema_slope_gate` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `hl_contracts_2026-08-26.csv` | 5 | 缺列 | 缺列 | 缺列 | 5/5 | 5/5 |
| `hl_contracts_batch2_2026-08-26.csv` | 3 | 缺列 | 缺列 | 缺列 | 3/3 | 3/3 |
| `hl_large_contracts_2026-08-27.csv` | 37 | 缺列 | 缺列 | 缺列 | 37/37 | 37/37 |
| `hl_next_contracts_2026-08-27.csv` | 5 | 缺列 | 缺列 | 缺列 | 5/5 | 5/5 |
| `hl_next2_contracts_2026-08-27.csv` | 2 | 2/2 | 2/2 | 缺列 | 2/2 | 2/2 |
| `hl_next4_contracts_2026-08-27.csv` | 2 | 2/2 | 2/2 | 缺列 | 2/2 | 2/2 |
| `hl_next5_contracts_2026-08-27.csv` | 6 | 6/6 | 6/6 | 缺列 | 6/6 | 6/6 |
| **合计** | **60** | **10/60** | **10/60** | **0/60** | **60/60** | **60/60** |

10 条含 A/B 字段的历史原值分布为：`strong_A=9`、`ordinary_A=1`；`controlled_B=9`、`deep_late_controlled_B=1`。这些值按上表映射阅读，但没有被改写成新的当前合同列，也没有进入 engine 的胜率分母。

`h_l_pullback_location` 的 60 条原值全部非空，但其中 5 条包含 `controlled_B`、1 条包含 `deep_late_controlled_B`、1 条包含 `event_aftershock`。这些是旧人工说明中的混合文本；当前 engine 不解析它们，也不能把它们当作独立 `b_leg_class`、`b_leg_location` 或事件资格。

## 三、selection/replay 和 16 个 pattern README 核对

selection/replay 报告的分层仍按 `internal_label`、方向、事件、空间和 EMA gate 组织，没有用 A/B 字段计算胜率。`hl_next2_selection_2026-08-27_CN.md` 中出现 `ordinary_A`、`strong_A` 和 `deep_late_controlled_B`，与对应 CSV 一样保留为历史说明；它们不应在报告中被读成 schema 的新枚举。其他 H/L selection/replay 报告没有形成独立 A/B 统计，因此不补造统计或结果。

16 个 pattern README 均继续指向统一输出 schema 和视觉复核卡，由共同上下文规定 A/B 字段职责；共同索引现在同时登记 canonical 字段和历史别名边界：

- [`01_h1_l1_first_entry`](../../patterns/01_h1_l1_first_entry/README.md)
- [`02_h2_l2_second_entry`](../../patterns/02_h2_l2_second_entry/README.md)
- [`03_abc_continuation`](../../patterns/03_abc_continuation/README.md)
- [`04_range_edge_second_entry`](../../patterns/04_range_edge_second_entry/README.md)
- [`05_failed_breakout_climax`](../../patterns/05_failed_breakout_climax/README.md)
- [`06_breakout_pullback_bop`](../../patterns/06_breakout_pullback_bop/README.md)
- [`07_mtr_reversal`](../../patterns/07_mtr_reversal/README.md)
- [`08_three_push_h3_l3`](../../patterns/08_three_push_h3_l3/README.md)
- [`09_vcp_minervini`](../../patterns/09_vcp_minervini/README.md)
- [`10_final_flag`](../../patterns/10_final_flag/README.md)
- [`11_opening_reversal`](../../patterns/11_opening_reversal/README.md)
- [`12_channel`](../../patterns/12_channel/README.md)
- [`13_inside_bar_two_bar_reversal`](../../patterns/13_inside_bar_two_bar_reversal/README.md)
- [`14_triangle_expanding_range`](../../patterns/14_triangle_expanding_range/README.md)
- [`15_double_top_bottom`](../../patterns/15_double_top_bottom/README.md)
- [`16_head_shoulders_rounded`](../../patterns/16_head_shoulders_rounded/README.md)

独立主题可以把 A/B 质量当背景观察，但不能因为一个 pattern README 提到强 A 或受控 B，就把其样本并入 ABC/H-L 统计或回放合同。

## 四、修复和保留的边界

1. 在规则、统一 schema、共同上下文、每日候选卡、视觉复核卡和 `patterns/README.md` 中明确 canonical A/B 字段分离及历史别名映射。
2. 在回放 README 中明确 A/B 字段不是当前 H/L 最小回放必需列；旧合同缺失时保留缺失，不能从 `h_l_pullback_location`、EMA gate 或结果回填。
3. validator 对已经存在的可选 A/B 列只接受 canonical 值或本审计登记的历史别名；缺列不报错，未知值报错，位置字段仍不被机器推断。
4. 新增回归测试固定 7 个 CSV 的覆盖事实、别名映射、EMA gate 分布、16 个 README 的共同 schema 指针和报告边界。

没有改写任何冻结 CSV，没有把 50 条缺失 A/B 的历史记录伪造为 `ordinary`，没有把 60 条缺失 `b_leg_location` 的记录补成位置统计，也没有新增回放样本、胜率、盈亏比或正向结论。

## 五、验证与项目范围

验证目标：全量 unittest、Python 编译检查、文档 validator 和 `git diff --check` 均应通过；若不能通过，本审计不应提交。当前结论继续是 `no-new-positive`，`validated win-rate: not-computable`。

本审计只属于 **PA Research**（`PA Research only`）。范围声明：`no Codex Trading`、`no quantitative scanner`、`no Execution Agent`、`no Futu/OpenD`。

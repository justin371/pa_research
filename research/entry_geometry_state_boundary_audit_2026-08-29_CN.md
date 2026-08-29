# 入场几何与不交易状态边界审计（2026-08-29）

结论：本轮只审计 PA Research 的统一输出合同、两张审查卡、共同上下文、pattern 索引和 16 个 pattern README。发现并修正了入场几何别名、首障碍与粗略 R/R 顺序，以及 `observation_only` / `valid_no_trade` 的解释漂移；没有下载行情、查看新图、运行回放、增加样本或改变 pattern/engine 的有效语义。结论继续保持 `no-new-positive`，`validated win-rate: not-computable`。

## 一、统一几何顺序

所有 pattern 的预入场记录现在都按以下顺序理解：

```text
structural_invalidation
→ structural_stop
→ first_independent_obstacle
→ pre_entry_space_R / space_status
→ rough_R_R / target_layers
```

最近独立支撑/阻力或其他实际障碍优先于更远的 measured move、区间另一侧或后续结果。研究阶段可以把止损和障碍保留为区域、`pending` 或 `unknown`；冻结回放合同前必须收敛成 engine 要求的数值字段，不能用事后路径倒推入场前空间。

## 二、发现与修复

1. `docs/daily_candidate_review_card_CN.md` 原来使用 `trigger_price_or_zone`、`structural_stop_or_zone`，且没有直接列出 `new_trigger`、`order_price_or_zone`、`pre_entry_space_R`、`rough_R_R` 和 `target_layers`。现已改为 canonical 字段，并把区域/距离字段明确标为审查阶段的补充信息。
2. `docs/visual_pa_review_card_CN.md` 原来的 `stop_zone`、`stop_price_or_area` 和 `space_to_first_obstacle` 容易与统一合同及结果阶段字段混淆。现已使用 `structural_stop`、`structural_stop_zone`、`rough_space_to_first_obstacle_R`、`pre_entry_space_R`、`space_status` 和 `rough_R_R`。
3. 16 个 pattern 的最小协议仍然只保留差异字段，但 `patterns/README.md` 现在明确列出 `location`、`space`、`trigger`、`prior_boundary`、`first_magnet` 等说明性短字段到 canonical 几何字段的映射；完整案例仍必须套用统一输出合同。
4. 16 个 pattern README 统一补充状态边界：证据或合同不完整时使用 `pending`/`observation_only`；形态、方向和入场几何可复核但已知硬闸门否决交易时使用 `valid_no_trade`。两者都不建立订单，不能互换。
5. 视觉复核卡的当前研究状态改为使用 canonical `research_state` 轴，不再用单独的 `final_state` 或旧状态表制造第二套当前枚举；旧案例别名仍只在映射说明中保留。

## 三、状态边界

- `observation_only`：关键图表、事件、方向、触发或空间证据尚不完整，或只保留形态学习价值，尚未建立交易合同；必要时可同时写 `pending`。
- `valid_no_trade`：形态、方向和入场几何已经足够复核，但首障碍过近、结构止损过宽、事件排除或订单合同等已知硬闸门明确阻止新交易；它不是亏损结果。
- `research_state`、`trade_state` 和 `gate_result` 继续分轴记录。状态不能替代首障碍、空间、止损或触发字段，也不能把形态相似度当作胜率。

## 四、验证与范围

- 新增回归测试覆盖统一几何字段、16 个入口的状态边界和索引映射。
- 文档 validator 增加 canonical 几何字段及旧别名边界检查，并保持 PowerShell 5.1/7 的 UTF-8 读取兼容。
- Scope: PA Research only; no Codex Trading, no quantitative scanner, no Execution Agent。

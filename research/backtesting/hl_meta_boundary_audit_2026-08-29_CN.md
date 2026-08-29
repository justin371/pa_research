# H/L META 字段与授权边界审计（2026-08-29）

## 审计范围

本次只检查 PA Research 已冻结的 7 份 H/L 合同 CSV、对应 selection/replay 报告、META 说明和 validator/engine 的现有边界。没有下载行情、没有看新图、没有运行回放、没有增加样本或统计分母，也没有修改 Codex Trading。

`meta_confluence` 是位置/背景汇合字段，不是交易触发器。当前冻结合同的 canonical 值只有 `present`、`absent`、`unknown`；`pending` 属于整体视觉复核、触发或 gate 尚未完成的状态，不是 META 字段值。冻结 H/L 合同必须填写一个合法 canonical 值；证据不足时保留 `unknown`，同时可以在整体状态字段保留 `pending`。

## 60 条冻结合同的机器核对

7 份 CSV 共 60 行，`meta_confluence` 分布如下：

| `meta_confluence` | 行数 | `meta_zone` / `meta_components` | 解释 |
| --- | ---: | --- | --- |
| `present` | 49 | 49/49 都非空；39 行有 3 个、10 行有 2 个不同的组件名称 | 通过现有字段/validator 的至少两个来源边界；来源是否真正独立仍由人工图表审查负责 |
| `absent` | 11 | 11/11 都为空 | 明确记录没有可登记的 META，不等于方向或 H/L gate 失败 |
| `unknown` | 0 | 当前没有 | 当前批次没有保留未知 META 的冻结行 |
| `pending` | 0 | 当前没有 | `pending` 未被写入 META 字段；它仍只属于整体状态轴 |

### 与 EMA gate 的交叉核对

| META | `long_pass` | `short_pass` | `fail_flat_or_opposite` | 合计 |
| --- | ---: | ---: | ---: | ---: |
| `present` | 23 | 21 | 5 | 49 |
| `absent` | 4 | 7 | 0 | 11 |

5 条 `present` 但 `fail_flat_or_opposite` 的 H/L 行说明 META 不能覆盖 EMA 方向闸门；11 条 `absent` 中仍有 4 条多头通过和 7 条空头通过，说明 META 缺失也不能自动否决方向。当前没有 `pending` 或反向 pass gate 的交叉异常。

### 与空间字段的交叉核对

| META | 空间字段未提供 | `strict_ge_1R` | `borderline_ge_1R` | 合计 |
| --- | ---: | ---: | ---: | ---: |
| `present` | 45 | 4 | 0 | 49 |
| `absent` | 5 | 5 | 1 | 11 |

旧批次的空白空间字段表示该合同没有提供显式 `space_status`/`pre_entry_space_R`，不能被读成“空间 blocked”或“空间通过”。`present` 不产生空间资格；`absent` 也不阻止独立空间字段存在。空间仍需按首障碍、结构止损和入场几何单独判断。

### META 组件与位置/方向

组件中没有发现多头使用 `falling`/`downward` 或空头使用 `rising`/`upward` 的方向词冲突；也没有发现组件方向词与 H/L EMA pass gate 相反的记录。位置文本、EMA 斜率、`h_l_ema_slope_gate` 和空间字段仍是独立观察轴；META 组件不能把 `h_l_pullback_location`、EMA gate 或空间字段偷偷合并成一个资格。

## selection/replay 报告核对

抽查 7 批 H/L selection/replay 报告及历史 intake/字段审计后，未发现报告把 `META present` 单独写成入场触发、结构止损、首障碍空间或授权条件。现有报告把 META 与触发、止损、事件和空间分开，并对 `n=1`、`n=2` 或失败结果保留不可验证边界。

本轮修正了一处说明歧义：`strategy/meta_multiple_edge.md` 原来把“到第一目标的空间”列在 META 常见优势中，容易与 `meta_components` 混淆；现已明确空间是独立 trade-geometry gate，不能为了得到 `meta_confluence=present` 而加入组件。没有修改 CSV、engine 有效语义、历史结果或统计分母。

## 结论

现有 60 条冻结合同的 META 状态、组件数量、EMA gate 和空间分层没有发现数据异常。当前结论继续为 `no-new-positive`，`validated win-rate: not-computable`。META 只能作为合格候选的位置/背景分层，不能替代方向、触发、止损、首障碍、空间或执行授权。

Scope boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent; no Futu/OpenD.

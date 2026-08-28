# 多头 ABC/H1/H2 合同审计（2026-08-28）

日期：2026-08-28<br>
范围：V、NVDA、KLAC、CRWD 四个已有多头人工视觉案例到正式回放合同的准入复核<br>
状态：`research_only / candidate_intake / contract_frozen=no / no-new-positive`

## 一、复核原则

本次只使用仓库已有的人工视觉记录，不重新抓取行情，也不把同一图表在不同 pattern 目录中的描述当成独立样本。目标是找出一条能与 NFLX/TSM 空头条件案例对照的多头候选，但“形态像”不等于“合同已冻结”。

正式冻结至少要有：唯一的 `order_branch`、结果发生前的精确 `entry_trigger`、`structural_stop`、`first_obstacle/target_price`、`max_hold_bars`、事件字段、完整 `>=2y` Daily/重要高低点/EMA20/50/200 人工审查、lineage 和机器可读结果边界。低周期窄止损不能替代 ABC/H2 的母级结构止损。

## 二、四个候选的逐案结论

| 候选 | 视觉证据 | 合同证据 | 主要缺口 | 裁决 |
| --- | --- | --- | --- | --- |
| V 2024-05-15 | 普通/方向性 A；深但后段开始稳定 B；H2-like 恢复；低周期触发可读 | `273.338` 附近低周期触发、`269.15` B 低点、`276.89–277.72` 首阻力；粗略只有 `0.85R–1.05R` | 日线与低周期分支未选定；事件未闭合；没有完整两年、EMA/H-L 字段、最大持有期和结果 | `boundary / contract_frozen=no` |
| NVDA 2024-09-24 | 强 A；深但后段受控 B；第一次尝试失败后第二次 H2 恢复；SOXX 同向 | `116.81` 原方向分支和 `117.27` 低周期确认分支；日线止损约 `112.5` 时首阻力约 `0.9R`，低周期 `114.8` 另有约 `1.9R` | 两种 thesis 不能事后择优；事件未闭合；精确订单、目标、最大持有期、完整两年/EMA/H-L 字段和结果缺失 | `dual-stop boundary / contract_frozen=no` |
| KLAC 2025-06-03 | 强 A；H1 后在重复支撑/EMA 区形成 H2；`06-03` 15m 有跟随 | 约 `75.90` buy-stop、约 `72.00` 结构止损、`79.03–79.79` 首阻力；日线粗略 `0.8R–1.0R` | buy-stop 与收盘/低周期确认分支未选定；目标和最大持有期未冻结；事件、两年 Daily、EMA/H-L、lineage、结果字段不完整；同一窗口已有独立 H/L 合同，不能复用 | `conditional / highest-priority-after-CRWD / contract_frozen=no` |
| CRWD 2024-10-03 | 强 A；深 B 前段压力强、后段在 `68.17` 附近稳定；H1-like 失败后 H2-like 恢复；15m 跟随清楚 | 约 `70.54` buy-stop 或后续 15m 收盘确认；结构止损观察区 `67.4–67.8`；首阻力 `75.11–75.54`，粗略约 `1.5R–1.9R` | 两个订单分支、精确 stop/target、最大持有期、incident/事件闭环、完整两年 Daily/EMA/H-L、lineage 和机器结果未冻结 | `conditional / highest-priority long / contract_frozen=no` |

## 三、重点判断

### V：触发真实，但第一阻力先否决

[`VISA 多头 ABC/H2-like 边界`](../v_bullish_abc_h2_no_gap_first_obstacle_boundary_2024-05-06_2024-05-17.md)的价值是证明低周期触发可以真实存在，而不是把“没有成交”误判成“没有形态”。但日线触发分支更晚、第一阻力更近；即使低周期触发能重建，也不能抹掉 `276.89–277.72` 的首阻力。它是边界样本，不是多头基准。

### NVDA：低周期几何不能替代日线 thesis

[`NVDA 多头 H2 条件候选`](../nvda_bullish_h2_60m_conditional_2024-09-11_2024-09-25.md)同时描述了宽日线结构止损和窄低周期止损。两者分别对应不同交易 thesis；如果没有在结果发生前选择其中一个，就不能用约 `1.9R` 的低周期几何拯救约 `0.9R` 的日线几何，也不能把两个结果合并。

### KLAC：视觉质量强，但不得借用 H/L 冻结合同

[`KLAC H2 Bull-Flag`](../klac_h2_case_study_2025-05-07_2025-06-03.md)是很好的多头视觉候选：A 有方向性、B 在重复支撑/EMA 附近形成第二次测试、`06-03` 有确认和跟随。但它的首阻力只有边界空间，而且仓库另有 H/L 研究批次的 KLAC 合同。后者的主标签、触发路径和统计归属不同，不能直接转成 `ABC_CONT`；否则会把同一 episode 重复计数。

### CRWD：目前最值得补齐的多头候选，但仍未冻结

[`CRWD 多头 H2-like`](../crwd_bullish_h2_deep_b_late_stabilization_2024-09-11_2024-10-11.md)在四个案例中最接近条件性多头合同：A 方向清楚，B 虽深但后段稳定，第一次尝试失败后出现新的位置测试，`10-02`/`10-03` 触发与跟随可读，首阻力相对 V/KLAC 更有空间。

不过它仍不是正式回放合同。`70.54` 盘中 buy-stop 和 15m 收盘确认必须二选一；`67.4–67.8` 是止损观察区而非唯一 stop；`75.11–75.54` 是阻力区而非已冻结目标；`max_hold_bars`、两年左侧审查、EMA20/50/200 与 H/L 闸门、lineage 及机器化结果边界都没有在源记录中闭合。`2024-07-19` incident 和财报背景也不能被压缩成普通 `none`。

## 四、机器可读清单

`abc_bop_contract_intake_2026-08-28.csv` 已加入 KLAC 与 CRWD 两行，并扩展 V/NVDA 的缺失字段。四条多头行都标记 `primary_pattern=ABC_CONT`、`contract_frozen=no`；它们是 ABC/H1/H2 intake，不进入 H/L 冻结 CSV，也不增加胜率分母。

当前优先级：

1. CRWD：先选择 buy-stop 或 15m 收盘确认，再补精确止损、目标、最大持有期、事件/事故、两年 Daily、EMA/H-L、lineage 和结果；
2. KLAC：先解决 ABC 合同与既有 H/L 合同的独立性，再审查首阻力是否足够；
3. NVDA：先选日线或低周期 thesis，不能保留双止损；
4. V：作为首阻力边界保留，不为增加多头样本而冻结。

## 五、最终结论

本轮没有冻结新的多头 ABC/H1/H2 合同。CRWD 是最高优先级的条件候选，KLAC 是次级条件候选，V/NVDA 是有效边界；四者均保持 `contract_frozen=no`。多头对照尚未形成新的验证分母，`no-new-positive` 与 `validated win-rate: not-computable` 不变。

## 六、范围声明

本审计只属于 PA Research。它不修改规则、不创建量化扫描器、不连接 Execution Agent、不修改 Codex Trading，也不把 H/L、ABC、BOP 或三推的结果混在一起。

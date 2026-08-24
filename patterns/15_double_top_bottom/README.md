# Double Top / Double Bottom / 双顶双底

状态：`independent-pa / visual-research / provisional / not-quantitative`

双顶/双底首先是“同一结构区域的两次有分离测试”，不是看到两个相近高点/低点就自动反转。它可以属于区间边缘、MTR、Final Flag 或普通回调中的局部结构；父级状态、位置、第二次确认和第一障碍决定是否值得交易。

## 最小定义

```text
父级背景与主要位置
→ 第一次测试
→ 中间摆动/清楚分离
→ 第二次测试
→ 反向尝试与第二次确认
→ 结构止损、第一障碍和交易合同
```

- 两次测试不要求精确同价，可以略高、略低或一次刺破后收回；
- 两次之间必须有可见反应/中间摆动，不能只是连续影线；
- 第二次测试应仍在同一母级结构区域；若已离开并建立新趋势，旧双顶/双底叙事重置；
- 双顶/双底是位置和形状描述，不单独授权做空或做多。

## 状态分流

| 状态 | 证据 | 默认处理 |
| --- | --- | --- |
| `ordinary-pullback` | 原趋势仍有方向和跟随，第二次测试未破坏主要结构 | 优先 H1/H2 或 L1/L2 延续 |
| `range-edge-double-top-bottom` | 父级区间成熟，第二次测试在上沿/下沿 | 区间边缘二次入场；中部不交易 |
| `final-flag-candidate` | 长趋势末端压缩/窄平台，最后一次原方向尝试待确认 | 接受则延续/BOP，失败才审计反向 |
| `mtr-candidate` | 成熟趋势、主要位置、反向结构破坏、第二次确认和空间同时出现 | 反向 stop 或结构回测 limit |
| `reversal-attempt` | 只有第二次测试后第一根反向 K | 先观察，不宣布 MTR |
| `failed-thesis` | 原方向强收盘越过第二次测试并接受 | 取消反向假设，切换延续/BOP |
| `range-transition` | 两次测试后高重叠、双方反复、父级未定 | 改用区间/过渡逻辑 |

## 反转确认

第二次测试后的第一根反向 K 只记为 `reversal-attempt`。更可靠的确认包括：

- 反向 stop 突破信号 K 或中间摆动/颈线；
- 第一次反向跟随不足后，再次反向突破；
- 失败突破重新回到原区间，并在边缘形成二次入场；
- 回测双顶/双底颈线或角色转换边界后守住。

MTR 需要成熟趋势、重要位置、反向结构破坏、第二次确认、接受/跟随和空间。Final Flag 更强调趋势末端压缩；普通趋势中段小旗形不自动叫 Final Flag。区间边缘双顶/双底先按区间逻辑，不强行升级 MTR。

## 订单与风险

- `stop-confirmation`：第二次测试形成信号 K 后，在反向一侧等待触发；记录原始触发与实际成交；
- `limit-retest`：颈线、失败突破边界或支撑阻力转换已清楚后，单列回测合同；未回测前不假设成交；
- `market/close-confirmation`：反向收盘很强、结构破坏且首障碍仍有空间时才研究；
- `observation-only`：形状有但位置不清、父级是区间中部、首障碍不足、事件/跳空改变几何，或原方向已重新接受。

结构止损要放在第二次测试极端或母级主要高/低点外，不能压在反向 K 的小尾巴里。第一独立支撑/阻力先于颈线目标和 MM；首障碍不足约 1R 记为 `valid_no_trade`，约 2R 只是完整波段参考。

## 与相邻 pattern 的边界

- **三推/H3-L3**：三次测试的次数与压力状态另行审计；双顶/双底只描述两次有分离测试，不能互相替代。
- **区间边缘二次入场**：父级成熟区间时优先用区间边缘逻辑，区间内部高低点不继承趋势腿数。
- **MTR**：双顶/双底只是位置证据；结构破坏和第二次确认才可能升级 MTR。
- **Final Flag**：需要长趋势和末端压缩；普通回调或区间边缘双顶不自动叫 Final Flag。
- **ABC/H1-H2**：原趋势仍强且第二次测试未破坏结构时，优先视为延续，而非反转。
- **BOP**：原方向强收盘越过第二次测试并接受后，旧反向 thesis 失效。

## 当前案例入口

- [`TSLA 2024-03-04–03-14`](../../research/tsla_bearish_abc_case_2024-03-04_2024-03-14.md)：区间上沿双顶/失败突破与 L2，条件性反向候选但过程先止损；
- [`RBLX 2024-03-18–04-05`](../../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)：区间下沿双底样，首障碍与信号质量否决；
- [`NFLX 2024-08-05–09-26`](../../research/nflx_three_push_top_boundary_2024-08-05_2024-09-26.md)：高位多次测试/Final Flag/MTR 边界，首支撑拥挤；
- [`TSLA 2025-09-08–09-12`](../../research/tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)：阻力下双高/多推观察被突破接受改写为 BOP；
- [`KLAC 2025-10-14–10-24`](../../research/klac_h1_case_study_2025-10-14_2025-10-24.md)：普通趋势旗形/浅回调对照，不是双顶反转；
- [`ASML 2025-05-19–06-13`](../../research/asml_h3_l3_range_transition_boundary_2025-05-19_2025-06-13.md)：双底样测试进入区间过渡，不冻结 MTR；
- [`PLTR 2024-12-24–2025-01-08`](../../research/pltr_bearish_abc_l1_ordinary_a_boundary_2024-12-24_2025-01-08.md)：B 内近似双顶，但主要仍是普通 A 后 L1，说明局部双顶不能替代背景。

专项证据审计见 [`Double Top / Double Bottom 专项视觉证据审计`](../../research/double_top_bottom_visual_evidence_gap_audit_2026-08-24_CN.md)，比较框架见 [`双顶/双底、MTR 与 Final Flag 视觉边界对照`](../../research/double_top_bottom_mtr_final_flag_comparison_CN.md)。

本目录只服务 PA Research 的视觉识别、案例复核、订单语义和 no-trade 判断，不建立量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

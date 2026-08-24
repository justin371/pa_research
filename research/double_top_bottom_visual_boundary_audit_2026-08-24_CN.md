# Double Top / Double Bottom / 双顶双底视觉边界复核

日期：`2026-08-24`  
状态：`visual-research / provisional / not-statistical`

双顶/双底首先是“同一结构区域的两次有分离测试”，不是看到两个相近高点/低点就自动反转。它可以属于区间边缘、MTR、Final Flag 或普通回调；父级状态、第二次确认和第一障碍决定是否值得交易。

## 1. 最小定义

```text
父级背景与主要位置
→ 第一次测试
→ 中间摆动/清楚分离
→ 第二次测试
→ 反向尝试与第二次确认
→ 结构止损、第一障碍和交易合同
```

- 两次测试不要求精确同价，可以略高、略低或一次刺破后收回；
- 两次之间必须有可见反应/中间摆动，不能只是连续影线或高重叠；
- 第二次测试应仍在同一母级结构区域；离开并建立新趋势后，旧双顶/双底叙事重置；
- 双顶/双底是位置和形状描述，不单独授权做空或做多。

## 2. 分类状态

| 状态 | 证据 | 默认处理 |
| --- | --- | --- |
| `ordinary-pullback` | 原趋势仍有方向和跟随，第二次测试未破坏主要结构 | 优先 H1/H2 或 L1/L2 延续 |
| `range-edge-double-top-bottom` | 父级区间成熟，第二次测试在上沿/下沿 | 区间边缘二次入场，中部不交易 |
| `final-flag-candidate` | 长趋势末端压缩/窄平台，最后一次原方向尝试待确认 | 接受则延续/BOP，失败才看反向 |
| `mtr-candidate` | 成熟趋势、主要位置、反向结构破坏、第二次确认和空间 | 反向 stop 或结构回测 limit |
| `reversal-attempt` | 第二次测试后只有第一根反向 K | 观察，不宣布 MTR |
| `failed-thesis` | 原方向强收盘越过第二次测试并接受 | 取消反向假设，切换延续/BOP |
| `range-transition` | 两次测试后高重叠、双方反复、父级未定 | 改用区间/过渡逻辑 |

如果原方向强势收盘越过第二次测试并获得跟随，双顶/双底反转假设必须结束；不能继续沿用旧的 MTR 或区间空头/多头剧本。

## 3. 反转确认与相邻 pattern

第二次测试后的第一根反向 K 只记为 `reversal_attempt`。更可靠的确认包括：

- 反向 stop 突破信号 K 或中间摆动/颈线；
- 第一次反向跟随不足后，第二次反向再次突破；
- 失败突破重新回到原区间，并在边缘形成有跟随的二次入场；
- 回测双顶/双底颈线或角色转换边界后守住。

MTR 需要成熟趋势、重要位置、反向结构破坏、第二次确认、接受/跟随和空间。Final Flag 更强调趋势末端压缩；普通趋势中段的小旗形不自动叫 Final Flag。区间边缘双顶/双底先按区间逻辑，不强行升级 MTR。

三推/H3-L3 描述三次测试的数量和压力状态；双顶/双底只描述两次有分离测试，不能用一个标签重复计分。颈线/中间摆动是确认和管理位置，不等于必到目标；左侧第一独立障碍优先于远端 MM。

## 4. 订单和风险合同

### `stop-confirmation`

第二次测试形成信号 K 后，在反向一侧等待触发。冻结原始触发价、实际成交价、是否跳空越过触发，以及结构止损所在的主要高/低点外。

### `limit-retest`

只有颈线、失败突破边界或支撑阻力转换已经清楚时，才单列回测限价单。未回到区域前不假设成交；跳空后旧合同作废，不能用理想触发价计算 R/R。

### `market/close-confirmation`

只在反向收盘很强、结构已经破坏、等待会明显错过且第一障碍仍有空间时研究。大 K 同时是事件/高潮 K 时，优先降级或观察。

### `observation-only`

只有形状、父级是区间中部、首障碍不足约 `1R`、原方向已经重新接受、或事件/跳空改变几何时，输出 `valid_no_trade`。

结构止损应放在第二次测试极端或母级主要高/低点外，不能压在反向 K 的小尾巴里。目标顺序是第一独立支撑/阻力、颈线/中线或最近磁铁，然后才看 MM；约 `2R` 只是完整波段参考。

## 5. 案例裁决

### 5.1 TSLA `2024-03-04–03-14`：区间上沿双顶/失败突破候选

入场前价格在约 `190–205` 反复交易，`2024-02-27` 上探约 `205.60`，父级更接近区间上沿而非开放趋势中段。`03-04` 后空头反应，第一次下行失败后 `03-11–13` 出现第二次向下尝试，可以记为区间上沿失败突破后的 L2/双顶反向候选。

研究 sell stop 约在 `172.41` 下方，结构止损约 `182.87` 上方；静态到 `152.37–153.75` 约 `1.6–1.9R`，但过程中先触发结构止损。裁决：`range-edge-double-top / MTR-candidate / process-stop-first`，不是无条件 MTR 正例。

### 5.2 RBLX `2024-03-18–04-05`：双底样被区间和首障碍否决

父级约 `35.8–39.0` 宽区间；`03-18` 低点约 `35.95`，`04-02/03` 再测试 `35.90/35.79`，外形像双底。但反弹重叠多，`04-04` 冲高约 `38.09` 后收约 `36.80`，信号质量和区间中部位置都不支持升级趋势反转。

若按下沿逻辑，结构止损在 `35.79` 下方，第一目标约 `37.3–37.8` 中部，很快到达；原 buy stop 约 `36.66` 还被开盘约 `36.97` 越过。裁决：`range-edge-double-bottom-like / failed-signal / valid_no_trade`。

### 5.3 NFLX `2024-08-05–09-26`：高位测试与 Final Flag/MTR 边界

强多头腿后高位压缩、多次测试，可以先标为 `final_flag_or_MTR-candidate`；但测试次数超过三次、重叠明显，计数不干净。低周期卖出触发约 `67.10` 下方，结构止损约 `71.60–71.70` 外；第一支撑 `66.54–65.98` 只给约 `0.1–0.25R`。

裁决：`high-test / final-flag-boundary / valid_no_trade`，不是标准双顶 MTR 正例。后来高位重新被接受，不能选择性地用后续路径证明双顶成立。

### 5.4 TSLA `2025-09-08–09-12`：双高观察被 BOP 否定

`09-08–10` 在 `355.39–357.54` 阻力下多次试探，先有双高/多推观察；`09-11` 强阳线收在约 `368.81`，突破阻力并有 15m 跟随，随后回测守住。

裁决：`reversal_attempt / failed-MTR-thesis / BOP-acceptance`。反向订单假设取消，新交易必须按 BOP 合同重建，不能继续把它当双顶空头。

### 5.5 KLAC `2025-10-14–10-24`：普通趋势旗形对照

强多头腿后 `10-22` 只有浅回调，`10-23` 强阳线突破并在 `10-24` 接受前高。没有清楚的两次分离测试，父级趋势旗形解释更直接。

`114.26` 上方 buy stop 可研究，但 `115.49–115.63` 第一阻力贴近；严格日线分支 `valid_no_trade`，强趋势分支只保留条件性延续，不升级双顶/底反转。

### 5.6 ASML `2025-05-19–06-13`：双底样的区间过渡

两个低位测试接近 `715–718`，之后高重叠和区间过渡，缺少反向二次确认。裁决：`double-bottom-like / range-transition / not-MTR`；不冻结独立 buy stop 或 MTR 合同。

### 5.7 PLTR `2024-12-24–2025-01-08`：局部双顶不能替代普通 ABC/L1

B 腿内出现近似双顶，但主结构仍是普通 A 后的 L1/空头延续，结构止损要放在 B 顶部约 `80.06` 上方。它说明局部双顶可以嵌套在 ABC/H-L 中，但不能与父级 pattern 重复计为独立优势。

## 6. 统一视觉复核卡

```text
parent_state: open_trend / mature_range / channel / transition
test_type: double_top / double_bottom / near_equal / expanded / ambiguous
first_test / second_test: levels and separation
location: major_sr / range_edge / trend_extreme / middle / unknown
reversal_state: attempt / structure_break / second_confirmation / failed_thesis
related_family: ordinary_pullback / range_edge / final_flag / MTR / H3_L3
order_branch / actual_fill / open_skip
structural_stop / invalidation
neckline_or_mid_swing
first_independent_obstacle / MM_after_obstacle
rough_R_R / event / sector / market
status: candidate / continuation / range_transition / BOP / valid_no_trade
```

## 7. 当前结论与缺口

1. 双顶/双底是位置加两次有分离测试，不自动做空/做多；
2. 区间边缘先按区间逻辑，开放趋势先问普通回调，趋势末端才考虑 Final Flag；
3. MTR 需要反向结构破坏、第二次确认、接受/跟随和空间；第一反向通常只是小反转/区间候选；
4. 原方向重新接受极端后，旧双顶/底和 MTR thesis 必须结束并切换 BOP/延续；
5. 当前已有多空、区间、Final Flag、MTR 边界和 BOP 否定，但没有事件干净、首障碍宽裕、反向二次确认清楚且过程完整的标准 MTR 正例。

Double Top / Double Bottom 保持 `provisional`，只服务 PA Research 的视觉筛选、订单重建和观望纪律；不修改 Codex Trading，不建立量化扫描器，不连接 Execution Agent。

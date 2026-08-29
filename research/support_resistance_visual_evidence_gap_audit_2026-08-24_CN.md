# Support / Resistance 支撑阻力专项视觉证据缺口审计

日期：2026-08-24  
状态：`visual-foundation / partial / provisional / no-new-positive`

本审计把支撑阻力从“画一条水平线”改成 PA 研究中的位置、止损、首障碍和角色转换层。它不为每个区域评分，也不把单独 EMA、整数位或 MM 变成自动信号。

## 1. 当前可复用合同

| 合同 | 需要看到的证据 | 当前结论 |
| --- | --- | --- |
| 主要区域条件候选 | 多周期主要摆动/区间边缘/角色转换，价格在区域出现 pattern 反应 | KLAC 支撑簇 + H2 是条件候选；位置不等于自动成交 |
| 中部/首障碍否决 | 形态触发后最近独立区域太近，结构止损正常但空间不足 | VRT、XOM、COIN、RBLX 提供 no-trade 边界 |
| 角色转换 | 强收盘越界、跟随、回测守住 | TSLA 2025-09 提供阻力转支撑/BOP 对照 |
| 影线测试/失败 | 只有刺破或影线，收盘回到原侧 | 先记测试/失败突破，不能直接称转换 |
| 价格簇去重 | 前高、EMA、缺口、50% 和 MM 在同一区域 | 只算一个独立障碍，来源分别记录 |

## 2. 案例审计

### 2.1 KLAC 2025-05-07–06-03：支撑簇与 H2 条件候选

- `2025-05-23`、`05-30` 的低点、EMA20 和左侧高低点共同形成重复支撑区；`06-02` 收回 EMA20，`06-03` 触发 H2 延续。
- 研究结构止损约 `72.00` 下方，支撑区域内部不能压窄止损；上方 `79.03–79.79` 前高簇是第一阻力，远端 MM 不能跳过它。
- 结论：`major/intermediate-support-confluence / H2-candidate / first-resistance-boundary`。支撑质量增加候选质量，但首阻力仍决定日线是否值得交易。

### 2.2 TSLA 2025-09-08–09-12：阻力转支撑

- `09-08–10` 在 `355.39–357.54` 阻力区下方多次试探，影线越过但收盘未接受；此时仍是阻力/观察区。
- `09-11` 强收盘越过，15m 有跟随，之后回测守住旧阻力；状态切换为 `resistance-turned-support / BOP-acceptance`。
- 旧的 MTR/双顶/三推空头合同失效；新 BOP 合同必须重算实际成交、结构止损、第一独立阻力和 R/R。

### 2.3 VRT 2026-04-14–04-20：形态恢复但首阻力否决

- 多头 ABC/H1-like 视觉恢复成立，触发前已经存在 `310.94` 和约 `314.08` 的近端阻力簇。
- 两个价位相距不远，合并为一个第一阻力簇；不能把它们重复计成两个目标，也不能用 `2026-04-20` 后来的高点扩大入场前空间。
- 触发约 `316.35`、结构止损约 `303.45`，到第一阻力约 `0.42R`；结论是 `pattern_like / first-obstacle-boundary / valid_no_trade`。

### 2.4 XOM 2024-07-18–08-02：首支撑先于远端目标

- 空头触发前，第一支撑约 `105.20`，更远 `102.74` 只能是后续磁铁；结构止损约 `111.43–111.60` 上方。
- 原触发的静态空间接近 `1R`，但 `08-02` 开盘重订到约 `107.90` 后只剩约 `0.7R`；跳空使实际合同失去边际。
- 结论：即使第三次测试和空头方向都像，首支撑与成交重订仍否决交易。

### 2.5 COIN 2024-01-02–01-12：局部触发不能跳过主要支撑

- `01-09` L1-like 空头触发前，`01-04` 低点约 `148.81` 已是第一支撑，`144.11` 更远；结构止损约 `161.38` 上方。
- 到 `148.81` 的空间不足约 `1R`，`01-10` 低开又穿过原触发区；不能用后续 `140` 附近的支撑把入场前 R/R 美化。
- 结论：低周期触发和方向正确不等于位置合同通过。

### 2.6 RBLX 2024-03-18–04-05：区间边缘与中部磁铁

- `35.8–36.0` 是父级区间下沿支撑簇，`37.3–37.8` 是区间中部/第一磁铁，`39.0–39.2` 是上沿。
- 从下沿反应做多，目标顺序应先看中部，再看上沿；不能以局部 ABC 或远端 MM 跳过中部。
- `04-04` 上冲失败且收盘弱，`04-05` 恢复不能倒灌成高质量趋势买点；结论 `range-edge / signal-failure / valid_no_trade`。

## 3. 可复用视觉规则

1. **强度排序与距离排序分开**：major/intermediate/local 描述结构影响力；第一障碍描述从实际入场方向最先遇到的独立区域。
2. **区域优先于精确线**：按价格簇记录实体、影线、缺口、EMA 和多次反应；相近结构不重复计数。
3. **左侧可见性优先**：只使用入场前已经形成的高低点、区间、缺口和角色转换；后续极端不能倒灌。
4. **角色转换需要接受**：强收盘、跟随和回测守住才算；影线越过后收回仍是测试/失败候选。
5. **结构止损覆盖正常测试**：不要把止损压到支撑/阻力区域内部，除非明确是低周期独立合同。
6. **首障碍先于 MM**：形态再好，首障碍不足约 1R 仍是 no-trade；MM 只能作为后续路径。
7. **META 不重复计分**：EMA、缺口、50% 回调、整数位和 MM 若同一价格簇，只提高区域解释质量，不制造多个独立优势。
8. **事件与跳空重订合同**：财报前三个交易日不新开仓；跳空越过触发后，重算成交、止损、首障碍和 R/R。

## 4. 最小视觉复核卡

```text
parent_state: open_trend / trading_range / range_edge / transition / climax / unclear
level_type: major / intermediate / local / candidate
zone_source: swing / range_edge / role_reversal / gap / EMA / channel / other
left_side_tests_and_departure
current_role: support / resistance / magnet / converted / unconfirmed
location: edge / middle / near_entry / unknown
pattern_context_and_signal
order_branch / actual_fill / open_skip
structural_stop / invalidation
first_independent_obstacle / MM_after_obstacle
rough_R_R / event / sector / market
status: candidate / accepted_role / failed_test / valid_no_trade / pending
```

## 5. 当前缺口与停止条件

- 需要继续寻找一组事件干净、主要区域清楚、形态触发后首障碍宽裕且实际路径完整的多空对称案例；当前 KLAC 是条件候选，VRT/XOM/COIN/RBLX 是边界。
- 尚无一组能在不同周期同时冻结 major/intermediate/local，并清楚完成阻力转支撑、支撑转阻力两侧回测的完整对照；TSLA 2025-09 先作为一侧样本。
- 新案例只有在填补角色转换、首障碍先到、区域去重或多周期强度之一时才值得深审；不为数量重复同质形态。

基础目录：[`Support / Resistance`](../foundations/01_support_resistance/README.md)。跨 pattern 参考：[`支撑/阻力强度与八个 Pattern 的位置审计`](support_resistance_cross_pattern_audit_CN.md)。

# Opening Reversal 专项视觉证据审计

日期：2026-08-24

状态：`framework / partial / provisional / no-new-positive`

## 0. 审计结论

Opening Reversal 的视觉工作版已经清楚：**盘前背景和关键位置 → 开盘第一方向 → 失败/接受 → 反向 H/L 或第二次确认 → 订单、止损和首障碍**。当前案例覆盖了开盘失败、空头开盘反应、开盘接受和跳空后的订单重订，但尚未出现一个事件干净、反向确认清晰、首障碍宽裕且完整路径可复核的双向标准正例。

## 1. 条件候选/但被区间否决：RBLX 2024-04-04

- 父级约 `35.8–39.0` 是宽交易区间，不能把局部 A→B→C 改写成开放趋势；
- `2024-04-04` 开盘约 `36.97`，越过前日高点约 `36.66`，盘中上冲约 `38.09` 后收约 `36.80`，接近日内低位；
- 开盘多头方向没有接受，可记录为开盘上冲失败/空头反应候选；
- 但区间中部约 `37.3–37.8`、信号 K 质量和结构空间都不理想，结论为 `opening-reversal-candidate / range-edge / valid_no_trade`。

它说明“开盘反向”必须服从父级区间；区间中部的局部失败不能包装成高胜率开盘反转。

## 2. 条件候选/首支撑否决：COIN 2024-01-09

- `2024-01-02–03` 下跌与缺口压力后，`01-04–08` 反弹到约 `161.38`；
- `2024-01-09` 15m 开盘约 `159.60`，先上探约 `159.99`，随后第一根大阴线低到约 `153.29`；
- 视觉上是高位空头开盘反应，可研究 L1-like sell stop；
- 但 `148.81`、`146.51`、`144.11` 左侧支撑在入场前已可见，结构止损约在 `161.38` 上方，第一空间约 `0.25–0.5R`；
- `2024-01-10` 低开越过原 L2 触发位，不能事后使用理想填充价。

结论：`opening-reversal-candidate / H3-like-expansion-boundary / valid_no_trade`。方向可能对，订单几何和首障碍不支持完整新仓。

## 3. 状态切换边界：VRT 2026-04-17

- `2026-04-14` 的缺口冲击型多头 A 后，`04-15/16` 出现较深 B；
- `04-17` 开盘约 `298.64` 后守住并继续向上，更像开盘接受与 H1-like 恢复；
- 原约 `296.46` buy stop 已被开盘越过，若重新等 `305.53` 上方，第一阻力 `310.94–312.40` 只余约 `0.42–0.53R`；
- 不能把高开越过原触发价当作低风险开盘反转。

结论：`opening-acceptance / original-stop-opening-skip / first-obstacle-boundary`，不是 Opening Reversal。

## 4. 订单语义边界：TSLA 2025-03-04

- `2025-03-03` 空头信号 K 低点约 `277.30`；`2025-03-04` 约 `270.93` 低开，原 sell stop 被跳过；
- 如果价格在 `284.65` 附近，挂 `284.50` 的卖出 limit 可能立即成交，不是等待下跌；
- 等待反弹至 `284.0–284.3` 的 sell-limit/retest 是新合同；等待向下破位用 sell stop；
- 该案例属于缺口延续/角色转换回测，不是开盘反转。

结论：`gap-continuation / order-reprice-boundary`。

## 5. 反向与延续的统一状态机

```text
pre-open context
→ opening drive
  ├─ close/follow-through/acceptance → opening-drive-continuation / BOP
  ├─ magnet failure + return to prior side → opening-reversal-candidate
  │     ├─ second confirmation + space → conditional opening reversal
  │     └─ no follow-through / first obstacle close → observation-only
  └─ two-sided overlap → opening-range-transition / range logic
```

不能在同一时点同时保留“已经接受的 BOP”和“等待它失败的空头反转”两个互斥合同；只允许把后者写成未决假设，直到新证据出现。

## 6. 订单、止损、首障碍审计卡

| 字段 | 必须冻结的内容 | 常见否决 |
| --- | --- | --- |
| 盘前位置 | 前日高低点、缺口、区间边缘、主要 S/R | 位置只在收盘后才出现 |
| 第一波 | 推进方向、收盘、跟随、是否到磁铁 | 只凭第一根 K |
| 反向触发 | signal K、trigger K、H/L 计数 | 只有影线、没有跟随 |
| 订单 | stop / limit-retest / market-close | 理想价未成交却按成交分析 |
| 结构止损 | 开盘极端或真实失效位外 | 止损压在正常波动内 |
| 首障碍 | 第一独立 S/R、缺口边缘或左侧磁铁 | 用远端 MM 跳过近端障碍 |
| 事件 | 财报前三交易日、新闻重定价 | 把事件 K 并入普通样本 |
| 状态 | continuation / reversal / range | 多个互斥叙事同时成立 |

## 7. 当前证据缺口

已有案例足够形成视觉过滤语言，但还缺：

- 无重大事件、开盘反向失败后有清楚 H2/L2、首障碍宽裕的多头或空头标准正例；
- 同一个前日结构上，开盘失败与开盘接受的成对对照；
- 15m 触发与 1H/日线父级止损同时可复核的案例；
- 开盘反转和成熟区间边缘二次入场不重复计数的对照。

因此不建立固定开盘分钟数、固定成交量倍数或固定胜率，继续保持 `partial / provisional`。

本审计只服务 PA Research 的视觉筛选、订单语义和观望纪律，不建立量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

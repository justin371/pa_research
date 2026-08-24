# Opening Reversal 开盘反转视觉边界复核

日期：`2026-08-24`；状态：`visual-research / provisional / not-statistical`

## 开盘状态机

```text
盘前位置/缺口 → 第一波推进 → 接受还是失败
→ 反向 H1/L1 → 第二次确认 → 订单/首磁铁/R/R
```

缺口、第一根 K 或缺口回补本身都不是反转。第一方向若强收盘、跟随并在结构外接受，优先归 `opening-drive-continuation/BOP`；若在前日高低点、区间边缘或主要磁铁失败并回到原侧，才进入反向候选。

## 案例裁决

- `RBLX 2024-04-04`：开盘越过前日高点后冲高收弱，属于失败候选；父级宽区间、中线近、信号 K 差，`valid_no_trade`。
- `COIN 2024-01-09`：高位开盘上冲后空头反应清楚，但左侧支撑只给约 `0.25–0.5R`，`valid_no_trade`。
- `VRT 2026-04-17`：开盘守住并继续走强，是开盘接受/H1-like，不是反转；原 buy-stop 被跳过，需重订。
- `TSLA 2025-03-04`：跳空延续后 `284` 回测是新的 sell-limit/retest，不是开盘反转；下方 `284.50` 卖出 limit 可能立即成交，不能当等待下跌。
- `GOOGL/WMT/BKNG`：强开盘方向或原触发跳过，首障碍/未回测否决，不能用后续结果假设成交。

## 统一输出

```text
pre_open_context / gap_or_open_position
first_opening_pressure
acceptance_or_failure
reverse_attempt: none / H1-like / L1-like / H2-like / L2-like
order: stop / limit-retest / market-close / observe
actual_fill_or_open_skip
structural_stop / first_obstacle / rough_R_R
state: continuation / reversal-candidate / opening-range / valid_no_trade
```

当前结论：Opening Reversal 已有足够语言区分反向失败、开盘接受、区间过渡、普通 H/L 和订单重订，但尚无事件干净、反向二次确认清楚、首障碍宽裕且路径完整的标准正例；保持 provisional，不建立固定开盘分钟或量化阈值。

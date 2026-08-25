# 订单类型与风险合同视觉证据审计

日期：`2026-08-24`  
文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。

## 审计目的

把形态、订单是否成立、订单是否成交、成交后是否有空间拆成四个问题，防止用后续走势或低周期窄止损美化交易。

## 当前合同

### C1：stop 是证明，不是追价授权

Buy/sell stop 只有在价格真实越过冻结触发时才可能成交；如果触发后已贴近第一障碍，仍可跳过。

### C2：limit 必须等结构回测

Limit-retest 需要事先存在的支撑、阻力、角色转换或缺口边缘。未回测不成交；低于当前价的 sell-limit 可能立即成交，不能当作 downside sell-stop。

### C3：实际成交改变风险

开盘跳过、滑点、缺口和重订价会同时改变入场、止损、首障碍和 R/R。旧合同的静态数字不能继承。

### C4：风险顺序固定

订单合同 → 结构止损 → 第一独立障碍 → 粗略 R/R → MM/管理。`1R`/`2R` 只是视觉研究语言，不是固定胜率门槛。

## 案例矩阵

| 案例 | 订单问题 | 正确结论 |
| --- | --- | --- |
| TSLA `2025-03-03/04` | 原 `277.30` 下方 sell-stop 被 `03-04` 约 `270.93` 开盘跳过；`284` 附近反弹是另一笔回测 | 原 stop 不按理想价成交；`283.8–284.3` sell-limit 单独审计 |
| KLAC `2025-06-02/03` | H2 信号 K 后约 `75.90` buy-stop，15m 后续真实越过 | `stop_confirmation` 可重建；结构止损约 `72`、首阻力近，形态与日线 tradeability 分开 |
| LRCX `2024-07-10`–`2024-07-25` | 原 sell-stop 被开盘跳过；`93.98` 附近 limit-retest 未回到区域 | 原价未成交，limit 未成交，开盘接受/低周期重订另列；不能用后续下跌补成交 |
| GOOGL `2024-03-04`–`2024-03-22` | buy-stop 被开盘跳过，后来未必回测旧区 | 需要实际成交或新回测；未回测就没有 limit 成交 |
| QCOM `2024-07-17`–`2024-07-30` | 理想触发约 `1.37R`，开盘重订后约 `0.48R`，且财报/首支撑拥挤 | 实际合同 `valid_no_trade`；不继承理想 R/R |
| VRT `2026-04-14`–`2026-04-20` | 原触发被开盘越过，晚的低周期重新触发到首阻力只约 `0.42–0.53R` | 低周期可形成新合同，但高周期首障碍仍否决 |
| KLAC `2025-06` 持仓管理 | 已有多头接近 MM/动能减弱时分批止盈 | 这是管理动作，不是新的买入正例；追加仓必须重建风险 |

## 五个必须保留的对照

### 1. Stop 真正触发

KLAC `2025-06-03` 和已有 H3 案例显示，15m 真实穿越触发后才能记录 `triggered/filled` 的研究分支；只看到日线信号 K 或后来价格上涨不够。

### 2. Limit-retest 未成交

LRCX 的价格没有回到预先定义的 `93.98` 回测区，后续继续下跌不能证明 limit 本来会成交。GOOGL 同样要求真实回测；这是必须保留的负证据。

### 3. 开盘跳过重订

TSLA、LRCX、GOOGL、QCOM、VRT 说明开盘跳过后，原合同至少要进入 `opening-skip`，再决定重订、回测或观望；不能保留原价和原 R/R。

### 4. 持仓管理不等于新入场

已有仓位在 MM/首障碍处减仓或保护利润，不等于在同一位置新增一笔同样质量的订单。新仓要有新的触发、结构止损、首障碍和风险。

### 5. 第一障碍/RR 否决

KLAC、QCOM 和 VRT 说明即使订单语义正确、信号 K 清楚，首障碍太近仍然 `valid_no_trade`。订单层的职责包括拒绝成交，不只是选择一种下单方式。

## 统一审计字段

```text
decision_time:
contract_scope: deep_review
direction: long / short / no_valid_direction
pattern_state:
signal_bar:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
trigger_or_zone:
actual_or_assumed_fill:
original_order_status:
structural_stop:
first_independent_obstacle:
rough_space_and_R_R:
gap_event_sector_adjustment:
management_or_new_entry:
what_cancels_contract:
final_status:
```

## 当前结论

可迁移原则是：方向语义先准确；stop 要真实穿越，limit 要真实回测；market/close 要接受滑点；stop-limit 可能不成交；开盘跳过必须重订；已有仓位管理与新入场分开；结构止损与首障碍先于 MM；空间不足时 observation-only 是正确答案。

本层仍为 `provisional`，不产生胜率、不生成订单、不进入 Codex Trading、不连接 Execution Agent。只有新案例能提供清楚的订单分支、实际成交状态和路径 R/R 时，才继续深审。

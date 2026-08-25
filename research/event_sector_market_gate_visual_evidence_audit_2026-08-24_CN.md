# 财报 / 事件 / 板块 / 大盘视觉证据审计

日期：`2026-08-24`  
文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一字段、方向和状态分轴见[`PA Research 统一输出合同 v0.1`](../docs/pa_research_output_schema_v0_1_CN.md)。

## 审计目的

检查背景过滤是否在形态之前真正发挥作用：财报前三日是否直接禁止新仓，事件后强 A 是否被单独分组，SOXX/相关板块和 SPY/QQQ 是否只是许可项，以及跳空后是否重建订单合同。

## 当前合同

### C1：财报前三个交易 session 不新开仓

这是项目边界，不是概率判断。已有仓位管理另记；事件后方向正确也不能倒推财报窗口内原本应该交易。

### C2：事件驱动与普通 PA 分组

财报后的跳空、宏观冲击或其他重新定价可以产生强 A、BOP 或反转外观，但必须标 `event_driven`，不能与无事件普通 A 合并。

### C3：板块/大盘是许可，不是信号

顺势提高研究优先级，逆势提高证据要求；无论顺逆，都不能取消第一障碍、结构止损和实际 R/R。

### C4：跳空改变合同

开盘越过 stop 后按实际成交重算；回测、gap-and-go 和原 stop 分开。低周期不能把原成交价恢复出来。

## 案例矩阵

| 案例 | 过滤状态 | 形态/结构证据 | 当前结论 |
| --- | --- | --- | --- |
| DIS `2024-07-16`–`2024-08-02` | `2024-08-07` 财报前 3 个交易 session | 空头 A/B/L1-like，且开盘跳过和首支撑拥挤 | 直接 `earnings-window-invalid / valid_no_trade`；事件过滤独立否决 |
| AAPL `2024-05-03`–`2024-05-09` | 财报后重新定价 | 强 A、浅 B、H1-like，低周期触发可重建 | `event_driven / conditional`；不能作为普通无事件基准 |
| QCOM `2024-07-17`–`2024-07-30` | 板块方向同向，但财报窗口与首支撑拥挤 | 空头 L1/L2-like，方向和板块许可不等于空间 | `valid_no_trade`；重订后粗略约 `0.48R` |
| LRCX `2024-07-10`–`2024-07-25` | SOXX/SMH 同步；原 stop 被开盘跳过 | 空头 A/L1 顺序可见，缺口重订后首支撑仍近 | `conditional / gap-reprice / first-support-borderline` |
| NVDA `2024-09-11`–`2024-09-25` | SOXX 同向，财报窗口待确认 | Daily H2 + 60m/15m 确认清楚 | `sector-aligned / conditional`；低周期窄 R/R 不能冒充日线 R/R |
| HD `2024-07-01`–`2024-07-31` | XLY/SPY 逆风 | 支撑处 H1-like、EMA200 接近，结构证据存在 | `countertrend / downgraded / valid_no_trade`；逆板块不是绝对禁止，但证据不足以抵消首障碍 |
| JNJ `2025-08-01`–`2025-09-02` | XLV 顺势 | 强 A、controlled B、H1-like；开盘跳过且前高簇近 | `sector-aligned / opening-skip / valid_no_trade` |
| ADBE `2026-01-12`–`2026-01-27` | 财报通过，IGV/市场并非全面同向 | 父级过渡转空、局部 L1-like，低周期顺序较清楚 | `conditional / market-countertrend`；不算纯开放趋势基准 |

## 五类必须保留的对照

### 1. 财报前三日直接 no-trade

DIS 是硬边界：即使图形和方向存在，`2024-08-02` 仍在 `2024-08-07` 财报前三个交易 session 内。不能用后续下跌证明当时应开空仓。

### 2. 事件后强 A 只作条件样本

AAPL 的强 A 发生在事件后，买压确实可能更强，但事件也改变了波动、缺口和支撑阻力。它可以进入条件研究，不能与普通无事件 A 混合。

### 3. 板块顺势但首障碍仍否决

QCOM、LRCX、NVDA 和 JNJ 表明板块同步可以提高许可，但不保证 R/R；开盘重订或主要障碍太近时，仍然 no-trade 或边界。

### 4. 逆板块但有结构证据的降级

HD 和 ADBE 表明逆板块/市场并非机械禁止：若主要位置、结构破坏、信号和空间较清楚，可以保留 `conditional`；但首次尝试、首障碍拥挤或父级过渡时必须降级，不把它当普通基准。

### 5. 跳空导致原订单重订

LRCX、QCOM、JNJ 和 GOOGL 共同说明，开盘越过原 stop 后，旧合同不能按理想价成交。只能等回测、按实际价重订或建立 BOP；所有分支都要重新审计止损、首障碍和 R/R。

## 统一记录字段

```text
decision_timestamp:
data_source / data_status / as_of_time:
earnings_next_three_sessions:
event_context:
direction: long / short / no_valid_direction
sector_reference / sector_state:
market_reference / market_state:
permission:
parent_state_and_location:
pattern_and_attempt:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
actual_or_assumed_fill:
structural_stop:
first_independent_obstacle:
rough_R_R:
gate_result:
failure_condition:
```

## 当前结论

可迁移的共同语言是：先确认数据，再过财报闸门，再看板块/大盘许可，最后才审计 pattern；财报前三日不新开仓；事件后强 A 要单列；板块是许可不是信号；逆板块需要更强结构证据；跳空重建订单；顺势也不能取消首障碍和 R/R。

本层仍为 `provisional`，不产生胜率、不进入 Codex Trading、不连接 Execution Agent。只有事件日期、板块状态、订单重订和结构路径都能重建的新案例，才继续增加深审。

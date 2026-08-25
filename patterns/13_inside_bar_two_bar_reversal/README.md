# Inside Bar / 两根 K 线反转

文档状态：`document_status=research_only / research_state=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补母 K、内包/IOI 和两根反转边界。严格内包定义不能替代事件、订单、止损和方向字段。

这个目录把四种容易混淆的东西分开：严格 Inside Bar、二内包/IOI、两根 K 线反转，以及 H1/H2 或 L1/L2 的 setup—signal—trigger 序列。它们可以重叠，但任何一个名称都不能替代背景、位置、突破接受、订单和空间审计。

## 最小定义

### 严格 Inside Bar

若母 K 为 `mother`，内包 K 为 `inside`，至少要满足：

```text
inside.high <= mother.high
inside.low  >= mother.low
```

比较的是整根 K 的高低点，不是实体。影线越出母 K 时，不是严格 Inside Bar；如果母 K 的高低点没有冻结，只能写 `inside-like / pending-ohlc`。

`ii` 是连续两根内包；`ioi` 是内包—外包—内包。它们描述平衡/压缩，不自动决定方向。

### 两根 K 线反转

第一根把价格推向某方向或测试结构，第二根在有意义的位置明显拒绝该方向并向另一侧收盘。没有位置、触发和跟随的两根相反 K，只是普通摆动。

### H/L 信号序列

Inside Bar 关注范围压缩；H1/H2、L1/L2 关注回调中的尝试次数；setup K、signal K 和 trigger K 必须分栏记录。一个内包可以是 H2 的 setup，但不能因为它是内包就跳过确认。

## 状态分流

| 状态 | 证据 | 默认处理 |
| --- | --- | --- |
| `pause-continuation` | 趋势中压缩，原方向仍有收盘和跟随 | 顺势等待突破/回测；不逆势猜反转 |
| `two-bar-reversal-candidate` | 关键位置的压力转换和第二根强反向 K | 等 stop 或第二次确认；不直接宣布 MTR |
| `inside-breakout-candidate` | 母 K/内包范围冻结，某侧突破并获得接受 | 记录突破、回踩、失败三个分支 |
| `range-middle-noise` | 区间中部压缩或两根反向 K | 默认观望；不把局部波动当趋势启动 |
| `pending-ohlc` | 只有图形外观，没有完整母 K 高低点 | 只保留形态候选，不升级严格定义 |

## 研究顺序

1. 先判父级：开放趋势、通道、交易区间、边缘或过渡；
2. 冻结母 K、inside K 或两根 K 的整根范围；
3. 标出左侧主要支撑/阻力、EMA、缺口、区间边缘和事件/板块背景；
4. 区分 setup/count、signal 和 trigger/confirmation；
5. 事前冻结 stop、limit-retest、market-close 或 observation-only 合同；
6. 用结构极端确定止损，再看第一独立障碍和 rough R/R；
7. 只有突破被接受、反向有跟随或出现二次入场时，才升级状态；
8. 后续 MM、盈利或反转不能倒灌成当时的入场证据。

## 订单与风险

- **Stop-confirmation**：多头放在母 K/信号 K 高点外，空头放在低点外；宽 K、跳空或接近首障碍时要重算。
- **Limit-retest**：只在旧边界、母 K 边缘或角色转换区已经明确后研究；未回到区域前不假设成交。
- **Market/close-confirmation**：只给强反向收盘、结构已经破坏且等待代价明显的分支；小内包突破不自动授权追入。
- **Observation-only**：母 K 未冻结、处于区间中部、首障碍贴近、事件/跳空改变原合同，或只能把止损压在母 K 内部才得到好看的 R/R。

结构止损要覆盖回调极端、母 K/反向测试极端和真正失效位置，不能只放在第二根 K 的小尾巴外。第一独立支撑/阻力不足约 1R 时记录为 `valid_no_trade`；约 2R 是完整波段参考，不是固定门槛。MM 只有在首障碍被接受穿越后才作为延伸目标。

## 当前案例入口

- [`KLAC 2025-10-22/23`](../../research/klac_h1_case_study_2025-10-14_2025-10-24.md)：两根反转/趋势延续条件候选，确认 K 优于 setup K，但第一阻力贴近；
- [`AAPL 2024-05-08/09`](../../research/aapl_bullish_h1_event_driven_a_2024-05-03_2024-05-09.md)：小实体、下影线和低周期确认，不足以证明严格内包；
- [`RBLX 2024-04-04/05`](../../research/rblx_range_edge_not_abc_boundary_2024-03-18_2024-04-05.md)：区间中的两根反向 K，位置和空间否决；
- [`KLAC 2025-05-30/06-03`](../../research/klac_h2_case_study_2025-05-07_2025-06-03.md)：H2 setup—signal—confirmation 序列，内包关系仍待 OHLC 冻结；
- [`TSLA 2025-03-03/04`](../../research/tsla_abc_playbook_2025-03-04_284_retest.md)：跳空重新定价，明确不是严格 Inside Bar 或有序两根反转。

专项证据审计见 [`Inside Bar / 两根 K 线专项视觉证据审计`](../../research/inside_bar_two_bar_reversal_visual_evidence_gap_audit_2026-08-24_CN.md)，基础框架见 [`Inside Bar / 两根 K 线反转视觉研究框架`](../../research/inside_bar_two_bar_reversal_visual_framework_CN.md)。

本目录只服务 PA Research 的视觉识别、案例复核、订单语义和 no-trade 判断，不建立量化扫描器、不修改 Codex Trading、不连接 Execution Agent。

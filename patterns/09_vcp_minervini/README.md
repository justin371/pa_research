# VCP / Volatility Contraction Pattern（Minervini）

文档状态：`document_status=research_only / research_state=provisional / handoff_status=not_ready / not-quantitative`

完整案例先套用[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)；本目录只补 VCP 的 T1/T2/T3、pivot 和收缩 lineage。VCP 仍是独立视觉研究主题，不与 Brooks pattern 或 BOP 统计合并。

VCP 是 Mark Minervini / SEPA 体系中的独立主题。它不是 Al Brooks 的 H1/H2、L1/L2、ABC、三推或 BOP 的别名，也不计入 PA Research 的“核心八个”PA pattern。这个目录只负责把 VCP 的视觉结构、交易合同和边界写清楚；后续如果出现 PA 触发，只作为二次确认，不改写 VCP 的定义。

## 研究版核心定义

一个合格的 VCP 候选通常同时具备：

1. 左侧已有明显、健康的上涨和相对强势；
2. 价格进入一个整理母体，而不是从长期下跌或 Stage 4 反弹中随意画出的窄区间；
3. 母体内部出现至少两次可区分的回撤/收缩（T1、T2、T3…），后一次的价格波动明显小于前一次，整体由左到右变紧；
4. 成交量和/或下跌时的供应压力总体减弱，最后阶段趋于安静；
5. 最后一次收缩上方存在可定义的 pivot（通常是最近一次收缩的上沿/最后阻力）；
6. 价格向上突破 pivot，并出现需求和接受的证据，才进入 VCP breakout 合同。

这里的“变紧”是相对股票自身近期波动来判断，不预先冻结 20%→10%→5%、固定收缩次数或固定成交量倍数。那些数字可以作为复核时的示例，不能代替图表判断。

## 不足以称为 VCP 的外观

- 只有一个很窄的交易区间，没有前置上涨和连续收缩；
- 低成交量但价格仍在宽幅、反复破坏低点；
- 任何三角形、旗形、ABC 或三推，只因为右侧变窄就贴 VCP 标签；
- 下一个回撤比前一个更深、放量跌破母体关键低点，却仍事后把它画成“最后一次收缩”；
- 财报跳空后仅凭一两根 K 线形成的压缩；
- 在长期下跌、父级交易区间中部或明显分配环境里强行寻找多头 VCP。

## 视觉审查顺序

```text
weekly / daily parent context
→ prior leader and stage-2-like strength
→ base and contraction lineage
→ T1 > T2 > T3 的相对收缩
→ volume / supply behavior
→ pivot and breakout acceptance
→ order, structural stop, first independent resistance, rough R/R
→ earnings / market / sector / failure state
```

### 1. 左侧背景

先问：这是否是一只已经证明过相对强势的股票？上涨是否有方向性、跟随和较少重叠？如果左侧只是大跌后的反弹、长期横盘或父级区间中部，VCP 评级降为 `vcp-like / observation-only`，不能因为局部收缩而升级。

Stage 2、Trend Template、相对强度和行业领导地位是背景过滤，不是 VCP 图形本身。PA Research 不把它们改造成量化扫描器；图表复核时只记录“满足、部分满足、无法判断”。

### 2. 母体和收缩 lineage

从左到右标出 T1、T2、T3，而不是用未来走势反推端点。比较每次高点到低点的相对幅度、持续时间、反弹质量和重叠度：后一次应明显更受控，最终收缩应接近 pivot，且不应出现无解释的深度扩张。

“约半幅”是常见的教学描述，不是硬性比例；某一只股票的正常 ATR、行业波动和前一段上涨幅度必须进入判断。时间缩短可以作为加分项，但暂不作为必要条件。

### 3. 成交量和供应

观察下跌日是否逐步缩量、收缩末端是否安静、反弹日是否能在较少供应下恢复。成交量不能脱离价格位置单独解释：低量下跌可能是供应耗尽，也可能是无人承接；放量突破需要结合收盘位置和后续接受。

本项目把“回撤量缩/卖压减弱”列为重要参考项，非必要条件；不设固定均量倍数。

### 4. Pivot 和突破

标准研究合同是：在最后收缩上方预先定义 pivot，等待价格向上突破并观察需求、收盘位置和后续接受。核心订单优先记录为 `buy-stop / stop-entry above pivot`，而不是在母体中间提前猜底。

若突破高开太远、接近财报或没有足够空间，不追价；记录为 `gap-reprice / wait-for-new-base / no-trade`。在母体内提前用 limit 或 cheat 属于另一个实验分支，不能与标准 pivot breakout 混为一谈。

### 5. 风险、空间和退出

- 止损优先放在最后收缩低点或其下方的结构位置；不得为了追求小百分比而把正常波动排除在外；
- 入场前先看第一道独立阻力/前高，再看 measured move；没有空间就 `valid_no_trade`；
- measured move、AB=CD、EMA 和 META 可以帮助估算空间或汇合，但不是 VCP 定义，也不是自动止盈点；
- 价格快速脱离 pivot 后可按强度分批止盈，不能机械等待某个精确 MM 点；
- PA Research 的用户覆盖规则：财报前三个交易日不新开仓；财报跳空后的重订合同单独记录；板块（例如半导体的 SOXX）和整体市场背景优先于单一形态。

## 与 Brooks PA 的边界

| 主题 | VCP 的角色 | Brooks PA 的角色 |
| --- | --- | --- |
| ABC | 不是同一结构；ABC 可出现在母体前后，但不自动构成 VCP | 识别 A 腿、B 回调、恢复和区间重置 |
| H1/H2、L1/L2 | 不是 VCP 定义 | VCP 突破后的回踩或新背景中可作为 PA 二次触发 |
| 三推/H3-L3 | 不是收缩计数 | 可以提醒压力、衰竭或状态转换，但不能替代 T1/T2/T3 |
| BOP | 可描述 pivot 突破后的接受状态 | 用来判断突破是否被接受、是否转入新的交易合同 |
| META | 只能作为多重优势汇聚的记录层 | 支撑/阻力、信号 K、板块和空间可作为加分项 |

## 状态词汇

- `not_vcp`：背景或收缩 lineage 不成立；
- `vcp_like`：外观接近，但仍缺背景、量价或 pivot 证据；
- `developing`：母体和收缩在形成，尚未到标准触发；
- `pivot_ready`：最后收缩和 pivot 已可定义，等待突破；
- `triggered_pending_acceptance`：突破发生，但仍需观察接受；
- `accepted_breakout`：突破、收盘/需求和后续路径支持新合同；
- `failed_vcp`：假突破、重返母体、放量破坏最后支撑或后续收缩扩张；
- `valid_no_trade`：形态像，但事件、首阻力、跳空、R/R 或订单合同否决。

## 研究边界

当前不把 VCP 写成扫描条件，不声称已有胜率，也不把任何后见之明的上涨当作证据。下一阶段应从收盘后的完整日线/周线图中寻找事件干净、背景清楚、T1/T2/T3 可回看、pivot 和首阻力都能在当时确定的多空对照；在此之前，VCP 只保持为独立的视觉工作版。

详细来源层级、未核实的原始定义见 [`VCP / Minervini 定义与视觉证据缺口审计`](../../research/vcp_minervini_visual_evidence_gap_audit_2026-08-24_CN.md)；首轮公开图表对照见 [`VCP / Minervini 首轮公开图表视觉对照审计`](../../research/vcp_visual_case_audit_round1_2026-08-24_CN.md)。

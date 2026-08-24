# VCP / Minervini 首轮公开图表视觉对照审计

日期：2026-08-24

状态：`source-anchored / visual-comparison / provisional / no-new-positive`

## 0. 这轮审计能证明什么

本轮使用公开教育页面和其标注图，目的是把 VCP 的视觉语言落到具体图形：前置上涨、母体、T1/T2/T3 收缩、量能、pivot、突破和失败。它们不是 PA Research 自己用原始 OHLC 逐根盲审的完整案例，因此不能用于声称胜率，也不能把后续涨幅回填成入场证据。

当前结论：

- `WFRD`：最适合保留为“条件性视觉候选”，因为公开图示同时给出收缩数量、首末收缩和 pivot/量能关系；独立核对事件、板块、原始日期和实际 R/R 仍未完成；
- `NVDA 2023`：结构示范很清楚，但突破与财报跳空相邻；按用户规则应先归入事件/跳空否决或重订合同，不能当普通 VCP 入场正例；
- `TSLA 2020`、`SHOP 2016`：教材级结构对照，说明强势背景和逐次收缩，但目前缺少本项目所需的当时可执行订单、事件窗口和第一独立阻力审计；
- `AM`：提供假突破返回母体、随后放量弱化的失败边界；它说明“突破过 pivot”不等于 VCP 成功；
- 当前仍没有一个已经完成独立原始数据盲审、事件干净、pivot/结构止损/首障碍/R/R 全部可重建的 VCP 正向样本，整体状态保持 `no-new-positive`。

## 1. 候选一：WFRD 的收缩母体（条件性候选）

### 公开图表证据

ChartMill 的 Minervini 二手整理展示了 Weatherford International（WFRD）的两个 VCP 图例：一个图例标成约 `19W 19/7 4T`，另一个约 `3W 7/4.5 2T`；页面同时描述了收缩末端量能下降、pivot 突破和突破量能增加。

这组图至少提供了可复用的视觉检查顺序：

1. 不是单独看最后一小段窄区间，而是从母体左侧追踪 T1→T2→T3→T4；
2. 比较首个和最后一个收缩的相对幅度，而不是假设每次必须精确减半；
3. 观察收缩末端的低参与/低供应，再看 pivot 是否被需求突破；
4. 把“图形成熟”和“可以买”分开，后者仍需事件、板块、首阻力和风险合同。

### PA Research 的初步判定

`conditional_candidate / source-anchored`

保留理由：公开图示具备强势背景、连续收缩、量能收缩和 pivot 的完整叙事，适合成为第一张重新用原始收盘数据复核的图。

尚未通过的部分：

- 原始日期、每个 T 的端点和 pivot 需要独立重建；
- 需要核对财报前三个交易日规则；
- 需要看 WFRD 当时的行业/市场背景，而不是只看个股；
- 需要计算 pivot 到最后收缩低点的结构风险，以及到第一独立阻力的粗略 R/R；
- 需要区分图中的两个 VCP 是否是同一母体的嵌套结构，不能重复计数。

### 不允许的回填

不能因为图示后来突破，就把某个模糊的低点事后升级为 T3 或把突破日当成已知的买点。下一次审计必须先冻结“突破前一日可见的版本”，再单独记录突破后的路径。

## 2. 候选二：NVDA 2023（结构清楚，但事件否决）

TraderLion 的公开图文镜像使用了 Mark Minervini 账号标注的 NVDA 示例，展示了三段收缩，示例数字约为 22%→11%→6.17%，并强调右侧收缩、量能干涸、最终窄收缩和 pivot。Deepvue 也把 NVDA 2023 列为 VCP 示例。

### 结构层

- 左侧强势上涨与相对强度明显；
- 母体内的回撤由宽变窄，右侧更紧；
- 最后收缩较浅，能够定义更近的风险位置；
- 突破有需求/量能的教学级示范。

### 事件层

NVDA 2023 的公开资料把突破描述为财报/指引驱动的巨大跳空。即使图形在突破前已经成熟，也不能把事件跳空当成普通 stop-entry 的可复制填充：

- 用户覆盖规则是财报前三个交易日不新开仓；
- 若突破直接以事件跳空越过 pivot，应标记为 `event_gap / gap-reprice`；
- 如果跳空太远，不能用“后来涨得多”授权追价；
- 后续需要新母体或回踩合同，而不是强行复原原始 VCP 入口。

### PA Research 的初步判定

`pattern_like / event_blocked / no-trade-for-standard-contract`

它是很好的定义图，但不是当前普通 VCP 正向样本。它提醒我们：VCP 的结构质量、事件可交易性和实际 R/R 是三个不同问题。

## 3. 候选三：TSLA 2020（高波动强势背景的边界）

Deepvue 将 TSLA 2020 描述为一次强劲上涨后的约三个月 VCP，最后约 10% 的回撤小于前面约 20% 和 25% 的回撤，突破后继续大幅推进。

这张图的研究价值不在于直接复制百分比，而在于提醒：

- 高波动成长股的“窄”必须相对于自身前段波动判断；
- 10% 对 TSLA 可能已经是收缩，对低波动大盘股却可能仍然很宽；
- 强势背景可以让较深的前置收缩仍有意义，但不能因此放弃事件、首阻力和结构止损；
- 需要确认是否存在多个嵌套母体，避免把一次更大趋势中的内部回调重复算成多个 VCP。

### 初步判定

`textbook_visual_boundary / raw-bar-audit-needed`

它是有价值的教材级对照，但未达到 PA Research 的可执行案例标准。

## 4. 候选四：SHOP 2016（教材级窄末端对照）

Deepvue 将 SHOP 2016 标为强势上涨后的 VCP 示例，并强调最后收缩很浅、量能收缩，随后突破并出现大幅延续。

它对我们最有用的不是后续涨幅，而是两个视觉问题：

1. 最后收缩必须能提供可承受的结构风险；
2. “窄”不能脱离前段上涨和个股自身波动，不能把任何小箱体都标成 VCP。

### 初步判定

`textbook_visual_reference / raw-bar-audit-needed`

缺少本项目所需的原始日期、财报窗口、pivot 填充、第一独立阻力和路径 R/R，因此暂不升级为正向案例。

## 5. 失败边界：AM 的假突破 / squat

ChartMill 的二手整理描述了 Antero Midstream（AM）的一次 VCP 假突破：价格突破后在当天或次日回到母体；随后若出现更明显的下跌、放量并跌破 20SMA/最近低点，则应收紧风险或退出。

这给 PA Research 一个清楚的失败分流：

```text
pivot break
→ acceptance? 
  ├─ yes：进入 accepted_breakout，继续看首阻力和路径
  └─ no：回到母体
        ├─ 低量、受控、仍守结构：观察 / 原合同待验证
        └─ 放量破坏最后支撑：failed_vcp，不能再叫健康收缩
```

### 初步判定

`failed_vcp_boundary / source-anchored`

它没有证明某个失败处理方式的固定百分比或固定持仓规则；它只证明“突破之后的接受性”必须单独审计，且 VCP 失败不能用后续反弹猜测来覆盖。

## 6. 本轮冻结的视觉合同

### 观察卡

| 层级 | 必须回答的问题 | 结论词 |
| --- | --- | --- |
| 背景 | 左侧是否为强势领导/Stage-2-like，而非下跌反弹或区间中部？ | `leader / mixed / not-qualified` |
| 母体 | T1、T2、T3 是否真实可分，后者是否明显收窄？ | `contracting / mixed / expanding` |
| 供应 | 下跌是否受控、量能是否趋弱、是否有 accumulation/RS 迹象？ | `drying / mixed / distributing` |
| pivot | 突破线在当时是否可定义，且是否与远处主要阻力重叠？ | `clear / crowded / unclear` |
| 事件 | 财报、新闻、跳空是否改变了普通合同？ | `clean / event-gap / hold` |
| 订单 | 是 pivot stop、gap-reprice、回踩还是母体内提前猜测？ | `contract name` |
| 风险 | 结构止损是否合理，第一独立阻力是否留有空间？ | `A / B / C / no-trade` |
| 结果 | 只记录后来路径，不反写原始信号质量 | `accepted / failed / unresolved` |

### 统一否决

- 后一次收缩更深或放量扩张；
- 母体中部没有清楚 pivot；
- 突破立即回到母体且没有接受；
- 财报前三交易日；
- 第一独立阻力太近或结构止损不可承受；
- 只凭后续暴涨、量能或图中标注就声称“高胜率”。

## 7. 还缺什么才算独立视觉正例

下一轮不再收集更多教学图，而是对 WFRD、NVDA 或用户指定标的中的一个，取得收盘后的原始日线并做一张“突破前冻结卡”：

1. 只看到突破前最后一天；
2. 标出左侧趋势、T1/T2/T3、pivot、最后收缩低点和第一独立阻力；
3. 记录市场、板块、财报和订单合同；
4. 计算粗略 R/R，但不把 MM 当保证；
5. 再打开后续 K 线，分开审计接受、失败、gap、止盈和路径。

在没有完成这五步前，本文件中的候选全部保持 `source-anchored`，不移交 Codex Trading。

## 8. 公开视觉来源

- [ChartMill：Mark Minervini Strategy Part 2](https://www.chartmill.com/documentation/stock-screener/fundamental-analysis-investing-strategies/465-Mark-Minervini-Strategy-Think-and-Trade-Like-a-Champion-Trading-Strategy)
- [Deepvue：Mastering the VCP](https://deepvue.com/screener/volatility-contraction-pattern/)
- [TraderLion 公开 VCP 图文镜像（含 Mark Minervini 标注图）](https://en.rattibha.com/thread/1751278912632426918)
- [Business Insider：Minervini 采访摘要](https://www.businessinsider.com/stock-trading-tips-strategies-advice-from-lengendary-investor-mark-minervini-2020-6)

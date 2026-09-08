# PA Research 形态边界视觉决策卡

> 适用范围（2026-09-08）：本文保留指定历史实验与兼容输出的合同。日常 AI 看图发现使用 [AI 视觉研究](ai_visual_research_CN.md)，不强制继承本文的分类、均线、窗口和字段门槛；冻结样本与既有校准边界保持原样。

文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / evidence_scope=visual_calibration_only`

## 一、用途

本卡把两年 Daily 图上的 H1/H2/L1/L2、BOP、三推/H3-L3 与普通 ABC continuation 按固定顺序分流。它解决的是“这张图当前更接近哪个研究家族、计数是否还能延续”，不是自动选股、精确识别器或交易授权。

本卡来自[形态覆盖候选集 v1 独立盲审与裁决审计](../research/morphology_calibration_adjudication_audit_2026-09-01_CN.md)：两名 reviewer 在 `b_leg_class` 上只有 25.00% 精确一致，候选来源的 H1/H2/L1/L2 与盲裁决只有 1/8 精确一致。因此必须先判父级、B 腿、状态迁移和 lineage，再计 H/L；不能从一个相似 K 线形状直接命名。

本卡中的盲裁决是独立模型视觉裁决，不是人工专家 ground truth，也没有未来 K 线或交易结果。它不改变 `no-new-positive / validated win-rate: not-computable`。

## 二、六步固定顺序

同一张图只按以下顺序检查；前一步触发状态迁移时，后面的旧计数失效。

| 顺序 | 先问什么 | 是 | 否/不清楚 |
|---:|---|---|---|
| 1 | 两年 Daily 左侧、重要高低点、EMA20/50/200 和事件证据是否完整？ | 继续 | `pending / observation_only`，不冻结 family 或 H/L 计数 |
| 2 | 父级是开放趋势，还是成熟区间/边缘/过渡/高潮？ | 先冻结 `parent_state` | 不用局部 A/B 形状替代父级 |
| 3 | 事前可见边界是否已被收盘突破、获得跟随，并在回踩时守住？ | `primary_pattern: BOP`；旧 ABC/H-L/三推合同失效 | 继续 |
| 4 | 当前是否为成熟区间边缘，或同一 lineage 的第三次有意义尝试？ | 先进入 range-edge 或 H3/L3/三推压力分支 | 继续 |
| 5 | A 是否方向清楚、B 是否仍是同一开放趋势中的受控回调？ | 才允许研究 `ABC_CONT + internal_label H1/H2/L1/L2` | `range_like/uncontrolled/reset/pending` |
| 6 | 触发、结构止损和第一独立障碍是否给出至少约 1R 的真实空间？ | 可进入 deep review | `valid_no_trade` 或等待结构 |

这个顺序表达的是**状态优先级**，不是优势分数：`BOP 状态迁移 > 区间/第三推分流 > 普通 ABC/H-L 计数 > 交易几何`。BOP 优先并不代表它更容易盈利，只表示旧合同已经不再准确。

## 三、先把 B 腿分清楚

`b_leg_class` 只回答反向压力和父级结构，不回答位置是否好，也不回答最后会不会盈利。

| `b_leg_class` | 必须看见的视觉事实 | 不能混入 |
|---|---|---|
| `not_formed` | A 后尚未形成可分辨的反向腿或时间整理 | 不能预先猜 H1/H2 |
| `controlled` | 反向实体/跟随未持续扩张；重叠或时间整理增加；母腿关键结构仍守住；末端在支撑/阻力或 EMA 附近重新获得原方向控制 | “回调浅”本身不足；单次 EMA 触碰不足 |
| `controlled_late` | B 早段仍有压力，但截止图末端已出现连续收缩或重新控制；尚未形成宽幅双向轮动 | 不能因为最终反弹/下跌而事后补写 |
| `deep_but_late_controlled` | 回撤明显较深，但未吞没 A 起点或建立反向趋势；末端在预先存在的位置稳定 | 必须与浅 B 分层；深不等于自动失控 |
| `uncontrolled` | 反向实体、收盘或跟随持续增强；穿越 A 的关键结构/起点；或形成可独立识别的反向趋势 | 不再继承原 H1/H2/L1/L2 计数 |
| `range_like` | 多根 K 线双向轮动、重复穿越 EMA/中轴、上下都有跟随、没有清楚的回调终点 | 区间中部不能用 H2/L2 编号挽救 |
| `unclear` | 截止图允许两个以上合理 B 锚点，或事件/缺口改变尺度 | 保留边界，不强选一个类别 |

辅助问题按顺序回答：

1. 反向压力是在缩小、持平，还是扩大？
2. 母腿的关键极值或起点是否仍然有效？
3. 价格是围绕一个位置收缩，还是在宽范围两边来回获得跟随？
4. 末端稳定是截止日前可见，还是只有看了未来结果才显得稳定？

不设固定回撤百分比、K 线数量、EMA 距离或实体阈值。图形识别保持视觉化，但每个判断必须能指出可见的压力、结构与位置事实。

## 四、H1/H2/L1/L2 的最小资格

只有以下条件同时成立，才从 `H/L-like` 升级为可计数的普通趋势 H/L：

- `parent_state: open_trend`，不是成熟区间中部；
- 多头 Daily EMA20/50 都向上，空头两条都向下；
- A 与原趋势同向，B 为 `controlled / controlled_late / deep_but_late_controlled`；
- 第一次尝试、失败/无跟随和第二次尝试都属于同一 timeframe、同一 B、同一 lineage；
- 计数期间没有接受性突破、父级重建、事件重定价或区间化；
- 回调结束位有预先存在的 EMA、前高/前低角色转换、支撑/阻力或 META 区域；
- H3/L3 必须转入第三推压力分支，不能继续作为普通第三次 H/L。

### 计数重置

出现以下任一项，先写 `lineage_status: reset / pending`，不要继续把下一次尝试称为旧 H2/L2：

- B 接受性穿越母腿关键极值或 A 起点；
- `b_leg_class` 变为 `range_like` 或 `uncontrolled`；
- 新的强方向腿已经可以独立定义为新 A；
- 旧边界被突破接受，主合同切换为 BOP；
- 事件缺口或重定价改变了原触发、止损和支撑阻力关系；
- 计数必须依赖不同周期或事后结果才能成立。

## 五、family 分流卡

| 当前证据 | family/合同处理 | 明确禁止 |
|---|---|---|
| 事前边界 + 收盘越界 + 跟随/守住回踩 | `BOP_like`；正式记录切换 `primary_pattern: BOP` | 继续沿用突破前 H1/H2 或三推反转合同 |
| 开放趋势 + 同一 lineage + 强/普通 A + 受控 B | `ABC_CONT_like / H_L_like`；H/L 只作 `internal_label` | 把 family 和 attempt 当两个独立优势 |
| 同一 lineage 的第三次有意义尝试 | `THREE_PUSH_like` 并填写压力 variant；attempt 为 H3/L3-like | 降格为普通 H1/H2/L1/L2 |
| 成熟区间上沿/下沿的第三次测试 | `range_edge` 三推/失败突破分支；等待拒绝、反向触发与空间 | 用开放趋势 H2/L2 解释区间中部或边缘轮动 |
| 区间中部双向重叠 | `NONE / wait_for_structure / rejected_gate` | 为了得到候选强行选择 ABC/H-L |
| 事件跳空直接越过边界或旧触发 | `event_boundary`；先重建状态与几何 | 把事件驱动推进混入 ordinary H/L/BOP 统计 |

## 六、冻结 cohort 的成对边界例子

以下样本只用于解释决策顺序。候选来源标签是假设，盲裁决也不是 ground truth；图表和完整逐样本记录见审计及其 JSON。

| 对照 | 共同外形 | 关键差异与正确处理 |
|---|---|---|
| `MC2-004` vs `MC2-010` | 都是开放多头、强 A、EMA long pass，候选来源分别写 H1/H2 | 两者盲裁决都优先读成 `BOP_like`；先确认旧边界和回踩接受，再决定 H/L 只作 secondary/internal context。`MC2-010` 可 deep review，`MC2-004` 仍等待结构 |
| `MC2-002` vs `MC2-008` | 都靠近宽区间上沿，也都能看出向上尝试 | `MC2-002` 为 `range_like`、无有效方向；`MC2-008` 有强 A 和后段稳定，但仍须突破上沿并回踩守住。区间边缘不能仅凭 H2 外形授权 |
| `MC2-007` vs `MC2-014` | 候选来源分别写 L1/L2，EMA 都允许空头 | 盲裁决都转为 `THREE_PUSH_like / L3_like`；两者都贴近支撑或位于末端，故 `rejected_gate`。计数到第三次后不能继续按普通 L1/L2 追空 |
| `MC2-012` vs `MC2-015` | 都是 `parabolic_climactic` 第三推 | `MC2-012` EMA/支撑不允许空头并直接 reject；`MC2-015` 趋势仍多头但处于 climax/突破边界，只能 wait。高潮第三推既不是自动反转，也不是自动延续入场 |
| `MC2-005` vs `MC2-010` | 都可见下破/突破后的新状态 | `MC2-005` 是 event-driven gap 且缺回测，保留 `event_boundary`；`MC2-010` 是 ordinary BOP-like 且回踩受控。事件重定价必须与普通 BOP 分开 |

## 七、最小输出

每次快筛至少填写：

```text
parent_state:
direction:
a_leg_quality:
b_leg_class:
visible_prior_boundary:
breakout_acceptance_status: none / watch / accepted / failed / event_boundary
lineage_status: same_lineage / reset / unclear / pending
calibration_visual_family: ABC_CONT_like / BOP_like / H_L_like / THREE_PUSH_like / NONE / UNCLEAR
calibration_attempt_label: H1_like / H2_like / L1_like / L2_like / H3_like / L3_like / pending / not_applicable
ema_gate_reading: long_pass / short_pass / fail_flat_or_opposite / pending
location_reading:
first_obstacle_reading:
selection_disposition: deep_reviewed / deferred_capacity / wait_for_structure / rejected_gate / event_boundary
main_uncertainty:
```

如果两个 family 都合理，保留 `main_uncertainty`，并把 `selection_disposition` 设为等待或边界；不要为了提高命中率强行统一。

## 八、研究与统计边界

- 本卡只属于 `PA Research only`；
- 不是人工专家真值，不报告 overall accuracy；
- 不创建量化扫描器或 automatic pattern detector；
- 不修改 Codex Trading，不连接 Futu/OpenD，不连接 Execution Agent；
- 不从 16 张校准图推导交易胜率、盈亏比或买卖授权；
- `conclusion: no-new-positive`；
- `validated win-rate: not-computable`。

# 订单类型与风险合同

文档状态：`document_status=adopted / research_state=provisional / handoff_status=not_ready / not-quantitative`

统一字段和枚举见[`PA Research 统一输出合同 v0.1`](../../docs/pa_research_output_schema_v0_1_CN.md)。本层只定义订单合同，不把研究状态、市场许可或 pattern 分支角色塞进 `order_branch`。

同一个 PA pattern 可以有不同订单方式。视觉助手必须先判断形态、位置和空间，再选择订单合同；不能因为形态像，就假设成交，也不能用后续盈利补写原订单。

## 1. 五种基础合同

| Canonical `order_branch` | 成交逻辑 | 适用情况 | 不能假设 |
| --- | --- | --- | --- |
| `stop_confirmation` | 价格真实越过冻结触发价 | 信号 K 后等待方向继续 | 只碰到、后来盈利不等于成交 |
| `limit_retest` | 价格真实回到预先定义的支撑/阻力区 | 旧边界、角色转换、缺口边缘回测 | 没回测不能记成交 |
| `market_close` | 在强收盘/确认时按实际价成交 | 继续等待会改变合同且空间仍合理 | 强 K 自动授权市价，滑点不能忽略 |
| `stop_limit` | 先触发，再在 limit 范围内成交 | 需要限制最差成交价 | 跳过 limit 仍算成交；可能完全不成交 |
| `observation_only` | 不建立交易合同 | 形态像但空间、事件、数据或结构不合格 | 观望不是失败，后来盈利不能改写它 |

新记录只使用上述下划线枚举。历史案例中的 `stop`、`limit-retest`、`market-close`、`reverse-stop` 和 `limit-edge` 作为别名保留，并分别映射到 `order_branch` 与 `branch_role`，不能再混写到同一个字段。

## 2. 方向语义必须准确

- 多头向上突破用 `buy stop`；回落到支撑/旧阻力转支撑等 `buy limit`；
- 空头向下突破用 `sell stop`；反弹到阻力/旧支撑转阻力等 `sell limit`；
- 低于当前市场价的 `sell limit` 可能是可立即成交的 marketable limit，不是“等价格再跌一点”；
- 等价格向下穿过触发位，必须用 `sell stop`；
- 高于当前市场价的 `buy limit` 也可能立即可成交，不能仅凭名称推断等待方向。

订单名称、触发条件、价格区域和实际成交状态要分栏记录。

## 3. 统一订单卡

```text
pattern_state:
decision_time:
timeframe_and_parent_contract:
signal_bar:
trigger_or_zone:
order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only
branch_role: same_contract / reverse_stop / role_reversal_retest / gap_reprice / lower_timeframe / management
actual_or_assumed_fill:
original_order_status: pending / triggered / filled / opening-skip / not-filled / fill-unknown
structural_stop_zone:
stop_price_or_area:
first_independent_obstacle:
space_to_first_obstacle: positive / borderline / blocked / unknown
rough_R_R:
gap_event_sector_adjustment:
management_action:
what_cancels_contract:
final_status:
```

数值可以先是区域和粗略范围；订单语义、因果时点和失效条件不能含糊。

## 4. 订单选择顺序

```text
背景/位置/形态
→ 信号 K 与触发或回测区
→ 订单类型与实际成交假设
→ 结构止损
→ 第一独立障碍
→ 粗略 R/R
→ 目标/MM与持仓管理
```

结构止损要覆盖让 thesis 失效的区域和正常测试空间；低周期短线止损只有在明确另立低周期合同后才能使用。第一障碍不足约 1R 时，默认 `valid_no_trade` 或降级，不跳到远端 MM。

## 5. 跳空、未成交和状态转换

开盘跳过原 stop 时：

1. 原合同记为 `opening-skip / fill-unknown / not-filled`；
2. 记录实际可能成交价；
3. 重算结构止损、第一障碍和 R/R；
4. 空间恶化就取消或观望；
5. 回到已知结构区才另立 `limit-retest`；
6. 缺口被接受并跟随时，另立 BOP/gap-and-go。

没有回测就没有 limit 成交；后来的价格到达不能把未成交合同变成成交。若 stop-limit 穿过 trigger 后跳过 limit，结果仍可能是未成交。

## 6. 已有仓位与新入场

已有仓位在第一障碍、MM 或动能减弱处分批止盈，是 `management`，不是新入场。新的追加仓必须重新写成交、止损、首障碍和 R/R；不能因为原仓已经盈利，就把新增仓位当成“零风险”。

进入目标区后，实体变小、重叠增加、跟随失败、长影线或成熟通道可以支持部分止盈；MM 是目标区，不要求机械精确触碰。

## 7. 与 pattern 的关系

H1/L1、H2/L2、ABC 和 BOP 默认先研究 `stop_confirmation`；区间边缘、角色转换和失败突破可研究 `limit_retest`；MTR/三推反向合同仍需要结构破坏和第二次确认；强收盘才考虑 `market_close`；扩张、事件、首障碍拥挤时应 `observation_only`。

订单合同属于 pattern 之上的共用层。改变订单类型，就同时改变入场价、止损、首障碍、目标、仓位和结果解释，不能只改一个价格。

## 8. 证据入口

完整协议见 [`订单分支视觉协议`](../../research/order_branch_visual_protocol_CN.md)，跨 pattern 审计见 [`八个 Pattern 的订单合同与 R/R 审计`](../../research/order_contract_cross_pattern_audit_CN.md)，专项证据见 [`订单类型与风险合同视觉证据审计`](../../research/order_risk_contract_visual_evidence_audit_2026-08-24_CN.md)。

本层只服务 PA Research 的视觉筛选、复盘和人工计划，不生成订单、不修改 Codex Trading、不连接 Execution Agent。

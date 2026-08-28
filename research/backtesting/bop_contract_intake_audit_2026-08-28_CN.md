# BOP 合同准入审计（2026-08-28）

日期：2026-08-28<br>
范围：仓库已有 BOP、BOP-like 和相邻边界案例是否具备日线级多日回踩合同<br>
状态：`research_only / intake_only / contract_frozen=no / no-new-positive`

## 一、准入定义

本轮只把下面的链条视为“真正的多日 BOP 回踩候选”：

```text
事前可见旧支撑/阻力或成熟区间边界
→ 日线收盘有效突破并得到接受
→ 后续日线离开边界
→ 数日后回到旧边界附近
→ 角色转换守住
→ 再次离开并有跟随
→ 实际订单、结构止损、第一障碍和事件字段可重建
```

多日不是机械的固定根数；但单日 15m 回调、突破日影线、下一根 K 线测试、开盘跳过后的重订和只发生过一次的回测，都不能命名为日线级多日 BOP。`gap-and-go`、H1/H2、ABC/L1、三推和区间边界可以作为相邻状态记录，但不能进入同一个 BOP 回放分母。

## 二、现有案例盘点

本次从既有 BOP 审计与案例文件整理出 15 个 intake 行，详见[`bop_contract_intake_2026-08-28.csv`](bop_contract_intake_2026-08-28.csv)。它是准入清单，不是回放输入；全部行都保持 `contract_frozen=no`。

| 分类 | 数量 | 案例 | 结论 |
| --- | ---: | --- | --- |
| 接受但没有多日回踩 | 2 | TSLA 2025-09、KLAC 2025-10 | 只能证明接受或状态切换，不能证明回踩合同 |
| 同日回测 | 2 | TSLA 2025-03、NKE 2025-10 | 有旧位回测语言，但没有日线级多日守住/再离开 |
| 缺口/开盘重订边界 | 5 | VRT、GOOGL、WMT、BKNG、QCOM | 原订单被跳过、未回测、事件或首障碍压缩；不能补写成交 |
| 首障碍/失败突破边界 | 1 | JPM 2025-09 | 第一阻力约 `0.39R`，且没有接受后多日回踩 |
| H/L、ABC、区间或晚趋势相邻案例 | 5 | META、TSLA 2025-08、TSLA 2025-05、TSLA 2026-05、TSLA 2025-12 | 不能把相邻形态改名为 BOP |
| 日线级多日 BOP 正向候选 | 0 | 暂无 | 继续 `no-new-positive` |

## 三、案例裁决重点

### 1. TSLA 2025-09：接受样本，不是多日回踩样本

[`TSLA 突破接受跟踪`](../tsla_h1_h2_bop_followup_2025-09-08_2025-09-12.md)记录了 `355.39–357.54` 旧阻力外的强收盘、15m 跟随，以及同日回调没有重新跌回旧阻力。这是清楚的 `breakout_acceptance`，但回测只在同日低周期发生；没有“先离开数日、再回到旧边界、守住后再次离开”的 Daily 序列。因此它保留为接受对照，不是多日 BOP 正例。

### 2. TSLA 2025-03 与 NKE：回测存在，但只到单日合同

[`TSLA 284 回测`](../tsla_abc_playbook_2025-03-04_284_retest.md)和[`NKE 空头 ABC/L1`](../nke_bearish_abc_minor_gap_boundary_2025-10-03_2025-10-29.md)都能训练“旧位回测是新订单合同”：TSLA 的 `283.8–284.3`、NKE 的 `66.78` 都有同日回测语言。但它们分别属于跳空后的单日回测和 ABC/L1 小缺口分支，不能升级成日线级多日 BOP。

### 3. 缺口和开盘重订：先否决旧合同

VRT、GOOGL、WMT、BKNG、QCOM 的共同边界是：原 stop 被开盘跳过、没有真实回到旧边界、角色转换没有独立冻结、首障碍过近或进入财报窗口。缺口后的重订可以另立合同，但不能把原成交价、旧止损或后续路径倒灌给 BOP；在没有多日回踩和事件闭环前，全部留在边界层。

### 4. 相邻案例：保留隔离标签

JPM 的问题首先是首阻力拥挤；META 是阻力下的嵌套 H1/H2；两段 TSLA 2025-08、2026-05 和 2025-12 是 H/L、深回调或晚趋势边界；TSLA 2025-05 是父级交易区间。它们对 PA 识别有帮助，但没有完整 BOP 状态链，不能为了增加样本而重新命名。

## 四、机器可读准入结果

`bop_contract_intake_2026-08-28.csv` 逐行保留：

- `retest_class`：区分 `intraday-only`、`single-session`、`not-occurred`；
- `role_reversal_evidence`：区分旧位是否真的守住；
- `order_branch`：区分原订单、开盘重订、limit-retest 和 observation-only；
- `event_state`、`first_obstacle_evidence` 和 `space_evidence`：不把事件或 R/R 缺口藏起来；
- `missing_fields`：列出正式冻结前仍缺的订单、两年 Daily、EMA、lineage 和结果字段。

这个 CSV 不被回放器读取，也不增加 H/L 或 BOP 胜率分母。当前 15 行全部为边界/观察状态，`contract_frozen=no`。

## 五、最终结论

本轮没有找到同时满足以下条件的 BOP 合同：

```text
event-clean
parent-clear
old-boundary-preidentified
daily-acceptance
multi-day-retest-and-hold
role-reversal
re-departure-follow-through
actual-order-reconstructable
first-obstacle-space-positive
process-complete
```

正式结论保持：

> `BOP / daily-accepted / multi-day-retest-held / role-reversal / first-obstacle-space-positive / process-complete`：**no-new-positive**。

下一次只有在仓库新增完整的 Daily/低周期历史记录，能在结果发生前重建唯一订单分支、精确止损/目标、`max_hold_bars`、事件和 lineage 后，才可另写冻结合同。不能把本轮 15 个 intake 行当作交易样本，也不能把 `acceptance`、同日回测、gap-reprice 或相邻 H/L/ABC 结果混成多日 BOP 胜率。

## 六、范围声明

本审计只属于 PA Research。它不创建量化扫描器、不自动识别图表、不连接 Execution Agent、不修改 Codex Trading。

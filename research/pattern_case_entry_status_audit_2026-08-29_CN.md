# Pattern 案例入口与状态一致性审计（2026-08-29）

状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only`

## 审计目的与边界

本轮只审计 16 个 pattern 目录 README 的案例入口、代表性条件候选/边界/no-trade 文案，以及它们与 `patterns/README.md`、`research/abc_pattern_coverage_audit_CN.md`、`strategy/pattern_inventory_candidates.md` 的目录交叉关系。`patterns/` 是研究导航，不是量化扫描器或交易授权层。

`scope_boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`

本轮不下载行情、不查看新图、不运行正式回放、不新增样本，不改变 pattern 规则或 engine 有效语义。这里的案例链接只证明研究入口可导航，不把历史描述升级为统计证据。

## 16 个目录覆盖

下表是本轮实际核对的完整目录集合；核心八个与独立研究主题仍保持各自生命周期，不能因为都出现在同一索引而合并统计。

| 层级 | 目录 README | 当前状态与核对重点 |
| --- | --- | --- |
| core | [`01_h1_l1_first_entry`](../patterns/01_h1_l1_first_entry/README.md) | adopted / provisional；H1/L1 与 no-trade 分流 |
| core | [`02_h2_l2_second_entry`](../patterns/02_h2_l2_second_entry/README.md) | adopted / provisional；同一回调 lineage 与第二次尝试 |
| core | [`03_abc_continuation`](../patterns/03_abc_continuation/README.md) | adopted / provisional；强 A、受控 B、C 恢复与首障碍 |
| core | [`04_range_edge_second_entry`](../patterns/04_range_edge_second_entry/README.md) | adopted / provisional；区间边缘与 `valid_no_trade` |
| core | [`05_failed_breakout_climax`](../patterns/05_failed_breakout_climax/README.md) | adopted / provisional；失败接受、高潮与 no-trade |
| core | [`06_breakout_pullback_bop`](../patterns/06_breakout_pullback_bop/README.md) | adopted / provisional；BOP 状态切换与真实回踩 |
| core | [`07_mtr_reversal`](../patterns/07_mtr_reversal/README.md) | adopted / provisional；第二次反向确认与 `valid_no_trade` |
| core | [`08_three_push_h3_l3`](../patterns/08_three_push_h3_l3/README.md) | adopted / provisional；H3/L3、区间边缘、延续分流 |
| independent | [`09_vcp_minervini`](../patterns/09_vcp_minervini/README.md) | research_only / provisional；独立收缩主题 |
| independent | [`10_final_flag`](../patterns/10_final_flag/README.md) | research_only / provisional；末端压缩与状态分流 |
| independent | [`11_opening_reversal`](../patterns/11_opening_reversal/README.md) | research_only / provisional；开盘失败/接受 |
| independent | [`12_channel`](../patterns/12_channel/README.md) | research_only / provisional；通道与区间过渡 |
| independent | [`13_inside_bar_two_bar_reversal`](../patterns/13_inside_bar_two_bar_reversal/README.md) | research_only / provisional；内包、IOI 与两根反转 |
| independent | [`14_triangle_expanding_range`](../patterns/14_triangle_expanding_range/README.md) | research_only / provisional；收缩/扩张与突破接受 |
| independent | [`15_double_top_bottom`](../patterns/15_double_top_bottom/README.md) | research_only / provisional；双顶/双底与 MTR 边界 |
| independent | [`16_head_shoulders_rounded`](../patterns/16_head_shoulders_rounded/README.md) | research_only / provisional；头肩、圆形和颈线边界 |

## 发现与修复

### 1. IWM 案例入口断链已修复

`04_range_edge_second_entry/README.md` 的 `IWM 2024-04-17–04-30` 是一个带日期的案例行，但此前没有 Markdown 研究入口。现将它连接到[`区间边缘二次入场框架`](range_edge_second_entry_framework_CN.md)。该文件是现有框架锚点，不是新增的 IWM 专属图表或独立结果文件；案例仍维持下沿二次测试、约 1R 边界和 `valid_no_trade` 的原有描述，不增加回放分母。

### 2. 状态别名已统一

以下活动 README 中的历史写法已统一为统一输出合同的 `valid_no_trade`：

- `04_range_edge_second_entry`：RBLX、IWM；
- `05_failed_breakout_climax`：RBLX、COST；
- `07_mtr_reversal`：NFLX；
- `08_three_push_h3_l3`：XOM、UBER 及首障碍规则；
- `16_head_shoulders_rounded`：原 no-trade 说明。

同时修正 `research/README.md` 中的 `no_new_positive` 拼写漂移为 `no-new-positive`。这只是字段/结论别名归一化，不改变任何案例判断。

### 3. 未发现把边界案例升级为成功证据

交叉阅读 16 个 README、三个导航索引和现有覆盖审计后，没有发现把 `boundary`、`conditional` 或 `valid_no_trade` 写成已验证成功的新增表述。已有案例继续使用“条件候选”“边界”“观察”或明确 no-trade 语义；现阶段 `validated win-rate: not-computable` 仍然成立。

尤其是各目录已有的 `no-new-positive` 结论必须继续解释为“本轮没有新增可接纳的统计正例”，不是“没有任何形态值得研究”，也不是胜率为零。

## 验收口径

本轮通过以下静态检查后才可提交：

1. 16 个目录都仍由 `patterns/README.md`、覆盖审计和 strategy inventory 导航；
2. 各 README 中带日期的案例表行都有可解析的本地 Markdown 入口；
3. 活动 pattern 文档不再使用 `valid-no-trade` 或 `valid no-trade` 别名；
4. `valid_no_trade`、`no-new-positive` 和 `validated win-rate: not-computable` 的语义保持分离；
5. 文档验证器与 Python 回归测试覆盖本轮修复，且 Trading repo 的工作区不发生变化。

## 当前结论

案例入口与状态文案已对齐，仍没有新增可计入验证胜率的正例。研究结论保持 `no-new-positive`；`validated win-rate: not-computable`；本轮不产生交易授权、扫描器或 Execution Agent 连接。

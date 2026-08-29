# 选择记录与回放结果证据边界审计（2026-08-29）

状态：`research_only / audit_only / no-new-positive`

## 结论

本次只审计 PA Research 已存在的选择报告、候选卡、视觉记录、冻结合同和 replay/result 记录，没有下载行情、看新图、运行回放、增加样本或改变 pattern/engine 有效语义。审计确认：入场前的方向、主标签/内部标签、信号 K、触发、结构失效、结构止损、第一独立障碍、空间、事件和 lineage 必须在结果发生前冻结；成交、退出、胜负、胜率资格和实现 R 只能由独立的事后 replay/result 记录产生。

发现并修复一处明确的文档边界问题：`hl_next3_selection_2026-08-27_CN.md` 原来包含“回放与统计状态”及 `完成成交 / 胜率 / 实现 R` 汇总表。即使这些值都是 `0` 或不可计算，也会让选择记录看起来像事后结果记录。现在已移除该汇总，改为明确的 `frozen_pre_outcome` 事前记录边界；对应的“无合格合同、无回放分母”说明保留在独立的 `hl_next3_replay_2026-08-27_CN.md` 中。

其余检查未发现第二处同类倒灌：现有选择文件没有结果字段定义行，候选卡和视觉资产 README 没有实际成交/退出/胜负值，冻结合同 CSV 没有 post-outcome 列，当前 checkout 也没有持久化 `results.csv`、`summary.json`、`run_metadata.json` 或实际交易日志。结论继续为 `no-new-positive`；`validated win-rate: not-computable`。

## 审计范围与判定口径

本次逐项检查：

- 6 份 `research/backtesting/*_selection_*.md`，包括 `hl_large`、`hl_next` 至 `hl_next5`；
- `docs/daily_candidate_review_card_CN.md`、`docs/visual_pa_review_card_CN.md` 以及仓库中的候选/视觉研究记录；
- 11 个仓库内视觉资产 README、外部视觉 artifact manifest 及其 provenance 记录；
- 7 份冻结合同 CSV、2 份 ABC/BOP intake CSV 和所有已提交的 `*_replay_*.md` 结果报告；
- 已有的事前/事后隔离、旧结果 provenance、历史 replay/result-log 和 artifact inventory 审计。

选择记录、候选卡和视觉记录的事前字段包括：

```text
direction
primary_pattern / internal_label
signal_bar / new_trigger
structural_invalidation / structural_stop
first_independent_obstacle / space_status
event_context / lineage_id
```

这些字段只能使用决策日及其以前可观察的证据。结果记录的事后字段包括：

```text
fill_status / entry_price / entry_date
exit_price / exit_date / exit_reason / bars_held
path_result / first_obstacle_hit / trade_result
realized_R / win_rate_eligible / evidence_status
```

`first_obstacle_hit` 只描述路径过程，不能反向改写事前 `first_independent_obstacle` 或 `space_status`；`realized_R` 和胜负也不能反向改写方向、pattern、内部标签、事件或 lineage。结果中的 provenance 缺口只产生排除/描述性状态，不能补造事前证据。

## 发现与修复记录

### 1. `hl_next3` 选择报告

原文件把没有冻结合同这一事前结论与“可进入回放分母的成交”“完成成交”“胜率”“实现 R”放在同一个选择报告中。这个写法没有制造新的正例，但破坏了文件角色边界，容易把“没有合同”误读成一次结果统计。

修复内容：

1. 状态增加 `frozen_pre_outcome`；
2. 结论只保留候选方向/标签、无合同和事前排除理由；
3. 删除事后统计标题、结果表和完成成交/胜率摘要；
4. 增加事前记录边界，明确 replay/result 字段的唯一归属和不可反向改写规则。

### 2. 其他选择、候选和视觉记录

其余 5 份选择报告只保留冻结前结构、事件、EMA、空间、lineage 和排除理由；其中可能提到“后续回放”或链接到 replay 报告，但没有把实际成交、退出或实现 R 写成选择字段。候选卡与视觉卡的结果相关词只出现在边界说明/模板语义中，没有实际结果值；视觉 PNG 与 README 也不含事后标签或结果标记。

### 3. 冻结合同与 replay/result

7 份冻结合同 CSV 的列集合只包含入场前合同和 provenance 字段，不含 `fill_status`、`trade_result`、`realized_R`、退出字段、路径字段或胜率资格字段。replay/result 报告承担事后路径和统计说明，并保留合同 identity；已有结果 provenance 审计继续把缺少事前字段的旧结果标为 `historical_incomplete`/描述性，不把结果写回选择或合同。

仓库没有实际交易日志目录，也没有 Execution Agent 产物。历史外部 `results.csv` 仍按既有审计与当前分母边界处理，未被本次审计重新计数。

## 防回归约束

文档 validator 与回归测试新增以下检查：

- 所有 `*_selection_*.md` 必须声明 `frozen_pre_outcome`，不能出现 post-outcome 字段定义行；
- 选择报告不能重新出现“回放与统计状态”结果区块或 `完成成交 / 胜负 / 实现 R` 结果表；
- 冻结合同 CSV 的表头拒绝事后成交、退出、路径、胜负、实现 R 和胜率资格列；
- 本审计及各索引必须保留事前/事后字段分界、`no-new-positive` 和 `validated win-rate: not-computable`。

这些检查只保护记录边界，不识别 pattern、不生成股票池、不计算胜率、不下载行情，也不改变回放器的有效交易语义。

## 验证与范围声明

验证命令：

```powershell
git diff --check
py -3 -m compileall -q .
py -3 -m unittest discover -s tests -v
pwsh -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_pa_research_docs.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_pa_research_docs.ps1
```

本次验证结果：`git diff --check` 通过；`compileall` 通过；全套回归测试 `157/157` 通过；PowerShell 7 与 Windows PowerShell 5.1 validator 均通过，均报告 `281` 个 Markdown 和 `1780` 个链接。当前 checkout 仍没有持久化 replay 三件套或交易日志目录。

本记录只属于 **PA Research**（PA Research only）。范围声明：**no Codex Trading**、**no quantitative scanner**、**no Execution Agent**；不新增回放分母。当前总体研究结论保持 `no-new-positive`，`validated win-rate: not-computable`。

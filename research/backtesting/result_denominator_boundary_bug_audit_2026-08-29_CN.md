# 回放结果分母边界 bug 审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research `build_summary`、完成交易掩码、结果 bucket 和 artifact 结果列要求<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、发现的可复现问题

本轮只使用最小内存 result fixture，不下载行情、不增加冻结合同、不重跑正式回放，也不改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。

当结果行已经带有完整事前合同证据、`fill_status=filled`、`trade_result=win/loss/scratch`、有限 `realized_R` 和 `win_rate_eligible=yes`，但缺少 `path_result` 时，旧的 `_completed_trade_mask` 没有把空路径字段排除。这样的行可能进入 `completed_trade_count` 和 `win_rate_pct`，尽管缺少退出路径审计证据。

## 二、修复

- 完成交易掩码现在要求 `path_result` 非空；
- 缺失路径字段的行进入互斥的 `missing_path_result` 排除 bucket，不进入胜率分母；
- artifact validator 将 `path_result` 列列入当前结果 schema 的必需字段；缺列的旧/不完整 artifact 返回 `historical_incomplete`，不能作为当前验证样本；
- 既有非有限 `realized_R`、非法结果旗标、重复 sample/合同族、缺失事前 provenance、事件/空间派生 mismatch、共享 lineage/市场状态和持仓重叠的隔离逻辑保持不变。

这只收紧缺失结果路径证据的分母边界；对 engine `0.3.9` 的有效合同回放语义和已有结果数值不作改变，因此不升级 engine 版本。

## 三、验证结果

```text
new missing-path denominator regression: passed
existing duplicate/provenance/event/space/independence tests: passed
full unittest suite: 64 passed
document validation: passed
compileall and git diff --check: passed
```

## 四、结论与范围声明

本轮没有新增样本或新的市场结论，也没有把任何结果加入统计分母。当前结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

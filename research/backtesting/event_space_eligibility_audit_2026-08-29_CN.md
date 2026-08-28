# 事件与首障碍空间资格审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research 现有 H/L 冻结合同、ABC/BOP intake、回放摘要和人工审查记录<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计口径

本次不重新选股、不重新抓取行情、不重算历史交易结果。只检查已有的 `event_context`、`space_status`、`pre_entry_space_R`、首障碍和回放摘要，防止把事件未核实、空间未知或边界样本误读为普通非事件合格证据。

回放摘要现在对原始事件字符串做保守的 `event_bucket` 分类：

- `ordinary_non_event`：原始记录明确写明普通非事件，且没有事件驱动或 gap-reprice 冲突；
- `event_reviewed_non_event`：有事件核对/事件在窗口外的证据，但没有明确的普通非事件标签；
- `event_driven`、`earnings_adjacent`：单独分层；
- `event_unverified_or_pending`：事件过滤未核实、待定、需要重新核对或公开价格审查未闭合；
- `unknown`、`other_unclassified`：不能升级为普通非事件。

首障碍空间只把合同中明确冻结的 `space_status` 作为资格证据。旧合同虽能在回放后计算实际几何 `space_gate`，也不能倒推成事前的 `strict_ge_1R`。

## 二、现有 60 条冻结 H/L 合同

### 事件分层

| 保守 event_bucket | 合同数 | 解释 |
| --- | ---: | --- |
| `ordinary_non_event` | 11 | 原始记录明确包含普通非事件标签 |
| `event_reviewed_non_event` | 3 | 有事件窗口外/已核对信息，但没有直接使用普通非事件标签 |
| `event_driven` | 4 | 财报后、aftershock 或事件驱动路径 |
| `earnings_adjacent` | 1 | 与财报相邻，单独保留 |
| `event_unverified_or_pending` | 40 | 37 条历史事件过滤未核实，加上待定/重新审查记录 |
| `unknown` | 1 | 仅有 `none`，没有足够的普通非事件证据 |

这 60 条不能合并成一个普通非事件分母。尤其 `contract_frozen=yes` 只表示订单和结果合同在回放前冻结，不等于事件过滤已经逐条核实。

### 空间分层

| 合同空间 bucket | 合同数 | 解释 |
| --- | ---: | --- |
| `strict_ge_1R` | 9 | 明确填写事前 `>=1R` 空间 |
| `borderline` | 1 | 明确填写边界空间 |
| `unknown_contract_space` | 50 | 旧合同没有 `space_status/pre_entry_space_R` |

按两个条件交叉后，只有 7 条同时属于 `ordinary_non_event + strict_ge_1R`；另有 1 条普通非事件但空间为 borderline，3 条普通非事件的空间仍未知。这个 7 条只是资格覆盖数量，不是胜率验证样本。

## 三、发现的问题与修复

### 1. 摘要缺少事件/空间资格分层

此前 `summary.json` 按原始 `event_context` 字符串分组，顶层 `win_rate_pct` 容易被读成普通、空间合格样本的胜率。现在结果保留原始字段，同时增加 `event_bucket`、`contract_space_bucket`，并报告：

- 各事件 bucket 的合同数；
- 各空间 bucket 的合同数；
- `ordinary_non_event_completed_trade_count` 和其描述性胜率；
- `ordinary_non_event_strict_space_completed_trade_count` 和其描述性胜率；
- 明确的限制说明：未知/待定事件和未知空间不升级，所有结果仍是 descriptive only。

### 2. 旧合同没有被无证据回填

50 条旧合同继续保留 `unknown_contract_space`。没有用第一障碍与触发价的事后计算替代结果发生前的空间字段，也没有为了提高普通组数量而把 `earnings_filter_passed`、`none` 或未核实事件自动改写成普通非事件。

### 3. 校验器增加冲突保护

文档校验现在会检查：

- 冻结合同的 `event_context` 不得为空；
- `space_status` 若存在必须使用规范枚举；
- `strict_ge_1R/clearly_positive` 不能配小于 `1R` 的 `pre_entry_space_R`；
- `historical_event_filter_not_verified` 不能同时标成 `ordinary_non_event`；
- ABC/BOP intake 仍全部是 `contract_frozen=no`，不进入回放分母。

## 四、最终结论

本次没有新增可冻结的 ABC、BOP、H3 或 L3 合同，也没有增加 H/L 回放分母。普通非事件且事前空间严格合格的覆盖只有 7 条，且还要继续按方向、H/L 标签、事件、空间和 lineage 分层；不能据此计算可靠胜率或证明用户设定的 `60%` 目标。

`no-new-positive` 与 `validated win-rate: not-computable` 保持不变。

## 五、范围声明

本审计只属于 PA Research。不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD，不把 ABC、BOP、H/L、三推或事件分支混成同一统计分母。

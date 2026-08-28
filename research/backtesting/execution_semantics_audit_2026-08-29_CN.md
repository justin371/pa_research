# 回放执行语义审计（2026-08-29）

日期：2026-08-29<br>
范围：PA Research engine `0.3.9` 的订单触发、gap policy、保护性退出和 horizon 处理<br>
状态：`research_only / descriptive_only / no-new-positive`

## 一、审计范围

本轮只使用最小合成 OHLCV fixture 和已有单元测试，覆盖多空方向、`stop_confirmation`、`limit_retest`、`market_close`、`skip`/`accept_open`/`flag_only`、止损/目标 gap、同 K 止损目标冲突、时间退出和 data-end。没有下载行情、没有新增冻结合同、没有重跑正式回放，也没有改变 ABC/BOP/H1/H2/L1/L2/H3/L3 规则。

## 二、核对结果

- 多头和空头的 stop/limit 触发方向、结构止损/目标判定和 `realized_R` 符号保持对称；
- `gap_policy=skip` 记录 `opening-skip`，不进入交易分母；`accept_open` 使用实际开盘价，`flag_only` 同样接受实际开盘价但保留 `gap_adjustment=flag_only`；
- gap 后若旧止损/目标相对实际开盘价不再满足方向几何，返回 `gap-reprice-required`，不静默复用旧合同；
- 入场 K 线完成后才挂保护性止损/目标；后续 K 线同时触及两者时标记 `ambiguous_intrabar`，不进入胜率分母；
- 非 `market_close` 时间退出在允许观察窗口结束后的下一根开盘执行，`market_close` 按收盘计数；数据末尾无可执行时间退出时保持 `incomplete-horizon`；
- 保护性止盈/止损即使因下一根开盘 gap 成交，也能按方向分类为 `target` 或 `stop`，而不是误报 `data_end`。

本轮未发现需要改变生产执行语义的 bug；补充了 gap flag 和空头 stop-confirmation 的对称回归测试，并将 `flag_only` 文档化。

## 三、验证结果

```text
new execution symmetry/gap tests: 2 passed
full unittest suite: 66 passed
document validation: passed
compileall and git diff --check: passed
```

engine 版本仍为 `0.3.9`，因为有效合同的成交、退出和 horizon 语义没有改变；本轮只是补充覆盖和审计证据。

## 四、结论与范围声明

本轮没有新增样本或市场结论，统计口径继续隔离 pattern、事件、空间和 lineage。当前结论保持：

```text
no-new-positive
validated win-rate: not-computable
```

本文件只属于 PA Research；不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent，不连接 Futu/OpenD。

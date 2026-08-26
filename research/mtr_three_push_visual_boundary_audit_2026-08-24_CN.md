# MTR 与三推/H3-L3 视觉边界复核

日期：`2026-08-24`；修订：`2026-08-26`；状态：`visual-research / provisional / not-statistical`

## 复核顺序

```text
父级状态 → 主要位置 → 三次尝试是否同一 lineage → 压力减弱/扩张
→ 反向结构破坏 → 反向第二次确认 → 首障碍/结构止损/订单 → 裁决
```

三推只描述原方向的三次尝试；MTR 描述控制权是否改变。原方向 H3/L3 与反方向 H1/H2、L1/L2 是两套计数，不能直接合并。

## 边界矩阵

| 外观 | 更准确的状态 | 不应做的事 | 进入下一层的证据 |
| --- | --- | --- | --- |
| 第三推更快、更宽、收盘靠极值 | `continuation_or_climax` | 仅凭 H3/L3 逆势 | 回调后失败或真正接受反转结构 |
| 第三推减弱且在主要位置 | `exhaustion_candidate` | 把第一根反向 K 当确认 MTR | 反向局部结构破坏、第二次确认、首障碍有空间 |
| 三次围绕区间边界反复 | `range_repeat_test`；若第三推在上沿/下沿并有拒绝，则加 `range_edge_three_push` | 继承开放趋势 ABC/H-L 计数，或把第三推自动当反转 | 边缘反向触发、止损和中线空间；区间外接受并回测守住则重建趋势合同 |
| 三次沿通道运行 | `channel_continuation` | 把触碰通道线当反转 | 通道破坏、接受、跟随及空间同时成立 |
| 三推/双高后强收盘突破 | `failed-MTR-thesis → BOP` | 继续保留旧反向合同 | 新 BOP 回踩合同独立审计 |

## 案例裁决

- `KLAC 2025-03-17–03-26`：H3 衰竭候选，空头反向跟随和空间较好；仍是单方向条件样本，不冻结规则。
- `TSLA 2025-09-08–09-12`：阻力下三推/双高只构成反转观察；`2025-09-11` 接受突破后切换 BOP，MTR thesis 失效。
- `NFLX 2024-08-05–09-26`：高位多次测试有 MTR-like 外观，但首支撑过近，触发时即 `valid_no_trade`。
- `ASML 2025-05-19–06-13`：低位重复测试属于区间过渡，不能补齐 L3 反转证据。
- `TSLA 2026-05-19–06-26` 与 `XOM 2024-07-18–08-02`：前者短线衰竭但首障碍不足，后者第三推扩张；两者都不是波段 MTR 正例。

## 统一输出

```text
three_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear
range_edge_three_push: yes / no / pending
range_edge_side: upper / lower / none / pending
mtr_state: not_started / reversal_attempt / candidate / confirmed_for_research / failed
reverse_lineage: none / H1-like / H2-like / L1-like / L2-like
first_obstacle: clear / crowded / unknown
decision: research_candidate / conditional / valid_no_trade / observation_only
```

当前结论：H3 衰竭只有 KLAC 条件候选，L3 衰竭仍无过程完整正例；三推的主要价值是识别压力状态和避免误判，而不是直接授权反转。MTR 仍须等待反向二次确认、首障碍和路径审计。

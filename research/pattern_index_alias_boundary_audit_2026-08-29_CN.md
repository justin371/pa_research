# PA Research Pattern 索引、别名与主次标签边界审计

日期：2026-08-29
文档状态：`document_status=adopted / document_maturity=provisional / handoff_status=not_ready / research-only / not-quantitative`

## 目的与范围

本次只审计 PA Research 内部的 pattern 目录、研究索引、本地链接、别名和统一输出字段边界。审计范围包括 `patterns/README.md`、16 个 pattern 目录、`strategy/pattern_inventory_candidates.md`、`research/abc_pattern_coverage_audit_CN.md`、统一输出合同及代表性研究示例。

本次不下载行情、不查看新图、不运行正式回放、不增加样本、不计算胜率，也不改变 engine 的有效枚举或回放语义。它是索引和文档合同修复，不是新的 pattern 规则发布。`validated win-rate: not-computable` 仍然成立。

`scope_boundary: PA Research only; no Codex Trading; no quantitative scanner; no Execution Agent`。Canonical shorthand 为 `internal_label=H1 / L1`、`internal_label=H2 / L2` 和 `internal_label=H3 / L3`。

## 1. 盘点结论

当前仓库有 16 个实际 pattern 目录：前 8 个是 PA Research 的核心结构，后 8 个是独立的视觉研究主题。`patterns/README.md`、`strategy/pattern_inventory_candidates.md` 和覆盖审计现在都提供可追踪入口；覆盖审计此前遗漏的 `09_vcp_minervini` 已补回。

核心结构与独立主题必须分层：独立主题可以帮助视觉识别和边界对照，但不能因为目录名称就成为统一输出合同中的核心 `primary_pattern`，也不能与 ABC、BOP、H/L 或三推混合统计。

## 2. 16 个目录与 canonical 角色

| # | 目录入口 | 层级 | canonical 角色与当前边界 |
| --- | --- | --- | --- |
| 01 | [`H1/L1 第一次入场`](../patterns/01_h1_l1_first_entry/README.md) | 核心八个 | 日线母级通常是 `ABC_CONT`，`internal_label=H1 / L1`；历史兼容枚举 `H1_L1` 不等于新的日线主标签 |
| 02 | [`H2/L2 第二次入场`](../patterns/02_h2_l2_second_entry/README.md) | 核心八个 | 日线母级通常是 `ABC_CONT`，`internal_label=H2 / L2`；历史兼容枚举 `H2_L2` 不等于新的日线主标签 |
| 03 | [`ABC 趋势延续`](../patterns/03_abc_continuation/README.md) | 核心八个 | `primary_pattern: ABC_CONT`；A/B/C 是母级结构，H/L 是内部尝试或关系描述 |
| 04 | [`区间边缘二次入场`](../patterns/04_range_edge_second_entry/README.md) | 核心八个 | 只有区间边缘失败突破和二次确认合同才用 `RFB`；不把趋势 H2/L2 计数直接搬进区间中部 |
| 05 | [`失败突破与高潮`](../patterns/05_failed_breakout_climax/README.md) | 核心八个 | 失败突破使用 `RFB`；高潮、扩张或尚未闭合的反转观察可用 `other` 加状态描述，不能自动变成 BOP |
| 06 | [`突破回踩 / BOP`](../patterns/06_breakout_pullback_bop/README.md) | 核心八个 | 主标签固定为 `BOP`；接受、回踩、角色转换等写入 `state_transition`，不能拼成 `BOP_acceptance` 等新主标签 |
| 07 | [`MTR 趋势反转`](../patterns/07_mtr_reversal/README.md) | 核心八个 | 只有成熟趋势、控制权改变、反向确认和空间等条件闭合后才用 `MTR`；双顶、三推等只是证据 |
| 08 | [`三推 / H3-L3 压力状态`](../patterns/08_three_push_h3_l3/README.md) | 核心八个 | 三推合同才用 `H3_L3`，并明确 `internal_label=H3 或 L3`；不完整计数使用 `other`/`pending`，不能凭“三次”自动升级 |
| 09 | [`VCP / Minervini 独立主题`](../patterns/09_vcp_minervini/README.md) | 独立主题 | 保留 VCP/Minervini 的目录级视觉语义；未扩展统一 schema 时，统一记录使用 `other` 加 `secondary_context`/`pattern_like_reason` |
| 10 | [`Final Flag 独立主题`](../patterns/10_final_flag/README.md) | 独立主题 | 保留 Final Flag 的目录级语义；不把它当作 MTR 或 `ABC_CONT` 的别名 |
| 11 | [`Opening Reversal 独立主题`](../patterns/11_opening_reversal/README.md) | 独立主题 | 保留开盘第一波接受/失败和反向机会的视觉语义；开盘事件、触发和订单另行记录 |
| 12 | [`Channel 独立主题`](../patterns/12_channel/README.md) | 独立主题 | 保留紧通道、宽通道和状态切换的背景语义；通道本身不创造 H/L、BOP 或 MTR 主标签 |
| 13 | [`Inside Bar / Two-Bar Reversal 独立主题`](../patterns/13_inside_bar_two_bar_reversal/README.md) | 独立主题 | 保留母 K、内包和两根反转边界；OHLC 或接受条件未冻结时保持观察状态 |
| 14 | [`Triangle / Expanding Range 独立主题`](../patterns/14_triangle_expanding_range/README.md) | 独立主题 | 保留三角形、扩张区间和区间内区间的视觉语义；突破接受或失败另写状态转换 |
| 15 | [`Double Top/Bottom 独立主题`](../patterns/15_double_top_bottom/README.md) | 独立主题 | 双顶/双底首先是位置形状；根据父级和接受/失败再归入 RFB、MTR 或普通回调 |
| 16 | [`Head & Shoulders / Rounded 独立主题`](../patterns/16_head_shoulders_rounded/README.md) | 独立主题 | 保留头肩、圆顶和圆底的视觉边界；颈线、确认和空间不完整时不升级为 MTR |

## 3. canonical 别名规则

### 3.1 日线母级与内部计数

- 当前统一输出的日线候选主标签只允许 `ABC_CONT` 或 `BOP`；历史/兼容回放枚举仍可保留 `H1_L1`、`H2_L2`、`H3_L3`、`RFB`、`MTR`、`other`，但不能把兼容枚举误写成新的生产规则。
- `H1`、`H2`、`L1`、`L2` 是 ABC 或局部回调中的内部尝试标签，不是新的独立母级结构。它们写入 `internal_label` 或 `secondary_context`。
- `H3`、`L3` 只有在三推/复杂回调合同确实闭合时才使用；`H3_L3` 不能作为含糊的内部标签，未完成计数必须保留 `pending` 或 `other`。
- Daily、4H、1H 和 15m 的计数不相加。低周期确认也不能把日线母级改写成另一个主标签。

### 3.2 状态转换与独立主题

- `BOP` 是主标签；`breakout_acceptance`、`pullback_hold`、`role_reversal` 等属于 `state_transition` 或关系字段。
- `RFB` 表示已满足失败突破/区间边缘合同的结构，不能用来包装普通趋势回调；`MTR` 需要独立的控制权改变和反向确认。
- `ABC_CONT`、`BOP`、`H3_L3`、`RFB` 和 `MTR` 之间可以存在历史关系，但关系不是额外优势，也不能把多个名称叠加为多个机会。
- VCP、Final Flag、Opening Reversal、Channel、Inside Bar、Triangle、Double Top/Bottom、Head & Shoulders/Rounded 仍是独立主题。它们的目录名称不是统一输出主标签的别名；在 schema 未扩展前，使用 `other` 加清楚的次级语义和观察原因。

## 4. 已修复的有证据问题

1. `research/priority_pattern_visual_candidate_matrix_2026-08-24_CN.md` 的代表性矩阵曾把 `H2`、`L1`、`H3`、`L3`、`range-edge second-entry` 和 `BOP / breakout-acceptance` 放在主标签列。现在改为母级 `ABC_CONT`、`BOP`、`RFB`、`H3_L3` 或 `other`，并单独记录内部标签和关系；矩阵末尾示例也同步改为 `primary_pattern: ABC_CONT` 与 `internal_label: H2`。
2. `research/cross_pattern_visual_priority_audit_2026-08-24_CN.md` 的 BOP 示例曾把接受状态写进主标签。现在保留 `primary_pattern: BOP`，用 `state_transition: breakout_acceptance` 表达状态切换。
3. `strategy/reviews/2026-06-25-tsla-meta-example.md` 是不完整的历史观察，曾同时写 `primary_pattern: H3_L3` 和 `internal_label: pending`。现在保留观察语义，改用 `primary_pattern: other`、`pattern_like_reason` 和 `pending`，避免把未完成计数冻结成三推合同。
4. `strategy/pattern_inventory_candidates.md` 新增 16 个目录的直接入口与 canonical 字段边界；`research/abc_pattern_coverage_audit_CN.md` 补回 `09_vcp_minervini` 直接链接；研究索引、策略索引和 pattern 索引都链接到本审计。

上述修复只涉及索引、示例和文档边界，不新增样本，不改写历史结果，不改变 engine 有效语义。既有 `no-new-positive` 结论保持不变。

## 5. 验证与范围声明

- 16 个目录均存在且 `patterns/README.md` 的入口完整；核心八个与独立八个分层可追踪。
- `primary_pattern`、`internal_label`、`secondary_context` 和 `state_transition` 的职责已在代表性矩阵、候选清单、覆盖审计和本报告中对齐。
- 当前没有因这次索引修复而产生新的 validated sample 或胜率分母；`validated win-rate: not-computable`。
- 本 goal 不修改 Codex Trading，不创建量化扫描器，不连接 Execution Agent；也不把 PA Research 变成执行系统。

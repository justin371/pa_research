[CmdletBinding()]
# Keep this script UTF-8-with-BOM encoded for Windows PowerShell 5.1 compatibility.
param(
    [string]$RepoRoot
)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $repoRoot = Split-Path -Parent $PSScriptRoot
} else {
    try {
        $repoRoot = (Resolve-Path -LiteralPath $RepoRoot -ErrorAction Stop).Path
    } catch {
        Write-Error "RepoRoot does not exist: $RepoRoot"
        exit 1
    }
    if (-not (Test-Path -LiteralPath $repoRoot -PathType Container)) {
        Write-Error "RepoRoot is not a directory: $RepoRoot"
        exit 1
    }
}
$errors = [System.Collections.Generic.List[string]]::new()
$checkedLinks = 0

function Add-ValidationError {
    param([Parameter(Mandatory)][string]$Message)
    [void]$errors.Add($Message)
}

function Get-TrimmedText {
    param([AllowNull()][object]$Value)
    if ($null -eq $Value) { return '' }
    $text = ([string]$Value).Trim()
    # Match pandas.read_csv's default missing-value tokens used by engine.py.
    $pandasMissingTokens = @(
        '', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
        '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NULL', 'NaN', 'None', 'n/a',
        'nan', 'null'
    )
    if ($pandasMissingTokens -ccontains $text) {
        return ''
    }
    return $text
}

function Get-Utf8Text {
    param([Parameter(Mandatory)][string]$Path)
    return [System.IO.File]::ReadAllText($Path, [System.Text.UTF8Encoding]::new($false))
}

function Test-FiniteNumber {
    param(
        [AllowNull()][object]$Value,
        [ref]$Number
    )

    $text = Get-TrimmedText $Value
    if ([string]::IsNullOrWhiteSpace($text)) { return $false }
    $parsed = 0.0
    if (-not [double]::TryParse(
        $text,
        [Globalization.NumberStyles]::Float,
        [Globalization.CultureInfo]::InvariantCulture,
        [ref]$parsed
    )) { return $false }
    if ([double]::IsNaN($parsed) -or [double]::IsInfinity($parsed)) { return $false }
    $Number.Value = $parsed
    return $true
}

function Test-ValidDate {
    param([AllowNull()][object]$Value)

    $text = Get-TrimmedText $Value
    if ([string]::IsNullOrWhiteSpace($text)) { return $false }
    $parsed = [DateTime]::MinValue
    return [DateTime]::TryParse(
        $text,
        [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::AllowWhiteSpaces,
        [ref]$parsed
    )
}

function Get-CanonicalDateKey {
    param([AllowNull()][object]$Value)

    $text = Get-TrimmedText $Value
    if ([string]::IsNullOrWhiteSpace($text)) { return '' }
    $parsed = [DateTimeOffset]::MinValue
    if (-not [DateTimeOffset]::TryParse(
        $text,
        [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::AllowWhiteSpaces,
        [ref]$parsed
    )) {
        return $text.ToLowerInvariant()
    }
    return $parsed.ToString('yyyy-MM-dd', [Globalization.CultureInfo]::InvariantCulture)
}

function Test-PathInsideRepo {
    param(
        [Parameter(Mandatory)][string]$SourcePath,
        [Parameter(Mandatory)][string]$RawTarget
    )

    $target = $RawTarget.Trim()
    if ($target.StartsWith('<') -and $target.EndsWith('>')) {
        $target = $target.Substring(1, $target.Length - 2)
    }
    if ([string]::IsNullOrWhiteSpace($target) -or $target.StartsWith('#')) {
        return
    }
    if ($target -match '^(?i)(https?|mailto|data):') {
        return
    }

    $fragmentIndex = $target.IndexOf('#')
    if ($fragmentIndex -ge 0) {
        $target = $target.Substring(0, $fragmentIndex)
    }
    $target = $target.Trim()
    if ([string]::IsNullOrWhiteSpace($target)) {
        return
    }
    if ([IO.Path]::IsPathRooted($target)) {
        Add-ValidationError "$SourcePath -> absolute local link: $RawTarget"
        return
    }

    $sourceDirectory = Split-Path -Parent $SourcePath
    $normalizedTarget = $target -replace '/', [IO.Path]::DirectorySeparatorChar
    $resolved = [IO.Path]::GetFullPath((Join-Path -Path $sourceDirectory -ChildPath $normalizedTarget))
    $rootWithSeparator = $repoRoot.TrimEnd('\') + '\'
    if (-not $resolved.Equals($repoRoot, [StringComparison]::OrdinalIgnoreCase) -and
        -not $resolved.StartsWith($rootWithSeparator, [StringComparison]::OrdinalIgnoreCase)) {
        Add-ValidationError "$SourcePath -> link escapes repository: $RawTarget"
        return
    }
    if (-not (Test-Path -LiteralPath $resolved)) {
        Add-ValidationError "$SourcePath -> missing local link: $RawTarget"
    }
}

$requiredFiles = @(
    'README.md',
    'docs/README.md',
    'docs/pa_research_output_schema_v0_1_CN.md',
    'docs/pa_research_daily_selection_rules_v0_1_CN.md',
    'docs/visual_pa_review_card_CN.md',
    'docs/daily_candidate_review_card_CN.md',
    'docs/common_context.md',
    'patterns/README.md',
    'patterns/08_three_push_h3_l3/README.md',
    'foundations/README.md',
    'research/README.md',
    'research/process_improvement_audit_2026-08-28_CN.md',
    'research/backtesting/contract_coverage_audit_2026-08-28_CN.md',
    'research/backtesting/abc_bop_contract_intake_2026-08-28.csv',
    'research/backtesting/abc_bop_contract_intake_audit_2026-08-28_CN.md',
    'research/backtesting/abc_bop_candidate_freeze_review_2026-08-28_CN.md',
    'research/backtesting/abc_bullish_candidate_contract_audit_2026-08-28_CN.md',
    'research/backtesting/cross_pattern_statistics_isolation_audit_2026-08-29_CN.md',
    'research/backtesting/event_space_eligibility_audit_2026-08-29_CN.md',
    'research/backtesting/event_space_lineage_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/special_subtype_event_axis_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/hl_leg_quality_location_axis_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/event_bucket_label_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/hl_lineage_market_context_independence_audit_2026-08-29_CN.md',
    'research/backtesting/hl_order_gap_contract_audit_2026-08-29_CN.md',
    'research/backtesting/hl_report_state_count_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/replay_outcome_denominator_audit_2026-08-29_CN.md',
    'research/backtesting/replay_lineage_independence_audit_2026-08-29_CN.md',
    'research/backtesting/replay_provenance_reproducibility_audit_2026-08-29_CN.md',
    'research/backtesting/frozen_contract_field_partition_audit_2026-08-29_CN.md',
    'research/backtesting/pre_entry_result_evidence_isolation_audit_2026-08-29_CN.md',
    'research/backtesting/pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md',
    'research/backtesting/legacy_result_provenance_completeness_audit_2026-08-29_CN.md',
    'research/backtesting/artifact_schema_roundtrip_audit_2026-08-29_CN.md',
    'research/backtesting/validator_engine_contract_parity_audit_2026-08-29_CN.md',
    'research/backtesting/report_index_inventory_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/batch_report_numeric_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/abc_bop_intake_schema_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/historical_replay_result_log_provenance_audit_2026-08-29_CN.md',
    'research/candidate_visual_record_consistency_audit_2026-08-29_CN.md',
    'research/unified_output_state_axis_audit_2026-08-29_CN.md',
    'research/pattern_index_alias_boundary_audit_2026-08-29_CN.md',
    'research/backtesting/three_push_h3_l3_contract_boundary_audit_2026-08-29_CN.md',
    'research/backtesting/three_push_strategy_case_contract_audit_2026-08-29_CN.md',
    'research/backtesting/h3_l3_candidate_screen_provenance_audit_2026-08-29_CN.md',
    'research/pattern_visual_preflight_audit_2026-08-29_CN.md',
    'research/pattern_case_entry_status_audit_2026-08-29_CN.md',
    'research/pattern_state_axis_field_enum_audit_2026-08-29_CN.md',
    'research/common_visual_preflight_field_consistency_audit_2026-08-29_CN.md',
    'research/evidence_scope_status_boundary_audit_2026-08-29_CN.md',
    'research/entry_geometry_state_boundary_audit_2026-08-29_CN.md',
    'research/three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md',
    'research/h_l_lineage_visual_boundary_audit_2026-08-24_CN.md',
    'research/visual_recognition_round5_two_year_daily_2026-08-24_CN.md',
    'research/visual_recognition_round4_historical_practice_2026-08-24_CN.md',
    'research/backtesting/visual_evidence_canonical_boundary_audit_2026-08-29_CN.md',
    'research/visual_recognition_smoke_test_2026-08-24_CN.md',
    'research/visual_pattern_triage_protocol_CN.md',
    'research/assets/visual_recognition/2026-08-24/round2_multisymbol/README.md',
    'research/assets/visual_recognition/2026-08-24/round3_hl_drills/README.md',
    'research/assets/visual_recognition/2026-08-24/round3_l1_l2_mar/README.md',
    'research/assets/visual_recognition/2026-08-24/round4_historical_practice/README.md',
    'research/assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md',
    'research/assets/visual_recognition/2026-08-24/tsla_public_mtf/README.md',
    'research/assets/visual_recognition/2026-08-26/hl_contract_batch/README.md',
    'research/assets/visual_recognition/2026-08-26/hl_contract_batch2/README.md',
    'research/assets/visual_recognition/2026-08-27/hl_large_backtest/README.md',
    'research/assets/visual_recognition/2026-08-27/hl_next_backtest/README.md',
    'research/assets/visual_recognition/2026-08-27/hl_next2_backtest/README.md',
    'research/backtesting/visual_recognition_canonical_boundary_audit_2026-08-29_CN.md',
    'research/backtesting/visual_asset_canonical_boundary_audit_2026-08-29_CN.md',
    'research/backtesting/visual_asset_provenance_coverage_audit_2026-08-29_CN.md',
    'research/backtesting/visual_authority_schema_alignment_audit_2026-08-29_CN.md',
    'research/backtesting/pattern_foundation_canonical_contract_audit_2026-08-29_CN.md',
    'research/backtesting/required_report_index_coverage_audit_2026-08-29_CN.md',
    'research/backtesting/conclusion_boundary_consistency_audit_2026-08-29_CN.md',
    'research/backtesting/visual_capability_boundary_audit_2026-08-29_CN.md',
    'research/backtesting/visual_asset_pre_entry_evidence_audit_2026-08-29_CN.md',
    'research/backtesting/external_visual_artifact_provenance_audit_2026-08-29_CN.md',
    'research/backtesting/external_visual_artifact_manifest_2026-08-29.json',
    'research/backtesting/bop_contract_intake_2026-08-28.csv',
    'research/backtesting/bop_contract_intake_audit_2026-08-28_CN.md',
    'scripts/validate_pa_research_artifact.py',
    'strategy/README.md'
)
foreach ($relativePath in $requiredFiles) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) {
        Add-ValidationError "missing required file: $relativePath"
    }
}

$canonicalResearchIndexRelativePaths = @(
    'README.md',
    'docs/README.md',
    'research/README.md',
    'research/backtesting/README.md',
    'patterns/README.md',
    'foundations/README.md',
    'strategy/README.md'
)
$canonicalResearchIndexContents = foreach ($indexRelativePath in $canonicalResearchIndexRelativePaths) {
    $indexAbsolutePath = Join-Path -Path $repoRoot -ChildPath ($indexRelativePath -replace '/', '\')
    if (Test-Path -LiteralPath $indexAbsolutePath -PathType Leaf) {
        Get-Utf8Text -Path $indexAbsolutePath
    }
}
$requiredResearchReportPaths = @($requiredFiles | Where-Object {
    ($_ -match '^research/[^/]+\.md$' -or $_ -match '^research/backtesting/[^/]+\.md$') -and
    $_ -notmatch '/README\.md$'
})
foreach ($relativePath in $requiredResearchReportPaths) {
    $fileName = [IO.Path]::GetFileName($relativePath)
    $indexMatches = @($canonicalResearchIndexContents | Where-Object { $_.Contains($fileName) })
    if ($indexMatches.Count -eq 0) {
        Add-ValidationError "required research report is not referenced by a canonical index: $relativePath"
    }
}

$coreBoundaryIndexPaths = @(
    'README.md',
    'docs/README.md',
    'patterns/README.md',
    'research/README.md',
    'strategy/README.md',
    'research/backtesting/README.md'
)
$coreBoundaryTokens = @(
    'PA Research only',
    'no-new-positive',
    'validated win-rate: not-computable',
    '60%',
    '不是 Codex Trading 生产规则',
    '量化扫描器',
    'Execution Agent'
)
foreach ($relativePath in $coreBoundaryIndexPaths) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in $coreBoundaryTokens) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "core boundary index is missing token '$token': $relativePath"
        }
    }
}

$trackedHistoricalVisualCandidatePaths = @(
    'research/crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md',
    'research/meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md',
    'research/msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md',
    'research/nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md',
    'research/visual_screen_candidate_grid_2024_2025_CN.md'
)
foreach ($relativePath in $trackedHistoricalVisualCandidatePaths) {
    $fileName = [IO.Path]::GetFileName($relativePath)
    $indexMatches = @($canonicalResearchIndexContents | Where-Object { $_.Contains($fileName) })
    if ($indexMatches.Count -eq 0) {
        Add-ValidationError "tracked historical visual candidate is not referenced by a canonical index: $relativePath"
    }
}

$markdownFiles = Get-ChildItem -LiteralPath $repoRoot -Recurse -File -Filter '*.md' | Where-Object {
    $relative = $_.FullName.Substring($repoRoot.Length + 1)
    -not $relative.StartsWith('.codex' + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
}
foreach ($file in $markdownFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1)
    $content = Get-Utf8Text -Path $file.FullName

    foreach ($match in [regex]::Matches($content, '(?<!\!)\[[^\]]*\]\(([^)\r\n]+)\)|!\[[^\]]*\]\(([^)\r\n]+)\)')) {
        $target = if ($match.Groups[1].Success) { $match.Groups[1].Value } else { $match.Groups[2].Value }
        $checkedLinks++
        Test-PathInsideRepo -SourcePath $file.FullName -RawTarget $target
    }

    if ($content -match '(?i)C:\\Users\\lwang\\Documents\\Codex\\worktrees\\trading|\.local/research/replay|current checkout') {
        Add-ValidationError "non-portable Codex Trading path or checkout wording: $relativePath"
    }
}

$canonicalChecks = @{
    'docs/pa_research_output_schema_v0_1_CN.md' = @(
        'document_maturity: provisional',
        'chart_scope: full / partial / unavailable',
        'a_leg_quality: strong / ordinary / unclear / event_driven',
        'b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear',
        'special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none',
        'b_leg_location:',
        'direction: long / short / no_valid_direction',
        'daily_candidate` 只允许 `ABC_CONT` 或 `BOP`',
        '当 `contract_scope: daily_candidate` 时，`timeframes_seen` 必须只写 `Daily`',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'range_edge_three_push` 只是区间边缘位置/分支旗标，不是 `primary_pattern`',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'event_bucket:',
        'win_rate_eligible:',
        'pre_entry_provenance_status:',
        'pre_entry_provenance_missing_fields:',
        'planned_entry_trigger:',
        'first_obstacle_hit:',
        'max_hold_bars',
        'lineage_id:',
        'market_context_id:',
        'duplicate_result',
        'price_file_sha256',
        'backtesting_version',
        'python_version',
        'engine_source_sha256',
        'results_file_sha256',
        'summary_provenance',
        'contract_eligibility_mismatch_count',
        'event_bucket_mismatch_count',
        'contract_space_bucket_mismatch_count',
        'bop_state:',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'gate_result:',
        'contract_scope:',
        '`actual_fill_or_open_skip` 只表示研究合同/历史回放的订单路径注释，不是券商或账户的实际成交日志',
        '真实交易日志必须来自另立的独立来源'
    )
    'research/backtesting/contract_coverage_audit_2026-08-28_CN.md' = @(
        'validated win-rate: not-computable',
        'conclusion: no-new-positive',
        '本文件只属于 PA Research',
        '不创建量化扫描器',
        '不连接 Execution Agent'
    )
    'research/backtesting/conclusion_boundary_consistency_audit_2026-08-29_CN.md' = @(
        'validated win-rate: not-computable',
        'conclusion: no-new-positive',
        'win_rate_eligible',
        'research_positive_conditional',
        'ready_for_system',
        '不修改 Codex Trading',
        '不创建量化扫描器',
        '不连接 Execution Agent'
    )
    'research/backtesting/visual_capability_boundary_audit_2026-08-29_CN.md' = @(
        'visual_capability: human_chart_review / approximate_pattern_like_only',
        'validated win-rate: not-computable',
        'conclusion: no-new-positive',
        'daily_context_window: <2y / unavailable',
        'major_high_low_review',
        'ema20_50_200_review',
        'pattern_like',
        'research_positive_conditional',
        '不修改 Codex Trading',
        '不创建量化扫描器',
        '不连接 Execution Agent'
    )
    'docs/pa_research_daily_selection_rules_v0_1_CN.md' = @(
        'completed_bar_as_of:',
        'avg_20d_dollar_volume_usd:',
        'daily_context_window: >=2y / <2y / unavailable',
        'chart_scope: full / partial / unavailable',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'a_leg_quality: strong / ordinary / unclear / event_driven',
        'b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear',
        'special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none',
        'why_it_meets_or_fails_the_rule:',
        'possible_entry_trigger:',
        'direction: long / short / no_valid_direction',
        '日线候选的 `primary_pattern` 白名单只有 `ABC_CONT` 和 `BOP`',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'range_edge_three_push` 只表示成熟区间边缘的第三推位置，不是 `H3_L3` 主标签',
        'range_edge_side: upper / lower / none / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'event_bucket:',
        'bop_state:',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'gate_result:',
        'contract_scope:'
    )
    'docs/visual_pa_review_card_CN.md' = @(
        'chart_scope:             # full / partial / unavailable',
        'event_context:           # none / earnings / macro / gap / other / unknown',
        'a_leg_quality: strong / ordinary / unclear / event_driven',
        'b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear',
        'special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none',
        'b_leg_location:',
        'structural_stop:',
        'structural_stop_zone:',
        'first_independent_obstacle:',
        'rough_space_to_first_obstacle_R: positive / borderline / blocked / unknown',
        'pre_entry_space_R:',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'rough_R_R:',
        'direction: long / short / no_valid_direction',
        'pattern_family: ABC_CONT | BOP | RFB_SECOND | H3_L3 | MTR | other',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        '`pattern_family` 是本卡的视觉速记/历史显示字段，不是统一合同的额外主标签',
        '当 `contract_scope: daily_candidate` 时，`timeframes_seen` 只能填写 `Daily`',
        '原 pattern/反向 thesis 与旧订单合同失效',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'gate_result:',
        'contract_scope:',
        '硬闸门阻止新交易',
        '本卡的订单字段是事前研究假设，不是 broker/account fill record'
    )
    'docs/daily_candidate_review_card_CN.md' = @(
        'contract_scope: daily_candidate',
        'directional_bias: bull / bear / balanced / changing',
        'direction: long / short / no_valid_direction',
        'chart_scope: full / partial / unavailable',
        'timeframes_seen:',
        'ema20_50_200_review: complete / partial / unavailable',
        'daily_ema20_50_200:',
        'special_subtype: ordinary / deep_late_controlled_B / bull_flag / earnings_driven / event_driven / gap_reprice / none',
        'universe_coverage: complete / partial / discovery_only / unknown',
        'avg_20d_dollar_volume_usd:',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'range_edge_side: upper / lower / none / pending',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'event_bucket:',
        'permission: long_allowed / short_allowed / both_allowed / no_direction / unknown',
        'lineage_id:',
        'market_context_id:',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'bop_state: acceptance_watch / ordinary_pullback / failed_breakout / gap_event / bull_flag_continuation / not_applicable',
        'breakout_boundary:',
        'acceptance_close:',
        'follow_through:',
        'retest_zone:',
        'role_reversal_held: yes / no / unclear / not_occurred',
        'key_breakout_or_structure_location:',
        'daily_context_window: >=2y / <2y / unavailable',
        'major_high_low_review: complete / partial / unavailable',
        'h_l_ema_slope_gate:',
        'new_trigger:',
        'order_price_or_zone:',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'structural_stop:',
        'first_independent_obstacle:',
        'pre_entry_space_R:',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'rough_R_R:',
        'research_state:',
        '本卡逐标的记录的 `contract_scope` 固定为 `daily_candidate`：`timeframes_seen` 只能填写 `Daily`',
        'Execution Agent',
        '关键图表、事件、触发或空间证据尚不完整',
        '本卡只记录入场前候选证据，不填写实际成交、退出、胜负、`realized_R` 或 broker/account transaction log'
    )
    'patterns/08_three_push_h3_l3/README.md' = @(
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'canonical `direction`',
        'lineage_status: same_lineage / reset / unclear / pending',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'timeframes_seen:',
        'event_bucket:',
        'space_status:',
        'trade_state:',
        'gate_result:',
        'handoff_status: research_only / not_ready / ready_for_system'
    )
    'strategy/01_three_push_wedge_candidate.md' = @(
        'no-new-positive',
        'validated win-rate: not-computable',
        'A/B/C 是解释性分流，不是新的状态枚举',
        'lineage_status: same_lineage / reset / unclear / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'direction: long / short / no_valid_direction',
        'first_independent_obstacle:',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending'
    )
    'research/h3_l3_research_gate_CN.md' = @(
        '统一合同映射',
        'lineage_status: same_lineage / reset / unclear / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'direction: long / short / no_valid_direction',
        'first_independent_obstacle:',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        '历史案例中的连字符和自然语言标签只作为说明别名'
    )
    'research/h3_l3_visual_comparison_CN.md' = @(
        'no-new-positive',
        'validated win-rate: not-computable',
        '`lineage_status`',
        '`third_push_state`',
        '`first_reverse`',
        '`second_confirmation`',
        '`first_independent_obstacle`',
        'research_positive_conditional',
        '新记录必须使用 canonical 字段'
    )
    'research/three_push_pressure_state_framework_CN.md' = @(
        'lineage_status: same_lineage / reset / unclear / pending',
        'direction: long / short / no_valid_direction',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'first_independent_obstacle: where and why',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending'
    )
    'research/mtr_visual_framework_CN.md' = @(
        'exhaustion_candidate`、`continuation_or_climax`、`range_repeat_test` 或 `channel_continuation`',
        'research_positive_conditional'
    )
    'research/h3_l3_candidate_screen_2025-08_2025-11_CN.md' = @(
        'visual-screen / boundary-log / no-new-positive / validated win-rate: not-computable / not-quantitative',
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: unavailable_in_original_log',
        'timezone: unavailable_in_original_log',
        'session_state: historical_close_review',
        'chart_scope: partial',
        'timeframes_seen: Daily',
        'lineage_status: same_lineage / reset / unclear / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified',
        'direction: long / short / no_valid_direction',
        'first_independent_obstacle:',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending',
        '本日志不产生胜率分母'
    )
    'research/h3_l3_candidate_screen_futu_targeted_2024_2026_CN.md' = @(
        'historical / no-new-positive / validated win-rate: not-computable / not-quantitative',
        'data_status: historical',
        'contract_scope: historical_context_only',
        'as_of_time: unavailable_in_original_log',
        'timezone: unavailable_in_original_log',
        'session_state: historical_close_review',
        'chart_scope: partial',
        'timeframes_seen: Daily',
        'lineage_status: same_lineage / reset / unclear / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'event_bucket: ordinary_non_event / event_reviewed_non_event / event_driven / earnings_adjacent / event_unverified_or_pending / unknown / other_unclassified',
        'direction: long / short / no_valid_direction',
        'first_independent_obstacle:',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending',
        '不建立统计分母',
        '事件链接只覆盖本日志中明确列出的部分财报核对'
    )
    'patterns/README.md' = @(
        'timeframes_seen / data_status / as_of_time / timezone / session_state / chart_scope',
        'left_structure_and_location / major_highs_lows / support_resistance_and_role_zones',
        'daily_ema20_50_200 / a_leg_quality / b_leg_class / b_leg_location / special_subtype',
        'lineage_status / lineage_id / internal_label / attempt_direction / third_push_state / first_reverse / second_confirmation / range_edge_three_push / range_edge_side',
        'daily_context_window / major_high_low_review / ema20_50_200_review',
        'signal_bar / confirmation_bar / new_trigger / follow_through',
        'structural_stop / structural_invalidation',
        'first_independent_obstacle / rough_space_to_first_obstacle_R / space_status / rough_R_R',
        'event_context / event_bucket / sector_state / market_state / permission / gate_result',
        'Pattern-specific shorthand',
        '日线主标签白名单与状态迁移',
        'contract_scope: daily_candidate',
        'primary_pattern` 只允许 `ABC_CONT` 或 `BOP`',
        'range_edge_three_push` 只是区间边缘位置分支',
        '原 pattern/反向 thesis 与旧订单合同失效',
        '几何顺序固定为：结构失效/止损 → 首障碍 → 入场前空间 → 粗略 R/R → 目标层',
        'observation_only',
        'valid_no_trade'
    )
    'patterns/07_mtr_reversal/README.md' = @(
        'mtr_state: reversal_attempt / mtr_candidate / mtr_confirmed_for_research / failed_mtr_thesis',
        'thesis_state: working / failed / invalidated / replaced / pending'
    )
    'patterns/05_failed_breakout_climax/README.md' = @(
        'breakout_climax_state: continuation / small_reversal / range / mtr_candidate / pending',
        'canonical `research_state`'
    )
    'docs/common_context.md' = @(
        '### Common visual preflight',
        'data_status: historical / delayed / live_confirmed / incomplete',
        'chart_scope: full / partial / unavailable',
        'daily_context_window: >=2y / <2y / unavailable',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'a_leg_quality: strong / ordinary / unclear / event_driven',
        'b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear',
        'first_independent_obstacle:',
        '### Entry geometry and state boundary',
        'structural_invalidation` → `structural_stop` →',
        '`observation_only` 表示关键图表、事件、方向、触发或空间证据还不完整',
        '`valid_no_trade` 表示形态、方向和入场几何已经足够复核',
        'rule specifications that may be validated later; current validation remains not-computable.'
    )
    'research/h_l_lineage_visual_boundary_audit_2026-08-24_CN.md' = @(
        'direction: long / short / no_valid_direction',
        'parent_state: open_trend / trading_range / range_edge / transition / climax / unclear',
        'lineage_status: same_lineage / reset / unclear / pending',
        'lineage_id:',
        'contract_scope: historical_context_only',
        'data_status: historical / delayed / live_confirmed / incomplete',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_three_push: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'first_independent_obstacle:',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending',
        'same-lineage-provisional',
        'lineage_status: pending'
    )
    'research/three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md' = @(
        'validated win-rate: not-computable',
        'contract_scope: historical_context_only',
        'lineage_status: same_lineage / reset / unclear / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'direction: long / short / no_valid_direction',
        'first_independent_obstacle:',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'research_positive_candidate',
        '历史说明别名'
    )
    'research/visual_recognition_round5_two_year_daily_2026-08-24_CN.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: per-case cutoff; query timestamp unavailable in original log',
        'timezone: unavailable_in_original_log',
        'session_state: historical_close',
        'timeframes_seen: Daily / 4H / 15m (case-specific)',
        'chart_scope: partial',
        'daily_context_window: >=2y (8/8 cases)',
        'major_high_low_review: complete (8/8 cases)',
        'ema20_50_200_review: complete (8/8 cases)',
        'lineage_status: same_lineage / reset / unclear / pending',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'first_reverse: none / touch / structural_break',
        'second_confirmation: yes / no / pending',
        'range_edge_three_push: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'first_independent_obstacle: visual candidate only; not a frozen order field',
        'pre_entry_space_R: unknown unless trigger and structural stop are independently frozen',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending',
        'historical_count_label',
        'same-lineage-provisional',
        'same-pressure-zone-provisional',
        'unclear-to-range',
        'first-obstacle-boundary',
        'space_status: unknown',
        'order_branch: observation_only',
        'no-new-positive: maintained'
    )
    'research/visual_recognition_round4_historical_practice_2026-08-24_CN.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: per-case cutoff; dataset end 2026-08-10',
        'timezone: unavailable_in_original_snapshot',
        'session_state: historical_close',
        'timeframes_seen: Daily / 4H / 15m (case-specific)',
        'chart_scope: partial',
        'daily_context_window: <2y',
        'major_high_low_review: partial',
        'ema20_50_200_review: partial',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'parent_state: open_trend / trading_range / range_edge / transition / climax / unclear',
        'direction: long / short / no_valid_direction',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'lineage_status: same_lineage / reset / unclear / pending',
        'attempt_direction: bullish_attempts / bearish_attempts / unknown',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'range_edge_three_push: yes / no / pending',
        'range_edge_side: upper / lower / none / pending',
        'first_independent_obstacle: visual candidate only; not a frozen order field',
        'pre_entry_space_R: unknown unless trigger and structural stop are independently frozen',
        'space_status: strict_ge_1R / borderline_ge_1R / clearly_positive / borderline / blocked / unknown',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending',
        'handoff_status: not_ready',
        'no-new-positive: maintained',
        'validated win-rate: not-computable'
    )
    'research/backtesting/visual_evidence_canonical_boundary_audit_2026-08-29_CN.md' = @(
        'three_push_h3_l3_visual_evidence_gap_audit_2026-08-24_CN.md',
        'h_l_lineage_visual_boundary_audit_2026-08-24_CN.md',
        'visual_recognition_round5_two_year_daily_2026-08-24_CN.md',
        'lineage_status: pending',
        'third_push_state: range_repeat_test',
        'space_status: unknown',
        '7 份 CSV、60 行',
        'H3/L3 冻结合同仍为 0',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )
    'research/visual_pattern_triage_protocol_CN.md' = @(
        'contract_scope: stage_1_fast_screen',
        'timeframes_seen:',
        'data_status: historical / delayed / live_confirmed / incomplete',
        'chart_scope: full / partial / unavailable',
        'daily_context_window: >=2y / <2y / unavailable',
        '不把 4H/1H/15m 倒灌成日线选股证据',
        'contract_scope: stage_1_fast_screen / historical_context_only',
        'session_state: premarket / RTH / after_hours / historical_close / unknown',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'parent_state: open_trend / trading_range / range_edge / transition / climax / unclear',
        'primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'lineage_status: same_lineage / reset / unclear / pending',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'range_edge_side: upper / lower / none / pending',
        'research_state: pattern_like / research_candidate / research_positive_conditional / observation_only / valid_no_trade / failed_thesis / pending',
        'trade_state: not_authorized / conditional / valid_no_trade / observation_only / pending',
        'gap_policy: accept_open / skip / flag_only / not_applicable',
        'rough_space` 和',
        'stage_2_status` 是历史工作别名',
        'strong-looking-A'
    )
    'research/visual_recognition_smoke_test_2026-08-24_CN.md' = @(
        'contract_scope: stage_1_fast_screen',
        'contract_scope: historical_context_only',
        'visual_pattern_label',
        'lineage_status: same_lineage / reset / unclear / pending',
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'as_of_time: unavailable_in_original_images',
        'major_high_low_review: unavailable',
        'ema20_50_200_review: unavailable',
        'daily_context_window_review: saved assets >=2y; public five unavailable',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'no-new-positive-for-clean-multiday-BOP'
    )
    'research/assets/visual_recognition/2026-08-24/round2_multisymbol/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: 2026-08-21 16:00 America/New_York',
        'timezone: America/New_York',
        'session_state: historical_close',
        'timeframes_seen: Daily / 4H-like / 1H / 15m',
        'chart_scope: full',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired smoke review',
        'ema20_50_200_review: complete in paired smoke review',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'handoff_status: not_ready',
        'primary_pattern',
        'secondary_context'
    )
    'research/assets/visual_recognition/2026-08-24/round3_hl_drills/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'session_state: historical_close',
        'timeframes_seen: 1H / 15m plus paired Daily from round2_multisymbol',
        'chart_scope: partial',
        'daily_context_window: >=2y via paired Daily asset',
        'major_high_low_review: complete in paired smoke review',
        'ema20_50_200_review: complete in paired smoke review',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'handoff_status: not_ready',
        'primary_pattern',
        'secondary_context'
    )
    'research/assets/visual_recognition/2026-08-24/round3_l1_l2_mar/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: 2026-06-26; latest complete Daily bar in asset request',
        'session_state: historical_close',
        'timeframes_seen: Daily (~2Y left context) / 4H-like / 60m proxy',
        'chart_scope: partial',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired smoke review',
        'ema20_50_200_review: complete in paired smoke review',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'handoff_status: not_ready',
        'primary_pattern',
        'secondary_context'
    )
    'research/assets/visual_recognition/2026-08-24/round4_historical_practice/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: 2026-08-10 dataset end; 2026-07-29 targeted cutoff case-specific',
        'timezone: unavailable_in_original_snapshot',
        'session_state: historical_close',
        'timeframes_seen: Daily / 4H / 15m (case-specific)',
        'chart_scope: partial',
        'daily_context_window: <2y',
        'major_high_low_review: partial',
        'ema20_50_200_review: partial',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'range_edge_three_push: pending',
        'range_edge_side: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'handoff_status: not_ready'
    )
    'research/assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: per-case cutoff; query timestamp unavailable in original log',
        'timezone: unavailable_in_original_log',
        'session_state: historical_close',
        'timeframes_seen: Daily / 4H / 15m (case-specific)',
        'chart_scope: partial',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired historical review; per-case text below',
        'ema20_50_200_review: complete in paired historical review; Daily EMA only',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'range_edge_three_push: pending',
        'range_edge_side: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'handoff_status: not_ready'
    )
    'research/assets/visual_recognition/2026-08-24/tsla_public_mtf/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: 2026-08-21 16:00 America/New_York',
        'timezone: America/New_York',
        'session_state: historical_close',
        'timeframes_seen: Daily / 4H-like / 1H / 15m',
        'chart_scope: full',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired smoke review; not drawn on the asset',
        'ema20_50_200_review: complete in paired smoke review; Daily EMA only',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'handoff_status: not_ready'
    )
    'research/assets/visual_recognition/2026-08-26/hl_contract_batch/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: per-case decision cutoff',
        'review_time: 2026-08-26',
        'timezone: America/New_York',
        'session_state: historical_close',
        'timeframes_seen: Daily',
        'chart_scope: full',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired contract review',
        'ema20_50_200_review: complete in paired contract review',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'range_edge_three_push: pending',
        'range_edge_side: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'first_independent_obstacle: paired contract only; not frozen in this asset',
        'pre_entry_space_R: unknown unless trigger and structural stop are independently frozen',
        'space_status: unknown',
        'order_branch: observation_only',
        'label_source: human_chart_review',
        'handoff_status: not_ready'
    )
    'research/assets/visual_recognition/2026-08-26/hl_contract_batch2/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: per-case decision cutoff',
        'review_time: 2026-08-26',
        'timezone: America/New_York',
        'session_state: historical_close',
        'timeframes_seen: Daily',
        'chart_scope: full',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired contract review',
        'ema20_50_200_review: complete in paired contract review',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'range_edge_three_push: pending',
        'range_edge_side: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'first_independent_obstacle: paired contract only; not frozen in this asset',
        'pre_entry_space_R: unknown unless trigger and structural stop are independently frozen',
        'space_status: unknown',
        'order_branch: observation_only',
        'label_source: human_chart_review',
        'handoff_status: not_ready'
    )
    'research/assets/visual_recognition/2026-08-27/hl_large_backtest/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: 2026-08-26 latest complete RTH bar',
        'review_time: 2026-08-27 Asia/Shanghai',
        'timezone: America/New_York',
        'session_state: historical_close',
        'timeframes_seen: Daily',
        'chart_scope: full',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired frozen-contract review',
        'ema20_50_200_review: complete in paired frozen-contract review',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'range_edge_three_push: pending',
        'range_edge_side: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'first_independent_obstacle: paired contract only; not frozen in this asset',
        'pre_entry_space_R: unknown unless trigger and structural stop are independently frozen',
        'space_status: unknown',
        'order_branch: observation_only',
        'label_source: human_chart_review',
        'handoff_status: not_ready'
    )
    'research/assets/visual_recognition/2026-08-27/hl_next_backtest/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: 2026-08-26 latest complete RTH bar',
        'review_time: 2026-08-27 Asia/Shanghai',
        'timezone: America/New_York',
        'session_state: historical_close',
        'timeframes_seen: Daily',
        'chart_scope: full',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired frozen-contract review',
        'ema20_50_200_review: complete in paired frozen-contract review',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'range_edge_three_push: pending',
        'range_edge_side: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'first_independent_obstacle: paired contract only; not frozen in this asset',
        'pre_entry_space_R: unknown unless trigger and structural stop are independently frozen',
        'space_status: unknown',
        'order_branch: observation_only',
        'label_source: human_chart_review',
        'handoff_status: not_ready'
    )
    'research/assets/visual_recognition/2026-08-27/hl_next2_backtest/README.md' = @(
        'contract_scope: historical_context_only',
        'data_status: historical',
        'as_of_time: 2026-08-26 latest complete RTH bar',
        'review_time: 2026-08-27 Asia/Shanghai',
        'timezone: America/New_York',
        'session_state: historical_close',
        'timeframes_seen: Daily',
        'chart_scope: full',
        'daily_context_window: >=2y',
        'major_high_low_review: complete in paired frozen-contract review',
        'ema20_50_200_review: complete in paired frozen-contract review',
        'daily_ema20_slope: unknown',
        'daily_ema50_slope: unknown',
        'h_l_ema_slope_gate: pending',
        'direction: no_valid_direction',
        'lineage_status: pending',
        'internal_label: pending',
        'third_push_state: unclear',
        'range_edge_three_push: pending',
        'range_edge_side: pending',
        'research_state: observation_only',
        'trade_state: observation_only',
        'gate_result: observation_only',
        'first_independent_obstacle: paired contract or boundary review only; not frozen in this asset',
        'pre_entry_space_R: unknown unless trigger and structural stop are independently frozen',
        'space_status: unknown',
        'order_branch: observation_only',
        'label_source: human_chart_review',
        'handoff_status: not_ready'
    )
    'research/backtesting/visual_recognition_canonical_boundary_audit_2026-08-29_CN.md' = @(
        'visual_recognition_smoke_test_2026-08-24_CN.md',
        'visual_pattern_triage_protocol_CN.md',
        'round2_multisymbol/README.md',
        'round3_hl_drills/README.md',
        'round3_l1_l2_mar/README.md',
        'major_high_low_review',
        'ema20_50_200_review',
        'primary_pattern',
        'internal_label',
        'third_push_state',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )
    'research/backtesting/visual_asset_canonical_boundary_audit_2026-08-29_CN.md' = @(
        'Round4、Round5 与 TSLA',
        'round4_historical_practice/README.md',
        'round5_two_year_daily/README.md',
        'tsla_public_mtf/README.md',
        'daily_context_window: <2y',
        'daily_context_window: >=2y',
        'major_high_low_review',
        'ema20_50_200_review',
        'timeframes_seen',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )
    'research/backtesting/visual_asset_provenance_coverage_audit_2026-08-29_CN.md' = @(
        '11 个视觉资产目录',
        '105 张 PNG',
        'contract_scope: historical_context_only',
        'daily_context_window: <2y',
        'daily_context_window: >=2y',
        'major_high_low_review',
        'ema20_50_200_review',
        'two_year_daily: pending',
        'two_year_daily_context: pass',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )
    'research/backtesting/visual_asset_pre_entry_evidence_audit_2026-08-29_CN.md' = @(
        'Round4 的 canonical `daily_context_window: <2y`',
        '`two_year_daily: pending`',
        '11 个视觉资产 README',
        '105 张 PNG',
        'no-new-positive',
        'validated win-rate: not-computable'
    )
    'docs/research_to_system_handoff_CN.md' = @(
        'no-new-positive'
    )
    'research/backtesting/README.md' = @(
        'contract_scope`、`data_status`、`chart_scope` 和 `timeframes_seen` 属于上游视觉/研究记录的证据 provenance',
        'daily_context_window` 不是“CSV 有两年价格”这一事实的别名',
        '`*_selection_*.md`、候选卡和视觉资产 README 属于入场前记录',
        '结果不得反向改写入场前字段',
        '`eligible`/EMA gate',
        '`filled` 只表示历史订单路径有成交',
        '当前 PA Research checkout 不包含券商或账户的真实交易日志；研究合同、历史回放结果和运行 metadata 都不能代替真实交易日志。',
        '记录回放器的模拟成交状态、模拟退出状态'
    )
    'strategy/pattern_inventory_candidates.md' = @(
        '如果目标是 `daily_candidate`，第一步只能看完成的 Daily',
        '只要“看起来像”只能先进入研究 inventory 的 `stage_1_fast_screen`/观察行',
        'contract_scope: stage_1_fast_screen / deep_review / daily_candidate / historical_context_only',
        'outcome                     # 仅独立 replay/result 的事后字段；候选记录保持 pending，不用于授权',
        '`research_state`、`trade_state`、`gate_result` 和 `outcome` 分别属于研究状态、交易状态、闸门状态和事后结果',
        '入场前可复核的结构和粗略 R/R',
        'actual_fill_or_open_skip       # 研究/回放订单路径；不是券商/账户交易日志；候选阶段不写 filled',
        'timeframes_seen',
        'data_status: historical / delayed / live_confirmed / incomplete',
        'chart_scope: full / partial / unavailable',
        'daily_context_window: >=2y / <2y / unavailable',
        '| 视觉候选 ID | direction | 先看什么 | 代表性入口 | 当前状态 |',
        '完整候选卡和冻结合同仍必须逐行写 canonical `direction`',
        'validated evidence（若形成）',
        'validated win-rate: not-computable'
    )
    'research/crm_bearish_abc_l1_l2_visual_candidate_2025-03-10_2025-03-28.md' = @(
        'contract_scope: historical_context_only',
        'directional_bias: bear',
        'direction: short',
        'data_status: historical',
        'timeframes_seen: Daily / 60m / 15m',
        'chart_scope: partial',
        'daily_context_window: <2y',
        'major_high_low_review: partial',
        'ema20_50_200_review: unavailable',
        'a_leg_quality: unclear',
        'b_leg_class: unclear',
        'event_context: unknown',
        'event_bucket: event_unverified_or_pending',
        'sector_state: aligned',
        'market_state: aligned',
        'permission: short_allowed',
        'first_independent_obstacle: pending',
        'pre_entry_space_R: unknown',
        'space_status: unknown',
        'research_state: pattern_like',
        'trade_state: not_authorized',
        'gate_result: pending'
    )
    'research/meta_bullish_h1_h2_visual_candidate_2024-09-11_2024-10-11.md' = @(
        'contract_scope: stage_1_fast_screen',
        'directional_bias: bull',
        'direction: long',
        'data_status: historical',
        'timeframes_seen: Daily',
        'chart_scope: partial',
        'daily_context_window: unavailable',
        'major_high_low_review: partial',
        'ema20_50_200_review: partial',
        'a_leg_quality: unclear',
        'b_leg_class: unclear',
        'event_context: unknown',
        'event_bucket: event_unverified_or_pending',
        'sector_state: unknown',
        'market_state: unknown',
        'permission: unknown',
        'first_independent_obstacle: pending',
        'pre_entry_space_R: unknown',
        'space_status: unknown',
        'research_state: pattern_like',
        'trade_state: not_authorized',
        'gate_result: pending'
    )
    'research/msft_bearish_abc_l1_l2_visual_candidate_2025-10-28_2025-11-20.md' = @(
        'contract_scope: stage_1_fast_screen',
        'directional_bias: bear',
        'direction: short',
        'data_status: historical',
        'timeframes_seen: Daily',
        'chart_scope: partial',
        'daily_context_window: <2y',
        'major_high_low_review: partial',
        'ema20_50_200_review: unavailable',
        'a_leg_quality: unclear',
        'b_leg_class: unclear',
        'event_context: unknown',
        'event_bucket: event_unverified_or_pending',
        'sector_state: unknown',
        'market_state: unknown',
        'permission: unknown',
        'first_independent_obstacle: pending',
        'pre_entry_space_R: unknown',
        'space_status: unknown',
        'research_state: pattern_like',
        'trade_state: not_authorized',
        'gate_result: pending'
    )
    'research/nvda_bullish_abc_h1_visual_candidate_2025-06-23_2025-07-03.md' = @(
        'contract_scope: stage_1_fast_screen',
        'directional_bias: bull',
        'direction: long',
        'data_status: historical',
        'timeframes_seen: Daily',
        'chart_scope: partial',
        'daily_context_window: <2y',
        'major_high_low_review: partial',
        'ema20_50_200_review: partial',
        'a_leg_quality: unclear',
        'b_leg_class: unclear',
        'event_context: unknown',
        'event_bucket: event_unverified_or_pending',
        'sector_state: unknown',
        'market_state: unknown',
        'permission: unknown',
        'first_independent_obstacle: pending',
        'pre_entry_space_R: unknown',
        'space_status: unknown',
        'research_state: pattern_like',
        'trade_state: not_authorized',
        'gate_result: pending'
    )
    'research/visual_screen_candidate_grid_2024_2025_CN.md' = @(
        'contract_scope: stage_1_fast_screen',
        'directional_bias: changing',
        'direction: no_valid_direction',
        'data_status: historical',
        'timeframes_seen: Daily',
        'chart_scope: full',
        'daily_context_window: unavailable',
        'major_high_low_review: partial',
        'ema20_50_200_review: unavailable',
        'a_leg_quality: unclear',
        'b_leg_class: unclear',
        'event_context: unknown',
        'event_bucket: event_unverified_or_pending',
        'sector_state: unknown',
        'market_state: unknown',
        'permission: unknown',
        'first_independent_obstacle: pending',
        'pre_entry_space_R: unknown',
        'space_status: unknown',
        'research_state: pattern_like',
        'trade_state: not_authorized',
        'gate_result: pending'
    )
}
foreach ($entry in $canonicalChecks.GetEnumerator()) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($entry.Key -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in $entry.Value) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "missing canonical token '$token': $($entry.Key)"
        }
    }
}

$legacyConclusionStatusPatterns = @(
    '(?m)^\s*validated_win_rate\s*:',
    '(?m)^\s*win_rate\s*:\s*not-computable\s*$'
)
$legacyConclusionMarkdownPaths = @(
    Get-ChildItem -LiteralPath $repoRoot -File -Filter '*.md' -ErrorAction SilentlyContinue
    Get-ChildItem -LiteralPath (Join-Path $repoRoot 'docs') -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue
    Get-ChildItem -LiteralPath (Join-Path $repoRoot 'research') -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue
    Get-ChildItem -LiteralPath (Join-Path $repoRoot 'strategy') -Recurse -File -Filter '*.md' -ErrorAction SilentlyContinue
)
foreach ($markdownPath in @($legacyConclusionMarkdownPaths | Sort-Object FullName -Unique)) {
    $content = Get-Utf8Text -Path $markdownPath.FullName
    foreach ($pattern in $legacyConclusionStatusPatterns) {
        if ($content -match $pattern) {
            $relativePath = $markdownPath.FullName.Substring($repoRoot.Length + 1).Replace('\', '/')
            Add-ValidationError "legacy non-canonical conclusion status: $relativePath"
            break
        }
    }
}

$patternCaseEntryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_case_entry_status_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternCaseEntryAuditPath -PathType Leaf) {
    $patternCaseEntryAuditContent = Get-Utf8Text -Path $patternCaseEntryAuditPath
    foreach ($token in @(
        'valid_no_trade',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $patternCaseEntryAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern case-entry audit token '$token'"
        }
    }
}

$patternCaseReadmeRelativePaths = @(
    'patterns/01_h1_l1_first_entry/README.md',
    'patterns/02_h2_l2_second_entry/README.md',
    'patterns/03_abc_continuation/README.md',
    'patterns/04_range_edge_second_entry/README.md',
    'patterns/05_failed_breakout_climax/README.md',
    'patterns/06_breakout_pullback_bop/README.md',
    'patterns/07_mtr_reversal/README.md',
    'patterns/08_three_push_h3_l3/README.md',
    'patterns/09_vcp_minervini/README.md',
    'patterns/10_final_flag/README.md',
    'patterns/11_opening_reversal/README.md',
    'patterns/12_channel/README.md',
    'patterns/13_inside_bar_two_bar_reversal/README.md',
    'patterns/14_triangle_expanding_range/README.md',
    'patterns/15_double_top_bottom/README.md',
    'patterns/16_head_shoulders_rounded/README.md'
)
$patternStateAxisAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_state_axis_field_enum_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternStateAxisAuditPath -PathType Leaf) {
    $patternStateAxisAuditContent = Get-Utf8Text -Path $patternStateAxisAuditPath
    foreach ($token in @(
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $patternStateAxisAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern state-axis audit token '$token'"
        }
    }
}
foreach ($relativePath in $patternCaseReadmeRelativePaths) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in @(
        'data_status: historical / delayed / live_confirmed / incomplete',
        'as_of_time',
        'chart_scope',
        'daily_context_window',
        'timeframes_seen',
        '至少两年的 Daily 左侧背景',
        'EMA20/50/200',
        'direction: long / short / no_valid_direction',
        'pending',
        '状态边界：关键图表、事件、触发或空间证据尚不完整时使用',
        '形态、方向和入场几何已可复核但已知硬闸门否决交易时使用',
        '两者都不建立订单，不能互换'
    )) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "pattern README missing common visual preflight token '$token': $relativePath"
        }
    }
    if ($content -notmatch '重要高点|主要高点' -or $content -notmatch '重要低点|主要低点') {
        Add-ValidationError "pattern README missing major high/low preflight wording: $relativePath"
    }
    if ($content -notmatch '第一独立障碍|first_independent_obstacle|首障碍') {
        Add-ValidationError "pattern README missing first-obstacle preflight wording: $relativePath"
    }
    if ($content -notmatch '统一合同映射：') {
        Add-ValidationError "pattern README missing canonical label mapping: $relativePath"
    }
    if ($content -notmatch 'BOP 状态迁移：若事前可见边界被日线强收盘越过') {
        Add-ValidationError "pattern README missing BOP old-contract invalidation boundary: $relativePath"
    }
    if ($content -match '(?<![\w-])valid(?:-| )no-trade(?![\w-])') {
        Add-ValidationError "legacy valid-no-trade status alias in active pattern README: $relativePath"
    }
    if ($content -match '(?i)(?<![\w-])observation-only(?![\w-])') {
        Add-ValidationError "legacy observation-only status alias in active pattern README: $relativePath"
    }
    if ($content -match '(?<![A-Za-z_])no_trade(?![A-Za-z_])') {
        Add-ValidationError "legacy no_trade status alias in active pattern README: $relativePath"
    }
    if ($relativePath -eq 'patterns/05_failed_breakout_climax/README.md' -and
        $content -match '(?m)^final_state:') {
        Add-ValidationError 'pattern 05 retains ambiguous final_state field; use breakout_climax_state plus canonical state axes'
    }
}

$currentPatternStatusCanonicalPaths = @(
    'research/abc_decision_matrix_CN.md',
    'research/priority_pattern_visual_candidate_matrix_2026-08-24_CN.md',
    'research/order_branch_visual_protocol_CN.md',
    'research/largecap_visual_screen_2024_CN.md'
)
foreach ($relativePath in $currentPatternStatusCanonicalPaths) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($legacyStatusPattern in @(
        '(?<![\w-])research_positive_candidate(?![\w-])',
        'research_positive conditional',
        '(?<![\w-])valid(?:-| )no-trade(?![\w-])'
    )) {
        if ($content -match $legacyStatusPattern) {
            Add-ValidationError "legacy status alias in current pattern entry: $relativePath"
            break
        }
    }
}

$dailyCandidateReviewCardPath = Join-Path -Path $repoRoot -ChildPath 'docs/daily_candidate_review_card_CN.md'
if (Test-Path -LiteralPath $dailyCandidateReviewCardPath -PathType Leaf) {
    $dailyCandidateReviewCardContent = Get-Utf8Text -Path $dailyCandidateReviewCardPath
    foreach ($legacyToken in @('(?m)^\s*trigger_price_or_zone:', '(?m)^\s*structural_stop_or_zone:')) {
        if ($dailyCandidateReviewCardContent -match $legacyToken) {
            Add-ValidationError "daily candidate review card retains non-canonical geometry alias: $legacyToken"
        }
    }
}

$visualPaReviewCardPath = Join-Path -Path $repoRoot -ChildPath 'docs/visual_pa_review_card_CN.md'
if (Test-Path -LiteralPath $visualPaReviewCardPath -PathType Leaf) {
    $visualPaReviewCardContent = Get-Utf8Text -Path $visualPaReviewCardPath
    foreach ($legacyToken in @('(?m)^\s*stop_zone:', '(?m)^\s*stop_price_or_area:', '(?m)^\s*space_to_first_obstacle:')) {
        if ($visualPaReviewCardContent -match $legacyToken) {
            Add-ValidationError "visual PA review card retains ambiguous geometry alias: $legacyToken"
        }
    }
}

$corePatternOrderBranchRelativePaths = @(
    'patterns/04_range_edge_second_entry/README.md',
    'patterns/05_failed_breakout_climax/README.md',
    'patterns/06_breakout_pullback_bop/README.md',
    'patterns/07_mtr_reversal/README.md',
    'patterns/08_three_push_h3_l3/README.md'
)
foreach ($relativePath in $corePatternOrderBranchRelativePaths) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    if ($content -notmatch '(?m)^order_branch:.*\bstop_limit\b') {
        Add-ValidationError "core pattern order_branch omits research stop_limit: $relativePath"
    }
}

$rangeEdgeReadmePath = Join-Path -Path $repoRoot -ChildPath 'patterns/04_range_edge_second_entry/README.md'
if (Test-Path -LiteralPath $rangeEdgeReadmePath -PathType Leaf) {
    $rangeEdgeReadmeContent = Get-Utf8Text -Path $rangeEdgeReadmePath
    if ($rangeEdgeReadmeContent -notmatch 'IWM 2024-04-17' -or
        $rangeEdgeReadmeContent -notmatch 'range_edge_second_entry_framework_CN\.md') {
        Add-ValidationError 'IWM range-edge case is missing its framework entry link'
    }
}

$researchReadmePath = Join-Path -Path $repoRoot -ChildPath 'research/README.md'
if (Test-Path -LiteralPath $researchReadmePath -PathType Leaf) {
    $researchReadmeContent = Get-Utf8Text -Path $researchReadmePath
    if ($researchReadmeContent -match 'no_new_positive') {
        Add-ValidationError 'research README contains non-canonical no_new_positive alias'
    }
    if ($researchReadmeContent -notmatch 'no-new-positive') {
        Add-ValidationError 'research README is missing canonical no-new-positive status'
    }
}

$intakeRows = @()
$bopRows = @()
$intakeIdRecords = [System.Collections.Generic.List[object]]::new()
$intakePath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/abc_bop_contract_intake_2026-08-28.csv'
if (Test-Path -LiteralPath $intakePath -PathType Leaf) {
    $intakeRows = @(Import-Csv -LiteralPath $intakePath)
    $requiredIntakeColumns = @(
        'intake_id', 'symbol', 'source_case', 'decision_date', 'direction',
        'primary_pattern', 'internal_label', 'contract_branch', 'intake_state',
        'contract_frozen', 'event_state', 'trigger_evidence',
        'structural_stop_evidence', 'first_obstacle_evidence', 'space_evidence',
        'lineage_evidence', 'missing_fields', 'freeze_recommendation'
    )
    if ($intakeRows.Count -eq 0) {
        Add-ValidationError 'ABC/BOP intake CSV has no rows'
    } else {
        $intakePropertyNames = @($intakeRows[0].PSObject.Properties.Name)
        if ($intakePropertyNames.Count -ne $requiredIntakeColumns.Count) {
            Add-ValidationError 'ABC/BOP intake CSV schema column count mismatch'
        }
        foreach ($column in $requiredIntakeColumns) {
            if ($column -notin $intakePropertyNames) {
                Add-ValidationError "missing ABC/BOP intake column '$column'"
            }
        }
        if ('sample_id' -in $intakePropertyNames) {
            Add-ValidationError 'ABC/BOP intake CSV must use intake_id, not sample_id'
        }
        foreach ($row in $intakeRows) {
            $intakeId = Get-TrimmedText $row.intake_id
            foreach ($column in $requiredIntakeColumns) {
                $value = Get-TrimmedText $row.PSObject.Properties[$column].Value
                if ([string]::IsNullOrWhiteSpace($value)) {
                    Add-ValidationError "ABC/BOP intake row missing required value '$column': $intakeId"
                }
            }
            [void]$intakeIdRecords.Add([pscustomobject]@{
                intake_id = $intakeId
                file = 'abc_bop_contract_intake_2026-08-28.csv'
            })
            $sourceCase = Get-TrimmedText $row.source_case
            $sourceCaseRelative = $sourceCase -replace '/', [IO.Path]::DirectorySeparatorChar
            if ([IO.Path]::IsPathRooted($sourceCaseRelative) -or $sourceCaseRelative -match '(^|\\)\.\.(\\|$)') {
                Add-ValidationError "ABC/BOP intake row source_case escapes repository: $intakeId"
            } elseif (-not (Test-Path -LiteralPath (Join-Path -Path $repoRoot -ChildPath $sourceCaseRelative) -PathType Leaf)) {
                Add-ValidationError "ABC/BOP intake row source_case does not exist: $intakeId"
            }
            $direction = (Get-TrimmedText $row.direction).ToLowerInvariant()
            if ($direction -notin @('long', 'short')) {
                Add-ValidationError "ABC/BOP intake row has invalid direction: $intakeId"
            }
            if (-not (Test-ValidDate $row.decision_date)) {
                Add-ValidationError "ABC/BOP intake row has invalid decision_date: $intakeId"
            }
            $primaryPattern = (Get-TrimmedText $row.primary_pattern).ToUpperInvariant()
            if ($primaryPattern -notin @('ABC_CONT', 'BOP')) {
                Add-ValidationError "ABC/BOP intake row has invalid primary_pattern: $intakeId"
            }
            $internalLabel = (Get-TrimmedText $row.internal_label).ToLowerInvariant()
            if ($primaryPattern -eq 'BOP' -and $internalLabel -ne 'none') {
                Add-ValidationError "ABC/BOP intake BOP row must use internal_label=none: $intakeId"
            }
            if ($row.contract_frozen -ne 'no') {
                Add-ValidationError "ABC/BOP intake row is not marked contract_frozen=no: $intakeId"
            }
        }
    }
}

$bopIntakePath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/bop_contract_intake_2026-08-28.csv'
if (Test-Path -LiteralPath $bopIntakePath -PathType Leaf) {
    $bopRows = @(Import-Csv -LiteralPath $bopIntakePath)
    $requiredBopColumns = @(
        'intake_id', 'symbol', 'source_case', 'decision_date', 'direction',
        'classification', 'bop_state', 'old_boundary_evidence',
        'breakout_acceptance_evidence', 'retest_class', 'role_reversal_evidence',
        'order_branch', 'intake_state', 'contract_frozen', 'event_state',
        'first_obstacle_evidence', 'space_evidence', 'lineage_evidence',
        'missing_fields', 'freeze_recommendation'
    )
    if ($bopRows.Count -eq 0) {
        Add-ValidationError 'BOP intake CSV has no rows'
    } else {
        $bopPropertyNames = @($bopRows[0].PSObject.Properties.Name)
        if ($bopPropertyNames.Count -ne $requiredBopColumns.Count) {
            Add-ValidationError 'BOP intake CSV schema column count mismatch'
        }
        foreach ($column in $requiredBopColumns) {
            if ($column -notin $bopPropertyNames) {
                Add-ValidationError "missing BOP intake column '$column'"
            }
        }
        if ('sample_id' -in $bopPropertyNames) {
            Add-ValidationError 'BOP intake CSV must use intake_id, not sample_id'
        }
        foreach ($row in $bopRows) {
            $intakeId = Get-TrimmedText $row.intake_id
            foreach ($column in $requiredBopColumns) {
                $value = Get-TrimmedText $row.PSObject.Properties[$column].Value
                if ([string]::IsNullOrWhiteSpace($value)) {
                    Add-ValidationError "BOP intake row missing required value '$column': $intakeId"
                }
            }
            [void]$intakeIdRecords.Add([pscustomobject]@{
                intake_id = $intakeId
                file = 'bop_contract_intake_2026-08-28.csv'
            })
            $sourceCase = Get-TrimmedText $row.source_case
            $sourceCaseRelative = $sourceCase -replace '/', [IO.Path]::DirectorySeparatorChar
            if ([IO.Path]::IsPathRooted($sourceCaseRelative) -or $sourceCaseRelative -match '(^|\\)\.\.(\\|$)') {
                Add-ValidationError "BOP intake row source_case escapes repository: $intakeId"
            } elseif (-not (Test-Path -LiteralPath (Join-Path -Path $repoRoot -ChildPath $sourceCaseRelative) -PathType Leaf)) {
                Add-ValidationError "BOP intake row source_case does not exist: $intakeId"
            }
            $direction = (Get-TrimmedText $row.direction).ToLowerInvariant()
            if ($direction -notin @('long', 'short')) {
                Add-ValidationError "BOP intake row has invalid direction: $intakeId"
            }
            if (-not (Test-ValidDate $row.decision_date)) {
                Add-ValidationError "BOP intake row has invalid decision_date: $intakeId"
            }
            if ($row.retest_class -eq 'multi-day' -or $row.classification -eq 'multi_day_bop_positive') {
                Add-ValidationError "BOP intake row claims a multi-day positive without a frozen contract: $intakeId"
            }
            if ($row.contract_frozen -ne 'no') {
                Add-ValidationError "BOP intake row is not marked contract_frozen=no: $intakeId"
            }
        }
    }
}

foreach ($duplicate in @($intakeIdRecords | Group-Object intake_id | Where-Object { $_.Name -and $_.Count -gt 1 })) {
    $files = ($duplicate.Group | ForEach-Object { $_.file } | Sort-Object -Unique) -join ', '
    Add-ValidationError "duplicate intake_id across intake CSVs: $($duplicate.Name) [$files]"
}

$freezeReviewPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/abc_bop_candidate_freeze_review_2026-08-28_CN.md'
if (Test-Path -LiteralPath $freezeReviewPath -PathType Leaf) {
    $freezeReviewContent = Get-Utf8Text -Path $freezeReviewPath
    foreach ($token in @('NFLX', 'TSM', 'contract_frozen=no', 'no-new-positive', 'max_hold_bars', 'do_not_replay')) {
        if (-not $freezeReviewContent.Contains($token)) {
            Add-ValidationError "missing ABC/BOP freeze-review token '$token'"
        }
    }
}

$bullishCandidateAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/abc_bullish_candidate_contract_audit_2026-08-28_CN.md'
if (Test-Path -LiteralPath $bullishCandidateAuditPath -PathType Leaf) {
    $bullishCandidateAuditContent = Get-Utf8Text -Path $bullishCandidateAuditPath
    foreach ($token in @('V', 'NVDA', 'KLAC', 'CRWD', 'contract_frozen=no', 'no-new-positive', 'max_hold_bars', 'ABC_CONT')) {
        if (-not $bullishCandidateAuditContent.Contains($token)) {
            Add-ValidationError "missing bullish ABC candidate-audit token '$token'"
        }
    }
}

$crossPatternAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/cross_pattern_statistics_isolation_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $crossPatternAuditPath -PathType Leaf) {
    $crossPatternAuditContent = Get-Utf8Text -Path $crossPatternAuditPath
    foreach ($token in @('ABC_CONT', 'BOP', 'H1', 'H2', 'L1', 'L2', 'H3', 'L3', 'lineage_id', 'no-new-positive')) {
        if (-not $crossPatternAuditContent.Contains($token)) {
            Add-ValidationError "missing cross-pattern isolation-audit token '$token'"
        }
    }
}

$eventSpaceAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/event_space_eligibility_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $eventSpaceAuditPath -PathType Leaf) {
    $eventSpaceAuditContent = Get-Utf8Text -Path $eventSpaceAuditPath
    foreach ($token in @('event_bucket', 'ordinary_non_event', 'event_unverified_or_pending', 'space_status', 'unknown_contract_space', 'strict_ge_1R', 'no-new-positive')) {
        if (-not $eventSpaceAuditContent.Contains($token)) {
            Add-ValidationError "missing event/space eligibility-audit token '$token'"
        }
    }
}

$eventSpaceLineageAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/event_space_lineage_consistency_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $eventSpaceLineageAuditPath -PathType Leaf) {
    $eventSpaceLineageAuditContent = Get-Utf8Text -Path $eventSpaceLineageAuditPath
    foreach ($token in @(
        'event_context', 'event_bucket', 'ordinary_non_event', 'event_unverified_or_pending',
        'space_status', 'pre_entry_space_R', 'unknown_contract_space', 'strict_ge_1R',
        'lineage_id', 'market_context_id', 'no-new-positive', 'validated win-rate: not-computable',
        'PA Research only', 'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $eventSpaceLineageAuditContent.Contains($token)) {
            Add-ValidationError "missing event/space/lineage-consistency-audit token '$token'"
        }
    }
}

$eventBucketLabelAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/event_bucket_label_consistency_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $eventBucketLabelAuditPath -PathType Leaf) {
    $eventBucketLabelAuditContent = Get-Utf8Text -Path $eventBucketLabelAuditPath
    foreach ($token in @(
        'event_context', 'event_bucket', 'earnings-driven', 'earnings_adjacent', 'ordinary_non_event',
        'event_reviewed_non_event', 'event_unverified_or_pending', 'unknown', '60', 'no-new-positive',
        'validated win-rate: not-computable', 'PA Research', 'no Codex Trading', 'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $eventBucketLabelAuditContent.Contains($token)) {
            Add-ValidationError "missing event-bucket-label-audit token '$token'"
        }
    }
}

$hlReportSpaceVersionAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_report_space_version_conclusion_consistency_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlReportSpaceVersionAuditPath -PathType Leaf) {
    $hlReportSpaceVersionAuditContent = Get-Utf8Text -Path $hlReportSpaceVersionAuditPath
    foreach ($token in @(
        'ENGINE_VERSION = 0.3.9', 'pre_entry_space_R', 'space_status', 'strict_ge_1R',
        'borderline_ge_1R', 'unknown_contract_space', '历史几何', '1.40R', '1.50R',
        '60%', 'no-new-positive', 'validated win-rate: not-computable',
        'PA Research only', 'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlReportSpaceVersionAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L report space/version/conclusion-audit token '$token'"
        }
    }
}

$hlEmaGateReportAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_ema_gate_report_consistency_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlEmaGateReportAuditPath -PathType Leaf) {
    $hlEmaGateReportAuditContent = Get-Utf8Text -Path $hlEmaGateReportAuditPath
    foreach ($token in @(
        'daily_ema20_slope', 'daily_ema50_slope', 'h_l_ema_slope_gate', 'h_l_pullback_location',
        'long_pass', 'short_pass', 'fail_flat_or_opposite', 'pending', 'eligible', 'observation_only',
        '60', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only',
        'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlEmaGateReportAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L EMA-gate/report-consistency-audit token '$token'"
        }
    }
}

$hlPullbackLocationSemanticsAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_pullback_location_semantics_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlPullbackLocationSemanticsAuditPath -PathType Leaf) {
    $hlPullbackLocationSemanticsAuditContent = Get-Utf8Text -Path $hlPullbackLocationSemanticsAuditPath
    foreach ($token in @(
        'h_l_pullback_location', 'rising_EMA20', 'falling_EMA20', 'support', 'resistance',
        'role_reversal', 'controlled_B', 'deep_late_controlled_B', 'long_pass', 'short_pass',
        '60', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only',
        'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlPullbackLocationSemanticsAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L pullback-location-semantics-audit token '$token'"
        }
    }
}

$hlMetaBoundaryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_meta_boundary_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlMetaBoundaryAuditPath -PathType Leaf) {
    $hlMetaBoundaryAuditContent = Get-Utf8Text -Path $hlMetaBoundaryAuditPath
    foreach ($token in @(
        'meta_confluence', 'present', 'absent', 'unknown', 'pending', 'meta_zone', 'meta_components',
        'long_pass', 'short_pass', 'fail_flat_or_opposite', 'strict_ge_1R', 'space_status',
        '60', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only',
        'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlMetaBoundaryAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L META-boundary-audit token '$token'"
        }
    }
}

$hlVisualPreflightContractAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_visual_preflight_contract_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlVisualPreflightContractAuditPath -PathType Leaf) {
    $hlVisualPreflightContractAuditContent = Get-Utf8Text -Path $hlVisualPreflightContractAuditPath
    foreach ($token in @(
        'daily_context_window', 'major_high_low_review', 'ema20_50_200_review', 'label_source',
        'contract_frozen', 'human_chart_review', '>=2y', 'complete', 'ROST',
        'post-decision', 'provenance gap', 'descriptive research record', 'not-validated',
        '60', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only',
        'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlVisualPreflightContractAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L visual-preflight-contract-audit token '$token'"
        }
    }
}

$hlLineageMarketContextAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_lineage_market_context_independence_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlLineageMarketContextAuditPath -PathType Leaf) {
    $hlLineageMarketContextAuditContent = Get-Utf8Text -Path $hlLineageMarketContextAuditPath
    foreach ($token in @(
        'lineage_id', 'market_context_id', '53', '7', '14', '0/60',
        '不同 `lineage_id`', '不能证明市场状态', 'selection', 'replay',
        'no-new-positive', 'validated win-rate: not-computable', 'PA Research only',
        'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlLineageMarketContextAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L lineage/market-context-independence-audit token '$token'"
        }
    }
}

$hlOrderGapContractAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_order_gap_contract_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlOrderGapContractAuditPath -PathType Leaf) {
    $hlOrderGapContractAuditContent = Get-Utf8Text -Path $hlOrderGapContractAuditPath
    foreach ($token in @(
        'order_branch', 'gap_policy', 'entry_trigger', 'structural_stop', 'first_obstacle', 'target_price',
        'stop_confirmation', 'skip', 'accept_open', 'opening-skip', 'no-fill', 'accepted-open',
        '方向几何错误为 `0`', 'first_obstacle=target_price', 'max_hold_bars=10',
        '60/60', '59 行', 'no-new-positive', 'validated win-rate: not-computable',
        'PA Research only', 'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlOrderGapContractAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L order-gap-contract-audit token '$token'"
        }
    }
}

$hlReportStateCountAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_report_state_count_consistency_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $hlReportStateCountAuditPath -PathType Leaf) {
    $hlReportStateCountAuditContent = Get-Utf8Text -Path $hlReportStateCountAuditPath
    foreach ($token in @(
        '7 份有冻结合同', '60', 'eligible', 'filled', 'opening-skip', 'no-fill',
        'observation_only', 'completed', '23 / 11', '34 filled + 20 opening-skip + 1 no-fill + 5 observation_only = 60',
        'next3', '18 个候选、0 条冻结合同', 'next4', 'replay2', 'unproven',
        'no-new-positive', 'validated win-rate: not-computable', 'PA Research only',
        'no Codex Trading', 'no quantitative scanner', 'no Execution Agent'
    )) {
        if (-not $hlReportStateCountAuditContent.Contains($token)) {
            Add-ValidationError "missing H/L report-state-count-audit token '$token'"
        }
    }
}

$legacyNextContractPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_next_contracts_2026-08-27.csv'
$legacyNextReadmePath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/README.md'
$legacyNextSelectionPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_next_selection_2026-08-27_CN.md'
$legacyNextReplayPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/hl_next_replay_2026-08-27_CN.md'
if ((Test-Path -LiteralPath $legacyNextContractPath -PathType Leaf) -and
    (Test-Path -LiteralPath $legacyNextReadmePath -PathType Leaf) -and
    (Test-Path -LiteralPath $legacyNextSelectionPath -PathType Leaf) -and
    (Test-Path -LiteralPath $legacyNextReplayPath -PathType Leaf)) {
    $legacyNextHeader = (Get-Content -LiteralPath $legacyNextContractPath -TotalCount 1) -split ','
    $legacyNextReadmeContent = Get-Utf8Text -Path $legacyNextReadmePath
    $legacyNextSelectionContent = Get-Utf8Text -Path $legacyNextSelectionPath
    $legacyNextReplayContent = Get-Utf8Text -Path $legacyNextReplayPath
    $legacyNextHasExplicitSpace = ($legacyNextHeader -contains 'pre_entry_space_R') -and ($legacyNextHeader -contains 'space_status')
    if (-not $legacyNextHasExplicitSpace) {
        if ($legacyNextReadmeContent -match '全部通过事前\s+`>=1R`\s+空间字段') {
            Add-ValidationError 'hl_next legacy geometry must not be described as explicit pre-entry space fields'
        }
        if ($legacyNextSelectionContent -notmatch 'unknown_contract_space') {
            Add-ValidationError 'hl_next selection must disclose unknown_contract_space when explicit space fields are absent'
        }
        if ($legacyNextReplayContent -notmatch '非当前显式 strict-space') {
            Add-ValidationError 'hl_next replay must qualify historical geometry as non-explicit strict-space'
        }
    }
}

$replayOutcomeAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/replay_outcome_denominator_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $replayOutcomeAuditPath -PathType Leaf) {
    $replayOutcomeAuditContent = Get-Utf8Text -Path $replayOutcomeAuditPath
    foreach ($token in @('win_rate_eligible', 'completed_trade_count', 'incomplete-horizon', 'opening-skip', 'ambiguous_intrabar', 'first_obstacle_hit', 'realized_R', 'max_hold_bars', 'no-new-positive')) {
        if (-not $replayOutcomeAuditContent.Contains($token)) {
            Add-ValidationError "missing replay outcome-audit token '$token'"
        }
    }
}

$replayLineageAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/replay_lineage_independence_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $replayLineageAuditPath -PathType Leaf) {
    $replayLineageAuditContent = Get-Utf8Text -Path $replayLineageAuditPath
    foreach ($token in @('lineage_id', 'market_context_id', 'duplicate_result', 'sample_id', 'results.csv', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $replayLineageAuditContent.Contains($token)) {
            Add-ValidationError "missing replay lineage-independence-audit token '$token'"
        }
    }
}

$replayProvenanceAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/replay_provenance_reproducibility_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $replayProvenanceAuditPath -PathType Leaf) {
    $replayProvenanceAuditContent = Get-Utf8Text -Path $replayProvenanceAuditPath
    foreach ($token in @('engine_version', 'engine_source_sha256', 'results_file_sha256', 'replay2', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $replayProvenanceAuditContent.Contains($token)) {
            Add-ValidationError "missing replay provenance-reproducibility-audit token '$token'"
        }
    }
}

$frozenContractFieldAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/frozen_contract_field_partition_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $frozenContractFieldAuditPath -PathType Leaf) {
    $frozenContractFieldAuditContent = Get-Utf8Text -Path $frozenContractFieldAuditPath
    foreach ($token in @('hl_contracts_2026-08-26.csv', 'contract_state', 'space_status', 'strict_ge_1R', 'observation-only', 'ABC_CONT', 'BOP', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $frozenContractFieldAuditContent.Contains($token)) {
            Add-ValidationError "missing frozen-contract-field-audit token '$token'"
        }
    }
}

$preEntryResultIsolationAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/pre_entry_result_evidence_isolation_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $preEntryResultIsolationAuditPath -PathType Leaf) {
    $preEntryResultIsolationAuditContent = Get-Utf8Text -Path $preEntryResultIsolationAuditPath
    foreach ($token in @('event_context', 'pre_entry_space_R', 'pre_entry_provenance_status', 'pre_entry_provenance_incomplete', 'first_obstacle_hit', 'realized_R', 'contract_eligibility_mismatch_count', 'event_bucket_mismatch_count', 'contract_space_bucket_mismatch_count', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $preEntryResultIsolationAuditContent.Contains($token)) {
            Add-ValidationError "missing pre-entry/result-isolation-audit token '$token'"
        }
    }
}

$preEntryPostOutcomeBoundaryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/pre_entry_post_outcome_boundary_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $preEntryPostOutcomeBoundaryAuditPath -PathType Leaf) {
    $preEntryPostOutcomeBoundaryAuditContent = Get-Utf8Text -Path $preEntryPostOutcomeBoundaryAuditPath
    foreach ($token in @(
        '6 份 `research/backtesting/*_selection_*.md`',
        'signal_bar / new_trigger',
        'structural_invalidation / structural_stop',
        'first_independent_obstacle / space_status',
        'event_context / lineage_id',
        'frozen_pre_outcome',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $preEntryPostOutcomeBoundaryAuditContent.Contains($token)) {
            Add-ValidationError "missing pre-entry/post-outcome boundary-audit token '$token'"
        }
    }
}

$legacyResultProvenanceAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/legacy_result_provenance_completeness_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $legacyResultProvenanceAuditPath -PathType Leaf) {
    $legacyResultProvenanceAuditContent = Get-Utf8Text -Path $legacyResultProvenanceAuditPath
    foreach ($token in @('pre_entry_provenance_status', 'pre_entry_provenance_missing_fields', 'completed_trade_count', 'pre_entry_provenance_incomplete', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $legacyResultProvenanceAuditContent.Contains($token)) {
            Add-ValidationError "missing legacy-result-provenance-audit token '$token'"
        }
    }
}

$artifactSchemaRoundtripAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/artifact_schema_roundtrip_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $artifactSchemaRoundtripAuditPath -PathType Leaf) {
    $artifactSchemaRoundtripAuditContent = Get-Utf8Text -Path $artifactSchemaRoundtripAuditPath
    foreach ($token in @('results.csv', 'summary.json', 'run_metadata.json', 'summary_provenance', 'result_columns', 'pre_entry_provenance_status', 'contract_eligibility_mismatch_count', 'event_bucket_mismatch_count', 'contract_space_bucket_mismatch_count', 'historical', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $artifactSchemaRoundtripAuditContent.Contains($token)) {
            Add-ValidationError "missing artifact-schema-roundtrip-audit token '$token'"
        }
    }
}

$historicalReplayResultLogAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/historical_replay_result_log_provenance_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $historicalReplayResultLogAuditPath -PathType Leaf) {
    $historicalReplayResultLogAuditContent = Get-Utf8Text -Path $historicalReplayResultLogAuditPath
    foreach ($token in @('external_results_files=13', 'external_result_rows=88', 'unique_sample_ids=63', 'duplicate_sample_id_groups=13', 'rows_in_duplicate_groups=38', 'extra_duplicate_rows=25', 'current_valid=0', 'historical_incomplete=13', 'invalid=0', 'historical_exit_code=2', 'journal/', 'trade_log/', 'transaction/', 'ledger/', '冻结合同 CSV', 'results.csv` 是模拟结果记录，不是券商订单', '当前 PA Research 没有实际订单', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $historicalReplayResultLogAuditContent.Contains($token)) {
            Add-ValidationError "missing historical replay/result-log provenance audit token '$token'"
        }
    }
    foreach ($indexRelativePath in @('docs/README.md', 'strategy/README.md', 'docs/research_to_system_handoff_CN.md')) {
        $indexPath = Join-Path -Path $repoRoot -ChildPath ($indexRelativePath -replace '/', '\\')
        if (-not (Test-Path -LiteralPath $indexPath -PathType Leaf)) {
            Add-ValidationError "missing transaction-log boundary index '$indexRelativePath'"
            continue
        }
        $indexContent = Get-Utf8Text -Path $indexPath
        if (-not $indexContent.Contains('historical_replay_result_log_provenance_audit_2026-08-29_CN.md')) {
            Add-ValidationError "missing transaction-log provenance audit link in '$indexRelativePath'"
        }
    }
}

$unifiedOutputStateAxisAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/unified_output_state_axis_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $unifiedOutputStateAxisAuditPath -PathType Leaf) {
    $unifiedOutputStateAxisAuditContent = Get-Utf8Text -Path $unifiedOutputStateAxisAuditPath
    foreach ($token in @('document_maturity', 'attempt_direction', 'Daily', '4H', '15m', 'lineage_id', 'event_bucket', 'space_status', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $unifiedOutputStateAxisAuditContent.Contains($token)) {
            Add-ValidationError "missing unified-output state-axis audit token '$token'"
        }
    }
}

$patternIndexAliasBoundaryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_index_alias_boundary_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternIndexAliasBoundaryAuditPath -PathType Leaf) {
    $patternIndexAliasBoundaryAuditContent = Get-Utf8Text -Path $patternIndexAliasBoundaryAuditPath
    foreach ($token in @('01_h1_l1_first_entry', '02_h2_l2_second_entry', '03_abc_continuation', '04_range_edge_second_entry', '05_failed_breakout_climax', '06_breakout_pullback_bop', '07_mtr_reversal', '08_three_push_h3_l3', '09_vcp_minervini', '10_final_flag', '11_opening_reversal', '12_channel', '13_inside_bar_two_bar_reversal', '14_triangle_expanding_range', '15_double_top_bottom', '16_head_shoulders_rounded', 'primary_pattern: ABC_CONT', 'internal_label=H1 / L1', 'internal_label=H2 / L2', 'internal_label=H3 / L3', 'state_transition', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only', 'no Codex Trading', 'no quantitative scanner', 'no Execution Agent')) {
        if (-not $patternIndexAliasBoundaryAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern-index-alias-boundary-audit token '$token'"
        }
    }
}

$patternLabelTransitionAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_label_transition_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternLabelTransitionAuditPath -PathType Leaf) {
    $patternLabelTransitionAuditContent = Get-Utf8Text -Path $patternLabelTransitionAuditPath
    foreach ($token in @(
        '01_h1_l1_first_entry',
        '02_h2_l2_second_entry',
        '03_abc_continuation',
        '04_range_edge_second_entry',
        '05_failed_breakout_climax',
        '06_breakout_pullback_bop',
        '07_mtr_reversal',
        '08_three_push_h3_l3',
        '09_vcp_minervini',
        '10_final_flag',
        '11_opening_reversal',
        '12_channel',
        '13_inside_bar_two_bar_reversal',
        '14_triangle_expanding_range',
        '15_double_top_bottom',
        '16_head_shoulders_rounded',
        '日线候选的主标签白名单',
        'H1/H2/L1/L2 只能写入 `internal_label`',
        'range_edge_three_push',
        'primary_pattern: BOP',
        'state_transition: breakout_acceptance',
        '原 pattern 或反向 thesis 与旧订单合同同时失效',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $patternLabelTransitionAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern-label-transition-audit token '$token'"
        }
    }
}

$threePushContractBoundaryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/three_push_h3_l3_contract_boundary_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $threePushContractBoundaryAuditPath -PathType Leaf) {
    $threePushContractBoundaryAuditContent = Get-Utf8Text -Path $threePushContractBoundaryAuditPath
    foreach ($token in @(
        'third_push_state: exhaustion_candidate / continuation_or_climax / range_repeat_test / channel_continuation / unclear',
        'range_edge_side: upper / lower / none / pending',
        'range_edge_three_push=yes',
        'H3/L3 冻结行 | 0',
        '订单/状态分轴',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $threePushContractBoundaryAuditContent.Contains($token)) {
            Add-ValidationError "missing three-push contract-boundary audit token '$token'"
        }
    }
}

$threePushStrategyCaseAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/three_push_strategy_case_contract_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $threePushStrategyCaseAuditPath -PathType Leaf) {
    $threePushStrategyCaseAuditContent = Get-Utf8Text -Path $threePushStrategyCaseAuditPath
    foreach ($token in @(
        'strategy/01_three_push_wedge_candidate.md',
        '../h3_l3_research_gate_CN.md',
        '../h3_l3_visual_comparison_CN.md',
        '../three_push_pressure_state_framework_CN.md',
        'A/B/C 是解释性分流，不是新的状态枚举',
        'third_push_state=exhaustion_candidate',
        'first_independent_obstacle',
        'research_state=research_positive_conditional',
        'H3/L3 冻结行数为 0',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $threePushStrategyCaseAuditContent.Contains($token)) {
            Add-ValidationError "missing three-push strategy/case audit token '$token'"
        }
    }
}

$h3CandidateScreenProvenanceAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/h3_l3_candidate_screen_provenance_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $h3CandidateScreenProvenanceAuditPath -PathType Leaf) {
    $h3CandidateScreenProvenanceAuditContent = Get-Utf8Text -Path $h3CandidateScreenProvenanceAuditPath
    foreach ($token in @(
        'h3_l3_candidate_screen_2025-08_2025-11_CN.md',
        'h3_l3_candidate_screen_futu_targeted_2024_2026_CN.md',
        'data_status: historical',
        'as_of_time: unavailable_in_original_log',
        'event_unverified_or_pending',
        'third_push_state',
        'opening-skip/gap-reprice',
        '7 份 CSV、60 行',
        'H3/L3 冻结行数为 0',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $h3CandidateScreenProvenanceAuditContent.Contains($token)) {
            Add-ValidationError "missing H3/L3 candidate-screen provenance audit token '$token'"
        }
    }
}

$threePushActiveLegacyChecks = @{
    'research/h3_l3_visual_comparison_CN.md' = @('h3_l3_state:', 'reverse_trigger_present', 'short_reaction_candidate')
    'research/three_push_pressure_state_framework_CN.md' = @('same_lineage:', 'first_obstacle:', 'rough_rr:', 'status: research_candidate / short_reaction / continuation / valid_no_trade')
    'research/mtr_visual_framework_CN.md' = @('short_reaction_candidate')
    'strategy/01_three_push_wedge_candidate.md' = @('research_positive_candidate')
}
foreach ($entry in $threePushActiveLegacyChecks.GetEnumerator()) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($entry.Key -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in $entry.Value) {
        if ($content.Contains($token)) {
            Add-ValidationError "legacy three-push field or enum in active document '$token': $($entry.Key)"
        }
    }
}

$visualRecognitionSmokeTestPath = Join-Path -Path $repoRoot -ChildPath 'research/visual_recognition_smoke_test_2026-08-24_CN.md'
if (Test-Path -LiteralPath $visualRecognitionSmokeTestPath -PathType Leaf) {
    $visualRecognitionSmokeTestContent = Get-Utf8Text -Path $visualRecognitionSmokeTestPath
    if ($visualRecognitionSmokeTestContent -notmatch 'visual_pattern_label:') {
        Add-ValidationError 'visual recognition smoke test is missing visual_pattern_label'
    }
    if ($visualRecognitionSmokeTestContent -match '(?m)^primary_pattern:') {
        Add-ValidationError 'visual recognition smoke test must not use free-text primary_pattern field'
    }
    if ($visualRecognitionSmokeTestContent -match '(?m)^two_year_daily_context:') {
        Add-ValidationError 'visual recognition smoke test must use canonical daily_context_window field'
    }
}

$canonicalEvidenceLegacyPaths = @(
    'research/cost_bullish_abc_h2_visual_boundary_2025-04-21_2025-05-16.md',
    'research/jnj_bullish_h1_first_obstacle_2025-09-18_2025-10-08.md',
    'research/jpm_bullish_h1_first_obstacle_failure_2025-08-22_2025-09-05.md',
    'research/nvda_bullish_h1_trigger_branch_first_obstacle_2025-04-21_2025-05-08.md',
    'research/tsla_bearish_abc_candidate_screen_2026-08-22.md',
    'research/tsla_h1_h2_candidate_screen_2024-08-22_2026-08-21.md',
    'research/visual_recognition_smoke_test_2026-08-24_CN.md',
    'research/visual_recognition_round4_historical_practice_2026-08-24_CN.md',
    'research/assets/visual_recognition/2026-08-24/round4_historical_practice/README.md',
    'research/assets/visual_recognition/2026-08-24/round5_two_year_daily/README.md',
    'research/assets/visual_recognition/2026-08-24/tsla_public_mtf/README.md'
)
foreach ($relativePath in $canonicalEvidenceLegacyPaths) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    if ($content -match '(?m)^timeframe_seen:') {
        Add-ValidationError "legacy singular timeframe field remains: $relativePath"
    }
    if ($content -match '(?m)^data_status:\s*(?:historical_close|historical / after-close|historical public)') {
        Add-ValidationError "non-canonical data_status remains: $relativePath"
    }
    foreach ($token in @('data_status:', 'timeframes_seen:', 'chart_scope:', 'daily_context_window:')) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "canonical evidence field missing '$token': $relativePath"
        }
    }
}

$evidenceScopeStatusAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/evidence_scope_status_boundary_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $evidenceScopeStatusAuditPath -PathType Leaf) {
    $evidenceScopeStatusAuditContent = Get-Utf8Text -Path $evidenceScopeStatusAuditPath
    foreach ($token in @(
        'contract_scope: daily_candidate',
        'timeframes_seen: Daily',
        'daily_context_window',
        'chart_scope',
        'data_status',
        'historical_close` 是 `session_state` 的值',
        '回放 CSV',
        '16 个 `patterns/*/README.md`',
        'historical',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $evidenceScopeStatusAuditContent.Contains($token)) {
            Add-ValidationError "missing evidence-scope/status audit token '$token'"
        }
    }
}

$patternVisualPreflightAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_visual_preflight_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternVisualPreflightAuditPath -PathType Leaf) {
    $patternVisualPreflightAuditContent = Get-Utf8Text -Path $patternVisualPreflightAuditPath
    foreach ($token in @('daily_context_window: >=2y / <2y / unavailable', 'major_highs', 'major_lows', 'daily_ema20_50_200', 'A_quality: strong', 'B_quality: controlled', 'first_independent_obstacle', '强 A→H1/L1 优先', 'H2/L2 可以承接普通 A', '成熟区间边缘三推是明确例外', '允许普通/偏弱 A', '区间中部三推仍为观察', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only', 'no Codex Trading', 'no quantitative scanner', 'no Execution Agent')) {
        if (-not $patternVisualPreflightAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern-visual-preflight-audit token '$token'"
        }
    }
}

$commonVisualPreflightAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/common_visual_preflight_field_consistency_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $commonVisualPreflightAuditPath -PathType Leaf) {
    $commonVisualPreflightAuditContent = Get-Utf8Text -Path $commonVisualPreflightAuditPath
    foreach ($token in @(
        'chart_scope: full / partial / unavailable',
        'daily_context_window: >=2y / <2y / unavailable',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'a_leg_quality: strong / ordinary / unclear / event_driven',
        'b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear',
        'first_independent_obstacle:',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $commonVisualPreflightAuditContent.Contains($token)) {
            Add-ValidationError "missing common-visual-preflight audit token '$token'"
        }
    }
}

$visualAuthoritySchemaAlignmentAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/visual_authority_schema_alignment_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $visualAuthoritySchemaAlignmentAuditPath -PathType Leaf) {
    $visualAuthoritySchemaAlignmentAuditContent = Get-Utf8Text -Path $visualAuthoritySchemaAlignmentAuditPath
    foreach ($token in @(
        '23 个活动文档',
        'no-new-positive',
        'validated win-rate: not-computable',
        '不修改 Codex Trading',
        '不创建量化扫描器',
        '不连接 Futu/OpenD',
        '不连接 Execution Agent',
        '不修改 CSV/历史结果/engine 有效语义'
    )) {
        if (-not $visualAuthoritySchemaAlignmentAuditContent.Contains($token)) {
            Add-ValidationError "missing visual-authority-schema-alignment audit token '$token'"
        }
    }
}

$visualAuthorityActiveTemplateRelativePaths = @(
    'research/market_state_context_visual_evidence_audit_2026-08-24_CN.md',
    'research/inside_bar_two_bar_reversal_visual_framework_CN.md',
    'research/triangle_expanding_range_visual_framework_CN.md',
    'research/late_trend_entry_visual_framework_CN.md',
    'research/multitimeframe_visual_review_framework_CN.md'
)
foreach ($relativePath in $visualAuthorityActiveTemplateRelativePaths) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in @(
        'contract_scope:',
        'data_status:',
        'as_of_time:',
        'timeframes_seen:',
        'daily_context_window:',
        'major_high_low_review:',
        'ema20_50_200_review:',
        'direction: long / short / no_valid_direction',
        'order_branch:',
        'research_state:',
        'trade_state:',
        'gate_result:',
        'handoff_status:'
    )) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "visual authority template missing canonical token '$token': $relativePath"
        }
    }
    $requiredGeometryToken = if ($relativePath -eq 'research/multitimeframe_visual_review_framework_CN.md') {
        'parent_first_independent_obstacle:'
    } else {
        'first_independent_obstacle:'
    }
    if (-not $content.Contains($requiredGeometryToken)) {
        Add-ValidationError "visual authority template missing canonical obstacle '$requiredGeometryToken': $relativePath"
    }
    foreach ($legacyToken in @(
        '(?m)^\s*final_state:',
        '(?m)^\s*order_contract:',
        '(?m)^\s*first_obstacle:',
        '(?m)^\s*rough_rr:',
        '(?m)^\s*three_push_state:',
        '(?m)^\s*trigger_order:',
        '(?m)^\s*actual_or_assumed_fill:',
        '(?m)^\s*review_timeframe:',
        '(?m)^\s*parent_pattern:',
        '(?m)^\s*decision:',
        '(?m)^\s*status:'
    )) {
        if ($content -match $legacyToken) {
            Add-ValidationError "legacy visual authority template field remains '$legacyToken': $relativePath"
        }
    }
}

$patternFoundationCanonicalAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/pattern_foundation_canonical_contract_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternFoundationCanonicalAuditPath -PathType Leaf) {
    $patternFoundationCanonicalAuditContent = Get-Utf8Text -Path $patternFoundationCanonicalAuditPath
    foreach ($token in @(
        '16 个 pattern README',
        '8 个基础视觉层',
        'contract_scope',
        'timeframes_seen',
        'daily_context_window',
        'major_high_low_review',
        'ema20_50_200_review',
        'primary_pattern',
        'internal_label',
        'lineage_status',
        'state_transition',
        'order_branch',
        'structural_stop',
        'first_independent_obstacle',
        'pre_entry_space_R',
        'space_status',
        'research_state',
        'trade_state',
        'gate_result',
        'handoff_status',
        'no-new-positive',
        'validated win-rate: not-computable',
        'PA Research only',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent',
        '追加交易日志边界复核',
        '研究/回放订单路径',
        '真实交易日志',
        '独立来源'
    )) {
        if (-not $patternFoundationCanonicalAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern-foundation-canonical-audit token '$token'"
        }
    }
}

$patternFoundationDirectories = @(
    '01_h1_l1_first_entry',
    '02_h2_l2_second_entry',
    '03_abc_continuation',
    '04_range_edge_second_entry',
    '05_failed_breakout_climax',
    '06_breakout_pullback_bop',
    '07_mtr_reversal',
    '08_three_push_h3_l3',
    '09_vcp_minervini',
    '10_final_flag',
    '11_opening_reversal',
    '12_channel',
    '13_inside_bar_two_bar_reversal',
    '14_triangle_expanding_range',
    '15_double_top_bottom',
    '16_head_shoulders_rounded'
)
foreach ($directory in $patternFoundationDirectories) {
    $patternReadmePath = Join-Path -Path $repoRoot -ChildPath ("patterns\$directory\README.md")
    if (-not (Test-Path -LiteralPath $patternReadmePath -PathType Leaf)) { continue }
    $patternReadmeContent = Get-Utf8Text -Path $patternReadmePath
    foreach ($token in @(
        '../../docs/pa_research_output_schema_v0_1_CN.md',
        '../../docs/visual_pa_review_card_CN.md',
        'data_status: historical / delayed / live_confirmed / incomplete',
        'as_of_time',
        'timeframes_seen',
        'chart_scope',
        'daily_context_window',
        'EMA20/50/200',
        'pending',
        'primary_pattern'
    )) {
        if (-not $patternReadmeContent.Contains($token)) {
            Add-ValidationError "pattern README missing canonical coverage token '$token': $directory"
        }
    }
    if ($patternReadmeContent -notmatch '重要高点|主要高点' -or $patternReadmeContent -notmatch '重要低点|主要低点') {
        Add-ValidationError "pattern README missing major high/low preflight wording: $directory"
    }
    if ($patternReadmeContent -notmatch '第一独立障碍|first_independent_obstacle|首障碍') {
        Add-ValidationError "pattern README missing independent-obstacle wording: $directory"
    }
}

$threePushPatternReadmePath = Join-Path -Path $repoRoot -ChildPath 'patterns\08_three_push_h3_l3\README.md'
if (Test-Path -LiteralPath $threePushPatternReadmePath -PathType Leaf) {
    $threePushPatternReadmeContent = Get-Utf8Text -Path $threePushPatternReadmePath
    foreach ($token in @(
        'contract_scope: deep_review / daily_candidate / historical_context_only',
        'timeframes_seen: Daily / 4H / 1H / 15m / other',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'direction: long / short / no_valid_direction',
        'primary_pattern: ABC_CONT / BOP / H3_L3 / other',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'lineage_id:',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable',
        'structural_invalidation:',
        'rough_space_to_first_obstacle_R:',
        'pre_entry_space_R:',
        'count_timeframe',
        '不能用单数 `timeframe` 或 `context_timeframes_seen`'
    )) {
        if (-not $threePushPatternReadmeContent.Contains($token)) {
            Add-ValidationError "three-push README missing canonical local-card token '$token'"
        }
    }
    if ($threePushPatternReadmeContent -match '(?m)^timeframe:' -or
        $threePushPatternReadmeContent -match '(?m)^context_timeframes_seen:') {
        Add-ValidationError 'three-push README retains singular timeframe evidence field'
    }
}

$foundationCanonicalChecks = @{
    'foundations/03_late_trend_entry_filter/README.md' = @(
        'contract_scope: deep_review / daily_candidate / historical_context_only',
        'timeframes_seen:',
        'daily_context_window: >=2y / <2y / unavailable',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'direction: long / short / no_valid_direction',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'actual_fill_or_open_skip:',
        'structural_stop:',
        'first_independent_obstacle:',
        'pre_entry_space_R:',
        'space_status:',
        'research_state:',
        'trade_state:',
        'gate_result:',
        'handoff_status:'
    )
    'foundations/04_multitimeframe_review/README.md' = @(
        'chart_scope: full / partial / unavailable',
        'daily_context_window: >=2y / <2y / unavailable',
        'major_high_low_review: complete / partial / unavailable',
        'ema20_50_200_review: complete / partial / unavailable',
        'primary_pattern: ABC_CONT / BOP / H1_L1 / H2_L2 / H3_L3 / RFB / MTR / other',
        'signal_bar:',
        'new_trigger:',
        'actual_fill_or_open_skip:',
        'gap_policy:',
        'structural_stop:',
        'first_independent_obstacle:',
        'pre_entry_space_R:',
        'space_status:',
        'research_state:',
        'trade_state:',
        'gate_result:',
        'handoff_status:'
    )
    'foundations/05_event_sector_market_gate/README.md' = @(
        'contract_scope: deep_review',
        'data_status: historical / delayed / live_confirmed / incomplete',
        'as_of_time:',
        'timeframes_seen:',
        'direction: long / short / no_valid_direction',
        'permission: long_allowed / short_allowed / both_allowed / no_direction / unknown',
        'gate_result: pass / conditional / observation_only / valid_no_trade / pending'
    )
    'foundations/06_order_risk_contracts/README.md' = @(
        'contract_scope: deep_review / daily_candidate / historical_context_only',
        'as_of_time:',
        'timeframes_seen:',
        'new_trigger:',
        'order_price_or_zone:',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'actual_fill_or_open_skip: filled / no_fill / opening_skip / fill_unknown / not_applicable',
        '`actual_fill_or_open_skip` 和 `original_order_status` 只描述研究/回放订单路径，不是券商或账户的实际成交日志',
        'structural_invalidation:',
        'structural_stop:',
        'first_independent_obstacle:',
        'rough_space_to_first_obstacle_R:',
        'pre_entry_space_R:',
        'space_status:',
        'research_state:',
        'trade_state:',
        'gate_result:',
        'handoff_status:'
    )
    'foundations/07_market_state_context/README.md' = @(
        'contract_scope: deep_review / daily_candidate / historical_context_only',
        'data_status: historical / delayed / live_confirmed / incomplete',
        'timeframes_seen:',
        'daily_context_window: >=2y / <2y / unavailable',
        'parent_state: open_trend / trading_range / range_edge / transition / climax / unclear',
        'range_state: mature / developing / transition / not_range',
        'lineage_status: same_lineage / reset / unclear / pending',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'research_state:',
        'trade_state:',
        'gate_result:',
        'handoff_status:'
    )
    'foundations/08_leg_pressure_signal_quality/README.md' = @(
        'a_leg_quality: strong / ordinary / unclear / event_driven',
        'b_leg_class: controlled / controlled_late / deep_but_late_controlled / uncontrolled / range_like / unclear',
        'b_leg_location:',
        'signal_bar:',
        'confirmation_bar:',
        'new_trigger:',
        'follow_through:',
        'daily_ema20_slope: up / flat / down / unknown',
        'daily_ema50_slope: up / flat / down / unknown',
        'h_l_pullback_location:',
        'direction: long / short / no_valid_direction',
        'primary_pattern:',
        'internal_label:',
        'lineage_status:',
        'research_state:',
        'trade_state:',
        'gate_result:',
        'handoff_status:'
    )
}
foreach ($entry in $foundationCanonicalChecks.GetEnumerator()) {
    $relativePath = $entry.Key
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in $entry.Value) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "foundation README missing canonical coverage token '$token': $relativePath"
        }
    }
}

$foundationLegacyFieldChecks = @{
    'foundations/03_late_trend_entry_filter/README.md' = @('(?m)^timeframe:', '(?m)^actual_fill_assumption:', '(?m)^rough_R_R_to_first_obstacle:', '(?m)^final_state:')
    'foundations/04_multitimeframe_review/README.md' = @('(?m)^parent_pattern:', '(?m)^actual_or_assumed_fill:', '(?m)^gap_state:', '(?m)^decision:')
    'foundations/06_order_risk_contracts/README.md' = @('(?m)^decision_time:', '(?m)^timeframe_and_parent_contract:', '(?m)^trigger_or_zone:', '(?m)^actual_or_assumed_fill:', '(?m)^space_to_first_obstacle:', '(?m)^final_status:')
    'foundations/07_market_state_context/README.md' = @('(?m)^timeframe:', '(?m)^attempt_lineage:', '(?m)^breakout_acceptance:', '(?m)^decision:', '(?m)^parent_state:.*mature_range')
    'foundations/08_leg_pressure_signal_quality/README.md' = @('(?m)^A_quality:', '(?m)^EMA20_slope:', '(?m)^EMA50_slope:', '(?m)^pullback_location:', '(?m)^decision:')
}
foreach ($entry in $foundationLegacyFieldChecks.GetEnumerator()) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($entry.Key -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($legacyPattern in $entry.Value) {
        if ($content -match $legacyPattern) {
            Add-ValidationError "active foundation legacy field remains '$legacyPattern': $($entry.Key)"
        }
    }
}

$transactionBoundaryIndexPaths = @(
    'foundations/README.md',
    'patterns/README.md'
)
foreach ($relativePath in $transactionBoundaryIndexPaths) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in @('研究合同', '历史回放', '真实交易日志', '独立来源')) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "transaction-log boundary index missing '$token': $relativePath"
        }
    }
}

$coreTransactionLogBoundaryChecks = @{
    'research/README.md' = @(
        '当前 PA Research checkout 不包含券商或账户的真实交易日志；研究合同、历史回放结果和运行 metadata 都不能代替真实交易日志。'
    )
    'research/backtesting/README.md' = @(
        '当前 PA Research checkout 不包含券商或账户的真实交易日志；研究合同、历史回放结果和运行 metadata 都不能代替真实交易日志。',
        '记录回放器的模拟成交状态、模拟退出状态'
    )
}
foreach ($entry in $coreTransactionLogBoundaryChecks.GetEnumerator()) {
    $relativePath = $entry.Key
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($relativePath -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Utf8Text -Path $absolutePath
    foreach ($token in $entry.Value) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "core transaction-log boundary missing '$token': $relativePath"
        }
    }
}

$activeOrderTemplateReadmes = @(
    Get-ChildItem -LiteralPath (Join-Path -Path $repoRoot -ChildPath 'foundations') -Recurse -File -Filter 'README.md'
    Get-ChildItem -LiteralPath (Join-Path -Path $repoRoot -ChildPath 'patterns') -Recurse -File -Filter 'README.md'
)
foreach ($file in $activeOrderTemplateReadmes) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1)
    $content = Get-Utf8Text -Path $file.FullName
    if ($content -match '(?im)^\s*actual_fill_or_open_skip:') {
        foreach ($token in @('订单路径', '交易日志', '独立来源')) {
            if (-not $content.Contains($token)) {
                Add-ValidationError "active order template missing transaction-log boundary '$token': $relativePath"
            }
        }
    }
}

$visualPaReviewCardPath = Join-Path -Path $repoRoot -ChildPath 'docs/visual_pa_review_card_CN.md'
if (Test-Path -LiteralPath $visualPaReviewCardPath -PathType Leaf) {
    $visualPaReviewCardContent = Get-Utf8Text -Path $visualPaReviewCardPath
    foreach ($token in @(
        'primary_pattern: ABC_CONT | BOP | RFB | H3_L3 | MTR | other',
        'pattern_family: ABC_CONT | BOP | RFB_SECOND | H3_L3 | MTR | other',
        'lineage_status: same_lineage / reset / unclear / pending',
        'lineage_id:',
        '历史显示值 `RFB_SECOND` 只映射到兼容主标签 `RFB`'
    )) {
        if (-not $visualPaReviewCardContent.Contains($token)) {
            Add-ValidationError "visual PA review card missing canonical authority token '$token'"
        }
    }
    foreach ($legacyToken in @('(?m)^\s*attempt:', '(?m)^\s*same_lineage:')) {
        if ($visualPaReviewCardContent -match $legacyToken) {
            Add-ValidationError "visual PA review card retains active counting alias '$legacyToken'"
        }
    }
}

$entryGeometryStateBoundaryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/entry_geometry_state_boundary_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $entryGeometryStateBoundaryAuditPath -PathType Leaf) {
    $entryGeometryStateBoundaryAuditContent = Get-Utf8Text -Path $entryGeometryStateBoundaryAuditPath
    foreach ($token in @(
        '统一几何顺序',
        'observation_only',
        'valid_no_trade',
        'first_independent_obstacle',
        'rough_R_R',
        'no-new-positive',
        'validated win-rate: not-computable',
        'no Codex Trading',
        'no quantitative scanner',
        'no Execution Agent'
    )) {
        if (-not $entryGeometryStateBoundaryAuditContent.Contains($token)) {
            Add-ValidationError "missing entry-geometry/state-boundary audit token '$token'"
        }
    }
}

$frozenContractFiles = @(Get-ChildItem -LiteralPath (Join-Path -Path $repoRoot -ChildPath 'research/backtesting') -File -Filter '*contracts*.csv' | Where-Object {
    $_.Name -ne 'contracts.example.csv'
})
$frozenContractRecords = [System.Collections.Generic.List[object]]::new()
$allowedSpaceStatuses = @('strict_ge_1R', 'borderline_ge_1R', 'clearly_positive', 'borderline', 'blocked', 'unknown')
$allowedDirections = @('long', 'short')
$allowedPatterns = @('ABC_CONT', 'BOP', 'H1_L1', 'H2_L2', 'H3_L3', 'RFB', 'MTR', 'other')
$allowedLabels = @('H1', 'H2', 'L1', 'L2', 'H3', 'L3', 'none', 'pending')
$allowedEmaSlopes = @('up', 'flat', 'down', 'unknown')
$allowedEmaGates = @('long_pass', 'short_pass', 'fail_flat_or_opposite', 'pending', 'not_applicable')
$allowedALegQualities = @('strong', 'ordinary', 'unclear', 'event_driven')
$legacyALegQualityAliases = @('strong_A', 'ordinary_A')
$allowedBLegClasses = @('controlled', 'controlled_late', 'deep_but_late_controlled', 'uncontrolled', 'range_like', 'unclear')
$legacyBLegClassAliases = @('controlled_B', 'deep_late_controlled_B')
$allowedContractStates = @('', 'frozen_pre_outcome')
$allowedOrderBranches = @('stop_confirmation', 'limit_retest', 'market_close')
$allowedGapPolicies = @('accept_open', 'skip', 'flag_only', 'not_applicable')
$allowedMetaConfluence = @('present', 'absent', 'unknown')
$postOutcomeColumns = @(
    'entry_price', 'entry_date', 'exit_price', 'exit_date', 'exit_reason',
    'bars_held', 'fill_status', 'trade_result', 'realized_R', 'win_rate_eligible',
    'path_result', 'first_obstacle_hit', 'ambiguous_intrabar', 'gap_adjustment',
    'evidence_status'
)
$requiredFrozenContractColumns = @(
    'sample_id', 'symbol', 'decision_date', 'direction', 'primary_pattern',
    'internal_label', 'order_branch', 'entry_trigger', 'structural_stop',
    'first_obstacle', 'target_price', 'max_hold_bars', 'gap_policy',
    'label_source', 'daily_context_window', 'major_high_low_review',
    'ema20_50_200_review', 'event_context', 'contract_frozen', 'lineage_id'
)
$requiredNonEmptyFrozenContractColumns = @(
    'sample_id', 'symbol', 'decision_date', 'direction', 'primary_pattern',
    'internal_label', 'order_branch', 'structural_stop', 'first_obstacle',
    'target_price', 'max_hold_bars', 'gap_policy', 'label_source',
    'daily_context_window', 'major_high_low_review', 'ema20_50_200_review',
    'event_context', 'contract_frozen', 'lineage_id'
)
foreach ($file in $frozenContractFiles) {
    $rows = @(Import-Csv -LiteralPath $file.FullName)
    if ($rows.Count -eq 0) {
        Add-ValidationError "frozen contract CSV has no rows: $($file.Name)"
        continue
    }
    $columnNames = @($rows[0].PSObject.Properties.Name)
    foreach ($column in @($columnNames | Where-Object { $_ -in $postOutcomeColumns })) {
        Add-ValidationError "post-outcome column is not allowed in frozen contract CSV: $($file.Name) / $column"
    }
    $missingColumns = @($requiredFrozenContractColumns | Where-Object { $_ -notin $columnNames })
    foreach ($column in $missingColumns) {
        if ($column -notin $columnNames) {
            Add-ValidationError "missing frozen contract column '$column': $($file.Name)"
        }
    }
    if ($missingColumns.Count -gt 0) {
        continue
    }
    foreach ($row in $rows) {
        $sampleId = Get-TrimmedText $row.sample_id
        $symbol = Get-TrimmedText $row.symbol
        $decisionDate = Get-TrimmedText $row.decision_date
        $direction = (Get-TrimmedText $row.direction).ToLowerInvariant()
        $primaryPattern = (Get-TrimmedText $row.primary_pattern).ToUpperInvariant()
        if ($primaryPattern -eq 'OTHER') {
            $primaryPattern = 'other'
        }
        $internalLabel = (Get-TrimmedText $row.internal_label).ToUpperInvariant()
        if ($internalLabel -eq 'NONE') { $internalLabel = 'none' }
        if ($internalLabel -eq 'PENDING') { $internalLabel = 'pending' }
        $lineageId = Get-TrimmedText $row.lineage_id
        $orderBranch = (Get-TrimmedText $row.order_branch).ToLowerInvariant()
        $gapPolicy = (Get-TrimmedText $row.gap_policy).ToLowerInvariant()
        $labelSource = (Get-TrimmedText $row.label_source).ToLowerInvariant()
        $dailyContextWindow = (Get-TrimmedText $row.daily_context_window).ToLowerInvariant()
        $majorHighLowReview = (Get-TrimmedText $row.major_high_low_review).ToLowerInvariant()
        $emaReview = (Get-TrimmedText $row.ema20_50_200_review).ToLowerInvariant()
        $eventContext = Get-TrimmedText $row.event_context
        $contractFrozen = (Get-TrimmedText $row.contract_frozen).ToLowerInvariant()
        $spaceStatus = Get-TrimmedText $row.space_status
        $spaceStatusLower = $spaceStatus.ToLowerInvariant()
        $ema20Slope = (Get-TrimmedText $row.daily_ema20_slope).ToLowerInvariant()
        $ema50Slope = (Get-TrimmedText $row.daily_ema50_slope).ToLowerInvariant()
        $emaGate = (Get-TrimmedText $row.h_l_ema_slope_gate).ToLowerInvariant()
        $pullbackLocation = Get-TrimmedText $row.h_l_pullback_location
        $metaConfluence = (Get-TrimmedText $row.meta_confluence).ToLowerInvariant()
        $aLegQuality = Get-TrimmedText $row.a_leg_quality
        $bLegClass = Get-TrimmedText $row.b_leg_class
        $contractState = (Get-TrimmedText $row.contract_state).ToLowerInvariant()

        foreach ($column in $requiredNonEmptyFrozenContractColumns) {
            $value = Get-TrimmedText $row.PSObject.Properties[$column].Value
            if ([string]::IsNullOrWhiteSpace($value)) {
                Add-ValidationError "frozen contract row missing required value '$column': $($file.Name) / $sampleId"
            }
        }
        if ($contractFrozen -ne 'yes') {
            Add-ValidationError "non-frozen row in frozen contract CSV: $($file.Name) / $sampleId"
        }
        if ([string]::IsNullOrWhiteSpace($sampleId) -or [string]::IsNullOrWhiteSpace($symbol) -or [string]::IsNullOrWhiteSpace($decisionDate)) {
            Add-ValidationError "frozen contract row missing identity field: $($file.Name) / $sampleId"
        }
        if (-not (Test-ValidDate $decisionDate)) {
            Add-ValidationError "frozen contract row has invalid decision_date: $($file.Name) / $sampleId"
        }
        if ($direction -notin $allowedDirections) {
            Add-ValidationError "frozen contract row has invalid direction: $($file.Name) / $sampleId"
        }
        if ($primaryPattern -notin $allowedPatterns) {
            Add-ValidationError "frozen contract row has invalid primary_pattern: $($file.Name) / $sampleId"
        }
        if ($internalLabel -notin $allowedLabels) {
            Add-ValidationError "frozen contract row has invalid internal_label: $($file.Name) / $sampleId"
        }
        if ([string]::IsNullOrWhiteSpace($lineageId)) {
            Add-ValidationError "frozen contract row missing lineage_id: $($file.Name) / $sampleId"
        }
        if ([string]::IsNullOrWhiteSpace($eventContext)) {
            Add-ValidationError "frozen contract row missing event_context: $($file.Name) / $sampleId"
        }
        if ($columnNames -contains 'a_leg_quality' -and $aLegQuality -and $aLegQuality -notin ($allowedALegQualities + $legacyALegQualityAliases)) {
            Add-ValidationError "frozen contract row has invalid a_leg_quality (canonical or registered historical alias required): $($file.Name) / $sampleId"
        }
        if ($columnNames -contains 'b_leg_class' -and $bLegClass -and $bLegClass -notin ($allowedBLegClasses + $legacyBLegClassAliases)) {
            Add-ValidationError "frozen contract row has invalid b_leg_class (canonical or registered historical alias required): $($file.Name) / $sampleId"
        }
        if ($orderBranch -notin $allowedOrderBranches) {
            Add-ValidationError "frozen contract row has invalid order_branch: $($file.Name) / $sampleId"
        }
        if ($gapPolicy -notin $allowedGapPolicies) {
            Add-ValidationError "frozen contract row has invalid gap_policy: $($file.Name) / $sampleId"
        } elseif ($orderBranch -eq 'market_close' -and $gapPolicy -ne 'not_applicable') {
            Add-ValidationError "market_close requires gap_policy=not_applicable: $($file.Name) / $sampleId"
        } elseif ($orderBranch -ne 'market_close' -and $gapPolicy -eq 'not_applicable') {
            Add-ValidationError "non-market-close branch cannot use gap_policy=not_applicable: $($file.Name) / $sampleId"
        }
        if ($labelSource -ne 'human_chart_review') {
            Add-ValidationError "frozen contract row has invalid label_source: $($file.Name) / $sampleId"
        }
        if ($dailyContextWindow -ne '>=2y') {
            Add-ValidationError "frozen contract row requires daily_context_window=>=2y: $($file.Name) / $sampleId"
        }
        if ($majorHighLowReview -ne 'complete') {
            Add-ValidationError "frozen contract row requires major_high_low_review=complete: $($file.Name) / $sampleId"
        }
        if ($emaReview -ne 'complete') {
            Add-ValidationError "frozen contract row requires ema20_50_200_review=complete: $($file.Name) / $sampleId"
        }

        $numericValues = @{}
        foreach ($field in @('structural_stop', 'first_obstacle', 'target_price')) {
            $parsedValue = 0.0
            if (-not (Test-FiniteNumber -Value $row.PSObject.Properties[$field].Value -Number ([ref]$parsedValue))) {
                Add-ValidationError "frozen contract row has non-finite ${field}: $($file.Name) / $sampleId"
            } else {
                $numericValues[$field] = $parsedValue
            }
        }
        $entryReference = 0.0
        $entryText = Get-TrimmedText $row.entry_trigger
        $hasEntryReference = $false
        if ($orderBranch -ne 'market_close' -and [string]::IsNullOrWhiteSpace($entryText)) {
            Add-ValidationError "non-market-close branch requires entry_trigger: $($file.Name) / $sampleId"
        } elseif (-not [string]::IsNullOrWhiteSpace($entryText)) {
            if (-not (Test-FiniteNumber -Value $entryText -Number ([ref]$entryReference))) {
                Add-ValidationError "frozen contract row has non-finite entry_trigger: $($file.Name) / $sampleId"
            } else {
                $hasEntryReference = $true
            }
        }
        $maxHoldBars = 0.0
        if (-not (Test-FiniteNumber -Value $row.max_hold_bars -Number ([ref]$maxHoldBars)) -or
            $maxHoldBars -lt 1 -or $maxHoldBars -ne [math]::Truncate($maxHoldBars)) {
            Add-ValidationError "frozen contract row has invalid max_hold_bars: $($file.Name) / $sampleId"
        }
        if ($hasEntryReference -and $numericValues.ContainsKey('structural_stop') -and
            $numericValues.ContainsKey('first_obstacle') -and $numericValues.ContainsKey('target_price')) {
            if ($direction -eq 'long') {
                if ($numericValues['structural_stop'] -ge $entryReference) {
                    Add-ValidationError "long structural_stop must be below entry reference: $($file.Name) / $sampleId"
                }
                if ($numericValues['first_obstacle'] -le $entryReference) {
                    Add-ValidationError "long first_obstacle must be above entry reference: $($file.Name) / $sampleId"
                }
                if ($numericValues['target_price'] -le $entryReference) {
                    Add-ValidationError "long target_price must be above entry reference: $($file.Name) / $sampleId"
                }
            } elseif ($direction -eq 'short') {
                if ($numericValues['structural_stop'] -le $entryReference) {
                    Add-ValidationError "short structural_stop must be above entry reference: $($file.Name) / $sampleId"
                }
                if ($numericValues['first_obstacle'] -ge $entryReference) {
                    Add-ValidationError "short first_obstacle must be below entry reference: $($file.Name) / $sampleId"
                }
                if ($numericValues['target_price'] -ge $entryReference) {
                    Add-ValidationError "short target_price must be below entry reference: $($file.Name) / $sampleId"
                }
            }
        }
        if ($spaceStatus -and $spaceStatusLower -notin @($allowedSpaceStatuses | ForEach-Object { $_.ToLowerInvariant() })) {
            Add-ValidationError "frozen contract row has invalid space_status: $($file.Name) / $sampleId"
        }
        if ($contractState -notin $allowedContractStates) {
            Add-ValidationError "frozen contract row has invalid contract_state: $($file.Name) / $sampleId"
        }
        $spaceValue = 0.0
        $hasSpaceValue = -not [string]::IsNullOrWhiteSpace((Get-TrimmedText $row.pre_entry_space_R))
        if ($hasSpaceValue -and -not (Test-FiniteNumber -Value $row.pre_entry_space_R -Number ([ref]$spaceValue))) {
            Add-ValidationError "frozen contract row has non-finite pre_entry_space_R: $($file.Name) / $sampleId"
            $hasSpaceValue = $false
        }
        if ($spaceStatusLower -in @('strict_ge_1r', 'clearly_positive', 'blocked') -and -not $hasSpaceValue) {
            Add-ValidationError "explicit space_status requires pre_entry_space_R: $($file.Name) / $sampleId"
        }
        if ($spaceStatusLower -in @('strict_ge_1r', 'clearly_positive') -and $hasSpaceValue) {
            if ($spaceValue -lt 1) {
                Add-ValidationError "strict space_status is below 1R: $($file.Name) / $sampleId"
            }
        }
        if ($spaceStatusLower -eq 'blocked' -and $hasSpaceValue -and $spaceValue -gt 0) {
            Add-ValidationError "blocked space_status is above 0R: $($file.Name) / $sampleId"
        }

        if ($internalLabel -in @('H1', 'H2') -and $direction -ne 'long') {
            Add-ValidationError "H1/H2 direction mismatch: $($file.Name) / $sampleId"
        }
        if ($internalLabel -in @('L1', 'L2') -and $direction -ne 'short') {
            Add-ValidationError "L1/L2 direction mismatch: $($file.Name) / $sampleId"
        }
        if ($internalLabel -eq 'H3' -and ($direction -ne 'long' -or $primaryPattern -ne 'H3_L3')) {
            Add-ValidationError "H3 requires long direction and H3_L3 pattern: $($file.Name) / $sampleId"
        }
        if ($internalLabel -eq 'L3' -and ($direction -ne 'short' -or $primaryPattern -ne 'H3_L3')) {
            Add-ValidationError "L3 requires short direction and H3_L3 pattern: $($file.Name) / $sampleId"
        }
        if ($internalLabel -in @('H3', 'L3') -and $emaGate -ne 'not_applicable') {
            Add-ValidationError "H3/L3 requires EMA gate not_applicable: $($file.Name) / $sampleId"
        }
        if ($ema20Slope -and $ema20Slope -notin $allowedEmaSlopes) {
            Add-ValidationError "frozen contract row has invalid daily_ema20_slope: $($file.Name) / $sampleId"
        }
        if ($ema50Slope -and $ema50Slope -notin $allowedEmaSlopes) {
            Add-ValidationError "frozen contract row has invalid daily_ema50_slope: $($file.Name) / $sampleId"
        }
        if ($internalLabel -in @('H1', 'H2', 'L1', 'L2')) {
            if ([string]::IsNullOrWhiteSpace($pullbackLocation)) {
                Add-ValidationError "H/L row missing h_l_pullback_location: $($file.Name) / $sampleId"
            }
            if ($ema20Slope -notin $allowedEmaSlopes -or $ema50Slope -notin $allowedEmaSlopes) {
                Add-ValidationError "H/L row has invalid EMA slope: $($file.Name) / $sampleId"
            }
            if ($emaGate -notin $allowedEmaGates) {
                Add-ValidationError "H/L row has invalid EMA gate: $($file.Name) / $sampleId"
            }
            if ($emaGate -eq 'not_applicable') {
                Add-ValidationError "H/L row cannot use EMA gate not_applicable: $($file.Name) / $sampleId"
            }
            $expectedGate = if ($internalLabel -in @('H1', 'H2')) { 'long_pass' } else { 'short_pass' }
            $expectedSlope = if ($internalLabel -in @('H1', 'H2')) { 'up' } else { 'down' }
            if ($emaGate -in @('long_pass', 'short_pass') -and $emaGate -ne $expectedGate) {
                Add-ValidationError "H/L EMA pass gate does not match internal_label direction (requires $expectedGate): $($file.Name) / $sampleId"
            }
            if ($emaGate -eq $expectedGate -and ($ema20Slope -ne $expectedSlope -or $ema50Slope -ne $expectedSlope)) {
                Add-ValidationError "EMA pass gate does not match both EMA slopes: $($file.Name) / $sampleId"
            }
            if ($emaGate -eq 'fail_flat_or_opposite' -and $ema20Slope -eq $expectedSlope -and $ema50Slope -eq $expectedSlope) {
                Add-ValidationError "EMA fail gate has two passing slopes: $($file.Name) / $sampleId"
            }
            if ($emaGate -eq 'fail_flat_or_opposite' -and ($ema20Slope -eq 'unknown' -or $ema50Slope -eq 'unknown')) {
                Add-ValidationError "EMA fail gate cannot use unknown slope evidence; use pending: $($file.Name) / $sampleId"
            }
            if ($emaGate -eq 'pending' -and ($ema20Slope -ne 'unknown' -and $ema50Slope -ne 'unknown')) {
                Add-ValidationError "EMA pending gate lacks unknown slope evidence: $($file.Name) / $sampleId"
            }
        } elseif ($emaGate -and $emaGate -ne 'not_applicable') {
            Add-ValidationError "non-H/L row must leave EMA gate blank or not_applicable: $($file.Name) / $sampleId"
        }
        if ($metaConfluence -and $metaConfluence -notin $allowedMetaConfluence) {
            Add-ValidationError "frozen contract row has invalid meta_confluence: $($file.Name) / $sampleId"
        }
        if ($internalLabel -in @('H1', 'H2', 'L1', 'L2') -and [string]::IsNullOrWhiteSpace((Get-TrimmedText $row.meta_confluence))) {
            Add-ValidationError "H/L row missing meta_confluence: $($file.Name) / $sampleId"
        }
        if ($metaConfluence -eq 'present') {
            if ([string]::IsNullOrWhiteSpace((Get-TrimmedText $row.meta_zone))) {
                Add-ValidationError "meta_confluence=present requires meta_zone: $($file.Name) / $sampleId"
            }
            $metaComponents = @([regex]::Split((Get-TrimmedText $row.meta_components), '[;,|+]') | ForEach-Object {
                $component = ([string]$_).Trim().ToLowerInvariant()
                if ($component) { $component }
            } | Sort-Object -Unique)
            if ($metaComponents.Count -lt 2) {
                Add-ValidationError "meta_confluence=present requires two meta_components: $($file.Name) / $sampleId"
            }
        }
        if (($eventContext -match 'historical_event_filter_not_verified') -and
            ($eventContext -match 'ordinary_non_event')) {
            Add-ValidationError "event-unverified row is mislabeled ordinary_non_event: $($file.Name) / $sampleId"
        }
        if (($primaryPattern -eq 'H1_L1') -and ($internalLabel -notin @('H1', 'L1'))) {
            Add-ValidationError "H1_L1 mapping mismatch: $($file.Name) / $sampleId"
        }
        if (($primaryPattern -eq 'H2_L2') -and ($internalLabel -notin @('H2', 'L2'))) {
            Add-ValidationError "H2_L2 mapping mismatch: $($file.Name) / $sampleId"
        }
        if ($internalLabel -eq 'H3_L3') {
            Add-ValidationError "ambiguous combined H3_L3 internal label: $($file.Name) / $sampleId"
        }
        if (($primaryPattern -eq 'BOP') -and ($internalLabel -in @('H1', 'H2', 'L1', 'L2', 'H3', 'L3'))) {
            Add-ValidationError "BOP row mixes an internal PA label: $($file.Name) / $sampleId"
        }
        [void]$frozenContractRecords.Add([pscustomobject]@{
            file = $file.Name
            sample_id = $sampleId
            sample_id_key = $sampleId.ToLowerInvariant()
            symbol = $symbol
            decision_date = Get-CanonicalDateKey $decisionDate
            direction = $direction
            primary_pattern = $primaryPattern
            internal_label = $internalLabel
            lineage_id = $lineageId
            contract_family_key = @(
                $symbol.ToLowerInvariant(),
                $decisionDate.ToLowerInvariant(),
                $direction,
                $primaryPattern.ToLowerInvariant(),
                $internalLabel.ToLowerInvariant(),
                $lineageId.ToLowerInvariant()
            ) -join '|'
        })
    }
}
foreach ($duplicate in @($frozenContractRecords | Group-Object sample_id_key | Where-Object { $_.Name -and $_.Count -gt 1 })) {
    Add-ValidationError "duplicate frozen sample_id across contract CSVs: $($duplicate.Name)"
}
foreach ($duplicate in @($frozenContractRecords | Where-Object { $_.lineage_id } | Group-Object contract_family_key | Where-Object { $_.Count -gt 1 })) {
    Add-ValidationError "duplicate frozen contract family across contract CSVs: $($duplicate.Name)"
}

$selectionMarkdownFiles = @(Get-ChildItem -LiteralPath (Join-Path -Path $repoRoot -ChildPath 'research/backtesting') -File -Filter '*_selection_*.md')
$selectionPostOutcomeFieldPattern = '(?im)^\s*(?:entry_price|entry_date|exit_price|exit_date|exit_reason|bars_held|fill_status|trade_result|realized_R|win_rate_eligible|path_result|first_obstacle_hit|ambiguous_intrabar|gap_adjustment|evidence_status)\s*:'
$selectionOutcomeTablePattern = '(?im)^\s*\|[^\r\n]*(?:完成成交|是否成交|胜负|胜率)[^\r\n]*实现\s*R[^\r\n]*\|'
foreach ($file in $selectionMarkdownFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1)
    $content = Get-Utf8Text -Path $file.FullName
    if ($content -notmatch '(?i)frozen_pre_outcome') {
        Add-ValidationError "selection record missing frozen_pre_outcome status: $relativePath"
    }
    if ($content -notmatch '(?im)^\s*contract_scope:\s*historical_context_only\s*$') {
        Add-ValidationError "selection record missing historical_context_only scope: $relativePath"
    }
    if ($content -notmatch '(?im)^\s*timeframes_seen:\s*Daily\s*$') {
        Add-ValidationError "selection record is not explicitly Daily-only: $relativePath"
    }
    if ($content -match $selectionPostOutcomeFieldPattern) {
        Add-ValidationError "post-outcome field leaked into selection record: $relativePath"
    }
    if ($content -match '(?im)^\s*##\s+回放与统计状态\s*$') {
        Add-ValidationError "replay result section leaked into selection record: $relativePath"
    }
    if ($content -match $selectionOutcomeTablePattern) {
        Add-ValidationError "post-outcome table leaked into selection record: $relativePath"
    }
}

$candidateInventoryPath = Join-Path -Path $repoRoot -ChildPath 'strategy/pattern_inventory_candidates.md'
if (Test-Path -LiteralPath $candidateInventoryPath -PathType Leaf) {
    $candidateInventory = Get-Utf8Text -Path $candidateInventoryPath
    foreach ($legacyAlias in @('research_positive conditional', 'valid no-trade', 'research_positive_candidate')) {
        if ($candidateInventory.Contains($legacyAlias)) {
            Add-ValidationError "non-canonical status alias in candidate inventory: $legacyAlias"
        }
    }
    $candidateRows = @($candidateInventory -split '\r?\n' | Where-Object { $_ -match '^\| `VIS-' })
    if ($candidateRows.Count -eq 0) {
        Add-ValidationError 'candidate inventory has no visual candidate rows'
    }
    foreach ($candidateRow in $candidateRows) {
        $cells = @($candidateRow.Trim('|').Split('|') | ForEach-Object { $_.Trim() })
        if ($cells.Count -ne 5) {
            Add-ValidationError "candidate inventory direction table must have five columns: $candidateRow"
            continue
        }
        if ($cells[1] -notin @('long', 'short', 'no_valid_direction')) {
            Add-ValidationError "candidate inventory row has invalid direction '$($cells[1])': $candidateRow"
        }
    }
}

$activeRoots = @('docs', 'foundations', 'patterns', 'strategy') | ForEach-Object {
    Join-Path -Path $repoRoot -ChildPath $_
}
$activeMarkdownFiles = foreach ($root in $activeRoots) {
    Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.md'
}
foreach ($file in $activeMarkdownFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1)
    $content = Get-Utf8Text -Path $file.FullName
    if ($content -match '(?i)BOP-ABC|same_contract_stop') {
        Add-ValidationError "legacy pattern/status token in active contract: $relativePath"
    }
    if ($content -match '(?im)^\s*order_branch:\s*(stop|stop-limit|limit-retest|market-close|reverse-stop|observation-only)\b') {
        Add-ValidationError "legacy order_branch enum in active contract: $relativePath"
    }
}

if ($errors.Count -gt 0) {
    Write-Output "PA Research document validation failed: $($errors.Count) error(s); checked $($markdownFiles.Count) Markdown files and inspected $checkedLinks link targets (external targets skipped)."
    $errors | ForEach-Object { Write-Output "- $_" }
    exit 1
}

Write-Output "PA Research document validation passed: $($markdownFiles.Count) Markdown files, $checkedLinks links, canonical contracts and boundary checks OK."
Write-Output 'This validator is read-only documentation validation; it is not a market-data or quantitative scanner.'

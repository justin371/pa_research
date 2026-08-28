[CmdletBinding()]
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
    'research/backtesting/replay_outcome_denominator_audit_2026-08-29_CN.md',
    'research/backtesting/replay_lineage_independence_audit_2026-08-29_CN.md',
    'research/backtesting/replay_provenance_reproducibility_audit_2026-08-29_CN.md',
    'research/backtesting/frozen_contract_field_partition_audit_2026-08-29_CN.md',
    'research/backtesting/pre_entry_result_evidence_isolation_audit_2026-08-29_CN.md',
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
    'research/pattern_visual_preflight_audit_2026-08-29_CN.md',
    'research/pattern_case_entry_status_audit_2026-08-29_CN.md',
    'research/pattern_state_axis_field_enum_audit_2026-08-29_CN.md',
    'research/h_l_lineage_visual_boundary_audit_2026-08-24_CN.md',
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

$markdownFiles = Get-ChildItem -LiteralPath $repoRoot -Recurse -File -Filter '*.md' | Where-Object {
    $relative = $_.FullName.Substring($repoRoot.Length + 1)
    -not $relative.StartsWith('.codex' + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
}
foreach ($file in $markdownFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1)
    $content = Get-Content -LiteralPath $file.FullName -Raw

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
        'direction: long / short / no_valid_direction',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
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
        'gate_result:',
        'contract_scope:'
    )
    'docs/pa_research_daily_selection_rules_v0_1_CN.md' = @(
        'direction: long / short / no_valid_direction',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'event_bucket:',
        'bop_state:',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'gate_result:',
        'contract_scope:'
    )
    'docs/visual_pa_review_card_CN.md' = @(
        'direction: long / short / no_valid_direction',
        'state_transition: none / breakout_acceptance / role_reversal / failed_breakout / range_transition / MTR_candidate',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'gate_result:',
        'contract_scope:'
    )
    'docs/daily_candidate_review_card_CN.md' = @(
        'universe_coverage: complete / partial / discovery_only / unknown',
        'avg_20d_dollar_volume_usd:',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'event_bucket:',
        'daily_context_window: >=2y / <2y / unavailable',
        'major_high_low_review: complete / partial / unavailable',
        'h_l_ema_slope_gate:',
        'first_independent_obstacle:',
        'research_state:',
        'Execution Agent'
    )
    'patterns/08_three_push_h3_l3/README.md' = @(
        'attempt_direction: bullish_attempts / bearish_attempts',
        'canonical `direction`',
        'lineage_status: same_lineage / reset / unclear / pending',
        'context_timeframes_seen:',
        'event_bucket:',
        'space_status:',
        'trade_state:',
        'gate_result:',
        'handoff_status:'
    )
    'patterns/README.md' = @(
        'lineage_status / lineage_id / internal_label / range_edge_three_push',
        'daily_context_window / major_high_low_review / ema20_50_200_review',
        'signal_bar / confirmation_bar / new_trigger / follow_through',
        'structural_stop / structural_invalidation',
        'first_independent_obstacle / rough_space_to_first_obstacle_R / space_status / rough_R_R',
        'event_context / event_bucket / sector_state / market_state / permission / gate_result'
    )
    'patterns/07_mtr_reversal/README.md' = @(
        'mtr_state: reversal_attempt / mtr_candidate / mtr_confirmed_for_research / failed_mtr_thesis',
        'thesis_state: working / failed / invalidated / replaced / pending'
    )
    'research/h_l_lineage_visual_boundary_audit_2026-08-24_CN.md' = @(
        'direction: long / short / no_valid_direction',
        'parent_state: open_trend / trading_range / range_edge / transition / climax / unclear',
        'lineage_status: same_lineage / reset / unclear / pending',
        'lineage_id:'
    )
}
foreach ($entry in $canonicalChecks.GetEnumerator()) {
    $absolutePath = Join-Path -Path $repoRoot -ChildPath ($entry.Key -replace '/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
    $content = Get-Content -LiteralPath $absolutePath -Raw
    foreach ($token in $entry.Value) {
        if (-not $content.Contains($token)) {
            Add-ValidationError "missing canonical token '$token': $($entry.Key)"
        }
    }
}

$patternCaseEntryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_case_entry_status_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternCaseEntryAuditPath -PathType Leaf) {
    $patternCaseEntryAuditContent = Get-Content -LiteralPath $patternCaseEntryAuditPath -Raw
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
    $patternStateAxisAuditContent = Get-Content -LiteralPath $patternStateAxisAuditPath -Raw
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
    $content = Get-Content -LiteralPath $absolutePath -Raw
    if ($content -match '(?<![\w-])valid(?:-| )no-trade(?![\w-])') {
        Add-ValidationError "legacy valid-no-trade status alias in active pattern README: $relativePath"
    }
    if ($content -match '(?i)(?<![\w-])observation-only(?![\w-])') {
        Add-ValidationError "legacy observation-only status alias in active pattern README: $relativePath"
    }
    if ($content -match '(?<![A-Za-z_])no_trade(?![A-Za-z_])') {
        Add-ValidationError "legacy no_trade status alias in active pattern README: $relativePath"
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
    $content = Get-Content -LiteralPath $absolutePath -Raw
    if ($content -notmatch '(?m)^order_branch:.*\bstop_limit\b') {
        Add-ValidationError "core pattern order_branch omits research stop_limit: $relativePath"
    }
}

$rangeEdgeReadmePath = Join-Path -Path $repoRoot -ChildPath 'patterns/04_range_edge_second_entry/README.md'
if (Test-Path -LiteralPath $rangeEdgeReadmePath -PathType Leaf) {
    $rangeEdgeReadmeContent = Get-Content -LiteralPath $rangeEdgeReadmePath -Raw
    if ($rangeEdgeReadmeContent -notmatch 'IWM 2024-04-17' -or
        $rangeEdgeReadmeContent -notmatch 'range_edge_second_entry_framework_CN\.md') {
        Add-ValidationError 'IWM range-edge case is missing its framework entry link'
    }
}

$researchReadmePath = Join-Path -Path $repoRoot -ChildPath 'research/README.md'
if (Test-Path -LiteralPath $researchReadmePath -PathType Leaf) {
    $researchReadmeContent = Get-Content -LiteralPath $researchReadmePath -Raw
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
    $freezeReviewContent = Get-Content -LiteralPath $freezeReviewPath -Raw
    foreach ($token in @('NFLX', 'TSM', 'contract_frozen=no', 'no-new-positive', 'max_hold_bars', 'do_not_replay')) {
        if (-not $freezeReviewContent.Contains($token)) {
            Add-ValidationError "missing ABC/BOP freeze-review token '$token'"
        }
    }
}

$bullishCandidateAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/abc_bullish_candidate_contract_audit_2026-08-28_CN.md'
if (Test-Path -LiteralPath $bullishCandidateAuditPath -PathType Leaf) {
    $bullishCandidateAuditContent = Get-Content -LiteralPath $bullishCandidateAuditPath -Raw
    foreach ($token in @('V', 'NVDA', 'KLAC', 'CRWD', 'contract_frozen=no', 'no-new-positive', 'max_hold_bars', 'ABC_CONT')) {
        if (-not $bullishCandidateAuditContent.Contains($token)) {
            Add-ValidationError "missing bullish ABC candidate-audit token '$token'"
        }
    }
}

$crossPatternAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/cross_pattern_statistics_isolation_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $crossPatternAuditPath -PathType Leaf) {
    $crossPatternAuditContent = Get-Content -LiteralPath $crossPatternAuditPath -Raw
    foreach ($token in @('ABC_CONT', 'BOP', 'H1', 'H2', 'L1', 'L2', 'H3', 'L3', 'lineage_id', 'no-new-positive')) {
        if (-not $crossPatternAuditContent.Contains($token)) {
            Add-ValidationError "missing cross-pattern isolation-audit token '$token'"
        }
    }
}

$eventSpaceAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/event_space_eligibility_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $eventSpaceAuditPath -PathType Leaf) {
    $eventSpaceAuditContent = Get-Content -LiteralPath $eventSpaceAuditPath -Raw
    foreach ($token in @('event_bucket', 'ordinary_non_event', 'event_unverified_or_pending', 'space_status', 'unknown_contract_space', 'strict_ge_1R', 'no-new-positive')) {
        if (-not $eventSpaceAuditContent.Contains($token)) {
            Add-ValidationError "missing event/space eligibility-audit token '$token'"
        }
    }
}

$replayOutcomeAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/replay_outcome_denominator_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $replayOutcomeAuditPath -PathType Leaf) {
    $replayOutcomeAuditContent = Get-Content -LiteralPath $replayOutcomeAuditPath -Raw
    foreach ($token in @('win_rate_eligible', 'completed_trade_count', 'incomplete-horizon', 'opening-skip', 'ambiguous_intrabar', 'first_obstacle_hit', 'realized_R', 'max_hold_bars', 'no-new-positive')) {
        if (-not $replayOutcomeAuditContent.Contains($token)) {
            Add-ValidationError "missing replay outcome-audit token '$token'"
        }
    }
}

$replayLineageAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/replay_lineage_independence_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $replayLineageAuditPath -PathType Leaf) {
    $replayLineageAuditContent = Get-Content -LiteralPath $replayLineageAuditPath -Raw
    foreach ($token in @('lineage_id', 'market_context_id', 'duplicate_result', 'sample_id', 'results.csv', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $replayLineageAuditContent.Contains($token)) {
            Add-ValidationError "missing replay lineage-independence-audit token '$token'"
        }
    }
}

$replayProvenanceAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/replay_provenance_reproducibility_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $replayProvenanceAuditPath -PathType Leaf) {
    $replayProvenanceAuditContent = Get-Content -LiteralPath $replayProvenanceAuditPath -Raw
    foreach ($token in @('engine_version', 'engine_source_sha256', 'results_file_sha256', 'replay2', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $replayProvenanceAuditContent.Contains($token)) {
            Add-ValidationError "missing replay provenance-reproducibility-audit token '$token'"
        }
    }
}

$frozenContractFieldAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/frozen_contract_field_partition_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $frozenContractFieldAuditPath -PathType Leaf) {
    $frozenContractFieldAuditContent = Get-Content -LiteralPath $frozenContractFieldAuditPath -Raw
    foreach ($token in @('hl_contracts_2026-08-26.csv', 'contract_state', 'space_status', 'strict_ge_1R', 'observation-only', 'ABC_CONT', 'BOP', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $frozenContractFieldAuditContent.Contains($token)) {
            Add-ValidationError "missing frozen-contract-field-audit token '$token'"
        }
    }
}

$preEntryResultIsolationAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/pre_entry_result_evidence_isolation_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $preEntryResultIsolationAuditPath -PathType Leaf) {
    $preEntryResultIsolationAuditContent = Get-Content -LiteralPath $preEntryResultIsolationAuditPath -Raw
    foreach ($token in @('event_context', 'pre_entry_space_R', 'pre_entry_provenance_status', 'pre_entry_provenance_incomplete', 'first_obstacle_hit', 'realized_R', 'contract_eligibility_mismatch_count', 'event_bucket_mismatch_count', 'contract_space_bucket_mismatch_count', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $preEntryResultIsolationAuditContent.Contains($token)) {
            Add-ValidationError "missing pre-entry/result-isolation-audit token '$token'"
        }
    }
}

$legacyResultProvenanceAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/legacy_result_provenance_completeness_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $legacyResultProvenanceAuditPath -PathType Leaf) {
    $legacyResultProvenanceAuditContent = Get-Content -LiteralPath $legacyResultProvenanceAuditPath -Raw
    foreach ($token in @('pre_entry_provenance_status', 'pre_entry_provenance_missing_fields', 'completed_trade_count', 'pre_entry_provenance_incomplete', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $legacyResultProvenanceAuditContent.Contains($token)) {
            Add-ValidationError "missing legacy-result-provenance-audit token '$token'"
        }
    }
}

$artifactSchemaRoundtripAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/artifact_schema_roundtrip_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $artifactSchemaRoundtripAuditPath -PathType Leaf) {
    $artifactSchemaRoundtripAuditContent = Get-Content -LiteralPath $artifactSchemaRoundtripAuditPath -Raw
    foreach ($token in @('results.csv', 'summary.json', 'run_metadata.json', 'summary_provenance', 'result_columns', 'pre_entry_provenance_status', 'contract_eligibility_mismatch_count', 'event_bucket_mismatch_count', 'contract_space_bucket_mismatch_count', 'historical', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $artifactSchemaRoundtripAuditContent.Contains($token)) {
            Add-ValidationError "missing artifact-schema-roundtrip-audit token '$token'"
        }
    }
}

$historicalReplayResultLogAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/historical_replay_result_log_provenance_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $historicalReplayResultLogAuditPath -PathType Leaf) {
    $historicalReplayResultLogAuditContent = Get-Content -LiteralPath $historicalReplayResultLogAuditPath -Raw
    foreach ($token in @('external_results_files=13', 'external_result_rows=88', 'unique_sample_ids=63', 'duplicate_sample_id_groups=13', 'rows_in_duplicate_groups=38', 'extra_duplicate_rows=25', 'current_valid=0', 'historical_incomplete=13', 'invalid=0', 'historical_exit_code=2', 'journal/', 'trade_log/', 'transaction/', 'ledger/', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $historicalReplayResultLogAuditContent.Contains($token)) {
            Add-ValidationError "missing historical replay/result-log provenance audit token '$token'"
        }
    }
}

$unifiedOutputStateAxisAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/unified_output_state_axis_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $unifiedOutputStateAxisAuditPath -PathType Leaf) {
    $unifiedOutputStateAxisAuditContent = Get-Content -LiteralPath $unifiedOutputStateAxisAuditPath -Raw
    foreach ($token in @('document_maturity', 'attempt_direction', 'Daily', '4H', '15m', 'lineage_id', 'event_bucket', 'space_status', 'no-new-positive', 'validated win-rate: not-computable')) {
        if (-not $unifiedOutputStateAxisAuditContent.Contains($token)) {
            Add-ValidationError "missing unified-output state-axis audit token '$token'"
        }
    }
}

$patternIndexAliasBoundaryAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_index_alias_boundary_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternIndexAliasBoundaryAuditPath -PathType Leaf) {
    $patternIndexAliasBoundaryAuditContent = Get-Content -LiteralPath $patternIndexAliasBoundaryAuditPath -Raw
    foreach ($token in @('01_h1_l1_first_entry', '02_h2_l2_second_entry', '03_abc_continuation', '04_range_edge_second_entry', '05_failed_breakout_climax', '06_breakout_pullback_bop', '07_mtr_reversal', '08_three_push_h3_l3', '09_vcp_minervini', '10_final_flag', '11_opening_reversal', '12_channel', '13_inside_bar_two_bar_reversal', '14_triangle_expanding_range', '15_double_top_bottom', '16_head_shoulders_rounded', 'primary_pattern: ABC_CONT', 'internal_label=H1 / L1', 'internal_label=H2 / L2', 'internal_label=H3 / L3', 'state_transition', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only', 'no Codex Trading', 'no quantitative scanner', 'no Execution Agent')) {
        if (-not $patternIndexAliasBoundaryAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern-index-alias-boundary-audit token '$token'"
        }
    }
}

$patternVisualPreflightAuditPath = Join-Path -Path $repoRoot -ChildPath 'research/pattern_visual_preflight_audit_2026-08-29_CN.md'
if (Test-Path -LiteralPath $patternVisualPreflightAuditPath -PathType Leaf) {
    $patternVisualPreflightAuditContent = Get-Content -LiteralPath $patternVisualPreflightAuditPath -Raw
    foreach ($token in @('daily_context_window: >=2y / <2y / unavailable', 'major_highs', 'major_lows', 'daily_ema20_50_200', 'A_quality: strong', 'B_quality: controlled', 'first_independent_obstacle', 'no-new-positive', 'validated win-rate: not-computable', 'PA Research only', 'no Codex Trading', 'no quantitative scanner', 'no Execution Agent')) {
        if (-not $patternVisualPreflightAuditContent.Contains($token)) {
            Add-ValidationError "missing pattern-visual-preflight-audit token '$token'"
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
$allowedContractStates = @('', 'frozen_pre_outcome')
$allowedOrderBranches = @('stop_confirmation', 'limit_retest', 'market_close')
$allowedGapPolicies = @('accept_open', 'skip', 'flag_only', 'not_applicable')
$allowedMetaConfluence = @('present', 'absent', 'unknown')
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
            if ($emaGate -eq $expectedGate -and ($ema20Slope -ne $expectedSlope -or $ema50Slope -ne $expectedSlope)) {
                Add-ValidationError "EMA pass gate does not match both EMA slopes: $($file.Name) / $sampleId"
            }
            if ($emaGate -eq 'fail_flat_or_opposite' -and $ema20Slope -eq $expectedSlope -and $ema50Slope -eq $expectedSlope) {
                Add-ValidationError "EMA fail gate has two passing slopes: $($file.Name) / $sampleId"
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

$activeRoots = @('docs', 'foundations', 'patterns', 'strategy') | ForEach-Object {
    Join-Path -Path $repoRoot -ChildPath $_
}
$activeMarkdownFiles = foreach ($root in $activeRoots) {
    Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.md'
}
foreach ($file in $activeMarkdownFiles) {
    $relativePath = $file.FullName.Substring($repoRoot.Length + 1)
    $content = Get-Content -LiteralPath $file.FullName -Raw
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

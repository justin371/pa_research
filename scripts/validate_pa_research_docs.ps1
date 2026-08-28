[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$errors = [System.Collections.Generic.List[string]]::new()
$checkedLinks = 0

function Add-ValidationError {
    param([Parameter(Mandatory)][string]$Message)
    [void]$errors.Add($Message)
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
    'research/backtesting/bop_contract_intake_2026-08-28.csv',
    'research/backtesting/bop_contract_intake_audit_2026-08-28_CN.md',
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
        'direction: long / short / no_valid_direction',
        'internal_label: H1 / H2 / L1 / L2 / H3 / L3 / none / pending',
        'event_bucket:',
        'win_rate_eligible:',
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

$intakePath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/abc_bop_contract_intake_2026-08-28.csv'
if (Test-Path -LiteralPath $intakePath -PathType Leaf) {
    $intakeRows = @(Import-Csv -LiteralPath $intakePath)
    $requiredIntakeColumns = @(
        'intake_id', 'symbol', 'source_case', 'decision_date', 'direction',
        'primary_pattern', 'intake_state', 'contract_frozen', 'event_state',
        'trigger_evidence', 'structural_stop_evidence', 'first_obstacle_evidence',
        'missing_fields', 'freeze_recommendation'
    )
    if ($intakeRows.Count -eq 0) {
        Add-ValidationError 'ABC/BOP intake CSV has no rows'
    } else {
        $intakePropertyNames = @($intakeRows[0].PSObject.Properties.Name)
        foreach ($column in $requiredIntakeColumns) {
            if ($column -notin $intakePropertyNames) {
                Add-ValidationError "missing ABC/BOP intake column '$column'"
            }
        }
        foreach ($row in $intakeRows) {
            if ($row.contract_frozen -ne 'no') {
                Add-ValidationError "ABC/BOP intake row is not marked contract_frozen=no: $($row.intake_id)"
            }
            if ([string]::IsNullOrWhiteSpace($row.source_case)) {
                Add-ValidationError "ABC/BOP intake row missing source_case: $($row.intake_id)"
            }
            if ([string]::IsNullOrWhiteSpace($row.missing_fields)) {
                Add-ValidationError "ABC/BOP intake row missing missing_fields: $($row.intake_id)"
            }
        }
    }
}

$bopIntakePath = Join-Path -Path $repoRoot -ChildPath 'research/backtesting/bop_contract_intake_2026-08-28.csv'
if (Test-Path -LiteralPath $bopIntakePath -PathType Leaf) {
    $bopRows = @(Import-Csv -LiteralPath $bopIntakePath)
    $requiredBopColumns = @(
        'intake_id', 'symbol', 'source_case', 'decision_date', 'direction',
        'classification', 'bop_state', 'retest_class', 'order_branch',
        'contract_frozen', 'event_state', 'missing_fields', 'freeze_recommendation'
    )
    if ($bopRows.Count -eq 0) {
        Add-ValidationError 'BOP intake CSV has no rows'
    } else {
        $bopPropertyNames = @($bopRows[0].PSObject.Properties.Name)
        foreach ($column in $requiredBopColumns) {
            if ($column -notin $bopPropertyNames) {
                Add-ValidationError "missing BOP intake column '$column'"
            }
        }
        foreach ($row in $bopRows) {
            if ($row.contract_frozen -ne 'no') {
                Add-ValidationError "BOP intake row is not marked contract_frozen=no: $($row.intake_id)"
            }
            if ([string]::IsNullOrWhiteSpace($row.source_case)) {
                Add-ValidationError "BOP intake row missing source_case: $($row.intake_id)"
            }
            if ([string]::IsNullOrWhiteSpace($row.missing_fields)) {
                Add-ValidationError "BOP intake row missing missing_fields: $($row.intake_id)"
            }
            if ($row.retest_class -eq 'multi-day' -or $row.classification -eq 'multi_day_bop_positive') {
                Add-ValidationError "BOP intake row claims a multi-day positive without a frozen contract: $($row.intake_id)"
            }
        }
    }
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
foreach ($file in $frozenContractFiles) {
    $rows = @(Import-Csv -LiteralPath $file.FullName)
    if ($rows.Count -eq 0) {
        Add-ValidationError "frozen contract CSV has no rows: $($file.Name)"
        continue
    }
    $columnNames = @($rows[0].PSObject.Properties.Name)
    foreach ($column in @('sample_id', 'symbol', 'decision_date', 'direction', 'primary_pattern', 'internal_label', 'contract_frozen', 'lineage_id')) {
        if ($column -notin $columnNames) {
            Add-ValidationError "missing frozen contract column '$column': $($file.Name)"
        }
    }
    foreach ($row in $rows) {
        $sampleId = ([string]$row.sample_id).Trim()
        $symbol = ([string]$row.symbol).Trim()
        $decisionDate = ([string]$row.decision_date).Trim()
        $direction = ([string]$row.direction).Trim().ToLowerInvariant()
        $primaryPattern = ([string]$row.primary_pattern).Trim().ToUpperInvariant()
        if ($primaryPattern -eq 'OTHER') {
            $primaryPattern = 'other'
        }
        $internalLabel = ([string]$row.internal_label).Trim()
        $lineageId = ([string]$row.lineage_id).Trim()
        $spaceStatus = ([string]$row.space_status).Trim()
        $spaceStatusLower = $spaceStatus.ToLowerInvariant()
        $ema20Slope = ([string]$row.daily_ema20_slope).Trim().ToLowerInvariant()
        $ema50Slope = ([string]$row.daily_ema50_slope).Trim().ToLowerInvariant()
        $emaGate = ([string]$row.h_l_ema_slope_gate).Trim().ToLowerInvariant()
        $contractState = ([string]$row.contract_state).Trim().ToLowerInvariant()

        if (([string]$row.contract_frozen).Trim().ToLowerInvariant() -ne 'yes') {
            Add-ValidationError "non-frozen row in frozen contract CSV: $($file.Name) / $sampleId"
        }
        if ([string]::IsNullOrWhiteSpace($sampleId) -or [string]::IsNullOrWhiteSpace($symbol) -or [string]::IsNullOrWhiteSpace($decisionDate)) {
            Add-ValidationError "frozen contract row missing identity field: $($file.Name) / $sampleId"
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
        if ([string]::IsNullOrWhiteSpace($row.event_context)) {
            Add-ValidationError "frozen contract row missing event_context: $($file.Name) / $sampleId"
        }
        if ($spaceStatus -and $spaceStatusLower -notin @($allowedSpaceStatuses | ForEach-Object { $_.ToLowerInvariant() })) {
            Add-ValidationError "frozen contract row has invalid space_status: $($file.Name) / $sampleId"
        }
        if ($contractState -notin $allowedContractStates) {
            Add-ValidationError "frozen contract row has invalid contract_state: $($file.Name) / $sampleId"
        }
        $spaceValue = 0.0
        $hasSpaceValue = -not [string]::IsNullOrWhiteSpace($row.pre_entry_space_R)
        if ($hasSpaceValue -and -not [double]::TryParse([string]$row.pre_entry_space_R, [ref]$spaceValue)) {
            Add-ValidationError "frozen contract row has non-numeric pre_entry_space_R: $($file.Name) / $sampleId"
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
        if ($internalLabel -in @('H1', 'H2', 'L1', 'L2')) {
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
        if (([string]$row.event_context -match 'historical_event_filter_not_verified') -and
            ([string]$row.event_context -match 'ordinary_non_event')) {
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
            decision_date = $decisionDate
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

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
        'bop_state:',
        'order_branch: stop_confirmation / limit_retest / market_close / stop_limit / observation_only',
        'gate_result:',
        'contract_scope:'
    )
    'docs/pa_research_daily_selection_rules_v0_1_CN.md' = @(
        'direction: long / short / no_valid_direction',
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

[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter()]
    [string]$SourcePath = (Join-Path $PSScriptRoot "..\src\codex-keybindings.json"),

    [Parameter()]
    [string]$TargetPath = (Join-Path ([Environment]::GetFolderPath("UserProfile")) ".codex\keybindings.json"),

    [Parameter()]
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Read-KeybindingArray {
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [string]$Description
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Description file was not found: $Path"
    }

    $content = Get-Content -LiteralPath $Path -Raw
    if ([string]::IsNullOrWhiteSpace($content)) {
        throw "$Description file is empty: $Path"
    }

    try {
        $items = @(ConvertFrom-Json -InputObject $content)
    }
    catch {
        throw "$Description file is not valid JSON: $Path`n$($_.Exception.Message)"
    }

    foreach ($item in $items) {
        if (-not $item.command -or -not $item.key) {
            throw "$Description contains an entry without both 'command' and 'key': $Path"
        }
    }

    return $items
}

$source = Read-KeybindingArray -Path $SourcePath -Description "Source keybindings"
$duplicateCommands = @($source | Group-Object command | Where-Object Count -gt 1)
$duplicateKeys = @($source | Group-Object key | Where-Object Count -gt 1)
if ($duplicateCommands.Count -gt 0) {
    throw "Source keybindings contain duplicate command IDs: $($duplicateCommands.Name -join ', ')"
}
if ($duplicateKeys.Count -gt 0) {
    throw "Source keybindings contain duplicate shortcuts: $($duplicateKeys.Name -join ', ')"
}

$existing = @()
$targetExists = Test-Path -LiteralPath $TargetPath -PathType Leaf
if ($targetExists) {
    $existing = Read-KeybindingArray -Path $TargetPath -Description "Existing Codex keybindings"
}

$managedCommands = @($source | ForEach-Object { $_.command })
$managedKeys = @($source | ForEach-Object { $_.key })
$unmanaged = @($existing | Where-Object { $_.command -notin $managedCommands })
$conflicts = @($unmanaged | Where-Object { $_.key -in $managedKeys })
if ($conflicts.Count -gt 0 -and -not $Force) {
    $details = $conflicts | ForEach-Object { "  $($_.key) is already assigned to $($_.command)" }
    throw "Shortcut conflicts were found. Resolve them or rerun with -Force to replace the conflicting entries:`n$($details -join "`n")"
}
if ($Force) {
    $unmanaged = @($unmanaged | Where-Object { $_.key -notin $managedKeys })
}

$merged = @($unmanaged) + @($source)
$json = ConvertTo-Json -InputObject @($merged) -Depth 10
$targetDirectory = Split-Path -Parent $TargetPath
$backupPath = $null

if ($PSCmdlet.ShouldProcess($TargetPath, "Merge Codex keyboard shortcuts")) {
    [System.IO.Directory]::CreateDirectory($targetDirectory) | Out-Null

    if ($targetExists) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backupPath = "$TargetPath.backup-$stamp"
        Copy-Item -LiteralPath $TargetPath -Destination $backupPath
    }

    $tempPath = Join-Path $targetDirectory ("keybindings.{0}.tmp" -f [Guid]::NewGuid().ToString("N"))
    try {
        $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
        [System.IO.File]::WriteAllText($tempPath, "$json`n", $utf8NoBom)
        $null = Read-KeybindingArray -Path $tempPath -Description "Generated keybindings"
        Move-Item -LiteralPath $tempPath -Destination $TargetPath -Force
    }
    finally {
        if (Test-Path -LiteralPath $tempPath) {
            Remove-Item -LiteralPath $tempPath -Force
        }
    }

    $installed = Read-KeybindingArray -Path $TargetPath -Description "Installed Codex keybindings"
    foreach ($binding in $source) {
        $match = @($installed | Where-Object { $_.command -eq $binding.command -and $_.key -eq $binding.key })
        if ($match.Count -ne 1) {
            throw "Verification failed for $($binding.command) at $TargetPath"
        }
    }
}

[PSCustomObject]@{
    TargetPath = $TargetPath
    ManagedBindings = $source.Count
    PreservedBindings = $unmanaged.Count
    BackupPath = $backupPath
    RestartCodexRequired = $true
}

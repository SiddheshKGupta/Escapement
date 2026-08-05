param(
    [Parameter(Mandatory=$true)]
    [string]$EventName
)

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Python = $env:ESCAPEMENT_PYTHON

if (-not $Python) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 (Join-Path $Root "scripts\agent_runtime.py") $EventName
        exit $LASTEXITCODE
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        & python (Join-Path $Root "scripts\agent_runtime.py") $EventName
        exit $LASTEXITCODE
    }
    Write-Error "Escapement requires Python 3.10+."
    exit 127
}

& $Python (Join-Path $Root "scripts\agent_runtime.py") $EventName
exit $LASTEXITCODE

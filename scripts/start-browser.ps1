param([switch]$NoOpen, [int]$Port = 8791)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$webRoot = [IO.Path]::GetFullPath((Join-Path $root 'dist\browser'))
$serverScript = Join-Path $PSScriptRoot 'serve-web.mjs'
if (-not (Test-Path -LiteralPath (Join-Path $webRoot 'index.pck'))) { throw 'Browser build missing. Run scripts\build-browser.ps1 first.' }
$nodeCommand = Get-Command node.exe -ErrorAction SilentlyContinue
$nodeExe = if ($nodeCommand) { $nodeCommand.Source } elseif (Test-Path -LiteralPath 'D:\node\node.exe') { 'D:\node\node.exe' } else { throw 'Node.js is required to start the local web server.' }
$url = "http://127.0.0.1:$Port/"
function Read-Health {
    try { Invoke-RestMethod -Uri ($url + '__health') -TimeoutSec 2 } catch { $null }
}
$health = Read-Health
if ($health) {
    if ($health.app -ne 'tianxia-wuzhu' -or $health.root -ne $webRoot) {
        throw "Port $Port is used by another server or another build. Close that server first; existing browser saves stay at this address."
    }
} else {
    $logRoot = Join-Path $root '.runtime\browser-server'
    New-Item -ItemType Directory -Force -Path $logRoot | Out-Null
    $service = Start-Process -FilePath $nodeExe -ArgumentList @(('"' + $serverScript + '"'),'--root',('"' + $webRoot + '"'),'--port',$Port) -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logRoot 'stdout.log') -RedirectStandardError (Join-Path $logRoot 'stderr.log') -PassThru
    $service.Id | Set-Content -LiteralPath (Join-Path $logRoot 'server.pid')
    for ($attempt=0; $attempt -lt 30; $attempt++) {
        Start-Sleep -Milliseconds 200
        $health = Read-Health
        if ($health -and $health.app -eq 'tianxia-wuzhu' -and $health.root -eq $webRoot) { break }
        if ($service.HasExited) { throw "Web server exited. See $logRoot\stderr.log" }
    }
    if (-not $health -or $health.root -ne $webRoot) { throw 'The local game server did not become ready.' }
}
Write-Output "天下无主：$url"
if (-not $NoOpen) { Start-Process $url }

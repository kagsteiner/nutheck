param([string]$MSBuildPath = 'C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (Test-Path -LiteralPath (Join-Path $projectRoot 'Saved\NetHack')) {
    & (Join-Path $PSScriptRoot 'BackupNetHackSaves.ps1') -Reason 'Before rebuilding/replacing the native backend'
}
$solution = Join-Path $projectRoot 'upstream\NetHack\sys\windows\vs\NetHack.sln'
& $MSBuildPath $solution /m /t:NetHack /p:Configuration=Release /p:Platform=x64 /v:minimal
if ($LASTEXITCODE -ne 0) { throw "NetHack bridge build failed: $LASTEXITCODE" }
$source = Join-Path $projectRoot 'upstream\NetHack\binary\Release\x64'
$destination = Join-Path $projectRoot 'Binaries\NetHack'
New-Item -ItemType Directory -Force $destination | Out-Null
foreach ($name in @('nhdat500','license','Guidebook.txt','nethack.txt','opthelp','symbols.template','sysconf.template','nethackrc.template')) {
    Copy-Item -LiteralPath (Join-Path $source $name) -Destination $destination
}
Copy-Item -LiteralPath (Join-Path $source 'NetHack.exe') -Destination (Join-Path $destination 'NetHackBridge.exe')
Write-Output "NetHack bridge staged in $destination"

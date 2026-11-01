param([string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
& (Join-Path $PSScriptRoot 'BuildNetHackBridge.ps1')
$project = Join-Path $projectRoot 'nUthEck.uproject'
$build = Join-Path $EngineRoot 'Engine\Build\BatchFiles\Build.bat'
& $build NUthEckEditor Win64 Development "-Project=$project" -WaitMutex -NoHotReloadFromIDE
if ($LASTEXITCODE -ne 0) { throw "Unreal build failed: $LASTEXITCODE" }
$editor = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$assets = Join-Path $PSScriptRoot 'CreatePrototypeAssets.py'
& $editor $project "-ExecutePythonScript=$assets" -unattended -NullRHI -nosound -nop4
if ($LASTEXITCODE -ne 0) { throw "Prototype asset generation failed: $LASTEXITCODE" }
& (Join-Path $PSScriptRoot 'BuildDefaultTiles.ps1') -EngineRoot $EngineRoot -AssetsOnly -SkipGalleryRender

param(
    [string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7',
    [string]$Blender='C:\Program Files\Blender Foundation\Blender 5.2\blender.exe',
    [switch]$AssetsOnly,
    [switch]$SkipGalleryRender
)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$blenderArgs=@('--background','--threads','4','--python',(Join-Path $PSScriptRoot 'CreateDefaultTileFigures.py'))
if($SkipGalleryRender){$blenderArgs+=@('--','--no-render')}
& $Blender @blenderArgs
if($LASTEXITCODE -ne 0){throw 'Default tile figure generation failed'}
$project=Join-Path $projectRoot 'nUthEck.uproject'
if(!$AssetsOnly){
    & (Join-Path $PSScriptRoot 'BuildNetHackBridge.ps1')
    & (Join-Path $EngineRoot 'Engine\Build\BatchFiles\Build.bat') NUthEckEditor Win64 Development "-Project=$project" -WaitMutex -NoHotReloadFromIDE
    if($LASTEXITCODE -ne 0){throw 'Unreal build failed'}
}
$importLog=Join-Path $projectRoot ('Saved\Logs\DefaultTileImport-'+[guid]::NewGuid().ToString('N')+'.log')
$importScript=Join-Path $PSScriptRoot 'ImportDefaultTileFigures.py'
$importArgs=@(('"'+$project+'"'),('-ExecutePythonScript="'+$importScript+'"'),'-unattended','-nosound','-nop4','-NoSplash',('-abslog="'+$importLog+'"'))
$process=Start-Process -FilePath (Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe') -ArgumentList $importArgs -WindowStyle Hidden -PassThru -Wait
$importText=Get-Content -LiteralPath $importLog -Raw
if($process.ExitCode -ne 0 -or !$importText.Contains('DEFAULT_TILES_IMPORT_READY') -or $importText.Contains('Fatal error:')){throw "Default tile import failed: $importLog"}
Write-Output 'Default tile figures ready. Run Scripts/LaunchPrototype.ps1 -NewGame.'

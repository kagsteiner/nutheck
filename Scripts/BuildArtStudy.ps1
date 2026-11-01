param(
    [string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7',
    [string]$Blender='C:\Program Files\Blender Foundation\Blender 5.2\blender.exe',
    [switch]$SkipBlenderRender
)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$blenderArgs=@('--background','--threads','4','--python',(Join-Path $PSScriptRoot 'CreateArtStudy.py'))
if($SkipBlenderRender){$blenderArgs+=@('--','--no-render')}
& $Blender @blenderArgs
if($LASTEXITCODE -ne 0){throw 'Blender study export failed'}
$project=Join-Path $projectRoot 'nUthEck.uproject'
& (Join-Path $EngineRoot 'Engine\Build\BatchFiles\Build.bat') NUthEckEditor Win64 Development "-Project=$project" -WaitMutex -NoHotReloadFromIDE
if($LASTEXITCODE -ne 0){throw 'Unreal study build failed'}
$importLog=Join-Path $projectRoot ('Saved\Logs\ArtImport-'+[guid]::NewGuid().ToString('N')+'.log')
$importScript=Join-Path $PSScriptRoot 'ImportArtStudy.py'
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$importArgs=@(('"'+$project+'"'),('-ExecutePythonScript="'+$importScript+'"'),'-unattended','-nosound','-nop4','-NoSplash',('-abslog="'+$importLog+'"'))
$importProcess=Start-Process -FilePath $editor -ArgumentList $importArgs -WindowStyle Hidden -PassThru -Wait
$importText=Get-Content -LiteralPath $importLog -Raw
if($importProcess.ExitCode -ne 0 -or !$importText.Contains('ART_STUDY_IMPORT_READY') -or $importText.Contains('Fatal error:')){throw "Study import failed: $importLog"}
Write-Output 'Art study ready. Run Scripts/LaunchArtStudy.ps1.'

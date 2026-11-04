param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$project=Join-Path $projectRoot 'nUthEck.uproject'
$log=Join-Path $projectRoot 'build-creature-batch28-live.log'
$arguments=@(('"'+$project+'"'),'/Game/Maps/DungeonPrototype','-game','-windowed','-ResX=1600','-ResY=1200','-ForceRes',
    '-nosound','-NoSplash','-unattended','-NewGame','-SculptedCreatures','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom',
    '-HideEntityGlyphs','-VerifyCreatureBatch28','-PreviewCreatureBatch28',('-abslog="'+$log+'"'))
$taskProcess=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
$output=Get-Content -LiteralPath $log -Raw
foreach($marker in @('CREATURE_BATCH28_CHECK PASS','NETHACK_LIVE_CHECK PASS','DUNGEON_ZOOM_CHECK PASS','DEFAULT_TILES_CHECK PASS')) {
    if(!$output.Contains($marker)){throw "Missing $marker in $log"}
}
if($taskProcess.ExitCode -ne 0){throw "Capture failed with exit code $($taskProcess.ExitCode): $log"}
Copy-Item -LiteralPath (Join-Path $projectRoot 'Saved\Screenshots\DefaultTilesDungeon.png') -Destination (Join-Path $projectRoot 'Art\CreatureInterpretations\Batch28-Unreal-fixtures.png') -Force
Write-Output "Creature batch 28 checks passed: $log"

param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$project=Join-Path $projectRoot 'nUthEck.uproject'
$log=Join-Path $projectRoot 'build-creature-batch15-live.log'
$arguments=@(('"'+$project+'"'),'/Game/Maps/DungeonPrototype','-game','-windowed','-ResX=1600','-ResY=900','-ForceRes',
    '-nosound','-NoSplash','-unattended','-NewGame','-SculptedCreatures','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom',
    '-HideEntityGlyphs','-VerifyCreatureBatch15','-PreviewCreatureBatch15',('-abslog="'+$log+'"'))
$taskProcess=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
$output=Get-Content -LiteralPath $log -Raw
foreach($marker in @('CREATURE_BATCH15_CHECK PASS','NETHACK_LIVE_CHECK PASS','DUNGEON_ZOOM_CHECK PASS','DEFAULT_TILES_CHECK PASS')) {
    if(!$output.Contains($marker)){throw "Missing $marker in $log"}
}
if($taskProcess.ExitCode -ne 0){throw "Capture failed with exit code $($taskProcess.ExitCode): $log"}
Copy-Item -LiteralPath (Join-Path $projectRoot 'Saved\Screenshots\DefaultTilesDungeon.png') -Destination (Join-Path $projectRoot 'Art\CreatureInterpretations\Batch15-Unreal-fixtures.png') -Force
Write-Output "Creature batch 15 checks passed: $log"

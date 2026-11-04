param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$log=Join-Path $projectRoot 'build-oracle-regression.log'
$arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype',
    '-game','-windowed','-ResX=1600','-ResY=900','-ForceRes','-nosound','-NoSplash','-unattended',
    '-NewGame','-HideEntityGlyphs','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom',
    '-VerifyObjectPlacement','-VerifyTopmost','-PreviewTopmost',('-abslog="'+$log+'"'))
$taskProcess=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
$output=Get-Content -LiteralPath $log -Raw
foreach($marker in @('TOPMOST_PRESENTATION_CHECK PASS','OBJECT_PLACEMENT_CHECK PASS','NETHACK_LIVE_CHECK PASS','DUNGEON_ZOOM_CHECK PASS','DEFAULT_TILES_CHECK PASS')) {
    if(!$output.Contains($marker)){throw "Missing $marker in $log"}
}
if($taskProcess.ExitCode -ne 0){throw "Object placement capture failed with exit code $($taskProcess.ExitCode): $log"}
Copy-Item -LiteralPath (Join-Path $projectRoot 'Saved\Screenshots\DefaultTilesDungeon.png') -Destination (Join-Path $projectRoot 'Art\OracleSanctuary\Oracle-Regression.png') -Force
Write-Output "Object placement checks passed: $log"

param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$data=Get-Content (Join-Path $root 'build-appearance-batch1-fixture.json') -Raw | ConvertFrom-Json
$id=Split-Path $data.session -Leaf
if($id -notmatch '^[a-f0-9]{32}$'){throw 'Invalid isolated fixture'}
$log=Join-Path $root 'build-appearance-batch1-live.log'
$args=@(('"'+(Join-Path $root 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype','-game','-windowed','-ResX=1600','-ResY=1000','-ForceRes','-nosound','-NoSplash','-unattended','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom','-VerifyObjectPlacement','-VerifyTopmost','-VerifyAppearanceBatch1','-PreviewAppearanceBatch1','-HideEntityGlyphs',('-MinesCaptureSession='+$id),('-abslog="'+$log+'"'))
$p=Start-Process -FilePath (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor.exe') -ArgumentList $args -WindowStyle Hidden -PassThru -Wait
$text=Get-Content $log -Raw
$markers=@('APPEARANCE_BATCH1_CHECK PASS','OBJECT_PLACEMENT_CHECK PASS','TOPMOST_PRESENTATION_CHECK PASS','NETHACK_LIVE_CHECK PASS','DUNGEON_ZOOM_CHECK PASS','DEFAULT_TILES_CHECK PASS')
foreach($marker in $markers){if(!$text.Contains($marker)){throw "Missing $marker"}}
if($p.ExitCode -ne 0){throw 'Appearance capture failed'}
Copy-Item (Join-Path $root 'Saved/Screenshots/DefaultTilesDungeon.png') (Join-Path $root 'Art/ObjectInterpretations/AppearanceBatch1-Unreal.png') -Force
@{status='PASS';checks=$markers;appearance_check=[regex]::Match($text,'APPEARANCE_BATCH1_CHECK PASS[^\r\n]+').Value;fixture=$data;player_session_used=$false} | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $root 'Art/ObjectInterpretations/appearance-batch1-live.json') -Encoding utf8
Write-Output 'APPEARANCE_BATCH1_CAPTURE_PASS'

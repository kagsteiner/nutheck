param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7',[switch]$UpperVault)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$data=Get-Content (Join-Path $root 'build-sokoban-fixture.json') -Raw | ConvertFrom-Json
if($UpperVault){
 $layouts=Get-Content (Join-Path $root 'Art/Sokoban/native-layouts.json') -Raw | ConvertFrom-Json
 $data=$layouts.layouts.'soko1-1'
}
$tag=if($UpperVault){'upper'}else{'live'}
$capture=if($UpperVault){'Sokoban-UpperVault-Unreal.png'}else{'Sokoban-Unreal.png'}
$id=Split-Path $data.session -Leaf
if($id -notmatch '^[a-f0-9]{32}$'){throw 'Invalid isolated fixture'}
$log=Join-Path $root ('build-sokoban-'+$tag+'.log')
$args=@(('"'+(Join-Path $root 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype','-game','-windowed','-ResX=1600','-ResY=1000','-ForceRes','-nosound','-NoSplash','-unattended','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom','-VerifySokoban','-VerifyObjectPlacement','-VerifyTopmost','-HideEntityGlyphs','-SculptedCreatures',('-MinesCaptureSession='+$id),('-abslog="'+$log+'"'))
$p=Start-Process -FilePath (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor.exe') -ArgumentList $args -WindowStyle Hidden -PassThru -Wait
$text=Get-Content $log -Raw
foreach($marker in @('SOKOBAN_CHECK PASS','OBJECT_PLACEMENT_CHECK PASS','TOPMOST_PRESENTATION_CHECK PASS','NETHACK_LIVE_CHECK PASS','SOKOBAN_CAMERA_CHECK PASS','DEFAULT_TILES_CHECK PASS')){if(!$text.Contains($marker)){throw "Missing $marker"}}
if($p.ExitCode -ne 0){throw 'Sokoban capture failed'}
Copy-Item (Join-Path $root 'Saved/Screenshots/DefaultTilesDungeon.png') (Join-Path $root ('Art/Sokoban/'+$capture)) -Force
$report=@{status='PASS';checks=@('SOKOBAN_CHECK PASS','OBJECT_PLACEMENT_CHECK PASS','TOPMOST_PRESENTATION_CHECK PASS','NETHACK_LIVE_CHECK PASS','SOKOBAN_CAMERA_CHECK PASS','DEFAULT_TILES_CHECK PASS');sokoban_check=[regex]::Match($text,'SOKOBAN_CHECK PASS[^\r\n]+').Value;capture=$capture;fixture=$data;player_session_used=$false}
$report | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $root ('Art/Sokoban/'+$tag+'-verification.json')) -Encoding utf8
Write-Output 'SOKOBAN_CAPTURE_PASS'

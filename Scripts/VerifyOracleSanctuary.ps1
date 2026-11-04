param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$data=Get-Content (Join-Path $root 'build-oracle-fixture.json') -Raw | ConvertFrom-Json
$id=Split-Path $data.session -Leaf
if($id -notmatch '^[a-f0-9]{32}$'){throw 'Invalid isolated fixture'}
$log=Join-Path $root 'build-oracle-live.log'
$args=@(('"'+(Join-Path $root 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype','-game','-windowed','-ResX=1600','-ResY=1000','-ForceRes','-nosound','-NoSplash','-unattended','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom','-VerifyOracle',('-MinesCaptureSession='+$id),('-abslog="'+$log+'"'))
$p=Start-Process -FilePath (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor.exe') -ArgumentList $args -WindowStyle Hidden -PassThru -Wait
$text=Get-Content $log -Raw
foreach($marker in @('ORACLE_SANCTUARY_CHECK PASS','NETHACK_LIVE_CHECK PASS','DUNGEON_ZOOM_CHECK PASS','DEFAULT_TILES_CHECK PASS')){if(!$text.Contains($marker)){throw "Missing $marker"}}
if($p.ExitCode -ne 0){throw 'Oracle capture failed'}
Copy-Item (Join-Path $root 'Saved/Screenshots/DefaultTilesDungeon.png') (Join-Path $root 'Art/OracleSanctuary/Oracle-Unreal.png') -Force
Write-Output 'ORACLE_CAPTURE_PASS'

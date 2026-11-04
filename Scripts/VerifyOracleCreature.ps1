param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$data=Get-Content (Join-Path $root 'build-oracle-fixture.json') -Raw | ConvertFrom-Json
$id=Split-Path $data.session -Leaf
if($id -notmatch '^[a-f0-9]{32}$'){throw 'Invalid isolated fixture'}
$log=Join-Path $root 'build-oracle-creature-live.log'
$args=@(('"'+(Join-Path $root 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype','-game','-windowed','-ResX=1600','-ResY=1000','-ForceRes','-nosound','-NoSplash','-unattended','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom','-VerifyOracle','-VerifyOracleCreature','-SculptedCreatures',('-MinesCaptureSession='+$id),('-abslog="'+$log+'"'))
$p=Start-Process -FilePath (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor.exe') -ArgumentList $args -WindowStyle Hidden -PassThru -Wait
$text=Get-Content $log -Raw
foreach($marker in @('ORACLE_CREATURE_CHECK PASS','ORACLE_SANCTUARY_CHECK PASS','NETHACK_LIVE_CHECK PASS','DUNGEON_ZOOM_CHECK PASS','DEFAULT_TILES_CHECK PASS')){if(!$text.Contains($marker)){throw "Missing $marker"}}
if($p.ExitCode -ne 0){throw 'Oracle capture failed'}
Copy-Item (Join-Path $root 'Saved/Screenshots/DefaultTilesDungeon.png') (Join-Path $root 'Art/CreatureInterpretations/Oracle-Unreal.png') -Force
$report=@{status='PASS';checks=@('ORACLE_CREATURE_CHECK PASS','ORACLE_SANCTUARY_CHECK PASS','NETHACK_LIVE_CHECK PASS','DUNGEON_ZOOM_CHECK PASS','DEFAULT_TILES_CHECK PASS');oracle_check=[regex]::Match($text,'ORACLE_CREATURE_CHECK PASS[^\r\n]+').Value;capture='Oracle-Unreal.png';fixture=$data;player_session_used=$false}
$report | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $root 'Art/CreatureInterpretations/oracle-live-verification.json') -Encoding utf8
Write-Output 'ORACLE_CREATURE_CAPTURE_PASS'

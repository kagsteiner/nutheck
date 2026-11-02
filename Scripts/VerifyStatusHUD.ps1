param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$out=Join-Path $projectRoot 'Docs\Images\StatusHUD'
New-Item -ItemType Directory -Force -Path $out | Out-Null
foreach($case in @(@('normal',1600,900),@('warning',1280,720),@('critical',1600,900),@('stress',800,600),@('stress',640,480))) {
    $name="$($case[0])-$($case[1])x$($case[2])"
    $log=Join-Path $projectRoot "build-status-hud-$name.log"
    $arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype',
        '-game','-windowed',('-ResX='+$case[1]),('-ResY='+$case[2]),'-ForceRes','-nosound','-NoSplash','-unattended',
        '-NewGame','-SculptedCreatures','-HideEntityGlyphs','-CaptureLive','-CaptureDefaultTiles','-CaptureZoom',
        '-VerifyStatusHUD','-VerifyMouseTravel',('-StatusHUDPreview='+$case[0]),('-abslog="'+$log+'"'))
    $process=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
    $text=Get-Content -LiteralPath $log -Raw
    foreach($marker in @('STATUS_HUD_CHECK PASS','MOUSE_TRAVEL_CHECK PASS','NETHACK_LIVE_CHECK PASS','DEFAULT_TILES_CHECK PASS')) {
        if(!$text.Contains($marker)){throw "Missing $marker in $log"}
    }
    if($process.ExitCode -ne 0 -or $text.Contains('STATUS_HUD_CHECK FAIL')){throw "Status HUD failed: $log"}
    Copy-Item -LiteralPath (Join-Path $projectRoot 'Saved\Screenshots\DefaultTilesDungeon.png') -Destination (Join-Path $out "$name.png") -Force
    Write-Output "Status HUD passed: $name"
}

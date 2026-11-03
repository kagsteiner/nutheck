param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7',[string[]]$Views=@('lit','dark','town','wide'))
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$out=Join-Path $projectRoot 'Docs\Images\Mines'
New-Item -ItemType Directory -Force -Path $out | Out-Null
foreach($view in $Views) {
    $fixture=if($view -in @('wide','eye')){'lit'}else{$view}
    $data=Get-Content -LiteralPath (Join-Path $projectRoot "build-mines-$fixture-fixture.json") -Raw | ConvertFrom-Json
    $captureId=Split-Path $data.session -Leaf
    if($captureId -notmatch '^[a-f0-9]{32}$'){throw 'Invalid isolated capture GUID'}
    $log=Join-Path $projectRoot "build-mines-$view.log"
    $arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype',
        '-game','-windowed','-ResX=1600','-ResY=900','-ForceRes','-nosound','-NoSplash','-unattended',
        '-SculptedCreatures','-HideEntityGlyphs','-CaptureLive','-CaptureDefaultTiles','-VerifyMines',
        ('-MinesCaptureSession='+$captureId),('-abslog="'+$log+'"'))
    if($view -eq 'eye'){$arguments+='-CaptureFirstPerson'}elseif($view -ne 'wide'){$arguments+='-CaptureZoom'}
    $process=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
    $text=Get-Content -LiteralPath $log -Raw
    foreach($marker in @('MINES_CHECK PASS','NETHACK_LIVE_CHECK PASS','DEFAULT_TILES_CHECK PASS')) {
        if(!$text.Contains($marker)){throw "Missing $marker in $log"}
    }
    if($process.ExitCode -ne 0 -or $text.Contains('MINES_CHECK FAIL') -or $text.Contains('Failed to compile Material')){throw "Mines checks failed: $log"}
    if($view -eq 'eye' -and !$text.Contains('DUNGEON_FIRST_PERSON_CHECK PASS')){throw "First person check failed: $log"}
    if($view -eq 'lit' -and $text -match 'MINES_CHECK PASS[^\r\n]*torches=0 '){throw "Lit cavern fixture has no torches: $log"}
    Copy-Item -LiteralPath (Join-Path $projectRoot 'Saved\Screenshots\DefaultTilesDungeon.png') -Destination (Join-Path $out "$view.png") -Force
    Write-Output "Mines checks passed: $view"
}

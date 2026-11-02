param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$out=Join-Path $projectRoot 'Docs\Images\Navigation'
New-Item -ItemType Directory -Force -Path $out | Out-Null
foreach($view in @('close','wide')) {
    $log=Join-Path $projectRoot "build-navigation-$view.log"
    $arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype',
        '-game','-windowed','-ResX=1600','-ResY=900','-ForceRes','-nosound','-NoSplash','-unattended',
        '-NewGame','-SculptedCreatures','-HideEntityGlyphs','-CaptureLive','-CaptureDefaultTiles',
        '-VerifyNavigation','-PreviewStairs',('-abslog="'+$log+'"'))
    if($view -eq 'wide'){$arguments+='-NavigationWide'}else{$arguments+='-CaptureZoom'}
    $process=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
    $text=Get-Content -LiteralPath $log -Raw
    foreach($marker in @('NAVIGATION_CHECK PASS','NETHACK_LIVE_CHECK PASS','DEFAULT_TILES_CHECK PASS')) {
        if(!$text.Contains($marker)){throw "Missing $marker in $log"}
    }
    if($view -eq 'wide' -and !$text.Contains('PROTOTYPE_FRAME_CHECK PASS')){throw "Level framing check failed: $log"}
    if($process.ExitCode -ne 0 -or $text.Contains('NAVIGATION_CHECK FAIL')){throw "Navigation checks failed: $log"}
    Copy-Item -LiteralPath (Join-Path $projectRoot 'Saved\Screenshots\DefaultTilesDungeon.png') -Destination (Join-Path $out "$view.png") -Force
    Write-Output "Navigation checks passed: $view"
}

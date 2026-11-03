param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$outputDir=Join-Path $projectRoot 'Docs\Images\EndScreen'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
foreach($scenario in @('save','quit')) {
    $log=Join-Path $projectRoot ('build-end-screen-'+$scenario+'.log')
    $arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype',
        '-game','-windowed','-ResX=1600','-ResY=900','-ForceRes','-nosound','-NoSplash','-unattended',
        '-NewGame','-CaptureLive','-VerifyEndScreen',('-EndScreenCase='+$scenario),('-abslog="'+$log+'"'))
    $process=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
    $text=Get-Content -LiteralPath $log -Raw
    foreach($marker in @('END_SCREEN_CHECK PASS','NETHACK_APP_QUIT ended=1 backend_running=0')) {
        if(!$text.Contains($marker)){throw "Missing $marker in $log"}
    }
    if($process.ExitCode -ne 0){throw "End-screen verification exited $($process.ExitCode): $log"}
    if($text -notmatch 'NETHACK_SESSION_START (.+NetHackCaptures[^\r\n]+)'){throw "Capture session was not isolated: $log"}
    $sessionRoot=$Matches[1].Trim()
    if($scenario -eq 'save' -and !(Get-ChildItem -LiteralPath $sessionRoot -File | Where-Object {$_.Name -like '*saved-game*'})) {
        throw "Save scenario did not preserve a native save in $sessionRoot"
    }
    Copy-Item -LiteralPath (Join-Path $projectRoot ('Saved\Screenshots\EndScreen-'+$scenario+'.png')) -Destination (Join-Path $outputDir ($scenario+'.png')) -Force
    Write-Output "END_SCREEN_LIVE_PASS case=$scenario isolated=$sessionRoot"
}

param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$log=Join-Path $projectRoot 'build-presentation-controls-live.log'
$arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype',
    '-game','-windowed','-ResX=1600','-ResY=900','-ForceRes','-nosound','-NoSplash','-unattended',
    '-NewGame','-SculptedCreatures','-CaptureLive','-CaptureFirstPerson','-VerifyPresentationControls',
    '-VerifyCreatureBatch11','-PreviewCreatureBatch11',('-abslog="'+$log+'"'))
$taskProcess=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
$output=Get-Content -LiteralPath $log -Raw
foreach($marker in @('PRESENTATION_CONTROLS_CHECK PASS','DUNGEON_FIRST_PERSON_CHECK PASS','NETHACK_LIVE_CHECK PASS','CREATURE_BATCH11_CHECK PASS')) {
    if(!$output.Contains($marker)){throw "Missing $marker in $log"}
}
if($taskProcess.ExitCode -ne 0){throw "Capture failed with exit code $($taskProcess.ExitCode): $log"}
$captureOutput=Join-Path $projectRoot 'Docs\Images\PresentationControls'
New-Item -ItemType Directory -Path $captureOutput -Force | Out-Null
foreach($name in @('Presentation-Labels-On.png','Presentation-Labels-Off.png','Presentation-Camera-Mid.png',
    'Presentation-Camera-Eye.png','Presentation-Camera-Out-Mid.png','Presentation-Camera-Returned.png','FirstPersonDungeon.png')) {
    Copy-Item -LiteralPath (Join-Path $projectRoot ('Saved\Screenshots\'+$name)) -Destination (Join-Path $captureOutput $name) -Force
}
Write-Output "Presentation controls passed: $log"

param([string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
foreach($view in @('close','gameplay','level')){
    $log=Join-Path $projectRoot "build-fur-$view.log"
    $arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype',
        '-game','-FurStudy',"-FurView=$view",'-windowed','-ResX=1920','-ResY=1280','-ForceRes','-unattended','-nosound','-NoSplash',('-abslog="'+$log+'"'))
    $taskProcess=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle Hidden -PassThru -Wait
    $text=Get-Content -LiteralPath $log -Raw
    if($taskProcess.ExitCode -ne 0 -or !$text.Contains('FUR_STUDY_CHECK PASS')){throw "Fur capture failed: $log"}
    Write-Output "Fur study $view capture passed: $log"
}

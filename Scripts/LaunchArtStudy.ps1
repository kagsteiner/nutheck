param(
    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.7',
    [ValidateSet('overview','detail','eye','level')][string]$View='overview',
    [switch]$Capture
)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path $PSScriptRoot -Parent
$editor=Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
$arguments=@(('"'+(Join-Path $projectRoot 'nUthEck.uproject')+'"'),'/Game/Maps/DungeonPrototype','-game','-ArtStudy',"-ArtView=$View",'-windowed','-ResX=1600','-ResY=900','-ForceRes','-nosound','-NoSplash')
if($Capture) {
    $verificationLog=Join-Path $projectRoot ('Saved\Logs\ArtStudy-'+[guid]::NewGuid().ToString('N')+'.log')
    $arguments+=@('-CaptureArt','-unattended',('-abslog="'+$verificationLog+'"'))
}
$style=if($Capture){'Hidden'}else{'Normal'}
$process=Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle $style -PassThru -Wait
if($Capture) {
    if(!(Get-Content -LiteralPath $verificationLog -Raw).Contains("ART_STUDY_CHECK PASS view=$View")) { throw "Art study failed: $verificationLog" }
    Write-Output "Art study passed: $verificationLog"
}
exit $process.ExitCode

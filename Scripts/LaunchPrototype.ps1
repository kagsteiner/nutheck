param(
    [string]$EngineRoot = 'C:\Program Files\Epic Games\UE_5.7',
    [int]$Width = 1600,
    [int]$Height = 900,
    [switch]$Windowed,
    [switch]$Capture,
    [switch]$StaticStudy,
    [switch]$ZoomedCapture,
    [switch]$FirstPersonCapture,
    [switch]$DefaultTileCapture,
    [switch]$NewGame,
    [switch]$SculptedCreatures
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$editor = Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe'
if (!(Test-Path -LiteralPath $editor)) { throw "Unreal Editor not found: $editor" }
$arguments = @(
    ('"' + (Join-Path $projectRoot 'nUthEck.uproject') + '"'),
    '/Game/Maps/DungeonPrototype', '-game', '-nosound', '-NoSplash'
)
if ($StaticStudy) { $arguments += '-StaticStudy' }
if ($NewGame) { $arguments += '-NewGame' }
if ($SculptedCreatures) { $arguments += '-SculptedCreatures' }
if ($DefaultTileCapture) {
    if ($StaticStudy -or $FirstPersonCapture) { throw 'DefaultTileCapture requires a live overhead game.' }
    $Capture=$true
    $ZoomedCapture=$true
    $arguments+='-CaptureDefaultTiles'
}
if ($FirstPersonCapture) {
    if ($StaticStudy -or $ZoomedCapture) { throw 'FirstPersonCapture requires a live game without ZoomedCapture.' }
    $Capture = $true
    $arguments += '-CaptureFirstPerson'
}
if ($ZoomedCapture) {
    if ($StaticStudy) { throw 'ZoomedCapture runs against a live game.' }
    $Capture = $true
    $arguments += '-CaptureZoom'
}
if ($Windowed -or $Capture) {
    $arguments += @('-windowed', "-ResX=$Width", "-ResY=$Height", '-ForceRes')
} else {
    $arguments += '-fullscreen'
}
if ($Capture) {
    $arguments += '-unattended'
    $arguments += $(if ($StaticStudy) { '-CapturePrototype' } else { '-CaptureLive' })
    $verificationLog = Join-Path $projectRoot ('Saved\Logs\Verification-' + [guid]::NewGuid().ToString('N') + '.log')
    $arguments += ('-abslog="' + $verificationLog + '"')
}
$windowStyle = if ($Capture) { 'Hidden' } else { 'Normal' }
if (!$Capture -and !$StaticStudy -and (Test-Path -LiteralPath (Join-Path $projectRoot 'Saved\NetHack'))) {
    & (Join-Path $PSScriptRoot 'BackupNetHackSaves.ps1') -Reason 'Before normal player launch'
}
$gameProcess = Start-Process -FilePath $editor -ArgumentList $arguments -WindowStyle $windowStyle -PassThru -Wait
if (!$Capture -and !$StaticStudy -and (Test-Path -LiteralPath (Join-Path $projectRoot 'Saved\NetHack'))) {
    & (Join-Path $PSScriptRoot 'BackupNetHackSaves.ps1') -Reason 'After normal player exit'
}
if ($Capture) {
    $verificationText = Get-Content -LiteralPath $verificationLog -Raw
    $cameraCheck = if ($FirstPersonCapture) { 'DUNGEON_FIRST_PERSON_CHECK PASS' } elseif ($ZoomedCapture) { 'DUNGEON_ZOOM_CHECK PASS' } else { 'PROTOTYPE_FRAME_CHECK PASS' }
    if (!$verificationText.Contains($cameraCheck) -or (!$StaticStudy -and !$verificationText.Contains('NETHACK_LIVE_CHECK PASS'))) {
        Write-Error "Capture verification failed; inspect $verificationLog"
        exit 1
    }
    if ($DefaultTileCapture -and !$verificationText.Contains('DEFAULT_TILES_CHECK PASS')) { throw "Default tile figure check failed: $verificationLog" }
    Write-Output "Capture checks passed: $verificationLog"
}
exit $gameProcess.ExitCode

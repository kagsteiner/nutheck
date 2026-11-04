param(
    [ValidateSet('home','upper','locate','lower','goal')][string]$Stage='home',
    [switch]$Capture,
    [switch]$Orb,
    [switch]$Inside,
    [switch]$Eye,
    [string]$EngineRoot='C:\Program Files\Epic Games\UE_5.7'
)
$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$python=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if(!(Test-Path $python)){$python=(Get-Command python -ErrorAction Stop).Source}
Push-Location $root
try {
    $fixtureArgs=@('Tests/CreateValkyrieQuestPreview.py',$Stage)
    if($Inside){
        if($Stage -ne 'locate'){throw '-Inside is available for locate only'}
        $fixtureArgs+='--inside'
    }
    if($Orb){$fixtureArgs+='--orb'}
    $report=& $python @fixtureArgs
    if($LASTEXITCODE -ne 0){throw 'Isolated quest creation failed'}
    $data=$report | ConvertFrom-Json
    if($data.id -notmatch '^[a-f0-9]{32}$'){throw 'Invalid isolated session ID'}
    Write-Output "Fresh isolated quest preview: $($data.session)"
    $log=Join-Path $root "build-valkyrie-$Stage.log"
    $arguments=@(('"'+$root+'\nUthEck.uproject"'),'/Game/Maps/DungeonPrototype','-game',
        '-windowed','-ResX=1600','-ResY=1000','-ForceRes','-nosound','-NoSplash',
        '-ddc=InstalledNoZenLocalFallback','-QuestPreview',('-QuestPreviewSession='+$data.id),
        '-SculptedCreatures','-HideEntityGlyphs',('-abslog="'+$log+'"'))
    if($Capture){
        $arguments+=@('-unattended','-CaptureLive','-CaptureDefaultTiles','-VerifyValkyrieQuest')
        if($Eye){$arguments+='-CaptureFirstPerson'}elseif($Orb -or $Inside){$arguments+='-CaptureZoom'}
    }
    $style=if($Capture){'Hidden'}else{'Normal'}
    $p=Start-Process (Join-Path $EngineRoot 'Engine\Binaries\Win64\UnrealEditor.exe') -ArgumentList $arguments -WindowStyle $style -PassThru -Wait
    if($p.ExitCode -ne 0){throw "Quest preview failed: $log"}
    if($Capture){
        $text=Get-Content $log -Raw
        foreach($marker in @('VALKYRIE_QUEST_CHECK PASS','NETHACK_LIVE_CHECK PASS','DEFAULT_TILES_CHECK PASS')){
            if(!$text.Contains($marker)){throw "Missing $marker in $log"}
        }
        if($text.Contains('Failed to compile Material')){throw "Material compilation failure: $log"}
        $out=Join-Path $root 'Docs/Images/ValkyrieQuest'
        New-Item -ItemType Directory -Force $out | Out-Null
        $imageName=if($Eye){"$Stage-moon-eye.png"}elseif($Orb){"$Stage-orb.png"}elseif($Inside){"$Stage-lighting.png"}else{"$Stage.png"}
        Copy-Item (Join-Path $root 'Saved/Screenshots/DefaultTilesDungeon.png') (Join-Path $out $imageName)
        Write-Output "Quest preview checks passed: $Stage"
    }
} finally {Pop-Location}

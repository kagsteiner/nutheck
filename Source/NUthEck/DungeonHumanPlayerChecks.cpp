#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "Misc/CommandLine.h"
#include "TimerManager.h"

void ADungeonPrototype::VerifyAndCaptureHumanPlayers()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    const FString Race=Session->HeroRace;const bool Poly=Session->HeroPolymorphed,Style=SculptedCreatures;
    bool Passed=true;int32 Cases=0;
    FString Preview;FParse::Value(FCommandLine::Get(),TEXT("HumanPlayerPreview="),Preview);
    const auto Actual=Session->Cells[Session->Hero.Y*Columns+Session->Hero.X];
    Passed &= Race==TEXT("human") && !Poly
        && ((Preview==TEXT("valkyrie_female_human") && Actual.DisplayMonster==TEXT("valkyrie") && Actual.Female)
        || (Preview==TEXT("barbarian_male_human") && Actual.DisplayMonster==TEXT("barbarian") && !Actual.Female)
        || (Preview==TEXT("samurai_male_human") && Actual.DisplayMonster==TEXT("samurai") && !Actual.Female)
        || (Preview==TEXT("samurai_female_human") && Actual.DisplayMonster==TEXT("samurai") && Actual.Female));
    if(!SculptedCreatures) HandleLiveKey(EKeys::F9,false);
    const auto Probe=[this,&Passed,&Cases](const FString& Name,bool Female,const FString& Ancestry,bool Polymorphed,bool Hero,const FString& Expected)
    {
        Session->HeroRace=Ancestry;Session->HeroPolymorphed=Polymorphed;
        FNetHackCell Cell;Cell.DisplayMonster=Name;Cell.Female=Female;
        auto* Batch=GetDefaultTileBatch(Cell,Hero);
        const FString Path=Batch && Batch->GetStaticMesh()?Batch->GetStaticMesh()->GetPathName():TEXT("");
        if(!Expected.IsEmpty())
        {
            Passed &= Path==TEXT("/Game/CreatureInterpretations/Meshes/SM_")+Expected+TEXT(".SM_")+Expected;
            if(Batch && Batch->GetStaticMesh())
            {
                const auto* Data=Batch->GetStaticMesh()->GetRenderData();
                Passed &= Data && Data->LODResources.Num()>0 && Data->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
            }
        }
        else Passed &= !Path.Contains(TEXT("_female_human")) && !Path.Contains(TEXT("_male_human"));
        ++Cases;
    };
    Probe(TEXT("valkyrie"),true,TEXT("human"),false,true,TEXT("valkyrie_female_human"));
    Probe(TEXT("barbarian"),false,TEXT("human"),false,true,TEXT("barbarian_male_human"));
    Probe(TEXT("valkyrie"),false,TEXT("human"),false,true,TEXT(""));
    Probe(TEXT("barbarian"),true,TEXT("human"),false,true,TEXT(""));
    Probe(TEXT("valkyrie"),true,TEXT("dwarf"),false,true,TEXT(""));
    Probe(TEXT("barbarian"),false,TEXT("orc"),false,true,TEXT(""));
    Probe(TEXT("valkyrie"),true,TEXT(""),false,true,TEXT(""));
    Probe(TEXT("valkyrie"),true,TEXT("human"),true,true,TEXT(""));
    Probe(TEXT("valkyrie"),true,TEXT("human"),false,false,TEXT(""));
    for(bool Female:{false,true}) {
        Probe(TEXT("samurai"),Female,TEXT("human"),false,true,Female?TEXT("samurai_female_human"):TEXT("samurai_male_human"));
        Probe(TEXT("samurai"),Female,TEXT("orc"),false,true,TEXT(""));
        Probe(TEXT("samurai"),Female,TEXT(""),false,true,TEXT(""));
        Probe(TEXT("samurai"),Female,TEXT("human"),true,true,TEXT(""));
        Probe(TEXT("samurai"),Female,TEXT("human"),false,false,TEXT(""));
    }
    Session->HeroRace=Race;Session->HeroPolymorphed=Poly;
    HandleLiveKey(EKeys::F9,false);
    Probe(TEXT("samurai"),false,TEXT("human"),false,true,TEXT(""));
    Probe(TEXT("samurai"),true,TEXT("human"),false,true,TEXT(""));
    Probe(TEXT("valkyrie"),true,TEXT("human"),false,true,TEXT(""));
    Probe(TEXT("barbarian"),false,TEXT("human"),false,true,TEXT(""));
    HandleLiveKey(EKeys::F9,false);
    Session->HeroRace=Race;Session->HeroPolymorphed=Poly;
    if(!Style) HandleLiveKey(EKeys::F9,false);
    RebuildLiveMap();AdjustZoom(12.f);
    Passed &= Session->Turn==Turn && Session->Sequence==Sequence && HeroVolumeKey==TEXT("Sculpted_")+Preview;
    UE_LOG(LogTemp,Display,TEXT("HUMAN_PLAYER_CHECK %s selected=%s race=%s cases=%d turn_before=%d turn_after=%d sequence=%d"),
        Passed?TEXT("PASS"):TEXT("FAIL"),*Preview,*Race,Cases,Turn,Session->Turn,Sequence);
    if(!Passed) { FPlatformMisc::RequestExitWithStatus(false,1);return; }
    const float Zoom=ZoomFactor;const FVector Focus=CameraFocus;
    HandleLiveKey(EKeys::F,true);
    FTimerHandle Enter;
    GetWorldTimerManager().SetTimer(Enter,[this,Turn,Zoom,Focus]()
    {
        const auto* HeroBatch=LiveBatches.Find(TEXT("PlayerVolume"));
        const bool Hidden=IsFirstPerson() && HeroBatch && !(*HeroBatch)->IsVisible();
        HandleLiveKey(EKeys::F,true);
        FTimerHandle Leave;
        GetWorldTimerManager().SetTimer(Leave,[this,Turn,Zoom,Focus,Hidden]()
        {
            const auto* HeroBatch=LiveBatches.Find(TEXT("PlayerVolume"));
            const bool Passed=Hidden && !IsFirstPerson() && HeroBatch && (*HeroBatch)->IsVisible()
                && ZoomFactor==Zoom && CameraFocus.Equals(Focus,.1) && Session->Turn==Turn;
            UE_LOG(LogTemp,Display,TEXT("HUMAN_PLAYER_FIRST_PERSON_CHECK %s hidden=%d restored=%d turn=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),Hidden,Passed,Session->Turn);
            if(!Passed) { FPlatformMisc::RequestExitWithStatus(false,1);return; }
            CaptureAndValidate();
        },1.3f,false);
    },1.3f,false);
}

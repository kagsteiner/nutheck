#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "Materials/MaterialInterface.h"
#include "Misc/CommandLine.h"
#include "Misc/PackageName.h"
#include "InputCoreTypes.h"

UInstancedStaticMeshComponent* ADungeonPrototype::GetFountainBatch(const FNetHackCell& Cell)
{
    if(Cell.Terrain!=TEXT("fountain") || Cell.Kind==TEXT("unknown")) return nullptr;
    const FString Package=TEXT("/Game/EnvironmentInterpretations/Meshes/SM_fountain");
    if(!FPackageName::DoesPackageExist(Package)) return nullptr;
    const FName Name(Cell.Visible?TEXT("Fountain"):TEXT("FountainMemory"));
    if(auto* Existing=LiveBatches.Find(Name)) return Existing->Get();
    auto* Mesh=LoadObject<UStaticMesh>(nullptr,*(Package+TEXT(".SM_fountain")));if(!Mesh)return nullptr;
    auto* Batch=NewObject<UInstancedStaticMeshComponent>(this,Name);
    Batch->SetupAttachment(RootComponent);Batch->SetStaticMesh(Mesh);
    Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision);Batch->SetCastShadow(true);
    Batch->SetLightingChannels(Cell.Visible,!Cell.Visible,false);
    if(!Cell.Visible) for(int32 I=0;I<Mesh->GetStaticMaterials().Num();++I)
    {
        const FString Material=GetNameSafe(Mesh->GetMaterial(I))+TEXT("Memory");
        if(auto* Dim=LoadObject<UMaterialInterface>(nullptr,*(TEXT("/Game/EnvironmentInterpretations/")+Material+TEXT(".")+Material)))Batch->SetMaterial(I,Dim);
    }
    AddInstanceComponent(Batch);Batch->RegisterComponent();LiveBatches.Add(Name,Batch);return Batch;
}

void ADungeonPrototype::VerifySpecialBatch1()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;const bool Style=SculptedCreatures;bool Passed=true;
    const auto Painted=[&Passed](UInstancedStaticMeshComponent* Batch,bool Memory)
    {
        if(!Batch || !Batch->GetStaticMesh()){Passed=false;return;}
        const auto* Data=Batch->GetStaticMesh()->GetRenderData();
        Passed &= Data && Data->LODResources.Num()>0 && Data->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
        for(int32 I=0;I<Batch->GetStaticMesh()->GetStaticMaterials().Num();++I)
            Passed &= GetNameSafe(Batch->GetMaterial(I)).EndsWith(TEXT("Memory"))==Memory;
    };
    for(int32 I=0;I<2;++I)
    {
        for(bool Visible:{false,true})
        {
            FNetHackCell Corpse;Corpse.Kind=TEXT("item");Corpse.DisplayObject=TEXT("corpse");Corpse.Visible=Visible;
            auto* Remains=GetDisplayedObjectBatch(Corpse);Painted(Remains,!Visible);
            Passed &= Remains && Remains->GetStaticMesh()->GetName()==TEXT("SM_corpse");
            FNetHackCell Water;Water.Kind=TEXT("terrain");Water.Terrain=TEXT("fountain");Water.Visible=Visible;
            auto* Basin=GetFountainBatch(Water);Painted(Basin,!Visible);
            Passed &= Basin && Basin->GetStaticMesh()->GetName()==TEXT("SM_fountain");
        }
        for(bool Female:{false,true})
        {
            FNetHackCell Bug;Bug.Kind=TEXT("monster");Bug.DisplayMonster=TEXT("grid bug");Bug.Female=Female;Bug.Visible=true;Bug.TileIndex=236+(Female?1:0);
            auto* Mesh=GetDefaultTileBatch(Bug,false);
            if(SculptedCreatures){Painted(Mesh,false);Passed &= Mesh && Mesh->GetStaticMesh()->GetName()==TEXT("SM_grid_bug");}
            else Passed &= !Mesh; // This species has no retained tile-volume proxy.
            Passed &= AddTileFallback(Bug,0,0);
        }
        HandleLiveKey(EKeys::F9,false);
    }
    for(const FString& Terrain:{FString(TEXT("sink")),FString(TEXT("floor")),FString(TEXT("none"))})
    {FNetHackCell Probe;Probe.Kind=TEXT("terrain");Probe.Terrain=Terrain;Passed &= GetFountainBatch(Probe)==nullptr;}
    FNetHackCell Hidden;Hidden.Kind=TEXT("unknown");Hidden.Terrain=TEXT("fountain");Passed &= GetFountainBatch(Hidden)==nullptr;
    FNetHackCell Wrong;Wrong.Kind=TEXT("monster");Wrong.DisplayObject=TEXT("corpse");Passed &= GetDisplayedObjectBatch(Wrong)==nullptr;
    Passed &= Turn==Session->Turn && Sequence==Session->Sequence && Style==SculptedCreatures;
    RebuildLiveMap();
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewSpecialBatch1")))
    {
        TArray<FIntPoint> Floors;
        for(int32 Y=0;Y<Rows;++Y)for(int32 X=0;X<Columns;++X)
        {const auto& C=Session->Cells[Y*Columns+X];if(C.Visible && C.Terrain==TEXT("floor") && C.Kind==TEXT("terrain") && FIntPoint(X,Y)!=Session->Hero)Floors.Add(FIntPoint(X,Y));}
        const auto Score=[this](const FIntPoint& At)
        {
            int32 Penalty=(At-Session->Hero).SizeSquared();
            for(int32 DY=-1;DY<=1;++DY)for(int32 DX=-1;DX<=1;++DX)
            {
                const FIntPoint Near=At+FIntPoint(DX,DY);
                if(Near.X<0 || Near.X>=Columns || Near.Y<0 || Near.Y>=Rows){Penalty+=100;continue;}
                const auto& Cell=Session->Cells[Near.Y*Columns+Near.X];
                if(!Cell.Visible || Cell.Terrain!=TEXT("floor"))Penalty+=100;
            }
            return Penalty;
        };
        Floors.Sort([&Score](const FIntPoint& A,const FIntPoint& B){return Score(A)<Score(B);});
        Passed &= Floors.Num()>=3;
        if(Floors.Num()>=3)
        {
            FNetHackCell Bug;Bug.Kind=TEXT("monster");Bug.DisplayMonster=TEXT("grid bug");Bug.Visible=true;
            if(auto* B=GetDefaultTileBatch(Bug,false))B->AddInstance(FTransform(FRotator(0,-75,0),CellPosition(Floors[0].X,Floors[0].Y,8),FVector(1)));
            FNetHackCell Corpse;Corpse.Kind=TEXT("item");Corpse.DisplayObject=TEXT("corpse");Corpse.Visible=true;
            if(auto* B=GetDisplayedObjectBatch(Corpse))B->AddInstance(FTransform(FRotator(0,15,0),CellPosition(Floors[1].X,Floors[1].Y,8),FVector(1)));
            FNetHackCell Water;Water.Kind=TEXT("terrain");Water.Terrain=TEXT("fountain");Water.Visible=true;
            if(auto* B=GetFountainBatch(Water))B->AddInstance(FTransform(FQuat::Identity,CellPosition(Floors[2].X,Floors[2].Y,8),FVector(1)));
        }
    }
    UE_LOG(LogTemp,Display,TEXT("SPECIAL_BATCH1_CHECK %s creature_sexes=2 styles=2 memory=2 sink_guard=1 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),Turn,Session->Turn,Sequence,Session->Sequence);
    if(!Passed)FPlatformMisc::RequestExitWithStatus(false,1);
}

#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "Materials/MaterialInterface.h"
#include "Misc/CommandLine.h"
#include "Misc/PackageName.h"
#include "InputCoreTypes.h"

UInstancedStaticMeshComponent* ADungeonPrototype::GetAltarBatch(const FNetHackCell& Cell)
{
    if(Cell.Kind==TEXT("unknown")) return nullptr;
    const TArray<FString> Keys={TEXT("altar_unaligned"),TEXT("altar_chaotic"),TEXT("altar_neutral"),TEXT("altar_lawful"),TEXT("altar_other")};
    if(!Keys.Contains(Cell.Terrain)) return nullptr;
    const FString Package=TEXT("/Game/EnvironmentInterpretations/Meshes/SM_")+Cell.Terrain;
    if(!FPackageName::DoesPackageExist(Package)) return nullptr;
    const FName Name(*(Cell.Terrain+(Cell.Visible?TEXT(""):TEXT("Memory"))));
    if(auto* Existing=LiveBatches.Find(Name)) return Existing->Get();
    auto* Mesh=LoadObject<UStaticMesh>(nullptr,*(Package+TEXT(".SM_")+Cell.Terrain));if(!Mesh)return nullptr;
    auto* Batch=NewObject<UInstancedStaticMeshComponent>(this,Name);
    Batch->SetupAttachment(RootComponent);Batch->SetStaticMesh(Mesh);
    Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision);Batch->SetCastShadow(true);
    Batch->SetLightingChannels(Cell.Visible,!Cell.Visible,false);
    if(!Cell.Visible)
    {
        auto* Dim=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/EnvironmentInterpretations/M_AltarPaintMemory.M_AltarPaintMemory"));
        if(!Dim) return nullptr;
        for(int32 I=0;I<Mesh->GetStaticMaterials().Num();++I)Batch->SetMaterial(I,Dim);
    }
    AddInstanceComponent(Batch);Batch->RegisterComponent();LiveBatches.Add(Name,Batch);return Batch;
}

void ADungeonPrototype::VerifySpecialBatch2()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;const bool OriginalStyle=SculptedCreatures;bool Passed=true;
    const TArray<FString> Keys={TEXT("altar_unaligned"),TEXT("altar_chaotic"),TEXT("altar_neutral"),TEXT("altar_lawful"),TEXT("altar_other")};
    const auto Painted=[&Passed](UInstancedStaticMeshComponent* B,bool Memory)
    {
        if(!B || !B->GetStaticMesh()){Passed=false;return;}
        const auto* Data=B->GetStaticMesh()->GetRenderData();
        Passed &= Data && Data->LODResources.Num()>0 && Data->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
        for(int32 I=0;I<B->GetStaticMesh()->GetStaticMaterials().Num();++I)
            Passed &= GetNameSafe(B->GetMaterial(I)).EndsWith(TEXT("Memory"))==Memory;
    };
    for(int32 Style=0;Style<2;++Style)
    {
        for(const FString& Key:Keys)for(bool Visible:{false,true})
        {
            FNetHackCell C;C.Kind=TEXT("terrain");C.Terrain=Key;C.Visible=Visible;
            auto* B=GetAltarBatch(C);Painted(B,!Visible);
            Passed &= B && B->GetStaticMesh()->GetName()==TEXT("SM_")+Key;
            // A displayed monster may cover the altar while retaining known background terrain.
            C.Kind=TEXT("monster");C.DisplayMonster=TEXT("shopkeeper");Passed &= GetAltarBatch(C)==B;
            C.Kind=TEXT("unknown");Passed &= GetAltarBatch(C)==nullptr;
        }
        for(bool Female:{false,true})
        {
            FNetHackCell C;C.Kind=TEXT("monster");C.DisplayMonster=TEXT("shopkeeper");C.Female=Female;C.Visible=true;C.TileIndex=554+(Female?1:0);
            auto* B=GetDefaultTileBatch(C,false);
            if(SculptedCreatures){Painted(B,false);Passed &= B && B->GetStaticMesh()->GetName()==TEXT("SM_shopkeeper");}
            else if(B)Passed &= !B->GetStaticMesh()->GetName().StartsWith(TEXT("SM_shopkeeper.")) && B->GetStaticMesh()->GetName()!=TEXT("SM_shopkeeper");
            Passed &= AddTileFallback(C,0,0);
        }
        HandleLiveKey(EKeys::F9,false);
    }
    for(const FString& T:{FString(TEXT("floor")),FString(TEXT("fountain")),FString(TEXT("sink")),FString(TEXT("altar_unknown"))})
    {FNetHackCell C;C.Kind=TEXT("terrain");C.Terrain=T;Passed &= GetAltarBatch(C)==nullptr;}
    FNetHackCell Unknown;Unknown.DisplayMonster=TEXT("unmapped fixture");Passed &= GetDefaultTileBatch(Unknown,false)==nullptr;
    Passed &= Turn==Session->Turn && Sequence==Session->Sequence && OriginalStyle==SculptedCreatures;
    RebuildLiveMap();
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewSpecialBatch2")))
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
                const auto& C=Session->Cells[Near.Y*Columns+Near.X];
                if(!C.Visible || C.Terrain!=TEXT("floor") || C.Kind!=TEXT("terrain"))Penalty+=100;
            }
            return Penalty;
        };
        Floors.Sort([&Score](const FIntPoint& A,const FIntPoint& B){return Score(A)<Score(B);});
        int32 Offset=0;FParse::Value(FCommandLine::Get(),TEXT("AltarPreviewOffset="),Offset);Offset=FMath::Clamp(Offset,0,3);
        const int32 Count=FMath::Min(3,Keys.Num()-Offset);Passed &= Floors.Num()>=Count+1 && SculptedCreatures;
        if(Floors.Num()>=Count+1)
        {
            FNetHackCell C;C.Kind=TEXT("monster");C.DisplayMonster=TEXT("shopkeeper");C.Visible=true;
            if(auto* B=GetDefaultTileBatch(C,false))B->AddInstance(FTransform(FRotator(0,15,0),CellPosition(Floors[0].X,Floors[0].Y,8),FVector(1)));
            for(int32 I=0;I<Count;++I)
            {
                C.Kind=TEXT("terrain");C.DisplayMonster.Empty();C.Terrain=Keys[Offset+I];
                if(auto* B=GetAltarBatch(C))B->AddInstance(FTransform(FQuat::Identity,CellPosition(Floors[I+1].X,Floors[I+1].Y,8),FVector(1)));
            }
        }
    }
    UE_LOG(LogTemp,Display,TEXT("SPECIAL_BATCH2_CHECK %s shopkeeper_sexes=2 altar_variants=5 styles=2 memory=2 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),Turn,Session->Turn,Sequence,Session->Sequence);
    if(!Passed)FPlatformMisc::RequestExitWithStatus(false,1);
}

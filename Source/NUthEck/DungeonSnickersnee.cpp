#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"

void ADungeonPrototype::VerifySnickersnee()
{
    const auto SavedCells=Session->Cells;const auto Hero=Session->Hero;
    const bool Style=SculptedCreatures;const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    bool Good=false;for(const auto& C:SavedCells)if(C.Kind==TEXT("item") && C.DisplayObject==TEXT("katana") && C.DisplayArtifact==TEXT("Snickersnee"))Good=true;
    int32 Cases=0;
    for(bool Mode:{false,true})for(bool Visible:{false,true}) {
        SculptedCreatures=Mode;FNetHackCell C;C.Kind=TEXT("item");C.DisplayObject=TEXT("katana");C.DisplayArtifact=TEXT("Snickersnee");C.Visible=Visible;
        auto* Named=GetDisplayedObjectBatch(C);Good &= Named && Named->GetStaticMesh();
        if(Named && Named->GetStaticMesh()) {
            Good &= Named->GetStaticMesh()->GetName()==TEXT("SM_snickersnee");
            const auto T=GetDisplayedObjectTransform(C,4,4,Named->GetStaticMesh());const auto B=Named->GetStaticMesh()->GetBoundingBox().TransformBy(T);
            Good &= FMath::IsNearlyEqual(B.Min.Z,26.f,.02f) && T.TransformVectorNoScale(FVector::UpVector).Z>.99f;
            Good &= B.GetSize().X<CellSize*.90f && B.GetSize().Y<CellSize*.90f && B.Max.Z<125.f;
            for(int32 I=0;I<Named->GetStaticMesh()->GetStaticMaterials().Num();++I)Good &= Named->GetMaterial(I) && (Visible || GetNameSafe(Named->GetMaterial(I)).EndsWith(TEXT("Memory")));
            C.DisplayArtifact.Empty();auto* Ordinary=GetDisplayedObjectBatch(C);Good &= Ordinary && Ordinary!=Named;
            if(Ordinary && Ordinary->GetStaticMesh()) {
                Good &= Ordinary->GetStaticMesh()->GetName()==TEXT("SM_katana");
                const auto Flat=GetDisplayedObjectTransform(C,4,4,Ordinary->GetStaticMesh());
                Good &= FMath::Abs(Flat.TransformVectorNoScale(FVector::UpVector).Z)<.01f;
            }
            C.DisplayArtifact=TEXT("Pretender");Good &= GetDisplayedObjectBatch(C)==Ordinary;
            C.DisplayArtifact=TEXT("Cleaver");Good &= GetDisplayedObjectBatch(C)==Ordinary;
            C.DisplayArtifact=TEXT("Snickersnee");C.Kind=TEXT("monster");Good &= GetDisplayedObjectBatch(C)==nullptr;
            C.Kind=TEXT("unknown");Good &= GetDisplayedObjectBatch(C)==nullptr;
            C.Kind=TEXT("item");C.DisplayObject=TEXT("long sword");Good &= GetDisplayedObjectBatch(C)!=Named;
        }
        ++Cases;
    }
    const auto Snapshot=[this]() {TMap<FName,int32> R;for(const auto& P:LiveBatches)if(P.Value->GetInstanceCount()>0)R.Add(P.Key,P.Value->GetInstanceCount());return R;};
    Session->Cells.Init(FNetHackCell(),Rows*Columns);Session->Hero=FIntPoint(8,8);int32 Covered=0;
    for(bool Mode:{false,true})for(bool Visible:{false,true}) {
        SculptedCreatures=Mode;FNetHackCell C;C.Kind=TEXT("item");C.Terrain=TEXT("floor");C.DisplayObject=TEXT("katana");C.DisplayArtifact=TEXT("Snickersnee");C.Visible=Visible;
        Session->Cells[4*Columns+4]=C;RebuildLiveMap();const auto Floor=Snapshot();
        for(const FString Terrain:{TEXT("altar_lawful"),TEXT("fountain"),TEXT("sink"),TEXT("trap")}) {
            C.Terrain=Terrain;Session->Cells[4*Columns+4]=C;RebuildLiveMap();const auto Now=Snapshot();bool Same=Floor.Num()==Now.Num();
            for(const auto& P:Floor){const auto* N=Now.Find(P.Key);Same &= N && *N==P.Value;}
            Good &= Same && Session->Cells[4*Columns+4].Terrain==Terrain;++Covered;
        }
        Session->Hero=FIntPoint(4,4);RebuildLiveMap();auto* B=GetDisplayedObjectBatch(C);Good &= B && B->GetInstanceCount()==0;Session->Hero=FIntPoint(8,8);
    }
    Session->Cells=SavedCells;Session->Hero=Hero;SculptedCreatures=Style;RebuildLiveMap();HandleLiveKey(EKeys::F9,false);HandleLiveKey(EKeys::F9,false);
    Good &= Turn==Session->Turn && Sequence==Session->Sequence && Style==SculptedCreatures;
    UE_LOG(LogTemp,Display,TEXT("SNICKERSNEE_CHECK %s cases=%d covered_features=%d turn=%d sequence=%d"),Good?TEXT("PASS"):TEXT("FAIL"),Cases,Covered,Turn,Sequence);
    if(!Good)FPlatformMisc::RequestExitWithStatus(false,1);
}

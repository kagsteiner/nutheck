#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Components/PointLightComponent.h"
#include "Misc/CommandLine.h"

bool ADungeonPrototype::IsOracleCell(int32 X,int32 Y) const
{
    if(!Session || Session->OracleCenter.X<0)return false;
    const auto D=FIntPoint(X,Y)-Session->OracleCenter;
    return FMath::Abs(D.X)<=6 && FMath::Abs(D.Y)<=5;
}

bool ADungeonPrototype::AddOracleArchitecture(const FNetHackCell& C,int32 X,int32 Y)
{
    if(!IsOracleCell(X,Y) || C.Kind==TEXT("unknown"))return false;
    for(bool Memory:{false,true}) {
        const FName Name(Memory?TEXT("OracleFloorMemory"):TEXT("OracleFloor"));
        if(!LiveBatches.Contains(Name))LiveBatches.Add(Name,MakeBatch(*Name.ToString(),TEXT("/Engine/BasicShapes/Cube.Cube"),FLinearColor(.48f,.45f,.36f)*(Memory?.40f:1.f)));
    }
    if(C.Terrain!=TEXT("wall"))return false;
    const FName Key(C.Visible?TEXT("OracleWall"):TEXT("OracleWallMemory"));
    auto* Found=LiveBatches.Find(Key);
    if(!Found) {
        auto* Mesh=LoadObject<UStaticMesh>(nullptr,TEXT("/Game/OracleSanctuary/Meshes/SM_oracle_wall.SM_oracle_wall"));
        if(!Mesh)return false;
        auto* B=NewObject<UInstancedStaticMeshComponent>(this,Key);B->SetupAttachment(RootComponent);B->SetStaticMesh(Mesh);
        B->SetCollisionEnabled(ECollisionEnabled::NoCollision);B->SetCastShadow(true);B->SetLightingChannels(C.Visible,!C.Visible,false);
        if(!C.Visible)for(int32 I=0;I<Mesh->GetStaticMaterials().Num();++I) {
            const FString Name=GetNameSafe(Mesh->GetMaterial(I))+TEXT("Memory");
            auto* M=LoadObject<UMaterialInterface>(nullptr,*(TEXT("/Game/OracleSanctuary/")+Name+TEXT(".")+Name));
            if(M)B->SetMaterial(I,M);
        }
        AddInstanceComponent(B);B->RegisterComponent();LiveBatches.Add(Key,B);Found=LiveBatches.Find(Key);
    }
    const auto D=FIntPoint(X,Y)-Session->OracleCenter;
    const bool Vertical=FMath::Abs(D.X)==6 || (FMath::Abs(D.X)==2 && FMath::Abs(D.Y)<=2);
    (*Found)->AddInstance(FTransform(FRotator(0,Vertical?90:0,0),CellPosition(X,Y,0),FVector(1)));
    return true;
}

void ADungeonPrototype::VerifyOracleSanctuary()
{
    bool Good=Session->OracleCenter.X>=0;
    const int32 Turn=Session->Turn,Seq=Session->Sequence;const bool Style=SculptedCreatures;
    for(int32 S=0;S<2;++S) {
        RebuildLiveMap();int32 Expected=0,Actual=0;
        for(int32 Y=0;Y<Rows;++Y)for(int32 X=0;X<Columns;++X) {
            const auto& C=Session->Cells[Y*Columns+X];
            if(IsOracleCell(X,Y) && C.Kind==TEXT("terrain") && C.Terrain==TEXT("wall") && Session->Hero!=FIntPoint(X,Y))++Expected;
        }
        for(const FName Key:{FName(TEXT("OracleWall")),FName(TEXT("OracleWallMemory"))})if(auto* B=LiveBatches.Find(Key)) {
            Actual+=(*B)->GetInstanceCount();Good &= (*B)->GetStaticMesh()!=nullptr;
            for(int32 I=0;I<(*B)->GetInstanceCount();++I) {
                FTransform T;(*B)->GetInstanceTransform(I,T,true);
                const int32 X=FMath::RoundToInt(T.GetLocation().X/CellSize+(Columns-1)*.5f),Y=FMath::RoundToInt(T.GetLocation().Y/CellSize+(Rows-1)*.5f);
                Good &= X>=0 && X<Columns && Y>=0 && Y<Rows;
                if(X>=0 && X<Columns && Y>=0 && Y<Rows)Good &= Session->Cells[Y*Columns+X].Kind==TEXT("terrain");
            }
        }
        Good &= Expected>0 && Actual==Expected;
        HandleLiveKey(EKeys::F9,false);
    }
    const auto SavedCells=Session->Cells;const auto SavedCenter=Session->OracleCenter;
    const auto WallCount=[this]() {int32 N=0;for(const FName K:{FName(TEXT("OracleWall")),FName(TEXT("OracleWallMemory"))})if(auto* B=LiveBatches.Find(K))N+=(*B)->GetInstanceCount();return N;};
    RebuildLiveMap();const int32 Baseline=WallCount();int32 Probe=-1;
    for(int32 I=0;I<Session->Cells.Num();++I)if(IsOracleCell(I%Columns,I/Columns) && Session->Cells[I].Kind==TEXT("terrain") && Session->Cells[I].Terrain==TEXT("wall")){Probe=I;break;}
    Good &= Probe>=0;
    if(Probe>=0) {
        Session->Cells[Probe].Kind=TEXT("unknown");RebuildLiveMap();Good &= WallCount()==Baseline-1;
        Session->Cells[Probe]=SavedCells[Probe];Session->Cells[Probe].Kind=TEXT("item");Session->Cells[Probe].DisplayObject=TEXT("dagger");RebuildLiveMap();Good &= WallCount()==Baseline-1;
    }
    Session->Cells=SavedCells;Session->OracleCenter=FIntPoint(-1,-1);RebuildLiveMap();Good &= WallCount()==0;
    Session->OracleCenter=SavedCenter;RebuildLiveMap();Good &= WallCount()==Baseline;
    int32 Fountains=0,BlueLights=0;
    for(int32 I=0;I<Session->Cells.Num();++I) {
        const auto& C=Session->Cells[I];
        if(IsOracleCell(I%Columns,I/Columns) && C.Visible && C.PermanentLight && C.Kind==TEXT("terrain") && C.Terrain==TEXT("fountain") && Session->Hero!=FIntPoint(I%Columns,I/Columns))++Fountains;
    }
    for(const auto& L:AtmosphereLights)if(L->IsVisible() && L->AttenuationRadius==140.f)++BlueLights;
    Good &= Fountains==BlueLights;
    Good &= Turn==Session->Turn && Seq==Session->Sequence && Style==SculptedCreatures;
    UE_LOG(LogTemp,Display,TEXT("ORACLE_SANCTUARY_CHECK %s center=%s"),Good?TEXT("PASS"):TEXT("FAIL"),*Session->OracleCenter.ToString());
    if(!Good)FPlatformMisc::RequestExitWithStatus(false,1);
}

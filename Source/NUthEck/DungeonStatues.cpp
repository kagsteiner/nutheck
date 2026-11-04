#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"
#include "Misc/PackageName.h"
#include "StaticMeshResources.h"

UInstancedStaticMeshComponent* ADungeonPrototype::GetDisplayedStatueBatch(const FNetHackCell& C)
{
    if(C.Kind!=TEXT("item") || C.DisplayObject!=TEXT("statue") || C.DisplayStatue.IsEmpty())return nullptr;
    FString Key;
    for(TCHAR Ch:C.DisplayStatue.ToLower()) {
        if(FChar::IsAlnum(Ch))Key.AppendChar(Ch);
        else if(!Key.IsEmpty() && !Key.EndsWith(TEXT("_")))Key.AppendChar('_');
    }
    Key.RemoveFromEnd(TEXT("_"));
    if(C.Female && FPackageName::DoesPackageExist(TEXT("/Game/CreatureInterpretations/Meshes/SM_")+Key+TEXT("_female")))Key+=TEXT("_female");
    FString Package=TEXT("/Game/CreatureInterpretations/Meshes/SM_")+Key;
    if(!FPackageName::DoesPackageExist(Package)) {
        const FString Player=Key+(C.Female?TEXT("_female_human"):TEXT("_male_human"));
        const FString PlayerPackage=TEXT("/Game/CreatureInterpretations/Meshes/SM_")+Player;
        if(FPackageName::DoesPackageExist(PlayerPackage))Package=PlayerPackage;
        else Package=TEXT("/Game/DefaultTiles/Meshes/SM_")+Key+(C.Female?TEXT("_female"):TEXT("_male"));
    }
    if(!FPackageName::DoesPackageExist(Package))return nullptr;
    const FName BatchName(*(TEXT("Statue_")+Key+(C.Female?TEXT("_F"):TEXT("_M"))+(C.Visible?TEXT(""):TEXT("_Memory"))));
    if(auto* Existing=LiveBatches.Find(BatchName))return Existing->Get();
    auto* Mesh=LoadObject<UStaticMesh>(nullptr,*(Package+TEXT(".")+FPackageName::GetShortName(Package)));
    const FString Material=C.Visible?TEXT("/Game/Statues/M_WhiteMarble.M_WhiteMarble"):TEXT("/Game/Statues/M_WhiteMarbleMemory.M_WhiteMarbleMemory");
    auto* Marble=LoadObject<UMaterialInterface>(nullptr,*Material);
    if(!Mesh || !Marble)return nullptr;
    auto* B=NewObject<UInstancedStaticMeshComponent>(this,BatchName);B->SetupAttachment(RootComponent);B->SetStaticMesh(Mesh);
    B->SetCollisionEnabled(ECollisionEnabled::NoCollision);B->SetCastShadow(true);B->SetLightingChannels(C.Visible,!C.Visible,false);
    // Every slot is marble, including eyes, hair, equipment and metal fittings.
    // Component overrides leave the living mesh and all shared materials intact.
    for(int32 I=0;I<Mesh->GetStaticMaterials().Num();++I)B->SetMaterial(I,Marble);
    AddInstanceComponent(B);B->RegisterComponent();LiveBatches.Add(BatchName,B);return B;
}

FTransform ADungeonPrototype::GetDisplayedStatueTransform(int32 X,int32 Y,UStaticMesh* Mesh) const
{
    if(!Mesh)return FTransform::Identity;
    const FTransform Rotation(FRotator(0,15,0));
    const FBox Rotated=Mesh->GetBoundingBox().TransformBy(Rotation);
    const FVector Size=Rotated.GetSize();
    const float Scale=FMath::Min(1.f,CellSize*.88f/FMath::Max(1.f,FMath::Max(Size.X,Size.Y)));
    const FTransform Local(Rotation.GetRotation(),FVector::ZeroVector,FVector(Scale));
    const FBox Bounds=Mesh->GetBoundingBox().TransformBy(Local);
    const FVector Center=Bounds.GetCenter();
    return FTransform(Local.GetRotation(),CellPosition(X,Y,9)-FVector(Center.X,Center.Y,Bounds.Min.Z),Local.GetScale3D());
}

void ADungeonPrototype::VerifyStatues()
{
    const bool Style=SculptedCreatures;const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    bool Good=true;int32 Checks=0,Native=0;
    for(int32 I=0;I<Session->Cells.Num();++I) {
        const auto& C=Session->Cells[I];
        if(IsOracleCell(I%Columns,I/Columns) && C.Kind==TEXT("item") && C.DisplayObject==TEXT("statue")) {
            ++Native;Good &= !C.DisplayStatue.IsEmpty() && GetDisplayedStatueBatch(C)!=nullptr;
        }
    }
    Good &= Native==8;
    for(const FString Name:{TEXT("plains centaur"),TEXT("forest centaur"),TEXT("mountain centaur"),TEXT("Oracle"),TEXT("goblin"),TEXT("soldier ant"),TEXT("gnomish wizard")})
        for(bool Female:{false,true})for(bool Visible:{false,true})for(bool Sculpted:{false,true}) {
            FNetHackCell C;C.Kind=TEXT("item");C.DisplayObject=TEXT("statue");C.DisplayStatue=Name;C.Female=Female;C.Visible=Visible;
            SculptedCreatures=Sculpted;auto* B=GetDisplayedStatueBatch(C);Good &= B && B->GetStaticMesh();
            if(!B || !B->GetStaticMesh())continue;
            UStaticMesh* Mesh=B->GetStaticMesh();const auto* D=Mesh->GetRenderData();Good &= D && D->LODResources.Num()>0 && D->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
            for(int32 I=0;I<Mesh->GetStaticMaterials().Num();++I) {
                Good &= GetNameSafe(B->GetMaterial(I))==(Visible?TEXT("M_WhiteMarble"):TEXT("M_WhiteMarbleMemory"));
                Good &= GetNameSafe(Mesh->GetMaterial(I))!=TEXT("M_WhiteMarble");
            }
            const FBox Bounds=Mesh->GetBoundingBox().TransformBy(GetDisplayedStatueTransform(0,0,Mesh));
            const FVector Center=CellPosition(0,0,0);
            Good &= FMath::IsNearlyEqual(Bounds.Min.Z,9.f,.02f) && FMath::Abs(Bounds.GetCenter().X-Center.X)<.02f && FMath::Abs(Bounds.GetCenter().Y-Center.Y)<.02f;
            Good &= Bounds.GetSize().X<=CellSize*.881f && Bounds.GetSize().Y<=CellSize*.881f;
            C.Kind=TEXT("monster");Good &= GetDisplayedStatueBatch(C)==nullptr;
            C.Kind=TEXT("item");C.DisplayStatue.Empty();Good &= GetDisplayedStatueBatch(C)==nullptr;
            C.DisplayStatue=Name;C.DisplayObject=TEXT("dagger");Good &= GetDisplayedStatueBatch(C)==nullptr;++Checks;
        }
    for(const FString Name:{TEXT("plains centaur"),TEXT("forest centaur"),TEXT("mountain centaur")})for(bool Female:{false,true}) {
        FNetHackCell C;C.Kind=TEXT("monster");C.DisplayMonster=Name;C.Female=Female;
        SculptedCreatures=true;auto* Living=GetDefaultTileBatch(C,false);Good &= Living && Living->GetStaticMesh();
        if(Living && Living->GetStaticMesh())Good &= Living->GetStaticMesh()->GetName().StartsWith(TEXT("SM_")) && GetNameSafe(Living->GetMaterial(0))!=TEXT("M_WhiteMarble");
        SculptedCreatures=false;auto* Default=GetDefaultTileBatch(C,false);Good &= !Default || Default!=Living;
    }
    FNetHackCell Bad;Bad.Kind=TEXT("item");Bad.DisplayObject=TEXT("statue");Bad.DisplayStatue=TEXT("unbuilt statue test");Good &= GetDisplayedStatueBatch(Bad)==nullptr;
    SculptedCreatures=Style;RebuildLiveMap();HandleLiveKey(EKeys::F9,false);HandleLiveKey(EKeys::F9,false);
    Good &= Style==SculptedCreatures && Turn==Session->Turn && Sequence==Session->Sequence;
    UE_LOG(LogTemp,Display,TEXT("STATUES_CHECK %s native_oracle=%d model_cases=%d centaur_aliases=6 turn=%d sequence=%d"),Good?TEXT("PASS"):TEXT("FAIL"),Native,Checks,Turn,Sequence);
    if(!Good)FPlatformMisc::RequestExitWithStatus(false,1);
}

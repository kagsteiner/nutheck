#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "Materials/MaterialInterface.h"
#include "Misc/PackageName.h"
#include "Misc/CommandLine.h"

namespace {
enum class EObjectPose { Legacy, Standing, Lying, Hover };
struct FObjectPresentation { const TCHAR* Name; const TCHAR* Key; const TCHAR* Folder; EObjectPose Pose; float Scale; };
const FObjectPresentation ObjectPresentations[]={
    {TEXT("large box"),TEXT("large_box"),TEXT("/Game/ObjectInterpretations"),EObjectPose::Legacy,1.0f},
    {TEXT("chest"),TEXT("chest"),TEXT("/Game/ObjectInterpretations"),EObjectPose::Legacy,1.0f},
    {TEXT("gold piece"),TEXT("gold_piece"),TEXT("/Game/ObjectInterpretations"),EObjectPose::Legacy,1.0f},
    {TEXT("corpse"),TEXT("corpse"),TEXT("/Game/ObjectInterpretations"),EObjectPose::Legacy,1.0f},
    {TEXT("long sword"),TEXT("long_sword"),TEXT("/Game/WeaponBatch1"),EObjectPose::Lying,0.66f},
    {TEXT("scimitar"),TEXT("scimitar"),TEXT("/Game/WeaponBatch1"),EObjectPose::Lying,0.66f},
    {TEXT("katana"),TEXT("katana"),TEXT("/Game/WeaponBatch1"),EObjectPose::Lying,0.66f},
    {TEXT("dagger"),TEXT("dagger"),TEXT("/Game/WeaponBatch2"),EObjectPose::Lying,1.0f},
    {TEXT("short sword"),TEXT("short_sword"),TEXT("/Game/WeaponBatch2"),EObjectPose::Lying,0.85f},
    {TEXT("spear"),TEXT("spear"),TEXT("/Game/WeaponBatch2"),EObjectPose::Lying,0.42f},
    {TEXT("leather armor"),TEXT("leather_armor"),TEXT("/Game/ArmorStudy"),EObjectPose::Standing,1.0f},
    {TEXT("studded leather armor"),TEXT("studded_leather_armor"),TEXT("/Game/ArmorStudy"),EObjectPose::Standing,1.0f},
    {TEXT("chain mail"),TEXT("chain_mail"),TEXT("/Game/ArmorStudy"),EObjectPose::Standing,1.0f},
    {TEXT("banded mail"),TEXT("banded_mail"),TEXT("/Game/ArmorStudy"),EObjectPose::Standing,1.0f},
    {TEXT("elven mithril-coat"),TEXT("elven_mithril_coat"),TEXT("/Game/ArmorStudy"),EObjectPose::Standing,1.0f},
    {TEXT("dwarvish mithril-coat"),TEXT("dwarvish_mithril_coat"),TEXT("/Game/ArmorStudy"),EObjectPose::Standing,1.0f},
    {TEXT("dwarvish cloak"),TEXT("dwarvish_cloak"),TEXT("/Game/ArmorStudy"),EObjectPose::Standing,1.0f},
    {TEXT("plate mail"),TEXT("plate_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("crystal plate mail"),TEXT("crystal_plate_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("bronze plate mail"),TEXT("bronze_plate_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("gray dragon scale mail"),TEXT("gray_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("gold dragon scale mail"),TEXT("gold_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("silver dragon scale mail"),TEXT("silver_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("red dragon scale mail"),TEXT("red_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("white dragon scale mail"),TEXT("white_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("orange dragon scale mail"),TEXT("orange_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("black dragon scale mail"),TEXT("black_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("blue dragon scale mail"),TEXT("blue_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("green dragon scale mail"),TEXT("green_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("yellow dragon scale mail"),TEXT("yellow_dragon_scale_mail"),TEXT("/Game/ArmorBatch2"),EObjectPose::Standing,1.0f},
    {TEXT("war hammer"),TEXT("mjollnir"),TEXT("/Game/ArtifactInterpretations"),EObjectPose::Hover,0.9f},
    {TEXT("battle-axe"),TEXT("cleaver"),TEXT("/Game/ArtifactInterpretations/Cleaver"),EObjectPose::Hover,0.62f},
};
const FObjectPresentation* FindObjectPresentation(const FNetHackCell& Cell)
{
    if(Cell.Kind!=TEXT("item")) return nullptr;
    for(const auto& Spec:ObjectPresentations)
    {
        if(Cell.DisplayObject!=Spec.Name) continue;
        if(Spec.Pose==EObjectPose::Hover &&
            Cell.DisplayArtifact!=(FString(Spec.Key)==TEXT("mjollnir")?TEXT("Mjollnir"):TEXT("Cleaver"))) continue;
        return &Spec;
    }
    return nullptr;
}
}

UInstancedStaticMeshComponent* ADungeonPrototype::GetDisplayedObjectBatch(const FNetHackCell& Cell)
{
    if(Cell.Kind!=TEXT("item")) return nullptr;
    const auto* Spec=FindObjectPresentation(Cell);
    if(!Spec) return nullptr;
    const FString Key=Spec->Key;
    const FString Package=FString(Spec->Folder)+TEXT("/Meshes/SM_")+Key;
    if(!FPackageName::DoesPackageExist(Package)) return nullptr;
    const FName BatchName(*(TEXT("Object_")+Key+(Cell.Visible?TEXT(""):TEXT("_Memory"))));
    if(auto* Existing=LiveBatches.Find(BatchName)) return Existing->Get();
    auto* Mesh=LoadObject<UStaticMesh>(nullptr,*(Package+TEXT(".SM_")+Key));
    if(!Mesh) return nullptr;
    auto* Batch=NewObject<UInstancedStaticMeshComponent>(this,BatchName);
    Batch->SetupAttachment(RootComponent);Batch->SetStaticMesh(Mesh);
    Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision);Batch->SetCastShadow(true);
    Batch->SetLightingChannels(Cell.Visible,!Cell.Visible,false);
    if(!Cell.Visible)
        for(int32 Slot=0;Slot<Mesh->GetStaticMaterials().Num();++Slot)
        {
            const FString Name=GetNameSafe(Mesh->GetMaterial(Slot))+TEXT("Memory");
            auto* Material=LoadObject<UMaterialInterface>(nullptr,*(FString(Spec->Folder)+TEXT("/")+Name+TEXT(".")+Name));
            if(Material) Batch->SetMaterial(Slot,Material);
        }
    AddInstanceComponent(Batch);Batch->RegisterComponent();LiveBatches.Add(BatchName,Batch);
    return Batch;
}


FTransform ADungeonPrototype::GetDisplayedObjectTransform(const FNetHackCell& Cell,int32 X,int32 Y,UStaticMesh* Mesh) const
{
    const auto* Spec=FindObjectPresentation(Cell);
    if(!Spec || !Mesh || Spec->Pose==EObjectPose::Legacy)
        return FTransform(FRotator(0,15,0),CellPosition(X,Y,8),FVector(1));
    // Source models stand along Z. Roll lays their broad XZ face on the floor.
    const bool Lying=Spec->Pose==EObjectPose::Lying;
    const float Yaw=Lying?float((X*37+Y*17)%120)-60.f:15.f;
    const FTransform Local(FRotator(0,Yaw,Lying?90.f:0.f),FVector::ZeroVector,FVector(Spec->Scale));
    const FBox Bounds=Mesh->GetBoundingBox().TransformBy(Local);
    // Floor cubes are 16 cm deep and centered at cell Z=0.
    const float SupportPlane=8.f;
    const float Clearance=SupportPlane+(Spec->Pose==EObjectPose::Hover?18.f:4.f);
    const FVector Center=Bounds.GetCenter();
    return FTransform(Local.GetRotation(),CellPosition(X,Y,Clearance)-FVector(Center.X,Center.Y,Bounds.Min.Z),Local.GetScale3D());
}

void ADungeonPrototype::VerifyObjectPlacement()
{
    bool Passed=true;
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    const bool SavedStyle=SculptedCreatures;
    for(int32 Style=0;Style<2;++Style) {
    for(const auto& Spec:ObjectPresentations)
        for(bool Visible:{false,true})
        {
            FNetHackCell Cell;Cell.Kind=TEXT("item");Cell.DisplayObject=Spec.Name;Cell.Visible=Visible;
            if(Spec.Pose==EObjectPose::Hover) Cell.DisplayArtifact=FString(Spec.Key)==TEXT("mjollnir")?TEXT("Mjollnir"):TEXT("Cleaver");
            auto* Batch=GetDisplayedObjectBatch(Cell);
            bool Good=Batch && Batch->GetStaticMesh();
            if(Good)
            {
                UStaticMesh* Mesh=Batch->GetStaticMesh();
                const auto* RenderData=Mesh->GetRenderData();
                Good &= RenderData && RenderData->LODResources.Num()>0;
                if(RenderData && RenderData->LODResources.Num()>0)
                    Good &= RenderData->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
                const auto Transform=GetDisplayedObjectTransform(Cell,0,0,Mesh);
                if(Spec.Pose!=EObjectPose::Legacy)
                {
                    const FBox Bounds=Mesh->GetBoundingBox().TransformBy(Transform);
                    Good &= FMath::IsNearlyEqual(Bounds.Min.Z,Spec.Pose==EObjectPose::Hover?26.0:12.0,0.01);
                    const FVector Axis=Transform.TransformVectorNoScale(FVector::UpVector);
                    Good &= Spec.Pose==EObjectPose::Lying?FMath::Abs(Axis.Z)<0.01:Axis.Z>0.99;
                }
                for(int32 Slot=0;Slot<Mesh->GetStaticMaterials().Num();++Slot)
                {
                    Good &= Batch->GetMaterial(Slot)!=nullptr;
                    Good &= Visible || GetNameSafe(Batch->GetMaterial(Slot)).EndsWith(TEXT("Memory"));
                }
            }
            Passed &= Good;
            UE_LOG(LogTemp,Display,TEXT("OBJECT_PLACEMENT_CASE %s visible=%d %s"),Spec.Key,Visible,Good?TEXT("PASS"):TEXT("FAIL"));
        }
    HandleLiveKey(EKeys::F9,false);
    }
    Passed &= SavedStyle==SculptedCreatures;
    FNetHackCell Probe;Probe.Kind=TEXT("monster");Probe.DisplayObject=TEXT("long sword");
    Passed &= GetDisplayedObjectBatch(Probe)==nullptr;
    Probe.Kind=TEXT("item");Probe.DisplayObject=TEXT("war hammer");Probe.DisplayArtifact=TEXT("Cleaver");
    Passed &= GetDisplayedObjectBatch(Probe)==nullptr;
    Probe.DisplayArtifact.Empty();Passed &= GetDisplayedObjectBatch(Probe)==nullptr;
    Passed &= Session->Turn==Turn && Session->Sequence==Sequence;
    RebuildLiveMap();
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewObjectPlacement")))
    {
        TArray<FIntPoint> Floors;
        for(int32 Y=0;Y<Rows;++Y) for(int32 X=0;X<Columns;++X)
        {
            const auto& Cell=Session->Cells[Y*Columns+X];
            if(Cell.Visible && Cell.Terrain==TEXT("floor") && Cell.Kind==TEXT("terrain") && FIntPoint(X,Y)!=Session->Hero) Floors.Add(FIntPoint(X,Y));
        }
        const auto Score=[this](const FIntPoint& At) {
            int32 Penalty=(At-Session->Hero).SizeSquared();
            // Keep capture fixtures clear of the hero and native glyph billboards.
            if(Penalty<5) Penalty+=2000;
            for(int32 DY=-1;DY<=1;++DY) for(int32 DX=-1;DX<=1;++DX) {
                const FIntPoint Near=At+FIntPoint(DX,DY);
                if(Near.X>=0 && Near.X<Columns && Near.Y>=0 && Near.Y<Rows &&
                    Session->Cells[Near.Y*Columns+Near.X].Kind!=TEXT("terrain")) Penalty+=1000;
            }
            for(int32 DY=-1;DY<=1;++DY) for(int32 DX=-1;DX<=1;++DX) {
                const FIntPoint Near=At+FIntPoint(DX,DY);
                if(Near.X<0 || Near.X>=Columns || Near.Y<0 || Near.Y>=Rows) {Penalty+=40;continue;}
                const auto& Cell=Session->Cells[Near.Y*Columns+Near.X];
                if(!Cell.Visible || Cell.Terrain!=TEXT("floor")) Penalty+=40;
            }
            return Penalty;
        };
        Floors.Sort([&Score](const FIntPoint& A,const FIntPoint& B){return Score(A)<Score(B);});
        const TCHAR* Names[]={TEXT("dagger"),TEXT("short sword"),TEXT("spear"),TEXT("battle-axe"),TEXT("crystal plate mail")};
        const int32 PreviewCount=FParse::Param(FCommandLine::Get(),TEXT("PreviewWeaponBatch2"))?3:5;
        Passed &= Floors.Num()>=PreviewCount;
        if(Floors.Num()>=PreviewCount) for(int32 I=0;I<PreviewCount;++I)
        {
            FNetHackCell Cell;Cell.Kind=TEXT("item");Cell.DisplayObject=Names[I];Cell.Visible=true;
            if(I==3) Cell.DisplayArtifact=TEXT("Cleaver");
            if(auto* Batch=GetDisplayedObjectBatch(Cell)) Batch->AddInstance(GetDisplayedObjectTransform(Cell,Floors[I].X,Floors[I].Y,Batch->GetStaticMesh()));
        }
    }
    UE_LOG(LogTemp,Display,TEXT("OBJECT_PLACEMENT_CHECK %s"),Passed?TEXT("PASS"):TEXT("FAIL"));
    if(!Passed) FPlatformMisc::RequestExitWithStatus(false,1);
}


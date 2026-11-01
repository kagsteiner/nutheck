#include "DungeonPrototype.h"
#include "OfficialTileAtlas.h"
#include "Camera/CameraComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "Misc/CommandLine.h"

bool ADungeonPrototype::AddTileFallback(const FNetHackCell& Cell,int32 X,int32 Y,bool Hero)
{
    if(Cell.TileIndex<0 || Cell.TileIndex>=OfficialTileCount
        || (!Hero && Cell.Kind!=TEXT("item") && Cell.Kind!=TEXT("monster") && Cell.Kind!=TEXT("pet") && Cell.Kind!=TEXT("effect"))) return false;
    const FName Name=Hero?TEXT("PlayerTileFallback"):TEXT("TileFallback");
    auto* Found=LiveBatches.Find(Name);
    UInstancedStaticMeshComponent* Batch=Found?Found->Get():nullptr;
    if(!Batch)
    {
        auto* Mesh=LoadObject<UStaticMesh>(nullptr,TEXT("/Game/TileFallback/SM_TileStandee.SM_TileStandee"));
        if(!Mesh) return false;
        Batch=NewObject<UInstancedStaticMeshComponent>(this,Name);Batch->SetupAttachment(RootComponent);
        Batch->NumCustomDataFloats=2;Batch->SetStaticMesh(Mesh);
        Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision);Batch->SetCastShadow(false);
        AddInstanceComponent(Batch);Batch->RegisterComponent();LiveBatches.Add(Name,Batch);
    }
    const float Size=Hero?1.05f:Cell.Kind==TEXT("item")?.64f:.90f;
    const FVector Anchor=CellPosition(X,Y,8);
    const FVector Toward=Camera->ProjectionMode==ECameraProjectionMode::Orthographic?-Camera->GetForwardVector():(Camera->GetComponentLocation()-Anchor).GetSafeNormal();
    const FQuat Facing=FRotationMatrix::MakeFromYZ(-Toward,FVector::UpVector).ToQuat();
    const FVector Position=Anchor-Facing.GetAxisZ()*Size*100.f*OfficialTileBottomPadding[Cell.TileIndex]/16.f;
    const int32 Instance=Batch->AddInstance(FTransform(Facing,Position,FVector(Size)));
    Batch->SetCustomDataValue(Instance,0,float(Cell.TileIndex),false);
    Batch->SetCustomDataValue(Instance,1,Cell.Visible || Hero?1.f:.20f,true);
    if(Hero) Batch->SetVisibility(!IsFirstPerson());
    return true;
}

void ADungeonPrototype::UpdateTileFallbackFacing()
{
    // Face the view in both projections, preserving the tile's aspect on screen.
    for(const FName Name:{FName(TEXT("TileFallback")),FName(TEXT("PlayerTileFallback"))})
        if(auto* Found=LiveBatches.Find(Name))
        {
            auto* Batch=Found->Get();bool Changed=false;
            for(int32 I=0;I<Batch->GetInstanceCount();++I)
            {
                FTransform Transform;Batch->GetInstanceTransform(I,Transform,true);
                const int32 Tile=FMath::RoundToInt(Batch->PerInstanceSMCustomData[I*2]);
                const float Bottom=Transform.GetScale3D().Z*100.f*OfficialTileBottomPadding[Tile]/16.f;
                const FVector Anchor=Transform.GetLocation()+Transform.GetRotation().GetAxisZ()*Bottom;
                const FVector Toward=Camera->ProjectionMode==ECameraProjectionMode::Orthographic?-Camera->GetForwardVector():(Camera->GetComponentLocation()-Anchor).GetSafeNormal();
                const FQuat Rotation=FRotationMatrix::MakeFromYZ(-Toward,FVector::UpVector).ToQuat();
                if(!Rotation.Equals(Transform.GetRotation(),.0001f))
                {
                    Transform.SetRotation(Rotation);Transform.SetLocation(Anchor-Rotation.GetAxisZ()*Bottom);
                    Batch->UpdateInstanceTransform(I,Transform,true,false,true);
                    Changed=true;
                }
            }
            if(Changed) Batch->MarkRenderStateDirty();
        }
}

void ADungeonPrototype::VerifyTileFallback()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;bool Passed=true;
    // Source indices selected from the generated atlas, independent of gameplay identities.
    const TArray<int32> Tiles={4,OfficialTileDemoMonster,OfficialTileDemoItem};
    const TArray<FString> Kinds={TEXT("monster"),TEXT("monster"),TEXT("item")};
    for(int32 I=0;I<Tiles.Num();++I) for(bool Visible:{false,true})
    {
        FNetHackCell Probe;Probe.Kind=Kinds[I];Probe.Visible=Visible;Probe.TileIndex=Tiles[I];
        Passed &= AddTileFallback(Probe,0,0);
        auto* Found=LiveBatches.Find(TEXT("TileFallback"));
        if(!Found) { Passed=false;continue; }
        const auto* Batch=Found->Get();const int32 Index=Batch->GetInstanceCount()-1;
        Passed &= Batch->NumCustomDataFloats==2 && Index>=0;
        if(Index>=0)
        {
            Passed &= Batch->PerInstanceSMCustomData[Index*2]==Tiles[I];
            Passed &= FMath::IsNearlyEqual(Batch->PerInstanceSMCustomData[Index*2+1],Visible?1.f:.20f);
        }
        Passed &= Batch->GetStaticMesh() && Batch->GetStaticMesh()->GetRenderData()->LODResources[0].GetNumTriangles()==2;
    }
    FNetHackCell Bad;Bad.Kind=TEXT("item");Bad.TileIndex=-1;Passed &= !AddTileFallback(Bad,0,0);
    Bad.TileIndex=OfficialTileCount;Passed &= !AddTileFallback(Bad,0,0);
    Bad.TileIndex=4;Bad.Kind=TEXT("terrain");Passed &= !AddTileFallback(Bad,0,0);
    // Camera-facing cards retain orientation at compass and eye-level views.
    const FTransform SavedCamera=Camera->GetComponentTransform();
    const auto SavedProjection=Camera->ProjectionMode;Camera->ProjectionMode=ECameraProjectionMode::Perspective;
    for(int32 Heading=0;Heading<8;++Heading)
    {
        const float A=FMath::DegreesToRadians(Heading*45.f);
        Camera->SetWorldLocation(CellPosition(0,0,80)+FVector(FMath::Cos(A)*300,FMath::Sin(A)*300,0));
        UpdateTileFallbackFacing();
        if(auto* Found=LiveBatches.Find(TEXT("TileFallback")))
            for(int32 I=0;I<(*Found)->GetInstanceCount();++I)
            {
                FTransform T;(*Found)->GetInstanceTransform(I,T,true);
                const int32 Tile=FMath::RoundToInt((*Found)->PerInstanceSMCustomData[I*2]);
                const FVector Anchor=T.GetLocation()+T.GetRotation().GetAxisZ()*T.GetScale3D().Z*100.f*OfficialTileBottomPadding[Tile]/16.f;
                const FVector Toward=(Camera->GetComponentLocation()-Anchor).GetSafeNormal();
                Passed &= FVector::DotProduct(T.TransformVectorNoScale(FVector(0,-1,0)),Toward)>.999f;
                Passed &= T.TransformVectorNoScale(FVector::UpVector).Z>.5f;
                Passed &= FMath::IsNearlyEqual(Anchor.Z,8.f,.01f);
            }
    }
    Camera->SetWorldTransform(SavedCamera);Camera->ProjectionMode=SavedProjection;
    FNetHackCell Hero;Hero.TileIndex=OfficialTileDemoMonster;Hero.Visible=true;
    Passed &= AddTileFallback(Hero,Session->Hero.X,Session->Hero.Y,true);
    const bool SavedFirst=FirstPerson;const float SavedBlend=FirstPersonBlend;
    const FVector SavedFocus=CameraFocus;const float SavedZoom=ZoomFactor;
    FirstPerson=true;FirstPersonBlend=1;FitCamera();
    if(auto* Found=LiveBatches.Find(TEXT("PlayerTileFallback"))) Passed &= !(*Found)->IsVisible();else Passed=false;
    FirstPerson=false;FirstPersonBlend=0;FitCamera();
    if(auto* Found=LiveBatches.Find(TEXT("PlayerTileFallback"))) Passed &= (*Found)->IsVisible();else Passed=false;
    FirstPerson=SavedFirst;FirstPersonBlend=SavedBlend;CameraFocus=SavedFocus;ZoomFactor=SavedZoom;FitCamera();
    for(const FString& Name:{FString(TEXT("large box")),FString(TEXT("chest")),FString(TEXT("gold piece"))})
    {
        FNetHackCell Model;Model.Kind=TEXT("item");Model.DisplayObject=Name;Model.Visible=true;
        Passed &= GetDisplayedObjectBatch(Model)!=nullptr;
    }
    HandleLiveKey(EKeys::F9,false);HandleLiveKey(EKeys::F9,false);
    Passed &= Session->Turn==Turn && Session->Sequence==Sequence;
    RebuildLiveMap();
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewTileFallback")))
    {
        TArray<FIntPoint> Floors;
        for(int32 Y=0;Y<Rows;++Y) for(int32 X=0;X<Columns;++X)
        {
            const auto& C=Session->Cells[Y*Columns+X];
            if(C.Visible && C.Terrain==TEXT("floor") && C.Kind==TEXT("terrain") && FIntPoint(X,Y)!=Session->Hero) Floors.Add(FIntPoint(X,Y));
        }
        const auto Nearby=Floors.FilterByPredicate([this](const FIntPoint& At){return (At-Session->Hero).SizeSquared()<=9;});
        if(Nearby.Num()>=3) Floors=Nearby;
        const auto Score=[this](const FIntPoint& At)
        {
            int32 Penalty=(At-Session->Hero).SizeSquared();
            for(int32 DY=-1;DY<=1;++DY) for(int32 DX=-1;DX<=1;++DX)
            {
                const FIntPoint Near=At+FIntPoint(DX,DY);
                if(Near.X<0 || Near.X>=Columns || Near.Y<0 || Near.Y>=Rows) { Penalty+=40;continue; }
                const auto& C=Session->Cells[Near.Y*Columns+Near.X];
                if(!C.Visible || C.Terrain!=TEXT("floor")) Penalty+=40;
            }
            return Penalty;
        };
        Floors.Sort([&Score](const FIntPoint& A,const FIntPoint& B){return Score(A)<Score(B);});
        Passed &= Floors.Num()>=3;
        if(Floors.Num()>=3) for(int32 I=0;I<3;++I)
        {
            FNetHackCell Probe;Probe.Kind=Kinds[I];Probe.Visible=true;Probe.TileIndex=Tiles[I];
            Passed &= AddTileFallback(Probe,Floors[I].X,Floors[I].Y);
        }
    }
    UpdateTileFallbackFacing();
    UE_LOG(LogTemp,Display,TEXT("TILE_FALLBACK_CHECK %s tiles=3 visible_memory=2 quad_triangles=2 invalid=3 model_priority=3 camera_headings=8 player_hide_restore=1 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),Turn,Session->Turn,Sequence,Session->Sequence);
    if(!Passed) FPlatformMisc::RequestExitWithStatus(false,1);
}

#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"
#include "StaticMeshResources.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/PlayerController.h"

UInstancedStaticMeshComponent* ADungeonPrototype::GetSokobanBatch(const TCHAR* Key,bool Memory)
{
    const FString Name=FString(TEXT("Soko_"))+Key+(Memory?TEXT("Memory"):TEXT(""));
    if(auto* Existing=LiveBatches.Find(FName(*Name)))return Existing->Get();
    const FString Package=FString(TEXT("/Game/Sokoban/Meshes/SM_"))+Key;
    auto* Mesh=LoadObject<UStaticMesh>(nullptr,*(Package+TEXT(".SM_")+Key));
    if(!Mesh)return nullptr;
    auto* B=NewObject<UInstancedStaticMeshComponent>(this,FName(*Name));B->SetupAttachment(RootComponent);B->SetStaticMesh(Mesh);
    B->SetCollisionEnabled(ECollisionEnabled::NoCollision);B->SetCastShadow(true);B->SetLightingChannels(!Memory,Memory,false);
    if(Memory)for(int32 I=0;I<Mesh->GetStaticMaterials().Num();++I) {
        const FString Mat=GetNameSafe(Mesh->GetMaterial(I))+TEXT("Memory");
        if(auto* M=LoadObject<UMaterialInterface>(nullptr,*(TEXT("/Game/Sokoban/")+Mat+TEXT(".")+Mat)))B->SetMaterial(I,M);
    }
    AddInstanceComponent(B);B->RegisterComponent();LiveBatches.Add(FName(*Name),B);return B;
}

bool ADungeonPrototype::AddSokobanArchitecture(const FNetHackCell& C,int32 X,int32 Y)
{
    if(!Session->InSokoban || C.Kind==TEXT("unknown"))return false;
    const auto Add=[&](const TCHAR* Key,FRotator Rotation=FRotator::ZeroRotator) {
        if(auto* B=GetSokobanBatch(Key,!C.Visible))B->AddInstance(FTransform(Rotation,CellPosition(X,Y,0),FVector(1)));
    };
    if(C.Terrain==TEXT("wall")) {
        Add(TEXT("soko_wall"));
        if(Session->SokobanStage>=2)Add(TEXT("soko_trim"));
        if(Session->SokobanStage>=4)if(auto* B=GetSokobanBatch(TEXT("soko_trim"),!C.Visible))B->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y,-25),FVector(1)));
        return true;
    }
    // Trap identity comes only from the presented foreground. Topmost items,
    // creatures and hero have a neutral floor and cannot disclose a well below.
    if(C.Kind==TEXT("terrain") && C.Terrain==TEXT("trap") && (C.DisplayTrap==TEXT("pit") || C.DisplayTrap==TEXT("hole"))) {
        Add(C.DisplayTrap==TEXT("pit")?TEXT("soko_pit"):TEXT("soko_hole"));return true;
    }
    if(C.Terrain!=TEXT("down"))Add(TEXT("soko_floor"));
    if(C.Terrain==TEXT("up") || C.Terrain==TEXT("down") || C.Terrain==TEXT("open") || C.Terrain==TEXT("closed")) {
        Add(TEXT("soko_frame"),FRotator(0,(C.Terrain==TEXT("open") || C.Terrain==TEXT("closed"))?(C.Horizontal?0:90):0,0));
        // The upper vaults gain restrained additional bronze joints. This is
        // level-wide craftsmanship, never an object/solution/reward detector.
        if(Session->SokobanStage>=3)Add(TEXT("soko_trim"));
    }
    return false;
}

void ADungeonPrototype::UpdateSokobanAtmosphere()
{
    int32 Count=0;
    const auto Light=[&](FVector P,float Radius,float Lumens,FLinearColor Color) {
        if(Count==AtmosphereLights.Num()) {
            auto* L=NewObject<UPointLightComponent>(this);L->SetupAttachment(RootComponent);L->SetMobility(EComponentMobility::Movable);
            AddInstanceComponent(L);L->RegisterComponent();AtmosphereLights.Add(L);
        }
        auto* L=AtmosphereLights[Count++].Get();L->SetLightingChannels(true,false,false);L->IntensityUnits=ELightUnits::Lumens;
        L->SetWorldLocation(P);L->SetAttenuationRadius(Radius);L->SetSourceRadius(28);L->SetCastShadows(false);
        L->SetLightColor(Color);L->SetIntensity(Lumens);L->SetVolumetricScatteringIntensity(0);L->SetVisibility(true);
    };
    const FIntPoint Directions[]={FIntPoint(1,0),FIntPoint(0,1),FIntPoint(-1,0),FIntPoint(0,-1)};
    for(int32 Y=0;Y<Rows;++Y)for(int32 X=0;X<Columns;++X) {
        const auto& C=Session->Cells[Y*Columns+X];
        if(!C.Visible || !C.PermanentLight || C.Kind==TEXT("unknown"))continue;
        if(C.Terrain!=TEXT("wall") && C.Terrain!=TEXT("stone") && C.Terrain!=TEXT("none") && X%3==1 && Y%3==1)
            Light(CellPosition(X,Y,170),400,180,FLinearColor(1.f,.85f,.65f));
        if(C.Kind!=TEXT("terrain") || C.Terrain!=TEXT("wall") || (X+Y)%3!=0)continue;
        for(auto D:Directions) {
            const int32 NX=X+D.X,NY=Y+D.Y;if(NX<0 || NY<0 || NX>=Columns || NY>=Rows)continue;
            const auto& N=Session->Cells[NY*Columns+NX];
            if(!N.Visible || !N.PermanentLight || N.Terrain!=TEXT("floor"))continue;
            const FVector Position=CellPosition(X,Y,83)+FVector(D.X*47,D.Y*47,0);
            if(auto* B=GetSokobanBatch(TEXT("soko_lamp"),false))B->AddInstance(FTransform(FRotator(0,FMath::RadiansToDegrees(FMath::Atan2(float(D.Y),float(D.X)))-90,0),Position,FVector(1)));
            Light(Position+FVector(D.X*8,D.Y*8,0),260,90,FLinearColor(1.f,.66f,.34f));break;
        }
    }
    for(int32 I=Count;I<AtmosphereLights.Num();++I)AtmosphereLights[I]->SetVisibility(false);
}

FBox ADungeonPrototype::GetSokobanRenderBounds() const
{
    FBox Bounds(ForceInit);
    for(const auto& Entry:LiveBatches) {
        const auto* B=Entry.Value.Get();if(!B->GetStaticMesh())continue;
        for(int32 I=0;I<B->GetInstanceCount();++I) {
            FTransform T;B->GetInstanceTransform(I,T,true);Bounds+=B->GetStaticMesh()->GetBoundingBox().TransformBy(T);
        }
    }
    return Bounds;
}

void ADungeonPrototype::FrameSokobanCapture()
{
    const FBox Bounds=GetSokobanRenderBounds();if(!Bounds.IsValid)return;
    // Use the zoomed camera budget for both measurement and final framing.
    // Overview at 1x reserves a different HUD margin inside FitCamera.
    FollowHero=false;OverviewOrbitOffset.Pitch=-12.f;CameraFocus=Bounds.GetCenter();ZoomFactor=2.f;FitCamera();
    float Width=0,Height=0;
    for(int32 I=0;I<8;++I) {
        const FVector P=FVector((I&1)?Bounds.Max.X:Bounds.Min.X,(I&2)?Bounds.Max.Y:Bounds.Min.Y,(I&4)?Bounds.Max.Z:Bounds.Min.Z)-Bounds.GetCenter();
        Width=FMath::Max(Width,FMath::Abs(FVector::DotProduct(P,Camera->GetRightVector()))*2);
        Height=FMath::Max(Height,FMath::Abs(FVector::DotProduct(P,Camera->GetUpVector()))*2);
    }
    const float S=FMath::Clamp(LastViewport.X/1600.f,.65f,1.5f);
    const float Top=84*S,Bottom=LastViewport.Y-(LiveFooterHeight>0?LiveFooterHeight:214*S);
    const float Desired=FMath::Max(Width/.92f,Height*LastViewport.X/FMath::Max(1.f,(Bottom-Top)*.92f));
    ZoomFactor=FMath::Clamp(OverviewWidth/Desired,1.f,16.f);FitCamera();
    const float PixelScale=Camera->OrthoWidth/LastViewport.X;
    CameraFocus=Bounds.GetCenter()-Camera->GetUpVector()*(LastViewport.Y*.5f-(Top+Bottom)*.5f)*PixelScale;
    FitCamera();
}

bool ADungeonPrototype::ValidateSokobanCapture() const
{
    auto* PC=GetWorld()->GetFirstPlayerController();const FBox B=GetSokobanRenderBounds();bool Good=PC && B.IsValid;
    const float S=FMath::Clamp(LastViewport.X/1600.f,.65f,1.5f),Bottom=LastViewport.Y-(LiveFooterHeight>0?LiveFooterHeight:214*S);
    for(int32 I=0;I<8 && Good;++I) {
        FVector2D P;Good &= PC->ProjectWorldLocationToScreen(FVector((I&1)?B.Max.X:B.Min.X,(I&2)?B.Max.Y:B.Min.Y,(I&4)?B.Max.Z:B.Min.Z),P);
        Good &= P.X>=0 && P.X<=LastViewport.X && P.Y>=84*S && P.Y<=Bottom;
    }
    UE_LOG(LogTemp,Display,TEXT("SOKOBAN_CAMERA_CHECK %s zoom=%.3f"),Good?TEXT("PASS"):TEXT("FAIL"),ZoomFactor);return Good;
}

void ADungeonPrototype::VerifySokoban()
{
    const auto SavedCells=Session->Cells;const auto Hero=Session->Hero;const bool Branch=Session->InSokoban,Style=SculptedCreatures;
    const int32 Stage=Session->SokobanStage,Turn=Session->Turn,Seq=Session->Sequence;
    bool Good=Branch && Stage>=1 && Stage<=4;int32 NativeBoulders=0;
    const auto Count=[this](const TCHAR* Key) {
        int32 N=0;
        for(bool Memory:{false,true}) {
            const FString Name=FString(TEXT("Soko_"))+Key+(Memory?TEXT("Memory"):TEXT(""));
            if(auto* B=LiveBatches.Find(FName(*Name)))N+=(*B)->GetInstanceCount();
        }
        return N;
    };
    for(int32 Mode=0;Mode<2;++Mode) {
        RebuildLiveMap();int32 Walls=0,Pits=0,Holes=0;
        for(int32 I=0;I<Session->Cells.Num();++I) {
            const auto& C=Session->Cells[I];const bool IsHero=Hero==FIntPoint(I%Columns,I/Columns);
            if(C.Kind==TEXT("terrain") && !IsHero){Walls+=C.Terrain==TEXT("wall");Pits+=C.Terrain==TEXT("trap") && C.DisplayTrap==TEXT("pit");Holes+=C.Terrain==TEXT("trap") && C.DisplayTrap==TEXT("hole");}
            if(Mode==0 && C.Kind==TEXT("item") && C.DisplayObject==TEXT("boulder") && !IsHero)++NativeBoulders;
        }
        Good &= Walls>0 && Count(TEXT("soko_wall"))==Walls && Count(TEXT("soko_pit"))==Pits && Count(TEXT("soko_hole"))==Holes;
        for(bool Memory:{false,true})for(const TCHAR* Key:{TEXT("soko_wall"),TEXT("soko_floor"),TEXT("soko_pit"),TEXT("soko_hole"),TEXT("soko_frame"),TEXT("soko_trim"),TEXT("soko_lamp")}) {
            auto* B=GetSokobanBatch(Key,Memory);Good &= B && B->GetStaticMesh();
            if(B && B->GetStaticMesh())for(int32 I=0;I<B->GetStaticMesh()->GetStaticMaterials().Num();++I)Good &= B->GetMaterial(I) && (!Memory || GetNameSafe(B->GetMaterial(I)).EndsWith(TEXT("Memory")));
        }
        HandleLiveKey(EKeys::F9,false);
    }
    FNetHackCell Rock;Rock.Kind=TEXT("item");Rock.DisplayObject=TEXT("boulder");Rock.Visible=true;
    auto* B=GetDisplayedObjectBatch(Rock);Good &= B && B->GetStaticMesh() && NativeBoulders>0;
    if(B && B->GetStaticMesh()) {
        const auto T=GetDisplayedObjectTransform(Rock,0,0,B->GetStaticMesh());const FBox Box=B->GetStaticMesh()->GetBoundingBox().TransformBy(T);
        Good &= FMath::IsNearlyEqual(Box.Min.Z,8.f,.02f) && Box.GetSize().X<CellSize*.95f && Box.GetSize().Y<CellSize*.95f;
        Rock.DisplayMonster=TEXT("giant mimic");Good &= GetDisplayedObjectBatch(Rock)==B;
    }
    Session->Cells.Init(FNetHackCell(),Rows*Columns);Session->Hero=FIntPoint(8,8);const int32 At=4*Columns+4;
    for(const FString Trap:{TEXT("pit"),TEXT("hole")})for(bool Visible:{false,true}) {
        FNetHackCell C;C.Kind=TEXT("terrain");C.Terrain=TEXT("trap");C.DisplayTrap=Trap;C.Visible=Visible;Session->Cells[At]=C;RebuildLiveMap();
        Good &= Count(Trap==TEXT("pit")?TEXT("soko_pit"):TEXT("soko_hole"))==1;
        for(const FString Kind:{TEXT("item"),TEXT("monster"),TEXT("unknown")}) {
            Session->Cells[At].Kind=Kind;RebuildLiveMap();Good &= Count(TEXT("soko_pit"))==0 && Count(TEXT("soko_hole"))==0;
        }
        Session->Cells[At]=C;Session->Hero=FIntPoint(4,4);RebuildLiveMap();Good &= Count(TEXT("soko_pit"))==0 && Count(TEXT("soko_hole"))==0;Session->Hero=FIntPoint(8,8);
        C.Terrain=TEXT("floor");C.DisplayTrap.Empty();Session->Cells[At]=C;RebuildLiveMap();Good &= Count(TEXT("soko_floor"))==1;
    }
    Session->Cells[At].Kind=TEXT("terrain");Session->Cells[At].Terrain=TEXT("wall");Session->Cells[At].Visible=false;
    for(int32 S=1;S<=4;++S) {Session->SokobanStage=S;RebuildLiveMap();Good &= Count(TEXT("soko_wall"))==1 && Count(TEXT("soko_trim"))==(S==1?0:S==4?2:1);}
    Session->InSokoban=false;RebuildLiveMap();Good &= Count(TEXT("soko_wall"))==0;
    Session->InSokoban=true;Session->Cells[At].Terrain=TEXT("floor");
    for(bool Lit:{false,true})for(bool Visible:{false,true}) {
        Session->Cells[At].Visible=Visible;Session->Cells[At].PermanentLight=Lit;RebuildLiveMap();int32 Lights=0;for(const auto& L:AtmosphereLights)if(L->IsVisible())++Lights;
        Good &= Lights==(Lit && Visible?1:0);
    }
    Session->Cells=SavedCells;Session->Hero=Hero;Session->InSokoban=Branch;Session->SokobanStage=Stage;RebuildLiveMap();
    Good &= Style==SculptedCreatures && Turn==Session->Turn && Seq==Session->Sequence;
    UE_LOG(LogTemp,Display,TEXT("SOKOBAN_CHECK %s stage=%d native_boulders=%d turn=%d sequence=%d"),Good?TEXT("PASS"):TEXT("FAIL"),Stage,NativeBoulders,Turn,Seq);
    if(!Good)FPlatformMisc::RequestExitWithStatus(false,1);
}

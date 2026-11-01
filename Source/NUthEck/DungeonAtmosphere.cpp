#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/LocalFogVolumeComponent.h"
#include "Materials/MaterialInterface.h"
#include "Engine/SkyLight.h"
#include "Engine/TextureCube.h"
#include "Components/SkyLightComponent.h"

void ADungeonPrototype::CreateAmbientLight()
{
    // Constant environment radiance supplies light from every direction. It
    // neither captures unknown geometry nor introduces a sky or another sun.
    auto* Environment=UTextureCube::CreateTransient(16,16,PF_B8G8R8A8);
    check(Environment);
    Environment->SRGB=false;
    auto& Mip=Environment->GetPlatformData()->Mips[0];
    void* Pixels=Mip.BulkData.Lock(LOCK_READ_WRITE);
    FMemory::Memset(Pixels,255,Mip.BulkData.GetBulkDataSize());
    Mip.BulkData.Unlock();
    Environment->UpdateResource();
    auto* Ambient=GetWorld()->SpawnActor<ASkyLight>()->GetLightComponent();
    Ambient->SetMobility(EComponentMobility::Movable);
    Ambient->SourceType=SLS_SpecifiedCubemap;
    Ambient->bLowerHemisphereIsBlack=false;
    Ambient->SetCastShadows(false);
    Ambient->SetLightColor(FLinearColor(.88f,.90f,.94f));
    Ambient->SetIntensity(.6f);
    Ambient->SetCubemap(Environment);
}

// Cosmetic fixtures are a function of level coordinates, never discovery order
// or gameplay RNG. No presentation state needs to be written to native saves.
void ADungeonPrototype::UpdateAtmosphere()
{
    int32 LightCount=0,FogCount=0;
    const auto Light=[&](FVector Position,float Radius,float Lumens,bool Shadows) {
        if(LightCount==AtmosphereLights.Num())
        {
            auto* Component=NewObject<UPointLightComponent>(this);
            Component->SetupAttachment(RootComponent);
            Component->SetMobility(EComponentMobility::Movable);
            Component->IntensityUnits=ELightUnits::Lumens;
            Component->SetSourceRadius(5.f);
            AddInstanceComponent(Component);Component->RegisterComponent();
            AtmosphereLights.Add(Component);
        }
        auto* Component=AtmosphereLights[LightCount++].Get();
        Component->SetWorldLocation(Position);
        Component->SetAttenuationRadius(Radius);
        Component->SetLightColor(FLinearColor(1.f,.57f,.25f));
        Component->SetCastShadows(Shadows);
        Component->SetIntensity(Lumens);
        Component->SetVisibility(true);
    };
    const auto Batch=[&](const TCHAR* Name,const TCHAR* Mesh,FLinearColor Color) {
        const FName Key(Name);
        if(!LiveBatches.Contains(Key)) LiveBatches.Add(Key,MakeBatch(Name,Mesh,Color));
        return LiveBatches[Key].Get();
    };
    auto* Wax=Batch(TEXT("CandleWax"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.85f,.69f,.39f));
    auto* Iron=Batch(TEXT("CandleIron"),TEXT("/Engine/BasicShapes/Cube.Cube"),FLinearColor(.10f,.075f,.055f));
    auto* Flame=Batch(TEXT("CandleFlame"),TEXT("/Engine/BasicShapes/Sphere.Sphere"),FLinearColor(1.f,.5f,.1f));
    if(auto* Material=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Materials/M_CandleFlame.M_CandleFlame"))) Flame->SetMaterial(0,Material);
    Flame->SetCastShadow(false);
    for(int32 Y=0;Y<Rows;++Y) for(int32 X=0;X<Columns;++X)
    {
        const auto& Cell=Session->Cells[Y*Columns+X];
        if(!Cell.Visible || Cell.Kind==TEXT("unknown") || Cell.Terrain==TEXT("none") || Cell.Terrain==TEXT("stone")) continue;
        if(Cell.Terrain==TEXT("wall"))
        {
            // Each wall has a fixed candidate face. Unknown neighbours cannot
            // influence placement or be exposed by a decorative light source.
            const uint32 Seed=uint32(X)*73856093u ^ uint32(Y)*19349663u
                ^ uint32(Session->Depth)*83492791u ^ uint32(Session->Dungeon)*2654435761u;
            // Retain all original candidates and add a second seeded subset.
            if(Seed%3==2) continue;
            const FIntPoint Directions[]={FIntPoint(1,0),FIntPoint(0,1),FIntPoint(-1,0),FIntPoint(0,-1)};
            const auto D=Directions[(Seed/3)%4];
            const int32 NX=X+D.X,NY=Y+D.Y;
            if(NX<0 || NX>=Columns || NY<0 || NY>=Rows) continue;
            const auto& Adjacent=Session->Cells[NY*Columns+NX];
            if(!Adjacent.Visible || !Adjacent.PermanentLight || Adjacent.Terrain!=TEXT("floor")) continue;
            const FVector Position=CellPosition(X,Y,82)+FVector(D.X*57.f,D.Y*57.f,0);
            Iron->AddInstance(FTransform(FQuat::Identity,Position-FVector(0,0,10),FVector(.20f,.20f,.045f)));
            Wax->AddInstance(FTransform(FQuat::Identity,Position,FVector(.055f,.055f,.18f)));
            Flame->AddInstance(FTransform(FQuat::Identity,Position+FVector(0,0,12),FVector(.045f,.045f,.09f)));
            Light(Position+FVector(0,0,14),340.f,180.f,true);
            continue;
        }
        // Temporary light retains a warm accent within NH's visibility. Room
        // illumination comes from ambient light and actual candle fixtures.
        if((Cell.TemporaryLight && X%3==1 && Y%3==1)
            || (Cell.TemporaryLight && Session->Hero==FIntPoint(X,Y)))
            Light(CellPosition(X,Y,95),250.f,85.f,false);
        if(Cell.Terrain!=TEXT("floor") || (X+Y)%2!=0) continue;
        if(FogCount==AtmosphereFog.Num())
        {
            auto* Fog=NewObject<ULocalFogVolumeComponent>(this);
            Fog->SetupAttachment(RootComponent);
            Fog->SetMobility(EComponentMobility::Movable);
            Fog->RadialFogExtinction=.20f;
            Fog->HeightFogExtinction=0.f;
            Fog->FogAlbedo=FLinearColor(.55f,.63f,.70f);
            Fog->FogEmissive=FLinearColor(.015f,.02f,.025f);
            AddInstanceComponent(Fog);Fog->RegisterComponent();
            AtmosphereFog.Add(Fog);
        }
        auto* Fog=AtmosphereFog[FogCount++].Get();
        // Sphere stays inside this visible tile; its upper cap is floor haze.
        Fog->SetWorldLocation(CellPosition(X,Y,-18));
        Fog->SetWorldScale3D(FVector(49.f/ULocalFogVolumeComponent::GetBaseVolumeSize()));
        Fog->SetVisibility(true);
    }
    for(int32 I=LightCount;I<AtmosphereLights.Num();++I) AtmosphereLights[I]->SetVisibility(false);
    for(int32 I=FogCount;I<AtmosphereFog.Num();++I) AtmosphereFog[I]->SetVisibility(false);
}

void ADungeonPrototype::TickAtmosphere()
{
    // Gentle continuous flicker is decorative; it never advances a NH turn.
    const double Time=GetWorld()->GetTimeSeconds();
    for(auto& Light:AtmosphereLights)
        if(Light->IsVisible() && Light->AttenuationRadius==340.f)
        {
            const FVector P=Light->GetComponentLocation();
            Light->SetIntensity(180.f*(1.f+.04f*FMath::Sin(Time*5.3+P.X*.07+P.Y*.11)));
        }
    if(auto* Batch=LiveBatches.Find(FName(TEXT("CandleFlame"))))
    {
        for(int32 I=0;I<(*Batch)->GetInstanceCount();++I)
        {
            FTransform Transform;(*Batch)->GetInstanceTransform(I,Transform);
            const FVector P=Transform.GetLocation();
            const float Flicker=1.f+.07f*FMath::Sin(Time*5.3+P.X*.07+P.Y*.11);
            Transform.SetScale3D(FVector(.045f,.045f,.09f*Flicker));
            (*Batch)->UpdateInstanceTransform(I,Transform,false,false);
        }
        if((*Batch)->GetInstanceCount()>0) (*Batch)->MarkRenderStateDirty();
    }
}

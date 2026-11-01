#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"
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

    // This is map presentation, not dungeon illumination: only remembered
    // geometry receives the shadowless fill, on its separate lighting channel.
    for(const FVector Position:{FVector(-3500,-3000,7000),FVector(3500,3000,5000)})
    {
        auto* Fill=NewObject<UPointLightComponent>(this);
        Fill->SetupAttachment(RootComponent);
        Fill->SetMobility(EComponentMobility::Movable);
        Fill->bUseInverseSquaredFalloff=false;
        Fill->IntensityUnits=ELightUnits::Unitless;
        Fill->SetAttenuationRadius(50000.f);
        Fill->SetVolumetricScatteringIntensity(0.f);
        Fill->SetAffectTranslucentLighting(false);
        Fill->LightingChannels.bChannel0=false;
        Fill->LightingChannels.bChannel1=true;
        Fill->SetCastShadows(false);
        Fill->SetLightColor(FLinearColor(.80f,.86f,1.f));
        Fill->SetIntensity(0.f);
        AddInstanceComponent(Fill);Fill->RegisterComponent();
        Fill->SetWorldLocation(Position);
        MapFillLights.Add(Fill);
    }
}

void ADungeonPrototype::UpdateOverviewLighting()
{
    if(MistMaterial)
    {
        const float Detail=FMath::SmoothStep(1.f,2.4f,ZoomFactor);
        const float MistAmount=FMath::Lerp(Detail,1.f,FirstPersonBlend);
        MistMaterial->SetScalarParameterValue(TEXT("MistAmount"),MistAmount);
        if(auto* Mist=LiveBatches.Find(FName(TEXT("FloorMist")))) (*Mist)->SetVisibility(MistAmount>0.f);
    }
    // Full support at level scale, smoothly gone by room scale. Never alter
    // the candle-lit current view, native visibility, or first-person lighting.
    const float Amount=(1.f-FMath::SmoothStep(1.f,2.5f,ZoomFactor))*(1.f-FirstPersonBlend);
    for(int32 I=0;I<MapFillLights.Num();++I)
        MapFillLights[I]->SetIntensity(Amount*(I==0?1.8f:.6f));
}

// Cosmetic fixtures are a function of level coordinates, never discovery order
// or gameplay RNG. No presentation state needs to be written to native saves.
void ADungeonPrototype::UpdateAtmosphere()
{
    int32 LightCount=0;
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
    auto* Mist=Batch(TEXT("FloorMist"),TEXT("/Engine/BasicShapes/Plane.Plane"),FLinearColor::White);
    Mist->SetNumCustomDataFloats(1);
    if(!MistMaterial)
    {
        auto* Material=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Materials/M_DriftingMist.M_DriftingMist"));
        checkf(Material,TEXT("Run Scripts/CreateAtmosphereAssets.py to create the mist material."));
        MistMaterial=UMaterialInstanceDynamic::Create(Material,this);
        Mist->SetMaterial(0,MistMaterial);
    }
    Mist->SetCastShadow(false);
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
        if(Cell.Terrain!=TEXT("floor")) continue;
        int32 Edges=0;
        const FIntPoint Neighbours[]={FIntPoint(-1,0),FIntPoint(1,0),FIntPoint(0,-1),FIntPoint(0,1)};
        for(int32 I=0;I<4;++I)
        {
            const int32 NX=X+Neighbours[I].X,NY=Y+Neighbours[I].Y;
            if(NX<0 || NX>=Columns || NY<0 || NY>=Rows) { Edges|=1<<I;continue; }
            const auto& Near=Session->Cells[NY*Columns+NX];
            if(!Near.Visible || Near.Terrain!=TEXT("floor") || Near.Kind==TEXT("unknown")) Edges|=1<<I;
        }
        // World-space noise flows continuously across these layers. Geometry
        // never leaves its visible cell, even while the shader pattern drifts.
        for(float Height:{16.f,30.f,44.f})
        {
            const int32 Instance=Mist->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y,Height),FVector::OneVector));
            Mist->SetCustomDataValue(Instance,0,float(Edges),false);
        }
    }
    for(int32 I=LightCount;I<AtmosphereLights.Num();++I) AtmosphereLights[I]->SetVisibility(false);
    Mist->MarkRenderStateDirty();
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

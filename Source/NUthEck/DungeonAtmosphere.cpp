#include "DungeonPrototype.h"
#include "DungeonTopmost.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/PointLightComponent.h"
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
    const bool Cavern=IsMinesCavern();
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
        Component->SetLightingChannels(!Cavern,false,Cavern);
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
    UInstancedStaticMeshComponent* TorchWood=nullptr,*TorchFlame=nullptr;
    if(Cavern)
    {
        TorchWood=Batch(TEXT("TorchWood"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.16f,.065f,.025f));
        TorchFlame=Batch(TEXT("TorchFlame"),TEXT("/Engine/BasicShapes/Sphere.Sphere"),FLinearColor(1,.5f,.1f));
        if(auto* M=LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Materials/M_CandleFlame.M_CandleFlame")))TorchFlame->SetMaterial(0,M);
        TorchFlame->SetCastShadow(false);
    }
    for(int32 Y=0;Y<Rows;++Y) for(int32 X=0;X<Columns;++X)
    {
        const auto Cell=TopmostRenderCell(Session->Cells[Y*Columns+X],Session->Hero==FIntPoint(X,Y));
        if(!Cell.Visible || Cell.Kind==TEXT("unknown") || Cell.Terrain==TEXT("none") || Cell.Terrain==TEXT("stone")) continue;
        if(Cell.Terrain==TEXT("wall"))
        {
            // Each wall has a fixed candidate face. Unknown neighbours cannot
            // influence placement or be exposed by a decorative light source.
            const uint32 Seed=uint32(X)*73856093u ^ uint32(Y)*19349663u
                ^ uint32(Session->Depth)*83492791u ^ uint32(Session->Dungeon)*2654435761u;
            // Retain all original candidates and add a second seeded subset.
            if(Cavern?Seed%5!=0:Seed%3==2) continue;
            const FIntPoint Directions[]={FIntPoint(1,0),FIntPoint(0,1),FIntPoint(-1,0),FIntPoint(0,-1)};
            auto D=Directions[(Seed/3)%4];
            if(Cavern)
                for(int32 Face=0;Face<4;++Face)
                {
                    const auto Candidate=Directions[((Seed/3)+Face)%4];const auto P=FIntPoint(X,Y)+Candidate;
                    if(P.X<0 || P.X>=Columns || P.Y<0 || P.Y>=Rows)continue;
                    const auto& N=Session->Cells[P.Y*Columns+P.X];
                    if(N.Visible && N.PermanentLight && N.Terrain==TEXT("floor")){D=Candidate;break;}
                }
            const int32 NX=X+D.X,NY=Y+D.Y;
            if(NX<0 || NX>=Columns || NY<0 || NY>=Rows) continue;
            const auto& Adjacent=Session->Cells[NY*Columns+NX];
            if(!Adjacent.Visible || !Adjacent.PermanentLight || Adjacent.Terrain!=TEXT("floor")) continue;
            const FVector Position=CellPosition(X,Y,82)+FVector(D.X*57.f,D.Y*57.f,0);
            if(Cavern)
            {
                Iron->AddInstance(FTransform(FQuat::Identity,Position-FVector(D.X*6,D.Y*6,14),FVector(.13f,.13f,.09f)));
                TorchWood->AddInstance(FTransform(FRotator(D.Y*12,-D.X*12,0),Position-FVector(0,0,6),FVector(.05f,.05f,.32f)));
                TorchFlame->AddInstance(FTransform(FQuat::Identity,Position+FVector(0,0,14),FVector(.065f,.065f,.16f)));
                Light(Position+FVector(0,0,18),380.f,240.f,true);
                continue;
            }
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
    }
    for(int32 I=LightCount;I<AtmosphereLights.Num();++I) AtmosphereLights[I]->SetVisibility(false);
}

void ADungeonPrototype::TickAtmosphere()
{
    // Gentle continuous flicker is decorative; it never advances a NH turn.
    const double Time=GetWorld()->GetTimeSeconds();
    const auto FlickerAt=[Time](FVector P) {
        const double Phase=P.X*.07+P.Y*.11;
        return float(.55*FMath::Sin(Time*5.3+Phase)
            +.30*FMath::Sin(Time*9.7+Phase*1.73)
            +.15*FMath::Sin(Time*17.1+Phase*.61));
    };
    for(auto& Light:AtmosphereLights)
        if(Light->IsVisible() && (Light->AttenuationRadius==340.f || Light->AttenuationRadius==380.f))
        {
            const FVector P=Light->GetComponentLocation();
            const bool Torch=Light->AttenuationRadius==380.f;
            Light->SetIntensity((Torch?240.f:180.f)*(1.f+(Torch?.20f:.16f)*FlickerAt(P)));
        }
    for(const FName Key : {FName(TEXT("CandleFlame")),FName(TEXT("TorchFlame"))})
    if(auto* Batch=LiveBatches.Find(Key))
    {
        for(int32 I=0;I<(*Batch)->GetInstanceCount();++I)
        {
            FTransform Transform;(*Batch)->GetInstanceTransform(I,Transform);
            const FVector P=Transform.GetLocation();
            const float Flicker=FlickerAt(P);
            const bool Torch=Key==FName(TEXT("TorchFlame"));
            const float Width=Torch?.065f:.045f,Height=Torch?.16f:.09f;
            Transform.SetScale3D(FVector(Width*(1.f-.06f*Flicker),Width*(1.f-.06f*Flicker),Height*(1.f+.18f*Flicker)));
            (*Batch)->UpdateInstanceTransform(I,Transform,false,false);
        }
        if((*Batch)->GetInstanceCount()>0) (*Batch)->MarkRenderStateDirty();
    }
}

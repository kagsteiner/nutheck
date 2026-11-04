#include "DungeonPrototype.h"
#include "DungeonTopmost.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"

UStaticMesh* CreateDungeonCaveRock(UObject* Outer);

bool ADungeonPrototype::AddValkyrieArchitecture(const FNetHackCell& C,int32 X,int32 Y)
{
    if(!Session->ValkyrieQuest || C.Kind==TEXT("unknown"))return false;
    const int32 Stage=Session->ValkyrieStage;
    const bool Cold=Stage<=3,Home=Stage==1;
    const auto Part=[&](const TCHAR* Key,const TCHAR* Mesh,FVector Offset,FVector Scale) {
        const bool CaveLit=IsMoonlitValkyrieLevel() && C.Visible && C.PermanentLight;
        const FString Name=FString(TEXT("Val_"))+Key+(!C.Visible?TEXT("Memory"):CaveLit?TEXT("Lit"):TEXT(""));
        auto* Found=LiveBatches.Find(FName(*Name));
        if(!Found) {
            auto* B=MakeBatch(*Name,Mesh,FLinearColor::White);
            B->SetLightingChannels(C.Visible,!C.Visible,CaveLit);
            const bool CaveRock=FString(Key)==TEXT("CaveRock");
            if(CaveRock)B->SetStaticMesh(CreateDungeonCaveRock(B));
            const FString MaterialKey=CaveRock?TEXT("Basalt"):Key;
            const FString Path=FString(TEXT("/Game/ValkyrieQuest/M_"))+MaterialKey+TEXT(".M_")+MaterialKey;
            if(auto* Base=LoadObject<UMaterialInterface>(nullptr,*Path)) {
                auto* M=UMaterialInstanceDynamic::Create(Base,this);
                M->SetScalarParameterValue(TEXT("Memory"),C.Visible?1.f:.4f);B->SetMaterial(0,M);
            }
            LiveBatches.Add(FName(*Name),B);Found=LiveBatches.Find(FName(*Name));
        }
        (*Found)->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y,0)+Offset,Scale));
    };
    const TCHAR* Cube=TEXT("/Engine/BasicShapes/Cube.Cube");
    if(Stage==3 && C.Kind==TEXT("terrain") && C.Terrain==TEXT("stone")) {
        Part(TEXT("CaveRock"),Cube,FVector(0,0,88),FVector(1,1,1.6f));
        return true;
    }
    if(C.Terrain==TEXT("wall")) {
        Part(Home?TEXT("Sanctuary"):TEXT("Basalt"),TEXT("/Game/DefaultTiles/Meshes/SM_GreyWall.SM_GreyWall"),FVector(0,0,60),FVector(.99f,.99f,1.2f));
        if(Home) {
            Part(TEXT("Bronze"),Cube,FVector(0,0,112),FVector(.99f,.99f,.045f));
            Part(TEXT("Snow"),Cube,FVector(0,0,121),FVector(.96f,.96f,.055f));
        }
        return true;
    }
    // Only presented terrain selects ice/water/lava: foregrounds retain neutral paths.
    if(C.Terrain!=TEXT("down")) {
        const TCHAR* Key=C.DisplaySurface==TEXT("ice")?TEXT("Ice"):C.Terrain==TEXT("lava")?TEXT("Lava"):
            C.Terrain==TEXT("water")?TEXT("Water"):Home?TEXT("SanctuaryFloor"):Cold?TEXT("ColdRock"):TEXT("BasaltFloor");
        Part(Key,Cube,FVector(0,0,0),FVector(.995f,.995f,.16f));
    }
    return C.DisplaySurface==TEXT("ice") || C.Terrain==TEXT("lava") || C.Terrain==TEXT("water");
}

void ADungeonPrototype::UpdateValkyrieAtmosphere()
{
    int32 Count=0;
    const bool Cave=IsMoonlitValkyrieLevel();
    int32 ShadowCount=0;
    const auto Light=[&](FVector P,float Radius,float Power,FLinearColor Color,bool Shadows=false) {
        if(Count==AtmosphereLights.Num()) {
            auto* L=NewObject<UPointLightComponent>(this);L->SetupAttachment(RootComponent);
            L->SetMobility(EComponentMobility::Movable);AddInstanceComponent(L);L->RegisterComponent();AtmosphereLights.Add(L);
        }
        auto* L=AtmosphereLights[Count++].Get();L->SetLightingChannels(!Cave,false,Cave);
        L->IntensityUnits=ELightUnits::Lumens;L->SetWorldLocation(P);L->SetAttenuationRadius(Radius);
        L->SetSourceRadius(Cave?(Radius==650.f?160.f:65.f):90.f);L->SetCastShadows(Shadows);L->SetVolumetricScatteringIntensity(0);
        L->SetLightColor(Color);L->SetIntensity(Power);L->SetVisibility(true);
    };
    for(int32 Y=0;Y<Rows;++Y)for(int32 X=0;X<Columns;++X) {
        const auto C=TopmostRenderCell(Session->Cells[Y*Columns+X],Session->Hero==FIntPoint(X,Y));
        if(!C.Visible || !C.PermanentLight || C.Kind==TEXT("unknown"))continue;
        if(Cave) {
            // Lunar directional light replaces the former warm interior grid
            // and local blue entrance lamps. Lava is the only warm source.
            if(C.Kind==TEXT("terrain") && C.Terrain==TEXT("lava")) {
                const bool Shadows=ShadowCount<4;
                ShadowCount+=Shadows;
                Light(CellPosition(X,Y,55),420,260,FLinearColor(1.f,.24f,.045f),Shadows);
            }
            continue;
        }
        if(C.Kind==TEXT("terrain") && C.Terrain==TEXT("lava") && X%2==0 && Y%2==0)
            Light(CellPosition(X,Y,36),220,95,FLinearColor(1.f,.18f,.025f));
        else if(C.Terrain==TEXT("floor") && X%4==1 && Y%4==1)
            Light(CellPosition(X,Y,170),550,35,Session->ValkyrieStage<=3?FLinearColor(.57f,.77f,1.f):FLinearColor(1.f,.58f,.30f));
    }
    for(int32 I=Count;I<AtmosphereLights.Num();++I)AtmosphereLights[I]->SetVisibility(false);
}

void ADungeonPrototype::VerifyValkyrieQuest()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    bool Good=Session->ValkyrieQuest && Session->ValkyrieStage>=1 && Session->ValkyrieStage<=5;
    int32 Ice=0,Lava=0,Rock=0;
    for(int32 I=0;I<Session->Cells.Num();++I) {
        const auto C=TopmostRenderCell(Session->Cells[I],Session->Hero==FIntPoint(I%Columns,I/Columns));
        if(C.Kind==TEXT("unknown"))continue;
        Ice+=C.DisplaySurface==TEXT("ice");Lava+=C.Terrain==TEXT("lava");
        Rock+=Session->ValkyrieStage==3 && C.Kind==TEXT("terrain") && C.Terrain==TEXT("stone");
    }
    for(int32 Mode=0;Mode<2;++Mode) {
        RebuildLiveMap();int32 IceInstances=0,LavaInstances=0,RockInstances=0;
        for(const auto& B:LiveBatches) {
            if(B.Key.ToString().StartsWith(TEXT("Val_Ice")))IceInstances+=B.Value->GetInstanceCount();
            if(B.Key.ToString().StartsWith(TEXT("Val_Lava")))LavaInstances+=B.Value->GetInstanceCount();
            if(B.Key.ToString().StartsWith(TEXT("Val_CaveRock"))) {
                RockInstances+=B.Value->GetInstanceCount();
                for(int32 I=0;I<B.Value->GetInstanceCount();++I) {
                    FTransform T;B.Value->GetInstanceTransform(I,T);
                    Good &= T.GetTranslation().Z>80.f && T.GetScale3D().Z>1.5f;
                }
            }
        }
        Good &= Ice==IceInstances && Lava==LavaInstances && Rock==RockInstances;HandleLiveKey(EKeys::F9,false);
    }
    for(bool Visible:{false,true}) {
        FNetHackCell Probe;Probe.Kind=TEXT("item");Probe.DisplayObject=TEXT("crystal ball");Probe.Visible=Visible;
        auto* Ordinary=GetDisplayedObjectBatch(Probe);Probe.DisplayArtifact=TEXT("The Orb of Fate");
        auto* Named=GetDisplayedObjectBatch(Probe);Good &= Named && Named!=Ordinary;
        if(Named && Named->GetStaticMesh()) {
            const auto Bounds=Named->GetStaticMesh()->GetBoundingBox().TransformBy(GetDisplayedObjectTransform(Probe,4,4,Named->GetStaticMesh()));
            Good &= Bounds.Min.Z>=25.f && Bounds.Max.Z<125.f && Bounds.GetSize().X<90.f;
            if(!Visible)for(int32 I=0;I<Named->GetStaticMesh()->GetStaticMaterials().Num();++I)
                Good &= Named->GetMaterial(I) && GetNameSafe(Named->GetMaterial(I)).EndsWith(TEXT("Memory"));
        }
        Probe.DisplayArtifact=TEXT("Pretender");Good &= GetDisplayedObjectBatch(Probe)==Ordinary;
        Probe.Kind=TEXT("monster");Probe.DisplayArtifact=TEXT("The Orb of Fate");Good &= !GetDisplayedObjectBatch(Probe);
        Probe.Kind=TEXT("item");Probe.Terrain=TEXT("lava");Probe.DisplaySurface=TEXT("ice");
        const auto Presented=TopmostRenderCell(Probe,false);Good &= Presented.Terrain==TEXT("floor") && Presented.DisplaySurface.IsEmpty();
    }
    if(IsMoonlitValkyrieLevel()) {
        const auto SavedCells=Session->Cells;const auto SavedHero=Session->Hero;const int32 SavedStage=Session->ValkyrieStage;
        Session->Cells.Init(FNetHackCell(),Columns*Rows);Session->Hero=FIntPoint(70,19);
        const auto Cell=[this](int32 X,int32 Y,const TCHAR* Terrain,const TCHAR* Surface=TEXT("")) {
            auto& C=Session->Cells[Y*Columns+X];C.Kind=TEXT("terrain");C.Terrain=Terrain;
            C.DisplaySurface=Surface;C.Visible=true;C.PermanentLight=true;
        };
        Cell(10,10,TEXT("floor"));Cell(9,10,TEXT("floor"),TEXT("ice"));
        Cell(11,10,TEXT("lava"));Cell(12,10,TEXT("stone"));
        const auto HotLights=[&]() {
            int32 Hot=0,Shadows=0;
            for(const auto& L:AtmosphereLights)if(L->IsVisible()) {
                Good &= L->LightingChannels.bChannel2 && !L->LightingChannels.bChannel0 && !L->LightingChannels.bChannel1;
                Hot+=L->AttenuationRadius==420.f;Shadows+=L->CastShadows;
            }
            Good &= Shadows<=4;
            Good &= ValkyrieMoon && ValkyrieMoon->LightingChannels.bChannel2 && !ValkyrieMoon->LightingChannels.bChannel0 && !ValkyrieMoon->LightingChannels.bChannel1;
            Good &= ValkyrieMoon && ValkyrieMoon->IsVisible() && ValkyrieSky && ValkyrieSky->IsVisible();
            for(const auto& B:LiveBatches)if(B.Key.ToString().StartsWith(TEXT("Val_"))) {
                const FString Name=B.Key.ToString();
                Good &= B.Value->LightingChannels.bChannel2==Name.EndsWith(TEXT("Lit"));
            }
            return Hot;
        };
        RebuildLiveMap();Good &= HotLights()==1;
        auto& LavaProbe=Session->Cells[10*Columns+11];
        LavaProbe.Visible=false;LavaProbe.PermanentLight=false;RebuildLiveMap();Good &= HotLights()==0;
        LavaProbe.Visible=true;RebuildLiveMap();Good &= HotLights()==0;
        LavaProbe.PermanentLight=true;LavaProbe.Kind=TEXT("item");RebuildLiveMap();Good &= HotLights()==0;
        LavaProbe.Kind=TEXT("unknown");RebuildLiveMap();Good &= HotLights()==0;
        Session->ValkyrieStage=2;UpdateValkyrieSky();Good &= !ValkyrieSky->IsVisible() && !ValkyrieMoon->IsVisible();
        Session->ValkyrieStage=3;Session->ValkyrieQuest=false;UpdateValkyrieSky();Good &= !ValkyrieSky->IsVisible() && !ValkyrieMoon->IsVisible();
        Session->ValkyrieQuest=true;Session->ValkyrieStage=SavedStage;
        Session->Cells=SavedCells;Session->Hero=SavedHero;RebuildLiveMap();
        UE_LOG(LogTemp,Display,TEXT("VALKYRIE_CAVE_LIGHT_CHECK %s visible_lava=1 memory_unlit_foreground_unknown=0 channels=isolated shadows_max=4 moon_sky_lifecycle=pass"),Good?TEXT("PASS"):TEXT("FAIL"));
    }
    Good &= Turn==Session->Turn && Sequence==Session->Sequence;
    UE_LOG(LogTemp,Display,TEXT("VALKYRIE_QUEST_CHECK %s stage=%d ice=%d lava=%d turn=%d sequence=%d"),Good?TEXT("PASS"):TEXT("FAIL"),Session->ValkyrieStage,Ice,Lava,Turn,Sequence);
    if(!Good)FPlatformMisc::RequestExitWithStatus(false,1);
}

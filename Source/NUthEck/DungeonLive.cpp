#include "DungeonPrototype.h"
#include "Camera/CameraComponent.h"
#include "Camera/PlayerCameraManager.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "InputKeyEventArgs.h"
#include "Misc/CommandLine.h"
#include "Misc/PackageName.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "Materials/MaterialInterface.h"
#include "TimerManager.h"

void ADungeonPrototype::StartLiveGame(bool NewGame)
{
    if(LiveBatches.IsEmpty())
    {
        auto* Base=MakeBatch(TEXT("LiveFoundation"),TEXT("/Engine/BasicShapes/Cube.Cube"),FLinearColor(.014f,.022f,.027f));
        Base->AddInstance(FTransform(FQuat::Identity,FVector(0,0,-36),FVector(80,22,.45f)));
        const auto Add=[this](const TCHAR* Name,const TCHAR* Mesh,FLinearColor Color) {
            LiveBatches.Add(FName(Name),MakeBatch(Name,Mesh,Color));
        };
        const TCHAR* Cube=TEXT("/Engine/BasicShapes/Cube.Cube");
        Add(TEXT("Floor"),TEXT("/Game/DefaultTiles/Meshes/SM_GreyFloor.SM_GreyFloor"),FLinearColor(.27f,.28f,.29f));
        Add(TEXT("FloorMemory"),TEXT("/Game/DefaultTiles/Meshes/SM_GreyFloor.SM_GreyFloor"),FLinearColor(.075f,.08f,.085f));
        Add(TEXT("Wall"),TEXT("/Game/DefaultTiles/Meshes/SM_GreyWall.SM_GreyWall"),FLinearColor(.43f,.44f,.45f));
        Add(TEXT("WallMemory"),TEXT("/Game/DefaultTiles/Meshes/SM_GreyWall.SM_GreyWall"),FLinearColor(.14f,.15f,.16f));
        Add(TEXT("Mortar"),Cube,FLinearColor(.16f,.15f,.13f));
        Add(TEXT("MortarMemory"),Cube,FLinearColor(.045f,.043f,.039f));
        Add(TEXT("Door"),Cube,FLinearColor(.55f,.29f,.10f));
        Add(TEXT("DoorMemory"),Cube,FLinearColor(.16f,.085f,.03f));
        Add(TEXT("DoorFrame"),Cube,FLinearColor(.25f,.095f,.025f));
        Add(TEXT("DoorFrameMemory"),Cube,FLinearColor(.073f,.029f,.008f));
        Add(TEXT("DoorBrace"),Cube,FLinearColor(.34f,.14f,.035f));
        Add(TEXT("DoorBraceMemory"),Cube,FLinearColor(.10f,.042f,.011f));
        Add(TEXT("DoorHardware"),Cube,FLinearColor(.13f,.15f,.16f));
        Add(TEXT("DoorHardwareMemory"),Cube,FLinearColor(.039f,.045f,.048f));
        Add(TEXT("Water"),Cube,FLinearColor(.025f,.32f,.48f));
        Add(TEXT("WaterMemory"),Cube,FLinearColor(.01f,.08f,.12f));
        Add(TEXT("Lava"),Cube,FLinearColor(.7f,.12f,.02f));
        Add(TEXT("LavaMemory"),Cube,FLinearColor(.17f,.035f,.01f));
        Add(TEXT("Stairs"),Cube,FLinearColor(.71f,.77f,.67f));
        Add(TEXT("StairsMemory"),Cube,FLinearColor(.22f,.25f,.20f));
        Add(TEXT("Feature"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.33f,.48f,.63f));
        Add(TEXT("FeatureMemory"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.08f,.13f,.17f));
        Add(TEXT("Player"),TEXT("/Engine/BasicShapes/Cone.Cone"),FLinearColor(1,.65f,.13f));
        Add(TEXT("Monster"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.73f,.13f,.14f));
        Add(TEXT("Pet"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.56f,.36f,.85f));
        Add(TEXT("Item"),TEXT("/Engine/BasicShapes/Sphere.Sphere"),FLinearColor(.24f,.79f,.65f));
        Add(TEXT("ItemMemory"),TEXT("/Engine/BasicShapes/Sphere.Sphere"),FLinearColor(.06f,.20f,.16f));
        Add(TEXT("Trap"),TEXT("/Engine/BasicShapes/Cone.Cone"),FLinearColor(.85f,.4f,.18f));
        Add(TEXT("TrapMemory"),TEXT("/Engine/BasicShapes/Cone.Cone"),FLinearColor(.21f,.1f,.04f));
    }
    Session=MakeUnique<FNetHackSession>();
    Session->Start(NewGame || FParse::Param(FCommandLine::Get(),TEXT("NewGame")),!CaptureLive);
    LiveStartedTime=FPlatformTime::Seconds();
}

UInstancedStaticMeshComponent* ADungeonPrototype::GetDefaultTileBatch(const FNetHackCell& Cell,bool Hero)
{
    if(Cell.DisplayMonster.IsEmpty()) return nullptr;
    FString Key;
    for(TCHAR Character:Cell.DisplayMonster.ToLower())
    {
        if(FChar::IsAlnum(Character)) Key.AppendChar(Character);
        else if(!Key.IsEmpty() && !Key.EndsWith(TEXT("_"))) Key.AppendChar('_');
    }
    Key.RemoveFromEnd(TEXT("_"));
    const FString Species=Key;
    Key+=Cell.Female?TEXT("_female"):TEXT("_male");
    FString PlayerAsset;
    if(Hero && Session && Session->HeroRace==TEXT("human") && !Session->HeroPolymorphed)
    {
        if(Species==TEXT("valkyrie") && Cell.Female) PlayerAsset=TEXT("valkyrie_female_human");
        if(Species==TEXT("barbarian") && !Cell.Female) PlayerAsset=TEXT("barbarian_male_human");
    }
    FString CreatureAsset=Species;
    if(Cell.Female && (Species==TEXT("gnomish_wizard") || Species==TEXT("gnome_zombie"))) CreatureAsset+=TEXT("_female");
    const FString AssetKey=PlayerAsset.IsEmpty()?CreatureAsset:PlayerAsset;
    const FString SculptedPackage=TEXT("/Game/CreatureInterpretations/Meshes/SM_")+AssetKey;
    const bool Sculpted=SculptedCreatures && (!PlayerAsset.IsEmpty() || Species==TEXT("giant_ant") || Species==TEXT("little_dog") || Species==TEXT("goblin")
        || Species==TEXT("jackal") || Species==TEXT("fox") || Species==TEXT("gnome")
        || Species==TEXT("sewer_rat") || Species==TEXT("giant_rat") || Species==TEXT("gnome_ruler")
        || Species==TEXT("kitten") || Species==TEXT("housecat") || Species==TEXT("large_cat")
        || Species==TEXT("wolf") || Species==TEXT("winter_wolf_cub") || Species==TEXT("winter_wolf")
        || Species==TEXT("dog") || Species==TEXT("large_dog") || Species==TEXT("dingo")
        || Species==TEXT("coyote") || Species==TEXT("warg") || Species==TEXT("rabid_rat")
        || Species==TEXT("bat") || Species==TEXT("giant_bat") || Species==TEXT("vampire_bat")
        || Species==TEXT("jaguar") || Species==TEXT("lynx") || Species==TEXT("panther")
        || Species==TEXT("tiger") || Species==TEXT("hell_hound_pup") || Species==TEXT("hell_hound")
        || Species==TEXT("pony") || Species==TEXT("horse") || Species==TEXT("warhorse")
        || Species==TEXT("white_unicorn") || Species==TEXT("gray_unicorn") || Species==TEXT("black_unicorn") || Species==TEXT("kobold") || Species==TEXT("large_kobold") || Species==TEXT("kobold_leader") || Species==TEXT("kobold_shaman") || Species==TEXT("kobold_mummy") || Species==TEXT("kobold_zombie") || Species==TEXT("gnomish_wizard") || Species==TEXT("gnome_mummy") || Species==TEXT("gnome_zombie") || Species==TEXT("dwarf") || Species==TEXT("dwarf_leader") || Species==TEXT("dwarf_ruler") || Species==TEXT("dwarf_mummy") || Species==TEXT("dwarf_zombie") || Species==TEXT("hobgoblin") || Species==TEXT("hill_orc") || Species==TEXT("mordor_orc") || Species==TEXT("floating_eye") || Species==TEXT("newt") || Species==TEXT("lichen") || Species==TEXT("uruk_hai") || Species==TEXT("orc_shaman") || Species==TEXT("orc_captain") || Species==TEXT("grid_bug"))
        && FPackageName::DoesPackageExist(SculptedPackage);
    const FString Package=Sculpted?SculptedPackage:TEXT("/Game/DefaultTiles/Meshes/SM_")+Key;
    const FString ObjectName=Sculpted?TEXT("SM_")+AssetKey:TEXT("SM_")+Key;
    if(Sculpted) Key=TEXT("Sculpted_")+(PlayerAsset.IsEmpty()?Key:PlayerAsset);
    if(MissingTileFigures.Contains(Key)) return nullptr;
    const FName BatchName=Hero?FName(TEXT("PlayerVolume")):FName(*(TEXT("Tile_")+Key));
    auto* Existing=LiveBatches.Find(BatchName);
    if(Existing && (!Hero || HeroVolumeKey==Key)) return Existing->Get();
    if(!FPackageName::DoesPackageExist(Package)) { MissingTileFigures.Add(Key); return nullptr; }
    auto* Mesh=LoadObject<UStaticMesh>(nullptr,*(Package+TEXT(".")+ObjectName));
    if(!Mesh) { MissingTileFigures.Add(Key); return nullptr; }
    UInstancedStaticMeshComponent* Batch=Existing?Existing->Get():NewObject<UInstancedStaticMeshComponent>(this,BatchName);
    if(!Existing)
    {
        Batch->SetupAttachment(RootComponent); Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision);
        Batch->SetCastShadow(true); AddInstanceComponent(Batch); Batch->RegisterComponent();
        LiveBatches.Add(BatchName,Batch);
    }
    Batch->SetStaticMesh(Mesh);
    if(const auto* Data=Mesh->GetRenderData())
        if(Data->LODResources.Num()>0)
        {
            const auto& Colors=Data->LODResources[0].VertexBuffers.ColorVertexBuffer;
            int32 MaxColor=0;
            for(uint32 I=0;I<Colors.GetNumVertices();++I)
            {
                const FColor C=Colors.VertexColor(I);
                MaxColor=FMath::Max(MaxColor,int32(FMath::Max3(C.R,C.G,C.B)));
            }
            UE_LOG(LogTemp,Display,TEXT("DEFAULT_TILE_COLORS %s vertices=%u max=%d material=%s"),*Key,Colors.GetNumVertices(),MaxColor,*GetNameSafe(Mesh->GetMaterial(0)));
        }
    if(Hero) HeroVolumeKey=Key;
    UE_LOG(LogTemp,Display,TEXT("DEFAULT_TILE_FIGURE_LOADED %s hero=%d"),*Key,Hero);
    return Batch;
}

UInstancedStaticMeshComponent* ADungeonPrototype::GetDisplayedObjectBatch(const FNetHackCell& Cell)
{
    if(Cell.Kind!=TEXT("item")) return nullptr;
    FString Key;
    if(Cell.DisplayObject==TEXT("large box")) Key=TEXT("large_box");
    else if(Cell.DisplayObject==TEXT("chest")) Key=TEXT("chest");
    else if(Cell.DisplayObject==TEXT("gold piece")) Key=TEXT("gold_piece");
    else if(Cell.DisplayObject==TEXT("corpse")) Key=TEXT("corpse");
    else return nullptr;
    const FString Package=TEXT("/Game/ObjectInterpretations/Meshes/SM_")+Key;
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
            auto* Material=LoadObject<UMaterialInterface>(nullptr,*(TEXT("/Game/ObjectInterpretations/")+Name+TEXT(".")+Name));
            if(Material) Batch->SetMaterial(Slot,Material);
        }
    AddInstanceComponent(Batch);Batch->RegisterComponent();LiveBatches.Add(BatchName,Batch);
    return Batch;
}

void ADungeonPrototype::VerifyObjectBatch1()
{
    const int32 SavedTurn=Session->Turn,SavedSequence=Session->Sequence;
    const bool SavedStyle=SculptedCreatures;bool Passed=true;
    const TArray<FString> Names={TEXT("large box"),TEXT("chest"),TEXT("gold piece")};
    for(int32 Style=0;Style<2;++Style)
    {
        for(const FString& Name:Names) for(bool Visible:{false,true})
        {
            FNetHackCell Probe;Probe.Kind=TEXT("item");Probe.DisplayObject=Name;Probe.Visible=Visible;
            auto* Figure=GetDisplayedObjectBatch(Probe);
            const FString Expected=TEXT("/Game/ObjectInterpretations/Meshes/SM_")+Name.Replace(TEXT(" "),TEXT("_")).Replace(TEXT("-"),TEXT("_")).ToLower();
            Passed &= Figure && Figure->GetStaticMesh() && Figure->GetStaticMesh()->GetPathName().StartsWith(Expected+TEXT("."));
            if(Figure && Figure->GetStaticMesh())
            {
                const auto* Data=Figure->GetStaticMesh()->GetRenderData();
                Passed &= Data && Data->LODResources.Num()>0 && Data->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
                for(int32 Slot=0;Slot<Figure->GetStaticMesh()->GetStaticMaterials().Num();++Slot)
                    Passed &= GetNameSafe(Figure->GetMaterial(Slot)).EndsWith(TEXT("Memory"))==!Visible;
            }
        }
        HandleLiveKey(EKeys::F9,false);
    }
    for(const FString& Kind:{FString(TEXT("monster")),FString(TEXT("terrain")),FString(TEXT("unknown"))})
    {
        FNetHackCell Probe;Probe.Kind=Kind;Probe.DisplayObject=TEXT("chest");Passed &= GetDisplayedObjectBatch(Probe)==nullptr;
    }
    FNetHackCell Unknown;Unknown.Kind=TEXT("item");Unknown.DisplayObject=TEXT("unknown object");Passed &= GetDisplayedObjectBatch(Unknown)==nullptr;
    Passed &= SavedStyle==SculptedCreatures && SavedTurn==Session->Turn && SavedSequence==Session->Sequence;
    RebuildLiveMap();
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewObjectBatch1")))
    {
        TArray<FIntPoint> Floors;
        for(int32 Y=0;Y<Rows;++Y) for(int32 X=0;X<Columns;++X)
        {
            const auto& Cell=Session->Cells[Y*Columns+X];
            if(Cell.Visible && Cell.Terrain==TEXT("floor") && Cell.Kind==TEXT("terrain") && FIntPoint(X,Y)!=Session->Hero) Floors.Add(FIntPoint(X,Y));
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
                const auto& Cell=Session->Cells[Near.Y*Columns+Near.X];
                if(!Cell.Visible || Cell.Terrain!=TEXT("floor")) Penalty+=40;
            }
            return Penalty;
        };
        Floors.Sort([&Score](const FIntPoint& A,const FIntPoint& B){return Score(A)<Score(B);});
        Passed &= Floors.Num()>=3;
        if(Floors.Num()>=3) for(int32 I=0;I<3;++I)
        {
            FNetHackCell Probe;Probe.Kind=TEXT("item");Probe.DisplayObject=Names[I];Probe.Visible=true;
            if(auto* Figure=GetDisplayedObjectBatch(Probe))
                Figure->AddInstance(FTransform(FRotator(0,15,0),CellPosition(Floors[I].X,Floors[I].Y,8),FVector(1)));
            UE_LOG(LogTemp,Display,TEXT("OBJECT_BATCH1_FIXTURE %s x=%d y=%d"),*Names[I],Floors[I].X,Floors[I].Y);
        }
    }
    UE_LOG(LogTemp,Display,TEXT("OBJECT_BATCH1_CHECK %s styles=2 forms=3 visibility=2 fallback=4 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),SavedTurn,Session->Turn,SavedSequence,Session->Sequence);
    if(!Passed) FPlatformMisc::RequestExitWithStatus(false,1);
}

void ADungeonPrototype::EndPlay(const EEndPlayReason::Type Reason)
{
    Session.Reset();
    Super::EndPlay(Reason);
}

void ADungeonPrototype::RebuildLiveMap()
{
    for(auto& Batch:LiveBatches) Batch.Value->ClearInstances();
    UpdateAtmosphere();
    const auto Put=[this](const FString& Name,int32 X,int32 Y,float Z,FVector Scale,FQuat Rotation=FQuat::Identity) {
        if(auto* Batch=LiveBatches.Find(FName(*Name))) (*Batch)->AddInstance(FTransform(Rotation,CellPosition(X,Y,Z),Scale));
    };
    for(int32 Y=0;Y<Rows;++Y) for(int32 X=0;X<Columns;++X)
    {
        const auto& Cell=Session->Cells[Y*Columns+X];
        if(Cell.Kind==TEXT("unknown") || Cell.Terrain==TEXT("stone") || Cell.Terrain==TEXT("none")) continue;
        const FString Suffix=Cell.Visible?TEXT(""):TEXT("Memory");
        if(Cell.Terrain==TEXT("wall"))
        {
            Put(TEXT("Wall")+Suffix,X,Y,60,FVector(.98f,.98f,1.2f));
            // The beveled stones are individual solids. Recessed mortar closes
            // their joints without covering the masonry faces or changing light.
            Put(TEXT("Mortar")+Suffix,X,Y,60,FVector(.93f,.93f,1.182f));
            // Each known wall pair gets one continuous backing across its tile
            // seam. Never bridge a door, unknown cell, or diagonal corner.
            for(const FIntPoint Step:{FIntPoint(1,0),FIntPoint(0,1)})
            {
                const int32 NX=X+Step.X,NY=Y+Step.Y;
                if(NX>=Columns || NY>=Rows) continue;
                const auto& Near=Session->Cells[NY*Columns+NX];
                if(Near.Kind==TEXT("unknown") || Near.Terrain!=TEXT("wall")) continue;
                const FString JointSuffix=Cell.Visible && Near.Visible?TEXT(""):TEXT("Memory");
                if(auto* Mortar=LiveBatches.Find(FName(*(TEXT("Mortar")+JointSuffix))))
                    (*Mortar)->AddInstance(FTransform(FQuat::Identity,
                        CellPosition(X,Y,60)+FVector(Step.X*50.f,Step.Y*50.f,0),
                        Step.X?FVector(.10f,.93f,1.182f):FVector(.93f,.10f,1.182f)));
            }
            continue;
        }
        Put(TEXT("Floor")+Suffix,X,Y,0,FVector(.96f,.96f,.16f));
        if(Cell.Terrain==TEXT("closed") || Cell.Terrain==TEXT("open")) AddFramedDoor(Cell,X,Y);
        else if(Cell.Terrain==TEXT("water")) Put(TEXT("Water")+Suffix,X,Y,10,FVector(.95f,.95f,.06f));
        else if(Cell.Terrain==TEXT("lava")) Put(TEXT("Lava")+Suffix,X,Y,10,FVector(.95f,.95f,.06f));
        else if(Cell.Terrain==TEXT("up") || Cell.Terrain==TEXT("down"))
            for(int32 I=0;I<4;++I)
            {
                const int32 Step=Cell.Terrain==TEXT("up")?I:3-I;
                auto* Batch=LiveBatches.Find(FName(*(TEXT("Stairs")+Suffix)));
                (*Batch)->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y,14+Step*7)+FVector(0,I*21-32,0),FVector(.75f,.19f,.12f+Step*.14f)));
            }
        else if(Cell.Terrain==TEXT("fountain"))
        {
            if(auto* Fountain=GetFountainBatch(Cell)) Fountain->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y,8),FVector(1)));
            else Put(TEXT("Feature")+Suffix,X,Y,36,FVector(.7f,.7f,.5f));
        }
        else if(Cell.Terrain==TEXT("sink")) Put(TEXT("Feature")+Suffix,X,Y,36,FVector(.7f,.7f,.5f));
        else if(Cell.Terrain==TEXT("trap")) Put(TEXT("Trap")+Suffix,X,Y,12,FVector(.65f,.65f,.10f));
        if(Session->Hero==FIntPoint(X,Y)) continue;
        if(auto* Object=GetDisplayedObjectBatch(Cell))
        {
            Object->AddInstance(FTransform(FRotator(0,15,0),CellPosition(X,Y,8),FVector(1)));
            continue;
        }
        if((Cell.Kind==TEXT("pet") || Cell.Kind==TEXT("monster")) && !Cell.DisplayMonster.IsEmpty())
            if(auto* Figure=GetDefaultTileBatch(Cell,false))
            {
                const bool Sculpted=Figure->GetFName().ToString().StartsWith(TEXT("Tile_Sculpted_"));
                const float Yaw=Sculpted?((Cell.DisplayMonster==TEXT("Uruk-hai") || Cell.DisplayMonster==TEXT("orc shaman") || Cell.DisplayMonster==TEXT("orc-captain") || Cell.DisplayMonster==TEXT("floating eye") || Cell.DisplayMonster==TEXT("hobgoblin") || Cell.DisplayMonster==TEXT("hill orc") || Cell.DisplayMonster==TEXT("Mordor orc") || Cell.DisplayMonster==TEXT("dwarf") || Cell.DisplayMonster.StartsWith(TEXT("dwarf ")) || Cell.DisplayMonster==TEXT("goblin") || Cell.DisplayMonster==TEXT("gnome") || Cell.DisplayMonster.StartsWith(TEXT("gnome ")) || Cell.DisplayMonster==TEXT("gnomish wizard") || Cell.DisplayMonster==TEXT("kobold") || Cell.DisplayMonster==TEXT("large kobold") || Cell.DisplayMonster.StartsWith(TEXT("kobold ")))?15.f:-75.f):105.f;
                Figure->AddInstance(FTransform(FRotator(0,Yaw,0),CellPosition(X,Y,8),FVector(1)));
                continue;
            }
        if(AddTileFallback(Cell,X,Y)) continue;
        if(Cell.Kind==TEXT("pet")) Put(TEXT("Pet"),X,Y,49,FVector(.44f,.44f,.55f));
        else if(Cell.Kind==TEXT("monster") || Cell.Kind==TEXT("effect")) Put(TEXT("Monster"),X,Y,49,FVector(.44f,.44f,.55f));
        else if(Cell.Kind==TEXT("item")) Put(TEXT("Item")+Suffix,X,Y,32,FVector(.37f,.37f,.37f));
    }
    if(Session->IsReady())
    {
        if(auto* Figure=GetDefaultTileBatch(Session->Cells[Session->Hero.Y*Columns+Session->Hero.X],true))
            Figure->AddInstance(FTransform(FRotator(0,HeroVolumeKey.EndsWith(TEXT("_human"))?15.f:105.f,0),CellPosition(Session->Hero.X,Session->Hero.Y,8),FVector(1)));
        else if(!AddTileFallback(Session->Cells[Session->Hero.Y*Columns+Session->Hero.X],Session->Hero.X,Session->Hero.Y,true)) Put(TEXT("Player"),Session->Hero.X,Session->Hero.Y,61,FVector(.65f,.65f,1));
    }
}

void ADungeonPrototype::TickLiveGame()
{
    Session->Pump();
    TickAtmosphere();
    if(AutoFirstPosition.X>=0 && Session->IsReady() && Session->Hero!=AutoFirstPosition) AutoMoved=true;
    if(Session->IsReady() && Session->Hero!=PreviousHero)
    {
        if(PreviousHero.X>=0)
        {
            const FIntPoint Delta=Session->Hero-PreviousHero;
            if(FMath::Abs(Delta.X)<=1 && FMath::Abs(Delta.Y)<=1)
                EyeRotation=FRotator(0,FMath::RadiansToDegrees(FMath::Atan2(float(Delta.Y),float(Delta.X))),0);
        }
        PreviousHero=Session->Hero;
    }
    if(Session->TakeMapDirty()) RebuildLiveMap();
    if(CaptureLive && !LiveCaptureRequested && FPlatformTime::Seconds()-LiveStartedTime>45)
    {
        LiveCaptureRequested=true;
        UE_LOG(LogTemp,Error,TEXT("NETHACK_LIVE_CAPTURE_TIMEOUT"));
        CaptureAndValidate();
    }
    if(!CaptureLive || LiveCaptureRequested || !Session->Awaiting) return;
    if(Session->IsCommand())
    {
        if(AutoFirstPosition.X<0) AutoFirstPosition=Session->Hero;
        // The camera experiment needs only a few movement events; avoid a long
        // random combat sequence before a test that is about camera state.
        const int32 CaptureCommands=(FParse::Param(FCommandLine::Get(),TEXT("CaptureFirstPerson")) || FParse::Param(FCommandLine::Get(),TEXT("CaptureDefaultTiles")))?4:12;
        // Fast roles can take multiple movement inputs within one native turn.
        // Wait for the same minimum turn required by CaptureAndValidate.
        if(AutoCommands>=CaptureCommands && Session->Turn>=4)
        {
            LiveCaptureRequested=true;
            // Explicit capture-only fixtures exercise displayed identity, both sex
            // aliases, fallback and real F9 rebuilds without querying world monsters.
            const bool VerifyBatch20=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch20"));
            const bool VerifyBatch19=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch19"));
            const bool VerifyBatch18=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch18"));
            const bool VerifyBatch17=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch17"));
            const bool VerifyBatch16=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch16"));
            const bool VerifyBatch15=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch15"));
            const bool VerifyBatch14=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch14"));
            const bool VerifyBatch13=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch13"));
            const bool VerifyBatch12=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch12"));
            const bool VerifyBatch11=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch11"));
            const bool VerifyBatch10=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch10"));
            const bool VerifyBatch9=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch9"));
            const bool VerifyBatch8=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch8"));
            const bool VerifyBatch7=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch7"));
            const bool VerifyBatch6=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch6"));
            const bool VerifyBatch5=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch5"));
            const bool VerifyBatch4=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch4"));
            const bool VerifyBatch3=FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch3"));
            if(VerifyBatch20 || VerifyBatch19 || VerifyBatch18 || VerifyBatch17 || VerifyBatch16 || VerifyBatch15 || VerifyBatch14 || VerifyBatch13 || VerifyBatch12 || VerifyBatch11 || VerifyBatch10 || VerifyBatch9 || VerifyBatch8 || VerifyBatch7 || VerifyBatch6 || VerifyBatch5 || VerifyBatch4 || VerifyBatch3 || FParse::Param(FCommandLine::Get(),TEXT("VerifyCreatureBatch2")))
            {
                const int32 SavedTurn=Session->Turn,SavedSequence=Session->Sequence;
                const bool OriginalStyle=SculptedCreatures;
                const int32 BatchNumber=VerifyBatch20?20:VerifyBatch19?19:VerifyBatch18?18:VerifyBatch17?17:VerifyBatch16?16:VerifyBatch15?15:VerifyBatch14?14:VerifyBatch13?13:VerifyBatch12?12:VerifyBatch11?11:VerifyBatch10?10:VerifyBatch9?9:VerifyBatch8?8:VerifyBatch7?7:VerifyBatch6?6:VerifyBatch5?5:VerifyBatch4?4:VerifyBatch3?3:2;
                const TArray<FString> SpeciesNames=VerifyBatch20
                    ? TArray<FString>{TEXT("Uruk-hai"),TEXT("orc shaman"),TEXT("orc-captain")}
                    : VerifyBatch19
                    ? TArray<FString>{TEXT("floating eye"),TEXT("newt"),TEXT("lichen")}
                    : VerifyBatch18
                    ? TArray<FString>{TEXT("hobgoblin"),TEXT("hill orc"),TEXT("Mordor orc")}
                    : VerifyBatch17
                    ? TArray<FString>{TEXT("dwarf mummy"),TEXT("dwarf zombie")}
                    : VerifyBatch16
                    ? TArray<FString>{TEXT("dwarf"),TEXT("dwarf leader"),TEXT("dwarf ruler")}
                    : VerifyBatch15
                    ? TArray<FString>{TEXT("gnomish wizard"),TEXT("gnome mummy"),TEXT("gnome zombie")}
                    : VerifyBatch14
                    ? TArray<FString>{TEXT("kobold shaman"),TEXT("kobold mummy"),TEXT("kobold zombie")}
                    : VerifyBatch13
                    ? TArray<FString>{TEXT("kobold"),TEXT("large kobold"),TEXT("kobold leader")}
                    : VerifyBatch12
                    ? TArray<FString>{TEXT("white unicorn"),TEXT("gray unicorn"),TEXT("black unicorn")}
                    : VerifyBatch11
                    ? TArray<FString>{TEXT("pony"),TEXT("horse"),TEXT("warhorse")}
                    : VerifyBatch10
                    ? TArray<FString>{TEXT("tiger"),TEXT("hell hound pup"),TEXT("hell hound")}
                    : VerifyBatch9
                    ? TArray<FString>{TEXT("jaguar"),TEXT("lynx"),TEXT("panther")}
                    : VerifyBatch8
                    ? TArray<FString>{TEXT("bat"),TEXT("giant bat"),TEXT("vampire bat")}
                    : VerifyBatch7
                    ? TArray<FString>{TEXT("coyote"),TEXT("warg"),TEXT("rabid rat")}
                    : VerifyBatch6
                    ? TArray<FString>{TEXT("dog"),TEXT("large dog"),TEXT("dingo")}
                    : VerifyBatch5
                    ? TArray<FString>{TEXT("wolf"),TEXT("winter wolf cub"),TEXT("winter wolf")}
                    : VerifyBatch4
                    ? TArray<FString>{TEXT("kitten"),TEXT("housecat"),TEXT("large cat")}
                    : VerifyBatch3
                    ? TArray<FString>{TEXT("sewer rat"),TEXT("giant rat"),TEXT("gnome ruler")}
                    : TArray<FString>{TEXT("jackal"),TEXT("fox"),TEXT("gnome")};
                if(!SculptedCreatures) HandleLiveKey(EKeys::F9,false);
                bool Passed=true;
                for(const FString& Name:SpeciesNames)
                    for(bool Female:{false,true})
                    {
                        FNetHackCell Probe; Probe.DisplayMonster=Name; Probe.Female=Female;
                        auto* Figure=GetDefaultTileBatch(Probe,false);
                        const FString Expected=FString(TEXT("/Game/CreatureInterpretations/Meshes/SM_"))+Name.Replace(TEXT(" "),TEXT("_")).Replace(TEXT("-"),TEXT("_")).ToLower()
                            +((VerifyBatch15 && Female && (Name==TEXT("gnomish wizard") || Name==TEXT("gnome zombie")))?TEXT("_female"):TEXT(""));
                        Passed &= Figure && Figure->GetStaticMesh() && Figure->GetStaticMesh()->GetPathName().StartsWith(Expected+TEXT("."));
                        if((VerifyBatch20 || VerifyBatch19 || VerifyBatch18 || VerifyBatch17 || VerifyBatch16 || VerifyBatch15 || VerifyBatch14 || VerifyBatch13) && Figure && Figure->GetStaticMesh())
                        {
                            const auto* Data=Figure->GetStaticMesh()->GetRenderData();
                            bool PaintValid=Data && Data->LODResources.Num()>0;
                            if(PaintValid) PaintValid=Data->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
                            Passed &= PaintValid;
                            UE_LOG(LogTemp,Display,TEXT("CREATURE_BATCH%d_PAINT %s valid=%d"),BatchNumber,*Name,PaintValid);
                        }
                        if((VerifyBatch5 || VerifyBatch6 || VerifyBatch7 || VerifyBatch8 || VerifyBatch9 || VerifyBatch10 || VerifyBatch11 || VerifyBatch12) && Figure && Figure->GetStaticMesh())
                        {
                            UStaticMesh* Mesh=Figure->GetStaticMesh();
                            const auto* Data=Mesh->GetRenderData();
                            bool FurValid=Data && Data->LODResources.Num()>0;
                            int32 FurSlots=0;
                            for(int32 Slot=0;Slot<Mesh->GetStaticMaterials().Num();++Slot)
                                FurSlots+=GetNameSafe(Mesh->GetMaterial(Slot))==TEXT("M_PaintedFur")?1:0;
                            FurValid &= FurSlots>0;
                            if(Data && Data->LODResources.Num()>0)
                            {
                                const auto& LOD=Data->LODResources[0];
                                FurValid &= LOD.VertexBuffers.StaticMeshVertexBuffer.GetNumTexCoords()>0
                                    && LOD.VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
                                UE_LOG(LogTemp,Display,TEXT("CREATURE_BATCH%d_FUR %s valid=%d slots=%d uv_channels=%u triangles=%u"),
                                    BatchNumber,*Name,FurValid,FurSlots,LOD.VertexBuffers.StaticMeshVertexBuffer.GetNumTexCoords(),LOD.GetNumTriangles());
                            }
                            Passed &= FurValid;
                        }
                    }
                HandleLiveKey(EKeys::F9,false);
                for(const FString& Name:SpeciesNames)
                    for(bool Female:{false,true})
                    {
                        FNetHackCell Probe; Probe.DisplayMonster=Name; Probe.Female=Female;
                        auto* Figure=GetDefaultTileBatch(Probe,false);
                        const FString Key=Name.Replace(TEXT(" "),TEXT("_")).Replace(TEXT("-"),TEXT("_")).ToLower()+(Female?TEXT("_female"):TEXT("_male"));
                        const FString Package=TEXT("/Game/DefaultTiles/Meshes/SM_")+Key;
                        Passed &= FPackageName::DoesPackageExist(Package)
                            ? Figure && Figure->GetStaticMesh() && Figure->GetStaticMesh()->GetPathName().StartsWith(Package+TEXT("."))
                            : Figure==nullptr;
                    }
                if(VerifyBatch20 || VerifyBatch19 || VerifyBatch18 || VerifyBatch17 || VerifyBatch16 || VerifyBatch15 || VerifyBatch14)
                {
                    const TArray<int32> TileIndices=VerifyBatch20?TArray<int32>{154,156,158}:VerifyBatch19?TArray<int32>{58,658,324}:VerifyBatch18?TArray<int32>{146,150,152}:VerifyBatch17?TArray<int32>{390,496}:VerifyBatch16?TArray<int32>{92,96,98}:VerifyBatch15?TArray<int32>{342,386,492}:TArray<int32>{128,384,490};
                    for(int32 I=0;I<SpeciesNames.Num();++I) for(bool Female:{false,true})
                    {
                        FNetHackCell Probe;Probe.Kind=TEXT("monster");Probe.Visible=true;
                        Probe.DisplayMonster=SpeciesNames[I];Probe.Female=Female;Probe.TileIndex=TileIndices[I]+(Female?1:0);
                        Passed &= AddTileFallback(Probe,0,0);
                        if(auto* Card=LiveBatches.Find(TEXT("TileFallback")))
                        {
                            const int32 Last=(*Card)->GetInstanceCount()-1;
                            Passed &= Last>=0 && (*Card)->PerInstanceSMCustomData[Last*2]==Probe.TileIndex;
                        }
                        else Passed=false;
                    }
                }
                HandleLiveKey(EKeys::F9,false);
                FNetHackCell Unknown; Unknown.DisplayMonster=TEXT("unmapped fixture");
                Passed &= GetDefaultTileBatch(Unknown,false)==nullptr && Session->Turn==SavedTurn && Session->Sequence==SavedSequence;
                if(!OriginalStyle) HandleLiveKey(EKeys::F9,false);
                RebuildLiveMap();
                UE_LOG(LogTemp,Display,TEXT("CREATURE_BATCH%d_CHECK %s forms=%d fallback=%d turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),BatchNumber,Passed?TEXT("PASS"):TEXT("FAIL"),SpeciesNames.Num()*2,SpeciesNames.Num()*2,SavedTurn,Session->Turn,SavedSequence,Session->Sequence);
                if(!Passed) { FPlatformMisc::RequestExitWithStatus(false,1); return; }
                if(FParse::Param(FCommandLine::Get(),*FString::Printf(TEXT("PreviewCreatureBatch%d"),BatchNumber)))
                {
                    // Presentation-only fixtures on revealed floor for a material
                    // and camera check. Never modify the native gameplay session.
                    TArray<FIntPoint> Floors;
                    for(int32 Y=0;Y<Rows;++Y) for(int32 X=0;X<Columns;++X)
                    {
                        const auto& Cell=Session->Cells[Y*Columns+X];
                        if(Cell.Visible && Cell.Terrain==TEXT("floor") && Cell.DisplayMonster.IsEmpty()
                            && FIntPoint(X,Y)!=Session->Hero) Floors.Add(FIntPoint(X,Y));
                    }
                    // Keep detail fixtures within the hero-centred 8x view when
                    // nearby floor permits it, before preferring open floor.
                    const TArray<FIntPoint> NearbyFloors=Floors.FilterByPredicate([this](const FIntPoint& At)
                    { return (At-Session->Hero).SizeSquared()<=9; });
                    if(NearbyFloors.Num()>=3) Floors=NearbyFloors;
                    const auto FixtureScore=[this](const FIntPoint& At)
                    {
                        int32 Penalty=0;
                        for(int32 DY=-1;DY<=1;++DY) for(int32 DX=-1;DX<=1;++DX)
                        {
                            const FIntPoint Near=At+FIntPoint(DX,DY);
                            if(Near.X<0 || Near.X>=Columns || Near.Y<0 || Near.Y>=Rows) { Penalty+=40; continue; }
                            const auto& Cell=Session->Cells[Near.Y*Columns+Near.X];
                            if(!Cell.Visible || Cell.Terrain!=TEXT("floor")) Penalty+=40;
                        }
                        return Penalty+(At-Session->Hero).SizeSquared();
                    };
                    Floors.Sort([&FixtureScore](const FIntPoint& A,const FIntPoint& B)
                    { return FixtureScore(A)<FixtureScore(B); });
                    int32 Index=0;
                    if(Floors.Num()<SpeciesNames.Num() || !SculptedCreatures) { FPlatformMisc::RequestExitWithStatus(false,1); return; }
                    for(const FString& Name:SpeciesNames)
                    {
                        FNetHackCell Probe; Probe.DisplayMonster=Name;
                        if(auto* Figure=GetDefaultTileBatch(Probe,false))
                        {
                            const auto& At=Floors[Index++];
                            Figure->AddInstance(FTransform(FRotator(0,(Probe.DisplayMonster==TEXT("Uruk-hai") || Probe.DisplayMonster==TEXT("orc shaman") || Probe.DisplayMonster==TEXT("orc-captain") || Probe.DisplayMonster==TEXT("floating eye") || Probe.DisplayMonster==TEXT("hobgoblin") || Probe.DisplayMonster==TEXT("hill orc") || Probe.DisplayMonster==TEXT("Mordor orc") || Probe.DisplayMonster==TEXT("dwarf") || Probe.DisplayMonster.StartsWith(TEXT("dwarf ")) || Probe.DisplayMonster==TEXT("gnome") || Probe.DisplayMonster.StartsWith(TEXT("gnome ")) || Probe.DisplayMonster==TEXT("gnomish wizard") || Probe.DisplayMonster==TEXT("kobold") || Probe.DisplayMonster==TEXT("large kobold") || Probe.DisplayMonster.StartsWith(TEXT("kobold ")))?15.f:-75.f,0),CellPosition(At.X,At.Y,8),FVector(1)));
                            UE_LOG(LogTemp,Display,TEXT("CREATURE_BATCH%d_PREVIEW_FIXTURE %s cell=%d,%d"),BatchNumber,*Name,At.X,At.Y);
                        }
                    }
                }
            }
            if(FParse::Param(FCommandLine::Get(),TEXT("VerifyTileFallback"))) VerifyTileFallback();
            if(FParse::Param(FCommandLine::Get(),TEXT("VerifyObjectBatch1"))) VerifyObjectBatch1();
            if(FParse::Param(FCommandLine::Get(),TEXT("VerifySpecialBatch1"))) VerifySpecialBatch1();
            if(FParse::Param(FCommandLine::Get(),TEXT("VerifyDoorFrames"))) VerifyDoorFrames();
            if(FParse::Param(FCommandLine::Get(),TEXT("VerifyHumanPlayers")))
            {
                VerifyAndCaptureHumanPlayers();
                return;
            }
            if(FParse::Param(FCommandLine::Get(),TEXT("CaptureFirstPerson")))
            {
                CaptureFirstPersonTransition();
                return;
            }
            if(FParse::Param(FCommandLine::Get(),TEXT("CaptureZoom")))
            {
                ResetOverview();
                AdjustZoom((FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch3")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch4")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch5")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch6")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch7")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch8")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch9")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch10")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch11")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch12")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch13")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch14")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch20")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch19")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch18")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch17")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch16")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch15")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewDoorFrames")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewSpecialBatch1")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewObjectBatch1")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewTileFallback")))?12.f:6.f);
            }
            // Let the updated meshes render before capturing.
            FTimerHandle Handle;
            GetWorldTimerManager().SetTimer(Handle,this,&ADungeonPrototype::CaptureAndValidate,2.f,false);
            return;
        }
        ++AutoCommands;
        if(AutoCommands==8) { Session->Key('i'); return; }
        int32 Command='.';
        const TArray<FIntPoint> Dirs={{1,0},{0,1},{-1,0},{0,-1}};
        const char Keys[]={'l','j','h','k'};
        for(int32 I=0;I<Dirs.Num();++I)
        {
            FIntPoint P=Session->Hero+Dirs[I];
            if(P.X<0 || P.X>=Columns || P.Y<0 || P.Y>=Rows) continue;
            const auto& Cell=Session->Cells[P.Y*Columns+P.X];
            if((Cell.Terrain==TEXT("floor") || Cell.Terrain==TEXT("up") || Cell.Terrain==TEXT("down") || Cell.Terrain==TEXT("open")) && Cell.Kind!=TEXT("pet") && Cell.Kind!=TEXT("monster")) { Command=Keys[I]; break; }
        }
        Session->Key(Command);
    }
    else if(Session->PromptType==TEXT("menu"))
    {
        if(Session->IsReady()) { Session->Reply(Session->MenuMode?TEXT("-1"):TEXT("")); return; }
        FString Answer;
        for(const auto& Item:Session->Menu) if(Item.Selectable && Session->MenuMode) { Answer=FString::FromInt(Item.Index); break; }
        Session->Reply(Answer);
    }
    else if(Session->PromptType==TEXT("yn")) Session->Key(Session->IsReady()?'n':'y');
    else if(Session->PromptType==TEXT("line")) Session->Reply(TEXT("Adventurer"));
    else Session->Key(32);
}

bool ADungeonPrototype::HandleLiveKey(FKey Key,bool Control)
{
    if(Key==EKeys::Escape && FirstPerson) { ToggleFirstPerson(); return true; }
    const bool MenuOpen=Session && Session->Awaiting && Session->PromptType==TEXT("menu");
    if(Key==EKeys::F7)
    {
        ShowEntityGlyphs=!ShowEntityGlyphs;
        UE_LOG(LogTemp,Display,TEXT("ENTITY_GLYPHS %s turn=%d"),ShowEntityGlyphs?TEXT("ON"):TEXT("OFF"),Session?Session->Turn:0);
        return true;
    }
    if(Key==EKeys::F9)
    {
        SculptedCreatures=!SculptedCreatures;
        if(Session) RebuildLiveMap();
        UE_LOG(LogTemp,Display,TEXT("CREATURE_STYLE %s turn=%d"),SculptedCreatures?TEXT("sculpted candidates"):TEXT("default tile volumes"),Session?Session->Turn:0);
        return true;
    }
    if(Control && Key==EKeys::F) { ToggleFirstPerson(); return true; }
    if(Key==EKeys::F5) { ResetOverview(); return true; }
    if(Key==EKeys::F8) { FollowHero=true; FitCamera(); return true; }
    if(Key==EKeys::MouseScrollUp || Key==EKeys::MouseScrollDown)
    {
        if(MenuOpen) Session->Scroll(Key==EKeys::MouseScrollUp?-Session->MenuPageSize:Session->MenuPageSize);
        else AdjustZoom(Key==EKeys::MouseScrollUp?1.f:-1.f);
        return true;
    }
    if(!Session) return false;
    SuppressedNumpadCharacter=0;
    if(Key==EKeys::F2 && Session->Ended) { StartLiveGame(true); return true; }
    if(MenuOpen && (Key==EKeys::PageDown || Key==EKeys::PageUp)) { Session->Scroll(Key==EKeys::PageDown?Session->MenuPageSize:-Session->MenuPageSize); return true; }
    if(MenuOpen && (Key==EKeys::Up || Key==EKeys::Down)) { Session->Scroll(Key==EKeys::Down?1:-1); return true; }
    int32 C=0;
    const FString Name=Key.GetFName().ToString();
    // Printable characters arrive separately through InputChar, already translated by Windows.
    if(Control && Name.Len()==1 && Name[0]>='A' && Name[0]<='Z') C=Name[0]-'A'+1;
    if(Key==EKeys::Enter) C=13;
    else if(Key==EKeys::Escape) C=27;
    else if(Key==EKeys::BackSpace) C=8;
    else if(Key==EKeys::Tab) C=9;
    else if(Key==EKeys::F1) C='?';
    else if(Key==EKeys::Left || Key==EKeys::NumPadFour) C='h';
    else if(Key==EKeys::Down || Key==EKeys::NumPadTwo) C='j';
    else if(Key==EKeys::Up || Key==EKeys::NumPadEight) C='k';
    else if(Key==EKeys::Right || Key==EKeys::NumPadSix) C='l';
    else if(Key==EKeys::Home || Key==EKeys::NumPadSeven) C='y';
    else if(Key==EKeys::NumPadNine || Key==EKeys::PageUp) C='u';
    else if(Key==EKeys::End || Key==EKeys::NumPadOne) C='b';
    else if(Key==EKeys::NumPadThree || Key==EKeys::PageDown) C='n';
    else if(Key==EKeys::NumPadFive || Key==EKeys::Decimal) C='.';
    const FKey PadKeys[]={EKeys::NumPadZero,EKeys::NumPadOne,EKeys::NumPadTwo,EKeys::NumPadThree,EKeys::NumPadFour,EKeys::NumPadFive,EKeys::NumPadSix,EKeys::NumPadSeven,EKeys::NumPadEight,EKeys::NumPadNine};
    for(int32 I=0;I<10;++I) if(Key==PadKeys[I]) SuppressedNumpadCharacter=TCHAR('0'+I);
    if(Key==EKeys::Decimal) SuppressedNumpadCharacter='.';
    if(SuppressedNumpadCharacter) NumpadCharacterTime=FPlatformTime::Seconds();
    if(C) { Session->Key(C); return true; }
    return false;
}

bool ADungeonPrototype::HandleLiveCharacter(TCHAR Character)
{
    if(!Session || Character<32) return false;
    if(TextRepeatSuppressed) return true;
    if(Character==SuppressedNumpadCharacter && FPlatformTime::Seconds()-NumpadCharacterTime<.3) return true;
    if(Character<=126)
    {
        UE_LOG(LogTemp,Display,TEXT("NETHACK_CHARACTER code=%d"),int32(Character));
        Session->Key(int32(Character));
    }
    return true;
}

bool UDungeonGameViewportClient::InputChar(FViewport* InViewport,int32 ControllerId,TCHAR Character)
{
    if(!IgnoreInput() && GetWorld())
        if(auto* PC=GetWorld()->GetFirstPlayerController())
            if(auto* Dungeon=Cast<ADungeonPrototype>(PC->GetViewTarget()))
                if(Dungeon->HandleLiveCharacter(Character)) return true;
    return Super::InputChar(InViewport,ControllerId,Character);
}

void ADungeonPlayerController::FlushPressedKeys()
{
    LeftControlHeld=RightControlHeld=LeftAltHeld=RightAltHeld=false;
    Super::FlushPressedKeys();
}

bool ADungeonPlayerController::InputKey(const FInputKeyEventArgs& Params)
{
    // Track modifiers in event order; PlayerInput state can lag behind a chord
    // when Windows delivers press/release events within the same engine frame.
    const bool Held=Params.Event!=IE_Released;
    if(Params.Key==EKeys::LeftControl) LeftControlHeld=Held;
    if(Params.Key==EKeys::RightControl) RightControlHeld=Held;
    if(Params.Key==EKeys::LeftAlt) LeftAltHeld=Held;
    if(Params.Key==EKeys::RightAlt) RightAltHeld=Held;
    if(Params.Event==IE_Pressed || Params.Event==IE_Repeat)
        if(auto* Dungeon=Cast<ADungeonPrototype>(GetViewTarget()))
        {
            auto* Session=Dungeon->GetSession();
            Dungeon->SetTextRepeatSuppressed(Params.Event==IE_Repeat && (!Session || Session->PromptType!=TEXT("line")));
            if(Params.Event==IE_Repeat && (!Session || Session->PromptType!=TEXT("line"))) return true;
            const bool Control=(LeftControlHeld||RightControlHeld) && !LeftAltHeld && !RightAltHeld;
            if(Dungeon->HandleLiveKey(Params.Key,Control)) return true;
        }
    return Super::InputKey(Params);
}

void ADungeonPrototypeHUD::DrawLiveHUD(FNetHackSession& Live)
{
    const float W=Canvas->SizeX,H=Canvas->SizeY,S=FMath::Clamp(W/1600.f,.65f,1.5f);
    const FLinearColor Ink(.81f,.86f,.84f),Muted(.40f,.51f,.53f),Gold(.95f,.66f,.23f),Panel(.018f,.028f,.036f,.98f);
    DrawRect(Panel,0,0,W,84*S);
    DrawRect(Gold,32*S,24*S,3*S,38*S);
    DrawGameTitle(48*S,19*S,S,Ink);
    DrawText(TEXT("THE DUNGEONS OF DOOM"),Muted,49*S,53*S,GEngine->GetSmallFont(),.9f*S);
    DrawText(Live.IsReady()?FString::Printf(TEXT("DLVL %d  /  TURN %d"),Live.Depth,Live.Turn):TEXT("A NEW ADVENTURE"),Gold,W-290*S,31*S,GEngine->GetSmallFont(),S);
    if(auto* View=Cast<ADungeonPrototype>(GetOwningPlayerController()->GetViewTarget()))
        DrawText(View->IsFirstPerson()?TEXT("FIRST PERSON  |  Esc / Ctrl+F Return  |  Right-drag Look"):FString::Printf(TEXT("%.1fx  |  F5 Full level  |  F8 Follow  |  Ctrl+F First person"),View->GetZoomFactor()),Muted,W-460*S,54*S,GEngine->GetSmallFont(),.85f*S);
    DrawRect(Panel,0,H-132*S,W,132*S);
    DrawRect(FLinearColor(.15f,.23f,.25f),32*S,H-132*S,W-64*S,1);
    const int32 MaxChars=FMath::Max(35,int32((W/S-64)/7.5f));
    TArray<FString> Lines;
    for(const auto& Message:Live.Messages)
    {
        FString Rest=Message;
        while(Rest.Len()>MaxChars)
        {
            int32 Break=MaxChars;
            while(Break>MaxChars/2 && Rest[Break]!=' ') --Break;
            if(Break<=MaxChars/2) Break=MaxChars;
            Lines.Add(Rest.Left(Break)); Rest=Rest.Mid(Break).TrimStart();
        }
        Lines.Add(Rest);
    }
    for(int32 I=FMath::Max(0,Lines.Num()-3),Row=0;I<Lines.Num();++I,++Row)
        DrawText(Lines[I],Ink,32*S,H-(114-Row*18)*S,GEngine->GetSmallFont(),S);
    DrawText(Live.IsReady()?FString::Printf(TEXT("ADVENTURER    HP %d/%d    AC %d    LV %d"),Live.HP,Live.MaxHP,Live.AC,Live.Level):TEXT("Choose your character to enter the dungeon."),Gold,32*S,H-48*S,GEngine->GetSmallFont(),S);
    DrawText(TEXT("ARROWS / NUMPAD Move   i Inventory   o Open   , Pick up   F1 Help   WHEEL Zoom   MIDDLE-DRAG Pan   F7 Labels   F9 Creature style"),Muted,32*S,H-25*S,GEngine->GetSmallFont(),.9f*S);
    DrawText(Live.Ended?TEXT("F2  New game"):TEXT("@ You  /  VIOLET LABEL Pet"),Muted,W-290*S,H-48*S,GEngine->GetSmallFont(),.9f*S);

    // Labels remain readable when a tall foreground wall obscures a small token.
    auto* Dungeon=Cast<ADungeonPrototype>(GetOwningPlayerController()->GetViewTarget());
    UFont* GlyphFont=GEngine->GetMediumFont();
    const float GlyphScale=S*(Dungeon?Dungeon->GetZoomFactor():1.f);
    for(int32 Y=0;Y<21;++Y) for(int32 X=0;X<79;++X)
    {
        const auto& Cell=Live.Cells[Y*79+X];
        if(Dungeon && !Dungeon->ShouldShowEntityGlyphs()) continue;
        const bool Hero=Live.IsReady() && Live.Hero==FIntPoint(X,Y);
        if(Dungeon && Dungeon->IsFirstPerson() && Hero) continue;
        const bool Creature=Cell.Kind==TEXT("monster") || Cell.Kind==TEXT("pet");
        if(!Hero && !Creature) continue;
        FVector2D Screen;
        const FVector Position((X-39)*100.f,(Y-10)*100.f,Hero?175.f:130.f);
        if(Dungeon && GetOwningPlayerController()->ProjectWorldLocationToScreen(Position,Screen))
        {
            const FLinearColor Color=Hero?Gold:(Cell.Kind==TEXT("pet")?FLinearColor(.73f,.55f,1):FLinearColor(1,.38f,.30f));
            const TCHAR Symbol=Hero?'@':(Cell.Symbol>=33 && Cell.Symbol<127?TCHAR(Cell.Symbol):'?');
            const FString Glyph=FString::Chr(Symbol);
            float GlyphWidth=0.f,GlyphHeight=0.f;
            Canvas->StrLen(GlyphFont,Glyph,GlyphWidth,GlyphHeight);
            float Scale=GlyphScale;
            if(Dungeon->IsFirstPerson())
            {
                FVector2D Side;
                const FVector Right=GetOwningPlayerController()->PlayerCameraManager->GetCameraRotation().RotateVector(FVector(0,1,0));
                if(GetOwningPlayerController()->ProjectWorldLocationToScreen(Position+Right*30.f,Side))
                    Scale=FMath::Clamp(float(FVector2D::Distance(Screen,Side))/16.f,.6f,3.f)*S;
            }
            GlyphWidth*=Scale;
            GlyphHeight*=Scale;
            const float GlyphPadding=2.f*Scale;
            // Anchor the badge above the piece and measure each glyph instead of
            // assuming fixed character dimensions. Text and padding zoom together.
            const float Left=Screen.X-GlyphWidth*.5f;
            const float Top=Screen.Y-GlyphHeight-GlyphPadding;
            DrawRect(FLinearColor(.01f,.015f,.02f,.85f),Left-GlyphPadding,Top-GlyphPadding,GlyphWidth+2*GlyphPadding,GlyphHeight+2*GlyphPadding);
            DrawText(Glyph,Color,Left,Top,GlyphFont,Scale);
        }
    }

    if(Live.Awaiting && Live.PromptType==TEXT("position") && Live.Cursor.X>=0)
    {
        FVector2D Screen;
        if(GetOwningPlayerController()->ProjectWorldLocationToScreen(FVector((Live.Cursor.X-39)*100.f,(Live.Cursor.Y-10)*100.f,135),Screen))
        {
            DrawRect(Gold,Screen.X-8*S,Screen.Y-8*S,16*S,2*S);
            DrawRect(Gold,Screen.X-8*S,Screen.Y+6*S,16*S,2*S);
            DrawRect(Gold,Screen.X-8*S,Screen.Y-8*S,2*S,16*S);
            DrawRect(Gold,Screen.X+6*S,Screen.Y-8*S,2*S,16*S);
        }
    }

    if(!Live.Awaiting || Live.IsCommand()) return;
    if(Live.PromptType==TEXT("menu"))
    {
        const float X=W*.12f,Y=100*S,Width=W*.76f,Height=H-260*S;
        DrawRect(Panel,X,Y,Width,Height);
        DrawRect(Gold,X,Y,3*S,Height);
        DrawText(Live.PromptText.IsEmpty()?TEXT("NetHack"):Live.PromptText,Gold,X+24*S,Y+18*S,GEngine->GetMediumFont(),S);
        Live.MenuPageSize=FMath::Max(1,int32((Height-100*S)/(20*S)));
        Live.Scroll(0);
        for(int32 I=Live.MenuScroll,Row=0;I<FMath::Min(Live.Menu.Num(),Live.MenuScroll+Live.MenuPageSize);++I,++Row)
        {
            const auto& Item=Live.Menu[I];
            FString Label=Item.Text;
            if(Item.Selectable) Label=FString::Printf(TEXT("%c %s  %s"),TCHAR(Item.Key),Live.Selection.Contains(Item.Index)?TEXT("[+]"):TEXT("[ ]"),*Label);
            DrawText(Label.Left(FMath::Max(40,int32(Width/(7.5f*S))-6)),Live.Selection.Contains(Item.Index)?Gold:Ink,X+24*S,Y+(56+Row*20)*S,GEngine->GetSmallFont(),S);
        }
        DrawText(FString::Printf(TEXT("%d-%d / %d   |   PgUp / PgDn   |   Enter: accept   Esc: cancel   %s"),Live.Menu.IsEmpty()?0:Live.MenuScroll+1,FMath::Min(Live.Menu.Num(),Live.MenuScroll+Live.MenuPageSize),Live.Menu.Num(),*Live.CountPrefix),Muted,X+24*S,Y+Height-28*S,GEngine->GetSmallFont(),.85f*S);
    }
    else
    {
        const float X=W*.12f,Y=H*.63f,Width=W*.76f;
        DrawRect(Panel,X,Y,Width,106*S);
        DrawRect(Gold,X,Y,3*S,106*S);
        DrawText(Live.PromptText,Gold,X+24*S,Y+18*S,GEngine->GetSmallFont(),S);
        DrawText(Live.PromptType==TEXT("line")?Live.Line+TEXT("_"):TEXT("Type your response.  Enter confirms; Esc cancels."),Ink,X+24*S,Y+54*S,GEngine->GetSmallFont(),S);
    }
}

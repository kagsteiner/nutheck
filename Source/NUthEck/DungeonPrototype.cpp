#include "DungeonPrototype.h"
#include "DungeonCameraTransition.h"
#include "Camera/CameraComponent.h"
#include "Camera/PlayerCameraManager.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Engine/Canvas.h"
#include "Engine/DirectionalLight.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/SkyLight.h"
#include "Engine/PointLight.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/PlayerController.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "TimerManager.h"
#include "UnrealClient.h"
#include "CanvasItem.h"
#include "Fonts/SlateFontInfo.h"
#include "Engine/Font.h"

void ADungeonPrototype::GenerateArtStudy()
{
    BoardMin=FVector(-570,-450,-50); BoardMax=FVector(610,450,160);
    const TArray<FName> Names={TEXT("Room"),TEXT("Hero"),TEXT("Dog"),TEXT("Ant"),TEXT("Goblin"),TEXT("Jelly")};
    // Blender metres -> Unreal centimetres, including the handedness change in Y.
    const TArray<FVector> Locations={FVector::ZeroVector,FVector(0,150,0),FVector(125,90,0),FVector(210,-100,0),FVector(-175,-140,0),FVector(-90,50,0)};
    for(int32 I=0;I<Names.Num();++I)
    {
        const FString Path=FString::Printf(TEXT("/Game/ArtStudy/Meshes/SM_%s.SM_%s"),*Names[I].ToString(),*Names[I].ToString());
        auto* Mesh=LoadObject<UStaticMesh>(nullptr,*Path);
        checkf(Mesh,TEXT("Missing art study mesh %s. Run Scripts/ImportArtStudy.py."),*Path);
        auto* Batch=NewObject<UInstancedStaticMeshComponent>(this,Names[I]);
        Batch->SetupAttachment(RootComponent); Batch->SetStaticMesh(Mesh);
        Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision); Batch->SetCastShadow(true);
        AddInstanceComponent(Batch); Batch->RegisterComponent();
        Batch->AddInstance(FTransform(Locations[I]));
        LiveBatches.Add(I==1?FName(TEXT("Player")):Names[I],Batch);
    }
    EyeRotation=FRotator(-4,-90,0);
}

void ADungeonPrototype::CaptureArtStudy()
{
    bool Passed=ArtStudy && ArtLightsReady && LiveBatches.Num()==6 && !Camera->GetComponentLocation().ContainsNaN();
    for(const auto& Entry:LiveBatches) Passed &= Entry.Value->GetInstanceCount()==1 && Entry.Value->GetStaticMesh()!=nullptr;
    FString View=TEXT("overview"); FParse::Value(FCommandLine::Get(),TEXT("ArtView="),View);
    if(View==TEXT("eye")) Passed &= FirstPerson && FirstPersonBlend==1.f && Camera->ProjectionMode==ECameraProjectionMode::Perspective;
    else Passed &= Camera->ProjectionMode==ECameraProjectionMode::Orthographic;
    UE_LOG(LogTemp,Display,TEXT("ART_STUDY_CHECK %s view=%s meshes=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),*View,LiveBatches.Num());
    FScreenshotRequest::RequestScreenshot(FPaths::ProjectDir()/TEXT("Art/Studies/01-MiniatureDungeon")/FString::Printf(TEXT("Unreal-%s.png"),*View),true,false);
    FTimerHandle Handle;
    GetWorldTimerManager().SetTimer(Handle,[Passed](){FPlatformMisc::RequestExitWithStatus(false,Passed?0:1);},3.f,false);
}

ADungeonPrototype::ADungeonPrototype()
{
    PrimaryActorTick.bCanEverTick = true;
    SetRootComponent(CreateDefaultSubobject<USceneComponent>(TEXT("Root")));
    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("DungeonCamera"));
    Camera->SetupAttachment(RootComponent);
    Camera->ProjectionMode = ECameraProjectionMode::Orthographic;
    Camera->bConstrainAspectRatio = false;
    Camera->bOverrideAspectRatioAxisConstraint = true;
    Camera->SetAspectRatioAxisConstraint(AspectRatio_MaintainXFOV);
    Camera->bAutoCalculateOrthoPlanes = true;
    Camera->bUpdateOrthoPlanes = true;
    Camera->OrthoNearClipPlane = 1.f;
    Camera->OrthoFarClipPlane = 40000.f;
    Camera->SetRelativeRotation(FRotator(-58.f, -75.f, 0.f));
    Camera->PostProcessSettings.bOverride_AutoExposureMethod = true;
    Camera->PostProcessSettings.AutoExposureMethod = EAutoExposureMethod::AEM_Manual;
    Camera->PostProcessSettings.bOverride_AutoExposureBias = true;
    Camera->PostProcessSettings.AutoExposureBias = 9.f;
}

FVector ADungeonPrototype::CellPosition(int32 X, int32 Y, float Z) const
{
    return FVector((X - (Columns - 1) * .5f) * CellSize,
                   (Y - (Rows - 1) * .5f) * CellSize, Z);
}

void ADungeonPrototype::CalcCamera(float DeltaTime,FMinimalViewInfo& OutResult)
{
    Super::CalcCamera(DeltaTime,OutResult);
    // Ortho plane correction must use the current focus, not the board actor's origin.
    if(!IsFirstPerson()) OutResult.SetCameraToViewTarget(CameraFocus);
    else { OutResult.PerspectiveNearClipPlane=2.f; OutResult.bAutoCalculateOrthoPlanes=false; }
}

UInstancedStaticMeshComponent* ADungeonPrototype::MakeBatch(const TCHAR* Name, const TCHAR* MeshPath, FLinearColor Color)
{
    auto* Batch = NewObject<UInstancedStaticMeshComponent>(this, Name);
    Batch->SetupAttachment(RootComponent);
    auto* Mesh = LoadObject<UStaticMesh>(nullptr, MeshPath);
    checkf(Mesh, TEXT("Missing prototype mesh: %s"), MeshPath);
    Batch->SetStaticMesh(Mesh);
    Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    Batch->SetCastShadow(true);
    Batch->SetLightingChannels(!FString(Name).EndsWith(TEXT("Memory")),FString(Name).EndsWith(TEXT("Memory")),false);
    auto* Base = LoadObject<UMaterialInterface>(nullptr, TEXT("/Game/Materials/M_Prototype.M_Prototype"));
    checkf(Base, TEXT("Run Scripts/CreatePrototypeAssets.py to create prototype assets."));
    // World-space stone keeps a consistent grain across slab faces and wall caps.
    const FString BatchName(Name);
    const TCHAR* StoneName = BatchName.StartsWith(TEXT("Floor")) ? TEXT("Floor") :
        BatchName.StartsWith(TEXT("Wall")) ? TEXT("Wall") : nullptr;
    if (StoneName)
    {
        const FString StonePath = FString::Printf(TEXT("/Game/WeatheredStone/M_Stone%s.M_Stone%s"), StoneName, StoneName);
        if (auto* Stone = LoadObject<UMaterialInterface>(nullptr, *StonePath))
        {
            Base = Stone;
            Color = BatchName.EndsWith(TEXT("Memory")) ? FLinearColor(.27f,.28f,.29f) : FLinearColor::White;
        }
    }
    // Keep the textured full-height walls; darken only live floor albedo so
    // room boundaries and entrances read more clearly from the overhead view.
    if(BatchName==TEXT("Floor") || BatchName==TEXT("FloorMemory"))
    {
        Color.R*=.75f;Color.G*=.75f;Color.B*=.75f;
    }
    auto* Material = UMaterialInstanceDynamic::Create(Base, this);
    Material->SetVectorParameterValue(TEXT("Tint"), Color);
    Batch->SetMaterial(0, Material);
    AddInstanceComponent(Batch);
    Batch->RegisterComponent();
    return Batch;
}

void ADungeonPrototype::GenerateDungeon()
{
    Cells.Init(0, Columns * Rows);
    const auto Carve = [this](int32 X, int32 Y) { Cells[Y * Columns + X] = 1; };
    // Nine rooms span the full drawable NetHack grid. Corridors form loops.
    const TArray<FIntRect> Rooms = {
        {2,2,13,9}, {19,2,31,8}, {38,1,49,8}, {57,2,76,9},
        {4,13,18,19}, {25,11,38,19}, {44,12,55,20}, {61,13,77,20}, {41,9,47,11}
    };
    for (const auto& Room : Rooms)
        for (int32 Y = Room.Min.Y; Y < Room.Max.Y; ++Y)
            for (int32 X = Room.Min.X; X < Room.Max.X; ++X) Carve(X,Y);
    const auto Connect = [&Carve](FIntPoint A, FIntPoint B) {
        while (A.X != B.X) { Carve(A.X,A.Y); A.X += A.X < B.X ? 1 : -1; }
        while (A.Y != B.Y) { Carve(A.X,A.Y); A.Y += A.Y < B.Y ? 1 : -1; }
        Carve(B.X,B.Y);
    };
    Connect({12,5},{19,5}); Connect({30,5},{38,5}); Connect({48,4},{57,4});
    Connect({8,8},{8,13}); Connect({17,16},{25,16}); Connect({31,7},{31,11});
    Connect({37,15},{44,15}); Connect({54,16},{61,16}); Connect({68,8},{68,13});
    Connect({44,7},{44,12});

    const TCHAR* Cube = TEXT("/Engine/BasicShapes/Cube.Cube");
    auto* Base = MakeBatch(TEXT("Foundation"), Cube, FLinearColor(.027f,.039f,.047f));
    Base->AddInstance(FTransform(FQuat::Identity,FVector(0,0,-36),FVector(80.f,22.f,.45f)));
    auto* Floors = MakeBatch(TEXT("Floors"), Cube, FLinearColor(.24f,.31f,.32f));
    auto* AlternateFloors = MakeBatch(TEXT("AlternateFloors"), Cube, FLinearColor(.21f,.27f,.28f));
    auto* Walls = MakeBatch(TEXT("Walls"), Cube, FLinearColor(.43f,.49f,.48f));
    for (int32 Y=0; Y<Rows; ++Y) for (int32 X=0; X<Columns; ++X)
    {
        if (Cells[Y*Columns+X])
        {
            auto* Batch = ((X+Y)%2) ? Floors : AlternateFloors;
            Batch->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y),FVector(.96f,.96f,.16f)));
        }
        else
        {
            bool Adjacent = false;
            for (int32 DY=-1; DY<=1; ++DY) for (int32 DX=-1; DX<=1; ++DX)
            {
                int32 NX=X+DX, NY=Y+DY;
                if (NX>=0 && NX<Columns && NY>=0 && NY<Rows && Cells[NY*Columns+NX]) Adjacent=true;
            }
            if (Adjacent) Walls->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y,60),FVector(.98f,.98f,1.20f)));
        }
    }
    auto* Doors = MakeBatch(TEXT("Doors"),Cube,FLinearColor(.55f,.29f,.10f));
    for (FIntPoint P : TArray<FIntPoint>{{13,5},{18,5},{31,8},{56,4},{68,9},{18,16},{38,15},{60,16}})
        Doors->AddInstance(FTransform(FQuat::Identity,CellPosition(P.X,P.Y,58),FVector(.20f,.86f,1.f)));
    auto* Water = MakeBatch(TEXT("Pool"),Cube,FLinearColor(.025f,.32f,.48f));
    for (int Y=4;Y<7;++Y) for (int X=65;X<71;++X)
        Water->AddInstance(FTransform(FQuat::Identity,CellPosition(X,Y,10),FVector(.95f,.95f,.06f)));
    auto* Stairs = MakeBatch(TEXT("Stairs"),Cube,FLinearColor(.71f,.77f,.67f));
    for (FIntPoint P : TArray<FIntPoint>{{5,4},{73,17}})
        for (int I=0;I<4;++I)
            Stairs->AddInstance(FTransform(FQuat::Identity,CellPosition(P.X,P.Y,14+I*7)+FVector(0,I*21-32,0),FVector(.75f,.19f,.12f+I*.14f)));
    auto* Player = MakeBatch(TEXT("Player"),TEXT("/Engine/BasicShapes/Cone.Cone"),FLinearColor(1.f,.65f,.13f));
    Player->AddInstance(FTransform(FQuat::Identity,CellPosition(9,6,61),FVector(.65f,.65f,1.f)));
    auto* Enemies = MakeBatch(TEXT("Creatures"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.73f,.13f,.14f));
    for (FIntPoint P : TArray<FIntPoint>{{24,4},{42,4},{29,15},{50,16},{70,15}})
        Enemies->AddInstance(FTransform(FQuat::Identity,CellPosition(P.X,P.Y,49),FVector(.44f,.44f,.55f)));
    auto* Items = MakeBatch(TEXT("Items"),TEXT("/Engine/BasicShapes/Sphere.Sphere"),FLinearColor(.24f,.79f,.65f));
    for (FIntPoint P : TArray<FIntPoint>{{7,15},{27,6},{46,3},{34,17},{63,18},{74,6}})
        Items->AddInstance(FTransform(FQuat::Identity,CellPosition(P.X,P.Y,32),FVector(.37f,.37f,.37f)));
    BoardMin=FVector(-4000,-1100,-60); BoardMax=FVector(4000,1100,140);
}

void ADungeonPrototype::BeginPlay()
{
    Super::BeginPlay();
    ShowEntityGlyphs=!FParse::Param(FCommandLine::Get(),TEXT("HideEntityGlyphs"));
    UE_LOG(LogTemp,Display,TEXT("ENTITY_GLYPHS initial=%s"),ShowEntityGlyphs?TEXT("ON"):TEXT("OFF"));
    StaticStudy=FParse::Param(FCommandLine::Get(),TEXT("StaticStudy"));
    ArtStudy=FParse::Param(FCommandLine::Get(),TEXT("ArtStudy"));
    FurStudy=FParse::Param(FCommandLine::Get(),TEXT("FurStudy"));
    SculptedCreatures=FParse::Param(FCommandLine::Get(),TEXT("SculptedCreatures"));
    CaptureLive=FParse::Param(FCommandLine::Get(),TEXT("CaptureLive"));
    BoardMin=FVector(-4000,-1100,-60); BoardMax=FVector(4000,1100,140);
    if(FurStudy) GenerateFurStudy();
    else if(ArtStudy) GenerateArtStudy();
    else if(StaticStudy) GenerateDungeon();
    else StartLiveGame();
    // Studio lighting belongs to the art fixtures. The live cave has no sun;
    // only its local sources cast shadows.
    if(ArtStudy || StaticStudy || FurStudy)
    {
        auto* Sun = GetWorld()->SpawnActor<ADirectionalLight>();
        Sun->GetComponent()->SetMobility(EComponentMobility::Movable);
        Sun->SetActorRotation(ArtStudy?FRotator(-42,-100,0):FRotator(-32,-120,0));
        Sun->GetComponent()->SetIntensity(ArtStudy?4.2f:StaticStudy?5.f:1.5f);
        Sun->GetComponent()->LightingChannels.bChannel1=true;
        Sun->GetComponent()->SetCastShadows(true);
        Sun->GetComponent()->bUseRayTracedDistanceFieldShadows = false;
        Sun->GetComponent()->SetForwardShadingPriority(1);
        Sun->GetComponent()->SetLightColor(ArtStudy?FLinearColor(1.f,.86f,.69f):FLinearColor(1.f,.91f,.77f));
        auto* Fill = GetWorld()->SpawnActor<ADirectionalLight>();
        Fill->GetComponent()->SetMobility(EComponentMobility::Movable);
        Fill->SetActorRotation(FRotator(-65,130,0));
        Fill->GetComponent()->SetIntensity(ArtStudy?1.15f:StaticStudy?.8f:.85f);
        Fill->GetComponent()->LightingChannels.bChannel1=true;
        Fill->GetComponent()->SetCastShadows(false);
        Fill->GetComponent()->SetLightColor(FLinearColor(.65f,.79f,1.f));
    }
    else CreateAmbientLight();
    if(ArtStudy)
    {
        auto* Bounce=GetWorld()->SpawnActor<ADirectionalLight>();
        Bounce->GetComponent()->SetMobility(EComponentMobility::Movable);
        Bounce->SetActorRotation(FRotator(-35,25,0));
        Bounce->GetComponent()->SetIntensity(.7f);
        Bounce->GetComponent()->SetCastShadows(false);
        Bounce->GetComponent()->SetLightColor(FLinearColor(1.f,.83f,.64f));
        ArtLightsReady=true;
        for(const FVector Position:TArray<FVector>{FVector(-458,-220,118),FVector(458,200,118)})
        {
            auto* Torch=GetWorld()->SpawnActor<APointLight>();
            auto* Light=Torch->PointLightComponent.Get();
            Light->SetMobility(EComponentMobility::Movable);
            Torch->SetActorLocation(Position);
            ArtLightsReady &= Light->GetComponentLocation().Equals(Position,1.f);
            Light->IntensityUnits=ELightUnits::Lumens;
            Light->SetIntensity(260.f);
            Light->SetAttenuationRadius(330.f);
            Light->SetSourceRadius(6.f);
            Light->SetLightColor(FLinearColor(1.f,.42f,.12f));
            Light->SetCastShadows(true);
            UE_LOG(LogTemp,Display,TEXT("ART_TORCH_POSITION %s"),*Light->GetComponentLocation().ToString());
        }
    }
    if (auto* PC = GetWorld()->GetFirstPlayerController())
    {
        PC->SetViewTarget(this);
        // The component/CalcCamera supplies corrected ortho planes and focus.
        // Avoid the manager replacing that focus with this board actor's origin.
        PC->PlayerCameraManager->bAutoCalculateOrthoPlanes=false;
        PC->bShowMouseCursor=true;
    }
    if(FurStudy)
    {
        FitFurCamera();
        FTimerHandle Handle;
        GetWorldTimerManager().SetTimer(Handle,this,&ADungeonPrototype::CaptureFurStudy,15.f,false);
    }
    else FitCamera();
    if(ArtStudy)
    {
        FString View; FParse::Value(FCommandLine::Get(),TEXT("ArtView="),View);
        if(View==TEXT("detail")) { ZoomFactor=2.2f; CameraFocus=FVector(0,60,30); FollowHero=false; }
        else if(View==TEXT("level")) { ZoomFactor=1.f; BoardMin=FVector(-4000,-1100,-60); BoardMax=FVector(4000,1100,160); }
        else if(View==TEXT("eye")) { FirstPerson=true; FirstPersonBlend=1.f; }
        FitCamera();
        if(FParse::Param(FCommandLine::Get(),TEXT("CaptureArt")))
        {
            FTimerHandle Handle;
            GetWorldTimerManager().SetTimer(Handle,this,&ADungeonPrototype::CaptureArtStudy,15.f,false);
        }
    }
    if (StaticStudy && FParse::Param(FCommandLine::Get(),TEXT("CapturePrototype")))
    {
        FTimerHandle Handle;
        GetWorldTimerManager().SetTimer(Handle,this,&ADungeonPrototype::CaptureAndValidate,15.f,false);
    }
}

void ADungeonPrototype::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if(FurStudy) { FitFurCamera(); return; }
    if(Session) TickLiveGame();
    FirstPersonBlend=FMath::FInterpConstantTo(FirstPersonBlend,FirstPerson?1.f:0.f,DeltaSeconds,1.25f);
    FitCamera();
    if(Session) UpdateTileFallbackFacing();
}

void ADungeonPrototype::FitCamera()
{
    UpdateOverviewLighting();
    auto* PC=GetWorld()->GetFirstPlayerController();
    int32 W=0,H=0;
    if (PC) PC->GetViewportSize(W,H);
    if (W<=0 || H<=0) return;
    const bool Resized=LastViewport!=FIntPoint(W,H);
    LastViewport=FIntPoint(W,H);
    const FRotator Rotation=ArtStudy?FRotator(-55,-125,0):FRotator(-58,-75,0);
    const FVector Forward=Rotation.Vector();
    const FVector Right=FRotationMatrix(Rotation).GetUnitAxis(EAxis::Y);
    const FVector Up=FRotationMatrix(Rotation).GetUnitAxis(EAxis::Z);
    float ExtentX=0,ExtentY=0;
    for (int32 I=0;I<8;++I)
    {
        const FVector Corner((I&1)?BoardMax.X:BoardMin.X,(I&2)?BoardMax.Y:BoardMin.Y,(I&4)?BoardMax.Z:BoardMin.Z);
        ExtentX=FMath::Max(ExtentX,FMath::Abs(FVector::DotProduct(Corner,Right)));
        ExtentY=FMath::Max(ExtentY,FMath::Abs(FVector::DotProduct(Corner,Up)));
    }
    // Reserve 6% at each side and 16% above/below for HUD and breathing room.
    const float Aspect=float(W)/H;
    Camera->SetAspectRatio(Aspect);
    OverviewWidth=FMath::Max(2*ExtentX/.88f,2*ExtentY*Aspect/(ArtStudy?.86f:.68f));
    Camera->SetOrthoWidth(OverviewWidth/ZoomFactor);
    if(IsFirstPerson())
    {
        Camera->ProjectionMode=ECameraProjectionMode::Perspective;
        Camera->FieldOfView=85.f;
        FVector2D Mouse=FVector2D::ZeroVector;
        const bool Looking=FirstPerson && FirstPersonBlend>=1.f && !(Session && Session->Awaiting && !Session->IsCommand())
            && PC->IsInputKeyDown(EKeys::RightMouseButton) && PC->GetMousePosition(Mouse.X,Mouse.Y);
        if(Looking && WasLooking)
        {
            const FVector2D Delta=Mouse-LastLookMouse;
            EyeRotation.Yaw+=Delta.X*.25f;
            EyeRotation.Pitch=FMath::Clamp(EyeRotation.Pitch-Delta.Y*.25f,-70.f,70.f);
        }
        WasLooking=Looking;
        if(Looking) LastLookMouse=Mouse;
        const FVector Eye=ArtStudy?FVector(0,150,95):Session && Session->IsReady()?CellPosition(Session->Hero.X,Session->Hero.Y,80.f):CellPosition(9,6,80.f);
        const float Distance=Camera->OrthoWidth/(2.f*FMath::Tan(FMath::DegreesToRadians(Camera->FieldOfView*.5f)));
        const float Alpha=FMath::SmoothStep(0.f,1.f,FirstPersonBlend);
        const auto Path=FDungeonCameraTransition::Make(CameraFocus-Forward*Distance,Forward,Eye,EyeRotation.Vector());
        Camera->SetWorldLocation(Path.Position(Alpha));
        Camera->SetWorldRotation(FDungeonCameraTransition::ViewRotation(Rotation,EyeRotation,Alpha));
        if(auto* Player=LiveBatches.Find(TEXT("Player"))) (*Player)->SetVisibility(false);
        if(auto* Player=LiveBatches.Find(TEXT("PlayerVolume"))) (*Player)->SetVisibility(false);
        if(auto* Player=LiveBatches.Find(TEXT("PlayerTileFallback"))) (*Player)->SetVisibility(false);
        return;
    }
    Camera->ProjectionMode=ECameraProjectionMode::Orthographic;
    Camera->SetWorldRotation(Rotation);
    if(auto* Player=LiveBatches.Find(TEXT("Player"))) (*Player)->SetVisibility(true);
    if(auto* Player=LiveBatches.Find(TEXT("PlayerVolume"))) (*Player)->SetVisibility(true);
    if(auto* Player=LiveBatches.Find(TEXT("PlayerTileFallback"))) (*Player)->SetVisibility(true);
    if(ZoomFactor<=1.f) CameraFocus=FVector::ZeroVector;
    else if(FollowHero && Session && Session->IsReady()) CameraFocus=CellPosition(Session->Hero.X,Session->Hero.Y);

    FVector2D Mouse=FVector2D::ZeroVector;
    const bool Panning=ZoomFactor>1.f && PC && PC->IsInputKeyDown(EKeys::MiddleMouseButton)
        && !(Session && Session->Awaiting && Session->PromptType==TEXT("menu")) && PC->GetMousePosition(Mouse.X,Mouse.Y);
    if(Panning && WasPanning)
    {
        const FVector2D Delta=Mouse-LastPanMouse;
        const float UnitsPerPixel=Camera->OrthoWidth/W;
        const FVector PlanarUp=Up.GetSafeNormal2D()/Up.Size2D();
        CameraFocus+=(-Right*Delta.X+PlanarUp*Delta.Y)*UnitsPerPixel;
        CameraFocus.X=FMath::Clamp(CameraFocus.X,BoardMin.X,BoardMax.X);
        CameraFocus.Y=FMath::Clamp(CameraFocus.Y,BoardMin.Y,BoardMax.Y);
        FollowHero=false;
    }
    WasPanning=Panning;
    if(Panning) LastPanMouse=Mouse;
    Camera->SetWorldLocation(CameraFocus-Forward*15000.f);
    if(Resized) UE_LOG(LogTemp,Display,TEXT("PROTOTYPE_CAMERA viewport=%dx%d orthoWidth=%.1f grid=79x21"),W,H,Camera->OrthoWidth);
}

void ADungeonPrototype::AdjustZoom(float Steps)
{
    if(IsFirstPerson()) return;
    ZoomFactor=FMath::Clamp(ZoomFactor*FMath::Pow(1.2f,Steps),1.f,8.f);
    if(ZoomFactor<=1.001f) ResetOverview();
    FitCamera();
    UE_LOG(LogTemp,Display,TEXT("DUNGEON_ZOOM factor=%.3f width=%.1f"),ZoomFactor,Camera->OrthoWidth);
}

void ADungeonPrototype::ResetOverview()
{
    FirstPerson=false; FirstPersonBlend=0.f; WasLooking=false;
    ZoomFactor=1.f; CameraFocus=FVector::ZeroVector; FollowHero=true; WasPanning=false;
    FitCamera();
    UE_LOG(LogTemp,Display,TEXT("DUNGEON_OVERVIEW_RESTORED width=%.1f"),Camera->OrthoWidth);
}

void ADungeonPrototype::ToggleFirstPerson()
{
    if(Session && !Session->IsReady()) return;
    FirstPerson=!FirstPerson;
    // EyeRotation already records the latest actual movement or right-drag look.
    // Entry must not replace that facing with an unrelated open corridor.
    WasPanning=false; WasLooking=false;
    UE_LOG(LogTemp,Display,TEXT("DUNGEON_FIRST_PERSON %s turn=%d"),FirstPerson?TEXT("ON"):TEXT("OFF"),Session?Session->Turn:0);
}

void ADungeonPrototype::CaptureAndValidate()
{
    auto* PC=GetWorld()->GetFirstPlayerController();
    bool bFits=true;
    FVector2D Min(1.e9,1.e9),Max(-1.e9,-1.e9);
    for (int32 I=0;I<8;++I)
    {
        FVector2D Screen=FVector2D::ZeroVector;
        const FVector Corner((I&1)?BoardMax.X:BoardMin.X,(I&2)?BoardMax.Y:BoardMin.Y,(I&4)?BoardMax.Z:BoardMin.Z);
        if (!PC || !PC->ProjectWorldLocationToScreen(Corner,Screen))
        {
            bFits=false;
            continue;
        }
        Min.X=FMath::Min(Min.X,Screen.X); Min.Y=FMath::Min(Min.Y,Screen.Y);
        Max.X=FMath::Max(Max.X,Screen.X); Max.Y=FMath::Max(Max.Y,Screen.Y);
    }
    bFits &= Min.X>=0 && Max.X<=LastViewport.X && Min.Y>=LastViewport.Y*.15f && Max.Y<=LastViewport.Y*.85f;
    // Containment alone would also pass a tiny board. Require useful screen coverage.
    bFits &= (Max.X-Min.X)>=LastViewport.X*.85f || (Max.Y-Min.Y)>=LastViewport.Y*.65f;
    const bool ZoomCapture=FParse::Param(FCommandLine::Get(),TEXT("CaptureZoom"));
    const bool EyeCapture=FParse::Param(FCommandLine::Get(),TEXT("CaptureFirstPerson"));
    if(EyeCapture)
    {
        const FVector Eye=CellPosition(Session->Hero.X,Session->Hero.Y,80.f);
        bFits=FirstPersonReturnChecked && FirstPerson && FirstPersonBlend==1.f && Camera->ProjectionMode==ECameraProjectionMode::Perspective
            && Camera->GetComponentLocation().Equals(Eye,1.f)
            && FVector::DotProduct(Camera->GetForwardVector(),EyeRotation.Vector())>.9999;
        UE_LOG(LogTemp,Display,TEXT("DUNGEON_FIRST_PERSON_CHECK %s eye=%s restored=%d"),bFits?TEXT("PASS"):TEXT("FAIL"),*Camera->GetComponentLocation().ToString(),FirstPersonReturnChecked);
    }
    else if(ZoomCapture)
    {
        FVector2D HeroScreen=FVector2D::ZeroVector;
        const float ExpectedZoom=(FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch3")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch4")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch5")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch6")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch7")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch8")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch9")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch10")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch11")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch12")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch13")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch14")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch20")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch19")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch18")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch17")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch16")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewCreatureBatch15")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewSpecialBatch1")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewObjectBatch1")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewTileFallback")) || FParse::Param(FCommandLine::Get(),TEXT("PreviewHumanPlayers")))?8.f:3.f;
        bFits=Session && Session->IsReady() && FMath::Abs(ZoomFactor-ExpectedZoom)<.1f
            && FMath::IsNearlyEqual(Camera->OrthoWidth*ZoomFactor,OverviewWidth,1.f)
            && PC->ProjectWorldLocationToScreen(CellPosition(Session->Hero.X,Session->Hero.Y),HeroScreen)
            && FMath::Abs(HeroScreen.X-LastViewport.X*.5f)<LastViewport.X*.1f
            && FMath::Abs(HeroScreen.Y-LastViewport.Y*.5f)<LastViewport.Y*.1f;
        UE_LOG(LogTemp,Display,TEXT("DUNGEON_ZOOM_CHECK %s factor=%.3f width=%.1f hero=%s"),bFits?TEXT("PASS"):TEXT("FAIL"),ZoomFactor,Camera->OrthoWidth,*HeroScreen.ToString());
    }
    else UE_LOG(LogTemp,Display,TEXT("PROTOTYPE_FRAME_CHECK %s min=%s max=%s"),bFits?TEXT("PASS"):TEXT("FAIL"),*Min.ToString(),*Max.ToString());
    if(CaptureLive)
    {
        const bool LivePass=Session && Session->Connected && Session->IsCommand() && Session->Turn>=4 && Session->KnownCellCount()>5 && Session->KnownCellCount()<Columns*Rows && AutoMoved;
        bFits &= LivePass;
        UE_LOG(LogTemp,Display,TEXT("NETHACK_LIVE_CHECK %s turn=%d known=%d hero=%s"),LivePass?TEXT("PASS"):TEXT("FAIL"),Session?Session->Turn:0,Session?Session->KnownCellCount():0,Session?*Session->Hero.ToString():TEXT("none"));
    }
    const bool TileCapture=FParse::Param(FCommandLine::Get(),TEXT("CaptureDefaultTiles"));
    if(TileCapture)
    {
        const auto* Player=LiveBatches.Find(TEXT("PlayerVolume"));
        int32 Figures=0;
        for(const auto& Entry:LiveBatches) if(Entry.Key.ToString().StartsWith(TEXT("Tile_"))) Figures+=Entry.Value->GetInstanceCount();
        const bool TilePass=Player && (*Player)->GetInstanceCount()==1 && !HeroVolumeKey.IsEmpty() && Session && Session->Depth==1;
        bFits &= TilePass;
        UE_LOG(LogTemp,Display,TEXT("DEFAULT_TILES_CHECK %s hero=%s creatures=%d depth=%d"),TilePass?TEXT("PASS"):TEXT("FAIL"),*HeroVolumeKey,Figures,Session?Session->Depth:0);
    }
    FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/(TileCapture?TEXT("Screenshots/DefaultTilesDungeon.png"):EyeCapture?TEXT("Screenshots/FirstPersonDungeon.png"):ZoomCapture?TEXT("Screenshots/ZoomedDungeon.png"):CaptureLive?TEXT("Screenshots/LiveDungeon.png"):TEXT("Screenshots/DungeonPrototype.png")),true,false);
    FTimerHandle Handle;
    GetWorldTimerManager().SetTimer(Handle,[bFits](){ FPlatformMisc::RequestExitWithStatus(false,bFits?0:1); },3.f,false);
}

float ADungeonPrototypeHUD::DrawGameTitle(float X,float Y,float Scale,FLinearColor Color)
{
    if(!TitleFont) TitleFont=LoadObject<UFont>(nullptr,TEXT("/Engine/EngineFonts/Roboto.Roboto"));
    check(TitleFont);
    const float Start=X;
    const TCHAR* Runs[]={TEXT("n"),TEXT("u"),TEXT("th"),TEXT("e"),TEXT("ck")};
    for(int32 I=0;I<UE_ARRAY_COUNT(Runs);++I)
    {
        const FSlateFontInfo Font(TitleFont,12,I==1 || I==3?FName(TEXT("Bold")):FName(TEXT("Regular")));
        FCanvasTextItem Text(FVector2D(X,Y),FText::FromString(Runs[I]),Font,Color);
        Text.Scale=FVector2D(Scale);
        Canvas->DrawItem(Text);
        X+=Text.DrawnSize.X;
    }
    return X-Start;
}

void ADungeonPrototypeHUD::DrawHUD()
{
    Super::DrawHUD();
    if (!Canvas) return;
    if(auto* Dungeon=Cast<ADungeonPrototype>(GetOwningPlayerController()->GetViewTarget()))
    {
        if(Dungeon->IsFurStudy()) return;
        if(auto* Live=Dungeon->GetSession()) { DrawLiveHUD(*Live); return; }
        if(Dungeon->IsArtStudy())
        {
            const float Scale=Canvas->SizeX/1600.f;
            const FLinearColor TitleColor(.85f,.74f,.55f);
            const float TitleWidth=DrawGameTitle(32*Scale,24*Scale,Scale,TitleColor);
            DrawText(TEXT("  /  PAINTED MINIATURE STUDY"),TitleColor,32*Scale+TitleWidth,24*Scale,GEngine->GetMediumFont(),Scale);
            DrawText(TEXT("BLENDER MESHES / UNREAL REAL-TIME RENDER  |  WHEEL Zoom  |  MIDDLE-DRAG Pan  |  Ctrl+F First person  |  RIGHT-DRAG Look  |  F5 Reset"),FLinearColor(.65f,.7f,.7f),32*Scale,Canvas->SizeY-36*Scale,GEngine->GetSmallFont(),.85f*Scale);
            return;
        }
    }
    const float W=Canvas->SizeX,H=Canvas->SizeY;
    const float S=FMath::Clamp(W/1600.f,.65f,1.5f);
    const FLinearColor Ink(.81f,.86f,.84f),Muted(.40f,.51f,.53f),Gold(.95f,.66f,.23f);
    DrawRect(FLinearColor(.018f,.028f,.036f,.98f),0,0,W,84*S);
    DrawRect(Gold,32*S,24*S,3*S,38*S);
    DrawGameTitle(48*S,19*S,S,Ink);
    DrawText(TEXT("THE DUNGEONS OF DOOM"),Muted,49*S,53*S,GEngine->GetSmallFont(),.9f*S);
    DrawText(TEXT("DLVL 1   /   THE ENTRANCE"),Gold,W-300*S,31*S,GEngine->GetSmallFont(),1.f*S);
    DrawRect(FLinearColor(.15f,.23f,.25f),32*S,84*S,W-64*S,1);
    DrawRect(FLinearColor(.018f,.028f,.036f,.98f),0,H-112*S,W,112*S);
    DrawRect(FLinearColor(.15f,.23f,.25f),32*S,H-112*S,W-64*S,1);
    DrawText(TEXT("The stairs disappear into the stone below."),Ink,32*S,H-89*S,GEngine->GetMediumFont(),1.f*S);
    DrawText(TEXT("@  ADVENTURER    HP 16/16    AC 10    LV 1"),Gold,32*S,H-48*S,GEngine->GetSmallFont(),1.f*S);
    DrawText(TEXT("PLAYER"),Gold,W-510*S,H-48*S,GEngine->GetSmallFont(),.9f*S);
    DrawText(TEXT("CREATURE"),FLinearColor(.9f,.24f,.23f),W-415*S,H-48*S,GEngine->GetSmallFont(),.9f*S);
    DrawText(TEXT("ITEM"),FLinearColor(.3f,.85f,.69f),W-290*S,H-48*S,GEngine->GetSmallFont(),.9f*S);
    DrawText(TEXT("STATIC STUDY  /  01"),Muted,W-200*S,H-89*S,GEngine->GetSmallFont(),.85f*S);
}

ADungeonPrototypeGameMode::ADungeonPrototypeGameMode()
{
    DefaultPawnClass=nullptr;
    HUDClass=ADungeonPrototypeHUD::StaticClass();
    PlayerControllerClass=ADungeonPlayerController::StaticClass();
}

void ADungeonPrototypeGameMode::StartPlay()
{
    Super::StartPlay();
    GetWorld()->SpawnActor<ADungeonPrototype>();
}

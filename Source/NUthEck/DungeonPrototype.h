#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "GameFramework/PlayerController.h"
#include "Engine/GameViewportClient.h"
#include "NetHackSession.h"
#include "DungeonPrototype.generated.h"

class UCameraComponent;
class UInstancedStaticMeshComponent;

// Default presentation for the live NetHack process; -StaticStudy retains the fixture.
UCLASS()
class ADungeonPrototype : public AActor
{
    GENERATED_BODY()
public:
    ADungeonPrototype();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void EndPlay(const EEndPlayReason::Type Reason) override;
    virtual void CalcCamera(float DeltaTime,FMinimalViewInfo& OutResult) override;
    FNetHackSession* GetSession() const { return Session.Get(); }
    bool HandleLiveKey(FKey Key, bool Control);
    bool HandleLiveCharacter(TCHAR Character);
    void SetTextRepeatSuppressed(bool Suppressed) { TextRepeatSuppressed=Suppressed; }
    void AdjustZoom(float Steps);
    void ResetOverview();
    float GetZoomFactor() const { return ZoomFactor; }
    void ToggleFirstPerson();
    bool IsFirstPerson() const { return FirstPerson || FirstPersonBlend>0.f; }
    bool ShouldShowEntityGlyphs() const { return ShowEntityGlyphs; }
    bool IsArtStudy() const { return ArtStudy; }
    bool IsFurStudy() const { return FurStudy; }
private:
    static constexpr int32 Columns = 79;
    static constexpr int32 Rows = 21;
    static constexpr float CellSize = 100.f;
    TArray<uint8> Cells;
    UPROPERTY() TObjectPtr<UCameraComponent> Camera;
    FVector BoardMin;
    FVector BoardMax;
    FIntPoint LastViewport = FIntPoint::ZeroValue;
    UInstancedStaticMeshComponent* MakeBatch(const TCHAR* Name, const TCHAR* MeshPath, FLinearColor Color);
    void GenerateDungeon();
    void GenerateArtStudy();
    void CaptureArtStudy();
    void GenerateFurStudy();
    void FitFurCamera();
    void CaptureFurStudy();
    void FitCamera();
    void CaptureAndValidate();
    FVector CellPosition(int32 X, int32 Y, float Z = 0.f) const;
    void StartLiveGame(bool NewGame=false);
    void RebuildLiveMap();
    void UpdateAtmosphere();
    void CreateAmbientLight();
    void UpdateOverviewLighting();
    UPROPERTY() TArray<TObjectPtr<class UPointLightComponent>> MapFillLights;
    void TickAtmosphere();
    UPROPERTY() TArray<TObjectPtr<class UPointLightComponent>> AtmosphereLights;
    UInstancedStaticMeshComponent* GetDefaultTileBatch(const FNetHackCell& Cell,bool Hero);
    UInstancedStaticMeshComponent* GetDisplayedObjectBatch(const FNetHackCell& Cell);
    UInstancedStaticMeshComponent* GetFountainBatch(const FNetHackCell& Cell);
    void VerifySpecialBatch1();
    void VerifyObjectBatch1();
    bool AddTileFallback(const FNetHackCell& Cell,int32 X,int32 Y,bool Hero=false);
    void UpdateTileFallbackFacing();
    void VerifyTileFallback();
    TSet<FString> MissingTileFigures;
    FString HeroVolumeKey;
    void TickLiveGame();
    bool VerifyPresentationControls();
    void CaptureFirstPersonTransition();
    void VerifyAndCaptureHumanPlayers();
    UPROPERTY() TMap<FName,TObjectPtr<UInstancedStaticMeshComponent>> LiveBatches;
    TUniquePtr<FNetHackSession> Session;
    bool StaticStudy=false, CaptureLive=false, LiveCaptureRequested=false;
    bool ArtStudy=false,ArtLightsReady=false;
    bool FurStudy=false;
    bool SculptedCreatures=false;
    bool ShowEntityGlyphs=true;
    int32 AutoCommands=0;
    bool AutoMoved=false;
    FIntPoint AutoFirstPosition=FIntPoint(-1,-1);
    double LiveStartedTime=0;
    float ZoomFactor=1.f,OverviewWidth=10000.f;
    FVector CameraFocus=FVector::ZeroVector;
    FVector2D LastPanMouse=FVector2D::ZeroVector;
    bool FollowHero=true,WasPanning=false,TextRepeatSuppressed=false;
    TCHAR SuppressedNumpadCharacter=0;
    double NumpadCharacterTime=0;
    bool FirstPerson=false,WasLooking=false;
    float FirstPersonBlend=0.f;
    FRotator EyeRotation=FRotator(0,-90,0);
    FIntPoint PreviousHero=FIntPoint(-1,-1);
    FVector2D LastLookMouse=FVector2D::ZeroVector;
    bool FirstPersonReturnChecked=false;
};

UCLASS()
class UDungeonGameViewportClient : public UGameViewportClient
{
    GENERATED_BODY()
public:
    virtual bool InputChar(FViewport* InViewport,int32 ControllerId,TCHAR Character) override;
};

UCLASS()
class ADungeonPrototypeHUD : public AHUD
{
    GENERATED_BODY()
public:
    virtual void DrawHUD() override;
private:
    void DrawLiveHUD(FNetHackSession& Session);
};

UCLASS()
class ADungeonPlayerController : public APlayerController
{
    GENERATED_BODY()
public:
    virtual bool InputKey(const FInputKeyEventArgs& Params) override;
    virtual void FlushPressedKeys() override;
private:
    bool LeftControlHeld=false,RightControlHeld=false,LeftAltHeld=false,RightAltHeld=false;
};

UCLASS()
class ADungeonPrototypeGameMode : public AGameModeBase
{
    GENERATED_BODY()
public:
    ADungeonPrototypeGameMode();
    virtual void StartPlay() override;
};

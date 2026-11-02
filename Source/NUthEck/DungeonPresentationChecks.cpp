#include "DungeonPrototype.h"
#include "DungeonCameraTransition.h"
#include "Camera/CameraComponent.h"
#include "Components/PointLightComponent.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "TimerManager.h"
#include "UnrealClient.h"

// Explicit capture-only checks. These never send input to the native game.
bool ADungeonPrototype::VerifyPresentationControls()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    const bool Labels=ShowEntityGlyphs,SavedFirstPerson=FirstPerson,SavedFollow=FollowHero;
    const float SavedBlend=FirstPersonBlend,SavedZoom=ZoomFactor;
    const FVector SavedFocus=CameraFocus;
    const FRotator SavedLook=EyeRotation,SavedOrbit=OverviewOrbitOffset;
    bool Passed=HandleLiveKey(EKeys::F7,false) && ShowEntityGlyphs!=Labels;
    // The overview lift must never reach current geometry or survive at room
    // scale/first person. Exercise real camera updates without native input.
    Passed &= MapFillLights.Num()==2;
    FirstPerson=false;FirstPersonBlend=0;ZoomFactor=1;FitCamera();
    for(const auto& Light:MapFillLights)
        Passed &= Light->Intensity>0 && !Light->CastShadows
            && !Light->LightingChannels.bChannel0 && Light->LightingChannels.bChannel1;
    ZoomFactor=2.5f;FitCamera();
    for(const auto& Light:MapFillLights) Passed &= Light->Intensity==0;
    ZoomFactor=1;FirstPerson=true;FirstPersonBlend=1;FitCamera();
    for(const auto& Light:MapFillLights) Passed &= Light->Intensity==0;
    FirstPerson=SavedFirstPerson;FirstPersonBlend=SavedBlend;ZoomFactor=SavedZoom;FitCamera();
    Passed &= HandleLiveKey(EKeys::F7,false) && ShowEntityGlyphs==Labels;
    const FVector Eye=CellPosition(Session->Hero.X,Session->Hero.Y,80.f);
    // Exercise the same gesture handler as the viewport and real camera fit.
    // Horizontal motion only changes heading; vertical motion only changes tilt.
    FirstPerson=false;FirstPersonBlend=0;ZoomFactor=3;FollowHero=false;
    CameraFocus=SavedFocus;OverviewOrbitOffset=FRotator::ZeroRotator;
    UpdateOverviewDrag(FVector2D(100,100),false);
    UpdateOverviewDrag(FVector2D(100,100),true);
    const FRotator InitialOrbit=OverviewRotation();
    Passed &= OverviewOrbitOffset.IsZero();
    UpdateOverviewDrag(FVector2D(340,100),true);
    Passed &= FMath::IsNearlyEqual(OverviewRotation().Yaw,InitialOrbit.Yaw+60.f)
        && OverviewRotation().Pitch==InitialOrbit.Pitch && OverviewRotation().Roll==0;
    UpdateOverviewDrag(FVector2D(340,28),true);
    const FRotator DraggedOrbit=OverviewRotation();
    Passed &= FMath::IsNearlyEqual(DraggedOrbit.Pitch,InitialOrbit.Pitch+18.f)
        && DraggedOrbit.Yaw==InitialOrbit.Yaw+60.f && DraggedOrbit.Roll==0;
    FitCamera();
    Passed &= Camera->GetComponentRotation().Equals(DraggedOrbit,.001)
        && CameraFocus.Equals(SavedFocus,.001) && !FollowHero;
    const FRotator ReleasedOffset=OverviewOrbitOffset;
    UpdateOverviewDrag(FVector2D(10000,10000),false);
    UpdateOverviewDrag(FVector2D(-10000,-10000),true);
    Passed &= OverviewOrbitOffset.Equals(ReleasedOffset,.001);
    UpdateOverviewDrag(FVector2D(-10000,10000),true);
    Passed &= FMath::IsNearlyEqual(OverviewRotation().Pitch,-85.f);
    UpdateOverviewDrag(FVector2D(-10000,-10000),true);
    Passed &= FMath::IsNearlyEqual(OverviewRotation().Pitch,-20.f) && OverviewRotation().Roll==0;
    UpdateOverviewDrag(FVector2D::ZeroVector,false);
    OverviewOrbitOffset=ReleasedOffset;
    AdjustZoom(-100.f); // Reaching full-level zoom preserves the selected angle.
    Passed &= OverviewRotation().Equals(DraggedOrbit,.001);
    HandleLiveKey(EKeys::F5,false);
    Passed &= OverviewOrbitOffset.IsZero() && ZoomFactor==1.f;
    OverviewOrbitOffset=ReleasedOffset;ZoomFactor=SavedZoom;FitCamera();
    const FRotator Overhead=OverviewRotation();
    int32 Paths=0;
    for(const FVector Offset:{FVector::ZeroVector,FVector(3000,-1800,0)})
    for(float Zoom:{1.f,3.f,8.f}) for(float Pitch:{-70.f,-35.f,0.f,40.f,70.f}) for(int32 Heading=0;Heading<8;++Heading)
    {
        const FRotator Look(Pitch,Heading*45.f,0);
        const double Distance=OverviewWidth/Zoom/(2.*FMath::Tan(FMath::DegreesToRadians(42.5)));
        const FVector Start=SavedFocus+Offset-Overhead.Vector()*Distance;
        const auto Path=FDungeonCameraTransition::Make(Start,Overhead.Vector(),Eye,Look.Vector());
        Passed &= Path.Position(0).Equals(Start,.001) && Path.Position(1).Equals(Eye,.001);
        Passed &= FVector::DotProduct(Path.Tangent(1).GetSafeNormal(),Look.Vector())>.99999;
        Passed &= FVector::DotProduct(Path.Tangent(0).GetSafeNormal(),Overhead.Vector())>.99999;
        for(int32 Sample=0;Sample<=40;++Sample)
        {
            const double T=Sample/40.;
            Passed &= !Path.Position(T).ContainsNaN() && Path.Position(T).Z>=19.999;
            const auto View=FDungeonCameraTransition::ViewRotation(Overhead,Look,T);
            Passed &= FMath::Abs(View.Roll)<.0001 && !View.ContainsNaN();
        }
        // Arrival really travels forward along the gaze axis, even for diagonal/pitched views.
        Passed &= FVector::DotProduct((Path.Position(1)-Path.Position(.999)).GetSafeNormal(),Look.Vector())>.999;
        ++Paths;
    }
    for(int32 Heading=0;Heading<8;++Heading)
    {
        CameraFocus=SavedFocus+FVector(150,-75,0);FollowHero=false;
        const FVector PannedFocus=CameraFocus;
        FirstPerson=false;FirstPersonBlend=0;EyeRotation=FRotator(0,Heading*45.f,0);
        const FRotator Facing=EyeRotation;
        HandleLiveKey(EKeys::F,true);
        Passed &= EyeRotation.Equals(Facing,.001); // catches the former first-entry corridor override
        FirstPersonBlend=1;FitCamera();
        Passed &= Camera->GetComponentLocation().Equals(Eye,.001)
            && FVector::DotProduct(Camera->GetForwardVector(),Facing.Vector())>.99999;
        FirstPersonBlend=.37f;FitCamera();
        const FVector Before=Camera->GetComponentLocation();const FQuat BeforeRotation=Camera->GetComponentQuat();
        Passed &= HandleLiveKey(Heading%2==0?EKeys::Escape:EKeys::F,Heading%2!=0) && !FirstPerson;
        FitCamera();
        Passed &= Camera->GetComponentLocation().Equals(Before,.001) && Camera->GetComponentQuat().Equals(BeforeRotation,.00001);
        FirstPersonBlend=0;FitCamera();
        Passed &= Camera->ProjectionMode==ECameraProjectionMode::Orthographic && CameraFocus.Equals(PannedFocus,.001) && !FollowHero && Camera->GetComponentRotation().Equals(Overhead,.001);
    }
    FirstPerson=SavedFirstPerson;FirstPersonBlend=SavedBlend;EyeRotation=SavedLook;OverviewOrbitOffset=SavedOrbit;WasOrbiting=false;
    ZoomFactor=SavedZoom;CameraFocus=SavedFocus;FollowHero=SavedFollow;ShowEntityGlyphs=Labels;FitCamera();
    Passed &= Session->Turn==Turn && Session->Sequence==Sequence;
    UE_LOG(LogTemp,Display,TEXT("PRESENTATION_CONTROLS_CHECK %s key=F7 return=Escape/Ctrl+F paths=%d headings=8 orbit=right_drag tilt_limits=20:85 roll=0 orbit_return=preserved interruption=continuous turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),
        Passed?TEXT("PASS"):TEXT("FAIL"),Paths,Turn,Session->Turn,Sequence,Session->Sequence);
    return Passed;
}

void ADungeonPrototype::CaptureFirstPersonTransition()
{
    const bool Verify=FParse::Param(FCommandLine::Get(),TEXT("VerifyPresentationControls"));
    AdjustZoom(Verify?12.f:6.f);
    if(Verify && !VerifyPresentationControls()) { FPlatformMisc::RequestExitWithStatus(false,1); return; }
    const float SavedZoom=ZoomFactor;
    const FVector SavedFocus=CameraFocus;
    const bool SavedFollow=FollowHero;
    const FRotator Facing=EyeRotation;
    const int32 SavedTurn=Session->Turn;
    const auto Capture=[](const TCHAR* Name)
    { FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("Screenshots")/Name,true,false); };
    const auto Enter=[this,SavedZoom,SavedFocus,SavedFollow,Facing,SavedTurn,Verify,Capture]()
    {
        HandleLiveKey(EKeys::F,true);
        if(Verify)
        {
            FTimerHandle Mid;GetWorldTimerManager().SetTimer(Mid,[Capture](){Capture(TEXT("Presentation-Camera-Mid.png"));},.4f,false);
        }
        FTimerHandle ReturnHandle;
        GetWorldTimerManager().SetTimer(ReturnHandle,[this,SavedZoom,SavedFocus,SavedFollow,Facing,SavedTurn,Verify,Capture]()
        {
            const bool Entered=FirstPerson && FirstPersonBlend==1.f && EyeRotation.Equals(Facing,.001)
                && FVector::DotProduct(Camera->GetForwardVector(),Facing.Vector())>.99999 && Session->Turn==SavedTurn;
            if(Verify) Capture(TEXT("Presentation-Camera-Eye.png"));
            // Keep the screenshot on the settled eye frame, then reverse the same path.
            FTimerHandle Leave;
            GetWorldTimerManager().SetTimer(Leave,[this,SavedZoom,SavedFocus,SavedFollow,SavedTurn,Entered,Verify,Capture]()
            {
                HandleLiveKey(EKeys::F,true);
                if(Verify)
                {
                    FTimerHandle Mid;GetWorldTimerManager().SetTimer(Mid,[Capture](){Capture(TEXT("Presentation-Camera-Out-Mid.png"));},.4f,false);
                }
                FTimerHandle CheckHandle;
                GetWorldTimerManager().SetTimer(CheckHandle,[this,SavedZoom,SavedFocus,SavedFollow,SavedTurn,Entered,Verify,Capture]()
                {
                    FirstPersonReturnChecked=Entered && !IsFirstPerson() && ZoomFactor==SavedZoom && CameraFocus.Equals(SavedFocus,1.f)
                        && FollowHero==SavedFollow && Camera->ProjectionMode==ECameraProjectionMode::Orthographic && Session->Turn==SavedTurn;
                    if(Verify) Capture(TEXT("Presentation-Camera-Returned.png"));
                    FTimerHandle Reenter;
                    GetWorldTimerManager().SetTimer(Reenter,[this]()
                    {
                        HandleLiveKey(EKeys::F,true);
                        FTimerHandle Final;GetWorldTimerManager().SetTimer(Final,this,&ADungeonPrototype::CaptureAndValidate,1.3f,false);
                    },.25f,false);
                },1.3f,false);
            },.25f,false);
        },1.3f,false);
    };
    if(Verify)
    {
        // Let texture streaming settle before the paired label screenshots.
        FTimerHandle Warmup;
        GetWorldTimerManager().SetTimer(Warmup,[this,Enter,Capture]()
        {
            ShowEntityGlyphs=true;Capture(TEXT("Presentation-Labels-On.png"));
            FTimerHandle Hide;
            GetWorldTimerManager().SetTimer(Hide,[this,Enter,Capture]()
            {
                HandleLiveKey(EKeys::F7,false);Capture(TEXT("Presentation-Labels-Off.png"));
                FTimerHandle Begin;GetWorldTimerManager().SetTimer(Begin,Enter,.3f,false);
            },.3f,false);
        },2.f,false);
    }
    else Enter();
}

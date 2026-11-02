#include "DungeonPrototype.h"
#include "Camera/CameraComponent.h"
#include "Camera/PlayerCameraManager.h"

bool ADungeonPrototype::PickTravelCell(FVector2D Screen,FIntPoint& Cell) const
{
    Cell=FIntPoint(-1,-1);
    if(!Session || IsFirstPerson() || !Session->IsCommand() || Session->Ended)return false;
    auto* PC=GetWorld()->GetFirstPlayerController();
    if(!PC)return false;
    int32 W=0,H=0;PC->GetViewportSize(W,H);
    const float S=FMath::Clamp(W/1600.f,.65f,1.5f);
    const float Footer=LiveFooterHeight>0?LiveFooterHeight:232*S;
    if(Screen.X<0 || Screen.X>=W || Screen.Y<84*S || Screen.Y>=H-Footer)return false;
    FVector Origin,Direction;
    if(!PC->DeprojectScreenPositionToWorld(Screen.X,Screen.Y,Origin,Direction) || Direction.Z>=-.001)return false;
    const double Distance=(8.-Origin.Z)/Direction.Z;
    if(Distance<0)return false;
    const FVector Floor=Origin+Direction*Distance;
    const FIntPoint Candidate(FMath::FloorToInt(Floor.X/CellSize+Columns*.5f),FMath::FloorToInt(Floor.Y/CellSize+Rows*.5f));
    if(!Session->CanTravelTo(Candidate))return false;
    Cell=Candidate;return true;
}

void ADungeonPrototype::TickMouseTravel()
{
    auto* PC=GetWorld()->GetFirstPlayerController();
    FVector2D Mouse;FIntPoint Target;
    const bool Eligible=PC && !IsFirstPerson() && Session && Session->IsCommand() && !Session->Ended
        && !PC->IsInputKeyDown(EKeys::RightMouseButton) && !PC->IsInputKeyDown(EKeys::MiddleMouseButton)
        && PC->GetMousePosition(Mouse.X,Mouse.Y);
    MouseTravelCell=FIntPoint(-1,-1);
    if(!Eligible){WasTravelHeld=false;return;}
    if(PickTravelCell(Mouse,Target))MouseTravelCell=Target;
    if(WasTravelHeld && FVector2D::DistSquared(Mouse,TravelPressMouse)>36.)TravelDragCancelled=true;
}

void ADungeonPrototype::HandleTravelMouseButton(bool Pressed)
{
    auto* PC=GetWorld()->GetFirstPlayerController();FVector2D Mouse;
    if(!PC || PC->IsInputKeyDown(EKeys::RightMouseButton) || PC->IsInputKeyDown(EKeys::MiddleMouseButton)
        || !PC->GetMousePosition(Mouse.X,Mouse.Y)) { WasTravelHeld=false;return; }
    UpdateTravelButton(Mouse,Pressed);
}

void ADungeonPrototype::UpdateTravelButton(FVector2D Mouse,bool Pressed)
{
    FIntPoint Target;
    const bool Valid=PickTravelCell(Mouse,Target);
    if(Pressed)
    {
        WasTravelHeld=Valid;PressedTravelCell=Target;TravelPressMouse=Mouse;TravelDragCancelled=false;
        return;
    }
    if(WasTravelHeld && Valid && !TravelDragCancelled && Target==PressedTravelCell
        && FVector2D::DistSquared(Mouse,TravelPressMouse)<=36.)
    {
        if(Session->TravelTo(Target))UE_LOG(LogTemp,Display,TEXT("NETHACK_MOUSE_TRAVEL target=%d,%d"),Target.X,Target.Y);
        MouseTravelCell=FIntPoint(-1,-1);
    }
    WasTravelHeld=false;
}

// Presentation-only checks: exercise screen picking at real camera rotations
// without issuing a move in this capture session. Native travel has its own
// isolated bridge tests, including path selection and save/resume compatibility.
void ADungeonPrototype::VerifyMouseTravel()
{
    auto* PC=GetWorld()->GetFirstPlayerController();
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    const float SavedZoom=ZoomFactor;
    const FVector SavedFocus=CameraFocus;
    const bool SavedFollow=FollowHero;
    const FRotator SavedOrbit=OverviewOrbitOffset;
    bool Passed=Session->MouseTravelSupported;int32 Picks=0;
    ZoomFactor=3;FollowHero=false;CameraFocus=CellPosition(Session->Hero.X,Session->Hero.Y);
    for(float Pitch:{-20.f,-58.f,-85.f})for(float Yaw:{-170.f,-75.f,35.f,130.f})
    {
        OverviewOrbitOffset=FRotator(Pitch+58,Yaw+75,0);FitCamera();
        // Refresh the player camera cache used by project/deproject.
        PC->PlayerCameraManager->UpdateCamera(0);
        FVector2D Screen;FIntPoint Picked;
        Passed &= PC->ProjectWorldLocationToScreen(CellPosition(Session->Hero.X,Session->Hero.Y,8),Screen)
            && PickTravelCell(Screen,Picked) && Picked==Session->Hero;
        ++Picks;
    }
    FVector2D HeroScreen;PC->ProjectWorldLocationToScreen(CellPosition(Session->Hero.X,Session->Hero.Y,8),HeroScreen);
    UpdateTravelButton(HeroScreen,true);
    Passed &= WasTravelHeld && Session->IsCommand();
    UpdateTravelButton(HeroScreen+FVector2D(10,0),false);
    Passed &= !WasTravelHeld && Session->IsCommand();
    UpdateTravelButton(HeroScreen,true);CancelCameraDrag();UpdateTravelButton(HeroScreen,false);
    Passed &= !WasTravelHeld && Session->IsCommand();
    FIntPoint Rejected;
    Passed &= !PickTravelCell(FVector2D(20,20),Rejected) && !Session->CanTravelTo(FIntPoint(-1,0))
        && !Session->CanTravelTo(FIntPoint(79,0));
    const bool Awaiting=Session->Awaiting;Session->Awaiting=false;
    Passed &= !PickTravelCell(FVector2D(800,450),Rejected);Session->Awaiting=Awaiting;
    FirstPerson=true;Passed &= !PickTravelCell(FVector2D(800,450),Rejected);FirstPerson=false;
    ZoomFactor=SavedZoom;CameraFocus=SavedFocus;FollowHero=SavedFollow;OverviewOrbitOffset=SavedOrbit;FitCamera();
    PC->PlayerCameraManager->UpdateCamera(0);
    Passed &= Session->Turn==Turn && Session->Sequence==Sequence;
    UE_LOG(LogTemp,Display,TEXT("MOUSE_TRAVEL_CHECK %s picks=%d hud_rejected=1 bounds_rejected=1 prompts_rejected=1 first_person_rejected=1 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),
        Passed?TEXT("PASS"):TEXT("FAIL"),Picks,Turn,Session->Turn,Sequence,Session->Sequence);
    if(!Passed)FPlatformMisc::RequestExitWithStatus(false,1);
}

#include "DungeonPrototype.h"

void ADungeonPrototype::ToggleLevelOverview()
{
    if(IsFirstPerson() || FurStudy)return;
    CancelCameraDrag();
    if(LevelOverviewActive)
    {
        LevelOverviewActive=false;ZoomFactor=LevelOverviewZoom;
        CameraFocus=LevelOverviewFocus;OverviewOrbitOffset=LevelOverviewOrbit;FollowHero=LevelOverviewFollow;
        if(Session && LevelOverviewLocation!=FIntPoint(Session->Dungeon,Session->Depth))FollowHero=true;
        FitCamera();
        UE_LOG(LogTemp,Display,TEXT("LEVEL_OVERVIEW RETURN zoom=%.3f follow=%d"),ZoomFactor,FollowHero);
    }
    else if(ZoomFactor>1.001f)
    {
        LevelOverviewZoom=ZoomFactor;LevelOverviewFocus=CameraFocus;
        LevelOverviewOrbit=OverviewOrbitOffset;LevelOverviewFollow=FollowHero;
        LevelOverviewLocation=Session?FIntPoint(Session->Dungeon,Session->Depth):FIntPoint(-1,-1);
        LevelOverviewActive=true;ZoomFactor=1;CameraFocus=FVector::ZeroVector;FollowHero=false;
        FitCamera();
        UE_LOG(LogTemp,Display,TEXT("LEVEL_OVERVIEW PEEK saved_zoom=%.3f"),LevelOverviewZoom);
    }
}

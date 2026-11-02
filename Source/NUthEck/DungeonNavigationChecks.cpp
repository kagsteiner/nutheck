#include "DungeonPrototype.h"
#include "Camera/CameraComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Misc/CommandLine.h"

void ADungeonPrototype::VerifyNavigation()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    const float SavedZoom=ZoomFactor;const FVector SavedFocus=CameraFocus;
    const bool SavedFollow=FollowHero,Style=SculptedCreatures;const FRotator SavedOrbit=OverviewOrbitOffset;
    bool Passed=true;int32 Views=0;
    const auto NativeCells=Session->Cells;
    for(float Zoom:{1.2f,3.f,8.f})for(bool Follow:{false,true})for(float Pitch:{-20.f,-58.f,-85.f})
    {
        LevelOverviewActive=false;ZoomFactor=Zoom;FollowHero=Follow;
        CameraFocus=CellPosition(Session->Hero.X,Session->Hero.Y)+FVector(120,-60,0);
        OverviewOrbitOffset=FRotator(Pitch+58,42,0);FitCamera();
        const FVector Focus=CameraFocus;const FQuat Rotation=Camera->GetComponentQuat();
        const float Width=Camera->OrthoWidth;
        Passed &= HandleLiveKey(EKeys::F6,false) && LevelOverviewActive && ZoomFactor==1 && CameraFocus.IsZero();
        OverviewOrbitOffset=FRotator(0,-130,0);FitCamera();
        Passed &= HandleLiveKey(EKeys::F6,false) && !LevelOverviewActive && ZoomFactor==Zoom
            && FollowHero==Follow && CameraFocus.Equals(Focus,.001) && Camera->GetComponentQuat().Equals(Rotation,.00001)
            && FMath::IsNearlyEqual(Camera->OrthoWidth,Width,.01f);
        ++Views;
    }
    HandleLiveKey(EKeys::F6,false);HandleLiveKey(EKeys::F5,false);
    Passed &= !LevelOverviewActive && ZoomFactor==1;
    HandleLiveKey(EKeys::F6,false);Passed &= !LevelOverviewActive && ZoomFactor==1;
    ZoomFactor=3;FitCamera();HandleLiveKey(EKeys::F6,false);HandleLiveKey(EKeys::F,true);
    Passed &= FirstPerson && !LevelOverviewActive && ZoomFactor==3;
    HandleLiveKey(EKeys::F,true);FirstPersonBlend=0;
    for(int32 StylePass=0;StylePass<2;++StylePass)
    {
        for(bool Visible:{false,true})for(bool Up:{false,true})
        {
            TArray<FName> Keys;const FString Suffix=Visible?TEXT(""):TEXT("Memory");
            for(const TCHAR* Key:{TEXT("StairUp"),TEXT("StairUpEdge"),TEXT("StairRim"),TEXT("StairVoid")})Keys.Add(FName(*(FString(Key)+Suffix)));
            for(int32 I=0;I<7;++I)Keys.Add(FName(*(FString::Printf(TEXT("StairDown%d"),I)+Suffix)));
            TMap<FName,int32> Before;for(const auto Key:Keys)Before.Add(Key,LiveBatches[Key]->GetInstanceCount());
            FNetHackCell Cell;Cell.Kind=TEXT("terrain");Cell.Visible=Visible;Cell.Terrain=Up?TEXT("up"):TEXT("down");
            AddStair(Cell,0,0);int32 Parts=0;float Highest=-1000,Lowest=1000;
            for(const auto Key:Keys)
            {
                auto* Batch=LiveBatches[Key].Get();Passed &= Batch->GetCollisionEnabled()==ECollisionEnabled::NoCollision;
                for(int32 I=Before[Key];I<Batch->GetInstanceCount();++I)
                {
                    FTransform T;Batch->GetInstanceTransform(I,T,true);++Parts;
                    const FBox Bounds=Batch->GetStaticMesh()->GetBoundingBox().TransformBy(T).ShiftBy(-CellPosition(0,0,0));
                    Passed &= Bounds.Min.X>=-50.01 && Bounds.Max.X<=50.01 && Bounds.Min.Y>=-50.01 && Bounds.Max.Y<=50.01;
                    Highest=FMath::Max(Highest,float(Bounds.Max.Z));Lowest=FMath::Min(Lowest,float(Bounds.Min.Z));
                }
            }
            Passed &= Parts==(Up?13:20) && (Up?Highest>100:Highest<20 && Lowest<0);
        }
        HandleLiveKey(EKeys::F9,false);
    }
    Passed &= Style==SculptedCreatures;
    RebuildLiveMap();
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewStairs")))
    {
        TArray<FIntPoint> Floors;
        for(int32 Y=1;Y<Rows-1;++Y)for(int32 X=1;X<Columns-1;++X)
        {
            const auto& C=Session->Cells[Y*Columns+X];
            if(C.Visible && C.Kind==TEXT("terrain") && C.Terrain==TEXT("floor"))Floors.Add(FIntPoint(X,Y));
        }
        const auto Score=[this](FIntPoint P)
        {
            int32 Walls=0;
            for(auto D:{FIntPoint(1,0),FIntPoint(-1,0),FIntPoint(0,1),FIntPoint(0,-1)})
                if(Session->Cells[(P.Y+D.Y)*Columns+P.X+D.X].Terrain==TEXT("wall"))++Walls;
            return Walls*100+(P-Session->Hero).SizeSquared();
        };
        Floors.Sort([&](auto A,auto B){return Score(A)<Score(B);});
        if(Floors.Num()>=2)
        {
            const FIntPoint A=Floors[0];FIntPoint B=Floors[1];
            for(const auto P:Floors)if((P-A).SizeSquared()>=4){B=P;break;}
            const int32 Before=LiveBatches[TEXT("Floor")]->GetInstanceCount();
            StairPreview.Add(A,TEXT("up"));StairPreview.Add(B,TEXT("down"));RebuildLiveMap();
            Passed &= LiveBatches[TEXT("Floor")]->GetInstanceCount()==Before-1;
            UE_LOG(LogTemp,Display,TEXT("STAIR_PREVIEW up=%d,%d down=%d,%d"),A.X,A.Y,B.X,B.Y);
        }
        else Passed=false;
    }
    for(int32 I=0;I<NativeCells.Num();++I)Passed &= NativeCells[I].Terrain==Session->Cells[I].Terrain && NativeCells[I].Kind==Session->Cells[I].Kind;
    ZoomFactor=SavedZoom;CameraFocus=SavedFocus;FollowHero=SavedFollow;OverviewOrbitOffset=SavedOrbit;LevelOverviewActive=false;FitCamera();
    if(FParse::Param(FCommandLine::Get(),TEXT("NavigationWide"))){ZoomFactor=6;FitCamera();HandleLiveKey(EKeys::F6,false);}
    Passed &= Session->Turn==Turn && Session->Sequence==Sequence;
    UE_LOG(LogTemp,Display,TEXT("NAVIGATION_CHECK %s key=F6 views=%d exact_restore=1 f5_cancels=1 first_person_restore=1 stair_types=2 memory=2 styles=2 native_cells_unchanged=1 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),
        Passed?TEXT("PASS"):TEXT("FAIL"),Views,Turn,Session->Turn,Sequence,Session->Sequence);
    if(!Passed)FPlatformMisc::RequestExitWithStatus(false,1);
}

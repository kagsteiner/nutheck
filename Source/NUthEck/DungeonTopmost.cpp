#include "DungeonTopmost.h"
#include "DungeonPrototype.h"
#include "OfficialTileAtlas.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Misc/CommandLine.h"

void ADungeonPrototype::VerifyTopmostPresentation()
{
    const auto NativeCells=Session->Cells;
    const auto NativeHero=Session->Hero;
    const bool NativeMines=Session->InMines,NativeTown=Session->MinesTown,Style=SculptedCreatures;
    const auto SavedPreview=StairPreview;StairPreview.Empty();
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    bool Passed=true;int32 Cases=0;
    Session->Cells.Init(FNetHackCell(),Rows*Columns);
    const FIntPoint At(2,2);const int32 Index=At.Y*Columns+At.X;
    Session->Hero=FIntPoint(5,5);
    const TArray<FString> Terrains={TEXT("altar_unaligned"),TEXT("altar_chaotic"),TEXT("altar_neutral"),TEXT("altar_lawful"),TEXT("altar_other"),TEXT("fountain"),TEXT("sink"),TEXT("up"),TEXT("down"),TEXT("trap"),TEXT("open"),TEXT("closed"),TEXT("water"),TEXT("lava"),TEXT("wall")};
    const auto Snapshot=[this]() {
        TMap<FName,int32> Counts;
        for(const auto& Entry:LiveBatches) if(Entry.Value->GetInstanceCount()>0)
            Counts.Add(Entry.Key,Entry.Value->GetInstanceCount());
        return Counts;
    };
    const auto Equal=[](const TMap<FName,int32>& A,const TMap<FName,int32>& B) {
        if(A.Num()!=B.Num())return false;
        for(const auto& Entry:A) {const auto* N=B.Find(Entry.Key);if(!N || *N!=Entry.Value)return false;}
        return true;
    };
    for(int32 Mode=0;Mode<2;++Mode) {
        Session->InMines=Mode==1;Session->MinesTown=false;
        for(int32 S=0;S<2;++S) {
            for(bool Visible:{false,true})for(const FString& Terrain:Terrains) {
                Session->Hero=FIntPoint(5,5);
                FNetHackCell Ground;Ground.Kind=TEXT("terrain");Ground.Terrain=Terrain;Ground.Visible=Visible;
                Session->Cells[Index]=Ground;RebuildLiveMap();const auto Empty=Snapshot();
                Session->Cells[Index].Terrain=TEXT("floor");RebuildLiveMap();
                Passed &= !Equal(Empty,Snapshot());
                for(int32 Foreground=0;Foreground<10;++Foreground) {
                    FNetHackCell Top=Ground;Top.Terrain=TEXT("floor");Top.TileIndex=OfficialTileDemoItem;
                    Top.Kind=Foreground<7?TEXT("item"):Foreground==7?TEXT("monster"):Foreground==8?TEXT("pet"):TEXT("effect");
                    if(Foreground==0)Top.DisplayObject=TEXT("dagger");
                    if(Foreground==1){Top.DisplayObject=TEXT("war hammer");Top.DisplayArtifact=TEXT("Mjollnir");}
                    if(Foreground==7)Top.DisplayMonster=TEXT("goblin");
                    if(Foreground==4)Top.DisplayObject=TEXT("pick-axe");
                    if(Foreground==5)Top.DisplayObject=TEXT("grappling hook");
                    if(Foreground==6)Top.DisplayObject=TEXT("stethoscope");
                    Session->Hero=Foreground==3?At:FIntPoint(5,5);
                    Session->Cells[Index]=Top;RebuildLiveMap();const auto Floor=Snapshot();
                    if(Foreground==0 || Foreground==1 || (Foreground>=4 && Foreground<=6)) {
                        const TArray<const TCHAR*> Keys={TEXT("dagger"),TEXT("mjollnir"),TEXT(""),TEXT(""),TEXT("pick_axe"),TEXT("grappling_hook"),TEXT("stethoscope")};
                        const FName Name(*(FString(TEXT("Object_"))+Keys[Foreground]+(Visible?TEXT(""):TEXT("_Memory"))));
                        const auto* Count=Floor.Find(Name);Passed &= Count && *Count==1;
                    }
                    Top.Terrain=Terrain;Session->Cells[Index]=Top;RebuildLiveMap();
                    const bool Good=Equal(Floor,Snapshot()) && Session->Cells[Index].Terrain==Terrain;
                    Passed &= Good;++Cases;
                    if(!Good)UE_LOG(LogTemp,Error,TEXT("TOPMOST_CASE_FAIL terrain=%s foreground=%d visible=%d mines=%d"),*Terrain,Foreground,Visible,Mode);
                }
                // Removing the foreground restores the exact native terrain presentation.
                Session->Hero=FIntPoint(5,5);Session->Cells[Index]=Ground;RebuildLiveMap();
                Passed &= Equal(Empty,Snapshot());
            }
            HandleLiveKey(EKeys::F9,false);
        }
    }
    Session->Cells=NativeCells;Session->Hero=NativeHero;Session->InMines=NativeMines;Session->MinesTown=NativeTown;
    StairPreview=SavedPreview;RebuildLiveMap();
    Passed &= Turn==Session->Turn && Sequence==Session->Sequence && Style==SculptedCreatures;
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewTopmost"))) {
        TArray<FIntPoint> Floors;
        for(int32 Y=0;Y<Rows;++Y)for(int32 X=0;X<Columns;++X) {
            const auto& C=Session->Cells[Y*Columns+X];
            if(C.Visible && C.Kind==TEXT("terrain") && C.Terrain==TEXT("floor") && FIntPoint(X,Y)!=Session->Hero)Floors.Add(FIntPoint(X,Y));
        }
        Floors.Sort([this](const FIntPoint& A,const FIntPoint& B){return (A-Session->Hero).SizeSquared()<(B-Session->Hero).SizeSquared();});
        Passed &= Floors.Num()>=3;
        if(Floors.Num()>=3)for(int32 I=0;I<3;++I) {
            auto& C=Session->Cells[Floors[I].Y*Columns+Floors[I].X];
            C.Terrain=TEXT("altar_lawful");C.Kind=I==0?TEXT("terrain"):TEXT("item");C.TileIndex=-1;
            C.DisplayObject=I==1?TEXT("dagger"):I==2?TEXT("war hammer"):TEXT("");C.DisplayArtifact=I==2?TEXT("Mjollnir"):TEXT("");
            UE_LOG(LogTemp,Display,TEXT("TOPMOST_SYNTHETIC_FIXTURE %d x=%d y=%d"),I,Floors[I].X,Floors[I].Y);
        }
        RebuildLiveMap();
    }
    UE_LOG(LogTemp,Display,TEXT("TOPMOST_PRESENTATION_CHECK %s cases=%d native_state_unchanged=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),Cases,Turn==Session->Turn && Sequence==Session->Sequence);
    if(!Passed)FPlatformMisc::RequestExitWithStatus(false,1);
}

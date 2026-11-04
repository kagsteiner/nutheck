#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"

void ADungeonPrototype::VerifyAppearanceBatch2()
{
    const bool Style=SculptedCreatures;const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    bool Good=true;int32 Cases=0,Native=0;
    const int32 Tiles[]={976,995,1213};
    const TCHAR* Keys[]={TEXT("sapphire_ring"),TEXT("triangular_amulet"),TEXT("silver_wand")};
    for(int32 N=0;N<3;++N) {
        bool Found=false;
        for(const auto& C:Session->Cells)if(C.Kind==TEXT("item") && C.TileIndex==Tiles[N])Found=true;
        Good &= Found;Native+=Found?1:0;
        for(bool Visible:{false,true})for(bool Mode:{false,true}) {
            SculptedCreatures=Mode;FNetHackCell C;C.Kind=TEXT("item");C.TileIndex=Tiles[N];C.Visible=Visible;
            auto* B=GetDisplayedObjectBatch(C);Good &= B && B->GetStaticMesh();
            if(B && B->GetStaticMesh()) {
                Good &= B->GetStaticMesh()->GetName()==FString(TEXT("SM_"))+Keys[N];
                const auto T=GetDisplayedObjectTransform(C,0,0,B->GetStaticMesh());
                const auto Bounds=B->GetStaticMesh()->GetBoundingBox().TransformBy(T);
                // FBX's handedness conversion maps Blender's -Y jewel face to UE +Y.
                if(Visible && !Mode)UE_LOG(LogTemp,Display,TEXT("APPEARANCE_POSE %s floor=%.3f face_z=%.3f mesh_y_min=%.3f mesh_y_max=%.3f"),Keys[N],Bounds.Min.Z,T.TransformVectorNoScale(N==0?FVector::UpVector:FVector(0,1,0)).Z,B->GetStaticMesh()->GetBoundingBox().Min.Y,B->GetStaticMesh()->GetBoundingBox().Max.Y);
                Good &= FMath::IsNearlyEqual(Bounds.Min.Z,12.f,.02f);
                Good &= T.TransformVectorNoScale(N==0?FVector::UpVector:FVector(0,1,0)).Z>.99f;

                for(int32 I=0;I<B->GetStaticMesh()->GetStaticMaterials().Num();++I)
                    Good &= B->GetMaterial(I) && (Visible || GetNameSafe(B->GetMaterial(I)).EndsWith(TEXT("Memory")));
                // Distinct underlying glyphs sharing this public appearance use one mesh.
                C.Glyph=123;Good &= GetDisplayedObjectBatch(C)==B;C.Glyph=987;Good &= GetDisplayedObjectBatch(C)==B;
            }
            C.Kind=TEXT("monster");Good &= GetDisplayedObjectBatch(C)==nullptr;
            C.Kind=TEXT("unknown");Good &= GetDisplayedObjectBatch(C)==nullptr;
            C.Kind=TEXT("item");C.TileIndex=-1;C.DisplayObject=Keys[N];Good &= GetDisplayedObjectBatch(C)==nullptr;
            ++Cases;
        }
    }
    FNetHackCell Unsupported;Unsupported.Kind=TEXT("item");Unsupported.TileIndex=978;Good &= GetDisplayedObjectBatch(Unsupported)==nullptr;
    const auto SavedCells=Session->Cells;const auto SavedHero=Session->Hero;
    const auto Snapshot=[this]() {
        TMap<FName,int32> Result;
        for(const auto& Pair:LiveBatches)if(Pair.Value->GetInstanceCount()>0)Result.Add(Pair.Key,Pair.Value->GetInstanceCount());
        return Result;
    };
    Session->Cells.Init(FNetHackCell(),Columns*Rows);Session->Hero=FIntPoint(8,8);
    int32 Covered=0;
    for(bool Mode:{false,true})for(bool Visible:{false,true})for(int32 Tile:Tiles) {
        SculptedCreatures=Mode;FNetHackCell C;C.Kind=TEXT("item");C.TileIndex=Tile;C.Visible=Visible;C.Terrain=TEXT("floor");
        Session->Cells[4*Columns+4]=C;RebuildLiveMap();const auto Floor=Snapshot();
        for(const FString Terrain:{TEXT("altar_lawful"),TEXT("fountain"),TEXT("sink"),TEXT("trap")}) {
            C.Terrain=Terrain;Session->Cells[4*Columns+4]=C;RebuildLiveMap();const auto CoveredMap=Snapshot();
            bool Same=Floor.Num()==CoveredMap.Num();
            for(const auto& Pair:Floor){const auto* Count=CoveredMap.Find(Pair.Key);Same &= Count && *Count==Pair.Value;}
            Good &= Same && Session->Cells[4*Columns+4].Terrain==Terrain;++Covered;
        }
    }
    Session->Cells=SavedCells;Session->Hero=SavedHero;
    SculptedCreatures=Style;RebuildLiveMap();HandleLiveKey(EKeys::F9,false);HandleLiveKey(EKeys::F9,false);
    Good &= Style==SculptedCreatures && Turn==Session->Turn && Sequence==Session->Sequence;
    UE_LOG(LogTemp,Display,TEXT("APPEARANCE_BATCH2_CHECK %s cases=%d covered_features=%d native_appearances=%d turn=%d sequence=%d"),Good?TEXT("PASS"):TEXT("FAIL"),Cases,Covered,Native,Turn,Sequence);
    if(!Good)FPlatformMisc::RequestExitWithStatus(false,1);
}

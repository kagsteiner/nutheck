#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"

void ADungeonPrototype::VerifyOracleCreature()
{
    const bool Style=SculptedCreatures;
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    bool Good=true;int32 Native=0;
    for(const auto& C:Session->Cells)if(C.Kind==TEXT("monster") && C.DisplayMonster==TEXT("Oracle")) {
        ++Native;Good &= C.Female;
    }
    Good &= Native==1;
    for(bool Female:{false,true}) {
        FNetHackCell C;C.Kind=TEXT("monster");C.DisplayMonster=TEXT("Oracle");C.Female=Female;C.TileIndex=Female?561:560;
        SculptedCreatures=true;
        auto* B=GetDefaultTileBatch(C,false);Good &= B && B->GetStaticMesh() && B->GetStaticMesh()->GetName()==TEXT("SM_oracle");
        if(B && B->GetStaticMesh()) {
            const auto* D=B->GetStaticMesh()->GetRenderData();
            Good &= D && D->LODResources.Num()>0 && D->LODResources[0].VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
        }
        SculptedCreatures=false;B=GetDefaultTileBatch(C,false);
        Good &= !B || !B->GetStaticMesh() || B->GetStaticMesh()->GetName()!=TEXT("SM_oracle");
        if(!B)for(bool Visible:{false,true}) {
            C.Visible=Visible;Good &= AddTileFallback(C,0,0);
            auto* Card=LiveBatches.Find(TEXT("TileFallback"));Good &= Card!=nullptr;
            if(Card) {
                const int32 I=(*Card)->GetInstanceCount()-1;
                Good &= I>=0 && (*Card)->NumCustomDataFloats==2;
                if(I>=0)Good &= (*Card)->PerInstanceSMCustomData[I*2]==C.TileIndex && FMath::IsNearlyEqual((*Card)->PerInstanceSMCustomData[I*2+1],Visible?1.f:.20f);
            }
        }
    }
    SculptedCreatures=true;
    FNetHackCell Unknown;Unknown.DisplayMonster=TEXT("unsupported oracle test");
    Good &= GetDefaultTileBatch(Unknown,false)==nullptr;
    Unknown.DisplayMonster.Empty();Good &= GetDefaultTileBatch(Unknown,false)==nullptr;
    SculptedCreatures=Style;RebuildLiveMap();
    HandleLiveKey(EKeys::F9,false);Good &= SculptedCreatures!=Style;
    HandleLiveKey(EKeys::F9,false);Good &= SculptedCreatures==Style;
    Good &= Turn==Session->Turn && Sequence==Session->Sequence;
    UE_LOG(LogTemp,Display,TEXT("ORACLE_CREATURE_CHECK %s native=%d aliases=2 fallback=2 turn=%d sequence=%d"),Good?TEXT("PASS"):TEXT("FAIL"),Native,Turn,Sequence);
    if(!Good)FPlatformMisc::RequestExitWithStatus(false,1);
}

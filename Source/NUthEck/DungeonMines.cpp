#include "DungeonPrototype.h"
#include "DungeonTopmost.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "MeshDescription.h"
#include "StaticMeshAttributes.h"
#include "Components/PointLightComponent.h"

namespace {
UStaticMesh* MineRock(UObject* Outer,int32 Mask)
{
    FMeshDescription D;FStaticMeshAttributes A(D);A.Register();
    auto Positions=A.GetVertexPositions();auto Normals=A.GetVertexInstanceNormals();
    auto Tangents=A.GetVertexInstanceTangents();auto Signs=A.GetVertexInstanceBinormalSigns();
    auto UV=A.GetVertexInstanceUVs();UV.SetNumChannels(1);
    const FPolygonGroupID Group=D.CreatePolygonGroup();
    A.GetPolygonGroupMaterialSlotNames()[Group]=TEXT("StairStone");
    const auto Triangle=[&](FVector3f P,FVector3f Q,FVector3f R)
    {
        const FVector3f N=FVector3f::CrossProduct(Q-P,R-P).GetSafeNormal();
        const FVector3f T=FMath::Abs(N.Z)>.9f?FVector3f(1,0,0):FVector3f::CrossProduct(FVector3f(0,0,1),N).GetSafeNormal();
        TArray<FVertexInstanceID> Instances;
        // Unreal's front faces use clockwise winding. Keep the outward normal
        // above, but reverse the vertex order so exterior faces survive culling.
        for(const auto V:{P,R,Q})
        {
            const auto ID=D.CreateVertex();Positions[ID]=V;
            const auto I=D.CreateVertexInstance(ID);Normals[I]=N;Tangents[I]=T;Signs[I]=1;
            UV.Set(I,0,FVector2f(V.X/100.f,V.Y/100.f));Instances.Add(I);
        }
        D.CreatePolygon(Group,Instances);
    };

    for(int32 Face=0;Face<6;++Face)for(int32 U=0;U<4;++U)for(int32 V=0;V<4;++V)
    {
        if(Face>=2 && (Mask & (1<<(Face-2))))continue;
        const auto Point=[&](int32 I,int32 J)
        {
            const float A=-50+I*25.f,B=-50+J*25.f;
            const float Heights[]={-60,-52,-20,20,60};const float Z=Heights[J];
            switch(Face)
            {
                case 0:return FVector3f(A,B,60);
                case 1:return FVector3f(A,-B,-60);
                case 2:return FVector3f(50,A,Z);
                case 3:return FVector3f(-50,-A,Z);
                case 4:return FVector3f(-A,50,Z);
                default:return FVector3f(A,-50,Z);
            }
        };
        const auto P0=Point(U,V),P1=Point(U+1,V),P2=Point(U+1,V+1),P3=Point(U,V+1);
        Triangle(P0,P1,P2);Triangle(P0,P2,P3);
    }
    auto* Mesh=NewObject<UStaticMesh>(Outer,*FString::Printf(TEXT("MineRock%d"),Mask));
    Mesh->GetStaticMaterials().Add(FStaticMaterial());
    UStaticMesh::FBuildMeshDescriptionsParams P;P.bFastBuild=true;P.bMarkPackageDirty=false;
    check(Mesh->BuildFromMeshDescriptions({&D},P));return Mesh;
}
}

void ADungeonPrototype::CreateMinesBatches()
{
    UStaticMesh* Rocks[16];for(int32 I=0;I<16;++I)Rocks[I]=MineRock(this,I);
    for(const FString Suffix:{FString(),FString(TEXT("Lit")),FString(TEXT("Memory"))})
    {
        const bool Memory=Suffix==TEXT("Memory");
        const auto Add=[&](const FString& Name,const TCHAR* Material,UStaticMesh* Mesh=nullptr)
        {
            auto* B=MakeBatch(*(Name+Suffix),TEXT("/Engine/BasicShapes/Cube.Cube"),FLinearColor::White);
            if(Mesh)B->SetStaticMesh(Mesh);
            auto* Base=LoadObject<UMaterialInterface>(nullptr,Material);check(Base);
            auto* M=UMaterialInstanceDynamic::Create(Base,this);
            M->SetVectorParameterValue(TEXT("Tint"),Memory?FLinearColor(.4f,.4f,.4f):FLinearColor::White);
            B->SetBoundsScale(1.15f);B->SetMaterial(0,M);B->SetLightingChannels(!Memory,Memory,Suffix==TEXT("Lit"));
            LiveBatches.Add(FName(*(Name+Suffix)),B);
        };
        const TCHAR* Rock=TEXT("/Game/Mines/M_MinesRock.M_MinesRock");
        Add(TEXT("MinesFloor"),TEXT("/Game/Mines/M_MinesFloor.M_MinesFloor"));
        for(int32 I=0;I<16;++I)Add(FString::Printf(TEXT("MinesRock%d"),I),Rock,Rocks[I]);
    }
}

void ADungeonPrototype::AddMinesSurface(const FNetHackCell& C,int32 X,int32 Y)
{
    bool Lit=C.PermanentLight || C.TemporaryLight;
    if(C.Visible && C.Terrain==TEXT("wall"))
        for(const FIntPoint D:{FIntPoint(1,0),FIntPoint(-1,0),FIntPoint(0,1),FIntPoint(0,-1)})
        {
            const auto P=FIntPoint(X,Y)+D;if(P.X<0 || P.X>=Columns || P.Y<0 || P.Y>=Rows)continue;
            const auto& N=Session->Cells[P.Y*Columns+P.X];
            Lit |= N.Visible && N.Kind!=TEXT("unknown") && (N.PermanentLight || N.TemporaryLight);
        }
    const FString Suffix=!C.Visible?TEXT("Memory"):Lit?TEXT("Lit"):TEXT("");
    const auto Part=[&](const FString& Name,FVector Pos,FVector Scale)
    {LiveBatches[FName(*(Name+Suffix))]->AddInstance(FTransform(FQuat::Identity,Pos,Scale));};
    if(C.Terrain==TEXT("wall"))
    {
        int32 Mask=0,Bit=1;
        for(const FIntPoint D:{FIntPoint(1,0),FIntPoint(-1,0),FIntPoint(0,1),FIntPoint(0,-1)})
        {
            const auto P=FIntPoint(X,Y)+D;
            if(P.X>=0 && P.X<Columns && P.Y>=0 && P.Y<Rows)
            {const auto N=TopmostRenderCell(Session->Cells[P.Y*Columns+P.X],Session->Hero==P);if(N.Kind!=TEXT("unknown") && N.Terrain==TEXT("wall"))Mask|=Bit;}
            Bit<<=1;
        }
        Part(FString::Printf(TEXT("MinesRock%d"),Mask),CellPosition(X,Y,60),FVector(1));

    }
    else if(C.Terrain!=TEXT("down"))Part(TEXT("MinesFloor"),CellPosition(X,Y,0),FVector(1,1,.16f));
}

void ADungeonPrototype::VerifyMines()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    const bool Style=SculptedCreatures;bool Passed=Session->InMines;
    const auto Count=[this](const FString& Prefix)
    {
        int32 N=0;for(const auto& B:LiveBatches)if(B.Key.ToString().StartsWith(Prefix))N+=B.Value->GetInstanceCount();return N;
    };
    int32 Floors=0,Walls=0;
    for(int32 I=0;I<Session->Cells.Num();++I)
    {
        const auto C=TopmostRenderCell(Session->Cells[I],Session->Hero==FIntPoint(I%Columns,I/Columns));
        if(C.Kind==TEXT("unknown") || C.Terrain==TEXT("none") || C.Terrain==TEXT("stone"))continue;
        if(C.Terrain==TEXT("wall"))++Walls;else if(C.Terrain!=TEXT("down"))++Floors;
    }
    for(int32 I=0;I<2;++I)
    {
        if(IsMinesCavern())
        {
            Passed &= Count(TEXT("MinesFloor"))==Floors && Count(TEXT("MinesRock"))==Walls;
            Passed &= Count(TEXT("Floor"))==0 && Count(TEXT("Wall"))==0 && Count(TEXT("CandleFlame"))==0;
            Passed &= !LiveBatches[TEXT("MinesFloor")]->LightingChannels.bChannel2
                && LiveBatches[TEXT("MinesFloorLit")]->LightingChannels.bChannel2
                && !LiveBatches[TEXT("MinesFloorMemory")]->LightingChannels.bChannel2;
            for(const auto& L:AtmosphereLights)if(L->IsVisible())Passed &= L->LightingChannels.bChannel2 && !L->LightingChannels.bChannel0;
            if(auto* Found=LiveBatches.Find(TEXT("TorchFlame")))
                for(int32 J=0;J<(*Found)->GetInstanceCount();++J)
                {
                    FTransform T;(*Found)->GetInstanceTransform(J,T,true);
                    const int32 X=FMath::RoundToInt(T.GetLocation().X/100+39),Y=FMath::RoundToInt(T.GetLocation().Y/100+10);
                    if(X<0 || X>=Columns || Y<0 || Y>=Rows){Passed=false;continue;}
                    const auto& C=Session->Cells[Y*Columns+X];
                    Passed &= C.Visible && C.PermanentLight && C.Terrain==TEXT("floor");
                }
        }
        else Passed &= Session->MinesTown && Count(TEXT("MinesRock"))==0 && Count(TEXT("TorchFlame"))==0;
        HandleLiveKey(EKeys::F9,false);
    }
    Passed &= Style==SculptedCreatures && Session->Turn==Turn && Session->Sequence==Sequence;
    UE_LOG(LogTemp,Display,TEXT("MINES_CHECK %s cavern=%d town=%d floors=%d walls=%d torches=%d native_unlit_receives_torch=0 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),
        Passed?TEXT("PASS"):TEXT("FAIL"),IsMinesCavern(),Session->MinesTown,Floors,Walls,Count(TEXT("TorchFlame")),Turn,Session->Turn,Sequence,Session->Sequence);
    if(!Passed)FPlatformMisc::RequestExitWithStatus(false,1);
}

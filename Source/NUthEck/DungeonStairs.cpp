#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "MeshDescription.h"
#include "StaticMeshAttributes.h"
#include "Misc/CommandLine.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Camera/CameraComponent.h"

namespace
{
UStaticMesh* MakeStairWedge(UObject* Outer)
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
        for(const auto V:{P,Q,R})
        {
            const auto ID=D.CreateVertex();Positions[ID]=V;
            const auto I=D.CreateVertexInstance(ID);Normals[I]=N;Tangents[I]=T;Signs[I]=1;
            UV.Set(I,0,FVector2f(V.X/100.f,V.Y/100.f));Instances.Add(I);
        }
        D.CreatePolygon(Group,Instances);
    };
    FVector3f V[8];
    for(int32 Z=0;Z<2;++Z)for(int32 I=0;I<4;++I)
    {
        const float Angle=FMath::DegreesToRadians((I==0 || I==1)?-23.f:23.f);
        const float Radius=(I==1 || I==2)?50.f:10.f;
        V[Z*4+I]=FVector3f(FMath::Cos(Angle)*Radius,FMath::Sin(Angle)*Radius,Z?50.f:-50.f);
    }
    Triangle(V[4],V[5],V[6]);Triangle(V[4],V[6],V[7]);
    Triangle(V[0],V[2],V[1]);Triangle(V[0],V[3],V[2]);
    for(int32 I=0;I<4;++I){const int32 J=(I+1)%4;Triangle(V[I],V[J],V[J+4]);Triangle(V[I],V[J+4],V[I+4]);}
    auto* Mesh=NewObject<UStaticMesh>(Outer,TEXT("SpiralStairWedge"));
    Mesh->GetStaticMaterials().Add(FStaticMaterial());
    UStaticMesh::FBuildMeshDescriptionsParams Params;Params.bFastBuild=true;Params.bMarkPackageDirty=false;
    Params.bBuildSimpleCollision=false;Params.bAllowCpuAccess=true;
    check(Mesh->BuildFromMeshDescriptions({&D},Params));
    return Mesh;
}
}

void ADungeonPrototype::CreateStairBatches()
{
    auto* Wedge=MakeStairWedge(this);
    for(bool Memory:{false,true})
    {
        const FString Suffix=Memory?TEXT("Memory"):TEXT("");const float Dim=Memory?.30f:1.f;
        const auto Add=[&](const FString& Name,const TCHAR* Mesh,FLinearColor Color,bool UseWedge=false)
        {
            auto* Batch=MakeBatch(*(Name+Suffix),Mesh,Color*Dim);
            if(UseWedge)Batch->SetStaticMesh(Wedge);
            LiveBatches.Add(FName(*(Name+Suffix)),Batch);
        };
        const TCHAR* Cube=TEXT("/Engine/BasicShapes/Cube.Cube");
        Add(TEXT("StairUp"),Cube,FLinearColor(.64f,.65f,.61f));
        Add(TEXT("StairUpEdge"),Cube,FLinearColor(.12f,.14f,.15f));
        Add(TEXT("StairRim"),Cube,FLinearColor(.34f,.36f,.37f));
        Add(TEXT("StairVoid"),TEXT("/Engine/BasicShapes/Cylinder.Cylinder"),FLinearColor(.003f,.004f,.006f));
        for(int32 I=0;I<7;++I)
        {
            const float Shade=FMath::Lerp(.48f,.018f,I/6.f);
            Add(FString::Printf(TEXT("StairDown%d"),I),Cube,FLinearColor(Shade,Shade*1.03f,Shade*1.07f),true);
        }
    }
}

void ADungeonPrototype::AddStair(const FNetHackCell& Cell,int32 X,int32 Y)
{
    if(Cell.Kind==TEXT("unknown") || (Cell.Terrain!=TEXT("up") && Cell.Terrain!=TEXT("down")))return;
    const FString Suffix=Cell.Visible?TEXT(""):TEXT("Memory");
    const FVector Origin=CellPosition(X,Y,0);
    const auto Part=[&](const FString& Name,FVector Position,FVector Size,float Yaw=0.f)
    {
        if(auto* Batch=LiveBatches.Find(FName(*(Name+Suffix))))
            (*Batch)->AddInstance(FTransform(FRotator(0,Yaw,0),Origin+Position,Size/100.f));
    };
    if(Cell.Terrain==TEXT("up"))
    {
        // Solid raised flight, culminating in a pale stone portal near wall top.
        for(int32 I=0;I<5;++I)
        {
            const float Height=(I+1)*20.f;
            Part(TEXT("StairUp"),FVector(0,36-I*18,8+Height*.5f),FVector(80,17,Height));
            Part(TEXT("StairUpEdge"),FVector(0,43.5f-I*18,9+Height),FVector(80,2.5f,2));
        }
        for(float Side:{-1.f,1.f})Part(TEXT("StairUp"),FVector(Side*44,-37,60),FVector(8,14,104));
        Part(TEXT("StairUp"),FVector(0,-37,112),FVector(96,14,8));
    }
    else
    {
        // Floor is absent over this tile. Descending wedge treads shrink and
        // darken into the well, finishing against the dark base above foundation.
        Part(TEXT("StairVoid"),FVector(0,0,-12),FVector(86,86,2));
        for(int32 I=0;I<12;++I)
        {
            const float Angle=I*30.f,R=FMath::DegreesToRadians(Angle);
            Part(TEXT("StairRim"),FVector(FMath::Cos(R)*43,FMath::Sin(R)*43,10),FVector(6,23,8),Angle);
        }
        for(int32 I=0;I<7;++I)
        {
            const float Diameter=90-I*7.f,Top=10-I*4.f;
            Part(FString::Printf(TEXT("StairDown%d"),I),FVector(0,0,Top-2),FVector(Diameter,Diameter,4),-80-I*38.f);
        }
    }
}

TMap<FIntPoint,FString> ADungeonPrototype::KnownStairs() const
{
    TMap<FIntPoint,FString> Result;
    if(!Session)return Result;
    for(int32 Y=0;Y<Rows;++Y)for(int32 X=0;X<Columns;++X)
    {
        const auto& C=Session->Cells[Y*Columns+X];
        if(C.Kind!=TEXT("unknown") && (C.Terrain==TEXT("up") || C.Terrain==TEXT("down")))Result.Add(FIntPoint(X,Y),C.Terrain);
    }
    for(const auto& P:StairPreview)Result.Add(P.Key,P.Value);
    return Result;
}

void ADungeonPrototypeHUD::DrawStairMarkers(ADungeonPrototype& Dungeon)
{
    if(Dungeon.IsFirstPerson() || Dungeon.GetZoomFactor()>2.f)return;
    auto* Live=Dungeon.GetSession();if(!Live)return;
    const float S=FMath::Clamp(Canvas->SizeX/1600.f,.65f,1.5f);
    const auto Stairs=Dungeon.KnownStairs();TArray<FIntPoint> Locations;Stairs.GetKeys(Locations);
    Locations.Sort([](auto A,auto B){return A.Y==B.Y?A.X<B.X:A.Y<B.Y;});
    TArray<FBox2D> Occupied;
    for(const auto Location:Locations)
    {
        FVector2D Screen;
        if(!GetOwningPlayerController()->ProjectWorldLocationToScreen(FVector((Location.X-39)*100.f,(Location.Y-10)*100.f,138),Screen))continue;
        const FString Label=Stairs[Location]==TEXT("up")?TEXT("< UP"):TEXT("> DOWN");
        const bool Visible=Live->Cells[Location.Y*79+Location.X].Visible;
        const FLinearColor Ink=Visible?FLinearColor(.90f,.92f,.84f):FLinearColor(.60f,.64f,.65f);
        float W=0,H=0;Canvas->StrLen(GEngine->GetSmallFont(),Label,W,H);W*=S;H*=S;
        const FVector2D Anchor=Screen;
        const auto& Cell=Live->Cells[Location.Y*79+Location.X];
        if(Dungeon.ShouldShowEntityGlyphs() && (Location==Live->Hero || Cell.Kind==TEXT("monster") || Cell.Kind==TEXT("pet")))
            Screen.Y-=(18+12*Dungeon.GetZoomFactor())*S;
        FBox2D Bounds;
        for(int32 Attempt=0;Attempt<16;++Attempt)
        {
            Bounds=FBox2D(FVector2D(Screen.X-W*.5f-3*S,Screen.Y-H-2*S),FVector2D(Screen.X+W*.5f+3*S,Screen.Y+2*S));
            bool Collision=false;for(const auto& Other:Occupied)Collision |= Bounds.Intersect(Other);
            if(!Collision)break;
            Screen.Y-=H+8*S;
        }
        const float Bottom=Canvas->SizeY-Dungeon.GetLiveFooterHeight();
        if(Anchor.X<0 || Anchor.X>Canvas->SizeX || Anchor.Y<84*S || Anchor.Y>Bottom)continue;
        if(Bounds.Min.X<0 || Bounds.Max.X>Canvas->SizeX || Bounds.Min.Y<84*S || Bounds.Max.Y>Bottom)continue;
        Occupied.Add(Bounds);
        if(!Screen.Equals(Anchor,.1))DrawLine(Anchor.X,Anchor.Y,Screen.X,Screen.Y+2*S,Ink*.5f,1);
        DrawRect(FLinearColor(.015f,.022f,.027f,.95f),Bounds.Min.X,Bounds.Min.Y,Bounds.GetSize().X,Bounds.GetSize().Y);
        DrawText(Label,Ink,Screen.X-W*.5f,Screen.Y-H,GEngine->GetSmallFont(),S);
    }
}

#include "DungeonPrototype.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Misc/CommandLine.h"

void ADungeonPrototype::AddFramedDoor(const FNetHackCell& Cell,int32 X,int32 Y)
{
    if(Cell.Kind==TEXT("unknown") || (Cell.Terrain!=TEXT("closed") && Cell.Terrain!=TEXT("open")))return;
    const FString Suffix=Cell.Visible?TEXT(""):TEXT("Memory");
    const FVector Origin=CellPosition(X,Y,0);
    const FQuat Frame=FRotator(0,Cell.Horizontal?0:90,0).Quaternion();
    const auto Part=[this,&Suffix,&Origin,&Frame](const TCHAR* Kind,FVector Position,FVector Size,FQuat Rotation=FQuat::Identity)
    {
        if(auto* Batch=LiveBatches.Find(FName(*(FString(Kind)+Suffix))))
            (*Batch)->AddInstance(FTransform(Frame*Rotation,Origin+Frame.RotateVector(Position),Size/100.f));
    };
    // Fixed timber jambs/lintel reach the existing 120cm wall top. Their inner
    // faces leave a 74cm opening; floor top is 8cm. No lowered/cutaway walls.
    for(float Side:{-1.f,1.f})Part(TEXT("DoorFrame"),FVector(Side*43,0,64),FVector(12,22,112));
    Part(TEXT("DoorFrame"),FVector(0,0,114),FVector(98,22,12));

    const FQuat Swing=FRotator(0,Cell.Terrain==TEXT("open")?90:0,0).Quaternion();
    const FVector Hinge(-36,0,58);
    const auto Leaf=[&Part,&Swing,&Hinge](const TCHAR* Kind,FVector Offset,FVector Size)
    {
        Part(Kind,Hinge+Swing.RotateVector(FVector(36,0,0)+Offset),Size,Swing);
    };
    // The panel rotates about its left edge, not its centre. When open it lies
    // along the side of the passage, with the frame and centre clearly empty.
    Leaf(TEXT("Door"),FVector(0,0,0),FVector(72,4.5,96));
    for(int32 I=0;I<5;++I)
        Leaf(TEXT("Door"),FVector(-36+(I+.5f)*14.4f,-.8f,0),FVector(14.1f,6,96));
    for(float Z:{-31.f,31.f})Leaf(TEXT("DoorBrace"),FVector(0,-4, Z),FVector(66,3,7));
    Leaf(TEXT("DoorHardware"),FVector(29,-7,0),FVector(5,5,5));
    for(float Z:{27.f,89.f})Part(TEXT("DoorHardware"),FVector(-36,0,Z),FVector(4,9,12));
}

void ADungeonPrototype::VerifyDoorFrames()
{
    const int32 Turn=Session->Turn,Sequence=Session->Sequence;
    const bool Style=SculptedCreatures;bool Passed=true;
    const FVector Origin=CellPosition(0,0,0);
    const TCHAR* Kinds[]={TEXT("DoorFrame"),TEXT("Door"),TEXT("DoorBrace"),TEXT("DoorHardware")};
    for(int32 Pass=0;Pass<2;++Pass)
    {
        for(bool Horizontal:{false,true})for(bool Open:{false,true})for(bool Visible:{false,true})
        {
            const FString Suffix=Visible?TEXT(""):TEXT("Memory");
            TMap<FName,int32> Before;
            for(const TCHAR* Kind:Kinds)
            {const FName Key(*(FString(Kind)+Suffix));Before.Add(Key,LiveBatches[Key]->GetInstanceCount());}
            FNetHackCell Probe;Probe.Kind=TEXT("terrain");Probe.Terrain=Open?TEXT("open"):TEXT("closed");Probe.Horizontal=Horizontal;Probe.Visible=Visible;
            AddFramedDoor(Probe,0,0);
            const FQuat Frame=FRotator(0,Horizontal?0:90,0).Quaternion();
            // Geometric traversal invariant: an open assembly leaves a 40cm
            // central corridor below head height clear; a closed leaf blocks it.
            const FBox Passage(FVector(-20,-45,8),FVector(20,45,100));
            bool Blocked=false;int32 Parts=0;
            for(const TCHAR* Kind:Kinds)
            {
                const FName Key(*(FString(Kind)+Suffix));auto* Batch=LiveBatches[Key].Get();
                for(int32 I=Before[Key];I<Batch->GetInstanceCount();++I)
                {
                    FTransform T;Passed &= Batch->GetInstanceTransform(I,T,true);++Parts;
                    FBox Local(ForceInit);
                    for(int32 Corner=0;Corner<8;++Corner)
                    {
                        const FVector P((Corner&1)?50:-50,(Corner&2)?50:-50,(Corner&4)?50:-50);
                        Local+=Frame.UnrotateVector(T.TransformPosition(P)-Origin);
                    }
                    Blocked |= Local.Intersect(Passage);
                    Passed &= Local.Max.Z<=120.01 && Local.Min.Z>=7.99;
                }
            }
            Passed &= Parts==14 && Blocked==!Open;
            const FName LeafKey(*(TEXT("Door")+Suffix));FTransform Core;
            Passed &= LiveBatches[LeafKey]->GetInstanceTransform(Before[LeafKey],Core,true);
            const FVector Pivot=Core.TransformPosition(FVector(-50,0,0));
            Passed &= Pivot.Equals(Origin+Frame.RotateVector(FVector(-36,0,58)),.01);
        }
        HandleLiveKey(EKeys::F9,false);
    }
    Passed &= Session->Turn==Turn && Session->Sequence==Sequence && Style==SculptedCreatures;
    RebuildLiveMap();
    if(FParse::Param(FCommandLine::Get(),TEXT("PreviewDoorFrames")))
    {
        TArray<FIntPoint> Floors;
        for(int32 Y=0;Y<Rows;++Y)for(int32 X=0;X<Columns;++X)
        {const auto& C=Session->Cells[Y*Columns+X];if(C.Visible && C.Terrain==TEXT("floor") && C.Kind==TEXT("terrain") && FIntPoint(X,Y)!=Session->Hero)Floors.Add(FIntPoint(X,Y));}
        Floors.Sort([this](const FIntPoint& A,const FIntPoint& B){return (A-Session->Hero).SizeSquared()<(B-Session->Hero).SizeSquared();});
        if(Floors.Num()>=2)for(int32 I=0;I<2;++I)
        {
            FNetHackCell Door;Door.Kind=TEXT("terrain");Door.Terrain=I?TEXT("closed"):TEXT("open");Door.Visible=true;Door.Horizontal=true;
            AddFramedDoor(Door,Floors[I].X,Floors[I].Y);
        }
        else Passed=false;
    }
    UE_LOG(LogTemp,Display,TEXT("DOOR_FRAMES_CHECK %s states=2 orientations=2 memory=2 styles=2 clear_centre=1 hinge_fixed=1 turn_before=%d turn_after=%d sequence_before=%d sequence_after=%d"),Passed?TEXT("PASS"):TEXT("FAIL"),Turn,Session->Turn,Sequence,Session->Sequence);
    if(!Passed)FPlatformMisc::RequestExitWithStatus(false,1);
}

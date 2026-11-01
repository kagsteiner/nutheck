#include "DungeonPrototype.h"
#include "Camera/CameraComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Engine/Engine.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "TimerManager.h"
#include "UnrealClient.h"

// Optional staged comparison. It never changes the live creature selection.
void ADungeonPrototype::GenerateFurStudy()
{
    BoardMin=FVector(-400,-300,-10);BoardMax=FVector(400,300,100);
    auto* Floor=MakeBatch(TEXT("FurFloor"),TEXT("/Engine/BasicShapes/Cube.Cube"),FLinearColor(.16f,.18f,.19f));
    Floor->AddInstance(FTransform(FQuat::Identity,FVector(0,0,-5),FVector(8,6,.1f)));
    const FRotator Rotation(-38,-75,0);
    const FVector Right=FRotationMatrix(Rotation).GetUnitAxis(EAxis::Y);
    const FVector Row=FRotationMatrix(Rotation).GetUnitAxis(EAxis::Z).GetSafeNormal2D();
    const TArray<FString> Species={TEXT("little_dog"),TEXT("housecat")};
    const TArray<FString> Variants={TEXT("smooth"),TEXT("painted"),TEXT("tufted")};
    for(int32 Y=0;Y<Species.Num();++Y) for(int32 X=0;X<Variants.Num();++X)
    {
        const FString Key=Species[Y]+TEXT("_")+Variants[X];
        const FString Path=TEXT("/Game/FurStudy/Meshes/SM_")+Key+TEXT(".SM_")+Key;
        auto* Mesh=LoadObject<UStaticMesh>(nullptr,*Path);
        checkf(Mesh,TEXT("Missing fur study mesh: %s"),*Path);
        auto* Batch=NewObject<UInstancedStaticMeshComponent>(this,FName(*Key));
        Batch->SetupAttachment(RootComponent);Batch->SetStaticMesh(Mesh);
        Batch->SetCollisionEnabled(ECollisionEnabled::NoCollision);Batch->SetCastShadow(true);
        AddInstanceComponent(Batch);Batch->RegisterComponent();
        const FVector At=Right*((X-1)*165.f)+Row*(Y==0?95.f:-95.f);
        Batch->AddInstance(FTransform(FRotator(0,-20,0),At,FVector(1)));
        LiveBatches.Add(FName(*Key),Batch);
    }
    CameraFocus=FVector(0,0,27);
}

void ADungeonPrototype::FitFurCamera()
{
    auto* PC=GetWorld()->GetFirstPlayerController();int32 W=0,H=0;
    if(PC) PC->GetViewportSize(W,H);if(W<=0 || H<=0)return;
    LastViewport=FIntPoint(W,H);Camera->SetAspectRatio(float(W)/H);
    FString View=TEXT("close");FParse::Value(FCommandLine::Get(),TEXT("FurView="),View);
    const float Width=View==TEXT("level")?9700.f:View==TEXT("gameplay")?1211.3f:680.f;
    const FRotator Rotation(View==TEXT("close")?-38.f:-58.f,-75,0);
    Camera->ProjectionMode=ECameraProjectionMode::Orthographic;
    Camera->SetOrthoWidth(Width);Camera->SetWorldRotation(Rotation);
    Camera->SetWorldLocation(CameraFocus-Rotation.Vector()*15000.f);
}

void ADungeonPrototype::CaptureFurStudy()
{
    bool Passed=FurStudy && !Session && LiveBatches.Num()==6 && LastViewport.X>0;
    TMap<FString,uint32> Triangles;
    auto* PC=GetWorld()->GetFirstPlayerController();
    for(const auto& Entry:LiveBatches)
    {
        UStaticMesh* Mesh=Entry.Value->GetStaticMesh();Passed &= Mesh && Entry.Value->GetInstanceCount()==1;
        if(!Mesh || !Mesh->GetRenderData() || Mesh->GetRenderData()->LODResources.Num()==0){Passed=false;continue;}
        const auto& LOD=Mesh->GetRenderData()->LODResources[0];
        Passed &= LOD.VertexBuffers.ColorVertexBuffer.GetNumVertices()>0;
        const FString Key=Entry.Key.ToString();Triangles.Add(Key,LOD.GetNumTriangles());
        FTransform At;Entry.Value->GetInstanceTransform(0,At,true);
        FVector2D Screen;
        Passed &= PC && PC->ProjectWorldLocationToScreen(At.GetLocation()+FVector(0,0,35),Screen);
        UE_LOG(LogTemp,Display,TEXT("FUR_STUDY_MESH %s triangles=%u vertices=%u uv_channels=%u anchor_x=%.1f anchor_y=%.1f"),
            *Key,LOD.GetNumTriangles(),LOD.VertexBuffers.PositionVertexBuffer.GetNumVertices(),LOD.VertexBuffers.StaticMeshVertexBuffer.GetNumTexCoords(),Screen.X,Screen.Y);
    }
    for(const FString Species:{FString(TEXT("little_dog")),FString(TEXT("housecat"))})
    {
        const uint32* Smooth=Triangles.Find(Species+TEXT("_smooth"));
        const uint32* Paint=Triangles.Find(Species+TEXT("_painted"));
        const uint32* Tuft=Triangles.Find(Species+TEXT("_tufted"));
        Passed &= Smooth && Paint && Tuft && *Smooth==*Paint && *Tuft>=*Smooth && *Tuft-*Smooth<=160;
    }
    FString View=TEXT("close");FParse::Value(FCommandLine::Get(),TEXT("FurView="),View);
    UE_LOG(LogTemp,Display,TEXT("FUR_STUDY_CHECK %s view=%s variants=%d width=%.1f"),Passed?TEXT("PASS"):TEXT("FAIL"),*View,LiveBatches.Num(),Camera->OrthoWidth);
    FScreenshotRequest::RequestScreenshot(FPaths::ProjectDir()/TEXT("Art/FurStudy")/FString::Printf(TEXT("Unreal-%s.png"),*View),false,false);
    FTimerHandle Handle;GetWorldTimerManager().SetTimer(Handle,[Passed](){FPlatformMisc::RequestExitWithStatus(false,Passed?0:1);},3.f,false);
}

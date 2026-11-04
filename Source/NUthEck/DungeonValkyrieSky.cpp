#include "DungeonPrototype.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"

void ADungeonPrototype::UpdateValkyrieSky()
{
    const bool Night=IsMoonlitValkyrieLevel();
    if(Night && !ValkyrieSky) {
        ValkyrieSky=NewObject<UStaticMeshComponent>(this,TEXT("ValkyrieNightSky"));
        ValkyrieSky->SetupAttachment(RootComponent);
        ValkyrieSky->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Sphere.Sphere")));
        ValkyrieSky->SetMaterial(0,LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/ValkyrieQuest/M_NightSky.M_NightSky")));
        ValkyrieSky->SetCollisionEnabled(ECollisionEnabled::NoCollision);ValkyrieSky->SetCastShadow(false);
        ValkyrieSky->bVisibleInRayTracing=false;
        ValkyrieSky->SetWorldScale3D(FVector(800));
        AddInstanceComponent(ValkyrieSky);ValkyrieSky->RegisterComponent();
        ValkyrieMoon=NewObject<UDirectionalLightComponent>(this,TEXT("ValkyrieMoonlight"));
        ValkyrieMoon->SetupAttachment(RootComponent);ValkyrieMoon->SetMobility(EComponentMobility::Movable);
        ValkyrieMoon->SetLightingChannels(false,false,true);
        // Light travels from the large moon at 20 degrees above the northern horizon.
        ValkyrieMoon->SetWorldRotation((-FVector(0,-.9396926f,.3420201f)).Rotation());
        ValkyrieMoon->SetLightColor(FLinearColor(.58f,.72f,1.f));ValkyrieMoon->SetIntensity(1.8f);
        ValkyrieMoon->SetLightSourceAngle(7.5f);ValkyrieMoon->SetCastShadows(true);
        ValkyrieMoon->SetVolumetricScatteringIntensity(0);
        AddInstanceComponent(ValkyrieMoon);ValkyrieMoon->RegisterComponent();
    }
    if(ValkyrieSky) {
        ValkyrieSky->SetVisibility(Night);ValkyrieMoon->SetVisibility(Night);
        if(Night)ValkyrieSky->SetWorldLocation(Camera->GetComponentLocation());
    }
    if(EnvironmentLight) {
        EnvironmentLight->SetLightColor(Night?FLinearColor(.58f,.70f,.95f):FLinearColor(.88f,.90f,.94f));
        EnvironmentLight->SetIntensity(Night?.55f:.6f);
    }
}

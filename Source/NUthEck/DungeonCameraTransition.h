#pragma once

#include "CoreMinimal.h"

// Reversible quartic dolly. Its final tangent is the player's viewing direction,
// so arrival is a forward approach from behind the eyes, rather than a sideways slide.
struct FDungeonCameraTransition
{
    FVector Start, Control1, Control2, Control3, Eye;

    static FDungeonCameraTransition Make(const FVector& Overview, const FVector& OverviewForward,
        const FVector& EyePosition, const FVector& EyeForward)
    {
        const double Distance=FVector::Distance(Overview,EyePosition);
        double Lead=Distance*.42;
        // A panned overview can be far from the hero. Its initial dolly must
        // also stay above the floor, rather than using that whole lateral gap.
        if(OverviewForward.Z<0.) Lead=FMath::Min(Lead,FMath::Max(0.,(Overview.Z-20.)/-OverviewForward.Z));
        double Approach=FMath::Clamp(Distance*.18,100.,300.);
        // Looking up puts the approach point below the eyes. Keep the entire
        // Bezier hull above the level's floor while retaining the exact gaze tangent.
        if(EyeForward.Z>0.) Approach=FMath::Min(Approach,FMath::Max(1.,(EyePosition.Z-20.)/(2.*EyeForward.Z)));
        // Three equally spaced final controls give zero curvature at arrival,
        // avoiding a lateral hook when entering from a distant panned view.
        return {Overview,Overview+OverviewForward*Lead,EyePosition-EyeForward*(2.*Approach),EyePosition-EyeForward*Approach,EyePosition};
    }

    FVector Position(double T) const
    {
        const double U=1.-T;
        return Start*(U*U*U*U)+Control1*(4.*U*U*U*T)+Control2*(6.*U*U*T*T)+Control3*(4.*U*T*T*T)+Eye*(T*T*T*T);
    }

    FVector Tangent(double T) const
    {
        const double U=1.-T;
        return (Control1-Start)*(4.*U*U*U)+(Control2-Control1)*(12.*U*U*T)
            +(Control3-Control2)*(12.*U*T*T)+(Eye-Control3)*(4.*T*T*T);
    }

    static FRotator ViewRotation(const FRotator& Overview, const FRotator& Look, double T)
    {
        // Shortest yaw arc with a level horizon; quaternion slerp can bank the
        // camera between an inclined overview and a very different final yaw.
        return FRotator(FMath::Lerp(Overview.Pitch,Look.Pitch,T),
            Overview.Yaw+FMath::FindDeltaAngleDegrees(Overview.Yaw,Look.Yaw)*T,0.);
    }
};

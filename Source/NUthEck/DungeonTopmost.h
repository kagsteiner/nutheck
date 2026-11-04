#pragma once
#include "NetHackSession.h"

// Presentation copy only: retain native terrain for navigation, memory and rules.
// The native foreground wins over background features; the neutral floor remains.
inline FNetHackCell TopmostRenderCell(const FNetHackCell& Native,bool Hero=false)
{
    FNetHackCell Result=Native;
    if(Result.Kind!=TEXT("unknown") && (Hero || Result.Kind!=TEXT("terrain")))
    {Result.Terrain=TEXT("floor");Result.DisplaySurface.Empty();}
    return Result;
}

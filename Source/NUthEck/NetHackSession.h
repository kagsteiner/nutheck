#pragma once
#include "CoreMinimal.h"
#include "HAL/PlatformProcess.h"

struct FNetHackCell
{
    FString Terrain=TEXT("none"), Kind=TEXT("unknown");
    int32 Glyph=-1;
    int32 TileIndex=-1;
    int32 Symbol=0;
    FString DisplayMonster;
    FString DisplayObject;
    FString DisplayStatue;
    FString DisplayTrap;
    FString DisplayArtifact;
    bool Female=false;
    bool Visible=false,Horizontal=false;
    bool PermanentLight=false,TemporaryLight=false;
};
struct FNetHackMenuItem
{
    FString Text;
    int32 Index=0, Key=0, Group=0;
    bool Selectable=false;
};

struct FNetHackStatusField
{
    FString Value,Text;
    bool Enabled=false;
    int32 Color=0;
};

// The child owns NetHack's globals and blocking loop. All access here is on the game thread.
class FNetHackSession
{
public:
    ~FNetHackSession();
    bool Start(bool NewGame=false,bool Remember=true);
    void Stop();
    void Pump();
    bool Reply(const FString& Payload);
    void Key(int32 Character);
    bool CanTravelTo(FIntPoint Cell) const;
    bool TravelTo(FIntPoint Cell);
    bool MouseTravelSupported=false;
    void Scroll(int32 Delta);
    bool TakeMapDirty() { bool Result=MapDirty; MapDirty=false; return Result; }
    bool IsCommand() const { return Awaiting && PromptType==TEXT("command"); }
    bool IsReady() const { return Hero.X>=0 && Turn>0; }
    bool IsBackendRunning();
    int32 KnownCellCount() const;

    TMap<FString,FNetHackStatusField> Status;
    TArray<FString> Conditions;
    FString StatusValue(const TCHAR* Name) const { const auto* F=Status.Find(Name);return F && F->Enabled?F->Value.TrimStartAndEnd():FString(); }
    FString StatusText(const TCHAR* Name) const { const auto* F=Status.Find(Name);return F && F->Enabled?F->Text.TrimStartAndEnd():FString(); }
    TArray<FNetHackCell> Cells;
    TArray<FString> Messages;
    TArray<FNetHackMenuItem> Menu;
    TMap<int32,int32> Selection;
    FString PromptType, PromptText, Line, CountPrefix, Error, SessionDirectory;
    FIntPoint OracleCenter=FIntPoint(-1,-1);
    FIntPoint Hero=FIntPoint(-1,-1);
    FString HeroRace;
    bool HeroPolymorphed=false,InMines=false,MinesTown=false,InSokoban=false;
    int32 SokobanStage=0;
    FIntPoint Cursor=FIntPoint(-1,-1);
    int32 Turn=0,HP=0,MaxHP=0,AC=0,Level=0,Depth=0,Dungeon=0;
    int32 Sequence=0,MenuMode=0,MenuScroll=0,MenuPageSize=20;
    bool Awaiting=false,Ended=false,Connected=false;
private:
    void Event(const TSharedPtr<class FJsonObject>& Object);
    void AddMessage(const FString& Text);
    void ToggleItem(const FNetHackMenuItem& Item);
    FProcHandle Process;
    void* OutputRead=nullptr;
    void* InputWrite=nullptr;
    FString Pending;
    bool MapDirty=true;
};

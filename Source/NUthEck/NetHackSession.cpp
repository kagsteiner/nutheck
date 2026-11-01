#include "NetHackSession.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "HAL/FileManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Misc/CommandLine.h"

FNetHackSession::~FNetHackSession() { Stop(); }

bool FNetHackSession::Start(bool NewGame,bool Remember)
{
    Cells.SetNum(79*21);
    const FString Executable=FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()/TEXT("Binaries/NetHack/NetHackBridge.exe"));
    if(!FPaths::FileExists(Executable))
    {
        Error=TEXT("NetHack bridge is missing. Run Scripts/BuildNetHackBridge.ps1.");
        AddMessage(Error); Ended=true; return false;
    }
    const FString SessionsRoot=FPaths::ConvertRelativePathToFull(FPaths::ProjectSavedDir()/TEXT("NetHack"));
    FString SessionId;
    FGuid ExistingId;
    if(Remember && !NewGame) FFileHelper::LoadFileToString(SessionId,*(SessionsRoot/TEXT("LastSession.txt")));
    SessionId.TrimStartAndEndInline();
    if(!FGuid::ParseExact(SessionId,EGuidFormats::Digits,ExistingId)) SessionId=FGuid::NewGuid().ToString(EGuidFormats::Digits);
    SessionDirectory=SessionsRoot/SessionId;
    IFileManager::Get().MakeDirectory(*SessionDirectory,true);
    FString Preview;
    if(NewGame && FParse::Value(FCommandLine::Get(),TEXT("HumanPlayerPreview="),Preview))
    {
        const bool Valkyrie=Preview==TEXT("valkyrie_female_human");
        if(Valkyrie || Preview==TEXT("barbarian_male_human"))
        {
            const FString Profile=FString::Printf(TEXT("OPTIONS=number_pad:0,!tutorial,!legacy,!news,time,lit_corridor,!autopickup\nOPTIONS=role:%s,race:human,gender:%s,align:%s\n"),
                Valkyrie?TEXT("Valkyrie"):TEXT("Barbarian"),Valkyrie?TEXT("female"):TEXT("male"),Valkyrie?TEXT("lawful"):TEXT("neutral"));
            FFileHelper::SaveStringToFile(Profile,*(SessionDirectory/TEXT(".nethackrc")));
        }
    }
    if(Remember) FFileHelper::SaveStringToFile(SessionId,*(SessionsRoot/TEXT("LastSession.txt")));
    void *OutputWrite=nullptr,*InputRead=nullptr;
    if(!FPlatformProcess::CreatePipe(OutputRead,OutputWrite) || !FPlatformProcess::CreatePipe(InputRead,InputWrite,true))
    {
        FPlatformProcess::ClosePipe(OutputRead,OutputWrite);
        FPlatformProcess::ClosePipe(InputRead,InputWrite);
        OutputRead=InputWrite=nullptr;
        Error=TEXT("Unable to create NetHack pipes."); AddMessage(Error); Ended=true; return false;
    }
    const FString Arguments=FString::Printf(TEXT("\"--ue-root=%s\" -uAdventurer"),*SessionDirectory);
    const FString WorkingDirectory=FPaths::GetPath(Executable);
    Process=FPlatformProcess::CreateProc(*Executable,*Arguments,false,true,true,nullptr,0,*WorkingDirectory,OutputWrite,InputRead,OutputWrite);
    FPlatformProcess::ClosePipe(nullptr,OutputWrite);
    FPlatformProcess::ClosePipe(InputRead,nullptr);
    if(!Process.IsValid()) { Error=TEXT("Unable to launch NetHack."); AddMessage(Error); Ended=true; Stop(); return false; }
    UE_LOG(LogTemp,Display,TEXT("NETHACK_SESSION_START %s"),*SessionDirectory);
    return true;
}

void FNetHackSession::Stop()
{
    if(InputWrite) { FPlatformProcess::ClosePipe(nullptr,InputWrite); InputWrite=nullptr; }
    if(Process.IsValid())
    {
        const double Deadline=FPlatformTime::Seconds()+2.0;
        while(FPlatformProcess::IsProcRunning(Process) && FPlatformTime::Seconds()<Deadline)
        {
            // A final map/message burst must not fill stdout and block the core's save-on-EOF.
            if(OutputRead) FPlatformProcess::ReadPipe(OutputRead);
            FPlatformProcess::Sleep(.01f);
        }
        if(FPlatformProcess::IsProcRunning(Process)) FPlatformProcess::TerminateProc(Process,true);
        FPlatformProcess::CloseProc(Process);
    }
    if(OutputRead) { FPlatformProcess::ClosePipe(OutputRead,nullptr); OutputRead=nullptr; }
}

void FNetHackSession::AddMessage(const FString& Text)
{
    if(Text.IsEmpty()) return;
    Messages.Add(Text);
    if(Messages.Num()>100) Messages.RemoveAt(0,Messages.Num()-100);
    UE_LOG(LogTemp,Display,TEXT("NETHACK_MESSAGE %s"),*Text);
}

void FNetHackSession::Pump()
{
    if(!OutputRead) return;
    FString Chunk=FPlatformProcess::ReadPipe(OutputRead);
    if(!Chunk.IsEmpty())
    {
        FFileHelper::SaveStringToFile(Chunk,*(SessionDirectory/TEXT("events.ndjson")),FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM,&IFileManager::Get(),FILEWRITE_Append);
        Pending+=Chunk;
    }
    int32 End;
    while(Pending.FindChar('\n',End))
    {
        FString Record=Pending.Left(End).TrimEnd();
        Pending.RightChopInline(End+1);
        TSharedPtr<FJsonObject> Object;
        if(FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Record),Object) && Object.IsValid()) Event(Object);
        else if(!Record.IsEmpty()) AddMessage(Record.Left(500));
    }
    if(Pending.Len()>1024*1024) { Error=TEXT("NetHack protocol record exceeded its limit."); AddMessage(Error); Stop(); Ended=true; }
    if(Process.IsValid() && !FPlatformProcess::IsProcRunning(Process))
    {
        int32 Code=0; FPlatformProcess::GetProcReturnCode(Process,&Code);
        if(!Ended) AddMessage(FString::Printf(TEXT("NetHack ended (exit %d). Press F2 for a new game."),Code));
        Ended=true; Awaiting=false;
        FPlatformProcess::CloseProc(Process);
        UE_LOG(LogTemp,Display,TEXT("NETHACK_SESSION_END code=%d"),Code);
    }
}

void FNetHackSession::Event(const TSharedPtr<FJsonObject>& O)
{
    FString Type;
    if(!O->TryGetStringField(TEXT("event"),Type)) return;
    if(Type==TEXT("hello")) { Connected=true; return; }
    if(Type==TEXT("cursor")) { Cursor=FIntPoint(O->GetIntegerField(TEXT("x")),O->GetIntegerField(TEXT("y"))); return; }
    if(Type==TEXT("message")) { AddMessage(O->GetStringField(TEXT("text"))); return; }
    if(Type==TEXT("end")) { Ended=true; Awaiting=false; AddMessage(TEXT("Game ended. Press F2 for a new game.")); return; }
    if(Type==TEXT("clear")) { for(auto& Cell:Cells) Cell=FNetHackCell(); MapDirty=true; return; }
    if(Type==TEXT("tile"))
    {
        const int32 X=O->GetIntegerField(TEXT("x")),Y=O->GetIntegerField(TEXT("y"));
        if(X<0 || X>=79 || Y<0 || Y>=21) return;
        FNetHackCell& Cell=Cells[Y*79+X];
        const FString Terrain=O->GetStringField(TEXT("terrain"));
        Cell.Kind=O->GetStringField(TEXT("kind")); Cell.Glyph=O->GetIntegerField(TEXT("glyph"));
        Cell.TileIndex=-1;
        if(O->HasTypedField<EJson::Number>(TEXT("tile_index"))) Cell.TileIndex=O->GetIntegerField(TEXT("tile_index"));
        Cell.DisplayMonster.Empty(); Cell.Female=false;
        Cell.DisplayObject.Empty();
        O->TryGetStringField(TEXT("display_object"),Cell.DisplayObject);
        O->TryGetStringField(TEXT("display_monster"),Cell.DisplayMonster);
        O->TryGetBoolField(TEXT("female"),Cell.Female);
        Cell.Symbol=O->GetIntegerField(TEXT("symbol")); Cell.Horizontal=O->GetBoolField(TEXT("horizontal"));
        if(Cell.Kind==TEXT("unknown")) Cell.Terrain=TEXT("none");
        else if(Terrain!=TEXT("none")) Cell.Terrain=Terrain;
        // An entity needs a support surface, but never query hidden core terrain.
        else if(Cell.Terrain==TEXT("none") || Cell.Terrain==TEXT("stone")) Cell.Terrain=TEXT("floor");
        MapDirty=true; return;
    }
    if(Type==TEXT("state"))
    {
        O->TryGetStringField(TEXT("hero_race"),HeroRace);
        O->TryGetBoolField(TEXT("hero_polymorphed"),HeroPolymorphed);
        Hero=FIntPoint(O->GetIntegerField(TEXT("x")),O->GetIntegerField(TEXT("y")));
        Turn=O->GetIntegerField(TEXT("moves")); HP=O->GetIntegerField(TEXT("hp")); MaxHP=O->GetIntegerField(TEXT("maxhp"));
        AC=O->GetIntegerField(TEXT("ac")); Level=O->GetIntegerField(TEXT("level")); Depth=O->GetIntegerField(TEXT("depth")); Dungeon=O->GetIntegerField(TEXT("dungeon"));
        const FString Vision=O->GetStringField(TEXT("vision"));
        for(int32 I=0;I<Cells.Num();++I) Cells[I].Visible=Vision.IsValidIndex(I) && Vision[I]=='1';
        MapDirty=true; return;
    }
    if(Type==TEXT("menu"))
    {
        Menu.Reset(); Selection.Reset(); MenuScroll=0; CountPrefix.Reset();
        MenuMode=O->GetIntegerField(TEXT("how"));
        for(const auto& Value:O->GetArrayField(TEXT("items")))
        {
            auto Item=Value->AsObject(); FNetHackMenuItem Entry;
            Entry.Index=Item->GetIntegerField(TEXT("index")); Entry.Key=Item->GetIntegerField(TEXT("key"));
            Entry.Group=Item->GetIntegerField(TEXT("group")); Entry.Text=Item->GetStringField(TEXT("text"));
            Entry.Selectable=Item->GetBoolField(TEXT("selectable"));
            if(MenuMode && Entry.Selectable && Item->GetBoolField(TEXT("selected"))) Selection.Add(Entry.Index,-1);
            Menu.Add(MoveTemp(Entry));
        }
        return;
    }
    if(Type==TEXT("input"))
    {
        Sequence=O->GetIntegerField(TEXT("seq")); PromptType=O->GetStringField(TEXT("type")); PromptText=O->GetStringField(TEXT("text"));
        Awaiting=true; Line.Reset();
        UE_LOG(LogTemp,Display,TEXT("NETHACK_INPUT seq=%d type=%s turn=%d"),Sequence,*PromptType,Turn);
    }
}

bool FNetHackSession::Reply(const FString& Payload)
{
    if(!Awaiting || !InputWrite || Payload.Contains(TEXT("\n")) || Payload.Contains(TEXT("\r"))) return false;
    const FString Response=FString::Printf(TEXT("%d\t%s"),Sequence,*Payload);
    if(!FPlatformProcess::WritePipe(InputWrite,Response)) { AddMessage(TEXT("NetHack input pipe closed.")); Ended=true; return false; }
    FFileHelper::SaveStringToFile(Response+TEXT("\n"),*(SessionDirectory/TEXT("input.tsv")),FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM,&IFileManager::Get(),FILEWRITE_Append);
    Awaiting=false; return true;
}

int32 FNetHackSession::KnownCellCount() const
{
    int32 Count=0;
    for(const auto& Cell:Cells) if(Cell.Kind!=TEXT("unknown") && Cell.Terrain!=TEXT("stone")) ++Count;
    return Count;
}

void FNetHackSession::Scroll(int32 Delta)
{
    MenuScroll=FMath::Clamp(MenuScroll+Delta,0,FMath::Max(0,Menu.Num()-MenuPageSize));
}

void FNetHackSession::ToggleItem(const FNetHackMenuItem& Item)
{
    if(MenuMode==0 || !Item.Selectable) return;
    const int32 Count=CountPrefix.IsEmpty()?-1:FMath::Max(1,FCString::Atoi(*CountPrefix));
    CountPrefix.Reset();
    if(MenuMode==1) Reply(FString::Printf(TEXT("%d:%d"),Item.Index,Count));
    else if(Selection.Contains(Item.Index)) Selection.Remove(Item.Index);
    else Selection.Add(Item.Index,Count);
}

void FNetHackSession::Key(int32 C)
{
    if(!Awaiting || Ended) return;
    if(PromptType==TEXT("line"))
    {
        if(C==27) Reply(FString::Chr(27));
        else if(C==13 || C==10) Reply(Line);
        else if(C==8) Line.LeftChopInline(1);
        else if(C>=32 && C<=126 && Line.Len()<240) Line.AppendChar(TCHAR(C));
        return;
    }
    if(PromptType==TEXT("menu"))
    {
        if(C==27) { Reply(MenuMode?TEXT("-1"):TEXT("")); return; }
        if(C==13 || C==10 || (C==32 && MenuScroll+MenuPageSize>=Menu.Num()))
        {
            FString Answer; TArray<int32> Indices; Selection.GetKeys(Indices); Indices.Sort();
            for(int32 Index:Indices) { if(!Answer.IsEmpty()) Answer+=TEXT(","); Answer+=FString::Printf(TEXT("%d:%d"),Index,Selection[Index]); }
            Reply(Answer); return;
        }
        if(C==32) { Scroll(MenuPageSize); return; }
        if(C==8) { CountPrefix.LeftChopInline(1); return; }
        for(const auto& Item:Menu) if(Item.Selectable && Item.Key==C) { ToggleItem(Item); return; }
        if(C>='0' && C<='9' && CountPrefix.Len()<6) { CountPrefix.AppendChar(TCHAR(C)); return; }
        if(MenuMode==2)
        {
            if(C=='-') Selection.Reset();
            else if(C=='.' || C=='@')
            {
                for(const auto& Item:Menu) if(Item.Selectable) {
                    if(C=='@' && Selection.Contains(Item.Index)) Selection.Remove(Item.Index);
                    else Selection.Add(Item.Index,-1);
                }
            }
            else
            {
                for(const auto& Item:Menu) if(Item.Selectable && Item.Group && Item.Group==C) ToggleItem(Item);
            }
        }
        return;
    }
    if(PromptType==TEXT("continue")) { if(C==32 || C==13 || C==27) Reply(FString::FromInt(C)); return; }
    Reply(FString::FromInt(C));
}

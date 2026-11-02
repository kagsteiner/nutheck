#include "DungeonPrototype.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/Font.h"
#include "Misc/CommandLine.h"
#include "CanvasItem.h"
#include "Fonts/SlateFontInfo.h"

namespace
{
const FLinearColor StatusInk(.88f,.91f,.89f),StatusMuted(.57f,.65f,.66f);
const FLinearColor StatusYellow(1.f,.77f,.12f),StatusRed(1.f,.22f,.18f),StatusGreen(.34f,.88f,.57f);
struct FStatusToken { FString Text;FLinearColor Color; };
struct FStatusRun { FString Text;FLinearColor Color;FVector2D Position;float Width; };

FLinearColor HealthColor(int32 HP,int32 MaxHP)
{
    if(MaxHP<=0)return StatusMuted;
    const double Ratio=double(HP)/MaxHP;
    return Ratio<=.25?StatusRed:Ratio<=.5?StatusYellow:StatusGreen;
}
FLinearColor HungerColor(const FString& Hunger)
{
    if(Hunger==TEXT("Hungry") || Hunger==TEXT("Satiated"))return StatusYellow;
    return Hunger.IsEmpty() || Hunger==TEXT("Normal")?StatusInk:StatusRed;
}
}

void ADungeonPrototypeHUD::DrawLiveFooter(FNetHackSession& Live)
{
    const float W=Canvas->SizeX,H=Canvas->SizeY,S=FMath::Clamp(W/1600.f,.65f,1.5f);
    auto* Dungeon=Cast<ADungeonPrototype>(GetOwningPlayerController()->GetViewTarget());
    int32 HP=Live.StatusValue(TEXT("hitpoints")).IsEmpty()?FMath::Max(0,Live.HP):FCString::Atoi(*Live.StatusValue(TEXT("hitpoints")));
    int32 MaxHP=Live.StatusValue(TEXT("hitpoints-max")).IsEmpty()?Live.MaxHP:FCString::Atoi(*Live.StatusValue(TEXT("hitpoints-max")));
    FString Hunger=Live.StatusValue(TEXT("hunger"));
    if(Hunger.IsEmpty())Hunger=Live.Status.Contains(TEXT("hunger"))?TEXT("Normal"):TEXT("--");
    TArray<TArray<FStatusToken>> Groups;Groups.SetNum(3);
    const auto Add=[&Groups](int32 Row,const FString& Text,FLinearColor Color=StatusInk)
    {if(!Text.IsEmpty())Groups[Row].Add({Text,Color});};
    if(Live.Ended)Add(0,TEXT("SESSION ENDED"),StatusYellow);
    for(const TCHAR* Name:{TEXT("title"),TEXT("strength"),TEXT("dexterity"),TEXT("constitution"),TEXT("intelligence"),TEXT("wisdom"),TEXT("charisma"),TEXT("alignment"),TEXT("score")})
        Add(0,Live.StatusText(Name));
    if(Groups[0].IsEmpty())Add(0,Live.IsReady()?TEXT("Waiting for native status..."):TEXT("Choose your character to enter the dungeon."));
    Add(1,Live.StatusText(TEXT("dungeon-level")));
    const FString Gold=Live.StatusValue(TEXT("gold"));
    if(!Gold.IsEmpty())Add(1,Gold); // Includes NetHack's currency symbol and amount.
    Add(1,Live.StatusText(TEXT("power"))+Live.StatusText(TEXT("power-max")));
    Add(1,Live.StatusText(TEXT("armor-class")));
    Add(1,Live.StatusText(TEXT("experience-level"))+Live.StatusText(TEXT("experience")));
    Add(1,Live.StatusText(TEXT("HD")));
    Add(1,Live.StatusText(TEXT("time")));
    Add(1,Live.StatusText(TEXT("version")));
    Add(2,Live.StatusText(TEXT("carrying-capacity")),StatusYellow);
    for(const FString& Condition:Live.Conditions)
    {
        const bool Fatal=Condition==TEXT("Stone") || Condition==TEXT("Slime") || Condition==TEXT("Strngl")
            || Condition==TEXT("FoodPois") || Condition==TEXT("TermIll") || Condition==TEXT("Grab") || Condition==TEXT("InLava");
        Add(2,Condition,Fatal?StatusRed:StatusYellow);
    }
    for(const TCHAR* Name:{TEXT("weapon"),TEXT("armor"),TEXT("terrain")})Add(2,Live.StatusText(Name));

    // Capture-only display fixtures do not modify the session or native game.
    FString Preview;
    if(FParse::Param(FCommandLine::Get(),TEXT("CaptureLive")))FParse::Value(FCommandLine::Get(),TEXT("StatusHUDPreview="),Preview);
    if(Preview==TEXT("warning")){HP=8;MaxHP=20;Hunger=TEXT("Hungry");}
    if(Preview==TEXT("critical")){HP=3;MaxHP=20;Hunger=TEXT("Weak");}
    if(Preview==TEXT("stress"))
    {
        HP=1234;MaxHP=9999;Hunger=TEXT("Fainting");
        Add(0,TEXT("A very long hero name the Master of Thieves"));Add(0,TEXT("St:18/**"));Add(0,TEXT("S:1234567890"));
        Add(1,TEXT("Astral Plane $:999999 Pw:9999(9999) AC:-127 Xp:30/123456789 T:123456789"));
        for(const TCHAR* Text:{TEXT("Overloaded"),TEXT("Stone"),TEXT("Slime"),TEXT("Strngl"),TEXT("FoodPois"),TEXT("TermIll"),TEXT("Blind"),TEXT("Deaf"),TEXT("Stun"),TEXT("Conf"),TEXT("Hallu"),TEXT("Lev"),TEXT("Ride"),TEXT("Grab"),TEXT("Held"),TEXT("InLava"),TEXT("Parlyz"),TEXT("Zzz"),TEXT("Out"),TEXT("Fly"),TEXT("Iron"),TEXT("Glow"),TEXT("Slip"),TEXT("Teth"),TEXT("Trap"),TEXT("WLegs"),TEXT("UHold"),TEXT("Submrg"),TEXT("Icy"),TEXT("Busy"),TEXT("Bare"),TEXT("Weapon: dual-wielding"),TEXT("Armor: full plate"),TEXT("Terrain: ice")})Add(2,Text,StatusYellow);
    }

    UFont* Font=GEngine->GetSmallFont();
    const float TextScale=1.05f*S,LineHeight=22*S,TextX=280*S,Right=W-24*S;
    TArray<FStatusRun> Runs;int32 Row=0;
    for(const auto& Group:Groups)
    {
        float X=TextX;bool Used=false;
        for(const auto& Token:Group)
        {
            // Wrap words instead of truncating fields, long titles or conditions.
            TArray<FString> Words;Token.Text.ParseIntoArray(Words,TEXT(" "),true);
            for(const FString& Word:Words)
            {
                float TW=0,TH=0;Canvas->StrLen(Font,Word,TW,TH);TW*=TextScale;
                if(X+TW>Right && X>TextX){++Row;X=TextX;}
                Runs.Add({Word,Token.Color,FVector2D(X,Row*LineHeight),TW});
                X+=TW+7*S;Used=true;
            }
            if(Used)X+=9*S;
        }
        if(Used)++Row;
    }
    const float BodyHeight=FMath::Max(108*S,Row*LineHeight);
    const float FooterHeight=76*S+BodyHeight+30*S,Top=H-FooterHeight,StatusY=Top+76*S;
    if(Dungeon)Dungeon->SetLiveFooterHeight(FooterHeight);
    DrawRect(FLinearColor(.018f,.028f,.036f,.99f),0,Top,W,FooterHeight);
    DrawLine(24*S,Top,W-24*S,Top,FLinearColor(.22f,.32f,.34f),1);

    TArray<FString> MessageLines;
    const int32 MaxChars=FMath::Max(35,int32((W/S-64)/7.5f));
    for(const auto& Message:Live.Messages)
    {
        FString Rest=Message;
        while(Rest.Len()>MaxChars)
        {
            int32 Break=MaxChars;while(Break>MaxChars/2 && Rest[Break]!=' ')--Break;
            if(Break<=MaxChars/2)Break=MaxChars;
            MessageLines.Add(Rest.Left(Break));Rest=Rest.Mid(Break).TrimStart();
        }
        MessageLines.Add(Rest);
    }
    for(int32 I=FMath::Max(0,MessageLines.Num()-3),N=0;I<MessageLines.Num();++I,++N)
        DrawText(MessageLines[I],StatusInk,32*S,Top+(10+N*18)*S,Font,S);

    const FLinearColor Health=HealthColor(HP,MaxHP);
    DrawRect(FLinearColor(.04f,.075f,.085f),24*S,StatusY-3*S,232*S,108*S);
    DrawRect(Health,24*S,StatusY-3*S,4*S,108*S);
    DrawText(TEXT("HIT POINTS"),StatusMuted,38*S,StatusY+3*S,Font,.9f*S);
    const FString HPText=Live.IsReady()?FString::Printf(TEXT("%d / %d"),HP,MaxHP):TEXT("-- / --");
    // Rasterize bold text at its target size; scaling the small bitmap font
    // makes this most important number blurry on larger displays.
    const int32 HPFontSize=FMath::Max(10,FMath::FloorToInt(FMath::Min(28.f,202.f/(HPText.Len()*.8f))*S));
    FCanvasTextItem HealthText(FVector2D(38*S,StatusY+18*S),FText::FromString(HPText),FSlateFontInfo(TitleFont,HPFontSize,FName(TEXT("Bold"))),Health);
    Canvas->DrawItem(HealthText);
    DrawRect(FLinearColor(.14f,.18f,.19f),38*S,StatusY+62*S,202*S,8*S);
    const float Ratio=MaxHP>0?FMath::Clamp(float(HP)/MaxHP,0.f,1.f):0.f;
    DrawRect(Health,38*S,StatusY+62*S,202*S*Ratio,8*S);
    DrawText(TEXT("Hunger: ")+Hunger,HungerColor(Hunger),38*S,StatusY+82*S,Font,S);
    for(const auto& Run:Runs)DrawText(Run.Text,Run.Color,Run.Position.X,StatusY+Run.Position.Y,Font,TextScale);
    DrawText(Live.Ended?TEXT("Esc Quit app  /  F2 New game"):TEXT("ARROWS / NUMPAD Move   i Inventory   o Open   , Pick up   F1 Help   WHEEL Zoom   LEFT-CLICK Travel   RIGHT-DRAG Orbit   MIDDLE-DRAG Pan   F7 Labels   F9 Style"),
        StatusMuted,32*S,H-22*S,Font,.85f*S);

    if(FParse::Param(FCommandLine::Get(),TEXT("VerifyStatusHUD")) && Live.IsReady() && !Live.Status.IsEmpty())
    {
        bool Fits=Top>=84*S && StatusY+BodyHeight<=H-30*S && HealthText.DrawnSize.X<=202*S+1 && HealthText.DrawnSize.Y<=44*S+1;
        for(const auto& Run:Runs)Fits &= Run.Position.X+Run.Width<=Right+1;
        static FString LastCase;const FString Key=FString::Printf(TEXT("%.0fx%.0f_%s"),W,H,*Preview);
        if(LastCase!=Key)
        {
            LastCase=Key;
            UE_LOG(LogTemp,Display,TEXT("STATUS_HUD_CHECK %s viewport=%.0fx%.0f scenario=%s fields=%d conditions=%d rows=%d footer=%.1f hp=%d/%d hunger=%s"),
                Fits?TEXT("PASS"):TEXT("FAIL"),W,H,*Preview,Live.Status.Num(),Live.Conditions.Num(),Row,FooterHeight,HP,MaxHP,*Hunger);
            if(!Fits)FPlatformMisc::RequestExitWithStatus(false,1);
        }
    }
}

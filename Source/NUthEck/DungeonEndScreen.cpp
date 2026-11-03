#include "DungeonPrototype.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "UnrealClient.h"

bool ADungeonPrototype::IsEndScreenVisible() const
{
    return Session && Session->Ended && !Session->Awaiting;
}

bool ADungeonPrototype::CanLeaveEndedSession() const
{
    return IsEndScreenVisible() && !Session->IsBackendRunning();
}

FBox2D ADungeonPrototype::EndScreenButton(FVector2D Size,bool Quit)
{
    const float S=FMath::Clamp(Size.X/1600.f,.65f,1.5f);
    const FVector2D Min((Size.X-560*S)*.5f+(Quit?28:296)*S,(Size.Y-210*S)*.5f+130*S);
    return FBox2D(Min,Min+FVector2D(236*S,48*S));
}

bool ADungeonPrototype::ActivateEndScreenAt(FVector2D Position)
{
    if(!CanLeaveEndedSession())return false;
    int32 W=0,H=0;GetWorld()->GetFirstPlayerController()->GetViewportSize(W,H);
    if(EndScreenButton(FVector2D(W,H),true).IsInside(Position)){QuitEndedSession();return true;}
    if(EndScreenButton(FVector2D(W,H),false).IsInside(Position)){StartLiveGame(true);return true;}
    return false;
}

void ADungeonPrototype::QuitEndedSession()
{
    // Wait until the core has completed saves/post-game output and exited.
    // Never turn this presentation action into a native Q command or forced kill.
    if(!CanLeaveEndedSession())return;
    UE_LOG(LogTemp,Display,TEXT("NETHACK_APP_QUIT ended=1 backend_running=0 turn=%d sequence=%d"),Session->Turn,Session->Sequence);
    UKismetSystemLibrary::QuitGame(this,GetWorld()->GetFirstPlayerController(),EQuitPreference::Quit,false);
}

// Explicit -CaptureLive test only: a fresh disposable native session saves or
// quits normally, then exercises the same end-panel exit paths as player input.
void ADungeonPrototype::TickEndScreenVerification()
{
    const double Now=FPlatformTime::Seconds();
    if(Now-LiveStartedTime>45){UE_LOG(LogTemp,Error,TEXT("END_SCREEN_CHECK FAIL timeout"));FPlatformMisc::RequestExitWithStatus(false,1);return;}
    FString Case;FParse::Value(FCommandLine::Get(),TEXT("EndScreenCase="),Case);
    const bool Save=Case==TEXT("save");
    if(EndScreenCheckStage==0 && Session->Awaiting && !Session->IsCommand())
    {
        if(Session->PromptType==TEXT("menu"))Session->Reply(Session->MenuMode?TEXT("-1"):TEXT(""));
        else Session->Key(' ');
        return;
    }
    if(EndScreenCheckStage==0 && Session->IsCommand())
    {
        bool Passed=!IsEndScreenVisible() && !CanLeaveEndedSession();
        const int32 Turn=Session->Turn,Sequence=Session->Sequence;
        Passed &= !ActivateEndScreenAt(EndScreenButton(FVector2D(1600,900),true).GetCenter());
        Passed &= Session->Turn==Turn && Session->Sequence==Sequence;
        for(FVector2D Size:{FVector2D(1024,768),FVector2D(1600,900),FVector2D(3840,2160)})
        {
            const auto Quit=EndScreenButton(Size,true),New=EndScreenButton(Size,false);
            Passed &= Quit.Min.X>=0 && New.Max.X<=Size.X && Quit.Max.X<New.Min.X && Quit.Min.Y>=0 && Quit.Max.Y<=Size.Y;
        }
        if(!Passed){UE_LOG(LogTemp,Error,TEXT("END_SCREEN_CHECK FAIL active_guard_or_layout"));FPlatformMisc::RequestExitWithStatus(false,1);return;}
        Session->Key(Save?'S':'#');EndScreenCheckStage=1;
    }
    else if(EndScreenCheckStage==1)
    {
        if(Session->Awaiting)
        {
            // NetHack's native quit command is #quit; Q remains quiver.
            if(!Save && Session->PromptType==TEXT("line"))Session->Reply(TEXT("quit"));
            else if(Session->IsCommand()){UE_LOG(LogTemp,Error,TEXT("END_SCREEN_CHECK FAIL native_command_did_not_end"));FPlatformMisc::RequestExitWithStatus(false,1);return;}
            else if(Session->PromptType==TEXT("menu"))Session->Reply(Session->MenuMode?TEXT("-1"):TEXT(""));
            else if(Session->PromptType==TEXT("yn"))Session->Key('y');
            else Session->Key(' ');
        }
        if(CanLeaveEndedSession())
        {
            ResetOverview();EndScreenCheckStage=2;EndScreenCheckTime=Now;
        }
    }
    else if(EndScreenCheckStage==2 && Now-EndScreenCheckTime>.5)
    {
        FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/FString::Printf(TEXT("Screenshots/EndScreen-%s.png"),*Case),true,false);
        EndScreenCheckStage=3;EndScreenCheckTime=Now;
    }
    else if(EndScreenCheckStage==3 && Now-EndScreenCheckTime>1)
    {
        UE_LOG(LogTemp,Display,TEXT("END_SCREEN_CHECK PASS case=%s active_guard=1 layout_sizes=3 ended=1 backend_running=0 exit=%s"),*Case,Save?TEXT("Escape"):TEXT("click"));
        // Esc must quit the ended app even if death/save occurred in first person.
        if(Save){FirstPerson=true;HandleLiveKey(EKeys::Escape,false);}
        else
        {
            int32 W=0,H=0;GetWorld()->GetFirstPlayerController()->GetViewportSize(W,H);
            ActivateEndScreenAt(EndScreenButton(FVector2D(W,H),true).GetCenter());
        }
        EndScreenCheckStage=4;
    }
}

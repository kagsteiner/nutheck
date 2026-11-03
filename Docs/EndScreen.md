# End-of-session app controls

After NetHack finishes saving, quitting or death, a centred **Session ended**
panel offers **Quit app [Esc]** and **New game [F2]**. Both controls are clickable.
The footer also lists the keys. The panel uses neutral wording because a saved
run is not a dead character, and hides the native terminal HP value.

Quit uses Unreal's normal quit command. It is enabled only when the native
session has ended, is not awaiting a prompt, and its backend process has exited.
While NetHack finishes, the panel says to wait and the actions do nothing.
Native post-game menus/prompts remain in control until completion. This path
never sends a native quit command or force-kills a player backend.

During a live game, Escape still cancels native prompts or returns from first
person as before. `S` remains native save; `#quit` remains native quit. `Q` is
NetHack's native quiver command and is not rebound. After the run ends, Escape
quits even if it ended in first-person view. F2/new-game retains the existing
explicit new-session action and does not delete the saved run.

`DungeonEndScreen.cpp` shares button bounds between HUD drawing and mouse hit
testing. `CanLeaveEndedSession` guards keyboard, mouse and new-game actions.
`NetHackSession::IsBackendRunning` queries process state without stopping it.
No change is made to native save handling or the existing shutdown timeout.

Verification uses disposable `Saved/NetHackCaptures` and `NetHackGameplayTests`
roots. `VerifyEndScreen.ps1` saves a real native game and verifies that its save
exists, then exercises Escape exit. A second run uses native `#quit` and clicks
the app-exit button. The live tests cover active-game rejection, three viewport
sizes and the first-person Escape precedence after ending. `BridgeDeathEnd.py`
verifies that a real isolated native death emits the same terminal `end` event.
The UI does not branch on cause of ending, so that event exposes the same panel.

Editor build and both live scenarios pass, with normal app process exit code 0.
The native save scenario retains its save file. The death terminal-event check
also passes. Both panel screenshots were inspected:
[after save](Images/EndScreen/save.png), [after quit](Images/EndScreen/quit.png).
Existing first-person/presentation verification passes all 240 paths and eight
headings, with unchanged turn 5/input sequence 7.

Before changes, all player sessions and native runtime were backed up in
`Backups/NetHackSaves/20261101T132814.882773Z.zip`. The final hash audit confirms
all 1,076 original files, the played-session file set and `LastSession.txt` are
unchanged. No played game was launched, advanced or stopped; no native backend
was rebuilt. Audit: `Images/EndScreen/save-preservation.json`.

Evidence: `build-end-screen-{unreal,save,quit,death}.log`,
`build-presentation-controls-live.log`, `Scripts/VerifyEndScreen.ps1`,
`Scripts/VerifyPresentationControls.ps1` and `Tests/BridgeDeathEnd.py`.

# Player save protection

The user's instruction of 2026-10-31 supersedes the earlier permission to reset
development saves. This installation is now their actual NetHack game.

Player sessions live in `Saved/NetHack/<session-id>/`. Preserve the whole tree,
including `LastSession.txt`, hidden configuration, native saves, level/lock files
and diagnostics. Tests must use fresh isolated sessions and must not change the
last-played pointer. Do not launch or advance the player's session for testing.

## Backups

Run `Scripts/BackupNetHackSaves.ps1` while the backend is stopped. It creates a
new timestamped archive under `Backups/NetHackSaves/`, outside `Saved`, with all
session files plus the matching `Binaries/NetHack` runtime/data. Nothing is pruned.
Every file has a SHA-256 digest and size in the archive manifest. The helper
checks the archive and rechecks source contents before publishing it as `.zip`.

The helper refuses a running NetHack backend; save and exit normally first.
Never force-stop the player game to obtain a backup. A process-list permission
failure also stops the backup rather than assuming the game is closed. In the
Codex sandbox, Windows process inspection may require an escalated tool call.

`LaunchPrototype.ps1` automatically backs up before and after normal player
launches. Capture/study runs remain isolated. `BuildNetHackBridge.ps1` backs up
before rebuilding or replacing the backend. Launching directly in the Unreal
editor bypasses launcher backups; make a manual backup before save-affecting
work. There is no in-game rolling backup/checkpoint feature in this change.

These are local verified snapshots within the project. Verification proves file
integrity; it does not claim that an incomplete crash save is playable or that
an off-device copy has completed.

## Recovery

First preserve the current files in another verified snapshot. Choose a known
backup by date/session, and verify it with:

```powershell
python Scripts/NetHackSaveBackup.py verify Backups/NetHackSaves/<archive>.zip
python Scripts/NetHackSaveBackup.py recover Backups/NetHackSaves/<archive>.zip Backups/RecoveredNetHack/<new-directory>
```

Recovery extracts into a **new** directory, checks every extracted file, and
refuses an existing destination. It never changes the live saves or installs an
older runtime. The result contains `NetHack/` (including the original session
pointer) and `Runtime/` (the matching backend and data).

Inspect the staged save/session before selecting it for play. Keep the newer
live files and all backups. If an actual crash left native level/lock files,
perform native NetHack recovery only on a preserved working copy, retaining the
originals. Do not silently roll back a newer run or install an older backend;
resolve the intended run/compatibility before applying the staged recovery.


## Initial verified baseline

The baseline archive is `Backups/NetHackSaves/20261101T075321.151456Z.zip`.
It contains 1,023 files, including all existing player sessions, their pointer
and the matching runtime. A complete verified recovery was staged under
`Backups/RecoveredNetHack/Baseline-20261101T075321`; live saves/runtime were
rechecked against the archive and remained unchanged. No player game was
launched or advanced. Four safety tests pass in `Tests/SaveBackup.py`: round-trip
integrity/hidden files, overwrite refusal, corrupt-backup rejection before
extraction, and active-backend refusal.

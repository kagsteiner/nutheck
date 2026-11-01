# Player saves are valuable

The user's instruction of 2026-10-31 supersedes all earlier permission to reset
or replace development saves. This is now their actual NetHack installation.

- Preserve `Saved/NetHack`, its `LastSession.txt`, all session/save/level/lock
  files and configuration. Never delete, reset, overwrite or resume the user's
  played session for testing. Do not kill a running player backend.
- Before work that could affect saves, startup/shutdown, native gameplay,
  compatibility or backend replacement, run `Scripts/BackupNetHackSaves.ps1`.
  It refuses a live backend and verifies every archived file. If the player is
  running, continue independent work and arrange a normal save/exit before any
  dependent mutation. Do not force-close the game to obtain a backup.
- Keep tests in fresh isolated roots, without changing the player session
  pointer. Never use `-NewGame` for a normal player launch unless requested.
- Recovery starts by preserving the current files, verifying a chosen backup,
  and extracting into a new recovery directory. Keep originals and snapshots;
  never silently replace a newer run with an older one or restore an older
  backend over the current installation. See `Docs/SaveProtection.md`.
- Backups live outside `Saved`, under `Backups/NetHackSaves`. Do not prune them
  or delete them as build cleanup. Ordinary art work needs no save mutation.

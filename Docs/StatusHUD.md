# Complete native status and prominent health

The lower bar now presents the full enabled NetHack status field set instead
of a hand-selected HP/AC/level subset. Identity/rank, all six attributes,
alignment, location, gold, current/max power, AC, experience level and the
native turn counter appear beside the health panel. Native hunger, burden
and every active native condition are retained. Polymorph uses the native
monster title, monster HP and HD instead of the ordinary experience display.

Optional native fields (experience points, score, weapon, armor, terrain and
version) follow NetHack's own enabled-field flags. The installed native build
does not compile `SCORE_ON_BOTL`; its score field is therefore disabled even
when requested in configuration. No score is invented or calculated in Unreal.
Player configuration files are not rewritten to toggle these preferences.

## Health and hunger

Current/max HP has its own large bold type, numeric value, coloured accent and
health bar. The bold font is rasterized at its target size for crisp digits.

- Above 50%: green.
- At or below 50%: yellow.
- At or below 25%: red.

The numbers remain visible independently of colour. Hunger is always labelled
in the same panel. Native blank hunger (the ordinary not-hungry state) appears
as **Normal**; Hungry/Satiated use yellow, and Weak/Fainting and other severe
native hunger states use red. No hidden numeric nutrition value is exposed.
Fatal conditions such as Stone, Slime and Strngl are red in the condition row.

## Layout and native data

Status words wrap rather than truncating a field or condition list. The footer
grows for crowded status combinations, with its measured height excluding that
whole area from map clicks. Three recent message lines and the control legend
remain separate from the status values. Camera, movement and native rules are
unchanged.

The window port copies values from `win_status_update`, native enable/format
metadata and native condition masks. Each `BL_FLUSH`/`BL_RESET` emits a complete
protocol-1 `status` snapshot with 27 fields and the ordered active condition
names. The frontend replaces the whole snapshot, preventing cleared or disabled
fields from lingering. Currency escapes are decoded by NetHack. Strength forms
such as `18/**` stay strings. No frontend derivation of attributes, encumbrance,
hunger, rank, branch location or conditions is used.

Sources: `Patches/NetHack/win/ue/winue.c`, `NetHackSession.{h,cpp}`,
`DungeonStatusHUD.cpp`, `DungeonLive.cpp` and `DungeonMouseTravel.cpp`.

## Verification

- Editor and native backend builds pass.
- `Tests/BridgeStatusHUD.py`: 27 native fields; real blindness set/clear; actual
  Normal → Hungry → Weak transitions; Overloaded burden; controlled giant-ant
  polymorph with native HD/XP enable changes and HP matching native state.
- `Scripts/VerifyStatusHUD.ps1`: normal/warning/critical captures and crowded
  status fixtures down to 640×480. Measured words and health digits stay within
  their bounds, and map-picking regression checks pass with the larger footer.
- `Tests/BridgeBackendCompatibility.py`: a fresh isolated save created by the
  prior backed-up runtime restores and advances with the updated runtime.
  `Tests/BridgeLifecycle.py` also passes normal save/resume.
- Captures below use real isolated game views. Warning/critical/stress values
  are explicit renderer-only fixtures; they never modify the game or player saves.

[Normal](Images/StatusHUD/normal-1600x900.png) ·
[Low HP / Weak](Images/StatusHUD/critical-1600x900.png) ·
[Crowded 640×480](Images/StatusHUD/stress-640x480.png) ·
[Verification](Images/StatusHUD/verification.json)

Pre-update snapshot: `Backups/NetHackSaves/20261102T075209.966214Z.zip`.
All verification uses fresh isolated roots. No played session is resumed,
advanced or stopped for testing.

The final preservation audit confirms all 1,068 played-session files and their
complete file set, including `LastSession.txt`, match the pre-update snapshot.
Only `Runtime/NetHackBridge.exe` changed. A verified post-update snapshot pairs
the untouched saves with the new runtime at
`Backups/NetHackSaves/20261102T081208.519701Z.zip`.

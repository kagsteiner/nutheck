# Native mouse travel

In overview, hover over a known square to see its turquoise floor outline.
Left-click and release on the same square to travel there. The selection is
projected onto the floor plane, independently of walls, and works at rotated
and tilted overview angles. The outline shows the selected destination before
the click is submitted, including when a tall wall covers the floor.

Travel is NetHack's existing `#travel`, with its own pathfinding, turn costs,
hazard handling, interruptions and remembered destination. Nothing in Unreal
plans a route or emits a sequence of movement keys. `#retravel` remains native.
Known means seen/remembered terrain; the hero need not have stood on the square.
Unknown cells, walls, off-map positions, HUD areas, prompts and ended sessions
are excluded from this mouse control. Native travel decides whether an eligible
destination is reachable. Selecting the hero's current square spends no turn.

Moving the mouse more than six pixels while holding right cancels the click,
as does losing window focus. Press and release are handled as input events so
a short click between rendered frames still works. Right-drag camera orbit,
middle-drag pan and first-person right-drag look retain their existing roles.
Left-click travel is available in overview only.

## Bridge

The protocol-1 hello event adds `mouse_travel: true`. At a command prompt,
`travel X Y` uses zero-based presentation coordinates. The window port resolves
the currently bound native travel key and supplies one mouse coordinate event
only to travel's `getpos` picker. Native X is presentation X plus one. Invalid
coordinates/payloads are cancelled without movement. If travel is unbound, the
port reports that a native key binding is needed; keyboard `#travel` remains
available. No player configuration is rewritten.

This explicit travel action avoids the generic native mouse action's contextual
drink/loot/open/kick behaviour. The native travel command itself retains all
its normal rules. An older bridge without the capability simply leaves mouse
travel disabled. Save structures, version and game rules are unchanged.

Canonical bridge source: `Patches/NetHack/win/ue/winue.c`; matching build copy:
`upstream/NetHack/win/ue/winue.c`. Frontend integration is in
`DungeonMouseTravel.cpp`, `DungeonLive.cpp` and `NetHackSession.cpp`.

## Verification

- Editor and native backend builds passed.
- `Tests/BridgeMouseTravel.py` uses fresh isolated wizard roots and native Lua
  level fixtures. Mouse and keyboard travel both take a 22-turn detour around
  a five-square-thick wall to the same destination. Both stop after one turn
  beside an awake hostile. Invalid destinations and selecting the current
  square spend no turns. No fixture touches the played installation's sessions.
- `Scripts/VerifyMouseTravel.ps1` checks project/deproject picking with real
  camera components at three pitches and four headings, HUD/bounds/prompt/
  first-person rejection, drag cancellation and focus-loss cancellation.
  Native turn and sequence are unchanged. Live/default-tile/zoom checks pass.
- `Scripts/VerifyPresentationControls.ps1` passes the existing camera orbit,
  first-person, label and native-turn regression checks.
- `Tests/BridgeBackendCompatibility.py` creates a save using the backed-up
  previous runtime in a fresh test directory, then restores and advances it
  using the updated runtime. `Tests/BridgeLifecycle.py` also passes save/resume.
- Logs: `build-mouse-travel-{bridge,unreal,native-tests,live,compatibility,lifecycle}.log`
  and `build-presentation-controls-live.log`.

Before modification, saves/runtime were verified in
`Backups/NetHackSaves/20261101T223834.724795Z.zip`. All 1,069 player files,
their complete file set and `LastSession.txt` remain unchanged. Only the native
bridge executable changed among runtime files. No played session was resumed,
advanced or stopped. [Preservation and test evidence](Images/MouseTravel/verification.json).

## Mouse button revision (2026-11-02)

Following player feedback, left-click is now the primary travel action and
right-drag orbits the overview. First-person right-drag remains look, and
middle-drag remains pan. The HUD and control reference use these bindings.
Both gameplay mouse buttons held together suppress travel and overview orbit,
so releasing one after another does not turn a camera gesture into a move.
Native travel and the native backend are unchanged by this binding revision.

Editor build (`build-mouse-button-swap-unreal.log`) and isolated mouse-travel /
presentation checks pass. All 1,078 player/runtime files and the full file set
match the verified pre-change backup, including the player session pointer.
[Button-swap verification](Images/MouseTravel/ButtonSwapVerification.json).

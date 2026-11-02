# Level peek and readable stairs

## F6: reversible level overview

F6 is unused elsewhere in the project's input handling/configuration. It now
toggles a full-level peek from the zoomed overview. Press again to restore the
previous zoom factor, camera angle, panned focus and follow setting. It sends
no command to NetHack and spends no turn. The header shows **F6 Level** or
**F6 Back**. F5 remains the unconditional framing/angle reset and clears the
peek bookmark.

F6 does nothing at full-level zoom if there is no saved close-up. It is an
overview control; first-person entry from a peek first restores the saved
overview, then follows the existing eye transition. If the dungeon level
changes while peeking, returning restores the zoom/angle and follows the hero
instead of restoring a pan location belonging to the prior map. Camera state
is in-memory and is not written to native saves.

Full-level framing now reserves space for the actual status footer, so the
bottom of the map does not disappear behind the larger health/status panel.
Zoomed room framing is preserved.

## Stair direction

- **Up:** a raised five-step pale stone flight with contrasting tread edges reaching a stone portal near
  the unchanged full wall height. It ascends away from the default camera.
- **Down:** the floor tile is omitted over a dark recessed well. Seven
  trapezoidal spiral treads rotate, shrink, descend and darken into its centre,
  framed by a stone ring. The deepest tread vanishes against the foundation.
  The backing remains within the existing dungeon base; this is a compact
  board-scale stairwell rather than a second rendered dungeon level.
- At **1–2× zoom**, fixed-size **< UP** / **> DOWN** badges identify known
  stairs even behind foreground walls. Nearby badges stack with short leader
  lines; they avoid the HUD and entity labels. They remain visible when F7 hides
  entity glyphs. Close-up and first-person views show the geometry without these
  badges.

Both creature styles and remembered stairs use the same geometry, with the
existing dim memory materials/lighting. Source is the native displayed `up`/
`down` terrain (including the previously grouped ladder/branch variants).
Unknown cells do not acquire a stair model or marker. No destination, unseen
stair or other hidden level information is queried. Native < / > commands,
travel, collisions and rules remain authoritative. Walls are not lowered.

The wedge is a small runtime static mesh built from MeshDescription data; all
other parts reuse instanced basic meshes. No imported art asset is replaced.

## Verification

`Scripts/VerifyNavigation.ps1` builds two fresh isolated live captures. Explicit
renderer-only up/down fixtures demonstrate both presentations without changing
native cells or the played session. The checks cover:

- 18 real-camera F6 round trips across three zooms, three tilts and both follow
  states, restoring zoom, orientation, width and panned/follow focus exactly.
- F5 bookmark cancellation, no-op full-level presses and first-person entry.
- Both stair directions, remembered/current materials and both F9 styles;
  geometry stays inside the cell and has no gameplay collision. Raised stairs
  reach above 100 cm; the well/treads descend below the floor. Removing the
  down-stair floor is checked independently against the floor instance count.
- Unchanged native cells, turn and input sequence. Existing presentation-control
  regression checks also pass.

[Close-up](Images/Navigation/close.png) · [Level peek](Images/Navigation/wide.png) ·
[Preservation and verification](Images/Navigation/verification.json).

Logs: `build-navigation-{unreal,close,wide}.log` and
`build-presentation-controls-live.log`.

The verified pre-change save/runtime snapshot is
`Backups/NetHackSaves/20261102T085701.590664Z.zip`. Tests use fresh capture roots
and do not resume, advance or stop a played session.

The final preservation audit verifies all 1,078 player/runtime files and their
complete file set still match the pre-change archive, including
`LastSession.txt`. The native runtime was not rebuilt or replaced.

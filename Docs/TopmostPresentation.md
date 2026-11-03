# Strict topmost presentation

Implemented 2026-11-03 at the user's request. Native NetHack's displayed foreground wins: render one item, creature or effect above a neutral floor, suppressing background feature geometry. The hero also hides the feature beneath them. The rule covers modelled items, fallback tiles and named artifacts equally. There is no physical pile, stack-height calculation, surface anchor or altar exception. Ten dropped objects or a polypile of a hundred still provide only the native top displayed object to the renderer.

When the native foreground clears, the known terrain feature reappears. The underlying native cell is preserved for navigation, rules and memory. Unknown cells remain unknown. No hidden pile contents are inspected, and artifact-name eligibility is unchanged. A known named weapon retains its existing hover pose; an altar beneath it is hidden. The user's idea of an altar with a named weapon hovering above it is recorded as a possible future artistic direction, not implemented as an exception.

## Implementation

`Source/NUthEck/DungeonTopmost.h` provides `TopmostRenderCell`, a render-only copy which substitutes neutral floor terrain for a known foreground or hero cell. `DungeonLive.cpp` uses it before choosing terrain geometry; this also supplies the missing floor beneath an occupied downstairs cell. Original `Session->Cells` are not altered by normal rendering. Existing displayed-object, creature and tile-fallback selection continues to consume the same native foreground metadata.

The policy suppresses all five altar presentations, fountains, sinks, stairs, traps, doors, water/lava surface geometry and occupied walls. The remaining floor uses the normal visible/memory or Mines material treatment. Wall mortar connections, Mines rock adjacency and decorative wall-light rendering use the displayed terrain where applicable, avoiding leftover geometry attached to a suppressed wall. Native illumination flags continue to determine illumination. `VerifyMines` counts the presented surfaces rather than hidden native features.

The change is entirely in Unreal presentation. The NetHack bridge, protocol, save format and installed backend are unchanged. There is no new gameplay RNG or native command.

## Verification

`DungeonTopmost.cpp::VerifyTopmostPresentation` exercises the real `RebuildLiveMap` path using explicitly synthetic in-memory cells in an isolated capture session. It saves and restores the original cell array, hero, Mines flags, preview map and style. The checks compare actual instanced-mesh batch populations against each foreground on an ordinary floor, rather than checking just a policy flag.

The 840 cases cover:

- 15 background types: five altars, fountain, sink, upstairs/downstairs, trap, open/closed door, water, lava and wall.
- Seven foreground cases: modelled dagger, known Mjollnir, unsupported item using official tile fallback, hero, modelled monster, pet fallback and effect fallback.
- Visible and remembered cells; both F9 styles; regular dungeon and Mines rendering.
- Every background first produces a distinct feature presentation; foreground suppression must match the same foreground over neutral floor exactly. Removing the foreground must restore the original feature batch population.
- The dagger/Mjollnir cases require exactly one corresponding object instance. Native terrain strings remain unchanged; style, native turn and event sequence must be restored/unchanged.

Evidence:

- `build-topmost-unreal.log`: Unreal Development build succeeds.
- `Scripts/VerifyTopmostPresentation.ps1`, `build-topmost-live.log`: `TOPMOST_PRESENTATION_CHECK PASS cases=840 native_state_unchanged=1`, plus the existing all-32-object placement checks and live/zoom/default-tile checks.
- `Art/ObjectInterpretations/Topmost-Unreal.png`: opened and inspected real Unreal capture. The three **synthetic** render fixtures are an uncovered lawful altar, a dagger over altar terrain, and known Mjollnir over altar terrain. Only the first altar is visible; the other cells show their foreground weapons above neutral floor. This is render-layer evidence, not a claim that the fixture objects were spawned by native gameplay.
- `Scripts/AuditTopmostSaves.py`, `build-topmost-save-audit.log`, `Art/ObjectInterpretations/topmost-save-preservation.json`: full file-set, size and SHA-256 comparison against verified pre-change archive `Backups/NetHackSaves/20261103T073300.639492Z.zip`. All 1,081 player files (including LastSession pointer) and all nine backend/runtime files are unchanged. No played session was launched or advanced. No backend replacement occurred, so old/new-backend compatibility testing is unnecessary for this renderer-only change.

The development backlog records implementation and automated verification while leaving human visual testing pending. Earlier asset finishing/LOD work remains separate.

![Strict topmost rendering — synthetic fixtures](../Art/ObjectInterpretations/Topmost-Unreal.png)

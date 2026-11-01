# Framed, side-hinged doors

Live open and closed doors now share a timber frame with two jambs and a
lintel reaching the existing 120 cm wall top. The panel has planks, cross braces,
hinges and a knob. Opening places the leaf at 90 degrees about its side hinge,
along the edge of the passage. The middle of the frame stays empty.

The same assembly follows both native doorway orientations and both creature
styles. Remembered doors use the existing dim memory lighting/material scheme.
This is static presentation of native displayed open/closed state; opening,
movement, collision rules, visibility, locks and traps remain native NetHack
decisions. No hidden door properties are represented. High walls and the
accepted 0.75 floor tint are preserved.

Implementation: `Source/NUthEck/DungeonDoors.cpp`; existing instanced cube meshes
and materials, without new imported assets or changes to the creature inventory.

Editor build and `Scripts/VerifyDoorFrames.ps1` pass. Geometric checks cover
open/closed, both orientations, visible/remembered and both F9 styles: the fixed
hinge is preserved, a 40 cm central corridor is clear when open and blocked when
closed, and all parts remain between floor and wall top. F9 verification leaves
native turn/sequence unchanged. Live/default-tile/zoom checks pass too.

- [Overhead capture](Images/DoorFrames/Live.png): open/closed preview fixtures
  placed on visible floor cells in an isolated native session.
- [Save preservation audit](Images/DoorFrames/verification.json).
- Logs: `build-door-frames-unreal.log`, `build-door-frames-live.log`.

Before testing, the verified backup was
`Backups/NetHackSaves/20261101T144719.440849Z.zip`. All 1,076 player/runtime files
and the complete file set still match it, including `LastSession.txt`. Testing
used fresh `Saved/NetHackCaptures` sessions. No played session was resumed or
stopped.

The accepted floor change was committed separately as `eb3d4db`.

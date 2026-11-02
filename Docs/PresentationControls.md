# Entity labels and first-person camera

Implemented for the user's request before continuing creature generation.

## Controls

- **F6** temporarily shows the whole level; press again to restore the prior
  zoom, angle and pan/follow state. **F5** still resets unconditionally.
  See [level peek and readable stairs](NavigationReadability.md).
- **Right-drag in overview** tilts the camera with vertical movement and rotates
  around the dungeon's vertical axis with horizontal movement. There is no roll.
  Dragging upward gives a steeper overhead view; downward gives a shallower view.
  Tilt stays 20–85 degrees below the horizon, at 0.25 degrees per mouse pixel.
  Rotation uses the current view focus, at both full-level and room zoom.
  Middle-drag still pans. The selected angle survives zooming (including 1x),
  following, panning and first-person entry/exit. **F5** resets angle and framing.
  Releasing the button or losing window focus ends the gesture. Prompts and the
  session-ended panel do not rotate the camera; their controls remain usable.
  Angle is an in-memory preference for the current app launch.

- **F7** toggles all existing floating entity glyphs and their background badges
  (hero, pets and monsters). Labels start visible on a fresh launch. The setting
  stays in effect across camera changes, map rebuilds and creature-style changes.
  Menus, messages, status text and the targeting cursor remain usable.
- **Ctrl+F** enters/leaves first person over .8 seconds. Entry follows the most
  recent actual movement direction, or the last right-drag look direction if the
  player looked around more recently. With no movement/look history, the default
  is north. The former first-entry longest-corridor override has been removed.
- **Escape** also leaves first person, including during entry, without sending
  a cancel command to NetHack. In the overview it retains normal prompt/menu cancellation.
- **Left-click in overview** invokes native travel to the highlighted known
  square. [Mouse travel](MouseTravel.md) describes selection, native behaviour
  and verification.
- **Right-drag** looks around once entry settles. Movement retains map directions
  and faces actual travel. Exit restores the prior zoom, focus and follow state.
  **F5** still returns directly to the full-level overview.

F7 was unused in the project input handling and configuration. It groups the
presentation controls beside F8 (follow) and F9 (creature style), leaves NetHack's
letter commands available, and avoids the configured F11 fullscreen binding.
The toggle is handled before game/menu input dispatch and sends no command to
NetHack. It changes drawing only, without changing displayed identities or
revealing hidden entities. It is an in-memory presentation preference, not a
new persistent settings system.

## Camera curve

`Source/NUthEck/DungeonCameraTransition.h` defines a quartic Bezier dolly:

`B(t) = (1-t)^4 P0 + 4(1-t)^3 t P1 + 6(1-t)^2 t^2 P2 + 4(1-t)t^3 P3 + t^4 P4`.

`P0` is the overview position at equivalent perspective scale. `P1` continues
along the overview forward axis. `P4` is the hero's eye position, 80cm above the
tile. `P3 = P4 - d * lookForward` and `P2 = P4 - 2d * lookForward`. Therefore
`B'(1) = 4d * lookForward` and `B''(1) = 0`: the camera arrives from behind the
player's eyes along exactly the direction they are looking, with zero curvature
at arrival. The extra control point eliminates a small sideways hook seen in the
far-panned, steep-upward diagnostic. It no longer slides directly from a fixed
diagonal overview angle to the eye position.

Smoothstep remaps the .8-second blend for gentle starts/stops. Exiting traverses
the same path backward; reversing midway retains the current blend and pose.
Yaw follows its shortest arc, pitch blends to the current look pitch, and roll
stays zero to avoid banking the horizon. Looking upward shortens the final
approach as needed to keep the Bezier control hull above the flat dungeon floor.
The initial lead is also limited for far-panned views.
The existing orthographic overview/perspective eye modes are retained. This is
a camera path, not a new wall-collision or hidden-cell rendering system.

Actual direction comes from the existing movement/mouse-look tracking, without
accessing hidden monster state. Creature meshes and their generation inventory
are unchanged.

## Verification and artifacts

- `build-presentation-controls-unreal.log`: editor build succeeded.
- `Scripts/VerifyPresentationControls.ps1` runs a throwaway native game, includes
  the existing batch11 displayed-identity/material/fallback/F9 checks, and checks
  the new controls using real camera components and timed entry/exit captures.
- `build-presentation-controls-live.log`: `PRESENTATION_CONTROLS_CHECK PASS`,
  `DUNGEON_FIRST_PERSON_CHECK PASS`, `CREATURE_BATCH11_CHECK PASS` and
  `NETHACK_LIVE_CHECK PASS`.
- 240 curve cases cover eight headings, five pitches (-70, -35, 0, 40, 70 degrees),
  three zoom levels (1x, 3x, 8x), and both hero-centred and far-panned origins. Checks cover start/end positions, first/final
  tangents, finite samples, floor clearance and zero roll. Eight real-camera
  heading checks verify facing retention on entry and continuous mid-transition
  reversal and restoration of a panned focus with following disabled. F7 toggles
  both ways with turn and native sequence unchanged.
- The final real timed entry/exit/re-entry preserved zoom/focus/follow and
  restored the overhead mode. The final camera matched the hero's eye position
  and look direction. Native turn remained **5**; the control check also retained
  native sequence **7**.
- `Docs/Images/PresentationControls/` contains actual paired labels-on/off,
  entry midpoint, eye endpoint, exit midpoint and restored-view engine captures.
  These have been visually inspected. `LabelsComparison.png` assembles the actual
  labels-on/off captures for review.

The original first-person capture command remains supported. The new dedicated
verification additionally waits for texture streaming before its paired label
captures and uses 8x zoom for a clear model view. Synthetic equine fixtures are
presentation-only; they are not native monster spawns.

For unattended model captures, `-HideEntityGlyphs` starts with labels hidden.
F7 still toggles them, and ordinary launches retain labels-on by default. Batch 12
verifies this launch state and supplies a clear three-unicorn engine capture.

## Overview drag verification (2026-11-01)

`build-camera-orbit-unreal.log` and the expanded presentation suite pass. The
same drag handler used by the viewport is exercised against real camera
components: isolated horizontal/vertical motion, tilt limits, zero roll,
release/restart without cursor jumps, full-level zoom retaining the angle and
F5 restoring the default. The existing eight-heading first-person checks now
also verify return to a custom overview angle. Native turn and sequence remain
unchanged. These are automated gesture/camera checks, not a manual mouse test.

Save/runtime preservation was checked against the verified backup
`Backups/NetHackSaves/20261101T223018.872149Z.zip`: all 1,078 files and the complete
file set, including the player session pointer, match. Tests used fresh isolated
capture sessions. [Audit](Images/PresentationControls/CameraOrbitVerification.json).

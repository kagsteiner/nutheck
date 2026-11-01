# Live NetHack integration

The Unreal actor starts an isolated NetHack 5.0.0 process and polls its
standard-output pipe on the game thread. NetHack blocks on input in its own
process; it never blocks Unreal's rendering thread. No TCP service or
external account is involved.

## Data boundary

The new `ue` window port exports glyphs from `print_glyph`, text/messages,
menus, cursor updates, and the hero's own status and current visibility mask.
It does not export the underlying level terrain array, monster list,
undiscovered traps, secret-door flags, or true identities of unknown items.
Terrain categories and door orientation are derived from display glyphs.
Unexplored cells produce no dungeon geometry; remembered cells are dimmed.

An entity on a cell with no usable terrain glyph is drawn over the last
displayed terrain, or a neutral support floor if none was displayed. That
fallback does not consult hidden core terrain. All map dimensions stay
fixed at the full drawable grid so exploration does not change the camera.

Generic meshes represent terrain, features, creatures, and objects. These
are not yet individual models for every NetHack species or object. Labels
use the displayed glyph's character, preserving the game's apparent
identity (including the effects of hallucination).

Glyph badges use a larger base font and scale in direct proportion to camera
zoom. Their background padding scales with the text. Each glyph is measured
so the badge stays centred above its piece without assuming fixed character
dimensions.

## Protocol version 1

Output consists of newline-delimited JSON events:

- `hello`: protocol version and grid dimensions.
- `clear`: clear the displayed map before a redraw or level transition.
- `tile`: drawable x/y, foreground glyph, semantic kind, displayed terrain,
  displayed character, and displayed door orientation.
- `state`: hero position, turn, HP, AC, experience level, depth, branch id,
  and a row-major visibility mask. Status is the hero's own information.
- `message`: messages and raw startup diagnostics.
- `menu`: ordered entries with opaque backend indices, accelerators, group
  accelerators, selection flags, and text.
- `cursor`: the core's map cursor position.
- `input`: a sequence number, input type, and prompt text.
- `end`: the game window port has finished.

Replies are `sequence<TAB>payload<NEWLINE>`. Key/direction/question payloads
are numeric character codes. Line-input payloads contain ASCII text.
Menu payloads contain comma-separated `index:count` pairs; `-1` cancels.
The backend retains all actual NetHack menu identifiers and translates
these indices back into the requested native menu result.

Input types distinguish top-level commands, directions, map targeting,
single-key queries, yes/no questions, text entry, menus, and continuation
prompts. This distinction is essential: a direction request is not another
turn and must not be interpreted as one by automation or the renderer.

## Lifecycle

The helper uses an explicit writable session root under the project's
`Saved/NetHack/` folder. NetHack's own files remain separate from the native
Windows installation's configuration and saved games. The last normal
session id is remembered; a normal launch restores its save when available.
F2 after game end starts a new session. Automated captures use throwaway
session ids without replacing the normal last-session pointer.

Ending Play or closing Unreal closes the helper's input pipe. The helper
then uses the core's `end_of_input` path to save, clear locks, and exit.
Unreal drains any remaining output during a bounded shutdown wait and
releases all process and pipe handles. A child that does not exit within
that wait is terminated to avoid leaving an orphan simulation.

## Validation

The native bridge and Unreal editor module were compiled locally. Real
generated-level integration tests verified movement and turn advancement,
exploration beyond the initial room, inventory and text prompts, a door
changing from closed to open, item pickup, and a non-pet creature appearing.
The final recorded successful gameplay run advanced to turn 12 and expanded
known cells from 25 to 37 while satisfying all gameplay gates
(`build-bridge-gameplay.log`). An earlier longer run reached turn 243.

The lifecycle test closed stdin, observed exit code 0, restored the same
hero position, HP and turn in the same session, and advanced another turn
(`build-bridge-lifecycle.log`).

The actual Unreal window was also checked with native keyboard input:
character randomization and confirmation, an arrow-key move from turn 1
to turn 2, inventory opening/cancellation, and the open-door direction
prompt/cancellation. These checks returned to live play without advancing
a turn for cancelled menus or prompts.

The final 1600 by 900 Unreal capture passed both the full-board framing
check and live-state check at turn 12. The image was inspected and is
retained at `Docs/Images/LiveDungeon-1600x900.png`; its log is
`build-unreal-live-1600x900.log`. It shows the explored starting room,
unexplored board area, hero/pet labels, current HP, and real combat messages.

The full static visual study remains available with `-StaticStudy`.
After the live integration, it was also launched at 1200 by 800 and passed
the full-board framing check with exit code 0
(`build-unreal-static-restored.log`). Its latest image is
`Docs/Images/StaticStudy-1200x800.png`. Earlier static screenshots are retained
under `Docs/Images/`.

## Zoom and keyboard layout (2026-10-30)

Ctrl+F toggles an experimental first-person camera with a 0.8-second curved transition.
It uses an 85-degree perspective view at 80 cm above the hero's tile, below the
1.2 m walls. Entry keeps the latest movement or mouse-look direction. A quartic
Bezier dolly finishes with its tangent parallel to that direction; the return
traverses the same curve backward. Yaw/pitch ease without banking the horizon.
Right-mouse dragging looks around; moving faces the direction of
travel. Movement keys retain their map directions. The hero mesh and its own
badge are hidden in this view. The overhead zoom, focus and follow setting are
preserved, and F5 returns directly to the full-level overview. Camera controls
consume no NetHack turns. F7 toggles the floating hero/pet/monster glyphs and
badges without hiding messages, menus or the targeting cursor. Labels start
visible. Ctrl+F overrides NetHack's wizard-only map command.
See [PresentationControls.md](PresentationControls.md) for the curve, key choice
and verified 240-case camera coverage.
Modifier keys are tracked in input-event order and reset on loss of focus so
chords delivered within a single frame are recognized reliably.
The existing known-tile renderer is retained, so there are no ceilings or newly
revealed cells in this experiment.

`Scripts/LaunchPrototype.ps1 -FirstPersonCapture` exercises the toggle, verifies
return to the previous camera state and unchanged turn count, then captures the
eye-level view. Evidence: `build-unreal-first-person.log` and
`Docs/Images/FirstPersonDungeon-1600x900.png`.

Mouse-wheel zoom ranges from 1x to 8x. The view follows the hero when
zoomed; middle-mouse dragging pans and suspends following. F8 resumes hero
following, and F5 restores the full-level view. The wheel scrolls an open
menu rather than changing the camera. Zoom and pan do not send game input
or spend turns.

Printable input is delivered through a custom `UGameViewportClient` using
Windows character events. It no longer synthesizes US shifted punctuation
from physical key names. This keeps `:` distinct from the descend command
`>` on a German keyboard. Numpad-generated text is suppressed after its
movement event to avoid duplicate commands; ordinary number-row characters
still arrive through the active layout. UE's console hotkeys are disabled
so they do not intercept playable punctuation.

The camera uses the current zoom/pan focus as its orthographic view target.
The camera manager does not replace that focus with the board actor's
origin. A live capture verified 2.986x magnification, the expected camera
width, and hero projection at the viewport centre (800,450) at 1600x900.
The inspected image is `Docs/Images/ZoomedDungeon-1600x900.png` and its
verification log is `build-unreal-zoom.log`.

The live German-layout regression check sent Shift+Period through the
actual window. It logged character code 58, displayed "There is a doorway
here.", and remained at dungeon level 2, turn 124. Inventory and wheel
context were also checked without advancing the turn. The log is
`build-unreal-input-layout.log`.

The final build also passed live wheel zoom and F5 reset without changing
Unreal's render mode, followed by another character-code-58 check at the
same turn (`build-unreal-input-final.log`). Project debug exec bindings
are cleared so Unreal's view-mode shortcuts cannot consume NetHack/camera
controls.

## Current limits

This is the first live presentation milestone. Meshes are placeholders,
the status strip shows essential values rather than NetHack's full status
field set, and game commands are keyboard-based. ASCII text input follows
the active Windows keyboard layout. Non-ASCII text entry, mouse targeting,
animation, sound, and
individual Blender assets remain subsequent increments. This is an editor
project and staged native helper, not yet a packaged Unreal release.


## Object appearance mapping (2026-10-31)

The tile event optionally includes `display_object` for displayed large box,
chest and gold-piece glyphs, including normal and pile-top forms. These are
non-shuffled appearances whitelisted by `glyph_to_obj`; hidden objects,
contents, stack quantity and lock/trap state are never consulted/exported.
The parser clears the field on every tile replacement. Individual object meshes
now replace the generic sphere for these types in either creature style;
remembered items use dim wood/metal materials. Unsupported items keep spheres.
Native wish/drop/reveal checks and existing bridge smoke pass. Live mapping,
visible/memory materials, fallbacks, no-turn/no-sequence F9 switching, map and
8x zoom pass. See [Object batch 1](ObjectBatch1.md).


## Official tile fallback (2026-10-31)

`tile` events now include `tile_index` from the foreground glyph's native
resolved `gm.tileidx`. The bridge compiles generated `tile.c` and enables
`TILES_IN_GLYPHMAP`, so shuffled unidentified appearances and restored games use
NetHack's own tile mapping. There is no hidden object/monster lookup. Missing
3D entity models now use transparent camera-facing official tile cards, including
remembered dimming and first-person hero hiding. Existing 3D model selection and
terrain rendering stay intact. See [implementation and evidence](TileFallback.md).

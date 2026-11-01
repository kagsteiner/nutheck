# Default tiles and the early dungeon

The official NetHack 5.0 tileset is the canonical reference for this iteration.
Alternative tilesets require a concrete reason. The early main dungeon uses
regular neutral grey worked stone and NetHack's actual generated room/corridor
layout. The separate miniature-room studies remain reference experiments.

## Actual live integration

The normal live renderer now uses Blender-exported regular grey floor and wall
modules. It draws only tiles received from the core's display interface, keeping
the existing exploration/memory behaviour. One gameplay cell remains one metre;
the full 79x21 level framing, zoom, glyph badges and first-person toggle remain.

The bridge emits optional `display_monster` and `female` fields for a monster
display glyph. They are resolved using `glyph_to_mon` and the glyph's sex flags.
No lookup of the hidden monster on that square is performed. Mimics displaying
an item keep their item appearance. Hallucinated monster display glyphs map to
their apparent form. Invisible-marker glyphs carry no species identity.

Unreal maps the displayed canonical name and sex to a generated mesh asset,
using a normalised name rather than assuming a numeric glyph/tile-index match.
The source `monsters.txt` labels supply the corresponding asset keys. Existing
assets are reused through mesh batches. Unsupported appearances retain the
previous placeholder and glyph badge. Hero mesh batches are separate so first
person can hide the hero without hiding another creature of the same species.

## The 2D-to-3D experiment

`Scripts/CreateDefaultTileFigures.py` reads the official palette and named tiles
directly from `upstream/NetHack/win/share/monsters.txt`. It creates 76 figures:
male/female variants of all 13 roles and 25 common creatures, including starting
dogs/cats. `Art/DefaultTiles/manifest.json` records each file-local source index,
name, sex, occupied-pixel count, size and conversion method.

The converter:

1. Removes the official background colour.
2. Trims the black drop-shadow fringe to one pixel around nearby coloured
   scanlines, retaining interior black details. This heuristic is recorded in
   the manifest and may need species-specific masks later.
3. Builds a solid cell for each retained pixel, thickening the volume according
   to distance from the silhouette boundary, with lightly bevelled edges.
4. Stores the original palette colours as mesh vertex colours and exports FBX.
5. Imports a shared opaque vertex-colour material into Unreal. Shader-link calls
   are checked for success; the vertex-colour node's combined output is unnamed
   in this engine version. Each imported figure must have a vertex-colour buffer.

These are deliberately **tile-derived volume proxies**, with a retro pixel
surface. They preserve recognisable default-tile imagery and cast actual
real-time shadows, but they are not complete anatomical reconstructions.
The reverse side mirrors the front, depth is inferred, and limbs are not
independently rigged. This is a repeatable fidelity baseline to compare with
future sculpted interpretations. No image-to-3D service or alternate art pack
is involved.

`Art/DefaultTiles/DefaultTileVolumes.blend` is the editable source/gallery;
`DefaultTileVolumes.png` shows representative figures. The official source
tiles and their attribution/licence remain in the upstream distribution.

## Build and run

- `Scripts/BuildPrototype.ps1` now also builds/imports the default tile assets.
- `Scripts/BuildDefaultTiles.ps1` rebuilds the figure meshes, bridge, Unreal
  module and imported assets. `-AssetsOnly` skips bridge/Unreal compilation;
  `-SkipGalleryRender` skips the Blender gallery image.
- `Scripts/LaunchPrototype.ps1 -NewGame` starts a fresh live dungeon.
- `Scripts/LaunchPrototype.ps1 -DefaultTileCapture` creates a disposable game,
  advances four inputs, zooms to about 3x, then checks live map/turn state,
  hero centring, depth one and a loaded hero volume before capturing.
- `Scripts/LaunchPrototype.ps1 -FirstPersonCapture` exercises the in/out camera
  toggle and restoration against the same live renderer.

The Mines and quest environment skins are future work; this iteration establishes
the early dungeon and figure pipeline. Items still use their prior placeholders.

## Validation

The bridge smoke test checks the displayed identity/sex against the character
introduction chosen by character setup, since setup may choose a character
independently of command-line role preferences in this port. It also checks
that terrain/item/unknown events do not expose a monster identity.

The live capture must contain explicit `NETHACK_LIVE_CHECK PASS`,
`DUNGEON_ZOOM_CHECK PASS` and `DEFAULT_TILES_CHECK PASS` markers. Runtime figure
logs report the mesh colour-buffer size/range and its assigned material, helping
distinguish lost colour data from an unconnected material graph.

Validated results for this iteration:

- 76 figure assets and two grey terrain modules imported; figure vertex colours
  were checked by the editor. Import evidence: `build-default-import.log`.
- The shared shader's actual combined vertex-colour connection is checked;
  final shader evidence: `build-default-material.log`.
- The bridge identity/sex/appearance smoke test passed in
  `build-default-protocol-smoke.log`.
- Live depth-one capture passed at 2.986x zoom with a `monk_male` hero volume
  and one pet volume, turn 5 and 80 known cells. Evidence:
  `Saved/Logs/Verification-ac78b9adac264323ab0a89306fb0c0bd.log`.
- First-person entry and restoration passed without advancing a turn, using
  the revised renderer. Evidence:
  `Saved/Logs/Verification-1b48da25cbad46d8b6e4cd385a6f1435.log`.
- Live capture now records whether movement occurred during the sequence;
  returning to the starting square after a short loop is valid movement.

Actual game captures are saved alongside the gallery as `LiveLevelOne.png`
and `LiveFirstPerson.png`. The gallery is a Blender render; those two images
are real Unreal captures of generated levels.

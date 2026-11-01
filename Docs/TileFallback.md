# Official tile fallback

Unsupported creatures, objects, effects and player forms now use their official
displayed tile on a transparent 2D card before the old generic geometry fallback.
Existing selected 3D assets, including the retained tile-volume proxies, keep
priority. The F9 creature-style control is unchanged. The three object models
remain available in either style.

## Rendering

All fallback appearances share one two-triangle quad, one texture atlas and one
masked unlit material. Per-instance data selects the tile and normal/remembered
brightness. The card faces the camera in both orthographic and perspective
views, preserving the tile's proportions on screen. It rotates about the floor
anchor; transparent lower rows are compensated so the lowest visible pixels
stay at floor height. Sprite-based heroes hide during first person and return
afterward. No render-state update is issued when card orientation is unchanged.

The texture uses nearest filtering, no mipmaps and transparent gutters. Only
the official `.` background becomes transparent. Black anatomy, outlines and
the tile's original drawn shadow are preserved as 2D pixels; none becomes
inferred 3D geometry. Cards do not cast additional flat-card shadows. Remembered
sprites use 20% brightness, with the existing visibility boundary retained.

## Correct native mapping

The bridge now builds with NetHack's generated `tile.c` and
`TILES_IN_GLYPHMAP`. It sends optional `tile_index` from the foreground
`glyph_info.gm.tileidx` in each tile event. This is NetHack's resolved displayed
tile, including sex, pet/detected/ridden aliases, pile-top objects, corpses,
statues and shuffled unidentified appearances. No hidden monster/object lookup
or true unidentified name is exported. Tile indices are not guessed from glyph
numbers or file-local object indices.

NetHack's own `shuffle_tiles` updates the mapping for each game's object
appearance shuffle, and re-establishes it on restore. This matters: a potion of
healing can be magenta in one game and brown in another. The sprite must show
the appearance that the player sees. The console still renders its usual
characters; tile mapping is additional presentation metadata, with no save
format or gameplay-rule changes.

The Unreal parser clears `TileIndex` before each tile update. Missing/invalid
metadata or missing fallback assets safely retain the existing generic last
resort. Unknown/unexplored terrain does not acquire a card. Normal terrain
geometry remains unchanged; this fallback concerns entities and effects that
would otherwise receive a generic marker.

## Atlas and editable source

`CreateOfficialTileAtlas.py` reads all official source entries in native order:
789 monster tiles, 483 object tiles, 243 other tiles, then 789 statue variants.
It includes the 17 generic-object entries with intervening source comments.
Statues use the palette remapping in NetHack's `tiletext.c`. The atlas contains
2,304 slots; the current native mapping uses indices through 2,302, while the
last grayscale invisible-monster slot is unused.

The atlas is 960×960: 48×48 cells, each containing 16×16 original pixels with
two transparent gutter pixels on each side. No source pixels are smoothed or
repainted. Generated metadata retains each source label and file-local index.
The generated C++ header records tile count, demo indices and floor padding.
Regenerate/reimport the atlas and rebuild the bridge/module together if the
pinned tileset or native tile mapping changes.

- `Art/TileFallback/OfficialTiles.png`: RGBA atlas.
- `Art/TileFallback/atlas.json`: complete slot/source metadata.
- `Art/TileFallback/TileStandee.blend` / `.fbx`: editable quad and export.
- `Source/NUthEck/OfficialTileAtlas.h`: generated atlas constants/anchors.
- `/Game/TileFallback/T_OfficialTiles`, `M_OfficialTile`, `SM_TileStandee`:
  imported runtime assets.
- `Art/TileFallback/TileFallback-Unreal.png`: inspected live capture.
- `Source/NUthEck/DungeonTileFallback.cpp`: instancing, view facing and checks.

Rebuild using `CreateOfficialTileAtlas.py` with the project Python, then
`CreateTileStandee.py` with Blender background/four threads. Build the bridge
using `BuildNetHackBridge.ps1`, build the editor module, then run full-editor
startup Python `ImportTileFallback.py`. `VerifyTileFallback.ps1` performs the
live verification/capture. No creature/player/object mesh regeneration is needed.

## Verification

Bridge/editor builds and atlas/quad/material import pass. Native bridge smoke
and existing object wish/drop/reveal tests pass. `BridgeTileFallback.py` checks
six potions across two isolated native games: displayed inventory colour agrees
with the tile appearance, and save/restore retains the mapping. In the recorded
run, all six resolved appearances differ from their unshuffled source defaults.

Live checks pass three tile appearances, visible/remembered per-instance values,
two-triangle geometry, invalid metadata rejection and existing object-model
priority. Eight perspective camera headings preserve facing and floor anchors.
A sprite-based hero hides/restores correctly in first person. Two real F9
switches preserve native turn and input sequence. Native movement/map, hero
centring and 8× zoom pass. The actual engine screenshot is inspected; ordinary
wall occlusion still applies.

Evidence: `build-tile-fallback-{bridge,unreal,mesh,import,bridge-smoke,native-objects,native-tiles,live}.log`.
All 41 creature/player exports and the three object exports remain unchanged.
No creature/object draft completion counts increase: these are generic fallback
presentation assets, not reconstructed anatomy or new individual 3D models.

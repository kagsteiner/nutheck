# Dungeon atmosphere

The live renderer uses neutral ambient illumination and warm wall candles.
Ordinary dungeon rooms and corridors have no decorative fog. There is no alternate
appearance mode; use Git to review or revert the experiment.
The shadow-casting directional studio light is limited to art/study fixtures;
only candles cast lighting shadows in live gameplay. The ambient light is a
movable Sky Light supplied with a constant white cubemap, with shadowing and
the black lower hemisphere disabled. It does not capture the level or require
a visible sky. The directional fill and cool room point lights are removed.

Wall stones retain their bevels and shallow masonry joints. Recessed, opaque
mortar cores (93 x 93 x 118.2 cm) back each wall tile, and short connectors close
the seams between cardinally adjacent known wall tiles. These shadow-casting
solids stop candlelight passing through the separated stones. Mortar reaches
1 mm below the stone caps to close the top joints without covering their texture,
while staying recessed behind side faces. Connectors never
cross doors or unknown cells; remembered mortar uses the separate memory
lighting channel. The original stone meshes and candle settings are unchanged.

## Authority and persistence

NetHack still determines sight, illumination, detection, and all gameplay.
The state event includes a 79-by-21 `lighting` string, matching `vision`:
bit 0 means permanent illumination and bit 1 means temporary illumination.
Both bits are zero outside `cansee()`, including while blind. No unseen room
layout, light-source positions, or item identities are exported.

UE does not calculate a lamp's gameplay radius. A warm shadowless accent follows
the native temporarily illuminated visible cells. This is a presentation of
illumination, not identification of its source:
the protocol does not distinguish a lamp from another temporary light source.
Permanently lit cells can also result from magic.

Candles are non-interactive decoration explaining permanent illumination. A
fixed coordinate/level hash chooses wall candidates and their facing. Only
visible wall candidates next to visible, permanently illuminated floor render.
Discovery order and gameplay RNG do not affect their positions. They disappear
outside current sight; remembered map geometry remains subdued. This adds no
native save fields or cosmetic save files.

Local lights affect current geometry on lighting channel 0. Remembered terrain,
objects and fountains use channel 1, excluding candle and temporary accents.
Ambient illumination affects both, with the existing dim memory materials
preserving the distinction between currently visible and remembered geometry.
At overview scale, a soft shadowless map fill affects only remembered geometry
on channel 1. It fades smoothly between 1x and 2.5x zoom and fades away during
entry to first person. This lifts explored rooms and connecting corridors for
navigation without brightening current candle lighting or revealing new cells.
Dynamic global illumination remains disabled: indirect light does not obey
these direct-light channels. Point-light falloff is artistic and never grants
vision. Special perception still uses the existing displayed-glyph system.

The rejected floor-mist experiment and its implementation are documented in
[MistExperiment.md](MistExperiment.md). Fog is reserved as a future possibility
for appropriate environments such as the Castle moat; no such effect is active.

## Build and checks

`BuildPrototype.ps1` builds the bridge and UE module, and generates the candle
flame material with `CreateAtmosphereAssets.py`.

`Tests/BridgeLighting.py` uses a fresh isolated wizard session to check the
lighting mask, a real oil lamp switched on/off, and blindness with the lamp lit.
Normal capture launches now use `Saved/NetHackCaptures`, separate from the player
tree and its LastSession pointer. Overhead and first-person captures exercise
the live renderer. No player session is resumed by these checks.

The experimental backend changes only window-port output, not native save
structures or game rules. Before building/staging it, a verified whole-session
and matching-runtime backup is required as described in SaveProtection.md.

# Dungeon atmosphere

The live renderer uses a soft shadowless fill, warm wall candles, cooler
local fill, and small local fog volumes at floor height. There is no alternate
appearance mode; use Git to review or revert the experiment.
The shadow-casting directional studio light is limited to art/study fixtures;
only local sources cast shadows in live gameplay.

## Authority and persistence

NetHack still determines sight, illumination, detection, and all gameplay.
The state event includes a 79-by-21 `lighting` string, matching `vision`:
bit 0 means permanent illumination and bit 1 means temporary illumination.
Both bits are zero outside `cansee()`, including while blind. No unseen room
layout, light-source positions, or item identities are exported.

UE does not calculate a lamp's gameplay radius. Local fill follows the native
illuminated visible cells. Temporary illumination is warm; permanent fill is
cooler. This is a presentation of illumination, not identification of its source:
the protocol does not distinguish a lamp from another temporary light source.
Permanently lit cells can also result from magic.

Candles are non-interactive decoration explaining permanent illumination. A
fixed coordinate/level hash chooses wall candidates and their facing. Only
visible wall candidates next to visible, permanently illuminated floor render.
Discovery order and gameplay RNG do not affect their positions. They disappear
outside current sight; remembered map geometry remains subdued. This adds no
native save fields or cosmetic save files.

Local lights affect current geometry on lighting channel 0. Remembered terrain,
objects and fountains use channel 1, lit only by the subdued general lights.
Dynamic global illumination remains disabled: indirect light does not obey
these direct-light channels. Point-light falloff is artistic and never grants
vision. Special perception still uses the existing displayed-glyph system.

Fog spheres fit wholly inside visible floor tiles, with most of each sphere
below the floor. They add a faint haze without revealing unexplored geometry.
Lights and fog components are pooled and hidden when no longer needed.

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

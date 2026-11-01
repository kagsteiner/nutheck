# Dungeon atmosphere

The live renderer uses neutral ambient illumination, warm wall candles,
and gently drifting floor mist. There is no alternate
appearance mode; use Git to review or revert the experiment.
The shadow-casting directional studio light is limited to art/study fixtures;
only candles cast lighting shadows in live gameplay. The ambient light is a
movable Sky Light supplied with a constant white cubemap, with shadowing and
the black lower hemisphere disabled. It does not capture the level or require
a visible sky. The directional fill and cool room point lights are removed.

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

Mist uses three translucent layers at 16, 30 and 44 cm above the tile origin.
An animated material combines two scales of procedural world-space noise,
drifting in different directions at a few centimetres per second. The world
pattern stays continuous across tile boundaries while each tile's geometry and
soft edge keep the effect inside currently visible floor cells. Depth fading
softens intersections with models. Surface lighting lets candles tint the wisps;
a small neutral emissive contribution keeps mist readable in ambient light.

This is layered mist, not a simulation of smoke or global volumetric fog.
It adds no particles, gameplay RNG, save data, or native turns. It fades in from
1x to 2.4x zoom, is completely hidden at full overview, and remains in first
person. Existing candle light and native visibility are unchanged. Fog density
does not determine which objects may be displayed.

## Build and checks

`BuildPrototype.ps1` builds the bridge and UE module, and generates the candle
flame and drifting mist materials with `CreateAtmosphereAssets.py`.

`Tests/BridgeLighting.py` uses a fresh isolated wizard session to check the
lighting mask, a real oil lamp switched on/off, and blindness with the lamp lit.
Normal capture launches now use `Saved/NetHackCaptures`, separate from the player
tree and its LastSession pointer. Overhead and first-person captures exercise
the live renderer. No player session is resumed by these checks.
Presentation checks additionally verify mist coverage of visible floor cells,
tile bounds, shadow exclusion and overview/room/first-person opacity. Paired
`Mist-Flow-A.png` and `Mist-Flow-B.png` captures show motion three seconds apart
without advancing the native game.

The experimental backend changes only window-port output, not native save
structures or game rules. Before building/staging it, a verified whole-session
and matching-runtime backup is required as described in SaveProtection.md.

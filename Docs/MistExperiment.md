# Floor mist experiment and future water-side fog

## Decision (2026-11-01)

The player rejected ambient mist in ordinary dungeon rooms: it felt artificial
and did not belong in those environments. Keep the approved candle lighting,
ambient illumination and readable zoomed-out map. Ordinary rooms and corridors
should have no decorative fog, including the earlier near-invisible placeholder.

Fog remains a possible environmental effect for places where it has a physical
reason to exist, especially the Castle's large moat. This is a future idea,
not an instruction to add fog to every water tile or implement it now.

## Preserved implementation

Commit `7f06ee9` contains the complete experiment, including the generated UE
material and its reproducible Python/HLSL source. The approved lighting baseline
is tagged `lighting-baseline-2026-11-01` (commit `d15d5c5`). Inspect the experiment
with `git show 7f06ee9 -- Scripts/CreateAtmosphereAssets.py` and
`git show 7f06ee9 -- Source/NUthEck/DungeonAtmosphere.cpp`.
Do not restore its backend or native saves to revisit this visual technique.

The experiment used three horizontal, translucent plane instances per currently
visible floor tile, at heights of 16, 30 and 44 cm. Planes were exactly one tile
(100 cm) wide, instanced together as `FloorMist`, with no collision or shadows.

`M_DriftingMist` was a two-sided, translucent, surface-forward-lit material.
`Scripts/CreateAtmosphereAssets.py` built its graph and embedded a Custom HLSL
expression. A scalar `MistAmount` controlled its overall visibility.

The shader combined two octaves of smooth value noise, generated procedurally
from hashed lattice corners with cubic interpolation. Coordinates were absolute
world XY divided by 150 cm, so a single noise pattern flowed across all tiles.
The primary drift was `Time * float2(0.035, 0.016)` in noise space (about 5.25 and
2.4 cm per second); a second octave used 2.3 times the spatial frequency and
counter-drift at 0.6 times the speed. Layer height offset the noise phase so the
three layers did not move as a single flat sheet.

Noise weights were 0.65 and 0.35; `smoothstep(0.28, 0.75, noise)` formed wisps.
Opacity was `0.55 * wisps * edge * saturate(1 - worldZ/75) * MistAmount * depthFade`.
Depth fade used a 12 cm distance to soften intersections with models. Base color
was linear RGB (0.72, 0.76, 0.78), emissive (0.10, 0.12, 0.14), roughness 1 and
specular 0. Candles shaded the layers; emission kept them legible in ambient light.
This was layered transparency, not a volumetric smoke or fluid simulation.

## Visibility boundaries and overview

Each plane instance stored one four-bit boundary mask in per-instance custom
data: west/east/south/north boundaries against non-visible or non-floor cells.
A VertexInterpolator carried this into the pixel shader. A 12 cm soft edge was
applied only at those boundaries, never between adjacent visible floor tiles.
This removed internal tile seams while preventing the animated effect from
extending into unseen terrain. No hidden geometry was used for placement.

Mist faded from zero at 1x zoom to full strength at 2.4x via smoothstep. It was
hidden entirely at full overview and blended back in for first person. Motion
used shader time, so it continued while the turn-based game waited for input,
without consuming a turn, gameplay RNG or saved simulation state.

Capture checks verified visible-floor coverage, bounds, no shadow casting,
overview/room/first-person opacity, and unchanged native turn/sequence counters.
Paired `Mist-Flow-A.png` and `Mist-Flow-B.png` captures were taken three seconds
apart with the camera and native game stationary. These diagnostics live under
ignored `Saved/Screenshots`; the source remains in the experiment commit.

## Lessons for a future Castle/moat effect

- Give fog an environmental reason and local scope: low water mist over the moat,
  rather than atmospheric coverage throughout the dungeon.
- Preserve NetHack's authoritative visibility. Fog must not reveal a hidden
  shoreline, moat extent, creature, reflection or unexplored room.
- Anchor the pattern to world space; preserve soft boundaries without tile seams.
- Keep tactical overview clear and small items readable.
- Layered transparency is relatively simple and works in both camera modes, but
  can look like flat sheets at grazing angles and wash out surfaces when dense.
  Evaluate the technique afresh for water; true local volumetric fog is another
  option if it produces a better result within the rendering budget.
- Verify in an isolated session and preserve the player's saves before any build
  or gameplay/backend work. Never resume the player's run to test the effect.

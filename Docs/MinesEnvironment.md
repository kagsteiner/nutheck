# Gnomish Mines: rock caverns and torches

The Mines now have a separate cavern treatment: continuous muted rust-red rock,
a neutral grey-brown gritty floor, and sparse wall-mounted wooden torches.
High walls, native terrain topology, figurines, stairs and the status HUD remain
intact. Minetown retains the existing masonry and candles as the settled setting
for this first pass; mixed natural/constructed areas within town can be refined
separately.

## Surfaces

New `/Game/Mines/M_MinesRock` and `M_MinesFloor` materials use world-space
procedural mineral variation, fine fractures and matte surface relief. They do
not reuse the floor's regular slab joints. Noise continues across cell boundaries
without UV stretching on vertical faces. The floor has only ±1.2 cm of smooth
geometric relief; the rest is surface shading, preserving clear silhouettes and
the native one-metre movement/picking grid. Small rock displacement gives the
walls an uneven surface and crown while preserving their enclosing height.

The rock surface mesh is subdivided for displacement. Shared faces between known
wall neighbours are omitted, while faces against unknown cells remain closed.
Displacement is only a few centimetres and does not change which native cells
are walkable. All new
geometry has no gameplay collision. The existing dungeon limestone textures and
materials are not edited. Cavern components are cleared on map rebuilds, so
leaving the Mines restores the ordinary dungeon treatment.

Rebuild the new materials with `Scripts/CreateMinesMaterials.py` through Unreal
Editor Python. Only the new Mines material assets are written. The shader
generates the textures procedurally; no image-generation service or downloaded
texture is required.

## Fixtures and native lighting

Torch candidates use a stable coordinate/depth seed and a sparse subset of known
walls. Suitable wall faces are selected only against visible, permanently lit
native floor. Fixtures consist of a wood shaft, iron mounting and emissive flame,
with a broader warm light pool and gentle time-based flicker. Native gameplay RNG
and turns are not involved. Minetown and other dungeon levels keep candles.

Cavern lit terrain uses an additional light channel. Torch lights affect that
channel only; unlit and remembered cavern terrain do not receive torch light.
Visible walls can join the lit channel when they border visible native-lit
terrain. Temporary native light uses the lit terrain channel too. Ambient/map
readability is retained, without pretending that a decorative torch changes
NetHack's vision, illumination, monsters or exploration.

The additive `in_mines` and `mines_town` state fields describe only the hero's
current branch/level setting. They come from native `In_mines` and the current
special-level town flag, rather than assuming fixed dungeon numbers. No unseen
level, object or monster data is inspected. The native save format and rules are
unchanged.

## Verification

`Tests/CreateMinesCapture.py` makes disposable wizard saves under
`Saved/NetHackCaptures`, reaches the actual Mines through native level selection,
and uses native light/darkness effects for the two lighting fixtures. Wizard map
revelation is confined to these test saves. Normal launches do not use it.

`Scripts/VerifyMines.ps1` restores those isolated fixtures through a GUID-only
capture flag which is ignored for remembered/player launches. It verifies actual
lit cavern, dark cavern, Minetown and level-scale views, including:

- Exact terrain instance counts against known native cells.
- Both F9 presentation styles without changing native turn or input sequence.
- Torch fixtures supported by visible, permanently lit native floor.
- Separate light channels for current-lit, current-unlit and remembered terrain.
- No torches in the dark fixture; candles/masonry retained in Minetown.
- Live/default-tile checks and no runtime material shader fallbacks.

The normal dungeon's presentation and navigation suites also pass. Isolated
old-runtime save compatibility, native mouse travel and save/resume checks pass.

[Lit cavern](Images/Mines/lit.png) · [Dark cavern](Images/Mines/dark.png) ·
[Minetown](Images/Mines/town.png) · [First person](Images/Mines/eye.png) · [Level view](Images/Mines/wide.png) ·
[Verification](Images/Mines/verification.json).

Pre-change verified backup:
`Backups/NetHackSaves/20261102T122329.845987Z.zip`. Tests never resume, advance or
stop a played session. Save preservation and runtime changes are recorded in the
verification artifact.

The final audit verifies all 1,081 played-session files and their complete file
set, including `LastSession.txt`, against the pre-change snapshot. Only
`Runtime/NetHackBridge.exe` changed among runtime files; the original limestone
PNGs, textures and materials still match their preservation hashes. A verified
post-update snapshot pairs these unchanged saves with the tested backend at
`Backups/NetHackSaves/20261102T132628.524817Z.zip`.

## Exterior-face correction (2026-11-02)

The initial runtime rock mesh used counterclockwise exterior triangles, which
Unreal culled from outside. This made rocks appear hollow and removed their tops
and visible sides. The mesh now emits clockwise triangles while retaining outward
shading normals. Internal shared-face omission is unchanged. The editor rebuild
passed, and isolated lit overhead and first-person captures passed their native
visibility/turn checks and were visually inspected after the correction. No player
backend or played save was used, and no native backend change was required.

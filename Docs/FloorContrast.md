# Darker textured floors

User direction, 2026-11-01: keep the high walls in both overhead and first-person
views. Their enclosed, slightly claustrophobic dungeon feeling is intentional.
Improve floor contrast first; do not substitute lowered/faded/cutaway walls.

Live `Floor` and `FloorMemory` batches now multiply the existing tint RGB by
0.75. This is a 25% reduction of linear material base colour, not a claim that
final screenshot brightness changes by exactly 25% under every light.

The original floor texture and triplanar projection, grain, scale, seams,
roughness, instance variation, lighting and walls are preserved. The wall tint
is unchanged. Remembered floors keep the existing colour/dimming relationship,
with the same extra floor multiplier. The grey fallback is darkened consistently
if the textured material is unavailable. No texture or material asset is edited.

Editor build and the existing isolated live/default-tile/zoom capture checks
pass. The capture was visually reviewed; this is an initial contrast adjustment,
not a claim that wall occlusion or every doorway is now solved.

- [Live view](Images/FloorContrast/DarkerFloors.png)
- [Preservation checks](Images/FloorContrast/verification.json)
- `build-floor-contrast-{unreal,live}.log`

Before the update, player sessions and runtime were verified in
`Backups/NetHackSaves/20261101T140724.870261Z.zip`. The capture used a fresh
`Saved/NetHackCaptures` session. All 1,076 original player/runtime files, the
played file set and session pointer remain unchanged. Original floor/wall PNG,
texture and material asset hashes also match. No played session was launched,
advanced or stopped. The change applies on the next normal app launch.

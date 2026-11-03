# Mjollnir: named hammer design

Update, 2026-11-02: these models are now connected to the live dungeon under the
[MVP placement rules](MVPObjectPlacement.md), with isolated native mapping and
Unreal placement checks passed. Earlier pending-live statements below describe
the original art-only milestone. Finishing and broader edge-case review remain
separate from MVP placement; full-completion checkboxes are unchanged.

Requested 2026-11-02. Editable model: `Art/ObjectInterpretations/Mjollnir.blend`;
painted export: `mjollnir.fbx`. Unreal asset:
`/Game/ArtifactInterpretations/Meshes/SM_mjollnir`.

## Sources and design

NetHack `include/artilist.h:109` defines Mjollnir on `WAR_HAMMER`, neutral and
associated with Valkyrie, with electrical attack. The base hammer is iron
(`include/objects.h:367`). Return/throw behaviour remains native gameplay.

The [forging narrative](https://www.worldhistory.org/article/2785/the-meanings-of-mjolnir/)
describes dwarven makers and a short handle resulting from Loki's interference.
The [Swedish History Museum's iron hammer pendant](https://vikingar.historiska.se/object_details.php?e=no&l=en&object=F807E634-9CE1-48BB-A37C-47AC7C937685)
provides archaeological context for hammer-shaped protective objects; these are
pendants, not surviving full-size mythical weapons or an exact weapon blueprint.

This design uses a short wooden haft, broad forged iron head with flared
striking ends, silver face plates/collars, mirrored gold interlace and a diamond
boss. All surfaces, rear and underside are modelled. The precious fittings,
exact profile and ornament are creative interpretations for exceptional divine
loot. Interlace is ornament, not a fabricated readable runic inscription. No
permanent lightning or magical rarity glow is added. Official tiles are ignored
for design as directed in `ObjectArtDirection.md`; tiny projections are scale
diagnostics only, not attempts to reproduce generic hammer pixels.

## Evidence and scope

`CreateMjollnir.py` generates only the named asset. `ReviewMjollnir.py` checks
closed, finite, nonzero geometry, corner paint and all 95 prior canonical FBX
hashes, then renders front/rear/underside/detail. The native scene contains
individually editable geometry and paint. `ImportMjollnir.py` imports into a
separate artifact folder and validates vertex colours and normal/memory materials.
Logs: `build-mjollnir-{blender,review,import-final}.log`. Geometry evidence:
`Art/ObjectInterpretations/mjollnir-inspection.json`.

Actual studio views are `mjollnir-three-quarter.png`, `mjollnir-front.png`,
`mjollnir-rear.png`, `mjollnir-underside.png`, `mjollnir-detail.png`; six real
16x16 renders and bounds are in `projection-report-mjollnir.json`, with a
`Mjollnir-Projections.png` review board. Closed geometry/paint checks pass for
30 editable parts and 417,456 triangles (dense grain sampling; LOD reduction remains); all 95 earlier FBX exports are unchanged.

**Design/import draft; live integration pending.** The current bridge exports
only selected ordinary displayed objects, not known artifact eligibility.
There is no safe native displayed-artifact key yet. This model is deliberately
not selected from a hidden artifact ID or an arbitrary named ordinary hammer.
Before live selection, implement and test an explicit native knowledge rule
including unidentified/identified, named ordinary items, hallucination, piles,
memory, save/restore, fallback and no-turn style switching. The checklist remains
unchecked until that work passes. Base `WAR_HAMMER` also remains incomplete.

No gameplay was launched, native backend replaced or player save modified.
Creature coverage stays 78/381 (20.5%); four live object presentations remain.
Head proportions, ornament seating, physical material finish and LODs remain
reviewable draft work.

## Material revision
User requested a sturdy metallic head and wooden hilt. Head and striking faces now use full metallic response with lower roughness and brighter iron/silver reflectance. Removed the helical leather binding and replaced the grip with densely sampled longitudinal wood-grain paint. The editable model, export and Unreal materials are updated together. Live eligibility remains pending; saves unchanged.



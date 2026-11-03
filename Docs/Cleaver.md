# Cleaver: oversized barbarian gift axe

Update, 2026-11-02: these models are now connected to the live dungeon under the
[MVP placement rules](MVPObjectPlacement.md), with isolated native mapping and
Unreal placement checks passed. Earlier pending-live statements below describe
the original art-only milestone. Finishing and broader edge-case review remain
separate from MVP placement; full-completion checkboxes are unchanged.

User request: huge, cool and barbaric, worthy of a barbarian's divine gift.
Native source `include/artilist.h:114` defines Cleaver on `BATTLE_AXE`, neutral,
associated with `PM_BARBARIAN`, with physical attack. `objects.h:239` calls the
base appearance a double-headed axe and specifies iron. Gameplay is unchanged.

The design has two massive crescent blades with long beard points, thick forged
cheeks and bright tapered cutting bevels. A long hardwood haft carries two
heavy hide-wrapped grips, reinforced bronze ferrules, an iron socket, crown
spike and pointed pommel. Broken chevron inlays, peened rivets and paired ivory
fang ornaments give the head a rough ceremonial identity. These are creative
craft choices, not native equipment, kill trophies, readable runes or claims
about a particular barbarian culture. No blood state, elemental effect, blessing
glow or hidden rarity indicator is added. Original generic tiles are ignored
for design, following the user's weapon-art direction.

Standing examination dimensions are approximately 1.14m across and 1.55m tall,
deliberately much bigger than the Mjollnir study. This is an art interpretation,
not a change to native reach, damage, weight or strength requirements. Static
loot examination is the intended scope; it does not replace fixed player
clothing or add weapon-swing animation.

Artifacts under `Art/ObjectInterpretations/`: `Cleaver.blend`, `cleaver.fbx`,
`cleaver-three-quarter.png`, front/rear/underside/detail renders, six actual
16x16 reverse projections and `projection-report-cleaver.json`.
`cleaver-inspection.json` records closed finite/nonzero geometry and corner
paint. `cleaver-protected-assets.json` preserves the 103 previous canonical
exports, including Mjollnir and all seven armor/cloak designs.

Scripts: `CreateCleaver.py`, `ReviewCleaver.py`, `ImportCleaver.py`.
Unreal destination: `/Game/ArtifactInterpretations/Cleaver/Meshes/SM_cleaver`.
The separate folder preserves the existing hammer's materials. Normal and
memory variants separate forged iron, polished cutting edges, bronze and
nonmetal parts. Evidence: `build-cleaver-{blender,review,import}.log`.

**Design/import draft; native known-artifact mapping and live checks remain
pending**, as for Mjollnir. Do not reveal Cleaver from a hidden artifact ID or
an arbitrary named battle-axe. Native known/unknown, named ordinary items,
hallucination, piles, memory, save/restore, fallback and no-turn switching need
verification before live use. Artifact and base-object checklist items remain
unchecked. This art work launches no gameplay and changes no player saves or
native backend. Creature/live-object counts remain unchanged.

Cutting-bevel transitions, inlay seating, grip wear, fine surface finish and
LOD/runtime budgets remain draft finishing work.

Final design checks pass: 38 editable parts, 26,504 triangles, closed geometry,
valid corner paint and all 103 previous exports unchanged. Front/rear/underside,
detail and six actual tiny projections were visually inspected; combined board:
`Cleaver-Review.png`, assembled with `CreateCleaverBoard.py`. Unreal import
reports `CLEAVER_IMPORT_READY count=1` with vertex colours and material assignment
validated. Source-catalogue tests pass in `build-cleaver-catalogue-tests.log`.

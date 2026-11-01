# Dwarf mummy and dwarf zombie

Batch 17 extends the saved dwarf family with two editable, vertex-painted,
unrigged static drafts. Each identity has one shared male/female appearance.

## Source facts and interpretation

| Identity | Source / official tiles | Source traits |
| --- | --- | --- |
| `PM_DWARF_MUMMY` | `monsters.h:1926`; 390/391 | Level 5, difficulty 6; one 1d6 physical claw attack |
| `PM_DWARF_ZOMBIE` | `monsters.h:2445`; 496/497 | Level 2, difficulty 3; one 1d6 physical claw attack; stalking |

Both are hostile, breathless, mindless dwarf undead with cold/sleep/poison
resistance, infravision, poison flags and no corpse. Mummy also has greedy/jewel
flags. `MZ_HUMAN` is abstract source size, not a literal height specification.
NetHack retains the gameplay traits; the meshes do not implement attacks or AI.

Both sex tiles are identical for each identity. The mummy shows a blue cap,
pale linen/beard, peach skin and red face/shin accents. The zombie shows the
same blue/cyan clothing and cap as the dwarf, green skin and an ash-blue beard.
The offset black mass to the right and beneath the feet is cast shadow, not a
weapon, cloak or extra limb. The spatial comparison mask retains enclosed
black details and excludes the exterior fringe. Original comparison tiles
remain unmodified; silhouette overlap is only a rough diagnostic.

Hidden anatomy, garment construction, complete back views and precise linen
layout are art interpretations. The mummy's red face pixels are represented
by seated red eyes. Its isolated shin pixel becomes a small red cloth accent;
it is ambiguous and is not treated as evidence of blood or a wound. No held
weapon, inventory, aura, exposed bone or graphic injury is inferred. The
zombie retains dark eyes, matching the source instead of borrowing the red
gnome-undead treatment.

## Geometry and paint

`DwarfStates.py` appends the existing `dwarf` collection from batch 16. Body,
ears, beard, eyes and cap preserve their saved geometry. The mummy omits the
tunic, sleeves and trousers, retaining pale-painted boots and a blue cap;
eleven separate closed linen ribbons follow the actual ancestry surface.
The zombie retains the saved costume, changing skin and beard paint only.
No earlier asset is regenerated.

Saved body vertex hashes match `dwarf_body` exactly for both identities.
Paint uses `FLOAT_COLOR` / `CORNER`, and both eyes retain their original skull
fit. Linen is solidified by 1.5mm and fits within 4.6mm of the actual body.
The native triangle counts are 117,636 mummy / 154,348 zombie. These are draft
costs; no production LOD, performance, rigging or animation claim is made.
Cloth edges/folds, face/beard finishing, undead pose, rigs, motion, effects and
LOD/performance review remain finishing work.

## Artifacts and verification

- `Art/CreatureInterpretations/CreatureBatch17.blend`: two editable collections,
  paint and saved studio; mummy initially visible.
- `dwarf_mummy.fbx` / `dwarf_zombie.fbx`: painted mesh exports.
- `Batch17-SourceReview.png`: both official sex tiles plus the saved ancestry tile.
- `Batch17-Models.png` / `MeshComparison-batch17.png`: actual models, front/rear
  renders, source pixels and the best actual 16x16 projection for each identity.
- `Batch17-Projections.png` / `projection-report-batch17.json`: all twelve true
  16x16 camera candidates, bounds and spatial shadow diagnostics.
- `Batch17-EyeReview.png`: saved front/profile head renders.
- `batch17-mesh-inspection.json`: saved geometry/paint, floor, eye fit, closed
  linen, exact ancestry hashes, matching sex tiles and preceding export hashes.
- `batch17-protected-assets.json`: all 56 preceding FBX hashes (52 creature/player,
  three objects and the shared tile quad).
- `Batch17-Unreal-fixtures.png`: actual live engine fixture capture.

`CreateCreatureBatch17.py` generates only these two derivatives.
`RenderCreatureBatch17.py`, `ReviewCreatureBatch17.py` and
`InspectCreatureBatch17.py` inspect saved work. `ImportCreatureBatch17.py`
targets only the two new meshes. Runtime selection uses displayed canonical
identity and sex metadata; both sexes select the same ancestry/state mesh.
The dwarf family's 15-degree orientation is retained. Other displays retain
the existing official tile fallback and perception boundary.

Native saved-mesh inspection, editor build and both targeted imports pass.
Studio front/rear, head views, all twelve true 16x16 projections and the actual
engine capture were inspected. Both engine fixtures are unobstructed, painted
and casting shadows. All 56 preceding exports retain their original hashes.

The final live run passes all four displayed sex forms and their four official
tile fallbacks, unknown identity and paint buffers. Both real F9 switches retain
native turn 5/input sequence 7. Native map, hero centring and 8x zoom pass. The
capture validator now recognises batch 17's existing 8x preview configuration.
Evidence: `build-creature-batch17-{blender,review,inspect,unreal,import,live}.log`.

Current inventory: 394 unique source identities = 50 completed creatures + one
completed player role + 331 remaining creatures + 12 remaining player roles.
There are 54 creature/player physical forms: 50 primary creatures, two extra
female creature appearances and two human player forms. Three object assets
remain separate. Next suggested batch: hobgoblin, hill orc and Mordor orc,
reviewing source traits/sex tiles before establishing a compatible family.

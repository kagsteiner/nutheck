# Pony, horse and warhorse

Batch 11 introduces a reusable equine family, with complete editable anatomy,
painted static FBX exports and the approved texture-only short-coat treatment.
The user approved batch 10 before authorizing this work. Previous 30 FBX exports,
including the approved jaguar coat, are protected by pre-batch SHA-256 checks.

## Source facts and interpretation

| Identity | Pinned NetHack facts | Art interpretation |
| --- | --- | --- |
| Pony (`PM_PONY`) | `monsters.h:1002`; medium domestic herbivore, level 3, 1d6 kick and 1d2 bite; tiles 204/205 show chestnut body, darker mane/tail, blue eye and pale hooves | Compact stocky pony with shorter legs and muzzle, upright neck, long equine head, leaf-shaped ears, lateral blue eyes, continuous dark mane/tail masses and four pale horn hooves |
| Horse (`PM_HORSE`) | `monsters.h:1034`; large domestic herbivore, level 5, 1d8 kick and 1d3 bite; tiles 212/213 show longer chestnut body/legs with the same mane, eye and hoof palette | Longer, taller adult horse with narrower barrel relative to length, longer nasal bridge, articulated forelegs/hind hocks, flowing tail and short mane crest |
| Warhorse (`PM_WARHORSE`) | `monsters.h:1042`; large strong domestic herbivore, level 7, 1d10 kick and 1d4 bite; tiles 214/215 show a larger chestnut equine with broad neck/head and pale/orange hoof accents | Stronger chest/haunches/neck, broader head, larger single hooves, dark mane/tail and warmer chestnut coat; no armour, saddle or bridle inferred |

The pony is a compact equine type, not a claim that all ponies are juvenile horses.
The three forms vary independently rather than by uniform scaling. Pony
leg/torso ratio is 1.189 versus horse 1.340; width/torso ratio is .416 versus .357;
muzzle/head ratio is 1.265 versus 1.591. Warhorse width is .163m versus horse
.127m, head length .159m versus .137m, with a deeper body and taller neck. These
are miniature art dimensions for grid readability, not literal conversions of
NetHack size or weight. Both displayed sexes share each mesh.

The brown `J` pixels are retained as mane/tail shading and pale `L` pixels as hoof
horn. Black pixels offset below the feet and behind neck/tail are treated as
cast-shadow fringe. The projection diagnostic keeps the two reviewed mouth
pixels per tile and excludes the remaining black fringe, without altering source
images. Small blue eye accents are explicit in the official tile. No clear tack
is depicted, so these drafts introduce no saddle, bridle or armour module. Future
equipment needs its own displayed-state rules.

## Construction and review

`EquineFamily.py` builds a continuous barrel, haunches, shoulders, upright tapered
neck, poll, jaw, long nasal bridge and muzzle. Front legs have knees, cannons,
fetlocks and pasterns; hind legs have distinct stifle/hock bends. Four separate
closed, bevelled single hoof meshes replace the paws used by earlier families.
Small dark nostrils and mouth creases sit on the muzzle.

`EquineEyes.py` casts onto the actual saved skull to fit small lateral almond
eyes, horizontal dark pupils and coat-coloured lids. It leaves all earlier eye
helpers unchanged. Rounded leaf ears use closed geometry and fitted inner leaves.
The short coat reuses FurFlow UVs and the shared texture-only fur material.
Mane and tail are smooth continuous long-hair silhouette masses, not individual
strands or a short-fur clump treatment.

Initial studio review found the mane mostly buried in the neck and inner ear
shapes detached forward. `RefineCreatureBatch11.py` repaired the saved scene by
casting onto the rear neck silhouette for the mane and onto each evaluated ear
for its inner leaf. Fresh generation already uses these fitted constructors.
Do not repeat the repair merely to inspect existing geometry. Ear-lining gap
checks measure about .5mm from the closed ear surface. Frontal/profile head
views supplement symmetry checks, and rear views inspect the mane, tail and hocks.

## Artifacts and reproduction

- `Art/CreatureInterpretations/CreatureBatch11.blend`: separate editable
  collections, corner paint, packed short-coat maps and studio camera/lights;
  pony initially visible.
- `pony.fbx`, `horse.fbx`, `warhorse.fbx` alongside the blend: painted static
  meshes with floor origins and coat UVs.
- `MeshComparison-batch11.png`: official tiles, actual 16x16 reverse projections,
  actual three-quarter/rear renders. Six candidates per creature, bounds and
  explicit shadow exclusions are in `projection-report-batch11.json`.
- `Batch11-EyeReview.png`: six actual saved-mesh frontal/profile head views.
- `Batch11-Models.png`: actual studio mesh renders together.
- `batch11-mesh-inspection.json`: saved geometry, paint, UV, floor, lateral-eye,
  horizontal-pupil, four-hoof, fitted-ear and independent-proportion checks.
- `batch11-protected-assets.json`: SHA-256 protection for all prior 30 FBX exports.
- `Batch11-Unreal-fixtures.png`: actual engine fixture capture on revealed
  floor, using displayed identities rather than native monster spawns.

Generate with Blender background mode, four threads, and
`Scripts/CreateCreatureBatch11.py`. For existing geometry use
`InspectCreatureBatch11.py`, `RenderCreatureBatch11.py` and
`ReviewCreatureBatch11.py`; these do not regenerate anatomy. The head-review
script restores the opening collection and saves the gallery after rendering.
Assemble the boards with `CreateCreatureBatch11Comparison.py` and
`CreateCreatureBatch11EyeComparison.py` using Python/Pillow.

The full Unreal importer now supports 33 candidates;
`ImportCreatureBatch11.py` targets only pony/horse/warhorse. The new equines face
-X and use -75 degree yaw like other quadrupeds. Runtime selection remains
based only on displayed identity and sex. Ordinary style/fallback behavior is
retained. `VerifyCreatureBatch11.ps1` checks all six displayed sex forms, six
fallback cases, unknown identity, materials/UV/paint, F9 both directions with no
turn, native movement/map, hero centring and 8x zoom.

## Verification

- `build-creature-batch11-blender.log`: three native models, painted FBX exports,
  six initial studio renders and 18 true 16x16 projections completed.
- `build-creature-batch11-refine.log`: three fitted manes, six fitted inner ears,
  updated FBX files and saved scene completed.
- `build-creature-batch11-inspect.log`: native checks and protection of all
  previous 30 exports passed. Native triangles: 85,524 pony / 109,412 horse /
  140,036 warhorse.
- `build-creature-batch11-unreal.log`: editor build passed.
- `build-creature-batch11-renders.log` and `build-creature-batch11-review.log`:
  refreshed six studio views, 18 projections and six head views completed.
  Actual front/rear, fitted-ear/eye close-ups and comparison boards inspected.
- `build-creature-batch11-import.log`: all three targeted imports passed with
  fur material/paint validation, count 3 and successful editor exit. Engine
  triangle counts match native: 85,524 pony / 109,412 horse / 140,036 warhorse;
  each has one fur slot and two UV channels.
- `build-creature-batch11-live.log`: six displayed sex forms, six fallbacks,
  unknown identity, material/UV/paint buffers and F9 both ways passed at unchanged
  turn 5. Native movement/map, hero centring and 8x zoom passed. Actual engine
  capture inspected; glyph badges obscure portions of two fixtures, while studio
  and head views provide unobstructed geometry inspection.
- Final source/export/inventory check: 394 source identities = 33 verified static
  drafts + 348 remaining creatures + 13 player-role presentations. Checkboxes
  updated in place; all 30 earlier FBX hashes are retained.

All three are unrigged static drafts. Mane/tail grooming, ear rims, shoulder/neck
transitions, hoof detail, rigs, gait/kick/bite animation, riding/equipment state,
LODs and production performance budgets remain finish work. No equestrian rig,
dynamic tack behavior or animation is claimed complete.

# Wolf, winter wolf cub and winter wolf

The fifth batch follows the session handoff's suggested wolf family. These are
complete editable anatomical static drafts with vertex paint and texture-only
fur, using the approved middle treatment from the fur study.

**User review correction completed:** blue/cyan tile pixels are cast shadow,
not coat colour. Both winter forms now have pale limbs, neutral ear lining and
no cyan muzzle patches. Their red eyes have been moved forward and inward,
reduced to skull-conforming almond apertures, and framed by pale eyelids with
small dark pupils. The saved meshes were repaired; unrelated bodies were not
regenerated. User visual acceptance remains separate from technical validation.

## Source facts and artistic assumptions

| Identity | Pinned source facts | Artistic assumptions |
| --- | --- | --- |
| Wolf (`PM_WOLF`) | `monsters.h:257`; medium, level 5 carnivore, physical bite, grey ASCII colour; official tiles 40/41 show blue-grey body, pale eyes, red nose and lifted tail | Lean standing wolf frame, digitigrade legs, long muzzle, triangular ears and soft underside shading |
| Winter wolf cub (`PM_WINTER_WOLF_CUB`) | `monsters.h:275`; small, level 5 carnivore; bite, cold breath and cold resistance; tiles 44/45 show white body and red eyes/nose, with a cyan cast-shadow fringe | Shorter torso, legs and muzzle with relatively large head and paws; pale coat, neutral ear lining, smaller inset red eyes and independent juvenile proportions |
| Winter wolf (`PM_WINTER_WOLF`) | `monsters.h:290`; large, strong level 7 carnivore; stronger bite/cold breath and cold resistance; tiles 48/49 show pale coat/red eyes/nose plus a cyan cast shadow | Larger adult wolf frame and longer muzzle; restrained coat texture and inset red eyes; cast-shadow colours excluded |

One parameterised family varies torso, head, muzzle, legs, ears and paws
independently. The cub is not a uniformly scaled adult. Head/torso length ratios
are 0.546 for cub, 0.403 for winter adult and 0.410 for ordinary wolf. Both
displayed sexes share the same geometry. Dimensions favour one-metre game cells;
they do not convert NetHack's abstract size/weight into real measurements.

Winter forms have named `*_cold_breath_socket` empty objects in the blend at
the muzzle. Static mesh FBX excludes these empties. They record a future effect
attachment, not an implemented cold-breath effect, rig or animation.

## Artifacts and reproduction

- `Art/CreatureInterpretations/CreatureBatch5.blend`: editable paint, geometry,
  three named species collections, packed coat maps, camera and lights; wolf
  initially visible.
- `wolf.fbx`, `winter_wolf_cub.fbx`, `winter_wolf.fbx`: painted static mesh exports
  in the same directory, with `FurFlow` UVs on coat parts.
- `MeshComparison-batch5.png`: official tiles, actual 16x16 renders and actual
  front-quarter/rear model views; six camera candidates per identity are retained
  in `projection-report-batch5.json`. Silhouette overlap is only a diagnostic.
- `batch5-mesh-inspection.json`: native geometry, age, paint, floor and UV checks.
- `Batch5-Unreal-fixtures.png`: actual engine capture of synthetic presentation
  fixtures on visible floor; these are not native monster spawns.

Run Blender background mode with four threads and
`Scripts/CreateCreatureBatch5.py`, then Python/Pillow
`Scripts/CreateCreatureBatch5Comparison.py`. `CreatureBatch2Pipeline.py` now
accepts an optional post-paint surface hook. `CreatureFur.py` adds the same two
shared 512x512 brush/normal maps from `Art/FurStudy/Textures`, four UV repeats per
metre and no added triangles, strands, shells or clumps. Paint modulation and
shallow normals match the existing study material. Maps are packed in the blend.

`Scripts/RenderCreatureBatch5.py` refreshes saved renders without regenerating
geometry. It repaired the first render pass's premature relative texture paths;
`build-creature-batch5-renders.log` is the corrected render evidence. The
generator now packs textures before rendering as well.
`Scripts/InspectCreatureBatch5.py` inspects the saved blend without rebuilding it.

Build `NUthEckEditor`, then use full editor startup Python to run
`Scripts/ImportCreatureInterpretations.py`. It validates fifteen painted imports,
with the new `Fur_*` slots assigned to `/Game/FurStudy/M_PaintedFur`. Existing
twelve models are not regenerated or retrofitted with fur. The shared material
retains the approved linear brush sampling, normal green-channel flip and .82
roughness from the verified fur study.

`Scripts/VerifyCreatureBatch5.ps1` runs native gameplay plus explicit displayed
identity fixtures. Selection reads only displayed species and sex, including
both displayed sexes, fallback and unknown identity. New wolves use -75 degree
yaw like the existing quadrupeds. F9 remains a no-turn presentation switch.
Runtime checks also require coat material slots, UV channels and colour buffers.

## Review and remaining work

Front-quarter/rear views and all three official-tile comparisons were inspected.
The miniature colours and lifted tails are recognisable; lean standing anatomy
deliberately differs from the tile outline. The cub has a larger relative head
and shorter legs. Eyes now use matched anterior orbital placement, small conforming apertures,
pale lids and dark pupils. Muzzle/neck transitions, toe shapes and coat flow
still need refinement. Red facial details
lose contrast at 16x16. Texture-only fur is subtle and adds no silhouette detail.

Revised native triangle counts are 59,568 wolf, 40,228 cub and 76,396 winter wolf. These
are procedural static drafts, not production LODs or validated frame budgets.
No rigs, gait/attack animations, cold-breath effects or finished performance
claims are included. Generation completion remains separate from finish work.

## Verification evidence

- `build-creature-batch5-inspect.log`: native geometry, CORNER/FLOAT_COLOR paint,
  coat UV/material slots, valid coordinates, floor clearance, independent age
  proportions and cold-breath attachment checks passed.
- `build-creature-batch5-renders.log`: corrected studio views and eighteen true
  16x16 candidate renders completed from the saved geometry.
- `build-creature-batch5-unreal.log`: editor module build.
- `build-creature-batch5-import.log`: fifteen imports, three
  `CREATURE_FUR_MATERIAL_VALID` markers, and
  `SCULPTED_CREATURES_READY count=15`; import exited successfully.
- `build-creature-batch5-live.log`: six displayed sex forms, six fallback cases,
  unsupported identity, fur materials/UVs/colour buffers and both F9 directions
  passed with turn 5 unchanged. Native map, hero centring and 8x zoom passed.
  Actual `Batch5-Unreal-fixtures.png` was inspected.
- The shadow interpretation correction is applied; technical checks do not
  substitute for the user reviewing the revised anatomy.

## Winter-wolf revision evidence

- `Scripts/RepairWinterWolves.py` repairs the two saved winter identities,
  repainting the continuous anatomy, removing false cyan muzzle objects and
  replacing the old floating globes. It checks that ordinary `wolf.fbx` stays
  byte-for-byte unchanged. Evidence: `build-winter-wolf-repair.log`.
- `WinterWolfEyes.py` provides the same eye construction to both repair and
  future generation: cast onto the actual skull surface, bilateral forward gaze,
  shallow red apertures, dark round pupils and pale upper/lower eyelids.
- Saved inspection confirms removal of cyan coat paint and paired eye centres
  within 1mm in height/fore-aft/mirrored spacing; measured differences are much
  smaller. These checks establish symmetry, not biological accuracy by themselves.
- `ReviewWinterWolfEyes.py` renders actual frontal, three-quarter and profile
  close views. `WinterWolf-EyeReview.png` assembles all six. These views, revised
  front-quarter/rear body renders and true 16x16 comparisons were inspected.
- Camera fitting now explicitly excludes palette `B` (cyan cast shadow), as well
  as background and black fringe, for the two winter identities. The untouched
  official tiles remain on the comparison sheet. The projection report records
  excluded shadow entries. Cyan pixels do not guide coat palette or anatomy.
- `ImportWinterWolfRevision.py` reimports just the two changed FBX assets using
  the shared validated importer. `build-winter-wolf-reimport.log` reports two
  painted imports, two fur-material checks and `SCULPTED_CREATURES_READY count=2`.
- Revised live validation passed all six displayed sex forms, six fallback cases,
  unknown identity, material/UV/paint buffers and both F9 directions with turn 5
  unchanged. Native map, hero centring and 8x zoom passed. The revised actual
  Unreal fixture capture was inspected. Evidence: `build-creature-batch5-live.log`.
  Engine triangle counts are 40,220 cub and 76,388 adult.
- `REVISION_SOURCE_AND_INVENTORY_CHECK PASS`: revision scripts parse, cyan shadow
  exclusions are recorded, and all 394 unique backlog identities remain intact,
  with 15 generated drafts. No identity was duplicated by this repair.

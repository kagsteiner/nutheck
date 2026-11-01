# Bat, giant bat and vampire bat

The eighth batch establishes a parameterised bat family: complete editable
anatomy, closed wing membranes, painted colours and body-only texture fur.
These are static spread-wing drafts, not rigged or animated flight assets.
The prior twenty-one FBX files are not regenerated.

## Source facts and interpretation

| Identity | Pinned source facts | Artistic interpretation |
| --- | --- | --- |
| Bat (`PM_BAT`) | `monsters.h:1269`; tiny, flying carnivore, level 0, physical bite 1d4; tiles 256/257 show a brown upper figure with orange/yellow facial accents and a detached lower black shadow | Brown body, yellow fitted eyes, large cupped ears, arm-supported wings, free thumbs, hind feet and tail membrane; hovering spread-wing pose |
| Giant bat (`PM_GIANT_BAT`) | `monsters.h:1276`; small, hostile flying carnivore, level 2, bite 1d6; tiles 258/259 add broader brown/orange wings; ASCII colour is red | Longer body and wider wings, independently smaller relative head, different chord and warmer brown palette; not a uniform enlargement |
| Vampire bat (`PM_VAMPIRE_BAT`) | `monsters.h:1291`; small, hostile flying omnivore, level 5; physical/poison bites, regeneration, sleep/poison resistance; tiles 262/263 use a black upper silhouette with red eyes and a separate lower black shadow | Charcoal body/membranes with red fitted eyes, broader head/nose pad, broader wing chord, reduced tail-membrane extension and tiny incisors |

These are NetHack fantasy identities, not reconstructions of named zoological
species. Colour masses come from the actual tiles, not ASCII colour codes.
Sexes share geometry. Literal metre dimensions, ear shape, hidden anatomy,
tooth detail and exact flight pose are artistic assumptions. Poison, regeneration,
resistance and flight behaviour remain NetHack gameplay, not material effects.

The basic anatomical construction uses modified forelimbs and finger-supported
membranes, with a separate free thumb, following the
[Smithsonian bat overview](https://www.si.edu/spotlight/bats/batfacts) and
[National Park Service wing anatomy](https://home.nps.gov/subjects/bats/how-bats-fly.htm).
The model gives each side an arm, four elongated wing digits and a clawed thumb;
the inner membrane attaches near the hind foot. These references inform the
blockout, not a claim of species-level biological accuracy.

## Cast-shadow handling

Each tile contains a detached black lower silhouette. Rows 9-15 are excluded
from geometry inference and projection matching. The upper black pixels are
retained, including the vampire bat's actual black body and wing shape. Blanket
black-palette exclusion would erase that creature and fit only its red eyes.
The comparison sheet retains the untouched official tiles, with both figure
and shadow visible; the true 16x16 render contains only the actual bat geometry.

Camera candidates are frontal/oblique (-180/-155/-125 degrees), each at 25/45
degrees elevation. This preserves broad wing presentation rather than comparing
a foreshortened side view with the tile's front silhouette. All 18 candidates
are actual 16x16 renders; silhouette overlap remains only a rough diagnostic.

## Artifacts and workflow

- `Art/CreatureInterpretations/CreatureBatch8.blend`: three named editable
  collections; bat visible initially; native geometry, corner paint, packed fur
  maps, camera and studio lights.
- `bat.fbx`, `giant_bat.fbx`, `vampire_bat.fbx` alongside the blend: painted static
  meshes. Floor origins remain below the hovering pose; lowest geometry is about
  .16-.17m above that origin. Real engine shadows provide the ground separation.
- `MeshComparison-batch8.png`: official tiles, actual 16x16 projections, frontal
  model views and rear studio renders. Front-quarter renders are retained too.
- `projection-report-batch8.json`: six poses each, bounds and explicit excluded
  shadow rows, with upper black anatomy retained.
- `Batch8-WingFaceReview.png`: nine actual front/underside/face views, with a
  shared extra underside fill light for geometry inspection.
- `batch8-mesh-inspection.json`: geometry, paint, fur UVs, closed membrane edges,
  digits/thumbs, eye pairing, floor clearance and proportion checks.
- `Batch8-Unreal-fixtures.png`: actual engine capture with synthetic displayed
  identity fixtures on revealed floor, not native monster spawns.

Generate with Blender background mode, four threads, and
`Scripts/CreateCreatureBatch8.py`. `BatFamily.py` independently varies body/head,
ear, half-span and wing chord. Each membrane panel follows the bent finger
paths and has curved scalloped edges. Solidified 3-4mm membranes provide actual
front/back geometry and shadows; there are no alpha cards or one-sided wings.
The tail membrane has its own geometry between the hind limbs.

Initial studio review replaced overly flat panels with curved finger-following
panels through `RefineCreatureBatch8Wings.py`, preserving the other saved anatomy
and paint. The generator already contains the final construction. For inspection
rerenders use `RenderCreatureBatch8.py`, not geometry regeneration.
`CreatureFur.py` adds the approved two-map texture treatment only to the body;
membranes, wing digits, pinnae and claws keep painted surfaces.
`WinterWolfEyes.py` supplies skull-conforming paired apertures/lids, with yellow
or red iris pigments. No existing models receive a fur retrofit.

`InspectCreatureBatch8.py` inspects the saved blend. `ReviewCreatureBatch8.py`
renders front/underside/face detail. Python/Pillow
`CreateCreatureBatch8Comparison.py` and `CreateCreatureBatch8Review.py` assemble
the boards from actual renders.

Build `NUthEckEditor` and run `ImportCreatureBatch8.py` via full editor startup
Python. Targeted import validates these three and reports count 3; the full
shared importer now supports 24. Body fur uses the existing verified study
material, while membranes use the opaque vertex-paint material.

`VerifyCreatureBatch8.ps1` checks six displayed sex forms, six fallback cases,
unknown identity, fur materials/UV/paint buffers and F9 both ways without a turn,
plus native map, hero centring and 8x preview zoom. The chosen orientation is
front -X in Blender and -75 degrees yaw in gameplay, matching the existing
front-facing sculpt convention. Flight elevation is in the static mesh pose;
no hidden-world state is used to choose the mesh. Ordinary launches retain the
tile-volume default.

## Verification and remaining work

- `build-creature-batch8-inspect.log`: native checks passed, including all membrane
  edges manifold after thickness, nonzero membrane face areas, four wing digits
  per side, two free thumbs/claws, paired eyes, valid paint/UVs and floor clearance.
- Native triangles are 35,872 bat / 43,328 giant bat / 45,628 vampire bat.
  Half-spans .350/.470/.445m and chord .235/.295/.320m distinguish the forms.
  Head/body length ratios .480/.430/.478 confirm independent proportions.
- `build-creature-batch8-wings.log`: saved wing-panel refinement, three final FBX
  exports and updated front-quarter/rear plus 18 true 16x16 renders completed.
- `build-creature-batch8-review.log`: nine saved-mesh inspection views completed.
  Front, rear, underside, face and comparison boards were visually inspected.
- `build-creature-batch8-unreal.log`: editor build succeeded.
- `build-creature-batch8-import.log`: all three targeted imports passed painted
  buffers and body-fur material checks, ending with count 3 and successful exit.
- `build-creature-batch8-live.log`: six displayed sex forms, six fallback cases,
  unknown identity and both F9 directions passed at unchanged turn 5. Runtime
  coat material, UV and painted buffers passed for each form. Native map, hero
  centring and 8x zoom passed. The engine capture was inspected; foreground walls
  obscure portions of the two larger bats, so studio views are the complete
  geometry inspection.
- Native and imported engine triangle counts agree: 35,872 / 43,328 / 45,628.
  Each imported model has one fur slot and two UV channels. Membranes retain
  opaque vertex-paint material slots.
- Backlog/catalogue reconciliation: 394 identities = 24 generated static drafts
  + 357 remaining creature identities + 13 remaining player-role presentations.

Wing roots, membrane folds, ear rims and face proportions remain refinement
targets. Thin claws, digits and eye details average away at overview scale.
Manifold-edge checks do not certify a production deformation mesh. No rig,
wingbeat/landing/hanging poses, membrane simulation, combat animation, LODs or
production performance budget has been validated. These remain static drafts.

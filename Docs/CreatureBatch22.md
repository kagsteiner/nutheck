# Soldier ant, fire ant and giant beetle

Batch 22 follows the handoff queue. There are three identities and five physical
forms: both ants have distinct female silhouettes in the official tiles; the
beetle's sex tiles are identical. These are editable static drafts. Animation
and rigs are outside the intended product scope under `GameVision.md`.

## Source and interpretation

| Identity | Source / official sex tiles | Native traits |
| --- | --- | --- |
| `PM_SOLDIER_ANT` | `monsters.h:103`; 4/5 | Level 3, difficulty 7; 2d4 physical bite, 3d4 poisonous sting; poison resistance/conveyance |
| `PM_FIRE_ANT` | `monsters.h:111`; 6/7 | Level 3, difficulty 6; 2d4 physical bite and 2d4 fire bite; fire resistance/conveyance, infravisible |
| `PM_GIANT_BEETLE` | `monsters.h:119`; 8/9 | Level 5, difficulty 6; 3d6 physical bite; poison resistance/conveyance |

All are hostile carnivorous animals without grasping hands. Ants are oviparous
and abstractly tiny; beetle is abstractly large. Soldier and beetle have the
poisonous-body flag. None has `M1_FLY`. Native attacks, resistances, turns and
generation remain unchanged. Source size does not define literal metre sizes.

Soldier ant follows the brown/orange source palette and cyan eye accents,
with broader head/mandibles than giant/fire ant. Blue ASCII colour is not blue
chitin. Fire ant uses red/orange chitin and green eye accents. Its fire bite
does not justify flame geometry or emissive paint. Beetle follows the actual
red/orange/brown/peach tile despite black ASCII colour, with cyan eye accents.

The tile artist explicitly describes female ants as slightly larger. Each new
female form has a 6% longer, 10% wider, 7% deeper thorax and 10% wider leg reach;
head and gaster remain unchanged. Exact dimensions and hidden anatomy are art
interpretations, not measured sexual anatomy. Both beetle sexes share one form.
No wings, armour, horns or inventory items were inferred.

Exterior black tile fringes are excluded spatially from projection diagnostics;
enclosed dark pixels remain. Original comparison tiles are unmodified. Masks
and silhouette overlap are approximate diagnostics, not anatomical proof.

## Construction

`AntBeetleFamily.py` parameterises the existing giant-ant construction from
`CreateCreatureInterpretations.py`: segmented gaster, petiole, thorax, paired
antennae and mandibles, and six thorax-rooted jointed legs. It does not modify
the original giant ant. Soldier ant gains independent head/mandible dimensions
and a small static sting corresponding to its attack. Gaster segmentation is
subtle vertex paint rather than additional raised rings.

Beetle has a separate broad abdomen/pronotum/head plan, stout legs, small
mandibles and closed paired elytra. The fitted half-ellipsoid covers form one
domed shell with a narrow medial seam. The underlying abdomen stays inside the
covers. `RefineCreatureBatch22Elytra.py` records the saved review correction;
fresh generation already contains the final anatomy. Do not run the repair
merely to inspect the scene. Use saved Render/Review scripts instead.

Paint is `FLOAT_COLOR` / `CORNER`, shared by Blender and UE. Native triangles:
17,916 each soldier form, 17,848 each fire-ant form, 11,636 beetle. They are
technical drafts, with shell/leg transitions, miniature surface painting,
overview readability and LOD/runtime costs still requiring visual finishing.

## Artifacts and verification

- `Art/CreatureInterpretations/CreatureBatch22.blend`: five editable collections,
  painted meshes and saved studio; soldier ant initially visible.
- `soldier_ant.fbx`, `soldier_ant_female.fbx`, `fire_ant.fbx`,
  `fire_ant_female.fbx`, `giant_beetle.fbx`: canonical painted exports.
- `Batch22-SourceReview.png`: all six original official sex tiles.
- `Batch22-Models.png` / `MeshComparison-batch22.png`: actual front-quarter and
  rear renders, original sex tiles and best true 16x16 projections.
- `Batch22-Projections.png` / `projection-report-batch22.json`: thirty actual
  tiny camera renders, bounds and explicit spatial mask exclusions.
- `Batch22-HeadReview.png`: ten actual front/profile head views.
- `batch22-mesh-inspection.json`: saved closed topology, valid paint/floor,
  six thoracic legs, paired eyes/mandibles/antennae, female proportions and
  separate beetle elytra; hashes of all 72 previous exports remain unchanged.
- `Batch22-Unreal-fixtures.png`: actual final engine fixture capture.
- `batch22-save-preservation.json`: verified played-session/runtime hash audit.

`CreateCreatureBatch22.py` builds only this batch. `RenderCreatureBatch22.py`
rerenders saved work; pass `-- giant_beetle` to refresh only the beetle and merge
its report into the existing five-form report. `ReviewCreatureBatch22.py` renders
saved close views, and `InspectCreatureBatch22.py` checks saved meshes.
`ImportCreatureBatch22.py` targets only these five exports.

Runtime mapping uses displayed identity and sex only. Female ants select their
respective female mesh, beetle shares one. Both normal placement and preview
use -75 degree yaw, matching the -X-facing ant construction. Official tile-card
fallbacks remain available for all six sex cases. F7/F9, camera controls, fixed
player clothing, walls, floor tint, doors, status HUD and DX12/SM6 remain intact.

Editor build, five imports/material colour buffers and saved native checks
pass. Final studio/rear, close views, thirty true tiny projections and live
captures were inspected. The final capture shows all three fixtures, with the
foreground wall hiding part of the fire ant; the retained staircase capture
shows its full body. Studio renders provide unobstructed views of every form.
Live checks cover all six
displayed sex cases, six fallbacks, unknown identity, vertex paint, actual F9
both ways without advancing turn/input sequence, native map/hero and 8x zoom.
Evidence: `build-creature-batch22-{blender,refine,renders,renders-beetle,review,
inspect,unreal,import,live}.log`.

## Save protection and inventory

Required backup `Backups/NetHackSaves/20261102T141755.766497Z.zip` verified
1,090 original player/runtime files before integration. `AuditCreatureBatch22Saves.py`
compares the complete file set, SHA-256 contents and LastSession pointer against
that archive. Native backend files are not rebuilt. Gameplay tests use fresh
`Saved/NetHackCaptures` sessions with `Remember=false`, never the played session.
No player game was launched, advanced, stopped or replaced.

After verified closeout: 65 completed creature IDs + one completed player role
+ 316 remaining creatures + 12 remaining roles = 394 source identities.
There are 71 physical creature/player forms: 65 primary creatures, four extra
female creature forms and two human players. Four object drafts and one
fountain remain separate. Coverage is 65/381 creatures = 17.1%, or
66/394 creature/player identities = 16.8%; this does not measure visual finishing.

Next suggestion: killer bee, queen bee and xan. Review sex tiles/source traits
and actual wing anatomy; reuse compatible bee construction while treating xan
as a separately reviewed body plan, rather than assuming glyph-class ancestry.

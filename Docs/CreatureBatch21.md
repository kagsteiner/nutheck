# Orc mummy and orc zombie

Batch 21 adds two static creature drafts using the reviewed saved upright orc
anatomy. Both official sex-tile pairs are identical; each identity uses one
shared appearance. Static poses are the intended product presentation under
`GameVision.md`; rigs and animation are outside scope.

## Source facts and interpretation

| Identity | Source / official tiles | Native traits |
| --- | --- | --- |
| `PM_ORC_MUMMY` | `monsters.h:1917`; 388/389 | Level 5, difficulty 6; one 1d6 physical claw attack; strong, greedy/jewels |
| `PM_ORC_ZOMBIE` | `monsters.h:2437`; 494/495 | Level 2, difficulty 3; one 1d6 physical claw attack; stalking, small groups |

Both are hostile orc undead: breathless, mindless, humanoid, poisonous,
infravision, cold/sleep/poison resistance, no conferred resistance and no corpse.
Abstract `MZ_HUMAN` does not specify literal metre proportions. NetHack retains
all attacks, generation, movement, resistance and corpse behaviour.

The mummy tile shows pale wrappings, pale headwear, red face accents and an
orange diagonal. This becomes fitted pale linen, retained helmet, seated red
eyes and a narrow orange cloth accent. The meaning of the diagonal is ambiguous;
it is not treated as evidence of a held weapon or gore. Zombie shows orange/
brown costume, cyan arms, gray limbs/headwear, green face accents and a bright
green waist. Those are surface pigments on the saved body and costume.

Hidden back/underside anatomy, precise linen construction, facial treatment and
static pose are artistic interpretations. The large offset black region below/
right is cast shadow, not armour, extra limbs, cape or a second body. Spatial
masks retain enclosed dark details, excluding the exterior fringe; original
source comparison tiles are unmodified. Silhouette overlap is diagnostic only.

## Geometry and paint

`OrcUndead.py` appends `mordor_orc` from the saved `CreatureBatch18.blend` for
both forms. Continuous body vertex signatures match that ancestry exactly;
no earlier model is regenerated. Both retain the helmet, ears and fitted eyes.
All held rods/blades are omitted rather than inherited as unsupported weapons.

Mummy omits the tunic, belt, sleeves and trousers. Twelve separate solid linen
ribbons fit the actual ancestry: torso, forehead/jaw, arms, legs and orange
accent. Ordinary linen fits within 4.6mm of the body. The outer orange cloth
accent fits within 7.6mm, clearing underlying linen. Boots and remaining skin
have pale paint. Both eyes follow the original seated geometry with red pigment.

Zombie retains costume geometry, painting sleeves orange, tunic orange/brown,
belt lime green, exposed arms cyan and remaining skin/legwear blue-gray. Eye,
brow and lower-lid pigments are green; two small dark pupils are added, with
no additional sex-specific facial structure. The lower face has a source-green
accent. There are no raised wound blobs, exposed bones or spell effects.

Paint uses `FLOAT_COLOR` on `CORNER`, through the established miniature material
pipeline. Native triangles: 91,292 mummy / 104,036 zombie. Linen edge/fold cleanup,
face/cloth paint refinement and LOD/runtime costs remain finish work. No animation
or rig requirement is implied.

## Artifacts and validation

- `Art/CreatureInterpretations/CreatureBatch21.blend`: two editable collections,
  saved studio and paint, with mummy initially visible.
- `orc_mummy.fbx` / `orc_zombie.fbx`: painted exports.
- `Batch21-SourceReview.png`: both official sex tiles plus saved-family reference.
- `Batch21-Models.png` / `MeshComparison-batch21.png`: actual models, source
  tiles, front/rear renders and the best actual 16x16 candidates.
- `Batch21-Projections.png` / `projection-report-batch21.json`: all twelve true
  tiny camera candidates, bounds and spatial shadow masks.
- `Batch21-EyeReview.png`: saved front/profile head renders.
- `batch21-mesh-inspection.json`: saved geometry/paint/floor/eyes, closed linen,
  source-shape signatures, sex-tile equality and previous-export hashes.
- `batch21-protected-assets.json`: 70 preceding canonical exports (64 creature/
  player, four objects, one fountain and the shared tile quad).
- `Batch21-Unreal-fixtures.png`: actual live fixture capture.
- `batch21-save-preservation.json`: player session/pointer and runtime hash audit.

`CreateCreatureBatch21.py` builds only the two derivatives.
`RenderCreatureBatch21.py`, `ReviewCreatureBatch21.py` and
`InspectCreatureBatch21.py` inspect saved work. `ImportCreatureBatch21.py`
targets only these two meshes. `VerifyCreatureBatch21.ps1` checks all four
displayed sex forms, their official tile fallbacks, unknown identity, paint,
both real F9 switches without a native turn/sequence change, map and 8x zoom.
Both normal placement and preview use the family's 15-degree orientation.
Selection uses only displayed canonical identity and sex.

## Save protection

Before integration, the complete played-session tree, pointer and matching
runtime were backed up and verified in
`Backups/NetHackSaves/20261101T131621.286474Z.zip`. No player game was launched,
advanced or stopped. Native backend files are not rebuilt for this art batch.
The capture uses `Remember=false`, a fresh `Saved/NetHackCaptures/<id>` root,
and never reads/writes the played `LastSession.txt`. The final audit confirms all
1,076 baseline files match their hashes: the full played-session file set,
pointer and matching runtime remain unchanged. Evidence is recorded in
`batch21-save-preservation.json`.

Saved geometry/paint/floor/eye/closed-wrap/ancestry inspection, editor build
and both targeted imports pass. All 70 earlier canonical FBX exports remain
unchanged. Four studio views, four heads, all twelve true 16x16 candidates and
the actual engine capture were inspected. Both fixtures are clearly visible.
All four displayed sex forms and their four official tile fallbacks pass,
including unknown identity and paint buffers. Both real F9 switches preserve
native turn 5/input sequence 7. Native map, hero centring and 8x zoom pass.
Evidence: `build-creature-batch21-{blender,review,inspect,unreal,import,live}.log`.
The capture log confirms a fresh `Saved/NetHackCaptures` session; final hash
verification confirms the played sessions, pointer and backend remain unchanged.

Current inventory: 62 completed creatures + one completed player role + 319
remaining creatures + 12 remaining player roles = 394 unique source identities.
There are 66 physical creature/player forms (62 primary creatures, two extra
female creature appearances and two human players). Four objects and one
fountain feature remain separate. Static-draft coverage is **62/381 creatures =
16.3%**, or **63/394 creature/player identities = 16.0%**. This does not measure
visual finishing or the entire game-art scope.

Next suggestion: soldier ant, fire ant and giant beetle. Review both sex tiles
and source traits; preserve supported ant construction and establish a separate
beetle anatomy rather than assuming all insects share the same body.

# Uruk-hai, orc shaman and orc-captain

Batch 20 extends the saved upright orc family with three editable, vertex-painted,
unrigged static drafts. Each identity's official male/female tiles are identical;
one shared appearance is used per identity, without invented sex anatomy.

## Source facts and interpretation

| Identity | Source / official tiles | Native traits |
| --- | --- | --- |
| `PM_URUK_HAI` | `monsters.h:770`; 154/155 | Level 3, difficulty 5; one 1d8 weapon attack; strong, collecting; large groups |
| `PM_ORC_SHAMAN` | `monsters.h:779`; 156/157 | Level 3, difficulty 5; magic/spell attack 0d0; magic flag |
| `PM_ORC_CAPTAIN` | `monsters.h:788`; 158/159 | Level 5, difficulty 7; two 2d4 weapon attacks; strong, collecting |

All three are omnivorous orc humanoids with poison resistance, infravision,
infravisibility, greedy and jewel flags. No conferred resistance is specified.
`MZ_HUMAN` is abstract source size rather than a literal metre measurement.
Native spell, resistance and combat distinctions remain in NetHack.

The source tiles show blue-gray skin with paired peach cheek pixels, pale metal
headwear, cyan vertical accents and distinct costumes. Uruk-hai has magenta
cloth and a blue-gray rectangular shield with a red centre. Shaman has orange/
brown clothes and a bright green waist accent. Captain has a wider pale helmet
edge, red shoulder accents, green chest and magenta lower cloth. The exterior
black mass extending down/right is cast shadow, not more equipment or anatomy.
Spatial masks exclude that fringe while retaining enclosed dark details;
original comparison tiles remain unmodified. Overlap is only a rough diagnostic.

Hidden back views, garment construction, exact shield curvature, a pale Uruk
waist band and the precise captain brim are artistic interpretations. The cyan
vertical strips retain the family's separate simple held rods; their exact
meaning is ambiguous, and these do not guarantee native staff/weapon inventory.
Uruk's shield and the captain's short pale blade are presentation cues, without
hidden equipment queries. Shaman has no blade, shield or invented magic effect.
No crown, horns, additional faction insignia, cape or shadow-derived appendage
is introduced. The red shield rectangle follows the tile rather than adding
an external emblem.

## Geometry and paint

`OrcRanks.py` appends the saved `mordor_orc` collection from batch 18 for each
identity. All three continuous body vertex hashes match that exact saved
ancestry. Existing ears, eyes, nose/jaw, clothes and helmet remain unchanged
in geometry. Shared blue-gray skin gains soft peach cheek paint. All previous
assets are retained without regeneration.

Uruk replaces the short blade with a separately editable curved shield and
back grip fitted to the retained hand. Its red centre is vertex paint on the
shield, with no raised emblem object. Shaman omits the blade and changes paint
to orange/brown costume and a green belt. Captain retains the blade and adds
a separate wider closed helmet-rim shell; red shoulders/green front panel are
paint on existing cloth. Head/body proportions remain shared.

Paint is `FLOAT_COLOR` / `CORNER`, through the established miniature materials.
The shield, helmet/rim, tunic and belt have closed thickness. Native triangles:
102,844 Uruk-hai / 101,648 shaman / 102,716 captain. These are draft costs, with
cloth/face/equipment refinement, rigs, spells/attacks/defence animation, effects,
LODs and runtime performance review remaining as separate finish work.

## Artifacts and verification

- `Art/CreatureInterpretations/CreatureBatch20.blend`: three editable collections,
  saved paint/studio, with Uruk-hai initially visible.
- `uruk_hai.fbx`, `orc_shaman.fbx`, `orc_captain.fbx`: painted exports.
- `Batch20-SourceReview.png`: all six official sex tiles plus hill-orc reference.
- `Batch20-Models.png` / `MeshComparison-batch20.png`: actual models, front/rear,
  original tiles and the best actual 16x16 candidate for each identity.
- `Batch20-Projections.png` / `projection-report-batch20.json`: all 18 true tiny
  camera candidates, bounds and spatial shadow diagnostics.
- `Batch20-EyeReview.png`: saved front/profile head and helmet views.
- `batch20-mesh-inspection.json`: geometry/paint/floor, eye fit, exact saved body
  hashes, closed state modules, shield colours/grip and matching sex tiles.
- `batch20-protected-assets.json`: 64 previous FBXs (60 creature/player,
  three objects and the shared tile quad).
- `Batch20-Unreal-fixtures.png`: actual live engine capture.

`CreateCreatureBatch20.py` generates these derivatives. Use
`RenderCreatureBatch20.py`, `ReviewCreatureBatch20.py` and
`InspectCreatureBatch20.py` to inspect saved work. `ImportCreatureBatch20.py`
targets only the three new meshes. `VerifyCreatureBatch20.ps1` exercises six
displayed sex forms and their six official tile fallbacks, unknown identity,
paint buffers, real F9 switches without changing native turn/sequence, map and
8x zoom. Both live placement and fixtures use 15-degree humanoid orientation.
Selection uses displayed identity only, preserving the perception boundary.
Fixture expectations now normalise spaces, hyphens and case like the asset
keys, covering `Uruk-hai` and `orc-captain` correctly.

Saved geometry/paint/floor/eye/ancestry/closed-module checks, editor build and
all three targeted imports pass. All 64 earlier exports retain their hashes.
Six studio views, six heads, all 18 true 16x16 candidates and the actual engine
capture were inspected; all three fixtures are clearly visible with paint and
cast shadows. All six displayed sex forms, their six official tile fallbacks,
unknown identity and paint buffers pass. Both real F9 switches preserve turn
5/input sequence 7; native map, hero centring and 8x zoom pass. Evidence:
`build-creature-batch20-{blender,review,inspect,unreal,import,live}.log`.

Current inventory: 59 completed creatures + one completed player role + 322
remaining creatures + 12 remaining roles = 394 unique source identities.
There are 63 creature/player physical forms (59 primary creatures, two extra
female creature appearances and two human players). Three objects remain
separate. Static-draft coverage is **59/381 creatures = 15.5%**, or **60/394
creature/player identities = 15.2%**; finishing/rigging/animation is separate.
Next suggested family extension: orc mummy and orc zombie, reviewing both sex
tiles, state modules and source traits before ancestry reuse.

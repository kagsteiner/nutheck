# Hobgoblin, hill orc and Mordor orc

Batch 18 adds three editable, vertex-painted, unrigged static drafts. Matching
male/female source tiles support one shared appearance per identity.

## Source and interpretation

| Identity | Source / official tiles | Source traits |
| --- | --- | --- |
| `PM_HOBGOBLIN` | `monsters.h:734`; 146/147 | Level 1, difficulty 3, one 1d6 weapon attack; no innate resistance |
| `PM_HILL_ORC` | `monsters.h:752`; 150/151 | Level 2, difficulty 4, one 1d6 weapon attack; poison resistance |
| `PM_MORDOR_ORC` | `monsters.h:761`; 152/153 | Level 3, difficulty 5, one 1d6 weapon attack; poison resistance |

All three are strong, collecting, omnivorous orc humanoids, with infravision and
infravisibility. Hill/Mordor orcs also have greedy/jewel flags and large-group
generation. Abstract `MZ_HUMAN` does not specify a literal metre height.
NetHack retains all combat, resistance and behaviour distinctions.

The hobgoblin tile closely follows the goblin, with yellow rather than green
eyes, magenta clothing and brown/tan masses. Hill/Mordor orcs instead share an
upright silhouette and pale headwear. Hill orc has peach/brown skin, green/lime
clothing and brown footwear/held rod. Mordor orc has blue-gray skin/footwear,
magenta clothing, red accents and a cyan held rod. Both have a pale diagonal
held detail. The large offset black mass on the right/below is cast shadow;
spatial masks exclude exterior black while retaining enclosed dark details.
Original source comparison tiles remain unmodified.

Hidden anatomy, back views, exact stature, helmet construction and complete
costume/equipment shapes are artistic interpretations. The existing goblin
construction supplies the hobgoblin's face/cap and separate dagger cue. The
upright pair use simple separate rods and small pale blades; these are tile
interpretations, not guarantees about a live monster's inventory. The retained hobgoblin cape is an earlier goblin art interpretation, not new
evidence from the shadow. No hidden inventory, heraldry, faction insignia or
axe head is inferred.

## Geometry and reuse

`OrcFamily.py` appends the saved goblin collection for hobgoblin, retaining all
local mesh vertices and applying object stature factors 1.06 / 1.05 / 1.10.
Yellow iris paint distinguishes its source appearance. Tiny degenerate ear
faces inherited from the saved goblin are removed in this derivative only;
vertex signatures are retained and the earlier goblin stays unchanged.

Hill and Mordor orcs share a new upright body, helmet and costume geometry.
Short strong limbs, a complete jaw/nose and rounded ears give them a different
silhouette from the goblin-derived hobgoblin. Paired eyes sit against the skull.
Tunic/belt have closed thickness; sleeves cover shoulders and the lower tunic
covers the hip transition. Held pieces remain separate editable objects.
Both continuous-body vertex hashes match exactly; state differences are paint.

Paint uses `FLOAT_COLOR` on `CORNER`, through the established shared miniature
materials. These are static drafts: anatomy/face, garment edges, equipment
refinement, rigs, animation, LODs and runtime cost remain finish work.

## Artifacts and validation

- `Art/CreatureInterpretations/CreatureBatch18.blend`: three editable collections
  and saved studio, with hobgoblin initially visible.
- `hobgoblin.fbx`, `hill_orc.fbx`, `mordor_orc.fbx`: painted exports.
- `Batch18-SourceReview.png`: all six official sex tiles plus goblin reference.
- `Batch18-Models.png` / `MeshComparison-batch18.png`: actual models, front/rear,
  source tiles and best true 16x16 candidates.
- `Batch18-Projections.png` / `projection-report-batch18.json`: all 18 actual
  tiny camera candidates, bounds and shadow masks. Overlap is diagnostic only.
- `Batch18-EyeReview.png`: saved front/profile heads for each identity.
- `batch18-mesh-inspection.json`: saved geometry, paint, floor, eye fit,
  closed clothes, ancestry hashes and protected preceding exports.
- `batch18-protected-assets.json`: 58 earlier FBX hashes (54 creature/player,
  three objects and the shared tile quad).
- `Batch18-Unreal-fixtures.png`: actual live engine capture.

`CreateCreatureBatch18.py` generates the batch. Fresh generation includes the
review corrections. `RefineCreatureBatch18.py` was a one-time saved garment/ear
repair; use `RenderCreatureBatch18.py`, `ReviewCreatureBatch18.py` and
`InspectCreatureBatch18.py` to inspect existing assets. `ImportCreatureBatch18.py`
imports only the three new meshes; `VerifyCreatureBatch18.ps1` checks all six
displayed sex cases, their official tile fallbacks, unknown identity, paint,
real F9 switches without a native turn/sequence change, map and 8x zoom.
The humanoid orientation is 15 degrees. Selection uses displayed canonical
identity/sex only, preserving player ancestry guards and perception boundaries.

Saved geometry/paint/floor/eye-fit/closed-cloth checks pass. The hobgoblin's
saved local vertex signatures match the original goblin, including repaired
ear vertices; hill/Mordor body hashes match exactly. All 58 preceding exports
remain unchanged. Native triangles: 55,610 hobgoblin / 101,692 hill orc /
101,692 Mordor orc. No production performance budget is claimed.

Editor build and all three targeted imports pass, with vertex-colour buffers.
All six displayed sex cases, six official tile fallbacks and unknown identity
pass. Both real F9 switches preserve turn 5/input sequence 7; native map,
hero centring and 8x zoom pass. Six studio views, six heads, all 18 true 16x16
candidates and the final actual engine capture were inspected. The first live
capture partly hid Mordor orc behind a wall; the retained final capture shows
all three fixtures clearly. Evidence:
`build-creature-batch18-{blender,refine,review,inspect,unreal,import,live}.log`.

Current inventory: 53 completed creature identities + one completed player role
+ 328 remaining creatures + 12 remaining roles = 394 unique source identities.
There are 57 physical creature/player forms (53 primary creatures, two extra
female creature appearances and two human players), plus three separate objects.
Verified static-draft coverage is **53/381 creatures = 13.9%**, or **54/394
creature/player identities = 13.7%**. These percentages exclude finishing,
rigging, animation and the separate object/terrain inventories. Next suggested
batch: Uruk-hai, orc shaman and orc-captain, after sex-tile/anatomy review.

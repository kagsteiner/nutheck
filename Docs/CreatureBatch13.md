# Kobold, large kobold and kobold leader

Batch 13 establishes a parameterised kobold family. The three creatures have
editable painted Blender geometry, independent FBX exports and verified Unreal
selection. They are unrigged static drafts. All 38 preceding creature/player
FBX files match their pre-batch SHA-256 hashes.

## Source and interpretation

The selected records are `PM_KOBOLD`, `PM_LARGE_KOBOLD` and `PM_KOBOLD_LEADER`
in the pinned NetHack 5.0 catalogue, `include/monsters.h:624–647`.
All have small source size, humanoid/omnivore traits, poison resistance,
hostility, collection and infravision. Base levels are 0/1/2; weapon attacks
are 1d4/1d6/2d4. The leader also has the lord flag. The encyclopedia describes
small humanoids with vaguely dog-like faces. Source sizes and weight are not
literal miniature dimensions.

| Identity | Official tiles | Interpretation |
| --- | --- | --- |
| Kobold | 122/123 | Blue/cyan body, short dog-like muzzle, dark eyes and pale upright ear tips |
| Large kobold | 124/125 | Same palette, longer limbs and independently broader torso and head |
| Kobold leader | 126/127 | Broader compatible body, separate orange hood/tunic and muted blue-gray belt |

The tiles' actual blue pigment is used instead of the brown/red ASCII colours.
Their white upper pixels are interpreted as pale ear tips, not helmet horns.
Orange pixels surrounding the leader's face/torso support an open hood and
tunic. Bare blue anatomy on the other two and the exact garment construction
are artistic assumptions. No tail, crown, shield or held weapon is inferred.
The weapon attack does not establish an actual visible inventory item.
Male/female tile pairs are identical; both displayed sexes use the same body.

The large black mass to the right is offset from the coloured body and continues
below/behind it. It is treated as cast shadow, not a second body, cape, shield
or tail. Projection diagnostics use a spatial background flood to exclude the
external black fringe while retaining enclosed black face/body details. Original
tiles remain untouched on the comparisons. Ambiguous dark pixels and silhouette
IoU are approximate diagnostics, not evidence of exact reconstruction.

## Geometry and review

`KoboldFamily.py` varies height, chest width, head width and arm spread
independently. Continuous sculpted anatomy includes torso, neck, skull, muzzle,
jaw, jointed limbs, hands and feet. Paired dark eyes overlap the actual skull,
with upper/lower skin lids. Pale ear tips are vertex paint on the ears themselves.
The blue surface is interpreted as skin; no unsupported fur, scales or separate
coat overlays were added. The approved texture-only fur direction remains for
future models with a supported fur interpretation.

Initial review corrected pinched arm joints and detached-looking tip geometry.
A saved-scene repair then replaced only the leader's intersecting tunic and
rectangular belt with oval cloth shells. `RefineCreatureBatch13Garment.py` is a
one-time repair; the family generator already contains the final construction.
Do not repeat this repair for inspection. `RenderCreatureBatch13.py` and
`ReviewCreatureBatch13.py` render existing saved geometry without rebuilding it.
Cloth and rank pieces remain separate editable objects. They represent the tile,
not dynamically equipped clothing; the player fixed-clothing rule is unchanged.

Native triangle counts: kobold 54,596; large kobold 54,916; leader 61,876.
These are draft costs, not a reviewed production performance budget.

## Artifacts and validation

- `Art/CreatureInterpretations/CreatureBatch13.blend`: separate editable
  collections, corner paint and studio setup, initially showing kobold.
- `kobold.fbx`, `large_kobold.fbx`, `kobold_leader.fbx`: actual mesh exports.
- `Batch13-Models.png`: actual three-quarter model renders.
- `MeshComparison-batch13.png`: official tiles, actual 16×16 best candidates,
  front-quarter and rear renders.
- `Batch13-Projections.png` and `projection-report-batch13.json`: all 18 true
  16×16 candidates, spatial masks, bounds and camera diagnostics.
- `Batch13-EyeReview.png`: six actual front/profile head renders.
- `batch13-mesh-inspection.json`: saved paint, finite/nonzero geometry,
  floor clearance, paired eyes and surface distances, painted ear tips,
  separate rank modules, independent proportions and previous-export checks.
- `batch13-protected-assets.json`: pre-batch hashes for 36 creatures and two players.
- `Batch13-Unreal-fixtures.png`: actual live capture with entity labels hidden.

The editor build and targeted `ImportCreatureBatch13.py` passed. Three imports
logged `SCULPTED_CREATURE_IMPORTED`, then `SCULPTED_CREATURES_READY count=3`;
vertex paint and assigned miniature materials passed validation. The corrected
leader FBX was written before its final import. The full importer now supports
41 forms. No prior mesh was regenerated or reimported.

`VerifyCreatureBatch13.ps1` passed six displayed sex forms, six fallback cases,
unknown identity and paint buffers. Real F9 switching both ways kept turn 5
unchanged. Native movement/map, hero centring and 8× zoom passed. Runtime model
selection uses displayed identity only, with 15-degree yaw for the -Y-facing
kobolds. F7, the first-person camera curve and hero ancestry guards are retained.
The fixture capture was inspected: all three new forms are visible without badges.

Logs: `build-creature-batch13-{blender,refine,renders,review,inspect,unreal,import,live}.log`.

## Remaining work

Further anatomy/face/cloth refinement, smoother hood transitions, hand/toe
detail, rigs, gait/combat/casting animation, dynamic equipment rules, LODs and
performance review remain finishing work. No hidden inventory, sex-specific
anatomy, production readiness or animation is claimed.

Inventory: 39 verified creature drafts and two player forms, 41 physical forms.
The 394 source identities comprise 39 completed creatures, one completed player
role, 342 remaining creatures and 12 remaining roles. Suggested next family
batch: kobold shaman, kobold mummy and kobold zombie, with separate caster and
undead changes after tile review.

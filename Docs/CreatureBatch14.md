# Kobold shaman, kobold mummy and kobold zombie

Batch 14 extends the reviewed kobold family with caster and undead states.
All three have editable Blender geometry, painted FBX exports, inspected studio
and 16×16 views, targeted Unreal imports and live mapping/fallback validation.
They remain unrigged static drafts.

## Source facts and artistic assumptions

| Identity | Pinned source / tiles | Traits and interpretation |
| --- | --- | --- |
| `PM_KOBOLD_SHAMAN` | `monsters.h:649`; tiles 128/129 | Small level-2 humanoid, poison resistant, magical spell attack. Blue dog-faced ancestry with yellow hood/tunic from the actual tile |
| `PM_KOBOLD_MUMMY` | `monsters.h:1901`; tiles 384/385 | Small level-3 breathless/mindless undead, 1d4 claw attack, cold/sleep/poison resistance. Pale separate linen wraps over warm exposed skin |
| `PM_KOBOLD_ZOMBIE` | `monsters.h:2421`; tiles 490/491 | Small level-0 breathless/mindless stalking undead, 1d4 claw attack, cold/sleep/poison resistance. Blue skin with broad green discoloration matching the principal source colour masses |

The mummy and zombie have no-corpse generation flags; those and all combat
traits remain native gameplay distinctions. Abstract size/weight do not define
literal miniature dimensions. Each male/female tile pair is identical, so no
sex-specific anatomy has been invented.

Source tiles retain the family's dog-like face and pale upright ear tips.
The shaman's yellow surroundings support caster clothing, not yellow skin or
an invented staff. No weapon, crown, magical aura or held equipment is inferred
from the offset black shape. The mummy's white/gray bands and peach accents
support wraps and exposed skin; the exact winding pattern is an interpretation.
Small isolated pale/gray pixels and the red torso fleck are ambiguous. No extra
limb or graphic wound was added. The zombie's small blue/violet/orange accents
remain refinement targets; they do not establish equipment or exposed bones.

All three have the same offset right/bottom black cast-shadow pattern as the
earlier kobolds. Projection masks exclude external background-connected black
regions while retaining enclosed dark face/body detail. Original tiles remain
untouched on the comparisons. These are diagnostic masks, not exact segmentation
or claims of pixel-perfect reconstruction.

## Reuse and construction

`KoboldStates.py` appends saved geometry from `CreatureBatch13.blend`.
The shaman reuses the leader body and separate garment pieces, recoloured yellow.
The mummy and zombie reuse the large-kobold ancestry body. Saved vertex hashes
match those reference bodies exactly; prior source scenes and exports were not
regenerated or modified. Eyes, short muzzles, pale ear tips, limbs and feet are
preserved. State paint is encoded per corner on continuous anatomy.

The mummy adds 14 independently editable solid linen ribbons around the head,
torso and limbs. Rays fit their surfaces to the actual saved body; thickness
is 1.5 mm, with final surfaces within 4.5 mm of the anatomy. Closed topology,
nonzero faces and floor clearance pass. Early review found foot bands following
the ankle and creating spikes. `RefineCreatureBatch14Wraps.py` replaced only
the saved wrap pieces, narrowing foot bands to the forefoot and revising jaw/
crown wrapping while keeping the eyes clear. Fresh generation already uses
the corrected construction. Do not repeat this one-time repair for inspection.

The zombie changes skin paint rather than adding raised wound blobs or an
unrelated body. Neither new undead form is a uniformly rescaled human model.
The current static stance is inherited; undead gait/deformation and caster
animation remain future work. No unsupported fur or scales were added.

Native triangle counts: shaman 61,876; mummy 71,348; zombie 54,916.
These are draft costs, not validated production budgets.

## Artifacts and repeatable review

- `Art/CreatureInterpretations/CreatureBatch14.blend`: three editable
  collections, corner paint and studio; shaman initially visible.
- `kobold_shaman.fbx`, `kobold_mummy.fbx`, `kobold_zombie.fbx`: actual exports.
- `Batch14-Models.png`: actual three-quarter model renders.
- `MeshComparison-batch14.png`: official tiles, best true 16×16 projections,
  actual front-quarter and rear views.
- `Batch14-Projections.png` / `projection-report-batch14.json`: all 18 true
  16×16 candidates, camera diagnostics, spatial masks and bounds.
- `Batch14-EyeReview.png`: six front/profile head/wrap views.
- `batch14-mesh-inspection.json`: paint, finite/nonzero geometry, floor,
  eye fit/symmetry, closed fitted wraps and exact ancestry body hashes.
- `batch14-protected-assets.json`: hashes for all 45 preceding exports:
  41 creature/player forms, three objects and the tile-fallback quad.
- `Batch14-Unreal-fixtures.png`: inspected live capture with labels hidden;
  all three forms are visible.

Generate with Blender background mode/four threads and
`CreateCreatureBatch14.py`. For saved inspection use `InspectCreatureBatch14.py`,
`ReviewCreatureBatch14.py` and `RenderCreatureBatch14.py`. The two comparison
scripts assemble actual geometry renders and official source pixels.

## Unreal and verification

The editor build and three targeted imports pass. Vertex paint and shared
miniature materials are validated. Full import now supports 44 creature/player
forms; object assets and tile-fallback assets remain separate. Runtime selection
uses only displayed neutral identity/sex, with 15-degree yaw for these -Y-facing
kobolds. No hidden monster/world lookup was introduced.

`VerifyCreatureBatch14.ps1` passes six displayed sex forms, six fallbacks,
unknown identity and paint-buffer checks. It additionally verifies all six
official tile cards for the new forms in the default style, using their source
male/female tile indices. Two real F9 switches preserve turn 5 and input
sequence 7. Native movement/map, hero centring and 8× zoom pass. The engine
capture, six studio views, six head views and all 18 tiny projections have
been inspected. Previous 45 export hashes match.

Evidence: `build-creature-batch14-{blender,refine,renders,review,inspect,unreal,import,live}.log`.

## Status and remaining work

The 394-ID inventory now contains 42 completed creature drafts, one completed
player role, 339 remaining creatures and 12 remaining roles. There are 44
physical creature/player forms, plus the separately tracked three object assets.
Suggested next family batch: gnomish wizard, gnome mummy and gnome zombie.

Finishing remains separate: face/cloth transitions, finer linen folds/loose
ends, zombie colour accents and decay/pose refinement, caster/undead animation,
spell effects, rigs, LODs and performance. Existing player fixed-clothing rules,
F7, F9, ancestry guards, first-person camera and general tile fallback are preserved.

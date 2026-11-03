# Cave spider, giant spider and scorpion

Batch 24 follows the next suggested creature queue. Three identities have three
editable static forms; each official male/female tile pair is identical and
shares its model. This does not infer additional sex anatomy. Static poses are
the intended presentation; animation and rigs remain outside product scope.

## Source and art interpretation

| Identity | Source / official tiles | Native traits |
| --- | --- | --- |
| `PM_CAVE_SPIDER` | `monsters.h:940`; 192/193 | Level 1, difficulty 3; 1d2 physical bite; tiny, concealing, small groups |
| `PM_GIANT_SPIDER` | `monsters.h:956`; 196/197 | Level 5, difficulty 7; 2d4 poison bite; large, strong, poisonous |
| `PM_SCORPION` | `monsters.h:964`; 198/199 | Level 5, difficulty 8; two 1d2 physical claws and 1d4 poison sting; small, concealing, poisonous |

All are hostile, oviparous, carnivorous animals without grasping hands, with
poison resistance/conveyance. Cave spider lacks the giant spider's poisonous-body
flag and poison attack. Source size is abstract, not literal metre dimensions.
No native rules, generation, movement, combat or poison behavior were changed.

Actual source palettes guide the models: cave spider is blue-gray with cyan
accents, giant spider is brown/orange, and scorpion is brown/orange. All retain
green eye accents and small red mouth/claw/sting cues. Giant spider's magenta
ASCII colour and scorpion's red ASCII colour are not their body pigments.

The two spiders share a complete cephalothorax/petiole/abdomen family, with
independent dimensions, height and leg reach. Giant spider has a much larger,
broader abdomen and cephalothorax; it is not a uniformly scaled recolour. Each
has eight walking legs rooted in the cephalothorax, paired pedipalps, two
cheliceral fangs and small posterior spinnerets. Two green primary eyes follow
the tile cue; six tiny secondary dark eyes complete an interpreted eye layout.
The exact eye arrangement, spinnerets, joints and hidden anatomy are artistic
assumptions, not a reconstruction of a named real spider species.

Scorpion has a separate prosoma/mesosoma body, six simplified dorsal plates,
eight walking legs, two articulated pedipalp claws with genuinely separated
fingers, five editable tail segments, overlapping joint masses, telson and
curved sting. The tail arches forward above the back. Green eyes are fitted to
the carapace. Plate simplification, claw shape, tail pose and precise segmentation
are miniature-art choices; claws are anatomy, not live inventory equipment.

Offset black tile fringes are excluded spatially from projection diagnostics,
with enclosed dark details retained. Original tiles stay unmodified. Those masks
and silhouette overlap are approximate diagnostics, not proof of anatomical
truth. No shadow-derived limbs, static web, aura, poison cloud or wound state
was added. Native display continues to determine what the player can perceive.

## Geometry and artifacts

`ArachnidFamily.py` parameterises compatible spiders and constructs scorpion
independently. Objects are closed geometry with `FLOAT_COLOR` / `CORNER` paint
and complete rear/underside surfaces. Feet clear the floor by about 11–14mm.
Ground origins and metres follow the established export pipeline. There is no
animation, alpha-card anatomy or hidden-state material effect.

Native triangle costs: 26,544 each spider / 22,128 scorpion. Leg/root and joint
transitions, eye/fang detail, scorpion plate/tail-joint refinement, paint finish,
tiny-scale readability and LOD/runtime budgets remain visual finishing work.

- `Art/CreatureInterpretations/CreatureBatch24.blend`: three editable collections,
  saved paint and studio; cave spider initially visible.
- `cave_spider.fbx`, `giant_spider.fbx`, `scorpion.fbx`: canonical painted exports.
- `Batch24-SourceReview.png`: all six original official sex tiles.
- `Batch24-Models.png` / `MeshComparison-batch24.png`: actual front/rear models,
  original tiles and best true 16x16 reverse projections.
- `Batch24-Projections.png` / `projection-report-batch24.json`: all eighteen
  actual tiny camera renders, bounds and spatial shadow exclusions.
- `Batch24-HeadReview.png` / `Batch24-UndersideReview.png`: six face/profile and
  three underside views showing eight-leg construction and scorpion claws/tail.
- `batch24-mesh-inspection.json`: saved finite/nonzero/closed topology, valid
  paint/floor, eight legs, eye symmetry, fangs/pedipalps, independent spider
  proportions, four pincer fingers, six plates, five tail segments and telson.
- `batch24-protected-assets.json`: 86 preceding canonical FBX exports, unchanged.
- `Batch24-Unreal-fixtures.png`: actual final live fixture capture. The first,
  wall-obscured capture is retained as `Batch24-Unreal-fixtures-first.png`.
- `batch24-save-preservation.json`: complete played-session/runtime hash audit.

`CreateCreatureBatch24.py` builds only this trio. `RenderCreatureBatch24.py`
rerenders saved work; optional `-- <key>` refreshes selected forms and merges
the projection report. `ReviewCreatureBatch24.py` renders faces/undersides, and
`InspectCreatureBatch24.py` audits saved geometry and previous exports.
`ImportCreatureBatch24.py` targets only these three meshes.

Saved native inspection, editor build and three imports/colour buffers pass.
All six studio views, six face views, three undersides and eighteen true tiny
renders were inspected. The final live capture shows all three fixtures clearly.
Live checks cover six displayed sex aliases, six
official tile fallbacks, unknown identity and paint buffers. Both actual F9
switches preserve native turn/input sequence; native map, hero centring and 8x
zoom pass. Both normal and preview placement use -75-degree yaw. Runtime selection
uses only displayed canonical identity and sex. Evidence is in
`build-creature-batch24-{blender,review,inspect,unreal,import,live}.log`.

## Saves and inventory

Required verified backup:
`Backups/NetHackSaves/20261102T154654.148400Z.zip`. Final audit confirms all
1,090 baseline player/runtime files, complete file set and LastSession pointer
are unchanged. No native backend was rebuilt. Capture tests use fresh isolated
`Saved/NetHackCaptures` sessions with `Remember=false`; no played session was
resumed, advanced, stopped or replaced.

**72 of 381 creatures = 18.9%** have verified static drafts. Including the
completed Valkyrie role gives **73 of 394 creature/player identities = 18.5%**.
Inventory: 72 completed creatures + one completed role + 309 remaining creatures
+ 12 remaining roles = 394 IDs. There are 78 creature/player forms (72 primary,
four additional female creature appearances, two human players). Four objects
and two terrain-feature identities / six terrain forms stay separate. These
percentages describe draft coverage, not visual finishing or the whole game-art
inventory. The object source inventory and manual checklist remain unchanged.

Next suggestion: gecko, iguana and lizard. Review both sex tiles/source traits,
construct a compatible reptile family with distinct digits/head/tail proportions,
and do not assume the existing amphibian newt is an interchangeable reptile body.

The user's priority that divine-gift weapons must look amazing is recorded in
the object art direction/backlog for their later review. This batch adds no
weapon designs. Preserve the deferred object-art work, altar/shopkeeper and
winged-insect assets, F7/F9/camera, fixed player clothing, full status HUD,
high walls/floor/doors, tile fallback and DX12/SM6 shadows.

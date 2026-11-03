# Killer bee, queen bee and xan

Batch 23 completes the next suggested trio as static flight drafts. There are
three source identities and three physical forms. Actual male/female tile
pairs are identical for each identity. Both bee species have `M2_FEMALE` in
native rules; testing both displayed aliases does not claim that normal
gameplay generates male bees. Xan has no fixed-sex flag.

## Source and interpretation

| Identity | Source / official tile pair | Native traits |
| --- | --- | --- |
| `PM_KILLER_BEE` | `monsters.h:96`; 2/3 | Level 1, difficulty 6; 1d3 poison sting; hostile, female, large groups |
| `PM_QUEEN_BEE` | `monsters.h:126`; 10/11 | Level 9, difficulty 12; 1d8 poison sting; hostile, female, oviparous, prince flag, special generation |
| `PM_XAN` | `monsters.h:1157`; 238/239 | Level 7, difficulty 9; 1d4 leg-targeting sting; hostile and infravisible |

All three fly, lack grasping hands, have poisonous-body flags and poison
resistance/conveyance, and are abstractly tiny. Source size does not specify
literal metre dimensions. NetHack remains authoritative for flight, poison,
leg injury, combat, generation and turns.

Bee tiles show brown head/thorax/legs, cyan eyes, yellow/black abdomen bands
and blue-gray wings with warm root pixels. Queen has a larger, lower abdomen,
broader wings and longer leg reach. The prince flag is not evidence for a
crown; none was added. Two closed forewings and two smaller hindwings per bee
complete an insect wing plan. Fine thoracic fuzz uses only the approved shared
fur texture. Abdomen stripes are vertex paint on a continuous surface.

The source encyclopedia describes xan as a mosquito. Its actual tile is
green with white eyes, dark pupils and yellow extensions, despite red ASCII
colour. It therefore has separate slender anatomy: raised green abdomen,
large white/dark eyes, yellow long legs, one paired set of pale gold wings,
two small balancing knobs, antennae and a pointed green proboscis. The yellow
tile extensions do not resolve every leg/wing boundary; the exact wing shape,
haltere completion, proboscis and six-leg placement are artistic interpretation,
not a literal zoological species reconstruction. No bee stripes, extra bee
wings, red body paint or invented poison effect was added to xan.

The killer-bee shadow is detached at rows 13–14; rows 12–15 are excluded from
its projection mask. Queen's bottom black shadow at row 14 is excluded while
actual feet/abdomen bands above it remain. Xan's black lower/right mass is cast
shadow; its two enclosed pupil pixels are retained explicitly. Original source
images remain unmodified. Spatial masks and overlap scores are diagnostics,
not proof of exact reconstruction.

## Construction and review

`WingedInsects.py` parameterises the two bees. Queen's thorax dimensions,
abdomen length/width/depth and tilt, wing span/chord and leg reach vary
independently. The head remains the same size. Each form has six jointed legs
rooted in the thorax, paired antennae/eyes/mandibles and one static sting.
Xan uses a separate body plan and proboscis attack cue instead of a rear sting.

Wings are closed, thin swept solids with slightly curved upper/lower surfaces,
minimum nominal 3mm normal thickness, capped tips and small closed veins. They
cast real shadows and use opaque paint, with no alpha cards or animation.
Bee hover clearance is about 187mm; xan clearance is about 158mm. Exact scale,
flight pose and hidden anatomy are miniature presentation choices.

Paint uses `FLOAT_COLOR` / `CORNER` in Blender and UE. Native draft costs are
32,220 triangles per bee and 12,088 for xan. `RefineCreatureBatch23Bands.py`
records the saved review correction: denser pigment sampling and full dark
bands remove the initial jagged colour boundary without raised stripe objects.
Fresh generation already contains that correction. Do not repeat the repair
merely to inspect; use saved Render/Review scripts.

Wing-root transitions, vein/eye detail, thorax texture flow, stinger/leg
refinement, distant readability and LOD/runtime cost remain finishing work.
Static presentation is intended; no rig or animation is required.

## Artifacts and checks

- `Art/CreatureInterpretations/CreatureBatch23.blend`: three editable collections,
  saved paint/materials and studio; killer bee initially visible.
- `killer_bee.fbx`, `queen_bee.fbx`, `xan.fbx`: canonical painted exports.
- `Batch23-SourceReview.png`: all six original sex tiles.
- `Batch23-Models.png` / `MeshComparison-batch23.png`: actual front/rear models,
  original source tiles and best true 16x16 reverse projections.
- `Batch23-Projections.png` / `projection-report-batch23.json`: all eighteen
  actual tiny camera renders and explicit spatial mask exclusions.
- `Batch23-HeadReview.png` / `Batch23-UndersideReview.png`: six actual head views
  and three underside views showing wing/leg construction.
- `batch23-mesh-inspection.json`: saved closed topology, valid paint/floor,
  hover clearance, six thoracic legs, paired eyes, four/two wings, symmetry,
  bee fur UV/material, painted bands and independent queen proportions.
- `batch23-protected-assets.json`: all 83 preceding canonical exports, unchanged.
- `Batch23-Unreal-fixtures.png`: actual live capture with all three forms visible.
- `batch23-save-preservation.json`: complete played-session/runtime audit.

Editor build, three targeted imports, colour buffers and saved native checks
pass. All six studio views, six head views, three undersides and eighteen tiny
projections were inspected, followed by the actual engine capture. Live checks
pass six displayed aliases and their six official fallbacks, unknown identity,
vertex paint and bee fur/UV materials. Actual F9 switching both ways preserves
turn 5 / input sequence 7. Native map, hero centring and 8x zoom pass. Selection
uses only displayed identity/sex; live and preview yaw are -75 degrees.

`CreateCreatureBatch23.py` builds only this trio. `RenderCreatureBatch23.py`
rerenders saved work; optional `-- <key>` refreshes selected forms and merges
the report. `ReviewCreatureBatch23.py` inspects heads/undersides;
`InspectCreatureBatch23.py` audits saved geometry and prior exports.
`ImportCreatureBatch23.py` targets only these three meshes, and
`VerifyCreatureBatch23.ps1` launches an isolated capture.
Evidence: `build-creature-batch23-{blender,refine,renders,review,inspect,unreal,
import,live}.log`. Preserve the existing altar/shopkeeper integration,
F7/F9/camera, fixed player clothing, full status HUD, walls/floor/doors,
tile fallback and DX12/SM6 shadows.

## Saves and completion

Required verified backup:
`Backups/NetHackSaves/20261102T150827.273748Z.zip`. The final audit confirms
all 1,090 baseline files, complete file set and LastSession pointer are
unchanged. No native backend was rebuilt. Tests use a fresh
`Saved/NetHackCaptures` root with `Remember=false`; no played session was
resumed, advanced, stopped or replaced.

**69 of 381 creatures = 18.1%** have generated and verified static drafts.
Including the completed Valkyrie role gives **70 of 394 creature/player
identities = 17.8%**. The inventory is 69 completed creatures + one completed
player role + 312 remaining creatures + 12 remaining roles = 394 unique IDs.
There are 75 creature/player forms (69 primary + four female variants + two
human players). Four objects and two terrain-feature identities / six terrain
forms remain separate. These percentages measure draft coverage, not visual
finishing or the full game-art inventory.

Next suggestion: cave spider, giant spider and scorpion. Review both sex tiles
and source traits; reuse a compatible spider family, while scorpion requires
its own pincers, segmented tail and stinger construction.

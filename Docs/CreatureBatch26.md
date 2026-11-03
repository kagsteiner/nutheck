# Garter snake, snake and water moccasin

Three static drafts follow the suggested queue. Each official male/female pair
is identical and shares a form. No additional sex anatomy is inferred.

| Identity | Source / official tiles | Native traits |
| --- | --- | --- |
| `PM_GARTER_SNAKE` | `monsters.h:2167`; 438/439 | Level 1, difficulty 3; 1d2 physical bite; tiny; large-group generation; no hostile flag |
| `PM_SNAKE` | `monsters.h:2176`; 440/441 | Level 4, difficulty 6; 1d6 poisonous bite; small; hostile, poison resistance/conveyance |
| `PM_WATER_MOCCASIN` | `monsters.h:2185`; 442/443 | Level 4, difficulty 7; 1d6 poisonous bite; small; hostile, poison resistance/conveyance; no ordinary random generation |

All are swimming, concealing, limbless, slithy, oviparous carnivores unable to
take objects. Abstract source size is not a literal metre measurement. The
native backend, combat, generation and perception rules remain unchanged.

Original tiles show orange-brown garter/ordinary snakes and a black water
moccasin, despite green/brown/red ASCII colours. Pale eye accents and green/red
tongue accents guide the models. The garter's blue-gray offset fringe is treated
as cast shading, not a blue body appendage. Spatial masks exclude exterior dark
fringes for the orange forms. The moccasin uses an explicit mask retaining every
non-background pixel: black is its actual body, not disposable shadow. Some
outline/shadow ambiguity remains; masks and silhouette overlap are diagnostics,
not proof of anatomy. Original tiles remain unmodified.

`Scripts/SnakeFamily.py` constructs sampled smooth coils with parallel-transport
cross sections, continuous raised necks, integrated closed heads and tapering
tails. Garter snake has the smallest slender body and narrow head. Ordinary
snake is heavier with a broader head. Water moccasin has a thick body and wider
cheeks. Independent dimensions and tail hooks avoid uniform recolouring.
Each has two pale lateral eyes with pupils, nostrils and a fine mouth seam.
Ordinary snake and water moccasin have small static forked tongues. There are
no limbs, cobra hoods, fins, display stands, venom clouds or hidden-state glows.

Exact pose, species anatomy, head proportions, subtle garter dorsal stripe,
ordinary-snake mottling and faint moccasin bands are artistic interpretations.
Paint is sampled continuously along the curved body; scale-like grain is pigment
rather than extruded beads. The common painted-miniature shader is retained.
These are verified static drafts. Head/neck integration, eye seating, ventral
scutes, scale finish, dark-body contrast and runtime LODs remain finishing work.
Animation and rigs are outside product scope. Native triangle costs are 59,776
garter snake / 78,208 snake / 98,232 water moccasin; LOD review remains necessary.

Artifacts under `Art/CreatureInterpretations/`:

- `CreatureBatch26.blend`: editable collections, saved paint and studio; garter snake initially visible.
- `garter_snake.fbx`, `snake.fbx`, `water_moccasin.fbx`: painted canonical exports.
- `Batch26-SourceReview.png`: all six original official tiles.
- `Batch26-Models.png`, `MeshComparison-batch26.png`: actual front/rear geometry and tile comparisons.
- `Batch26-Projections.png`, `projection-report-batch26.json`: eighteen true 16x16 camera projections and mask diagnostics.
- `Batch26-HeadReview.png`, `Batch26-UndersideReview.png`: actual saved face/profile/underside views.
- `batch26-mesh-inspection.json`: finite/nonzero/manifold geometry, connected body, paint, floor, eye/tail/head checks.
- `batch26-protected-assets.json`: all 92 preceding canonical exports, unchanged.
- `Batch26-Unreal-fixtures.png`: actual final isolated live capture.
- `batch26-save-preservation.json`: complete player/runtime hash audit.

Scripts `CreateCreatureBatch26.py`, `RenderCreatureBatch26.py` (saved rerender,
optional `-- <key>`), `ReviewCreatureBatch26.py`, `InspectCreatureBatch26.py`,
`CreateCreatureBatch26Comparison.py`, `ImportCreatureBatch26.py`,
`VerifyCreatureBatch26.ps1` and `AuditCreatureBatch26Saves.py` reproduce the work.
Evidence is in `build-creature-batch26-*.log`.

Saved topology/paint checks, actual studio/detail/tiny image inspection, Unreal
compile, three targeted imports, material assignments and colour buffers pass.
Live checks cover six displayed sex aliases, six official fallbacks, unknown
identity and paint buffers. Both actual F9 switches preserve turn/input sequence.
Native map, hero centring and 8x zoom pass. Runtime selection uses displayed
canonical identity/sex only; preview and normal forms use the established yaw.

Verified backup: `Backups/NetHackSaves/20261102T162533.043395Z.zip`. All 1,090
baseline player/runtime files, the complete file set and LastSession pointer
remain unchanged. No native backend was rebuilt. No played session was resumed,
advanced, stopped or replaced. Tests use fresh `Saved/NetHackCaptures` roots with
`Remember=false`. Existing players, controls, HUD, walls, floors/doors, perception
and object/terrain art remain preserved.

**78/381 creatures = 20.5%** have verified static drafts. Including completed
Valkyrie gives **79/394 = 20.1%**. Inventory: 78 creatures + one role + 303
remaining creatures + 12 remaining roles = 394. There are 84 physical forms
(78 primary creatures, four additional female forms and two human players).
Objects and terrain stay separate. Divine-gift weapon direction remains deferred
for the user's later review.

Next suggestion: python, pit viper and cobra. Inspect source traits and both sex
tiles; preserve constrictor proportions, viper head and cobra hood differences.

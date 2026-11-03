# Python, pit viper and cobra

The next suggested batch adds three verified static creature drafts. Each
official male/female pair is identical and shares its form; this does not infer
further sex anatomy. Source: pinned NetHack `include/monsters.h`.

| Identity | Source / official tiles | Native traits |
| --- | --- | --- |
| `PM_PYTHON` | line 2194; 444/445 | Level 6, difficulty 8; large, strong; physical bite/touch and wrapping/constricting hugs; infravision |
| `PM_PIT_VIPER` | line 2204; 446/447 | Level 6, difficulty 9; medium; two 1d4 poisonous bites; poison resistance/conveyance, infravision |
| `PM_COBRA` | line 2213; 448/449 | Level 6, difficulty 10; medium; 2d4 poisonous bite and blinding spit; poison resistance/conveyance |

All are hostile, swimming, limbless, slithy, oviparous carnivores unable to take
objects. Viper/cobra conceal; python lacks that flag. Abstract sizes do not
define literal dimensions. No movement, combat, wrapping, poison or spit rules
changed; no native backend was rebuilt.

## Source and interpretation

Actual tile colours guide the miniatures: brown/orange python with green eyes,
black pit viper with pale eyes, and black cobra with slate eye accents. Their
magenta/blue ASCII colours are not body paint. Explicit spatial masks retain
every non-background pixel of the two black species; dark anatomy is not
discarded as shadow. Python uses conservative coloured/enclosed-black masking.
Original tiles remain unchanged; tiny projection overlap is a rough diagnostic.

`AdvancedSnakeFamily.py` shares sampled tube construction with `SnakeFamily.py`
while building independent paths, girths, skull/snout dimensions and hood.
Python is a low, heavy double-coiled constrictor with a much larger footprint.
Viper has a broad head, narrower snout and paired facial pit marks. Cobra has
a thinner trunk, taller posture and a closed hood volume joined into the same
continuous sculpt as its neck and head; it is not a detached disc or fin.
Eyes are fitted to the actual saved head surface. Complete mouths, nostrils,
rear and underside geometry, tapering tails and small static red forked tongues
on viper/cobra finish the figures. No venom cloud, active spit effect or glow.

Exact species, eye/pupil layout, pit placement, subtle python saddles and coil
pose are artistic assumptions. The source icon does not resolve this anatomy.
The existing six snake/other reptile exports are preserved. No rigs or animation
are planned. Coil spacing, mouth/eye/pit seating, hood transition, scale paint
and LOD/runtime costs remain separate visual finishing work.

## Artifacts and checks

All art is under `Art/CreatureInterpretations/`:

- `CreatureBatch27.blend`: editable collections, saved corner paint and studio.
- `python.fbx`, `pit_viper.fbx`, `cobra.fbx`: canonical painted exports.
- `Batch27-SourceReview.png`: six original official sex tiles.
- `Batch27-Models.png`, `MeshComparison-batch27.png`: actual front/rear meshes and source comparison.
- `Batch27-Projections.png`, `projection-report-batch27.json`: eighteen actual 16x16 views and masks.
- `Batch27-HeadReview.png`, `Batch27-UndersideReview.png`: saved face/profile/interior-side geometry views.
- `batch27-mesh-inspection.json`: finite/nonzero/manifold geometry, connected bodies, floor, eyes, tails, pit marks, girth/head ordering and physical hood width.
- `batch27-protected-assets.json`: all 117 preceding canonical export hashes, unchanged.
- `Batch27-Unreal-fixtures.png`: final isolated live capture.
- `batch27-save-preservation.json`: complete played-save/runtime hash audit.

Native triangle costs: 170,132 python / 80,460 pit viper / 76,848 cobra.
Reusable scripts: `CreateCreatureBatch27.py`, `RenderCreatureBatch27.py`
(saved rerender with optional `-- <key>`), `InspectCreatureBatch27.py`,
`ReviewCreatureBatch27.py`, `CreateCreatureBatch27Comparison.py`,
`ImportCreatureBatch27.py`, `VerifyCreatureBatch27.ps1` and
`AuditCreatureBatch27Saves.py`. Evidence is in `build-creature-batch27-*.log`.

Saved geometry/paint checks, actual multiview/tiny inspection, editor build and
three targeted imports pass. Live checks cover six displayed sex aliases, six
official fallbacks, unknown identity and paint buffers. Both real F9 switches
preserve native turn/input sequence. Native map, hero centring and 8x zoom pass.
Mapping uses only displayed canonical identity and sex; normal and preview
models retain the established -75-degree orientation.

The first isolated capture passed creature checks but had insufficient revealed
floor for three preview fixtures; its log is retained as
`build-creature-batch27-live-insufficient-floor-first.log`. A subsequent passing
two captures partly hid fixtures behind walls; they are retained as
`Batch27-Unreal-fixtures-wall-obscured.png` and `-wall-obscured-2.png` with
matching logs. The final capture uses a larger isolated starting room (105
known cells). No wall height or verification condition was relaxed.

## Saves and inventory

Verified baseline: `Backups/NetHackSaves/20261102T201016.119063Z.zip`.
All 1,090 played-session/runtime files, the complete file set and LastSession
pointer remain unchanged. Tests use fresh `Saved/NetHackCaptures` roots with
`Remember=false`; no played session was resumed, advanced, stopped or replaced.
F7/F9/camera, fixed player clothing, high walls, floor/doors, status HUD and
native perception remain preserved. Existing armor/artifact designs are unchanged.

**81/381 creatures = 21.3%** have verified static drafts. Including completed
Valkyrie gives **82/394 = 20.8%**. Inventory balances: 81 creatures + one role +
300 remaining creatures + 12 remaining roles = 394. There are 87 physical forms
(81 primary creatures, four additional female appearances, two human players).
Objects/terrain and visual finishing stay separate.

Next suggestion: monkey, ape and carnivorous ape; review both sex tiles and source
traits first, preserving independent faces/hands/feet/proportions and monkey tail
versus tailless ape anatomy.

# Monkey, ape and carnivorous ape

Batch 28 follows the Session handoff's regular queue. Three independently
proportioned painted miniatures share the primate construction family. These
are static drafts; visual finishing and runtime/LOD work remain separate.

## Source and interpretation

Pinned `upstream/NetHack/include/monsters.h` provides the native traits:

| Identity | Official male/female tiles | Source traits |
| --- | --- | --- |
| `PM_MONKEY` | 478/479 | Small, level 2 / difficulty 4; omnivore; stealing claw and 1d3 bite |
| `PM_APE` | 480/481 | Large, level 4 / difficulty 6; strong omnivore; two 1d3 claws and 1d6 bite; small groups |
| `PM_CARNIVOROUS_APE` | 486/487 | Large, level 6 / difficulty 8; hostile, strong carnivore; two 1d4 claws and 1d8 hug |

All three are animal/humanoid and infravisible. Each official sex pair is
identical, so it shares one physical sculpt. No additional sex anatomy is
claimed. Native combat, stealing, grouping and disposition remain unchanged.

The official tiles show orange/brown coats and pale peach exposed areas;
gray/black ASCII colours are not coat instructions. The apes have blue eyes;
the monkey has dark eyes. The carnivorous ape retains a red mouth. Its isolated
red lower-left pixels are ambiguous and are not treated as blood or a held item.
Offset lower/right black pixels are cast shadow. The comparison mask retains
enclosed dark marks, excludes exterior fringe and is an approximate diagnostic,
not anatomical proof. Original tiles remain unmodified beside actual renders.

`PrimateFamily.py` supplies a complete connected torso/head/limbs, four separate
extremities with four fingers/toes and opposed thumb/big toe, rounded ears,
fitted eye patches, muzzle, nostrils, mouth, rear and underside. Monkey has
independent small proportions, an asymmetric raised hand and curved tail.
Both apes are tailless. Ape has long low arms; the broader carnivorous ape
reaches forward in a static embracing pose. Teeth, precise species, digits,
tail shape, hidden anatomy and poses are artistic completions. No stolen loot,
weapon or inventory promise was added. Fur is the approved texture-only
treatment, with paint on continuous surfaces and no hair/clump geometry.

Studio review caught angular joints caused by tube-frame changes. The final
family uses smooth interpolated paths and a continuously transported frame,
with rounded anatomical unions. Fresh generation contains the correction;
use saved Render/Review scripts for inspection, without regenerating old assets.

## Artifacts and verification

All artwork is under `Art/CreatureInterpretations/`:

- `CreatureBatch28.blend`: editable collections, corner paint, packed fur maps and studio.
- `monkey.fbx`, `ape.fbx`, `carnivorous_ape.fbx`: canonical painted static exports.
- `Batch28-SourceReview.png`: all six original official tiles.
- `Batch28-Models.png`, `MeshComparison-batch28.png`: actual front/rear mesh comparison.
- `Batch28-Projections.png`, `projection-report-batch28.json`: eighteen genuine 16x16 render candidates.
- `Batch28-HeadReview.png`, `Batch28-UndersideReview.png`: saved detail views; individual `*-head-hands.png` views show hands/feet.
- `batch28-mesh-inspection.json`: saved geometry, paint, connected body, closed solids, paired hands/feet, eye fit, UV/fur, distinct proportions and preceding export checks.
- `batch28-native-living.json`: native displayed identity, sex and tile results from six fresh isolated games.
- `batch28-unreal-assets.json`: imported material slots and colour verification.
- `Batch28-Unreal-fixtures.png`: isolated live engine capture.
- `batch28-protected-assets.json`, `batch28-save-preservation.json`: preserved export and played-save/runtime signatures.

Scripts follow the existing Prepare/Create/Inspect/Render/Review/Comparison/
Import/Verify/AuditCreatureBatch28 convention; native checks use
`Tests/BridgePrimates.py`. Evidence is in `build-creature-batch28-*.log`.
The targeted importer reuses existing Paint/Eye/Fur materials without rebuilding
shared shaders. Runtime selection uses only displayed canonical identity and sex;
animal orientation remains -75 degrees. Unsupported entities retain fallbacks.
The shared statue renderer can automatically reuse these canonical meshes as
white marble; no separate statue sculpt or creature identity is counted.

Saved inspection, final editor build, three targeted imports/material checks,
six native displayed sex cases, six live aliases and six official tile fallbacks
pass. Fur slots, UVs and colour buffers pass. Actual F9 toggles both ways retain
turn 4 / sequence 7. Native map, hero centring and 8x zoom pass. The final actual
engine capture was inspected with all three fixtures clearly visible.

Native triangle counts: 177,424 monkey / 219,592 ape / 275,000 carnivorous ape.
These are dense static drafts, with face/brow/eye/mouth and digit seating,
coat flow, compact source-pose readability and LOD/runtime costs still requiring
visual finishing. Tiny projections use front/oblique angles (-180/-155/-125)
to expose the source-facing silhouette; the shared default stays unchanged for
other families. No animation or production performance completion is claimed.

Coverage is now **88/381 creatures (23.1%)**, or **89/394 creature/player
identities (22.6%)** including the completed Valkyrie role. There are 94 physical
forms: 88 primary creatures, four additional female appearances and two human
players. 293 creature IDs and 12 roles remain. Next suggested family extension:
yeti and sasquatch; separately review owlbear bear/bird anatomy afterward.

## Save protection

Verified baseline: `Backups/NetHackSaves/20261103T142232.737274Z.zip`, 1,090
files. Tests use fresh `Saved/NetHackGameplayTests` / `Saved/NetHackCaptures`
roots with the player pointer excluded. No played session is resumed, advanced,
stopped or replaced. No native backend rebuild is required for this art batch.
Final hash audit passes: all 1,090 baseline files, complete player/runtime file
set and `LastSession.txt` remain unchanged. All 240 preceding FBX exports also
match their pre-batch signatures.

# Yeti, sasquatch and owlbear

Batch 29 follows the handoff queue. All three official sex pairs are identical:
yeti 484/485, sasquatch 488/489 and owlbear 482/483. Each shares one static form.

Source: pinned include/monsters.h. Yeti is a large strong hostile carnivore,
level 5/difficulty 7, cold-resistant with two claws and a bite. Sasquatch is a
large strong omnivore, level 7/difficulty 9, with see-invisible and claws/kick.
Owlbear is a large strong hostile carnivore, level 5/difficulty 7, with paired
claws and a crushing hug. These native rules remain unchanged.

Yeti follows white fur, dark eyes and red mouth. Cyan/slate edge pixels are
interpreted as cast shading, not coloured fur; the orange side shape is a wooden club, as clarified by the user. The revised
yeti holds that club; this source art cue does not promise live inventory.
Sasquatch follows brown/orange fur and green eyes. Owlbear has a separate broad
bear torso, short tail, owl facial discs, tufted head, hooked beak and claws.
Pale facial discs and slate claws follow the actual tile. Offset black fringe
is excluded spatially; enclosed dark anatomy remains. Masks are diagnostic.

HairyBipeds.py extends compatible primate construction with independent height,
head, shoulder, limb and face dimensions. Batch29Family.py builds owlbear
independently; it is not an ape recolour. Exact zoological identity, unseen
anatomy, digits, poses and feather/coat interpretation are artistic assumptions.
Texture-only fur follows the approved treatment. No rigs or animation.

Artifacts under Art/CreatureInterpretations: CreatureBatch29.blend; yeti.fbx,
sasquatch.fbx, owlbear.fbx; Batch29-SourceReview.png, Batch29-Models.png,
MeshComparison-batch29.png, Batch29-Projections.png, Batch29-HeadReview.png,
Batch29-UndersideReview.png and individual hand views. Six true 16x16 candidates
per form accompany actual front/rear geometry. Scripts use Batch29 names.

Checks: batch29-mesh-inspection.json, batch29-native-living.json,
batch29-unreal-assets.json, Batch29-Unreal-fixtures.png and
batch29-save-preservation.json. Logs: build-creature-batch29-*.log.

Verified pre-integration snapshot: 20261103T190116.926434Z.zip (1,091 files).
Tests use fresh isolated roots. No played session is resumed or replaced.
Dense draft geometry, eyes/beak/claw seating, coat flow, proportions, tiny-scale
readability and LOD/runtime costs remain finishing work.

Saved inspection passes closed solids, connected body, paint and fur UVs for all
three forms. Native triangle counts: 266,648 revised yeti / 284,708 sasquatch / 201,076
owlbear. Owl facial discs are closed overlapping volumes; they are not a claim
of fine feather reconstruction. Shoulder/hip transitions remain blockout-like
and need finishing. The targeted importer preserves existing shared shaders.

The initial test editor stalled before import while waiting for Zen. Only that
verified import process was restarted with -ddc=InstalledNoZenLocalFallback.
This per-launch cache choice does not alter player configuration or saves.


Final build/import/native/live checks pass: six displayed sex aliases, six
fallbacks, unknown guards, paint/fur/UV and actual no-turn F9 both ways.
Native map, hero centring and 8x zoom pass. The first passing capture partly
obscures owlbear behind a wall and is retained separately. Studio views show
complete geometry. Player audit verifies all 1,091 files, file set, backend and
LastSession pointer unchanged; all 251 preceding exports match hashes.
Coverage: 91/381 creatures (23.9%), 92/394 including Valkyrie (23.4%); 97 physical
forms. Backlog/catalogue updated; next suggested batch is acid blob, quivering
blob and gelatinous cube. Static finishing remains separate.

Final second live capture shows all three fixtures clearly, at turn 4.

Yeti correction: user identifies the orange tile shape as a wooden club.
YetiClub.py and saved ReviseYetiClub.py add a closed painted wooden club through
the right palm, with thick low head and wood-grain paint. Other FBXs are protected
by yeti-club-protected.json. Fresh generation includes the club; do not repeat
the one-time saved revision. Backup: 20261103T193300.214615Z.zip.

Club revision: saved closed geometry/paint/floor inspection, targeted yeti
import/material validation and isolated live alias/fallback/F9/map/zoom checks
pass. All 256 other FBX files and all 1,091 save/runtime baseline files match.

User revision: club is now much larger, with one straight 1.03m centreline
and a broad upper head (22cm maximum diameter). It leans outward from the
right hand; tile grip orientation is explicitly not binding. YetiClub.py drives
fresh builds; EnlargeYetiClub.py revises the saved club only. Backup:
20261103T194459.852011Z.zip. Other anatomy and exports remain protected.

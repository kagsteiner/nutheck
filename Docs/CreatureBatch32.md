# Gray ooze, brown pudding and black pudding

Batch 32 follows the handoff queue. Official sex pairs are identical: gray ooze
422/423, brown pudding 424/425, black pudding 428/429. Native sex is neuter;
wizard sex requests retain neuter display glyphs. Synthetic sex aliases verify
shared-art model/fallback handling, not native female specimens.

Pinned include/monsters.h: all three are hostile, breathless, amorphous,
mindless, acidic omnivores with no head/limbs, native NOEYES and no corpse.
Gray ooze: medium, level 3/difficulty 4, 2d8 rusting bite; fire/cold/poison/
acid/stone resistance. Brown: medium, level 5/difficulty 6, decay bite; cold/
electricity/poison/acid/stone resistance. Black: large, level 10/difficulty 12,
3d8 corrosive bite and corrosive contact; same resistances as brown.
Native attack, perception, resistance and gameplay rules remain unchanged.

## User correction: pudding eyes

The user explicitly identifies the visible brown and black pudding marks as
eyes. This art instruction governs their reconstruction despite native NOEYES.
Brown has two pale eyes with dark pupils; black has orange upper/red lower
apertures. Do not revert these to gel inclusions because of source flags.
PuddingEyes.py ray-fits closed thin eye volumes to the existing body surface.
RevisePuddingEyes.py updates saved models; fresh generation includes the same
eyes. It also removes the earlier eye-like inclusion paint. Gray ooze remains
unchanged. This visual correction adds no native sight or knowledge.

## Source and interpretation

Gray ooze follows blue/cyan/slate masses and an amber trailing surface accent,
not neutral ASCII gray alone. Its low flowing sheet has independent lobes and
one low crest. The amber patch is art, not a promised swallowed item.
Brown follows brown/orange, with a rounded lopsided mass and small curled rear
gel fold. Black follows the entire black elongated silhouette, with a raised
narrow upper curve and tapered base. No black anatomy is discarded by blanket
palette removal; its comparison mask conservatively retains every foreground
pixel. Other source masks exclude exterior black fringe while keeping enclosed
marks. These masks are diagnostics; original tiles remain unmodified.

Independent soft-body construction supplies complete backs and undersides.
No separate animal skull, mouth, teeth, limb or invented inventory was added.
Precise hidden surface, dimensions, pose, gel texture and eye seating are art.
Existing opaque M_Gel is reused unchanged (.32 roughness). No transparency,
animation, splitting effect, rig or fur. Static folds remain intentional.

## Evidence

Art/CreatureInterpretations/CreatureBatch32.blend and three named FBXs contain
editable geometry and corner paint. Batch32-SourceReview.png,
Batch32-Models.png, MeshComparison-batch32.png, Batch32-Projections.png,
Batch32-HeadReview.png and Batch32-UndersideReview.png show actual geometry;
eighteen genuine 16x16 candidates accompany front/rear renders. Legacy *-head-*
filenames denote detail views; generic pipeline naming is not anatomy metadata.

Reports: batch32-mesh-inspection.json, batch32-native-living.json,
batch32-unreal-assets.json, batch32-protected-assets.json,
batch32-eye-protected.json, batch32-live-verification.json and
batch32-save-preservation.json. Capture: Batch32-Unreal-fixtures.png.
Scripts use Batch32 names; native checks use Tests/BridgeBatch32.py.
Logs are build-creature-batch32-*.log, including the saved eye revision and
final targeted ImportCreatureBatch32Eyes.py run. Saved Render/Review scripts
inspect existing work without regeneration or repeating the one-time revision.

Verified backup: 20261104T065340.898491Z.zip (1,091 files). All 263 preceding
FBX exports are protected; eye revision also protects gray ooze. Tests use
fresh isolated roots; no played session resumed or native backend rebuilt.
Body transitions, eye seating, source-palette/silhouette balance, dark overview
readability and LOD/runtime costs remain static finishing work.


Final saved inspection passes closed solids, connected bodies, corner paint,
floor origin and two tile-supported eyes per pudding. Triangle counts: 84,984
gray ooze / 110,456 brown pudding / 3,804 black pudding. Editor build, native
neuter identities, targeted eye reimports/material checks and live six aliases/
six official fallbacks/unknown/paint/no-turn F9 both ways pass. Native map,
hero centring and 8x zoom pass. Final actual capture shows all three fixtures;
first wall-obscured capture and log remain separately retained.

All 263 prior exports and 1,091 baseline save/runtime files, complete file set
and LastSession pointer match. No native backend changed. Coverage: 100/381
creatures (26.2%), 101/394 including Valkyrie (25.6%); 106 physical forms.
Next suggested batch: brown mold, yellow mold and green mold.

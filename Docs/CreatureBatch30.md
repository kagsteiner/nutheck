# Acid blob, quivering blob and gelatinous cube

Batch 30 follows the handoff queue. Three neuter, mindless, eyeless, headless,
limbless creatures have distinct static gel forms. Both official sex tiles are
identical: acid blob 12/13, quivering blob 14/15, gelatinous cube 16/17.

Pinned include/monsters.h: acid blob is tiny, level 1/difficulty 2, breathless,
amorphous, passively acidic; resistant to sleep, poison, acid and petrification.
Quivering blob is small, level 5/difficulty 6, with physical touch and sleep/
poison resistance. Cube is large, level 6/difficulty 8, an acidic omnivore with
paralyzing touch/contact and broad elemental/sleep/poison/acid/stone resistance.
Native gameplay is unchanged. Wizard sex requests still display neuter glyphs;
synthetic male/female aliases only verify shared art and fallback selection.

Actual tiles guide red/magenta acid gel, blue/white quivering gel, and orange/
peach cube with lime inclusions, rather than green/white/cyan ASCII colours.
Their conspicuous pale/dark central marks resemble eyes but source explicitly
forbids eyes: paint interprets these as irregular inclusions, without eyeballs,
pupils, faces or mouths. Spatial exterior black fringe is excluded; enclosed
dark marks are retained by diagnostic masks. Exact composition, volume, lobe
arrangement and paint are artistic assumptions. Original tiles are unchanged.

CreateCreatureBatch30.py constructs connected low lobed acid gel and a larger,
taller quivering volume, plus an independently built rounded cube. No detached
attack splashes, limbs or inventory contents. Material M_Gel uses opaque vertex
paint, roughness .32, preserving the painted miniature language. No time-driven
quivering, transparency, rigs or animation. Green inclusions are paint, not
hidden swallowed objects. Cube surface density was increased after review so
paint varies across faces; fresh generation includes the repair. Saved one-time
RefineCreatureBatch30Cube.py should not be repeated merely for inspection.

Artifacts in Art/CreatureInterpretations: CreatureBatch30.blend; acid_blob.fbx,
quivering_blob.fbx, gelatinous_cube.fbx; Batch30-SourceReview.png,
Batch30-Models.png, MeshComparison-batch30.png, Batch30-Projections.png,
Batch30-HeadReview.png and Batch30-UndersideReview.png. Individual *-head-* files
show surface details, using established pipeline filenames despite having no
heads or hands. Eighteen genuine 16x16 renders accompany front/rear views.

Native checks use Tests/BridgeBatch30.py in fresh isolated roots. Other scripts
follow Prepare/Create/Inspect/Render/Review/Comparison/Import/Verify/AuditBatch30
names. Saved reports: batch30-mesh-inspection.json, batch30-native-living.json,
batch30-unreal-assets.json, batch30-protected-assets.json and
batch30-save-preservation.json. Live image: Batch30-Unreal-fixtures.png.

Verified backup: 20261104T063243.957994Z.zip, 1,091 baseline save/runtime files.
All 257 preceding exports are protected. Player session is never resumed,
advanced or replaced; tests use NetHackGameplayTests/NetHackCaptures roots.

These are static drafts. Surface continuity, lobe silhouettes, source-colour
balance, inclusions and LOD/runtime costs remain finishing work. No animation.


Saved inspection, native neuter tests, editor build, final import/gel material
validation and live checks pass. Six synthetic sex aliases and their respective
official fallbacks pass; both F9 toggles preserve turn 5 / sequence 7. Map, hero
centring and 8x zoom pass. Capture inspected: cube partially overlaps acid blob;
studio views are unobscured. Triangle counts: 77,776 acid blob / 148,224 quivering
blob / 55,476 cube. Final audit preserves all 257 preceding FBXs and all 1,091
player/runtime files, file set and LastSession pointer. Backend unchanged.

Coverage: 94/381 creatures (24.7%), or 95/394 creature/player identities (24.1%)
including Valkyrie; 100 physical forms. Next: blue, spotted and ochre jellies.

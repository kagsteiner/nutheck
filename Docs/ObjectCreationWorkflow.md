# Object creation workflow

This is the operational entry point for a fresh session. Read this entire file,
[ObjectArtDirection.md](ObjectArtDirection.md), repository `AGENTS.md`, and the
current [object backlog](../object-backlog.md) before building. Follow newer user
direction when it overrides an older study. A request to build a batch authorizes
modelling, import and live integration; carry it through verification without
stopping after a plan or a design-only draft.

## 1. Choose the batch and inspect existing work

For “the next three weapons,” use an explicit user selection first, otherwise the
next unbuilt group in the backlog's suggested queue. The current next group is
**dagger (`DAGGER`), short sword (`SHORT_SWORD`), spear (`SPEAR`)**. Recheck that
these are still unbuilt: unchecked means incomplete, not necessarily unmodelled.
Read their catalogue status, batch documents, scripts, FBX and Unreal assets before
choosing. Finish existing work when requested; do not rebuild completed swords.
If this group is already built, choose the next coherent group of three unbuilt
ordinary weapons from the backlog, record the choice, and proceed. Artifacts are
a separate queue unless the user asks for them. Do not start the next batch merely
because this workflow is being read for a review or documentation task.

Use `Art/ObjectCatalogue/{objects,appearances,artifacts}.json` for stable IDs and
source pointers. Verify each selected entry against pinned
`upstream/NetHack/include/objects.h`, and `artilist.h` for artifacts. Record type,
physical description, material, cultural cues and shuffle/shared-appearance rules.
Keep native facts separate from artistic interpretation. Do not infer an effect
from a shuffled appearance. Consult `dev_backlog.md` for non-modelling work and
preserve its human-testing notes and statuses.

## 2. Design and build editable models

Use `Scripts/CreateWeaponBatch1.py` as the working ordinary-weapon example;
`Scripts/CreatureGeometry.py` provides geometry/paint helpers and
`Scripts/CreatureBatch2Pipeline.py` provides export/studio/projection machinery.
Read dependencies before adapting them. These are examples, not a generic
parameterized object generator: write new batch-specific create/review/import
scripts, keys, output names and evidence instead of rerunning the old sword batch.
Existing helpers use the object property `creature` as a geometry group key even
for weapons; preserve compatibility or update the new pipeline consistently.

Ignore generic object tiles as design targets. Build distinct, beautiful physical
weapons from their construction: appropriate blade/head section and thickness,
cutting edges, taper, guard/socket, grip/shaft and fittings. Use reliable museum or
construction references when useful; browse for external facts you rely on.
Artifacts deserve exceptional craftsmanship. Make complete front, rear and
underside geometry, real bevels and recessed details where appropriate. Metal
must read as metal; wood and leather must have their own surface character.
Do not use flat extruded tile silhouettes, painted-only detail or identical
silhouettes with different colours. Static loot models are sufficient.

Keep editable parts and collections in `Art/ObjectInterpretations/<Batch>.blend`.
Use metres, Z upright, the established XZ presentation plane, an origin at floor
level, applied transforms and compatible scale. The existing swords are about
1.1–1.3 m long; choose sensible proportions for each new family. Preserve the
examination model and use runtime placement scale to fit a dungeon cell.
Use valid `Paint` corner-domain FLOAT_COLOR vertex colours and separate material
families for paint/wood/leather and metal. Preserve actual material properties in
Unreal; vertex colours alone do not make plastic-looking surfaces metallic.

Before generation, save hashes of all existing canonical FBX exports in the art
folders. Verify them afterward. Never reuse an old manifest's hard-coded asset
count as the new baseline. Avoid editing shared helpers or material assets unless
needed; if changed, verify affected existing assets as well.

## 3. Export, inspect and visually review

Export one selected model per `<key>.fbx`, meshes only, no cameras/lights/animation,
with the established exporter settings: `apply_unit_scale=True`,
`axis_forward='-Y'`, `axis_up='Z'`, `bake_anim=False`, `add_leaf_bones=False`.
Keep studio lights in the editable scene, not in the exported mesh.

Adapt `ReviewWeaponBatch1.py` and `CreateWeaponBatch1Boards.py` for the new batch.
Validate finite vertices, nonzero faces, appropriate closed/manifold solids,
valid paint, dimensions, floor bounds, applied modifiers and no animation.
Record actual part/triangle counts and the prior-asset hash comparison in JSON.
Do not satisfy checks with hard-coded success flags.

Render actual three-quarter, front, rear, underside and relevant detail views,
plus actual 16×16 model projections from multiple useful angles. Open and inspect
the images; fix visible geometry/material problems and rerender affected views.
Assemble labelled review boards from the real renders. The tiny views judge
readability, not fidelity to generic weapon tiles. Do not substitute generated
concept art or a screenshot of unrelated assets for model evidence.

## 4. Import into Unreal and connect the live renderer

Adapt `Scripts/ImportWeaponBatch1.py` into a new batch-specific importer. Use a
separate `/Game/<Batch>/Meshes/SM_<key>` namespace and batch-local materials;
import static meshes with vertex colours retained, authored normals, combined
parts, no automatic collision, no imported textures/materials. Map every imported
slot intentionally. Provide normal and memory material variants, preserving the
current project's memory treatment rather than copying an obsolete multiplier
blindly. Validate vertex-colour buffers, slots and saved asset paths.

Use the installed Blender and Unreal executable paths after discovering them.
Typical script invocation shapes, with absolute resolved paths, are:

```powershell
& $blenderExe --background --threads 4 --python $createScript
& $blenderExe --background --threads 4 --python $reviewScript
& $pythonExe $boardsScript
& $unrealEditorCmd $projectFile -run=pythonscript "-script=$importScript" -unattended -nosplash
```

Resolve those task-specific variables before running; retain per-step logs and
check exit codes and explicit verification markers. Do not run the old batch's
scripts unchanged: they can replace existing assets.

Live selection and transforms are in
`Source/NUthEck/DungeonObjectPlacement.cpp`; ordinary displayed metadata is in
`upstream/NetHack/win/ue/winue.c`, and parsing is in `NetHackSession.cpp`.
Extend the presentation registry, native fixed-appearance whitelist where lawful,
and tests for the chosen models. Confirm exact displayed strings and base types.
Require `Kind == item`; unsupported/missing models keep the existing fallback.
Only the native displayed pile-top is rendered; do not inspect hidden contents.

Follow [MVPObjectPlacement.md](MVPObjectPlacement.md): ordinary weapons lie flat,
armor/cloaks stand, named artifact weapons hover upright, all static. Use transformed
mesh bounds for centering and floor clearance, deterministic poses without native
gameplay RNG, and per-family scale where needed. Preserve both F9 styles, normal
and remembered lighting/materials, and no-turn switching.

Artifact names are visible before full identification: native `xname` appends
ONAME when `has_oname && dknown`. Do **not** require `!undiscovered_artifact` or full
identification for the special pose. Require a real matching artifact and native
visible-name knowledge; an ordinary player-given name is insufficient. Preserve
blindness, hallucination and fake-mimic safeguards. For shuffled families, design
and verify a displayed-appearance protocol instead of adding hidden effect IDs
to this fixed whitelist.

## 5. Verify safely and close the batch

Follow `AGENTS.md` and [SaveProtection.md](SaveProtection.md). Pure art work needs
no save mutation. Before native/backend/save-affecting work run
`Scripts/BackupNetHackSaves.ps1`; it must verify and refuse a live player backend.
Continue independent art work if the player is running. Never kill it, resume the
played session, reset saves or alter `LastSession.txt` for testing. Test exclusively
in fresh isolated roots. `-NewGame` is only for isolated capture/test launches.

Build affected code with `Scripts/BuildNetHackBridge.ps1` and the installed UE
`Build.bat NUthEckEditor Win64 Development -Project=<absolute uproject>
-WaitMutex -NoHotReloadFromIDE` as applicable. Adapt
`Tests/BridgeObjectPlacement.py` to wish/drop/reveal all new appearances through
real native events. Extend `VerifyObjectPlacement` and its isolated capture in
`Scripts/VerifyObjectPlacement.ps1` to cover all added models, both visibility
states, both styles, material/mesh validity, flat/standing/hover bounds, fallback
and no-turn switching. Inspect a real Unreal capture with the new models visible.
Clearly label synthetic capture fixtures; they are not proof of native spawning.

Exercise relevant pile, memory, identification, hallucination and restore cases
when extending the protocol. After a backend replacement run
`Tests/BridgeBackendCompatibility.py <pre-change backup>` using its isolated
old-save/new-runtime test, then adapt `Scripts/AuditObjectPlacementSaves.py` to
that backup and verify all player hashes/file paths/session pointer unchanged.
Preserve the backup and logs. Do not reuse another batch's audit result.

Write `Docs/<Batch>.md` with source facts versus invention, model and script paths,
actual visual evidence, checks run/results, live mapping and remaining work.
Update existing entries in `object-backlog.md`, not a replacement checklist.
Update `Art/ObjectInterpretations/object-assets.json` only for verified completed
drafts; align `Scripts/CreateObjectCatalogue.py` status overrides, regenerate
catalogue metadata and run `Tests/ObjectCatalogue.py`. Its current completion
expectations may need an evidence-backed update if completed counts change.
Keep ordinary object types, appearance slots and artifact overlays separate;
do not change creature counts. Distinguish modelled/imported, MVP live verified,
and full checklist completion. Leave unfinished checks explicit and unchecked.

Deliver a short account of the three built objects, an actual review image or
board, validation, and any concrete remaining limitation. Finishing/LOD work is
separate; do not claim production performance from a successful import.

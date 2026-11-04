# Tool batch 1: pick-axe, grappling hook and stethoscope

Built 2026-11-03. This batch moves from ordinary weapons to three unbuilt fixed utility-tool appearances, after checking the backlog, catalogue, scripts, exports and Unreal assets. All three have editable geometry, painted FBX exports, saved Unreal assets and MVP live verification. The separate jewelry/consumable appearance study remains in the queue.

## Native facts and artistic interpretation

Pinned `upstream/NetHack/include/objects.h` defines `STETHOSCOPE` at line 957 (`TOOL`), `PICK_AXE` at line 1007 and `GRAPPLING_HOOK` at line 1010 (both `WEPTOOL`). All are initially known, `NoDes`, main material `IRON`, with no shuffle group, shared appearance ambiguity or cultural modifier. All remain in native **Tools**, including the two usable as weapons. Stable enum IDs are catalogue keys; runtime displayed strings are exactly `pick-axe`, `grappling hook`, `stethoscope`.

Construction, proportions and ornament below are artistic interpretation, not new native lore, gameplay features or historical claims:

- Pick-axe: a long curved tapered pick opposite a broad transverse chisel, forged eye block with an actual cut haft opening, shaped wood handle, reinforcing straps, rivets, heel ferrule and restrained leather binding.
- Grappling hook: four individually editable sweeping solid tines around a forged spine/hub, open rope eye and worked fittings. No rope bundle, stack-size representation or deployment state is invented.
- Stethoscope: steel ear arms and soft tips, a hanging sound tube, metal junction and a double-sided chest piece with a recessed diaphragm and rear bell rim. Visual review removed a disconnected internal strip and modestly thickened/lightened the tubing for small-scale readability before final export/import.

Iron is the main native material; subsidiary wood, leather, brass and flexible tubing are construction choices. No geometry or colour encodes enchantment, blessing, charges, hidden contents, item value or artifact identity. Generic object tiles were not design targets. Models are static loot, with no equipment/use animation.

| Model | Height | Parts | Triangles | Dungeon scale |
| --- | ---: | ---: | ---: | ---: |
| pick-axe | 0.8220 m | 26 | 15,148 | 0.80 |
| grappling hook | 0.4299 m | 12 | 10,892 | 1.25 |
| stethoscope | 0.5754 m | 11 | 8,244 | 1.20 |

## Editable geometry and actual renders

`Art/ObjectInterpretations/ToolBatch1.blend` contains separate editable parts, model collections and studio lighting, using metres and Z upright. Each model's lowest point is normalized to its floor origin. The examination model retains full proportions; per-model runtime scale fits the miniature dungeon presentation. `pick_axe.fbx`, `grappling_hook.fbx` and `stethoscope.fbx` export only meshes, using established unit/axis settings and no animation/lights/cameras.

Batch-specific scripts: `CreateToolBatch1.py`, `ReviewToolBatch1.py`, `CreateToolBatch1Boards.py`. Shared geometry, vertex-paint and projection/export helpers were inspected and reused without modification. Inspection asserts finite vertices, nonzero polygon areas, manifold closed solids, applied modifiers, unit scales, no animation, valid finite CORNER FLOAT_COLOR Paint and floor bounds; actual counts and dimensions are recorded in `tool-batch1-inspection.json`.

`tool-batch1-protected.json` captured all **229** previous canonical FBX hashes before generation. Every hash remains unchanged after the final revision. The baseline count was discovered rather than inherited from an older batch.

Actual three-quarter, front, rear, underside, mechanism/detail and six 16x16 projections per model were rendered and inspected. Labelled boards: `ToolBatch1-{Models,Front,Rear,Underside,Hilts,Projections}.png` (the inherited Hilts filename contains construction close-ups). Tiny projections assess readability, not resemblance to generic tiles. Fine stethoscope tubing remains less prominent at very distant pixel scales; close inspection shows its construction.

![Actual model renders](../Art/ObjectInterpretations/ToolBatch1-Models.png)

## Unreal and native displayed mapping

`ImportToolBatch1.py` uses the established hidden full-editor `-ExecutePythonScript` path. Static mesh assets live at `/Game/ToolBatch1/Meshes/SM_<key>`. Parts are combined, vertex colours retained and authored normals requested; no automatic collision or imported textures/materials are requested. Every source material slot is mapped explicitly to batch-local metallic iron/polished metal/brass or nonmetal wood/leather/tube paint. Normal and Memory variants preserve existing object shading and the .20 memory colour multiplier, with separate visibility lighting channels. `VerifyToolBatch1Assets.py` reloads saved packages and checks exact slot assignments, saved paths and vertex-colour buffers.

`DungeonObjectPlacement.cpp` registers the three tools as static flat presentations, above neutral floor at minimum Z=12 cm (4 cm over the 8 cm floor surface). Placement centers transformed mesh bounds and uses deterministic yaw without native gameplay RNG. Both F9 styles use the same object models; unsupported/missing presentations retain tile fallback. The batch capture alone uses the established steeper camera orbit to keep flat loot visible.

`winue.c` extends only the fixed displayed-glyph whitelist with these three exact names; it does not inspect hidden pile contents or invent effect IDs. The tracked copy under `Patches/NetHack/win/ue/winue.c` is synchronized. Existing generic parsing in `NetHackSession.cpp` needs no change. Selection still requires `Kind == item`. Identification does not change these initially known physical designs; no shuffled appearance protocol is introduced.

The strict-topmost verifier now explicitly covers all three tools in addition to existing foregrounds. Underlying altars, fountains, stairs and other features stay hidden beneath the single native displayed foreground. Known named weapons retain their earlier special pose rules, without an altar exception.

## Verification and player-save protection

- Native and Unreal Development builds pass: `build-tool-batch1-{native,unreal}.log`. Existing native/compiler warnings and engine startup automation messages remain separate from the explicit successful batch markers.
- Final geometry/render review passes: `build-tool-batch1-{create,review}.log`, inspection JSON and actual boards.
- Final import: `build-tool-batch1-import.log`, `TOOL_BATCH1_IMPORT_READY count=3`. Reloaded saved assets: `build-tool-batch1-saved-assets.log`, `TOOL_BATCH1_SAVED_ASSETS_PASS`, `tool-batch1-unreal-assets.json`.
- `Tests/BridgeObjectPlacement.py`: **32 ordinary presentations plus two artifacts** wished, dropped and revealed through real native window events in an isolated wizard root (`build-tool-batch1-bridge.log`).
- `Tests/BridgeToolBatch1.py`: each new tool's displayed string/glyph and absence of artifact identity survive isolated native save/restore (`build-tool-batch1-restore.log`, `tool-batch1-restore.json`).
- `Scripts/VerifyToolBatch1.ps1`: all **38 presentations**, two visibility states and both styles pass mesh/material/colour-buffer, flat/standing/hover clearance, ordinary/artifact, fallback/non-item and no-turn checks (`build-tool-batch1-live.log`, `build-tool-batch1-capture-run.log`).
- `Scripts/VerifyToolBatch1Topmost.ps1`: **1,200 cases pass** across 15 terrain backgrounds, ten foreground cases (including all three new tools), two visibility states, two F9 styles and regular/Mines rendering. Background geometry is verified present, hidden beneath the foreground, and restored when uncovered; native turn/sequence remain unchanged. Evidence: `build-tool-batch1-topmost.log`.
- `ToolBatch1-Unreal.png` is an opened and inspected actual Unreal capture with the three models visible. Its objects are **synthetic render fixtures**, not proof of native spawning. The native wish/drop test supplies that separate proof. `ToolBatch1-Topmost.png` belongs to the separate synthetic layer regression.
- `Tests/BridgeBackendCompatibility.py Backups/NetHackSaves/20261103T075929.624342Z.zip`: isolated old-runtime save -> new-runtime restore passes (`build-tool-batch1-compatibility.log`).
- `Scripts/AuditToolBatch1Saves.py`: full file set, **1,081 player files** and LastSession pointer remain unchanged against that verified pre-change snapshot. Only intended `Runtime/NetHackBridge.exe` changes. Evidence: `tool-batch1-save-preservation.json`, `build-tool-batch1-save-audit.log`. The native build also made its required backup. No played session was launched, resumed or advanced.
- Catalogue regenerated; `Tests/ObjectCatalogue.py` passes with explicit scoped statuses for all three new tool IDs. Four fully verified old drafts remain separate from MVP counts. Creature counts, native category counts, appearance-slot counts and artifact-overlay counts do not change.

![Unreal capture - synthetic tool fixtures](../Art/ObjectInterpretations/ToolBatch1-Unreal.png)

## Remaining scope

Backlog entries stay unchecked for full completion. Finishing, LOD/runtime cost review and exhaustive hallucination/mimic, identification, remembered-pile replacement and map-clear transitions remain separate. The three fixed physical presentations are modelled, imported and MVP live verified; this does not claim production performance or completion of the shuffled jewelry/consumable appearance families.

# Weapon batch 2: dagger, short sword and spear

Built 2026-11-03. Editable geometry, painted FBX exports, Unreal imports and MVP live placement are verified. Full finishing/LOD and broader presentation edge cases remain separate.

## Native facts and design interpretation

Pinned source `upstream/NetHack/include/objects.h` defines `SPEAR` at line 174, `DAGGER` at line 200 and `SHORT_SWORD` at line 244. All three have `NoDes`, initially known fixed appearances and `IRON` as the main native material. They have no shuffled/shared description pool or cultural modifier. The stable enum keys, not numeric offsets, identify these catalogue records. No artifact overlay was added.

The construction and ornament are artistic interpretation, not extra native lore: the dagger has a narrow diamond-section blade, swept guard, leather binding, turned collars and peened pommel. The short sword has a broad waisted blade, compact brass guard, carved wood grip, rivets and restrained blade-root inlay on both faces. The spear has a leaf head, forged socket with rivets and bands, tapered wood shaft, hand binding and iron butt fitting. Native `IRON` describes the main weapon material; subsidiary wood/leather/brass fittings are artistic construction choices. No marking encodes enchantment, blessing, value, hidden identity or magical effects. No generic tile silhouette was used as the design target.

| Model | Height | Editable mesh parts | Triangles | Runtime scale |
| --- | ---: | ---: | ---: | ---: |
| dagger | 0.470 m | 17 | 12,336 | 1.00 |
| short sword | 0.770 m | 12 | 8,116 | 0.85 |
| spear | 2.156 m (bounds 0.004–2.160) | 27 | 18,796 | 0.42 |

The examination scene remains in metres with Z upright and an XZ broad-face presentation. Runtime transformed bounds center the flat weapon and give 4 cm clearance above the 8 cm floor surface (minimum world Z=12 cm). Hovering presentations now use Z=26 cm for their 18 cm clearance. Visual review caught and corrected an older verifier/placement bug that measured from cell Z=0 and buried thin weapons in the floor. The corrected shared verifier checks all existing presentations as well. The spear's reduced dungeon scale fits a cell without shortening the editable examination model.

## Editable assets and evidence

- `Art/ObjectInterpretations/WeaponBatch2.blend`: separate editable parts and collections, real sections/edges/fittings on both sides, static geometry, studio cameras/lights.
- `Art/ObjectInterpretations/{dagger,short_sword,spear}.fbx`: meshes only; established unit/axis settings, no animation or studio lights.
- `Scripts/CreateWeaponBatch2.py`, `ReviewWeaponBatch2.py`, `CreateWeaponBatch2Boards.py`: batch-specific model/export, geometry inspection and actual-render boards. Shared geometry/export helpers were read and reused without modification.
- `WeaponBatch2-{Models,Front,Rear,Underside,Hilts,Projections}.png`: actual multi-angle, detail and 16×16 model renders; opened and inspected. Initial dark-metal studio renders were replaced with better reflection-strip lighting. Tiny images judge silhouette readability; tile overlap scores in the inherited report are not a fidelity target.
- `weapon-batch2-inspection.json`: finite vertices, nonzero faces, manifold closed parts, no pending modifiers/animation, unit scale, finite Paint corner FLOAT_COLOR values, measured bounds and actual counts.
- `weapon-batch2-protected.json`: pre-generation SHA-256 baseline of all 223 existing canonical art FBX files; every hash remains unchanged. Counts are discovered, not copied from the older batch.

![Actual model review](../Art/ObjectInterpretations/WeaponBatch2-Models.png)

## Unreal and live integration

`Scripts/ImportWeaponBatch2.py` imports to `/Game/WeaponBatch2/Meshes/SM_<key>`. Every imported material slot is mapped explicitly to batch-local iron, brass or paint materials. Iron is metallic 1.0/roughness .22, brass .75/.32, wood/leather paint 0/.58. Vertex colours are retained; no automatic collision or texture/material import is requested. Normal and Memory variants preserve the existing object treatment: .20 base-colour multiplier, separate visible/memory lighting channels. The 40% remembered-stone tint in the development backlog is a different material treatment.

The default `-run=pythonscript` commandlet hit Unreal's Interchange/Slate assertion; the repository's established hidden full-editor `-ExecutePythonScript` path imported successfully. Final import log: `build-weapon-batch2-import-editor.log`, marker `WEAPON_BATCH2_IMPORT_READY count=3`. Startup also logs unrelated engine automation condition messages before the import; all three explicit import/colour-buffer checks succeed. `VerifyWeaponBatch2Assets.py` reloads saved assets, verifies exact slot assignments and memory asset paths, checks saved packages and retained vertex colours; evidence is `weapon-batch2-unreal-assets.json` and `build-weapon-batch2-saved-assets.log`.

`DungeonObjectPlacement.cpp` adds exact `dagger`, `short sword` and `spear` presentations, requiring `Kind == item`. They lie flat in both F9 styles using deterministic yaw and transformed mesh bounds. Unsupported/missing presentations retain existing tile fallback. `winue.c` extends only the fixed displayed-glyph whitelist; it does not inspect hidden floor objects or pile contents. `NetHackSession.cpp` already parses these generic displayed strings and needs no change. Identification does not select a different mesh. Native fake-object/hallucination behavior continues to supply the displayed glyph rather than hidden identity; exhaustive transition tests remain below.

The synthetic capture preview places only the three new models when `PreviewWeaponBatch2` is set, moves fixture selection clear of billboards and centers its camera on those instances. The batch-specific zoom check validates that explicit camera target; normal captures retain hero-centering validation. Fixtures add render instances only and do not wish/drop objects in the native game.

## Verification and save protection

- Native build: `build-weapon-batch2-native.log`; existing unreachable-code warning in `winue.c`, build succeeds.
- Unreal Development build: `build-weapon-batch2-unreal.log`, succeeds.
- `Tests/BridgeObjectPlacement.py`: 26 ordinary presentations plus Cleaver/Mjollnir wished, dropped and revealed through real native events in a fresh wizard root; `build-weapon-batch2-bridge.log` passes. Existing native piles are displayed only via their top glyph.
- `Tests/BridgeWeaponBatch2.py`: each new fixed appearance survives a normal isolated native save/restore, with matching glyph/string and no artifact identity. It selects the newly wished inventory entry rather than an initially equipped weapon. Evidence: `build-weapon-batch2-restore.log`, `weapon-batch2-restore.json`.
- `Tests/BridgeObjects.py`: existing box/chest/gold mapping regression passes (`build-weapon-batch2-existing-objects.log`). An initial random native newt obscured a dropped chest; a fresh isolated rerun passed.
- `Scripts/VerifyWeaponBatch2.ps1`: shared verifier covers all 32 presentations × two visibility states × two styles; actual loaded mesh/materials, nonempty vertex-colour buffers, flat/standing/hover axes, floor clearance, unsupported/non-item fallback and unchanged native turn/sequence. `build-weapon-batch2-live.log` and `build-weapon-batch2-capture-run.log` contain pass markers.
- `WeaponBatch2-Unreal.png` is an inspected real Unreal dungeon capture with synthetic render fixtures, not proof of native spawning. Native spawning evidence is the separate wish/drop event test.
- `Tests/BridgeBackendCompatibility.py Backups/NetHackSaves/20261103T070545.522214Z.zip`: isolated old-runtime save -> new-runtime restore passes (`build-weapon-batch2-compatibility.log`).
- `Scripts/AuditWeaponBatch2Saves.py`: verifies all 1,081 player files, full file set and LastSession pointer unchanged against that verified pre-change archive; only `Runtime/NetHackBridge.exe` changes. Evidence: `weapon-batch2-save-preservation.json`. The native build also took its own required backup. No played session was launched, resumed or advanced.
- Catalogue regenerated with `CreateObjectCatalogue.py`; `Tests/ObjectCatalogue.py` retains four full verified drafts and checks the new three MVP statuses. Ordinary types, appearance slots and artifact overlays remain separate; no creature counts change.

![Unreal capture — synthetic render fixtures](../Art/ObjectInterpretations/WeaponBatch2-Unreal.png)

## Remaining checklist scope

The three entries remain unchecked for full completion. Further finishing, LOD/runtime cost review and exhaustive blindness/hallucination/mimic, identification, remembered-pile replacement and map-clear transitions remain. This batch verifies fixed displayed mapping, isolated native restore, visible/memory materials and no-turn styles; it does not claim a newly designed protocol for shuffled families or production performance. Spears are necessarily fine silhouettes at a distant 16×16 projection; inspect craftsmanship in the examination model.

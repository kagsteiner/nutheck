# Weapon batch 3: axe, mace and ordinary war hammer

Built 2026-11-03. Selected as the next coherent group of three unbuilt ordinary weapons after checking the backlog, catalogue, scripts, FBX and Unreal assets. All three now have editable geometry, painted exports, saved Unreal assets and MVP live verification. Full finishing/LOD and broader presentation transitions remain separate.

## Source facts and interpretation

Pinned `upstream/NetHack/include/objects.h` defines `AXE` at line 236, `MACE` at line 355 and `WAR_HAMMER` at line 367. All are initially known fixed appearances with `NoDes`, main material `IRON`, no shuffle group, shared-description ambiguity or cultural modifier. Runtime names are exactly `axe`, `mace`, `war hammer`. These stable enums are catalogue keys; numeric glyphs are not global IDs.

The following construction and ornament are artistic interpretation, not historical claims or additional NetHack lore:

- Axe: asymmetric bearded cutting head with varying forged cheek thickness and a thin edge, an actual boolean-cut haft eye, curved wood haft, binding, wedge and restrained bilateral brass lines.
- Mace: eight individually editable closed flanges around an iron core, bevelled striking ridges, turned collars, finial, leather grip and peened fittings. Its radial crown differs from both the axe and hammer profiles.
- War hammer: compact iron head with a broad square striking poll and tapered descending rear pick, real haft eye, wood haft, two metal reinforcement straps, rivets, collars and leather grip. It has no Mjollnir motif or magical marking.

Subsidiary wood, leather and brass fittings are construction choices; native `IRON` remains the main source material. Ornament does not encode blessing, enchantment, artifact identity, value or rarity. Generic tiles were not design targets. Static poses only.

| Model | Measured Z bounds | Parts | Triangles | Dungeon scale |
| --- | --- | ---: | ---: | ---: |
| axe | 0.0130-0.7925 m | 18 | 7,364 | 0.85 |
| mace | 0-0.7600 m | 35 | 18,844 | 0.90 |
| war hammer | 0-0.7395 m | 31 | 16,268 | 0.90 |

Editable scene: `Art/ObjectInterpretations/WeaponBatch3.blend`. Each model has its own collection and separate editable solid parts; units are metres, Z upright, broad presentation in XZ, no animation. One meshes-only FBX per key uses the established unit/axis/export settings. Studio lighting is not exported.

## Actual geometry and visual evidence

`Scripts/CreateWeaponBatch3.py`, `ReviewWeaponBatch3.py` and `CreateWeaponBatch3Boards.py` are new batch-specific scripts. They reuse the inspected geometry/paint/export helpers without modifying shared helpers or prior assets. Inspection asserts finite vertices, nonzero polygon areas, manifold closed solids, applied modifiers, unit scales, no animation, valid finite CORNER FLOAT_COLOR Paint, measured bounds and actual part/triangle counts. The axe and hammer retain their cut haft openings in the editable construction. A boolean-created empty material slot was caught during generation and removed before export/import.

`weapon-batch3-protected.json` captured SHA-256 hashes of all **226** prior canonical FBX files before generation. `weapon-batch3-inspection.json` confirms all unchanged; the baseline count is discovered rather than inherited from an older manifest.

Actual three-quarter, front, rear, underside, head/detail and six 16x16 projections per weapon were rendered, opened and inspected. Labelled boards are `WeaponBatch3-{Models,Front,Rear,Underside,Hilts,Projections}.png`; the inherited Hilts filename now contains head/construction close-ups. Pixel projections judge readability independently of generic tiles; inherited tile-overlap scores are not an art target.

![Actual three-quarter model renders](../Art/ObjectInterpretations/WeaponBatch3-Models.png)

## Unreal and displayed mapping

`ImportWeaponBatch3.py` uses the established hidden full-editor `-ExecutePythonScript` import path. Assets live at `/Game/WeaponBatch3/Meshes/SM_{axe,mace,war_hammer}`. Static meshes retain vertex colours and authored normals, combine parts, request no automatic collision or imported textures/materials. Every imported material slot has an explicit mapping. Batch-local materials preserve metallic iron (1.0), polished striking metal (1.0), brass (.75) and nonmetal wood/leather paint (0); memory variants retain the existing object .20 colour multiplier and lighting-channel treatment. `VerifyWeaponBatch3Assets.py` reloads saved packages and checks exact normal/memory slot paths and retained colour buffers.

`DungeonObjectPlacement.cpp` adds the three ordinary flat presentations. Transformed bounds center them above the floor at minimum Z=12 cm (4 cm above the existing 8 cm floor surface). Deterministic yaw does not use native gameplay RNG. Both F9 styles select these same presentations.

Known native Mjollnir is matched **before** the ordinary `war hammer` entry, preserving its separate artifact mesh and upright hovering pose. Empty or unrelated artifact metadata uses the ordinary hammer; ordinary player naming cannot activate the Mjollnir treatment. The verifier checks ordinary versus named selection, and the existing native visible-artifact test passes. Native artifact eligibility itself is unchanged.

`winue.c` adds only AXE/MACE to the fixed displayed-glyph whitelist; WAR_HAMMER was already supported. The parser needs no changes. Selection still requires `Kind == item`, reads no hidden pile contents and keeps unsupported/missing presentations on fallback. The existing strict-topmost rule hides underlying features even for named weapons. The native window-port copy in `Patches/NetHack/win/ue/winue.c` is kept in sync for reproducible builds.

## Validation and preservation

- Native build: `build-weapon-batch3-native.log`; succeeds with existing upstream/compiler warnings.
- Unreal Development build: `build-weapon-batch3-unreal.log`; succeeds.
- Geometry/render review: `build-weapon-batch3-{create,review}.log`, inspection JSON and boards.
- Import/reload: `build-weapon-batch3-import.log` has `WEAPON_BATCH3_IMPORT_READY count=3`; `build-weapon-batch3-saved-assets.log` has `WEAPON_BATCH3_SAVED_ASSETS_PASS`. Persisted slot evidence: `weapon-batch3-unreal-assets.json`. Existing engine startup automation condition messages precede the successful imports/reload checks.
- `Tests/BridgeObjectPlacement.py`: 29 ordinary presentations plus two artifacts wished, dropped and revealed through real native window events. `build-weapon-batch3-bridge.log` passes. The first isolated attempt could not find an adjacent reveal square; a fresh isolated rerun passed. Artifact inventory selection now chooses the actual wished named weapon, avoiding the newly supported ordinary hammer with the same base name.
- `Tests/BridgeWeaponBatch3.py`: each new weapon's displayed string/glyph and absence of artifact identity survive isolated native save/restore. `build-weapon-batch3-restore.log`, `weapon-batch3-restore.json` pass.
- `Tests/BridgeArtifactKnowledge.py`: visible Mjollnir/Cleaver and ordinary player naming regression passes (`build-weapon-batch3-artifact.log`).
- `Scripts/VerifyWeaponBatch3.ps1`: all **35** presentations, two visibility states and both F9 styles pass loaded mesh/material/colour-buffer, flat/standing/hover bounds, ordinary/artifact selection, fallback/non-item and no-turn checks (`build-weapon-batch3-live.log`).
- Strict-topmost regression: **840 cases pass** with the expanded registry (`build-weapon-batch3-topmost.log`). Its map rebuild clears synthetic weapon previews, so the final screenshot is a separate weapon-only capture. `WeaponBatch3-Unreal.png` is an inspected actual Unreal capture with **synthetic render fixtures**, not evidence of native spawning; native spawning is proven by the separate wish/drop event tests. Capture placement prioritizes clear floor away from walls that can obscure flat loot; the batch-only camera uses a legal steeper orbit so all three models are visible. Normal player camera settings are unaffected.
- `Tests/BridgeBackendCompatibility.py Backups/NetHackSaves/20261103T074327.634074Z.zip`: isolated old-runtime save -> new-runtime restore passes (`build-weapon-batch3-compatibility.log`).
- `Scripts/AuditWeaponBatch3Saves.py`: full file set, **1,081 player files** and LastSession pointer remain unchanged against that verified pre-change archive. Only intended `Runtime/NetHackBridge.exe` changes. Evidence: `weapon-batch3-save-preservation.json` and `build-weapon-batch3-save-audit.log`. The native build also made its required backup. No played session was launched or advanced.
- Catalogue regenerated; UTF-8 punctuation in the catalogue generator was repaired to preserve the existing readable inventory text. `Tests/ObjectCatalogue.py` passes and checks the new three scoped MVP statuses. Four fully verified old drafts remain separate from MVP counts; creature counts and artifact-overlay counts do not change.

![Unreal dungeon capture - synthetic weapon fixtures](../Art/ObjectInterpretations/WeaponBatch3-Unreal.png)

## Remaining scope

Backlog entries stay unchecked for full completion: finishing, LOD/runtime cost review and exhaustive hallucination/mimic, identification, remembered-pile replacement and map-clear transitions remain. All three fixed appearances are modelled, imported and MVP live verified. This batch does not introduce a shuffled-appearance protocol or claim production performance.

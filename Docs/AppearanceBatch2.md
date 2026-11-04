# Sapphire ring, triangular amulet and silver wand

Built 2026-11-03 as the next three unbuilt physical appearances in the object
queue, following `ObjectArtDirection.md` and `ObjectCreationWorkflow.md`.
These are scoped MVP live drafts. Magical effect identities, ordinary-object
completion counts and creature totals are unchanged.

## Native facts versus design

| Physical appearance | Source description slot | Native material | Source tile / combined atlas |
| --- | --- | --- | --- |
| Sapphire ring | RIN_AGGRAVATE_MONSTER | GEMSTONE | 187 / 976 |
| Triangular amulet | AMULET_OF_RESTFUL_SLEEP | IRON | 206 / 995 |
| Silver wand | WAN_POLYMORPH | SILVER | 424 / 1213 |

The slots and materials come from pinned `upstream/NetHack/include/objects.h`;
tile labels/order come from `win/share/objects.txt` and the generated catalogue.
`o_init.c` shuffles appearances within their native pools. The listed source
effect/description pairs are not live bindings. No aggravation, sleep or
polymorph emblem is built into any object.

The carved blue sapphire shank, twelve-sided round crown, six silver claws,
open gallery rail and split shoulders are artistic construction choices.
The triangle's forged open frame, bevels, six peened pins, bail and 48 alternating
chain links are likewise invention. The wand's tapered polished silver rod,
twisting eight-flute grip, turned ferrules, fine beading and rounded closed ends
are physical craftsmanship, not native charge/enchantment cues. No glow,
blessing, curse or rarity marking was added.

## Editable geometry and review

Source is [AppearanceBatch2.blend](../Art/ObjectInterpretations/AppearanceBatch2.blend),
with one painted FBX per `sapphire_ring`, `triangular_amulet`, `silver_wand`.
Create with `Scripts/CreateAppearanceBatch2.py`; use the saved-model
`RenderAppearanceBatch2.py`, `ReviewAppearanceBatch2.py` and
`CreateAppearanceBatch2Boards.py` for the final studio/details/tiny boards.
The studio renderer adds a broad reflection card so silver catches light along
its shaft, not only at its end caps. It is not exported or added to game lighting.

| Model | Parts | Triangles | Authored height |
| --- | ---: | ---: | ---: |
| Sapphire ring | 17 | 6028 | 35.4 mm |
| Triangular amulet and chain | 57 | 32192 | 129.7 mm |
| Silver wand | 16 | 15496 | 381.5 mm |

All saved solids pass finite/nondegenerate/manifold checks, valid CORNER
FLOAT_COLOR paint, applied scale, absence of modifiers/animation and floor
origin. The ring's actual twelve table vertices share the gem's highest XY
plane: its crown points +Z, perpendicular to its Y finger-hole axis. It is
not a pendant-facing setting. The entire gallery/prong construction agrees.

Actual renders were opened and inspected, including the silver reflection and
chain-spacing refinements:

- [Models](../Art/ObjectInterpretations/AppearanceBatch2-Models.png),
  [front](../Art/ObjectInterpretations/AppearanceBatch2-Front.png),
  [rear](../Art/ObjectInterpretations/AppearanceBatch2-Rear.png),
  [underside](../Art/ObjectInterpretations/AppearanceBatch2-Underside.png).
- [Setting / pendant / grip details](../Art/ObjectInterpretations/AppearanceBatch2-Hilts.png).
- [Eighteen true 16×16 projections](../Art/ObjectInterpretations/AppearanceBatch2-Projections.png),
  for physical readability, not tile-fidelity scoring. Tiny silver rods and chain
  remain thin; fine beading is examination detail, not a distant silhouette cue.
- [Actual Unreal fixture](../Art/ObjectInterpretations/AppearanceBatch2-Unreal.png).

`ImportAppearanceBatch2.py` targets only `/Game/AppearanceBatch2`. Dedicated
sapphire, silver, darker silver, iron and darker iron materials preserve distinct
roughness and metalness, with 20% memory variants. Sapphire is currently opaque
and glossy; transmission/refraction remains finishing work. Exported meshes
contain no studio lights, animation or gameplay collision.

## Runtime presentation

The existing public native `fg->gm.tileidx` protocol already supplies the three
appearance tiles. No backend rebuild, new whitelist or hidden effect metadata
was needed. `DungeonObjectPlacement.cpp` adds three tile-keyed registry rows;
`Kind == item` is required, and unsupported/missing models keep the fallback.
Underlying effect glyphs and invented object names cannot override that tile.

The ring stands crown-up at the established jewelry miniature scale 11.
Amulet and wand lie face-up, at scales 3.6 and 1.9. FBX handedness and transformed
bounds determine centering and 12 cm floor height (4 cm above the floor's top).
Native terrain remains intact; strict topmost presentation suppresses covered
features. Both F9 styles retain the same ordinary object geometry and memory
materials, without spending a turn. No physical pile stacking is introduced.

## Verification and preservation

- `Tests/BridgeAppearanceBatch2.py`: nine fresh-game wish/drop/identify/restore
  cases, three per appearance, with multiple underlying effects for each tile.
  Sapphire observed gain strength/conflict/warning, triangle reflection/restful
  sleep/change, and silver make invisible/death. Identification changed native
  text while preserving the displayed glyph/tile through normal save/restore.
- `Tests/BridgeAppearanceBatch2Transitions.py`: all three appearances individually
  pass native dagger cover/pick-up/uncover, blind memory across restore, and
  hallucination using native random tiles rather than the hidden real appearance.
- `Tests/CreateAppearanceBatch2Capture.py`: three actual native wished appearances
  in one fresh generated room. Only this disposable fixture controls lighting
  and disables monsters/traps; it is not proof of random natural spawning.
- UE editor build, targeted import and fresh-editor saved-mesh/paint/slot/material
  checks pass. Roughness and metallic graph inputs are independently verified.
- `VerifyAppearanceBatch2`: twelve appearance/style/visibility bindings, crown
  or face-up transforms, memory slots, shared-tile aliases, unknown/monster and
  unsupported-tile fallbacks; 48 rendered comparisons confirm covered altars,
  fountains, sinks and traps match neutral-floor presentation for all three.
- Live capture also passes existing object placement, 1200 strict-topmost cases,
  F9/no-turn restoration, native live/default-tile and legal 8× camera checks.
  Native cells, hero, turn and sequence are restored after presentation checks.
- All **254 preceding canonical FBXs** and **430 preceding Unreal uassets**
  remain byte-identical. This batch uses separate meshes/materials.
- Verified backup `20261103T191533.981595Z.zip`: all **1091 player/runtime files**,
  file set, configuration, pointer and backend remain unchanged. No player
  session was opened, advanced, force-closed or replaced. Test/capture roots are
  isolated; the ordinary player pointer is never used. No runtime replacement
  occurred, so an old-runtime compatibility experiment is not needed.
- Object catalogue generation/tests keep these three entries under physical
  appearance slots; their default source effect identities remain uncompleted.
  There are now six scoped appearance drafts across batches 1 and 2; the four
  fully verified older object drafts, 37 ordinary MVP presentations and two
  artifact treatments retain their separate counts.

Evidence is `Art/ObjectInterpretations/appearance-batch2-{inspection,native,
transitions,fixture,live,unreal-assets,save-preservation}.json`, plus protected
FBX/Unreal manifests. Logs are `build-appearance-batch2-*.log`. Reproduce engine
checks with `Scripts/VerifyAppearanceBatch2.ps1`; save audit is
`Scripts/AuditAppearanceBatch2Saves.py`. Per-launch local DDC fallback changes no
player or project configuration.

Human visual testing, gemstone optics, small-scale metal/chain readability and
LOD/runtime-cost review remain finishing work. These are static, scoped MVP
drafts, not full magical-category completion or a production performance claim.

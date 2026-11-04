# Centaurs and white-marble statues

User direction, 2026-11-03: statues depict their respective creatures in pure
white marble. Reuse the creature's geometry, rather than creating independent
statue designs. The three centaurs and the shared statue renderer are implemented
and live verified. These are static art drafts; finishing and LOD work remain.

## What the Oracle room creates

Pinned `upstream/NetHack/dat/oracle.lua:9–16` creates eight **historic statues**
with `montype="C"`: four outer corners and four intermediate positions. Each
species is selected from the centaur class, rather than a fixed lineup:
**plains centaur, forest centaur, mountain centaur**. Historic status and any
native contents/traps have no extra visual decoration. No room geometry, statue
positions, object material or gameplay rules were changed.

The isolated observed fixture contains six plains, one forest and one mountain
centaur statue. That is evidence of this generated level, not a universal ratio.
`statues-native-oracle.json` records the eight displayed glyphs, coordinates,
sexes and successful restore. The Oracle room's saved identity remains independent
of the monster's life, as implemented in `OracleSanctuary.md`.

## Creature art

Native `include/monsters.h` defines all three as large, strong, omnivorous
humanoids with weapon and kicking attacks; mountain has a second kick. A weapon
attack does not establish visible equipment, so these fixed models carry none.
Official tiles 264–269 show peach human upper bodies, chestnut/brown equine bodies,
hair and hooves. ASCII green/cyan species colours are not anatomical paint.
Each male/female pair is identical; the contributing artist explicitly notes
that the sexes are not differentiated. Each pair shares one sculpt.

The editable `Art/CreatureInterpretations/Centaurs.blend` contains three separately
proportioned complete horse/human figures. Plains has a raised conversational
hand; forest is leaner and raises its hand higher; mountain is broader, with
lowered arms and a brown jerkin. Beards, detailed hands, fitted eyes, complete
backs/tails and folded clothing are anatomical/artistic interpretations of sparse
tiles, not additional gameplay facts. Offset right/lower black cast shadows are
excluded with reviewed spatial masks; small upper dark anatomy is retained.
The original source images are unchanged.

| Creature | Mesh parts | Triangles | Approximate height |
|---|---:|---:|---:|
| Plains centaur | 38 | 266,280 | 1.91 m |
| Forest centaur | 38 | 247,080 | 1.91 m |
| Mountain centaur | 39 | 299,904 | 1.99 m |

`CreateCentaurs.py` exports three painted FBXs. `ReviewCentaurs.py` inspects the
saved scene without regenerating it: finite/nondegenerate geometry, closed solids
except deliberate fitted-eye paint patches, connected human/equine body meshes,
four hooves, complete hands, two fitted eyes, valid Paint, floor origin, no
pending modifiers or animation. All **234 preceding canonical FBX hashes** match
`centaurs-protected.json`. Source-sex equality is asserted from the tile file.

Actual evidence:

- [Living and marble models](../Art/CreatureInterpretations/Centaurs-Models.png).
- [Front, face, rear and underside review](../Art/CreatureInterpretations/Centaurs-Details.png).
- [Official tiles and six true 16×16 projections per sculpt](../Art/CreatureInterpretations/Centaurs-Projections.png).
- [Native Oracle-level capture](../Art/CreatureInterpretations/Statues-Unreal.png).

`ImportCentaursAndMarble.py` imports only these three new meshes into
`/Game/CreatureInterpretations/Meshes/SM_<centaur>`, reusing existing M_Paint/M_Eye.
Living centaurs use the established displayed-monster/F9 path with cell-scale
placement. No prior creature was regenerated or reimported.

## Shared statue presentation

The native bridge adds `display_statue` and `female` only when
`glyph_is_statue(g)` holds. `glyph_to_statue_corpsenm` and `glyph_is_fem_statue`
cover ordinary, pile-top and remembered statue glyphs. There is no floor-object,
monster, trap or container-content lookup. An unresolved generic statue does not
gain a guessed creature identity. During hallucination native statues appear as
random monsters; their hidden actual species never forces marble presentation.

`NetHackSession.cpp` clears stale statue metadata on each tile event.
`DungeonStatues.cpp` requires an item explicitly displayed as a statue, then
resolves the matching canonical creature mesh, automatically preferring an available female variant, including the four
established female sculpts. Matching fixed human player forms or existing default-tile volumes can
serve as geometry where appropriate. New canonical creature meshes automatically
enable the corresponding statues, without a per-statue whitelist.

The renderer overrides **every material slot on the component** with
`/Game/Statues/M_WhiteMarble`: base RGB **(1,1,1)**, roughness **0.28**, metallic
**0**, specular **0.5**. It reads no vertex paint and contains no veins, coloured
eyes, metal fittings or retained clothing colours. Lighting still shades the
white surface naturally. Remembered statues use a uniform neutral 20% material
and the existing memory lighting channel. Shared mesh/material assets remain
unchanged, so living creatures retain their colours and material properties.
Both F9 styles retain the marble treatment for statues.

Bounds center each sculpture, cap its footprint to 88% of a square, and put its
lowest point 1 cm above the floor. No pedestal, physical stacking, collision or
additional native object is introduced. The hero/foreground and native pile-top
continue to take precedence. A dagger covering a statue displays only the dagger.

Current saved-asset inventory supports **202 display-sex forms across 101 source
IDs**, including legacy volume proxies and roles; these are not 202 independent
sculpts. **Unmodelled species keep their official native statue tiles** until a
matching mesh exists. `statue-model-coverage.json` lists both supported forms and
remaining native-tile fallbacks. The all-species statue checklist remains open.

## Verification and preservation

- Native and Unreal Development builds pass.
- `Tests/BridgeCentaurs.py`: all six living centaur display aliases pass through
  native wizard generation, including correct sex and official tile indices.
- `Tests/CreateStatueCapture.py`: a fresh native Oracle level supplies all eight
  historic statue positions. All are visited and their displayed species/sexes
  survive normal save/restore. No played save is used.
- `Tests/BridgeStatues.py`: eight statue species/sex restore cases, including an
  unmodelled red dragon; dagger-over-statue suppression; hallucination displaying
  a native random monster with no statue metadata all pass.
- `VerifyCentaurAssets.py`: reloads saved meshes/materials, checks paint and every
  imported slot, and verifies the marble shader's actual constant colour,
  roughness, metallic and specular connections. Neither marble shader reads
  vertex colours. Coverage is computed from existing asset paths.
- `VerifyStatues.ps1`: 56 model/style/visibility cases, six living centaur aliases,
  all-slot marble, unchanged living materials, floor/footprint bounds, unsupported
  and wrong-kind guards, actual eight-statue mapping and both F9 toggles pass at
  unchanged **turn 18 / sequence 2**. Sanctuary, live map, default presentation and
  4× zoom also pass. The screenshot uses real native statues, normal high walls,
  native memory/visibility and hidden F7 badges; no synthetic statues were inserted.
- Verified pre-change backup: `20261103T114902.378796Z.zip`. The isolated
  `BridgeBackendCompatibility.py` old-save/new-runtime check passes.
  `AuditStatueSaves.py` confirms the file set and **all 1,081 played files**,
  including LastSession, remain identical. Of 1,090 archived files only the
  intended `Runtime/NetHackBridge.exe` changed. Backups/originals are retained.

Remaining: human visual review, refinement of faces/limb/cloth transitions,
LOD/performance work for these dense drafts, and remaining creature models for
full statue coverage. The native object's mineral material, historic behaviour,
contents, traps, petrification and stone-to-flesh rules remain authoritative.

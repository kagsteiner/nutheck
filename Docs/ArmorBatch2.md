# Plate armor and the full dragon-scale-mail family

Update, 2026-11-02: these models are now connected to the live dungeon under the
[MVP placement rules](MVPObjectPlacement.md), with isolated native mapping and
Unreal placement checks passed. Earlier pending-live statements below describe
the original art-only milestone. Finishing and broader edge-case review remain
separate from MVP placement; full-completion checkboxes are unchanged.

Recommended working batch size: three related basic armor types. This request
also explicitly scopes the complete dragon-mail family, built as a dedicated
ten-variant batch with a common construction and separately reviewed palettes.

**Current dragon design:** the user rejected the large slab-like scales.
[DragonMailReferenceRevision.md](DragonMailReferenceRevision.md) supersedes the
initial dragon construction below with small rounded leaf scales and curved
layered shoulders across all ten colours. Plate/crystal/bronze assets are unchanged.

## Native facts

Pinned `include/objects.h` defines plate mail (IRON), bronze plate mail (COPPER)
and crystal plate mail (GLASS). Crystal's polished appearance is cosmetic: it
does not confer the reflection property. Dragon scale mail is DRAGON_HIDE.
Ten active colours are gray, gold, silver, red, white, orange, black, blue,
green and yellow. Shimmering is inside a deferred `#if 0` block and is excluded.

**Gray grants ANTIMAGIC (magic resistance); black grants DISINT_RES
(disintegration resistance).** Gray remains the user's requested visual showpiece;
this clarification changes no gameplay. Silver grants reflection; red fire,
white cold, orange sleep, blue shock, green poison and yellow acid resistance.
Gold has native light-source behaviour. This study adds no independent renderer
glow or light source; that must follow native display when live mapping is added.
These are source properties, not hidden-state labels painted onto the designs.

## Initial art interpretation (dragon design superseded by reference revision)

Plate armor has a hollow metal torso, raised ridged front/back cuirass, waist
lames, rivets and articulated lower tassets. Steel is dark and polished; bronze
is warm. Crystal has pale faceted plates and a highly polished layered finish:
roughness .055, clearcoat 1, coat roughness .025, with stylised metallic response
.75 to satisfy the requested mirror-like appearance. This is an opaque game-art
interpretation, not physically accurate transparent glass. It is explicitly
different from the native magical reflection property.

Dragon mail has more than 400 individually closed pointed/keeled scales per
variant, staggered around the full torso, larger breast scutes, layered shoulder
plates and two swept horns. No rings are used as substitute scales. Pigment
variation remains on the geometry. Gray adds three silver collar crest scales,
silver horn treatment and a large nested silver-rimmed pectoral scale. Exact
horns, layering, tailoring and material treatments are artistic assumptions.
Their ornament does not claim an enchantment, blessing, curse or artifact ID.
All colours are present, including restrained charcoal black and pale white.
Scales and mail are separate native object types: these models do not complete
the unworked loose dragon-scales inventory.

## Artifacts and verification

`Art/ObjectInterpretations/ArmorBatch2.blend` contains thirteen editable named
collections and painted meshes. Canonical exports use their native names with
underscores. Actual front-quarter/rear/front/underside images exist for every
form; six actual 16x16 projections per form are documented in
`projection-report-armor-batch2.json`. Tiles are ignored for design; tiny views
are readability diagnostics. Prior 104 canonical exports are protected by
`armor-batch2-protected.json`.

Scripts: `CreateArmorBatch2.py`, `ArmorBatch2Config.py`, `InspectArmorBatch2.py`,
`ReviewArmorBatch2.py`, `CreateArmorBatch2Boards.py` and `ImportArmorBatch2.py`.
Unreal destination `/Game/ArmorBatch2` isolates all new assets/materials from
the earlier armor and weapon studies. Crystal has an explicit clearcoat shader;
each dragon colour retains its own material, plus dark backing, horns and trim.
Normal/memory materials share paint; remembered paint is multiplied by .20.
Logs use `build-armor-batch2-*`.

The initial import exposed an Unreal Python limitation: the
[MaterialProperty enum](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MaterialProperty?application_version=5.7)
does not expose the custom clearcoat properties. The final importer connects
named ClearCoat/ClearCoatRoughness pins on MakeMaterialAttributes instead, with
assertions on every connection. Final evidence uses
`build-armor-batch2-import-final.log`; the initial failed log is retained.

**Design/import drafts; live mapping and native appearance checks remain pending.**
As with the preceding studies, no backend or played-session changes are made.
No gameplay is launched. Native appearance/pile/memory/hallucination/save/fallback
and no-turn checks must pass before marking live-object checklist completion.
Four existing live objects and 78/381 creatures remain the current coverage.

Raised-plate attachment, armhole tailoring, scale overlap/intersections, horn
integration, small-scale readability and LODs remain visual finishing work.
Static objects are the intended presentation; equipped-player clothing and rigs
are outside this study.

## Initial batch design checks (retained history)

All thirteen saved geometry checks pass: finite/nonzero closed surfaces, valid
corner paint and all 104 prior canonical exports unchanged. Each plate has
21,704 triangles; gray dragon mail has 23,790; each of the other nine dragon
mails has 23,680. Each dragon mail has over 400 actual scales, two shoulder horns
and complete rear geometry; gray has three additional collar crest pieces.
These costs exclude future LOD decisions.

All thirteen final Unreal imports validate paint and material assignment;
the final marker is `ARMOR_BATCH2_IMPORT_READY count=13 crystal_clearcoat=True`.
Source-catalogue tests pass in `build-armor-batch2-catalogue-tests.log`.
All actual studio/front/rear/interior views and 78 tiny projections were inspected.
Boards use `ArmorBatch2-Plate-*`, `ArmorBatch2-Dragons-*` and
`ArmorBatch2-Projections.png` under the object art folder. The imported assets
have not been visually tested in live gameplay; live eligibility remains pending.

Suggested next basic batch: splint mail, scale mail and ring mail, with real
construction differences and source-appearance review. Dragon scales as loose
items remain a separate future task.

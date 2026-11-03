# Objects: beautiful, distinctive loot

Start here for a new build session: read this file and follow the complete
[Object creation workflow](ObjectCreationWorkflow.md). That workflow specifies
batch selection, editable modelling, export, visual review, Unreal/live integration,
save-safe validation and progress updates. This file supplies the art direction.

User direction, 2026-11-02: build a complete object list and backlog. Objects
deserve focused work alongside creatures. Loot should be beautiful and rewarding
to discover; interpret weapons and equipment more creatively than a literal
extrusion of their tiny tiles. Differences between items matter more than making
a large collection of nearly identical generic objects.

Later user clarification: the user will revisit detailed art direction later.
Weapons granted as gifts by the player's god deserve especially exceptional,
memorable designs. Record that priority for the future review; it does not
authorize object generation now or a hidden divine-gift marker in the renderer.

## A shallow hierarchy, with useful facets

Use **native category → visual family** for finding and batching work. Within
Weapons, for example: swords/long blades, daggers/short blades, axes/picks,
polearms, launchers, ammunition/thrown weapons, flexible weapons and blunt arms.
Armor groups by body slot. Tools group by construction and function. Potions,
rings, wands and amulets have appearance families of their own.

Material, cultural cues, construction, ornament and wear are tags/facets, not a
deep compulsory inheritance tree. Reuse a blade or bottle construction where it
helps, but do not let one “sword mesh” erase the difference between a long sword,
scimitar, katana, two-handed sword and elven blade. A class in NetHack is not a
claim that every object in it can share a final silhouette.

The source list is [Inventory.md](../Art/ObjectCatalogue/Inventory.md), with
filterable JSON/CSV alongside it. The working checklist is
[object-backlog.md](../object-backlog.md). Stable object enum names are keys;
numeric enum offsets and display names are not global identifiers.

## Make the loot worth looking at

- Contrary to the monsters, where we try to follow the tiles in how they look, weapons have a very generic look, All armor looks like generic shields. Same for helmets. When creating the 3D model, completely ignore the tiles. Instead, use your knowledge and Blender guides on weapon and armor construction to build them. 
- Give each weapon family clear blade/head profiles, proportion, edge treatment,
  guard, grip and pommel construction. Differences should read at normal dungeon
  distance, with finer craftsmanship visible when examined closely.
- Use coherent motifs and material treatment: restrained inlay, engraving,
  wrapped grips, worked wood, forged surfaces, polished edges, decorated fittings
  and subtle use-wear. Design the whole object, including its rear and underside.
- Let elven, orcish and dwarvish source cues guide distinct design languages;
  exact ornament is artistic interpretation, not additional lore or equipment
  information. Document source facts separately from invention.
- Extend the same care to armor construction, jewelry settings, wand handles,
  bottle silhouettes, scroll labels and tool mechanisms. Everyday loot may be
  beautifully made too. Do not reserve all interesting art for artifacts.
- Artifacts have a separate design queue linked to their base object types.
  Their names and source themes offer room for memorable designs, subject to
  the same native-information boundary as ordinary items.
  - Invest special care and attention to detail when creating the named weapons. These are usually gifted to you by your god or as the prize for a quest. Make them awesome.

Keep the established miniature/world scale, coherent sculpt/material language,
real geometry and shadows. Preserve recognizable physical type and actual
visible material/appearance cues while allowing more creative craftsmanship.
Colour and texture alone should not carry every distinction. Static objects
remain the intended finished presentation; no opening/swinging animation is
required. Beauty does not change native damage, price, rarity or rules.

## Identity and appearance are different inventories

The generated source inventory has **440 named object types**: 439 unconditional
types and conditional mail. It also records **463 non-auxiliary source appearance
slots**, including **23 extra descriptions** (20 scroll labels and 3 wand forms),
**18 display auxiliaries**, **4 deferred object types**, and **33 current artifact
overlays** plus one obsolete artifact. All **483 official object tile definitions**
are accounted for; two are deferred shimmering-dragon armor tiles. Those source
tiles do not establish that the deferred objects are available in normal play.
These are separate scopes, not numbers to add into one “unique meshes” total.

`objects.json` describes native identities. `appearances.json` describes default
appearance slots, keyed separately and linked to the native shuffle pools.
`artifacts.json` describes named overlays on base objects. JSON retains source
locations, conditions, physical categories, materials, traits, default tile
references and current draft status. CSV supports browsing/filtering.

`o_init.c::obj_shuffle_range`, `shuffle_all` and `shuffle` determine actual
appearance shuffling. Potions, rings, wands, scrolls, spellbooks and amulets have
pools/exceptions; some helmets, gloves, cloaks and boots also shuffle. Materials
and colours can move with descriptions. Shared descriptions outside those pools
also matter: two identical-looking conical hats or gray stones must not acquire
type-revealing ornament merely because they have separate source enum names.

Therefore a source pairing such as “ruby / gain ability” is **not** a permanent
gameplay mapping. A ruby potion can have different effects in different games.
Build a beautiful ruby appearance, not an invisible-effect-specific bottle.
Identifying it should not magically change its physical design; its known
properties belong in native text/UI unless NetHack actually supplies a visible
distinction. The same applies to jewelry and armor. Shared appearances may need
one indistinguishable physical design even when source tiles differ slightly.

Do not encode hidden enchantment, blessing/curse, charges, artifact identity,
contents, traps or item value in geometry, colour, glow or decorative symbols.
An effect-specific emblem can spoil an unidentified item just as surely as its
name. A special artifact treatment is eligible only when the native displayed
information supports distinguishing it; otherwise preserve the legal base look.
Do not invent colour-coded rarity or a new loot-tier system.

Runtime selection must continue from native displayed appearance/tile and
explicit permitted knowledge. Never select unknown magical effects through
hidden object type. Before extending `display_object` beyond the current fixed
whitelist, design and test the appearance/knowledge protocol across new games,
save/restore, piles, memory, hallucination and identification.

## Progress and future work

Dragon-mail reference correction: reject large breast/shoulder slabs and faceted
pyramid scales. Use small, rounded overlapping leaf scales, fitted tailoring and
curved layered pauldrons, following the user's two armor photographs. Keep gray
special through fine silver edging rather than a huge chest badge. This overrides
the first dragon-mail draft; see `DragonMailReferenceRevision.md`.

2026-11-02 armor direction: crystal plate mail should be highly polished and
mirror-like. Dragon scale mail should look exceptional and unmistakably made
from overlapping dragon scales, in all ten active native colours; gray is the
visual showpiece. Native fact: gray grants magic resistance, black grants
disintegration resistance. Preserve the requested gray emphasis without changing
or mislabelling game properties. Gold is active in this pinned source;
shimmering is deferred. See `ArmorBatch2.md` for the current design study.

The four existing fixed presentations—large box, chest, gold piece and generic
corpse—remain verified drafts. This inventory work generates no new meshes and
changes no runtime, game session or save. It does not mark other items complete.
The corpse is generic; the statue/corpse species cross-product remains a separate
display-scope task. Artifact designs and physical appearance slots are not extra
ordinary object types. Source family groups are modelling proposals.

Long sword, scimitar and katana already have editable models and MVP live
placement, alongside twenty armor/cloak models and Cleaver/Mjollnir. Dagger, short sword and spear now also have editable models and
[MVP live verification](WeaponBatch2.md); finishing and extended transitions remain
explicitly separate in the backlog. A jewelry/consumable appearance study follows
as a separate family task.
This is a queue, not a request to generate objects automatically. Verify each
asset with editable geometry, painted export, actual multi-angle/tiny renders,
Unreal material/import checks, displayed mapping/fallback, memory and no-turn
presentation checks. Keep visual finishing and LOD/runtime review separate.

## MVP dungeon placement (2026-11-02)

Armor and cloaks stand upright. Ordinary weapons lie flat. Known named weapons
hover upright; the first two implemented treatments are Cleaver and Mjollnir.
Use static poses for now. Native displayed knowledge decides identity; presentation
must not reveal hidden pile contents or a name the player cannot yet see.
A visible artifact name qualifies before full identification; do not gate its
special pose on the full-identification discovery list. See
[MVP implementation and verification](MVPObjectPlacement.md).

## Strict topmost presentation (2026-11-03)

Only NetHack's displayed foreground is presented above a neutral floor. Raised
terrain features (including altars) disappear beneath items, creatures, effects
and the hero, and return when uncovered. A pile of ten or a hundred objects still
shows just its native displayed top item. Known named weapons keep their static
hover pose but do not reveal an altar underneath. The user likes the idea of a
named weapon hovering over an altar as a future artistic possibility; it is not
an exception to this rule. See [implementation and verification](TopmostPresentation.md).

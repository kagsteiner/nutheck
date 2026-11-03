# Object asset backlog

Working checklist, created 2026-11-02. Maintained by hand: catalogue regeneration must never replace checkboxes, priorities, review notes or evidence.

**440 named source object types: 439 unconditional + 1 conditional mail type. Four verified fixed-object drafts; 436 types remain.**
There are also 463 non-auxiliary default appearance slots (including 23 extra shuffled descriptions), 18 display auxiliaries, 4 deferred types and 33 current artifact overlays. These scopes are not additive unique-mesh counts.

MVP integration update: the three swords, twenty armor/cloak models, Cleaver and
Mjollnir now have [live placement](Docs/MVPObjectPlacement.md). Dagger, short sword and spear now also have [MVP live placement](Docs/WeaponBatch2.md). That is 30 ordinary
presentations including the four older models, plus two artifact treatments.
Full art/edge-case completion counts and checkboxes above remain separate.


Read [Object art direction](Docs/ObjectArtDirection.md) and follow the
[Object creation workflow](Docs/ObjectCreationWorkflow.md) before modelling. User direction: make loot beautiful, distinctive and rewarding; allow more creative craftsmanship while preserving visible type/material cues and NetHack information boundaries.

## How to use this checklist

- Navigate by native category → useful visual family. Treat materials, cultural cues, construction and finish as facets. Reuse generators without making every sword, ring or bottle interchangeable.
- Query [objects.json](Art/ObjectCatalogue/objects.json) by stable enum ID. Browse [Inventory.md](Art/ObjectCatalogue/Inventory.md) or filter [objects.csv](Art/ObjectCatalogue/objects.csv). Source inventory includes conditional/deferred records; review scope before modelling.
- Use [appearances.json](Art/ObjectCatalogue/appearances.json) / [appearances.csv](Art/ObjectCatalogue/appearances.csv) for physical appearance slots and shuffle groups. Default source effect/description pairings are not live bindings.
- For shuffled types, a checkbox needs coverage by the legal 3D appearance family and verified native mapping. A mesh for one named effect does not complete it. Indistinguishable native appearances must stay indistinguishable. The source appearance slots are not a requirement for one mesh each.
- Check only after editable geometry, painted export, actual front/rear/tiny comparisons, UE import/material, displayed mapping/fallback/memory and no-turn checks exist. Official tile fallback alone is not a completed 3D draft. Add evidence beside the existing item.
- Leave incomplete items unchecked with artifact paths and the exact remaining step. Keep refinement/LOD costs separate; static objects are the target and animation is out of scope.
- Preserve all existing four completed presentations. Generic corpse does not finish species-specific corpse/statue representations. Artifact overlays are not ordinary base types and do not require unique geometry when lawful reuse suffices.
- Regenerate metadata with `Scripts/CreateObjectCatalogue.py`; it never writes this checklist, models, runtime files or saves. Update the selected-object registry only after verification, then reconcile counts and checklist notes.

## Suggested object work

1. Long sword, scimitar and katana now have a [design/import craftsmanship study](Docs/WeaponBatch1.md). Review finish and native live mapping separately. Dagger, short sword and spear now have an [editable/imported and MVP live verified batch](Docs/WeaponBatch2.md), with independent proportions and construction. Full edge-case completion remains separate.
2. A ring, amulet and wand appearance study: coherent jewelry/metal/wood language; choose physical source appearances, not effect-coded ornament.
3. Potion/scroll appearance pipeline: bottles, liquids and labels; verify native shuffling and persistence before completing effect identities.
4. Artifact designs linked to base types, with an explicit native-knowledge eligibility rule before unique live visuals.

These are future priorities, not an instruction to generate assets automatically.

## Named object types

| Category | Source types | Verified drafts |
| --- | ---: | ---: |
| Weapons | 71 | 0 |
| Armor | 84 | 0 |
| Rings | 28 | 0 |
| Amulets | 13 | 0 |
| Tools | 50 | 2 |
| Food | 33 | 1 |
| Potions | 26 | 0 |
| Scrolls | 23 | 0 |
| Spellbooks | 44 | 0 |
| Wands | 25 | 0 |
| Coins | 1 | 1 |
| Gems and stones | 36 | 0 |
| Large rocks and statues | 2 | 0 |
| Punishment gear | 2 | 0 |
| Venom | 2 | 0 |

### Weapons

#### Ammunition and thrown weapons

- [ ] **arrow** (`ARROW`).
- [ ] **elven arrow** (`ELVEN_ARROW`) — default appearance: runed arrow.
- [ ] **orcish arrow** (`ORCISH_ARROW`) — default appearance: crude arrow.
- [ ] **silver arrow** (`SILVER_ARROW`).
- [ ] **ya** (`YA`) — default appearance: bamboo arrow.
- [ ] **crossbow bolt** (`CROSSBOW_BOLT`).
- [ ] **dart** (`DART`).
- [ ] **shuriken** (`SHURIKEN`) — default appearance: throwing star.
- [ ] **boomerang** (`BOOMERANG`).

#### Polearms and thrusting weapons

- [ ] **spear** (`SPEAR`) — editable, imported and MVP live verified; [models, review boards and safe native/Unreal evidence](Docs/WeaponBatch2.md). Remaining: extended hallucination/mimic/pile/memory transitions, finishing and LOD review.
- [ ] **elven spear** (`ELVEN_SPEAR`) — default appearance: runed spear.
- [ ] **orcish spear** (`ORCISH_SPEAR`) — default appearance: crude spear.
- [ ] **dwarvish spear** (`DWARVISH_SPEAR`) — default appearance: stout spear.
- [ ] **silver spear** (`SILVER_SPEAR`).
- [ ] **javelin** (`JAVELIN`) — default appearance: throwing spear.
- [ ] **trident** (`TRIDENT`).
- [ ] **partisan** (`PARTISAN`) — default appearance: vulgar polearm.
- [ ] **ranseur** (`RANSEUR`) — default appearance: hilted polearm.
- [ ] **spetum** (`SPETUM`) — default appearance: forked polearm.
- [ ] **glaive** (`GLAIVE`) — default appearance: single-edged polearm.
- [ ] **halberd** (`HALBERD`) — default appearance: angled poleaxe.
- [ ] **bardiche** (`BARDICHE`) — default appearance: long poleaxe.
- [ ] **voulge** (`VOULGE`) — default appearance: pole cleaver.
- [ ] **fauchard** (`FAUCHARD`) — default appearance: pole sickle.
- [ ] **guisarme** (`GUISARME`) — default appearance: pruning hook.
- [ ] **bill-guisarme** (`BILL_GUISARME`) — default appearance: hooked polearm.
- [ ] **lucern hammer** (`LUCERN_HAMMER`) — default appearance: pronged polearm.
- [ ] **bec de corbin** (`BEC_DE_CORBIN`) — default appearance: beaked polearm.
- [ ] **lance** (`LANCE`).

#### Daggers and short blades

- [ ] **dagger** (`DAGGER`) — editable, imported and MVP live verified; [models, review boards and safe native/Unreal evidence](Docs/WeaponBatch2.md). Remaining: extended hallucination/mimic/pile/memory transitions, finishing and LOD review.
- [ ] **elven dagger** (`ELVEN_DAGGER`) — default appearance: runed dagger.
- [ ] **orcish dagger** (`ORCISH_DAGGER`) — default appearance: crude dagger.
- [ ] **silver dagger** (`SILVER_DAGGER`).
- [ ] **athame** (`ATHAME`).
- [ ] **scalpel** (`SCALPEL`).
- [ ] **knife** (`KNIFE`).
- [ ] **stiletto** (`STILETTO`).
- [ ] **worm tooth** (`WORM_TOOTH`).
- [ ] **crysknife** (`CRYSKNIFE`).

#### Axes and picks

- [ ] **axe** (`AXE`).
- [ ] **battle-axe** (`BATTLE_AXE`) — default appearance: double-headed axe.
- [ ] **dwarvish mattock** (`DWARVISH_MATTOCK`) — default appearance: broad pick.

#### Swords and long blades

- [ ] **short sword** (`SHORT_SWORD`) — editable, imported and MVP live verified; [models, review boards and safe native/Unreal evidence](Docs/WeaponBatch2.md). Remaining: extended hallucination/mimic/pile/memory transitions, finishing and LOD review.
- [ ] **elven short sword** (`ELVEN_SHORT_SWORD`) — default appearance: runed short sword.
- [ ] **orcish short sword** (`ORCISH_SHORT_SWORD`) — default appearance: crude short sword.
- [ ] **dwarvish short sword** (`DWARVISH_SHORT_SWORD`) — default appearance: broad short sword.
- [ ] **scimitar** (`SCIMITAR`) — design/import draft; [model and craftsmanship study](Docs/WeaponBatch1.md). Remaining: native displayed-appearance/pile/memory/hallucination/save/fallback/no-turn live checks.
- [ ] **silver saber** (`SILVER_SABER`).
- [ ] **broadsword** (`BROADSWORD`).
- [ ] **elven broadsword** (`ELVEN_BROADSWORD`) — default appearance: runed broadsword.
- [ ] **long sword** (`LONG_SWORD`) — design/import draft; [model and craftsmanship study](Docs/WeaponBatch1.md). Remaining: native displayed-appearance/pile/memory/hallucination/save/fallback/no-turn live checks.
- [ ] **two-handed sword** (`TWO_HANDED_SWORD`).
- [ ] **katana** (`KATANA`) — design/import draft; [model and craftsmanship study](Docs/WeaponBatch1.md). Remaining: native displayed-appearance/pile/memory/hallucination/save/fallback/no-turn live checks.
- [ ] **tsurugi** (`TSURUGI`) — default appearance: long samurai sword.
- [ ] **runesword** (`RUNESWORD`) — default appearance: runed broadsword.

#### Clubs, hammers and staves

- [ ] **mace** (`MACE`).
- [ ] **silver mace** (`SILVER_MACE`).
- [ ] **morning star** (`MORNING_STAR`).
- [ ] **war hammer** (`WAR_HAMMER`).
- [ ] **club** (`CLUB`).
- [ ] **quarterstaff** (`QUARTERSTAFF`) — default appearance: staff.
- [ ] **aklys** (`AKLYS`) — default appearance: thonged club.

#### Flexible weapons

- [ ] **rubber hose** (`RUBBER_HOSE`).
- [ ] **flail** (`FLAIL`).
- [ ] **bullwhip** (`BULLWHIP`).

#### Launchers

- [ ] **bow** (`BOW`).
- [ ] **elven bow** (`ELVEN_BOW`) — default appearance: runed bow.
- [ ] **orcish bow** (`ORCISH_BOW`) — default appearance: crude bow.
- [ ] **yumi** (`YUMI`) — default appearance: long bow.
- [ ] **sling** (`SLING`).
- [ ] **crossbow** (`CROSSBOW`).


### Armor

#### Headwear

- [ ] **elven leather helm** (`ELVEN_LEATHER_HELM`) — default appearance: leather hat.
- [ ] **orcish helm** (`ORCISH_HELM`) — default appearance: iron skull cap.
- [ ] **dwarvish iron helm** (`DWARVISH_IRON_HELM`) — default appearance: hard hat.
- [ ] **fedora** (`FEDORA`).
- [ ] **cornuthaum** (`CORNUTHAUM`) — default appearance: conical hat.
- [ ] **dunce cap** (`DUNCE_CAP`) — default appearance: conical hat.
- [ ] **dented pot** (`DENTED_POT`).
- [ ] **helm of brilliance** (`HELM_OF_BRILLIANCE`) — default appearance: crystal helmet.
- [ ] **helmet** (`HELMET`) — default appearance: plumed helmet; shuffled pool `helmet_appearances`.
- [ ] **helm of caution** (`HELM_OF_CAUTION`) — default appearance: etched helmet; shuffled pool `helmet_appearances`.
- [ ] **helm of opposite alignment** (`HELM_OF_OPPOSITE_ALIGNMENT`) — default appearance: crested helmet; shuffled pool `helmet_appearances`.
- [ ] **helm of telepathy** (`HELM_OF_TELEPATHY`) — default appearance: visored helmet; shuffled pool `helmet_appearances`.

#### Body armor

- [ ] **gray dragon scale mail** (`GRAY_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **gold dragon scale mail** (`GOLD_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **silver dragon scale mail** (`SILVER_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **red dragon scale mail** (`RED_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **white dragon scale mail** (`WHITE_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **orange dragon scale mail** (`ORANGE_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **black dragon scale mail** (`BLACK_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **blue dragon scale mail** (`BLUE_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **green dragon scale mail** (`GREEN_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **yellow dragon scale mail** (`YELLOW_DRAGON_SCALE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md). [Revised small-scale reference design](Docs/DragonMailReferenceRevision.md).
- [ ] **gray dragon scales** (`GRAY_DRAGON_SCALES`).
- [ ] **gold dragon scales** (`GOLD_DRAGON_SCALES`).
- [ ] **silver dragon scales** (`SILVER_DRAGON_SCALES`).
- [ ] **red dragon scales** (`RED_DRAGON_SCALES`).
- [ ] **white dragon scales** (`WHITE_DRAGON_SCALES`).
- [ ] **orange dragon scales** (`ORANGE_DRAGON_SCALES`).
- [ ] **black dragon scales** (`BLACK_DRAGON_SCALES`).
- [ ] **blue dragon scales** (`BLUE_DRAGON_SCALES`).
- [ ] **green dragon scales** (`GREEN_DRAGON_SCALES`).
- [ ] **yellow dragon scales** (`YELLOW_DRAGON_SCALES`).
- [ ] **plate mail** (`PLATE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md).
- [ ] **crystal plate mail** (`CRYSTAL_PLATE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md).
- [ ] **bronze plate mail** (`BRONZE_PLATE_MAIL`) — design/import draft; [artifacts and remaining live checks](Docs/ArmorBatch2.md).
- [ ] **splint mail** (`SPLINT_MAIL`).
- [ ] **banded mail** (`BANDED_MAIL`) — design/import draft; [models and evidence](Docs/ArmorStudy.md). Remaining: native displayed-appearance, pile/memory/hallucination/save/fallback and no-turn live checks.
- [ ] **dwarvish mithril-coat** (`DWARVISH_MITHRIL_COAT`) — design/import draft; [models and evidence](Docs/ArmorStudy.md). Remaining: native displayed-appearance, pile/memory/hallucination/save/fallback and no-turn live checks.
- [ ] **elven mithril-coat** (`ELVEN_MITHRIL_COAT`) — design/import draft; [models and evidence](Docs/ArmorStudy.md). Remaining: native displayed-appearance, pile/memory/hallucination/save/fallback and no-turn live checks.
- [ ] **chain mail** (`CHAIN_MAIL`) — design/import draft; [models and evidence](Docs/ArmorStudy.md). Remaining: native displayed-appearance, pile/memory/hallucination/save/fallback and no-turn live checks.
- [ ] **orcish chain mail** (`ORCISH_CHAIN_MAIL`) — default appearance: crude chain mail.
- [ ] **scale mail** (`SCALE_MAIL`).
- [ ] **studded leather armor** (`STUDDED_LEATHER_ARMOR`) — design/import draft; [models and evidence](Docs/ArmorStudy.md). Remaining: native displayed-appearance, pile/memory/hallucination/save/fallback and no-turn live checks.
- [ ] **ring mail** (`RING_MAIL`).
- [ ] **orcish ring mail** (`ORCISH_RING_MAIL`) — default appearance: crude ring mail.
- [ ] **leather armor** (`LEATHER_ARMOR`) — design/import draft; [models and evidence](Docs/ArmorStudy.md). Remaining: native displayed-appearance, pile/memory/hallucination/save/fallback and no-turn live checks.
- [ ] **leather jacket** (`LEATHER_JACKET`).

#### Shirts

- [ ] **Hawaiian shirt** (`HAWAIIAN_SHIRT`).
- [ ] **T-shirt** (`T_SHIRT`).

#### Cloaks

- [ ] **mummy wrapping** (`MUMMY_WRAPPING`).
- [ ] **elven cloak** (`ELVEN_CLOAK`) — default appearance: faded pall.
- [ ] **orcish cloak** (`ORCISH_CLOAK`) — default appearance: coarse mantelet.
- [ ] **dwarvish cloak** (`DWARVISH_CLOAK`) — design/import draft; [models and evidence](Docs/ArmorStudy.md). Remaining: native displayed-appearance, pile/memory/hallucination/save/fallback and no-turn live checks.
- [ ] **oilskin cloak** (`OILSKIN_CLOAK`) — default appearance: slippery cloak.
- [ ] **robe** (`ROBE`).
- [ ] **alchemy smock** (`ALCHEMY_SMOCK`) — default appearance: apron.
- [ ] **leather cloak** (`LEATHER_CLOAK`).
- [ ] **cloak of protection** (`CLOAK_OF_PROTECTION`) — default appearance: tattered cape; shuffled pool `cloak_of_protection_appearances`.
- [ ] **cloak of invisibility** (`CLOAK_OF_INVISIBILITY`) — default appearance: opera cloak; shuffled pool `cloak_of_protection_appearances`.
- [ ] **cloak of magic resistance** (`CLOAK_OF_MAGIC_RESISTANCE`) — default appearance: ornamental cope; shuffled pool `cloak_of_protection_appearances`.
- [ ] **cloak of displacement** (`CLOAK_OF_DISPLACEMENT`) — default appearance: piece of cloth; shuffled pool `cloak_of_protection_appearances`.

#### Shields

- [ ] **small shield** (`SMALL_SHIELD`) — default appearance: wooden shield.
- [ ] **shield of drain resistance** (`SHIELD_OF_DRAIN_RESISTANCE`) — default appearance: wooden shield.
- [ ] **shield of shock resistance** (`SHIELD_OF_SHOCK_RESISTANCE`) — default appearance: wooden shield.
- [ ] **elven shield** (`ELVEN_SHIELD`) — default appearance: blue and green shield.
- [ ] **Uruk-hai shield** (`URUK_HAI_SHIELD`) — default appearance: white-handed shield.
- [ ] **orcish shield** (`ORCISH_SHIELD`) — default appearance: red-eyed shield.
- [ ] **large shield** (`LARGE_SHIELD`).
- [ ] **dwarvish roundshield** (`DWARVISH_ROUNDSHIELD`) — default appearance: large round shield.
- [ ] **shield of reflection** (`SHIELD_OF_REFLECTION`) — default appearance: polished silver shield.

#### Gloves and gauntlets

- [ ] **leather gloves** (`LEATHER_GLOVES`) — default appearance: old gloves; shuffled pool `leather_gloves_appearances`.
- [ ] **gauntlets of fumbling** (`GAUNTLETS_OF_FUMBLING`) — default appearance: padded gloves; shuffled pool `leather_gloves_appearances`.
- [ ] **gauntlets of power** (`GAUNTLETS_OF_POWER`) — default appearance: riding gloves; shuffled pool `leather_gloves_appearances`.
- [ ] **gauntlets of dexterity** (`GAUNTLETS_OF_DEXTERITY`) — default appearance: fencing gloves; shuffled pool `leather_gloves_appearances`.

#### Footwear

- [ ] **low boots** (`LOW_BOOTS`) — default appearance: walking shoes.
- [ ] **iron shoes** (`IRON_SHOES`) — default appearance: hard shoes.
- [ ] **high boots** (`HIGH_BOOTS`) — default appearance: jackboots.
- [ ] **speed boots** (`SPEED_BOOTS`) — default appearance: combat boots; shuffled pool `speed_boots_appearances`.
- [ ] **water walking boots** (`WATER_WALKING_BOOTS`) — default appearance: jungle boots; shuffled pool `speed_boots_appearances`.
- [ ] **jumping boots** (`JUMPING_BOOTS`) — default appearance: hiking boots; shuffled pool `speed_boots_appearances`.
- [ ] **elven boots** (`ELVEN_BOOTS`) — default appearance: mud boots; shuffled pool `speed_boots_appearances`.
- [ ] **kicking boots** (`KICKING_BOOTS`) — default appearance: buckled boots; shuffled pool `speed_boots_appearances`.
- [ ] **fumble boots** (`FUMBLE_BOOTS`) — default appearance: riding boots; shuffled pool `speed_boots_appearances`.
- [ ] **levitation boots** (`LEVITATION_BOOTS`) — default appearance: snow boots; shuffled pool `speed_boots_appearances`.


### Rings

#### Bands and settings

- [ ] **adornment** (`RIN_ADORNMENT`) — default appearance: wooden; shuffled pool `ring_appearances`.
- [ ] **gain strength** (`RIN_GAIN_STRENGTH`) — default appearance: granite; shuffled pool `ring_appearances`.
- [ ] **gain constitution** (`RIN_GAIN_CONSTITUTION`) — default appearance: opal; shuffled pool `ring_appearances`.
- [ ] **increase accuracy** (`RIN_INCREASE_ACCURACY`) — default appearance: clay; shuffled pool `ring_appearances`.
- [ ] **increase damage** (`RIN_INCREASE_DAMAGE`) — default appearance: coral; shuffled pool `ring_appearances`.
- [ ] **protection** (`RIN_PROTECTION`) — default appearance: black onyx; shuffled pool `ring_appearances`.
- [ ] **regeneration** (`RIN_REGENERATION`) — default appearance: moonstone; shuffled pool `ring_appearances`.
- [ ] **searching** (`RIN_SEARCHING`) — default appearance: tiger eye; shuffled pool `ring_appearances`.
- [ ] **stealth** (`RIN_STEALTH`) — default appearance: jade; shuffled pool `ring_appearances`.
- [ ] **sustain ability** (`RIN_SUSTAIN_ABILITY`) — default appearance: bronze; shuffled pool `ring_appearances`.
- [ ] **levitation** (`RIN_LEVITATION`) — default appearance: agate; shuffled pool `ring_appearances`.
- [ ] **hunger** (`RIN_HUNGER`) — default appearance: topaz; shuffled pool `ring_appearances`.
- [ ] **aggravate monster** (`RIN_AGGRAVATE_MONSTER`) — default appearance: sapphire; shuffled pool `ring_appearances`.
- [ ] **conflict** (`RIN_CONFLICT`) — default appearance: ruby; shuffled pool `ring_appearances`.
- [ ] **warning** (`RIN_WARNING`) — default appearance: diamond; shuffled pool `ring_appearances`.
- [ ] **poison resistance** (`RIN_POISON_RESISTANCE`) — default appearance: pearl; shuffled pool `ring_appearances`.
- [ ] **fire resistance** (`RIN_FIRE_RESISTANCE`) — default appearance: iron; shuffled pool `ring_appearances`.
- [ ] **cold resistance** (`RIN_COLD_RESISTANCE`) — default appearance: brass; shuffled pool `ring_appearances`.
- [ ] **shock resistance** (`RIN_SHOCK_RESISTANCE`) — default appearance: copper; shuffled pool `ring_appearances`.
- [ ] **free action** (`RIN_FREE_ACTION`) — default appearance: twisted; shuffled pool `ring_appearances`.
- [ ] **slow digestion** (`RIN_SLOW_DIGESTION`) — default appearance: steel; shuffled pool `ring_appearances`.
- [ ] **teleportation** (`RIN_TELEPORTATION`) — default appearance: silver; shuffled pool `ring_appearances`.
- [ ] **teleport control** (`RIN_TELEPORT_CONTROL`) — default appearance: gold; shuffled pool `ring_appearances`.
- [ ] **polymorph** (`RIN_POLYMORPH`) — default appearance: ivory; shuffled pool `ring_appearances`.
- [ ] **polymorph control** (`RIN_POLYMORPH_CONTROL`) — default appearance: emerald; shuffled pool `ring_appearances`.
- [ ] **invisibility** (`RIN_INVISIBILITY`) — default appearance: wire; shuffled pool `ring_appearances`.
- [ ] **see invisible** (`RIN_SEE_INVISIBLE`) — default appearance: engagement; shuffled pool `ring_appearances`.
- [ ] **protection from shape changers** (`RIN_PROTECTION_FROM_SHAPE_CHAN`) — default appearance: shiny; shuffled pool `ring_appearances`.


### Amulets

#### Pendants

- [ ] **amulet of ESP** (`AMULET_OF_ESP`) — default appearance: circular; shuffled pool `amulet_appearances`.
- [ ] **amulet of life saving** (`AMULET_OF_LIFE_SAVING`) — default appearance: spherical; shuffled pool `amulet_appearances`.
- [ ] **amulet of strangulation** (`AMULET_OF_STRANGULATION`) — default appearance: oval; shuffled pool `amulet_appearances`.
- [ ] **amulet of restful sleep** (`AMULET_OF_RESTFUL_SLEEP`) — default appearance: triangular; shuffled pool `amulet_appearances`.
- [ ] **amulet versus poison** (`AMULET_VERSUS_POISON`) — default appearance: pyramidal; shuffled pool `amulet_appearances`.
- [ ] **amulet of change** (`AMULET_OF_CHANGE`) — default appearance: square; shuffled pool `amulet_appearances`.
- [ ] **amulet of unchanging** (`AMULET_OF_UNCHANGING`) — default appearance: concave; shuffled pool `amulet_appearances`.
- [ ] **amulet of reflection** (`AMULET_OF_REFLECTION`) — default appearance: hexagonal; shuffled pool `amulet_appearances`.
- [ ] **amulet of magical breathing** (`AMULET_OF_MAGICAL_BREATHING`) — default appearance: octagonal; shuffled pool `amulet_appearances`.
- [ ] **amulet of guarding** (`AMULET_OF_GUARDING`) — default appearance: perforated; shuffled pool `amulet_appearances`.
- [ ] **amulet of flying** (`AMULET_OF_FLYING`) — default appearance: cubical; shuffled pool `amulet_appearances`.
- [ ] **cheap plastic imitation of the Amulet of Yendor** (`FAKE_AMULET_OF_YENDOR`) — default appearance: Amulet of Yendor.
- [ ] **Amulet of Yendor** (`AMULET_OF_YENDOR`).


### Tools

#### Containers

- [x] **large box** (`LARGE_BOX`); verified fixed presentation; [evidence](Docs/ObjectBatch1.md).
- [x] **chest** (`CHEST`); verified fixed presentation; [evidence](Docs/ObjectBatch1.md).
- [ ] **ice box** (`ICE_BOX`).
- [ ] **sack** (`SACK`) — default appearance: bag.
- [ ] **oilskin sack** (`OILSKIN_SACK`) — default appearance: bag.
- [ ] **bag of holding** (`BAG_OF_HOLDING`) — default appearance: bag.
- [ ] **bag of tricks** (`BAG_OF_TRICKS`) — default appearance: bag.

#### Hand tools and equipment

- [ ] **skeleton key** (`SKELETON_KEY`) — default appearance: key.
- [ ] **lock pick** (`LOCK_PICK`).
- [ ] **credit card** (`CREDIT_CARD`).
- [ ] **mirror** (`MIRROR`) — default appearance: looking glass.
- [ ] **saddle** (`SADDLE`).
- [ ] **leash** (`LEASH`).
- [ ] **stethoscope** (`STETHOSCOPE`).
- [ ] **tinning kit** (`TINNING_KIT`).
- [ ] **tin whistle** (`TIN_WHISTLE`) — default appearance: whistle.
- [ ] **magic whistle** (`MAGIC_WHISTLE`) — default appearance: whistle.

#### Lights

- [ ] **tallow candle** (`TALLOW_CANDLE`) — default appearance: candle.
- [ ] **wax candle** (`WAX_CANDLE`) — default appearance: candle.
- [ ] **brass lantern** (`BRASS_LANTERN`).
- [ ] **oil lamp** (`OIL_LAMP`) — default appearance: lamp.
- [ ] **magic lamp** (`MAGIC_LAMP`) — default appearance: lamp.

#### Special tools and devices

- [ ] **expensive camera** (`EXPENSIVE_CAMERA`).
- [ ] **crystal ball** (`CRYSTAL_BALL`) — default appearance: glass orb.
- [ ] **tin opener** (`TIN_OPENER`).
- [ ] **can of grease** (`CAN_OF_GREASE`).
- [ ] **figurine** (`FIGURINE`).
- [ ] **magic marker** (`MAGIC_MARKER`).
- [ ] **land mine** (`LAND_MINE`).
- [ ] **beartrap** (`BEARTRAP`).
- [ ] **Candelabrum of Invocation** (`CANDELABRUM_OF_INVOCATION`) — default appearance: candelabrum.
- [ ] **Bell of Opening** (`BELL_OF_OPENING`) — default appearance: silver bell.

#### Eyewear

- [ ] **lenses** (`LENSES`).
- [ ] **blindfold** (`BLINDFOLD`).
- [ ] **towel** (`TOWEL`).

#### Instruments and sound tools

- [ ] **wooden flute** (`WOODEN_FLUTE`) — default appearance: flute.
- [ ] **magic flute** (`MAGIC_FLUTE`) — default appearance: flute.
- [ ] **tooled horn** (`TOOLED_HORN`) — default appearance: horn.
- [ ] **frost horn** (`FROST_HORN`) — default appearance: horn.
- [ ] **fire horn** (`FIRE_HORN`) — default appearance: horn.
- [ ] **horn of plenty** (`HORN_OF_PLENTY`) — default appearance: horn.
- [ ] **wooden harp** (`WOODEN_HARP`) — default appearance: harp.
- [ ] **magic harp** (`MAGIC_HARP`) — default appearance: harp.
- [ ] **bell** (`BELL`).
- [ ] **bugle** (`BUGLE`).
- [ ] **leather drum** (`LEATHER_DRUM`) — default appearance: drum.
- [ ] **drum of earthquake** (`DRUM_OF_EARTHQUAKE`) — default appearance: drum.

#### Axes and picks

- [ ] **pick-axe** (`PICK_AXE`).

#### Flexible weapons

- [ ] **grappling hook** (`GRAPPLING_HOOK`).

#### Clubs, hammers and staves

- [ ] **unicorn horn** (`UNICORN_HORN`).


### Food

#### Food and organic objects

- [ ] **tripe ration** (`TRIPE_RATION`).
- [x] **corpse** (`CORPSE`); verified fixed presentation; [evidence](Docs/SpecialBatch1.md).
- [ ] **egg** (`EGG`).
- [ ] **meatball** (`MEATBALL`).
- [ ] **meat stick** (`MEAT_STICK`).
- [ ] **enormous meatball** (`ENORMOUS_MEATBALL`).
- [ ] **meat ring** (`MEAT_RING`).
- [ ] **glob of gray ooze** (`GLOB_OF_GRAY_OOZE`).
- [ ] **glob of brown pudding** (`GLOB_OF_BROWN_PUDDING`).
- [ ] **glob of green slime** (`GLOB_OF_GREEN_SLIME`).
- [ ] **glob of black pudding** (`GLOB_OF_BLACK_PUDDING`).
- [ ] **kelp frond** (`KELP_FROND`).
- [ ] **eucalyptus leaf** (`EUCALYPTUS_LEAF`).
- [ ] **apple** (`APPLE`).
- [ ] **orange** (`ORANGE`).
- [ ] **pear** (`PEAR`).
- [ ] **melon** (`MELON`).
- [ ] **banana** (`BANANA`).
- [ ] **carrot** (`CARROT`).
- [ ] **sprig of wolfsbane** (`SPRIG_OF_WOLFSBANE`).
- [ ] **clove of garlic** (`CLOVE_OF_GARLIC`).
- [ ] **slime mold** (`SLIME_MOLD`).
- [ ] **lump of royal jelly** (`LUMP_OF_ROYAL_JELLY`).
- [ ] **cream pie** (`CREAM_PIE`).
- [ ] **candy bar** (`CANDY_BAR`).
- [ ] **fortune cookie** (`FORTUNE_COOKIE`).
- [ ] **pancake** (`PANCAKE`).
- [ ] **lembas wafer** (`LEMBAS_WAFER`).
- [ ] **cram ration** (`CRAM_RATION`).
- [ ] **food ration** (`FOOD_RATION`).
- [ ] **K-ration** (`K_RATION`).
- [ ] **C-ration** (`C_RATION`).
- [ ] **tin** (`TIN`).


### Potions

#### Bottles and visible contents

- [ ] **gain ability** (`POT_GAIN_ABILITY`) — default appearance: ruby; shuffled pool `potion_appearances`.
- [ ] **restore ability** (`POT_RESTORE_ABILITY`) — default appearance: pink; shuffled pool `potion_appearances`.
- [ ] **confusion** (`POT_CONFUSION`) — default appearance: orange; shuffled pool `potion_appearances`.
- [ ] **blindness** (`POT_BLINDNESS`) — default appearance: yellow; shuffled pool `potion_appearances`.
- [ ] **paralysis** (`POT_PARALYSIS`) — default appearance: emerald; shuffled pool `potion_appearances`.
- [ ] **speed** (`POT_SPEED`) — default appearance: dark green; shuffled pool `potion_appearances`.
- [ ] **levitation** (`POT_LEVITATION`) — default appearance: cyan; shuffled pool `potion_appearances`.
- [ ] **hallucination** (`POT_HALLUCINATION`) — default appearance: sky blue; shuffled pool `potion_appearances`.
- [ ] **invisibility** (`POT_INVISIBILITY`) — default appearance: brilliant blue; shuffled pool `potion_appearances`.
- [ ] **see invisible** (`POT_SEE_INVISIBLE`) — default appearance: magenta; shuffled pool `potion_appearances`.
- [ ] **healing** (`POT_HEALING`) — default appearance: purple-red; shuffled pool `potion_appearances`.
- [ ] **extra healing** (`POT_EXTRA_HEALING`) — default appearance: puce; shuffled pool `potion_appearances`.
- [ ] **gain level** (`POT_GAIN_LEVEL`) — default appearance: milky; shuffled pool `potion_appearances`.
- [ ] **enlightenment** (`POT_ENLIGHTENMENT`) — default appearance: swirly; shuffled pool `potion_appearances`.
- [ ] **monster detection** (`POT_MONSTER_DETECTION`) — default appearance: bubbly; shuffled pool `potion_appearances`.
- [ ] **object detection** (`POT_OBJECT_DETECTION`) — default appearance: smoky; shuffled pool `potion_appearances`.
- [ ] **gain energy** (`POT_GAIN_ENERGY`) — default appearance: cloudy; shuffled pool `potion_appearances`.
- [ ] **sleeping** (`POT_SLEEPING`) — default appearance: effervescent; shuffled pool `potion_appearances`.
- [ ] **full healing** (`POT_FULL_HEALING`) — default appearance: black; shuffled pool `potion_appearances`.
- [ ] **polymorph** (`POT_POLYMORPH`) — default appearance: golden; shuffled pool `potion_appearances`.
- [ ] **booze** (`POT_BOOZE`) — default appearance: brown; shuffled pool `potion_appearances`.
- [ ] **sickness** (`POT_SICKNESS`) — default appearance: fizzy; shuffled pool `potion_appearances`.
- [ ] **fruit juice** (`POT_FRUIT_JUICE`) — default appearance: dark; shuffled pool `potion_appearances`.
- [ ] **acid** (`POT_ACID`) — default appearance: white; shuffled pool `potion_appearances`.
- [ ] **oil** (`POT_OIL`) — default appearance: murky; shuffled pool `potion_appearances`.
- [ ] **water** (`POT_WATER`) — default appearance: clear.


### Scrolls

#### Rolled sheets and labels

- [ ] **enchant armor** (`SCR_ENCHANT_ARMOR`) — default appearance: ZELGO MER; shuffled pool `scroll_appearances`.
- [ ] **destroy armor** (`SCR_DESTROY_ARMOR`) — default appearance: JUYED AWK YACC; shuffled pool `scroll_appearances`.
- [ ] **confuse monster** (`SCR_CONFUSE_MONSTER`) — default appearance: NR 9; shuffled pool `scroll_appearances`.
- [ ] **scare monster** (`SCR_SCARE_MONSTER`) — default appearance: XIXAXA XOXAXA XUXAXA; shuffled pool `scroll_appearances`.
- [ ] **remove curse** (`SCR_REMOVE_CURSE`) — default appearance: PRATYAVAYAH; shuffled pool `scroll_appearances`.
- [ ] **enchant weapon** (`SCR_ENCHANT_WEAPON`) — default appearance: DAIYEN FOOELS; shuffled pool `scroll_appearances`.
- [ ] **create monster** (`SCR_CREATE_MONSTER`) — default appearance: LEP GEX VEN ZEA; shuffled pool `scroll_appearances`.
- [ ] **taming** (`SCR_TAMING`) — default appearance: PRIRUTSENIE; shuffled pool `scroll_appearances`.
- [ ] **genocide** (`SCR_GENOCIDE`) — default appearance: ELBIB YLOH; shuffled pool `scroll_appearances`.
- [ ] **light** (`SCR_LIGHT`) — default appearance: VERR YED HORRE; shuffled pool `scroll_appearances`.
- [ ] **teleportation** (`SCR_TELEPORTATION`) — default appearance: VENZAR BORGAVVE; shuffled pool `scroll_appearances`.
- [ ] **gold detection** (`SCR_GOLD_DETECTION`) — default appearance: THARR; shuffled pool `scroll_appearances`.
- [ ] **food detection** (`SCR_FOOD_DETECTION`) — default appearance: YUM YUM; shuffled pool `scroll_appearances`.
- [ ] **identify** (`SCR_IDENTIFY`) — default appearance: KERNOD WEL; shuffled pool `scroll_appearances`.
- [ ] **magic mapping** (`SCR_MAGIC_MAPPING`) — default appearance: ELAM EBOW; shuffled pool `scroll_appearances`.
- [ ] **amnesia** (`SCR_AMNESIA`) — default appearance: DUAM XNAHT; shuffled pool `scroll_appearances`.
- [ ] **fire** (`SCR_FIRE`) — default appearance: ANDOVA BEGARIN; shuffled pool `scroll_appearances`.
- [ ] **earth** (`SCR_EARTH`) — default appearance: KIRJE; shuffled pool `scroll_appearances`.
- [ ] **punishment** (`SCR_PUNISHMENT`) — default appearance: VE FORBRYDERNE; shuffled pool `scroll_appearances`.
- [ ] **charging** (`SCR_CHARGING`) — default appearance: HACKEM MUCHE; shuffled pool `scroll_appearances`.
- [ ] **stinking cloud** (`SCR_STINKING_CLOUD`) — default appearance: VELOX NEB; shuffled pool `scroll_appearances`.
- [ ] **mail** (`SCR_MAIL`) — default appearance: stamped; **conditional ifdef MAIL_STRUCTURES**.
- [ ] **blank paper** (`SCR_BLANK_PAPER`) — default appearance: unlabeled.


### Spellbooks

#### Bindings and covers

- [ ] **dig** (`SPE_DIG`) — default appearance: parchment; shuffled pool `spbook_appearances`.
- [ ] **magic missile** (`SPE_MAGIC_MISSILE`) — default appearance: vellum; shuffled pool `spbook_appearances`.
- [ ] **fireball** (`SPE_FIREBALL`) — default appearance: ragged; shuffled pool `spbook_appearances`.
- [ ] **cone of cold** (`SPE_CONE_OF_COLD`) — default appearance: dog eared; shuffled pool `spbook_appearances`.
- [ ] **sleep** (`SPE_SLEEP`) — default appearance: mottled; shuffled pool `spbook_appearances`.
- [ ] **finger of death** (`SPE_FINGER_OF_DEATH`) — default appearance: stained; shuffled pool `spbook_appearances`.
- [ ] **light** (`SPE_LIGHT`) — default appearance: cloth; shuffled pool `spbook_appearances`.
- [ ] **detect monsters** (`SPE_DETECT_MONSTERS`) — default appearance: leathery; shuffled pool `spbook_appearances`.
- [ ] **healing** (`SPE_HEALING`) — default appearance: white; shuffled pool `spbook_appearances`.
- [ ] **knock** (`SPE_KNOCK`) — default appearance: pink; shuffled pool `spbook_appearances`.
- [ ] **force bolt** (`SPE_FORCE_BOLT`) — default appearance: red; shuffled pool `spbook_appearances`.
- [ ] **confuse monster** (`SPE_CONFUSE_MONSTER`) — default appearance: orange; shuffled pool `spbook_appearances`.
- [ ] **cure blindness** (`SPE_CURE_BLINDNESS`) — default appearance: yellow; shuffled pool `spbook_appearances`.
- [ ] **drain life** (`SPE_DRAIN_LIFE`) — default appearance: velvet; shuffled pool `spbook_appearances`.
- [ ] **slow monster** (`SPE_SLOW_MONSTER`) — default appearance: light green; shuffled pool `spbook_appearances`.
- [ ] **wizard lock** (`SPE_WIZARD_LOCK`) — default appearance: dark green; shuffled pool `spbook_appearances`.
- [ ] **create monster** (`SPE_CREATE_MONSTER`) — default appearance: turquoise; shuffled pool `spbook_appearances`.
- [ ] **detect food** (`SPE_DETECT_FOOD`) — default appearance: cyan; shuffled pool `spbook_appearances`.
- [ ] **cause fear** (`SPE_CAUSE_FEAR`) — default appearance: light blue; shuffled pool `spbook_appearances`.
- [ ] **clairvoyance** (`SPE_CLAIRVOYANCE`) — default appearance: dark blue; shuffled pool `spbook_appearances`.
- [ ] **cure sickness** (`SPE_CURE_SICKNESS`) — default appearance: indigo; shuffled pool `spbook_appearances`.
- [ ] **charm monster** (`SPE_CHARM_MONSTER`) — default appearance: magenta; shuffled pool `spbook_appearances`.
- [ ] **haste self** (`SPE_HASTE_SELF`) — default appearance: purple; shuffled pool `spbook_appearances`.
- [ ] **detect unseen** (`SPE_DETECT_UNSEEN`) — default appearance: violet; shuffled pool `spbook_appearances`.
- [ ] **levitation** (`SPE_LEVITATION`) — default appearance: tan; shuffled pool `spbook_appearances`.
- [ ] **extra healing** (`SPE_EXTRA_HEALING`) — default appearance: plaid; shuffled pool `spbook_appearances`.
- [ ] **restore ability** (`SPE_RESTORE_ABILITY`) — default appearance: light brown; shuffled pool `spbook_appearances`.
- [ ] **invisibility** (`SPE_INVISIBILITY`) — default appearance: dark brown; shuffled pool `spbook_appearances`.
- [ ] **detect treasure** (`SPE_DETECT_TREASURE`) — default appearance: gray; shuffled pool `spbook_appearances`.
- [ ] **remove curse** (`SPE_REMOVE_CURSE`) — default appearance: wrinkled; shuffled pool `spbook_appearances`.
- [ ] **magic mapping** (`SPE_MAGIC_MAPPING`) — default appearance: dusty; shuffled pool `spbook_appearances`.
- [ ] **identify** (`SPE_IDENTIFY`) — default appearance: bronze; shuffled pool `spbook_appearances`.
- [ ] **turn undead** (`SPE_TURN_UNDEAD`) — default appearance: copper; shuffled pool `spbook_appearances`.
- [ ] **polymorph** (`SPE_POLYMORPH`) — default appearance: silver; shuffled pool `spbook_appearances`.
- [ ] **teleport away** (`SPE_TELEPORT_AWAY`) — default appearance: gold; shuffled pool `spbook_appearances`.
- [ ] **create familiar** (`SPE_CREATE_FAMILIAR`) — default appearance: glittering; shuffled pool `spbook_appearances`.
- [ ] **cancellation** (`SPE_CANCELLATION`) — default appearance: shining; shuffled pool `spbook_appearances`.
- [ ] **protection** (`SPE_PROTECTION`) — default appearance: dull; shuffled pool `spbook_appearances`.
- [ ] **jumping** (`SPE_JUMPING`) — default appearance: thin; shuffled pool `spbook_appearances`.
- [ ] **stone to flesh** (`SPE_STONE_TO_FLESH`) — default appearance: thick; shuffled pool `spbook_appearances`.
- [ ] **chain lightning** (`SPE_CHAIN_LIGHTNING`) — default appearance: checkered; shuffled pool `spbook_appearances`.
- [ ] **blank paper** (`SPE_BLANK_PAPER`) — default appearance: plain.
- [ ] **novel** (`SPE_NOVEL`) — default appearance: paperback.
- [ ] **Book of the Dead** (`SPE_BOOK_OF_THE_DEAD`) — default appearance: papyrus.


### Wands

#### Rods and handles

- [ ] **light** (`WAN_LIGHT`) — default appearance: glass; shuffled pool `wand_appearances`.
- [ ] **secret door detection** (`WAN_SECRET_DOOR_DETECTION`) — default appearance: balsa; shuffled pool `wand_appearances`.
- [ ] **enlightenment** (`WAN_ENLIGHTENMENT`) — default appearance: crystal; shuffled pool `wand_appearances`.
- [ ] **create monster** (`WAN_CREATE_MONSTER`) — default appearance: maple; shuffled pool `wand_appearances`.
- [ ] **wishing** (`WAN_WISHING`) — default appearance: pine; shuffled pool `wand_appearances`.
- [ ] **stasis** (`WAN_STASIS`) — default appearance: redwood; shuffled pool `wand_appearances`.
- [ ] **nothing** (`WAN_NOTHING`) — default appearance: oak; shuffled pool `wand_appearances`.
- [ ] **striking** (`WAN_STRIKING`) — default appearance: ebony; shuffled pool `wand_appearances`.
- [ ] **make invisible** (`WAN_MAKE_INVISIBLE`) — default appearance: marble; shuffled pool `wand_appearances`.
- [ ] **slow monster** (`WAN_SLOW_MONSTER`) — default appearance: tin; shuffled pool `wand_appearances`.
- [ ] **speed monster** (`WAN_SPEED_MONSTER`) — default appearance: brass; shuffled pool `wand_appearances`.
- [ ] **undead turning** (`WAN_UNDEAD_TURNING`) — default appearance: copper; shuffled pool `wand_appearances`.
- [ ] **polymorph** (`WAN_POLYMORPH`) — default appearance: silver; shuffled pool `wand_appearances`.
- [ ] **cancellation** (`WAN_CANCELLATION`) — default appearance: platinum; shuffled pool `wand_appearances`.
- [ ] **teleportation** (`WAN_TELEPORTATION`) — default appearance: iridium; shuffled pool `wand_appearances`.
- [ ] **opening** (`WAN_OPENING`) — default appearance: zinc; shuffled pool `wand_appearances`.
- [ ] **locking** (`WAN_LOCKING`) — default appearance: aluminum; shuffled pool `wand_appearances`.
- [ ] **probing** (`WAN_PROBING`) — default appearance: uranium; shuffled pool `wand_appearances`.
- [ ] **digging** (`WAN_DIGGING`) — default appearance: iron; shuffled pool `wand_appearances`.
- [ ] **magic missile** (`WAN_MAGIC_MISSILE`) — default appearance: steel; shuffled pool `wand_appearances`.
- [ ] **fire** (`WAN_FIRE`) — default appearance: hexagonal; shuffled pool `wand_appearances`.
- [ ] **cold** (`WAN_COLD`) — default appearance: short; shuffled pool `wand_appearances`.
- [ ] **sleep** (`WAN_SLEEP`) — default appearance: runed; shuffled pool `wand_appearances`.
- [ ] **death** (`WAN_DEATH`) — default appearance: long; shuffled pool `wand_appearances`.
- [ ] **lightning** (`WAN_LIGHTNING`) — default appearance: curved; shuffled pool `wand_appearances`.


### Coins

#### Coins

- [x] **gold piece** (`GOLD_PIECE`); verified fixed presentation; [evidence](Docs/ObjectBatch1.md).


### Gems and stones

#### Faceted gems and rough stones

- [ ] **dilithium crystal** (`DILITHIUM_CRYSTAL`) — default appearance: white.
- [ ] **diamond** (`DIAMOND`) — default appearance: white.
- [ ] **ruby** (`RUBY`) — default appearance: red.
- [ ] **jacinth** (`JACINTH`) — default appearance: orange.
- [ ] **sapphire** (`SAPPHIRE`) — default appearance: blue.
- [ ] **black opal** (`BLACK_OPAL`) — default appearance: black.
- [ ] **emerald** (`EMERALD`) — default appearance: green.
- [ ] **turquoise** (`TURQUOISE`) — default appearance: green.
- [ ] **citrine** (`CITRINE`) — default appearance: yellow.
- [ ] **aquamarine** (`AQUAMARINE`) — default appearance: green.
- [ ] **amber** (`AMBER`) — default appearance: yellowish brown.
- [ ] **topaz** (`TOPAZ`) — default appearance: yellowish brown.
- [ ] **jet** (`JET`) — default appearance: black.
- [ ] **opal** (`OPAL`) — default appearance: white.
- [ ] **chrysoberyl** (`CHRYSOBERYL`) — default appearance: yellow.
- [ ] **garnet** (`GARNET`) — default appearance: red.
- [ ] **amethyst** (`AMETHYST`) — default appearance: violet.
- [ ] **jasper** (`JASPER`) — default appearance: red.
- [ ] **fluorite** (`FLUORITE`) — default appearance: violet.
- [ ] **obsidian** (`OBSIDIAN`) — default appearance: black.
- [ ] **agate** (`AGATE`) — default appearance: orange.
- [ ] **jade** (`JADE`) — default appearance: green.
- [ ] **worthless piece of white glass** (`WORTHLESS_WHITE_GLASS`) — default appearance: white.
- [ ] **worthless piece of blue glass** (`WORTHLESS_BLUE_GLASS`) — default appearance: blue.
- [ ] **worthless piece of red glass** (`WORTHLESS_RED_GLASS`) — default appearance: red.
- [ ] **worthless piece of yellowish brown glass** (`WORTHLESS_YELLOWBROWN_GLASS`) — default appearance: yellowish brown.
- [ ] **worthless piece of orange glass** (`WORTHLESS_ORANGE_GLASS`) — default appearance: orange.
- [ ] **worthless piece of yellow glass** (`WORTHLESS_YELLOW_GLASS`) — default appearance: yellow.
- [ ] **worthless piece of black glass** (`WORTHLESS_BLACK_GLASS`) — default appearance: black.
- [ ] **worthless piece of green glass** (`WORTHLESS_GREEN_GLASS`) — default appearance: green.
- [ ] **worthless piece of violet glass** (`WORTHLESS_VIOLET_GLASS`) — default appearance: violet.
- [ ] **luckstone** (`LUCKSTONE`) — default appearance: gray.
- [ ] **loadstone** (`LOADSTONE`) — default appearance: gray.
- [ ] **touchstone** (`TOUCHSTONE`) — default appearance: gray.
- [ ] **flint** (`FLINT`) — default appearance: gray.
- [ ] **rock** (`ROCK`).


### Large rocks and statues

#### Large stone forms

- [ ] **boulder** (`BOULDER`).
- [ ] **statue** (`STATUE`).


### Punishment gear

#### Balls

- [ ] **heavy iron ball** (`HEAVY_IRON_BALL`).

#### Chains

- [ ] **iron chain** (`IRON_CHAIN`).


### Venom

#### Splashes

- [ ] **splash of blinding venom** (`BLINDING_VENOM`) — default appearance: splash of venom; shuffled pool `venom_appearances`.
- [ ] **splash of acid venom** (`ACID_VENOM`) — default appearance: splash of venom; shuffled pool `venom_appearances`.

## Extra appearance-only slots

These are physical appearance work, not 23 additional object-effect identities. Their source default-slot IDs are not live effect identifiers.

- [ ] **FOOBIE BLETCH** (`APPEARANCE_SC01`) — Scrolls; source slot `SC01`.
- [ ] **TEMOV** (`APPEARANCE_SC02`) — Scrolls; source slot `SC02`.
- [ ] **GARVEN DEH** (`APPEARANCE_SC03`) — Scrolls; source slot `SC03`.
- [ ] **READ ME** (`APPEARANCE_SC04`) — Scrolls; source slot `SC04`.
- [ ] **ETAOIN SHRDLU** (`APPEARANCE_SC05`) — Scrolls; source slot `SC05`.
- [ ] **LOREM IPSUM** (`APPEARANCE_SC06`) — Scrolls; source slot `SC06`.
- [ ] **FNORD** (`APPEARANCE_SC07`) — Scrolls; source slot `SC07`.
- [ ] **KO BATE** (`APPEARANCE_SC08`) — Scrolls; source slot `SC08`.
- [ ] **ABRA KA DABRA** (`APPEARANCE_SC09`) — Scrolls; source slot `SC09`.
- [ ] **ASHPD SODALG** (`APPEARANCE_SC10`) — Scrolls; source slot `SC10`.
- [ ] **ZLORFIK** (`APPEARANCE_SC11`) — Scrolls; source slot `SC11`.
- [ ] **GNIK SISI VLE** (`APPEARANCE_SC12`) — Scrolls; source slot `SC12`.
- [ ] **HAPAX LEGOMENON** (`APPEARANCE_SC13`) — Scrolls; source slot `SC13`.
- [ ] **EIRIS SAZUN IDISI** (`APPEARANCE_SC14`) — Scrolls; source slot `SC14`.
- [ ] **PHOL ENDE WODAN** (`APPEARANCE_SC15`) — Scrolls; source slot `SC15`.
- [ ] **GHOTI** (`APPEARANCE_SC16`) — Scrolls; source slot `SC16`.
- [ ] **MAPIRO MAHAMA DIROMAT** (`APPEARANCE_SC17`) — Scrolls; source slot `SC17`.
- [ ] **VAS CORP BET MANI** (`APPEARANCE_SC18`) — Scrolls; source slot `SC18`.
- [ ] **XOR OTA** (`APPEARANCE_SC19`) — Scrolls; source slot `SC19`.
- [ ] **STRC PRST SKRZ KRK** (`APPEARANCE_SC20`) — Scrolls; source slot `SC20`.
- [ ] **forked** (`APPEARANCE_WAN1`) — Wands; source slot `WAN1`.
- [ ] **spiked** (`APPEARANCE_WAN2`) — Wands; source slot `WAN2`.
- [ ] **jeweled** (`APPEARANCE_WAN3`) — Wands; source slot `WAN3`.

## Artifact overlays

User priority for later art-direction review: weapons received as gifts from
the player's god must look amazing. The user will develop this direction later;
do not start weapon generation from this note. Preserve native knowledge rules.

33 current artifacts linked to their base types. Mjollnir and Cleaver have design/import drafts; no artifact has completed live-knowledge verification. A distinctive treatment is gated by native displayed knowledge, and must not expose an unidentified artifact.

- [ ] **Excalibur** (`ART_EXCALIBUR`) — base `LONG_SWORD`; design and visibility-rule review pending.
- [ ] **Stormbringer** (`ART_STORMBRINGER`) — base `RUNESWORD`; design and visibility-rule review pending.
- [ ] **Mjollnir** (`ART_MJOLLNIR`) — base `WAR_HAMMER`; modelled design/import draft. [Editable asset, myth sources and evidence](Docs/Mjollnir.md). Remaining: native known-artifact eligibility and live unidentified/identified, hallucination, named ordinary hammer, piles/memory/save/fallback/no-turn checks.
- [ ] **Cleaver** (`ART_CLEAVER`) — base `BATTLE_AXE`; oversized barbarian design/import draft. [Model and evidence](Docs/Cleaver.md). Remaining: native known-artifact eligibility and live knowledge/pile/memory/hallucination/save/fallback/no-turn checks.
- [ ] **Grimtooth** (`ART_GRIMTOOTH`) — base `ORCISH_DAGGER`; design and visibility-rule review pending.
- [ ] **Orcrist** (`ART_ORCRIST`) — base `ELVEN_BROADSWORD`; design and visibility-rule review pending.
- [ ] **Sting** (`ART_STING`) — base `ELVEN_DAGGER`; design and visibility-rule review pending.
- [ ] **Magicbane** (`ART_MAGICBANE`) — base `ATHAME`; design and visibility-rule review pending.
- [ ] **Frost Brand** (`ART_FROST_BRAND`) — base `LONG_SWORD`; design and visibility-rule review pending.
- [ ] **Fire Brand** (`ART_FIRE_BRAND`) — base `LONG_SWORD`; design and visibility-rule review pending.
- [ ] **Dragonbane** (`ART_DRAGONBANE`) — base `BROADSWORD`; design and visibility-rule review pending.
- [ ] **Demonbane** (`ART_DEMONBANE`) — base `SILVER_MACE`; design and visibility-rule review pending.
- [ ] **Werebane** (`ART_WEREBANE`) — base `SILVER_SABER`; design and visibility-rule review pending.
- [ ] **Grayswandir** (`ART_GRAYSWANDIR`) — base `SILVER_SABER`; design and visibility-rule review pending.
- [ ] **Giantslayer** (`ART_GIANTSLAYER`) — base `LONG_SWORD`; design and visibility-rule review pending.
- [ ] **Ogresmasher** (`ART_OGRESMASHER`) — base `WAR_HAMMER`; design and visibility-rule review pending.
- [ ] **Trollsbane** (`ART_TROLLSBANE`) — base `MORNING_STAR`; design and visibility-rule review pending.
- [ ] **Vorpal Blade** (`ART_VORPAL_BLADE`) — base `LONG_SWORD`; design and visibility-rule review pending.
- [ ] **Snickersnee** (`ART_SNICKERSNEE`) — base `KATANA`; design and visibility-rule review pending.
- [ ] **Sunsword** (`ART_SUNSWORD`) — base `LONG_SWORD`; design and visibility-rule review pending.
- [ ] **The Orb of Detection** (`ART_ORB_OF_DETECTION`) — base `CRYSTAL_BALL`; design and visibility-rule review pending.
- [ ] **The Heart of Ahriman** (`ART_HEART_OF_AHRIMAN`) — base `LUCKSTONE`; design and visibility-rule review pending.
- [ ] **The Sceptre of Might** (`ART_SCEPTRE_OF_MIGHT`) — base `MACE`; design and visibility-rule review pending.
- [ ] **The Staff of Aesculapius** (`ART_STAFF_OF_AESCULAPIUS`) — base `QUARTERSTAFF`; design and visibility-rule review pending.
- [ ] **The Magic Mirror of Merlin** (`ART_MAGIC_MIRROR_OF_MERLIN`) — base `MIRROR`; design and visibility-rule review pending.
- [ ] **The Eyes of the Overworld** (`ART_EYES_OF_THE_OVERWORLD`) — base `LENSES`; design and visibility-rule review pending.
- [ ] **The Mitre of Holiness** (`ART_MITRE_OF_HOLINESS`) — base `HELM_OF_BRILLIANCE`; design and visibility-rule review pending.
- [ ] **The Longbow of Diana** (`ART_LONGBOW_OF_DIANA`) — base `BOW`; design and visibility-rule review pending.
- [ ] **The Master Key of Thievery** (`ART_MASTER_KEY_OF_THIEVERY`) — base `SKELETON_KEY`; design and visibility-rule review pending.
- [ ] **The Tsurugi of Muramasa** (`ART_TSURUGI_OF_MURAMASA`) — base `TSURUGI`; design and visibility-rule review pending.
- [ ] **The Platinum Yendorian Express Card** (`ART_YENDORIAN_EXPRESS_CARD`) — base `CREDIT_CARD`; design and visibility-rule review pending.
- [ ] **The Orb of Fate** (`ART_ORB_OF_FATE`) — base `CRYSTAL_BALL`; design and visibility-rule review pending.
- [ ] **The Eye of the Aethiopica** (`ART_EYE_OF_THE_AETHIOPICA`) — base `AMULET_OF_ESP`; design and visibility-rule review pending.

## Conditional, deferred and auxiliary scope

- Conditional `SCR_MAIL` is included once above; it is not a guaranteed player-build item. The base unconditional list contains 439 types.
- Four `#if 0` declarations are excluded from the 440 named-type target: `SHIMMERING_DRAGON_SCALE_MAIL`, `SHIMMERING_DRAGON_SCALES`, `SPE_FLAME_SPHERE`, `SPE_FREEZE_SPHERE`. Shimmering dragon armor retains official source tiles; that does not make it active gameplay content.
- Eighteen display auxiliaries (strange object plus 17 generic classes) are retained in JSON/CSV. They are not ordinary loot identities and need separate fallback/glyph scope review.
- Obsolete artifact `ART_PALANTIR_OF_WESTERNESSE` is recorded separately; it is not one of the 33 current designs.

## Finishing and rendering work

- [ ] Establish a reviewed beautiful-object finish target at dungeon, room and close inspection scales.
- [ ] Build shared construction families while preserving meaningful silhouette/proportion/ornament differences.
- [ ] Design the native appearance/knowledge protocol before extending beyond the current fixed-object whitelist; cover shuffling, same-look objects, piles, memory, hallucination, save/restore and identification.
- [ ] Refine existing wood/metal/coin/corpse drafts and review LOD/runtime costs.
- [ ] Scope carried/equipped visuals against displayed information before showing NPC/player equipment dynamically.
- [ ] Scope corpse/statue species variants, food states, containers and quantity representations separately; do not infer hidden contents, traps or exact stack size from decorative geometry.

Creature completion counts remain separate. No new objects are generated by creating this inventory.


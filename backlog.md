# Creature asset backlog

Working checklist for anatomical creature and player-role assets. Based on the pinned NetHack source catalogue; updated 2026-11-04. This file is maintained by hand: preserve its checkboxes and notes when the catalogue is regenerated.

**394 source identities: 100 generated creature drafts + 2 completed player-role presentations + 281 remaining creature identities + 11 remaining player-role presentations.** Creature forms include four additional female appearances (beardless gnomish wizard/gnome zombie and independently proportioned soldier/fire ants), giving 104 physical creature forms across 100 identities. Four human player forms exist: female Valkyrie, male Barbarian, male Samurai and female Samurai. Barbarian remains partial because its female starting-sex target has not been generated. The player roles cover 25 permitted starting-sex variants; these are validation targets, not 25 mandatory separate sculpts.

Verified static-draft coverage: **100/381 creatures (26.2%)**, or **102/394 creature/player identities (25.9%)**. This does not measure visual finishing or the separate object/terrain inventories. Static presentation is the finished target; see [Game vision](Docs/GameVision.md).

## How to use this backlog

- Choose the next unchecked item from the suggested batches, then find its full record in [creatures.json](Art/CreatureCatalogue/creatures.json). Use the stable `PM_*` ID, since display names can repeat.
- Check a generation item only after editable Blender geometry, painted FBX, actual front/rear and 16x16 comparisons, Unreal import/material validation, and displayed-identity mapping/fallback checks exist. Link the evidence beside the item.
- **Checked means generated and verified as a static draft. It does not mean finished production art.** Track later visual refinement and runtime review in the completion section below. Animation is out of scope.
- One identity need not mean one independent mesh: reuse compatible family anatomy and keep clothing, rank, equipment, age, undead state and effects separate. Preserve distinct silhouettes.
- Suggested batches are recommendations, not authorizations to generate. Conditional and auxiliary source records need runtime/scope review before modelling.
- When completing an item, mark its existing checkbox in place and add evidence; do not add a duplicate entry. Move the suggested next batch forward and update the counts above.
- Follow [Session handoff](Docs/CreatureAssetContext.md). Keep source facts separate from artistic assumptions; select live assets only from displayed identity.

Winter wolf cub and winter wolf were revised after user review: cyan tile-shadow
colours removed; eyes moved forward/inward and embedded with eyelids. See the
[revised close views and evidence](Docs/CreatureBatch5.md). These remain static drafts.

## Suggested next batches

1. **Brown mold, yellow mold and green mold** (`PM_BROWN_MOLD`, `PM_YELLOW_MOLD`, `PM_GREEN_MOLD`): inspect source/sex tiles and fungal growth forms; distinct surface/silhouette construction rather than gel recolours.



## Generated and verified static drafts

- [x] **giant ant** (`PM_GIANT_ANT`) — [FBX](Art/CreatureInterpretations/giant_ant.fbx), [evidence](Docs/CreatureInterpretations.md).
- [x] **jackal** (`PM_JACKAL`) — [FBX](Art/CreatureInterpretations/jackal.fbx), [evidence](Docs/CreatureBatch2.md).
- [x] **fox** (`PM_FOX`) — [FBX](Art/CreatureInterpretations/fox.fbx), [evidence](Docs/CreatureBatch2.md).
- [x] **little dog** (`PM_LITTLE_DOG`) — [FBX](Art/CreatureInterpretations/little_dog.fbx), [evidence](Docs/CreatureInterpretations.md).
- [x] **goblin** (`PM_GOBLIN`) — [FBX](Art/CreatureInterpretations/goblin.fbx), [evidence](Docs/CreatureInterpretations.md).
- [x] **gnome** (`PM_GNOME`) — [FBX](Art/CreatureInterpretations/gnome.fbx), [evidence](Docs/CreatureBatch2.md).

Jackal review correction: removed the raised back overlay; darker fur is painted on the body. [Updated view](Art/CreatureInterpretations/jackal-three-quarter.png).

## Creature generation checklist by anatomy group

Batch 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 22, 23 and 24 completions, plus requested special batch 2 shopkeeper, are checked in place below; unchecked entries remain to generate.

The family names below are modelling proposals, not scientific taxonomy or a requirement for shared runtime rigs. Conditional declarations are retained for completeness, not counted as confirmed runtime monsters.

### Amorphous life / Disguised bodies / Mimics

- [ ] **small mimic** (`PM_SMALL_MIMIC`) — base `mimics`.
- [ ] **large mimic** (`PM_LARGE_MIMIC`) — base `mimics`.
- [ ] **giant mimic** (`PM_GIANT_MIMIC`) — base `mimics`.

### Amorphous life / Soft bodies / Blobs

- [x] **acid blob** (`PM_ACID_BLOB`) — neuter shared-art gel draft, saved geometry/paint/native/import/live/fallback/F9 verified. [Batch 30 evidence](Docs/CreatureBatch30.md).
- [x] **quivering blob** (`PM_QUIVERING_BLOB`) — neuter shared-art gel draft, saved geometry/paint/native/import/live/fallback/F9 verified. [Batch 30 evidence](Docs/CreatureBatch30.md).
- [x] **gelatinous cube** (`PM_GELATINOUS_CUBE`) — neuter shared-art gel draft, saved geometry/paint/native/import/live/fallback/F9 verified. [Batch 30 evidence](Docs/CreatureBatch30.md).

### Amorphous life / Soft bodies / Jellies

- [x] **blue jelly** (`PM_BLUE_JELLY`) — neuter shared-art jelly draft; geometry/paint/native/import/live/fallback/F9 verified. [Batch 31 evidence](Docs/CreatureBatch31.md).
- [x] **spotted jelly** (`PM_SPOTTED_JELLY`) — neuter shared-art jelly draft; geometry/paint/native/import/live/fallback/F9 verified. [Batch 31 evidence](Docs/CreatureBatch31.md).
- [x] **ochre jelly** (`PM_OCHRE_JELLY`) — neuter shared-art jelly draft; geometry/paint/native/import/live/fallback/F9 verified. [Batch 31 evidence](Docs/CreatureBatch31.md).

### Amorphous life / Soft bodies / Puddings and oozes

- [x] **gray ooze** (`PM_GRAY_OOZE`) — shared-art draft; source/geometry/paint/native/import/live/fallback/F9 verified. [Batch 32 evidence](Docs/CreatureBatch32.md).
- [x] **brown pudding** (`PM_BROWN_PUDDING`) — shared-art draft; source/geometry/paint/native/import/live/fallback/F9 verified. [Batch 32 evidence](Docs/CreatureBatch32.md).
- [ ] **green slime** (`PM_GREEN_SLIME`) — base `puddings_and_oozes`.
- [x] **black pudding** (`PM_BLACK_PUDDING`) — shared-art draft; source/geometry/paint/native/import/live/fallback/F9 verified. [Batch 32 evidence](Docs/CreatureBatch32.md).

### Animals / Aquatic bodies / Aquatic animals

- [ ] **giant eel** (`PM_GIANT_EEL`) — base `aquatic_animals`.
- [ ] **electric eel** (`PM_ELECTRIC_EEL`) — base `aquatic_animals`.

### Animals / Aquatic bodies / Cephalopods

- [ ] **kraken** (`PM_KRAKEN`) — base `cephalopods`.

### Animals / Aquatic bodies / Fish

- [ ] **piranha** (`PM_PIRANHA`) — base `fish`.

### Animals / Aquatic bodies / Jellyfish

- [ ] **jellyfish** (`PM_JELLYFISH`) — base `jellyfish`.

### Animals / Aquatic bodies / Sharks

- [ ] **shark** (`PM_SHARK`) — base `sharks`.

### Animals / Arthropods / Ants

- [x] **soldier ant** (`PM_SOLDIER_ANT`) — two source-supported sex forms; independently proportioned female thorax/leg reach. [Batch 22 artifacts and checks](Docs/CreatureBatch22.md).
- [x] **fire ant** (`PM_FIRE_ANT`) — two source-supported sex forms; independently proportioned female thorax/leg reach. [Batch 22 artifacts and checks](Docs/CreatureBatch22.md).

### Animals / Arthropods / Arachnids

- [ ] **centipede** (`PM_CENTIPEDE`) — base `arachnids`.
- [ ] **Scorpius** (`PM_SCORPIUS`) — base `arachnids`.

### Animals / Arthropods / Bees

- [x] **killer bee** (`PM_KILLER_BEE`) — female-only source species, four-wing static flight form. [Batch 23 artifacts and checks](Docs/CreatureBatch23.md).
- [x] **queen bee** (`PM_QUEEN_BEE`) — female-only source species, four-wing static flight form. [Batch 23 artifacts and checks](Docs/CreatureBatch23.md).

### Animals / Arthropods / Beetles

- [x] **giant beetle** (`PM_GIANT_BEETLE`) — shared-sex broad beetle body with fitted closed elytra. [Batch 22 artifacts and checks](Docs/CreatureBatch22.md).

### Animals / Arthropods / Flying insects

- [x] **grid bug** (`PM_GRID_BUG`) — base `flying_insects` is a broad catalogue group, not a flight flag; six-legged static electronic arthropod, without wings. [FBX](Art/CreatureInterpretations/grid_bug.fbx), [special batch evidence](Docs/SpecialBatch1.md).
- [x] **xan** (`PM_XAN`) — separate mosquito-like body, two wings, long legs and proboscis. [Batch 23 artifacts and checks](Docs/CreatureBatch23.md).

### Animals / Arthropods / Scorpions

- [x] **scorpion** (`PM_SCORPION`) — separate eight-legged body, two pincers and five-segment raised tail/telson. [Batch 24 artifacts and checks](Docs/CreatureBatch24.md).

### Animals / Arthropods / Spiders

- [x] **cave spider** (`PM_CAVE_SPIDER`) — shared-sex eight-legged spider family; independent body dimensions. [Batch 24 artifacts and checks](Docs/CreatureBatch24.md).
- [x] **giant spider** (`PM_GIANT_SPIDER`) — shared-sex eight-legged spider family; independent body dimensions. [Batch 24 artifacts and checks](Docs/CreatureBatch24.md).

### Animals / Invertebrates / Worms

- [ ] **baby long worm** (`PM_BABY_LONG_WORM`) — base `worms`.
- [ ] **baby purple worm** (`PM_BABY_PURPLE_WORM`) — base `worms`.
- [ ] **long worm** (`PM_LONG_WORM`) — base `worms`.
- [ ] **purple worm** (`PM_PURPLE_WORM`) — base `worms`.

### Animals / Mammals / Bats

- [x] **bat** (`PM_BAT`) — base `bats`. [Batch 8 artifacts and checks](Docs/CreatureBatch8.md).
- [x] **giant bat** (`PM_GIANT_BAT`) — base `bats`. [Batch 8 artifacts and checks](Docs/CreatureBatch8.md).
- [ ] **raven** (`PM_RAVEN`) — base `bats`.
- [x] **vampire bat** (`PM_VAMPIRE_BAT`) — base `bats`. [Batch 8 artifacts and checks](Docs/CreatureBatch8.md).

### Animals / Mammals / Canids

- [x] **coyote** (`PM_COYOTE`) — base `canid`. [Batch 7 artifacts and checks](Docs/CreatureBatch7.md).
- [x] **dingo** (`PM_DINGO`) — base `canid`. [Batch 6 artifacts and checks](Docs/CreatureBatch6.md).
- [x] **dog** (`PM_DOG`) — base `dog`. [Batch 6 artifacts and checks](Docs/CreatureBatch6.md).
- [x] **large dog** (`PM_LARGE_DOG`) — base `dog`. [Batch 6 artifacts and checks](Docs/CreatureBatch6.md).
- [x] **wolf** (`PM_WOLF`) — base `wolf`. [Batch 5 artifacts and checks](Docs/CreatureBatch5.md).
- [x] **winter wolf cub** (`PM_WINTER_WOLF_CUB`) — base `wolf`; reuse winter wolf. [Batch 5 artifacts and checks](Docs/CreatureBatch5.md).
- [x] **warg** (`PM_WARG`) — base `canid`. [Batch 7 artifacts and checks](Docs/CreatureBatch7.md).
- [x] **winter wolf** (`PM_WINTER_WOLF`) — base `wolf`. [Batch 5 artifacts and checks](Docs/CreatureBatch5.md).
- [x] **hell hound pup** (`PM_HELL_HOUND_PUP`) — base `canid`. [Batch 10 artifacts and checks](Docs/CreatureBatch10.md).
- [x] **hell hound** (`PM_HELL_HOUND`) — base `canid`. [Batch 10 artifacts and checks](Docs/CreatureBatch10.md).
- [ ] **Cerberus** (`PM_CERBERUS`) — base `canid`; conditional: ifdef CHARON.

### Animals / Mammals / Felids

- [x] **kitten** (`PM_KITTEN`) — base `felids`. [Batch 4 artifacts and checks](Docs/CreatureBatch4.md).
- [x] **housecat** (`PM_HOUSECAT`) — base `felids`. [Batch 4 artifacts and checks](Docs/CreatureBatch4.md).
- [x] **jaguar** (`PM_JAGUAR`) — base `felids`. [Batch 9 artifacts and checks](Docs/CreatureBatch9.md). [User-reference coat revision](Docs/JaguarReferenceRevision.md).
- [x] **lynx** (`PM_LYNX`) — base `felids`. [Batch 9 artifacts and checks](Docs/CreatureBatch9.md).
- [x] **panther** (`PM_PANTHER`) — base `felids`. [Batch 9 artifacts and checks](Docs/CreatureBatch9.md).
- [x] **large cat** (`PM_LARGE_CAT`) — base `felids`. [Batch 4 artifacts and checks](Docs/CreatureBatch4.md).
- [x] **tiger** (`PM_TIGER`) — base `felids`. [Batch 10 artifacts and checks](Docs/CreatureBatch10.md).
- [ ] **displacer beast** (`PM_DISPLACER_BEAST`) — base `felids`.

### Animals / Mammals / Primates

- [x] **monkey** (`PM_MONKEY`) — shared-sex static primate; independent proportions, complete hands/feet and texture-only fur. [Batch 28 artifacts and checks](Docs/CreatureBatch28.md).
- [x] **ape** (`PM_APE`) — shared-sex static primate; independent proportions, complete hands/feet and texture-only fur. [Batch 28 artifacts and checks](Docs/CreatureBatch28.md).
- [x] **carnivorous ape** (`PM_CARNIVOROUS_APE`) — shared-sex static primate; independent proportions, complete hands/feet and texture-only fur. [Batch 28 artifacts and checks](Docs/CreatureBatch28.md).

### Animals / Mammals / Rodents

- [x] **sewer rat** (`PM_SEWER_RAT`) — base `rat`. [Batch 3 artifacts and checks](Docs/CreatureBatch3.md).
- [x] **giant rat** (`PM_GIANT_RAT`) — base `rat`; reuse sewer rat. [Batch 3 artifacts and checks](Docs/CreatureBatch3.md).
- [x] **rabid rat** (`PM_RABID_RAT`) — base `rat`. [Batch 7 artifacts and checks](Docs/CreatureBatch7.md).
- [ ] **rock mole** (`PM_ROCK_MOLE`) — base `rock_mole`.
- [ ] **woodchuck** (`PM_WOODCHUCK`) — base `woodchuck`.

### Animals / Reptiles / Snakes

- [x] **garter snake** (`PM_GARTER_SNAKE`) — shared-sex continuous snake body; distinct head, girth and coil. [Batch 26 artifacts and checks](Docs/CreatureBatch26.md).
- [x] **snake** (`PM_SNAKE`) — shared-sex continuous snake body; distinct head, girth and coil. [Batch 26 artifacts and checks](Docs/CreatureBatch26.md).
- [x] **water moccasin** (`PM_WATER_MOCCASIN`) — shared-sex continuous snake body; distinct head, girth and coil. [Batch 26 artifacts and checks](Docs/CreatureBatch26.md).
- [x] **python** (`PM_PYTHON`) — shared-sex painted snake draft; distinct constrictor/viper/hood anatomy. [Batch 27 artifacts and checks](Docs/CreatureBatch27.md).
- [x] **pit viper** (`PM_PIT_VIPER`) — shared-sex painted snake draft; distinct constrictor/viper/hood anatomy. [Batch 27 artifacts and checks](Docs/CreatureBatch27.md).
- [x] **cobra** (`PM_COBRA`) — shared-sex painted snake draft; distinct constrictor/viper/hood anatomy. [Batch 27 artifacts and checks](Docs/CreatureBatch27.md).

### Animals / Reptiles and amphibians / Crocodilians

- [ ] **baby crocodile** (`PM_BABY_CROCODILE`) — base `crocodilians`.
- [ ] **crocodile** (`PM_CROCODILE`) — base `crocodilians`.

### Animals / Reptiles and amphibians / Geckos

- [x] **gecko** (`PM_GECKO`) — shared-sex painted reptile draft; independent head, body, feet and tail proportions. [Batch 25 artifacts and checks](Docs/CreatureBatch25.md).

### Animals / Reptiles and amphibians / Mixed small reptiles

- [x] **iguana** (`PM_IGUANA`) — shared-sex painted reptile draft; independent head, body, feet and tail proportions. [Batch 25 artifacts and checks](Docs/CreatureBatch25.md).
- [x] **lizard** (`PM_LIZARD`) — shared-sex painted reptile draft; independent head, body, feet and tail proportions. [Batch 25 artifacts and checks](Docs/CreatureBatch25.md).
- [ ] **chameleon** (`PM_CHAMELEON`) — base `mixed_small_reptiles`.
- [ ] **salamander** (`PM_SALAMANDER`) — base `mixed_small_reptiles`.

### Animals / Reptiles and amphibians / Newts

- [x] **newt** (`PM_NEWT`) — base `newts`; requested early-level draft, shared tile appearance. [FBX](Art/CreatureInterpretations/newt.fbx), [batch 19 evidence](Docs/CreatureBatch19.md).

### Animals and mythic beasts / Primate and hybrid bodies / Apes and hairy bipeds

- [x] **yeti** (`PM_YETI`) — shared-sex static draft; source/geometry/paint/native/import/live/fallback/F9 verified. [Batch 29 evidence](Docs/CreatureBatch29.md).
- [x] **sasquatch** (`PM_SASQUATCH`) — shared-sex static draft; source/geometry/paint/native/import/live/fallback/F9 verified. [Batch 29 evidence](Docs/CreatureBatch29.md).

### Animals and mythic beasts / Quadruped bodies / Large ungulate bodies

- [ ] **titanothere** (`PM_TITANOTHERE`) — base `large_ungulate_bodies`.
- [ ] **baluchitherium** (`PM_BALUCHITHERIUM`) — base `large_ungulate_bodies`.

### Animals and mythic beasts / Quadruped bodies / Mixed large quadrupeds

- [ ] **leocrotta** (`PM_LEOCROTTA`) — base `mixed_large_quadrupeds`.
- [ ] **wumpus** (`PM_WUMPUS`) — base `mixed_large_quadrupeds`.

### Animals and mythic beasts / Quadruped bodies / Proboscideans

- [ ] **mumak** (`PM_MUMAK`) — base `proboscideans`.
- [ ] **mastodon** (`PM_MASTODON`) — base `proboscideans`.

### Animals and mythic beasts / Quadruped bodies / Rothe

- [ ] **rothe** (`PM_ROTHE`) — base `rothe`.

### Constructs / Material bodies / Golems

- [ ] **straw golem** (`PM_STRAW_GOLEM`) — base `golems`.
- [ ] **paper golem** (`PM_PAPER_GOLEM`) — base `golems`.
- [ ] **rope golem** (`PM_ROPE_GOLEM`) — base `golems`.
- [ ] **gold golem** (`PM_GOLD_GOLEM`) — base `golems`.
- [ ] **leather golem** (`PM_LEATHER_GOLEM`) — base `golems`.
- [ ] **wood golem** (`PM_WOOD_GOLEM`) — base `golems`.
- [ ] **flesh golem** (`PM_FLESH_GOLEM`) — base `golems`.
- [ ] **clay golem** (`PM_CLAY_GOLEM`) — base `golems`.
- [ ] **stone golem** (`PM_STONE_GOLEM`) — base `golems`.
- [ ] **glass golem** (`PM_GLASS_GOLEM`) — base `golems`.
- [ ] **iron golem** (`PM_IRON_GOLEM`) — base `golems`.

### Display auxiliaries / Body segments / Worm tails

- [ ] **long worm tail** (`PM_LONG_WORM_TAIL`) — base `worm_tails`.

### Elemental manifestations / Elemental bodies / Elementals

- [ ] **stalker** (`PM_STALKER`) — base `elementals`.
- [ ] **air elemental** (`PM_AIR_ELEMENTAL`) — base `elementals`.
- [ ] **fire elemental** (`PM_FIRE_ELEMENTAL`) — base `elementals`.
- [ ] **earth elemental** (`PM_EARTH_ELEMENTAL`) — base `elementals`.
- [ ] **water elemental** (`PM_WATER_ELEMENTAL`) — base `elementals`.

### Elemental manifestations / Luminous bodies / Lights

- [ ] **yellow light** (`PM_YELLOW_LIGHT`) — base `lights`.
- [ ] **black light** (`PM_BLACK_LIGHT`) — base `lights`.

### Elemental manifestations / Volume effects / Vortices

- [ ] **fog cloud** (`PM_FOG_CLOUD`) — base `vortices`.
- [ ] **dust vortex** (`PM_DUST_VORTEX`) — base `vortices`.
- [ ] **ice vortex** (`PM_ICE_VORTEX`) — base `vortices`.
- [ ] **energy vortex** (`PM_ENERGY_VORTEX`) — base `vortices`.
- [ ] **steam vortex** (`PM_STEAM_VORTEX`) — base `vortices`.
- [ ] **fire vortex** (`PM_FIRE_VORTEX`) — base `vortices`.

### Fungi / Floating spore bodies / Gas spores

- [ ] **gas spore** (`PM_GAS_SPORE`) — base `gas_spores`.

### Fungi / Fungal bodies / Fungi and molds

- [x] **lichen** (`PM_LICHEN`) — base `fungi_and_molds`; requested early-level draft, shared tile appearance. [FBX](Art/CreatureInterpretations/lichen.fbx), [batch 19 evidence](Docs/CreatureBatch19.md).
- [ ] **brown mold** (`PM_BROWN_MOLD`) — base `fungi_and_molds`.
- [ ] **yellow mold** (`PM_YELLOW_MOLD`) — base `fungi_and_molds`.
- [ ] **green mold** (`PM_GREEN_MOLD`) — base `fungi_and_molds`.
- [ ] **red mold** (`PM_RED_MOLD`) — base `fungi_and_molds`.
- [ ] **shrieker** (`PM_SHRIEKER`) — base `fungi_and_molds`.
- [ ] **violet fungus** (`PM_VIOLET_FUNGUS`) — base `fungi_and_molds`.

### Humanoid peoples / Humanoids / Dwarves

- [x] **dwarf** (`PM_DWARF`) — [painted FBX](Art/CreatureInterpretations/dwarf.fbx), [batch 16 source, shared-sex anatomy and verification](Docs/CreatureBatch16.md).
- [x] **dwarf leader** (`PM_DWARF_LEADER`) — [painted FBX](Art/CreatureInterpretations/dwarf_leader.fbx), [batch 16 source, shared-sex anatomy and verification](Docs/CreatureBatch16.md).
- [x] **dwarf ruler** (`PM_DWARF_RULER`) — [painted FBX](Art/CreatureInterpretations/dwarf_ruler.fbx), [batch 16 source, shared-sex anatomy and verification](Docs/CreatureBatch16.md).

### Humanoid peoples / Humanoids / Elves

- [ ] **elf** (`PM_ELF`) — base `elves`.
- [ ] **Woodland-elf** (`PM_WOODLAND_ELF`) — base `elves`.
- [ ] **Green-elf** (`PM_GREEN_ELF`) — base `elves`.
- [ ] **Grey-elf** (`PM_GREY_ELF`) — base `elves`.
- [ ] **elf-noble** (`PM_ELF_NOBLE`) — base `elves`; aliases: elf-lord, elf-lady.
- [ ] **elven monarch** (`PM_ELVEN_MONARCH`) — base `elves`; aliases: Elvenking, Elvenqueen.
- [ ] **Earendil** (`PM_EARENDIL`) — base `elves`; conditional: if 0.
- [ ] **Elwing** (`PM_ELWING`) — base `elves`; conditional: if 0.
- [ ] **High-elf** (`PM_HIGH_ELF`) — base `elves`; conditional: if 0.

### Humanoid peoples / Humanoids / Hobbits

- [ ] **hobbit** (`PM_HOBBIT`) — base `hobbits`.

### Humanoid peoples / Humanoids / Humans and special identities

- [ ] **human** (`PM_HUMAN`) — base `humans_and_special_identities`.
- [ ] **doppelganger** (`PM_DOPPELGANGER`) — base `humans_and_special_identities`.
- [x] **shopkeeper** (`PM_SHOPKEEPER`) — shared icon appearance for both native sexes; black hat, blue/cyan jacket, green trousers. [Special batch 2 artifacts and checks](Docs/SpecialBatch2.md).
- [ ] **guard** (`PM_GUARD`) — base `humans_and_special_identities`.
- [ ] **prisoner** (`PM_PRISONER`) — base `humans_and_special_identities`.
- [x] **Oracle** (`PM_ORACLE`) — seated human Pythia, raised hands, white hair/laurel and cyan/blue folded chiton; saved geometry, true tiny projections, imported paint/materials, displayed identity/fallback/F9 and real Oracle-room capture verified. [Evidence](Docs/OracleCreature.md).
- [ ] **aligned cleric** (`PM_ALIGNED_CLERIC`) — base `humans_and_special_identities`; aliases: priest, priestess.
- [ ] **high cleric** (`PM_HIGH_CLERIC`) — base `humans_and_special_identities`; aliases: high priest, high priestess.
- [ ] **soldier** (`PM_SOLDIER`) — base `humans_and_special_identities`.
- [ ] **sergeant** (`PM_SERGEANT`) — base `humans_and_special_identities`.
- [ ] **nurse** (`PM_NURSE`) — base `humans_and_special_identities`.
- [ ] **lieutenant** (`PM_LIEUTENANT`) — base `humans_and_special_identities`.
- [ ] **captain** (`PM_CAPTAIN`) — base `humans_and_special_identities`.
- [ ] **watchman** (`PM_WATCHMAN`) — base `humans_and_special_identities`.
- [ ] **watch captain** (`PM_WATCH_CAPTAIN`) — base `humans_and_special_identities`.
- [ ] **Medusa** (`PM_MEDUSA`) — base `humans_and_special_identities`.
- [ ] **Wizard of Yendor** (`PM_WIZARD_OF_YENDOR`) — base `humans_and_special_identities`.
- [ ] **Croesus** (`PM_CROESUS`) — base `humans_and_special_identities`.
- [ ] **Charon** (`PM_CHARON`) — base `humans_and_special_identities`; conditional: ifdef CHARON.
- [ ] **Lord Carnarvon** (`PM_LORD_CARNARVON`) — base `humans_and_special_identities`.
- [ ] **Pelias** (`PM_PELIAS`) — base `humans_and_special_identities`.
- [ ] **Shaman Karnov** (`PM_SHAMAN_KARNOV`) — base `humans_and_special_identities`.
- [ ] **Hippocrates** (`PM_HIPPOCRATES`) — base `humans_and_special_identities`.
- [ ] **King Arthur** (`PM_KING_ARTHUR`) — base `humans_and_special_identities`.
- [ ] **Grand Master** (`PM_GRAND_MASTER`) — base `humans_and_special_identities`.
- [ ] **Arch Priest** (`PM_ARCH_PRIEST`) — base `humans_and_special_identities`.
- [ ] **Orion** (`PM_ORION`) — base `humans_and_special_identities`.
- [ ] **Master of Thieves** (`PM_MASTER_OF_THIEVES`) — base `humans_and_special_identities`.
- [ ] **Lord Sato** (`PM_LORD_SATO`) — base `humans_and_special_identities`.
- [ ] **Twoflower** (`PM_TWOFLOWER`) — base `humans_and_special_identities`.
- [ ] **Norn** (`PM_NORN`) — base `humans_and_special_identities`.
- [ ] **Neferet the Green** (`PM_NEFERET_THE_GREEN`) — base `humans_and_special_identities`.
- [ ] **Thoth Amon** (`PM_THOTH_AMON`) — base `humans_and_special_identities`.
- [ ] **Master Kaen** (`PM_MASTER_KAEN`) — base `humans_and_special_identities`.
- [ ] **Master Assassin** (`PM_MASTER_ASSASSIN`) — base `humans_and_special_identities`.
- [ ] **Ashikaga Takauji** (`PM_ASHIKAGA_TAKAUJI`) — base `humans_and_special_identities`.
- [ ] **Dark One** (`PM_DARK_ONE`) — base `humans_and_special_identities`.
- [ ] **student** (`PM_STUDENT`) — base `humans_and_special_identities`.
- [ ] **chieftain** (`PM_CHIEFTAIN`) — base `humans_and_special_identities`.
- [ ] **neanderthal** (`PM_NEANDERTHAL`) — base `humans_and_special_identities`.
- [ ] **attendant** (`PM_ATTENDANT`) — base `humans_and_special_identities`.
- [ ] **page** (`PM_PAGE`) — base `humans_and_special_identities`.
- [ ] **abbot** (`PM_ABBOT`) — base `humans_and_special_identities`.
- [ ] **acolyte** (`PM_ACOLYTE`) — base `humans_and_special_identities`.
- [ ] **hunter** (`PM_HUNTER`) — base `humans_and_special_identities`.
- [ ] **thug** (`PM_THUG`) — base `humans_and_special_identities`.
- [ ] **ninja** (`PM_NINJA`) — base `humans_and_special_identities`.
- [ ] **roshi** (`PM_ROSHI`) — base `humans_and_special_identities`.
- [ ] **guide** (`PM_GUIDE`) — base `humans_and_special_identities`.
- [ ] **warrior** (`PM_WARRIOR`) — base `humans_and_special_identities`.
- [ ] **apprentice** (`PM_APPRENTICE`) — base `humans_and_special_identities`.

### Humanoid peoples / Humanoids / Keystone Kops

- [ ] **Keystone Kop** (`PM_KEYSTONE_KOP`) — base `keystone_kops`.
- [ ] **Kop Sergeant** (`PM_KOP_SERGEANT`) — base `keystone_kops`.
- [ ] **Kop Lieutenant** (`PM_KOP_LIEUTENANT`) — base `keystone_kops`.
- [ ] **Kop Kaptain** (`PM_KOP_KAPTAIN`) — base `keystone_kops`.

### Humanoid peoples / Humanoids / Mind flayers

- [ ] **mind flayer** (`PM_MIND_FLAYER`) — base `mind_flayers`.
- [ ] **master mind flayer** (`PM_MASTER_MIND_FLAYER`) — base `mind_flayers`.

### Humanoid peoples / Humanoids / Mixed humanoids

- [ ] **bugbear** (`PM_BUGBEAR`) — base `mixed_humanoids`.

### Humanoid peoples / Humanoids / Orcs

- [x] **hobgoblin** (`PM_HOBGOBLIN`) — base `orcs`; shared sex appearance. [FBX](Art/CreatureInterpretations/hobgoblin.fbx), [batch 18 evidence](Docs/CreatureBatch18.md).
- [ ] **orc** (`PM_ORC`) — base `orcs`.
- [x] **hill orc** (`PM_HILL_ORC`) — base `orcs`; shared sex appearance. [FBX](Art/CreatureInterpretations/hill_orc.fbx), [batch 18 evidence](Docs/CreatureBatch18.md).
- [x] **Mordor orc** (`PM_MORDOR_ORC`) — base `orcs`; shared sex appearance. [FBX](Art/CreatureInterpretations/mordor_orc.fbx), [batch 18 evidence](Docs/CreatureBatch18.md).
- [x] **Uruk-hai** (`PM_URUK_HAI`) — base `orcs`; exact saved ancestry and shared sex appearance. [FBX](Art/CreatureInterpretations/uruk_hai.fbx), [batch 20 evidence](Docs/CreatureBatch20.md).
- [x] **orc shaman** (`PM_ORC_SHAMAN`) — base `orcs`; exact saved ancestry and shared sex appearance. [FBX](Art/CreatureInterpretations/orc_shaman.fbx), [batch 20 evidence](Docs/CreatureBatch20.md).
- [x] **orc-captain** (`PM_ORC_CAPTAIN`) — base `orcs`; exact saved ancestry and shared sex appearance. [FBX](Art/CreatureInterpretations/orc_captain.fbx), [batch 20 evidence](Docs/CreatureBatch20.md).
- [ ] **Goblin King** (`PM_GOBLIN_KING`) — base `orcs`; conditional: if 0.

### Humanoid peoples / Humanoids / Science specialists

- [ ] **quantum mechanic** (`PM_QUANTUM_MECHANIC`) — base `science_specialists`.
- [ ] **genetic engineer** (`PM_GENETIC_ENGINEER`) — base `science_specialists`.

### Humanoid peoples / Large humanoids / Giants

- [ ] **giant** (`PM_GIANT`) — base `giants`.
- [ ] **stone giant** (`PM_STONE_GIANT`) — base `giants`.
- [ ] **hill giant** (`PM_HILL_GIANT`) — base `giants`.
- [ ] **fire giant** (`PM_FIRE_GIANT`) — base `giants`.
- [ ] **frost giant** (`PM_FROST_GIANT`) — base `giants`.
- [ ] **ettin** (`PM_ETTIN`) — base `giants`.
- [ ] **storm giant** (`PM_STORM_GIANT`) — base `giants`.
- [ ] **titan** (`PM_TITAN`) — base `giants`.
- [ ] **minotaur** (`PM_MINOTAUR`) — base `giants`.
- [ ] **Cyclops** (`PM_CYCLOPS`) — base `giants`.
- [ ] **Lord Surtur** (`PM_LORD_SURTUR`) — base `giants`.

### Humanoid peoples / Large humanoids / Ogres

- [ ] **ogre** (`PM_OGRE`) — base `ogres`.
- [ ] **ogre leader** (`PM_OGRE_LEADER`) — base `ogres`; aliases: ogre lord, ogre lady.
- [ ] **ogre tyrant** (`PM_OGRE_TYRANT`) — base `ogres`; aliases: ogre king, ogre queen.

### Humanoid peoples / Large humanoids / Trolls

- [ ] **troll** (`PM_TROLL`) — base `trolls`.
- [ ] **ice troll** (`PM_ICE_TROLL`) — base `trolls`.
- [ ] **rock troll** (`PM_ROCK_TROLL`) — base `trolls`.
- [ ] **water troll** (`PM_WATER_TROLL`) — base `trolls`.
- [ ] **Olog-hai** (`PM_OLOG_HAI`) — base `trolls`.

### Humanoid peoples / Small humanoids / Gnomes

- [ ] **gnome leader** (`PM_GNOME_LEADER`) — base `gnome`; aliases: gnome lord, gnome lady.
- [x] **gnomish wizard** (`PM_GNOMISH_WIZARD`) — base `gnome`. [FBX](Art/CreatureInterpretations/gnomish_wizard.fbx), [batch 15 evidence and forms](Docs/CreatureBatch15.md).
- [x] **gnome ruler** (`PM_GNOME_RULER`) — base `gnome`; aliases: gnome king, gnome queen. [Batch 3 artifacts and checks](Docs/CreatureBatch3.md).

### Humanoid peoples / Small humanoids / Kobolds

- [x] **kobold** (`PM_KOBOLD`) — base `kobolds`. [FBX](Art/CreatureInterpretations/kobold.fbx), [batch 13 evidence](Docs/CreatureBatch13.md).
- [x] **large kobold** (`PM_LARGE_KOBOLD`) — base `kobolds`. [FBX](Art/CreatureInterpretations/large_kobold.fbx), [batch 13 evidence](Docs/CreatureBatch13.md).
- [x] **kobold leader** (`PM_KOBOLD_LEADER`) — base `kobolds`; aliases: kobold lord, kobold lady. [FBX](Art/CreatureInterpretations/kobold_leader.fbx), [batch 13 evidence](Docs/CreatureBatch13.md).
- [x] **kobold shaman** (`PM_KOBOLD_SHAMAN`) — base `kobolds`. [FBX](Art/CreatureInterpretations/kobold_shaman.fbx), [batch 14 evidence](Docs/CreatureBatch14.md).

### Humanoid peoples / Small humanoids / Leprechauns

- [ ] **leprechaun** (`PM_LEPRECHAUN`) — base `leprechauns`.

### Mythic bodies / Avian reptile bodies / Cockatrices

- [ ] **chickatrice** (`PM_CHICKATRICE`) — base `cockatrices`.
- [ ] **cockatrice** (`PM_COCKATRICE`) — base `cockatrices`.
- [ ] **pyrolisk** (`PM_PYROLISK`) — base `cockatrices`.

### Mythic bodies / Composite bodies / Centaurs

- [x] **plains centaur** (`PM_PLAINS_CENTAUR`) — complete horse/human anatomy, identical source sex tiles share one sculpt; paint, actual tiny/detail views, native living aliases, imported mesh and pure-white Oracle statue rendering verified. [Evidence](Docs/CentaursAndStatues.md).
- [x] **forest centaur** (`PM_FOREST_CENTAUR`) — complete horse/human anatomy, identical source sex tiles share one sculpt; paint, actual tiny/detail views, native living aliases, imported mesh and pure-white Oracle statue rendering verified. [Evidence](Docs/CentaursAndStatues.md).
- [x] **mountain centaur** (`PM_MOUNTAIN_CENTAUR`) — complete horse/human anatomy, identical source sex tiles share one sculpt; paint, actual tiny/detail views, native living aliases, imported mesh and pure-white Oracle statue rendering verified. [Evidence](Docs/CentaursAndStatues.md).

### Mythic bodies / Composite bodies / Jabberwocks

- [ ] **jabberwock** (`PM_JABBERWOCK`) — base `jabberwocks`.
- [ ] **vorpal jabberwock** (`PM_VORPAL_JABBERWOCK`) — base `jabberwocks`; conditional: if 0.

### Mythic bodies / Composite bodies / Ki-rin

- [ ] **ki-rin** (`PM_KI_RIN`) — base `ki-rin`.

### Mythic bodies / Composite bodies / Owlbears

- [x] **owlbear** (`PM_OWLBEAR`) — shared-sex static draft; source/geometry/paint/native/import/live/fallback/F9 verified. [Batch 29 evidence](Docs/CreatureBatch29.md).

### Mythic bodies / Composite bodies / Winged serpents

- [ ] **couatl** (`PM_COUATL`) — base `winged_serpents`.

### Mythic bodies / Equine bodies / Equines

- [x] **pony** (`PM_PONY`) — base `equines`. [Batch 11 artifacts and checks](Docs/CreatureBatch11.md).
- [x] **white unicorn** (`PM_WHITE_UNICORN`) — base `equines`. [Batch 12 artifacts and checks](Docs/CreatureBatch12.md).
- [x] **gray unicorn** (`PM_GRAY_UNICORN`) — base `equines`. [Batch 12 artifacts and checks](Docs/CreatureBatch12.md).
- [x] **black unicorn** (`PM_BLACK_UNICORN`) — base `equines`. [Batch 12 artifacts and checks](Docs/CreatureBatch12.md).
- [x] **horse** (`PM_HORSE`) — base `equines`. [Batch 11 artifacts and checks](Docs/CreatureBatch11.md).
- [x] **warhorse** (`PM_WARHORSE`) — base `equines`. [Batch 11 artifacts and checks](Docs/CreatureBatch11.md).

### Mythic bodies / Flattened ambush bodies / Trappers and lurkers

- [ ] **lurker above** (`PM_LURKER_ABOVE`) — base `trappers_and_lurkers`.
- [ ] **trapper** (`PM_TRAPPER`) — base `trappers_and_lurkers`.

### Mythic bodies / Floating bodies / Eyes and spheres

- [x] **floating eye** (`PM_FLOATING_EYE`) — base `eyes_and_spheres`; requested early-level draft, shared tile appearance. [FBX](Art/CreatureInterpretations/floating_eye.fbx), [batch 19 evidence](Docs/CreatureBatch19.md).
- [ ] **freezing sphere** (`PM_FREEZING_SPHERE`) — base `eyes_and_spheres`.
- [ ] **flaming sphere** (`PM_FLAMING_SPHERE`) — base `eyes_and_spheres`.
- [ ] **shocking sphere** (`PM_SHOCKING_SPHERE`) — base `eyes_and_spheres`.
- [ ] **beholder** (`PM_BEHOLDER`) — base `eyes_and_spheres`; conditional: if 0.

### Mythic bodies / Humanoids / Nymphs

- [ ] **wood nymph** (`PM_WOOD_NYMPH`) — base `nymphs`.
- [ ] **water nymph** (`PM_WATER_NYMPH`) — base `nymphs`.
- [ ] **mountain nymph** (`PM_MOUNTAIN_NYMPH`) — base `nymphs`.

### Mythic bodies / Insectoid bipeds / Umber hulks

- [ ] **umber hulk** (`PM_UMBER_HULK`) — base `umber_hulks`.

### Mythic bodies / Large bipedal beasts / Zruties

- [ ] **zruty** (`PM_ZRUTY`) — base `zruties`.

### Mythic bodies / Radial bodies / Xorns

- [ ] **xorn** (`PM_XORN`) — base `xorns`.

### Mythic bodies / Rocklike ambush bodies / Piercers

- [ ] **rock piercer** (`PM_ROCK_PIERCER`) — base `piercers`.
- [ ] **iron piercer** (`PM_IRON_PIERCER`) — base `piercers`.
- [ ] **glass piercer** (`PM_GLASS_PIERCER`) — base `piercers`.

### Mythic bodies / Serpentine bodies / Nagas

- [ ] **red naga hatchling** (`PM_RED_NAGA_HATCHLING`) — base `nagas`.
- [ ] **black naga hatchling** (`PM_BLACK_NAGA_HATCHLING`) — base `nagas`.
- [ ] **golden naga hatchling** (`PM_GOLDEN_NAGA_HATCHLING`) — base `nagas`.
- [ ] **guardian naga hatchling** (`PM_GUARDIAN_NAGA_HATCHLING`) — base `nagas`.
- [ ] **red naga** (`PM_RED_NAGA`) — base `nagas`.
- [ ] **black naga** (`PM_BLACK_NAGA`) — base `nagas`.
- [ ] **golden naga** (`PM_GOLDEN_NAGA`) — base `nagas`.
- [ ] **guardian naga** (`PM_GUARDIAN_NAGA`) — base `nagas`.

### Mythic bodies / Small humanoid bodies / Gargoyles

- [ ] **gargoyle** (`PM_GARGOYLE`) — base `gargoyles`.
- [ ] **winged gargoyle** (`PM_WINGED_GARGOYLE`) — base `gargoyles`.

### Mythic bodies / Small humanoid bodies / Gremlins

- [ ] **gremlin** (`PM_GREMLIN`) — base `gremlins`.

### Mythic bodies / Specialised quadrupeds / Disenchanter

- [ ] **disenchanter** (`PM_DISENCHANTER`) — base `disenchanter`.

### Mythic bodies / Specialised quadrupeds / Rust Monster

- [ ] **rust monster** (`PM_RUST_MONSTER`) — base `rust_monster`.

### Mythic bodies / Winged reptiles / Dragons

- [ ] **baby gray dragon** (`PM_BABY_GRAY_DRAGON`) — base `dragon`; reuse gray dragon.
- [ ] **baby gold dragon** (`PM_BABY_GOLD_DRAGON`) — base `dragon`; reuse gold dragon.
- [ ] **baby silver dragon** (`PM_BABY_SILVER_DRAGON`) — base `dragon`; reuse silver dragon.
- [ ] **baby shimmering dragon** (`PM_BABY_SHIMMERING_DRAGON`) — base `dragon`; reuse shimmering dragon; conditional: if 0.
- [ ] **baby red dragon** (`PM_BABY_RED_DRAGON`) — base `dragon`; reuse red dragon.
- [ ] **baby white dragon** (`PM_BABY_WHITE_DRAGON`) — base `dragon`; reuse white dragon.
- [ ] **baby orange dragon** (`PM_BABY_ORANGE_DRAGON`) — base `dragon`; reuse orange dragon.
- [ ] **baby black dragon** (`PM_BABY_BLACK_DRAGON`) — base `dragon`; reuse black dragon.
- [ ] **baby blue dragon** (`PM_BABY_BLUE_DRAGON`) — base `dragon`; reuse blue dragon.
- [ ] **baby green dragon** (`PM_BABY_GREEN_DRAGON`) — base `dragon`; reuse green dragon.
- [ ] **baby yellow dragon** (`PM_BABY_YELLOW_DRAGON`) — base `dragon`; reuse yellow dragon.
- [ ] **gray dragon** (`PM_GRAY_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **gold dragon** (`PM_GOLD_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **silver dragon** (`PM_SILVER_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **shimmering dragon** (`PM_SHIMMERING_DRAGON`) — base `dragon`; reuse adult dragon; conditional: if 0.
- [ ] **red dragon** (`PM_RED_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **white dragon** (`PM_WHITE_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **orange dragon** (`PM_ORANGE_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **black dragon** (`PM_BLACK_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **blue dragon** (`PM_BLUE_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **green dragon** (`PM_GREEN_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **yellow dragon** (`PM_YELLOW_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **Chromatic Dragon** (`PM_CHROMATIC_DRAGON`) — base `dragon`; reuse adult dragon.
- [ ] **Ixoth** (`PM_IXOTH`) — base `dragon`; reuse adult dragon.

### Supernatural beings / Celestial bodies / Celestials

- [ ] **Aleax** (`PM_ALEAX`) — base `celestials`.
- [ ] **Angel** (`PM_ANGEL`) — base `celestials`.
- [ ] **Archon** (`PM_ARCHON`) — base `celestials`.

### Supernatural beings / Infernal and unique bodies / Demons and related identities

- [ ] **water demon** (`PM_WATER_DEMON`) — base `demons_and_related_identities`.
- [ ] **amorous demon** (`PM_AMOROUS_DEMON`) — base `demons_and_related_identities`; aliases: incubus, succubus.
- [ ] **horned devil** (`PM_HORNED_DEVIL`) — base `demons_and_related_identities`.
- [ ] **erinys** (`PM_ERINYS`) — base `demons_and_related_identities`.
- [ ] **barbed devil** (`PM_BARBED_DEVIL`) — base `demons_and_related_identities`.
- [ ] **marilith** (`PM_MARILITH`) — base `demons_and_related_identities`.
- [ ] **vrock** (`PM_VROCK`) — base `demons_and_related_identities`.
- [ ] **hezrou** (`PM_HEZROU`) — base `demons_and_related_identities`.
- [ ] **bone devil** (`PM_BONE_DEVIL`) — base `demons_and_related_identities`.
- [ ] **ice devil** (`PM_ICE_DEVIL`) — base `demons_and_related_identities`.
- [ ] **nalfeshnee** (`PM_NALFESHNEE`) — base `demons_and_related_identities`.
- [ ] **pit fiend** (`PM_PIT_FIEND`) — base `demons_and_related_identities`.
- [ ] **sandestin** (`PM_SANDESTIN`) — base `demons_and_related_identities`.
- [ ] **balrog** (`PM_BALROG`) — base `demons_and_related_identities`.
- [ ] **Juiblex** (`PM_JUIBLEX`) — base `demons_and_related_identities`.
- [ ] **Yeenoghu** (`PM_YEENOGHU`) — base `demons_and_related_identities`.
- [ ] **Orcus** (`PM_ORCUS`) — base `demons_and_related_identities`.
- [ ] **Geryon** (`PM_GERYON`) — base `demons_and_related_identities`.
- [ ] **Dispater** (`PM_DISPATER`) — base `demons_and_related_identities`.
- [ ] **Baalzebub** (`PM_BAALZEBUB`) — base `demons_and_related_identities`.
- [ ] **Asmodeus** (`PM_ASMODEUS`) — base `demons_and_related_identities`.
- [ ] **Demogorgon** (`PM_DEMOGORGON`) — base `demons_and_related_identities`.
- [ ] **Minion of Huhetotl** (`PM_MINION_OF_HUHETOTL`) — base `demons_and_related_identities`.
- [ ] **Nalzok** (`PM_NALZOK`) — base `demons_and_related_identities`.

### Supernatural beings / Personifications / Riders

- [ ] **Death** (`PM_DEATH`) — base `riders`.
- [ ] **Pestilence** (`PM_PESTILENCE`) — base `riders`.
- [ ] **Famine** (`PM_FAMINE`) — base `riders`.

### Supernatural beings / Small supernatural bodies / Imps and related beings

- [ ] **manes** (`PM_MANES`) — base `imps_and_related_beings`.
- [ ] **homunculus** (`PM_HOMUNCULUS`) — base `imps_and_related_beings`.
- [ ] **imp** (`PM_IMP`) — base `imps_and_related_beings`.
- [ ] **lemure** (`PM_LEMURE`) — base `imps_and_related_beings`.
- [ ] **quasit** (`PM_QUASIT`) — base `imps_and_related_beings`.
- [ ] **tengu** (`PM_TENGU`) — base `imps_and_related_beings`.

### Supernatural beings / Special identities / Djinni

- [ ] **djinni** (`PM_DJINNI`) — base `djinni`.

### Supernatural beings / Special identities / Mail Daemon

- [ ] **mail daemon** (`PM_MAIL_DAEMON`) — base `mail_daemon`; conditional: ifdef MAIL_STRUCTURES.

### Supernatural forms / Lycanthropes / Canids

- [ ] **werejackal** (`PM_WEREJACKAL`) — base `canid`.
- [ ] **werewolf** (`PM_WEREWOLF`) — base `wolf`.

### Supernatural forms / Lycanthropes / Humans and special identities

- [ ] **wererat** (`PM_HUMAN_WERERAT`) — base `humans_and_special_identities`.
- [ ] **werejackal** (`PM_HUMAN_WEREJACKAL`) — base `humans_and_special_identities`.
- [ ] **werewolf** (`PM_HUMAN_WEREWOLF`) — base `humans_and_special_identities`.

### Supernatural forms / Lycanthropes / Rodents

- [ ] **wererat** (`PM_WERERAT`) — base `wererat`.

### Undead / Ancestry plus state / Mummies

- [x] **kobold mummy** (`PM_KOBOLD_MUMMY`) — base `kobold_humanoid`; reuse kobold. [FBX](Art/CreatureInterpretations/kobold_mummy.fbx), [batch 14 evidence](Docs/CreatureBatch14.md).
- [x] **gnome mummy** (`PM_GNOME_MUMMY`) — base `gnome_humanoid`; reuse gnome. [FBX](Art/CreatureInterpretations/gnome_mummy.fbx), [batch 15 evidence and forms](Docs/CreatureBatch15.md).
- [x] **orc mummy** (`PM_ORC_MUMMY`) — base `orc_humanoid`; exact saved upright orc anatomy, fitted linen and shared sex appearance. [FBX](Art/CreatureInterpretations/orc_mummy.fbx), [batch 21 evidence](Docs/CreatureBatch21.md).
- [x] **dwarf mummy** (`PM_DWARF_MUMMY`) — base `dwarf_humanoid`; exact saved dwarf ancestry, fitted linen and shared sex appearance. [FBX](Art/CreatureInterpretations/dwarf_mummy.fbx), [batch 17 evidence](Docs/CreatureBatch17.md).
- [ ] **elf mummy** (`PM_ELF_MUMMY`) — base `elf_humanoid`; reuse elf.
- [ ] **human mummy** (`PM_HUMAN_MUMMY`) — base `human_humanoid`; reuse human.
- [ ] **ettin mummy** (`PM_ETTIN_MUMMY`) — base `ettin_humanoid`; reuse ettin.
- [ ] **giant mummy** (`PM_GIANT_MUMMY`) — base `giant_humanoid`; reuse giant.

### Undead / Ancestry plus state / Zombies

- [x] **kobold zombie** (`PM_KOBOLD_ZOMBIE`) — base `kobold_humanoid`; reuse kobold. [FBX](Art/CreatureInterpretations/kobold_zombie.fbx), [batch 14 evidence](Docs/CreatureBatch14.md).
- [x] **gnome zombie** (`PM_GNOME_ZOMBIE`) — base `gnome_humanoid`; reuse gnome. [FBX](Art/CreatureInterpretations/gnome_zombie.fbx), [batch 15 evidence and forms](Docs/CreatureBatch15.md).
- [x] **orc zombie** (`PM_ORC_ZOMBIE`) — base `orc_humanoid`; exact saved upright orc anatomy, source undead paint and shared sex appearance. [FBX](Art/CreatureInterpretations/orc_zombie.fbx), [batch 21 evidence](Docs/CreatureBatch21.md).
- [x] **dwarf zombie** (`PM_DWARF_ZOMBIE`) — base `dwarf_humanoid`; exact saved dwarf anatomy/costume, green skin and shared sex appearance. [FBX](Art/CreatureInterpretations/dwarf_zombie.fbx), [batch 17 evidence](Docs/CreatureBatch17.md).
- [ ] **elf zombie** (`PM_ELF_ZOMBIE`) — base `elf_humanoid`; reuse elf.
- [ ] **human zombie** (`PM_HUMAN_ZOMBIE`) — base `human_humanoid`; reuse human.
- [ ] **ettin zombie** (`PM_ETTIN_ZOMBIE`) — base `ettin_humanoid`; reuse ettin.
- [ ] **ghoul** (`PM_GHOUL`) — base `ghoul_humanoid`; reuse ghoul.
- [ ] **giant zombie** (`PM_GIANT_ZOMBIE`) — base `giant_humanoid`; reuse giant.
- [ ] **skeleton** (`PM_SKELETON`) — base `skeleton_humanoid`; reuse skeleton.

### Undead / Humanoids and alternate forms / Vampires

- [ ] **vampire** (`PM_VAMPIRE`) — base `vampires`.
- [ ] **vampire leader** (`PM_VAMPIRE_LEADER`) — base `vampires`; aliases: vampire lord, vampire lady.
- [ ] **vampire mage** (`PM_VAMPIRE_MAGE`) — base `vampires`; conditional: if 0.
- [ ] **Vlad the Impaler** (`PM_VLAD_THE_IMPALER`) — base `vampires`.

### Undead / Skeletal spellcasters / Liches

- [ ] **lich** (`PM_LICH`) — base `liches`.
- [ ] **demilich** (`PM_DEMILICH`) — base `liches`.
- [ ] **master lich** (`PM_MASTER_LICH`) — base `liches`.
- [ ] **arch-lich** (`PM_ARCH_LICH`) — base `liches`.

### Undead / Spectral bodies / Ghosts

- [ ] **ghost** (`PM_GHOST`) — base `ghosts`.
- [ ] **shade** (`PM_SHADE`) — base `ghosts`.

### Undead / Spectral bodies / Wraiths

- [ ] **barrow wight** (`PM_BARROW_WIGHT`) — base `wraiths`.
- [ ] **wraith** (`PM_WRAITH`) — base `wraiths`.
- [ ] **Nazgul** (`PM_NAZGUL`) — base `wraiths`.

## Player-role presentations

Existing tile-volume proxies are not anatomical drafts. Reuse compatible anatomy, but build fixed characters as in their icons; no detachable player clothing (explicit user correction). The role entry is also its linked `PM_*` identity in the source roster, so it is listed here only once. Race/ancestry remains an independent design axis; a full ancestry/role/sex asset matrix has not been scoped.

- [ ] **Archeologist** (`PM_ARCHEOLOGIST`) — fixed icon appearance; validate Archeologist (male), Archeologist (female).
- [ ] **Barbarian** (`PM_BARBARIAN`) — fixed icon appearance; validate Barbarian (male), Barbarian (female). **Partial:** human male form generated and verified; female remains unrequested/unmodelled. [Human player artifacts and checks](Docs/HumanPlayers.md).
- [ ] **Cave Dweller** (`PM_CAVE_DWELLER`) — fixed icon appearance; validate Caveman (male), Cavewoman (female).
- [ ] **Healer** (`PM_HEALER`) — fixed icon appearance; validate Healer (male), Healer (female).
- [ ] **Knight** (`PM_KNIGHT`) — fixed icon appearance; validate Knight (male), Knight (female).
- [ ] **Monk** (`PM_MONK`) — fixed icon appearance; validate Monk (male), Monk (female).
- [ ] **Cleric** (`PM_CLERIC`) — fixed icon appearance; validate Priest (male), Priestess (female).
- [ ] **Rogue** (`PM_ROGUE`) — fixed icon appearance; validate Rogue (male), Rogue (female).
- [ ] **Ranger** (`PM_RANGER`) — fixed icon appearance; validate Ranger (male), Ranger (female).
- [x] **Samurai** (`PM_SAMURAI`) — distinct human male/female fixed characters, fitted uniform and faces; both legal starting-sex targets verified with native selection/fallback/F9/first-person tests. [Artifacts and evidence](Docs/SamuraiPlayers.md).
- [ ] **Tourist** (`PM_TOURIST`) — fixed icon appearance; validate Tourist (male), Tourist (female).
- [x] **Valkyrie** (`PM_VALKYRIE`) — fixed icon appearance; validate Valkyrie (female). Human female form generated and verified. Other ancestries retain proxies; no ancestry cross-product is claimed. [Human player artifacts and checks](Docs/HumanPlayers.md).
- [ ] **Wizard** (`PM_WIZARD`) — fixed icon appearance; validate Wizard (male), Wizard (female).

Valkyrie is female-only at character creation. The official male tile does not create a permitted male starting variant. Later transformations are outside these starting restrictions.

## Finish the existing drafts

Keep these separate from generation checkboxes. Nothing here is marked complete merely because a mesh exists.

- [x] Compare current paint, subtle fur texture, and texture plus sparse clumps on the little dog and housecat, using actual Blender/Unreal views and triangle counts. [Fur study](Docs/FurStudy.md).
- [ ] Review the fur-study variants and choose a coat treatment before extending it across compatible families; no individual hairs or polygon-heavy fur.

- [ ] Giant ant: refine body angle and leg spread against the source; review close and rear views.
- [ ] Little dog: refine head/chest proportions, coat transitions and curled tail.
- [ ] Goblin: refine crouch, arm spread and garment fit; keep equipment detachable.
- [ ] Jackal: refine rounded head/profile and coat markings; retain continuous back geometry.
- [ ] Fox: refine muzzle, coat transitions and brush silhouette against the tile.
- [ ] Gnome: refine neckline/belt fit, pose and axe visibility; keep rank modules detachable.
- [ ] Sewer rat: preserve the user-approved lean body, snout, whiskers, ears and palette; refine fur paint and source-colour accents at 16x16.
- [ ] Giant rat: preserve the larger lean frame and reduced haunches; refine fur paint without restoring the squat tile silhouette.
- [ ] Gnome ruler: refine inherited neckline, rank trim and axe visibility; preserve detachable crown and fitted belt.
- [ ] Kitten: refine eyelids, head/ear transitions and muzzle; preserve juvenile proportions and lean body.
- [ ] Housecat: refine coat brushwork, eye integration, whisker/paw readability and static adult pose.
- [ ] Large cat: refine eye/ear integration and coat detail while preserving the larger adult frame.
- [ ] Kobold family: refine anatomy, hood/garment transitions, hands/feet and paint; retain dog-like muzzles, source blue palette, pale painted ear tips and separate leader rank pieces. [Batch 13](Docs/CreatureBatch13.md).
- [ ] Kobold caster/undead states: refine caster cloth transitions, linen folds/ends and zombie colour accents/pose; animation is out of scope; effects remain optional. [Batch 14](Docs/CreatureBatch14.md).
- [ ] Gnome caster/undead states: refine neckline/belt transitions, linen folds/fray and zombie pose/paint; retain source-supported beardless female wizard/zombie forms, green caps and red undead eyes. [Batch 15](Docs/CreatureBatch15.md).
- [ ] Dwarf family: refine face/beard and cloth transitions, crown proportions and miniature paint; preserve shared sex appearances and separate rank pieces. Drafts are 154–157k triangles; LODs and runtime cost need review. [Batch 16](Docs/CreatureBatch16.md).
- [ ] Dwarf undead states: refine linen edges/folds, face/beard and zombie pose; preserve saved ancestry, blue caps, source palettes and shared sex appearances. Review LOD/runtime costs; animation is out of scope and effects remain optional. [Batch 17](Docs/CreatureBatch17.md).
- [ ] Orc family: refine goblin-derived face/clothing, upright orc sleeve transitions, helmet/held-item shapes and source-palette readability. Preserve saved goblin vertices, shared hill/Mordor anatomy and separate equipment. LOD/runtime review remains separate; animation is out of scope. [Batch 18](Docs/CreatureBatch18.md).
- [ ] Early-level trio: refine eye/cornea shading, newt toes/skin/pose and lichen lobe/paint transitions. Preserve hover clearance, curved iris, four-limbed amphibian anatomy and eyeless fungal thallus. LOD/runtime review remains separate; animation is out of scope and effects remain optional. [Batch 19](Docs/CreatureBatch19.md).
- [ ] Orc caster/rank states: refine shield/grip, cloth panels, helmet rim and face/cheek paint; preserve shared saved anatomy and source-specific modules. LOD/runtime review remains separate; animation is out of scope and effects remain optional. [Batch 20](Docs/CreatureBatch20.md).
- [ ] Orc undead states: refine linen edges/folds, orange cloth accent and zombie face/cloth transitions; preserve saved anatomy, pale headwear, red mummy eyes and green/cyan/orange zombie palette. Static poses remain intended; LOD/runtime review stays separate. [Batch 21](Docs/CreatureBatch21.md).
- [ ] Ant/beetle batch: refine shell/leg transitions, miniature surface paint and distant readability; preserve source-supported female ant forms and separate beetle anatomy. Static pose is intended; LOD/runtime costs remain separate. [Batch 22](Docs/CreatureBatch22.md).
- [ ] Shopkeeper: refine face/neckline and tailored jacket/hip transitions, paint and LOD/runtime costs; preserve shared official sex appearance. Altars: refine stone/red-pigment and ray-inlay treatment; five displayed variants are separate from creature counts. [Special batch 2](Docs/SpecialBatch2.md).
- [ ] Winged insects: refine wing roots/veins, bee thorax texture, leg/stinger and xan proboscis/eye details; preserve independent queen proportions and separate xan body. Static flight is intended; LOD/runtime costs remain separate. [Batch 23](Docs/CreatureBatch23.md).
- [ ] Arachnids: refine leg/root/joint transitions, eye/fang details, scorpion plates/tail joints and paint; preserve eight walking legs, separate pedipalps/pincers, source palettes and independent spider dimensions. Review tiny readability and LOD/runtime costs. [Batch 24](Docs/CreatureBatch24.md).
- [ ] Reptiles: refine limb roots, scale paint, mouth/eye integration, toe-pad separation and tiny readability; reduce dense draft topology with reviewed LODs. Preserve distinct gecko/iguana/lizard anatomy and source colours. [Batch 25](Docs/CreatureBatch25.md).
- [ ] Snakes: refine head/neck transitions, eye seating, ventral scutes and close scale paint; review dark-body contrast and LODs. Preserve limbless anatomy, source palettes and independent heads/girth/coils. [Batch 26](Docs/CreatureBatch26.md).
- [ ] Advanced snakes: refine constrictor coil clearance, head/mouth/eye seating, viper pit marks and cobra hood transition; preserve source colours, native display boundary and three independent body plans. Review scale paint and LODs. [Batch 27](Docs/CreatureBatch27.md).
- [ ] Establish a reviewed finish target for one creature before calling any draft production-ready.
- Static models are the final presentation target; family rigs, skinning and character/object animation are out of scope.
- [ ] Evaluate optional brief action effects, especially wand lightning, without changing NetHack turns or requiring character animation.
- [ ] Review materials/texture detail, overview/room/close/eye-level readability, LODs and runtime cost.
- [ ] Review equipment visibility rules against displayed information before dynamic equipment is introduced.

## Other asset categories to inventory separately

This is complete for the current creature source catalogue, not for all game artwork. The following still need their own source-derived rosters and completion criteria; existing study meshes and tile proxies do not automatically finish them.

- [x] Objects/items: inventory the official object tiles and source identities, including unidentified appearances. [Object checklist](object-backlog.md): 440 named types (439 unconditional + conditional mail), 463 source appearance slots and 33 current artifact overlays. [Source inventory](Art/ObjectCatalogue/Inventory.md), [art direction](Docs/ObjectArtDirection.md). This completes inventory work, not asset generation.
- [ ] Terrain/features: inventory doors, stairs, traps, fountains and branch-specific architecture/materials.
- [ ] Effects: inventory beams, explosions, spell/attack visuals and other displayed effects.
- [ ] Player ancestry modules: scope the compatible body/role combinations before expanding the roster.


## Object drafts (separate from the 394 creature/player identities)

Four selected object presentations are generated and verified. The complete
source list and future work now live in [object-backlog.md](object-backlog.md)
and [Art/ObjectCatalogue](Art/ObjectCatalogue/Inventory.md). Object progress stays
separate from creature percentages. User direction: beautiful, distinctive loot;
creative craftsmanship and clear physical differences, with native unknown
appearances preserved. [Art direction](Docs/ObjectArtDirection.md).
[Batch 1](Docs/ObjectBatch1.md), [generic corpse](Docs/SpecialBatch1.md).

- [x] **large box** (`LARGE_BOX`) — [painted FBX](Art/ObjectInterpretations/large_box.fbx), flat plank lid; native display, normal/memory materials and live checks passed.
- [x] **chest** (`CHEST`) — [painted FBX](Art/ObjectInterpretations/chest.fbx), rounded lid; native display, normal/memory materials and live checks passed.
- [x] **gold piece** (`GOLD_PIECE`) — [painted FBX](Art/ObjectInterpretations/gold_piece.fbx), representative coin cluster; native normal/pile-top display and live checks passed; no quantity claim.

- [x] **generic corpse** (`CORPSE`) — [painted FBX](Art/ObjectInterpretations/corpse.fbx); one generic remains asset, no species/freshness/edibility claim. Native displayed corpses and memory/style checks passed. [Evidence](Docs/SpecialBatch1.md).

## Terrain feature drafts (separate inventory)

- [x] **fountain** (`FOUNTAIN` / `S_fountain`) — [painted FBX](Art/EnvironmentInterpretations/fountain.fbx), carved pale stone, static blue water, normal/memory materials and displayed-terrain checks. Sinks remain separate. [Evidence](Docs/SpecialBatch1.md).

Object finishing remains separate: static carried representations,
quantity-aware coin layouts, wood/metal refinement, LODs and performance.


General presentation fallback: [official tile cards](Docs/TileFallback.md) now
cover unsupported entities while individual models are missing. This does not
check off any creature/object modelling item or change the source-ID inventory.


- [x] **altar** (`ALTAR` / native altar glyph family) — five verified displayed
  forms: unaligned, chaotic, neutral, lawful and special other/high altar.
  Shared complete stone construction, source palettes, visible/memory materials,
  native glyph/covered-terrain and F9 checks. “Opposed to player” is not an
  additional altar type. [Evidence](Docs/SpecialBatch2.md).

Terrain draft coverage now comprises two feature identities / six forms:
fountain and five altar variants. Complete terrain inventory remains pending.

Batch 28 finishing: refine primate face/brow/mouth and digit seating, coat flow, compact source-pose readability and LOD/runtime costs. Static drafts are verified; no animation is planned. See Docs/CreatureBatch28.md.

Batch 29 finishing: hairy-biped faces/coat and owlbear shoulder/hip transitions, facial discs, beak/claws and runtime/LOD costs. See Docs/CreatureBatch29.md.

Batch 30 finishing: lobe continuity and silhouettes, source palette/inclusion placement, gel material and LOD/runtime costs. See Docs/CreatureBatch30.md.

Batch 31 finishing: fold-root transitions, silhouette/source palette balance, spot distribution and LOD/runtime costs. See Docs/CreatureBatch31.md.

Batch 32 finishing: body transitions, eye seating, source palette/shape balance, dark readability and LOD/runtime costs. Brown/black pudding eyes follow explicit user tile interpretation; preserve them despite native NOEYES. See Docs/CreatureBatch32.md.

Samurai finishing: skin/cloth/hair and shoulder/hip refinement, dark hair/readability and LOD/runtime costs. Both forms share costume identity but female proportions/ponytail intentionally differ despite identical source tiles (user direction). See Docs/SamuraiPlayers.md.

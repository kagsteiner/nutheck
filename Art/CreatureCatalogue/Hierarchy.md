# Creature hierarchy and modelling catalogue

394 source declarations. See [creatures.json](creatures.json) for full traits, aliases, source locations and encyclopedia references; [creatures.csv](creatures.csv) for filtering.

This is a modelling taxonomy, not biological phylogeny. Unresolved source classes are explicit review queues. Conditional declarations and display auxiliaries are included; this is not a claim about compiled availability. All reuse recipes are proposals. Giant ant, little dog, goblin, jackal, fox, gnome, sewer rat, giant rat, gnome ruler, kitten, housecat, large cat, wolf, winter wolf cub, winter wolf, dog, large dog, dingo, coyote, warg, rabid rat, bat, giant bat, vampire bat, jaguar, lynx, panther, tiger, hell hound pup, hell hound, pony, horse, warhorse, white unicorn, gray unicorn, black unicorn, kobold, large kobold, kobold leader, kobold shaman, kobold mummy, kobold zombie, gnomish wizard, gnome mummy, gnome zombie, dwarf, dwarf leader, dwarf ruler, dwarf mummy, dwarf zombie, hobgoblin, hill orc, Mordor orc, floating eye, newt, lichen, Uruk-hai, orc shaman, orc-captain, grid bug, orc mummy, orc zombie, soldier ant, fire ant, giant beetle, shopkeeper, killer bee, queen bee, xan, cave spider, giant spider, scorpion, gecko, iguana, lizard, garter snake, snake, water moccasin, python, pit viper, cobra, Oracle, plains centaur, forest centaur, mountain centaur, monkey, ape, carnivorous ape, yeti, sasquatch, owlbear, acid blob, quivering blob, gelatinous cube, blue jelly, spotted jelly, ochre jelly, gray ooze, brown pudding and black pudding have static anatomical drafts. Catalogue generation itself never generates meshes.

Descriptions summarize native metadata. Source size is abstract, ASCII colour is not skin colour, and listed attacks are capabilities rather than current inventory. Canonical neutral names retain gendered aliases (for example gnome ruler = gnome king/queen).

## Player

Base class **Player** → role subclass → permitted starting-sex subclass. These are presentation/role classes, not biological species. Race/ancestry remains an independent axis. Rules come from `src/role.c` allow masks, not tile availability. See [players.json](players.json) or [players.csv](players.csv) for this branch alone.

**Valkyrie permits only female starting characters.** A male Valkyrie tile exists in the official artwork but does not make that a permitted starting choice. This hierarchy does not constrain later sex changes, polymorph or monster appearances.

### Player / Archeologist

Explorer and scholar; reusable expedition clothing and tool accessories. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:31`; linked creature: `PM_ARCHEOLOGIST`.

- **Archeologist — male** (`PLAYER_ROLE_ARCHEOLOGIST_MALE`): Male starting Archeologist; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Archeologist — female** (`PLAYER_ROLE_ARCHEOLOGIST_FEMALE`): Female starting Archeologist; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Barbarian

Martial adventurer; distinct muscular proportions and fixed icon-derived appearance. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:72`; linked creature: `PM_BARBARIAN`.

- **Barbarian — male** (`PLAYER_ROLE_BARBARIAN_MALE`): Male starting Barbarian; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Barbarian — female** (`PLAYER_ROLE_BARBARIAN_FEMALE`): Female starting Barbarian; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Cave Dweller

Prehistoric adventurer; shared body with primitive clothing and tool modules. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:113`; linked creature: `PM_CAVE_DWELLER`.

- **Caveman — male** (`PLAYER_ROLE_CAVE_DWELLER_MALE`): Male starting Caveman; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Cavewoman — female** (`PLAYER_ROLE_CAVE_DWELLER_FEMALE`): Female starting Cavewoman; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Healer

Medical adventurer; fixed icon-derived medical role appearance. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:154`; linked creature: `PM_HEALER`.

- **Healer — male** (`PLAYER_ROLE_HEALER_MALE`): Male starting Healer; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Healer — female** (`PLAYER_ROLE_HEALER_FEMALE`): Female starting Healer; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Knight

Armoured warrior; fixed icon-derived armour appearance on a compatible body. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:194`; linked creature: `PM_KNIGHT`.

- **Knight — male** (`PLAYER_ROLE_KNIGHT_MALE`): Male starting Knight; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Knight — female** (`PLAYER_ROLE_KNIGHT_FEMALE`): Female starting Knight; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Monk

Unarmed martial artist; robes, exposed hands and martial movement requirements. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:234`; linked creature: `PM_MONK`.

- **Monk — male** (`PLAYER_ROLE_MONK_MALE`): Male starting Monk; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Monk — female** (`PLAYER_ROLE_MONK_FEMALE`): Female starting Monk; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Cleric

Religious adventurer; fixed icon-derived vestments and religious appearance. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:275`; linked creature: `PM_CLERIC`.

- **Priest — male** (`PLAYER_ROLE_CLERIC_MALE`): Male starting Priest; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Priestess — female** (`PLAYER_ROLE_CLERIC_FEMALE`): Female starting Priestess; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Rogue

Stealth adventurer; fixed icon-derived light clothing appearance. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:318`; linked creature: `PM_ROGUE`.

- **Rogue — male** (`PLAYER_ROLE_ROGUE_MALE`): Male starting Rogue; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Rogue — female** (`PLAYER_ROLE_ROGUE_FEMALE`): Female starting Rogue; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Ranger

Wilderness adventurer; fixed icon-derived outdoor clothing appearance. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:358`; linked creature: `PM_RANGER`.

- **Ranger — male** (`PLAYER_ROLE_RANGER_MALE`): Male starting Ranger; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Ranger — female** (`PLAYER_ROLE_RANGER_FEMALE`): Female starting Ranger; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Samurai

Martial adventurer; distinct armour/clothing silhouette and weapon modules. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:413`; linked creature: `PM_SAMURAI`.

- **Samurai — male** (`PLAYER_ROLE_SAMURAI_MALE`): Male starting Samurai; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Samurai — female** (`PLAYER_ROLE_SAMURAI_FEMALE`): Female starting Samurai; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Tourist

Travelling adventurer; distinctive travel clothing and accessory modules. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:453`; linked creature: `PM_TOURIST`.

- **Tourist — male** (`PLAYER_ROLE_TOURIST_MALE`): Male starting Tourist; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Tourist — female** (`PLAYER_ROLE_TOURIST_FEMALE`): Female starting Tourist; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Valkyrie

Warrior role; female-only at initial character selection in this source version. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:493`; linked creature: `PM_VALKYRIE`.

- **Valkyrie — female** (`PLAYER_ROLE_VALKYRIE_FEMALE`): Female starting Valkyrie; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

### Player / Wizard

Arcane adventurer; fixed icon-derived robe silhouette. Visual modules are proposals, not live inventory facts.

Source: `src/role.c:533`; linked creature: `PM_WIZARD`.

- **Wizard — male** (`PLAYER_ROLE_WIZARD_MALE`): Male starting Wizard; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.
- **Wizard — female** (`PLAYER_ROLE_WIZARD_FEMALE`): Female starting Wizard; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.

## Amorphous life / Disguised bodies / Mimics

- **small mimic** (`PM_SMALL_MIMIC`): Mimics; medium source size; base level 7, difficulty 8. Carnivorous. Attacks: claw/physical.
  - Model: `mimics`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **large mimic** (`PM_LARGE_MIMIC`): Mimics; large source size; base level 8, difficulty 9. Carnivorous. Attacks: claw/stck.
  - Model: `mimics`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **giant mimic** (`PM_GIANT_MIMIC`): Mimics; large source size; base level 9, difficulty 11. Carnivorous. Attacks: claw/stck, claw/stck.
  - Model: `mimics`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Amorphous life / Soft bodies / Blobs

- **acid blob** (`PM_ACID_BLOB`): Blobs; tiny source size; base level 1, difficulty 2. Attacks: passive contact/acid.
  - Model: `blobs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **quivering blob** (`PM_QUIVERING_BLOB`): Blobs; small source size; base level 5, difficulty 6. Attacks: touch/physical.
  - Model: `blobs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **gelatinous cube** (`PM_GELATINOUS_CUBE`): Blobs; large source size; base level 6, difficulty 8. Omnivorous. Attacks: touch/plys, passive contact/plys.
  - Model: `blobs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Amorphous life / Soft bodies / Jellies

- **blue jelly** (`PM_BLUE_JELLY`): Jellies; medium source size; base level 4, difficulty 5. Attacks: passive contact/cold.
  - Model: `jellies`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **spotted jelly** (`PM_SPOTTED_JELLY`): Jellies; medium source size; base level 5, difficulty 6. Attacks: passive contact/acid.
  - Model: `jellies`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **ochre jelly** (`PM_OCHRE_JELLY`): Jellies; medium source size; base level 6, difficulty 8. Attacks: engulf/acid, passive contact/acid.
  - Model: `jellies`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Amorphous life / Soft bodies / Puddings and oozes

- **gray ooze** (`PM_GRAY_OOZE`): Puddings and oozes; medium source size; base level 3, difficulty 4. Omnivorous. Attacks: bite/rust.
  - Model: `puddings_and_oozes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **brown pudding** (`PM_BROWN_PUDDING`): Puddings and oozes; medium source size; base level 5, difficulty 6. Omnivorous. Attacks: bite/dcay.
  - Model: `puddings_and_oozes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **green slime** (`PM_GREEN_SLIME`): Puddings and oozes; large source size; base level 6, difficulty 8. Omnivorous. Attacks: touch/slim, passive contact/slim.
  - Model: `puddings_and_oozes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **black pudding** (`PM_BLACK_PUDDING`): Puddings and oozes; large source size; base level 10, difficulty 12. Omnivorous. Attacks: bite/corr, passive contact/corr.
  - Model: `puddings_and_oozes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Aquatic bodies / Aquatic animals

- **giant eel** (`PM_GIANT_EEL`): Aquatic animals; huge source size; base level 5, difficulty 7. Swims, amphibious, carnivorous. Attacks: bite/physical, touch/constriction.
  - Model: `aquatic_animals`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **electric eel** (`PM_ELECTRIC_EEL`): Aquatic animals; huge source size; base level 7, difficulty 10. Swims, amphibious, carnivorous. Attacks: bite/electricity, touch/constriction.
  - Model: `aquatic_animals`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Animals / Aquatic bodies / Cephalopods

- **kraken** (`PM_KRAKEN`): Cephalopods; huge source size; base level 20, difficulty 22. Swims, amphibious, no grasping hands, carnivorous. Attacks: claw/physical, claw/physical, hugs/constriction, bite/physical.
  - Model: `cephalopods`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Aquatic bodies / Fish

- **piranha** (`PM_PIRANHA`): Fish; small source size; base level 5, difficulty 7. Swims, amphibious, carnivorous. Attacks: bite/physical, bite/physical.
  - Model: `fish`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Aquatic bodies / Jellyfish

- **jellyfish** (`PM_JELLYFISH`): Jellyfish; small source size; base level 3, difficulty 5. Swims, amphibious. Attacks: sting/poison.
  - Model: `jellyfish`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Aquatic bodies / Sharks

- **shark** (`PM_SHARK`): Sharks; large source size; base level 7, difficulty 9. Swims, amphibious, carnivorous. Attacks: bite/physical.
  - Model: `sharks`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Arthropods / Ants

- **giant ant** (`PM_GIANT_ANT`): Ants; tiny source size; base level 2, difficulty 4. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `ants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **soldier ant** (`PM_SOLDIER_ANT`): Ants; tiny source size; base level 3, difficulty 7. No grasping hands, carnivorous. Attacks: bite/physical, sting/poison.
  - Model: `ants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **fire ant** (`PM_FIRE_ANT`): Ants; tiny source size; base level 3, difficulty 6. No grasping hands, carnivorous. Attacks: bite/physical, bite/fire.
  - Model: `ants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Arthropods / Arachnids

- **centipede** (`PM_CENTIPEDE`): Arachnids; tiny source size; base level 2, difficulty 4. No grasping hands, carnivorous. Attacks: bite/poison.
  - Model: `arachnids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Scorpius** (`PM_SCORPIUS`): Arachnids; human source size; base level 15, difficulty 17. No grasping hands, carnivorous. Attacks: claw/physical, claw/samu, sting/dise.
  - Model: `arachnids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Arthropods / Bees

- **killer bee** (`PM_KILLER_BEE`): Bees; tiny source size; base level 1, difficulty 6. Flies, no grasping hands. Attacks: sting/poison.
  - Model: `bees`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **queen bee** (`PM_QUEEN_BEE`): Bees; tiny source size; base level 9, difficulty 12. Flies, no grasping hands. Attacks: sting/poison.
  - Model: `bees`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Arthropods / Beetles

- **giant beetle** (`PM_GIANT_BEETLE`): Beetles; large source size; base level 5, difficulty 6. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `beetles`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Arthropods / Flying insects

- **grid bug** (`PM_GRID_BUG`): Flying insects; tiny source size; base level 0, difficulty 1. No grasping hands. Attacks: bite/electricity.
  - Model: `flying_insects`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **xan** (`PM_XAN`): Flying insects; tiny source size; base level 7, difficulty 9. Flies, no grasping hands. Attacks: sting/legs.
  - Model: `flying_insects`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Arthropods / Scorpions

- **scorpion** (`PM_SCORPION`): Scorpions; small source size; base level 5, difficulty 8. No grasping hands, carnivorous. Attacks: claw/physical, claw/physical, sting/poison.
  - Model: `scorpions`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Arthropods / Spiders

- **cave spider** (`PM_CAVE_SPIDER`): Spiders; tiny source size; base level 1, difficulty 3. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `spiders`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **giant spider** (`PM_GIANT_SPIDER`): Spiders; large source size; base level 5, difficulty 7. No grasping hands, carnivorous. Attacks: bite/poison.
  - Model: `spiders`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Invertebrates / Worms

- **baby long worm** (`PM_BABY_LONG_WORM`): Worms; large source size; base level 5, difficulty 6. Carnivorous. Attacks: bite/physical.
  - Model: `worms`. Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby purple worm** (`PM_BABY_PURPLE_WORM`): Worms; large source size; base level 8, difficulty 9. Carnivorous. Attacks: bite/physical.
  - Model: `worms`. Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **long worm** (`PM_LONG_WORM`): Worms; gigantic source size; base level 9, difficulty 10. Carnivorous. Attacks: bite/physical.
  - Model: `worms`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **purple worm** (`PM_PURPLE_WORM`): Worms; gigantic source size; base level 15, difficulty 17. Carnivorous. Attacks: bite/physical, engulf/dgst.
  - Model: `worms`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Mammals / Bats

- **bat** (`PM_BAT`): Bats; tiny source size; base level 0, difficulty 2. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `bats`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **giant bat** (`PM_GIANT_BAT`): Bats; small source size; base level 2, difficulty 3. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `bats`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **raven** (`PM_RAVEN`): Bats; small source size; base level 4, difficulty 6. Flies, no grasping hands, carnivorous. Attacks: bite/physical, claw/blnd.
  - Model: `bats`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **vampire bat** (`PM_VAMPIRE_BAT`): Bats; small source size; base level 5, difficulty 7. Flies, no grasping hands, omnivorous. Attacks: bite/physical, bite/poison.
  - Model: `bats`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Mammals / Canids

- **jackal** (`PM_JACKAL`): Canids; small source size; base level 0, difficulty 1. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `canid`; parent: canid. Distinct ears, muzzle, leg proportions and tail; not a palette swap.
- **fox** (`PM_FOX`): Canids; small source size; base level 0, difficulty 1. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `canid`; parent: canid. Distinct ears, muzzle, leg proportions and tail; not a palette swap.
- **coyote** (`PM_COYOTE`): Canids; small source size; base level 1, difficulty 2. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `canid`; parent: canid. Distinct ears, muzzle, leg proportions and tail; not a palette swap.
- **little dog** (`PM_LITTLE_DOG`): Canids; small source size; base level 2, difficulty 3. No grasping hands, carnivorous, domestic. Attacks: bite/physical.
  - Model: `dog`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **dingo** (`PM_DINGO`): Canids; medium source size; base level 4, difficulty 5. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `canid`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **dog** (`PM_DOG`): Canids; medium source size; base level 4, difficulty 5. No grasping hands, carnivorous, domestic. Attacks: bite/physical.
  - Model: `dog`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **large dog** (`PM_LARGE_DOG`): Canids; medium source size; base level 6, difficulty 7. No grasping hands, carnivorous, domestic. Attacks: bite/physical.
  - Model: `dog`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **wolf** (`PM_WOLF`): Canids; medium source size; base level 5, difficulty 6. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `wolf`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **winter wolf cub** (`PM_WINTER_WOLF_CUB`): Canids; small source size; base level 5, difficulty 7. No grasping hands, carnivorous. Attacks: bite/physical, breath/cold.
  - Model: `wolf`; parent: winter wolf. White fur (art interpretation); preserve default-tile accents; Cold-breath attachment and attack animation required; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **warg** (`PM_WARG`): Canids; medium source size; base level 7, difficulty 8. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `canid`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **winter wolf** (`PM_WINTER_WOLF`): Canids; large source size; base level 7, difficulty 9. No grasping hands, carnivorous. Attacks: bite/physical, breath/cold.
  - Model: `wolf`; parent: wolf. White fur (art interpretation); preserve default-tile accents; Cold-breath attachment and attack animation required.
- **hell hound pup** (`PM_HELL_HOUND_PUP`): Canids; small source size; base level 7, difficulty 9. No grasping hands, carnivorous. Attacks: bite/physical, breath/fire.
  - Model: `canid`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **hell hound** (`PM_HELL_HOUND`): Canids; medium source size; base level 12, difficulty 14. No grasping hands, carnivorous. Attacks: bite/physical, breath/fire.
  - Model: `canid`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Cerberus** (`PM_CERBERUS`): Canids; large source size; base level 12, difficulty 14. No grasping hands, carnivorous. Attacks: bite/physical, bite/physical, bite/physical. **Conditional source entry.**
  - Model: `canid`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Mammals / Felids

- **kitten** (`PM_KITTEN`): Felids; small source size; base level 2, difficulty 3. No grasping hands, carnivorous, domestic. Attacks: bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **housecat** (`PM_HOUSECAT`): Felids; small source size; base level 4, difficulty 5. No grasping hands, carnivorous, domestic. Attacks: bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **jaguar** (`PM_JAGUAR`): Felids; large source size; base level 4, difficulty 6. No grasping hands, carnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **lynx** (`PM_LYNX`): Felids; small source size; base level 5, difficulty 7. No grasping hands, carnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **panther** (`PM_PANTHER`): Felids; large source size; base level 5, difficulty 7. No grasping hands, carnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **large cat** (`PM_LARGE_CAT`): Felids; small source size; base level 6, difficulty 7. No grasping hands, carnivorous, domestic. Attacks: bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **tiger** (`PM_TIGER`): Felids; large source size; base level 6, difficulty 8. No grasping hands, carnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **displacer beast** (`PM_DISPLACER_BEAST`): Felids; large source size; base level 12, difficulty 14. No grasping hands, carnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `felids`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Mammals / Primates

- **monkey** (`PM_MONKEY`): Primates; small source size; base level 2, difficulty 4. Humanoid body, omnivorous. Attacks: claw/sitm, bite/physical.
  - Model: `primates`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **ape** (`PM_APE`): Primates; large source size; base level 4, difficulty 6. Humanoid body, omnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `primates`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **carnivorous ape** (`PM_CARNIVOROUS_APE`): Primates; large source size; base level 6, difficulty 8. Humanoid body, carnivorous. Attacks: claw/physical, claw/physical, hugs/physical.
  - Model: `primates`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Mammals / Rodents

- **sewer rat** (`PM_SEWER_RAT`): Rodents; tiny source size; base level 0, difficulty 1. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `rat`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **giant rat** (`PM_GIANT_RAT`): Rodents; tiny source size; base level 1, difficulty 2. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `rat`; parent: sewer rat. Larger lean frame than sewer rat; user approved thinner torso/haunches over squat tile fidelity; retain rodent anatomy.
- **rabid rat** (`PM_RABID_RAT`): Rodents; tiny source size; base level 2, difficulty 4. No grasping hands, carnivorous. Attacks: bite/drco.
  - Model: `rat`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **rock mole** (`PM_ROCK_MOLE`): Rodents; small source size; base level 3, difficulty 4. No grasping hands. Attacks: bite/physical.
  - Model: `rock_mole`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **woodchuck** (`PM_WOODCHUCK`): Rodents; small source size; base level 3, difficulty 4. Swims, no grasping hands, herbivorous. Attacks: bite/physical.
  - Model: `woodchuck`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Reptiles / Snakes

- **garter snake** (`PM_GARTER_SNAKE`): Snakes; tiny source size; base level 1, difficulty 3. Swims, carnivorous. Attacks: bite/physical.
  - Model: `snakes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **snake** (`PM_SNAKE`): Snakes; small source size; base level 4, difficulty 6. Swims, carnivorous. Attacks: bite/poison.
  - Model: `snakes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **water moccasin** (`PM_WATER_MOCCASIN`): Snakes; small source size; base level 4, difficulty 7. Swims, carnivorous. Attacks: bite/poison.
  - Model: `snakes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **python** (`PM_PYTHON`): Snakes; large source size; base level 6, difficulty 8. Swims, carnivorous. Attacks: bite/physical, touch/physical, hugs/constriction, hugs/physical.
  - Model: `snakes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **pit viper** (`PM_PIT_VIPER`): Snakes; medium source size; base level 6, difficulty 9. Swims, carnivorous. Attacks: bite/poison, bite/poison.
  - Model: `snakes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **cobra** (`PM_COBRA`): Snakes; medium source size; base level 6, difficulty 10. Swims, carnivorous. Attacks: bite/poison, spit/blnd.
  - Model: `snakes`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Reptiles and amphibians / Crocodilians

- **baby crocodile** (`PM_BABY_CROCODILE`): Crocodilians; medium source size; base level 3, difficulty 4. Swims, amphibious, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `crocodilians`. Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **crocodile** (`PM_CROCODILE`): Crocodilians; large source size; base level 6, difficulty 7. Swims, amphibious, no grasping hands, carnivorous. Attacks: bite/physical, claw/physical.
  - Model: `crocodilians`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Reptiles and amphibians / Geckos

- **gecko** (`PM_GECKO`): Geckos; tiny source size; base level 1, difficulty 2. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `geckos`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals / Reptiles and amphibians / Mixed small reptiles

- **iguana** (`PM_IGUANA`): Mixed small reptiles; tiny source size; base level 2, difficulty 3. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `mixed_small_reptiles`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **lizard** (`PM_LIZARD`): Mixed small reptiles; tiny source size; base level 5, difficulty 6. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `mixed_small_reptiles`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **chameleon** (`PM_CHAMELEON`): Mixed small reptiles; tiny source size; base level 6, difficulty 7. No grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `mixed_small_reptiles`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **salamander** (`PM_SALAMANDER`): Mixed small reptiles; human source size; base level 8, difficulty 12. Humanoid body. Attacks: weapon/physical, touch/fire, hugs/physical, hugs/fire.
  - Model: `mixed_small_reptiles`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Animals / Reptiles and amphibians / Newts

- **newt** (`PM_NEWT`): Newts; tiny source size; base level 0, difficulty 1. Swims, amphibious, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `newts`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals and mythic beasts / Primate and hybrid bodies / Apes and hairy bipeds

- **yeti** (`PM_YETI`): Apes and hairy bipeds; large source size; base level 5, difficulty 7. Humanoid body, carnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `apes_and_hairy_bipeds`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **sasquatch** (`PM_SASQUATCH`): Apes and hairy bipeds; large source size; base level 7, difficulty 9. Humanoid body, omnivorous. Attacks: claw/physical, claw/physical, kick/physical.
  - Model: `apes_and_hairy_bipeds`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Animals and mythic beasts / Quadruped bodies / Large ungulate bodies

- **titanothere** (`PM_TITANOTHERE`): Large ungulate bodies; large source size; base level 12, difficulty 13. No grasping hands, herbivorous. Attacks: claw/physical.
  - Model: `large_ungulate_bodies`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **baluchitherium** (`PM_BALUCHITHERIUM`): Large ungulate bodies; large source size; base level 14, difficulty 15. No grasping hands, herbivorous. Attacks: claw/physical, claw/physical.
  - Model: `large_ungulate_bodies`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals and mythic beasts / Quadruped bodies / Mixed large quadrupeds

- **leocrotta** (`PM_LEOCROTTA`): Mixed large quadrupeds; large source size; base level 6, difficulty 8. No grasping hands, omnivorous. Attacks: claw/physical, bite/physical, claw/physical.
  - Model: `mixed_large_quadrupeds`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **wumpus** (`PM_WUMPUS`): Mixed large quadrupeds; large source size; base level 8, difficulty 9. No grasping hands, omnivorous. Attacks: bite/physical.
  - Model: `mixed_large_quadrupeds`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Animals and mythic beasts / Quadruped bodies / Proboscideans

- **mumak** (`PM_MUMAK`): Proboscideans; large source size; base level 5, difficulty 7. No grasping hands, herbivorous. Attacks: headbutt/physical, bite/physical.
  - Model: `proboscideans`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **mastodon** (`PM_MASTODON`): Proboscideans; large source size; base level 20, difficulty 22. No grasping hands, herbivorous. Attacks: headbutt/physical, headbutt/physical.
  - Model: `proboscideans`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Animals and mythic beasts / Quadruped bodies / Rothe

- **rothe** (`PM_ROTHE`): Rothe; large source size; base level 2, difficulty 4. No grasping hands, omnivorous. Attacks: claw/physical, bite/physical, bite/physical.
  - Model: `rothe`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Constructs / Material bodies / Golems

- **straw golem** (`PM_STRAW_GOLEM`): Golems; large source size; base level 3, difficulty 4. Humanoid body. Attacks: claw/physical, claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **paper golem** (`PM_PAPER_GOLEM`): Golems; large source size; base level 3, difficulty 4. Humanoid body. Attacks: claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **rope golem** (`PM_ROPE_GOLEM`): Golems; large source size; base level 4, difficulty 6. Humanoid body. Attacks: claw/physical, claw/physical, hugs/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **gold golem** (`PM_GOLD_GOLEM`): Golems; large source size; base level 5, difficulty 6. Humanoid body. Attacks: claw/physical, claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **leather golem** (`PM_LEATHER_GOLEM`): Golems; large source size; base level 6, difficulty 7. Humanoid body. Attacks: claw/physical, claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **wood golem** (`PM_WOOD_GOLEM`): Golems; large source size; base level 7, difficulty 8. Humanoid body. Attacks: claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **flesh golem** (`PM_FLESH_GOLEM`): Golems; large source size; base level 9, difficulty 10. Humanoid body. Attacks: claw/physical, claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **clay golem** (`PM_CLAY_GOLEM`): Golems; large source size; base level 11, difficulty 12. Humanoid body. Attacks: claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **stone golem** (`PM_STONE_GOLEM`): Golems; large source size; base level 14, difficulty 15. Humanoid body. Attacks: claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **glass golem** (`PM_GLASS_GOLEM`): Golems; large source size; base level 16, difficulty 18. Humanoid body. Attacks: claw/physical, claw/physical.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.
- **iron golem** (`PM_IRON_GOLEM`): Golems; large source size; base level 18, difficulty 22. Humanoid body. Attacks: weapon/physical, breath/poison.
  - Model: `golems`. Shared articulated plan only where suitable; material, silhouette and joints may require new geometry.

## Display auxiliaries / Body segments / Worm tails

- **long worm tail** (`PM_LONG_WORM_TAIL`): Worm tails; siz(0, 0, 0, 0) source size; base level 0, difficulty 1.
  - Model: `worm_tails`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Elemental manifestations / Elemental bodies / Elementals

- **stalker** (`PM_STALKER`): Elementals; large source size; base level 8, difficulty 9. Flies. Attacks: claw/physical.
  - Model: `elementals`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **air elemental** (`PM_AIR_ELEMENTAL`): Elementals; huge source size; base level 8, difficulty 10. Flies. Attacks: engulf/physical.
  - Model: `elementals`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **fire elemental** (`PM_FIRE_ELEMENTAL`): Elementals; huge source size; base level 8, difficulty 10. Flies. Attacks: claw/fire, passive contact/fire.
  - Model: `elementals`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **earth elemental** (`PM_EARTH_ELEMENTAL`): Elementals; huge source size; base level 8, difficulty 10. Attacks: claw/physical.
  - Model: `elementals`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **water elemental** (`PM_WATER_ELEMENTAL`): Elementals; huge source size; base level 8, difficulty 10. Swims, amphibious. Attacks: claw/physical.
  - Model: `elementals`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Elemental manifestations / Luminous bodies / Lights

- **yellow light** (`PM_YELLOW_LIGHT`): Lights; small source size; base level 3, difficulty 5. Flies. Attacks: explosion/blnd.
  - Model: `lights`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **black light** (`PM_BLACK_LIGHT`): Lights; small source size; base level 5, difficulty 7. Flies. Attacks: explosion/halu.
  - Model: `lights`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Elemental manifestations / Volume effects / Vortices

- **fog cloud** (`PM_FOG_CLOUD`): Vortices; huge source size; base level 3, difficulty 4. Flies. Attacks: engulf/physical.
  - Model: `vortices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **dust vortex** (`PM_DUST_VORTEX`): Vortices; huge source size; base level 4, difficulty 6. Flies. Attacks: engulf/blnd.
  - Model: `vortices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **ice vortex** (`PM_ICE_VORTEX`): Vortices; huge source size; base level 5, difficulty 7. Flies. Attacks: engulf/cold.
  - Model: `vortices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **energy vortex** (`PM_ENERGY_VORTEX`): Vortices; huge source size; base level 6, difficulty 9. Flies. Attacks: engulf/electricity, engulf/dren, passive contact/electricity.
  - Model: `vortices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **steam vortex** (`PM_STEAM_VORTEX`): Vortices; huge source size; base level 7, difficulty 9. Flies. Attacks: engulf/fire.
  - Model: `vortices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **fire vortex** (`PM_FIRE_VORTEX`): Vortices; huge source size; base level 8, difficulty 10. Flies. Attacks: engulf/fire, passive contact/fire.
  - Model: `vortices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Fungi / Floating spore bodies / Gas spores

- **gas spore** (`PM_GAS_SPORE`): Gas spores; small source size; base level 1, difficulty 2. Flies. Attacks: death explosion/physical.
  - Model: `gas_spores`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Fungi / Fungal bodies / Fungi and molds

- **lichen** (`PM_LICHEN`): Fungi and molds; small source size; base level 0, difficulty 1. Attacks: touch/stck.
  - Model: `fungi_and_molds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **brown mold** (`PM_BROWN_MOLD`): Fungi and molds; small source size; base level 1, difficulty 2. Attacks: passive contact/cold.
  - Model: `fungi_and_molds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **yellow mold** (`PM_YELLOW_MOLD`): Fungi and molds; small source size; base level 1, difficulty 2. Attacks: passive contact/stun.
  - Model: `fungi_and_molds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **green mold** (`PM_GREEN_MOLD`): Fungi and molds; small source size; base level 1, difficulty 2. Attacks: passive contact/acid.
  - Model: `fungi_and_molds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **red mold** (`PM_RED_MOLD`): Fungi and molds; small source size; base level 1, difficulty 2. Attacks: passive contact/fire.
  - Model: `fungi_and_molds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **shrieker** (`PM_SHRIEKER`): Fungi and molds; small source size; base level 3, difficulty 2.
  - Model: `fungi_and_molds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **violet fungus** (`PM_VIOLET_FUNGUS`): Fungi and molds; small source size; base level 3, difficulty 5. Attacks: touch/physical, touch/stck.
  - Model: `fungi_and_molds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Humanoids / Dwarves

- **dwarf** (`PM_DWARF`): Dwarves; human source size; base level 2, difficulty 4. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `dwarves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **dwarf leader** (`PM_DWARF_LEADER`): Dwarves; human source size; base level 4, difficulty 6. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `dwarves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **dwarf ruler** (`PM_DWARF_RULER`): Dwarves; human source size; base level 6, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `dwarves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Humanoids / Elves

- **elf** (`PM_ELF`): Elves; human source size; base level 0, difficulty 1. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Woodland-elf** (`PM_WOODLAND_ELF`): Elves; human source size; base level 4, difficulty 6. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Green-elf** (`PM_GREEN_ELF`): Elves; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Grey-elf** (`PM_GREY_ELF`): Elves; human source size; base level 6, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **elf-noble** (`PM_ELF_NOBLE`): Elves; human source size; base level 8, difficulty 11. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **elven monarch** (`PM_ELVEN_MONARCH`): Elves; human source size; base level 9, difficulty 11. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Earendil** (`PM_EARENDIL`): Elves; human source size; base level 20, difficulty 22. Humanoid body, omnivorous. Attacks: weapon/physical. **Conditional source entry.**
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Elwing** (`PM_ELWING`): Elves; human source size; base level 20, difficulty 22. Humanoid body, omnivorous. Attacks: weapon/physical. **Conditional source entry.**
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **High-elf** (`PM_HIGH_ELF`): Elves; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical, magic/clrc. **Conditional source entry.**
  - Model: `elves`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Humanoids / Hobbits

- **hobbit** (`PM_HOBBIT`): Hobbits; small source size; base level 1, difficulty 2. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `hobbits`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Humanoids / Humans and special identities

- **human** (`PM_HUMAN`): Humans and special identities; human source size; base level 0, difficulty 2. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **doppelganger** (`PM_DOPPELGANGER`): Humans and special identities; human source size; base level 9, difficulty 11. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **shopkeeper** (`PM_SHOPKEEPER`): Humans and special identities; human source size; base level 12, difficulty 15. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **guard** (`PM_GUARD`): Humans and special identities; human source size; base level 12, difficulty 14. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **prisoner** (`PM_PRISONER`): Humans and special identities; human source size; base level 12, difficulty 14. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Oracle** (`PM_ORACLE`): Humans and special identities; human source size; base level 12, difficulty 13. Humanoid body, omnivorous. Attacks: passive contact/magm.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **aligned cleric** (`PM_ALIGNED_CLERIC`): Humans and special identities; human source size; base level 12, difficulty 15. Humanoid body, omnivorous. Attacks: weapon/physical, kick/physical, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **high cleric** (`PM_HIGH_CLERIC`): Humans and special identities; human source size; base level 25, difficulty 30. Humanoid body, omnivorous. Attacks: weapon/physical, kick/physical, magic/clrc, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **soldier** (`PM_SOLDIER`): Humans and special identities; human source size; base level 6, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **sergeant** (`PM_SERGEANT`): Humans and special identities; human source size; base level 8, difficulty 10. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **nurse** (`PM_NURSE`): Humans and special identities; human source size; base level 11, difficulty 13. Humanoid body, omnivorous. Attacks: claw/heal.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **lieutenant** (`PM_LIEUTENANT`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **captain** (`PM_CAPTAIN`): Humans and special identities; human source size; base level 12, difficulty 14. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **watchman** (`PM_WATCHMAN`): Humans and special identities; human source size; base level 6, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **watch captain** (`PM_WATCH_CAPTAIN`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Medusa** (`PM_MEDUSA`): Humans and special identities; large source size; base level 20, difficulty 25. Flies, swims, amphibious, humanoid body, omnivorous. Attacks: weapon/physical, claw/physical, gaze/petrification, bite/poison.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Wizard of Yendor** (`PM_WIZARD_OF_YENDOR`): Humans and special identities; human source size; base level 30, difficulty 34. Flies, humanoid body, omnivorous. Attacks: claw/samu, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Croesus** (`PM_CROESUS`): Humans and special identities; human source size; base level 20, difficulty 22. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Charon** (`PM_CHARON`): Humans and special identities; human source size; base level 76, difficulty 38. Humanoid body. Attacks: weapon/physical, touch/plys. **Conditional source entry.**
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **archeologist** (`PM_ARCHEOLOGIST`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **barbarian** (`PM_BARBARIAN`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **cave dweller** (`PM_CAVE_DWELLER`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **healer** (`PM_HEALER`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **knight** (`PM_KNIGHT`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **monk** (`PM_MONK`): Humans and special identities; human source size; base level 10, difficulty 11. Humanoid body, herbivorous. Attacks: claw/physical, kick/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **cleric** (`PM_CLERIC`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **ranger** (`PM_RANGER`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **rogue** (`PM_ROGUE`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **samurai** (`PM_SAMURAI`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **tourist** (`PM_TOURIST`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **valkyrie** (`PM_VALKYRIE`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **wizard** (`PM_WIZARD`): Humans and special identities; human source size; base level 10, difficulty 12. Humanoid body, omnivorous. Attacks: weapon/physical, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Lord Carnarvon** (`PM_LORD_CARNARVON`): Humans and special identities; human source size; base level 20, difficulty 24. Humanoid body, omnivorous. Attacks: weapon/physical, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Pelias** (`PM_PELIAS`): Humans and special identities; human source size; base level 20, difficulty 24. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Shaman Karnov** (`PM_SHAMAN_KARNOV`): Humans and special identities; human source size; base level 20, difficulty 24. Humanoid body, omnivorous. Attacks: weapon/physical, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Hippocrates** (`PM_HIPPOCRATES`): Humans and special identities; human source size; base level 20, difficulty 26. Humanoid body, omnivorous. Attacks: weapon/physical, magic/clrc, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **King Arthur** (`PM_KING_ARTHUR`): Humans and special identities; human source size; base level 20, difficulty 24. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Grand Master** (`PM_GRAND_MASTER`): Humans and special identities; human source size; base level 25, difficulty 30. Humanoid body, herbivorous. Attacks: claw/physical, kick/physical, magic/clrc, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Arch Priest** (`PM_ARCH_PRIEST`): Humans and special identities; human source size; base level 25, difficulty 30. Humanoid body, omnivorous. Attacks: weapon/physical, kick/physical, magic/clrc, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Orion** (`PM_ORION`): Humans and special identities; huge source size; base level 20, difficulty 24. Swims, amphibious, humanoid body, omnivorous. Attacks: weapon/physical, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Master of Thieves** (`PM_MASTER_OF_THIEVES`): Humans and special identities; human source size; base level 20, difficulty 24. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical, claw/samu.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Lord Sato** (`PM_LORD_SATO`): Humans and special identities; human source size; base level 20, difficulty 24. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Twoflower** (`PM_TWOFLOWER`): Humans and special identities; human source size; base level 20, difficulty 22. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Norn** (`PM_NORN`): Humans and special identities; huge source size; base level 20, difficulty 24. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Neferet the Green** (`PM_NEFERET_THE_GREEN`): Humans and special identities; human source size; base level 20, difficulty 25. Humanoid body, omnivorous. Attacks: weapon/physical, magic/spel, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Thoth Amon** (`PM_THOTH_AMON`): Humans and special identities; human source size; base level 16, difficulty 22. Humanoid body, omnivorous. Attacks: weapon/physical, magic/spel, magic/spel, claw/samu.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Master Kaen** (`PM_MASTER_KAEN`): Humans and special identities; human source size; base level 25, difficulty 31. Humanoid body, herbivorous. Attacks: claw/physical, claw/physical, magic/clrc, claw/samu.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Master Assassin** (`PM_MASTER_ASSASSIN`): Humans and special identities; human source size; base level 15, difficulty 20. Humanoid body, omnivorous. Attacks: weapon/poison, weapon/physical, claw/samu.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Ashikaga Takauji** (`PM_ASHIKAGA_TAKAUJI`): Humans and special identities; human source size; base level 15, difficulty 19. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical, claw/samu.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Dark One** (`PM_DARK_ONE`): Humans and special identities; human source size; base level 15, difficulty 20. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical, claw/samu, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **student** (`PM_STUDENT`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **chieftain** (`PM_CHIEFTAIN`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **neanderthal** (`PM_NEANDERTHAL`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **attendant** (`PM_ATTENDANT`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **page** (`PM_PAGE`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **abbot** (`PM_ABBOT`): Humans and special identities; human source size; base level 5, difficulty 8. Humanoid body, herbivorous. Attacks: claw/physical, kick/stun, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **acolyte** (`PM_ACOLYTE`): Humans and special identities; human source size; base level 5, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical, magic/clrc.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **hunter** (`PM_HUNTER`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **thug** (`PM_THUG`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **ninja** (`PM_NINJA`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **roshi** (`PM_ROSHI`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **guide** (`PM_GUIDE`): Humans and special identities; human source size; base level 5, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **warrior** (`PM_WARRIOR`): Humans and special identities; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **apprentice** (`PM_APPRENTICE`): Humans and special identities; human source size; base level 5, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical, magic/spel.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Humanoid peoples / Humanoids / Keystone Kops

- **Keystone Kop** (`PM_KEYSTONE_KOP`): Keystone Kops; human source size; base level 1, difficulty 3. Humanoid body. Attacks: weapon/physical.
  - Model: `keystone_kops`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Kop Sergeant** (`PM_KOP_SERGEANT`): Keystone Kops; human source size; base level 2, difficulty 4. Humanoid body. Attacks: weapon/physical.
  - Model: `keystone_kops`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Kop Lieutenant** (`PM_KOP_LIEUTENANT`): Keystone Kops; human source size; base level 3, difficulty 5. Humanoid body. Attacks: weapon/physical.
  - Model: `keystone_kops`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Kop Kaptain** (`PM_KOP_KAPTAIN`): Keystone Kops; human source size; base level 4, difficulty 6. Humanoid body. Attacks: weapon/physical.
  - Model: `keystone_kops`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Humanoids / Mind flayers

- **mind flayer** (`PM_MIND_FLAYER`): Mind flayers; human source size; base level 9, difficulty 13. Flies, humanoid body, omnivorous. Attacks: weapon/physical, tent/drin, tent/drin, tent/drin.
  - Model: `mind_flayers`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **master mind flayer** (`PM_MASTER_MIND_FLAYER`): Mind flayers; human source size; base level 13, difficulty 19. Flies, humanoid body, omnivorous. Attacks: weapon/physical, tent/drin, tent/drin, tent/drin, tent/drin, tent/drin.
  - Model: `mind_flayers`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Humanoids / Mixed humanoids

- **bugbear** (`PM_BUGBEAR`): Mixed humanoids; large source size; base level 3, difficulty 5. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `mixed_humanoids`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Humanoid peoples / Humanoids / Orcs

- **goblin** (`PM_GOBLIN`): Orcs; small source size; base level 0, difficulty 1. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **hobgoblin** (`PM_HOBGOBLIN`): Orcs; human source size; base level 1, difficulty 3. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **orc** (`PM_ORC`): Orcs; human source size; base level 1, difficulty 3. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **hill orc** (`PM_HILL_ORC`): Orcs; human source size; base level 2, difficulty 4. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Mordor orc** (`PM_MORDOR_ORC`): Orcs; human source size; base level 3, difficulty 5. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Uruk-hai** (`PM_URUK_HAI`): Orcs; human source size; base level 3, difficulty 5. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **orc shaman** (`PM_ORC_SHAMAN`): Orcs; human source size; base level 3, difficulty 5. Humanoid body, omnivorous. Attacks: magic/spel.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **orc-captain** (`PM_ORC_CAPTAIN`): Orcs; human source size; base level 5, difficulty 7. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Goblin King** (`PM_GOBLIN_KING`): Orcs; human source size; base level 15, difficulty 18. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical, claw/samu. **Conditional source entry.**
  - Model: `orcs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Humanoids / Science specialists

- **quantum mechanic** (`PM_QUANTUM_MECHANIC`): Science specialists; human source size; base level 7, difficulty 9. Humanoid body, omnivorous. Attacks: claw/tlpt.
  - Model: `science_specialists`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **genetic engineer** (`PM_GENETIC_ENGINEER`): Science specialists; human source size; base level 12, difficulty 14. Humanoid body, omnivorous. Attacks: claw/poly.
  - Model: `science_specialists`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Large humanoids / Giants

- **giant** (`PM_GIANT`): Giants; huge source size; base level 6, difficulty 8. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **stone giant** (`PM_STONE_GIANT`): Giants; huge source size; base level 6, difficulty 8. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **hill giant** (`PM_HILL_GIANT`): Giants; huge source size; base level 8, difficulty 10. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **fire giant** (`PM_FIRE_GIANT`): Giants; huge source size; base level 9, difficulty 11. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **frost giant** (`PM_FROST_GIANT`): Giants; huge source size; base level 10, difficulty 13. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **ettin** (`PM_ETTIN`): Giants; huge source size; base level 10, difficulty 13. Humanoid body, carnivorous. Attacks: weapon/physical, weapon/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **storm giant** (`PM_STORM_GIANT`): Giants; huge source size; base level 16, difficulty 19. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **titan** (`PM_TITAN`): Giants; huge source size; base level 16, difficulty 20. Flies, humanoid body, omnivorous. Attacks: weapon/physical, magic/spel.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **minotaur** (`PM_MINOTAUR`): Giants; large source size; base level 15, difficulty 17. Humanoid body, carnivorous. Attacks: claw/physical, claw/physical, headbutt/physical.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Cyclops** (`PM_CYCLOPS`): Giants; huge source size; base level 18, difficulty 23. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical, claw/samu.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Lord Surtur** (`PM_LORD_SURTUR`): Giants; huge source size; base level 15, difficulty 19. Humanoid body, omnivorous. Attacks: weapon/physical, weapon/physical, claw/samu.
  - Model: `giants`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Large humanoids / Ogres

- **ogre** (`PM_OGRE`): Ogres; large source size; base level 5, difficulty 7. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `ogres`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **ogre leader** (`PM_OGRE_LEADER`): Ogres; large source size; base level 7, difficulty 9. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `ogres`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **ogre tyrant** (`PM_OGRE_TYRANT`): Ogres; large source size; base level 9, difficulty 11. Humanoid body, carnivorous. Attacks: weapon/physical.
  - Model: `ogres`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Large humanoids / Trolls

- **troll** (`PM_TROLL`): Trolls; large source size; base level 7, difficulty 9. Humanoid body, carnivorous. Attacks: weapon/physical, claw/physical, bite/physical.
  - Model: `trolls`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **ice troll** (`PM_ICE_TROLL`): Trolls; large source size; base level 9, difficulty 12. Humanoid body, carnivorous. Attacks: weapon/physical, claw/cold, bite/physical.
  - Model: `trolls`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **rock troll** (`PM_ROCK_TROLL`): Trolls; large source size; base level 9, difficulty 12. Humanoid body, carnivorous. Attacks: weapon/physical, claw/physical, bite/physical.
  - Model: `trolls`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **water troll** (`PM_WATER_TROLL`): Trolls; large source size; base level 11, difficulty 13. Swims, humanoid body, carnivorous. Attacks: weapon/physical, claw/physical, bite/physical.
  - Model: `trolls`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Olog-hai** (`PM_OLOG_HAI`): Trolls; large source size; base level 13, difficulty 16. Humanoid body, carnivorous. Attacks: weapon/physical, claw/physical, bite/physical.
  - Model: `trolls`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Small humanoids / Gnomes

- **gnome** (`PM_GNOME`): Gnomes; small source size; base level 1, difficulty 3. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `gnome`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **gnome leader** (`PM_GNOME_LEADER`): Gnomes; small source size; base level 3, difficulty 4. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `gnome`; parent: gnome. Rank/role clothing and equipment modules.
- **gnomish wizard** (`PM_GNOMISH_WIZARD`): Gnomes; small source size; base level 3, difficulty 5. Humanoid body, omnivorous. Attacks: magic/spel.
  - Model: `gnome`; parent: gnome. Rank/role clothing and equipment modules.
- **gnome ruler** (`PM_GNOME_RULER`): Gnomes; small source size; base level 5, difficulty 6. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `gnome`; parent: gnome. Detachable crown and rank clothing; crown is an art decision, not an inventory fact.

## Humanoid peoples / Small humanoids / Kobolds

- **kobold** (`PM_KOBOLD`): Kobolds; small source size; base level 0, difficulty 1. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `kobolds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **large kobold** (`PM_LARGE_KOBOLD`): Kobolds; small source size; base level 1, difficulty 2. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `kobolds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **kobold leader** (`PM_KOBOLD_LEADER`): Kobolds; small source size; base level 2, difficulty 3. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `kobolds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **kobold shaman** (`PM_KOBOLD_SHAMAN`): Kobolds; small source size; base level 2, difficulty 4. Humanoid body, omnivorous. Attacks: magic/spel.
  - Model: `kobolds`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Humanoid peoples / Small humanoids / Leprechauns

- **leprechaun** (`PM_LEPRECHAUN`): Leprechauns; tiny source size; base level 5, difficulty 4. Humanoid body. Attacks: claw/sgld.
  - Model: `leprechauns`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Avian reptile bodies / Cockatrices

- **chickatrice** (`PM_CHICKATRICE`): Cockatrices; tiny source size; base level 4, difficulty 7. No grasping hands, omnivorous. Attacks: bite/physical, touch/petrification, passive contact/petrification.
  - Model: `cockatrices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **cockatrice** (`PM_COCKATRICE`): Cockatrices; small source size; base level 5, difficulty 8. No grasping hands, omnivorous. Attacks: bite/physical, touch/petrification, passive contact/petrification.
  - Model: `cockatrices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **pyrolisk** (`PM_PYROLISK`): Cockatrices; small source size; base level 6, difficulty 8. No grasping hands, omnivorous. Attacks: gaze/fire, bite/physical.
  - Model: `cockatrices`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Composite bodies / Centaurs

- **plains centaur** (`PM_PLAINS_CENTAUR`): Centaurs; large source size; base level 4, difficulty 6. Humanoid body, omnivorous. Attacks: weapon/physical, kick/physical.
  - Model: `centaurs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **forest centaur** (`PM_FOREST_CENTAUR`): Centaurs; large source size; base level 5, difficulty 8. Humanoid body, omnivorous. Attacks: weapon/physical, kick/physical.
  - Model: `centaurs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **mountain centaur** (`PM_MOUNTAIN_CENTAUR`): Centaurs; large source size; base level 6, difficulty 9. Humanoid body, omnivorous. Attacks: weapon/physical, kick/physical, kick/physical.
  - Model: `centaurs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Composite bodies / Jabberwocks

- **jabberwock** (`PM_JABBERWOCK`): Jabberwocks; large source size; base level 15, difficulty 18. Flies, carnivorous. Attacks: bite/physical, bite/physical, claw/physical, claw/physical.
  - Model: `jabberwocks`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **vorpal jabberwock** (`PM_VORPAL_JABBERWOCK`): Jabberwocks; large source size; base level 20, difficulty 25. Flies, carnivorous. Attacks: bite/physical, bite/physical, claw/physical, claw/physical. **Conditional source entry.**
  - Model: `jabberwocks`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Composite bodies / Ki-rin

- **ki-rin** (`PM_KI_RIN`): Ki-rin; large source size; base level 16, difficulty 21. Flies, no grasping hands. Attacks: kick/physical, kick/physical, headbutt/physical, magic/spel.
  - Model: `ki-rin`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Composite bodies / Owlbears

- **owlbear** (`PM_OWLBEAR`): Owlbears; large source size; base level 5, difficulty 7. Humanoid body, carnivorous. Attacks: claw/physical, claw/physical, hugs/physical.
  - Model: `owlbears`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Composite bodies / Winged serpents

- **couatl** (`PM_COUATL`): Winged serpents; large source size; base level 8, difficulty 11. Flies, no grasping hands. Attacks: bite/poison, bite/physical, hugs/constriction.
  - Model: `winged_serpents`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Equine bodies / Equines

- **pony** (`PM_PONY`): Equines; medium source size; base level 3, difficulty 4. No grasping hands, herbivorous, domestic. Attacks: kick/physical, bite/physical.
  - Model: `equines`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **white unicorn** (`PM_WHITE_UNICORN`): Equines; large source size; base level 4, difficulty 6. No grasping hands, herbivorous. Attacks: headbutt/physical, kick/physical.
  - Model: `equines`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **gray unicorn** (`PM_GRAY_UNICORN`): Equines; large source size; base level 4, difficulty 6. No grasping hands, herbivorous. Attacks: headbutt/physical, kick/physical.
  - Model: `equines`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **black unicorn** (`PM_BLACK_UNICORN`): Equines; large source size; base level 4, difficulty 6. No grasping hands, herbivorous. Attacks: headbutt/physical, kick/physical.
  - Model: `equines`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **horse** (`PM_HORSE`): Equines; large source size; base level 5, difficulty 7. No grasping hands, herbivorous, domestic. Attacks: kick/physical, bite/physical.
  - Model: `equines`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **warhorse** (`PM_WARHORSE`): Equines; large source size; base level 7, difficulty 9. No grasping hands, herbivorous, domestic. Attacks: kick/physical, bite/physical.
  - Model: `equines`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Flattened ambush bodies / Trappers and lurkers

- **lurker above** (`PM_LURKER_ABOVE`): Trappers and lurkers; huge source size; base level 10, difficulty 12. Flies, carnivorous. Attacks: engulf/constriction, engulf/physical.
  - Model: `trappers_and_lurkers`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **trapper** (`PM_TRAPPER`): Trappers and lurkers; huge source size; base level 12, difficulty 14. Carnivorous. Attacks: engulf/constriction, engulf/physical.
  - Model: `trappers_and_lurkers`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Floating bodies / Eyes and spheres

- **floating eye** (`PM_FLOATING_EYE`): Eyes and spheres; small source size; base level 2, difficulty 3. Flies, amphibious. Attacks: passive contact/plys.
  - Model: `eyes_and_spheres`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **freezing sphere** (`PM_FREEZING_SPHERE`): Eyes and spheres; small source size; base level 6, difficulty 9. Flies. Attacks: explosion/cold.
  - Model: `eyes_and_spheres`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **flaming sphere** (`PM_FLAMING_SPHERE`): Eyes and spheres; small source size; base level 6, difficulty 9. Flies. Attacks: explosion/fire.
  - Model: `eyes_and_spheres`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **shocking sphere** (`PM_SHOCKING_SPHERE`): Eyes and spheres; small source size; base level 6, difficulty 10. Flies. Attacks: explosion/electricity.
  - Model: `eyes_and_spheres`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **beholder** (`PM_BEHOLDER`): Eyes and spheres; small source size; base level 6, difficulty 13. Flies. Attacks: gaze/slow, gaze/sleep, gaze/disn, gaze/petrification, gaze/cncl, bite/physical. **Conditional source entry.**
  - Model: `eyes_and_spheres`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Mythic bodies / Humanoids / Nymphs

- **wood nymph** (`PM_WOOD_NYMPH`): Nymphs; human source size; base level 3, difficulty 5. Humanoid body. Attacks: claw/sitm, claw/sedu.
  - Model: `nymphs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **water nymph** (`PM_WATER_NYMPH`): Nymphs; human source size; base level 3, difficulty 5. Swims, humanoid body. Attacks: claw/sitm, claw/sedu.
  - Model: `nymphs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **mountain nymph** (`PM_MOUNTAIN_NYMPH`): Nymphs; human source size; base level 3, difficulty 5. Humanoid body. Attacks: claw/sitm, claw/sedu.
  - Model: `nymphs`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Insectoid bipeds / Umber hulks

- **umber hulk** (`PM_UMBER_HULK`): Umber hulks; large source size; base level 9, difficulty 12. Carnivorous. Attacks: claw/physical, claw/physical, bite/physical, gaze/conf.
  - Model: `umber_hulks`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Large bipedal beasts / Zruties

- **zruty** (`PM_ZRUTY`): Zruties; large source size; base level 9, difficulty 11. Humanoid body, carnivorous. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `zruties`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Radial bodies / Xorns

- **xorn** (`PM_XORN`): Xorns; medium source size; base level 8, difficulty 11. Attacks: claw/physical, claw/physical, claw/physical, bite/physical.
  - Model: `xorns`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Rocklike ambush bodies / Piercers

- **rock piercer** (`PM_ROCK_PIERCER`): Piercers; small source size; base level 3, difficulty 4. Carnivorous. Attacks: bite/physical.
  - Model: `piercers`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **iron piercer** (`PM_IRON_PIERCER`): Piercers; medium source size; base level 5, difficulty 6. Carnivorous. Attacks: bite/physical.
  - Model: `piercers`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **glass piercer** (`PM_GLASS_PIERCER`): Piercers; medium source size; base level 7, difficulty 9. Carnivorous. Attacks: bite/physical.
  - Model: `piercers`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Serpentine bodies / Nagas

- **red naga hatchling** (`PM_RED_NAGA_HATCHLING`): Nagas; large source size; base level 3, difficulty 4. Omnivorous. Attacks: bite/physical.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **black naga hatchling** (`PM_BLACK_NAGA_HATCHLING`): Nagas; large source size; base level 3, difficulty 4. Carnivorous. Attacks: bite/physical.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **golden naga hatchling** (`PM_GOLDEN_NAGA_HATCHLING`): Nagas; large source size; base level 3, difficulty 4. Omnivorous. Attacks: bite/physical.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **guardian naga hatchling** (`PM_GUARDIAN_NAGA_HATCHLING`): Nagas; large source size; base level 3, difficulty 4. Omnivorous. Attacks: bite/physical.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **red naga** (`PM_RED_NAGA`): Nagas; huge source size; base level 6, difficulty 8. Omnivorous. Attacks: bite/physical, breath/fire.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **black naga** (`PM_BLACK_NAGA`): Nagas; huge source size; base level 8, difficulty 10. Carnivorous. Attacks: bite/physical, spit/acid.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **golden naga** (`PM_GOLDEN_NAGA`): Nagas; huge source size; base level 10, difficulty 13. Omnivorous. Attacks: bite/physical, magic/spel.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **guardian naga** (`PM_GUARDIAN_NAGA`): Nagas; huge source size; base level 12, difficulty 17. Omnivorous. Attacks: spit/poison, bite/plys, touch/physical, hugs/constriction.
  - Model: `nagas`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Small humanoid bodies / Gargoyles

- **gargoyle** (`PM_GARGOYLE`): Gargoyles; human source size; base level 6, difficulty 8. Humanoid body. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `gargoyles`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **winged gargoyle** (`PM_WINGED_GARGOYLE`): Gargoyles; human source size; base level 9, difficulty 11. Flies, humanoid body. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `gargoyles`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Small humanoid bodies / Gremlins

- **gremlin** (`PM_GREMLIN`): Gremlins; small source size; base level 5, difficulty 8. Swims, humanoid body. Attacks: claw/physical, claw/physical, bite/physical, claw/curs.
  - Model: `gremlins`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Specialised quadrupeds / Disenchanter

- **disenchanter** (`PM_DISENCHANTER`): Disenchanter; large source size; base level 12, difficulty 14. Carnivorous. Attacks: claw/ench, passive contact/ench.
  - Model: `disenchanter`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Specialised quadrupeds / Rust Monster

- **rust monster** (`PM_RUST_MONSTER`): Rust Monster; medium source size; base level 5, difficulty 8. Swims, no grasping hands. Attacks: touch/rust, touch/rust, passive contact/rust.
  - Model: `rust_monster`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Mythic bodies / Winged reptiles / Dragons

- **baby gray dragon** (`PM_BABY_GRAY_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: gray dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby gold dragon** (`PM_BABY_GOLD_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: gold dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby silver dragon** (`PM_BABY_SILVER_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: silver dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby shimmering dragon** (`PM_BABY_SHIMMERING_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical. **Conditional source entry.**
  - Model: `dragon`; parent: shimmering dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby red dragon** (`PM_BABY_RED_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: red dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby white dragon** (`PM_BABY_WHITE_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: white dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby orange dragon** (`PM_BABY_ORANGE_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: orange dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby black dragon** (`PM_BABY_BLACK_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: black dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby blue dragon** (`PM_BABY_BLUE_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: blue dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby green dragon** (`PM_BABY_GREEN_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: green dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **baby yellow dragon** (`PM_BABY_YELLOW_DRAGON`): Dragons; huge source size; base level 12, difficulty 13. Flies, no grasping hands, carnivorous. Attacks: bite/physical.
  - Model: `dragon`; parent: yellow dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions; Juvenile proportions and gait; do not uniformly shrink adult mesh.
- **gray dragon** (`PM_GRAY_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/magm, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **gold dragon** (`PM_GOLD_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/fire, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **silver dragon** (`PM_SILVER_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/cold, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **shimmering dragon** (`PM_SHIMMERING_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/magm, bite/physical, claw/physical, claw/physical. **Conditional source entry.**
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **red dragon** (`PM_RED_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/fire, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **white dragon** (`PM_WHITE_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/cold, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **orange dragon** (`PM_ORANGE_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/sleep, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **black dragon** (`PM_BLACK_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/disn, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **blue dragon** (`PM_BLUE_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/electricity, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **green dragon** (`PM_GREEN_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/poison, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **yellow dragon** (`PM_YELLOW_DRAGON`): Dragons; gigantic source size; base level 15, difficulty 20. Flies, no grasping hands, carnivorous. Attacks: breath/acid, bite/physical, claw/physical, claw/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **Chromatic Dragon** (`PM_CHROMATIC_DRAGON`): Dragons; gigantic source size; base level 16, difficulty 23. No grasping hands, carnivorous. Attacks: breath/rbre, magic/spel, claw/samu, bite/physical, bite/physical, sting/physical.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.
- **Ixoth** (`PM_IXOTH`): Dragons; gigantic source size; base level 15, difficulty 22. Flies, no grasping hands, carnivorous. Attacks: breath/fire, bite/physical, magic/spel, claw/physical, claw/samu.
  - Model: `dragon`; parent: adult dragon. Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions.

## Supernatural beings / Celestial bodies / Celestials

- **Aleax** (`PM_ALEAX`): Celestials; human source size; base level 10, difficulty 12. Humanoid body. Attacks: weapon/physical, weapon/physical, kick/physical.
  - Model: `celestials`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Angel** (`PM_ANGEL`): Celestials; human source size; base level 14, difficulty 19. Flies, humanoid body. Attacks: weapon/physical, weapon/physical, claw/physical, magic/magm.
  - Model: `celestials`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Archon** (`PM_ARCHON`): Celestials; large source size; base level 19, difficulty 26. Flies, humanoid body. Attacks: weapon/physical, weapon/physical, gaze/blnd, claw/physical, magic/spel.
  - Model: `celestials`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Supernatural beings / Infernal and unique bodies / Demons and related identities

- **water demon** (`PM_WATER_DEMON`): Demons and related identities; human source size; base level 8, difficulty 11. Swims, humanoid body. Attacks: weapon/physical, claw/physical, bite/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **amorous demon** (`PM_AMOROUS_DEMON`): Demons and related identities; human source size; base level 6, difficulty 8. Flies, humanoid body.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **horned devil** (`PM_HORNED_DEVIL`): Demons and related identities; human source size; base level 6, difficulty 9. Attacks: weapon/physical, claw/physical, bite/physical, sting/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **erinys** (`PM_ERINYS`): Demons and related identities; human source size; base level 7, difficulty 10. Humanoid body. Attacks: weapon/poison.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **barbed devil** (`PM_BARBED_DEVIL`): Demons and related identities; human source size; base level 8, difficulty 11. Attacks: claw/physical, claw/stck, sting/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **marilith** (`PM_MARILITH`): Demons and related identities; large source size; base level 7, difficulty 11. Humanoid body. Attacks: weapon/physical, weapon/physical, claw/physical, claw/physical, claw/physical, claw/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **vrock** (`PM_VROCK`): Demons and related identities; large source size; base level 8, difficulty 11. Attacks: claw/physical, claw/physical, claw/physical, claw/physical, bite/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **hezrou** (`PM_HEZROU`): Demons and related identities; large source size; base level 9, difficulty 12. Humanoid body. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **bone devil** (`PM_BONE_DEVIL`): Demons and related identities; large source size; base level 9, difficulty 13. Attacks: weapon/physical, sting/poison.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **ice devil** (`PM_ICE_DEVIL`): Demons and related identities; large source size; base level 11, difficulty 15. Attacks: claw/physical, claw/physical, bite/physical, sting/cold, touch/slow.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **nalfeshnee** (`PM_NALFESHNEE`): Demons and related identities; large source size; base level 11, difficulty 15. Humanoid body. Attacks: claw/physical, claw/physical, bite/physical, magic/spel.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **pit fiend** (`PM_PIT_FIEND`): Demons and related identities; large source size; base level 13, difficulty 16. Attacks: weapon/physical, weapon/physical, hugs/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **sandestin** (`PM_SANDESTIN`): Demons and related identities; human source size; base level 13, difficulty 15. Humanoid body. Attacks: weapon/physical, weapon/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **balrog** (`PM_BALROG`): Demons and related identities; large source size; base level 16, difficulty 20. Flies. Attacks: weapon/physical, weapon/physical.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Juiblex** (`PM_JUIBLEX`): Demons and related identities; large source size; base level 50, difficulty 26. Flies, amphibious. Attacks: engulf/dise, spit/acid.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Yeenoghu** (`PM_YEENOGHU`): Demons and related identities; large source size; base level 56, difficulty 31. Flies. Attacks: weapon/physical, weapon/conf, claw/plys, magic/magm.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Orcus** (`PM_ORCUS`): Demons and related identities; huge source size; base level 66, difficulty 36. Flies. Attacks: weapon/physical, claw/physical, claw/physical, magic/spel, sting/poison.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Geryon** (`PM_GERYON`): Demons and related identities; huge source size; base level 72, difficulty 36. Flies. Attacks: claw/physical, claw/physical, sting/poison.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Dispater** (`PM_DISPATER`): Demons and related identities; human source size; base level 78, difficulty 40. Flies, humanoid body. Attacks: weapon/physical, magic/spel.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Baalzebub** (`PM_BAALZEBUB`): Demons and related identities; large source size; base level 89, difficulty 45. Flies. Attacks: bite/poison, gaze/stun.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Asmodeus** (`PM_ASMODEUS`): Demons and related identities; huge source size; base level 105, difficulty 53. Flies, humanoid body. Attacks: claw/physical, magic/cold.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Demogorgon** (`PM_DEMOGORGON`): Demons and related identities; huge source size; base level 106, difficulty 57. Flies, no grasping hands. Attacks: magic/spel, sting/life drain, claw/dise, claw/dise.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Minion of Huhetotl** (`PM_MINION_OF_HUHETOTL`): Demons and related identities; large source size; base level 16, difficulty 23. Flies. Attacks: weapon/physical, weapon/physical, magic/spel, claw/samu.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **Nalzok** (`PM_NALZOK`): Demons and related identities; large source size; base level 16, difficulty 23. Flies. Attacks: weapon/physical, weapon/physical, magic/spel, claw/samu.
  - Model: `demons_and_related_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Supernatural beings / Personifications / Riders

- **Death** (`PM_DEATH`): Riders; human source size; base level 30, difficulty 34. Flies, humanoid body. Attacks: touch/deth, touch/deth.
  - Model: `riders`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Pestilence** (`PM_PESTILENCE`): Riders; human source size; base level 30, difficulty 34. Flies, humanoid body. Attacks: touch/pest, touch/pest.
  - Model: `riders`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Famine** (`PM_FAMINE`): Riders; human source size; base level 30, difficulty 34. Flies, humanoid body. Attacks: touch/famn, touch/famn.
  - Model: `riders`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Supernatural beings / Small supernatural bodies / Imps and related beings

- **manes** (`PM_MANES`): Imps and related beings; small source size; base level 1, difficulty 3. Attacks: claw/physical, claw/physical, bite/physical.
  - Model: `imps_and_related_beings`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **homunculus** (`PM_HOMUNCULUS`): Imps and related beings; tiny source size; base level 2, difficulty 3. Flies. Attacks: bite/sleep.
  - Model: `imps_and_related_beings`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **imp** (`PM_IMP`): Imps and related beings; tiny source size; base level 3, difficulty 4. Attacks: claw/physical.
  - Model: `imps_and_related_beings`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **lemure** (`PM_LEMURE`): Imps and related beings; medium source size; base level 3, difficulty 5. Attacks: claw/physical.
  - Model: `imps_and_related_beings`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **quasit** (`PM_QUASIT`): Imps and related beings; small source size; base level 3, difficulty 7. Attacks: claw/drdx, claw/drdx, bite/physical.
  - Model: `imps_and_related_beings`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **tengu** (`PM_TENGU`): Imps and related beings; small source size; base level 6, difficulty 7. Attacks: bite/physical.
  - Model: `imps_and_related_beings`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Supernatural beings / Special identities / Djinni

- **djinni** (`PM_DJINNI`): Djinni; human source size; base level 7, difficulty 8. Flies, humanoid body. Attacks: weapon/physical.
  - Model: `djinni`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Supernatural beings / Special identities / Mail Daemon

- **mail daemon** (`PM_MAIL_DAEMON`): Mail Daemon; human source size; base level 56, difficulty 26. Flies, swims, humanoid body. **Conditional source entry.**
  - Model: `mail_daemon`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Supernatural forms / Lycanthropes / Canids

- **werejackal** (`PM_WEREJACKAL`): Canids; small source size; base level 2, difficulty 4. No grasping hands, carnivorous. Attacks: bite/were.
  - Model: `canid`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **werewolf** (`PM_WEREWOLF`): Canids; medium source size; base level 5, difficulty 7. No grasping hands, carnivorous. Attacks: bite/were.
  - Model: `wolf`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Supernatural forms / Lycanthropes / Humans and special identities

- **wererat** (`PM_HUMAN_WERERAT`): Humans and special identities; human source size; base level 2, difficulty 3. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **werejackal** (`PM_HUMAN_WEREJACKAL`): Humans and special identities; human source size; base level 2, difficulty 3. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.
- **werewolf** (`PM_HUMAN_WEREWOLF`): Humans and special identities; human source size; base level 5, difficulty 6. Humanoid body, omnivorous. Attacks: weapon/physical.
  - Model: `humans_and_special_identities`. Mixed production group: establish species anatomy before sharing a final body or rig.

## Supernatural forms / Lycanthropes / Rodents

- **wererat** (`PM_WERERAT`): Rodents; tiny source size; base level 2, difficulty 4. No grasping hands, carnivorous. Attacks: bite/were.
  - Model: `wererat`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Undead / Ancestry plus state / Mummies

- **kobold mummy** (`PM_KOBOLD_MUMMY`): Mummies; small source size; base level 3, difficulty 4. Humanoid body, undead. Attacks: claw/physical.
  - Model: `kobold_humanoid`; parent: kobold. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **gnome mummy** (`PM_GNOME_MUMMY`): Mummies; small source size; base level 4, difficulty 5. Humanoid body, undead. Attacks: claw/physical.
  - Model: `gnome_humanoid`; parent: gnome. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **orc mummy** (`PM_ORC_MUMMY`): Mummies; human source size; base level 5, difficulty 6. Humanoid body, undead. Attacks: claw/physical.
  - Model: `orc_humanoid`; parent: orc. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **dwarf mummy** (`PM_DWARF_MUMMY`): Mummies; human source size; base level 5, difficulty 6. Humanoid body, undead. Attacks: claw/physical.
  - Model: `dwarf_humanoid`; parent: dwarf. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **elf mummy** (`PM_ELF_MUMMY`): Mummies; human source size; base level 6, difficulty 7. Humanoid body, undead. Attacks: claw/physical.
  - Model: `elf_humanoid`; parent: elf. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **human mummy** (`PM_HUMAN_MUMMY`): Mummies; human source size; base level 6, difficulty 7. Humanoid body, undead. Attacks: claw/physical, claw/physical.
  - Model: `human_humanoid`; parent: human. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **ettin mummy** (`PM_ETTIN_MUMMY`): Mummies; huge source size; base level 7, difficulty 8. Humanoid body, undead. Attacks: claw/physical, claw/physical.
  - Model: `ettin_humanoid`; parent: ettin. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **giant mummy** (`PM_GIANT_MUMMY`): Mummies; huge source size; base level 8, difficulty 10. Humanoid body, undead. Attacks: claw/physical, claw/physical.
  - Model: `giant_humanoid`; parent: giant. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.

## Undead / Ancestry plus state / Zombies

- **kobold zombie** (`PM_KOBOLD_ZOMBIE`): Zombies; small source size; base level 0, difficulty 1. Humanoid body, undead. Attacks: claw/physical.
  - Model: `kobold_humanoid`; parent: kobold. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **gnome zombie** (`PM_GNOME_ZOMBIE`): Zombies; small source size; base level 1, difficulty 2. Humanoid body, undead. Attacks: claw/physical.
  - Model: `gnome_humanoid`; parent: gnome. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **orc zombie** (`PM_ORC_ZOMBIE`): Zombies; human source size; base level 2, difficulty 3. Humanoid body, undead. Attacks: claw/physical.
  - Model: `orc_humanoid`; parent: orc. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **dwarf zombie** (`PM_DWARF_ZOMBIE`): Zombies; human source size; base level 2, difficulty 3. Humanoid body, undead. Attacks: claw/physical.
  - Model: `dwarf_humanoid`; parent: dwarf. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **elf zombie** (`PM_ELF_ZOMBIE`): Zombies; human source size; base level 3, difficulty 4. Humanoid body, undead. Attacks: claw/physical.
  - Model: `elf_humanoid`; parent: elf. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **human zombie** (`PM_HUMAN_ZOMBIE`): Zombies; human source size; base level 4, difficulty 5. Humanoid body, undead. Attacks: claw/physical.
  - Model: `human_humanoid`; parent: human. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **ettin zombie** (`PM_ETTIN_ZOMBIE`): Zombies; huge source size; base level 6, difficulty 7. Humanoid body, undead. Attacks: claw/physical, claw/physical.
  - Model: `ettin_humanoid`; parent: ettin. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **ghoul** (`PM_GHOUL`): Zombies; small source size; base level 3, difficulty 5. Humanoid body, omnivorous, undead. Attacks: claw/plys, claw/physical.
  - Model: `ghoul_humanoid`; parent: ghoul. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **giant zombie** (`PM_GIANT_ZOMBIE`): Zombies; huge source size; base level 8, difficulty 9. Humanoid body, undead. Attacks: claw/physical, claw/physical.
  - Model: `giant_humanoid`; parent: giant. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.
- **skeleton** (`PM_SKELETON`): Zombies; human source size; base level 12, difficulty 14. Humanoid body, undead. Attacks: weapon/physical, touch/slow.
  - Model: `skeleton_humanoid`; parent: skeleton. Ancestry body plus undead deformation/skin; detachable wraps for mummy; Validate anatomy and source silhouette per ancestry.

## Undead / Humanoids and alternate forms / Vampires

- **vampire** (`PM_VAMPIRE`): Vampires; human source size; base level 10, difficulty 12. Flies, humanoid body, undead. Attacks: claw/physical, bite/life drain.
  - Model: `vampires`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **vampire leader** (`PM_VAMPIRE_LEADER`): Vampires; human source size; base level 12, difficulty 14. Flies, humanoid body, undead. Attacks: claw/physical, bite/life drain.
  - Model: `vampires`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **vampire mage** (`PM_VAMPIRE_MAGE`): Vampires; human source size; base level 20, difficulty 26. Flies, humanoid body, undead. Attacks: claw/life drain, bite/life drain, magic/spel. **Conditional source entry.**
  - Model: `vampires`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Vlad the Impaler** (`PM_VLAD_THE_IMPALER`): Vampires; human source size; base level 28, difficulty 32. Flies, humanoid body, undead. Attacks: weapon/physical, bite/life drain.
  - Model: `vampires`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Undead / Skeletal spellcasters / Liches

- **lich** (`PM_LICH`): Liches; human source size; base level 11, difficulty 14. Humanoid body, undead. Attacks: touch/cold, magic/spel.
  - Model: `liches`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **demilich** (`PM_DEMILICH`): Liches; human source size; base level 14, difficulty 18. Humanoid body, undead. Attacks: touch/cold, magic/spel.
  - Model: `liches`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **master lich** (`PM_MASTER_LICH`): Liches; human source size; base level 17, difficulty 21. Humanoid body, undead. Attacks: touch/cold, magic/spel.
  - Model: `liches`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **arch-lich** (`PM_ARCH_LICH`): Liches; human source size; base level 25, difficulty 29. Humanoid body, undead. Attacks: touch/cold, magic/spel.
  - Model: `liches`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Undead / Spectral bodies / Ghosts

- **ghost** (`PM_GHOST`): Ghosts; human source size; base level 10, difficulty 12. Flies, humanoid body, undead. Attacks: touch/physical.
  - Model: `ghosts`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **shade** (`PM_SHADE`): Ghosts; human source size; base level 12, difficulty 14. Flies, humanoid body, undead. Attacks: touch/plys, touch/slow.
  - Model: `ghosts`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.

## Undead / Spectral bodies / Wraiths

- **barrow wight** (`PM_BARROW_WIGHT`): Wraiths; human source size; base level 3, difficulty 8. Humanoid body, undead. Attacks: weapon/life drain, magic/spel, claw/physical, touch/cold.
  - Model: `wraiths`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **wraith** (`PM_WRAITH`): Wraiths; human source size; base level 6, difficulty 8. Flies, humanoid body, undead. Attacks: touch/life drain.
  - Model: `wraiths`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.
- **Nazgul** (`PM_NAZGUL`): Wraiths; human source size; base level 13, difficulty 17. Humanoid body, undead. Attacks: weapon/life drain, breath/sleep.
  - Model: `wraiths`. Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details.


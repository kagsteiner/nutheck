# Creature assets: session handoff

Read this file first for creature-art work. Open other documents/code only as
needed; do not load the entire project history or full catalogue into context.
Last updated: 2026-10-31. This file records decisions, not a request to run tools.

## Current instruction and status

- **Overall vision (2026-10-31):** follow [GameVision.md](GameVision.md).
  Preserve NetHack's tactical core and turn behaviour, with modern graphics
  and static characters/objects. Animation and runtime rigs are out of scope,
  not unfinished production work. Brief wand effects (especially lightning)
  remain optional. This overrides older animation-related future-work notes.
  The latest environment reference is the left Carved stone panel; retain
  existing creature-specific anatomy, palette and pose decisions.

- **Player correction:** no detachable clothing. Build each player as a single
  fixed character matching its icon. This overrides earlier modular player-clothing
  proposals. Female Valkyrie has fitted brown legwear; male Barbarian has a short
  brown waist garment, with no added skirts, long flap or decorative buckle.

- Two human player forms also exist: **female Valkyrie and male Barbarian**.
  See `Docs/HumanPlayers.md`. They are hero-only, ancestry/sex-specific static
  drafts. Valkyrie's permitted starting-sex target is complete; Barbarian remains
  partial at role level because female Barbarian was not requested/generated.

- Sixty creature identities have static drafts: **giant ant, little dog, goblin,
  jackal, fox, gnome, sewer rat, giant rat, gnome ruler, kitten, housecat,
  large cat, wolf, winter wolf cub, winter wolf, dog, large dog, dingo, coyote,
  warg, rabid rat, bat, giant bat, vampire bat, jaguar, lynx, panther, tiger, hell hound pup, hell hound, pony, horse, warhorse, white unicorn, gray unicorn and black unicorn, kobold, large kobold, kobold leader, kobold shaman, kobold mummy, kobold zombie, gnomish wizard, gnome mummy, gnome zombie, dwarf, dwarf leader, dwarf ruler, dwarf mummy, dwarf zombie, hobgoblin, hill orc, Mordor orc, floating eye, newt, lichen, Uruk-hai, orc shaman, orc-captain and grid bug**.
  See `Docs/SpecialBatch1.md` for the latest artifacts and checks; batches 5/6 document wolf/dog families
  and batch 7 documents coyote/warg/rabid rat. Both winter wolves
  have been revised to remove cyan cast-shadow colours and use smaller, more
  forward/inward skull-conforming red eyes with pale lids and dark pupils.
- Canids, rats, felines and equines use parameterised family generators. The feline
  family uses independent head, torso, leg, ear, paw and tail dimensions for
  juvenile/adult forms; peach coat patches and tail bands are vertex paint.
  Gnome ruler reuses the existing gnome body with detachable crown/rank modules.
  Wolves now have a parameterised family with texture-only fur; cold-breath
  effects are optional; animations are out of scope.
- Jackal correction after user review: no raised back overlay. Its darker fur
  marking is blended vertex paint on the continuous body. Do not recreate the
  former cushion-like `back_saddle` geometry.
- Rat correction after user review: **make both rats leaner and accept the tile
  silhouette difference**. The user likes the snout, whiskers, ears and colours;
  preserve those. Narrow the torso, belly and haunches, keeping a larger frame
  for giant rat. Do not recreate the fat, floor-hugging tile silhouette for fidelity.
- These are static drafts requiring visual finishing, not finished production art.
  The concept sheet is more polished than the actual geometry. Be candid.
- **Fur direction (user decision):** prefer the middle, texture-only treatment
  for future fur-bearing models where appropriate. The user agrees with this
  direction but considers the visual difference too small to justify redoing
  existing models: **do not retrofit or regenerate the existing twelve models
  just to add fur**. Individual hair, polygon-heavy fur and the extra sculpted
  clumps are not the selected direction. See
  [FurStudy.md](FurStudy.md) and `Art/FurStudy/` for smooth, painted texture and
  sparse-clump variants. Two shared 512x512 maps; texture-only adds no triangles;
  extra clumps add 80 dog / 32 cat triangles relative to current drafts.
  Study assets stay under `/Game/FurStudy`; canonical twelve live models remain
  unchanged. This is guidance for future work, not a request to start generation.
  Preserve the
  miniature palette/silhouette; fur should mostly average away at level distance.

- **Jaguar reference correction:** the user approved lynx/panther but rejected
  the sparse jaguar pattern and supplied a real jaguar photograph. The jaguar now
  uses dense irregular rosettes wrapping over the spine and both flanks, small
  head/leg spots, pale underside/lower legs and stronger tail bands. Preserve
  this direction and the unchanged lynx/panther. Reference and actual views:
  `Art/CreatureInterpretations/Jaguar-ReferenceRevision.png`; source photograph:
  `Art/CreatureInterpretations/References/Jaguar-user-reference.jpg`.
  `JaguarCoat.py` is the current sampler; do not restore the earlier sparse
  flank-only rings/squiggles. See `Docs/JaguarReferenceRevision.md` for evidence.
  Revision import/native and final live checks pass; all six displayed sex forms,
  six fallbacks, materials/UV/paint, native map/zoom and F9 both ways passed at
  unchanged turn 5. Saved geometry/paint and FBX hashes confirm lynx/panther are
  unchanged; jaguar geometry and the 27-draft inventory are retained.

## Product and art decisions

- Project: NetHack gameplay/core, Unreal presentation (nUthEck). Canonical source
  is NetHack 5.0 release, pinned upstream commit
  `16ff59115315917b93185d026aeefea06db9b0f4` in `upstream/NetHack`.
- Prefer the **official default tileset**. Alternatives need a strong concrete
  reason. Recognisability as NetHack matters more than generic fantasy polish.
- **Tile-shadow interpretation (explicit user correction):** most or all creature
  tiles include a crudely drawn, single-line cast shadow, typically black or dark
  grey. Separate those pixels from the creature before inferring anatomy,
  silhouette or coat colours. Shadows can also be coloured: the blue/cyan around
  the winter wolves is shadow, not blue fur, socks or muzzle markings. A shadow
  on blue ice is a possible explanation, not an established source fact.
  Check whether an offset edge continues beneath feet or along one side of the
  figure, and compare related tiles before assigning it to the body. Do not turn
  shadow pixels into extra geometry or painted markings to improve tile overlap.
  Exclude likely cast shadows from silhouette/palette comparisons, document
  ambiguous pixels, and let Unreal produce the actual cast shadow.
  **Use spatial masks, not blanket black-palette removal:** bat tiles have a
  detached lower shadow silhouette (rows 9-15). Upper black pixels belong to
  the figure, especially vampire bat. Do not model the lower shape as a second
  body or discard the actual black upper body. Future dark creatures need the
  same explicit separation of anatomy and shadow.
- Desired final creature direction: imagine a **complete anatomical 3D object**
  which, viewed from a suitable angle and pixelated, could plausibly give the
  original tiny tile. Infer hidden limbs/back/proportions creatively; explicitly
  distinguish source facts from artistic assumptions. User enthusiastically
  approved this direction and the first three concepts.
- Consistency is essential: shared sculpt language, proportions, palette logic,
  materials and detail scale. User rejected the visual incoherence of unrelated
  downloaded/AI assets. Preferred direction is **painted miniature**, not carved
  stone. Their initial “left/carved stone” selection was corrected to centre.
- Early regular dungeon: neutral grey worked stone and actual NetHack layouts.
  Gnomish Mines should respect their brownish identity; later branches/quests
  can have distinct environments. Do not impose one room-study palette on all
  branches. Creature consistency need not erase branch distinctions.
- Camera: Diablo-like angled top-down; whole 79x21 level must remain available.
  Zoom and experimental player-eye view also exist. Models must read at overview
  scale and remain complete/credible when viewed close up or from behind.
- Real geometry and real-time shadows matter. Walls were deliberately raised.
- **Presentation controls:** F7 hides/shows floating entity glyphs/badges (default
  shown); menus/messages/targeting stay visible. Ctrl+F uses a reversible .8s quartic
  approach ending in the latest movement/mouse-look direction, with no corridor
  override or horizon banking. F5 resets the overview. These consume no turn.
  `Docs/PresentationControls.md` records the math, keys and live verification.
- **Save policy changed by the user (2026-10-31): this is now their actual
  NetHack installation. Saves matter. All previous permission to reset or replace
  development saves is revoked. Preserve played sessions and the last-session
  pointer; use fresh isolated test sessions. Back up before save-affecting work
  or native backend replacement, and recover from verified staged copies. Follow
  `AGENTS.md` and [SaveProtection.md](SaveProtection.md). Never force-stop a player
  backend or resume their played session for a test.**

## Backlog workflow for future sessions

Use [backlog.md](../backlog.md) as the working progress checklist; use the source
catalogue for identity, traits and modelling recipes. The backlog is maintained
by hand and must not be overwritten by catalogue regeneration.

1. **Choose work:** read the backlog introduction and suggested next batches,
   then only the relevant anatomy-group entries. Query selected catalogue
   records by stable `PM_*` ID; do not load the entire roster. Prefer compatible
   family batches and existing reusable bodies, while checking each official
   tile and source traits. Suggestions do not themselves request generation;
   proceed when the user's task authorizes it, without asking again for work
   already authorized in that task.
2. **Track partial work:** leave the checkbox unchecked while work is incomplete.
   Add a short in-progress or blocked note with existing artifact paths and the
   exact remaining step, so another session can resume without regeneration.
3. **Mark generation complete:** check the existing identity's item only after
   editable Blender geometry, painted FBX, inspected front/rear renders and true
   16x16 comparisons, Unreal import/material validation, displayed-identity
   mapping/fallback and no-turn style-toggle checks exist. Link the actual
   artifacts and verification evidence beside the item. A concept image, mesh
   file alone or retained tile-volume proxy does not satisfy this milestone.
4. **Keep finish work separate:** checked means a generated and verified static
   draft, not production-ready art. Keep anatomical/material refinement, garment
   fixes, rigging, animations, effects and performance work in the finishing
   section. Review fixes update existing evidence; they do not create duplicate
   identity entries. If a required check regresses, uncheck the affected item and
   record the remaining repair.
5. **Close out each batch:** update checkboxes in place, summary counts, suggested
   next batches, known limitations and this handoff's current status. Update the
   draft-status list in `Scripts/CreateCreatureCatalogue.py`, then regenerate
   the source catalogue so JSON/CSV status agrees with the backlog. Do not count
   a shared body as completing every derivative; verify each displayed identity.
6. **Reconcile inventories:** preserve completed items, evidence, priorities and
   notes when source inventory changes. Match by `PM_*` ID, add new identities
   once, and explicitly review removed/conditional/auxiliary entries. Check for
   missing or duplicated IDs and recompute counts rather than copying stale
   totals. Player-role identities appear once in the player section; their 25
   permitted starting-sex variants are validation targets, not mandatory unique
   meshes. Objects, terrain and effects have separate inventory tasks; four objects
   and one fountain feature now have drafts, while full inventories remain pending. Do not describe the
   creature backlog as a complete game-art inventory.

Current baseline: **394 source identities = 60 verified creature drafts + 1 completed player role
+ 321 remaining creatures + 12 remaining player roles**. There are 64 physical
static forms: 62 creature forms (60 identities plus two beardless female variants)
plus two human player variants (Barbarian is partial).
Static-draft coverage is **60/381 creatures = 15.7%**, or **61/394 creature/player
identities = 15.5%**; finishing/rigging/animation and objects/terrain remain separate.
The next suggested batch is **orc mummy and orc zombie**
(review both sex tiles and source traits; reuse saved upright orc anatomy only
where compatible, with separate linen/undead/clothing/equipment modules). These are
planning recommendations; future progress must update the baseline and queue.

## Catalogue: how to use it without consuming context

- `backlog.md`: progress, next batches and finishing work; follow the workflow above.
- `Art/CreatureCatalogue/creatures.json`: authoritative generated inventory and
  proposed recipes. Query/filter by `id`, `name`, `hierarchy` or recipe base;
  read only selected records. `creatures.csv` supports spreadsheet filtering.
- `Art/CreatureCatalogue/Hierarchy.md`: readable full grouped roster. Avoid
  loading the whole file into an agent session unless necessary.
- Player branch: `players.json` / `players.csv`, also embedded as
  `player_hierarchy` in `creatures.json` (schema v2). **Player → 13 role
  subclasses → 25 permitted starting-sex subclasses**. Restrictions are parsed
  from `src/role.c` allow masks. Valkyrie is female-only at character creation;
  the official male Valkyrie tile does not imply a legal starting choice.
  Other roles allow male/female; aliases include Caveman/Cavewoman and
  Priest/Priestess (canonical creature names cave dweller and cleric).
  Race/ancestry is independent. Later sex changes/polymorph are outside these
  starting restrictions. Human female Valkyrie and human male Barbarian drafts
  are generated; female Barbarian remains a proxy. Other ancestry variants stay
  unscoped; existing role tile-volume proxies remain available.
- Regenerate with Python: `Scripts/CreateCreatureCatalogue.py`. This is a
  **source-only** script; it never invokes Blender, UE or asset import.
- It parses all `MON(...)` declarations in `include/monsters.h`, including
  conditional declarations and display auxiliaries. This is a source inventory,
  not the exact compiled runtime roster. Conditional guards are recorded.
- Unique identity is `PM_*` enum, not display name. Canonical neutral name and
  gender aliases are retained: **gnome ruler** = gnome king/queen. Different
  forms can share a name (e.g. lycanthropes), so names alone are not globally
  unique IDs. Numeric enum values can change with build options.
- Records preserve native level, difficulty, size, attacks, resistances, flags,
  ASCII colour, official file-local tile references and source locations.
  Encyclopedia key matches point into `dat/data.base`; literary excerpts are
  not copied wholesale. Descriptions are source-derived factual summaries.
- Modelling hierarchy is deliberately **not scientific phylogeny**. Anatomy,
  ancestry and overlays are separate concerns. Mixed source glyph classes are
  split where obvious; unresolved groups are review queues, not confident
  claims that unrelated monsters can share a final mesh.
- Recipes are initial suggestions requiring visual/anatomical review. The
  catalogue does not yet drive runtime selection or geometry generation.

## Reuse rules

1. Share anatomy/blockouts and eventually rigs within compatible families;
   preserve distinguishing silhouettes. Sharing a NetHack glyph class alone
   does not justify sharing anatomy (ants, bees and beetles differ).
2. Separate base body, age/proportion changes, rank, clothing/equipment,
   palette/material, undead state and elemental/attack effects.
3. Gnome ruler: gnome base plus detachable crown and rank clothing. Crown is
   an explicit user-approved visual interpretation, not evidence about a live
   monster's inventory. Keep weapon/armour/accessory modules detachable.
4. Winter wolf: wolf-family anatomy, pale/white fur interpretation, appropriate
   size/proportions and default-tile accents; retain cold resistance and cold
   breath as gameplay distinctions. Breath needs a future animation/effect hook,
   not just a white material. Cub needs juvenile proportions/gait.
5. Giant rat can reuse rat construction/rig but needs a larger, lean frame;
   jackal/fox need distinct muzzle, ears, legs and tail, not colour swaps only.
6. Baby/adult forms are not merely uniform scaling. Zombies/mummies retain
   ancestry anatomy with state changes/wraps. Golem material changes may also
   demand geometry/joint changes. Unique/quest creatures require review.
7. Abstract NetHack size/weight do not supply literal metre dimensions. ASCII
   colour is not automatically skin/fur colour; actual default-tile colour
   masses are the visual reference. Keep source traits separate from guesses.
8. Sixty creature identities have drafts. Gnomish wizard and gnome zombie
   include beardless female appearances supported by their actual tiles; the other
   58 use shared sex-neutral forms. Player forms are sex/ancestry-specific as
   described above. Do not claim further sex anatomy was reconstructed. Review
   both sex tiles in new batches and preserve aliases/sex metadata.

## Existing assets and evidence

All paths below are project-relative.

| Path | Purpose |
|---|---|
| `Art/SpecialBatch1/SpecialBatch1.blend` | Grid bug, generic corpse and carved fountain; mixed source references, static water, separate namespaces, displayed corpse mapping and fountain/sink distinction; native/import/live evidence |
| `Art/CreatureInterpretations/CreatureBatch20.blend` | Uruk-hai/shaman/captain; exact saved orc anatomy, separate red-centred shield and helmet rim, caster/rank paint and source/native/import/live evidence |
| `Art/CreatureInterpretations/CreatureBatch19.blend` | Requested floating eye/newt/lichen; curved hovering eye, complete four-legged amphibian and eyeless foliose thallus, original palettes and source/native/import/live evidence |
| `Art/CreatureInterpretations/CreatureBatch18.blend` | Hobgoblin/hill orc/Mordor orc; saved goblin vertices, exact shared upright orc body, source palettes, separate equipment and source/native/import/live evidence |
| `Art/CreatureInterpretations/CreatureBatch17.blend` | Dwarf mummy/zombie; two shared-sex forms, exact saved dwarf anatomy, blue caps, fitted linen/undead paint and source/native/import/live evidence |
| `Art/CreatureInterpretations/CreatureBatch16.blend` | Dwarf/leader/ruler; three shared-sex forms, exact common ancestry, blue costume, separate yellow band/crown and source/native/import/live evidence |
| `Art/CreatureInterpretations/CreatureBatch15.blend` | Gnomish wizard/mummy/zombie; five forms, exact saved gnome body reuse, sex-supported beard modules, green caps, red undead eyes and fitted linen; evidence alongside |
| `Art/CreatureInterpretations/CreatureBatch14.blend` | Kobold shaman/mummy/zombie; exact saved ancestry reuse, yellow caster cloth, 14 fitted linen ribbons and blue/green undead skin; native/import/live evidence alongside |
| `Art/CreatureInterpretations/CreatureBatch13.blend` | Kobold/large kobold/kobold leader; blue dog-faced family, pale painted ear tips, separate orange rank pieces, native checks and live capture alongside |
| `Art/CreatureInterpretations/HumanPlayers.blend` | Human female Valkyrie / male Barbarian; fitted eyes, fixed integral icon clothing, source/head comparisons, native profile and player camera checks alongside |
| `Art/CreatureInterpretations/CreatureBatch12.blend` | White/gray/black unicorns; shared compatible body, attached spiral horns, source coats/manes/eyes, coat-coloured tails and clean engine capture alongside |
| `Art/CreatureInterpretations/CreatureBatch11.blend` | Pony/horse/warhorse; new equine anatomy, fitted lateral eyes/inner ears/manes, single hooves, source/head comparisons and live evidence alongside |
| `Art/CreatureInterpretations/CreatureBatch10.blend` | Tiger/hell hound pup/hell hound; continuous stripes, fitted eyes, independent age proportions, source/head comparison and live evidence alongside |
| `Art/CreatureInterpretations/CreatureBatch9.blend` | Jaguar/lynx/panther; painted rosettes/cheeks, fitted eyes, batch9 source/render comparisons, native report and live capture alongside |
| `Art/CreatureInterpretations/CreatureBatch8.blend` | Bat/giant bat/vampire bat; closed curved wings, batch8 comparison, wing/face review, inspection and live fixture capture alongside |
| `Art/CreatureInterpretations/CreatureBatch7.blend` | Coyote/warg/rabid rat; batch7 comparisons, head detail views, exact rat-body reuse report and live fixture capture alongside |
| `Art/CreatureInterpretations/CreatureBatch6.blend` | Dog/large dog/dingo, texture-only fur; batch6 comparisons, eye detail views, inspection and live fixture capture alongside |
| `Art/CreatureInterpretations/CreatureBatch5.blend` | Wolf/winter wolf cub/winter wolf, revised pale coats and fitted eyes; batch5 evidence and winter-wolf eye board alongside |
| `Art/CreatureInterpretations/CreatureBatch4.blend` | Kitten/housecat/large cat; batch4 comparison, projections, mesh inspection and live fixture capture alongside |
| `Art/CreatureInterpretations/CreatureBatch3.blend` | Sewer rat/giant rat/gnome ruler; batch3 comparison, report and Unreal fixture capture alongside |
| `Art/CreatureInterpretations/CreatureBatch2.blend` | Jackal/fox/gnome, separate editable collections; comparisons and report carry batch2 suffix |
| `Art/CreatureInterpretations/CreatureInterpretations.blend` | Native editable anatomy, vertex paint, camera/lights; three named collections, ant visible initially |
| `Art/CreatureInterpretations/{giant_ant,little_dog,goblin}.fbx` | Actual mesh exports |
| `Art/CreatureInterpretations/Concept-v1.png` | AI design exploration, **not** a mesh render; prompt alongside it |
| `Art/CreatureInterpretations/MeshComparison-v1.png` | Actual Blender views, original tiles, actual 16x16 reverse projections |
| `Art/CreatureInterpretations/projection-report.json` | Camera candidates and rough silhouette overlap |
| `Art/CreatureInterpretations/LiveSculptedDog.png` | Actual live Unreal capture |
| `Docs/CreatureInterpretations.md` | Detailed first-draft workflow and verification |
| `Docs/DefaultTileIteration.md` | Official-tile proxies, runtime display boundary |

Interpretations already made:
- Giant ant: brown segmented shell, thorax-mounted six legs, pinched waist,
  antennae/mandibles; cyan tile detail interpreted as eye glint.
- Little dog: ginger spitz/terrier, cream muzzle/bib, pointed ears, curled tail.
- Goblin: tan skin, green eyes, magenta cloth, leather cap, boots and dagger.
  Dagger is an art cue, not a guaranteed live inventory item.

The retained alternate is `Art/DefaultTiles/DefaultTileVolumes.blend`: 76
male/female tile-volume figures covering 13 roles and 25 common creatures.
These preserve sprite colours with inferred depth, mirrored rear and no rig;
they are a useful fidelity baseline, not anatomical reconstructions.

## Geometry/export pipeline and learned pitfalls

- `Scripts/CreateCreatureInterpretations.py`: native bpy geometry, connected
  sculpt unions, folded cloth; fixes normals, paints vertices, exports FBX,
  renders front-quarter/rear and six 16x16 projection candidates per creature.
- Helpers: `orb`, `box`, `limb`, `sculpt_union`, `ear`, `cloth`. Future variants
  should use parameterised family generators rather than copied full models.
- Limb tube frame: `right=direction.cross(helper).normalized()` then
  `up=direction.cross(right).normalized()`. Incorrect frame made bad topology.
- When inspecting a saved gallery, enable hidden collections/viewports and call
  `bpy.context.view_layer.update()` before reading world-space bounds. Hidden
  collections may have unevaluated object transforms on load, producing false
  below-floor readings. This is an inspection issue, not a reason to regenerate.
- Apply modifiers and recalculate face normals (`bmesh`) before painting/export.
  `Paint` colour attribute is `FLOAT_COLOR`, `CORNER`; Blender shader also reads
  this vertex colour so Blender and UE surfaces agree.
- Units: Blender metres; UE import centimetres. Floor origin, XY ground/Z up;
  gameplay cell is 100 UE units (1m). Existing sizes favour grid readability.
- FBX: mesh only, `use_selection=True`, `apply_unit_scale=True`,
  `axis_forward='-Y'`, `axis_up='Z'`, `mesh_smooth_type='FACE'`, no animation.
- `Scripts/RefitCreatureProjections.py`: rerender camera fits from saved blend.
  `Scripts/CreateCreatureComparison.py`: assemble actual render comparisons.
  `Scripts/FinalizeCreatureGallery.py`: organise the existing three collections.
- Align projection framing/shift to source coloured-pixel bounds; background
  and black shadow fringe are excluded heuristically. Render true 16x16, then
  enlarge nearest-neighbour. Compare three-quarter, rear and overview readability.
  Silhouette IoU is only a rough diagnostic, never proof of faithful anatomy.
- Initial meshes still differ from the source. Known iteration targets: ant
  angle/leg spread; dog head/chest proportions; goblin crouch/arm spread.
  Do not silently pass concept artwork off as geometry or UE output.

## Unreal integration constraints

- Import script: `Scripts/ImportCreatureInterpretations.py`, full UE editor
  startup Python, not nullRHI commandlet (Interchange needs Slate).
- Destination `/Game/CreatureInterpretations/Meshes/SM_<canonical_name_key>`.
  Shared vertex-colour materials: Paint, Chitin, Metal, Eye.
- **VertexColor combined output pin is unnamed `''`, not `'RGB'`** in this UE
  version. Assert shader connection returns true; a failed link made meshes
  appear white. Validate colour buffers after import.
- FBX options: static, combine meshes, transform vertex to absolute, import
  normals, replace vertex colours, replace asset AND import settings.
- Material slot name requires `get_editor_property('imported_material_slot_name')`;
  direct attribute access failed. Assign shared material by original pigment.
- Required import markers: `SCULPTED_CREATURE_IMPORTED` for each mesh and
  `SCULPTED_CREATURES_READY count=64` for the full current script
  (mixed `ImportSpecialBatch1.py` reports creature count 1 and `SPECIAL_BATCH1_IMPORT_READY count=3`). Immediate explicit editor
  quit caused Slate shutdown problems; startup script normally exits itself.
- `Source/NUthEck/DungeonLive.cpp::GetDefaultTileBatch` currently hardcodes the
  sixty sculpted identities, two female creature variants and two human player forms. Future expansion must extend/generalise selection;
  simply dropping a new FBX does not integrate it. Current sculpted yaw is 15°
  for goblin/gnomes/dwarfs/kobolds/orcs/floating eye and -75° for ant/dog/jackal/fox/rats/cats/wolves. New families need explicit orientation data.
- `-SculptedCreatures` launch option or **F9** selects optional sculpted candidates.
  Default remains tile-volume style. F9 rebuilds presentation without a game
  turn. Unsupported species retain existing representation and glyph badge.
- Hero batches are separate, allowing first-person to hide only the player.
- **Perception boundary:** select models only from displayed glyph identity.
  Bridge `winue.c` uses `glyph_to_mon` and displayed sex flags; no hidden-world
  monster lookup. Respect disguises, hallucination, invisibility and memory.
- `display_monster` is canonical neutral name; `female` is displayed sex.
  Names are normalised into asset keys. Duplicate form names remain a future
  identity issue; use explicit displayed-form IDs if fixing it, never hidden
  monster state. File-local tile index != runtime glyph/monster index.

## Environment and minimal validation

- Workspace: `C:/Users/agste/OneDrive/Development/nUthEck` (root is not a Git
  checkout; upstream NetHack is nested Git).
- Blender: `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe` (5.2.2).
- Unreal: `C:/Program Files/Epic Games/UE_5.7`; project `nUthEck.uproject`.
- Python/Pillow:
  `C:/Users/agste/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
- Blender background invocation: `--background --threads 4 --python <script>`.
  Capture output to a project log. Do not rerun a generator just to inspect.
- Close running UE instances before compiling the module or importing assets;
  loaded DLLs can block builds. Hidden background editor launches should use
  PowerShell `Start-Process -WindowStyle Hidden`.
- UE build: Engine `Build/BatchFiles/Build.bat NUthEckEditor Win64 Development
  -Project=<absolute .uproject> -WaitMutex -NoHotReloadFromIDE`.
- Existing three imports passed vertex-colour checks; live little-dog candidate
  loaded and capture passed native turns/map, zoom and hero centring. Actual F9
  switching both directions was verified at turn 5 (`build-sculpted-style-toggle.log`).
- For future asset changes, inspect actual studio renders and UE materials,
  verify source mapping/fallback and no-turn style toggle. Geometry remains
  unrigged; no animation or production performance claims have been validated.
- No UE build or mesh regeneration is required for catalogue/document changes.
- Batch 2 passed all six imports, both displayed sex aliases per new species,
  default fallback and unsupported identity checks, and F9 both ways at turn 5.
  Native map/zoom/hero checks passed. See `Docs/CreatureBatch2.md` and
  `build-creature-batch2-{unreal,import,live}.log` for evidence and limits.

- Batch 3 generation, native paint/gnome-body reuse inspection, nine imports,
  module build and live mapping/fallback/F9 checks passed. Evidence is in
  `Docs/CreatureBatch3.md` and `build-creature-batch3-*.log`.
- Batch 3 generator: `Scripts/CreateCreatureBatch3.py`; comparison:
  `Scripts/CreateCreatureBatch3Comparison.py`; native inspection:
  `Scripts/InspectCreatureBatch3.py`; live verification/capture:
  `Scripts/VerifyCreatureBatch3.ps1`. The shared `CreatureBatch2Pipeline.py` now
  accepts group/output names and preserves paint on reused family parts.

- Batch 4 geometry/paint/floor/age inspection, twelve imports, editor build and
  live mapping/fallback/F9 checks passed at turn 5. Source and actual render
  comparisons are in `Docs/CreatureBatch4.md`; evidence is in
  `build-creature-batch4-*.log`.
- Batch 4 generator/comparison/inspection/live scripts follow the Batch4 names
  in `Scripts/`. The live fixture test now supports batches 2/3/4/5/6/7/8/9/10/11/12 and prefers
  visible floor away from walls; batch 3/4/5/6/7/8/9/10/11/12 detail previews explicitly validate
  8x zoom, while ordinary zoom captures retain the 3x check.

- Batch 5 technical verification passed saved geometry/paint/floor/age/coat UVs,
  fifteen imports, editor build, six displayed sex forms, six fallback cases,
  unsupported identity and fur material/UV/colour buffers. F9 both ways kept turn
  5 unchanged; native map, hero centring and 8x preview zoom passed. Evidence:
  `Docs/CreatureBatch5.md`, `build-creature-batch5-*.log` and
  `Art/CreatureInterpretations/Batch5-Unreal-fixtures.png`.
- **Batch 5 winter-wolf correction:** removed cyan shadow-derived limb paint,
  ear lining and muzzle patches. Eyes now follow the actual skull surface and
  sit forward/inward behind the muzzle root, with small almond red apertures,
  dark pupils and pale lids. Check frontal symmetry and side/profile embedding;
  saturated red makes small placement errors conspicuous (explicit user concern).
  Do not restore the former side-mounted red globes. Preserve the cub's independent
  proportions. `WinterWolfEyes.py` is shared by repair and future generation.
- Saved repair preserved the ordinary wolf FBX byte-for-byte. Eye-review images
  are `Art/CreatureInterpretations/WinterWolf-EyeReview.png`; source and evidence
  are in `Docs/CreatureBatch5.md`. Camera matching now excludes cyan shadow pixels
  for these two identities. User visual acceptance is separate from technical
  validation; these remain static drafts.

- Winter-wolf revision reimport and live revalidation passed: both revised FBX
  imports, six displayed sex forms, six fallback cases, unknown identity,
  material/UV/paint checks and F9 both ways at unchanged turn 5. Native map,
  hero centring and 8x zoom passed. Revised studio, eye detail and actual Unreal
  fixture captures were inspected. Evidence: `build-winter-wolf-reimport.log`,
  `build-creature-batch5-{inspect,live,renders}.log` and
  `build-winter-wolf-eye-review.log`. Generation counts remain 15.

- Batch 6 completed dog, large dog and dingo. `CanidFamily.py` varies torso, skull,
  muzzle, limbs, ears, paws and tails independently: dogs have curled tails and a
  painted chest bib; dingo is leaner, long-muzzled, with pale underside and swept
  tail. New coats use texture-only fur; previous fifteen meshes were not regenerated.
  The shared fitted-eye helper accepts iris/lid pigments, preserving winter-wolf
  defaults. All new canids use amber eyes, small pupils and coat-coloured lids.
- Batch 6 passed saved native geometry, paint, fur UVs, floor clearance, eye
  symmetry, size/species distinctions; actual front/rear, six head detail views
  and eighteen true 16x16 projections were inspected. Three targeted imports and
  the editor build passed. Live checks passed six displayed sex forms, six
  fallback cases, unknown identity, fur materials/UV/colour buffers and F9 both
  ways with turn 4 unchanged. Native map, hero centring and 8x zoom passed.
  See `Docs/CreatureBatch6.md` and `build-creature-batch6-*.log`.
- Dog/large-dog camera fitting excludes blue-grey palette P under the muzzle as
  likely shadow, alongside black fringe/background. Dingo uses orange/peach coat
  masses with no black shadow socks. Original source tiles remain on comparisons.
  Static draft counts are now 18; finish work (rigs, animations, LODs, anatomy,
  coat-flow refinement) remains separate. The user positively reviewed the prior
  winter-wolf repair and then authorized this next batch.

- Batch 7 completed coyote, warg and rabid rat. Canid family options preserve
  prior defaults; coyote is leaner with long muzzle/tall ears/brush tail, warg has
  broader chest/skull, raised tail, pale fitted eyes, open red mouth and ivory fangs.
  Warg grey/blue-grey dithering is distributed through the body and interpreted
  as subtle coat shading, not blue shadow socks. Do not generalise the winter
  wolf correction into treating every interior blue-grey pixel as cast shadow.
- Rabid rat appends the exact reviewed lean sewer-rat anatomy and original Paint;
  native inspection verifies both position and paint hashes against the saved
  source. Preserve its snout, whiskers, ears, green eyes and lean form. New fur is
  texture-only on the continuous body. `CreatureSaliva.py` adds five small mouth
  froth masses and two short drool threads as detachable static state objects.
  No fat body, raised back overlay or ground puddle was added. The prior eighteen
  meshes were not regenerated.
- Batch 7 passed native geometry/paint/UV/floor, canid eye symmetry, distinct
  body proportions, exact rat-body reuse; actual front/rear, 18 true 16x16
  projections and six head views were inspected. Editor build and three targeted
  imports passed. Live validation passed six displayed sex forms, six fallback
  cases, unknown identity, coat materials/UV/colour buffers and F9 both ways at
  unchanged turn 5. Native map, hero centring and 8x zoom passed. Capture fixtures
  now prefer floor within three cells of the hero before scoring wall clearance;
  all three new models were inspected in the final engine capture.
  See `Docs/CreatureBatch7.md` and `build-creature-batch7-*.log`.
- `RefineCreatureBatch7State.py` is a one-time saved-scene review repair (mouth
  froth placement and warg jaw opening); the generator already has final values.
  Use `RenderCreatureBatch7.py` for inspection rerenders, not regeneration or
  repeated jaw offsets. Counts are now 21 generated static drafts, with anatomy,
  coat flow, rigs, flight/gait/attack animation, state effects and LODs still
  tracked separately as finish work.

- Batch 8 completed bat, giant bat and vampire bat using `BatFamily.py`:
  independently parameterised bodies/heads, wing span/chord and ear dimensions;
  forelimb wings, four elongated digits per side, free clawed thumbs, hind feet
  and tail membrane. Main membranes are curved panels following bent digit
  paths, solidified 3-4mm for real upper/lower geometry and shadows. Body alone
  uses texture fur; membranes are opaque painted skin, not alpha cards.
- Source bat silhouettes are above the detached ground shadows. Camera fitting
  now excludes rows 9-15 but retains upper black anatomy; vampire bat is not
  reduced to its red eye pixels. Frontal/oblique projection poses preserve wing
  breadth. Ordinary/giant bats use yellow eyes and brown tile-derived palettes;
  vampire bat has charcoal skin/fur, fitted red eyes, broader nose/head and wing
  chord, and reduced tail membrane. These are fantasy interpretations, not
  named zoological species reconstructions. All remain unrigged static flight
  poses; no wingbeat, landing, hanging or membrane animation is implemented.
- Batch 8 passed saved paint/UV/floor, paired eyes, digit/thumb counts, manifold
  membrane edges/nonzero faces and independent proportions. Actual front/rear,
  underside and face views plus 18 true 16x16 candidates were inspected. Editor
  build and three targeted imports passed. Live checks passed six displayed sex
  forms, six fallback cases, unknown identity, fur/paint/UV materials and F9 both
  ways with turn 5 unchanged. Native map, hero centring and 8x zoom passed.
  `Docs/CreatureBatch8.md` and `build-creature-batch8-*.log` record the evidence.
  The engine capture is inspected; foreground walls obscure portions of the
  larger bats, while studio/underside views show their full geometry.
- The initial flat wing panels were refined from saved geometry with
  `RefineCreatureBatch8Wings.py`; fresh generation already uses the final panels.
  Use `RenderCreatureBatch8.py` for saved rerenders. Wing-root folds, ear rims,
  anatomy refinement, rigs, flight/combat animation and LODs remain finish work.
  Current inventory is 24 generated static drafts; prior 21 FBX files were not
  regenerated. `Batch8-WingFaceReview.png` is the detailed new-family review.

- Batch 9 completed jaguar, lynx and panther. `FelineFamily.py` extends the
  established short paired-muzzle/digitigrade feline blockout with independent
  torso, head, paw, ear and tail dimensions. Jaguar is broader with painted
  rosettes, lynx has broad paws/short bobbed tail/attached ear tufts, and panther
  is longer/leaner with charcoal coat and yellow fitted eyes. Body texture fur
  remains the approved shared treatment; prior 24 FBX files were not regenerated.
- Jaguar rosettes and lynx cheek/flank colour are vertex paint on continuous
  anatomy. Do not recreate raised spot/saddle geometry or separate pale cheek
  ovals. Lynx tuft roots overlap the actual bevelled ears; do not restore the
  initially floating tufts. `RefineCreatureBatch9.py` applies the one-time saved
  review correction; fresh generation already contains the final values. Use
  `RenderCreatureBatch9.py` for saved inspection rerenders, not repeated offsets.
- New feline eyes use optional anterior orbital hints in the shared fitted-eye
  helper; earlier bat/canid defaults are preserved. Front/profile eye views and
  front-quarter/rear/16x16 comparisons were inspected. Panther black anatomy is
  retained in projection masks; only eight reviewed fringe pixels are excluded.
  Jaguar/lynx masks retain enclosed black markings. These remain approximate
  diagnostic masks, not proof of exact silhouette reconstruction. Panther blue
  accents are not painted into bright blue coat patches; lynx uses its actual
  orange/peach tiles, not the cyan ASCII colour.
- Batch 9 native geometry/paint/fur UV/floor/eye/proportion checks, editor build,
  three targeted imports and final live verification passed. Live checks cover
  six displayed sex forms, six fallbacks, unknown identity, fur/UV/paint materials,
  F9 both ways at unchanged turn 5, native map, hero centring and 8x zoom. See
  `Docs/CreatureBatch9.md` and `build-creature-batch9-*.log`.
- Automated captures now wait for actual native turn >=4 as well as their input
  count. A fast role can consume several movement inputs within one native turn;
  the prior fixed four-input stop could fail the unchanged turn>=4 smoke check.
  This affects capture automation only, not normal gameplay or F9 behaviour.
  Earlier account-limit approval review prevented a build from executing; it
  was resolved on the user's request to continue. Final build/import/live checks
  succeeded. Current generation inventory is 27 drafts; art refinement, rigs,
  animation/effects, LODs and performance remain separate finish work.

- The user explicitly approved the corrected jaguar coat as perfect. Preserve it.
- Jaguar's user-reference coat repaint is complete. Only `jaguar.fbx` was
  re-exported/reimported; dense irregular rosettes wrap over both flanks/spine,
  smaller spots cover the head/legs/muzzle, with pale underside and banded tail.
  `JaguarCoat.py` plus the optional shared shading hook keep fresh generation
  consistent with the saved repaint. Saved native signatures protect the approved
  lynx/panther; geometry/eye positions and inventory count 27 remain unchanged.
  Evidence: `Docs/JaguarReferenceRevision.md`, `build-jaguar-reference-*.log`,
  refreshed batch9 boards and `build-creature-batch9-live.log` (all checks pass).

- Batch 10 completed tiger, hell hound pup and hell hound. All prior 27 FBX files,
  including the user-approved jaguar, lynx and panther, match pre-batch hashes.
  `CreatureBatch10Paint.py` paints wrapping tapered/forked tiger stripes and a
  pale underside directly on the continuous body; no raised marking geometry.
  Hell hounds follow orange/red default-tile masses, not black shadow fringes.
  Independent pup/adult torso, skull, muzzle, leg and paw parameters preserve
  juvenile proportions. Fitted green/red eyes use the existing surface-conforming
  helper. Warm oral surfaces/canines supply the tile mouth cue; fire-breath VFX
  and animation remain future work, with mouth hooks saved in the native source.
- Batch 10 native paint/UV/floor/eye/age/stripe checks, six studio views,
  eighteen true 16x16 projections, six head views, editor build and three targeted
  imports passed. Final live checks passed six displayed sex forms, six fallbacks,
  unknown identity, fur/paint/UV, F9 both ways at unchanged turn 5, native map,
  hero centring and 8x zoom. Engine fixtures were inspected; walls and badges
  obscure portions of the hounds. Use studio/head views for unobscured review.
  Evidence: `Docs/CreatureBatch10.md`, `build-creature-batch10-*.log`,
  `Art/CreatureInterpretations/Batch10-Models.png` and associated comparisons.
  Current inventory: 30 static drafts; 351 creature IDs and 13 player roles remain.
  Next suggested batch: pony/horse/warhorse. No rigs, breath animation, LODs or
  production performance budget is claimed complete.

- Batch 11 completed pony, horse and warhorse with a new `EquineFamily.py`:
  continuous barrel/haunch/shoulder/neck/poll/jaw/nasal bridge anatomy, jointed
  forelegs/hind hocks and four separate single hooves. Pony is a compact stocky
  equine type, not a claim that ponies are all juveniles. Adult horse and warhorse
  have independent proportions; warhorse broadens the chest, neck, head and hooves.
  Chestnut coats, brown manes/tails, pale hooves and small blue eyes follow the
  actual tiles. The offset black neck/foot/tail fringe is cast shadow; reviewed
  mouth pixels are retained in diagnostic masks. No clear tack appears in these
  tiles, so no saddle/bridle/armour was added. Source traits and assumptions are
  recorded separately in `Docs/CreatureBatch11.md`.
- New `EquineEyes.py` fits lateral eyes and horizontal pupils onto the skull;
  previous eye helpers remain unchanged. Inner ears fit evaluated closed ear
  surfaces; the mane follows the actual rear-neck silhouette. Initial buried
  mane/detached lining shapes were repaired in the saved scene using
  `RefineCreatureBatch11.py`; fresh generation already uses the final helpers.
  Short coats use approved texture-only fur. Mane/tail are continuous long-hair
  silhouette masses, with no individual strands. Saved review scripts render
  existing geometry; do not regenerate or repeat repair simply to inspect.
- Batch 11 native paint/UV/floor/eyes/hooves/ear-fit/proportion checks passed;
  six studio views, 18 true 16x16 projections and six head views were inspected.
  Editor build and three targeted imports passed. Final live checks passed six
  displayed sex forms, six fallbacks, unknown identity, fur/paint/UV, F9 both ways
  at unchanged turn 5, native map/hero centring and 8x zoom. Engine capture inspected;
  badges obscure parts of two fixtures. Unobstructed studio/head views are alongside.
  All 30 earlier exports, including user-approved batch 10, match saved hashes.
  Evidence: `Docs/CreatureBatch11.md`, `build-creature-batch11-*.log`,
  `Art/CreatureInterpretations/Batch11-Models.png` and associated comparisons.
  Current inventory is 33 static drafts; 348 creature IDs and 13 player roles
  remain. Next suggested batch: white/gray/black unicorns. Rigs, gait/attacks,
  riding/tack state, mane grooming, LODs and performance remain finish work.

- Before further creatures, the user requested and received the F7 entity-label
  toggle and facing-aligned first-person camera curve. Final editor/live checks
  pass; 240 path cases, eight actual heading/reversal checks, label on/off and
  timed camera restoration preserve native turn/sequence. See
  `build-presentation-controls-{unreal,live}.log`, `Scripts/VerifyPresentationControls.ps1`
  and `Docs/Images/PresentationControls/`. Creature inventory stays 33; next
  suggested batch remains white/gray/black unicorns.

- Batch 12 completed white/gray/black unicorns using `UnicornFamily.py` and the
  equine family. Matching source size/attacks support identical body anatomy,
  verified by vertex hashes; each identity/export/displayed sex form is separately
  checked. Blue/green/red lateral eyes retain fitted apertures/horizontal pupils.
  One closed, gold/cool-painted spiral horn is fitted 6mm into each forehead.
  No alignment jewellery, armour, aura, wings or tack was invented. Source
  alignments +7/0/-7 remain metadata; poison resistance and attacks are recorded.
- Unicorn palettes follow actual tiles: white/blue mane, blue-gray/white mane,
  charcoal/brown mane. Tails follow coat colours. Initial matching-mane tail
  colours were corrected with saved paint-only `RefineCreatureBatch12Palette.py`;
  every vertex remained unchanged and fresh generation uses the final pigments.
  The white blue neck column occupies the same position as other mane stripes,
  separate from the offset black shadow. Black unicorn's black anatomy is retained
  using paired white-tile spatial coordinates; the blue-gray outer fringe is
  shadow, not blue socks. Do not blanket-remove black or blue-gray palettes.
- Batch 12 saved paint/UV/floor/eyes/ear-fit/hooves/horn closure+attachment,
  palette/body-hash and 33 prior-export checks passed. Six studio views, 18 true
  16x16 projections and six head views were inspected. Editor build and final
  three targeted imports passed. Final live checks passed six displayed sex
  forms, six fallbacks, unknown identity, fur/UV/paint, F9 both ways at unchanged
  turn 4, native map/hero centring and 8x zoom. Engine capture inspected with
  labels hidden; all three new fixtures are clearly visible.
  `-HideEntityGlyphs` optionally starts a game/capture with labels off; F7 restores
  them. Ordinary launches still start with labels on. New batch capture uses this
  flag; keep the user's new F7/camera controls intact when expanding selection.
  Evidence: `Docs/CreatureBatch12.md`, `build-creature-batch12-*.log`,
  `Art/CreatureInterpretations/Batch12-Models.png` and associated comparisons.
  Current inventory: 36 static drafts, 345 remaining creature IDs and 13 player
  roles. Next suggestion: kobold/large kobold/kobold leader. Rigging, grooming,
  gait/headbutt/kick animation, effects, LODs and performance remain finish work.

- Requested human player work completed (2026-10-31): female Valkyrie and male
  Barbarian. `CreateHumanPlayers.py` / `HumanPlayerFamily.py` generate the forms;
  `InspectHumanPlayers.py` and `ReviewHumanPlayers.py` inspect saved geometry.
  Tile-derived blond hair, blue/green eyes, Valkyrie leather tunic/skirt/boots and
  Barbarian bare chest/leather wrap are art presentation, not live inventory.
  Do not interpret the common right-side black fringe as a giant held shield.
  No held weapon or horned helmet was inferred. Prior 36 FBX hashes are unchanged.
- New own-player bridge status fields `hero_race` / `hero_polymorphed` come from
  `gu.urace.noun` / `Upolyd`. They expose known player status, never hidden NPC
  ancestry. Role/sex selection still uses the displayed glyph. Only matching
  human hero forms use the new meshes; orc/dwarf, unsupported sex, unknown race,
  polymorph and NPC role appearances retain existing fallbacks. The hero batch
  uses 15-degree yaw for the human meshes and hides its whole combined costume
  during first person. Keep F7, F9 and the camera curve intact.
- Bridge and editor builds, 4 native ancestry profiles, existing bridge smoke,
  saved body/paint/eye/floor/icon checks and two final imports pass. Each
  live profile passes 11 selection/fallback cases, first-person hiding/restoration,
  native movement/map/8x zoom and real F9 toggles at unchanged turn 5/sequence 5.
  Actual hero captures are inspected. Native triangles: 155,408 Valkyrie /
  183,888 Barbarian. Source/evidence: `Docs/HumanPlayers.md`,
  `build-human-players-*.log`, `build-human-player-*-live.log`,
  `Art/CreatureInterpretations/HumanPlayers-Models.png` and associated boards.
- Inventory now distinguishes physical forms from completed identities: 36
  creature drafts + 2 requested human player forms = 38 forms. The 394-ID backlog
  has 36 completed creatures, 1 completed role (Valkyrie), 345 remaining creatures,
  and 12 remaining roles (including partial male-only Barbarian). Do not mark
  female Barbarian generated or duplicate role IDs. `players.json` sex nodes
  and source-record statuses capture this scope. Next creature suggestion stays
  kobold/large kobold/kobold leader. Rigging, facial/cloth refinement, animation and performance remain finishing work.

- Human icon revision: each saved character and FBX now has one mesh object,
  with painted surfaces joined after construction and no detachable-clothing
  objects/metadata. The Valkyrie's brown legwear and Barbarian's short waist
  garment replace the earlier skirt-like interpretations. Preserve faces/hair/eyes,
  ancestry/sex mapping and other models. See `Docs/HumanPlayers.md` for current checks.

- Batch 13 completed kobold, large kobold and kobold leader. `KoboldFamily.py`
  independently varies height/chest/head/arm proportions. Actual cyan/blue skin,
  pale ear tips and orange leader hood/tunic follow the official tiles; dog-like
  muzzles follow the encyclopedia. Offset black shadow is excluded spatially,
  retaining enclosed dark details. No shadow-derived cape/tail/shield, invented
  weapon/crown, unsupported scales or fur was added. Sex-neutral family forms
  serve both identical displayed tile sexes.
- Initial arm/tip geometry was corrected; tips are now paint on the actual ears.
  Saved leader cloth/belt was refitted using `RefineCreatureBatch13Garment.py`;
  fresh generation has final oval shells. Do not repeat the one-time repair to
  inspect. `RenderCreatureBatch13.py`/`ReviewCreatureBatch13.py` render saved meshes.
  Native paint/floor/eye/proportion/rank checks pass. All prior 38 creature/player
  FBX hashes are unchanged. Six studio views, six head views and all 18 true
  16x16 projections were inspected, followed by the actual engine fixture capture.
- Editor build, three targeted imports, six displayed sex forms, six fallbacks,
  unknown identity and paint checks passed. F9 both ways kept native turn 5
  unchanged; movement/map, hero centring and 8x zoom passed. All three fixtures
  are visible with labels hidden. Evidence: `Docs/CreatureBatch13.md`,
  `Art/CreatureInterpretations/Batch13-Models.png` and `build-creature-batch13-*.log`.
  Current baseline: 39 creatures + 2 human player forms = 41 physical forms;
  394 identities = 39 completed creatures + 1 completed role + 342 remaining
  creatures + 12 remaining roles. Suggested next: kobold shaman/mummy/zombie.
  Face/cloth refinement, rigs, animation, dynamic equipment, LODs and performance
  remain finishing work. Preserve the player fixed-clothing rule and F7/camera controls.

- First non-creature batch completed: large box (`LARGE_BOX`), chest (`CHEST`)
  and gold piece (`GOLD_PIECE`). See `Docs/ObjectBatch1.md` and
  `Art/ObjectInterpretations/ObjectBatch1.blend`. These are separate from the
  39-creature/2-player inventory; all 41 prior FBX hashes are unchanged.
  `ObjectFamily.py`/`CreateObjectBatch1.py` reuse geometry/paint/render utilities;
  `InspectObjectBatch1.py` and `RenderObjectBatch1.py` inspect saved work.
- New bridge `display_object` whitelists these three non-randomised appearances
  from the displayed glyph only (normal and pile-top), with no quantity,
  contents, lock/trap or hidden-object lookup. Parser clears it on each update.
  `GetDisplayedObjectBatch` selects `/Game/ObjectInterpretations` assets only
  for item displays; other items retain spheres. Objects appear in both F9
  creature styles and use separate dim remembered materials. Creature F9,
  F7, human ancestry guards and first-person controls are preserved.
- Object batch passed saved paint/closed geometry/floor/lid checks, six studio
  views and 18 true 16x16 projections, bridge/editor builds, three imports,
  native wish/drop/reveal tests (including pile-top gold), existing bridge smoke,
  visible/memory/material/fallback checks, F9 both ways with turn/sequence
  unchanged, and native map/8x zoom. Actual engine capture inspected.
  Registry: `Art/ObjectInterpretations/object-assets.json`; complete object
  inventory remains pending. Opening/looting animation, carried state,
  quantity-aware coin arrangements, refinement and LODs remain finish work.

- General official-tile fallback added after object batch 1 (2026-10-31).
  Existing selected 3D meshes retain priority. Unsupported entities now use
  transparent camera-facing official tile cards before generic markers; this
  includes creatures, items, effects and unsupported hero forms. Terrain stays
  on its existing 3D renderer. F9 still switches creature styles, retaining the
  older tile-volume proxies where available. See `Docs/TileFallback.md`.
- Native `tile_index` is `fg->gm.tileidx`, using compiled `tile.c` and
  `TILES_IN_GLYPHMAP` plus NetHack's native appearance shuffling. Never replace
  it with a guessed glyph offset, unshuffled object index or hidden-world lookup.
  `CreateOfficialTileAtlas.py` reads all 2,304 slots, including 17 generic object
  entries with interleaved comments and native grayscale statue variants.
  Keep atlas/header/import/bridge in sync when source changes.
- Cards share one two-triangle mesh/atlas/material, retain original dark pixels,
  use nearest filtering and transparent backgrounds, follow the view with floor
  anchoring, dim memory and hide a sprite hero in first person. Missing/invalid
  metadata retains the old last resort. All 41 creature/player and three object
  exports stay unchanged; model completion counts stay unchanged.
- Bridge/editor/import/live verification passed, including six shuffled potion
  appearances across two native games with save/restore, existing bridge smoke
  and object tests, three fallback tiles, visible/memory data, model priority,
  eight camera headings, floor anchors, player hiding/restoration, native map,
  8x zoom and F9 both ways with unchanged turn/sequence. Actual capture inspected:
  `Art/TileFallback/TileFallback-Unreal.png`; `build-tile-fallback-*.log`.

- Batch 14 completed kobold shaman, kobold mummy and kobold zombie using
  `KoboldStates.py`. Shaman appends the exact saved leader body/garments with
  yellow caster paint; mummy/zombie append the large-kobold body. Saved vertex
  hashes match reference anatomy exactly. Mummy has 14 separately editable,
  solid linen ribbons fitted within 4.5mm of anatomy; zombie has broad blue/green
  skin paint. Dog-like faces, pale ear tips and paired dark eyes are preserved.
  No staff, crown, invented inventory, aura or graphic wound was added.
- Saved wrap review repaired ankle-derived foot spikes and revised jaw/crown
  wraps using one-time `RefineCreatureBatch14Wraps.py`; fresh generation already
  has final values. Use `RenderCreatureBatch14.py`/`ReviewCreatureBatch14.py`
  to inspect saved work. All 45 prior exports (41 creature/player, three objects,
  tile quad) retain pre-batch hashes. Native geometry/paint/floor/eye/closed-wrap
  checks pass. Six studio views, six heads and all 18 true 16x16 projections
  were inspected. Outer black shadow is excluded spatially, with enclosed
  dark details retained.
- Editor build and three imports pass. Six displayed sex forms, six default
  fallbacks, unknown identity and paint checks pass. All six new official tile
  cards are verified in default style. F9 both ways preserves turn 5/sequence 7;
  movement/map, hero centring and 8x zoom pass. Actual engine capture inspected,
  all three forms visible. See `Docs/CreatureBatch14.md`,
  `Art/CreatureInterpretations/Batch14-Models.png` and `build-creature-batch14-*.log`.
  Current baseline: 42 creatures + 2 player forms = 44 physical forms;
  394 IDs = 42 completed creatures + 1 completed role + 339 remaining creatures
  + 12 remaining roles. Three object assets remain separately tracked.
  Next suggestion: gnomish wizard/gnome mummy/gnome zombie. Cloth/face/linen
  refinement, zombie accents/pose, rigs, casting/undead animation/effects, LODs
  and performance remain finish work. Preserve F7/F9/camera and tile fallback.

- Batch 15 completed gnomish wizard, gnome mummy and gnome zombie. All five
  physical forms append the exact saved `gnome_body` from batch 2. Green pointed
  caps and ancestry are preserved; original axe and red cap-tip modules are
  omitted for these tiles. Wizard/zombie have fitted curved belts; mummy has
  ten closed solid linen ribbons fitted within 4.5mm, pale wrapped-foot masses
  and red eyes. Zombie has green skin, ash-gray male beard and red eyes.
- Actual sex-tile review found beardless female wizard/zombie variants, unlike
  the identical mummy pair. Added only two female forms to the saved scene using
  one-time `CreateCreatureBatch15FemaleForms.py`; fresh generator includes them.
  Do not rerun the addition to inspect. Use `RenderCreatureBatch15.py` and
  `ReviewCreatureBatch15.py`. `batch15-forms.json` maps five forms to three IDs.
  Female geometry shares the exact ancestry body; only source-supported facial
  hair/brow treatment differs, with no further sex-anatomy claim.
- Native paint/geometry/floor/eyes/red pigment/closed linen/ancestry checks pass;
  all 48 prior exports (44 creature/player, three objects, tile quad) are unchanged.
  Ten studio views, ten head views and all 30 true 16x16 projections inspected.
  Editor build and five targeted imports pass. Displayed sex now selects female
  assets for wizard/zombie; mummy shares one mesh. Six displayed cases, six
  official tile fallbacks, unknown identity and paint pass. F9 both ways keeps
  turn 5/sequence 7 unchanged; native movement/map, hero centring and 8x zoom pass.
  Actual engine capture inspected. See `Docs/CreatureBatch15.md`,
  `Art/CreatureInterpretations/Batch15-{Models,FemaleModels}.png` and associated logs.
- Baseline: 45 completed creature IDs + 1 completed role + 336 remaining
  creature IDs + 12 remaining roles = 394 unique IDs. Physical creature/player
  forms total 49 (45 primary creatures + 2 female variants + 2 human players).
  Three object assets remain separate. Next suggestion: dwarf/leader/ruler,
  reviewing both sex tiles. Face/cloth/linen refinement, zombie pose/paint,
  rigs, casting/undead animation/effects, LODs and performance remain finish work.
  Preserve the player fixed-clothing rule and F7/F9/camera/tile fallback.


## Batch 16: dwarf ancestry and ranks (2026-10-31)

- Dwarf, dwarf leader and dwarf ruler now have verified static drafts. Both sex
  tiles are identical for each rank; the tile artist explicitly intended shared
  appearances. There are three physical meshes, with exact common body hashes.
- New stout ancestry, blue/cyan painted clothes/cap, pale fitted beard and seated
  eyes. Leader band and ruler crown are separate. Shadow pixels were not turned
  into weapons. Crown points are flat metal shapes; orange inlays meet the band.
- Saved Blender geometry/paint/floor/eyes/closed-tunic/rank inspection passes;
  all 49 preceding creature/player FBX hashes are unchanged. Native draft costs
  are 154348 / 154860 / 157232 triangles, so LOD/performance work remains.
- Targeted three-mesh import, colour buffers, all six displayed sex cases, six
  respective official tile fallbacks, unknown identity, F9 both ways at unchanged
  turn 5/sequence 7, native map, hero centring and 8x zoom pass. Actual studio
  front/rear, head views, all 18 true 16x16 projections and live capture inspected.
- See `Docs/CreatureBatch16.md`, `Art/CreatureInterpretations/Batch16-Models.png`
  and `build-creature-batch16-{blender,refine,review,inspect,unreal,import,live}.log`.
  Fresh generation includes the crown correction; do not repeat the one-time
  `RefineCreatureBatch16.py` to inspect. Use saved render/review scripts.
- Current baseline: 48 generated creatures + one completed role + 333 remaining
  creatures + 12 remaining roles = 394 unique source IDs. 52 physical forms:
  48 primary creatures + two female creature variants + two human players.
  Objects stay separate. Next suggested family extension: dwarf mummy/zombie.
- Windows now defaults to DX12/SM6 for actual Virtual Shadow Maps. SM5 silently
  fell back to conventional shadows and lost the overhead creature shadows;
  preserve `Config/DefaultEngine.ini`'s Windows shader target configuration.


## Batch 17: dwarf undead states (2026-10-31)

- Dwarf mummy and dwarf zombie now have verified shared-sex static drafts.
  Both sex tiles are identical for each identity. `DwarfStates.py` appends the
  exact saved dwarf anatomy from batch 16; body hashes match the source.
- Mummy retains the blue cap/pale beard and adds eleven closed, solid linen
  ribbons fitted within 4.6mm. Blue boots become pale; blue tunic/sleeves/trousers
  are omitted. Red eyes follow the face accent; a small red cloth band interprets
  the ambiguous shin pixel without inventing gore. Zombie keeps the blue costume,
  green skin, ash-blue beard and dark eyes. Cast shadows are excluded spatially.
- Saved geometry, paint, floor, eye fit, closed linen and ancestry checks pass;
  all 56 earlier FBX exports (52 creature/player, three objects, tile quad) remain
  unchanged. Four studio views, four heads and all twelve true 16x16 projections
  were inspected. Native triangles are 117636 / 154348; LOD/runtime work remains.
- Editor build and both imports pass. Four displayed sex cases, four respective
  official tile fallbacks, unknown identity and paint buffers pass. F9 both ways
  retains turn 5/sequence 7; native map, hero centring and 8x zoom pass. Actual
  engine capture inspected with both fixtures unobstructed and casting shadows.
- Evidence: `Docs/CreatureBatch17.md`, `Art/CreatureInterpretations/Batch17-Models.png`
  and `build-creature-batch17-{blender,review,inspect,unreal,import,live}.log`.
  Use `RenderCreatureBatch17.py` / `ReviewCreatureBatch17.py` to inspect saved work.
- Current baseline: 50 completed creatures + one completed role + 331 remaining
  creatures + 12 remaining roles = 394 unique source IDs. 54 physical forms:
  50 primary creatures + two female creature variants + two human players.
  Three objects remain separate. Next suggestion: hobgoblin/hill orc/Mordor orc,
  reviewing both sex tiles and ancestry compatibility before modelling.
  Linen/face/beard refinement, undead pose, rigs, animation/effects, LODs and
  performance remain finishing work. Preserve fixed player clothing, F7/F9,
  first-person controls, official tile fallback and DX12/SM6 shadow configuration.


## Batch 18: hobgoblin and upright orcs (2026-10-31)

- Hobgoblin, hill orc and Mordor orc have verified shared-sex static drafts.
  Each official male/female tile pair is identical. `OrcFamily.py` appends the
  saved goblin for hobgoblin with object stature factors 1.06/1.05/1.10 and yellow
  irises. All local vertex signatures remain identical; degenerate inherited
  ear faces are removed only in the derivative. Original goblin is untouched.
- Hill/Mordor orcs share a new complete upright body with equal vertex hashes,
  pale helmet, fitted shoulder-covering sleeves, hip-covering tunic, trousers
  and separate held rod/blade cues. Hill orc uses peach skin/green-lime cloth;
  Mordor uses blue-gray skin/magenta cloth/red belt/cyan rod. Source shadows
  are excluded spatially. Held items/cape are art interpretations, not native
  inventory promises. No hidden-world identity/equipment lookup is used.
- Native saved geometry/paint/floor/eye/closed-cloth/ancestry checks pass; all
  58 previous FBX exports (54 creature/player, three objects, tile quad) retain
  their hashes. Native triangles are 55610 / 101692 / 101692. Six studio views,
  six head views and all 18 true 16x16 candidates were inspected.
- Editor build, three targeted imports, six displayed sex forms and their six
  official tile fallbacks, unknown identity and paint buffers pass. F9 both ways
  preserves turn 5/sequence 7. Native map, hero centring and 8x zoom pass. Final
  engine capture inspected with all three fixtures clearly visible; first capture
  was retained separately because a wall partly obscured Mordor orc.
- Evidence: `Docs/CreatureBatch18.md`, `Art/CreatureInterpretations/Batch18-Models.png`
  and `build-creature-batch18-{blender,refine,review,inspect,unreal,import,live}.log`.
  Fresh generation includes shoulder/hip garment and degenerate-face repairs.
  Do not repeat one-time `RefineCreatureBatch18.py` to inspect; use saved
  `RenderCreatureBatch18.py` / `ReviewCreatureBatch18.py`.
- Baseline: 53 completed creatures + one completed role + 328 remaining creatures
  + 12 remaining roles = 394 IDs. Physical creature/player forms: 57 (53 primary
  creatures + two female creature variants + two human players). Three objects
  remain separate. Coverage: 53/381 creature drafts = 13.9%, or 54/394 source
  creature/player identities = 13.7%; rigging/animation/finishing is separate.
  Next: Uruk-hai/orc shaman/orc-captain, reviewing both sex tiles/source traits and
  ancestry compatibility first. Faces, cloth/equipment, rigs, motion/effects,
  LODs and runtime costs remain finishing work. Preserve F7/F9/camera, player
  fixed clothing, official tile fallback and DX12/SM6 shadows.


## Batch 19: requested early-level trio (2026-10-31)

- User requested floating eye, newt and lichen, ahead of the suggested orc batch.
  All three now have verified static drafts. Their official sex tile pairs are
  identical; eye and lichen are source-neuter. Each has a separate body plan.
- `EarlyDungeonCreatures.py` builds a complete white globe with a closed curved
  cyan/blue/dark iris aimed 20 degrees upward and 405mm hover clearance; a
  connected orange/peach newt with four splayed legs, toes, curved tapering tail
  and eyes fitted within 1mm; and one complete scalloped foliose lichen thallus,
  green with painted orange/pale patches. Lichen has no eyes/head/limbs/stem.
  Tile-shadow pixels are excluded spatially; original comparison tiles remain
  unmodified. Hidden anatomy, scale, toe completion and lobe layout are art.
- Saved geometry, paint, closure, hover, iris radius/palette, connected bodies,
  four feet, eye fit and fungal pigment checks pass. All 61 earlier exports
  (57 creature/player, three objects, tile quad) retain their hashes. Native
  triangles: 7360 / 85820 / 87364; no production performance claim.
- Editor build and three imports pass. Six displayed sex cases, their six
  official tile fallbacks, unknown identity and paint buffers pass. F9 both ways
  preserves turn 5/sequence 7. Native map, hero centring and 8x zoom pass. Six
  studio views, six detail views, all 18 true 16x16 candidates and actual live
  capture inspected, with all three fixtures clearly visible.
- Evidence: `Docs/CreatureBatch19.md`, `Art/CreatureInterpretations/Batch19-Models.png`
  and `build-creature-batch19-{blender,review,inspect,unreal,import,live}.log`.
  Inspect saved work with `RenderCreatureBatch19.py` / `ReviewCreatureBatch19.py`.
- Current baseline: 56 completed creatures + one completed role + 325 remaining
  creatures + 12 remaining roles = 394 source IDs. Physical creature/player
  forms: 60 (56 primary + two female creature variants + two human players).
  Three objects remain separate. Creature draft coverage is 56/381 = 14.7%;
  creature/player identity coverage is 57/394 = 14.5%. Finishing/rigging/animation
  remains separate. Next suggestion stays Uruk-hai/orc shaman/orc-captain.
  Eye/cornea shading, newt toes/pose/skin and lichen edges/paint, rigs, motion,
  effects and LOD/runtime cost remain finish work. Preserve existing models,
  F7/F9/camera, player fixed clothing, tile fallback and DX12/SM6 shadows.


## Batch 20: upright orc caster/ranks (2026-10-31)

- Uruk-hai, orc shaman and orc-captain have verified shared-sex static drafts;
  each actual male/female tile pair is identical. `OrcRanks.py` appends the
  saved batch-18 `mordor_orc` collection. All three body vertex hashes match
  that saved ancestry exactly. Shared gray skin gains peach cheek paint.
- Uruk-hai adds a separate closed curved blue-gray shield with red centre paint
  and a back grip fitted to the retained hand, replacing the short blade.
  Magenta cloth and a pale waist accent are retained. Shaman omits the blade,
  uses orange/brown costume and a green belt, and adds no invented magic effect.
  Captain retains the blade, adds a separate closed wider helmet rim, and uses
  red shoulder/green chest/magenta lower cloth paint. Cyan rods, white waist
  interpretation and precise equipment shapes are art cues, not inventory
  promises. No shadow-derived anatomy, horn, crown or extra insignia is added.
- Saved geometry/paint/floor/eye/ancestry/closed-state-module/shield-fit checks
  pass; all 64 prior exports (60 creature/player, three objects, tile quad) are
  unchanged. Native triangles: 102844 / 101648 / 102716. Six studio views, six
  heads and all 18 true 16x16 candidates were inspected.
- Editor build and three imports pass. Six displayed sex forms, six respective
  official tile fallbacks, unknown identity and paint buffers pass. F9 both ways
  preserves turn 5/sequence 7. Native map, hero centring and 8x zoom pass. Actual
  engine capture inspected; all three fixtures are clearly visible. Fixture
  package expectations now normalise case/spaces/hyphens like runtime keys,
  including Uruk-hai/orc-captain. Live orientation is 15 degrees.
- Evidence: `Docs/CreatureBatch20.md`, `Art/CreatureInterpretations/Batch20-Models.png`
  and `build-creature-batch20-{blender,review,inspect,unreal,import,live}.log`.
  Inspect saved work with `RenderCreatureBatch20.py` / `ReviewCreatureBatch20.py`.
- Current baseline: 59 completed creatures + one completed role + 322 remaining
  creatures + 12 remaining roles = 394 source IDs. Physical creature/player
  forms: 63 (59 primary + two female creature variants + two human players).
  Three objects remain separate. Creature draft coverage 59/381 = 15.5%;
  creature/player identity coverage 60/394 = 15.2%. Finishing, rigging and
  animation remain separate. Next suggestion: orc mummy/orc zombie, reviewing
  sex tiles/state modules/source traits first. Cloth/face/shield/grip/rim,
  rigs, spells/attacks/defence, effects, LOD/runtime review remain finish work.
  Preserve F7/F9/camera, fixed player clothing, tile fallback and DX12/SM6 shadows.


## Special batch 1: grid bug, corpse and fountain (2026-10-31)

- User requested one creature, generic corpse and a beautiful fountain. All
  three have verified static assets. `SpecialAssetGeometry.py` creates six red
  angular legs/antennae, blue head/thorax and pale yellow/orange abdomen for
  grid bug; generic collapsed remains/pale fragments for corpse; and a carved
  pale stone basin/foot/fluted centre, petal relief, six static blue water arcs
  and still ripple rings for fountain. Grid bug has no wings/M1_FLY; its broad
  catalogue group is not a source flight trait. Both sex tiles are identical.
- Follow current static `GameVision.md`: no rigs/animation are required or
  planned. Water is glossy opaque static geometry, without timed shaders.
  Corpse geometry does not assert species, sex, size, freshness, poison or
  edibility. Fountain shows no magical/blessed/looted status. Hidden anatomy
  and architectural details are art interpretations, with original source
  tiles preserved and exterior shadows spatially excluded.
- Editable mixed source: `Art/SpecialBatch1/SpecialBatch1.blend`; canonical FBX
  exports go to CreatureInterpretations/grid_bug, ObjectInterpretations/corpse
  and EnvironmentInterpretations/fountain. Registries: existing object-assets
  JSON now has four entries; terrain-assets JSON has one fountain feature.
  Shared pipeline optional `SOURCE_TILE_ENTRIES` and `EXPORT_PATHS` leave old
  defaults intact. Use saved Render/ReviewSpecialBatch1 scripts to inspect.
- Native geometry/paint/closed-surface/floor/six-leg/static-water checks pass;
  all 67 old exports (63 creature/player, three objects, quad) are unchanged.
  Triangles: 16648 grid bug / 27224 corpse / 36624 fountain. Thin water bevel
  was repaired once with `RefineSpecialBatch1Water.py`; fresh generation includes
  the correction. Do not repeat the repair for inspection.
- Bridge emits generic `display_object: corpse` from displayed normal/pile-top
  corpse glyphs, with no corpse monster identity or world-object lookup.
  Native wizard tests for newt/giant-rat corpses match tile 1056. Fountains and
  sinks now emit separate terrain strings; only known fountain terrain selects
  the new feature. Object selection respects item kind and memory materials.
- Bridge/editor builds, three final imports, native corpse/fountain/sink tests,
  existing object/smoke tests and final live checks pass. Both bug sexes and
  official fallbacks, both styles, corpse/fountain normal/memory materials,
  sink/floor/unknown guards, F9 both ways at turn 5/sequence 7, map, hero centring
  and 8x zoom pass. Six studio/close views, all 18 tiny projections and actual
  engine capture inspected. Final capture shows all three fixtures clearly,
  plus an actual native fountain; first wall-obscured capture is retained.
- Evidence: `Docs/SpecialBatch1.md`, `Art/SpecialBatch1/SpecialBatch1-Models.png`,
  `mesh-inspection.json` and `build-special-batch1-*.log`.
- Baseline: 60 completed creatures + one completed role + 321 remaining creatures
  + 12 remaining roles = 394 IDs; 64 physical creature/player forms. Four object
  presentations and one fountain feature stay separate. Creature coverage
  60/381 = 15.7%, creature/player coverage 61/394 = 15.5%. Next suggestion stays
  orc mummy/orc zombie. Refinement, LOD/runtime cost remain finish work; rigs and
  animation are out of scope. Preserve F7/F9/camera, fixed player clothing,
  tile fallback and the latest carved-stone environment materials/shadows.

# Shopkeeper and five altar appearances

Requested mixed batch, 2026-11-02: one creature identity with a shared sex
appearance, and one terrain feature with five displayed variants. These are
verified static drafts; visual finishing and runtime budgets remain separate.

## What NetHack actually displays

Female shopkeepers exist. `src/shknam.c:486` assigns sex as part of choosing a
name; `-`/`_` name prefixes select female and `+`/`|` select male. Izchak is an
explicit male special case. The official shopkeeper male/female tiles 554/555
are byte-for-byte identical, so both displayed sexes use one model. This is
shared icon appearance, not a claim that all shopkeepers have male anatomy.

`PM_SHOPKEEPER` (`include/monsters.h:2707`) is human-sized, level 12,
difficulty 15, with two 4d4 physical weapon attacks, peaceful/strong/collecting/
magic-using flags, and no polymorph. Those are native capabilities, not an
inventory promise. No held weapon, bag, shield or visible hostility state was
invented from the dark right-side tile shadow.

Altars do **not** all share an appearance in this pinned NetHack 5.0 source:

| Displayed variant | Official other.txt tile / combined atlas | Interpretation |
| --- | --- | --- |
| Unaligned | 33 / 1305 | Near-black stone, red top markings |
| Chaotic | 34 / 1306 | Dark gray stone, red top markings |
| Neutral | 35 / 1307 | Blue-gray stone, red top markings |
| Lawful | 36 / 1308 | Pale stone, sparse red top markings |
| Other | 37 / 1309 | Magenta stone with white ray inlay |

An opposing god's altar retains its native lawful/neutral/chaotic appearance.
“Unaligned” is its own native alignment, not shorthand for “opposed to you.”
`include/display.h:569` maps `AM_SANCTUM` to the special `altar_other` glyph;
otherwise the native alignment mask selects lawful, neutral, chaotic or
unaligned. High altars therefore follow the special displayed appearance,
without revealing an underlying alignment by consulting hidden terrain data.

## Geometry, paint and interpretation

Shopkeeper reuses the compatible human construction in `HumanPlayerFamily.py`,
with complete hands, seated eyes and a dark broad-brimmed hat. Source blue/cyan
jacket, green trousers and brown shoes are fixed icon appearance. There is no
live inventory lookup. Separate closed jacket/legwear, collar/cuffs and shoes
cover the ancestry; undergarment paint on the existing body prevents exposed
shoulder seams. Existing player models are unchanged. Costume folds, face,
body proportions and hidden rear anatomy remain art interpretations.

All five altars share the same stepped rectangular base, stone pedestal,
cornice, offering slab and inset rim. Colour follows the actual tiles. The red
marks are interpreted as mineral/inlay paint rather than a claim about blood,
recent sacrifices, blessing, ownership, priest presence or conversion state.
The exact pattern is artistic. Other altar's white rays become twelve static
surface inlays, with no animated aura or emissive shader. No real-world
religious symbol or invented deity insignia was added.

Paint uses `FLOAT_COLOR` / `CORNER`. Additional slab surface sampling preserves
the markings in FBX. Shopkeeper's upper black hat pixels are retained with a
reviewed spatial mask; lower/right shadow is excluded. Original source tiles
remain unmodified. Silhouette overlap is only an approximate diagnostic.

Native draft costs: shopkeeper 249,536 triangles; each ordinary altar 50,656;
other altar 51,184. Face/neckline, jacket/hip transitions, cloth tailoring,
stone/red-pigment refinement, close/overview readability and LOD/runtime cost
remain finish work. No animation or rig is required by the product vision.

## Integration and perception boundary

`win/ue/winue.c::terrain` maps only `glyph_is_cmap_altar` and its displayed
glyph offset to five explicit terrain strings. It never reads `levl[].altarmask`,
god identity, player alignment, or hidden monster state. Already displayed
terrain is retained by the existing parser when an actor covers it. An altar
created under an actor has no new visual geometry until NetHack actually
displays it; the test does not manufacture information about an unseen surface.

`DungeonAltars.cpp::GetAltarBatch` whitelists those five strings, rejects unknown
cells and uses separate dim materials/light channels for remembered terrain.
Covered known altars still support displayed actors/items. Terrain-only cells
skip the tile-card overlay after placing the 3D altar. Altars appear in both F9
styles. Shopkeeper follows optional sculpted-creature selection; both sexes
select `SM_shopkeeper` with 15-degree yaw. Default style retains official tile
fallbacks. F7/F9/camera, fixed player clothing, high walls, floor tint, doors,
complete status HUD and DX12/SM6 shadows remain intact.

## Artifacts and checks

- `Art/SpecialBatch2/SpecialBatch2.blend`: six editable collections with studio,
  saved paint and shopkeeper initially visible.
- `Art/CreatureInterpretations/shopkeeper.fbx`: shared-sex creature export.
- `Art/EnvironmentInterpretations/altar_{unaligned,chaotic,neutral,lawful,other}.fbx`:
  five canonical terrain exports.
- `SpecialBatch2-SourceReview.png`: both shopkeeper tiles and all five altar tiles.
- `SpecialBatch2-Models.png` / `SpecialBatch2-Comparison.png`: actual front/rear,
  source tiles and best true 16x16 reverse projections.
- `SpecialBatch2-Projections.png` / `projection-report-special2.json`: all 36
  actual tiny renders and reviewed mask exclusions.
- `SpecialBatch2-EyeReview.png`: twelve actual head/altar detail views.
- `mesh-inspection.json`: saved paint/finite geometry/floor/closed cloth and
  altar topology, paired eye/hat modules, exact shared altar construction,
  source sex equality and all 77 previous canonical FBX hashes unchanged.
- `SpecialBatch2-Unreal-0.png`: shopkeeper plus unaligned/chaotic/neutral altars.
- `SpecialBatch2-Unreal-3.png`: shopkeeper plus lawful/other altars. The foreground
  wall obscures the lower other-altar base; unobstructed studio views are supplied.
- `save-preservation.json`: complete played-session/runtime audit.

Native source checks, saved geometry inspection, bridge/editor builds and six
targeted imports pass. All front/rear/detail and tiny renders and both engine
captures were inspected. `Tests/BridgeSpecialBatch2.py` uses real wizard wishes
for four ordinary altars, steps away to reveal their glyphs, and verifies known
terrain retention after the hero returns. Wizard creation confirms both
shopkeeper sex glyphs, explicitly accepting NetHack's normally restricted NPC
creation prompt. Native dungeon-menu teleport to Astral plus magic mapping
confirms tile 1309 for the special high-altar appearance.

`VerifySpecialBatch2.ps1` runs two fresh captures, checking both shopkeeper sexes,
five altars in both styles, visible/memory material paint, unknown/non-altar
guards, covered terrain, official shopkeeper fallbacks, native map, hero centring
and 8x zoom. Both real F9 switches preserve native turn/input sequence in each
run. Existing bridge smoke and corpse/fountain/sink regression tests pass.
Evidence: `build-special-batch2-{bridge-build,unreal,blender,refine,shirt,renders,
renders-shopkeeper,review,inspect,import,native,compatibility,smoke,regression,
live-0,live-3}.log`.

Use `RenderSpecialBatch2.py` / `ReviewSpecialBatch2.py` to inspect saved work;
`-- shopkeeper` on Render refreshes only that form and merges its report.
Fresh generation contains the final clothing/paint corrections. Do not repeat
the one-time saved refinement/repaint scripts merely to inspect the scene.

## Saves and inventory

Initial required backup:
`Backups/NetHackSaves/20261102T144236.531581Z.zip`. The bridge build also made
verified backup `20261102T144609.300079Z.zip` before replacing the runtime.
All 1,081 player-session files, LastSession pointer and the complete file set
remain unchanged. Of 1,090 baseline player/runtime files, 1,089 are byte-identical;
only `Runtime/NetHackBridge.exe` changed, for the display-only output extension.
Data files and save format remain unchanged. Compatibility was tested by
creating a **new disposable save** with the archived runtime and restoring it
with the new runtime in an isolated directory. No played session was resumed,
advanced, force-stopped or overwritten.

Post-integration snapshot `Backups/NetHackSaves/20261102T150439.106734Z.zip`
also verifies the unchanged saves paired with the current runtime.

Inventory is now 66 verified creature identities + one completed player role
+ 315 remaining creatures + 12 remaining roles = 394 source identities. There
are 72 creature/player forms (66 primary + four female variants + two human
players), four object drafts and two terrain-feature identities with six forms
(fountain plus five altars). Creature coverage is 66/381 = 17.3%; creature/player
identity coverage is 67/394 = 17.0%. Full terrain/object inventories remain pending.
The regular next-creature queue stays killer bee, queen bee and xan.

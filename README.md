# nUthEck

A live NetHack 5.0.0 game presented in Unreal Engine 5.7. The original game
runs in a separate local process; Unreal renders its window-port events as
3D geometry on the full 79 by 21 drawable grid.

The [game vision](Docs/GameVision.md) is NetHack's turn-based tactical play with
modern graphics and static models. Character/object animation is out of scope;
brief wand effects, such as lightning, remain a possible addition.

For creature-art sessions, start with [CreatureAssetContext](Docs/CreatureAssetContext.md).
The [restrained fur study](Docs/FurStudy.md) compares dog/cat surface treatments without replacing the live models.
Use the [asset backlog](backlog.md) to choose the next batch and track generated drafts and finishing work.
The [creature hierarchy](Art/CreatureCatalogue/Hierarchy.md) and
[machine-readable catalogue](Art/CreatureCatalogue/creatures.json) record source
traits and proposed modelling reuse. Catalogue work does not generate meshes.
The [second creature batch](Docs/CreatureBatch2.md) adds jackal, fox and gnome
anatomical drafts; F9 selects them alongside the original ant, dog and goblin.
The [third batch](Docs/CreatureBatch3.md) adds sewer rat, giant rat and gnome ruler,
bringing the optional sculpted roster to nine.
The [fourth batch](Docs/CreatureBatch4.md) adds kitten, housecat and large cat,
bringing the current optional roster to twelve.
The [fifth batch](Docs/CreatureBatch5.md) adds wolf, winter wolf cub and winter wolf.
The [sixth batch](Docs/CreatureBatch6.md) adds dog, large dog and dingo, with
texture-only fur, fitted eyes and verified live integration.
The [seventh batch](Docs/CreatureBatch7.md) adds coyote, warg and rabid rat,
including fitted canid eyes, warg jaw detail and the reused lean rat with mouth froth.
The [eighth batch](Docs/CreatureBatch8.md) adds bat, giant bat and vampire bat,
with closed finger-supported wings, fitted eyes and explicit source-shadow separation.
The [ninth batch](Docs/CreatureBatch9.md) adds jaguar, lynx and panther, with
painted coat markings, distinct ear/tail proportions and fitted feline eyes.

The [thirteenth batch](Docs/CreatureBatch13.md) adds kobold, large kobold and kobold leader,
with independent family proportions, source blue palettes and separate orange rank clothing.

The [first object batch](Docs/ObjectBatch1.md) adds large boxes, rounded chests and gold-piece clusters
to both creature styles, with dim remembered materials and displayed-object mapping.

Missing entity models now use [transparent official tile cards](Docs/TileFallback.md),
with camera facing, remembered dimming and native shuffled-appearance mapping.

The [fourteenth creature batch](Docs/CreatureBatch14.md) adds kobold shaman, kobold mummy and kobold zombie,
with yellow caster clothing, fitted linen wraps and source blue/green undead paint.

The [fifteenth creature batch](Docs/CreatureBatch15.md) adds gnomish wizard, gnome mummy and gnome zombie,
including source-supported beardless female wizard/zombie forms and fitted mummy linen.

The [sixteenth creature batch](Docs/CreatureBatch16.md) adds dwarf, dwarf leader and dwarf ruler,
with shared male/female appearances, blue clothing and separate rank pieces.

The [seventeenth creature batch](Docs/CreatureBatch17.md) adds dwarf mummy and dwarf zombie,
with exact saved dwarf anatomy, fitted linen, source undead paint and verified shared sex appearances.

The [eighteenth creature batch](Docs/CreatureBatch18.md) adds hobgoblin, hill orc and Mordor orc,
with saved goblin ancestry, a shared upright orc body, source palettes and verified displayed-sex mapping.

The [nineteenth creature batch](Docs/CreatureBatch19.md) adds the requested floating eye, newt and lichen,
with a curved iris/hover gap, complete amphibian anatomy and a painted eyeless foliose thallus.

The [twentieth creature batch](Docs/CreatureBatch20.md) adds Uruk-hai, orc shaman and orc-captain,
with exact saved orc anatomy, a separate source-painted shield, caster clothing and captain helmet rim.

The [special mixed batch](Docs/SpecialBatch1.md) adds grid bug, generic corpse and a carved stone fountain
with static blue-water arcs. Corpses use displayed-glyph mapping; fountain and sink terrain stay distinct.

![Live dungeon](Docs/Images/LiveDungeon-1600x900.png)

## Play

Open `nUthEck.uproject` in Unreal Engine 5.7 and press **Play**, or run this
from PowerShell in the project directory:

```powershell
.\Scripts\LaunchPrototype.ps1
```

Windows rendering uses DirectX 12 with Shader Model 6 so Virtual Shadow Maps
work in the orthographic overhead view as well as first person. Restart Unreal
after changing these rendering settings; the first SM6 launch compiles shaders.

The launcher opens full screen at the display resolution. Use `-Windowed`
for a window (`-Width 1600 -Height 900` sets its size). Automated captures
continue to use a fixed-size window.

At first launch, answer the character-selection question with `y` for a
random character or `n` to choose. In menus, press the letter shown beside
an option. The scene starts with only the terrain NetHack has revealed;
exploration fills in the map. Previously seen terrain is dimmed when it
leaves the hero's current view. The camera always frames the entire level.

| Key | Action |
| --- | --- |
| Arrow keys | Move north, south, east, west |
| Numpad 1–9 | Eight directions; 5 waits |
| h j k l / y u b n | NetHack's letter movement keys |
| i | Inventory; press an item's letter for its actions |
| o, then a direction | Open a door |
| comma | Pick up items |
| < / > | Ascend / descend stairs (type the character using your keyboard layout) |
| : | Describe the current square |
| period | Wait one turn |
| F1 | NetHack help |
| # | Type an extended command, then Enter |
| Mouse wheel outside a menu | Zoom in/out, from 1x to 8x |
| Middle-mouse drag while zoomed | Pan around the level |
| F5 | Restore the full-level overview |
| F7 | Show/hide floating entity glyphs and badges |
| F8 | Recenter on the hero and follow movement |
| F9 | Compare tile volumes with sculpted ant/dog/goblin candidates |
| Ctrl+F | Follow a curved transition into/out of first person, ending in the hero's current look direction |
| Right-mouse drag in first person | Look around; movement still uses map directions |
| Escape | Return from first person; otherwise cancel a prompt or menu |
| PgUp / PgDn or mouse wheel | Scroll menus and text |
| Enter | Confirm text entry or menu selection |
| F2 after a game ends | Start a fresh game |

For a multiple-selection menu, item letters toggle selections and Enter
accepts them. A numeric prefix sets an item's count. `.` selects all,
`-` clears all, and `@` inverts selections. Text prompts support ASCII
entry and Backspace. Keyboard cursor targeting is supported; a gold outline
marks the cursor.

Printable commands use Windows character events, so punctuation follows the
active keyboard layout. Arrows, numpad movement, and control keys are handled
separately. NetHack still accepts ASCII commands/text; non-ASCII name entry
is not implemented. At more than 1x zoom the view follows the hero until
you pan; F8 resumes following. Zooming all the way out or pressing F5
restores the whole level. The mouse wheel scrolls menus while a menu is open.

Supported creatures and roles use their original default-tile colours on
tile-derived volume meshes. The hero's glyph is gold and pet glyphs are violet;
unsupported creatures retain coloured placeholders. Larger glyph labels scale
with zoom, including their background badges, and keep creatures identifiable
behind tall walls. Press F7 to hide/show these glyphs and badges for a clear
model view. Ctrl+F follows a smooth curved approach ending in the latest movement
or mouse-look direction, then reverses to the previous overhead framing. Neither
control consumes a game turn. [Controls and verification](Docs/PresentationControls.md).
NetHack decides movement, combat, perception, item identity,
and every other rule.

**Player saves are protected.** The launcher makes verified backups before and
after normal play, and native-backend builds back up first. [Backup and staged
recovery instructions](Docs/SaveProtection.md). Direct editor launches bypass
these launcher backups.

Closing the game asks the backend to follow NetHack's save-on-EOF path.
The next normal launch resumes that session if a save is available. Session
files and diagnostic traces live under `Saved/NetHack/<session-id>/`; they
are separate from the native NetHack installation's saves. Avoid running
two normal instances against the same last session. Automated captures use
fresh isolated sessions and do not change the last-played session.

## Build

Prerequisites: Unreal Engine 5.7, Visual Studio 2022 with the C++ tools and
Windows SDK, and the NetHack dependency releases described in `UPSTREAM.md`.

```powershell
.\Scripts\BuildPrototype.ps1
```

This builds NetHack's console target with the optional UE window port,
stages the helper and game data under `Binaries/NetHack/`, builds the Unreal
editor module, and creates the starter map/material if needed.
`BuildNetHackBridge.ps1` rebuilds just the native helper. Build and launch
scripts accept local installation path overrides.

The map in the editor is empty until Play starts. Runtime geometry is
assembled from engine primitives and a tintable material under `Content/`.
There are no Blender assets or packaged standalone Unreal distribution yet.

## Keep the static visual study

```powershell
.\Scripts\LaunchPrototype.ps1 -StaticStudy
```

This retains the original nine-room layout for camera, lighting, and asset
work. Its sample HUD values are independent of the live game.

## Verification

```powershell
.\Scripts\LaunchPrototype.ps1 -Capture
.\Scripts\LaunchPrototype.ps1 -StaticStudy -Capture
.\Scripts\LaunchPrototype.ps1 -ZoomedCapture
```

A live capture automatically starts an isolated character, moves through
several turns, exercises inventory, checks the live state and full-board
framing, writes `Saved/Screenshots/LiveDungeon.png`, then exits. This is a
presentation smoke check, not a complete gameplay test. It has a timeout
and returns a failing exit code if the live-game checks fail.

The static capture writes `Saved/Screenshots/DungeonPrototype.png`.
The zoomed capture checks approximately 3x magnification and hero centering,
then writes `Saved/Screenshots/ZoomedDungeon.png`.
Both checks project the full board bounds into the viewport and require
containment plus useful screen coverage. Engine startup and shader
compilation can take longer than the in-world capture delay.

The Python scripts under `Tests/` exercise the real helper executable:

- `BridgeSmoke.py`: native startup, map events, real movement and turns.
- `BridgeGameplay.py`: inventory, line entry, exploration, opening a door,
  pickup, and an actual non-hero, non-pet creature glyph. It uses only the
  same public display events as Unreal; it retries fresh random levels.
- `BridgeLifecycle.py`: close the input pipe, save and exit, restore the
  same position/turn/HP, then advance another turn.

Run these with a local Python 3 installation after building the helper.
Captured traces remain in `Saved/NetHackGameplayTests/` for inspection.
Current validation results are recorded in `Docs/LiveIntegration.md`.

## Asset conventions

The live iteration uses the **official default tileset** as its reference,
regular grey dungeon masonry, and tile-derived 3D figure prototypes. See
[Docs/DefaultTileIteration.md](Docs/DefaultTileIteration.md) for the conversion
method, coverage and limitations. `Scripts/LaunchPrototype.ps1 -NewGame` opens
a fresh real dungeon; `-DefaultTileCapture` verifies and captures it.

Three anatomical interpretations are available as an optional candidate through
F9 or `-SculptedCreatures`. Their source-tile/render comparisons, assumptions and
editable geometry are described in [Docs/CreatureInterpretations.md](Docs/CreatureInterpretations.md).

The first **painted miniature** art study is available through
`Scripts/LaunchArtStudy.ps1`. It loads actual Blender-authored meshes in Unreal
and supports the existing camera controls. Rebuild its assets with
`Scripts/BuildArtStudy.ps1`; use `-SkipBlenderRender` for an export-only iteration.
The direction, current limitations and source catalogue are documented in
[Docs/ArtDirection.md](Docs/ArtDirection.md). The generated concept board and
actual Blender/Unreal renders are saved in `Art/Studies/01-MiniatureDungeon/`.

- One cell is 100 Unreal units (one metre); the board lies in XY, with Z up.
- Blender assets should use a floor-centred origin and the same cell scale.
- Terrain, walls/doors, items, and characters occupy separate mesh batches.
- Walls are 1.2 m tall, doors are 1 m tall, and real-time shadows are enabled.
- The orthographic camera keeps its overhead angle while zooming and panning.
  F5 always restores the full-level framing.

Native source provenance, local modifications, and the original Windows
build are described in `UPSTREAM.md`. The bridge protocol and current
implementation boundaries are described in `Docs/LiveIntegration.md`.

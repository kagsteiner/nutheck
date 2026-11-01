# Large box, chest and gold pieces

The first object batch adds three source-derived painted miniature assets to
the live renderer. Objects have their own assets, materials and progress records;
they do not change the creature catalogue or its completion counts.

## Source and appearance

| Source identity | Official tile | Model |
| --- | --- | --- |
| `LARGE_BOX` / large box | `objects.txt:216` | Rectangular wooden container with flat plank lid, warm framing and yellow latch |
| `CHEST` / chest | `objects.txt:217` | Wooden container with rounded lid, curved braces, yellow latch and rear hinges |
| `GOLD_PIECE` / gold piece | `objects.txt:440` | Representative group of gold discs, small stacks and scattered coins |

`include/objects.h:899–902` defines both containers as wood. The coin declaration
at line 1512 defines gold pieces as gold. Neither container has a shuffled
unidentified appearance. Actual orange/brown/yellow tile colours guide the
palette. Dark offset bottom/right pixels are treated as cast shadows, not
painted black borders. Diagnostic spatial masks retain enclosed dark details;
original official tiles remain untouched on the comparison board.

The gold icon includes an ambiguous brown mass with bright scattered marks,
consistent with a spilling purse or a stylised gold pile. This batch chooses
the requested visible coins rather than reconstructing a bag. Disc arrangement,
blank rims, wooden joinery, hinges, framing and small nail heads are artistic
interpretations. There is no invented currency emblem. Nine decorative discs
form the asset regardless of native stack quantity; the geometry never claims
an exact amount. The container latch is static hardware, not a visible lock or
trap indicator. Closed lids do not imply a locked container.

## Geometry and artifacts

`ObjectFamily.py` builds complete solid containers with individual planks,
bevelled edges and editable lid components. The rounded lid uses closed
half-cylinder sections; both ends and the underside exist. The coins have
closed bevelled discs and restrained raised rims. All parts use corner vertex
paint, with subtle wood colour variation. Metal has broad highlights and
moderate roughness; wood remains matte. No downloaded meshes or texture packs
were introduced. Origins sit at floor level, in metres, within a one-cell
footprint. Each FBX combines into one Unreal static mesh.

- `Art/ObjectInterpretations/ObjectBatch1.blend`: editable source collections
  and studio, initially displaying the large box.
- `large_box.fbx`, `chest.fbx`, `gold_piece.fbx`: independent painted exports.
- `ObjectBatch1-Models.png`: actual Blender studio views.
- `ObjectComparison-batch1.png`: original tiles, true 16×16 projections and
  actual front-quarter/rear views.
- `ObjectBatch1-Projections.png` / `projection-report-object1.json`: all 18
  projection candidates, spatial masks, bounds and rough silhouette scores.
- `object-batch1-inspection.json`: saved paint, finite/nonzero geometry,
  manifold closed meshes, floor placement, dimensions and lid distinctions.
- `protected-creature-player-assets.json`: hashes confirming all 41 earlier
  creature/player exports are unchanged.
- `ObjectBatch1-Unreal.png`: actual live dungeon capture.
- `object-assets.json`: selected-object progress registry, not a full object inventory.

Native triangle counts: large box 9,400; chest 9,484; coin group 9,468.
These are static draft costs, without a production LOD/performance claim.

Generate using Blender `--background --threads 4 --python Scripts/CreateObjectBatch1.py`.
Inspect using `InspectObjectBatch1.py`. `RenderObjectBatch1.py` rerenders the
saved scene without regenerating geometry. `CreateObjectBatch1Comparison.py`
assembles the official-tile comparison.

## Live mapping and perception

`win/ue/winue.c` now sends optional `display_object` metadata only for three
whitelisted non-randomised appearances resolved by `glyph_to_obj(fg->glyph)`.
It supports normal and pile-top object glyphs. No floor-object lookup is used;
contents, quantity, lock/trap status, blessings and unidentified true types are
not exported. Disguises/hallucinations follow their displayed glyph, and memory
retains only previously displayed information. No under-monster/under-hero
object rendering has been added.

`FNetHackCell.DisplayObject` resets on every tile update, avoiding stale object
identities. `GetDisplayedObjectBatch` accepts only `Kind == item` and these keys:

`large box → SM_large_box`, `chest → SM_chest`, `gold piece → SM_gold_piece`.

Assets live under `/Game/ObjectInterpretations/Meshes`. They appear in both
creature styles; F9 continues to control creature style. Separate normal/memory
batches use vertex-painted wood/metal materials; remembered versions multiply
paint by 0.20. Unsupported items retain their existing sphere fallback. Missing
object assets also fall back safely. Native NetHack continues to handle pickup,
looting, opening, locks, traps, carrying and money.

## Verification and scope

Bridge and editor builds passed. Three targeted imports passed vertex-paint
checks and created normal/memory wood/metal materials. Saved geometry checks
passed, and front/rear plus all 18 true 16×16 renders were inspected.

`Tests/BridgeObjects.py` starts an isolated native wizard session (the normal
session is unchanged), uses native wish/drop/movement commands, then verifies
large box, chest and pile-top gold-piece display events. It checks the field
is absent from non-item displays. Existing `BridgeSmoke.py` also passes.

`VerifyObjectBatch1.ps1` passes three types × visible/remembered × both creature
styles, paint buffers, memory material assignment, unsupported identity and
non-item fallbacks. Two real F9 switches preserve native turn and input
sequence. Native movement/map, hero centring and 8× zoom pass. Final fixture
placement prefers nearby clear floor; the actual engine capture is inspected.

Evidence: `build-object-batch1-{blender,inspect,bridge,unreal,import,native-objects,bridge-smoke,live}.log`.

These are closed static object drafts. Lid opening, looting presentation,
carried/equipped representations, quantity-aware pile variants, further wood
brushwork, LODs and production performance review remain future work. The
three-item registry does not inventory every object, unidentified appearance,
terrain feature or effect in NetHack.

Later presentation update: unsupported item spheres are now preceded by the
[official tile-card fallback](TileFallback.md). The three object models retain priority.

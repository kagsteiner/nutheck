# Grid bug, generic corpse and carved fountain

This requested mixed batch adds one creature, one generic object presentation
and one terrain feature. It follows the static presentation in `GameVision.md`:
no rigs or animation are required, and the water arcs/ripples are static meshes.

## Source and art decisions

| Asset | Official reference | Native meaning |
| --- | --- | --- |
| Grid bug / `PM_GRID_BUG` | `monsters.h:1149`; monster tiles 236/237 | Tiny level-0 animal, difficulty 1, 1d1 electric bite, shock/poison resistance, no corpse; no grasping hands |
| Generic corpse / `CORPSE` | object tile 267; combined atlas 1056 | Displayed corpse object; one representative remains asset, with no species-specific geometry |
| Fountain / `FOUNTAIN`, `S_fountain` | other tile 41; combined atlas 1313 | Displayed/remembered fountain terrain, distinct from a sink |

Grid bug's male/female tiles are identical. The source describes an electronic
creature from another universe; the catalogue's broad Flying insects group is
not a flight trait. No `M1_FLY` or wings are present in the native declaration.
The interpretation has six angular red legs, red antennae, blue head/thorax,
pale abdomen with orange/yellow paint and small yellow eyes/mandibles. Its exact
leg/antenna arrangement and hidden anatomy are art completions, not a literal
reconstruction of tiny pixels. No glow, wings or timed electrical effect is added.

The corpse tile has pale fragments around a red/orange centre. The model uses
a low collapsed mass with four pale bone fragments. It is a generic remains
marker, not a claim about body species, sex, size, freshness, poison, edibility,
revival or native corpse contents. Shape and toned-down pigment are artistic
interpretations. It contains no invented clothing, weapon or species-specific
head. Native corpse behaviour remains entirely in NetHack.

The fountain tile shows a pale round basin, central white stem and blue jets.
The requested beautiful interpretation uses desaturated carved stone, a
stepped octagonal foot, fluted pedestal, sculpted bowl/rim, twelve petal reliefs,
fluted central column and bud finial. Six static water arcs fall into a glossy
blue basin with three still ripple rings. These architectural details and the
water curve are art interpretation; no hidden magical/blessed/looted state is
shown. Water is opaque, glossy static geometry, with no shader time dependency.
The closed forms remain complete from behind and below.

Source shadows are excluded spatially from diagnostic comparisons; original
16x16 source tiles remain unmodified. The opaque black offset below/right is
not anatomy, a second object or a painted black border. Diagnostic overlap is
not proof of exact tile fidelity.

## Geometry, materials and artifacts

`SpecialAssetGeometry.py` constructs these three different forms.
`SpecialBatchConfig.py` keeps mixed official source references and canonical
FBX destinations separate. `CreateSpecialBatch1.py` creates an editable mixed
scene; the shared pipeline accepts optional source-entry/export-path overrides
without changing earlier batch defaults.

- `Art/SpecialBatch1/SpecialBatch1.blend`: editable geometry, paint and studio.
- `Art/CreatureInterpretations/grid_bug.fbx`: creature export.
- `Art/ObjectInterpretations/corpse.fbx`: generic object export.
- `Art/EnvironmentInterpretations/fountain.fbx`: terrain-feature export.
- `SpecialBatch1-SourceReview.png`: all three original official references.
- `SpecialBatch1-Models.png` / `SpecialBatch1-Comparison.png`: actual meshes,
  front/rear studio views, source tiles and the best true 16x16 candidates.
- `SpecialBatch1-Projections.png` / `projection-report-special1.json`: all 18
  tiny camera candidates and spatial masks.
- `SpecialBatch1-EyeReview.png`: saved close-detail views.
- `mesh-inspection.json`: finite/nonzero geometry, closed manifold surfaces,
  corner paint, floor placement, six legs and static-water/basin checks.
- `protected-assets.json`: all 67 preceding canonical FBX hashes retained.
- `SpecialBatch1-Unreal.png`: actual engine fixture capture.

All meshes use `FLOAT_COLOR` / `CORNER` vertex paint. Corpse uses the established
object paint material and dim memory version. Fountain has separate stone and
glossy water materials, each with a 0.20-brightness memory variant. No imported
mesh, external texture pack or animated material is used. Native triangle
counts: 16,648 grid bug / 27,224 corpse / 36,624 fountain. The fountain footprint
is under 0.86m across and its height is about 0.98m, within one 1m cell.

The saved thin water cylinder's bevel was corrected using one-time
`RefineSpecialBatch1Water.py`; fresh generation includes the correction. Use
`RenderSpecialBatch1.py`, `ReviewSpecialBatch1.py` and `InspectSpecialBatch1.py`
to inspect saved assets rather than regenerating them. Surface finishing,
foot/antenna proportions, remains shapes, stone/water polish and LOD/runtime
review remain refinement work; animation is outside the product scope.

## Display boundary and integration

`glyph_to_obj` already resolves both normal and pile-top corpse glyphs to
`CORPSE`. The bridge now whitelists the optional string `display_object: corpse`
from that displayed glyph only, without exporting a corpse monster identity or
reading floor objects. The parser's existing per-event reset remains in place.
`GetDisplayedObjectBatch` selects the generic mesh only for item displays, in
both F9 creature styles, with dim remembered paint. Other items retain their
existing model/tile-card priority.

The bridge previously mapped both `S_fountain` and `S_sink` to `fountain`.
They now produce distinct `fountain` and `sink` terrain strings. The new
`GetFountainBatch` accepts known fountain terrain, including memory and terrain
beneath a displayed foreground entity. Unknown cells, sinks, floors and missing
fountain assets retain the existing fallback behaviour. The fountain replaces
the old feature cylinder; sinks retain their existing marker. No secret fountain
state, under-object lookup or gameplay collision is added. Grid bug selection
uses displayed canonical identity/sex in the established sculpted style.

## Verification

Saved inspection, bridge/editor builds and native wizard tests pass. Wishes
for newt and giant-rat corpses both emit generic `corpse` with official tile
1056 and no monster identity. Wished fountains/sinks emit distinct terrain.
Existing bridge object and smoke tests also pass. Final three-asset import
passes with vertex-colour buffers and all normal/memory materials. The live
check passes both grid-bug displayed sex forms, both creature styles, corpse
and fountain normal/memory cases, official grid-bug tile fallback, sink/floor/
unknown guards and no-turn F9. Both switches preserve native turn 5/input
sequence 7; native map, hero centring and 8x zoom pass.

Six studio views, six close views, all 18 true 16x16 candidates and the actual
engine capture were inspected. Capture-only fixture scoring was improved to
prefer open floor, after walls partly obscured the first view. The final view
clearly shows the bug, corpse, fixture fountain and an actual native fountain.
Stone/water shading and colours were reviewed. All 67 prior exports remain
unchanged. Evidence: `build-special-batch1-{blender,refine,review,inspect,bridge,
unreal,import,native,objects,smoke,live}.log`.

Only grid bug changes the creature completion count: 60 completed creatures +
one completed player role + 321 remaining creatures + 12 remaining roles =
394 unique source IDs. There are 64 creature/player physical forms. Objects
now total four selected presentations, and the fountain is the first separately
registered terrain feature. Coverage is 60/381 creatures = 15.7%, or 61/394
creature/player identities = 15.5%; these do not measure the entire art scope.
Next suggested creature family extension remains orc mummy/orc zombie. Static
presentation is intended; refinement and performance review remain separate.

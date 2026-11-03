# Gecko, iguana and lizard

Three verified static drafts follow the suggested queue. The original male and
female tiles are identical for each identity, so each pair shares one form.
No additional sex anatomy is inferred. Static presentation is the product target.

| Identity | Source / official tiles | Native traits |
| --- | --- | --- |
| `PM_GECKO` | `monsters.h:3268`; 660/661 | Level 1, difficulty 2; 1d3 physical bite |
| `PM_IGUANA` | `monsters.h:3275`; 662/663 | Level 2, difficulty 3; 1d4 physical bite |
| `PM_LIZARD` | `monsters.h:3292`; 666/667 | Level 5, difficulty 6; 1d6 physical bite; stone resistance/conveyance |

All three are tiny, hostile carnivorous animals without grasping hands in the
pinned NetHack source. These abstract sizes do not define literal dimensions.
No native gameplay, perception or backend code changed.

The actual tiles guide colour: pale gray/peach gecko with red eyes, green/lime
iguana, and green/brown lizard. Their ASCII colours are not paint specifications.
Offset black fringes are excluded spatially from projection diagnostics, while
enclosed black details remain. Blue-gray edge pixels are treated as ambiguous
outline/shading cues, not a mandate for blue anatomy. Original tiles are retained.
Masks and overlap scores are approximate, not proof of anatomical correctness.

`Scripts/ReptileFamily.py` constructs complete squamate bodies with independently
parameterised torso, skull, neck, stance and tail dimensions. These are new
reptile bodies; the existing amphibian newt was not reused. Each has four splayed
legs and five inferred digits per foot, integrated into a continuous sculpt.
Gecko has a broad head and adhesive toe pads. Iguana has a deeper torso, longer
tail, fitted throat dewlap and thirteen dorsal spines. Lizard is slender without
a crest. Both green forms have small static forked red tongue tips interpreting
the source accent. Exact species, digits, tongue, crest and hidden anatomy are
artistic assumptions. No visible feature claims native inventory or hidden state.

Paint supplies broad colour masses and fine scale-like grain without extruded
scale beads. Materials follow the shared painted miniature shader. Geometry is
closed, with complete rear/underside surfaces and positive floor clearance.
Draft topology is dense: approximately 112k/142k/111k triangles. Limb transitions,
mouth/eye integration, toe-pad separation, scale paint, tiny contrast and LOD
budgets remain visual finishing work. These are verified drafts, not production
assets; no rigs or animation are planned.

Artifacts under `Art/CreatureInterpretations/`:

- `CreatureBatch25.blend`: editable collections, vertex paint and studio; gecko initially visible.
- `gecko.fbx`, `iguana.fbx`, `lizard.fbx`: canonical painted exports.
- `Batch25-SourceReview.png`: all six original official sex tiles.
- `Batch25-Models.png`, `MeshComparison-batch25.png`: actual front/rear geometry and tile comparison.
- `Batch25-Projections.png`, `projection-report-batch25.json`: all eighteen actual 16x16 projections.
- `Batch25-HeadReview.png`, `Batch25-UndersideReview.png`: actual saved face/profile/underside views.
- `batch25-mesh-inspection.json`: finite/nonzero/manifold geometry, paint, floor, eyes, twenty surface toe-tip checks, crest/dewlap distinction.
- `batch25-protected-assets.json`: all 89 preceding canonical FBX hashes, unchanged.
- `Batch25-Unreal-fixtures.png`: final isolated live capture.
- `batch25-save-preservation.json`: complete played-session/runtime hash audit.

Reusable scripts are `CreateCreatureBatch25.py`, `RenderCreatureBatch25.py`
(saved rerender, optional `-- <key>`), `ReviewCreatureBatch25.py`,
`InspectCreatureBatch25.py`, `CreateCreatureBatch25Comparison.py`,
`ImportCreatureBatch25.py`, `VerifyCreatureBatch25.ps1` and
`AuditCreatureBatch25Saves.py`. Build, review, inspect, import and live evidence
is in `build-creature-batch25-*.log`.

Saved geometry and all actual studio/detail/tiny views were inspected. Unreal
compile, three targeted imports, material assignment and vertex colours pass.
Live checks cover six displayed sex aliases, six official fallbacks, unknown
identity and paint buffers. Both actual F9 switches preserve native turn/input
sequence. Native map, hero centring and 8x zoom pass. Normal and preview models
use the established -75-degree yaw; selection uses displayed identity/sex only.

The verified baseline backup is
`Backups/NetHackSaves/20261102T161037.219275Z.zip`. All 1,090 player/runtime files,
the complete file set and `LastSession.txt` remain unchanged. No played session
was resumed, advanced, stopped or replaced; no native backend was rebuilt.
Captures use fresh `Saved/NetHackCaptures` roots with `Remember=false`.

**75/381 creatures = 19.7%** now have verified static drafts. Including the
completed Valkyrie role gives **76/394 = 19.3%**. The inventory balances as
75 creatures + one role + 306 remaining creatures + 12 remaining roles = 394.
There are 81 physical creature/player forms (75 primary, four additional female
creature forms, two human players). Objects and terrain remain separate.

Next suggestion: garter snake, snake and water moccasin; review source traits,
both sex tiles, complete limbless anatomy and distinct heads/patterns first.
Detailed object art direction and exceptional divine-gift weapons remain deferred
for the user's later review. Existing players, HUD, F7/F9/camera, high walls,
floors/doors, perception and fallback behaviour are preserved.

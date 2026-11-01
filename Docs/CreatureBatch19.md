# Floating eye, newt and lichen

Batch 19 builds the user's three requested early-level creatures as separate
editable, vertex-painted, unrigged static drafts. They do not share anatomy.
Each official male/female tile pair is identical; one appearance serves each
identity. Floating eye and lichen are explicitly neuter in the native source.

## Source facts and interpretation

| Identity | Source / official tiles | Native traits |
| --- | --- | --- |
| `PM_FLOATING_EYE` | `monsters.h:333`; 58/59 | Level 2, difficulty 3; passive `AT_NONE` / `AD_PLYS`, 0d70; small, flying/amphibious, no head/limbs, cannot take items |
| `PM_NEWT` | `monsters.h:3260`; 658/659 | Level 0, difficulty 1; 1d2 bite; tiny animal, swims/amphibious, carnivorous, no grasping hands |
| `PM_LICHEN` | `monsters.h:1614`; 324/325 | Level 0, difficulty 1; sticky touch, 0d0; small, breathless, mindless, eyeless/headless/limbless, cannot take items |

All three are hostile and have no innate/conferred resistance. Floating eye
is infravisible. Abstract source size does not define literal metre dimensions.
Native combat and gaze/stick behaviour remain NetHack's responsibility; the
static models add no new effects or attack rules.

Official tiles show a white eyeball with cyan/blue iris and dark pupil; an
orange/peach newt; and a green lobed lichen with orange/pale patches. Exterior
black pixels continuing down/right form crude cast shadows. Spatial masks
exclude that fringe while retaining enclosed pupil/mouth/dark details. Original
comparison tiles are unmodified. The pale fungal patches are interpreted as
surface colour, never eyes. ASCII colours are metadata, not alternate palettes.

Hidden back/underside anatomy, precise body scale, iris aim, limbs/toes and
foliose lichen construction are artistic completions. No optic stalk, eyelashes,
veins, fur, scales, dorsal sail, mushroom stem, equipment or stand is invented.

## Geometry

`EarlyDungeonCreatures.py` constructs three complete forms:

- Floating eye: a closed white globe, radius 235mm, suspended with a 405mm gap
  above its local floor. Its solid curved iris follows a 236–237mm spherical
  radius, including cyan outer ring, blue inner ring and dark pupil. It points
  20 degrees upward for the angled view. The rear is complete white anatomy.
- Newt: one continuous sculpted orange/peach body, flattened head/muzzle, four
  low splayed legs, small toes and a curved tapering tail. Toe completion uses
  four forefoot / five hindfoot digits; individual digits are artistic anatomy,
  not readable source pixels. Paired dark eyes are fitted within 1mm of the
  actual head surface. No limb is replaced by the tile's offset shadow.
- Lichen: one connected closed thallus made from scalloped foliose lobes,
  including a complete underside. Orange-bordered pale patches are pigment
  on this surface, with no raised patch objects, eyes, head, limbs or stem.

Paint is `FLOAT_COLOR` on `CORNER`, through the established miniature material
pipeline. Native triangles: 7,360 floating eye / 85,820 newt / 87,364 lichen.
These are static drafts. Refinement of eye/cornea shading, newt feet/skin/pose,
lichen edges/colour transitions, rigs, animation/effects, LODs and runtime cost
remain finishing work.

## Artifacts and checks

- `Art/CreatureInterpretations/CreatureBatch19.blend`: three editable collections,
  paint and saved studio; floating eye initially visible.
- `floating_eye.fbx`, `newt.fbx`, `lichen.fbx`: painted exports.
- `Batch19-SourceReview.png`: all six original sex tiles.
- `Batch19-Models.png` / `MeshComparison-batch19.png`: actual geometry,
  front/rear views, source tiles and best actual 16x16 candidates.
- `Batch19-Projections.png` / `projection-report-batch19.json`: all 18 true tiny
  camera candidates, bounds and spatial shadow masks. Overlap is diagnostic.
- `Batch19-EyeReview.png`: actual globe/iris, newt head and lichen surface views.
- `batch19-mesh-inspection.json`: saved geometry/paint/closure, hover clearance,
  curved iris radius/palette, connected bodies, four feet, eyes and fungal paint.
- `batch19-protected-assets.json`: all 61 preceding FBXs (57 creature/player,
  three objects and the shared tile quad), retained without regeneration.
- `Batch19-Unreal-fixtures.png`: actual live engine capture.

`CreateCreatureBatch19.py` generates only these three forms.
`RenderCreatureBatch19.py`, `ReviewCreatureBatch19.py` and
`InspectCreatureBatch19.py` inspect saved geometry. `ImportCreatureBatch19.py`
targets only the three requested meshes. `VerifyCreatureBatch19.ps1` exercises
six displayed sex cases and respective official tile fallbacks, unknown identity,
paint buffers, real F9 switches without native turn/sequence changes, map and
8x zoom. Runtime selection uses displayed identity only; no hidden-world lookup
or gameplay change is added. Floating eye uses the frontal 15-degree orientation;
newt uses the existing quadruped -75-degree orientation. Lichen is unoriented.

Saved native geometry/paint/closure/iris/hover/feet/eye/fungal checks pass,
with all 61 earlier exports unchanged. Editor build and three targeted imports
pass with vertex-colour buffers. Six displayed sex forms, six respective
official tile fallbacks, unknown identity and paint pass. Both real F9 switches
preserve native turn 5/input sequence 7; native map, hero centring and 8x zoom
pass. Six studio views, six detail views, all 18 true 16x16 candidates and the
actual engine capture were inspected. All three fixtures are clearly visible.
Evidence: `build-creature-batch19-{blender,review,inspect,unreal,import,live}.log`.

Inventory: 56 completed creatures + one completed player role + 325 remaining
creatures + 12 remaining player roles = 394 unique source identities. There are
60 physical creature/player forms (56 primary creatures + two extra female
creature appearances + two human player forms); three objects remain separate.
Static-draft coverage: **56/381 creatures = 14.7%**, or **57/394 creature/player
identities = 14.5%**. Finishing, rigging and animation remain separate.

The user's requested trio took priority over the orc continuation. The next
suggested batch remains Uruk-hai, orc shaman and orc-captain, reviewing source
traits, both sex tiles and anatomy compatibility before reuse.

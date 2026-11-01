# Dwarf, dwarf leader and dwarf ruler

Batch 16 establishes dwarf ancestry with three shared-sex static drafts. These
are editable, vertex-painted, unrigged interpretations of the official tiles.

## Source facts and interpretation

| Identity | Source / official tiles | Source traits |
| --- | --- | --- |
| `PM_DWARF` | `monsters.h:485`; 92/93 | Level 2, one 1d8 weapon attack, strong humanoid, tunnelling with a pick |
| `PM_DWARF_LEADER` | `monsters.h:502`; 96/97 | Level 4, two 2d4 weapon attacks, lord rank |
| `PM_DWARF_RULER` | `monsters.h:511`; 98/99 | Level 6, two 2d6 weapon attacks, prince rank |

All three have `MZ_HUMAN` source size, dwarf ancestry, infravision, and no innate
resistance. Abstract size/weight do not specify literal miniature dimensions.
The neutral identities retain the lord/lady and king/queen aliases.

Both sex tiles are byte-for-byte identical for each identity; the tile file's
artist note explicitly describes the shared appearance. Each rank therefore
uses one bearded form for male and female display. No invented sex-specific
body, hairstyle or clothing is added.

Official pixels show blue/cyan clothing and headwear, peach face/hands, a pale
beard, a yellow leader band, and a yellow/orange ruler crown. The blue/cyan
split is interpreted as shading on continuous cloth. Hidden anatomy, garment
construction, back views and crown construction are artistic assumptions.
The offset black region to the right/below is cast shadow, not a held weapon
or extra limb. Black enclosed details remain in the spatial comparison mask;
ambiguous edge pixels are diagnostic, not proof of exact reconstruction.
No axe or pick is attached: source weapon attacks do not establish displayed
inventory. NetHack retains all gameplay distinctions.

## Geometry and paint

`DwarfFamily.py` makes a new broad-shouldered body with short sturdy limbs,
rounded ears, a complete nose/jaw and paired eyes seated against the skull.
This is a separate ancestry from the existing gnome. The three ranks copy
the exact same continuous body and costume. Pale beard, blue tunic, sleeves,
trousers, boots and headwear remain editable parts. A consistent sleeve frame
avoids twisted cloth at steep elbow bends. The tunic has closed thickness.

The leader adds a separate gold band to the blue cap. The ruler replaces the
cap peak with a separate crown with eight points and two orange inlays; their
precise three-dimensional layout is an interpretation. Body proportions and
beard are unchanged across ranks. No hidden live equipment is consulted.

Paint is `FLOAT_COLOR` on the `CORNER` domain, using the existing miniature
materials. Colour changes use surface pigment, not raised painted patches.
These remain draft meshes; cloth/face finishing, rigs, animations, LODs and
runtime performance review are separate milestones.

## Artifacts and verification

- `Art/CreatureInterpretations/CreatureBatch16.blend`: three editable collections,
  saved studio, camera and paint; the ordinary dwarf is initially visible.
- `dwarf.fbx`, `dwarf_leader.fbx`, `dwarf_ruler.fbx`: painted exports.
- `Batch16-SourceReview.png`: both official sex tiles for all three ranks.
- `Batch16-Models.png` and `MeshComparison-batch16.png`: actual models,
  front/rear studio views, official pixels and true 16x16 reverse projections.
- `Batch16-Projections.png` / `projection-report-batch16.json`: all 18 tiny
  camera candidates, spatial shadow masks and bounds. Overlap is diagnostic.
- `Batch16-EyeReview.png`: actual front/profile heads for all three ranks.
- `batch16-mesh-inspection.json`: saved geometry, paint, eyes, closed tunic,
  shared-body hashes, identical sex tiles and protected preceding exports.
- `batch16-protected-assets.json`: hashes of the 49 preceding creature/player
  FBXs; existing family meshes are not regenerated.
- `Batch16-Unreal-fixtures.png`: actual live engine capture.

`CreateCreatureBatch16.py` generates the batch. `RenderCreatureBatch16.py`,
`ReviewCreatureBatch16.py` and `InspectCreatureBatch16.py` work from the saved
blend. `ImportCreatureBatch16.py` targets only the three new meshes;
`VerifyCreatureBatch16.ps1` checks six displayed sex cases, paint, respective
official tile fallbacks, unknown-identity fallback, both F9 style changes,
unchanged native turn/input sequence, live map and 8x hero-centred zoom.
The sculpted orientation is 15 degrees, consistent with the other humanoids.

Native inspection, editor build and final three-mesh import pass. All six
sex cases select the correct shared mesh with paint buffers; all six respective
official tile fallbacks and unknown identity pass. Both real F9 switches preserve
turn 5/input sequence 7. Native map, 8x zoom and hero centring pass. Actual studio
front/rear, head views, all 18 projections and live capture were inspected.
All 49 preceding creature/player FBX hashes remain unchanged. Native triangle
counts are 154348 (dwarf), 154860 (leader) and 157232 (ruler), with no LOD/runtime
budget claimed. The live run uses SM6 and shows real overhead cast shadows.
Evidence: `build-creature-batch16-{blender,refine,review,inspect,unreal,import,live}.log`.
Fresh generation includes the final crown correction; the one-time
`RefineCreatureBatch16.py` repairs the saved review, not the ancestry. Use the
saved render/review scripts for later inspection.

The inventory is 394 unique source IDs = 48 generated
creatures + one completed player role + 333 remaining creatures + 12 remaining
roles. There are 52 creature/player physical forms: 48 primary creatures,
two additional female creature appearances, and two human player forms.
Objects remain separately tracked. Next suggested family extension: dwarf
mummy and dwarf zombie, reusing this saved ancestry after their tile review.

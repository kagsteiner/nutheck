# Ruby ring, spherical amulet and oak wand

Three physical appearance designs are now editable, imported and live verified.
They are **appearance slots**, not fixed magical effects or completed coverage
of the ring, amulet and wand categories. Unbuilt appearances keep native tiles.

## Source facts and design

| Physical appearance | Source slot / atlas tile | Native material | Authored design |
|---|---|---|---|
| Ruby ring | RIN_CONFLICT / 977 | GEMSTONE | Carved ruby band, octagonal cut ruby, open gold gallery, claws and small shoulder beads |
| Spherical amulet | AMULET_OF_LIFE_SAVING / 993 | IRON | Closed iron globe, polished latitude/meridian ribs, bail and interlocking chain |
| Oak wand | WAN_NOTHING / 1207 | WOOD | Tapered turned-oak shaft, recessed grip turnings, slender gold-coloured collar and heel ferrule |

These source enum names label default entries in pinned `include/objects.h`
(lines 783, 838, 1462), not permanent live bindings. `src/o_init.c::shuffle_all`
shuffles descriptions, colours and materials. `shuffle_tiles` remaps both ordinary
and pile-top glyph tile assignments from `oc_descr_idx`, including after restore.
Some wand descriptions can be unused because the source pool has extra slots.

Faceting, gallery/prongs, chain/rib construction, wood turnings, small metal
fittings and dimensions are artistic craftsmanship. Generic object tiles were
not used as shape targets. There are no effect-specific symbols, rarity colours,
invented magical lights, charge indicators or blessing/curse decoration. The
native material and gameplay properties remain unchanged by the rendering.

## Geometry and evidence

`Art/ObjectInterpretations/AppearanceBatch1.blend` contains all editable parts;
`ruby_ring.fbx`, `spherical_amulet.fbx` and `oak_wand.fbx` are the painted exports.
`CreateAppearanceBatch1.py` creates only these models. All solids have complete
front/rear/underside geometry; the ring has a genuine opening and cut crown /
girdle / pavilion, and every chain link is closed geometry.

| Model | Mesh parts | Triangles | Authored height |
|---|---:|---:|---:|
| Ruby ring | 21 | 16,476 | 35.7 mm |
| Spherical amulet with chain | 48 | 44,604 | 131.3 mm |
| Oak wand | 15 | 20,212 | 368 mm |

`ReviewAppearanceBatch1.py` opens the saved scene without regenerating it and
checks finite nondegenerate vertices/faces, closed manifold solids, applied
modifiers, no animation, valid corner-domain FLOAT_COLOR Paint, dimensions,
floor origin and distinguishing construction. It verifies all **237 preceding
canonical FBX hashes** from `appearance-batch1-protected.json` unchanged.

Actual render evidence (individual examination framing, not a common size scale):

- [Models](../Art/ObjectInterpretations/AppearanceBatch1-Models.png).
- [Front](../Art/ObjectInterpretations/AppearanceBatch1-Front.png),
  [rear](../Art/ObjectInterpretations/AppearanceBatch1-Rear.png),
  [underside](../Art/ObjectInterpretations/AppearanceBatch1-Underside.png),
  [setting / globe / grip details](../Art/ObjectInterpretations/AppearanceBatch1-Hilts.png).
- [Six genuine 16×16 projections per object](../Art/ObjectInterpretations/AppearanceBatch1-Projections.png).
- [Live native three-item fixture](../Art/ObjectInterpretations/AppearanceBatch1-Unreal.png).

`ImportAppearanceBatch1.py` imports into `/Game/AppearanceBatch1/Meshes/SM_<key>`.
Batch-local gold, iron, dark iron, ruby and oak materials preserve metallic versus
nonmetallic surfaces and distinct roughness; memory variants use the established
20% paint multiplier. No existing material was rewritten. Ruby uses an opaque
glossy faceted surface; gemstone transmission is future finishing work.
`VerifyAppearanceBatch1Assets.py` independently reloads saved meshes, checks paint,
every imported slot, material paths and the remembered counterparts.

## Live selection and placement

No backend or native whitelist extension was needed. The bridge already exports
the public, shuffled `fg->gm.tileidx`; the client already parses it per tile.
`DungeonObjectPlacement.cpp` now supports an optional appearance-tile key in its
registry. An item with tile 977, 993 or 1207 selects the corresponding physical
model regardless of the underlying effect glyph. Missing/unsupported models or
other kinds retain the established fallback. No object-world lookup or hidden
effect identity enters this path.

The ruby ring stands crown-up, with the shank in XZ, hole axis Y and crown
axis +Z. Its gemstone table lies in XY and faces radially outward from the top
of the band. The corrected gallery, continuous support rail and six prongs support this upward setting;
the former sideways, pendant-like crown is superseded by the user's correction
of 2026-11-03. `ReviewAppearanceBatch1.py` verifies the actual table vertices lie
on the gem's upper +Z plane. See the permanent construction rules in
`ObjectArtDirection.md` and `ObjectCreationWorkflow.md`.

The amulet and wand lie flat; FBX maps their authored -Y face to Unreal +Y and
their transforms account for that handedness conversion. All placements use
deterministic yaw and ordinary 4 cm clearance over the floor. Small jewelry uses
enlarged miniature placement scales (11 / 3.6), and the wand uses 1.9;
examination geometry remains at its authored dimensions. Bounds center each
model and compute clearance. There is no physical pile stacking or pedestal.

Both F9 styles retain these ordinary object models, including remembered
materials. Only the displayed native pile top appears. The normal lighting and
high walls remain; the close capture uses the same legal 8× zoom / steep orbit
available to the camera, with glyph badges hidden.

## Native and Unreal verification

- `BridgeAppearanceBatch1.py`: **nine fresh-game cases**, three per appearance,
  use native wishes, drop/reveal, actual identify scrolls, drop/reveal again and
  normal save/restore. Different effect glyphs map to the same physical tile.
  For example, the observed ruby ring identified as gain constitution or warning;
  oak identified as fire, nothing or create monster. Identification changes native
  text while preserving the physical appearance. This is not the wizard command's
  temporary identified-inventory preview.
- `BridgeAppearanceTransitions.py`: a dagger covers the ring and picking it up
  uncovers the ring again; blindness retains only the known appearance across
  restore; hallucination supplies native random tiles rather than the hidden
  actual item's appearance. All pass.
- `CreateAppearanceCapture.py`: places three **real native wished appearances**
  in a fresh generated level, then saves normally. Its disposable fixture disables
  monsters/traps and controls lighting for repeatability. It is not a claim that
  the objects spawned randomly, and no synthetic rendering-only objects were
  inserted into the capture. The native session supplies all displayed tiles.
- Unreal Development build and saved mesh/material reload checks pass.
- `VerifyAppearanceBatch1.ps1`: 12 appearance/style/visibility cases pass; native
  presence of all three appearances, differing glyphs sharing one appearance,
  face-up pose, bounds clearance, remembered materials, wrong-kind/missing-tile
  guards, unsupported appearance fallback and F9 both ways pass at unchanged
  **turn 11 / sequence 2**. Full existing object-placement checks and the
  **1,200-case topmost regression** also pass, as do live map, default presentation
  and 8× camera checks. Evidence: `appearance-batch1-live.json` and the live image.
- Verified backup: `20261103T130416.380535Z.zip`.
  `AuditAppearanceBatch1Saves.py` confirms all **1,090 played/runtime files**, the
  file set and LastSession pointer match exactly. No player session was resumed
  and the backend executable/data were unchanged.

The catalogue records these under a separate `appearances` registry. The associated
source effect rows remain incomplete, while the three physical source slots carry
their verified draft status. Named type, creature and artifact totals did not
increase. Further appearance-family coverage, human visual review, gemstone
optics, readability/material refinement and LOD work remain separate.


## Crown correction verification (2026-11-03)

`ReviseRubyRingCrown.py` replaces only the ring in the saved scene and exports
only `ruby_ring.fbx`. The full generator now constructs the corrected setting
from the start. The setting is rotated 90 degrees relative to the original:
table normal +Z, perpendicular to the finger-hole axis Y. The runtime ring pose
is standing/crown-up; amulet/wand placement is unchanged.

`ring-crown-preservation.json` verifies unchanged geometry and paint for the
other 63 saved mesh parts and all 239 other canonical FBX exports. The targeted
`ImportRubyRingCrown.py` reuses existing materials and touches only the ring mesh.
The saved-geometry review asserts the gem's upper table is horizontal in XY and
its recorded crown axis is +Z. The live appearance/placement/topmost checks pass for the corrected pose;
`ring-crown-live.json` records the rerun. Save verification uses the new pre-change backup
`20261103T134814.973520Z.zip`; player files and backend remain unchanged.

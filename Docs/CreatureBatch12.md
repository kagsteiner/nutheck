# White, gray and black unicorns

Batch 12 extends the reviewed equine family with three independently exported
and verified unicorn identities. All previous 33 painted FBX files, including
the approved jaguar and horse family, are protected by pre-batch SHA-256 checks.
These are editable unrigged static drafts, not production-ready characters.

## Source facts and interpretation

All three are large level-4 unicorns with speed 24, armour class 2, magic
resistance 70, a 1d12 headbutt and 1d6 kick. All resist/confer poison resistance
and have herbivore, no-hands, wander, strong, jewels and infravisible flags.
Their source body/size/attacks agree, so compatible anatomy is shared rather
than inventing unrelated proportions for each coat. Each displayed identity and
both displayed sex forms are still verified separately. Sex differences have
not been inferred.

| Identity | Source distinction | Actual tile and art interpretation |
| --- | --- | --- |
| White unicorn (`PM_WHITE_UNICORN`) | `monsters.h:1010`; alignment +7, generation frequency 2; official tiles 206/207 | White coat, blue eye and cyan/blue stripe along the rear neck; interpreted as a blue mane and pale tail, with pale hooves and one forward/upward spiral horn |
| Gray unicorn (`PM_GRAY_UNICORN`) | `monsters.h:1018`; alignment 0, generation frequency 1; tiles 208/209 | Blue-gray body, pale/white rear-neck stripe, green eye, pale hooves; interpreted as a blue-gray unicorn with white mane and gray tail and the same spiral horn construction |
| Black unicorn (`PM_BLACK_UNICORN`) | `monsters.h:1026`; alignment -7, generation frequency 1; tiles 210/211 | Actual black body, brown rear-neck stripe and red eye; interpreted as charcoal coat with brown mane and dark tail, red fitted eyes, pale hooves and one spiral horn |

Alignment is retained as metadata; it does not add invented equipment, auras or
symbols. No armour, saddle, bridle, wings or jewellery was added. The jewels flag
does not establish a visible ornament. Body dimensions support miniature/grid
readability, not a literal conversion of source weight.

## Shadows and palette

White/gray tiles have a black cast-shadow fringe offset below feet and behind
neck/tail. Their mouth pixels at (4,6) and (3,7) are retained separately. The
white tile's blue vertical rear-neck column occupies the same position as the
gray tile's white and black tile's brown mane stripe; a separate offset shadow
continues to its right. This repeated placement supports a coloured mane,
rather than the winter-wolf-style shadow-derived blue coat interpretation.

The black tile reverses the palette roles: its `A` black pixels are actual
anatomy, while much of the offset `P` blue-gray fringe is shadow. Its spatial
mask uses the paired white unicorn's coloured anatomy/mouth coordinates,
retaining the black body and interior nose highlights while excluding the
corresponding outer fringe. Do not discard its black body or paint blue shadow
socks. The gray tile's `P` pixels are its actual coat, not universally shadow.
All original tiles remain untouched on the comparison board. These spatial masks
are approximate diagnostics, not claims of exact anatomical segmentation.

## Construction and artifacts

`UnicornFamily.py` uses the existing `EquineFamily.py` anatomy, fitted inner ears,
jointed legs and four single hooves. `EquineEyes.py` now accepts an optional iris
pigment while preserving the previous blue-eye default. New blue/green/red eyes
retain lateral skull-conforming apertures, horizontal pupils and coat-coloured
lids. No earlier models were regenerated.

A ray cast fits each horn to the centre of the forehead. Its base sits 6mm into
the saved skull rather than floating above it. Each horn is one closed tapering
mesh, .245m long at art scale, with mild integrated helical relief and painted
gold/cool grooves informed by the repeated yellow/gray source horn pixels.
There are no floating spiral strips or decorative sockets. Its keratin-like
surface uses the painted miniature material, rather than a metallic effect.

All three body vertex hashes match. The common shape is supported by matching
source morphology, while each coat/eye/mane combination is checked independently.
Short coats use the approved texture-only fur. Mane/tail remain continuous
long-hair silhouette masses, with no individual strands.

- `Art/CreatureInterpretations/CreatureBatch12.blend`: separate editable
  collections, corner paint, packed maps and studio camera/lights; white unicorn
  initially visible.
- `white_unicorn.fbx`, `gray_unicorn.fbx`, `black_unicorn.fbx` alongside the blend.
- `Batch12-Models.png`: actual studio mesh renders together.
- `MeshComparison-batch12.png`: original official tiles, actual front/rear views
  and true 16x16 projections. Six candidates per identity, bounds and explicit
  spatial masks are in `projection-report-batch12.json`.
- `Batch12-EyeReview.png`: six actual saved-mesh front/profile head/horn views.
- `batch12-mesh-inspection.json`: geometry, paint, UV, eye/ear fit, hooves,
  closed horn topology/root attachment, body hash and palette checks.
- `batch12-protected-assets.json`: pre-batch SHA-256 values for all prior 33 FBX files.
- `Batch12-Unreal-fixtures.png`: actual engine fixture capture with labels hidden.

Generate using Blender background mode, four threads, and
`Scripts/CreateCreatureBatch12.py`. Use `InspectCreatureBatch12.py`,
`ReviewCreatureBatch12.py` and `RenderCreatureBatch12.py` to inspect existing
geometry without regenerating it. The two comparison scripts use actual renders
and official pixels. No saved-scene anatomical repair was needed for this batch.
`RefineCreatureBatch12Palette.py` corrected tail paint to follow the coats after
source review, preserving every vertex coordinate; fresh generation already uses
the final tail pigments. The contrasting neck stripe does not establish a
contrasting tail.

## Unreal and verification

`ImportCreatureBatch12.py` imports only the three new meshes. The full importer
supports 36 candidates. Runtime selection uses only displayed identity/sex,
retains existing fallbacks, and uses -75 degree yaw for the new -X-facing equines.
F9 remains a no-turn style switch. `VerifyCreatureBatch12.ps1` tests six displayed
sex forms, six fallback cases, unknown identity, fur/UV/paint materials, native
movement/map, hero centring, 8x zoom and F9 both ways.

The capture uses the optional `-HideEntityGlyphs` launch flag. Ordinary launches
still show labels, and F7 toggles either initial setting. This keeps the engine
review clear while preserving the newly requested interactive toggle. Synthetic
fixtures display the three identities on revealed floor; they are not native
monster spawns.

- `build-creature-batch12-blender.log`: three models, painted FBX exports, six
  studio renders and 18 true 16x16 projections completed.
- `build-creature-batch12-inspect.log`: saved native checks passed, including
  one closed/attached horn and four hooves per identity, palette distinctions,
  common body hashes and all 33 protected prior exports.
- Native triangles: 108,016 per unicorn, 28 mesh parts per identity. Fur adds no
  geometry. Body/eye/ear/horn and front/rear comparisons were inspected.
- `build-creature-batch12-review.log`: six head views completed and inspected.
- `build-creature-batch12-palette.log`: saved tail-paint review preserved all
  geometry. `build-creature-batch12-renders.log` refreshed studio/projection views.
- `build-creature-batch12-unreal.log`: editor build passed.
- `build-creature-batch12-import.log`: final tail-palette exports reimported;
  three fur-material/paint checks, count 3 and successful editor exit.
- `build-creature-batch12-live.log`: six displayed sex forms, six fallbacks,
  unknown identity, materials/UV/paint and both F9 directions passed with native
  turn 4 unchanged. Native map/movement, hero centring and 8x zoom passed. Each
  engine mesh has 108,016 triangles, one fur slot and two UV channels. Initial
  labels OFF is logged; the actual clean engine capture was visually inspected.
- Final source/export/inventory reconciliation: 394 identities = 36 verified
  static drafts + 345 remaining creatures + 13 player-role presentations.
  Checkboxes are checked in place; all 33 earlier exports retain their hashes.

Finishing work remains separate: horn brushwork, mane/tail grooming, ear rims,
neck/shoulder transitions, rigs, gait/headbutt/kick animation, effects, LODs and
performance budgets. No combat animation, aura or production rig is claimed.

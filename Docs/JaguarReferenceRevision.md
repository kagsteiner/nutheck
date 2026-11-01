# Jaguar coat revision from the user's photograph

The user approved lynx and panther, but requested a more realistic jaguar pattern
and supplied `Foto 1.jpg`. The saved reference is
`Art/CreatureInterpretations/References/Jaguar-user-reference.jpg`. It is a user
photograph/reference image, not a mesh render.

The revised coat follows the photograph's distribution: dense irregular rosettes
over the flanks and spine, smaller solid head/neck/leg spots, pale underside and
lower legs, marked muzzle, and stronger tail bands with a dark tip. Rosettes have
thicker mostly complete irregular borders, varied size/placement and one to three
small central spots. This replaces the former sparse, regular flank-only pattern.
Warm gold/cream tones support the supplied reference while retaining the painted
miniature presentation. Existing jaguar anatomy, eye positions and triangle count
are preserved; this is a coat revision, not a new creature identity.

## Construction and files

- `Scripts/JaguarCoat.py`: deterministic paint sampling in cylindrical surface
  coordinates, wrapping across the spine and both flanks. Separate smaller spot
  fields cover the head and legs. Muzzle and ear-back details are painted too.
  Tail bands and terminal dark marking follow the existing raised tail.
- `WildCatPaint.py` calls this sampler for jaguar coat surfaces. The previous
  sparse rosette implementation is removed. Fresh `CreateCreatureBatch9.py`
  generation uses the revised palette, pattern and shading hook.
- `RepaintJaguarReference.py`: updates only jaguar corner colours in the existing
  `CreatureBatch9.blend` and exports only `jaguar.fbx`. It asserts the jaguar's
  vertex coordinates are unchanged. Lynx/panther geometry/paint signatures and
  complete FBX SHA-256 values must remain unchanged.
- `RenderJaguarReference.py`: refreshes jaguar studio/pixel views, broad flank
  and overhead-back inspection views. It retains lynx/panther projection records.
- `Jaguar-ReferenceRevision.png`: supplied photograph beside actual saved-model
  flank, back and head renders. `MeshComparison-batch9.png` and
  `Batch9-EyeReview.png` are refreshed with the new coat.
- `jaguar-reference-repaint.json` / `jaguar-reference-inspection.json`: protected
  asset signatures, paint statistics and measured regional coverage.

The coat remains vertex paint over the existing fur shader and shared maps. No
raised rings, spot geometry, fur clumps, alpha cards or extra triangles are added.
The supplied photo guides pattern rather than replacing the actual mesh views.

## Verification

- `build-jaguar-reference-paint.log`: repaint passed; jaguar geometry unchanged,
  lynx/panther mesh/paint and FBX files unchanged.
- `build-jaguar-reference-inspect.log`: independent saved-file check passed those
  protected signatures and verified dark pattern coverage on spine, both flanks,
  head and legs. No bare strip is left over the back.
- `build-creature-batch9-inspect.log`: native paint/UV/floor/eye/proportion checks
  passed again. Jaguar remains 102,392 triangles, with unchanged bounds and eyes.
- `build-jaguar-reference-renders.log` and `build-creature-batch9-review.log`:
  updated front-quarter/rear, side/back, true 16x16 and head views were inspected.
- `build-jaguar-reference-import.log`: only jaguar reimported; painted buffers and
  body-fur material validated, `SCULPTED_CREATURES_READY count=1`, successful exit.
- `build-creature-batch9-live.log`: all six displayed sex forms, six fallbacks,
  unknown identity, runtime paint/fur/UV checks and both F9 directions passed with
  turn 5 unchanged. Native movement/map, hero centring and 8x zoom passed. The
  revised actual engine fixture capture was inspected.
- Final source/inventory check passed: repaint scripts parse, protected FBX hashes
  agree, all five tested surface regions contain dense markings, and inventory
  remains 27. Lynx and panther geometry/paint signatures also match the saved
  pre-repaint values.

Generation inventory remains 27. The new reference-directed pattern is still
painted miniature art; exact photographic anatomy, coat grooming, production UVs,
LODs and animation are separate work. Do not restore the former sparse squiggles
or regenerate the approved lynx/panther to reproduce this correction.

# Tiger, hell hound pup and hell hound

The tenth batch extends the existing feline and canid construction with three
editable painted static drafts. The user approved the corrected jaguar coat
before authorizing this batch. All previous 27 FBX files, including jaguar, lynx
and panther, are protected by SHA-256 checks and have not been regenerated.

## Source facts and interpretation

| Identity | Pinned NetHack facts | Art interpretation |
| --- | --- | --- |
| Tiger (`PM_TIGER`) | `monsters.h:429`; large hostile carnivore, level 6, two 2d4 claws and 1d10 bite; official tiles 80/81 show orange/black stripes, green eyes, pale muzzle, raised tail | Larger strong feline body, dark branching stripes wrapping spine/flanks, pale underside/lower cheeks/paws, rounded dark-backed ears with pale marks, green fitted eyes and ringed tail |
| Hell hound pup (`PM_HELL_HOUND_PUP`) | `monsters.h:297`; small hostile carnivore, level 7, 2d6 bite and fire breath, fire resistance; tiles 50/51 show orange body, red eyes, pointed ears, raised tail and yellow/red mouth cue | Juvenile body with larger head relative to torso, shorter muzzle and legs, orange-red painted coat, fitted red eyes, open mouth, four small canines and warm yellow-orange tongue |
| Hell hound (`PM_HELL_HOUND`) | `monsters.h:304`; medium strong hostile carnivore, level 12, 3d6 bite and fire breath, fire resistance; tiles 52/53 use a taller orange canid with red eyes and yellow/red mouth cue | Taller, broader adult canid with longer muzzle/legs, strong chest, raised tail, fitted red eyes and open toothed mouth |

These dimensions support grid readability, not literal conversions of NetHack
weight/size. Male/female displayed identities share each mesh. The hounds have a
single head and ordinary canid anatomy; horns, armour, extra heads and lava cracks
are not inferred from their names.

The offset black edge beneath feet and beside tails is cast shadow. Projection
masks retain enclosed black markings while excluding background-connected black
fringe; tiger body stripes remain anatomy/paint. Original tiles remain untouched
on the comparison board. These are rough silhouette diagnostics, not exact
anatomical segmentations. The hounds' yellow/red mouth pixels inform the warm
tongue and open jaw. Their animated fire breath and lighting effects remain
separate work; a named mouth-location hook is saved on each body.

## Construction and review

`FelineFamily.py` and `CanidFamily.py` provide the existing continuous anatomical
sculpts, independent head/torso/limb/paw/ear/tail parameters, and skull-conforming
eyes with pupils and coat-coloured lids. No earlier family defaults changed.
Pup head/torso ratio is .504 versus adult .408; muzzle/head ratios are .744
versus 1.089; leg/torso ratios are .884 versus .985. The two hounds are therefore
independent proportions, rather than uniform scales of one mesh.

`CreatureBatch10Paint.py` paints tapered, winding and selectively forked tiger
stripes directly onto the continuous body, with leg bands and finer face marks.
It paints pale cheeks/underside and dark ear backs with pale marks. No stripe
objects or raised coat overlays exist. All coats use the approved shared
texture-only fur treatment and FurFlow UVs; no individual hair geometry is added.
The native checks measure dark coverage over spine and both flanks, in addition
to inspecting actual front/rear renders and close frontal/profile head views.

## Artifacts and reproduction

- `Art/CreatureInterpretations/CreatureBatch10.blend`: separate editable
  collections, corner paint, packed fur maps, studio camera/lights; tiger initially visible.
- `tiger.fbx`, `hell_hound_pup.fbx`, `hell_hound.fbx` alongside the blend.
- `MeshComparison-batch10.png`: official tiles, actual 16x16 reverse projections,
  and actual three-quarter/rear mesh renders. `projection-report-batch10.json`
  records six candidates per identity, masks and bounds.
- `Batch10-EyeReview.png`: actual saved-mesh front/profile heads, tails hidden
  for these isolated close views; all six views inspected.
- `batch10-mesh-inspection.json`: saved geometry/paint/UV/eyes/floor checks,
  independent juvenile/adult proportions, stripe coverage and prior-export hashes.
- `batch10-protected-assets.json`: pre-batch SHA-256 values for all prior 27 FBX files.
- `Batch10-Unreal-fixtures.png`: actual engine material/presentation capture
  using synthetic displayed-identity fixtures on revealed floor, not monster spawns.

Generate with Blender background mode, four threads, and
`Scripts/CreateCreatureBatch10.py`. Inspect existing geometry using
`InspectCreatureBatch10.py`, `ReviewCreatureBatch10.py`, and
`RenderCreatureBatch10.py`; inspection does not require regeneration. Assemble
the boards with `CreateCreatureBatch10Comparison.py` and
`CreateCreatureBatch10EyeComparison.py` using Python/Pillow.

The full Unreal importer now supports 30 candidates; `ImportCreatureBatch10.py`
targets only the three new meshes. Display selection uses only the shown monster
identity/sex. The new -X-facing quadrupeds use the established -75 degree yaw;
ordinary presentation retains tile-volume style and unsupported identities keep
their fallback. `VerifyCreatureBatch10.ps1` validates six displayed sex forms,
six fallback cases, unknown identity, fur/paint/UV materials, F9 both ways with no
turn, native map/hero centring and 8x zoom.

## Verification

- `build-creature-batch10-blender.log`: three native sculpts, painted FBX exports,
  six studio renders and 18 true 16x16 projections completed.
- `build-creature-batch10-inspect.log`: saved geometry, paint, fur UVs, floor,
  paired skull-conforming eyes, stripe coverage, independent age proportions
  and protected 27 prior exports passed. Native triangles: 120,468 tiger /
  48,116 hell hound pup / 79,674 hell hound.
- `build-creature-batch10-review.log`: six head views completed and inspected;
  three-quarter/rear source comparison and eye boards inspected.
- `build-creature-batch10-unreal.log`: editor build passed. Its normal per-user
  cache required sandbox escalation after a denied cache write on the first attempt.
- `build-creature-batch10-import.log`: three imports, fur material checks,
  count 3 and successful editor exit. Engine triangles: 120,468 tiger /
  48,109 pup / 79,670 adult (minor import cleanup relative to native geometry).
- `build-creature-batch10-live.log`: six displayed sex forms, six fallbacks,
  unknown identity, fur/paint/UV buffers and both F9 directions passed with turn
  5 unchanged. Native movement/map, hero centring and 8x zoom passed.
  The actual engine capture was inspected: all three fixtures are present, but
  foreground walls and glyph badges obscure portions of the hounds. Studio and
  head views provide unobscured geometry review.
- Final source/hash check passed; catalogue/backlog inventory reconciles to
  394 identities = 30 verified static drafts + 351 remaining creatures + 13
  remaining player-role presentations. Checkboxes are now checked in place.

All three are unrigged static drafts. Ear rims, toe details, neck/muzzle
transitions, coat flow, rigs, gait/attack animation, fire breath, LODs and
performance budgets remain finish work. Fine markings average away at overview
distance; studio views show details more clearly than the engine fixtures.

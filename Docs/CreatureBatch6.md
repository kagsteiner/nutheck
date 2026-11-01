# Dog, large dog and dingo

The sixth batch extends the canid construction with three complete editable
static drafts. The new anatomy uses independent torso, limb, skull, muzzle, ear,
paw and tail parameters, approved texture-only fur, and fitted eyes based on the
reviewed winter-wolf construction. Existing fifteen FBX files are not regenerated.

## Source and interpretation

| Identity | Pinned NetHack facts | Artistic assumptions |
| --- | --- | --- |
| Dog (`PM_DOG`) | `monsters.h:242`; medium, domestic carnivore, base level 4, bite 1d6; official tiles 36/37 use brown/orange, pale facial details, red mouth cue and lifted tail | Adult ginger dog continuing the little-dog miniature language, pale muzzle/bib, black nose, small tongue and curled tail; fitted amber eyes |
| Large dog (`PM_LARGE_DOG`) | `monsters.h:249`; medium abstract size, strong/domestic flags, base level 6, bite 2d4; tiles 38/39 retain the dog palette with larger outline | Broader and deeper adult chest, stronger limbs/paws and longer torso; head changes independently, so this is not a uniformly scaled dog |
| Dingo (`PM_DINGO`) | `monsters.h:235`; medium, hostile carnivore, base level 4, bite 1d6; tiles 34/35 have orange and pale peach colour masses | Leaner trunk, narrower skull, longer muzzle, pointed ears, pale underside and swept-down tail; black nose and amber eyes are anatomical interpretation |

The black ground fringe is a cast-shadow cue, not black socks or added anatomy.
Dog/large-dog palette `P` (blue-grey under the muzzle) is conservatively treated
as shadow, not coat. Projection fitting excludes these entries and records the
mask in its report; the comparison retains the untouched original tiles.
Black noses, eye rims and mouth lines are deliberate facial anatomy assumptions,
not extensions of ground-shadow pixels. Dingo's peach mass is interpreted as
countershading on the underside, not an inferred flesh-coloured appendage.

The red domestic-dog mouth cue is interpreted as a small tongue, continuing the
existing little dog. Exact breed, hidden markings and literal metre dimensions
are not specified by the source. Both displayed sexes share each body; no sex
differences or native inventory are inferred. Live domestic/pet relationships
remain controlled by NetHack, not the mesh.

## Artifacts and reproduction

- `Art/CreatureInterpretations/CreatureBatch6.blend`: separate named collections,
  editable anatomy/paint, packed coat maps, studio lights and camera; dog visible
  initially.
- `dog.fbx`, `large_dog.fbx`, `dingo.fbx`: painted static mesh exports alongside
  the blend, with floor origins and `FurFlow` coat UVs.
- `MeshComparison-batch6.png`: official tiles, actual true 16x16 projections,
  front-quarter and rear mesh renders. Six projection candidates per identity
  and bounds are in `projection-report-batch6.json`.
- `batch6-mesh-inspection.json`: native paint/UV/floor/eye and proportion checks.
- `*-head-front.png` / `*-head-profile.png`: matched actual head detail renders;
  tails are hidden in these isolated head reviews to keep them out of the view.
- `Batch6-Unreal-fixtures.png`: actual engine capture of synthetic displayed
  identity fixtures on revealed floor, not native monster spawns.

Generate via Blender background mode, four threads, and
`Scripts/CreateCreatureBatch6.py`. `CanidFamily.py` shares anatomy while preserving
species dimensions, chest paint, tail and muzzle differences.
`WinterWolfEyes.py` now accepts iris/lid pigments; its winter defaults are
unchanged. New canids use skull-conforming almond apertures, dark round pupils
and coat-coloured lids, with no floating eyeball geometry.

`CreatureBatch2Pipeline.py` applies paint/normals, exports and renders. Its new
coat rules blend the domestic bib and dingo underside on the continuous mesh.
Initial review restricted the dog's bib to the chest after it extended too far
onto the forelegs. Shadows are produced by the renderer.
`CreatureFur.py` uses the same two shared brush/normal maps and .82 roughness as
the approved study, with no new coat geometry. Future flow refinement remains.

Inspect saved geometry using `InspectCreatureBatch6.py`, render isolated eye
views using `ReviewCreatureBatch6Eyes.py`, and assemble the comparison with
Python/Pillow `CreateCreatureBatch6Comparison.py`. Inspection is separate from
generation.

Build `NUthEckEditor` and run `ImportCreatureBatch6.py` through full Unreal
editor startup Python. It imports only these three using the shared importer,
requiring painted buffers, fur slots and `SCULPTED_CREATURES_READY count=3`.
The full importer now supports eighteen drafts. New coat slots use the existing
verified `/Game/FurStudy/M_PaintedFur`; non-coat details retain shared pigments.

`VerifyCreatureBatch6.ps1` checks six displayed sex forms, six fallback cases,
unknown identity, fur material/UV/paint buffers and F9 both ways without a turn,
plus native map, hero centring and 8x preview zoom. Runtime selection still reads
only displayed species/sex. These quadrupeds use -75 degrees yaw. Ordinary
launches retain tile-volume presentation; F9 enables the sculpted candidates.

## Review, validation and limitations

- `build-creature-batch6.log`: three painted FBX exports, complete saved blend,
  six front-quarter/rear views and eighteen true 16x16 candidates completed.
  Source/render comparison sheet was inspected.
- `build-creature-batch6-inspect.log`: valid native geometry, CORNER/FLOAT_COLOR
  paint, FurFlow UVs/materials, floor clearance, paired eye symmetry, independent
  dog/large-dog proportions, leaner dingo/longer muzzle and distinct tails passed.
- `build-creature-batch6-eyes.log`: six saved-mesh frontal/profile head renders
  completed. All were visually inspected in `Batch6-EyeReview.png`, assembled by
  `CreateCreatureBatch6EyeComparison.py`.
- `build-creature-batch6-unreal.log`: editor module build succeeded.
- `build-creature-batch6-import.log`: three targeted imports, three fur-material
  checks and `SCULPTED_CREATURES_READY count=3`; editor exited successfully.
- `build-creature-batch6-live.log`: six displayed sex forms, six fallback cases,
  unknown identity and both F9 directions passed with turn 4 unchanged. Every
  new form passed runtime fur-material, UV and colour-buffer checks. Native map,
  hero centring and 8x zoom passed. Actual engine fixture capture was inspected;
  the glyph badges overlap parts of the view, so studio views are clearer.

| Mesh | Native triangles | Imported engine triangles | Fur slots / UV channels |
| --- | ---: | ---: | --- |
| Dog | 68,334 | 68,330 | 2 / 2 |
| Large dog | 86,734 | 86,734 | 2 / 2 |
| Dingo | 59,904 | 59,896 | 2 / 2 |

Head/torso length ratios are .456 / .428 / .375. Dingo torso width parameter is
.108m versus dog .130m; dingo muzzle .135m versus dog .112m. These are explicit
art dimensions. The native report preserves actual bounds and eye centres.
Backlog/catalogue closeout retains 394 source identities: 18 generated static
drafts, 363 remaining creature identities and 13 remaining player-role presentations.

These are unrigged static drafts. Paw/toe anatomy, muzzle/neck transitions,
eyelid refinement and coat flow remain finish work. No gait/attack animations,
LODs or production performance budget has been validated. Texture-only fur does
not add triangles; UV seams and shader sampling still have costs. A silhouette
score is a rough diagnostic, not proof of anatomy or exact tile reconstruction.

# Jaguar, lynx and panther

The ninth batch extends the established digitigrade, paired-muzzle feline
construction with three distinct wild-cat forms. They have complete editable
geometry, vertex-painted coats, fitted eyes and the approved body texture fur.
These are unrigged static drafts. The previous twenty-four FBX files are not
regenerated or retrofitted.

## Source facts and interpretation

| Identity | Pinned NetHack facts | Artistic assumptions |
| --- | --- | --- |
| Jaguar (`PM_JAGUAR`) | `monsters.h:397`; large, hostile carnivore, level 4; two 1d4 claws and 1d8 bite; tiles 72/73 use orange/brown/dark markings, green eyes, red mouth cue and raised tail | Broad head/chest and stronger limbs, orange-gold coat, irregular dark rosettes with occasional centre dots, pale muzzle/underside, rose nose and ringed tail |
| Lynx (`PM_LYNX`) | `monsters.h:405`; small, hostile carnivore, level 5; two 1d4 claws and 1d10 bite; tiles 74/75 show orange/peach, green eyes, pale cheek/flank details, ear-tip accents and a short tail; ASCII colour is cyan | Shorter torso, relatively large paws/head, pointed ears with attached dark tufts, painted pale cheek/flank blend and bobbed black-tipped tail; no cyan coat |
| Panther (`PM_PANTHER`) | `monsters.h:413`; large, hostile carnivore, level 5; two 1d6 claws and 1d10 bite; tiles 76/77 show black body, yellow eyes, sparse blue edge/interior accents and a long high tail | Longer, leaner feline frame, charcoal coat, yellow fitted eyes, dark paired muzzle pads and long curved raised tail; blue pixels treated as lighting accents, not painted blue fur patches |

The [San Diego Zoo jaguar reference](https://animals.sandiegozoo.org/animals/jaguar)
informs the rosette interpretation, including occasional dots inside rings. The
[Smithsonian lynx reference](https://nationalzoo.si.edu/animals/canada-lynx)
informs tufted ears, broad feet and short black-tipped tail. These supply useful
shape cues; they do not identify the NetHack lynx as a particular real species.
The named game identities, actual tile palette and gameplay traits take priority.

Head, torso, limbs, paws, ears and tails vary independently. Jaguar torso width
parameter is .148m versus panther .129m; panther torso length .345m versus jaguar
.320m. Lynx paw/body ratio is .288 versus jaguar .213. These are art dimensions
for grid readability, not conversions of NetHack size/weight. Both displayed
sexes share each mesh; no anatomical sex differences were inferred.

## Coat, eyes and shadows

`WildCatPaint.py` paints rosettes directly on the continuous jaguar body: varied
centres, broken irregular arcs and occasional central spots. There are no raised
spot or saddle meshes. Lynx cheek and flank colour is also blended on its body,
with darker paint at the bobbed tail tip. Fur is the shared texture-only treatment;
whiskers and the two lynx ear tufts are silhouette/anatomy details, not a dense
coat-hair system.

`FelineFamily.py` extends the previous feline family blockout. The shared fitted-eye
helper now accepts optional orbital position/orientation hints; previous bat/canid
defaults stay unchanged. New felines use more anterior apertures, green or yellow
irises, dark pupils and coat-coloured lids. The eyes conform to the actual saved
skull surface, and front/profile renders supplement numeric symmetry checks.

Jaguar/lynx silhouette diagnostics retain enclosed black markings within the
coloured figure, while black regions connected to the background are treated
conservatively as fringe/shadow. Reviewed lynx ear-tuft pixels are retained.
Panther retains its black anatomy, including head, ears, tail and limbs; only
eight reviewed outer-fringe pixels are excluded. Blue accents remain in the
source silhouette but are not converted into blue coat patches. These masks
are approximate diagnostics, not claims of exact pixel/anatomy ground truth.
Original tiles remain untouched on the comparison board.

## Artifacts and reproduction

- `Art/CreatureInterpretations/CreatureBatch9.blend`: separate editable identity
  collections, corner paint, packed coat maps, camera and studio lighting; jaguar
  initially visible.
- `jaguar.fbx`, `lynx.fbx`, `panther.fbx` alongside the blend: static painted exports,
  floor origins and FurFlow UVs on coat surfaces.
- `MeshComparison-batch9.png`: official tiles, actual 16x16 projections and actual
  front-quarter/rear model views. Bounds, six candidate poses per identity and
  explicit mask method/pixel exclusions are in `projection-report-batch9.json`.
- `Batch9-EyeReview.png`: six actual saved-mesh front/profile head views, with
  tails hidden only for these isolated close views.
- `batch9-mesh-inspection.json`: native geometry, paint, fur UV, floor, eye and
  species distinction checks, including painted rosette/cheek evidence.
- `Batch9-Unreal-fixtures.png`: actual engine capture with synthetic displayed
  identity fixtures on revealed floor, not native monster spawns.

Generate using Blender background mode, four threads, and
`Scripts/CreateCreatureBatch9.py`. The initial studio review joined lynx tufts
into the bevelled ears, replaced separate pale cheek ovals with body paint,
softened the regular jaguar rings into varied broken rosettes and refined the
nose placement. `RefineCreatureBatch9.py` applies that one-time repair to saved
meshes; the generator already contains the final construction. Do not repeat its
offsets merely to inspect the file.

Use `RenderCreatureBatch9.py` for saved studio/projection rerenders;
`InspectCreatureBatch9.py` for native checks; `ReviewCreatureBatch9.py` for head
detail. Python/Pillow comparison scripts assemble the boards from actual pixels.
`CreatureFur.py` uses the existing shared maps and shader, adding no fur geometry.

Build `NUthEckEditor` and run `ImportCreatureBatch9.py` via full editor startup
Python. Targeted import validates three meshes and reports count 3; the full
importer supports 27. `VerifyCreatureBatch9.ps1` checks six displayed sex forms,
six fallbacks, unknown identity, runtime fur/paint/UV materials and F9 both ways
without a turn, plus native map, hero centring and 8x zoom. All three use -75
degrees yaw like the other -X-facing quadrupeds. Runtime selection remains based
only on displayed identity; ordinary launches retain tile-volume presentation.

## Verification and remaining work

- `build-creature-batch9-inspect.log`: valid geometry, CORNER/FLOAT_COLOR paint,
  FurFlow UVs/materials, floor clearance and paired-eye symmetry passed. Jaguar
  initially had 4,491 dark painted corners and 170,310 gold corners; the later
  user-reference coat revision supersedes that sparse pattern, with no spot objects;
  lynx has two ear tufts whose bounds overlap the ears, no cheek-overlay objects,
  and a painted dark tail tip. Panther has no bright blue body paint.
- `build-creature-batch9-refine.log`: saved review corrections and three revised
  FBX exports completed. `build-creature-batch9-renders.log` refreshed six studio
  views and 18 true 16x16 candidates without regenerating anatomy.
- `build-creature-batch9-review.log`: all six head views completed. Front/profile,
  front-quarter/rear and the comparison boards were visually inspected.
- `build-creature-batch9-unreal.log`: editor build succeeded after an earlier
  automatic approval-review account-limit failure prevented the first build from
  executing. That review failure was resolved on the user's request to continue.
- `build-creature-batch9-import.log`: three imports, three fur-material checks,
  count 3 and successful editor exit.
- First live run passed all creature mapping/material/fallback/style checks,
  but the native movement smoke test stopped at turn 3: the faster player role
  consumed multiple inputs within one native turn. Capture now waits for the
  required minimum actual turn 4 before validating; the assertion is unchanged.
  The final build and full live rerun passed.
- `build-creature-batch9-live.log`: six displayed sex forms, six fallback cases,
  unknown identity and F9 both ways passed with turn 5 unchanged. Native movement,
  revealed map, hero centring and 8x zoom passed. The actual engine fixture capture
  was inspected; walls and glyph badges may obscure some body detail, while the
  studio and face views provide full visual inspection.
- Imported engine triangles: 102,392 jaguar / 74,368 lynx / 94,272 panther. All
  have two fur slots and two UV channels, with validated painted colour buffers.
- Catalogue/backlog reconciliation: 394 identities = 27 generated static drafts
  + 354 remaining creature identities + 13 remaining player-role presentations.

Native triangles: 102,392 jaguar / 74,376 lynx / 94,272 panther. Coat coverage,
rosette refinement, ear rims, toe detail and muzzle/neck transitions remain
finishing work. Fine facial/coat detail averages away at overview scale. No rigs,
gait/attack animation, LODs or production performance budget is validated.

## User-reference jaguar coat correction

The user approved lynx and panther and supplied a photograph to correct the
jaguar pattern. See [JaguarReferenceRevision.md](JaguarReferenceRevision.md) and
`Art/CreatureInterpretations/Jaguar-ReferenceRevision.png` for the current coat.
It has dense wrapping rosettes, smaller head/leg spots, pale underside/legs and
stronger tail markings. The prior sparse flank-only pattern is superseded.
Geometry and eye positions are preserved; lynx/panther mesh/paint and FBX hashes
remain unchanged. Counts remain 27 generated static drafts.

# Coyote, warg and rabid rat

The seventh batch reuses the parameterised canid family and the exact reviewed
lean sewer-rat body. These are editable, vertex-painted static drafts with
texture-only fur. Previous eighteen creature FBX files are not regenerated.

## Source facts and artistic interpretation

| Identity | Pinned source facts | Artistic assumptions |
| --- | --- | --- |
| Coyote (`PM_COYOTE`) | `monsters.h:213`; small, hostile carnivore, level 1, physical bite 1d4; official tiles 28/29 use brown/orange, pale eye pixels, red front facial pixel and extended tail | Slim long-legged canid, long muzzle, tall ears, pale fitted eyes, small red nose and raised brush tail; softer underside paint |
| Warg (`PM_WARG`) | `monsters.h:283`; medium, hostile carnivore, level 7, physical bite 2d6; tiles 46/47 show distributed grey/blue-grey dithering, pale eye/tooth details, red mouth and lifted tail | Broad chest, heavier skull/jaw and larger paws than coyote, restrained cool coat mottling, fitted pale eyes, open lower jaw, red oral surfaces and four ivory upper fangs |
| Rabid rat (`PM_RABID_RAT`) | `monsters.h:903`; tiny, hostile carnivore, level 2; bite 2d4 with `AD_DRCO`, poison resistance and poisonous-body flag; tiles 184/185 add a pale mass around/below the mouth to the brown/green-eye rat palette | Preserve approved lean sewer-rat anatomy, snout, whiskers, ears and green eyes; interpret the pale mouth mass as a separate froth/drool state module |

`AD_DRCO` means constitution drain (`include/monattk.h:73`). The asset does not
implement gameplay damage or poison resistance; these remain NetHack behaviour.
The froth is an art interpretation of these fantasy pixels, not a clinical model
of real-world disease. Both displayed sexes use the same body per identity.

Cast-shadow analysis is explicit: black ground fringe is excluded from anatomy
and projection fitting. Warg blue-grey palette P alternates across the interior
of the whole body, so it is treated as dithered coat shading, not blue socks or
ice shadow. It is blended subtly on continuous anatomy, not copied as a checker
texture or raised patch. The rat's ambiguous under-face blue-grey P is excluded
from projection fitting; its tiny previously approved nose glint is retained as
an artistic facial detail. The pale mouth mass is unique to the rabid-rat tile,
unlike the shared black cast-shadow fringe. No baked ground puddle is modelled.

## Assets and process

- `Art/CreatureInterpretations/CreatureBatch7.blend`: three named identity
  collections; coyote initially visible; editable geometry/paint, packed fur maps,
  studio lights and camera.
- `coyote.fbx`, `warg.fbx`, `rabid_rat.fbx` alongside the blend: static painted
  exports with floor origins and coat UVs.
- `MeshComparison-batch7.png`: untouched official tiles, actual 16x16 projections,
  front-quarter and rear views. Six candidate poses per identity, bounds and
  excluded shadow entries are in `projection-report-batch7.json`.
- `Batch7-EyeReview.png`: six actual frontal/profile head renders, with tails
  hidden only in these isolated head views. Includes jaw/froth detail.
- `batch7-mesh-inspection.json`: native geometry/paint/UV/floor/eye checks and
  exact reused rat-body position/paint comparisons.
- `Batch7-Unreal-fixtures.png`: actual engine capture using synthetic displayed
  identity fixtures on revealed floor, not native monster spawns.

Generate using Blender background mode with four threads and
`Scripts/CreateCreatureBatch7.py`. `CanidFamily.py` now accepts optional coat,
iris, nose, marking and tail parameters; existing batch-6 defaults are unchanged.
Coyote and warg differ in dimensions and tail construction, not only palette.
`WinterWolfEyes.py` supplies the same skull-conforming paired apertures and lids.

Rabid rat appends the saved `sewer_rat_*` objects from `CreatureBatch3.blend`.
Existing anatomy, paint and facial details are preserved. Texture-only fur is
added only to its continuous body, leaving bare tail, toes, ears and whiskers
alone. `CreatureSaliva.py` supplies five mouth-corner froth masses and two short
drool threads as separately tagged state objects. The prior rat files remain
unchanged. `CreatureFur.py` uses the same two shared brush/normal maps and shader
as the approved fur study, with no added coat triangles.

First studio review moved froth from beneath the muzzle onto the mouth corners
and lowered the warg jaw slightly. `RefineCreatureBatch7State.py` applies that
one-time saved-scene correction; the generator already contains the final values.
`RenderCreatureBatch7.py` refreshes saved renders without regenerating anatomy.
`InspectCreatureBatch7.py` performs saved native inspection;
`ReviewCreatureBatch7Eyes.py` supplies the head detail views. Python/Pillow
comparison scripts assemble actual renders; no concept image substitutes for a
model render.

Build `NUthEckEditor`, then run `ImportCreatureBatch7.py` via full editor startup
Python. The targeted importer validates three painted meshes and fur materials,
ending with `SCULPTED_CREATURES_READY count=3`. The full importer supports 21.
`VerifyCreatureBatch7.ps1` exercises both displayed sex forms, fallback, unknown
identity, runtime coat material/UV/paint buffers and real F9 switching without a
turn, plus native map, hero centring and 8x zoom. Selection remains displayed
identity only. These quadrupeds use -75 degrees yaw; ordinary launches retain
the tile-volume default.

## Review and verification

- Saved native checks passed for valid coordinates, CORNER/FLOAT_COLOR paint,
  coat UVs/materials, floor clearance and paired canid eye alignment.
  Warg body width .158m versus coyote .092m, and head/torso ratios .461 versus
  .404, verify independent forms. Four upper fangs and seven saliva-state objects
  are present. Evidence: `build-creature-batch7-inspect.log`.
- The reused rat body's vertex positions and original Paint values match the
  saved approved source exactly, checked by SHA-256 comparison. The report keeps
  the geometry hash; this is actual body reuse, not a rebuilt imitation.
- Front-quarter/rear, true 16x16 comparisons and all six head views were inspected.
  Evidence: `build-creature-batch7.log`, `build-creature-batch7-renders.log`,
  `build-creature-batch7-eyes.log` and the comparison boards.
- Unreal editor module build passed: `build-creature-batch7-unreal.log`.
- Three targeted painted imports and three fur-material checks passed; importer
  exited successfully: `build-creature-batch7-import.log`.
- Final live verification passed all six displayed sex forms, six fallback cases,
  unknown identity, runtime fur material/UV/paint buffers and both F9 directions
  with turn 5 unchanged. Native map, hero centring and 8x zoom passed. Evidence:
  `build-creature-batch7-live.log`.
- Capture-only placement now prefers floor within three cells of the hero before
  scoring wall clearance, when at least three such floors exist. This prevents
  a distant clear floor winning over a floor inside the hero-centred detail view.
  The final actual engine capture was inspected with all three new models visible.
- Imported engine triangles are 45,509 coyote / 90,542 warg / 46,668 rabid rat;
  all have two UV channels, with two fur slots for coyote and one for warg/rat.
- Backlog/catalogue closeout: 394 source identities, 21 generated static drafts,
  360 remaining creature identities and 13 remaining player-role presentations.


Native triangles: 45,516 coyote, 90,542 warg and 46,668 rabid rat. These are
procedural static drafts; no production LOD or performance budget is validated.
Eye rims, paws, neck transitions and coat flow still need refinement. Froth,
teeth and facial details largely disappear at 16x16; do not enlarge them into
implausible anatomy to chase silhouette overlap. No rigs, gait/attack animations,
animated drool or finished-state effects are included.

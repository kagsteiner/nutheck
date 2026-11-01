# Kitten, housecat and large cat

The fourth backlog batch establishes a reusable feline generator. These are
vertex-painted, unrigged static drafts, with complete editable geometry.

## Source facts and interpretation

| Identity | Pinned NetHack source facts | Artistic assumptions |
| --- | --- | --- |
| Kitten (`PM_KITTEN`) | `monsters.h:381`; small domestic carnivore with physical bite, base level 2; official tiles 68/69 show orange/peach coat, pale eyes, pink mouth and upright tail | Relatively large head, ears and paws on a shorter torso and legs; triangular ears, short paired muzzle pads, whiskers and curved tail |
| Housecat (`PM_HOUSECAT`) | `monsters.h:389`; small domestic carnivore with physical bite, base level 4; official tiles 70/71 share the palette and upright tail | Lean adult frame, longer torso/legs relative to the head; broad peach flank patch and lighter tail bands |
| Large cat (`PM_LARGE_CAT`) | `monsters.h:421`; small abstract size, strong/domestic flags, base level 6 and stronger bite; tiles 78/79 show a larger orange/peach outline and red mouth | Larger adult frame, more substantial paws and limbs, restrained body width, red nose/chin accent |

The three use one parameterised anatomy construction, with independent torso,
head, legs, ears, paws and tail dimensions. The kitten is not a uniformly scaled
adult. Male/female displayed forms share these bodies; no anatomical sex
differences were reconstructed. Actual starting-pet status comes from gameplay,
not the model. Metre sizes favour grid readability and are not conversions from
NetHack's abstract size or weight.

Orange/peach colour masses guide the coat. Patches and tail bands are vertex
paint on existing anatomy, not raised overlay objects. The exact hidden markings,
amber irises, ear lining and whiskers are interpretations. A lean standing body
continues the user's approved direction for animal anatomy; exact pixel silhouette
overlap is a diagnostic rather than the sole target.

## Assets and workflow

- `Art/CreatureInterpretations/CreatureBatch4.blend`: one named collection per
  identity; kitten initially visible; native geometry, paint, camera and lighting.
- `kitten.fbx`, `housecat.fbx`, `large_cat.fbx`: metre-based static FBX exports.
- `MeshComparison-batch4.png`: official tiles, actual 16x16 mesh projections,
  front-quarter and rear studio views. No AI concept artwork is used.
- `projection-report-batch4.json`: bounds and six camera candidates per creature.
- `batch4-mesh-inspection.json`: saved-mesh bounds, paint checks and age proportions.
- `Batch4-Unreal-fixtures.png`: actual engine capture with explicitly synthetic
  presentation fixtures on revealed floor, not native monster spawns.

Generate with Blender background mode, `--threads 4 --python
Scripts/CreateCreatureBatch4.py`, then run `Scripts/CreateCreatureBatch4Comparison.py`
with Python/Pillow. The shared `CreatureBatch2Pipeline.py` authors corner paint,
fixes normals, exports geometry and evaluates camera framing against the source.
`Scripts/InspectCreatureBatch4.py` inspects the saved blend without regenerating it.

Build `NUthEckEditor` and run `Scripts/ImportCreatureInterpretations.py` through
the full Unreal editor startup Python option. It imports twelve optional drafts,
assigns shared vertex-colour materials and validates colour buffers. Expected
marker: `SCULPTED_CREATURES_READY count=12`.

`Scripts/VerifyCreatureBatch4.ps1` checks both displayed sexes of all three cats,
default fallback, unsupported identity and real F9 switching without advancing
a turn, plus native map/hero and 8x preview-zoom checks. Fixture placement prefers
visible floor away from walls; it reads only the presentation map. Actual live
selection remains based only on displayed species/sex. All three cats use -75
degrees yaw, and ordinary gameplay defaults to tile-volume presentation.

## Review and remaining work

Initial studio review prompted flatter, more embedded eyes. The source colour
masses and upright tails remain, with deliberate kitten/adult proportions.
Further refinement should improve head/ear transitions, eyelids, muzzle/whisker
readability, coat brushwork and paw detail. Studio projections still differ from
the tiles and do not establish an exact reconstruction. Whiskers and toe creases
are close-view details, not substitutes for readable silhouettes.

No rigs, gait/attack animations, bitmap fur textures, final LODs or production
performance targets have been validated. The static proportions provide a basis
for later age-specific gait; they do not constitute animated gait variation.

## Verified results

- Blender generation and three FBX exports succeeded:
  `build-creature-batch4.log`. Front-quarter/rear views and the comparison sheet
  were visually inspected.
- Saved native inspection passed paint, valid geometry, floor clearance and
  distinct age/size checks: `build-creature-batch4-inspect.log`. The head/torso
  length ratio is 0.60 for kitten, 0.457 for housecat and 0.435 for large cat.
  Gallery collections must be enabled and transforms evaluated before reading
  world bounds; otherwise hidden collections can produce a false floor warning.
- Unreal module build succeeded: `build-creature-batch4-unreal.log`.
- All twelve imports passed painted-buffer/material checks:
  `build-creature-batch4-import.log`, ending with count 12.
- Live verification passed all six displayed sex forms, six fallback cases,
  unsupported identity and both F9 directions with turn 5 unchanged. Native map,
  hero centring and 8x preview zoom also passed: `build-creature-batch4-live.log`.
- Runtime painted colour buffers contain 25,409 kitten vertices, 31,543 housecat
  vertices and 37,119 large-cat vertices, using `M_Paint` as first material.
- The actual Unreal fixture capture was inspected. Cats remain small at gameplay
  scale and the glyph badge can obscure an individual preview; the studio sheet
  provides the clearer anatomy comparison.

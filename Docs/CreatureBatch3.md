# Sewer rat, giant rat and gnome ruler

Batch 3 follows the handoff and the next suggested backlog batch. These are
editable, vertex-painted static anatomical drafts, not finished rigged assets.

## Source constraints and art interpretations

| Identity | Pinned source facts | Artistic assumptions |
| --- | --- | --- |
| Sewer rat (`PM_SEWER_RAT`) | `monsters.h:889`; tiny animal, carnivore, physical bite; male/female tiles 180/181 have brown/ochre masses, green eye accents and a cool pale detail at the snout | Lean brown body on four legs, rounded cupped ears, bare curved tail, whiskers, incisors; cool detail treated as a nose glint |
| Giant rat (`PM_GIANT_RAT`) | `monsters.h:896`; also abstract `MZ_TINY`, higher base level/difficulty than sewer rat, physical bite; tiles 182/183 show a broader body | Larger frame than sewer rat, with a lean torso and restrained haunches; shared rat construction rather than uniform scaling |
| Gnome ruler (`PM_GNOME_RULER`) | `monsters.h:1702`; small humanoid, prince/rank flag and weapon attack; aliases gnome king/queen; tiles 344/345 show green clothing, yellow crown and orange detail | Existing gnome body with detachable pointed crown, orange jewel, dark green rank mantle, gold trim and fitted belt |

The crown is the approved rank interpretation. The retained axe is an art cue,
not guaranteed current inventory. Crown, clothing, trim, belt and axe remain
separate editable objects. Both displayed sexes share the body; no reconstructed
sex differences are claimed. Metre dimensions favour grid readability rather
than translating NetHack's abstract size/weight into physical measurements.

## Assets and reproduction

- `Art/CreatureInterpretations/CreatureBatch3.blend`: separate named collections,
  with sewer rat visible initially. Enable one collection at a time for review.
- `sewer_rat.fbx`, `giant_rat.fbx`, `gnome_ruler.fbx`: actual painted mesh exports.
- `MeshComparison-batch3.png`: actual front-quarter/rear studio renders, original
  official tiles and true 16x16 renders enlarged with nearest-neighbour scaling.
- `projection-report-batch3.json`: bounds, six camera poses per identity and rough
  silhouette-overlap diagnostic. This does not prove exact tile reconstruction.
- `Batch3-Unreal-fixtures.png`: actual engine capture with presentation-only
  fixtures on revealed floor; they do not represent native monster spawns.

`Scripts/CreateCreatureBatch3.py` parameterises compatible rat anatomy. It appends
the actual painted gnome parts from `CreatureBatch2.blend`, removes the cap, and
adds rank modules. Reused body paint remains intact; the mantle is repainted.
The crown is a hollow band with a pointed rim, fitted to the forehead.

The shared `CreatureBatch2Pipeline.py` accepts batch groups/output names and
preserves already-painted reused parts. It fixes normals, applies modifiers,
exports FBX and renders the source comparisons. Run:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --threads 4 --python Scripts/CreateCreatureBatch3.py
& 'C:/Users/agste/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' Scripts/CreateCreatureBatch3Comparison.py
```

Build `NUthEckEditor`, then run `Scripts/ImportCreatureInterpretations.py` through
the full editor startup Python option. It imports nine optional creatures into
`/Game/CreatureInterpretations/Meshes`, validates painted buffers and assigns
the shared vertex-colour materials. Expected final marker:
`SCULPTED_CREATURES_READY count=9`.

`Scripts/VerifyCreatureBatch3.ps1` launches a real native game with fixture-only
capture flags. It validates all six displayed sex forms, default fallback,
unsupported identity and F9 both directions without consuming a turn, followed
by native map, hero and zoom checks. The batch 3 fixture preview uses 8x zoom;
its camera validation explicitly expects that factor while ordinary zoom captures
retain the 3x check. Rats use -75 degrees yaw; ruler uses 15.
The default presentation remains the tile volumes. Only displayed identity is
used for selection; no hidden monster-state lookup was added.

## Visual review and remaining refinement

Studio views were inspected at front quarter and rear. Initial review prompted
a lower crown fit, replacement of the widened rectangular belt with a curved
garment-following belt, and bringing the rats' green eyes out of their sockets.

User review explicitly approved departing from the squat, floor-hugging tile
silhouettes: both rats should be thinner while retaining the successful snout,
whiskers, ears and colours. The revised generator reduces torso width/depth and
haunch bulk, keeping the original head dimensions, facial details, palette and
head/body height placement. The slimmer belly leaves more clearance above the
floor. Do not restore the round torso merely to increase tile silhouette overlap.
Before views are retained in `Art/CreatureInterpretations/BeforeRatSlimming/`.
`Art/CreatureInterpretations/RatSlimmingComparison.png` compares the actual
before/after studio renders. Sewer-rat torso radii are reduced to 74% of their
initial width/depth; giant-rat radii to 62% width and 60% depth, with smaller
haunches and a narrower stance. This is a body-shape revision, not whole-model
scaling. Native geometry/paint inspection, reimport and live checks passed again.

Further work should preserve this lean direction, strengthen small source colour
accents at 16x16, and improve the ruler's inherited neckline and equipment readability.
Whiskers and toes are close-view details; they do not solve overview recognition.
There are no rigs, animations, bitmap fur/skin textures, final LODs or measured
production performance claims.

## Verification evidence

- `build-creature-batch3.log`: native Blender generation, three FBX exports,
  actual studio renders and six reverse-projection candidates per creature.
- `build-creature-batch3-inspect.log` and
  `Art/CreatureInterpretations/batch3-mesh-inspection.json`: all mesh parts have
  FLOAT_COLOR/CORNER paint; ruler body vertex positions exactly match the
  existing gnome body; crown is a separate object and the old pointed cap is absent.
- `build-creature-batch3-unreal.log`: successful editor module build.
- `build-creature-batch3-import.log`: nine `SCULPTED_CREATURE_IMPORTED` markers,
  painted-buffer checks and `SCULPTED_CREATURES_READY count=9`.
- `build-creature-batch3-live.log`: six displayed sex forms, six fallback cases,
  unsupported-identity fallback and both F9 directions checked without advancing
  turn 5; native map, hero and zoom capture checks.
- Runtime colour buffers contain 23,526 sewer rat vertices, 30,772 giant rat
  vertices and 36,366 ruler vertices. All use the shared `M_Paint` material.
- Backlog/catalogue reconciliation checked all 394 unique source identities:
  nine verified drafts, 372 remaining creatures and 13 remaining player roles.
  Next suggested batch: kitten, housecat and large cat.

Studio comparisons are the clearest shape evidence. The live preview uses an
actual randomly generated starting room, so wall and glyph-badge occlusion can
still affect individual fixture views; it is not a staged engine beauty render.

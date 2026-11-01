# Three anatomical interpretations of the default tiles

This is the sculpted candidate alongside the retained tile-volume option.
The official NetHack 5.0 giant ant, little dog and goblin tiles are the references.
The intent is a complete object which could plausibly produce the small image,
rather than depth-extruding the image itself.

## Deliverables

- `Art/CreatureInterpretations/Concept-v1.png`: AI-generated design exploration,
  made with the built-in image generator; its full prompt is `concept-prompt.txt`.
- `CreatureInterpretations.blend`: actual editable Blender geometry, sculpted
  unions, folded cloth, material/vertex paint, studio lights and camera.
- `giant_ant.fbx`, `little_dog.fbx`, `goblin.fbx`: real mesh exports, with floor
  origins in metres and painted vertex colours for Unreal.
- `MeshComparison-v1.png`: **actual Blender renders**, showing each official tile,
  the model rendered at 16x16 and enlarged with nearest-neighbour sampling, plus
  three-quarter and rear views. AI artwork is never substituted for these renders.
- `projection-report.json`: six camera poses evaluated per creature. Source
  colour pixels form a rough silhouette mask excluding background and black
  drop-shadow pixels; this is not a final perceptual or anatomical quality score.

The concept sheet is more detailed than the current meshes. These are the first
anatomical drafts for judging proportions, palette and visibility from all sides;
they do not yet have fur textures, detailed skin, rigs, animations or final LODs.

## Interpretation choices

| Creature | Source constraints | Artistic assumptions |
| --- | --- | --- |
| Giant ant | Brown tile; bite attack; animal/insect; `MZ_TINY` | Three main body sections and a pinched waist, six legs originating on the thorax, elbowed antennae, biting mandibles; the tiny cyan detail is interpreted as an eye glint |
| Little dog | Ginger default sprite, pale face/eyes, red mouth detail; domestic quadruped; `MZ_SMALL` | Compact spitz/terrier anatomy, pointed ears, connected shoulders/hips, cream muzzle/bib, lifted curved tail |
| Goblin | Brown/magenta/green colour masses; small humanoid with weapon attack | Tan skin, green eyes, broad ears and hooked nose, brown leather cap, magenta tunic/cape, belt, boots and a small dagger |

The dagger is an artistic cue, not an assertion about a particular live goblin's
inventory; production equipment should be detachable. The first three meshes
are sex-neutral anatomical drafts shared by the displayed male/female variants.
Chosen metre dimensions favour grid readability and are not inferred physical
measurements from NetHack's abstract size/weight fields.

The code references are `include/monsters.h` entries for `GIANT_ANT`, `LITTLE_DOG`
and `GOBLIN`, and `win/share/monsters.txt` tiles 0, 32 and 144 (male references).

## Reverse-projection workflow

`Scripts/CreateCreatureInterpretations.py` builds the meshes from native Blender
geometry, applies sculpt/cloth modifiers, fixes face normals and exports FBX.
It renders three-quarter/rear views and six 16x16 camera candidates. Projection
scale and camera shift match the source colour-pixel bounding box so a change
in framing is not confused with an anatomical difference.

`Scripts/RefitCreatureProjections.py` repeats only the camera search on the saved
Blender file. `Scripts/CreateCreatureComparison.py` assembles the source pixels
and actual renders into the comparison sheet using deterministic image scaling.

The first comparisons still differ substantially from the source sprites.
Useful next adjustments are the ant's body angle/leg spread, the dog's head and
chest proportions, and the goblin's crouch and arm spread. The report is evidence
for those decisions, not a claim that the original tiles have been reconstructed.

## Unreal option

`Scripts/ImportCreatureInterpretations.py` imports the three meshes into
`/Game/CreatureInterpretations/Meshes`, checks their colour buffers, and assigns
shared paint, chitin, metal and eye materials.

The original tile-volume style remains the default. Launch with
`Scripts/LaunchPrototype.ps1 -SculptedCreatures`, or press **F9** in the live game
to toggle the candidate for these three species. Other species and player roles
continue to use their existing representations. Only the core's displayed
species identity selects a model, preserving the existing perception boundary.
Switching style rebuilds the presentation and sends no command to NetHack.

## Rebuild

1. Run Blender with `--background --threads 4 --python Scripts/CreateCreatureInterpretations.py`.
2. Optionally run `Scripts/RefitCreatureProjections.py` in Blender for a camera-only iteration.
3. Run `Scripts/CreateCreatureComparison.py` with Python and Pillow.
4. Compile `NUthEckEditor` after code changes.
5. Run the full Unreal editor with `-ExecutePythonScript=<absolute path>/Scripts/ImportCreatureInterpretations.py -unattended -nosound -nop4`.

All three static mesh imports must report `SCULPTED_CREATURE_IMPORTED` followed
by `SCULPTED_CREATURES_READY count=3`. Vertex-colour shader connections are
explicitly checked for success.

## First validation

- All three final FBX imports passed colour-buffer checks and reported
  `SCULPTED_CREATURES_READY count=3` in `build-sculpted-import.log`.
- Unreal compilation succeeded. A live depth-one capture loaded
  `Sculpted_little_dog_female` through the normal displayed-glyph mapping.
- The capture passed native turn/map, 2.986x zoom/hero centring and figure checks
  in `Saved/Logs/Verification-cb01c69c08a849d5917b1655a28a9866.log`.
- `LiveSculptedDog.png` is the actual Unreal capture, separate from the concept
  and studio comparison images.
- Six aligned pixel projections per creature were rendered and inspected.
  Best rough silhouette-mask overlap is recorded in `projection-report.json`.
  These initial fits are incomplete and should guide further pose/proportion
  work; they are not a reconstruction-success criterion.

- The actual F9 shortcut was checked in the reopened dog level: it switched to
  default tile volumes and back to sculpted candidates, both at turn 5.
- The saved Blender source is organised into three named creature collections.
  The ant is visible initially; enable another collection to inspect that draft.

## Second batch

Jackal, fox and gnome now extend the optional sculpted mode to six species.
See [CreatureBatch2.md](CreatureBatch2.md) for files, source assumptions and checks.

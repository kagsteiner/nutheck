# nUthEck: painted miniature direction, study 01

**Current direction:** [GameVision.md](GameVision.md) governs current work:
NetHack tactics, modern graphics and static models, without character/object
animation. The latest environment reference is the left Carved stone panel.
The selection and painted-pass notes below describe the earlier study.

The selected direction is the **centre, Painted miniature** column of
[VisualDirections-v1.png](../Art/Studies/01-MiniatureDungeon/VisualDirections-v1.png).
The concept board was made with the built-in image-generation tool;
its complete prompt is saved beside it in `concept-prompt.txt`.

The concept board is an aspirational visual target. `BlenderStudy.png` and the
`Unreal-*.png` files are actual renders of the editable geometry. The concept
image is never substituted for geometry or presented as an engine screenshot.

## Shared visual rules

- Tangible, sculpted miniatures, with broad readable shapes and softly worn edges.
- Warm slate/limestone dungeon, oxblood cloth, aged bronze, restrained teal accents.
- Use the same material library for every model. `palette.json` is the shared
  source for Blender materials and Unreal material instances.
- Stone and cloth are matte; chitin has a restrained sheen; metal gets a broad
  highlight rather than a mirror finish. Avoid unrelated texture packs and
  arbitrary per-asset colour grading.
- Distinguish creatures through silhouette, anatomy and proportions before
  adding small details. Details that disappear at the full-level view are
  secondary to recognition and readable lighting.
- Floors use a consistent joint/bevel scale. Walls are 1.2 m tall so shadows
  remain visible while most overhead content can still be read.
- Keep the one-metre gameplay grid. Exaggerate identifying features within
  that footprint; large creatures need a deliberate later solution.
- Check every family at room scale, full-level scale, close zoom and eye level.
  Detailed geometry cannot replace glyph labels at the full-level distance.

## What exists in this study

`Scripts/CreateArtStudy.py` creates the editable Blender scene, six FBX exports
and a Blender render. Geometry is authored procedurally in Blender, with shared
bevels, smooth organic forms and sculpted cloth folds. No third-party mesh
collection is mixed in. The first version's harder forms and pale stone were
too close to the carved-stone concept; the painted pass changes geometry,
pigment, palette and lighting together.

| Asset | Shape/readability test | Current state |
| --- | --- | --- |
| Room | Masonry courses, capped walls, open timber door, stairs, crates, potion, scroll, coins | Static environment study |
| Hero | Cloak, helmet, shield and sword form a compact silhouette | Static mesh; not a specific role |
| Dog | Four legs, muzzle, pointed ears, tail and collar | Static quadruped study |
| Ant | Three body sections, six jointed legs, antennae and mandibles | Static insect study |
| Goblin | Small humanoid, large ears, nose, club and loincloth | Static humanoid study |
| Jelly | Low, broad organic mass and lobes | Opaque material study; not bound to blue jelly |

Each creature export has a floor-centred local origin. Placement in the study
is supplied separately in Unreal. The room is combined for this first import;
its Blender objects remain separate and can become reusable modular exports.
The stairs currently test silhouettes/materials rather than a functioning
opening. There are no rigs, creature animations, bitmap textures or damage
states yet. The working meshes are an early approximation of the
concept direction, not finished production sculpts.

## Painted pass

The original comparison renders, Blender scene, palette and source scripts are
preserved in `BeforePaintedPass/` beside the study. The current version adds:

- A warmer, deeper limestone palette and richer crimson cloth/aged bronze.
- Mixed-length flagstone rows, irregular stone vertices and less uniform bevels.
- Smooth organic surfaces, folded tunic/cape meshes, goblin pupils, brows,
  mouth/fangs, cheekbones, hands and ear details; dog eyes/toes and ant carapace.
- Restrained per-corner vertex paint: broad pigment variation and warmer
  highlights, with darker lower areas and undersides. This is authored colour
  data, not baked lighting or a claim of hand-painted bitmap textures.
- A shared `Tint * VertexColor` Unreal material. FBX imports explicitly replace
  vertex colours; the same data modulates Blender's base colours.
- Torch geometry, a small emissive material parameter, and two warm shadowed
  point lights. The study's fill/key balance is reduced to preserve contrast.

The vertex paint remains deliberately subtle. The selected concept image still
sets the quality target for further sculpting and brushwork; consistency alone
does not make these initial procedural meshes final art.

## Reference catalogue and identity

`Scripts/CreateTileCatalogue.py` extracts all named entries from the checked-out
NetHack 5.0 `monsters.txt`, `objects.txt` and `other.txt`. Output:

- `OfficialTileCatalogue.csv`: every reference entry and its file-local index;
  unassigned model-family, asset and status columns leave room for production.
- `OfficialTileReferences.png`: eight labelled original tiles, enlarged with
  nearest-neighbour sampling, spanning several useful model families.
- `catalogue-summary.json`: source-entry counts, not unique species counts.

These are official source references, not a visual commitment to the original
pixel palette. The entry count includes sex variants and non-monster entries.
Use `include/monsters.h`, `include/objects.h` and `dat/data.base` when preparing
species briefs. Tiles alone do not fully describe anatomy or behaviour.

This study is deliberately separate from live glyph-to-asset binding. When
binding comes next, use the compiled glyph mapping for our pinned NetHack
version rather than treating a reference-file index as a glyph ID. Appearance
must follow displayed glyphs, including disguises and unidentified appearances.
The entire-model catalogue must never reveal hidden game information.

## Reproduction

1. Run `blender --background --threads 4 --python Scripts/CreateArtStudy.py`.
2. Build `NUthEckEditor` with the usual Unreal build command.
3. Run Unreal Editor's startup Python with
   `-ExecutePythonScript=Scripts/ImportArtStudy.py` using an absolute script
   path and `-unattended -nosound -nop4`. It creates `/Game/ArtStudy` assets,
   material instances and imported static meshes.
4. Run `Scripts/LaunchArtStudy.ps1`. The `-ArtStudy` mode uses the existing
   Unreal camera controls and loads the six imported meshes.
5. Capture with `Scripts/LaunchArtStudy.ps1 -Capture -View overview`, then
   `detail`, `eye` or `level`. Logs require an explicit `ART_STUDY_CHECK PASS`.

`overview` frames the whole test room; `detail` starts at 2.2x; `eye` starts
inside the hero position; `level` shows the room at the original 79x21 level
framing. Ctrl+F, mouse-wheel zoom, middle-drag pan, right-drag look and F5 reset
are available in the interactive study. F5 resets the current study's framing.

The image generator created only the comparison board. Actual geometry comes
from Blender, and actual Unreal screenshots are labelled as such.

`Scripts/BuildArtStudy.ps1` automates export, compilation and import in that
order. It uses a hidden editor with its UI runtime initialized: this UE version's
Interchange import callbacks require Slate, including during automated imports.
The import script defers editor exit until the startup callbacks have completed.

## Next production decision

Review the actual room and creature silhouettes against the selected centre
column. Refine one creature and one environment module to the desired finish
before multiplying them into a bestiary. The painted pass addresses irregular
stone, cloth folds, facial details, pigment variation and local warm lighting.
Further work should refine anatomy, material brushwork and small animations,
while retaining the shared palette and scale rules.

## Baseline validation of study 01

- Blender 5.2.2 exported all six mesh groups and saved the editable source.
- Unreal 5.7 editor compilation succeeded without C++ warnings.
- Final import exited with code 0 and reported all six `ART_STUDY_IMPORTED`
  entries plus `ART_STUDY_IMPORT_READY`; evidence is `build-art-import.log`.
- The final overview, detail, eye and level runs each reported
  `ART_STUDY_CHECK PASS`, and their actual PNGs were inspected.
- The whole-level view makes the figures small, as expected from one-metre
  cells across a 79x21 map. Preserve the live renderer's glyph badges when
  these models are subsequently bound to gameplay.
- This proves the geometry/material pipeline and camera compatibility. It does
  not yet validate animation, live species binding or final art quality.

Baseline capture logs in `Saved/Logs/` (images preserved in `BeforePaintedPass/`):

| View | Log |
| --- | --- |
| overview | `ArtStudy-f952f8991c1d4c76be2d4c5ce0891eff.log` |
| detail | `ArtStudy-61b80bd1a7084f69868b8e980ea471c5.log` |
| eye | `ArtStudy-c0e0fb2040854b53baaed7515a817b83.log` |
| level | `ArtStudy-2e186dc4f0cd458f9047886f43aecba5.log` |

## Validation of the painted pass

- Blender exported and rendered the revised geometry and per-corner `Paint`
  colour layer. The editable `.blend` and FBX exports include this data.
- Unreal compilation passed without C++ warnings. Final import exited with
  code 0, and all six meshes passed `StaticMeshEditorSubsystem.has_vertex_colors`.
  Evidence: `build-painted-import-verified.log`.
- The final captures check that the two point lights actually occupy their
  wall-torch positions; moving the actors is performed after making their
  light components movable. Logged positions are (-458,-220,118) and
  (458,200,118) cm. This prevents the initial floor-origin hotspot recurring.
- Overview, detail, first person and whole-level captures passed and were
  visually inspected. `Unreal-*.png` now contains the painted pass.

Final painted-pass capture logs in `Saved/Logs/`:

| View | Log |
| --- | --- |
| detail | `ArtStudy-b607624df8934a9cae568892fbc44727.log` |
| overview | `ArtStudy-4dfca2e33ebe4a4c80ba08b0cf6d67fd.log` |
| eye | `ArtStudy-c811defc0c754a798698b6e691096e89.log` |
| level | `ArtStudy-c0135afc750540759a6cacc312303371.log` |

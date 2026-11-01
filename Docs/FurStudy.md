# Restrained fur comparison: dog and housecat

The user authorized a three-way comparison and explicitly rejected individual
hair and polygon-heavy fur. This study compares real geometry and materials:

| Variant | Change | Extra dog triangles | Extra cat triangles |
| --- | --- | ---: | ---: |
| Smooth | Existing painted surface | 0 | 0 |
| Painted | Subtle directional brush colour modulation and shallow normal texture | 0 | 0 |
| Tufted | Painted texture plus a few broad, closed coat clumps | 80 | 32 |

The source models are the current little dog and housecat, with their geometry,
proportions, vertex-painted colour masses, eyes, nose and whiskers retained.
The smooth dog already has the original generator's small ruff tufts; the last
column measures additions relative to that existing mesh, not a hypothetical
entirely tuft-free dog.

## Deliverables

- `Art/FurStudy/FurComparison-Blender.png`: actual close renders plus actual
  64x64 and 16x16 renders, with the small samples enlarged nearest-neighbour.
- `Art/FurStudy/FurComparison-Unreal.png`: crops of real engine captures at close,
  gameplay and whole-level camera widths. This is a staged comparison, not a
  native gameplay screenshot. The full captures are `Unreal-close.png`,
  `Unreal-gameplay.png` and `Unreal-level.png` beside the board.
- `Art/FurStudy/FurStudy.blend`: six editable collections, with the painted dog
  visible initially; enable one collection at a time. Shared texture files are
  relative to the blend in `Textures/`.
- Six FBX files named `{little_dog,housecat}_{smooth,painted,tufted}.fbx`.
- `Textures/FurBrush.png` and `FurBrushNormal.png`: two shared 512x512 maps.
- `study-manifest.json`: parts, triangles, fur surfaces and incremental counts.
- Unreal assets are isolated under `/Game/FurStudy`; the twelve canonical creature
  imports and their live mappings are unchanged. No bestiary-wide fur selection
  has been made. Generation checklist counts remain twelve.

## Surface treatment and cost

The brush map is deterministic, tileable, low-contrast painted strokes, with
mean-neutral colour multiplication over the existing vertex paint. UV direction
is projected along the body and down legs/tails; it is a first flow approximation,
not a hand-unwrapped production coat. A shallow normal map adds local response to
light without changing the silhouette. Eyes and non-coat facial details retain
their previous materials. Both renderers use linear brush data, shared roughness
and the same modulation; Unreal's normal import flips the green channel for its
tangent convention. Mipmaps let small marks average away at distance.

There are no strands, fur shells, alpha cards, groom simulation or displacement.
The tufted dog adds ten broad clumps; the cat adds four smaller clumps. The texture
variants add no triangles, but UV seams split some render vertices and two texture
samples add shader work. Existing procedural base meshes are still 52,642 dog
triangles and 57,420 housecat triangles; this study does not replace later LOD,
material-section and performance work. No frame-rate improvement or final budget
compliance has been measured.

## Reading the comparison

Use the close views to judge surface feel, and the small views to judge whether
fur obscures the broad NetHack colour/silhouette identity. The intended result is
a painted miniature with a suggested coat, rather than photographic fur.

The texture-only version is the current recommendation for the cat. The added
clumps give a little more dog silhouette, but the current clumps read angular
under Unreal's directional light, especially on the tail. Prefer the middle
variant as the general starting point; keep clumps selective and subject to
review rather than applying them indiscriminately. This is a recommendation,
not a recorded user choice or a bestiary-wide rollout.

## Reproduction and verification

1. Run `Scripts/CreateFurTextures.py` with Python/Pillow/NumPy.
2. Run Blender background mode, `--threads 4 --python Scripts/CreateFurStudy.py`.
   To refresh only textures/renders, use `Scripts/RenderFurStudy.py` instead of
   regenerating geometry.
3. Build `NUthEckEditor`, then run `Scripts/ImportFurStudy.py` via full editor
   startup Python. Require six `FUR_STUDY_IMPORTED` entries and
   `FUR_STUDY_IMPORT_READY variants=6 textures=2`.
4. Run `Scripts/CaptureFurStudy.ps1`. Its isolated `-FurStudy` scene uses equal
   directional lighting, poses and six variants at 680cm close, 1211.3cm gameplay,
   and 9700cm whole-level camera widths; close/gameplay use different elevations
   appropriate to their purpose. Every variant at a given scale shares the same
   camera and lighting. The scene starts no NetHack process and includes no HUD.
5. Run `Scripts/CreateFurComparisons.py` to assemble boards from actual pixels.

Native manifests assert no triangle increase for the painted version and at most
160 added triangles for the sparse-clump version. Unreal capture checks validate
six imported meshes, colour buffers, matching smooth/painted triangle counts,
bounded tuft additions and valid camera projections. Logs report actual render
vertices, triangles, UV channels and crop anchors.

Evidence: `build-fur-study.log`, `build-fur-renders.log`, `build-fur-unreal.log`,
`build-fur-import.log`, and `build-fur-{close,gameplay,level}.log`.

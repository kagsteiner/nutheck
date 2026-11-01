# Jackal, fox and gnome anatomical drafts

Built on 2026-10-30 following `CreatureAssetContext.md`, after the user's explicit
instruction to suggest and build three creatures. These extend the existing
painted-miniature drafts with two compatible canids and a small humanoid base.

## Source facts and interpretations

The pinned local NetHack source and official `win/share/monsters.txt` are the
references. File-local tile indices are reference locations, never runtime IDs.

| Creature | Source facts | Artistic assumptions |
| --- | --- | --- |
| Jackal (`PM_JACKAL`, tiles 24/25) | Small carnivorous animal, physical bite; pale grey body, pink and peach accents in the male tile | Slim four-legged canid, large pointed ears with pink lining, narrow muzzle, raised thin tail, darker fur painted directly onto the back |
| Fox (`PM_FOX`, tiles 26/27) | Small carnivorous animal, physical bite; orange horizontal silhouette and dark foot masses | Lower body and shorter legs than jackal, tapered head, triangular ears, broad descending brush and pale tail tip |
| Gnome (`PM_GNOME`, tiles 338/339) | Small humanoid, omnivorous, weapon attack; green clothes/cap, red accent, pale face and dark side mass | Pointed green cap with red tip, pale beard, green tunic/mantle, boots and detachable axe |

The axe is a visual interpretation, not guaranteed live inventory. Clothes,
cap and equipment remain separate mesh objects in Blender. No crown/ruler
variant was generated. All three bodies are shared across displayed sexes;
no anatomical sex differences are claimed. Dimensions favour the gameplay grid
and are not literal conversions of NetHack size or weight.

## Files and process

- `Art/CreatureInterpretations/CreatureBatch2.blend`: three named collections,
  editable geometry, corner vertex paint, camera and lighting. Jackal is visible
  initially; enable one collection at a time to inspect other species.
- `jackal.fbx`, `fox.fbx`, `gnome.fbx`: metre-based static mesh exports.
- `MeshComparison-batch2.png`: official tiles, actual 16x16 renders enlarged by
  nearest-neighbour, three-quarter and rear views. No AI concept image is used.
- `projection-report-batch2.json`: bounds, six camera candidates per species,
  best rough silhouette overlap and actual render filenames.
- `Batch2-Unreal-fixtures.png`: actual engine capture with explicitly synthetic
  presentation fixtures on revealed floor; these are not native spawned monsters.

`Scripts/CreateCreatureBatch2.py` defines a parameterised canid family, keeping
jackal and fox proportions and tail geometry distinct. `CreatureGeometry.py`
reuses the first batch's mesh construction and palette conventions.
`CreatureBatch2Pipeline.py` applies modifiers, recalculates normals, authors
FLOAT_COLOR/CORNER paint, exports FBX, renders views and searches projection
framing against the source coloured-pixel bounds.

Reproduce with Blender background mode, `--threads 4 --python
Scripts/CreateCreatureBatch2.py`, then run
`Scripts/CreateCreatureBatch2Comparison.py` with Python/Pillow. Build the
NUthEckEditor module and run `Scripts/ImportCreatureInterpretations.py` through
the full editor startup Python option. It now imports six meshes, checks colour
buffers, assigns shared vertex-colour materials and logs
`SCULPTED_CREATURES_READY count=6`.

The runtime allowlist includes six species, chosen only from displayed identity.
Canids use -75 degrees yaw; gnome/goblin use 15 degrees. Default tile volumes
remain the default presentation; F9 enables the optional sculpted candidates.
Unsupported identities retain the prior representation.

`Scripts/VerifyCreatureBatch2.ps1` runs a real native game, checks both displayed
sex aliases of every new species, validates default fallback and an unsupported
identity, toggles F9 in both directions, and asserts the turn stays unchanged.
Its preview option places only presentation fixtures, without modifying gameplay.

## Quality limits

These are unrigged static procedural drafts, with vertex-painted surfaces and
no bitmap fur/skin textures, animations or production LODs. Actual renders were
inspected from front quarter and rear. The gnome garment was enlarged and centred
after the first render revealed torso clipping. Further work should refine its
neckline/belt fit, reduce the jackal's rounded head and refine the canid coat
markings. The 16x16 views differ visibly from the tiles; silhouette overlap is
a diagnostic, not a claim of exact reconstruction. The gnome's thin axe is
especially sensitive to camera angle.

The initial jackal incorrectly represented its darker back fur as a raised oval
mesh. This was removed following user review. The marking now blends vertex
colours on the continuous anatomical body; it adds no surface geometry.

## Verified results

- Blender generation and all three FBX exports succeeded; final studio views and
  comparison sheet were visually inspected. Evidence: `build-creature-batch2.log`.
- Unreal module build succeeded: `build-creature-batch2-unreal.log`.
- All six mesh imports passed paint checks and material assignment:
  `build-creature-batch2-import.log`.
- Live mapping passed all six sex aliases and six default fallback cases. F9
  switched to default and back while turn remained 5. Native live map, zoom and
  hero checks also passed: `build-creature-batch2-live.log`.
- Actual runtime colour buffers contain 27,279 jackal vertices, 25,539 fox
  vertices and 35,161 gnome vertices, all using `M_Paint` as their first material.
- The live fixture image was inspected. At this gameplay zoom the miniatures
  remain small and the gnome is partly obscured by the player's glyph badge;
  the studio comparison provides the clearer shape review. No animation or
  performance target is claimed.
- After the jackal correction, Blender inspection confirmed the back overlay is
  absent and the body carries the coat-paint metadata (`build-jackal-coat-inspect.log`).
  Studio views, FBX, native blend, comparison and Unreal fixture capture were
  refreshed. Reimport and live checks passed again, with F9 retaining turn 5.

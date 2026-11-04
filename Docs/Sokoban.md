# Sokoban: the ancient puzzle vault

Implemented 2026-11-03 from the approved design: warm sandstone ashlar, dark
foundations, matte square paving, natural grey boulders and restrained bronze.
Keep the established high walls and every native puzzle rule. Unlike the Oracle's
white marble sanctuary, this branch feels like an old, carefully built stone vault.

## Native facts and information boundaries

The pinned native source has two layouts for each of four floors:
`upstream/NetHack/dat/soko{1,2,3,4}-{1,2}.lua`. The native branch is entered on
its fourth dungeon level and ascended toward its first. The presentation stages
are therefore 1 through 4 in the opposite order. The maps, boulders, traps,
premapping, restrictions and rewards are native; no level script was changed.

The bridge reports `in_sokoban` using `In_sokoban(&u.uz)` and `sokoban_stage`
as `5-u.uz.dlevel` within the branch, otherwise zero. Native saved dungeon
coordinates already persist this identity across saving, leaving and returning.
It never depends on a monster or a surviving puzzle object. No save-format
extension is needed.

`display_trap` is added only for a foreground cmap glyph that actually displays
`S_pit` or `S_hole`. Other traps retain their native fallback. The bridge does
not inspect a hidden trap or the background underneath an item/creature.
`display_object="boulder"` likewise comes from the displayed object glyph,
including the glyph of an unrevealed boulder mimic. Real and false boulders use
exactly the same mesh, scale, rotation, placement and material policy globally.
Hallucination can replace that glyph; it must not force the hidden real rock.

Architecture consumes the existing strict-topmost presentation copy. Items,
creatures, effects and the hero hide special terrain beneath a neutral floor.
A filled pit/hole returns to the ordinary vault paving when native NetHack
removes the trap. Unknown squares remain unknown. No target markings, push paths,
solution hints, trap detection, reward-specific decoration or pile arrangement
was added. Models have no gameplay collision; the backend still decides movement.

## Built assets

Editable source: [Sokoban.blend](../Art/Sokoban/Sokoban.blend). Eight painted FBX
exports import to `/Game/Sokoban/Meshes/SM_<key>` with dedicated materials.

| Key | Treatment | Parts | Triangles |
| --- | --- | ---: | ---: |
| soko_wall | 1.20 m ashlar wall, recessed dark mortar, foundation and capstone | 19 | 3572 |
| soko_floor | One bevelled slab per native square | 1 | 188 |
| soko_boulder | Rounded weathered grey rock, grounded flat base, clear cell margins | 1 | 1280 |
| soko_pit | Square opening, earthen lining/bottom and small stones | 13 | 6556 |
| soko_hole | Square opening with dark lining and shadowed bottom | 9 | 1692 |
| soko_frame | Stone jambs/lintel with restrained bronze joints | 8 | 1504 |
| soko_trim | Fine bronze cap bands | 6 | 1128 |
| soko_lamp | Recessed bronze housing, amber pane and mullions | 4 | 752 |

Sandstone, paving, basalt, bronze, boulder, earth, dark lining and lamp have
separate roughness/metallic settings and vertex paint. Bronze is metallic;
stone is matte. Architecture memory uses 40% tint, boulder memory the established
20% object tint. The lamp's visible pane is emissive. All eight normal/memory
families and mesh vertex-colour buffers were verified after a fresh editor reload.

The well models have actual open rims and recessed inner geometry, about 20 cm
below the paving top, terminating just above the common foundation. The hole's
dark bottom gives an impression of greater depth. This is a visual recess, not
a second walkable plane or a new physical falling simulation.

Stages 2–4 gain bronze wall bands; stages 3–4 add trim at known stair/door
surrounds; stage 4 gains a second wall band. This treatment depends only on
branch stage and displayed architectural cells, never reward contents. Ordinary
stairs and doors retain their existing native presentation inside the surrounds.

## Lighting and camera

Quiet warm fill and recessed wall lamps are placed deterministically from cell
coordinates. A lamp and its floor-facing light require the relevant wall/floor
cells to be both currently visible and permanently lit according to native
state. No ambient decoration reveals an unknown cell or turns an unlit area
into a lit one. These lights do not use the ordinary candle/torch flicker.

Premapped remembered architecture remains readable through the existing separate
memory lighting channel. Sokoban's overview memory fill fades between 2.5x and
5x zoom; first-person blending removes it as before. Native vision and knowledge
are unchanged. Remembered boulders remain distinctly darker than visible ones.

Normal camera controls are unchanged. `-VerifySokoban` alone fits the actual
rendered board above the HUD at a steeper overhead angle for repeatable review.
It checks projected geometry bounds, keeping the high walls intact.

## Actual visual evidence

[Entrance-floor Unreal capture](../Art/Sokoban/Sokoban-Unreal.png) is native
`soko4-2`, presentation stage 1. [Upper-vault Unreal capture](../Art/Sokoban/Sokoban-UpperVault-Unreal.png)
is native `soko1-1`, stage 4, with known holes and additional bronze. Both use
isolated generated/saved native levels, not altered puzzle layouts. Remembered
regions are intentionally darker and hidden monsters remain hidden.

The [construction study](../Art/Sokoban/Sokoban-ConstructionStudy.png) is an
explicitly synthetic assembly of the actual meshes, not a native Sokoban map.
[Models](../Art/Sokoban/Sokoban-Models.png), [rear](../Art/Sokoban/Sokoban-Rear.png),
[front](../Art/Sokoban/Sokoban-Front.png), [underside](../Art/Sokoban/Sokoban-Underside.png)
and [true 16×16 projections](../Art/Sokoban/Sokoban-Projections.png) were opened
and inspected. Projection masks are synthetic module footprints, not a claim
of fidelity to official object tiles. Thin bronze details deliberately disappear
at small sizes; wall, rock, paving and well silhouettes carry readability.

## Verification and preservation

- `Tests/BridgeSokoban.py`: all eight native variants matched against source wall
  layouts, including native reflection; public boulder/trap fields; branch
  save/restore, leave and return. Renderer does not load these source templates.
- `Tests/BridgeSokobanGameplay.py`: real orthogonal pushes consume a boulder and
  fill both pit and hole; filled floor survives restore. Controlled traps/mimic
  are created only in fresh test roots. Native holes are tested on a floor with
  a lower Sokoban level, respecting native trap placement restrictions.
- `Tests/BridgeBoulderPresentation.py`: blind remembered boulder survives restore;
  hallucinated native tiles replace its real appearance without leaking it.
- Native unrevealed giant mimic displays the same boulder tile and object key,
  with no monster or trap metadata.
- UE editor build, targeted imports and fresh saved-asset/material checks pass.
  Both real level captures pass architecture counts, stages, memory variants,
  both F9 styles, boulder bounds/shared mimic mapping, covered/uncovered wells,
  unknown/hero hiding, off-branch removal and visible/permanent-light masking.
- Both captures pass existing object placement and 1200 strict-topmost cases,
  native live/default-tile checks and full-board camera/HUD fit. Presentation
  checks restore native cells and preserve turn/sequence.
- Geometry checks pass closed/manifold solids, finite/nondegenerate faces,
  corner vertex paint, cell/floor bounds and absence of animation/modifiers.
  All **243** preceding canonical FBX exports remain byte-identical.
- `Tests/BridgeBackendCompatibility.py` passes isolated old-save/new-runtime
  restore against verified pre-change backup `20261103T165313.370516Z.zip`.
- `Scripts/AuditSokobanSaves.py` verifies all **1081 player files**, file set and
  `LastSession.txt` unchanged. Across 1090 baseline player/runtime files, only
  the intended `Runtime/NetHackBridge.exe` changed. No player session was opened,
  advanced, force-closed or replaced. Backups remain outside `Saved`.
- Object catalogue generation/tests pass. Boulder adds one scoped MVP ordinary
  presentation, bringing that scope to 37 including four older verified drafts.
  The seven architectural modules do not count as seven object identities.

Build/check logs are `build-sokoban-*.log`; machine-readable evidence is in
`Art/Sokoban/{inspection,native-layouts,native-gameplay,boulder-presentation,
unreal-assets,live-verification,upper-verification,save-preservation}.json`.
Reproduce via `CreateSokoban.py`, `ReviewSokoban.py`, `RenderSokobanDetails.py`,
`CreateSokobanBoards.py`, `ImportSokoban.py`, `VerifySokobanAssets.py` and
`VerifySokoban.ps1` (optional `-UpperVault`). Native test roots are isolated;
the capture script never uses the normal player pointer.

Human visual testing, fine material/readability refinement and LOD/performance
review remain. Boulder is tracked as an MVP live draft, not full catalogue
completion; extended pile cases remain explicit in the object backlog.

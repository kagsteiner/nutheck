# Snickersnee

Built and live-integrated 2026-11-04 at the user's explicit request. This is the
third scoped named-artifact treatment, alongside Cleaver and Mjollnir, with
exceptional craftsmanship and the established static upright-hover presentation.

## Native facts and artistic interpretation

Pinned `upstream/NetHack/include/artilist.h` defines `ART_SNICKERSNEE` on `KATANA`,
lawful and Samurai-associated, with `SPFX_RESTR`, `PHYS(0,8)`, no defensive/carried
or invoked property and `NO_COLOR`. Its source comment attributes the name to
Ko-Ko in Gilbert's *The Mikado*. The katana base is the native iron “samurai sword.”
Gameplay properties and native gift/restriction rules are unchanged.

The polished curved blade, high ridge, painted wavy temper boundary, restrained
paired gold blade-root waves, pierced black/gold wave guard, gold habaki/seppa,
indigo diamond wrapping over pale patterned underlay, gold menuki-like ornaments
and complete matching end fittings are artistic construction choices. These
motifs are not extra lore, magical effects or hidden blessing/enchantment cues.
There is no emitted magic light, bobbing or animation.

## Editable model and review

Editable source: [Snickersnee.blend](../Art/ObjectInterpretations/Snickersnee.blend).
Painted mesh export: `Art/ObjectInterpretations/snickersnee.fbx`. It has **113
closed parts / 45496 triangles**, stands **1.294 m** in the authored frame and
uses metres, Z upright, with its origin on the lowest fitting.

The blade has actual thickness, ridge, cutting bevel, taper and shaped tip.
The pierced guard consists of a complete outer ring, central mount and four
wave bridges, with open spaces rather than a painted cutout. Both hilt faces,
blade faces, fitting rims and underside are modelled. Indigo bands are real
overlapping solids; the temper boundary and pale underlay grain use vertex paint.

Saved geometry passes finite/nondegenerate/manifold checks, valid CORNER
FLOAT_COLOR paint, applied scale, floor origin and absence of modifiers/animation.
All **269 preceding canonical FBXs** remain unchanged. Targeted Unreal import
retains paint/normals, uses no imported textures/materials or automatic collision,
and targets only `/Game/Snickersnee/Meshes/SM_snickersnee` and dedicated materials.
Used blade/gold/black-metal/indigo/underlay slots have normal and 20% memory
variants. Material metallic/roughness graph values and vertex buffers were
independently verified after a fresh editor reload. Cutting-edge colour is
painted on the blade metal family. Studio softboxes are excluded from the export.

Opened and inspected actual saved-model renders:

- [Showcase](../Art/ObjectInterpretations/Snickersnee-Review-Showcase.png),
  [model](../Art/ObjectInterpretations/Snickersnee-Review-Models.png),
  [front](../Art/ObjectInterpretations/Snickersnee-Review-Front.png),
  [rear](../Art/ObjectInterpretations/Snickersnee-Review-Rear.png),
  [underside](../Art/ObjectInterpretations/Snickersnee-Review-Underside.png),
  [guard and grip](../Art/ObjectInterpretations/Snickersnee-Review-Hilts.png).
- [Six true 16×16 projections](../Art/ObjectInterpretations/Snickersnee-Review-Projections.png).
  These judge readability rather than generic katana tile fidelity. Thin blade,
  small gold waves and wrap detail simplify at distant scale.
- [Actual Unreal scene](../Art/ObjectInterpretations/Snickersnee-Unreal.png):
  Snickersnee hovering at left, ordinary katana lying flat at right, uncovered
  altar below/right. The named sword also covers an already-seen native altar;
  that altar correctly disappears under strict topmost presentation.

Review boards use `Snickersnee-Review-*` names to avoid Windows case-insensitive
collisions with the individual `snickersnee-front/rear/underside.png` renders.

## Native knowledge and runtime selection

The existing core `map_object` observation hook is unchanged. Its window-port
whitelist now also accepts a real `KATANA` with canonical artifact name
`Snickersnee`. Existing guards still require an actual artifact, `dknown`,
`has_oname`, visible floor placement and neither blindness nor hallucination.
The core's fake mimic object clears the observation; the window port never
searches hidden piles or monsters. Full identification is not required:
native “a katana named Snickersnee” already exposes the proper name.

The UE registry now stores an explicit canonical `ArtifactName` for each named
treatment, replacing the old two-artifact ternary. Snickersnee's row precedes
the ordinary katana row and requires `Kind == item`, displayed base `katana`
and native `DisplayArtifact == Snickersnee`. Other names, absent knowledge,
unknown/monster kinds or a wrong base cannot select it. Ordinary katana geometry
and its flat pose remain the fallback. Cleaver and Mjollnir retain their names,
models, scales and existing selection rules.

Snickersnee stands at scale **0.70**, with minimum Z **26 cm**: 18 cm above the
floor's top. Bounds center the miniature inside its cell; maximum height remains
below 125 cm. Both F9 styles and remembered materials are supported. Strict
topmost suppression covers altars/fountains/sinks/traps and the hero covers the
weapon on its own square. Native terrain, pile ordering and turns are unchanged.
The verification-only capture uses legal 8× zoom and a moderate overhead angle
to show the upright sword; normal camera controls are unchanged.

## Verification and preservation

- `Tests/BridgeSnickersnee.py` passes actual native known-name-before-full-ID,
  normal restore, real identify-scroll use, dagger cover/uncover, blindness,
  hallucination, ordinary player naming and a katana mimic replacing a previously
  observed artifact on the same square. Observed text changes from “a katana
  named Snickersnee” to “the +0 Snickersnee” without changing named presentation.
- `Tests/BridgeArtifactKnowledge.py` passes the existing Mjollnir/Cleaver/name
  regression after the additive native change.
- `Tests/CreateSnickersneeCapture.py` creates actual native wishes in a spacious
  generated room, with an ordinary katana and uncovered altar control. Lighting,
  monsters and traps are controlled only in that fresh isolated fixture.
- Native and UE builds, targeted import and fresh saved-asset checks pass.
  `VerifySnickersnee` passes four style/visibility bindings, hover/floor/cell
  bounds, memory slots, ordinary/wrong-name/wrong-base/unknown guards, sixteen
  rendered covered-feature comparisons and hero coverage. Native cells/hero,
  turn **12** and sequence **2** are restored/preserved after checks.
- Full existing object placement, 1200 strict-topmost cases, no-turn F9, native
  live/default-tile/hero and 8× camera checks pass in the native capture.
- Verified backup `20261104T072145.799461Z.zip` contains 1091 player/runtime files.
  All **1082 player files**, their file set, configuration and session pointer
  remain unchanged. Only the intended `Runtime/NetHackBridge.exe` changes.
  Isolated old-runtime save → new-runtime restore compatibility passes. No played
  session was opened, advanced, force-closed or replaced; backups are preserved.
- All **470 preceding Unreal uassets** remain byte-identical. Native port source
  and its tracked patch copy are synchronized. Catalogue generation/tests pass;
  this artifact is recorded separately from ordinary types and appearance slots.

Reproduce with `CreateSnickersnee.py`, `RenderSnickersnee.py`,
`ReviewSnickersnee.py`, `CreateSnickersneeBoards.py`, `ImportSnickersnee.py`,
`VerifySnickersneeAssets.py`, `VerifySnickersnee.ps1` and
`AuditSnickersneeSaves.py`. Evidence is
`Art/ObjectInterpretations/snickersnee-{inspection,native,fixture,live,
unreal-assets,save-preservation}.json`, plus protected manifests; logs are
`build-snickersnee-*.log`. Capture/test roots never use the normal player pointer.

Human visual testing, finer temper-line/metal/cloth finish, broader memory/level
transitions and LOD/runtime cost remain review work. This is a verified static
MVP artifact treatment, not a production-performance or full-checklist claim.

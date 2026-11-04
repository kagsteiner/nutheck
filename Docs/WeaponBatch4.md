# Silver saber, broadsword and two-handed sword

Built and live-integrated 2026-11-04 as the next coherent unbuilt ordinary weapon
batch, following the complete object creation workflow. These are static MVP
drafts with editable geometry, painted exports, actual review and native integration.

## Native facts and design

| Type | Source ID | Material / skill | Source tile / native displayed tile |
| --- | --- | --- | --- |
| Silver saber | SILVER_SABER | SILVER / P_SABER | 51 / 840 |
| Broadsword | BROADSWORD | IRON / P_BROAD_SWORD | 52 / 841 |
| Two-handed sword | TWO_HANDED_SWORD | IRON / P_TWO_HANDED_SWORD | 55 / 844 |

Pinned `upstream/NetHack/include/objects.h` defines all three with `NoDes` and
known physical names. None belongs to an appearance shuffle pool. Source tile
labels/order are checked against `win/share/objects.txt`, the atlas and actual
native events. Generic weapon tiles are not design targets.

The saber's curved single-edge section, blue wrapped grip, oval guard, swept
knuckle bow, rear quillon, langets and silver heel/pins are artistic construction.
The broadsword has a wide double-edge blade with two genuine recessed fuller
channels and a middle rib, short leather grip, downturned guard and inset wheel
pommel. The two-handed sword has a long leather grip, curved long quillons, side
rings, dark unsharpened ricasso, parrying hooks, diamond-section blade and rounded
scent-stopper-style pommel. The iron family is rendered as worked steel.

These proportions, fittings and finish are invention, not additional lore or
rules. No enchantment, blessing/curse, rarity or artifact identity is encoded.
Separate named-artifact designs remain future work.

## Geometry, materials and actual review

Editable source: [WeaponBatch4.blend](../Art/ObjectInterpretations/WeaponBatch4.blend).
One painted, mesh-only FBX is exported per group, in metres with Z upright.

| Key | Parts | Triangles | Authored height |
| --- | ---: | ---: | ---: |
| silver_saber | 23 | 15764 | 1.103 m |
| broadsword | 23 | 17608 | 1.098 m |
| two_handed_sword | 31 | 21148 | 1.656 m |

Saved geometry passes finite/nondegenerate/manifold checks, valid CORNER
FLOAT_COLOR Paint, applied scale, floor origin and no remaining modifiers or
animation. Blade thickness, section, taper, bevels and fuller channels are real
geometry. Backs, undersides and fittings are complete. All **266 preceding FBXs**
and **453 preceding Unreal uassets** remain byte-identical.

Opened and inspected actual model renders:

- [Models](../Art/ObjectInterpretations/WeaponBatch4-Models.png),
  [front](../Art/ObjectInterpretations/WeaponBatch4-Front.png),
  [rear](../Art/ObjectInterpretations/WeaponBatch4-Rear.png),
  [underside](../Art/ObjectInterpretations/WeaponBatch4-Underside.png),
  [hilts](../Art/ObjectInterpretations/WeaponBatch4-Hilts.png).
- [Eighteen true 16×16 projections](../Art/ObjectInterpretations/WeaponBatch4-Projections.png).
  These judge readability, not fidelity to generic weapon tiles. Blades simplify
  at this size; fuller/ring/pin details belong to examination. Boards use
  individual framing, not a shared physical scale.
- [Actual live Unreal capture](../Art/ObjectInterpretations/WeaponBatch4-Unreal.png).
  All three are native wished objects around the hero in a generated room.
  Other native loot retains its existing models or fallbacks.

Studio reflection strips remain outside exports. Dedicated `/Game/WeaponBatch4`
meshes and materials retain authored paint/normals, metallic steel/silver/brass
and matte grips. Edge colours are painted on the relevant metal blade family.
Memory variants retain 20% object tint. Roughness/metallic graph values, every
used slot and all mesh vertex-colour buffers pass a fresh-editor reload check.
Imported textures/materials, automatic collision and animation are disabled.

## Live presentation and tests

The existing public native `fg->gm.tileidx` protocol already supplies these fixed,
known types. Registry entries select displayed tiles **840/841/844**, require
`Kind == item`, and inspect no hidden object/effect identity. Native hallucination
or an apparent item glyph controls appearance. Unsupported/missing models and
non-item kinds retain the normal fallback. No backend/whitelist/save-format
change was needed.

All three lie flat at deterministic cell yaw, with scales **0.62/0.65/0.44**.
Transformed bounds center each model and place its lowest point at 12 cm, 4 cm
above the floor top. Horizontal extents must stay below 90 cm. Both F9 styles
retain these ordinary models and their remembered materials. The hero and native
displayed pile top retain strict topmost priority; background features disappear
under a sword without changing native terrain or arranging hidden contents.

- `Tests/BridgeWeaponBatch4.py`: native wish/drop/reveal and normal save/restore
  preserve each expected tile/glyph; no artifact metadata selects an ordinary model.
- `Tests/BridgeWeaponBatch4Transitions.py`: each sword passes dagger cover/pick-up/
  uncover, blind remembered appearance through restore, and hallucination using
  native random tiles rather than the actual hidden sword.
- `Tests/CreateWeaponBatch4Capture.py`: a fresh isolated native room with three
  real wished swords. Lighting/monsters/traps are controlled only in that fixture;
  it does not establish random spawning. No player pointer is used.
- UE editor build, targeted import and independent saved-asset checks pass.
- `VerifyWeaponBatch4`: twelve style/visibility bindings, flat pose, floor/cell
  bounds, memory slots, glyph aliases and unknown/monster/unsupported guards pass.
  Forty-eight rendered comparisons cover altars, fountains, sinks and traps;
  hero hiding also passes. Native cells/hero are restored after checks.
- Existing object placement, 1200 strict-topmost cases, no-turn F9, native live,
  default-tile/hero and legal 8× camera checks pass. Presentation verification
  preserves native turn **11**, sequence **2**.
- Verified backup `20261104T070800.717411Z.zip`: all **1091 player/runtime files**,
  file set, configuration, session pointer and backend are unchanged. No played
  session was opened, advanced, force-closed or replaced. No backend replacement
  occurred, so an old-runtime compatibility experiment is not needed.
- Catalogue generation/tests pass. Ordinary MVP presentation scope is now **40**
  including four older verified drafts; six shuffled physical appearance slots
  and two artifact treatments remain separate. Creature counts are unchanged.

Build/review/import/check scripts are `CreateWeaponBatch4.py`,
`ReviewWeaponBatch4.py`, `CreateWeaponBatch4Boards.py`, `ImportWeaponBatch4.py`,
`VerifyWeaponBatch4Assets.py`, `VerifyWeaponBatch4.ps1` and `AuditWeaponBatch4Saves.py`.
Logs are `build-weapon-batch4-*.log`; evidence is
`Art/ObjectInterpretations/weapon-batch4-{inspection,restore,transitions,fixture,
live,unreal-assets,save-preservation}.json`, plus protected FBX/Unreal manifests.
The per-launch local-DDC fallback changes no player configuration.

Human visual testing, fine surface/readability work, additional native mimic
cases and LOD/runtime-cost review remain. Full checklist completion and production
performance are separate from this verified static MVP integration.

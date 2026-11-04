# MVP dungeon object placement

User direction, 2026-11-02: keep armor standing for the MVP. Ordinary weapons
lie flat; known named weapons hover upright. Static poses keep the first pass simple.

## Implementation

`DungeonObjectPlacement.cpp` maps the existing three swords, twenty armor/cloak
models, Cleaver and Mjollnir into the live dungeon alongside the four older object
presentations. Ordinary swords lie on their broad face, at 66% examination scale,
with a deterministic cell-based yaw. Armor and the dwarvish cloak remain upright.
Bounds-based placement centers each model and keeps its lowest point 4 cm above
the support plane. Mjollnir and Cleaver stand upright with 18 cm clearance, scaled
to fit a dungeon cell. There is no bobbing animation or additional light source.

Only the native top displayed glyph is rendered. Other pile contents remain hidden.
The existing tile fallback handles assets not yet built, including ordinary war
hammers and battle-axes. Physical armor and sword appearances use fixed native
source entries, not shuffled effect identities. Normal/memory materials are loaded
from each model's own folder, in both F9 styles; switching styles spends no turn.

The native `map_object` display path records known artifact presentation separately
from the base glyph. Eligibility requires an actual floor artifact, visible and not
blind or hallucinating, and description/name known (`dknown` plus `has_oname`),
matching native `objnam.c::xname` naming. Full identification or the artifact
discovery list is not required. Canonical artifact identity and matching base type
are required; ordinary player-given names do not qualify. Fake mimic
objects clear this observation; the window port never searches floor piles or
monsters for a hidden identity. UE retains an observation only for an unchanged
remembered item glyph, clears it on explicit empty data or a changed/non-item glyph,
and resets it when the map clears. Saved native gameplay data is unchanged.

## Verification

- Native and Unreal development builds pass (`build-object-placement-{native,unreal}.log`).
- `Tests/BridgeObjectPlacement.py`: 23 ordinary models and two seen, unidentified
  artifacts wished, dropped and revealed through real native window events in a
  fresh wizard session; all mappings pass.
- `Tests/BridgeArtifactKnowledge.py`: seen artifacts show their identity without an identify command;
  a normal player-named sword produces no special artifact identity.
- `Tests/BridgeObjects.py`: existing box/chest/gold mapping regression passes.
- `Scripts/VerifyObjectPlacement.ps1`: all 29 presentations, two visibility states
  and both F9 styles pass mesh/material, upright/flat axis, floor/hover clearance,
  fallback and no-turn checks. Capture-only fixtures use an isolated session.
- Old-runtime isolated save -> updated runtime compatibility passes.
- `Scripts/AuditObjectPlacementSaves.py` verifies the complete player file set,
  hashes and LastSession pointer against the pre-change backup. Only the intended
  runtime executable changes. Evidence: `object-placement-save-preservation.json`.

The reference capture is `Art/ObjectInterpretations/ObjectPlacement-Unreal.png`.
It is an isolated fixture, not a player save. Existing models remain art drafts;
finishing, broader hallucination/mimic/pile transition and native restore presentation
coverage remain follow-up review, separate from this MVP placement implementation.
The catalogue's full-completion checkboxes are deliberately not promoted by this task.

## Native naming correction

The original MVP mistakenly required `!undiscovered_artifact`. That records full
identification, not whether the proper name is visible. `objnam.c::xname` appends
ONAME whenever `has_oname && dknown`; `obj_is_pname` only controls whether the
fully identified artifact can omit its base type. Thus "war hammer named Mjollnir"
already qualifies for the artifact pose. Magical armor effects such as a cloak of
displacement follow ordinary identification rules and are a separate issue.

## Weapon batch 2 and floor support correction (2026-11-03)

Dagger, short sword and spear add three fixed ordinary presentations; see
[WeaponBatch2.md](WeaponBatch2.md) for editable models, import, native restore and
Unreal evidence. Visual review exposed that the original clearance calculation
used cell Z=0, while the 16 cm floor cube surface is Z=8. Thin flat weapons were
buried. Bounds placement now adds that support height: ordinary nonlegacy models
have minimum Z=12 (4 cm above the floor), hovering models Z=26 (18 cm above it).
The verifier checks these corrected bounds, real colour buffers and nonnull
materials for all 32 presentations in both styles and visibility states.

## Strict topmost presentation (2026-11-03)

Foreground entities suppress background feature geometry and use the neutral
floor presentation, including over altars, stairs and fountains. This applies to
known named weapons too. The original native terrain remains available to game
rules and navigation; it is not changed by the renderer. See
[TopmostPresentation.md](TopmostPresentation.md) for layer, memory and style checks.

## Weapon batch 3 (2026-11-03)

Axe, mace and ordinary war hammer add three flat, fixed-appearance models.
There are now 33 ordinary presentations plus two artifact treatments. The known
Mjollnir match precedes the ordinary hammer match; an unnamed or player-named
ordinary hammer uses the flat ordinary model. See [WeaponBatch3.md](WeaponBatch3.md).

## Tool batch 1 (2026-11-03)

Pick-axe, grappling hook and stethoscope add three fixed ordinary presentations,
all static and flat. There are now 36 ordinary presentations plus two artifact
treatments. [ToolBatch1.md](ToolBatch1.md) records source facts, geometry, import,
native restore and the expanded 1,200-case strict-topmost verification.


## Shuffled physical appearances (2026-11-03)

Ruby ring, spherical amulet and oak wand now use optional native displayed tile
keys in the same item registry. The ring stands with its crown facing +Z; the amulet and wand lie flat,
and preserve fixed examination geometry through per-presentation scale and
bounds-based floor clearance. They never select a hidden magical effect. Native
identification, restore, pile, blind memory and hallucination checks plus live
UE validation pass; see [AppearanceBatch1](AppearanceBatch1.md).

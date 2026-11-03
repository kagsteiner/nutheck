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

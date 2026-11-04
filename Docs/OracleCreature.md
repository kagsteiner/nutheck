# Oracle creature

The Oracle is now an editable, painted static miniature selected through the
normal displayed-monster path. Read `CreatureAssetContext.md` for the workflow.
This is a verified sculpted draft, with visual finishing and LOD work still open.

## Source and interpretation

- Native source: `upstream/NetHack/include/monsters.h`, `PM_ORACLE`: unique,
  peaceful female human, medium size, speed zero, passive magic-missile attack.
  No weapon, floating pedestal or permanent magic effect was inferred from this.
- Official `monsters.txt` tiles 560/561, Oracle male/female, are identical.
  Their seated figure has raised arms, crossed bare legs, peach skin, cyan/blue
  cloth, a white head surround, small green crown marks and a central black mouth.
  The native creature is female; the male display alias shares this sculpt only
  because the official artwork is identical. It is not another creature identity.
- Artistic choices: the white surround becomes long white hair; green marks
  become a restrained laurel wreath. Fitted blue-grey eyes, a chanting mouth,
  continuous folded chiton, complete hands and crossed legs finish the miniature.
  These details interpret sparse artwork rather than claiming source anatomy.
- An explicit spatial mask retains the two central black mouth pixels and
  excludes the offset right/lower cast shadow. Source tiles remain unchanged.
  The six genuine 16×16 projections are diagnostic: best silhouette IoU 0.5766.
  Full anatomy and cloth take priority over reproducing a cast shadow or every
  jagged source pixel.

## Assets and evidence

`Art/CreatureInterpretations/OracleCreature.blend` contains the saved geometry;
`oracle.fbx` is its painted export. `Scripts/CreateOracleCreature.py` builds only
this creature; it reuses the existing human fitted-eye and hair-cap helpers
without modifying previous human/player assets. The figure has 62 mesh parts,
275,852 triangles and approximately 0.93 × 0.45 × 1.12 m seated bounds. Geometry
is static, unrigged and unanimated. Eye paint patches intentionally have open
surface boundaries; other parts are closed and the anatomical body is connected.

Actual views (not concept images):

- [Model review](../Art/CreatureInterpretations/Oracle-Review.png): front, rear,
  three-quarter, face, profile and underside.
- [Source and six tiny renders](../Art/CreatureInterpretations/Oracle-Projections.png).
- [Hand detail](../Art/CreatureInterpretations/oracle-hand.png).
- [Live native Oracle room](../Art/CreatureInterpretations/Oracle-Unreal.png).

`Scripts/ReviewOracleCreature.py` inspects the saved blend without regeneration:
finite nondegenerate geometry, connected body, closed solids except fitted eye
patches, floor origin, paint, eight fingers/two thumbs/ten toes/two eyes, no
pending modifiers or animation. `oracle-mesh-inspection.json` records PASS;
all 233 preceding canonical FBX hashes match `oracle-protected.json`.

`Scripts/ImportOracleCreature.py` imports only
`/Game/CreatureInterpretations/Meshes/SM_oracle`, reusing existing M_Paint/M_Eye
without rewriting shared materials. `VerifyOracleCreatureAssets.py` reloads the
saved asset and verifies slot assignments and colour data.

## Live integration and preservation

`DungeonLive.cpp` admits the canonical displayed `Oracle` identity in sculpted
mode, with the same 15-degree front orientation as other human miniatures.
No monster location, hidden identity or Oracle-room anchor forces this model.
The established fallback, F7 glyph labels and F9 presentation switch remain.
`DungeonOracleCreature.cpp` verifies both display-sex aliases, default-mode
fallback, visible/remembered tile-card data, unsupported/empty identities, actual
native female Oracle presence, paint buffers and F9 both ways without turns.

`Scripts/VerifyOracleCreature.ps1` uses the explicit disposable capture root in
`build-oracle-fixture.json`, never the player pointer. Results: creature PASS
(native=1, aliases=2, fallback=2, turn=6, sequence=2); sanctuary PASS; live map,
default tiles and 4× zoom PASS. The screenshot retains normal high walls and
glyph badges. The sanctuary's saved native room identity is unchanged and still
independent of whether the Oracle lives.

Verified backup: `Backups/NetHackSaves/20261103T100726.125114Z.zip`.
`Scripts/AuditOracleCreatureSaves.py` confirms all 1,090 archived played/runtime
files, the file set and LastSession pointer remain byte-identical. No backend
replacement or player-session resume was used.

Remaining visual work: human review of the miniature's face, hair locks, cloth
and limb transitions; dedicated LOD/performance work for this dense draft.
No production-performance claim is made. Centaur statues are now implemented through the shared renderer; see `CentaursAndStatues.md`.

# Human female Valkyrie and male Barbarian

The user's requested two adult human player forms extend the painted-miniature
style with fitted eyes and fixed icon-derived appearances. **User correction:
no detachable clothing; each saved character is one mesh.** They are
static unrigged drafts. The prior 36 creature FBX files are hash-protected and
unchanged; the suggested kobold batch has not been started.

## Source and art interpretation

The official tiles are `valkyrie,female` (699) and `barbarian,male` (678).
`role.c:493` permits female Valkyrie starts with human/dwarf ancestry;
`role.c:72` permits male/female human/orc Barbarians. These requested meshes are
specifically **human female Valkyrie** and **human male Barbarian**. They are not
substitutes for other ancestries or sexes.

The Valkyrie tile shows long blond hair, blue eyes and brown/orange clothing;
the interpretation is an athletic adult with a blond braid, fixed brown torso/hip/legwear and simple foot detailing. The Barbarian tile has blond hair, green eyes, bare chest/limbs
and a brown waist garment; the interpretation is a broader adult with a short brown waist garment and bare feet. The large black shapes offset to the right
of both tiles are cast shadows, not giant shields, cloaks or anatomy. Projection
masks retain enclosed dark pixels and exclude background-connected black fringe.
Original source tiles remain untouched on the comparison board.

No horned/winged helmet or held weapon was inferred. Starting inventory is a
separate fact: this pinned source gives Valkyrie spear/dagger/small shield and
Barbarian alternative weapon sets plus ring mail. The fixed tile-derived costume
does not assert current equipment. These are fixed characters matching the icons. Their clothing is part of the
character mesh, without independent clothing objects or a wardrobe system.

## Anatomy and review

`Scripts/HumanPlayerFamily.py` builds continuous torso, neck, skull/jaw, nose,
shoulders, arms, hips, legs, ankles and feet. Finger/thumb geometry is baked into the same character mesh. The male/female forms have independently chosen shoulder,
waist, limb and jaw parameters rather than uniform scaling. These are two
specific artistic bodies, not a claim that all people of either sex share those
proportions. Art height is about 1.66m/1.71m, not a conversion of NetHack size.

Eyes and brows are projected onto the actual face surface. Small almond sclera,
blue/green irises, pupils, lids and glints replace protruding eye globes. Hair
uses a closed/thickened cap, painted flow and a coarse braided long-hair mass;
no individual strand system or fur shader is added to human skin.

Studio review corrected insufficient ankle overlaps, boot/calf clipping, belt
fit, exaggerated cheek/brow/pectoral masses and brow placement. The anatomical surface remains connected in each form; facial, hair and costume
surfaces are joined into that same fixed mesh. Current checks verify the single
mesh, fitted eyes and Valkyrie legwear through ankle/calf/knee/thigh levels. All changes are present in fresh
generation; no one-time repair offsets need repeating.

Artifacts under `Art/CreatureInterpretations/`:

- `HumanPlayers.blend`, `valkyrie_female_human.fbx`, `barbarian_male_human.fbx`.
- `HumanPlayers-Models.png`: actual studio model renders together.
- `HumanPlayers-Comparison.png`: official selected-sex tiles, front/rear meshes
  and actual 16x16 reverse projections, six camera candidates per form.
- `HumanPlayers-FaceReview.png`: saved front/profile head views.
- `projection-report-human-players.json`, `human-players-inspection.json` and
  `human-players-protected-assets.json` record geometry, masks and prior hashes.
- `valkyrie_female_human-Unreal.png` / `barbarian_male_human-Unreal.png` are actual
  native player captures, not NPC substitutes or synthetic hero identities.

Generate with Blender background mode, four threads, and `CreateHumanPlayers.py`.
Use `InspectHumanPlayers.py` and `ReviewHumanPlayers.py` to inspect saved geometry;
the source comparison script assembles actual pixels/renders. After painting, `fixed_characters()` consolidates all surfaces into one mesh
per character. Separate clothing objects and detachable-clothing tags are absent.
First-person hiding continues to hide the entire character.

## Runtime selection and native metadata

The bridge now emits the player's own known `hero_race` and
`hero_polymorphed` status. It reads `gu.urace.noun` and `Upolyd`; no hidden
monster/race lookup is added. Displayed role and sex still come exclusively from
the shown glyph. Unknown ancestry, non-human ancestry, polymorphed state,
unsupported sex and NPC role appearances retain existing fallbacks.

The human assets use `/Game/CreatureInterpretations/Meshes/SM_<form>` and are
selected only for the hero, human ancestry, matching shown role/sex and no
polymorph, while sculpted style is on. F9 restores the original presentation
without a turn. Human meshes face -Y and use 15-degree display yaw. The existing
first-person camera/eye-height experiment is retained; the entire `PlayerVolume`
batch hides in first person and restores on exit. F7 remains available.

`-HumanPlayerPreview=<form>` writes an explicit native `.nethackrc` only into a
fresh throwaway preview session. Tests select actual human female Valkyrie and
human male Barbarian starts, rather than replacing a random player's identity.
Ordinary character selection remains native NetHack behavior.

## Verification and inventory

- `build-human-players-blender.log`: native geometry, two painted FBX exports,
  four studio views and twelve true 16x16 projections completed.
- `build-human-players-inspect.log`: paint, connected bodies/ankles, floor,
  fitted paired eyes, fixed integrated appearance and legwear coverage and all
  prior 36 exports passed. Native triangles: 155,408 Valkyrie / 183,888 Barbarian.
- `build-human-players-review.log`: four actual head views completed/inspected.
- `build-human-players-bridge.log` and `build-human-players-unreal.log`: builds
  passed. The first bridge compile used the old global spelling; the current
  `gu.urace` spelling fixes it.
- `build-human-players-native-profiles.log`: four real profiles passed (both
  requested humans, dwarf Valkyrie and orc Barbarian); displayed role/sex and
  own-race metadata agree. Existing nondisclosure checks remain intact.
- `build-human-players-bridge-smoke.log`: real movement and perception smoke
  check passed against the updated bridge.
- `build-human-players-import.log`: both final player meshes imported, validated
  painted colour buffers, count 2 and successful editor exit.
- `build-human-player-valkyrie_female_human-live.log` and
  `build-human-player-barbarian_male_human-live.log`: each actual native profile
  passed 11 selection/fallback cases, colour buffers, real F9 switches, unknown
  ancestry/unsupported sex/ancestry/polymorph/NPC guards and first-person whole-
  player hiding/restoration. Turn stayed 5 and sequence stayed 5 in both runs.
  Native map/movement, hero centring, 8x zoom and loaded player checks passed.
  Both actual engine captures were visually inspected; foreground walls obscure
  portions of the Valkyrie's lower legs, while studio views show the full model.

Physical asset inventory distinguishes the two requested forms from role
completion: Valkyrie's single permitted starting-sex target is represented by
the human female draft; Barbarian remains partial because the female target was
not requested/generated. Ancestry variants are explicitly unscoped, and the
existing non-human proxies remain fallbacks. No female Barbarian is claimed.

Rigging, facial expression, further anatomy/cloth/hair refinement, gait/combat
animation, LOD/performance work remain separate. These characters retain their fixed icon appearance.


Inventory reconciliation: 36 creature drafts plus two human player forms = 38
physical static forms. For the 394-ID checklist, 36 creature IDs + 1 completed
player role + 345 remaining creatures + 12 remaining player roles = 394.
Barbarian's male form is complete for this request, while its role checkbox stays
partial; Valkyrie's single permitted starting-sex target is checked. Catalogue
sex nodes record human scope and retain the ungenerated female Barbarian proxy.


The later user correction supersedes the earlier modular-clothing approach.
The skirt-like Valkyrie lower garment is replaced by fitted brown legwear; the
Barbarian has a short waist garment, with the long flap and decorative buckle
removed. Each editable collection contains one character mesh, and each FBX
exports that same fixed appearance. Generation, renders, inspection, final
imports and both live/camera checks were rerun for this revision. Inventory and
ancestry/sex selection behavior are unchanged.

# Male and female human Samurai

User request: two human Samurai characters, with a noticeably female variant
that is recognisably related to the male despite identical official tiles.
This explicit direction overrides treating identical tiles as a reason to
share one sculpt. No changes to previous creature sex forms are implied.

## Source and artistic decisions

Official tiles samurai,male / samurai,female are 694/695 and identical. Both show
black hair/topknot, green eyes, peach skin, magenta shoulders/feet, red lower
clothing and a cyan waist mass. The offset right-side black mass is cast shadow,
not a held shield or cloak. Spatial masks retain topknot/head dark pixels and
small interior marks; original source tiles remain alongside actual renders.

Pinned src/role.c permits male/female human Samurai, lawful alignment only.
Native character creation and role mechanics remain unchanged. Costume follows
the icons and is fixed to the character; it does not assert worn/carried gear.
No permanent sword or shield was inferred from starting inventory.

Both wear the same magenta wrap shirt/shoulder panels, red trousers, magenta
lower-leg treatment/tabi-like shoes and wide cyan obi. Black hair and green
fitted eyes establish shared family identity. Male has a broader athletic body,
stronger jaw and short topknot. Female has independently proportioned narrower
shoulders/waist, fuller hip-to-waist silhouette, softer jaw, fitted covered
chest and longer tied ponytail. These dimensions, hairstyle extension, garment
construction and unseen surfaces are artistic choices requested for distinction,
not claims that the two source tiles depict this anatomy or that every person
of a sex shares one body type. No detachable clothing or runtime wardrobe.

HumanPlayerFamily supplies compatible anatomy/face helpers; smooth transported
limb frames keep knees/elbows continuous. CreateSamurai.py replaces earlier
role-specific costume, fits shoulder/sleeve/leg volumes, paints the shin colour
on continuous trousers and consolidates every surface into one mesh per form.
Initial sleeve/legwear intersections and female shoulder clipping were fixed
after actual render review; fresh generation contains final fit. Old Valkyrie,
Barbarian and other approved exports are not regenerated.

## Artifacts

Under Art/CreatureInterpretations: Samurai.blend; samurai_male_human.fbx and
samurai_female_human.fbx; Samurai-SourceReview.png, Samurai-Models.png,
Samurai-Comparison.png, Samurai-FaceReview.png; twelve true 16x16 projection
candidates and projection-report-samurai.json. Actual front-quarter/rear and
saved front/profile face renders accompany each form.

Scripts: CreateSamurai.py, InspectSamurai.py, ReviewSamurai.py,
CreateSamuraiComparison.py, ImportSamurai.py, VerifySamuraiAssets.py,
VerifySamurai.ps1 and AuditSamuraiSaves.py. Native profiles: Tests/BridgeSamurai.py.
Reports: samurai-inspection.json, samurai-unreal-assets.json,
samurai-protected.json and samurai-save-preservation.json. Actual native-player
captures are samurai_male_human-Unreal.png and samurai_female_human-Unreal.png.

Saved inspection verifies a single fixed mesh per form, corner paint, connected
anatomical core, floor origin, paired fitted eyes/symmetry and prior export hashes.
Native triangles: 195,584 male / 174,156 female. Dense static drafts; cloth/skin/
hair and face finishing, source-palette balance and LOD/runtime costs remain.
No rig or animation is required/planned under the current game vision.

## Runtime and save boundary

Select only for the hero, known human ancestry, displayed samurai role and sex,
not polymorphed, with sculpted style on. Other ancestry, unknown race, polymorph
and NPC role displays retain previous fallbacks. No hidden monster lookup.
Both forms use the established -Y human front and 15-degree display orientation.
First-person hides/restores the entire fixed character. Shared statue renderer
can reuse the exact matching player mesh as white marble without a new sculpt.

-HumanPlayerPreview writes Samurai profile choices only to fresh isolated test
roots. Normal launches retain native character selection/resume behavior.
Verified backup: 20261104T080421.467671Z.zip (1,091 files). All 270 preceding
FBXs are protected. No native backend rebuild or played-session resume/test.


## Verification and inventory

Final editor build and two targeted imports pass colour/material validation.
Both real human Samurai profiles pass native role/sex/race checks. Each live
profile verifies 23 selection/fallback cases (including existing player forms),
F9 without native turn/sequence advance, entire-character first-person hiding
and restoration, native movement/map, hero centring and 8x zoom. Actual captures
were inspected; high foreground walls obscure lower legs. Studio views show
complete geometry. No wall height or visibility rule was relaxed.

All 270 preceding exports and all 1,091 played-session/runtime files, complete
file set, configuration and LastSession pointer remain unchanged. Only isolated
preview roots were used, without a native backend rebuild. Samurai completes
both permitted human starting-sex targets: backlog/catalogue now have 100
creature drafts plus 2 completed player roles, 281 remaining creatures and 11
remaining roles (394 unique IDs). Physical forms total 108; four human player
forms include the still-partial male-only Barbarian. Creature queue is unchanged.

Rear-calf trouser intersections were corrected from the saved scene via
RefineSamuraiTrouserFit.py; fresh generation includes the same depth allowance.
Use RenderSamurai.py / ReviewSamurai.py for saved inspection, without repeating
the one-time correction. These remain static drafts requiring visual finishing.

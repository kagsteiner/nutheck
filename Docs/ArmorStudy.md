# Requested torso armor study

Update, 2026-11-02: these models are now connected to the live dungeon under the
[MVP placement rules](MVPObjectPlacement.md), with isolated native mapping and
Unreal placement checks passed. Earlier pending-live statements below describe
the original art-only milestone. Finishing and broader edge-case review remain
separate from MVP placement; full-completion checkboxes are unchanged.

Six native armor types: leather armor, studded leather armor, chain mail,
banded mail, elven mithril-coat and dwarvish mithril-coat. The user clarified the
seventh request as **dwarvish cloak** (`DWARVISH_CLOAK`), the native cloth
"hooded cloak" at `objects.h:620`. Its separate `DwarvishCloak.blend` has an
open-front drape, hollow hood, woven edging and bronze clasp. Brown wool,
edging and exact tailoring are artistic interpretation, not hidden properties.

Source: `upstream/NetHack/include/objects.h:568–597`. The leather types use
LEATHER; chain/banded mail use IRON; both mithril coats use MITHRIL. These six
have no shuffled descriptive appearance. Exact tailoring, lining, decorative
fittings and cultural motifs are artistic interpretation. Generic armor tiles
are intentionally ignored for design, as directed in `ObjectArtDirection.md`.

Each garment is a hollow torso shell with neck, hem and arm openings, thickness,
rear and interior surfaces. Plain leather has simple dark binding and steel
fasteners; studded leather has individual metal studs. Chain mail uses actual
closed ring geometry. Banded mail uses overlapping formed horizontal steel
strips, not a painted stripe pattern. Both mithril coats use finer bright rings;
the elven coat has green lining and flowing leaf ornament, while the dwarvish
coat is wider with blue lining and geometric chest fittings. These are static
display garments, not equipped-player clothing replacements or tailored rigs.
Ring layout is a simplified miniature treatment, not a historically exact
four-in-one weave. Shoulder/armhole tailoring and cultural detailing remain
draft finishing work, as do LODs and material refinement.

Artifacts under `Art/ObjectInterpretations/`: `ArmorStudy.blend`, six named
FBX exports, front-quarter/rear/front/underside renders, actual six-camera
16x16 projections per item, and `projection-report-armor-study.json`.
`armor-study-protected.json` preserves all 96 prior canonical FBX hashes.
`armor-study-inspection.json` checks finite/nonzero/manifold geometry and paint.

Scripts: `CreateArmorStudy.py`, `InspectArmorStudy.py`, `ReviewArmorStudy.py`
and `ImportArmorStudy.py`, plus `CreateDwarvishCloak.py`,
`InspectDwarvishCloak.py` and `ReviewDwarvishCloak.py`. Unreal assets are
isolated under `/Game/ArmorStudy`.
Normal and remembered materials retain metal/paint separation and vertex colour.

**Design/import drafts; live mapping remains pending.** These models do not
change the native display whitelist. Before checking off live object completion,
test native displayed appearances, piles, memory, hallucination, save/restore,
fallback and no-turn presentation. No backend changes, gameplay launches or
save changes are part of this study. Four existing live object drafts and
78/381 creature coverage remain unchanged. No creature/player assets are replaced.

## Completed design checks

Saved geometry/paint/manifold checks pass for all seven. All 96 preceding
canonical exports are unchanged. Triangle counts: leather 17,208; studded
leather 148,536; chain 145,656; banded 24,104; elven mithril 241,888; dwarvish
mithril 240,784; cloak 22,236. These are dense editable drafts, not LOD budgets.
All seven Unreal imports pass vertex-colour validation, including normal and
memory material creation (`ARMOR_STUDY_IMPORT_READY count=7` in
`build-armor-study-import.log`). Source-catalogue tests pass in
`build-armor-study-catalogue-tests.log`; design status remains distinct from
verified live-object status.

Actual front/rear/interior views and all 42 tiny renders were inspected.
Boards: `ArmorStudy-Models.png`, `ArmorStudy-Rear.png`, `ArmorStudy-Details.png`
and `ArmorStudy-Projections.png`, assembled by `CreateArmorStudyBoards.py`.
The latter are readability diagnostics; leather studs and small mail details
largely disappear at 16x16, so close view and dungeon-distance finishing differ.

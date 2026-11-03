# Standard weapon study: long sword, scimitar and katana

Update, 2026-11-02: these models are now connected to the live dungeon under the
[MVP placement rules](MVPObjectPlacement.md), with isolated native mapping and
Unreal placement checks passed. Earlier pending-live statements below describe
the original art-only milestone. Finishing and broader edge-case review remain
separate from MVP placement; full-completion checkboxes are unchanged.

Three ordinary weapons follow the suggested craftsmanship study. Generic tiles
are intentionally ignored for design, as directed in `ObjectArtDirection.md`.
These designs share polished metal language but have independent silhouettes,
cross sections, cutting edges, guards, grips and pommels.

## Native identity and construction references

Pinned `include/objects.h` defines all three as IRON. `LONG_SWORD` has no extra
description; `SCIMITAR` is a "curved sword" and `KATANA` a "samurai sword".
None belongs to an appearance shuffle pool. No hidden artifact, blessing,
enchantment or rarity marker is added. Native handling/damage remains unchanged.

Museum construction references inform, rather than dictate, the designs:

- [Wallace Collection longsword](https://wallacelive.wallacecollection.org/eMP/eMuseumPlus?module=collection&objectId=60977&service=ExternalInterface): double-edged blade with a hollow groove and leather-bound grip.
- [Fitzwilliam Museum shamshir](https://data.fitzmuseum.cam.ac.uk/id/object/160100): curved single-edged blade with a flat back.
- [British Museum katana mountings](https://www.britishmuseum.org/collection/object/A_1998-1217-2): wood, ray-skin and braided-textile hilt construction.
- [Worcester Art Museum katana parts](https://worcester.emuseum.com/objects/59435/parts-for-a-katana-sword): slightly curved single-edged blade and separate mountings.

The NetHack long sword is not presented as an exact historical two-handed
longsword reproduction. "Scimitar" is a broad category; its chosen curve and
hooked hilt are an artistic interpretation, not a claim that all regional swords
share that shape. Materials, proportions, simple fittings and finish remain
game-art choices rather than museum replicas. No religious inscription is copied.

## Designs

Long sword: straight tapered double-edged blade, genuinely recessed fuller in
both faces, leather grip, curved steel crossguard and wheel pommel with small
brass inserts. Scimitar: stronger sweep, thicker flat spine and a single broad
cutting bevel, curved wood grip, hooked pommel, brass quillons and langets.
Katana: restrained curve, asymmetric spine/ridge/cutting section, oval tsuba,
seppa and habaki, longer pale underlay grip with crossed dark textile wrapping,
small menuki-like fittings and matching end caps. The underlay evokes mountings
without introducing a high-resolution external rayskin texture.

Blade geometry consists of 33 sampled closed cross sections, with real thickness,
taper and narrow capped tips. Edge/fullered-land colour varies on the actual
geometry. Complete backs and undersides exist. Neutral reflection strips in the
saved studio reveal the metal surface; these lights are not exported in FBX.
All are static examination/loot assets, not new equipped-player rigs or swing
animations. Fine temper-line treatment, textile wrapping, fuller finish, wear
and LODs remain reviewable finishing work.

## Artifacts and status

Under `Art/ObjectInterpretations/`: `WeaponBatch1.blend`, `long_sword.fbx`,
`scimitar.fbx`, `katana.fbx`; individual studio/front/rear/underside/hilt renders;
eighteen actual 16x16 projections and `projection-report-weapon-batch1.json`.
Boards use `WeaponBatch1-{Models,Rear,Front,Hilts,Underside,Projections}.png`.
`weapon-batch1-inspection.json` records topology/paint checks;
`weapon-batch1-protected.json` preserves the 120 previous canonical FBX files.

Scripts: `CreateWeaponBatch1.py`, `ReviewWeaponBatch1.py`,
`CreateWeaponBatch1Boards.py`, `ImportWeaponBatch1.py`.
Unreal folder: `/Game/WeaponBatch1`, separate from artifact and armor materials.
Normal/memory versions separate paint and metal while retaining vertex colour.
Evidence: `build-weapon-batch1-*.log`.

**Design/import drafts; native displayed-appearance and live verification remain
pending**, consistent with the preceding object studies. Native pile, memory,
hallucination, save/restore, fallback and no-turn switching must pass before live
checklist completion. No gameplay is launched; no backend/player-save changes.
The four existing live object drafts and 81/381 creature coverage stay unchanged.

Completed design checks: closed finite/nonzero geometry, valid corner paint and
all 120 prior canonical FBX exports unchanged. Long sword: 22 parts / 20,044
triangles; scimitar: 12 / 7,708; katana: 56 / 15,692. Front/rear/hilt/underside
views and eighteen actual tiny projections were inspected. Three targeted
Unreal imports pass material assignment and vertex-colour validation
(`WEAPON_BATCH1_IMPORT_READY count=3`). Source-catalogue tests pass in
`build-weapon-batch1-catalogue-tests.log`. Native live eligibility remains pending.

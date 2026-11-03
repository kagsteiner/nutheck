# Dragon mail: smaller-scale reference revision

User correction: remove the large slab-like scales. The two supplied armor
references guide smaller rounded leaf scales, more fitted tailoring and curved
overlapping shoulder layers. References are preserved under
`Art/ObjectInterpretations/References/DragonMail-user-reference-{1,2}.jpg`.
They are direction references, not generated meshes or exact reconstructions.

All ten colours are revised. The former large breast scutes, pectoral badge,
upright collar scales, flat shoulder slabs and tall horns are removed. Rounded
leaf scales with a low dome replace the faceted pyramid treatment. The torso
has a narrower waist, rounded arm openings, a thin V-shaped gorget and fitted
belt. Six curved shoulder lames carry finer scales and restrained outer spurs.
Gray has a small silver-edged leaf spine rather than an oversized chest badge.
The study remains torso armor; the reference helmets and gauntlets are not
additional assets created by this task.

The previous scene, ten exports and original views are archived in
`Art/ObjectInterpretations/DragonMail-v1/`. The current editable source remains
`ArmorBatch2.blend`; the ten canonical dragon FBX exports and Unreal meshes are
updated in place. All 107 unrelated canonical exports, including the three
plate armors, are preserved. Their saved native geometry and paint are also
compared directly against the archived scene.

`DragonMailFamily.py` is now the shared construction used by
`CreateArmorBatch2.py`. `ReworkDragonMail.py` revises the saved scene without
regenerating plates. `RenderDragonMailRevision.py` refreshes saved renders and
exports; `InspectDragonMailRevision.py` audits topology, paint, scale counts,
absence of the rejected slabs and exact plate preservation.
`ReviewDragonMailRevision.py` produces front/interior views, and
`ImportDragonMailRevision.py` targets only the ten dragon meshes. The import
skips the plate/crystal materials. No live mapping, native backend or saves are
changed; design status remains separate from pending gameplay verification.

Current previews use the existing `ArmorBatch2-Dragons-*` boards and individual
`*_dragon_scale_mail-{three-quarter,rear,front,underside}.png` views. The shared
projection report retains the unchanged plate entries and revised dragon entries.
`dragon-mail-revision-inspection.json` and `build-dragon-mail-revision-*.log`
record verification. `CreateArmorBatch2Boards.py` assembles the actual renders.

Small scale overlap, shoulder integration, surface wear and LODs remain visual
finishing work. Color identities and native resistances remain unchanged.

Final checks pass for all ten variants: closed finite/nonzero surfaces, valid
corner paint, 1,006 torso scales plus 600 shoulder scales per coat (gray adds
14 fine spine/rim leaves), six curved shoulder lames and no rejected large-slab
objects. Gray has 364,884 triangles; the others 362,224 each. These are dense
editable art drafts with LOD reduction still pending.

The final saved scene passes exact plate-geometry/paint comparison with the
archive and all 107 unrelated canonical export hashes match. Final targeted
Unreal import validates ten meshes and paint/material assignments, with
`ARMOR_BATCH2_IMPORT_READY count=10 crystal_clearcoat=untouched`. Actual front,
rear, interior and sixty tiny renders were inspected. The initial partial-scene
preview exposed the preserved plate mesh; the shared render helper now hides
unselected meshes, and the final saved rerenders show only each selected dragon
armor. Gameplay/live eligibility remains pending as before; no saves changed.

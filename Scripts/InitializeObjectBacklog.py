"""Create the manual object checklist once; refuse to overwrite existing progress."""
import json
from collections import defaultdict
from pathlib import Path
root=Path(__file__).resolve().parents[1];target=root/'object-backlog.md'
if target.exists():raise FileExistsError('Manual checklist exists; update it in place, never regenerate over progress.')
data=json.loads((root/'Art/ObjectCatalogue/objects.json').read_text(encoding='utf-8'))
art=json.loads((root/'Art/ObjectCatalogue/artifacts.json').read_text(encoding='utf-8'))['artifacts']
rows=data['objects'];summary=data['summary']
md=['# Object asset backlog','',
    'Working checklist, created 2026-11-02. Maintained by hand: catalogue regeneration must never replace checkboxes, priorities, review notes or evidence.',
    '', '**440 named source object types: 439 unconditional + 1 conditional mail type. Four verified fixed-object drafts; 436 types remain.**',
    'There are also 463 non-auxiliary default appearance slots (including 23 extra shuffled descriptions), 18 display auxiliaries, 4 deferred types and 33 current artifact overlays. These scopes are not additive unique-mesh counts.',
    '', 'Read [Object art direction](Docs/ObjectArtDirection.md) before modelling. User direction: make loot beautiful, distinctive and rewarding; allow more creative craftsmanship while preserving visible type/material cues and NetHack information boundaries.',
    '', '## How to use this checklist','',
    '- Navigate by native category → useful visual family. Treat materials, cultural cues, construction and finish as facets. Reuse generators without making every sword, ring or bottle interchangeable.',
    '- Query [objects.json](Art/ObjectCatalogue/objects.json) by stable enum ID. Browse [Inventory.md](Art/ObjectCatalogue/Inventory.md) or filter [objects.csv](Art/ObjectCatalogue/objects.csv). Source inventory includes conditional/deferred records; review scope before modelling.',
    '- Use [appearances.json](Art/ObjectCatalogue/appearances.json) / [appearances.csv](Art/ObjectCatalogue/appearances.csv) for physical appearance slots and shuffle groups. Default source effect/description pairings are not live bindings.',
    '- For shuffled types, a checkbox needs coverage by the legal 3D appearance family and verified native mapping. A mesh for one named effect does not complete it. Indistinguishable native appearances must stay indistinguishable. The source appearance slots are not a requirement for one mesh each.',
    '- Check only after editable geometry, painted export, actual front/rear/tiny comparisons, UE import/material, displayed mapping/fallback/memory and no-turn checks exist. Official tile fallback alone is not a completed 3D draft. Add evidence beside the existing item.',
    '- Leave incomplete items unchecked with artifact paths and the exact remaining step. Keep refinement/LOD costs separate; static objects are the target and animation is out of scope.',
    '- Preserve all existing four completed presentations. Generic corpse does not finish species-specific corpse/statue representations. Artifact overlays are not ordinary base types and do not require unique geometry when lawful reuse suffices.',
    '- Regenerate metadata with `Scripts/CreateObjectCatalogue.py`; it never writes this checklist, models, runtime files or saves. Update the selected-object registry only after verification, then reconcile counts and checklist notes.',
    '', '## Suggested object work','',
    '1. Long sword, scimitar and katana: one reviewed craftsmanship/finish study with clearly different blade, guard, grip and proportion. Compare ordinary and ornate interpretations while preserving recognition.',
    '2. A ring, amulet and wand appearance study: coherent jewelry/metal/wood language; choose physical source appearances, not effect-coded ornament.',
    '3. Potion/scroll appearance pipeline: bottles, liquids and labels; verify native shuffling and persistence before completing effect identities.',
    '4. Artifact designs linked to base types, with an explicit native-knowledge eligibility rule before unique live visuals.',
    '', 'These are future priorities, not an instruction to generate assets automatically.',
    '', '## Named object types','', '| Category | Source types | Verified drafts |','| --- | ---: | ---: |']
named=[r for r in rows if r['record_kind']=='object_type' and r['scope']!='deferred']
grouped=defaultdict(lambda:defaultdict(list))
for r in named:grouped[r['category']][r['visual_family']].append(r)
for category,count in summary['by_category'].items():md.append(f"| {category} | {count} | {sum(r['asset_status']=='generated and verified static draft' for r in named if r['category']==category)} |")
for category,families in grouped.items():
    md+=['',f'### {category}','']
    for family,items in families.items():
        md+=[f'#### {family}','']
        for r in items:
            done=r['asset_status']=='generated and verified static draft';name=r['name'];desc=r['default_description']
            note=(' — default appearance: '+desc) if desc and desc!=name else ''
            if r['shuffle_group']:note+='; shuffled pool `'+r['shuffle_group']+'`'
            if r['scope']=='conditional':note+='; **conditional '+', '.join(r['source']['conditions'])+'**'
            if done:note+='; verified fixed presentation; [evidence]('+r['evidence']+')'
            md.append(f"- [{'x' if done else ' '}] **{name}** (`{r['id']}`){note}.")
        md.append('')
md+=['## Extra appearance-only slots','', 'These are physical appearance work, not 23 additional object-effect identities. Their source default-slot IDs are not live effect identifiers.','']
for r in rows:
    if r['record_kind']=='appearance_only' and r['scope']!='deferred':md.append(f"- [ ] **{r['default_description']}** (`APPEARANCE_{r['id']}`) — {r['category']}; source slot `{r['id']}`.")
md+=['','## Artifact overlays','', '33 current artifacts linked to their base types. No artifact-specific geometry has been verified. A distinctive treatment is gated by native displayed knowledge, and must not expose an unidentified artifact.','']
for a in art:
    if a['scope']=='normal':md.append(f"- [ ] **{a['name']}** (`{a['id']}`) — base `{a['base_object_id']}`; design and visibility-rule review pending.")
md+=['','## Conditional, deferred and auxiliary scope','',
     '- Conditional `SCR_MAIL` is included once above; it is not a guaranteed player-build item. The base unconditional list contains 439 types.',
     '- Four `#if 0` declarations are excluded from the 440 named-type target: '+', '.join('`'+r['id']+'`' for r in rows if r['scope']=='deferred')+'. Shimmering dragon armor retains official source tiles; that does not make it active gameplay content.',
     '- Eighteen display auxiliaries (strange object plus 17 generic classes) are retained in JSON/CSV. They are not ordinary loot identities and need separate fallback/glyph scope review.',
     '- Obsolete artifact `ART_PALANTIR_OF_WESTERNESSE` is recorded separately; it is not one of the 33 current designs.',
     '', '## Finishing and rendering work','',
     '- [ ] Establish a reviewed beautiful-object finish target at dungeon, room and close inspection scales.',
     '- [ ] Build shared construction families while preserving meaningful silhouette/proportion/ornament differences.',
     '- [ ] Design the native appearance/knowledge protocol before extending beyond the current fixed-object whitelist; cover shuffling, same-look objects, piles, memory, hallucination, save/restore and identification.',
     '- [ ] Refine existing wood/metal/coin/corpse drafts and review LOD/runtime costs.',
     '- [ ] Scope carried/equipped visuals against displayed information before showing NPC/player equipment dynamically.',
     '- [ ] Scope corpse/statue species variants, food states, containers and quantity representations separately; do not infer hidden contents, traps or exact stack size from decorative geometry.',
     '', 'Creature completion counts remain separate. No new objects are generated by creating this inventory.']
target.write_text('\n'.join(md)+'\n',encoding='utf-8')
print('OBJECT_BACKLOG_INITIALIZED named_types='+str(len(named))+' artifacts='+str(sum(a['scope']=='normal' for a in art)))

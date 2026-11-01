# Gnomish wizard, gnome mummy and gnome zombie

Batch 15 extends the saved gnome ancestry with caster and undead presentations.
Three source identities use five physical forms: wizard and zombie each have
a bearded male and beardless female form; mummy uses one shared form. These
remain unrigged static drafts.

## Source facts and interpretation

| Identity | Source / official tiles | Traits and appearance |
| --- | --- | --- |
| `PM_GNOMISH_WIZARD` | `monsters.h:1695`; 342/343 | Small level-3 magical humanoid, spell attack, no innate resistance. Green pointed cap/clothing, peach face and pale male beard |
| `PM_GNOME_MUMMY` | `monsters.h:1909`; 386/387 | Small level-4 breathless/mindless undead, 1d6 claw, cold/sleep/poison resistance. Retained green cap, pale wraps/skin and red eyes |
| `PM_GNOME_ZOMBIE` | `monsters.h:2429`; 492/493 | Small level-1 breathless/mindless stalking undead, 1d5 claw, cold/sleep/poison resistance. Green face/clothing, gray male beard and red eyes |

Both undead identities carry gnome ancestry and no-corpse generation flags.
Gameplay distinctions stay in NetHack. Abstract size/weight do not define
literal miniature dimensions.

Sex-tile review found six pale beard pixels replaced by skin/green in the
female wizard and three gray beard pixels replaced by green in the female
zombie. The new female forms remove separate chin/beard locks and recolour
brows while retaining the exact same ancestry body, hat and costume. The mummy
tiles are identical, so its pale chin treatment is shared. No additional
sex-specific anatomy, hairstyle or outfit was invented.

The common offset black mass to the right/below is treated as cast shadow,
not an axe, staff, shield or cape. Existing source-gnome axe modules and red
cap-tip ornament are omitted in these derivatives. Their original source
models remain unchanged. Green cap and pale beard/chin cues are retained;
exact garment construction and mummy winding patterns are interpretations.
Minor colored cloth/hat flecks are ambiguous and remain refinement targets.
No invented exposed bones, graphic wounds, magical aura or equipment is added.

## Geometry and paint

`GnomeStates.py` appends the saved `gnome` collection from
`CreatureBatch2.blend`. All five saved body vertex hashes match `gnome_body`
exactly. Nose, ears, limbs, boots and pointed cap preserve the family. The
wizard has a pale face/beard and green costume; the zombie has green skin,
ash-gray male beard and red eyes. Beardless female variants follow the actual
tiles without changing body proportions.

Wizard/zombie garments stay separate and use new curved closed belts in place
of the base's rectangular belt. The mummy omits tunic, mantle, belt and buckle,
then adds ten solid linen ribbons fitted to the actual body. The neck strip
sits below the retained chin detail, leaving eyes and nose clear. Boots become
pale wrapped-foot masses while retaining the family's geometry. Final cloth
surfaces are within 4.5 mm of the body, with 1.5 mm thickness.

Paint uses corner vertex colors and shared miniature materials. Skin/cloth
changes are paint on existing surfaces, with no raised color patches. No fur
or scales were inferred. The established player fixed-clothing rule is unchanged;
these are separate NPC art-state modules, not claims about live inventory.

Native triangles: wizard/zombie male 62,184 each; mummy 70,236;
wizard/zombie female 60,704 each. These are draft costs, not production budgets.

`CreateCreatureBatch15.py` generates all five forms. The one-time
`CreateCreatureBatch15FemaleForms.py` added only the two female forms to the
initial saved review; fresh generation includes them. Use saved review scripts
to inspect rather than repeating that addition or regenerating ancestry.

## Artifacts

- `Art/CreatureInterpretations/CreatureBatch15.blend`: five editable collections,
  corner paint and studio; wizard male initially visible.
- `gnomish_wizard.fbx`, `gnome_mummy.fbx`, `gnome_zombie.fbx`,
  `gnomish_wizard_female.fbx`, `gnome_zombie_female.fbx`: actual exports.
- `Batch15-Models.png`: the three primary forms; female forms have separate
  actual studio/head renders alongside them.
- `MeshComparison-batch15.png`: all five forms, their respective official
  male/female tiles, actual front/rear and true 16×16 views.
- `Batch15-Projections.png` / `projection-report-batch15.json`: all 30 tiny
  camera candidates, spatial masks, bounds and diagnostic overlap scores.
- `Batch15-EyeReview.png`: ten actual front/profile head views.
- `batch15-mesh-inspection.json`: saved paint, geometry, floor, eye placement,
  red undead pigment, closed/fitted linen, ancestry hashes and sex modules.
- `batch15-protected-assets.json`: hashes of all preceding 48 exports:
  44 creature/player forms, three objects and the tile quad.
- `batch15-forms.json`: physical forms linked to the three stable `PM_*` IDs.
- `Batch15-Unreal-fixtures.png`: final live fixture capture.

`InspectCreatureBatch15.py`, `ReviewCreatureBatch15.py` and
`RenderCreatureBatch15.py` inspect/rerender saved geometry. Comparison scripts
use real renders and unmodified official pixels. Black source shadow is removed
spatially from projection targets while enclosed dark detail stays; diagnostic
overlap is not a claim of exact reconstruction.

## Integration and verification

Editor build and five targeted imports pass. The full importer supports 49
creature/player physical forms. Displayed neutral identity selects the species;
displayed female sex additionally selects `gnomish_wizard_female` or
`gnome_zombie_female`. Mummy remains shared. Selection uses no hidden-world
lookup. The new gnome forms use 15-degree yaw; other families retain their
existing orientation.

Live checks pass all six displayed sex cases, five correct physical meshes,
six respective official tile fallbacks, unknown identity and paint buffers.
Two real F9 switches preserve turn 5/input sequence 7. Native movement/map,
hero centring and 8x zoom pass. The actual engine capture is inspected, along
with ten studio front/rear views, ten head views and all 30 true 16x16 candidates.
All 48 preceding export hashes match. Tile fallback, objects, F7, first-person
camera and ancestry guards are preserved.

Evidence: `build-creature-batch15-{blender,female,renders,review,inspect,unreal,import,live}.log`.

Inventory: 394 unique source IDs = 45 completed creatures + one completed role
+ 336 remaining creatures + 12 remaining roles. There are 49 physical
creature/player forms: 45 primary creature forms, two female creature variants
and two requested human player forms. Objects remain separately tracked.
Suggested next batch: dwarf, dwarf leader and dwarf ruler.

## Finishing work

Further face/cloth/belt transitions, linen fold/fray refinement, zombie
pose/decay, rigs, casting/undead animation and effects, LODs and performance
remain separate work. These static drafts do not complete those milestones.

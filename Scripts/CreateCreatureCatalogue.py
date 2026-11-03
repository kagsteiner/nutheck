"""Source-only creature inventory and modelling taxonomy. No Blender/UE side effects."""
import csv
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Art/CreatureCatalogue'
SOURCE = ROOT / 'upstream/NetHack/include/monsters.h'


def split_args(text):
    result, start, depth, quoted, escape = [], 0, 0, False, False
    for i, char in enumerate(text):
        if quoted:
            if escape: escape = False
            elif char == '\\': escape = True
            elif char == '"': quoted = False
        elif char == '"': quoted = True
        elif char == '(': depth += 1
        elif char == ')': depth -= 1
        elif char == ',' and depth == 0:
            result.append(text[start:i].strip()); start = i + 1
    result.append(text[start:].strip())
    return result


def encyclopedia():
    entries, keys, line = [], [], 0
    for number, text in enumerate((ROOT/'upstream/NetHack/dat/data.base').read_text(encoding='utf-8').splitlines(), 1):
        if not text or text.startswith('#'): continue
        if text[0].isspace():
            if keys:
                entries.append((keys, line)); keys = []
        else:
            if not keys: line = number
            keys.append(text)
    return entries


def matches(pattern, name):
    return re.fullmatch(re.escape(pattern).replace(r'\*', '.*').replace(r'\?', '.'), name, re.I) is not None


# These are production groupings, not claims of biological descent. Source glyph
# classes remain separately available; several contain incompatible body plans.
CLASS_FAMILIES = {
 'DOG':('Animals','Mammals','Canids'), 'FELINE':('Animals','Mammals','Felids'),
 'RODENT':('Animals','Mammals','Rodents'), 'BAT':('Animals','Mammals','Bats'),
 'APE':('Animals','Mammals','Apes'), 'UNICORN':('Mythic bodies','Equine bodies','Equines'),
 'SPIDER':('Animals','Arthropods','Arachnids'), 'ANT':('Animals','Arthropods','Insects'),
 'XAN':('Animals','Arthropods','Flying insects'), 'WORM':('Animals','Invertebrates','Worms'),
 'SNAKE':('Animals','Reptiles','Snakes'), 'LIZARD':('Animals','Reptiles and amphibians','Mixed small reptiles'),
 'EEL':('Animals','Aquatic bodies','Aquatic animals'),
 'GNOME':('Humanoid peoples','Small humanoids','Gnomes'),
 'ORC':('Humanoid peoples','Humanoids','Orcs'), 'KOBOLD':('Humanoid peoples','Small humanoids','Kobolds'),
 'HUMAN':('Humanoid peoples','Humanoids','Humans and special identities'),
 'HUMANOID':('Humanoid peoples','Humanoids','Mixed humanoids'),
 'KOP':('Humanoid peoples','Humanoids','Keystone Kops'),
 'GIANT':('Humanoid peoples','Large humanoids','Giants'), 'OGRE':('Humanoid peoples','Large humanoids','Ogres'),
 'TROLL':('Humanoid peoples','Large humanoids','Trolls'),
 'NYMPH':('Mythic bodies','Humanoids','Nymphs'), 'CENTAUR':('Mythic bodies','Composite bodies','Centaurs'),
 'DRAGON':('Mythic bodies','Winged reptiles','Dragons'), 'NAGA':('Mythic bodies','Serpentine bodies','Nagas'),
 'GOLEM':('Constructs','Material bodies','Golems'),
 'MUMMY':('Undead','Ancestry plus state','Mummies'), 'ZOMBIE':('Undead','Ancestry plus state','Zombies'),
 'VAMPIRE':('Undead','Humanoids and alternate forms','Vampires'), 'LICH':('Undead','Skeletal spellcasters','Liches'),
 'WRAITH':('Undead','Spectral bodies','Wraiths'), 'GHOST':('Undead','Spectral bodies','Ghosts'),
 'JELLY':('Amorphous life','Soft bodies','Jellies'), 'BLOB':('Amorphous life','Soft bodies','Blobs'),
 'PUDDING':('Amorphous life','Soft bodies','Puddings and oozes'), 'FUNGUS':('Fungi','Fungal bodies','Fungi and molds'),
 'VORTEX':('Elemental manifestations','Volume effects','Vortices'),
 'ELEMENTAL':('Elemental manifestations','Elemental bodies','Elementals'),
 'LIGHT':('Elemental manifestations','Luminous bodies','Lights'),
 'WORM_TAIL':('Display auxiliaries','Body segments','Worm tails'),
 'ANGEL':('Supernatural beings','Celestial bodies','Celestials'),
 'DEMON':('Supernatural beings','Infernal and unique bodies','Demons and related identities'),
 'IMP':('Supernatural beings','Small supernatural bodies','Imps and related beings'),
 'COCKATRICE':('Mythic bodies','Avian reptile bodies','Cockatrices'),
 'EYE':('Mythic bodies','Floating bodies','Eyes and spheres'),
 'GREMLIN':('Mythic bodies','Small humanoid bodies','Gremlins and gargoyles'),
 'JABBERWOCK':('Mythic bodies','Composite bodies','Jabberwocks'),
 'LEPRECHAUN':('Humanoid peoples','Small humanoids','Leprechauns'),
 'MIMIC':('Amorphous life','Disguised bodies','Mimics'),
 'PIERCER':('Mythic bodies','Rocklike ambush bodies','Piercers'),
 'QUADRUPED':('Animals and mythic beasts','Quadruped bodies','Mixed large quadrupeds'),
 'QUANTMECH':('Humanoid peoples','Humanoids','Science specialists'),
 'RUSTMONST':('Mythic bodies','Specialised quadrupeds','Rust monsters and disenchanters'),
 'TRAPPER':('Mythic bodies','Flattened ambush bodies','Trappers and lurkers'),
 'UMBER':('Mythic bodies','Insectoid bipeds','Umber hulks'),
 'XORN':('Mythic bodies','Radial bodies','Xorns'),
 'YETI':('Animals and mythic beasts','Primate and hybrid bodies','Apes and hairy bipeds'),
 'ZRUTY':('Mythic bodies','Large bipedal beasts','Zruties'),
}


def classify(name, symbol, flags):
    cls = symbol.removeprefix('S_')
    path = CLASS_FAMILIES.get(cls, ('Unresolved body plans', 'Source class groups', cls.replace('_',' ').title()))
    family = path[-1]
    if cls == 'ANGEL' and name.lower() in ['couatl','ki-rin']:
        return ('Mythic bodies','Composite bodies','Winged serpents' if name.lower()=='couatl' else 'Ki-rin')
    if cls == 'DEMON' and name in ['Death','Pestilence','Famine']:
        return ('Supernatural beings','Personifications','Riders')
    if cls == 'DEMON' and name in ['djinni','mail daemon']:
        return ('Supernatural beings','Special identities',name.title())
    if cls == 'QUADRUPED':
        if name in ['mumak','mastodon']: return (*path[:2], 'Proboscideans')
        if name in ['titanothere','baluchitherium']: return (*path[:2], 'Large ungulate bodies')
        if name == 'rothe': return (*path[:2], 'Rothe')
    if cls == 'YETI':
        if name == 'owlbear': return ('Mythic bodies','Composite bodies','Owlbears')
        if name in ['monkey','ape','carnivorous ape']: return ('Animals','Mammals','Primates')
    if cls == 'EYE' and name == 'gas spore': return ('Fungi','Floating spore bodies','Gas spores')
    if cls == 'GREMLIN': return (*path[:2], 'Gargoyles' if 'gargoyle' in name else 'Gremlins')
    if cls == 'RUSTMONST': return (*path[:2], name.title())
    # Split mixed glyph classes where a shared sculpt would erase anatomy.
    for token, leaf in [('bee','Bees'), ('beetle','Beetles'), ('ant','Ants'),
                        ('scorpion','Scorpions'), ('spider','Spiders'),
                        ('newt','Newts'), ('gecko','Geckos'), ('crocodile','Crocodilians'),
                        ('turtle','Turtles'), ('piranha','Fish'), ('shark','Sharks'),
                        ('jellyfish','Jellyfish'), ('kraken','Cephalopods')]:
        if re.search(r'\b'+re.escape(token)+r's?\b', name) and cls in ['ANT','SPIDER','LIZARD','EEL']: return (*path[:2], leaf)
    if cls == 'HUMANOID':
        for token, leaf in [('dwarf','Dwarves'),('hobbit','Hobbits'),('mind flayer','Mind flayers')]:
            if token in name: return (*path[:2], leaf)
    if cls == 'HUMAN' and 'M2_ELF' in flags: return ('Humanoid peoples','Humanoids','Elves')
    if 'were' in name and cls in ['DOG','RODENT','HUMAN']:
        return ('Supernatural forms','Lycanthropes',family)
    return path


def recipe(name, path):
    base = path[-1].lower().replace(' ', '_')
    parent, changes = None, []
    if path[-1] == 'Canids':
        base = 'canid'
        if 'wolf' in name: base = 'wolf'
        elif 'dog' in name or 'puppy' in name: base = 'dog'
        if 'winter wolf' in name:
            parent = 'winter wolf' if 'cub' in name else 'wolf'
            changes += ['White fur (art interpretation); preserve default-tile accents', 'Cold-breath attachment and attack animation required']
        elif name in ['jackal','fox','coyote']: parent = 'canid'; changes += ['Distinct ears, muzzle, leg proportions and tail; not a palette swap']
    if path[-1] == 'Rodents':
        base = 'rat' if re.search(r'\brat\b',name) else name.replace(' ','_')
        if name == 'giant rat': parent = 'sewer rat'; changes += ['Larger lean frame than sewer rat; user approved thinner torso/haunches over squat tile fidelity; retain rodent anatomy']
    if path[-1] == 'Gnomes':
        base = 'gnome'
        if name == 'gnome ruler': parent = 'gnome'; changes += ['Detachable crown and rank clothing; crown is an art decision, not an inventory fact']
        elif name != 'gnome': parent = 'gnome'; changes += ['Rank/role clothing and equipment modules']
    if path[-1] == 'Dragons':
        base='dragon'; parent='adult dragon' if not name.startswith('baby ') else name.removeprefix('baby ')
        changes += ['Shared dragon anatomy with species palette; preserve breath effect/resistance distinctions']
    if name.startswith('baby ') or name.endswith(' cub'):
        changes += ['Juvenile proportions and gait; do not uniformly shrink adult mesh']
    if path[0] == 'Undead' and path[-1] in ['Mummies','Zombies']:
        ancestry = name.replace(' mummy','').replace(' zombie','')
        base = ancestry + '_humanoid'; parent = ancestry
        changes += ['Ancestry body plus undead deformation/skin; detachable wraps for mummy', 'Validate anatomy and source silhouette per ancestry']
    if path[-1] == 'Golems': changes += ['Shared articulated plan only where suitable; material, silhouette and joints may require new geometry']
    if path[-1] in ['Mixed large quadrupeds','Humans and special identities','Demons and related identities','Apes and hairy bipeds','Mixed small reptiles','Aquatic animals','Mixed humanoids','Eyes and spheres']:
        changes += ['Mixed production group: establish species anatomy before sharing a final body or rig']
    if not changes: changes = ['Reuse family blockout only after silhouette/anatomy review; per-species default-tile palette and details']
    return {'base':base, 'suggested_parent':parent, 'changes':changes,
            'review_required':True, 'status':'planning only'}


def player_hierarchy(creatures):
    """Role selection rules come from role.c, not monster flags or tile existence."""
    role_path = ROOT/'upstream/NetHack/src/role.c'
    raw = role_path.read_text(encoding='utf-8')
    clean = re.sub(r'/\*.*?\*/', lambda m: '\n'*m[0].count('\n'), raw, flags=re.S)
    start = clean.index('const struct Role roles[')
    end = clean.index('/* Table of all races */') if '/* Table of all races */' in clean else clean.index('const struct Race races[')
    declarations = list(re.finditer(r'^ {4}\{\s*\{\s*"([^"\n]+)"\s*,\s*("[^"\n]+"|0)\s*\}', clean[start:end], re.M))
    by_id = {r['id']:r for r in creatures}
    descriptions = {
        'PM_ARCHEOLOGIST':'Explorer and scholar; reusable expedition clothing and tool accessories.',
        'PM_BARBARIAN':'Martial adventurer; distinct muscular proportions and fixed icon-derived appearance.',
        'PM_CAVE_DWELLER':'Prehistoric adventurer; shared body with primitive clothing and tool modules.',
        'PM_HEALER':'Medical adventurer; fixed icon-derived medical role appearance.',
        'PM_KNIGHT':'Armoured warrior; fixed icon-derived armour appearance on a compatible body.',
        'PM_MONK':'Unarmed martial artist; robes, exposed hands and martial movement requirements.',
        'PM_CLERIC':'Religious adventurer; fixed icon-derived vestments and religious appearance.',
        'PM_ROGUE':'Stealth adventurer; fixed icon-derived light clothing appearance.',
        'PM_RANGER':'Wilderness adventurer; fixed icon-derived outdoor clothing appearance.',
        'PM_SAMURAI':'Martial adventurer; distinct armour/clothing silhouette and weapon modules.',
        'PM_TOURIST':'Travelling adventurer; distinctive travel clothing and accessory modules.',
        'PM_VALKYRIE':'Warrior role; female-only at initial character selection in this source version.',
        'PM_WIZARD':'Arcane adventurer; fixed icon-derived robe silhouette.',
    }
    base = dict(id='PLAYER', name='Player', node_type='base_class',
        description='Player presentation family: role subclasses with permitted starting-sex subclasses. Role is a profession, not a biological species.',
        model_recipe={'base':'player_body', 'changes':['Reuse compatible anatomy; integrate icon-derived costuming into one fixed character',
            'Race/ancestry is an independent anatomy axis; these nodes are not a full race/role/sex cross-product',
            'Never assume current inventory from a role or concept accessory']},
        restriction_scope='Initial character selection only; not a restriction on later transformations, polymorph or monster appearances.',
        children=[])
    for i, declaration in enumerate(declarations):
        offset=start+declaration.start()
        block=clean[offset:start+declarations[i+1].start() if i+1<len(declarations) else end]
        role_id=re.search(r'\bPM_\w+',block)[0]
        monster=by_id[role_id]
        allow=re.search(r'\bMH_\w+(?:\s*\|\s*(?:MH_|ROLE_)\w+)*',block)[0]
        line=clean.count('\n',0,clean.index('"'+declaration[1]+'"',offset))+1
        source={'path':'upstream/NetHack/src/role.c','line':line,'allow_mask':allow}
        male_name=declaration[1]; female_name=declaration[2].strip('"') if declaration[2]!='0' else male_name
        aliases=list(dict.fromkeys([male_name,female_name,monster['name'].title()]))
        node=dict(id='PLAYER_ROLE_'+role_id[3:],parent_id='PLAYER',name=monster['name'].title(),
            node_type='role_subclass',aliases=aliases,creature_id=role_id,
            description=descriptions[role_id]+' Visual modules are proposals, not live inventory facts.',
            source=source,allowed_starting_sexes=[],children=[],
            model_recipe={'base':'player_body','role_appearance':monster['name'].replace(' ','_'),'clothing_detachable':False,
                          'changes':['Reuse compatible anatomy/rig; fit role silhouette and official default-tile colours',
                                     'Fixed icon appearance; no detachable clothing (explicit user correction); sex variants may share compatible anatomy'],
                          'status':'planning only; existing tile-volume proxies are separate'})
        for sex,flag,label in [('male','ROLE_MALE',male_name),('female','ROLE_FEMALE',female_name),('neuter','ROLE_NEUTER',monster['name'].title())]:
            if not re.search(r'\b'+flag+r'\b',allow): continue
            node['allowed_starting_sexes'].append(sex)
            node['children'].append(dict(id=node['id']+'_'+sex.upper(),parent_id=node['id'],
                name=label,sex=sex,node_type='sex_subclass',creature_id=role_id,
                description=f'{sex.capitalize()} starting {label}; inherits player body and role modules. Separate catalogue variant does not require a separate sculpt.',
                official_tiles=[t for t in monster['official_tiles'] if t['label'].endswith(','+sex)],
                source=source,asset_status=('existing anatomical draft (human player)' if (role_id,sex) in {('PM_VALKYRIE','female'),('PM_BARBARIAN','male')} else 'existing tile-volume proxy; no anatomical player draft')))
        if role_id in {'PM_VALKYRIE','PM_BARBARIAN'}:
            node['generated_ancestries']=['human']
            node['asset_status']='human female draft verified' if role_id=='PM_VALKYRIE' else 'partial: human male draft verified; female unmodelled'
            node['model_recipe']['status']=node['asset_status']
        base['children'].append(node)
    assert len(base['children'])==13
    return base


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = SOURCE.read_text(encoding='utf-8')
    clean = re.sub(r'/\*.*?\*/', lambda m: '\n'*m[0].count('\n'), raw, flags=re.S)
    guards, conditions = [], {}
    for line, text in enumerate(clean.splitlines(), 1):
        directive = re.match(r'\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b(.*)', text)
        if directive:
            kind, expression = directive.groups()
            if kind in ['if','ifdef','ifndef']: guards.append(kind+' '+expression.strip())
            elif kind == 'endif': guards.pop()
            elif guards: guards[-1] += ' / '+kind+' '+expression.strip()
        conditions[line] = list(guards)
    entries = encyclopedia()
    tile_text=(ROOT/'upstream/NetHack/win/share/monsters.txt').read_text()
    tiles=defaultdict(list)
    for index,label in re.findall(r'^# tile (\d+) \(([^\n]+)\)',tile_text,re.M):
        tiles[label.rsplit(',',1)[0]].append({'index':int(index),'label':label})
    rows=[]
    for match in re.finditer(r'^\s*MON\(', clean, re.M):
        start=match.end(); depth=1; quoted=False; escape=False; end=start
        while depth:
            c=clean[end]
            if quoted:
                if escape: escape=False
                elif c=='\\': escape=True
                elif c=='"': quoted=False
            elif c=='"': quoted=True
            elif c=='(': depth+=1
            elif c==')': depth-=1
            end+=1
        args=split_args(clean[start:end-1]); assert len(args)==14, args
        aliases=re.findall(r'"([^"\n]*)"',args[0]); assert aliases, args[0]
        name=aliases[-1]; aliases=list(dict.fromkeys(aliases))
        line=clean.count('\n',0,match.start())+1
        # Leading whitespace may include a newline; point to the actual MON token.
        line=clean.count('\n',0,clean.index('MON(',match.start()))+1
        flags=' | '.join(args[8:11]); path=classify(name,args[1],flags)
        level=split_args(args[2][args[2].find('(')+1:-1])
        size=re.search(r'MZ_\w+',args[5]); size=size[0] if size else args[5]
        traits=[]
        for flag,label in [('M1_FLY','flies'),('M1_SWIM','swims'),('M1_AMPHIBIOUS','amphibious'),
                           ('M1_NOHANDS','no grasping hands'),('M1_HUMANOID','humanoid body'),
                           ('M1_CARNIVORE','carnivorous'),('M1_HERBIVORE','herbivorous'),
                           ('M1_OMNIVORE','omnivorous'),('M2_UNDEAD','undead'),('M2_DOMESTIC','domestic')]:
            if re.search(r'\b'+flag+r'\b',flags): traits.append(label)
        attacks=re.findall(r'ATTK\(\s*(AT_\w+)\s*,\s*(AD_\w+)\s*,\s*([^,]+),\s*([^\)]+)\)',args[4])
        description=f"{path[-1]}; {size.removeprefix('MZ_').lower()} source size; base level {level[0]}, difficulty {args[11]}."
        if traits: description+=' '+', '.join(traits).capitalize()+'.'
        methods={'WEAP':'weapon','BREA':'breath','MAGC':'magic','ENGL':'engulf','TUCH':'touch','BUTT':'headbutt','STNG':'sting','EXPL':'explosion','BOOM':'death explosion','NONE':'passive contact'}
        effects={'PHYS':'physical','COLD':'cold','FIRE':'fire','ELEC':'electricity','DRST':'poison','ACID':'acid','SLEE':'sleep','STON':'petrification','DRLI':'life drain','STUN':'stun','WRAP':'constriction'}
        if attacks: description+=' Attacks: '+', '.join(methods.get(a[0][3:],a[0][3:].lower())+'/'+effects.get(a[1][3:],a[1][3:].lower()) for a in attacks)+'.'
        refs=[]
        for keys, n in entries:
            if any(matches(k,a) for k in keys if not k.startswith('~') for a in aliases) and not any(matches(k[1:],a) for k in keys if k.startswith('~') for a in aliases):
                refs.append({'source':'upstream/NetHack/dat/data.base','line':n,'keys':keys})
        rows.append(dict(id='PM_'+args[13], name=name, aliases=aliases, hierarchy=list(path), description=description,
            source={'path':'upstream/NetHack/include/monsters.h','line':line,'conditions':conditions[line]},
            source_class=args[1], level=level[0], level_fields=level, difficulty=args[11],size=size,
            attacks=[dict(method=a[0],effect=a[1],dice=a[2],sides=a[3]) for a in attacks],
            generation=args[3],resistances=args[6],conferred_resistances=args[7],flags=args[8:11],ascii_colour=args[12],
            official_tiles=tiles.get(name,[]),encyclopedia=refs,model_recipe=recipe(name,path),
            asset_status='existing anatomical draft (human player, female)' if name=='valkyrie' else 'partial anatomical draft (human player, male only)' if name=='barbarian' else 'existing anatomical draft' if name in ['giant ant','little dog','goblin','jackal','fox','gnome','sewer rat','giant rat','gnome ruler','kitten','housecat','large cat','wolf','winter wolf cub','winter wolf','dog','large dog','dingo','coyote','warg','rabid rat','bat','giant bat','vampire bat','jaguar','lynx','panther','tiger','hell hound pup','hell hound','pony','horse','warhorse','white unicorn','gray unicorn','black unicorn','kobold','large kobold','kobold leader','kobold shaman','kobold mummy','kobold zombie','gnomish wizard','gnome mummy','gnome zombie','dwarf','dwarf leader','dwarf ruler','dwarf mummy','dwarf zombie','hobgoblin','hill orc','Mordor orc','floating eye','newt','lichen','Uruk-hai','orc shaman','orc-captain','grid bug','orc mummy','orc zombie','soldier ant','fire ant','giant beetle','shopkeeper','killer bee','queen bee','xan','cave spider','giant spider','scorpion','gecko','iguana','lizard','garter snake','snake','water moccasin','python','pit viper','cobra'] else 'not modelled in sculpted pipeline'))
    assert len({r['id'] for r in rows})==len(rows)
    players=player_hierarchy(rows)
    data={'schema_version':2,'source_revision':'16ff59115315917b93185d026aeefea06db9b0f4',
          'scope':'All MON declarations in pinned source, including conditional and auxiliary entries; not a compiled runtime roster.',
          'taxonomy':'Production anatomy grouping, not scientific phylogeny. Unresolved groups require manual review.',
          'description_policy':'Source-derived factual summaries, not copied literary encyclopedia passages. Raw AT_/AD_ codes are retained.',
          'count':len(rows),'creatures':rows,'player_hierarchy':players}
    (OUT/'creatures.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    (OUT/'players.json').write_text(json.dumps(players,indent=2,ensure_ascii=False),encoding='utf-8')
    with (OUT/'players.csv').open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=['id','parent_id','node_type','name','sex','creature_id','description','source_line'])
        writer.writeheader()
        for node in [players]+[n for role in players['children'] for n in [role]+role['children']]:
            writer.writerow({**{key:node.get(key,'') for key in ['id','parent_id','node_type','name','sex','creature_id','description']},'source_line':node.get('source',{}).get('line','')})
    with (OUT/'creatures.csv').open('w',newline='',encoding='utf-8-sig') as stream:
        fields=['id','name','hierarchy','description','aliases','base','parent','changes','conditions','source_line','asset_status']
        writer=csv.DictWriter(stream,fieldnames=fields); writer.writeheader()
        for r in rows:
            writer.writerow(dict(id=r['id'],name=r['name'],hierarchy=' / '.join(r['hierarchy']),description=r['description'],
                aliases='; '.join(r['aliases']),base=r['model_recipe']['base'],parent=r['model_recipe']['suggested_parent'],
                changes='; '.join(r['model_recipe']['changes']),conditions='; '.join(r['source']['conditions']),source_line=r['source']['line'],asset_status=r['asset_status']))
    grouped=defaultdict(list)
    for row in rows: grouped[tuple(row['hierarchy'])].append(row)
    md=['# Creature hierarchy and modelling catalogue','',f"{len(rows)} source declarations. See [creatures.json](creatures.json) for full traits, aliases, source locations and encyclopedia references; [creatures.csv](creatures.csv) for filtering.",'',
        'This is a modelling taxonomy, not biological phylogeny. Unresolved source classes are explicit review queues. Conditional declarations and display auxiliaries are included; this is not a claim about compiled availability. All reuse recipes are proposals. Giant ant, little dog, goblin, jackal, fox, gnome, sewer rat, giant rat, gnome ruler, kitten, housecat, large cat, wolf, winter wolf cub, winter wolf, dog, large dog, dingo, coyote, warg, rabid rat, bat, giant bat, vampire bat, jaguar, lynx, panther, tiger, hell hound pup, hell hound, pony, horse, warhorse, white unicorn, gray unicorn, black unicorn, kobold, large kobold, kobold leader, kobold shaman, kobold mummy, kobold zombie, gnomish wizard, gnome mummy, gnome zombie, dwarf, dwarf leader, dwarf ruler, dwarf mummy, dwarf zombie, hobgoblin, hill orc, Mordor orc, floating eye, newt, lichen, Uruk-hai, orc shaman, orc-captain, grid bug, orc mummy, orc zombie, soldier ant, fire ant, giant beetle, shopkeeper, killer bee, queen bee, xan, cave spider, giant spider, scorpion, gecko, iguana, lizard, garter snake, snake, water moccasin, python, pit viper and cobra have static anatomical drafts. Catalogue generation itself never generates meshes.','',
        'Descriptions summarize native metadata. Source size is abstract, ASCII colour is not skin colour, and listed attacks are capabilities rather than current inventory. Canonical neutral names retain gendered aliases (for example gnome ruler = gnome king/queen).','']
    md+=['## Player','',
         'Base class **Player** → role subclass → permitted starting-sex subclass. These are presentation/role classes, not biological species. Race/ancestry remains an independent axis. Rules come from `src/role.c` allow masks, not tile availability. See [players.json](players.json) or [players.csv](players.csv) for this branch alone.','',
         '**Valkyrie permits only female starting characters.** A male Valkyrie tile exists in the official artwork but does not make that a permitted starting choice. This hierarchy does not constrain later sex changes, polymorph or monster appearances.','']
    for role in players['children']:
        md += ['### Player / '+role['name'],'',role['description'],'',
               f"Source: `src/role.c:{role['source']['line']}`; linked creature: `{role['creature_id']}`.",'']
        for child in role['children']:
            md += [f"- **{child['name']} — {child['sex']}** (`{child['id']}`): {child['description']}"]
        md += ['']
    for path, members in sorted(grouped.items()):
        md+=['## '+' / '.join(path),'']
        for r in members:
            plan=r['model_recipe']; conditional=' **Conditional source entry.**' if r['source']['conditions'] else ''
            md += [f"- **{r['name']}** (`{r['id']}`): {r['description']}{conditional}",
                   f"  - Model: `{plan['base']}`"+(f"; parent: {plan['suggested_parent']}" if plan['suggested_parent'] else '')+'. '+'; '.join(plan['changes'])+'.']
        md.append('')
    (OUT/'Hierarchy.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({'count':len(rows),'families':len(grouped),'conditional':sum(bool(r['source']['conditions']) for r in rows),'unresolved':sum(r['hierarchy'][0]=='Unresolved body plans' for r in rows)}))


if __name__ == '__main__': main()

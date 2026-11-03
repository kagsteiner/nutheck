"""Real native altar wishes/covered backgrounds and both shopkeeper sex glyphs."""
from BridgeGameplay import Game,DIRS,WALK
import json
g=Game(debug=True);seen=[]
def wish(text):
    g.reply(23);p=g.next_input();assert p['type']=='line',p;g.reply(text);g.settle()
def step():
    old=g.position
    for dx,dy,key in DIRS:
        c=g.cells.get((old[0]+dx,old[1]+dy),{})
        if c.get('terrain') in WALK and c.get('kind') not in ('monster','pet'):
            g.command(key)
            if g.position!=old:return old
    raise AssertionError('No adjacent known floor')
try:
    g.settle()
    for kind in ['unaligned','chaotic','neutral','lawful']:
        wish(kind+' altar')
        old=step();tile=g.cells[old];assert tile['terrain']=='altar_'+kind,(kind,tile,g.messages[-8:])
        assert tile['tile_index']==1305+['unaligned','chaotic','neutral','lawful'].index(kind),tile
        delta=(old[0]-g.position[0],old[1]-g.position[1]);back=next(key for dx,dy,key in DIRS if (dx,dy)==delta)
        g.command(back);assert g.position==old
        assert g.cells[old]['terrain']=='altar_'+kind,g.cells[old]
        seen.append(dict(kind=kind,tile=tile['tile_index'],previously_displayed_terrain_retained_under_hero=True))
    for sex in ['male','female']:
        g.reply(7);p=g.next_input();assert p['type']=='line',p;g.reply(sex+' shopkeeper')
        p=g.next_input()
        if p['type']=='yn' and 'force shopkeeper' in p['text']:g.reply(ord('y'))
        else:raise AssertionError(p)
        g.settle()
        candidates=[c for c in g.cells.values() if c.get('display_monster')=='shopkeeper' and c.get('female')==(sex=='female')]
        assert candidates,(sex,g.messages[-8:]);assert any(c['tile_index']==554+(sex=='female') for c in candidates)
        seen.append(dict(shopkeeper_sex=sex,tile=554+(sex=='female')))
    # Native sanctum glyph is a distinct fifth appearance, irrespective of deity.
    g.reply(22);p=g.next_input();assert p['type']=='line',p;g.reply('?');p=g.next_input()
    assert p['type']=='menu',(p,g.menu)
    target=next(x for x in g.menu['items'] if 'astral' in x['text'].lower() and x['selectable'])
    g.reply(str(target['index'])+':-1');g.settle()
    g.command(6) # wizard magic mapping, preserving native glyph selection
    other=[c for c in g.cells.values() if c.get('terrain')=='altar_other']
    assert other,('No displayed sanctum altar',g.messages[-12:])
    assert any(c['tile_index']==1309 for c in other),other
    seen.append(dict(kind='other',tile=1309,native_sanctum=True))
    print('BRIDGE_SPECIAL_BATCH2_PASS '+json.dumps(seen),flush=True)
finally:g.close()

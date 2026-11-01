"""Native wizard wishes exercise displayed corpse and distinct terrain metadata."""
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
    raise AssertionError('No adjacent floor')
try:
    g.settle()
    for species in ['newt','giant rat']:
        wish(species+' corpse');g.command('i');item=next(x for x in g.menu['items'] if species+' corpse' in x['text'].lower())
        g.reply(ord('d'));g.next_input();g.reply(item['key']);g.settle();old=step();tile=g.cells[old]
        assert tile['kind']=='item' and tile.get('display_object')=='corpse',(tile,g.messages[-8:])
        assert 'display_monster' not in tile
        seen.append(dict(species_wished=species,display_object=tile['display_object'],tile=tile['tile_index']))
    for name in ['fountain','sink']:
        wish(name);old=step();tile=g.cells[old];assert tile['terrain']==name,(name,tile,g.messages[-8:])
        seen.append(dict(terrain=name,glyph=tile['glyph']))
    assert all('display_object' not in c for c in g.cells.values() if c['kind']!='item')
    print('BRIDGE_SPECIAL_BATCH1_PASS '+json.dumps(seen),flush=True)
finally:g.close()

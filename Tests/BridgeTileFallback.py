"""Native tile metadata, randomised potion appearances and restored mapping."""
from BridgeGameplay import Game,DIRS,WALK,ROOT
import json,re
atlas=json.loads((ROOT/'Art/TileFallback/atlas.json').read_text())
tiles=atlas['tiles'];report=[]
base={int(g):int(t) for t,g in re.findall(r'NO_CUSTOMCOLOR,\s+NO_CUSTOMCOLOR,\s+(\d+),\s+0\s*},\s*/\* \[(\d+)\]',(ROOT/'upstream/NetHack/src/tile.c').read_text())}
for attempt in range(2):
    g=Game(debug=True)
    try:
        g.settle()
        for name in ['potion of healing','potion of extra healing','potion of speed']:
            g.command('i');before={i['key']:i['text'] for i in g.menu['items'] if i['selectable']}
            g.reply(23);prompt=g.next_input();assert prompt['type']=='line';g.reply(name);g.settle()
            g.command('i');item=next(i for i in g.menu['items'] if i['selectable'] and before.get(i['key'])!=i['text'])
            g.reply(ord('d'));g.next_input();g.reply(item['key']);g.settle();old=g.position
            for dx,dy,key in DIRS:
                c=g.cells.get((old[0]+dx,old[1]+dy),{})
                if c.get('terrain') in WALK and c.get('kind') not in ('monster','pet'):
                    g.command(key)
                    if g.position!=old:break
            assert g.position!=old
            c=g.cells[old];assert c['kind']=='item',c
            idx=c['tile_index'];assert 0<=idx<atlas['tile_count']
            t=tiles[idx];assert t['source']=='objects' and not t['statue'] and '/' in t['label'],t
            appearance=t['label'].split(' / ')[0]
            assert appearance in item['text'].lower() or name in item['text'].lower(),(t,item)
            report.append(dict(wish=name,glyph=c['glyph'],tile_index=idx,appearance=t['label'],inventory=item['text'],static_tile=base[c['glyph']],session=str(g.root)))
        assert all(0<=c['tile_index']<atlas['tile_count'] for c in g.cells.values())
        # Save/restore must re-establish the same game's appearance shuffle.
        session=g.root;g.close();g=None
        restored=Game(session=session,debug=True);g=restored;g.settle()
        row=report[-1];assert any(c.get('tile_index')==row['tile_index'] for c in g.cells.values()),row
    finally:
        if g:g.close()
print('BRIDGE_TILE_FALLBACK_PASS '+json.dumps(dict(potions=report,shuffled_from_static=sum(r['tile_index']!=r['static_tile'] for r in report),restore_mapping=True)),flush=True)

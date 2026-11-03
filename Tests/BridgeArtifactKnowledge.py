"""Real isolated wizard session: wish, drop and reveal objects through window events."""
from BridgeGameplay import Game,DIRS,WALK
import json

g=Game(debug=True);seen=[]
try:
    g.settle()
    for name,wish in [('war hammer','Mjollnir'),('battle-axe','Cleaver'),('long sword','long sword named Pretender')]:
        g.reply(23) # NetHack wizard wish, Ctrl+W; native UI determines the result.
        prompt=g.next_input();assert prompt['type']=='line',(prompt,g.messages[-5:])
        g.reply(wish);g.settle()
        g.command('i')
        if name=='gold piece':key=ord('$')
        else:
            item=next(i for i in g.menu['items'] if (('pretender' in i['text'].lower()) if 'Pretender' in wish else (wish.lower() in i['text'].lower() or name in i['text'].lower())))
            if wish in ('Mjollnir','Cleaver'):
                assert ' named '+wish in item['text'],item # native name visible before full identification
            key=item['key']
            assert wish.lower().split(' named ')[-1] in item['text'].lower(),item
        g.reply(ord('d'));prompt=g.next_input()
        assert prompt['type'] not in ('command','line'),prompt
        g.reply(key);g.settle()
        old=g.position
        for dx,dy,key in DIRS:
            cell=g.cells.get((old[0]+dx,old[1]+dy),{})
            if cell.get('terrain') in WALK and cell.get('kind') not in ('monster','pet'):
                g.command(key)
                if g.position!=old:break
        assert g.position!=old,'No safe adjacent floor for object reveal'
        tile=g.cells[old];assert tile['kind']=='item' and tile.get('display_object')==name,(name,tile,g.messages[-8:])
        seen.append(dict(name=name,glyph=tile['glyph'],x=old[0],y=old[1]))
        assert tile.get('display_artifact','') == (wish if wish in ('Mjollnir','Cleaver') else ''),(wish,tile,g.messages[-8:])
        assert all('display_object' not in t for t in g.cells.values() if t['kind']!='item')
    report=dict(objects=seen,session=str(g.root),only_displayed_glyphs=True)
    (g.root/'object-check.json').write_text(json.dumps(report,indent=2))
    print('BRIDGE_ARTIFACT_KNOWLEDGE_PASS '+json.dumps(report),flush=True)
finally:g.close()

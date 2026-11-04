"""Fixed weapon appearance restore regression in separate native sessions."""
from BridgeGameplay import Game,DIRS,WALK,ROOT
import json
results=[]
for name,tile in [('silver saber',840),('broadsword',841),('two-handed sword',844)]:
    g=Game(debug=True)
    try:
        g.settle();g.command('i');prior={i['key']:i['text'] for i in g.menu['items'] if i['selectable']};g.reply(23);assert g.next_input()['type']=='line';g.reply(name);g.settle()
        g.command('i');item=next(i for i in g.menu['items'] if i['selectable'] and prior.get(i['key'])!=i['text'])
        g.reply(ord('d'));g.next_input();g.reply(item['key']);g.settle();at=g.position
        for dx,dy,key in DIRS:
            c=g.cells.get((at[0]+dx,at[1]+dy),{})
            if c.get('terrain') in WALK and c.get('kind') not in ('monster','pet'):
                g.command(key)
                if g.position!=at:break
        assert g.position!=at
        before=g.cells[at];assert before.get('tile_index')==tile and not before.get('display_artifact'),(name,before,g.messages[-5:])
        session=g.root;g.close();g=None
        g=Game(session=session,debug=True);g.settle();after=g.cells[at]
        assert after.get('tile_index')==tile and after['glyph']==before['glyph'],(before,after)
        results.append(dict(name=name,session=str(session),position=at,glyph=after['glyph']))
    finally:
        if g:g.close()
(ROOT/'Art/ObjectInterpretations/weapon-batch4-restore.json').write_text(json.dumps(results,indent=2))
print('WEAPON_BATCH4_RESTORE_PASS '+json.dumps(results))

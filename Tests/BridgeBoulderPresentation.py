"""Displayed boulders retain native blind memory and hallucinated glyph selection."""
from BridgeGameplay import Game,ROOT
from pathlib import Path
import os,json

def enter(g):
    g.settle();g.reply(22);g.next_input();g.reply('?');g.next_input()
    e=next(i for i in g.menu['items'] if i['selectable'] and 'soko4:' in i['text']);g.reply(str(e['index']));g.settle()
    p=g.root/'control.lua';p.write_text('nh.debug_flags({mongen=false,hunger=false});')
    g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(p,ROOT/'Binaries/NetHack')).as_posix());g.settle()
    return next(p for p,c in g.cells.items() if c.get('display_object')=='boulder' and g.state['vision'][p[1]*79+p[0]]=='1')

def wish(g,text):
    g.command('i');prior={i['key']:i['text'] for i in g.menu['items'] if i['selectable']}
    g.reply(23);g.next_input();g.reply(text);g.settle();g.command('i')
    return next(i['key'] for i in g.menu['items'] if i['selectable'] and prior.get(i['key'])!=i['text'])

result={};g=Game(debug=True)
try:
    at=enter(g);glyph=g.cells[at]['glyph'];key=wish(g,'uncursed blindfold')
    g.reply(ord('P'));g.next_input();g.reply(key);g.settle();g.command(18)
    assert '1' not in g.state['vision'] and g.cells[at].get('display_object')=='boulder' and g.cells[at]['glyph']==glyph
    root=g.root;g.close();g=None;g=Game(root,debug=True);g.settle()
    assert '1' not in g.state['vision'] and g.cells[at].get('display_object')=='boulder' and g.cells[at]['glyph']==glyph
    result['blind_memory_and_restore']=True
finally:
    if g:g.close()
g=Game(debug=True)
try:
    at=enter(g);tile=g.cells[at]['tile_index'];key=wish(g,'uncursed potion of hallucination')
    g.reply(ord('q'));g.next_input();g.reply(key);g.settle();seen=[]
    for _ in range(8):
        g.command(18);c=g.cells[at];seen.append(c['tile_index'])
        assert (c.get('display_object')=='boulder')==(c['tile_index']==tile),c
    assert any(t!=tile for t in seen),seen
    result['hallucinated_tiles']=seen;result['hidden_real_boulder_not_forced']=True
finally:g.close()
result['status']='PASS';(ROOT/'Art/Sokoban/boulder-presentation.json').write_text(json.dumps(result,indent=2))
print('BOULDER_PRESENTATION_PASS '+json.dumps(result),flush=True)

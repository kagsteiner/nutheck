"""Helpers for fresh isolated native artifact sessions; importing starts no game."""
from BridgeGameplay import Game,ROOT,DIRS,WALK
from pathlib import Path
import os

def load(g,code):
    p=g.root/'control.lua';p.write_text(code)
    g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(p,ROOT/'Binaries/NetHack')).as_posix());g.settle()

def setup():
    g=Game(debug=True);g.settle();load(g,'nh.debug_flags({mongen=false,hunger=false});for x=1,79 do for y=0,20 do nh.deltrap(x,y);end end;');return g

def wish(g,text):
    g.command('i');prior={i['key']:i['text'] for i in g.menu['items'] if i['selectable']}
    g.reply(23);g.next_input();g.reply(text);g.settle();g.command('i')
    return next(i for i in g.menu['items'] if i['selectable'] and prior.get(i['key'])!=i['text'])

def drop(g,key):g.reply(ord('d'));g.next_input();g.reply(key);g.settle()
def off(g):
    at=g.position
    for dx,dy,k in DIRS:
        c=g.cells.get((at[0]+dx,at[1]+dy),{})
        if c.get('kind')=='terrain' and c.get('terrain') in WALK:
            g.command(k)
            if g.position!=at:return at
    raise AssertionError('No safe adjacent floor')

def back(g,at):
    dx,dy=at[0]-g.position[0],at[1]-g.position[1];g.command(next(k for x,y,k in DIRS if (x,y)==(dx,dy)));assert g.position==at

def prepared():
    g=setup();item=wish(g,'Snickersnee');assert 'named Snickersnee' in item['text'],item
    drop(g,item['key']);at=off(g);c=g.cells[at]
    assert c.get('display_object')=='katana' and c.get('display_artifact')=='Snickersnee',(c,g.messages[-5:])
    return g,at,item

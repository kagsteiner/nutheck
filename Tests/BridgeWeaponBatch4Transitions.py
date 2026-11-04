"""Public appearance boundaries: pile top, memory, blindness and hallucination."""
from BridgeGameplay import Game,ROOT,DIRS,WALK
from pathlib import Path
import json,os
def setup():
 g=Game(debug=True);g.settle();control=g.root/'control.lua';control.write_text('nh.debug_flags({mongen=false,hunger=false});for x=1,79 do for y=0,20 do nh.deltrap(x,y);end end;')
 g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(control,ROOT/'Binaries/NetHack')).as_posix());g.settle();return g
def wish(g,name):
 g.command('i');prior={i['key']:i['text'] for i in g.menu['items'] if i['selectable']};g.reply(23);g.next_input();g.reply(name);g.settle();g.command('i')
 return next(i['key'] for i in g.menu['items'] if i['selectable'] and prior.get(i['key'])!=i['text'])
def drop(g,key):g.reply(ord('d'));g.next_input();g.reply(key);g.settle()
def off(g):
 at=g.position
 for dx,dy,key in DIRS:
  if g.cells.get((at[0]+dx,at[1]+dy),{}).get('terrain') in WALK:g.command(key);return at
 raise AssertionError('No floor')
report={}
for name,tile in [('silver saber',840),('broadsword',841),('two-handed sword',844)]:
 def prepared():
  for _ in range(12):
   game=setup();key=wish(game,name)
   item=next(i for i in game.menu['items'] if i['selectable'] and i['key']==key)
   if name in item['text']:return game,key
   game.close()
  raise AssertionError('Appearance was not assigned: '+name)
 checks={};g,key=prepared()
 try:
  drop(g,key);drop(g,wish(g,'dagger'));at=off(g);c=g.cells[at];assert c.get('display_object')=='dagger' and c['tile_index']!=tile,c
  dx,dy=at[0]-g.position[0],at[1]-g.position[1];g.command(next(k for x,y,k in DIRS if (x,y)==(dx,dy)))
  g.reply(ord(','));p=g.next_input();assert p['type']=='menu',p;item=next(i for i in g.menu['items'] if i['selectable'] and 'dagger' in i['text']);g.reply(str(item['index'])+':-1');g.settle();off(g)
  assert g.cells[at]['tile_index']==tile,g.cells[at];checks['pile_cover_and_uncover']=True
 finally:g.close()
 g,key=prepared()
 try:
  drop(g,key);at=off(g);assert g.cells[at]['tile_index']==tile
  key=wish(g,'uncursed blindfold');g.reply(ord('P'));g.next_input();g.reply(key);g.settle();g.command(18)
  assert '1' not in g.state['vision'] and g.cells[at]['tile_index']==tile,g.cells[at]
  root=g.root;g.close();g=None;g=Game(root,debug=True);g.settle();assert '1' not in g.state['vision'] and g.cells[at]['tile_index']==tile
  checks['blind_memory_and_restore']=True
 finally:
  if g:g.close()
 g,key=prepared()
 try:
  drop(g,key);at=off(g);key=wish(g,'uncursed potion of hallucination');g.reply(ord('q'));g.next_input();g.reply(key);g.settle();seen=[]
  for _ in range(8):g.command(18);seen.append(g.cells[at]['tile_index'])
  assert any(t!=tile for t in seen),seen;checks['hallucinated_tiles']=seen
 finally:g.close()
 report[name]=checks
report['status']='PASS';(ROOT/'Art/ObjectInterpretations/weapon-batch4-transitions.json').write_text(json.dumps(report,indent=2));print('WEAPON_BATCH4_TRANSITIONS_PASS '+json.dumps(report),flush=True)

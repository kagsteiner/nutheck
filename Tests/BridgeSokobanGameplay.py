"""Real orthogonal push, pit/hole filling, saved identity and boulder mimic display."""
from BridgeGameplay import Game,ROOT,DIRS
from pathlib import Path
from collections import deque
import json,os
def load(g,code):
 p=g.root/'control.lua';p.write_text(code);g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(p,ROOT/'Binaries/NetHack')).as_posix());g.settle()
def enter(g,level):
 g.reply(22);g.next_input();g.reply('?');g.next_input();e=next(i for i in g.menu['items'] if i['selectable'] and level in i['text']);g.reply(str(e['index']));g.settle()
def paths(g):
 todo=deque([(g.position,[])]);seen={g.position};out={}
 while todo:
  at,path=todo.popleft();out[at]=path
  for dx,dy,k in DIRS:
   n=(at[0]+dx,at[1]+dy);c=g.cells.get(n,{})
   if n not in seen and c.get('kind')=='terrain' and c.get('terrain') in ['floor','open','up','down']:
    seen.add(n);todo.append((n,path+[k]))
 return out
result=[]
for trap in ['pit','hole']:
 g=Game(debug=True)
 try:
  g.settle();enter(g,'soko4:' if trap=='pit' else 'soko3:');load(g,'nh.debug_flags({mongen=false,hunger=false});')
  reachable=paths(g);choices=[]
  for b,c in g.cells.items():
   if c.get('display_object')!='boulder':continue
   for dx,dy,k in DIRS:
    behind=(b[0]-dx,b[1]-dy);target=(b[0]+dx,b[1]+dy);t=g.cells.get(target,{})
    if behind in reachable and t.get('kind')=='terrain' and t.get('terrain')=='floor':choices.append((reachable[behind],b,target,k))
  assert choices;path,b,target,key=min(choices,key=lambda v:len(v[0]))
  for k in path:g.command(k)
  assert abs(g.position[0]-b[0])+abs(g.position[1]-b[1])==1
  load(g,f'des.trap({{type="{trap}",x={target[0]},y={target[1]},seen=true}});');g.command(6)
  assert g.cells[target].get('display_trap')==trap,(trap,target,g.cells[target],g.messages[-5:])
  total=sum(c.get('display_object')=='boulder' for c in g.cells.values());g.command(key)
  assert g.position==b,(b,g.position,g.messages[-6:])
  assert g.cells[target]['kind']=='terrain' and g.cells[target]['terrain']=='floor' and not g.cells[target].get('display_trap'),g.cells[target]
  assert sum(c.get('display_object')=='boulder' for c in g.cells.values())==total-1
  root=g.root;g.close();g=None;g=Game(root,debug=True);g.settle()
  assert g.state['in_sokoban'] and g.state['sokoban_stage']==(1 if trap=='pit' else 2) and g.cells[target]['terrain']=='floor' and not g.cells[target].get('display_trap')
  result.append(dict(trap=trap,consumed_boulder=True,filled_floor_survives_restore=True,session=str(root)))
  if trap=='pit':
   candidates=[p for p,c in g.cells.items() if c.get('kind')=='terrain' and c.get('terrain')=='floor' and max(abs(p[0]-g.position[0]),abs(p[1]-g.position[1]))>=2 and g.state['vision'][p[1]*79+p[0]]=='1']
   assert candidates;p=min(candidates,key=lambda p:abs(p[0]-g.position[0])+abs(p[1]-g.position[1]))
   load(g,f'nh.debug_flags({{mongen=true}});des.monster({{id="giant mimic",x={p[0]},y={p[1]},peaceful=1,asleep=1,appear_as="obj:boulder"}});');g.command(18)
   c=g.cells[p];assert c.get('kind')=='item' and c.get('display_object')=='boulder' and not c.get('display_monster') and not c.get('display_trap'),(c,g.messages[-6:])
   result.append(dict(unrevealed_mimic_same_public_boulder=True,glyph=c['glyph'],tile_index=c['tile_index']))
 finally:
  if g:g.close()
(ROOT/'Art/Sokoban/native-gameplay.json').write_text(json.dumps(dict(status='PASS',cases=result),indent=2));print('SOKOBAN_NATIVE_GAMEPLAY_PASS '+json.dumps(result),flush=True)

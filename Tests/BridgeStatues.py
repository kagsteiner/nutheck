"""Native statue display sex, pile top, hallucination and restore; isolated roots only."""
from BridgeGameplay import Game,DIRS,WALK,ROOT
import json
results=[]
def wish(g,text):
 g.reply(23);p=g.next_input();assert p['type']=='line';g.reply(text);g.settle()
def move_off(g):
 at=g.position
 for dx,dy,k in DIRS:
  c=g.cells.get((at[0]+dx,at[1]+dy),{})
  if c.get('terrain') in WALK and c.get('kind') not in ['monster','pet']:
   g.command(k)
   if g.position!=at:return at
 raise AssertionError('No adjacent floor')
def drop(g,word):
 g.command('i');items=[i for i in g.menu['items'] if i.get('selectable') and word in i['text'].lower()]
 if items:g.reply(ord('d'));g.next_input();g.reply(items[-1]['key']);g.settle()
 else:g.reply(27);g.settle()
for name,female in [(n,f) for n in ['plains centaur','forest centaur','mountain centaur'] for f in [False,True]]+[('goblin',False),('red dragon',False)]:
 g=Game(debug=True)
 try:
  g.settle();wish(g,'statue of a '+('female ' if female else 'male ')+name);drop(g,'statue');at=move_off(g)
  c=g.cells[at];assert c.get('display_object')=='statue' and c.get('display_statue')==name and c.get('female')==female,(name,female,c,g.messages[-8:])
  root=g.root;g.close();g=None;g=Game(root,debug=True);g.settle();c=g.cells[at]
  assert c.get('display_statue')==name and c.get('female')==female,c
  results.append(dict(creature=name,female=female,glyph=c['glyph'],restore=True,session=str(root)))
 finally:
  if g:g.close()
# A new top object must replace, rather than decorate, the statue underneath.
g=Game(debug=True)
try:
 g.settle();wish(g,'statue of a male plains centaur');drop(g,'statue')
 wish(g,'dagger');drop(g,'dagger');at=move_off(g);c=g.cells[at]
 assert c.get('display_object')=='dagger' and not c.get('display_statue'),(c,g.messages[-8:])
 results.append(dict(pile_top='dagger',statue_metadata_absent=True,session=str(g.root)))
finally:g.close()
# During hallucination native statues are displayed as random monsters, not statues.
g=Game(debug=True)
try:
 g.settle();wish(g,'statue of a male plains centaur');drop(g,'statue');at=move_off(g)
 wish(g,'uncursed potion of hallucination');g.command('i');item=next(i for i in g.menu['items'] if i.get('selectable') and 'potion' in i['text'].lower())
 g.reply(ord('q'));g.next_input();g.reply(item['key']);g.settle();g.command(18)
 c=g.cells[at];assert c['kind']=='monster' and c.get('display_monster') and not c.get('display_statue'),(c,g.messages[-8:])
 results.append(dict(hallucination_native_monster=True,statue_metadata_absent=True,session=str(g.root)))
finally:g.close()
(ROOT/'Art/CreatureInterpretations/statues-native-transitions.json').write_text(json.dumps(dict(status='PASS',results=results),indent=2))
print('BRIDGE_STATUES_PASS '+json.dumps(results),flush=True)

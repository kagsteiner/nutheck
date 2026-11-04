"""Fresh isolated Valkyrie quest save; never reads or writes the player pointer."""
from BridgeGameplay import Game,ROOT
import uuid,json,sys
stage=sys.argv[1] if len(sys.argv)>1 else 'home'
assert stage in ('home','upper','locate','lower','goal')
root=ROOT/'Saved/NetHackCaptures'/uuid.uuid4().hex
g=Game(root,debug=True)
try:
 g.settle();g.reply(22);assert g.next_input()['type']=='line';g.reply('?');assert g.next_input()['type']=='menu'
 items=g.menu['items'];quest=False;targets=[]
 for i in items:
  if not i['selectable']:
   quest='The Quest:' in i['text']
  elif quest:targets.append(i)
 if not targets:
  print(json.dumps(items));raise RuntimeError('No quest entries')
 target=next((i for i in targets if {'home':'strt','locate':'loca','goal':'goal','upper':'loca','lower':'loca'}[stage] in i['text']),None)
 if target is None:
  print(json.dumps(targets));raise RuntimeError('Requested quest destination missing')
 g.reply(str(target['index']));g.settle();assert g.state['valkyrie_quest']
 if stage in ('upper','lower'):
  # Numeric destinations within Quest are relative to Home 1.
  # Start from locate: the home level enforces quest permission on descent.
  destination=2 if stage=='upper' else 4
  g.reply(22);assert g.next_input()['type']=='line';g.reply(str(destination));g.settle()
 assert g.state['valkyrie_stage']=={'home':1,'upper':2,'locate':3,'lower':4,'goal':5}[stage]

 g.command(6)
 control=root/'preview.lua'
 control.write_text('nh.debug_flags({mongen=false,hunger=false});for x=1,79 do for y=0,20 do nh.deltrap(x,y);end end;')
 g.reply(ord('#'));assert g.next_input()['type']=='line';g.reply('wizloadlua');assert g.next_input()['type']=='line'
 import os
 g.reply(os.path.relpath(control,ROOT/'Binaries/NetHack').replace('\\','/'));g.settle()
 for _ in range(4):g.command('.')
 if '--inside' in sys.argv:
  assert stage=='locate'
  target=next(at for at,c in g.cells.items() if c.get('terrain')=='down')
  start=g.position
  g.reply(20);prompt=g.next_input()
  if prompt['type']=='menu':g.reply('');prompt=g.next_input()
  assert prompt['type']=='position'
  for key,count in [('l' if target[0]>start[0] else 'h',abs(target[0]-start[0])),('j' if target[1]>start[1] else 'k',abs(target[1]-start[1]))]:
   for _ in range(count):g.reply(ord(key));assert g.next_input()['type']=='position'
  g.reply(ord('.'));g.settle();assert g.position==target
 if '--orb' in sys.argv:
  from SnickersneeSupport import wish,drop,off
  item=wish(g,'The Orb of Fate');drop(g,item['key']);at=off(g)
  assert g.cells[at].get('display_artifact')=='The Orb of Fate'
 report=dict(session=str(root),id=root.name,stage=stage,native_stage=g.state['valkyrie_stage'])
 (root/'quest-preview.json').write_text(json.dumps(report));print(json.dumps(report),flush=True)
finally:g.close()

"""Place the three actual shuffled appearances in a disposable native room."""
from BridgeGameplay import Game,ROOT
from pathlib import Path
import uuid,os,json
def teleport(g,tx,ty):
 g.reply(20);p=g.next_input()
 while p['type']=='menu':g.reply('');p=g.next_input()
 assert p['type']=='position',p
 start=g.position
 for axis,dest,positive,negative in [(0,tx,'l','h'),(1,ty,'j','k')]:
  for _ in range(abs(dest-start[axis])):g.reply(ord(positive if dest>start[axis] else negative));assert g.next_input()['type']=='position'
 g.reply(ord('.'));g.settle();assert g.position==(tx,ty)
for attempt in range(12):
 root=ROOT/'Saved/NetHackCaptures'/uuid.uuid4().hex;g=Game(root,debug=True)
 try:
  g.settle();control=root/'control.lua';control.write_text('nh.debug_flags({mongen=false,hunger=false});for x=1,79 do for y=0,20 do nh.deltrap(x,y);end end;des.region(selection.area(1,0,79,20),"lit");')
  g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(control,ROOT/'Binaries/NetHack')).as_posix());g.settle();g.command(6)
  options=[]
  for x in range(2,77):
   for y in range(2,19):
    if all(g.cells.get((x+dx,y+dy),{}).get('terrain')=='floor' for dx in range(-1,2) for dy in range(-1,2)):options.append((x,y))
  assert options;cx,cy=min(options,key=lambda p:(p[0]-g.position[0])**2+(p[1]-g.position[1])**2)
  places=[(cx-1,cy-1),(cx+1,cy-1),(cx,cy+1)];items=[];retry=False
  for (name,tile),at in zip([('sapphire ring',976),('triangular amulet',995),('silver wand',1213)],places):
   teleport(g,*at);g.command('i');prior={x['key']:x['text'] for x in g.menu['items'] if x['selectable']}
   g.reply(23);g.next_input();g.reply(name);g.settle();g.command('i');item=next(x for x in g.menu['items'] if x['selectable'] and prior.get(x['key'])!=x['text'])
   if name not in item['text']:retry=True;break
   g.reply(ord('d'));g.next_input();g.reply(item['key']);g.settle();items.append(dict(name=name,tile=tile,position=at))
  if retry:continue
  teleport(g,cx,cy)
  for i in items:
   c=g.cells[tuple(i['position'])];assert c['kind']=='item' and c['tile_index']==i['tile'],(i,c)
  for _ in range(3):g.command('.')
  report=dict(session=str(root),hero=[cx,cy],items=items,fixture='native wished physical appearances; lighting controlled, monsters/traps disabled in isolated game')
  (ROOT/'build-appearance-batch2-fixture.json').write_text(json.dumps(report))
  (ROOT/'Art/ObjectInterpretations/appearance-batch2-fixture.json').write_text(json.dumps(report,indent=2));print('APPEARANCE_BATCH2_NATIVE_FIXTURE_PASS '+json.dumps(report),flush=True);break
 finally:g.close()
else:raise AssertionError('No seed with all three active appearances')

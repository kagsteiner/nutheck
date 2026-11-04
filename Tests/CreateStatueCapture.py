"""Visit all eight native Oracle statues in a fresh disposable capture session."""
from BridgeGameplay import Game,ROOT
from pathlib import Path
import uuid,json,os
root=ROOT/'Saved/NetHackCaptures'/uuid.uuid4().hex;g=Game(root,debug=True)
def teleport(tx,ty):
 g.reply(20);p=g.next_input()
 while p['type']=='menu':g.reply('');p=g.next_input()
 assert p['type']=='position',p
 start=g.position
 for axis,dest,positive,negative in [(0,tx,'l','h'),(1,ty,'j','k')]:
  for _ in range(abs(dest-start[axis])):g.reply(ord(positive if dest>start[axis] else negative));assert g.next_input()['type']=='position'
 g.reply(ord('.'));g.settle();assert g.position==(tx,ty),(g.position,g.messages[-5:])
try:
 g.settle();g.reply(22);assert g.next_input()['type']=='line';g.reply('?');g.next_input();entry=next(x for x in g.menu['items'] if x['selectable'] and 'oracle:' in x['text'].lower());g.reply(str(entry['index']));g.settle()
 cx,cy=g.state['oracle_x'],g.state['oracle_y'];assert cx>=0
 control=root/'control.lua';control.write_text('nh.debug_flags({hunger=false});')
 g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(control,ROOT/'Binaries/NetHack')).as_posix());g.settle();g.command(6)
 offsets=[(-5,-4),(-5,4),(5,-4),(5,4),(0,-3),(0,3),(-3,0),(3,0)];seen=[]
 for dx,dy in offsets:
  sx,sy=cx+dx,cy+dy
  tx,ty=(sx+(1 if dx<0 else -1),sy) if abs(dx)==5 else (sx+1,sy) if dx==0 else (sx,sy+1)
  teleport(tx,ty);c=g.cells[(sx,sy)]
  assert c['kind']=='item' and c.get('display_object')=='statue',c
  assert c.get('display_statue') in ['plains centaur','forest centaur','mountain centaur'],c
  assert not c.get('display_monster'),c
  seen.append(dict(position=[sx,sy],creature=c['display_statue'],female=c.get('female'),glyph=c['glyph'],tile_index=c['tile_index']))
 teleport(cx+3,cy+2)
 session=g.root;g.close();g=None;g=Game(session,debug=True);g.settle()
 for s in seen:
  c=g.cells[tuple(s['position'])];assert c.get('display_statue')==s['creature'] and c.get('female')==s['female'],(s,c)
 report=dict(session=str(root),center=[cx,cy],hero=g.position,depth=g.state['depth'],statues=seen,restore=True)
 (ROOT/'build-statues-fixture.json').write_text(json.dumps(report))
 (ROOT/'Art/CreatureInterpretations/statues-native-oracle.json').write_text(json.dumps(report,indent=2))
 print('ORACLE_EIGHT_NATIVE_STATUES_RESTORE_PASS '+json.dumps(report),flush=True)
finally:
 if g:g.close()

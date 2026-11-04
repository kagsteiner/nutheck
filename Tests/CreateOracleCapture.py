"""Real native Oracle-level capture; never touches the player pointer."""
from BridgeGameplay import Game,ROOT
from pathlib import Path
import uuid,json,os,sys
root=ROOT/'Saved/NetHackCaptures'/uuid.uuid4().hex;g=Game(root,debug=True)
try:
 g.settle();g.reply(22);assert g.next_input()['type']=='line';g.reply('?');g.next_input();target=next(x for x in g.menu['items'] if x['selectable'] and 'oracle:' in x['text'].lower());g.reply(str(target['index']));g.settle()
 cx,cy=g.state['oracle_x'],g.state['oracle_y'];assert cx>=0
 g.command(6)
 tx,ty=(cx+3,cy+2) if '--outer' in sys.argv else (cx+1,cy+1)
 g.reply(20);p=g.next_input()
 while p['type']=='menu':g.reply('');p=g.next_input()
 assert p['type']=='position',p
 start=g.position
 for axis,dest,positive,negative in [(0,tx,'l','h'),(1,ty,'j','k')]:
  for _ in range(abs(dest-start[axis])):g.reply(ord(positive if dest>start[axis] else negative));assert g.next_input()['type']=='position'
 g.reply(ord('.'));g.settle();assert g.position==(tx,ty),(g.position,g.messages[-5:])
 control=root/'control.lua';control.write_text('nh.debug_flags({hunger=false});')
 g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(control,ROOT/'Binaries/NetHack')).as_posix());g.settle()
 for _ in range(4):g.command('.')
 report=dict(session=str(root),center=[cx,cy],hero=g.position,depth=g.state['depth'])
 (ROOT/'build-oracle-fixture.json').write_text(json.dumps(report));print('ORACLE_NATIVE_FIXTURE_PASS '+json.dumps(report))
finally:g.close()

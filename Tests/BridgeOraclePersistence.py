"""Oracle death, revisit and restore: isolated native save only."""
from BridgeGameplay import Game,ROOT
from pathlib import Path
import json,shutil,uuid
fixture=json.loads((ROOT/'build-oracle-fixture.json').read_text());root=ROOT/'Saved/NetHackGameplayTests'/('oracle-death-'+uuid.uuid4().hex)
shutil.copytree(fixture['session'],root)
g=Game(root,debug=True)
try:
 g.settle();center=(g.state['oracle_x'],g.state['oracle_y']);assert center[0]>=0
 # Enter line of sight natively; the outer-room fixture does not expose her through walls.
 g.reply(20);p=g.next_input()
 while p['type']=='menu':g.reply('');p=g.next_input()
 assert p['type']=='position',p
 start=g.position
 for axis,dest,positive,negative in [(0,center[0]+1,'l','h'),(1,center[1]+1,'j','k')]:
  for _ in range(abs(dest-start[axis])):g.reply(ord(positive if dest>start[axis] else negative));assert g.next_input()['type']=='position'
 g.reply(ord('.'));g.settle()
 assert g.cells[center].get('display_monster')=='Oracle',g.cells[center]
 g.reply(ord('#'));g.next_input();g.reply('wizkill');p=g.next_input()
 while p['type']=='menu':g.reply('');p=g.next_input()
 assert p['type']=='position',p
 start=g.position
 for axis,positive,negative in [(0,'l','h'),(1,'j','k')]:
  for _ in range(abs(center[axis]-start[axis])):g.reply(ord(positive if center[axis]>start[axis] else negative));assert g.next_input()['type']=='position'
 g.reply(ord('.'));p=g.next_input()
 while p['type']=='menu':g.reply('');p=g.next_input()
 assert p['type']=='position',p
 g.reply(27);g.settle();assert g.cells[center].get('display_monster')!='Oracle'
 assert (g.state['oracle_x'],g.state['oracle_y'])==center
 depth=g.state['depth']
 g.reply(22);g.next_input();g.reply('1');g.settle();assert g.state['oracle_x']==-1
 g.reply(22);g.next_input();g.reply(str(depth));g.settle();assert (g.state['oracle_x'],g.state['oracle_y'])==center
 g.close();g=None;g=Game(root,debug=True);g.settle();assert (g.state['oracle_x'],g.state['oracle_y'])==center
 print('ORACLE_DEATH_REVISIT_RESTORE_PASS '+json.dumps({'session':str(root),'center':center,'depth':depth}))
finally:
 if g:g.close()

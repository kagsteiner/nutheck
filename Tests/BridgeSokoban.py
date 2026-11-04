"""Observe real Sokoban variants, saved branch identity and public glyph metadata."""
from BridgeGameplay import Game,ROOT
from pathlib import Path
import re,json,uuid
templates={}
for p in (ROOT/'upstream/NetHack/dat').glob('soko*-*.lua'):
 rows=re.search(r'des.map\(\[\[\n(.*?)\n\]\]\)',p.read_text(),re.S).group(1).splitlines()
 walls={(x,y) for y,row in enumerate(rows) for x,c in enumerate(row) if c in '-|'}
 w=max(x for x,y in walls)+1;h=max(y for x,y in walls)+1
 templates[p.stem]=[frozenset(((w-1-x if fx else x),(h-1-y if fy else y)) for x,y in walls) for fx in [0,1] for fy in [0,1]]
def level(g,name):
 g.reply(22);assert g.next_input()['type']=='line';g.reply('?');g.next_input()
 entry=next(x for x in g.menu['items'] if x['selectable'] and (name+':') in x['text']);g.reply(str(entry['index']));g.settle()
seen={};records=[];capture=None
for trial in range(12):
 root=ROOT/'Saved/NetHackCaptures'/uuid.uuid4().hex;g=Game(root,debug=True)
 try:
  g.settle();assert not g.state.get('in_sokoban') and g.state.get('sokoban_stage')==0
  for number in [4,3,2,1]:
   level(g,'soko'+str(number));assert g.state['in_sokoban'] and g.state['sokoban_stage']==5-number,g.state
   walls={(x,y) for (x,y),c in g.cells.items() if c.get('terrain')=='wall' and c['kind']!='unknown'}
   lx=min(x for x,y in walls);ly=min(y for x,y in walls);normalized=frozenset((x-lx,y-ly) for x,y in walls)
   matches=[name for name,variants in templates.items() if name.startswith('soko'+str(number)+'-') and normalized in variants]
   assert len(matches)==1,(number,len(walls),matches,str(root))
   variant=matches[0];boulders=[c for c in g.cells.values() if c.get('display_object')=='boulder'];traps=[c for c in g.cells.values() if c.get('display_trap') in ['pit','hole']]
   assert boulders and traps,(variant,len(boulders),len(traps))
   assert all(c['kind']=='item' and not c.get('display_monster') and not c.get('display_trap') for c in boulders)
   assert all(c['kind']=='terrain' and c['terrain']=='trap' for c in traps)
   record=dict(variant=variant,stage=g.state['sokoban_stage'],session=str(root),boulders=len(boulders),known_traps=len(traps),hero=g.position)
   seen[variant]=record;records.append(record)
   if number==4 and capture is None:
    # The actual native-generated first floor is the primary capture fixture.
    for _ in range(3):g.command('.')
    g.close();g=None;g=Game(root,debug=True);g.settle();assert g.state['in_sokoban'] and g.state['sokoban_stage']==1
    capture=dict(session=str(root),variant=variant,stage=1,hero=g.position)
    # Save this root for capture rather than later leaving it on another floor.
    break
  if len(seen)==8:break
 finally:
  if g:g.close()
# The first trial reserves its root; subsequent trials visit all four floors.
assert capture and len(seen)==8,sorted(seen)
g=Game(debug=True)
try:
 g.settle();level(g,'soko4');start=(g.state['dungeon'],g.state['depth']);g.close();root=g.root;g=None;g=Game(root,debug=True);g.settle();assert g.state['in_sokoban'] and (g.state['dungeon'],g.state['depth'])==start
 g.reply(22);g.next_input();g.reply('1');g.settle();assert not g.state['in_sokoban'] and g.state['sokoban_stage']==0
 level(g,'soko4');assert g.state['in_sokoban'] and g.state['sokoban_stage']==1
finally:
 if g:g.close()
(ROOT/'build-sokoban-fixture.json').write_text(json.dumps(capture))
(ROOT/'Art/Sokoban/native-layouts.json').write_text(json.dumps(dict(status='PASS',layouts=seen,visits=records,branch_restore_leave_return=True,capture=capture),indent=2))
print('SOKOBAN_NATIVE_LAYOUTS_PASS '+json.dumps(dict(variants=sorted(seen),capture=capture)),flush=True)

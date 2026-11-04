"""Verify native displayed identities for all six living centaur sex aliases."""
from BridgeGameplay import Game,ROOT
import json
results=[]
for name in ['plains centaur','forest centaur','mountain centaur']:
 for female in [False,True]:
  g=Game(debug=True)
  try:
   g.settle();g.reply(7);p=g.next_input();assert p['type']=='line',p
   g.reply('peaceful '+('female ' if female else 'male ')+name);g.settle()
   found=[c for c in g.cells.values() if c.get('display_monster')==name and c.get('female')==female]
   assert found,(name,female,g.messages[-8:])
   c=found[0];assert c['kind']=='monster' and not c.get('display_statue') and not c.get('display_object'),c
   results.append(dict(name=name,female=female,glyph=c['glyph'],tile_index=c['tile_index'],session=str(g.root)))
  finally:g.close()
(ROOT/'Art/CreatureInterpretations/centaurs-native-living.json').write_text(json.dumps(dict(status='PASS',forms=results),indent=2))
print('BRIDGE_CENTAURS_PASS '+json.dumps(results),flush=True)

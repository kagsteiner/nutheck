"""Shuffled physical appearance tiles, identification and restore in isolated games."""
from BridgeGameplay import Game,ROOT,DIRS,WALK
import json,os
from pathlib import Path
rows=[];unused_wand_attempts=[]
def wish(g,name):
 g.reply(23);assert g.next_input()['type']=='line';g.reply(name);g.settle()
def move_off(g):
 at=g.position
 for dx,dy,key in DIRS:
  c=g.cells.get((at[0]+dx,at[1]+dy),{})
  if c.get('terrain') in WALK and c.get('kind') not in ['monster','pet']:
   g.command(key)
   if g.position!=at:return at
 raise AssertionError('No adjacent floor')
for name,tile in [('ruby ring',977),('spherical amulet',993),('oak wand',1207)]:
 for trial in range(12):
  if sum(r['appearance']==name for r in rows)>=3 and len({r['glyph'] for r in rows if r['appearance']==name})>1:break
  g=Game(debug=True)
  try:
   g.settle();control=g.root/'control.lua';control.write_text('nh.debug_flags({mongen=false,hunger=false});for x=1,79 do for y=0,20 do nh.deltrap(x,y); end end;')
   g.reply(ord('#'));g.next_input();g.reply('wizloadlua');g.next_input();g.reply(Path(os.path.relpath(control,ROOT/'Binaries/NetHack')).as_posix());g.settle()
   g.command('i');prior={x['key']:x['text'] for x in g.menu['items'] if x['selectable']}
   g.reply(23);g.next_input();g.reply(name);g.settle();g.command('i')
   item=next(x for x in g.menu['items'] if x['selectable'] and prior.get(x['key'])!=x['text']);key=item['key'];unknown=item['text']
   if name=='oak wand' and name not in unknown:
    unused_wand_attempts.append(dict(session=str(g.root),returned=unknown));continue
   assert name in unknown,(name,unknown)
   g.reply(ord('d'));g.next_input();g.reply(key);g.settle();at=move_off(g)
   before=g.cells[at];assert before['kind']=='item' and before['tile_index']==tile,(name,before)
   assert not before.get('display_object') and not before.get('display_artifact'),before
   # Return to the object, pick it up, and let NetHack identify the inventory.
   dx,dy=at[0]-g.position[0],at[1]-g.position[1];g.command(next(k for x,y,k in DIRS if (x,y)==(dx,dy)))
   g.command(',')
   for attempt in range(5):
    g.command('i');oldkeys={x['key'] for x in g.menu['items'] if x['selectable']}
    g.reply(23);g.next_input();g.reply('blessed scroll of identify');g.settle();g.command('i');scroll=next(x for x in g.menu['items'] if x['selectable'] and x['key'] not in oldkeys)
    g.reply(ord('r'));g.next_input();g.reply(scroll['key']);g.settle(allow_pickup=True)
    g.command('i');identified=next(x for x in g.menu['items'] if x['selectable'] and x['key']==key)['text']
    if name not in identified:break
   assert name not in identified,(name,identified,g.messages[-6:])
   g.reply(ord('d'));g.next_input();g.reply(key);g.settle();at=move_off(g);after=g.cells[at]
   assert after['tile_index']==tile and after['glyph']==before['glyph'],(before,after)
   session=g.root;g.close();g=None;g=Game(session,debug=True);g.settle();restored=g.cells[at]
   assert restored['tile_index']==tile and restored['glyph']==after['glyph'],(after,restored)
   rows.append(dict(appearance=name,tile=tile,trial=trial,unknown_inventory=unknown,identified_inventory=identified,glyph=after['glyph'],session=str(session),identification_preserves_appearance=True,restore=True))
  finally:
   if g:g.close()
for name in ['ruby ring','spherical amulet','oak wand']:
 assert sum(r['appearance']==name for r in rows)>=3,(name,rows)
 assert len({r['glyph'] for r in rows if r['appearance']==name})>1,('shuffle did not vary',name,rows)
(ROOT/'Art/ObjectInterpretations/appearance-batch1-native.json').write_text(json.dumps(dict(status='PASS',cases=rows,unassigned_oak_fixture_attempts=unused_wand_attempts),indent=2))
print('APPEARANCE_BATCH1_NATIVE_PASS '+json.dumps(rows),flush=True)

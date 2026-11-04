"""Actual Snickersnee naming, restore, piles, blind/hallucinated guards and fake mimic."""
from SnickersneeSupport import *
import json
report={};g,at,item=prepared()
try:
    before=g.cells[at];report['visible_before_full_identification']=item['text']
    root=g.root;g.close();g=None;g=Game(root,debug=True);g.settle()
    assert g.cells[at].get('display_artifact')=='Snickersnee' and g.cells[at]['glyph']==before['glyph'];report['restore']=True
    back(g,at);g.command(',');key=item['key']
    # Native blessed identify scroll, not a temporary wizard inventory preview.
    for _ in range(5):
        scroll=wish(g,'blessed scroll of identify');g.reply(ord('r'));g.next_input();g.reply(scroll['key']);g.settle(allow_pickup=True)
        g.command('i');identified=next(i for i in g.menu['items'] if i['selectable'] and i['key']==key)['text']
        if 'named Snickersnee' not in identified:break
    assert 'Snickersnee' in identified and 'named Snickersnee' not in identified,identified
    drop(g,key);off(g);assert g.cells[at].get('display_artifact')=='Snickersnee';report['identification_keeps_identity']=identified
finally:
    if g:g.close()

g,at,item=prepared()
try:
    back(g,at);dagger=wish(g,'dagger');drop(g,dagger['key']);off(g)
    assert g.cells[at].get('display_object')=='dagger' and not g.cells[at].get('display_artifact'),g.cells[at]
    back(g,at);g.reply(ord(','));p=g.next_input();assert p['type']=='menu';d=next(i for i in g.menu['items'] if i['selectable'] and 'dagger' in i['text']);g.reply(str(d['index'])+':-1');g.settle();off(g)
    assert g.cells[at].get('display_artifact')=='Snickersnee';report['pile_cover_uncover']=True
    back(g,at);g.command(',');off(g)
    assert g.cells[at]['kind']=='terrain'
    load(g,f'nh.debug_flags({{mongen=true}});des.monster({{id="giant mimic",x={at[0]},y={at[1]},peaceful=1,asleep=1,appear_as="obj:katana"}});');g.command(18)
    c=g.cells[at];assert c['kind']=='item' and c.get('display_object')=='katana' and not c.get('display_artifact') and not c.get('display_monster'),(c,g.messages[-5:])
    report['fake_katana_clears_same_square_artifact_observation']=True
finally:g.close()

for mode in ['blind','hallucination']:
    g,at,item=prepared()
    try:
        i=wish(g,'uncursed blindfold' if mode=='blind' else 'uncursed potion of hallucination')
        g.reply(ord('P') if mode=='blind' else ord('q'));g.next_input();g.reply(i['key']);g.settle();g.command(18)
        assert not g.cells[at].get('display_artifact'),(mode,g.cells[at])
        if mode=='blind':assert '1' not in g.state['vision']
        report[mode+'_hides_artifact_identity']=True
    finally:g.close()
g=setup()
try:
    i=wish(g,'katana named Pretender');assert 'Pretender' in i['text'];drop(g,i['key']);at=off(g)
    assert g.cells[at].get('display_object')=='katana' and not g.cells[at].get('display_artifact');report['ordinary_player_name_does_not_qualify']=True
finally:g.close()
report['status']='PASS';(ROOT/'Art/ObjectInterpretations/snickersnee-native.json').write_text(json.dumps(report,indent=2));print('SNICKERSNEE_NATIVE_PASS '+json.dumps(report),flush=True)

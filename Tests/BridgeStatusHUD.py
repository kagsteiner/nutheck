"""Real native status fields, conditions, hunger transitions; isolated wizard root."""
from BridgeGameplay import Game,ROOT
from pathlib import Path
import json,os,uuid

class StatusGame(Game):
    def __init__(self,root):
        self.status={};self.conditions=[];self.offset=0
        super().__init__(root,debug=True)
    def next_input(self):
        prompt=super().next_input();self.trace.flush()
        with (self.root/'events.ndjson').open(encoding='utf-8') as f:
            f.seek(self.offset)
            for line in f:
                try:e=json.loads(line)
                except ValueError:continue
                if e.get('event')=='status':
                    self.status={x['name']:x for x in e['fields']};self.conditions=e['conditions']
            self.offset=f.tell()
        return prompt

root=ROOT/'Saved/NetHackGameplayTests'/('status-'+uuid.uuid4().hex);root.mkdir(parents=True)
(root/'.nethackrc').write_text('OPTIONS=number_pad:0,!tutorial,!legacy,!news,time,lit_corridor,!autopickup,!tips\nOPTIONS=role:Valkyrie,race:human,gender:female,align:lawful\nOPTIONS=showexp,showscore,weaponstatus,armorstatus,terrainstatus,showvers\n')
g=StatusGame(root)
def extended(name):
    g.reply(ord('#'));assert g.next_input()['type']=='line';g.reply(name)
def wish(text):
    g.reply(23);assert g.next_input()['type']=='line';g.reply(text);g.settle()
def wear(key,name):
    g.command('i');item=next(x for x in g.menu['items'] if x['selectable'] and name in x['text'])
    g.reply(ord(key));p=g.next_input()
    if p['type']!='command':g.reply(item['key']);g.settle()
try:
    g.settle()
    assert len(g.status)==27,g.status.keys()
    for name in ['title','strength','dexterity','constitution','intelligence','wisdom','charisma','alignment','gold','power','power-max','armor-class','experience-level','experience','time','hunger','hitpoints','hitpoints-max','dungeon-level','carrying-capacity','condition','weapon','armor','terrain','version']:
        assert g.status[name]['enabled'],name
    assert g.status['HD']['enabled'] is False
    assert int(g.status['hitpoints']['value'])==g.state['hp']
    assert int(g.status['hitpoints-max']['value'])==g.state['maxhp']
    assert 'wizard' in g.status['title']['value'].lower()
    assert '\\G' not in g.status['gold']['text']
    control=root/'control.lua';control.write_text('nh.debug_flags({mongen=false});')
    extended('wizloadlua');assert g.next_input()['type']=='line'
    g.reply(Path(os.path.relpath(control,ROOT/'Binaries/NetHack')).as_posix());g.settle()
    wish('uncursed blindfold');wear('P','blindfold');assert 'Blind' in g.conditions,g.conditions
    wear('R','blindfold');assert 'Blind' not in g.conditions,g.conditions
    hunger=set()
    for _ in range(1100):
        g.command('.');state=g.status['hunger']['value'].strip();hunger.add(state)
        if state=='Weak':break
    assert {'Hungry','Weak'}<=hunger,hunger
    for _ in range(4):
        wish('uncursed loadstone')
        if g.status['carrying-capacity']['value'].strip():break
    assert g.status['carrying-capacity']['value'].strip(),g.messages[-8:]
    # Native wizard polymorph uses its own control prompt and status reassessment.
    extended('polyself');p=g.next_input()
    if p['type']=='line':g.reply('giant ant');g.settle()
    else:
        if p['type']!='command':g.reply(27);g.settle()
    if g.state.get('hero_polymorphed'):
        assert g.status['HD']['enabled'] and not g.status['experience-level']['enabled']
        assert int(g.status['hitpoints']['value'])==g.state['hp']
    report=dict(session=str(root),fields=len(g.status),hunger_states=sorted(hunger),blind_condition_set_and_cleared=True,burden=g.status['carrying-capacity']['value'].strip(),polymorphed=g.state.get('hero_polymorphed'),hp_matches_native=True)
    (root/'verification.json').write_text(json.dumps(report,indent=2))
    print('BRIDGE_STATUS_HUD_PASS '+json.dumps(report),flush=True)
finally:g.close()

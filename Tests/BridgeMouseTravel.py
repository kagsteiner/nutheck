"""Native #travel equivalence and obstacle/threat checks, fresh wizard roots only."""
from BridgeGameplay import Game, ROOT
from pathlib import Path
import json, shutil, uuid, os

base=ROOT/'Saved/NetHackGameplayTests'/('mouse-travel-'+uuid.uuid4().hex)
base.mkdir(parents=True)

def extended(g, name):
    g.reply(ord('#'));p=g.next_input();assert p['type']=='line',p
    g.reply(name)

def fixture(threat=False):
    g=Game(base/('threat' if threat else 'obstacle'),debug=True)
    try:
        g.settle()
        script=g.root/'travel.lua'
        script.write_text('''des.reset_level();
des.level_flags("noflip");
des.level_init({style="solidfill",fg=".",lit=true});
des.teleport_region({region={10,10,10,10},region_islev=true,dir="both"});
des.finalize_level();
for x=20,24 do for y=3,17 do des.terrain(x,y,"|"); end end
'''+('des.monster({id="grid bug",x=11,y=9,peaceful=0,asleep=0});\n' if threat else ''))
        extended(g,'wizloadlua');p=g.next_input();assert p['type']=='line',p
        g.reply(Path(os.path.relpath(script, ROOT/"Binaries/NetHack")).as_posix());g.settle();g.command(6) # native wizard map
        start=g.position
        assert start==(9,10),(start,g.messages[-8:]) # native X=10 maps to UE X=9
        goal=(29,10)
        assert g.cells[goal]['terrain']=='floor'
        return g.root,start,goal
    finally:g.close()

def run(folder,target,mouse):
    g=Game(folder,debug=True)
    try:
        g.settle()
        control=g.root/'control.lua';control.write_text('nh.debug_flags({mongen=false,hunger=false});' + ('nh.debug_flags({mongen=true});des.monster({id="grid bug",x=11,y=9,peaceful=0,asleep=0});' if 'threat' in folder.name else ''))
        extended(g,'wizloadlua');p=g.next_input();assert p['type']=='line',p
        g.reply(Path(os.path.relpath(control, ROOT/'Binaries/NetHack')).as_posix());g.settle()
        turn=g.state['moves'];start=g.position
        # Invalid transport destinations must not become a key or spend a turn.
        if mouse:
            for payload in ['travel -1 10','travel 79 10','travel 10 21','travel 9 10 extra']:
                g.reply(payload);g.settle()
                assert g.position==start and g.state['moves']==turn,payload
            g.reply(f'travel {start[0]} {start[1]}');g.settle()
            assert g.position==start and g.state['moves']==turn
        else:
            pass
        if mouse:g.reply(f'travel {target[0]} {target[1]}')
        else:
            g.reply(ord('_'));p=g.next_input()
            while p['type']=='menu' and not g.menu['how']:
                g.reply('');p=g.next_input()
            assert p['type']=='position',p
            # Move only the native selection cursor, then accept with '.'.
            for axis,keyp,keym in [(0,'l','h'),(1,'j','k')]:
                for _ in range(abs(target[axis]-start[axis])):
                    g.reply(ord(keyp if target[axis]>start[axis] else keym))
                    p=g.next_input();assert p['type']=='position',p
            g.reply(ord('.'))
        g.settle()
        result=dict(position=g.position,turns=g.state['moves']-turn,hp=g.state['hp'])
        g.trace.flush()
        states=[json.loads(l) for l in (g.root/'events.ndjson').read_text(encoding='utf-8').splitlines() if l.startswith('{')]
        result['detoured']=any(e.get('event')=='state' and 19<=e['x']<=23 and (e['y']<=2 or e['y']>=18) for e in states)
        return result
    finally:g.close()

results=[]
for threat in [False,True]:
    source,start,target=fixture(threat)
    copies=[]
    for label in ['mouse','keyboard']:
        dest=base/(source.name+'-'+label);shutil.copytree(source,dest)
        config=dest/'.nethackrc';config.write_text(config.read_text().replace('OPTIONS=pettype:none\n',''))
        copies.append(dest)
    mouse=run(copies[0],target,True);keyboard=run(copies[1],target,False)
    assert mouse==keyboard,(threat,mouse,keyboard)
    if threat:assert mouse['position']!=target and mouse['turns']<20,mouse
    else:assert mouse['position']==target and mouse['detoured'],mouse
    results.append(dict(threat=threat,result=mouse))
report=dict(root=str(base),cases=results,mouse_equals_native_keyboard=True,invalid_coordinates_no_turn=True)
(base/'verification.json').write_text(json.dumps(report,indent=2))
print('BRIDGE_MOUSE_TRAVEL_PASS '+json.dumps(report),flush=True)

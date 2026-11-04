"""Native named sword over an altar, ordinary katana and uncovered altar control."""
from SnickersneeSupport import *
import uuid,json

def teleport(g,tx,ty):
    g.reply(20);p=g.next_input()
    while p['type']=='menu':g.reply('');p=g.next_input()
    assert p['type']=='position',p;start=g.position
    for axis,dest,positive,negative in [(0,tx,'l','h'),(1,ty,'j','k')]:
        for _ in range(abs(dest-start[axis])):g.reply(ord(positive if dest>start[axis] else negative));assert g.next_input()['type']=='position'
    g.reply(ord('.'));g.settle();assert g.position==(tx,ty)

def altar(g):g.reply(23);g.next_input();g.reply('lawful altar');g.settle()

for attempt in range(16):
    root=ROOT/'Saved/NetHackCaptures'/uuid.uuid4().hex;g=Game(root,debug=True)
    try:
        g.settle();load(g,'nh.debug_flags({mongen=false,hunger=false});for x=1,79 do for y=0,20 do nh.deltrap(x,y);end end;des.region(selection.area(1,0,79,20),"lit");');g.command(6)
        choices=[(x,y) for x in range(3,76) for y in range(3,18) if all(g.cells.get((x+dx,y+dy),{}).get('terrain')=='floor' for dx in range(-2,3) for dy in range(-2,3))]
        if not choices:continue
        cx,cy=min(choices,key=lambda p:(p[0]-g.position[0])**2+(p[1]-g.position[1])**2)
        named=(cx-1,cy-1);plain=(cx+1,cy-1);control=(cx+1,cy+1)
        teleport(g,*named);altar(g);teleport(g,cx,cy);assert g.cells[named]['terrain']=='altar_lawful'
        teleport(g,*named);item=wish(g,'Snickersnee');assert 'named Snickersnee' in item['text'];drop(g,item['key'])
        teleport(g,*plain);ordinary=wish(g,'katana');drop(g,ordinary['key'])
        teleport(g,*control);altar(g);teleport(g,cx,cy)
        assert g.cells[named].get('display_artifact')=='Snickersnee' and g.cells[named].get('display_object')=='katana',g.cells[named]
        assert g.cells[plain].get('display_object')=='katana' and not g.cells[plain].get('display_artifact'),g.cells[plain]
        assert g.cells[control]['terrain']=='altar_lawful'
        for _ in range(3):g.command('.')
        report=dict(session=str(root),hero=[cx,cy],named_sword=list(named),ordinary_katana=list(plain),uncovered_altar=list(control),native_name=item['text'],fixture='Actual native wishes in generated room; lighting/monsters/traps controlled only in isolated root; named sword covers an already-seen altar')
        (ROOT/'build-snickersnee-fixture.json').write_text(json.dumps(report));(ROOT/'Art/ObjectInterpretations/snickersnee-fixture.json').write_text(json.dumps(report,indent=2))
        print('SNICKERSNEE_NATIVE_FIXTURE_PASS '+json.dumps(report),flush=True);break
    finally:g.close()
else:raise AssertionError('No spacious native room found')

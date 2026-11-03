"""Create an isolated real Mines save for Unreal presentation verification."""
from BridgeGameplay import Game,ROOT
import uuid,re,json,collections,sys,os
root=ROOT/'Saved/NetHackCaptures'/uuid.uuid4().hex
g=Game(root,debug=True)
try:
    g.settle();assert not g.state.get('in_mines')
    g.reply(22);assert g.next_input()['type']=='line';g.reply('?');assert g.next_input()['type']=='menu'
    heading=next(x['text'] for x in g.menu['items'] if not x['selectable'] and x['text'].startswith('The Gnomish Mines:'))
    depth=int(re.search(r'levels (\d+)',heading)[1])
    target=next(x for x in g.menu['items'] if x['selectable'] and 'minetn:' in x['text'])
    g.reply(str(target['index']));g.settle();assert g.state['in_mines'] and g.state['mines_town']
    if '--town' not in sys.argv:
        g.reply(22);assert g.next_input()['type']=='line';g.reply(str(depth));g.settle();assert g.state['in_mines'] and not g.state['mines_town']
    g.command(6) # Native wizard map, only in this disposable fixture.
    if '--dark' not in sys.argv:
        g.reply(23);assert g.next_input()['type']=='line';g.reply('blessed wand of light');g.settle()
        g.command('i');wand=next(i for i in g.menu['items'] if i['selectable'] and 'wand' in i['text'].lower())
        g.reply(ord('z'));g.next_input();g.reply(wand['key']);g.settle()
    if '--dark' in sys.argv:
        g.reply(23);assert g.next_input()['type']=='line';g.reply('cursed scroll of light');g.settle()
        g.command('i');scroll=next(i for i in g.menu['items'] if i['selectable'] and 'scroll' in i['text'].lower())
        g.reply(ord('r'));g.next_input();g.reply(scroll['key']);g.settle()
    control=root/'control.lua';control.write_text('nh.debug_flags({mongen=false});')
    g.reply(ord('#'));assert g.next_input()['type']=='line';g.reply('wizloadlua');assert g.next_input()['type']=='line'
    g.reply(os.path.relpath(control,ROOT/'Binaries/NetHack').replace('\\','/'));g.settle()
    for _ in range(4):g.command('.')
    report=dict(session=str(root),depth=g.state['depth'],in_mines=g.state['in_mines'],mines_town=g.state['mines_town'],terrain=dict(collections.Counter(c['terrain'] for c in g.cells.values())),lit=sum(c in '13' for c in g.state['lighting']))
    (root/'mines-fixture.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
finally:g.close()

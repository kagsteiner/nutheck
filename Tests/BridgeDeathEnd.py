"""An isolated native death emits the same terminal event used by the end UI."""
from BridgeGameplay import Game
import json
g=Game(debug=True)
try:
    g.settle();g.reply(23);p=g.next_input();assert p['type']=='line'
    g.reply('wand of death');g.settle();g.command('i')
    wands=[x for x in g.menu['items'] if x['selectable'] and 'wand' in x['text'].lower()];assert len(wands)==1,wands
    wand=wands[0]
    g.reply(ord('z'));g.next_input();g.reply(wand['key']);g.next_input();g.reply(ord('.'))
    for _ in range(100):
        try:p=g.next_input()
        except RuntimeError:
            assert g.proc.poll()==0;break
        if p['type']=='yn':g.reply(ord('y'))
        elif p['type']=='menu':g.reply('-1' if g.menu['how'] else '')
        else:g.reply(32)
    else:raise AssertionError('Death did not finish')
    g.trace.flush();events=[json.loads(s) for s in (g.root/'events.ndjson').read_text(encoding='utf-8').splitlines() if s.startswith('{')]
    assert any(e.get('event')=='end' for e in events)
    assert any('die' in e.get('text','').lower() for e in events if e.get('event')=='message')
    print('BRIDGE_DEATH_END_PASS '+json.dumps(dict(session=str(g.root),terminal_event='end',exit=0)),flush=True)
finally:g.close()

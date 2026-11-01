"""Verify lighting disclosure and a real lamp in a fresh native wizard session."""
from BridgeGameplay import Game

g = Game(debug=True)

def check():
    vision, lighting = g.state['vision'], g.state['lighting']
    assert len(vision) == len(lighting) == 79 * 21
    assert set(lighting) <= set('0123')
    assert all(light == '0' for seen, light in zip(vision, lighting) if seen == '0')

try:
    g.settle()
    check()
    g.reply(23)  # Wizard wish: test session only.
    assert g.next_input()['type'] == 'line'
    g.reply('blessed oil lamp')
    g.settle()
    g.command('i')
    lamp = next(i for i in g.menu['items'] if 'lamp' in i['text'].lower())
    def apply_lamp():
        g.reply(ord('a'))
        assert g.next_input()['type'] != 'command'
        g.reply(lamp['key'])
        g.settle()
        check()
    apply_lamp()
    assert any(int(value) & 2 for value in g.state['lighting']), 'Lamp did not produce temporary light'
    apply_lamp()
    assert not any(int(value) & 2 for value in g.state['lighting']), 'Extinguished lamp still lights cells'
    for _ in range(8):
        g.command('.')
        check()
    g.reply(23)
    assert g.next_input()['type'] == 'line'
    g.reply('blindfold')
    g.settle()
    g.command('i')
    blindfold = next(i for i in g.menu['items'] if 'blindfold' in i['text'].lower())
    apply_lamp()
    g.reply(ord('P'))
    assert g.next_input()['type'] != 'command'
    g.reply(blindfold['key'])
    g.settle()
    check()
    assert '1' not in g.state['vision'], 'Blindfold did not block ordinary sight'
    assert set(g.state['lighting']) == {'0'}, 'Lighting disclosed while blind'
    print('BRIDGE_LIGHTING_PASS: masked illumination, lamp on/off, blindness; ' + str(g.root))
finally:
    g.close()


"""Real native profiles verify known own-race metadata and displayed role/sex."""
from pathlib import Path
import uuid
from BridgeGameplay import Game,ROOT
for role,sex,race,align in [('Valkyrie','female','human','lawful'),('Barbarian','male','human','neutral'),('Valkyrie','female','dwarf','lawful'),('Barbarian','male','orc','chaotic')]:
    root=ROOT/'Saved/HumanPlayerBridgeTests'/uuid.uuid4().hex;root.mkdir(parents=True)
    (root/'.nethackrc').write_text(f'OPTIONS=number_pad:0,!tutorial,!legacy,!news,time,lit_corridor,!autopickup\nOPTIONS=role:{role},race:{race},gender:{sex},align:{align}\n')
    game=Game(root)
    try:
        game.settle();assert game.state['hero_race']==race,game.state
        assert game.state['hero_polymorphed'] is False
        cell=game.cells[game.position];assert cell['display_monster']==role.lower() and cell['female']==(sex=='female'),cell
        assert all('display_monster' not in c for c in game.cells.values() if c['kind'] in ['terrain','item','unknown'])
        game.command('.')
        print(f'HUMAN_PLAYER_BRIDGE_CHECK PASS role={role} sex={sex} race={race} turn={game.state["moves"]}',flush=True)
    finally:game.close()

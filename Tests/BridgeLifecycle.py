"""Closing the UI input pipe should save, exit, and allow the same session to resume."""
from BridgeGameplay import Game

game=Game()
try:
    game.settle()
    game.command('.')
    game.command('.')
    expected=(game.position,game.state["moves"],game.state["hp"])
    folder=game.root
finally:
    game.close()
assert game.proc.returncode==0, game.proc.returncode

resumed=Game(folder)
try:
    resumed.settle()
    actual=(resumed.position,resumed.state["moves"],resumed.state["hp"])
    assert expected==actual, (expected,actual)
    resumed.command('.')
    assert resumed.state["moves"]>expected[1]
    print("BRIDGE_LIFECYCLE_PASS",expected,"resumed and advanced to",resumed.state["moves"],flush=True)
finally:
    resumed.close()
assert resumed.proc.returncode==0, resumed.proc.returncode

"""Integration test against the real NetHack executable and generated levels."""
import json
import pathlib
import queue
import subprocess
import threading
import time
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXE = ROOT / "upstream/NetHack/binary/Release/x64/NetHack.exe"
SESSION = ROOT / "Saved/NetHackTests" / uuid.uuid4().hex
for folder in (SESSION / "Local", SESSION / "Profile"):
    folder.mkdir(parents=True, exist_ok=True)

proc = subprocess.Popen(
    [str(EXE), f"--ue-root={SESSION}", "-uAdventurer", "-pValkyrie", "-rhuman", "-gfemale", "-alawful"],
    cwd=EXE.parent, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    encoding="utf-8", errors="replace", bufsize=1,
    creationflags=subprocess.CREATE_NO_WINDOW,
)
events = queue.Queue()
def read_output():
    for line in proc.stdout:
        events.put(line)
    events.put(None)
threading.Thread(target=read_output, daemon=True).start()
tiles, state, menu = {}, {}, {}
messages = []
commands = 0
first_position = None
deadline = time.monotonic() + 35
try:
    while time.monotonic() < deadline:
        try:
            line = events.get(timeout=3)
        except queue.Empty:
            print("WAIT", proc.poll(), flush=True)
            continue
        if line is None:
            raise RuntimeError(f"Backend exited early: {proc.wait(timeout=3)}")
        try:
            event = json.loads(line)
        except ValueError:
            print("RAW", line.strip(), flush=True)
            continue
        kind = event["event"]
        if kind == "tile":
            tiles[event["x"], event["y"]] = event
        elif kind == "state":
            state = event
        elif kind == "clear":
            tiles.clear()
        elif kind == "menu":
            menu = event
            print("MENU", menu["title"], [x["text"] for x in menu["items"]][:8], flush=True)
        elif kind == "message":
            messages.append(event["text"])
            print("MSG", event["text"], flush=True)
        elif kind == "input":
            typ = event["type"]
            print("INPUT", typ, event["text"], "state", {k:v for k,v in state.items() if k!="vision"}, flush=True)
            if typ == "command":
                if first_position is None:
                    first_position = state["x"], state["y"]
                commands += 1
                if commands >= 8:
                    assert len(tiles) > 10, "No map updates"
                    known = [t for t in tiles.values() if t["kind"] != "unknown" and t["terrain"] != "stone"]
                    assert 0 < len(known) < 79*21, "Exploration boundary missing"
                    assert state["moves"] > 1, "Real turns did not advance"
                    assert first_position != (state["x"],state["y"]), "Movement failed"
                    hero_tile=tiles[(state['x'],state['y'])]
                    introduction=next(m for m in messages if 'You are a ' in m)
                    displayed=hero_tile.get('display_monster','').lower()
                    aliases={'cleric':('cleric','priest','priestess'),'cave dweller':('cave dweller','caveman','cavewoman')}
                    assert displayed and any(name in introduction.lower() for name in aliases.get(displayed,(displayed,))), 'Displayed role identity missing or wrong'
                    assert hero_tile.get('female')==(' female ' in introduction), 'Displayed glyph sex did not match the selected character'
                    assert all('display_monster' not in t for t in tiles.values() if t['kind'] in ('terrain','item','unknown')), 'Monster identity leaked into non-monster appearances'
                    print("BRIDGE_SMOKE_PASS", {"turn":state["moves"],"known":len(known),"position":(state["x"],state["y"]),"initial":first_position}, flush=True)
                    break
                # Choose a known adjacent walkable glyph; the core decides whether it is legal.
                answer = str(ord('.'))
                for dx,dy,key in [(1,0,'l'),(0,1,'j'),(-1,0,'h'),(0,-1,'k')]:
                    t = tiles.get((state["x"]+dx,state["y"]+dy),{})
                    if t.get("terrain") in ("floor","open","up","down"):
                        answer = str(ord(key))
                        break
            elif typ == "menu":
                selectable = [x for x in menu.get("items",[]) if x["selectable"]]
                answer = str(selectable[0]["index"]) if selectable and menu["how"] else ""
                if "tutorial" in menu["title"].lower():
                    answer = str(next(x["index"] for x in selectable if x["text"].startswith("No,")))
            elif typ == "yn":
                answer = str(ord('y'))
            elif typ == "line":
                answer = "Adventurer"
            else:
                answer = "32"
            proc.stdin.write(f"{event['seq']}\t{answer}\n")
            proc.stdin.flush()
    else:
        raise TimeoutError("NetHack did not complete the live movement test")
finally:
    proc.stdin.close()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=3)

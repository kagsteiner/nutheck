"""Exercise the real game through the pipe API; inspect only window-port events."""
import collections
import json
import pathlib
import queue
import subprocess
import threading
import time
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXE = ROOT / "Binaries/NetHack/NetHackBridge.exe"
DIRS = [(1,0,'l'),(0,1,'j'),(-1,0,'h'),(0,-1,'k')]
WALK = {"floor", "open", "up", "down", "trap", "fountain", "sink"}

class Game:
    def __init__(self, session=None, debug=False):
        self.root = pathlib.Path(session) if session else ROOT / "Saved/NetHackGameplayTests" / uuid.uuid4().hex
        self.root.mkdir(parents=True, exist_ok=True)
        if not (self.root / ".nethackrc").exists():
            (self.root / ".nethackrc").write_text(
                "OPTIONS=number_pad:0,!tutorial,!legacy,!news,time,lit_corridor,!autopickup\n"
                "OPTIONS=role:Valkyrie,race:human,gender:female,align:lawful\n")
        if debug:
            with (self.root / ".nethackrc").open("a") as config:
                config.write("OPTIONS=pettype:none\n")
        self.proc = subprocess.Popen([str(EXE), f"--ue-root={self.root}", "-uwizard" if debug else "-uAdventurer"] + (["-D"] if debug else []),
            cwd=EXE.parent, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            encoding="utf-8", errors="replace", bufsize=1, creationflags=subprocess.CREATE_NO_WINDOW)
        self.queue = queue.Queue()
        self.cells, self.state, self.menu, self.messages = {}, {}, {}, []
        self.hostiles = set()
        self.item_locations = set()
        self.door_opened = False
        self.pending_direction = None
        self.trace = (self.root / "events.ndjson").open("w", encoding="utf-8")
        def reader():
            for line in self.proc.stdout:
                self.queue.put(line)
            self.queue.put(None)
        threading.Thread(target=reader, daemon=True).start()

    def next_input(self):
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            line = self.queue.get(timeout=10)
            if line is None:
                raise RuntimeError(f"Backend exited: {self.proc.wait(timeout=3)}")
            self.trace.write(line)
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e["event"] == "tile":
                p = e["x"],e["y"]
                old = self.cells.get(p,{})
                if old.get("terrain")=="closed" and e["terrain"] in ("open","floor"):
                    self.door_opened = True
                if e["terrain"]=="none" and e["kind"]!="unknown":
                    e["terrain"]=old.get("terrain","floor")
                self.cells[p]=e
                if e["kind"]=="monster" and p!=self.position:
                    self.hostiles.add(e["glyph"])
                if e["kind"]=="item":
                    self.item_locations.add(p)
            elif e["event"]=="clear":
                self.cells.clear()
            elif e["event"]=="state":
                self.state=e
            elif e["event"]=="message":
                self.messages.append(e["text"])
            elif e["event"]=="menu":
                self.menu=e
            elif e["event"]=="input":
                self.prompt=e
                return e
        raise TimeoutError("Input prompt was not emitted")

    @property
    def position(self):
        return self.state.get("x",-1),self.state.get("y",-1)

    def reply(self, payload):
        self.proc.stdin.write(f"{self.prompt['seq']}\t{payload}\n")
        self.proc.stdin.flush()

    def settle(self, allow_pickup=False):
        """Return at the next command prompt while servicing all intervening prompts."""
        for _ in range(50):
            e=self.next_input()
            typ=e["type"]
            if typ=="command":
                self.pending_direction=None
                return
            if typ=="yn":
                self.reply(ord('n') if self.state else ord('y'))
            elif typ=="menu":
                selectable=[x for x in self.menu["items"] if x["selectable"]]
                if not self.state:
                    self.reply(selectable[0]["index"] if selectable else "")
                elif allow_pickup and self.menu["how"]:
                    self.reply(",".join(f"{x['index']}:-1" for x in selectable))
                else:
                    self.reply("-1" if self.menu["how"] else "")
            elif typ=="line":
                self.reply("\x1b")
            else:
                self.reply(ord(self.pending_direction) if self.pending_direction else 32)
        raise RuntimeError("Prompt loop did not return to movement")

    def command(self, key, direction=None, pickup=False):
        self.pending_direction=direction
        self.reply(ord(key) if isinstance(key,str) else key)
        self.settle(pickup)

    def close(self):
        self.trace.close()
        self.proc.stdin.close()
        try:
            self.proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=3)

def explore(game, maximum=700):
    game.settle()
    initial_position=game.position
    initial_known=sum(t["kind"]!="unknown" and t["terrain"]!="stone" for t in game.cells.values())
    # Inventory is a real menu, and cancelling it must preserve the current turn.
    old_turn=game.state["moves"]
    game.command('i')
    assert game.menu.get("items"), "Inventory did not reach the menu interface"
    assert game.state["moves"]==old_turn, "Cancelling inventory spent a turn"
    game.command('#')  # Exercise line entry/cancellation.
    assert game.prompt["type"]=="command"
    visited=collections.Counter()
    attempts=collections.Counter()
    picked_up=False
    for step in range(maximum):
        here=game.position
        visited[here]+=1
        known=sum(t["kind"]!="unknown" and t["terrain"]!="stone" for t in game.cells.values())
        if game.door_opened and picked_up and game.hostiles and known>initial_known:
            assert game.position!=initial_position
            assert game.state["moves"]>old_turn
            assert known<79*21
            print("BRIDGE_GAMEPLAY_PASS",json.dumps({"turn":game.state["moves"],"initial_known":initial_known,"known":known,"opened_door":True,"picked_up":True,"hostiles":len(game.hostiles),"session":str(game.root)}),flush=True)
            return
        # Standing on a remembered item: ask the core to pick it up, then service its menu.
        cell=game.cells.get(here,{})
        if here in game.item_locations and attempts[(here,'pickup')]<2:
            attempts[(here,'pickup')]+=1
            before=len(game.messages)
            game.command(',',pickup=True)
            picked_up |= any(" - " in m or "You pick up" in m for m in game.messages[before:])
            continue
        # Open or kick a known adjacent door. Never inspect levl[] or hidden terrain.
        acted=False
        for dx,dy,key in DIRS:
            target=(here[0]+dx,here[1]+dy)
            if game.cells.get(target,{}).get("terrain")=="closed" and attempts[(target,'door')]<9:
                attempts[(target,'door')]+=1
                game.command('o' if attempts[(target,'door')]==1 else 4,direction=key)
                acted=True
                break
        if acted:
            continue
        # Search known walkable cells for an unvisited spot or unexplored boundary.
        frontier=collections.deque([(here,[])])
        seen={here}
        candidates=[]
        while frontier:
            pos,path=frontier.popleft()
            unknown=[]
            for dx,dy,key in DIRS:
                nxt=pos[0]+dx,pos[1]+dy
                if not (0<=nxt[0]<79 and 0<=nxt[1]<21):
                    continue
                terrain=game.cells.get(nxt,{}).get("terrain","none")
                if terrain in WALK and nxt not in seen and attempts[(pos,nxt)]<1:
                    seen.add(nxt)
                    frontier.append((nxt,path+[key]))
                elif terrain in ("none","stone") and attempts[(pos,nxt)]<1:
                    unknown.append((nxt,key))
            if pos!=here and visited[pos]==0:
                priority=-20 if game.cells.get(pos,{}).get("kind")=="item" else -10
                candidates.append((len(path)+priority,path,None))
            if unknown:
                nxt,key=unknown[0]
                candidates.append((len(path)+5,path+[key],(pos,nxt)))
        if not candidates:
            game.command('s')
            continue
        _,path,unknown_edge=min(candidates,key=lambda c:c[0])
        if not path:
            game.command('.')
            continue
        key=path[0]
        dx,dy=next((dx,dy) for dx,dy,k in DIRS if k==key)
        target=here[0]+dx,here[1]+dy
        game.command(key)
        if game.position==here:
            attempts[(here,target)]+=1
        if step%100==0:
            print("EXPLORING",game.state["moves"],known,"door",game.door_opened,"item",picked_up,"hostiles",len(game.hostiles),flush=True)
    raise AssertionError(f"Gameplay gates incomplete: door={game.door_opened}, item={picked_up}, hostiles={len(game.hostiles)}")

if __name__ == "__main__":
    failures=[]
    for attempt in range(3):
        game=Game()
        try:
            explore(game)
            break
        except Exception as exc:
            failures.append(str(exc))
            print("ATTEMPT",attempt+1,"FAILED",repr(exc),flush=True)
        finally:
            game.close()
    else:
        raise AssertionError(failures)

# Local NetHack bridge sources

The full upstream checkout is excluded from the project repository.
Baseline: https://github.com/NetHack/NetHack.git
Commit: 16ff59115315917b93185d026aeefea06db9b0f4 (NetHack-5.0.0_Release).

To reconstruct in a fresh checkout at that commit:

1. Apply `bridge.patch` with `git apply` from the NetHack checkout root.
2. Copy `win/ue/winue.c` from this directory to `win/ue/winue.c` in that checkout.
3. Follow UPSTREAM.md for dependencies and Windows build requirements.

Never apply this reconstruction to the played installation for testing.
The patch captures tracked upstream changes; the C source captures the new port.
When changing the bridge, refresh both copies before committing.

The additive `mouse_travel` hello capability enables `travel X Y` command replies
with zero-based presentation coordinates. The port invokes the existing native
travel command's bound key, then returns one mouse selection to that command's
`getpos` call. It does not change core pathfinding or the save format. See
[MouseTravel.md](../../Docs/MouseTravel.md).

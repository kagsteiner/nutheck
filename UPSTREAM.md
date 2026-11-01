# NetHack source baseline

The official NetHack GitHub mirror was cloned into `upstream/NetHack` for
analysis on 2026-10-30.

- Repository: https://github.com/NetHack/NetHack.git
- Release tag: `NetHack-5.0.0_Release`
- Commit: `16ff59115315917b93185d026aeefea06db9b0f4`
- Checkout: release source, with Git history retained; local packaging and
  UE window-port modifications are described below.
- Git submodules have not been initialized. The Windows build uses downloaded
  dependency releases under `lib/` instead.

The Windows download is a binary distribution. Git provides the source,
history, and upstream tracking needed for developing an Unreal adaptation.
The official source tarball is also suitable for reading a fixed release,
but does not include Git history.

Useful starting points inside `upstream/NetHack`:

- `README`: release overview and build entry points.
- `Porting` and `doc/window.txt`: platform and window interface guidance.
- `src/` and `include/`: shared game implementation and headers.
- `win/`: existing window interface implementations.
- `sys/`: platform-specific code.
- `dat/`: game data and the NetHack license (`dat/license`).

Official download information: https://nethack.org/v500/downloads.html

## Windows build

Build configuration: Visual Studio Community 2022, Release, x64. Dependencies
are Lua 5.4.8 and PDCursesMod 4.4.0, as specified by the upstream build.

From this project directory in PowerShell:

```powershell
& 'C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe' upstream/NetHack/sys/windows/vs/NetHack.sln /m /p:Configuration=Release /p:Platform=x64
```

Run this in a normal user session with access to the installed Windows SDK.
The Codex restricted build environment required elevated sandbox access for
Visual Studio SDK discovery.

Outputs:

- `upstream/NetHack/binary/Release/x64/`: console and graphical executables,
  runtime data, and recovery tool.
- `upstream/NetHack/vsbinary/`: staged playable package.
- `upstream/NetHack/vspackage/nethack-500-win-x64.zip`: game package.
- `build-nethack.log`: detailed MSBuild log.

Local fix: `sys/windows/vs/package/package.nmake` had two hard-coded references
to `nhdat370`. These now use `nhdat$(NHV)` so the 5.0.0 package includes
`nhdat500`. The file carries a dated modification notice.

## Unreal window-port modifications (2026-10-30)

- `win/ue/winue.c`: a new `ue` window port emitting NDJSON events and
  accepting sequenced input replies over standard pipes. It uses NetHack's
  own window interface and game loop; there is no alternate rules engine.
- `src/windows.c`: registers the optional port when compiled with `UEBRIDGE`.
- `sys/windows/windmain.c`: recognizes `--ue-root=<session-directory>`,
  selects the port, and preserves redirected standard handles.
- `sys/windows/windsys.c`: directs writable prefixes to the explicit session
  directory while retaining the executable directory for game data.
- `sys/windows/vs/NetHack/NetHack.vcxproj`: compiles the new port for the
  console target. Existing native tty behavior remains available when the
  bridge session argument is absent.

Modified upstream files carry dated notices. The Unreal module launches
the staged `Binaries/NetHack/NetHackBridge.exe` child process. NetHack's
license remains in `dat/license` and is staged beside the helper.
The game rules and level-generation code are unchanged.

Verified on 2026-10-30: the full solution and packaging completed with exit
code 0 (1210 compiler warnings, zero errors). The staged `NetHack.exe
--version` returned Windows NetHack 5.0.0 (x64), exit code 0. The game ZIP
contains both executables and `nhdat500`; the built `dlb.exe tf nhdat` tool
successfully listed 149 entries in that data archive. Interactive gameplay
has not been tested.

Dependency downloads (SHA-256, recorded for reproducibility):

- https://www.lua.org/ftp/lua-5.4.8.tar.gz
  `4f18ddae154e793e46eeab727c59ef1c0c0c2b744e7b94219710d76f530629ae`
- https://github.com/Bill-Gray/PDCursesMod/archive/refs/tags/v4.4.0.zip
  `3af105a31568dc4a5be7ac2105d8d98eeb10f5abe035f748d199f3c38aaa84d2`


2026-10-31 object presentation addition: `win/ue/winue.c` emits optional
`display_object` metadata for displayed `LARGE_BOX`, `CHEST` and `GOLD_PIECE`
glyphs only. No floor-object query, hidden state, contents, quantity, locks,
traps or gameplay rules were added. Native wish/drop/reveal and bridge smoke
verification passed; see `Docs/ObjectBatch1.md`.


2026-10-31 tile fallback: console bridge project enables `TILES_IN_GLYPHMAP`,
compiles native generated `src/tile.c`, and depends on the native tilemap tool.
`win/ue/winue.c` exports foreground `glyph_info.gm.tileidx` as `tile_index`.
NetHack's existing tile shuffle/restore logic supplies actual displayed object
appearances. No gameplay rules or save formats were changed. See `Docs/TileFallback.md`.

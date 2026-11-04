# Valkyrie quest: first scenery pass

Implemented 2026-11-04. The actual Val-strt/Val-fila/Val-loca/Val-filb/Val-goal definitions drive the home, upper ice fields, valley, lower lava fields and fortress treatments. Native state reports role-specific quest stage; tile glyphs report displayed ice without inspecting hidden terrain. No save structure or gameplay rules change.

The sanctuary retains dressed masonry with a bronze collar and snow cap. Ice uses a world-space cellular fracture field; cold paths, dark basalt, blue water and slowly moving lava seams have separate materials. Lava has low local light only on visible permanently lit terrain; remembered lava has no emission. Native layouts, stairs, doors and drawbridge mechanics remain intact. Foregrounds and the hero hide special background surfaces under the existing topmost rule.

This is a reviewable first pass. Elaborate Norse carvings, custom drawbridge models, steam/embers, hill silhouettes and bespoke Norn/Surtur models are further art work; they are not included in this pass.

## Isolated interactive previews

Run from the project directory:

```powershell
.\Scripts\PreviewValkyrieQuest.ps1 -Stage home
.\Scripts\PreviewValkyrieQuest.ps1 -Stage upper
.\Scripts\PreviewValkyrieQuest.ps1 -Stage locate
.\Scripts\PreviewValkyrieQuest.ps1 -Stage lower
.\Scripts\PreviewValkyrieQuest.ps1 -Stage goal
.\Scripts\PreviewValkyrieQuest.ps1 -Stage home -Orb
```

Every invocation creates a new female human Valkyrie wizard in Saved/NetHackCaptures/<new GUID>. It never reads or changes Saved/NetHack/LastSession.txt. The real native quest is generated, then mapped; existing monsters and traps are removed and monster generation/hunger disabled solely in this disposable preview. The Orb option wishes for the real artifact, drops it and steps away so its observed model can be reviewed. Wizard teleports (Ctrl+V then ?) remain available; normal quest leader permission still gates descent from home, so use the preset launcher to inspect later stages. Lava and water remain hazardous; the preview is not an invulnerability mode. Home toggles first person, PgUp/PgDown zoom, F7 labels, F9 display style.

Add -Capture for automated hidden rendering and verification; add -Orb for a close view of the artifact. Screenshots are stored under Docs/Images/ValkyrieQuest. Art assets can be regenerated with Scripts/BuildValkyrieAssets.py in Unreal; the Orb source/export/preview generator is Scripts/CreateOrbOfFate.py in Blender.

## Orb of Fate

Art/ObjectInterpretations/OrbOfFate.blend and orb_of_fate.fbx contain a blue crystal sphere, three interwoven silver rings, gold hour markers and an inset pale constellation. The displayed known name selects /Game/OrbOfFate/Meshes/SM_orb_of_fate; ordinary or falsely named crystal balls retain the existing fallback. The model hovers above the floor and has non-emissive memory materials.

Tests/BridgeOrbOfFate.py exercises real native naming before identification, identification, save/restore, pile cover/uncover, blindness, hallucination, fake mimic appearance and ordinary player naming. VALKYRIE_QUEST_CHECK checks actual ice/lava instance counts in both F9 styles, unchanged turn/sequence, Orb bounds and memory/fallback, and topmost surface suppression.

Verified player snapshots were created before bridge work; the initial archive is Backups/NetHackSaves/20261104T132521.463688Z.zip. All game testing uses fresh isolated roots. Player saves were not launched, resumed or modified.

## Validation results

Development Editor and native bridge builds succeeded. All five fresh quest presets passed VALKYRIE_QUEST_CHECK, NETHACK_LIVE_CHECK and DEFAULT_TILES_CHECK. A separate native Orb study also passed; its in-game close view and the home, valley and fortress images were visually inspected. The existing Snickersnee native regression passed. More detailed art remains pending as listed above.

Human review correction: locate's displayed solid stone now renders as tall rough basalt instead of an omitted black void. Only known terrain stone is raised; unknown tiles and foreground-covered terrain remain suppressed. Cave instances use separate component-owned geometry and do not alter the Mines meshes. Verification checks the rock count and raised transforms in both display styles.

## Moonlit outdoor valley

The home and locate levels are now presented as open night landscapes with the known rock boundary forming a basalt ridge. A large pale cratered moon and a fixed procedural star field sit above it. Cool directional moonlight casts soft shadows on currently visible, natively lit scenery, with blue ambient light for readability. Lava pools provide the only warm accent lights, with slow intensity variation and up to four shadow-casting sources. The former warm fill grid and local blue entrance lamps are removed.

The sky is a separate camera-centred component, excluded from map framing, collision, ray tracing and shadow casting. It and the moonlight are disabled outside home and locate; the usual ambient settings are restored. The overhead view retains the map presentation; use Home and look up in first person to see the moon above the ridge. The native map, portal/stairs, movement and visibility rules are unchanged.

Moonlight and lava lights use lighting channel 2. Only currently visible, permanently natively lit quest scenery receives that channel; remembered and unlit batches do not. Lava source placement uses topmost presented terrain, and invisible, unlit, foreground-covered or unknown lava cannot produce an accent source. Ordinary dungeon floor rendering is suppressed on quest stages, fixing an accidental overlap with the dedicated quest surfaces.

```powershell
.\Scripts\PreviewValkyrieQuest.ps1 -Stage locate -Inside
```

This creates a fresh disposable wizard preview and teleports to the known down staircase; press Home for the sky view. Add `-Capture -Eye` for an automated first-person image at Images/ValkyrieQuest/locate-moon-eye.png; `-Capture` alone produces the room-scale overhead image. Player saves and the last-played pointer are not used.

The moon/stars material generator is Scripts/CreateValkyrieSky.py, also included by Scripts/BuildValkyrieAssets.py. No external sky textures are needed. Tests retain source suppression and receiver-channel checks, and check that sky/moon disable on other stages and outside the quest.

Moonlit pass validation: Development Editor build succeeded; isolated locate first-person and overhead checks, sky/moon lifecycle and source/channel checks, and the home-stage regression all passed. Both night views were visually inspected. No native backend or player save was modified for this lighting replacement.


The first quest level shares the same moon, star field, cool directional lighting and warm lava accents as locate. Its sanctuary architecture and snow caps are retained. Use `.\Scripts\PreviewValkyrieQuest.ps1 -Stage home` and press Home for first person. Shared stage selection also controls lava flicker and lit receiver batches; other quest stages keep their own presentation. The home verification restores its original stage after synthetic lighting tests.

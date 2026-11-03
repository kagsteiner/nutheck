# Game vision

User direction, updated 2026-10-31. This supersedes older plans for animation
or animation-dependent asset completion.

nUthEck stays NetHack at its core: the same turn-based tactical game, with
graphics that meet today's standards. NetHack remains authoritative for rules,
turns, combat, movement, perception, item identity and outcomes. Presentation
must preserve the player's available information, including remembered terrain,
disguises and unidentified appearances.

## Beautiful objects and rewarding loot (2026-11-02)

Weapons, armor, jewelry, wands, consumables and tools should be beautiful and
distinctive. Allow creative interpretation of blade profiles, fittings,
craftsmanship, ornament and materials beyond literal tiny-tile reconstruction,
while retaining recognizable physical type and a coherent visual language.
Meaningful item differences matter; do not make every sword a recolour of one
generic mesh. Ordinary loot deserves design attention alongside artifacts.

Use a shallow category/visual-family organization with material and cultural
facets. Preserve native appearance shuffling and indistinguishable items; never
reveal unknown effects, enchantment, curse, artifact identity or value through
ornament or invented rarity colours. Identification does not itself transform
an object's physical design. See [ObjectArtDirection.md](ObjectArtDirection.md)
and [object-backlog.md](../object-backlog.md) for source inventory and future work.

## Static presentation

No character or object animation is planned: no idle, walking, attack, hit,
death, casting or chest-opening sequences. Static poses and direct board-state
updates are the intended finished presentation. Rigs, skinning and animation
are not production-readiness requirements. Existing camera navigation is a
viewing control; this update does not request changes to it.

Modern visual quality comes from anatomy, silhouettes, materials, textures,
lighting, environmental detail and clear composition. Prioritise tactical
readability at normal play distance, with polished detail when viewed closely.
Static assets still need finishing and performance review.

## Possible effects

Brief action effects may be considered, especially a wand of lightning.
This is a possibility, not a commitment to an effects system. Any effects
must follow NetHack's displayed events and preserve turn/input behaviour,
tactical readability and information boundaries. They must not introduce
timing-dependent decisions or require animated characters.

## Current environment reference

The user's latest wall/floor reference is the left, Carved stone panel:
desaturated, tactile, timeworn limestone with matte surfaces. The generated
textures and their prompts are recorded in
[WeatheredStone/Generation.md](../Art/WeatheredStone/Generation.md).
Earlier painted-miniature studies remain historical references; existing
creature-specific palette, anatomy and static-pose decisions remain applicable.

## Player saves

This is now the user's actual NetHack installation. Saves must be preserved,
backed up before save-affecting development/backend changes, and recovered from
verified staged copies if needed. Earlier permission to reset development saves
is revoked. Tests use isolated sessions; do not force-stop or test against a
played session. See [SaveProtection.md](SaveProtection.md) and root `AGENTS.md`.

## Overhead wall/floor readability (2026-11-01)

Keep high walls in overview and first person: the user likes their enclosed,
slightly claustrophobic dungeon feeling. Do not lower/fade/cut away walls to
solve doorway visibility. The selected first adjustment is darker floor tint,
preserving the existing texture and lighting. See [FloorContrast.md](FloorContrast.md).

The darker floors were accepted on 2026-11-01. Doorways now use a fixed timber
frame and a side-hinged leaf, leaving the opening's centre clear when open.
See [DoorFrames.md](DoorFrames.md).

## Gameplay status visibility (2026-11-02)

All native status information matters during play. Preserve the complete native
status field set and active conditions as graphics evolve. Current/max HP must
remain prominent, with yellow/red low-health cues, and hunger must always be
visible. Do not reduce the display to a selected HP/AC/level subset.
See [StatusHUD.md](StatusHUD.md) for the current implementation and evidence.

# Game vision

User direction, updated 2026-10-31. This supersedes older plans for animation
or animation-dependent asset completion.

nUthEck stays NetHack at its core: the same turn-based tactical game, with
graphics that meet today's standards. NetHack remains authoritative for rules,
turns, combat, movement, perception, item identity and outcomes. Presentation
must preserve the player's available information, including remembered terrain,
disguises and unidentified appearances.

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

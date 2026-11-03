# Candle and Mine torch flicker

2026-11-02: increased the previously subtle light variation from 4%/6.5% to
bounded 16% candle / 20% torch variation. Three spatially phased sine components
produce less regular motion without gameplay RNG. Average light intensity,
colour, placement, visibility rules and shadow settings remain unchanged.
Both candle and Mine torch flame instances now gently stretch and narrow.
Presentation time drives this while the native game waits for input.

Unreal Editor Development compilation passes (`build-flame-flicker-unreal.log`).
The effect has not been visually assessed in a running game in this change.
No game was launched and no player saves or native backend files were changed.

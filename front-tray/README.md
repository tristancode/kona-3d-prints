# Kona 2025 front console organiser (v6)

Tray for the strip of floor between the cupholders and the drive-mode panel, 13 mm tall throughout. It is 159.6 mm long at the top on the panel side and 157.3 mm at the floor (both ends taper 5°). The right end is angled in plan, 5 mm shorter on the cupholder side. The small bin at the left is 27.5 mm wide and sits in the 31 mm slot. The lip balm section is only 18.9 mm wide, and its trough walls are the outer walls joining the bin to the fob pocket. Only the key fob pocket is the full 44 mm width.

## Changes from v5
- The finger space beside the trough is gone. The trough's side walls are now the tray's outer walls, so the balm section is 18.9 mm wide and there is a gap to the panel instead.
- The trough's right end wall and the fob pocket's left wall are now one shared 1.6 mm wall, so it prints as one continuous wall. The bin grows to 20.6 mm.

## Changes from v4 (from Charlimit's second markup)
- The right end is angled in plan: full length on the panel side and 5 mm shorter on the cupholder side (RIGHT_END_SKEW).
- The lip balm trough moved to the cupholder side, so there is 7 mm of finger space between it and the panel side.
- The wide strip beside the trough is gone. The tray is only 27.5 mm wide from the left end to the fob pocket, which saves filament.
- The end taper is reduced to 5° (END_TAPER_LEFT_DEG, END_TAPER_RIGHT_DEG).
- The fob pocket is 64 mm long on the panel side and 59 mm on the cupholder side, so the 55 mm fob still fits after the angled end. The small bin shrinks to 19 mm to make room.

## Changes from v3 (from Charlimit's drawing)
- Both end faces taper 10° from vertical, so the tray is 2.3 mm shorter at the floor at each end (END_TAPER_LEFT_DEG, END_TAPER_RIGHT_DEG). This is so it fits the sloped ends of the space.
- The key fob floor is flat again (FOB_TILT_DEG = 0).
- The grip notch now cuts through both sides of the lip balm trough, including the panel-side wall.

## Changes from v2 (after the second test print)
- The narrow section is 2 mm narrower: 27.5 mm, with 1.75 mm clearance per side in the 31 mm slot (CLEAR_SLOT).
- 2 mm shorter overall: 159.6 mm (OVERALL_L). The feedback said "overall width too long"; this was read as the length, because the width is set by the fob pocket and the cupholder side of the strip is open floor.
- The lip balm sits in an open half-cylinder trough with straight vertical sides up to the top and closed ends. There is no snap any more, because the curved-in edges stopped the tube going in.
- The trough is pushed against the drive-mode-panel side. The rest of the width beside it is open floor, about 22 mm, for fingers, and there is a 22 mm grip notch in its finger-side wall.
- The key fob pocket floor tilts 6 degrees down towards the right-hand end (FOB_TILT_DEG, 0 = flat).

## Changes from v1 (after the test print)
- Overall length cut from 185.3 to 161.6 mm (OVERALL_L = CALIPER_L + 5).
- Height dropped from 20 to 13 mm, which is as low as the lip balm snap allows (the cradle top is 12.6 mm). The left section is now the same height as the rest.
- The finger well is removed. The lip balm cradle now starts inside the narrow section, and the space left over at the far end is a small 27 mm bin.
- The half-pencil lift nub is now on the inside of the key fob pocket's outer long wall. It protrudes 3.5 mm, leaving the pocket 37.3 mm wide at the nub, so the 33 mm fob still fits. The finger scoop is removed.

## Measurements
- Narrow slot: 31.0 x 39.8 mm (calipers). The narrow section is flush with the drive-mode-panel side, which fitted in v1.
- Strip length: 156.6 mm (calipers). The user asked for the tray to be 5 mm longer than this.
- Width: 44 mm, which fitted in v1.
- Lip balm: Burt's Bees tube, 15.3 x 68 mm. Fob: 55 x 33 mm.

## Layout (left to right, drive-mode panel side at the top)
- Small bin in the narrow section.
- Lip balm trough lying lengthways against the cupholder side: 15.7 mm wide, half-cylinder bottom, straight sides, closed ends, and a grip notch through both sides. Its side walls are the outer walls.
- Key fob pocket, 64 / 59 x 40.8 mm (angled right end), with the lift nub on the cupholder-side wall.

## Print (Bambu Lab)
PLA or PETG (ASA for hot cars), 0.2 mm layers, 3 walls, 15% gyroid, no supports, flat side down.

## Tuning
Edit the top of kona_front_organiser.py, run `python3 kona_front_organiser.py` (needs cadquery and numpy-stl), then run `python3 render_front.py` to redraw the pictures.
- Length: OVERALL_L. Narrow section fit: CLEAR_SLOT and TONGUE_OFFSET. Width: BODY_W.
- Nub: RIDGE_D (size) and RIDGE_L (length). End taper: END_TAPER_LEFT_DEG / END_TAPER_RIGHT_DEG. Right end angle: RIGHT_END_SKEW.

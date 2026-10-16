# Kona 2025 front console organiser (v3)

Tray for the strip of floor between the cupholders and the drive-mode panel. It is 159.6 mm long overall and 13 mm tall throughout. The wide section is 121.3 x 44 mm. The narrow section on the left is 38.3 x 27.5 mm and sits in the 31 mm slot so the tray can't slide or twist.

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
- Lip balm trough lying lengthways against the panel side: 15.7 mm wide, half-cylinder bottom, straight sides, closed ends, and open finger space beside it.
- Key fob pocket, 58 x 40.8 mm, with straight sides, the lift nub, and a floor tilted towards the right end.

## Print (Bambu Lab)
PLA or PETG (ASA for hot cars), 0.2 mm layers, 3 walls, 15% gyroid, no supports, flat side down.

## Tuning
Edit the top of kona_front_organiser.py, run `python3 kona_front_organiser.py` (needs cadquery and numpy-stl), then run `python3 render_front.py` to redraw the pictures.
- Length: OVERALL_L. Narrow section fit: CLEAR_SLOT and TONGUE_OFFSET. Width: BODY_W.
- Nub: RIDGE_D (size) and RIDGE_L (length). Fob floor tilt: FOB_TILT_DEG.

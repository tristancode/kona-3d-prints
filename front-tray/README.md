# Kona 2025 front console organiser

Narrow tray for the strip of floor between the cupholders and the drive-mode panel. Main body 147 x 44 x 20 mm, plus a 38.3 x 29.5 x 10 mm locating tongue on the left that drops into the narrow slot so the tray can't slide or twist. Overall 185.3 mm long.

## Measurements
Read from the photos:
- Narrow slot on the left: 31.0 mm across and 39.8 mm along (caliper readings).
- Main floor length ~150 mm, from the mouth of the narrow slot to where the tape bends over the far edge.

Inferred / assumed (check these first):
- Main floor width: not measured. The body is 44 mm wide, the minimum for the 40 mm fob pocket plus walls (BODY_W).
- The narrow slot is at the same floor level as the main strip, and flush with the drive-mode-panel side (TONGUE_OFFSET).
- Lip balm: Burt's Bees tube 15.3 x 68 mm. Fob: 55 x 33 mm.

## Layout (left to right, drive-mode panel side at the top)
- Locating tongue, hollow, 0.75 mm clearance per side in the 31 mm slot (CLEAR_SLOT).
- 12.8 mm finger well with a half-pencil (half-hexagon) lift ridge on the cradle end, so you can hook a finger and lift the tongue end out.
- One snap-in lip balm cradle lying lengthways: 13.8 mm opening over a 15.7 mm channel, closed ends, 22 mm grip notch in the middle.
- Key fob pocket 58 x 40.8 mm with straight sides and a finger scoop on the outer wall.

## Print (Bambu Lab)
PLA or PETG (ASA for hot cars), 0.2 mm layers, 3 walls, 15% gyroid, no supports, flat side down.

## Tuning
Edit the top of kona_front_organiser.py, run `python3 kona_front_organiser.py` (needs cadquery, numpy-stl), then `python3 render_front.py` for the pictures.
- Tongue too tight or loose: CLEAR_SLOT. Tongue is not flush with the panel side: TONGUE_OFFSET.
- Strip is wider than 44 mm: raise BODY_W (the fob pocket widens with it).
- Body too long or short: FLOOR_L.

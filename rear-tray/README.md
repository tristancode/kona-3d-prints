# Kona 2025 console organiser

Low tray (187 x 123 x 20 mm) that sits on the grey floor insert of the centre-console bin.

## Measurements used
Read from the tape photos:
- Floor insert along the car: ~190 mm
- Floor insert across the car: ~130 mm (about 120 mm at the narrower end by the rubber mat)

Inferred / assumed:
- Treated the floor as a rectangle. The walls slope outwards above it, so a 20 mm tray clears them.
- Burt's Bees tube: 15.3 mm dia x 68 mm long (standard 4.25 g tube).
- Clearance: 1.5 mm each side lengthwise, and 3.5 mm each side across the car to allow for the 12 cm narrow end.

## Layout
- Two snap-in lip balm cradles end to end along the wide (187 mm) front edge. Put that edge towards the front of the car. The top opening is 13.8 mm, narrower than the 15.7 mm channel, so the tube clicks in and can't roll. Closed ends stop it sliding. Use the finger notch in the middle to pull it out.
- A small key/coin pocket at the end of the cradle strip.
- One main bay (~110 mm) for a phone or wallet, plus one side bay (~70 mm) for cards and cables.
- Finger scoops in both short ends so you can lift the tray out.

## Print settings (Bambu Lab, any bed)
- PLA or PETG. PETG is better if the car sits in the sun, and ASA is best for hot climates.
- 0.4 mm nozzle, 0.2 mm layers, 3 walls, 15% gyroid infill, no supports, flat side down.
- Estimated ~45-55 g and ~2.5 h (check your slicer's figure).
- Optional: stick felt or rubber pads under the corners to stop it rattling.

## Tuning (edit the top of kona_organiser.py, then run `python3 kona_organiser.py`, which needs CadQuery)
- Tray doesn't drop in: lower FLOOR_L / FLOOR_W. If it slides around, raise them.
- Balm too tight to click in: raise SNAP_GAP to 14.2. Too loose: lower it to 13.4, or lower BALM_FIT.
- BALM_COUNT sets the number of cradles. HEIGHT sets the wall height.

# Kona 2025 console organiser

Low tapered tray (187 mm long, 118.5 mm wide at the back widening to 133 mm at the front, 20 mm tall) that sits on the grey floor insert of the centre-console bin.

## Measurements used
From the user: the floor is 12 cm wide for the back ~12 cm, then tapers out to 13.5 cm at the front.
From the tape photos: the floor is ~19 cm long.
Clearance: 1.5 mm at each end, and only 0.75 mm per side so the taper locks the tray in place.
Assumed: the Burt's Bees tube is 15.3 mm dia x 68 mm long (standard 4.25 g tube).

## Layout
- Two snap-in lip balm cradles side by side across the front short end (the end circled in the user's markup), each lying parallel to the front wall. The top opening is 13.8 mm, narrower than the 15.7 mm channel, so the tube clicks in and can't roll. Closed ends stop it sliding. Use the finger notch in the middle to pull it out.
- A 24 mm U-shaped finger notch in the wall behind the cradles, lined up with their grip notches, so you can reach in from the main bay and pinch a balm out (BACK_NOTCH_W).
- One half-pencil (half-hexagon) lift ridge on the back of the wall behind the cradles, next to the finger notch on the side nearer the middle of the tray. It is 22 mm long and sticks out 4 mm, so you can hook a finger under it and lift the tray (RIDGE_*). The underside is a 60° slope, so it prints without supports.
- A small key/coin pocket beside the cradles at the front.
- One large bay (~148 x 120 mm) behind them, big enough for a phone or wallet.
- Finger scoops in both short ends so you can lift the tray out.

## Print settings (Bambu Lab, any bed)
- PLA or PETG. PETG is better if the car sits in the sun, and ASA is best for hot climates.
- 0.4 mm nozzle, 0.2 mm layers, 3 walls, 15% gyroid infill, no supports, flat side down.
- Estimated ~45-55 g and ~2.5 h (check your slicer's figure).
- Optional: stick felt or rubber pads under the corners to stop it rattling.

## Tuning (edit the top of kona_organiser.py, then run `python3 kona_organiser.py`, which needs CadQuery)
- Tray doesn't drop in: raise CLEAR_SIDE / CLEAR_END. Adjust the shape with FLOOR_W_BACK, FLOOR_W_FRONT and TAPER_START.
- Balm too tight to click in: raise SNAP_GAP to 14.2. Too loose: lower it to 13.4, or lower BALM_FIT.
- BALM_COUNT sets the number of cradles. HEIGHT sets the wall height.

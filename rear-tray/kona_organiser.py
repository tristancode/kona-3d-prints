"""
Parametric centre-console organiser tray for a 2025 Hyundai Kona.
Run:  python3 kona_organiser.py   -> writes kona_organiser.stl / .step next to this file.

Coordinates: X = along the car (+X is the front), Y = across the car, Z = up.
All dimensions in mm. Print flat, open side up, no supports.
"""
import math, os
import cadquery as cq

# ---- Console bin floor (tape photos + the user's measurements) ----
FLOOR_L = 190.0          # back to front
FLOOR_W_BACK = 120.0     # constant width over the back section
FLOOR_W_FRONT = 135.0    # width at the front edge
TAPER_START = 120.0      # distance from the back where the taper begins
CLEAR_END = 1.5          # gap per end (front/back)
CLEAR_SIDE = 0.75        # gap per side; kept tight so the taper stops it shifting

# ---- Tray ----
HEIGHT = 20.0        # overall wall height (low profile)
FLOOR_T = 1.0        # base thickness (5 layers @ 0.2)
WALL_T = 1.6         # outer walls (4 lines @ 0.4 nozzle)
DIV_T = 1.2          # internal dividers (3 lines)
CORNER_R = 8.0       # outer corner radius

# ---- Lip balm cradle (Burt's Bees tube ~15.3 dia x 68 long) ----
BALM_D = 15.3
BALM_L = 68.0
BALM_FIT = 0.4       # diametral clearance -> snug, no rattle
BALM_AXIAL = 0.6     # end-to-end clearance
SNAP_GAP = 13.8      # width of the top opening; < channel dia so the tube clicks in
BALM_COUNT = 2       # cradles side by side at the front, parallel to the front wall
CRADLE_WALL = 1.6
GRIP_W = 22.0        # finger notch in the middle of each cradle
BACK_NOTCH_W = 24.0  # finger notch in the wall behind the cradles

# ---- Lift ridges (half-pencil bumps on the back of the cradle divider) ----
RIDGE_D = 8.0        # pencil size across the corners (protrudes RIDGE_D/2 = 4 mm)
RIDGE_L = 22.0       # length of each ridge
RIDGE_GAP = 4.0      # gap between the finger notch and each ridge
RIDGE_TOP_GAP = 1.5  # gap below the top of the divider
END_GAP = 6.0        # gap between the side wall and the channel ends (clears the corner)

# ---- Derived ----
ch_d = BALM_D + BALM_FIT
ch_r = ch_d / 2
ch_len = BALM_L + BALM_AXIAL
zc = FLOOR_T + ch_r                                     # channel axis height
cradle_top = zc + math.sqrt(ch_r**2 - (SNAP_GAP / 2) ** 2)

TRAY_L = FLOOR_L - 2 * CLEAR_END
xb, xf = -TRAY_L / 2, TRAY_L / 2                         # back / front faces
x_taper = -FLOOR_L / 2 + TAPER_START


def half_w(x):
    """Tray outer half-width at position x."""
    if x <= x_taper:
        w = FLOOR_W_BACK
    else:
        w = FLOOR_W_BACK + (FLOOR_W_FRONT - FLOOR_W_BACK) * (x - x_taper) / (FLOOR_L / 2 - x_taper)
    return w / 2 - CLEAR_SIDE


def outline(inset=0.0):
    hb, hf, ht = half_w(xb) - inset, half_w(xf) - inset, half_w(x_taper) - inset
    pts = [(xb + inset, -hb), (x_taper, -ht), (xf - inset, -hf),
           (xf - inset, hf), (x_taper, ht), (xb + inset, hb)]
    return cq.Workplane("XY").polyline(pts).close()


def build():
    envelope = outline().extrude(HEIGHT).edges("|Z").fillet(CORNER_R)
    cavity = (outline(WALL_T).extrude(HEIGHT).edges("|Z").fillet(CORNER_R - WALL_T)
              .translate((0, 0, FLOOR_T)))
    tray = envelope.cut(cavity)

    # Lip-balm cradles at the front, axis across the car (Y), rows stacked back from the front wall.
    ixf = xf - WALL_T
    pitch = ch_d + CRADLE_WALL
    zone_d = BALM_COUNT * pitch
    zone_x0 = ixf - zone_d                              # back edge of the cradle zone
    iy0 = -half_w(zone_x0) + WALL_T                     # narrowest inner wall within the zone
    cy = iy0 + END_GAP + ch_len / 2
    y_end = cy + ch_len / 2                             # far end of the channels
    block = (cq.Workplane("XY").center((zone_x0 + xf) / 2, (-half_w(xf) - 1 + y_end + CRADLE_WALL) / 2)
             .rect(xf - zone_x0, y_end + CRADLE_WALL + half_w(xf) + 1).extrude(cradle_top))
    tray = tray.union(block.intersect(envelope))
    for i in range(BALM_COUNT):
        bcx = ixf - i * pitch - ch_r
        chan = (cq.Workplane("XZ").workplane(offset=-(cy - ch_len / 2))
                .center(bcx, zc).circle(ch_r).extrude(-ch_len))
        slot = (cq.Workplane("XY").workplane(offset=zc)
                .center(bcx, cy).rect(SNAP_GAP, ch_len).extrude(HEIGHT))
        grip = (cq.Workplane("XY").workplane(offset=zc)
                .center(bcx, cy).rect(pitch + CRADLE_WALL + 0.01, GRIP_W).extrude(HEIGHT))
        tray = tray.cut(chan).cut(slot).cut(grip)

    # Full-height divider behind the cradle zone, and a wall between cradles and key pocket
    div = (cq.Workplane("XY").workplane(offset=FLOOR_T)
           .center(zone_x0 - DIV_T / 2, 0).rect(DIV_T, 2 * half_w(xf)).extrude(HEIGHT - FLOOR_T))
    side = (cq.Workplane("XY").workplane(offset=FLOOR_T)
            .center((zone_x0 + ixf) / 2, y_end + CRADLE_WALL / 2)
            .rect(zone_d + 0.02, CRADLE_WALL).extrude(HEIGHT - FLOOR_T))
    tray = tray.union(div.union(side).intersect(envelope))

    # U-shaped finger notch through the divider behind the cradles, lined up with the
    # grip notches, so the balm can be pinched out from the main bay
    nr = BACK_NOTCH_W / 2
    notch = (cq.Workplane("YZ").workplane(offset=zone_x0 - DIV_T - 1)
             .center(cy, zc + nr).circle(nr).extrude(DIV_T + 2)
             .union(cq.Workplane("XY").workplane(offset=zc + nr)
                    .center(zone_x0 - DIV_T / 2, cy).rect(DIV_T + 2, BACK_NOTCH_W).extrude(HEIGHT)))
    tray = tray.cut(notch)

    # Lift ridges: two half-pencil (half-hexagon) ridges on the back of the cradle divider,
    # either side of the finger notch, to hook a finger under and lift the tray.
    # Cut across the flats so the underside is a 60 deg slope plus a tiny bridge: no supports.
    r, h = RIDGE_D / 2, RIDGE_D / 2 * math.sqrt(3) / 2
    xw = zone_x0 - DIV_T                                 # back face of the divider
    zr = HEIGHT - h - RIDGE_TOP_GAP                      # ridge centre height
    prof = [(xw + 0.2, zr + h), (xw - r / 2, zr + h), (xw - r, zr),
            (xw - r / 2, zr - h), (xw + 0.2, zr - h)]
    y_wall = half_w(xw) - WALL_T
    for y1, y2 in ((cy - nr - RIDGE_GAP - RIDGE_L, cy - nr - RIDGE_GAP),
                   (cy + nr + RIDGE_GAP, cy + nr + RIDGE_GAP + RIDGE_L)):
        y1, y2 = max(y1, -y_wall), min(y2, y_wall)
        ridge = (cq.Workplane("XZ").workplane(offset=-y2)
                 .polyline(prof).close().extrude(y2 - y1))
        tray = tray.union(ridge)

    # Finger scoops: front one over the key pocket, back one centred
    iy_pocket_end = half_w(zone_x0) - WALL_T
    for sx, sy in ((xf, (y_end + CRADLE_WALL + iy_pocket_end) / 2), (xb, 0.0)):
        scoop = (cq.Workplane("YZ").workplane(offset=sx - 5)
                 .center(sy, HEIGHT).circle(12).extrude(10))
        tray = tray.cut(scoop)
    return tray


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    t = build()
    cq.exporters.export(t, os.path.join(here, "kona_organiser.stl"), tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(t, os.path.join(here, "kona_organiser.step"))
    bb = t.val().BoundingBox()
    print(f"size {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm, volume {t.val().Volume()/1000:.1f} cm3")
    print(f"width back {2*half_w(xb):.1f}, front {2*half_w(xf):.1f}; cradle top {cradle_top:.2f}")

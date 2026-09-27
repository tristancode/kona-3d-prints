"""
Parametric centre-console organiser tray for a 2025 Hyundai Kona.
Run:  python3 kona_organiser.py   -> writes kona_organiser.stl / .step next to this file.

Coordinates: X = along the car (front/back), Y = across the car, Z = up.
All dimensions in mm. Print flat, open side up, no supports.
"""
import math, os
import cadquery as cq

# ---- Console bin floor (read from the tape photos) ----
FLOOR_L = 190.0      # along the car, tape read ~19 cm across the grey floor insert
FLOOR_W = 130.0      # across the car, tape read ~13 cm (12 cm at the narrow end)
CLEARANCE = 3.0      # total gap removed from each dimension (1.5 mm per side)

# ---- Tray ----
TRAY_L = FLOOR_L - CLEARANCE
TRAY_W = FLOOR_W - CLEARANCE - 4.0   # extra 4 mm because the floor narrows to ~12 cm at one end
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
BALM_COUNT = 2       # cradles laid end to end along one long wall
CRADLE_WALL = 1.6
GRIP_W = 22.0        # finger notch in the middle of each cradle

# ---- Derived ----
ch_d = BALM_D + BALM_FIT
ch_r = ch_d / 2
ch_len = BALM_L + BALM_AXIAL
zc = FLOOR_T + ch_r                                     # channel axis height
cradle_top = zc + math.sqrt(ch_r**2 - (SNAP_GAP / 2) ** 2)
strip_w = ch_d + 2 * CRADLE_WALL                        # cradle strip width (Y)
cradle_len = ch_len + 2 * CRADLE_WALL                   # one cradle's length (X)

x0, y0 = -TRAY_L / 2, -TRAY_W / 2


def build():
    # Outer shell
    tray = (cq.Workplane("XY").rect(TRAY_L, TRAY_W).extrude(HEIGHT)
            .edges("|Z").fillet(CORNER_R))
    cavity = (cq.Workplane("XY").workplane(offset=FLOOR_T)
              .rect(TRAY_L - 2 * WALL_T, TRAY_W - 2 * WALL_T).extrude(HEIGHT)
              .edges("|Z").fillet(CORNER_R - WALL_T))
    tray = tray.cut(cavity)

    # Lip-balm cradles along the -Y wall, starting at the -X end
    iy0 = y0 + WALL_T                       # inner face of -Y wall
    cy = iy0 + strip_w / 2 - CRADLE_WALL / 2  # share the outer wall as one cradle side
    strip_w_eff = strip_w - CRADLE_WALL
    cx_start = x0 + WALL_T
    for i in range(BALM_COUNT):
        bx0 = cx_start + i * (cradle_len - CRADLE_WALL)
        bcx = bx0 + cradle_len / 2
        block = (cq.Workplane("XY").center(bcx, iy0 + strip_w_eff / 2)
                 .rect(cradle_len, strip_w_eff).extrude(cradle_top))
        tray = tray.union(block)
        # channel (cylinder along X) + slot to the top
        chan = (cq.Workplane("YZ").workplane(offset=bcx - ch_len / 2)
                .center(iy0 + ch_r, zc).circle(ch_r).extrude(ch_len))
        slot = (cq.Workplane("XY").workplane(offset=zc)
                .center(bcx, iy0 + ch_r).rect(ch_len, SNAP_GAP).extrude(HEIGHT))
        # finger notch: open the cradle walls down to the axis in the middle
        grip = (cq.Workplane("XY").workplane(offset=zc)
                .center(bcx, iy0 + strip_w_eff / 2).rect(GRIP_W, strip_w_eff + 0.01).extrude(HEIGHT))
        tray = tray.cut(chan).cut(slot).cut(grip)
    cradles_end = cx_start + BALM_COUNT * (cradle_len - CRADLE_WALL) + CRADLE_WALL

    inner_x1 = -x0 - WALL_T
    strip_y1 = iy0 + strip_w_eff
    # Long divider separating the cradle strip from the main area
    div = (cq.Workplane("XY").workplane(offset=FLOOR_T)
           .center((cradles_end - CRADLE_WALL + inner_x1) / 2, strip_y1 - DIV_T / 2)
           .rect(inner_x1 - (cradles_end - CRADLE_WALL), DIV_T).extrude(HEIGHT - FLOOR_T))
    tray = tray.union(div)
    # Short wall closing the pocket next to the cradles
    end = (cq.Workplane("XY").workplane(offset=FLOOR_T)
           .center(cradles_end - CRADLE_WALL / 2, iy0 + strip_w_eff / 2)
           .rect(CRADLE_WALL, strip_w_eff).extrude(HEIGHT - FLOOR_T))
    tray = tray.union(end)

    # Cross divider: phone/wallet bay (+X) and cards/misc bay (-X)
    bay_split = x0 + WALL_T + 70.0
    cross = (cq.Workplane("XY").workplane(offset=FLOOR_T)
             .center(bay_split, (strip_y1 + (-y0 - WALL_T)) / 2)
             .rect(DIV_T, (-y0 - WALL_T) - strip_y1).extrude(HEIGHT - FLOOR_T))
    tray = tray.union(cross)

    # Finger scoops in the two short walls so the tray lifts out easily
    for sx in (x0, -x0):
        scoop = (cq.Workplane("YZ").workplane(offset=sx - 5)
                 .center(TRAY_W * 0.15, HEIGHT).circle(12).extrude(10))
        tray = tray.cut(scoop)
    return tray


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    t = build()
    cq.exporters.export(t, os.path.join(here, "kona_organiser.stl"), tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(t, os.path.join(here, "kona_organiser.step"))
    bb = t.val().BoundingBox()
    print(f"size {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm, volume {t.val().Volume()/1000:.1f} cm3")
    print(f"cradle top {cradle_top:.2f}, axis {zc:.2f}")

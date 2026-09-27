"""
Parametric centre-console organiser tray for a 2025 Hyundai Kona.
Run:  python3 kona_organiser.py   -> writes kona_organiser.stl / .step next to this file.

Coordinates: X = along the long edge, Y = across it, Z = up. The cradle end (+X) is the front.
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
GRIP_W = 22.0
CORNER_OFFSET = 6.4  # gap between the -Y wall and the channel ends (clears the corner fillet)        # finger notch in the middle of each cradle

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
    envelope = (cq.Workplane("XY").rect(TRAY_L, TRAY_W).extrude(HEIGHT)
                .edges("|Z").fillet(CORNER_R))
    tray = envelope
    cavity = (cq.Workplane("XY").workplane(offset=FLOOR_T)
              .rect(TRAY_L - 2 * WALL_T, TRAY_W - 2 * WALL_T).extrude(HEIGHT)
              .edges("|Z").fillet(CORNER_R - WALL_T))
    tray = tray.cut(cavity)

    # Lip-balm cradles along the front short wall (built at -X, mirrored to +X at the end),
    # axis across the tray (Y), rows stacked front to back.
    ix0 = x0 + WALL_T
    iy0, iy1 = y0 + WALL_T, -y0 - WALL_T
    pitch = ch_d + CRADLE_WALL
    zone_d = BALM_COUNT * pitch            # depth of the cradle zone (X)
    cy = iy0 + CORNER_OFFSET + ch_len / 2  # keep channel ends clear of the corner fillet
    for i in range(BALM_COUNT):
        bcx = ix0 + i * pitch + ch_r
        block = (cq.Workplane("XY").center(ix0 + i * pitch + pitch / 2 - WALL_T / 2, cy)
                 .rect(pitch + WALL_T, ch_len + 2 * CRADLE_WALL).extrude(cradle_top))
        tray = tray.union(block.intersect(envelope))
        chan = (cq.Workplane("XZ").workplane(offset=-(cy - ch_len / 2))
                .center(bcx, zc).circle(ch_r).extrude(-ch_len))
        slot = (cq.Workplane("XY").workplane(offset=zc)
                .center(bcx, cy).rect(SNAP_GAP, ch_len).extrude(HEIGHT))
        grip = (cq.Workplane("XY").workplane(offset=zc)
                .center(bcx, cy).rect(pitch + CRADLE_WALL + 0.01, GRIP_W).extrude(HEIGHT))
        tray = tray.cut(chan).cut(slot).cut(grip)
    cradle_y1 = cy + ch_len / 2

    # Fill between the corner and the channel ends
    filler = (cq.Workplane("XY").center(ix0 + zone_d / 2 - WALL_T / 2, (iy0 + cy - ch_len / 2) / 2 - 1)
              .rect(zone_d + WALL_T, cy - ch_len / 2 - iy0 + 2).extrude(cradle_top))
    tray = tray.union(filler.intersect(envelope))

    # Full-height divider across the tray behind the cradle zone
    div = (cq.Workplane("XY").workplane(offset=FLOOR_T)
           .center(ix0 + zone_d + DIV_T / 2, 0).rect(DIV_T, iy1 - iy0 + 0.02).extrude(HEIGHT - FLOOR_T))
    # Wall between the cradles and the key/coin pocket beside them
    side = (cq.Workplane("XY").workplane(offset=FLOOR_T)
            .center(ix0 + zone_d / 2, cradle_y1 + CRADLE_WALL / 2)
            .rect(zone_d + 0.02, CRADLE_WALL).extrude(HEIGHT - FLOOR_T))
    tray = tray.union(div).union(side)

    # Finger scoops in the two short walls (the front one sits over the key pocket)
    scoop_y = (cradle_y1 + CRADLE_WALL + iy1) / 2
    for sx in (x0, -x0):
        scoop = (cq.Workplane("YZ").workplane(offset=sx - 5)
                 .center(scoop_y, HEIGHT).circle(12).extrude(10))
        tray = tray.cut(scoop)
    tray = tray.mirror("YZ")                # cradles end up at +X, matching the marked-up preview
    return tray


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    t = build()
    cq.exporters.export(t, os.path.join(here, "kona_organiser.stl"), tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(t, os.path.join(here, "kona_organiser.step"))
    bb = t.val().BoundingBox()
    print(f"size {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm, volume {t.val().Volume()/1000:.1f} cm3")
    print(f"cradle top {cradle_top:.2f}, axis {zc:.2f}")

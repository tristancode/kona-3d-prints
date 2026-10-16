"""
Parametric FRONT organiser for the 2025 Hyundai Kona centre console: the strip of floor
between the cupholders and the drive-mode panel.
Run:  python3 kona_front_organiser.py   -> writes kona_front_organiser.stl / .step / .3mf next to this file.

Coordinates (as seen in the user's photos, drive-mode panel at the top):
X = along the strip (+X is right, towards the key fob end), Y = across (+Y towards the
drive-mode panel), Z = up. All dimensions in mm. Print flat, open side up, no supports.

v2 (after the v1 test print): overall length = caliper 156.6 + 5 mm, one height throughout,
no finger well, lift nub on the key fob pocket wall.
v3 (after the v2 test print): narrow section 2 mm narrower, overall 2 mm shorter, lip balm
in an open half-cylinder trough with straight sides (no snap), moved towards the drive-mode
panel with open finger space beside it, key fob pocket floor tilted down towards the right end.
v4 (Charlimit's drawing on the v3 top view): both end faces taper so the tray is longer at the
top than at the floor (side view a trapezoid), the fob floor is flat again, and the lip balm
trough has the grip notch through both sides.
v5 (Charlimit's markup of the v4 top view): the right end is angled in plan (full length on the
panel side, RIGHT_END_SKEW shorter on the cupholder side), the lip balm trough moves to the
cupholder side so the finger space is against the car's panel, the wide section is cut back so
the strip beside the trough is gone (only the fob pocket is full width), end tapers 5 degrees.
Layout left to right: narrow section (sits in the 31 mm slot, small bin) -> lip balm trough
(starts in the narrow section) -> key fob pocket.
"""
import math, os
import cadquery as cq

# ---- Space ----
CALIPER_L = 156.6    # user's caliper reading along the strip (v1 test print)
OVERALL_L = CALIPER_L + 5.0 - 2.0   # v2 asked caliper + 5; v3 test print was ~2 mm too long
SLOT_W = 31.0        # narrow slot on the left, caliper (across)
SLOT_L = 39.8        # narrow slot on the left, caliper (along)
CLEAR_SLOT = 1.75    # gap per side of the narrow section in the slot (v2 at 0.75 was ~2 mm too wide)
CLEAR_END = 1.5
TONGUE_OFFSET = 0.0  # shift the narrow section across (+ towards the drive-mode panel)

# ---- Tray ----
BODY_W = 44.0        # wide section width (fitted in v1)
FLOOR_T = 1.0
WALL_T = 1.6
DIV_T = 1.2
CORNER_R = 3.0

# ---- Key fob pocket (fob ~55 x 33 mm) ----
POCKET_L = 64.0      # along the panel side; the cupholder side is RIGHT_END_SKEW shorter
POCKET_W = BODY_W - 2 * WALL_T   # 40.8 mm

# ---- Lip balm trough (Burt's Bees ~15.3 dia x 68 long), lying along X ----
BALM_D = 15.3
BALM_L = 68.0
BALM_FIT = 0.4
BALM_AXIAL = 0.6
CRADLE_WALL = 1.6    # trough end walls and its panel-side wall
GRIP_W = 22.0        # grip notch through both sides, in the middle

# ---- Ends ----
END_TAPER_LEFT_DEG = 5.0     # side view: end faces lean out, top longer than the floor
END_TAPER_RIGHT_DEG = 5.0
RIGHT_END_SKEW = 5.0         # plan view: right end is this much shorter on the cupholder side

# ---- Half-pencil lift nub on the inner face of the fob pocket's cupholder-side wall ----
RIDGE_D = 7.0        # across the corners -> protrudes 3.5 mm
RIDGE_L = 24.0
RIDGE_TOP_GAP = 1.0

# ---- Derived ----
ch_d = BALM_D + BALM_FIT
ch_r = ch_d / 2
ch_len = BALM_L + BALM_AXIAL
zc = FLOOR_T + ch_r
HEIGHT = 13.0                             # whole tray height (v2: as low as the balm allows)

TONGUE_W = SLOT_W - 2 * CLEAR_SLOT        # narrow width, now used for the whole balm section
TONGUE_L = SLOT_L - CLEAR_END
BODY_L = OVERALL_L - TONGUE_L
xl, xr = 0.0, BODY_L                      # xr = right end at the top, panel side
xn = xl - TONGUE_L                        # far left end
yb, yt = -BODY_W / 2, BODY_W / 2
ty1 = yt + TONGUE_OFFSET                  # narrow section flush with the drive-mode-panel side
ty0 = ty1 - TONGUE_W
cy = ty0 + WALL_T + ch_r                  # trough against the cupholder-side wall
y_trough1 = cy + ch_r + CRADLE_WALL       # panel-side face of the trough
FINGER_W = (ty1 - WALL_T) - y_trough1     # finger space between the trough and the panel side

# Interior stations along X (right to left)
x_pocket0 = xr - WALL_T - POCKET_L        # left edge of fob pocket
x_div = x_pocket0 - WALL_T                # wall between the pocket and the balm section
x_ch1 = x_div - CRADLE_WALL               # right end of balm channel
x_ch0 = x_ch1 - ch_len                    # left end of balm channel
x_cr0 = x_ch0 - CRADLE_WALL               # left face of the trough block
BIN_L = x_cr0 - (xn + WALL_T)             # small bin at the far left
WELL_L = BIN_L


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").workplane(offset=z0)
            .center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0))


def rbox(x0, x1, y0, y1, z0, z1, r):
    return box(x0, x1, y0, y1, z0, z1).edges("|Z").fillet(r)


def footprint(inset, z0, z1):
    r = max(CORNER_R - inset, 0.6)
    wide = rbox(x_div + inset, xr + 10, yb + inset, yt - inset, z0, z1, r)   # right end cut later
    narrow = rbox(xn + inset, x_div + CORNER_R + 2, ty0 + inset, ty1 - inset, z0, z1, r)
    return wide.union(narrow)


def end_line(y, z, side):
    """x of an end face at (y, z). Top edge sits at the nominal end; the floor edge is tapered in."""
    if side > 0:
        d = HEIGHT * math.tan(math.radians(END_TAPER_RIGHT_DEG))
        return xr - (yt - y) * RIGHT_END_SKEW / BODY_W - d * (HEIGHT - z) / HEIGHT
    d = HEIGHT * math.tan(math.radians(END_TAPER_LEFT_DEG))
    return xn + d * (HEIGHT - z) / HEIGHT


def end_solid(side, inset0, inset1):
    """Ruled solid between two copies of an end face, inset0..inset1 mm inward (x)."""
    ylo, yhi, z0, z1 = yb - 2, yt + 2, -0.02, HEIGHT + 0.02
    def ring(z):
        return [(end_line(ylo, z, side) - side * inset0, ylo), (end_line(ylo, z, side) - side * inset1, ylo),
                (end_line(yhi, z, side) - side * inset1, yhi), (end_line(yhi, z, side) - side * inset0, yhi)]
    return (cq.Workplane("XY").workplane(offset=z0).polyline(ring(z0)).close()
            .workplane(offset=z1 - z0).polyline(ring(z1)).close().loft(ruled=True))


def build():
    envelope = footprint(0, 0, HEIGHT)
    cavity = footprint(WALL_T, FLOOR_T, HEIGHT + 1)
    tray = envelope.cut(cavity)
    # Wall between the balm section and the fob pocket, across the narrow part
    tray = tray.union(box(x_div, x_pocket0, ty0 + WALL_T - 0.01, ty1 - WALL_T + 0.01, FLOOR_T - 0.01, HEIGHT))

    # Lip balm trough against the cupholder-side wall: half-cylinder bottom, straight sides,
    # closed ends. Open floor between it and the panel side for fingers.
    block = box(x_cr0, x_div + 0.01, ty0, y_trough1, FLOOR_T - 0.01, HEIGHT).intersect(envelope)
    tray = tray.union(block)
    chan = cq.Workplane("YZ").workplane(offset=x_ch0).center(cy, zc).circle(ch_r).extrude(ch_len)
    sides = box(x_ch0, x_ch1, cy - ch_r, cy + ch_r, zc, HEIGHT + 1)
    gx = (x_ch0 + x_ch1) / 2
    grip = box(gx - GRIP_W / 2, gx + GRIP_W / 2, ty0 - 1, y_trough1 + 0.01, zc, HEIGHT + 1)  # both sides
    tray = tray.cut(chan).cut(sides).cut(grip)
    # Close off the small bin across the finger space
    tray = tray.union(box(x_cr0, x_ch0, y_trough1 - 0.01, ty1 - WALL_T + 0.01, FLOOR_T - 0.01, HEIGHT))

    # Half-pencil (half-hexagon) lift nub on the inside of the fob pocket's cupholder-side wall.
    # Underside is a 60 deg slope, so no supports.
    r, h = RIDGE_D / 2, RIDGE_D / 2 * math.sqrt(3) / 2
    zr = HEIGHT - h - RIDGE_TOP_GAP
    yw = yb + WALL_T
    prof = [(yw - 0.2, zr + h), (yw + r / 2, zr + h), (yw + r, zr),
            (yw + r / 2, zr - h), (yw - 0.2, zr - h)]
    px = x_pocket0 + (POCKET_L - RIGHT_END_SKEW) / 2
    nub = (cq.Workplane("YZ").workplane(offset=px - RIDGE_L / 2)
           .polyline(prof).close().extrude(RIDGE_L))
    tray = tray.union(nub)

    # Ends: cut everything outside each (tapered, and on the right skewed) end face, then add
    # the end wall back along that face.
    for side in (1, -1):
        outside = end_solid(side, -20, 0)
        wall = end_solid(side, 0, WALL_T).intersect(envelope)
        tray = tray.cut(outside).union(wall)
    return tray


def export_3mf(shape, path):
    import zipfile, tempfile
    tmp = tempfile.mktemp(suffix=".stl")
    cq.exporters.export(shape, tmp, tolerance=0.02, angularTolerance=0.1)
    import numpy as np
    from stl import mesh as stlmesh  # numpy-stl
    m = stlmesh.Mesh.from_file(tmp)
    os.remove(tmp)
    tris = m.vectors.reshape(-1, 3)
    verts, idx = np.unique(np.round(tris, 5), axis=0, return_inverse=True)
    faces = idx.reshape(-1, 3)
    vx = "".join(f'<vertex x="{v[0]:.5f}" y="{v[1]:.5f}" z="{v[2]:.5f}"/>' for v in verts)
    tr = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in faces if len({a, b, c}) == 3)
    model = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             '<resources><object id="1" type="model" name="kona_front_organiser"><mesh>'
             f'<vertices>{vx}</vertices><triangles>{tr}</triangles></mesh></object></resources>'
             '<build><item objectid="1"/></build></model>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    t = build()
    cq.exporters.export(t, os.path.join(here, "kona_front_organiser.stl"), tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(t, os.path.join(here, "kona_front_organiser.step"))
    export_3mf(t, os.path.join(here, "kona_front_organiser.3mf"))
    bb = t.val().BoundingBox()
    print(f"size {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm, volume {t.val().Volume()/1000:.1f} cm3")
    print(f"narrow {xr - xn - (xr - x_div):.1f} x {TONGUE_W:.1f}, wide {xr - x_div:.1f} x {BODY_W:.1f}, height {HEIGHT}")
    print(f"fob pocket {POCKET_L} (panel side) / {POCKET_L - RIGHT_END_SKEW} (cupholder side) x {POCKET_W:.1f}, left bin {BIN_L:.1f}, finger space {FINGER_W:.1f}")
    print(f"channel x {x_ch0:.1f}..{x_ch1:.1f} (narrow section ends at x=0)")
    dl = HEIGHT * math.tan(math.radians(END_TAPER_LEFT_DEG)); dr = HEIGHT * math.tan(math.radians(END_TAPER_RIGHT_DEG))
    print(f"length at top {OVERALL_L:.1f}, at floor {OVERALL_L - dl - dr:.1f}")

"""
Parametric FRONT organiser for the 2025 Hyundai Kona centre console: the strip of floor
between the cupholders and the drive-mode panel.
Run:  python3 kona_front_organiser.py   -> writes kona_front_organiser.stl / .step / .3mf next to this file.

Coordinates (as seen in the user's photos, drive-mode panel at the top):
X = along the strip (+X is right, towards the key fob end), Y = across (+Y towards the
drive-mode panel), Z = up. All dimensions in mm. Print flat, open side up, no supports.

Layout left to right: locating tongue (drops into the narrow 31 x 39.8 mm slot) ->
finger well with half-pencil lift ridge -> snap-in lip balm cradle -> key fob pocket.
"""
import math, os
import cadquery as cq

# ---- Space (photos) ----
FLOOR_L = 150.0      # main floor length, tape photo (pocket mouth to far end) ~15 cm
SLOT_W = 31.0        # narrow slot on the left, caliper (across)
SLOT_L = 39.8        # narrow slot on the left, caliper (along)
CLEAR_END = 1.5      # gap per end of the main body
CLEAR_SLOT = 0.75    # gap per side of the tongue in the narrow slot (snug: this is what locks it)
TONGUE_OFFSET = 0.0  # shift the tongue across (+ towards the drive-mode panel) if the slot isn't flush

# ---- Tray ----
BODY_W = 44.0        # main body width (fits the 40 mm fob pocket + walls); assumed, check the strip
HEIGHT = 20.0        # wall height (low profile, same as the rear tray)
TONGUE_H = 10.0      # tongue height
FLOOR_T = 1.0
WALL_T = 1.6
DIV_T = 1.2
CORNER_R = 3.0

# ---- Key fob pocket (fob ~55 x 33 mm) ----
POCKET_L = 58.0      # along X
POCKET_W = BODY_W - 2 * WALL_T   # 40.8 mm, straight sides

# ---- Lip balm cradle (Burt's Bees ~15.3 dia x 68 long), lying along X ----
BALM_D = 15.3
BALM_L = 68.0
BALM_FIT = 0.4
BALM_AXIAL = 0.6
SNAP_GAP = 13.8
CRADLE_WALL = 1.6
GRIP_W = 22.0

# ---- Half-pencil lift ridge on the cradle's left end wall, facing the finger well ----
RIDGE_D = 7.0        # across the corners -> protrudes 3.5 mm
RIDGE_L = 24.0
RIDGE_TOP_GAP = 1.5

# ---- Derived ----
ch_d = BALM_D + BALM_FIT
ch_r = ch_d / 2
ch_len = BALM_L + BALM_AXIAL
zc = FLOOR_T + ch_r
cradle_top = zc + math.sqrt(ch_r**2 - (SNAP_GAP / 2) ** 2)

BODY_L = FLOOR_L - 2 * CLEAR_END
xl, xr = 0.0, BODY_L                      # main body left / right outer faces
TONGUE_W = SLOT_W - 2 * CLEAR_SLOT
TONGUE_L = SLOT_L - CLEAR_END
yb, yt = -BODY_W / 2, BODY_W / 2
ty1 = yt + TONGUE_OFFSET                  # tongue flush with the drive-mode-panel side
ty0 = ty1 - TONGUE_W

# Interior stations along X (right to left)
x_pocket0 = xr - WALL_T - POCKET_L        # left edge of fob pocket
x_div = x_pocket0 - DIV_T                 # divider between pocket and cradle
x_ch1 = x_div - CRADLE_WALL               # right end of balm channel
x_ch0 = x_ch1 - ch_len                    # left end of balm channel
x_cr0 = x_ch0 - CRADLE_WALL               # left face of cradle block (ridge sits here)
x_well0 = xl + WALL_T                     # finger well spans x_well0..x_cr0
WELL_L = x_cr0 - x_well0


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY").workplane(offset=z0)
            .center((x0 + x1) / 2, (y0 + y1) / 2).rect(x1 - x0, y1 - y0).extrude(z1 - z0))


def rbox(x0, x1, y0, y1, z0, z1, r):
    return box(x0, x1, y0, y1, z0, z1).edges("|Z").fillet(r)


def build():
    # Main body shell
    body = rbox(xl, xr, yb, yt, 0, HEIGHT, CORNER_R)
    body = body.cut(rbox(xl + WALL_T, xr - WALL_T, yb + WALL_T, yt - WALL_T, FLOOR_T, HEIGHT + 1,
                         CORNER_R - WALL_T + 0.4))

    # Locating tongue: hollow box off the left end, overlaps the end wall so it fuses
    tongue = rbox(xl - TONGUE_L, xl + WALL_T, ty0, ty1, 0, TONGUE_H, 2.0)
    tongue = tongue.cut(rbox(xl - TONGUE_L + WALL_T, xl - 0.01, ty0 + WALL_T, ty1 - WALL_T,
                             FLOOR_T, TONGUE_H + 1, 1.0))
    tray = body.union(tongue)

    # Divider between the cradle and the fob pocket (full height)
    tray = tray.union(box(x_div, x_pocket0, yb + WALL_T - 0.01, yt - WALL_T + 0.01, FLOOR_T - 0.01, HEIGHT))

    # Lip balm cradle block with a snap channel along X, centred across the body
    block = box(x_cr0, x_div + 0.01, yb + WALL_T - 0.01, yt - WALL_T + 0.01, FLOOR_T - 0.01, cradle_top)
    tray = tray.union(block)
    chan = (cq.Workplane("YZ").workplane(offset=x_ch0).center(0, zc).circle(ch_r).extrude(ch_len))
    slot = box(x_ch0, x_ch1, -SNAP_GAP / 2, SNAP_GAP / 2, zc, HEIGHT + 1)
    gx = (x_ch0 + x_ch1) / 2
    grip = box(gx - GRIP_W / 2, gx + GRIP_W / 2, yb + WALL_T, yt - WALL_T, zc, HEIGHT + 1)
    tray = tray.cut(chan).cut(slot).cut(grip)

    # Cradle end wall rises to full height on the well side so the ridge has something to sit on
    tray = tray.union(box(x_cr0, x_ch0 + 0.01, yb + WALL_T - 0.01, yt - WALL_T + 0.01, FLOOR_T, HEIGHT))

    # Half-pencil (half-hexagon) lift ridge on the left face of the cradle, facing the finger well.
    # Underside is a 60 deg slope, so no supports.
    r, h = RIDGE_D / 2, RIDGE_D / 2 * math.sqrt(3) / 2
    zr = HEIGHT - h - RIDGE_TOP_GAP
    xw = x_cr0
    prof = [(xw + 0.2, zr + h), (xw - r / 2, zr + h), (xw - r, zr),
            (xw - r / 2, zr - h), (xw + 0.2, zr - h)]
    ridge = (cq.Workplane("XZ").workplane(offset=-RIDGE_L / 2)
             .polyline(prof).close().extrude(RIDGE_L))
    tray = tray.union(ridge)

    # Finger scoop over the fob pocket on the outer long side (away from the panel)
    scoop = (cq.Workplane("XZ").workplane(offset=-(yb + 5))
             .center(x_pocket0 + POCKET_L / 2, HEIGHT).circle(12).extrude(10))
    tray = tray.cut(scoop)
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
    print(f"body {BODY_L:.1f} x {BODY_W:.1f}, tongue {TONGUE_L:.1f} x {TONGUE_W:.1f} x {TONGUE_H}")
    print(f"fob pocket {POCKET_L} x {POCKET_W:.1f}, finger well {WELL_L:.1f}, cradle top {cradle_top:.2f}")

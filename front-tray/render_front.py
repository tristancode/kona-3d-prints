import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
from stl import mesh
D = __import__("os").path.dirname(__import__("os").path.abspath(__file__)) + "/"
sys.path.insert(0, D)
import kona_front_organiser as k

m = mesh.Mesh.from_file(D + "kona_front_organiser.stl")
fig = plt.figure(figsize=(14, 5), dpi=130)
for i, (el, az) in enumerate(((35, -60), (60, 120))):
    ax = fig.add_subplot(1, 2, i + 1, projection="3d")
    v = m.vectors
    n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-9
    light = np.array([0.4, -0.5, 0.8]); light /= np.linalg.norm(light)
    sh = 0.35 + 0.65 * np.clip(n @ light, 0, 1)
    cols = np.c_[0.25 + 0.45 * sh, 0.45 + 0.4 * sh, 0.7 + 0.3 * sh, np.ones_like(sh)]
    cols = np.clip(cols, 0, 1)
    ax.add_collection3d(Poly3DCollection(v, facecolors=cols, edgecolor="none"))
    mn, mx = v.reshape(-1, 3).min(0), v.reshape(-1, 3).max(0)
    c = (mn + mx) / 2; r = (mx - mn).max() / 2
    ax.set_xlim(mn[0], mx[0]); ax.set_ylim(mn[1], mx[1]); ax.set_zlim(mn[2], mx[2]); ax.set_box_aspect(mx - mn, zoom=0.95)
    ax.view_init(el, az); ax.set_axis_off()
fig.suptitle("Kona front console organiser (tongue left, lip balm middle, key fob right)")
plt.tight_layout(); plt.savefig(D + "kona_front_organiser_preview.png"); plt.close()

# ---- Dimensioned top view ----
fig, ax = plt.subplots(figsize=(15, 6.5), dpi=130)
def rect(x0, x1, y0, y1, **kw):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **kw))
def dim(p0, p1, off, text, vertical=False):
    (x0, y0), (x1, y1) = p0, p1
    if vertical:
        xo = x0 + off
        ax.plot([x0, xo], [y0, y0], "k-", lw=0.5); ax.plot([x1, xo], [y1, y1], "k-", lw=0.5)
        ax.annotate("", (xo, y0), (xo, y1), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text(xo + (1.5 if off > 0 else -1.5), (y0 + y1) / 2, text, rotation=90, va="center",
                ha="left" if off > 0 else "right", fontsize=8.5)
    else:
        yo = y0 + off
        ax.plot([x0, x0], [y0, yo], "k-", lw=0.5); ax.plot([x1, x1], [y1, yo], "k-", lw=0.5)
        ax.annotate("", (x0, yo), (x1, yo), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text((x0 + x1) / 2, yo + (1.2 if off > 0 else -1.2), text, ha="center",
                va="bottom" if off > 0 else "top", fontsize=8.5)
body = dict(fc="#d6e4f2", ec="k", lw=1.2)
ax.add_patch(FancyBboxPatch((k.xl, k.yb), k.BODY_L, k.BODY_W, boxstyle=f"round,pad=0,rounding_size={k.CORNER_R}", **body))
ax.add_patch(FancyBboxPatch((k.xl - k.TONGUE_L, k.ty0), k.TONGUE_L + k.WALL_T, k.TONGUE_W, boxstyle="round,pad=0,rounding_size=2", fc="#f4d9a8", ec="k", lw=1.2))
rect(k.xl - k.TONGUE_L + k.WALL_T, k.xl, k.ty0 + k.WALL_T, k.ty1 - k.WALL_T, fc="white", ec="k", lw=0.6)
iw0, iw1 = k.yb + k.WALL_T, k.yt - k.WALL_T
rect(k.x_pocket0, k.xr - k.WALL_T, iw0, iw1, fc="white", ec="k", lw=0.8)       # fob pocket
rect(k.x_well0, k.x_cr0, iw0, iw1, fc="white", ec="k", lw=0.8)                 # finger well
rect(k.x_cr0, k.x_div, iw0, iw1, fc="#b9cfe6", ec="k", lw=0.8)                 # cradle block
rect(k.x_ch0, k.x_ch1, -k.ch_r, k.ch_r, fc="white", ec="k", lw=0.6, ls="--")    # channel
rect(k.x_ch0, k.x_ch1, -k.SNAP_GAP / 2, k.SNAP_GAP / 2, fc="none", ec="k", lw=0.6)
gx = (k.x_ch0 + k.x_ch1) / 2
rect(gx - k.GRIP_W / 2, gx + k.GRIP_W / 2, iw0, iw1, fc="#eef4fa", ec="k", lw=0.5, ls=":")
r = k.RIDGE_D / 2
rect(k.x_cr0 - r, k.x_cr0, -k.RIDGE_L / 2, k.RIDGE_L / 2, fc="#7a9cc6", ec="k", lw=0.6)
ax.text((k.x_pocket0 + k.xr) / 2, 0, "KEY FOB\n58 x 40.8\n(fob 55 x 33)", ha="center", va="center", fontsize=9)
ax.text(gx, -k.ch_r - 3.5, f"LIP BALM snap cradle  (13.8 opening, closed ends)", ha="center", va="top", fontsize=8)
ax.text((k.xl - k.TONGUE_L + k.xl) / 2, (k.ty0 + k.ty1) / 2, "LOCATING\nTONGUE\n10 tall", ha="center", va="center", fontsize=8)
ax.text((k.x_well0 + k.x_cr0) / 2 - 1.5, k.yb - 2, "finger well\n+ lift ridge", ha="center", va="top", fontsize=7.5)
# dims
dim((k.xl - k.TONGUE_L, k.yb), (k.xr, k.yb), -16, f"overall {k.BODY_L + k.TONGUE_L:.1f}")
dim((k.xl, k.yb), (k.xr, k.yb), -9, f"main body {k.BODY_L:.1f}  (floor 150)")
dim((k.xl - k.TONGUE_L, k.yt), (k.xl, k.yt), 6, f"tongue {k.TONGUE_L:.1f}  (slot 39.8)")
dim((k.x_well0, k.yt), (k.x_cr0, k.yt), 6, f"{k.WELL_L:.1f}")
dim((k.x_cr0, k.yt), (k.x_div, k.yt), 13, f"cradle {k.x_div - k.x_cr0:.1f}")
dim((k.x_ch0, k.yt), (k.x_ch1, k.yt), 6, f"channel {k.ch_len:.1f}")
dim((k.x_pocket0, k.yt), (k.xr - k.WALL_T, k.yt), 6, f"pocket {k.POCKET_L:.1f}")
dim((k.xr, k.yb), (k.xr, k.yt), 7, f"width {k.BODY_W:.1f}", vertical=True)
dim((k.xl - k.TONGUE_L, k.ty0), (k.xl - k.TONGUE_L, k.ty1), -6, f"tongue {k.TONGUE_W:.1f} (slot 31.0)", vertical=True)
dim((k.x_pocket0, iw0), (k.x_pocket0, iw1), 5, f"{k.POCKET_W:.1f}", vertical=True)
ax.text(k.xr / 2, k.yt + 22, "TOP VIEW  (drive-mode panel side at top, as in the photos)   all mm, height 20, walls 1.6",
        ha="center", fontsize=10, weight="bold")
ax.set_aspect("equal"); ax.set_xlim(k.xl - k.TONGUE_L - 22, k.xr + 22); ax.set_ylim(k.yb - 26, k.yt + 27)
ax.axis("off"); plt.tight_layout(); plt.savefig(D + "kona_front_organiser_dimensions.png"); plt.close()

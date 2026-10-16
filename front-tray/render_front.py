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
fig.suptitle(f"Kona front console organiser v3 ({k.OVERALL_L:.1f} long, {k.HEIGHT:g} tall)")
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
ax.add_patch(FancyBboxPatch((k.xn, k.ty0), k.TONGUE_L + 6, k.TONGUE_W, boxstyle="round,pad=0,rounding_size=3", **body))
iw0, iw1 = k.yb + k.WALL_T, k.yt - k.WALL_T
nw0, nw1 = k.ty0 + k.WALL_T, k.ty1 - k.WALL_T
rect(k.x_pocket0, k.xr - k.WALL_T, iw0, iw1, fc="white", ec="k", lw=0.8)       # fob pocket
rect(k.xl + k.WALL_T, k.x_div, iw0, iw1, fc="white", ec="k", lw=0.8)           # finger space beside the trough
rect(k.x_ch0, k.xl + k.WALL_T + 0.5, nw0, k.y_trough0, fc="white", ec="none")   # finger space in the narrow part
rect(k.x_cr0, k.x_div, k.y_trough0, iw1, fc="#b9cfe6", ec="k", lw=0.8)         # trough block
rect(k.x_cr0, k.x_ch0, nw0, k.y_trough0, fc="#b9cfe6", ec="k", lw=0.8)         # bin wall
rect(k.xn + k.WALL_T, k.x_cr0, nw0, nw1, fc="white", ec="k", lw=0.8)           # left bin
rect(k.x_ch0, k.x_ch1, k.cy - k.ch_r, k.cy + k.ch_r, fc="white", ec="k", lw=0.6)
gx = (k.x_ch0 + k.x_ch1) / 2
rect(gx - k.GRIP_W / 2, gx + k.GRIP_W / 2, k.y_trough0, k.cy - k.ch_r, fc="#eef4fa", ec="k", lw=0.5, ls=":")
r = k.RIDGE_D / 2
px = k.x_pocket0 + k.POCKET_L / 2
rect(px - k.RIDGE_L / 2, px + k.RIDGE_L / 2, iw0, iw0 + r, fc="#7a9cc6", ec="k", lw=0.6)
ax.text(px, 3, f"KEY FOB\n58 x 40.8\n(fob 55 x 33)\nfloor tilts {k.FOB_TILT_DEG:g}° down to the right", ha="center", va="center", fontsize=9)
ax.text(px, iw0 + r + 1, "lift nub", ha="center", va="bottom", fontsize=7.5)
ax.text(gx, k.cy, f"LIP BALM trough {k.ch_d:.1f} wide, straight sides, closed ends", ha="center", va="center", fontsize=8)
ax.text(gx, (iw0 + k.y_trough0) / 2, f"finger space {k.y_trough0 - iw0:.1f}", ha="center", va="center", fontsize=8)
dim((gx + 25, iw0), (gx + 25, k.y_trough0), 3, f"{k.y_trough0 - iw0:.1f}", vertical=True)
ax.text((k.xn + k.x_cr0) / 2, (k.ty0 + k.ty1) / 2, "small\nbin", ha="center", va="center", fontsize=8)
dim((k.xn, k.yb), (k.xr, k.yb), -12, f"overall {k.OVERALL_L:.1f}  (caliper 156.6 + 5 - 2)")
dim((k.xl, k.yb), (k.xr, k.yb), -5, f"wide section {k.BODY_L:.1f}")
dim((k.xn, k.yt), (k.xl, k.yt), 13, f"narrow section {k.TONGUE_L:.1f}  (slot 39.8)")
dim((k.xn + k.WALL_T, k.yt), (k.x_cr0, k.yt), 6, f"bin {k.BIN_L:.1f}")
dim((k.x_ch0, k.yt), (k.x_ch1, k.yt), 6, f"channel {k.ch_len:.1f}")
dim((k.x_pocket0, k.yt), (k.xr - k.WALL_T, k.yt), 6, f"pocket {k.POCKET_L:.1f}")
dim((k.xr, k.yb), (k.xr, k.yt), 7, f"width {k.BODY_W:.1f}", vertical=True)
dim((k.xn, k.ty0), (k.xn, k.ty1), -6, f"{k.TONGUE_W:.1f} (slot 31.0, v2 was 29.5)", vertical=True)
dim((k.x_pocket0 + 4, iw0), (k.x_pocket0 + 4, iw1), 5, f"{k.POCKET_W:.1f}", vertical=True)
ax.text((k.xn + k.xr) / 2, k.yt + 24, f"TOP VIEW v3  (drive-mode panel side at top)   all mm, height {k.HEIGHT:g} throughout, walls 1.6",
        ha="center", fontsize=10, weight="bold")
ax.set_aspect("equal"); ax.set_xlim(k.xn - 22, k.xr + 22); ax.set_ylim(k.yb - 22, k.yt + 29)
ax.axis("off"); plt.tight_layout(); plt.savefig(D + "kona_front_organiser_dimensions.png"); plt.close()

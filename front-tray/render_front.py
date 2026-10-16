import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
from stl import mesh
D = __import__("os").path.dirname(__import__("os").path.abspath(__file__)) + "/"
sys.path.insert(0, D)
import kona_front_organiser as k
import math
dl = k.HEIGHT * math.tan(math.radians(k.END_TAPER_LEFT_DEG)); dr = k.HEIGHT * math.tan(math.radians(k.END_TAPER_RIGHT_DEG))

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
fig.suptitle(f"Kona front console organiser v5 ({k.OVERALL_L:.1f} long, {k.HEIGHT:g} tall)")
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
from matplotlib.patches import Polygon
W = k.WALL_T
sk = k.RIGHT_END_SKEW
xr_b = k.xr - sk                                   # right end, cupholder side (top edge)
outer = [(k.xn, k.ty0), (k.x_div, k.ty0), (k.x_div, k.yb), (xr_b, k.yb), (k.xr, k.yt), (k.xn, k.yt)]
ax.add_patch(Polygon(outer, closed=True, fc="#d6e4f2", ec="k", lw=1.2))
iy0, iy1 = k.yb + W, k.yt - W
ny0, ny1 = k.ty0 + W, k.ty1 - W
# fob pocket (right wall follows the skew)
xi = lambda y: k.xr - W - (k.yt - y) * sk / k.BODY_W
ax.add_patch(Polygon([(k.x_pocket0, iy0), (xi(iy0), iy0), (xi(iy1), iy1), (k.x_pocket0, iy1)], closed=True, fc="white", ec="k", lw=0.8))
rect(k.xn + W, k.x_cr0, ny0, ny1, fc="white", ec="k", lw=0.8)                  # small bin
rect(k.x_cr0, k.x_div, k.ty0, k.y_trough1, fc="#b9cfe6", ec="k", lw=0.8)       # trough block
rect(k.x_cr0, k.x_ch0, k.y_trough1, ny1, fc="#b9cfe6", ec="k", lw=0.8)         # bin wall
rect(k.x_ch0, k.x_div, k.y_trough1, ny1, fc="white", ec="k", lw=0.8)           # finger space
rect(k.x_ch0, k.x_ch1, k.cy - k.ch_r, k.cy + k.ch_r, fc="white", ec="k", lw=0.6)
gx = (k.x_ch0 + k.x_ch1) / 2
rect(gx - k.GRIP_W / 2, gx + k.GRIP_W / 2, k.ty0, k.cy - k.ch_r, fc="#eef4fa", ec="k", lw=0.5, ls=":")
rect(gx - k.GRIP_W / 2, gx + k.GRIP_W / 2, k.cy + k.ch_r, k.y_trough1, fc="#eef4fa", ec="k", lw=0.5, ls=":")
ax.text(gx, k.ty0 - 1, f"grip notch {k.GRIP_W:g} both sides", ha="center", va="top", fontsize=7.5)
r_ = k.RIDGE_D / 2
px = k.x_pocket0 + (k.POCKET_L - sk) / 2
rect(px - k.RIDGE_L / 2, px + k.RIDGE_L / 2, iy0, iy0 + r_, fc="#7a9cc6", ec="k", lw=0.6)
ax.text(px, iy0 + r_ + 1, "lift nub", ha="center", va="bottom", fontsize=7.5)
ax.text(px, 3, "KEY FOB\n(fob 55 x 33)", ha="center", va="center", fontsize=9)
ax.text(gx, k.cy, f"LIP BALM trough {k.ch_d:.1f} wide, straight sides, closed ends", ha="center", va="center", fontsize=8)
ax.text(gx, (k.y_trough1 + ny1) / 2, f"finger space {k.FINGER_W:.1f}", ha="center", va="center", fontsize=7.5)
ax.text((k.xn + k.x_cr0) / 2, (k.ty0 + k.ty1) / 2, "small\nbin", ha="center", va="center", fontsize=8)
# dims
dim((k.xn, k.yt), (k.xr, k.yt), 20, f"overall {k.OVERALL_L:.1f} at the top (panel side), {k.OVERALL_L - dl - dr:.1f} at the floor")
dim((k.xn + W, k.yt), (k.x_cr0, k.yt), 6, f"bin {k.BIN_L:.1f}")
dim((k.x_ch0, k.yt), (k.x_ch1, k.yt), 6, f"channel {k.ch_len:.1f}")
dim((k.x_pocket0, k.yt), (k.xr - W, k.yt), 6, f"pocket {k.POCKET_L:.1f}")
dim((k.xn, k.ty0), (k.x_div, k.ty0), -12, f"narrow section {k.x_div - k.xn:.1f}")
dim((k.x_div, k.yb), (xr_b, k.yb), -6, f"{xr_b - k.x_div:.1f} (cupholder side)")
dim((k.x_pocket0, iy0), (xi(iy0), iy0), 8, f"pocket {xi(iy0) - k.x_pocket0:.1f}")
dim((k.xr + 2, k.yb), (k.xr + 2, k.yt), 7, f"width {k.BODY_W:.1f}", vertical=True)
dim((k.xn, k.ty0), (k.xn, k.ty1), -6, f"{k.TONGUE_W:.1f} (slot 31.0)", vertical=True)
dim((k.x_pocket0 + 4, iy0), (k.x_pocket0 + 4, iy1), 5, f"{k.POCKET_W:.1f}", vertical=True)
ax.text(k.xr + 3, k.yb + 3, f"right end\nangled {sk:g} mm\n({math.degrees(math.atan(sk / k.BODY_W)):.1f}°)", ha="left", va="bottom", fontsize=7.5)
ax.text((k.xn + k.xr) / 2, k.yt + 33, f"TOP VIEW v5  (drive-mode panel side at top)   all mm, height {k.HEIGHT:g} throughout, walls 1.6",
        ha="center", fontsize=10, weight="bold")
# Side view (panel side) showing the tapered ends
ys = k.yb - 34
pts = [(k.xn + dl, ys), (k.xr - dr, ys), (k.xr, ys + k.HEIGHT), (k.xn, ys + k.HEIGHT)]
ax.add_patch(Polygon(pts, closed=True, fc="#d6e4f2", ec="k", lw=1.2))
ax.text((k.xn + k.xr) / 2, ys + k.HEIGHT / 2, f"SIDE VIEW (panel side)  height {k.HEIGHT:g}", ha="center", va="center", fontsize=8.5)
ax.text(k.xn - 2, ys + 2, f"{k.END_TAPER_LEFT_DEG:g}° taper\n{dl:.1f} mm shorter", ha="right", va="center", fontsize=7.5)
ax.text(k.xr + 2, ys + 2, f"{k.END_TAPER_RIGHT_DEG:g}° taper\n{dr:.1f} mm shorter", ha="left", va="center", fontsize=7.5)
dim((k.xn + dl, ys), (k.xr - dr, ys), -4, f"floor {k.OVERALL_L - dl - dr:.1f}")
ax.set_aspect("equal"); ax.set_xlim(k.xn - 22, k.xr + 22); ax.set_ylim(k.yb - 46, k.yt + 37)
ax.axis("off"); plt.tight_layout(); plt.savefig(D + "kona_front_organiser_dimensions.png"); plt.close()
